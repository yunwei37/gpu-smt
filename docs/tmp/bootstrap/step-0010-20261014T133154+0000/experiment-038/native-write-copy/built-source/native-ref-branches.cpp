// SPDX-License-Identifier: Apache-2.0
// Experimental native runtime state branches. This is not a complete service,
// arbitrary-FFI sandbox, native policy emulation or accepted performance result.
#include "native-ref-branches.h"
#include <atomic>
#include <array>
#include <condition_variable>
#include <cstdint>
#include <mutex>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <chrono>
#include <cstdio>
#include <cstdlib>

namespace {
struct Version {lean_object *original,*value;};
struct Context {
 uint64_t id; bool enabled;
 uint8_t owner_tag=0; // cache only; zero keeps the unbounded full-ID lookup
 std::string fallback;
 std::mutex mutex;
 std::condition_variable changed;
 std::unordered_map<lean_object*,lean_object*> refs,thunks;
 std::vector<Version> held;
 std::atomic<uint64_t> ref_generation{0};
 uint64_t copied_refs=0;
 std::atomic<uint64_t> tasks{0},scopes{0},ref_ops{0},ref_read_ops{0},thunk_ops{0},created_tasks{0};
};
struct Owner {uint64_t id;uint8_t tag;};
struct Registry {
 std::mutex mutex;
 std::unordered_map<lean_object*,Owner> owners;
 // A slot stays reserved for its context AND every still-live tagged ref.
 std::array<uint64_t,256> tag_uses{};
 std::unordered_map<void*,Context*> tasks;
 std::atomic<uint64_t> next_id{1};
};
Registry& registry(){static Registry* value=new Registry;return *value;}
thread_local Context* current=nullptr;
thread_local bool bypass=false;
// Counts follow the dynamically installed branch context. Flush before every
// context switch; the branch lifetime already covers admitted tasks/scopes.
thread_local uint64_t local_ref_ops=0,local_ref_read_ops=0,local_thunk_ops=0;
void flush_local_ops(){
 if(current){
  current->ref_ops.fetch_add(local_ref_ops,std::memory_order_relaxed);
  current->ref_read_ops.fetch_add(local_ref_read_ops,std::memory_order_relaxed);
  current->thunk_ops.fetch_add(local_thunk_ops,std::memory_order_relaxed);
 }
 local_ref_ops=0;local_ref_read_ops=0;local_thunk_ops=0;
}
struct LastVersion {
 uint64_t context_id=0;
 lean_object* original=nullptr;
 lean_object* value=nullptr;
 uint64_t generation=0;
};
thread_local LastVersion last_ref,last_thunk;
lean_object* remember(LastVersion& cache,Context* ctx,lean_object* original,lean_object* value){
 cache={ctx->id,original,value,ctx->ref_generation.load(std::memory_order_relaxed)};return value;
}
struct Bypass {bool old;Bypass():old(bypass){bypass=true;}~Bypass(){bypass=old;}};
bool owned_here(lean_object* ref,Context* ctx){
 // Ref headers are initialized before publication and the tag is immutable.
 // Tags cannot be reused while any ref carrying that tag survives.
 if(ctx->owner_tag)return lean_ptr_other(ref)==ctx->owner_tag;
 auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);
 auto it=g.owners.find(ref);return it!=g.owners.end()&&it->second.id==ctx->id;
}
lean_object* io_error(const char* message){
 return lean_io_result_mk_error(lean_mk_io_user_error(lean_mk_string(message)));
}
}

