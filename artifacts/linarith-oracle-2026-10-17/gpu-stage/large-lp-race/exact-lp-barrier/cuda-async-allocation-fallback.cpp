// Finite benchmark compatibility repair for observed cudaMallocAsync error2
// under the user-required48GiB address-space ceiling. Never raises a limit.
// Stream synchronization before legacy free preserves prior stream operations.
// This may serialize work; all overhead belongs in the measured GPU path.
#include <cstddef>
#include <cstdio>
#include <dlfcn.h>
#include <mutex>
#include <unordered_set>
using cudaError_t=int;using cudaStream_t=void*;
static std::mutex owned_mutex;
static std::unordered_set<void*> legacy_allocations;
template<class F> static F next(const char* name) {
 auto f=reinterpret_cast<F>(dlsym(RTLD_NEXT,name));
 if(!f){std::fprintf(stderr,"gpu-smt allocator missing symbol %s\n",name);}
 return f;
}
extern "C" cudaError_t cudaMallocAsync(void** ptr,std::size_t bytes,cudaStream_t stream) {
 using Async=cudaError_t(*)(void**,std::size_t,cudaStream_t);
 using Legacy=cudaError_t(*)(void**,std::size_t);
 static auto original=next<Async>("cudaMallocAsync");
 static auto allocate=next<Legacy>("cudaMalloc");
 if(!original||!allocate)return 999;
 auto error=original(ptr,bytes,stream);
 if(error!=2)return error;
 auto repaired=allocate(ptr,bytes);
 if(!repaired&&*ptr){std::lock_guard<std::mutex> guard(owned_mutex);legacy_allocations.insert(*ptr);}
 std::fprintf(stderr,"gpu-smt cudaMallocAsync fallback bytes=%zu original=%d legacy=%d\n",bytes,error,repaired);
 return repaired;
}
extern "C" cudaError_t cudaFreeAsync(void* ptr,cudaStream_t stream) {
 bool legacy=false;
 {std::lock_guard<std::mutex> guard(owned_mutex);legacy=legacy_allocations.erase(ptr)>0;}
 if(!legacy){
  using Async=cudaError_t(*)(void*,cudaStream_t);
  static auto original=next<Async>("cudaFreeAsync");
  return original?original(ptr,stream):999;
 }
 using Sync=cudaError_t(*)(cudaStream_t);using Free=cudaError_t(*)(void*);
 static auto synchronize=next<Sync>("cudaStreamSynchronize");
 static auto release=next<Free>("cudaFree");
 if(!synchronize||!release)return 999;
 auto error=synchronize(stream);if(error)return error;
 return release(ptr);
}
