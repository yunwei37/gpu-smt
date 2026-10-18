// Untrusted phase-I support search. Every hint is repaired exactly on CPU
// and checked by Lean. One block owns each LP; cancellation is per model.
#include <cuda_runtime.h>
#include <math_constants.h>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <atomic>
#include <mutex>
struct Model {int m,n,stride;double* t;int* basis;volatile int* ctl;double* out;unsigned long long* ticks;};
struct Owned {Model gpu{};std::vector<double> host_table,scales,row_scales,host_out;std::vector<int> host_basis;int host_ctl[3]{};unsigned long long host_ticks[2]{};cudaStream_t prepare{},io{};cudaEvent_t ready{};std::mutex mutex;bool unscaled=false,dual_unscaled=false;};
struct Batch {Model* models;cudaEvent_t done;cudaStream_t stream;};
static thread_local std::string error_text;
static bool ok(cudaError_t e){if(e==cudaSuccess)return true;error_text=cudaGetErrorString(e);return false;}
extern "C" const char* simplex_error(){return error_text.c_str();}
__global__ void phase_one(Model* models){
 Model a=models[blockIdx.x];int tid=threadIdx.x;
 extern __shared__ double pivot_column[];
 __shared__ int enter,leave,finish,iterations;
 __shared__ double pivot;
 if(!tid){finish=0;iterations=0;asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a.ticks[0]));}__syncthreads();
 const int cols=a.stride-1;double* objective=a.t+a.m*a.stride;
 for(;;){
  if(!tid){
   if(a.ctl[0])finish=3;
   if(!finish){
    double scale=1.;for(int j=0;j<cols;j++)scale=fmax(scale,fabs(objective[j]));
    enter=-1;
    // Scaled Dantzig pricing; lowest-index ties. Numerical hints only.
    if(fabs(objective[cols])<=1e-8)finish=1;
    else{
     double best=-1e-10*scale;
     for(int j=0;j<cols;j++)if(objective[j]<best){enter=j;best=objective[j];}
     if(enter<0)finish=2;
     else{
      leave=-1;double ratio=CUDART_INF;int tie=0x7fffffff;
      for(int i=0;i<a.m;i++){
       double x=a.t[i*a.stride+enter],b=a.t[i*a.stride+cols];
       if(!isfinite(x)||!isfinite(b)||b < -1e-7){finish=4;break;}
       if(x>1e-12){
        double r=fmax(0.,b)/x;
        if(leave<0||r<ratio-1e-12*(1.+fabs(ratio))||
          (fabs(r-ratio)<=1e-12*(1.+fabs(ratio))&&a.basis[i]<tie)){
         ratio=r;leave=i;tie=a.basis[i];
        }
       }
      }
      if(!finish&&leave<0)finish=4;
      if(!finish)pivot=a.t[leave*a.stride+enter];
     }
    }
   }
  }
  __syncthreads();if(finish)break;
  for(int j=tid;j<a.stride;j+=blockDim.x)a.t[leave*a.stride+j]/=pivot;
  __syncthreads();
  for(int i=tid;i<=a.m;i+=blockDim.x)pivot_column[i]=a.t[i*a.stride+enter];
  __syncthreads();
  for(int k=tid;k<(a.m+1)*a.stride;k+=blockDim.x){
   int row=k/a.stride,j=k%a.stride;
   if(row!=leave)a.t[k]-=pivot_column[row]*a.t[leave*a.stride+j];
  }
  __syncthreads();
  if(!tid){a.basis[leave]=enter;++iterations;a.ctl[2]=iterations;}
  __syncthreads();
 }
 if(finish==1){
  for(int j=tid;j<a.n;j+=blockDim.x)a.out[j]=0.;
  __syncthreads();
  for(int i=tid;i<a.m;i+=blockDim.x)if(a.basis[i]<a.n)
   a.out[a.basis[i]]=a.t[i*a.stride+cols];
 }
 if(finish==2)for(int i=tid;i<a.m;i+=blockDim.x)a.out[a.n+i]=objective[a.n+i]-1.;
 __syncthreads();
 if(!tid){asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a.ticks[1]));__threadfence_system();a.ctl[1]=finish;}
}