extern "C" void gpu_smt_abort_fallback(const char* operation){
 std::fprintf(stderr,"native_branch_fallback_process:%s\n",operation);
 std::fflush(stderr);std::_Exit(70);
}
extern "C" int gpu_smt_branch_active(){return current&&current->enabled;}
extern "C" void gpu_smt_note_fallback(const char* operation){
 Context* ctx=current;if(!ctx||!ctx->enabled)return;
 std::lock_guard<std::mutex> guard(ctx->mutex);
 if(ctx->fallback.empty())ctx->fallback=operation;
}
extern "C" lean_object* gpu_smt_effect_error(const char* operation){
 gpu_smt_note_fallback(operation);
 return io_error("native branch requires original verifier fallback");
}
extern "C" lean_obj_res gpu_smt_emit_line(lean_obj_arg line,lean_obj_arg){
 static std::mutex output;std::lock_guard<std::mutex> guard(output);
 std::fputs(lean_string_cstr(line),stdout);std::fputs("\n\n",stdout);std::fflush(stdout);
 lean_dec(line);return lean_io_result_mk_ok(lean_box(0));
}
extern "C" void gpu_smt_ref_created(lean_object* ref){
 if(bypass)return;
 auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);
 uint8_t tag=current?current->owner_tag:0;
 ref->m_other=tag;
 g.owners[ref]=Owner{current?current->id:0,tag};
 if(tag)++g.tag_uses[tag];
}
extern "C" void gpu_smt_ref_freed(lean_object* ref){
 auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);
 auto found=g.owners.find(ref);
 if(found==g.owners.end())return;
 // Native deletion may already have overwritten the header's RC/list bytes.
 // Use retained owner metadata, never a deallocated or rewritten header.
 if(found->second.tag)--g.tag_uses[found->second.tag];
 g.owners.erase(found);
}
namespace {
lean_object* resolve_ref(lean_object* ref,bool mutation){
 Context* ctx=current;
 if(!ctx||bypass||!ctx->enabled)return ref;
 ++local_ref_ops;
 if(!mutation)++local_ref_read_ops;
 if(owned_here(ref,ctx))return ref;
 // Every map key is retained through branch drain, including a read-only key.
 // This prevents an old base-read cache entry matching a recycled address.
 if(last_ref.context_id==ctx->id&&last_ref.original==ref){
  if(last_ref.value!=ref)return last_ref.value;
  if(!mutation&&last_ref.generation==ctx->ref_generation.load(std::memory_order_acquire))
   return ref;
 }
 std::lock_guard<std::mutex> guard(ctx->mutex);
 auto inserted=ctx->refs.emplace(ref,ref);
 auto it=inserted.first;
 if(inserted.second){
  lean_inc(ref);
  ctx->held.push_back({ref,lean_box(0)});
 }
 if(!mutation||it->second!=ref)return remember(last_ref,ctx,ref,it->second);
 Bypass no_recursion;
 // Copy only before a destructive take/set/swap. Native get acquires an owned
 // value token with the persistent/MT cell's atomic exchange protocol.
 lean_object* value=lean_st_ref_get(ref);
 lean_object* clone=lean_st_mk_ref(value);
 lean_mark_mt(clone);
 ctx->held.push_back({lean_box(0),clone});
 it->second=clone;
 ++ctx->copied_refs;
 // Publish a changed resolution before another task may reuse a cached base.
 ctx->ref_generation.fetch_add(1,std::memory_order_release);
 return remember(last_ref,ctx,ref,clone);
}
}
extern "C" lean_object* gpu_smt_resolve_ref_read(lean_object* ref){
 return resolve_ref(ref,false);
}
extern "C" lean_object* gpu_smt_resolve_ref(lean_object* ref){
 return resolve_ref(ref,true);
}
extern "C" lean_object* gpu_smt_resolve_thunk(lean_object* thunk){
 Context* ctx=current;
 if(!ctx||bypass||!ctx->enabled)return thunk;
 ++local_thunk_ops;
 if(last_thunk.context_id==ctx->id&&last_thunk.original==thunk)return last_thunk.value;
 std::lock_guard<std::mutex> guard(ctx->mutex);
 auto found=ctx->thunks.find(thunk);if(found!=ctx->thunks.end())return remember(last_thunk,ctx,thunk,found->second);
 // The normal inline fast path already handles an evaluated prepared thunk.
 // An unresolved thunk is evaluated privately so its memoized result cannot
 // reflect the first candidate's versioned refs in another candidate.
 lean_object* value=lean_to_thunk(thunk)->m_value.load();
 if(value)return thunk;
 lean_object* closure=lean_to_thunk(thunk)->m_closure.load();
 if(!closure)gpu_smt_abort_fallback("in_flight_prepared_thunk");
 Bypass no_recursion;
 lean_inc(closure);
 lean_object* clone=lean_mk_thunk(closure);
 lean_mark_mt(clone);
 lean_inc(thunk);
 ctx->held.push_back({thunk,clone});
 ctx->thunks.emplace(thunk,clone);
 return remember(last_thunk,ctx,thunk,clone);
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
 flush_local_ops();
 *saved=current;auto& g=registry();
 std::lock_guard<std::mutex> guard(g.mutex);
 auto it=g.tasks.find(task);Context* ctx=it==g.tasks.end()?nullptr:it->second;
 if(ctx)ctx->scopes.fetch_add(1,std::memory_order_relaxed);
 current=ctx;return ctx;
}
extern "C" void gpu_smt_task_leave(void* context,void* saved){
 flush_local_ops();
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
 for(auto& entry:g.owners)if(entry.second.id==0)lean_mark_mt(entry.first);
 return lean_io_result_mk_ok(lean_box(0));
}
extern "C" lean_obj_res gpu_smt_branch_begin(uint8_t enabled,lean_obj_arg){
 if(current)return io_error("nested native branch setup is not implemented");
 auto* ctx=new Context;
 ctx->id=registry().next_id.fetch_add(1,std::memory_order_relaxed);
 ctx->enabled=enabled!=0;
 if(ctx->enabled){
  auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);
  for(size_t slot=1;slot<g.tag_uses.size();++slot){
   if(g.tag_uses[slot]==0){
    ctx->owner_tag=static_cast<uint8_t>(slot);++g.tag_uses[slot];break;
   }
  }
 }
 // Exhausted cache slots do not block or reject a branch: owner_tag remains0.
 current=ctx;
 return lean_io_result_mk_ok(lean_box_uint64(reinterpret_cast<uintptr_t>(ctx)));
}
extern "C" lean_obj_res gpu_smt_branch_end(uint64_t handle,lean_obj_arg){
 auto* ctx=reinterpret_cast<Context*>(static_cast<uintptr_t>(handle));
 if(current!=ctx)return io_error("native branch context mismatch");
 flush_local_ops();
 current=nullptr;
 const auto start=std::chrono::steady_clock::now();
 {
  std::unique_lock<std::mutex> lock(ctx->mutex);
  ctx->changed.wait(lock,[&]{return ctx->tasks.load(std::memory_order_acquire)==0
                              &&ctx->scopes.load(std::memory_order_acquire)==0;});
 }
 std::ostringstream out;
 out<<"{\"fallback\":"<<(ctx->fallback.empty()?"false":"true")<<",\"fallback_operation\":\""<<ctx->fallback<<"\",\"ref_ops\":"<<ctx->ref_ops.load()<<",\"ref_versions\":"<<ctx->copied_refs<<",\"prepared_refs\":"<<ctx->refs.size()<<",\"ref_read_ops\":"<<ctx->ref_read_ops.load()<<",\"owner_cache_tag\":"<<static_cast<unsigned>(ctx->owner_tag)
    <<",\"thunk_ops\":"<<ctx->thunk_ops.load()<<",\"thunk_versions\":"<<ctx->thunks.size()
    <<",\"descendant_tasks\":"<<ctx->created_tasks.load()
    <<",\"drain_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}";
 // The branch owner is released only after admitted descendants and scopes
 // finish. Keep original identities alive throughout to prevent address reuse.
 for(auto& version:ctx->held){lean_dec(version.value);lean_dec(version.original);}
 if(ctx->owner_tag){
  auto& g=registry();std::lock_guard<std::mutex> guard(g.mutex);
  --g.tag_uses[ctx->owner_tag]; // release context reservation AFTER clone cleanup
 }
 delete ctx;
 return lean_io_result_mk_ok(lean_mk_string(out.str().c_str()));
}
