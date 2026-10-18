// Untrusted phase-I support search. Every hint is repaired exactly on CPU
// and checked by Lean. One block owns each LP; cancellation is per model.
#include <cuda_runtime.h>
#include <math_constants.h>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <atomic>
struct Model {int m,n,stride;double* t;int* basis;volatile int* ctl;double* out;};
struct Owned {Model gpu;int* ctl;double* out;std::vector<double> scales,row_scales;bool unscaled=false,dual_unscaled=false;};
struct Batch {Model* models;cudaEvent_t done;cudaStream_t stream;};
static thread_local std::string error_text;
static bool ok(cudaError_t e){if(e==cudaSuccess)return true;error_text=cudaGetErrorString(e);return false;}
extern "C" const char* simplex_error(){return error_text.c_str();}
__global__ void phase_one(Model* models){
 Model a=models[blockIdx.x];int tid=threadIdx.x;
 extern __shared__ double pivot_column[];
 __shared__ int enter,leave,finish,iterations;
 __shared__ double pivot;
 if(!tid){finish=0;iterations=0;}__syncthreads();
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
 if(!tid){__threadfence_system();a.ctl[1]=finish;}
}
static void destroy(Owned* a){
 if(a->gpu.t)cudaFree(a->gpu.t);if(a->gpu.basis)cudaFree(a->gpu.basis);
 if(a->ctl)cudaFreeHost(a->ctl);if(a->out)cudaFreeHost(a->out);delete a;
}
extern "C" void* simplex_model(int m,int n,const int* offsets,const int* indices,const double* values,const double* rhs){
 if(m<=0||n<=0){error_text="empty model";return nullptr;}
 auto a=new Owned{};a->gpu.m=m;a->gpu.n=n;a->gpu.stride=n+m+1;
 std::vector<double> t(static_cast<size_t>(m+1)*a->gpu.stride,0.);
 std::vector<int> basis(m);a->row_scales.resize(m,1.);
 int last=n+m;
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
 // Equilibrate original rows/columns before adding/eliminating phase-I costs.
 // A*diag(scales)*y=b; return x=diag(scales)*y to the unchanged CPU repair.
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
 for(int i=0;i<m;i++)for(int j=0;j<a->gpu.stride;j++)
  t[m*a->gpu.stride+j]-=t[i*a->gpu.stride+j];
 if(!ok(cudaMalloc(&a->gpu.t,t.size()*sizeof(double)))||
    !ok(cudaMalloc(&a->gpu.basis,m*sizeof(int)))||
    !ok(cudaHostAlloc(&a->ctl,3*sizeof(int),cudaHostAllocMapped))||
    !ok(cudaHostAlloc(&a->out,(n+m)*sizeof(double),cudaHostAllocMapped))){destroy(a);return nullptr;}
 a->ctl[0]=a->ctl[1]=a->ctl[2]=0;
 int* dc=nullptr;double* dout=nullptr;
 if(!ok(cudaHostGetDevicePointer(&dc,a->ctl,0))||!ok(cudaHostGetDevicePointer(&dout,a->out,0))||
    !ok(cudaMemcpy(a->gpu.t,t.data(),t.size()*sizeof(double),cudaMemcpyHostToDevice))||
    !ok(cudaMemcpy(a->gpu.basis,basis.data(),m*sizeof(int),cudaMemcpyHostToDevice))){destroy(a);return nullptr;}
 a->gpu.ctl=dc;a->gpu.out=dout;return a;
}
extern "C" void* simplex_launch(void** handles,int count){
 auto b=new Batch{};std::vector<Model> models;int maxm=0;
 for(int i=0;i<count;i++){auto a=static_cast<Owned*>(handles[i]);models.push_back(a->gpu);maxm=std::max(maxm,a->gpu.m);}
 if(!ok(cudaStreamCreateWithFlags(&b->stream,cudaStreamNonBlocking))||
    !ok(cudaEventCreateWithFlags(&b->done,cudaEventDisableTiming))||
    !ok(cudaMalloc(&b->models,count*sizeof(Model)))||
    !ok(cudaMemcpy(b->models,models.data(),count*sizeof(Model),cudaMemcpyHostToDevice))){
  if(b->models)cudaFree(b->models);if(b->done)cudaEventDestroy(b->done);if(b->stream)cudaStreamDestroy(b->stream);delete b;return nullptr;
 }
 phase_one<<<count,256,(maxm+1)*sizeof(double),b->stream>>>(b->models);
 if(!ok(cudaGetLastError())||!ok(cudaEventRecord(b->done,b->stream))){
  cudaStreamSynchronize(b->stream);cudaFree(b->models);cudaEventDestroy(b->done);cudaStreamDestroy(b->stream);delete b;return nullptr;
 }
 return b;
}
extern "C" int simplex_state(void* h){auto a=static_cast<Owned*>(h);int v=*reinterpret_cast<volatile int*>(a->ctl+1);std::atomic_thread_fence(std::memory_order_acquire);return v;}
extern "C" int simplex_iterations(void* h){return *reinterpret_cast<volatile int*>(static_cast<Owned*>(h)->ctl+2);}
extern "C" double* simplex_values(void* h){auto a=static_cast<Owned*>(h);if(!a->unscaled){for(int j=0;j<a->gpu.n;j++)a->out[j]*=a->scales[j];a->unscaled=true;}return a->out;}
extern "C" double* simplex_dual_values(void* h){auto a=static_cast<Owned*>(h);if(!a->dual_unscaled){for(int i=0;i<a->gpu.m;i++)a->out[a->gpu.n+i]*=a->row_scales[i];a->dual_unscaled=true;}return a->out+a->gpu.n;}
extern "C" void simplex_cancel(void* h){auto a=static_cast<Owned*>(h);*reinterpret_cast<volatile int*>(a->ctl)=1;std::atomic_thread_fence(std::memory_order_seq_cst);}
extern "C" int simplex_done(void* h){auto e=cudaEventQuery(static_cast<Batch*>(h)->done);if(e==cudaSuccess)return 1;if(e==cudaErrorNotReady)return 0;ok(e);return -1;}
extern "C" void simplex_batch_free(void* h){auto b=static_cast<Batch*>(h);cudaEventSynchronize(b->done);cudaFree(b->models);cudaEventDestroy(b->done);cudaStreamDestroy(b->stream);delete b;}
extern "C" void simplex_model_free(void* h){destroy(static_cast<Owned*>(h));}
