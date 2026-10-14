#include <lean/lean.h>
#include "kernel/expr.h"
#include "runtime/thread.h"
#include <array>
#include <unordered_map>
#include <atomic>
#include <cstdio>
#include <cstring>
using namespace lean;
struct Key { std::array<unsigned char,13> cfg; expr term; };
struct Hash { size_t operator()(Key const&k)const {size_t h=hash(k.term);for(auto x:k.cfg)h=(h*131)^x;return h;} };
struct Eq { bool operator()(Key const&a,Key const&b)const{return a.cfg==b.cfg && a.term==b.term;} };
struct Memo {
 object_ref env,opts;
 std::unordered_map<Key,expr,Hash,Eq> entries;
 uint64_t reads=0,hits=0,puts=0,clears=0,peak=0;
};
static thread_local Memo *current=nullptr;
static void retire(void*p){
 Memo*m=(Memo*)p;
 fprintf(stderr,"closed_memo_finished reads=%llu hits=%llu puts=%llu scope_clears=%llu peak_entries=%llu\n",
 (unsigned long long)m->reads,(unsigned long long)m->hits,(unsigned long long)m->puts,
 (unsigned long long)m->clears,(unsigned long long)m->peak);
 delete m;current=nullptr;
}
static Memo& scope(lean_object*env,lean_object*opts){
 if(!current){current=new Memo;register_thread_finalizer(retire,current);}
 Memo&m=*current;
 if(m.env.raw()!=env || m.opts.raw()!=opts){
  m.entries.clear();m.env=object_ref(env,true);m.opts=object_ref(opts,true);++m.clears;
 }
 return m;
}
static bool config_bytes(lean_object*cfg,std::array<unsigned char,13>&bytes){
 if(lean_is_scalar(cfg)||lean_ctor_num_objs(cfg)!=0)return false;
 memcpy(bytes.data(),lean_ctor_scalar_cptr(cfg),13);return true;
}
extern "C" LEAN_EXPORT lean_obj_res gpu_smt_closed_get(b_lean_obj_arg env,b_lean_obj_arg opts,
 b_lean_obj_arg cfg,b_lean_obj_arg term,lean_obj_arg world){
 Memo&m=scope(env,opts);++m.reads;
 std::array<unsigned char,13> bytes;
 if(!config_bytes(cfg,bytes)){lean_dec(world);return lean_io_result_mk_ok(lean_box(0));}
 Key key{bytes,expr(term,true)};
 auto it=m.entries.find(key);
 lean_dec(world);
 if(it==m.entries.end())return lean_io_result_mk_ok(lean_box(0));
 ++m.hits;
 lean_object*some=lean_alloc_ctor(1,1,0);lean_inc(it->second.raw());lean_ctor_set(some,0,it->second.raw());
 return lean_io_result_mk_ok(some);
}
extern "C" LEAN_EXPORT lean_obj_res gpu_smt_closed_put(b_lean_obj_arg env,b_lean_obj_arg opts,
 b_lean_obj_arg cfg,b_lean_obj_arg term,b_lean_obj_arg result,lean_obj_arg world){
 Memo&m=scope(env,opts);std::array<unsigned char,13> bytes;
 if(config_bytes(cfg,bytes)){
  lean_mark_mt(term);lean_mark_mt(result);
  m.entries.insert_or_assign(Key{bytes,expr(term,true)},expr(result,true));++m.puts;
  if(m.entries.size()>m.peak)m.peak=m.entries.size();
 }
 lean_dec(world);return lean_io_result_mk_ok(lean_box(0));
}
extern "C" LEAN_EXPORT uint8_t gpu_smt_same_mctx(b_lean_obj_arg a,b_lean_obj_arg b){return a==b;}
extern "C" LEAN_EXPORT uint8_t gpu_smt_same_env(b_lean_obj_arg a,b_lean_obj_arg b){return a==b;}
