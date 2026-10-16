// SPDX-License-Identifier: Apache-2.0
// Experimental native runtime state branches. This is not a complete service,
// arbitrary-FFI sandbox, native policy emulation or accepted performance result.
#include "native-ref-branches.h"
#include <atomic>
#include <condition_variable>
#include <cstdint>
#include <mutex>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <chrono>

namespace {
struct Version {lean_object *original,*value;};
struct Context {
 uint64_t id; bool enabled;
 std::mutex mutex;
 std::condition_variable changed;
 std::unordered_map<lean_object*,lean_object*> refs,thunks;
 std::vector<Version> held;
 std::atomic<uint64_t> tasks{0},scopes{0},ref_ops{0},thunk_ops{0},created_tasks{0};
};
struct Registry {
 std::mutex mutex;
 std::unordered_map<lean_object*,uint64_t> owners;
 std::unordered_map<void*,Context*> tasks;
 std::atomic<uint64_t> next_id{1};
};
Registry& registry(){static Registry* value=new Registry;return *value;}
thread_local Context* current=nullptr;
thread_local bool bypass=false;
struct Bypass {bool old;Bypass():old(bypass){bypass=true;}~Bypass(){bypass=old;}};
bool owned_here(lean_object* ref,Context* ctx){
 auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);
 auto it=g.owners.find(ref);return it!=g.owners.end()&&it->second==ctx->id;
}
lean_object* io_error(const char* message){
 return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string(message)));
}
}

