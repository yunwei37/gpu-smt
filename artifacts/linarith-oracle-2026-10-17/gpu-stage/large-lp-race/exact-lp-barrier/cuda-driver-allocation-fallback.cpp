// Finite benchmark repair for static CUDA runtimes using Driver Entry Point Access.
// Forward all symbols/versions except async allocate/free, and preserve failures.
// Only CUDA_ERROR_OUT_OF_MEMORY triggers legacy allocation under unchanged limits.
#include <cstddef>
#include <cstdio>
#include <cstring>
#include <dlfcn.h>
#include <mutex>
#include <unordered_set>
using Result=int;using DevicePtr=unsigned long long;using Stream=void*;
using Lookup=void*(*)(void*,const char*);
using ProcV1=Result(*)(const char*,void**,int,unsigned long long);
using ProcV2=Result(*)(const char*,void**,int,unsigned long long,int*);
using Async=Result(*)(DevicePtr*,std::size_t,Stream);
using FreeAsync=Result(*)(DevicePtr,Stream);
static Async original_async=nullptr;
static FreeAsync original_free_async=nullptr;
static std::mutex allocations_mutex;
static std::unordered_set<DevicePtr> legacy;
static Lookup real_lookup(){
 static auto f=reinterpret_cast<Lookup>(dlvsym(RTLD_NEXT,"dlsym","GLIBC_2.2.5"));
 return f;
}
template<class F> static F driver(const char* name){
 static void* lib=dlopen("libcuda.so.1",RTLD_LAZY|RTLD_LOCAL);
 return reinterpret_cast<F>(real_lookup()(lib,name));
}
static Result allocate(DevicePtr* ptr,std::size_t bytes,Stream stream){
 auto original=original_async?original_async:driver<Async>("cuMemAllocAsync");
 if(!original)return 999;
 auto error=original(ptr,bytes,stream);if(error!=2)return error;
 using Legacy=Result(*)(DevicePtr*,std::size_t);
 static auto alloc=driver<Legacy>("cuMemAlloc_v2");
 auto fixed=alloc?alloc(ptr,bytes):999;
 if(!fixed&&*ptr){std::lock_guard<std::mutex> g(allocations_mutex);legacy.insert(*ptr);}
 std::fprintf(stderr,"gpu-smt driver async fallback bytes=%zu original=%d legacy=%d\n",bytes,error,fixed);
 return fixed;
}
static Result release(DevicePtr ptr,Stream stream){
 bool ours;
 {std::lock_guard<std::mutex> g(allocations_mutex);ours=legacy.erase(ptr)>0;}
 if(!ours){auto f=original_free_async?original_free_async:driver<FreeAsync>("cuMemFreeAsync");return f?f(ptr,stream):999;}
 using Sync=Result(*)(Stream);using Free=Result(*)(DevicePtr);
 static auto sync=driver<Sync>("cuStreamSynchronize");
 static auto free=driver<Free>("cuMemFree_v2");
 if(!sync||!free)return 999;
 auto error=sync(stream);return error?error:free(ptr);
}
static void replace(const char* symbol,void** fn){
 if(!std::strcmp(symbol,"cuMemAllocAsync")||!std::strcmp(symbol,"cuMemAllocAsync_ptsz")){
  original_async=reinterpret_cast<Async>(*fn);*fn=reinterpret_cast<void*>(allocate);
 }else if(!std::strcmp(symbol,"cuMemFreeAsync")||!std::strcmp(symbol,"cuMemFreeAsync_ptsz")){
  original_free_async=reinterpret_cast<FreeAsync>(*fn);*fn=reinterpret_cast<void*>(release);
 }
}
extern "C" Result cuGetProcAddress(const char* symbol,void** fn,int version,unsigned long long flags){
 static auto original=driver<ProcV1>("cuGetProcAddress");
 auto error=original?original(symbol,fn,version,flags):999;
 if(!error&&*fn)replace(symbol,fn);return error;
}
extern "C" Result cuGetProcAddress_v2(const char* symbol,void** fn,int version,unsigned long long flags,int* status){
 static auto original=driver<ProcV2>("cuGetProcAddress_v2");
 auto error=original?original(symbol,fn,version,flags,status):999;
 if(!error&&*fn)replace(symbol,fn);return error;
}
extern "C" void* dlsym(void* handle,const char* symbol){
 if(!std::strcmp(symbol,"cuGetProcAddress"))return reinterpret_cast<void*>(cuGetProcAddress);
 if(!std::strcmp(symbol,"cuGetProcAddress_v2"))return reinterpret_cast<void*>(cuGetProcAddress_v2);
 auto result=real_lookup()(handle,symbol);
 if(result&&(!std::strcmp(symbol,"cuMemAllocAsync")||!std::strcmp(symbol,"cuMemAllocAsync_ptsz"))){
  original_async=reinterpret_cast<Async>(result);return reinterpret_cast<void*>(allocate);
 }
 if(result&&(!std::strcmp(symbol,"cuMemFreeAsync")||!std::strcmp(symbol,"cuMemFreeAsync_ptsz"))){
  original_free_async=reinterpret_cast<FreeAsync>(result);return reinterpret_cast<void*>(release);
 }
 return result;
}