static void destroy(Owned* a){
 if(!a)return;
 if(a->prepare){
  if(a->gpu.t)cudaFreeAsync(a->gpu.t,a->prepare);
  if(a->gpu.basis)cudaFreeAsync(a->gpu.basis,a->prepare);
  if(a->gpu.ctl)cudaFreeAsync(const_cast<int*>(a->gpu.ctl),a->prepare);
  if(a->gpu.out)cudaFreeAsync(a->gpu.out,a->prepare);
  if(a->gpu.ticks)cudaFreeAsync(a->gpu.ticks,a->prepare);
  cudaStreamSynchronize(a->prepare);
 }
 if(a->ready)cudaEventDestroy(a->ready);
 if(a->io)cudaStreamDestroy(a->io);if(a->prepare)cudaStreamDestroy(a->prepare);delete a;
}
extern "C" void* simplex_model(int m,int n,const int* offsets,const int* indices,const double* values,const double* rhs){
 if(m<=0||n<=0){error_text="empty model";return nullptr;}
 auto a=new Owned{};a->gpu.m=m;a->gpu.n=n;a->gpu.stride=n+m+1;
 a->host_table.resize(static_cast<size_t>(m+1)*a->gpu.stride,0.);
 auto& t=a->host_table;a->host_basis.resize(m);auto& basis=a->host_basis;
 a->host_out.resize(n+m);a->row_scales.resize(m,1.);int last=n+m;
 for(int i=0;i<m;i++){
  double sign=rhs[i]<0?-1.:1.;a->row_scales[i]=sign;
  for(int k=offsets[i];k<offsets[i+1];k++){
   if(indices[k]<0||indices[k]>=n||!std::isfinite(values[k])){
    error_text="invalid coefficient";destroy(a);return nullptr;
   }
   t[i*a->gpu.stride+indices[k]]+=sign*values[k];
  }
  t[i*a->gpu.stride+n+i]=1.;t[i*a->gpu.stride+last]=fabs(rhs[i]);basis[i]=n+i;
 }
 for(int i=0;i<m;i++){
  double scale=std::fabs(t[i*a->gpu.stride+last]);
  for(int j=0;j<n;j++)scale=std::max(scale,std::fabs(t[i*a->gpu.stride+j]));
  if(scale>0.){
   a->row_scales[i]/=scale;
   for(int j=0;j<n;j++)t[i*a->gpu.stride+j]/=scale;
   t[i*a->gpu.stride+last]/=scale;
  }
 }
 a->scales.resize(n,1.);
 for(int j=0;j<n;j++){
  double largest=0.;for(int i=0;i<m;i++)largest=std::max(largest,std::fabs(t[i*a->gpu.stride+j]));
  if(largest>0.)a->scales[j]=1./largest;
  for(int i=0;i<m;i++)t[i*a->gpu.stride+j]*=a->scales[j];
 }
 for(int j=n;j<n+m;j++)t[m*a->gpu.stride+j]=1.;
 for(int i=0;i<m;i++)for(int j=0;j<a->gpu.stride;j++)t[m*a->gpu.stride+j]-=t[i*a->gpu.stride+j];
 int* ctl=nullptr;
 if(!ok(cudaStreamCreateWithFlags(&a->prepare,cudaStreamNonBlocking))||
    !ok(cudaStreamCreateWithFlags(&a->io,cudaStreamNonBlocking))||
    !ok(cudaEventCreateWithFlags(&a->ready,cudaEventDisableTiming))||
    !ok(cudaMallocAsync(&a->gpu.t,t.size()*sizeof(double),a->prepare))||
    !ok(cudaMallocAsync(&a->gpu.basis,m*sizeof(int),a->prepare))||
    !ok(cudaMallocAsync(&ctl,3*sizeof(int),a->prepare))){
  a->gpu.ctl=ctl;destroy(a);return nullptr;
 }
 a->gpu.ctl=ctl;
 if(!ok(cudaMallocAsync(&a->gpu.out,(n+m)*sizeof(double),a->prepare))||
    !ok(cudaMallocAsync(&a->gpu.ticks,2*sizeof(unsigned long long),a->prepare))||
    !ok(cudaMemsetAsync(a->gpu.ticks,0,2*sizeof(unsigned long long),a->prepare))||
    !ok(cudaMemsetAsync(ctl,0,3*sizeof(int),a->prepare))||
    !ok(cudaMemcpyAsync(a->gpu.t,t.data(),t.size()*sizeof(double),cudaMemcpyHostToDevice,a->prepare))||
    !ok(cudaMemcpyAsync(a->gpu.basis,basis.data(),m*sizeof(int),cudaMemcpyHostToDevice,a->prepare))||
    !ok(cudaEventRecord(a->ready,a->prepare))){destroy(a);return nullptr;}
 // I/O cancellation/polling must follow allocation even before kernel launch.
 if(!ok(cudaStreamWaitEvent(a->io,a->ready,0))){destroy(a);return nullptr;}
 return a;
}
extern "C" void* simplex_launch(void** handles,int count){
 auto b=new Batch{};std::vector<Model> models;int maxm=0;
 for(int i=0;i<count;i++){auto a=static_cast<Owned*>(handles[i]);models.push_back(a->gpu);maxm=std::max(maxm,a->gpu.m);}
 if(!ok(cudaStreamCreateWithFlags(&b->stream,cudaStreamNonBlocking))||
    !ok(cudaEventCreateWithFlags(&b->done,cudaEventDisableTiming))){if(b->done)cudaEventDestroy(b->done);if(b->stream)cudaStreamDestroy(b->stream);delete b;return nullptr;}
 for(int i=0;i<count;i++)if(!ok(cudaStreamWaitEvent(b->stream,static_cast<Owned*>(handles[i])->ready,0))){cudaStreamSynchronize(b->stream);cudaEventDestroy(b->done);cudaStreamDestroy(b->stream);delete b;return nullptr;}
 if(!ok(cudaMallocAsync(&b->models,count*sizeof(Model),b->stream))||
    !ok(cudaMemcpyAsync(b->models,models.data(),count*sizeof(Model),cudaMemcpyHostToDevice,b->stream))){
  if(b->models)cudaFreeAsync(b->models,b->stream);cudaStreamSynchronize(b->stream);
  cudaEventDestroy(b->done);cudaStreamDestroy(b->stream);delete b;return nullptr;
 }
 // models remains alive until this stream's copy has completed. Synchronizing
 // only this pre-launch stream never waits for a different model's kernel.
 if(!ok(cudaStreamSynchronize(b->stream))){cudaFreeAsync(b->models,b->stream);cudaStreamSynchronize(b->stream);cudaEventDestroy(b->done);cudaStreamDestroy(b->stream);delete b;return nullptr;}
 phase_one<<<count,256,(maxm+1)*sizeof(double),b->stream>>>(b->models);
 if(!ok(cudaGetLastError())||!ok(cudaEventRecord(b->done,b->stream))){
  cudaStreamSynchronize(b->stream);cudaFreeAsync(b->models,b->stream);
  cudaStreamSynchronize(b->stream);cudaEventDestroy(b->done);cudaStreamDestroy(b->stream);delete b;return nullptr;
 }
 return b;
}
extern "C" int simplex_state(void* h){
 auto a=static_cast<Owned*>(h);std::lock_guard<std::mutex> guard(a->mutex);
 if(!ok(cudaMemcpyAsync(a->host_ctl,const_cast<int*>(a->gpu.ctl),3*sizeof(int),cudaMemcpyDeviceToHost,a->io))||
    !ok(cudaStreamSynchronize(a->io)))return 4;
 return a->host_ctl[1];
}
extern "C" unsigned long long* simplex_ticks(void* h){
 auto a=static_cast<Owned*>(h);std::lock_guard<std::mutex>guard(a->mutex);
 if(!ok(cudaMemcpyAsync(a->host_ticks,a->gpu.ticks,2*sizeof(unsigned long long),cudaMemcpyDeviceToHost,a->io))||!ok(cudaStreamSynchronize(a->io)))return nullptr;
 return a->host_ticks;
}
extern "C" int simplex_iterations(void* h){auto a=static_cast<Owned*>(h);std::lock_guard<std::mutex>guard(a->mutex);return a->host_ctl[2];}
extern "C" double* simplex_values(void* h){
 auto a=static_cast<Owned*>(h);std::lock_guard<std::mutex>guard(a->mutex);
 if(!a->unscaled){
  if(!ok(cudaMemcpyAsync(a->host_out.data(),a->gpu.out,a->gpu.n*sizeof(double),cudaMemcpyDeviceToHost,a->io))||!ok(cudaStreamSynchronize(a->io)))return nullptr;
  for(int j=0;j<a->gpu.n;j++)a->host_out[j]*=a->scales[j];a->unscaled=true;
 }return a->host_out.data();
}
extern "C" double* simplex_dual_values(void* h){
 auto a=static_cast<Owned*>(h);std::lock_guard<std::mutex>guard(a->mutex);
 if(!a->dual_unscaled){
  if(!ok(cudaMemcpyAsync(a->host_out.data()+a->gpu.n,a->gpu.out+a->gpu.n,a->gpu.m*sizeof(double),cudaMemcpyDeviceToHost,a->io))||!ok(cudaStreamSynchronize(a->io)))return nullptr;
  for(int i=0;i<a->gpu.m;i++)a->host_out[a->gpu.n+i]*=a->row_scales[i];a->dual_unscaled=true;
 }return a->host_out.data()+a->gpu.n;
}
extern "C" void simplex_cancel(void* h){
 auto a=static_cast<Owned*>(h);std::lock_guard<std::mutex>guard(a->mutex);int one=1;
 if(!ok(cudaMemcpyAsync(const_cast<int*>(a->gpu.ctl),&one,sizeof(int),cudaMemcpyHostToDevice,a->io)))return;
 ok(cudaStreamSynchronize(a->io));
}
extern "C" int simplex_done(void* h){auto e=cudaEventQuery(static_cast<Batch*>(h)->done);if(e==cudaSuccess)return 1;if(e==cudaErrorNotReady)return 0;ok(e);return -1;}
extern "C" void simplex_batch_free(void* h){
 auto b=static_cast<Batch*>(h);cudaEventSynchronize(b->done);cudaFreeAsync(b->models,b->stream);
 cudaStreamSynchronize(b->stream);cudaEventDestroy(b->done);cudaStreamDestroy(b->stream);delete b;
}
extern "C" void simplex_model_free(void* h){destroy(static_cast<Owned*>(h));}