extern "C" void gpu_smt_ref_created(lean_object* ref){
 if(bypass)return;
 auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);
 g.owners[ref]=current?current->id:0;
}
extern "C" void gpu_smt_ref_freed(lean_object* ref){
 auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);g.owners.erase(ref);
}
extern "C" lean_object* gpu_smt_resolve_ref(lean_object* ref){
 Context* ctx=current;
 if(!ctx||bypass||!ctx->enabled)return ref;
 ctx->ref_ops.fetch_add(1,std::memory_order_relaxed);
 if(owned_here(ref,ctx))return ref;
 std::lock_guard<std::mutex> guard(ctx->mutex);
 auto it=ctx->refs.find(ref);if(it!=ctx->refs.end())return it->second;
 Bypass no_recursion;
 // Use the native primitive to acquire an owned RC token. In particular,
 // persistent/MT cells require the runtime's atomic exchange protocol.
 lean_object* value=lean_st_ref_get(ref);
 lean_object* clone=lean_st_mk_ref(value);
 lean_mark_mt(clone);
 lean_inc(ref);
 ctx->held.push_back({ref,clone});
 ctx->refs.emplace(ref,clone);
 return clone;
}
extern "C" lean_object* gpu_smt_resolve_thunk(lean_object* thunk){
 Context* ctx=current;
 if(!ctx||bypass||!ctx->enabled)return thunk;
 ctx->thunk_ops.fetch_add(1,std::memory_order_relaxed);
 std::lock_guard<std::mutex> guard(ctx->mutex);
 auto found=ctx->thunks.find(thunk);if(found!=ctx->thunks.end())return found->second;
 // The normal inline fast path already handles an evaluated prepared thunk.
 // An unresolved thunk is evaluated privately so its memoized result cannot
 // reflect the first candidate's versioned refs in another candidate.
 lean_object* value=lean_to_thunk(thunk)->m_value.load();
 if(value)return thunk;
 lean_object* closure=lean_to_thunk(thunk)->m_closure.load();
 if(!closure)return thunk; // unsupported in-flight prepared thunk: NOT qualified
 Bypass no_recursion;
 lean_inc(closure);
 lean_object* clone=lean_mk_thunk(closure);
 lean_mark_mt(clone);
 lean_inc(thunk);
 ctx->held.push_back({thunk,clone});
 ctx->thunks.emplace(thunk,clone);
 return clone;
}
extern "C" void gpu_smt_task_created(void* task,int has_closure){
 if(!current||!has_closure)return; // unresolved promises are data, not running code
 Context* ctx=current;auto& g=registry();
 std::lock_guard<std::mutex> guard(g.mutex);
 g.tasks.emplace(task,ctx);
 ctx->tasks.fetch_add(1,std::memory_order_relaxed);
 ctx->created_tasks.fetch_add(1,std::memory_order_relaxed);
}
extern "C" void gpu_smt_task_retired(void* task){
 Context* ctx=nullptr;auto& g=registry();
 {
  std::lock_guard<std::mutex> guard(g.mutex);
  auto it=g.tasks.find(task);if(it==g.tasks.end())return;
  ctx=it->second;
  std::lock_guard<std::mutex> owner_guard(ctx->mutex);
  g.tasks.erase(it);
  ctx->tasks.fetch_sub(1,std::memory_order_release);
  ctx->changed.notify_all();
 }
}
extern "C" void* gpu_smt_task_enter(void* task,void** saved){
 *saved=current;auto& g=registry();
 std::lock_guard<std::mutex> guard(g.mutex);
 auto it=g.tasks.find(task);Context* ctx=it==g.tasks.end()?nullptr:it->second;
 if(ctx)ctx->scopes.fetch_add(1,std::memory_order_relaxed);
 current=ctx;return ctx;
}
extern "C" void gpu_smt_task_leave(void* context,void* saved){
 current=static_cast<Context*>(saved);
 auto* ctx=static_cast<Context*>(context);
 if(ctx){std::lock_guard<std::mutex> guard(ctx->mutex);ctx->scopes.fetch_sub(1,std::memory_order_release);ctx->changed.notify_all();}
}
// This must run at a true prepared/quiescent boundary, before concurrent jobs.
// It promotes live runtime-created refs, not a reconstruction of their values.
extern "C" lean_obj_res gpu_smt_prepare_refs(lean_obj_arg){
 if(current)return io_error("prepare called within native branch");
 Bypass no_recursion;auto& g=registry();
 std::lock_guard<std::mutex> guard(g.mutex);
 for(auto& entry:g.owners)if(entry.second==0)lean_mark_mt(entry.first);
 return lean_io_result_mk_ok(lean_box(0));
}
extern "C" lean_obj_res gpu_smt_branch_begin(uint8_t enabled,lean_obj_arg){
 if(current)return io_error("nested native branch setup is not implemented");
 auto* ctx=new Context;
 ctx->id=registry().next_id.fetch_add(1,std::memory_order_relaxed);
 ctx->enabled=enabled!=0;current=ctx;
 return lean_io_result_mk_ok(lean_box_uint64(reinterpret_cast<uintptr_t>(ctx)));
}
extern "C" lean_obj_res gpu_smt_branch_end(uint64_t handle,lean_obj_arg){
 auto* ctx=reinterpret_cast<Context*>(static_cast<uintptr_t>(handle));
 if(current!=ctx)return io_error("native branch context mismatch");
 current=nullptr;
 const auto start=std::chrono::steady_clock::now();
 {
  std::unique_lock<std::mutex> lock(ctx->mutex);
  ctx->changed.wait(lock,[&]{return ctx->tasks.load(std::memory_order_acquire)==0
                              &&ctx->scopes.load(std::memory_order_acquire)==0;});
 }
 std::ostringstream out;
 out<<"{\"ref_ops\":"<<ctx->ref_ops.load()<<",\"ref_versions\":"<<ctx->refs.size()
    <<",\"thunk_ops\":"<<ctx->thunk_ops.load()<<",\"thunk_versions\":"<<ctx->thunks.size()
    <<",\"descendant_tasks\":"<<ctx->created_tasks.load()
    <<",\"drain_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}";
 // The branch owner is released only after admitted descendants and scopes
 // finish. Keep original identities alive throughout to prevent address reuse.
 for(auto& version:ctx->held){lean_dec(version.value);lean_dec(version.original);}
 delete ctx;
 return lean_io_result_mk_ok(lean_mk_string(out.str().c_str()));
}
