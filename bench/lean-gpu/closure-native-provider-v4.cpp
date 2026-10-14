// SPDX-License-Identifier: Apache-2.0
// Normal synchronous CUDA Driver provider for the native packet/quote ABI.
// Version4: conservative host rejection before CUDA; CPU algorithm unchanged.
// No SDK/live mutation, scheduler or explicit stack-limit override.
#include "closure-native-device-v2.h"
#include "closure-native-head-admission-v1.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <chrono>
#include <mutex>
#include <atomic>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <dlfcn.h>
#include <unistd.h>
extern "C" lean_obj_res closure_native_result(lean_obj_arg,uint32_t,uint64_t,uint64_t,uint64_t);
using U=uint32_t;using P=uint64_t;using Clock=std::chrono::steady_clock;
static uint64_t ns(Clock::time_point a){return std::chrono::duration_cast<std::chrono::nanoseconds>(Clock::now()-a).count();}
namespace {
struct State {
 std::mutex lock;std::atomic<bool> enabled{false},failed{false};bool initCurrent=false;pid_t pid=getpid();void* lib=nullptr;void* ctx=nullptr;void* module=nullptr;void* fn=nullptr;
 struct Buffer {P ptr=0;size_t size=0;};Buffer nodes,envs,args,answer;
 std::vector<CNEnv> hostEnvs;std::vector<CNClosure> cpuArgs;uint64_t hostGrowthCalls=0,hostGrowthNs=0;
 void hostScratch(size_t cap,bool cpu){auto begin=Clock::now();bool grew=false;
  if(hostEnvs.size()<cap){hostEnvs.resize(cap);++hostGrowthCalls;grew=true;}
  if(cpu&&cpuArgs.size()<cap){cpuArgs.resize(cap);++hostGrowthCalls;grew=true;}
  if(grew)hostGrowthNs+=ns(begin);
 }
 std::string device,error;uint64_t calls=0,supported=0,declined=0,cpuCalls=0,gpuCalls=0;
 uint64_t serializationNs=0,initNs=0,uploadNs=0,launchNs=0,downloadNs=0,quoteNs=0,wholeNs=0,allocBytes=0,peakBytes=0;
 uint64_t reasons[16]{};uint64_t hostDeclined=0,admissionNs=0;
 template<typename F> F symbol(const char* name){void* p=dlsym(lib,name);if(!p)throw std::runtime_error(std::string("missing driver symbol ")+name);return reinterpret_cast<F>(p);}
 template<typename... T> void call(const char* name,T... args){using F=int(*)(T...);int code=symbol<F>(name)(args...);if(code){error=std::string(name)+":"+std::to_string(code);throw std::runtime_error(error);}}
 void event(const char* event,const char* stage,uint64_t index){
  fprintf(stderr,"{\"event\":\"%s\",\"stage\":\"%s\",\"index\":%llu,\"pid\":%ld,\"calls\":%llu,\"supported\":%llu,\"declined\":%llu,\"cpu_calls\":%llu,\"gpu_calls\":%llu,\"serialization_ns\":%llu,\"initialization_ns\":%llu,\"allocation_upload_ns\":%llu,\"launch_sync_ns\":%llu,\"download_ns\":%llu,\"quotation_ns\":%llu,\"whole_provider_ns\":%llu,\"explicit_bytes\":%llu,\"explicit_peak_bytes\":%llu,\"device\":\"%s\",\"driver_error\":\"%s\",\"stack_limit_override\":false,\"memory_scope\":\"explicit allocations; excludes context/module/JIT/defaultstack/driver/otherowners\",\"reasons\":[",
   event,stage,(unsigned long long)index,(long)getpid(),(unsigned long long)calls,(unsigned long long)supported,(unsigned long long)declined,(unsigned long long)cpuCalls,(unsigned long long)gpuCalls,
   (unsigned long long)serializationNs,(unsigned long long)initNs,(unsigned long long)uploadNs,(unsigned long long)launchNs,(unsigned long long)downloadNs,(unsigned long long)quoteNs,(unsigned long long)wholeNs,(unsigned long long)allocBytes,(unsigned long long)peakBytes,device.c_str(),error.c_str());
  for(unsigned i=0;i<16;i++){fprintf(stderr,"%s%llu",i?",":"",(unsigned long long)reasons[i]);}fprintf(stderr,"] ,\"host_env_capacity\":%llu,\"host_cpu_arg_capacity\":%llu,\"host_scratch_bytes\":%llu,\"host_growth_calls\":%llu,\"host_growth_ns\":%llu,\"host_scratch_scope\":\"retained POD capacity only; excludes packets/native objects/allocator overhead\",\"host_declined\":%llu,\"head_admission_ns\":%llu}\n",
   (unsigned long long)hostEnvs.capacity(),(unsigned long long)cpuArgs.capacity(),
   (unsigned long long)(hostEnvs.capacity()*sizeof(CNEnv)+cpuArgs.capacity()*sizeof(CNClosure)),
   (unsigned long long)hostGrowthCalls,(unsigned long long)hostGrowthNs,(unsigned long long)hostDeclined,(unsigned long long)admissionNs);fflush(stderr);
 }
 void init(){
  if(ctx){return;}auto begin=Clock::now();
  try {
   lib=dlopen("libcuda.so.1",RTLD_NOW|RTLD_LOCAL);if(!lib)throw std::runtime_error("CUDA Driver library unavailable");
   call("cuInit",U(0));int dev=0;call("cuDeviceGet",&dev,int(0));char name[256]{};call("cuDeviceGetName",name,int(sizeof(name)),dev);device=name;
   if(!strstr(name,"RTX 5090")&&!strstr(name,"RTX5090"))throw std::runtime_error("device is not authorized RTX5090");
   const char* path=getenv("LEAN_NATIVE_CLOSURE_PTX");if(!path)throw std::runtime_error("LEAN_NATIVE_CLOSURE_PTX absent");
   std::ifstream file(path,std::ios::binary);if(!file)throw std::runtime_error("PTX open failed");std::ostringstream text;text<<file.rdbuf();std::string ptx=text.str();
   call("cuCtxCreate_v2",&ctx,U(0),dev);initCurrent=true;call("cuModuleLoadData",&module,(const void*)ptx.c_str());
   call("cuModuleGetFunction",&fn,module,"closure_native_reduce_device_v2");void* popped=nullptr;call("cuCtxPopCurrent_v2",&popped);initCurrent=false;
   initNs+=ns(begin);event("closure_native_device_ready","init",0);
  }catch(std::exception const& ex){error=ex.what();failed=true;if(initCurrent){void* popped=nullptr;try{call("cuCtxPopCurrent_v2",&popped);}catch(...){}initCurrent=false;}initNs+=ns(begin);event("closure_native_device_error","init",0);throw;}
 }
 void buffer(Buffer& b,size_t n){n=n?n:4;if(b.ptr&&b.size>=n)return;P next=0;call("cuMemAlloc_v2",&next,n);allocBytes+=n;if(allocBytes>peakBytes)peakBytes=allocBytes;
  if(b.ptr){try{call("cuMemFree_v2",b.ptr);allocBytes-=b.size;}catch(...){try{call("cuMemFree_v2",next);allocBytes-=n;}catch(...){}throw;}}b={next,n};}
 void close(){
  auto begin=Clock::now();enabled=false;
  if(ctx&&lib){bool pushed=false;try{call("cuCtxPushCurrent_v2",ctx);pushed=true;}catch(...){failed=true;}
   for(Buffer* b:{&nodes,&envs,&args,&answer})if(b->ptr){try{call("cuMemFree_v2",b->ptr);allocBytes-=b->size;}catch(...){failed=true;}*b={};}
   if(module){try{call("cuModuleUnload",module);}catch(...){failed=true;}}module=nullptr;
   if(pushed){void* previous=nullptr;try{call("cuCtxPopCurrent_v2",&previous);}catch(...){failed=true;}}
   try{call("cuCtxDestroy_v2",ctx);}catch(...){failed=true;}ctx=nullptr;
  }
  wholeNs+=ns(begin);event("closure_native_provider_finished","close",0);
 }
};
State state;
struct ContextScope {State& s;bool entered=false;explicit ContextScope(State& s):s(s){s.call("cuCtxPushCurrent_v2",s.ctx);entered=true;}~ContextScope(){if(entered){void* previous=nullptr;try{s.call("cuCtxPopCurrent_v2",&previous);}catch(...){s.failed=true;}}}};
lean_object* none_result(U why){return closure_native_result(lean_box(0),why,0,0,0);}
}
extern "C" lean_obj_res closure_native_result(lean_obj_arg,uint32_t,uint64_t,uint64_t,uint64_t);
extern "C" LEAN_EXPORT void closure_native_provider_enable(){std::lock_guard<std::mutex> g(state.lock);if(state.pid!=getpid()){if(state.lib||state.ctx){state.failed=true;state.enabled=false;return;}state.pid=getpid();state.failed=false;}if(!state.failed)state.enabled=true;}
extern "C" LEAN_EXPORT uint8_t closure_native_provider_enabled(b_lean_obj_arg /* expr */){const char* mode=getenv("LEAN_NATIVE_CLOSURE_MODE");return state.enabled&&!state.failed&&mode&&(strcmp(mode,"gpu")==0||strcmp(mode,"cpu")==0);}
extern "C" LEAN_EXPORT void closure_native_provider_disable(){state.enabled=false;}
extern "C" LEAN_EXPORT void closure_native_provider_checkpoint(uint64_t index,const char* stage){std::lock_guard<std::mutex> g(state.lock);const char* mode=getenv("LEAN_NATIVE_CLOSURE_MODE");if(mode&&(!strcmp(mode,"cpu")||!strcmp(mode,"gpu")))state.event("closure_native_provider_checkpoint",stage,index);}
extern "C" LEAN_EXPORT void closure_native_provider_close(){std::lock_guard<std::mutex> g(state.lock);if(state.pid!=getpid()){state.enabled=false;return;}const char* mode=getenv("LEAN_NATIVE_CLOSURE_MODE");if(state.calls||state.ctx||(mode&&(!strcmp(mode,"cpu")||!strcmp(mode,"gpu"))))state.close();else state.enabled=false;}
extern "C" LEAN_EXPORT lean_obj_res closure_native_provider_reduce(b_lean_obj_arg e,uint64_t limit,uint64_t cap,lean_obj_arg /* world */){
 auto begin=Clock::now();std::lock_guard<std::mutex> g(state.lock);++state.calls;U reason=0;lean_object* result=nullptr;ClosureNativePacket* packet=nullptr;
 try {
  if(!state.enabled||state.pid!=getpid()||state.failed||!limit||!cap||limit>0xffffffffu||cap>0xffffffffu)throw std::runtime_error("provider unavailable or unsupported bounds");
  auto step=Clock::now();packet=closure_native_v2_packet_prepare(e,U(cap),U(limit));state.serializationNs+=ns(step);reason=closure_native_v2_packet_error(packet);
  if(reason){result=none_result(reason);}else{
   CNAnswer answer{};const char* mode=getenv("LEAN_NATIVE_CLOSURE_MODE");
   bool cpu=mode&&strcmp(mode,"cpu")==0;
   U admissionCount=0;
   const CNNode* admissionNodes=closure_native_v2_packet_nodes(packet,&admissionCount);
   step=Clock::now();
   bool hostDecline=!cpu&&cn_definitely_unsupported_head(admissionNodes,admissionCount,U(limit));
   state.admissionNs+=ns(step);
   if(hostDecline){++state.hostDeclined;reason=4;result=none_result(reason);}
   else {
   state.hostScratch(static_cast<size_t>(cap),cpu);
   // Each cn_reduce call resets nenv/narg and writes every reachable entry.
   // Readback is bounded by answer.envCount; stale retained tails are unreachable.
   if(cpu){++state.cpuCalls;closure_native_v2_packet_cpu(packet,state.hostEnvs.data(),state.cpuArgs.data(),&answer);}
   else {
    state.init();ContextScope context(state);U nn=0;const CNNode* nodes=closure_native_v2_packet_nodes(packet,&nn);U root=0,maxsteps=U(limit),capacity=U(cap);
    step=Clock::now();state.buffer(state.nodes,size_t(nn)*sizeof(CNNode));state.buffer(state.envs,size_t(cap)*sizeof(CNEnv));state.buffer(state.args,size_t(cap)*sizeof(CNClosure));state.buffer(state.answer,sizeof(CNAnswer));
    state.call("cuMemcpyHtoD_v2",state.nodes.ptr,(const void*)nodes,size_t(nn)*sizeof(CNNode));state.call("cuCtxSynchronize");state.uploadNs+=ns(step);
    void* params[]={&state.nodes.ptr,&nn,&root,&state.envs.ptr,&state.args.ptr,&capacity,&maxsteps,&state.answer.ptr};
    step=Clock::now();state.call("cuLaunchKernel",state.fn,U(1),U(1),U(1),U(1),U(1),U(1),U(0),(void*)nullptr,(void*)params,(void*)nullptr);++state.gpuCalls;state.call("cuCtxSynchronize");state.launchNs+=ns(step);
    step=Clock::now();state.call("cuMemcpyDtoH_v2",(void*)&answer,state.answer.ptr,sizeof(answer));
    if(answer.envCount>cap)throw std::runtime_error("device environment count exceeds arena");
    if(answer.envCount){state.call("cuMemcpyDtoH_v2",(void*)state.hostEnvs.data(),state.envs.ptr,size_t(answer.envCount)*sizeof(CNEnv));}state.call("cuCtxSynchronize");state.downloadNs+=ns(step);
   }
   step=Clock::now();result=closure_native_v2_packet_quote(packet,&answer,state.hostEnvs.data());state.quoteNs+=ns(step);reason=lean_ctor_get_uint32(result,sizeof(void*)+24);
   }
  }
 }catch(std::exception const& ex){reason=11;if(state.ctx||state.lib){state.error=ex.what();state.failed=true;state.close();}result=none_result(reason);}
 closure_native_v2_packet_destroy(packet);
 if(!lean_is_scalar(lean_ctor_get(result,0)))++state.supported;else ++state.declined;
 ++state.reasons[reason<16?reason:15];state.wholeNs+=ns(begin);return lean_io_result_mk_ok(result);
}
