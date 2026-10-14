// SPDX-License-Identifier: Apache-2.0
// Exact semantic source: Lean4.9rc1 be6c4894e0a6, Meta/WHNF.lean easy/core
// beta/zeta rules. Native quote/rebuild helpers in ClosureNative.lean retain
// binder names/info, metadata, levels, literals and let nonDep hints.
// Separate CPU bridge; no CUDA launch or promotion of frozen partial W.
#include <lean/lean.h>
#include <cstdint>
#include <limits>
#include <vector>
#include <new>
#include <unordered_map>
#include "closure-native-device-v2.h"
extern "C" {
uint8_t lean_expr_has_fvar(lean_obj_arg);
uint8_t lean_expr_has_expr_mvar(lean_obj_arg);
uint8_t lean_expr_has_level_mvar(lean_obj_arg);
unsigned lean_expr_loose_bvar_range(lean_obj_arg);
lean_obj_res lean_expr_mk_bvar(lean_obj_arg);
lean_obj_res closure_native_rebuild(lean_obj_arg,lean_obj_arg,lean_obj_arg,lean_obj_arg);
lean_obj_res closure_native_result(lean_obj_arg,uint32_t,uint64_t,uint64_t,uint64_t);
}
namespace {
using U=uint32_t;constexpr U none=std::numeric_limits<U>::max();
enum Kind {BVAR=0,FVAR=1,MVAR=2,SORT=3,CONST=4,APP=5,LAM=6,PI=7,LET=8,LIT=9,MDATA=10,PROJ=11};
enum Why {OK=0,STEP_LIMIT=1,ARENA_LIMIT=2,LOOSE=3,HEAD_DEMAND=4,INVALID=5,ALLOC=6,UNSUPPORTED=7,STATE=8};
lean_object* retain(lean_object* p){lean_inc(p);return p;}
lean_object* child(lean_object* p,unsigned i){return lean_ctor_get(p,i);}
struct Cl {lean_object* e;U env;U level;};
struct Binding {U val,next;};
struct QuoteFrame {U id,depth,pc,a,b,c;};
struct Owned {
 lean_object* p;
 explicit Owned(lean_object* p):p(p){}
 Owned(Owned const&)=delete;Owned& operator=(Owned const&)=delete;
 Owned(Owned&& o) noexcept:p(o.p){o.p=nullptr;}
 ~Owned(){if(p)lean_dec(p);}
};
struct Machine {
 U cap,why=0;uint64_t limit,steps=0,quoted=0;
 std::vector<Cl> cls;std::vector<Binding> envs;std::vector<U> args;
 std::vector<QuoteFrame> frames;std::vector<Owned> output;
 Machine(uint64_t limit,U cap):cap(cap),limit(limit){}
 void fail(U w){if(!why)why=w;}
 bool tick(){if(++steps>limit){fail(STEP_LIMIT);return false;}return true;}
 U cl(lean_object* e,U env=none,U level=none){if(cls.size()>=cap){fail(ARENA_LIMIT);return 0;}cls.push_back({e,env,level});return U(cls.size()-1);}
 U bind(U val,U next){if(envs.size()>=cap){fail(ARENA_LIMIT);return none;}envs.push_back({val,next});return U(envs.size()-1);}
 U own(lean_object* p){if(output.size()>=cap){lean_dec(p);fail(ARENA_LIMIT);return 0;}output.emplace_back(p);return U(output.size()-1);}
 U index(lean_object* n){if(!lean_is_scalar(n)||lean_unbox(n)>std::numeric_limits<U>::max()){fail(UNSUPPORTED);return 0;}return U(lean_unbox(n));}
 U lookup(U e,U k){while(e!=none&&k){if(!tick())return 0;e=envs[e].next;--k;}if(e==none){fail(LOOSE);return 0;}return envs[e].val;}
 bool push(U id,U depth){if(frames.size()>=cap){fail(ARENA_LIMIT);return false;}frames.push_back({id,depth,0,0,0,0});return true;}
 U quote(U root){
  U ret=0;push(root,0);
  while(!frames.empty()&&!why&&tick()){
   // Read by value: push() can reallocate frames. Parent updates occur first.
   U pos=U(frames.size()-1);QuoteFrame f=frames[pos];Cl t=cls[f.id];
   if(!t.e){if(f.depth<=t.level){fail(LOOSE);break;}ret=own(lean_expr_mk_bvar(lean_unsigned_to_nat(f.depth-1-t.level)));frames.pop_back();continue;}
   if(f.pc==0){
    ++quoted;
    if(lean_expr_loose_bvar_range(retain(t.e))==0){ret=own(retain(t.e));frames.pop_back();continue;}
    unsigned tag=lean_obj_tag(t.e);
    if(tag==BVAR){U val=lookup(t.env,index(child(t.e,0)));frames[pos].pc=9;push(val,f.depth);continue;}
    if(tag==APP){frames[pos].pc=1;push(cl(child(t.e,0),t.env),f.depth);continue;}
    if(tag==LAM||tag==PI||tag==LET){frames[pos].pc=1;push(cl(child(t.e,1),t.env),f.depth);continue;}
    if(tag==MDATA||tag==PROJ){frames[pos].pc=8;push(cl(child(t.e,tag==MDATA?1:2),t.env),f.depth);continue;}
    fail(UNSUPPORTED);break;
   }
   if(f.pc==9){frames.pop_back();continue;}
   if(f.pc==8){ret=own(closure_native_rebuild(retain(t.e),retain(output[ret].p),retain(t.e),retain(t.e)));frames.pop_back();continue;}
   unsigned tag=lean_obj_tag(t.e);
   if(f.pc==1){frames[pos].a=ret;
    if(tag==APP){frames[pos].pc=2;push(cl(child(t.e,1),t.env),f.depth);continue;}
    if(tag==LET){frames[pos].pc=2;push(cl(child(t.e,2),t.env),f.depth);continue;}
    U marker=cl(nullptr,none,f.depth);U e=bind(marker,t.env);frames[pos].pc=2;push(cl(child(t.e,2),e),f.depth+1);continue;
   }
   if(f.pc==2&&tag==LET){frames[pos].b=ret;U marker=cl(nullptr,none,f.depth);U e=bind(marker,t.env);frames[pos].pc=3;push(cl(child(t.e,3),e),f.depth+1);continue;}
   if(f.pc==3&&tag==LET){ret=own(closure_native_rebuild(retain(t.e),retain(output[f.a].p),retain(output[f.b].p),retain(output[ret].p)));frames.pop_back();continue;}
   ret=own(closure_native_rebuild(retain(t.e),retain(output[f.a].p),retain(output[ret].p),retain(t.e)));frames.pop_back();
  }
  return ret;
 }
 lean_object* imported(const std::vector<lean_object*>& native,const CNAnswer& answer,const CNEnv* entries){
  steps=answer.steps;if(answer.reason)fail(answer.reason);
  if(answer.envCount>cap||answer.node>=native.size()||(answer.env!=none&&answer.env>=answer.envCount))fail(INVALID);
  if(!why){unsigned kind=lean_obj_tag(native[answer.node]);if(kind!=answer.terminalKind||(kind!=LAM&&kind!=PI&&kind!=SORT&&kind!=LIT))fail(HEAD_DEMAND);}
  for(U i=0;i<answer.envCount&&!why;i++){
   CNEnv e=entries[i];if(e.node>=native.size()||(e.env!=none&&e.env>=i)||(e.next!=none&&e.next>=i)){fail(INVALID);break;}
   U val=cl(native[e.node],e.env);bind(val,e.next);
  }
  U q=0;if(!why)q=quote(cl(native[answer.node],answer.env));
  lean_object* opt=lean_box(0);
  if(!why){opt=lean_alloc_ctor(1,1,0);lean_ctor_set(opt,0,retain(output[q].p));}
  return closure_native_result(opt,why,steps,quoted,uint64_t(envs.size()));
 }
};
}
// Source-native packet retains the original Expr and all child pointers through
// that owner. Native expression identity is translated to integer IDs only here.
struct ClosureNativePacket {
 lean_object* root;U cap,maxsteps,why=0;std::vector<lean_object*> native;std::vector<CNNode> nodes;
 std::unordered_map<lean_object*,U> ids;
 ClosureNativePacket(lean_object* e,U cap,U maxsteps):root(retain(e)),cap(cap),maxsteps(maxsteps){}
 ~ClosureNativePacket(){lean_dec(root);}
 U add(lean_object* e){auto it=ids.find(e);if(it!=ids.end())return it->second;if(native.size()>=cap){why=ARENA_LIMIT;return 0;}U id=U(native.size());ids.emplace(e,id);native.push_back(e);nodes.push_back({INVALID,0,0,0});return id;}
 void prepare(){
  if(lean_expr_loose_bvar_range(retain(root))){why=STATE;return;}
  add(root);
  // Serialize only children that reduction can demand. Binder domains/Pi bodies
  // remain native and are traversed on quote only when substitution needs them.
  for(U i=0;i<native.size()&&!why;i++){
   lean_object* e=native[i];U k=lean_obj_tag(e),a=0,b=0;
   if(k==BVAR){lean_object* idx=child(e,0);if(!lean_is_scalar(idx)||lean_unbox(idx)>std::numeric_limits<U>::max()){why=UNSUPPORTED;break;}a=U(lean_unbox(idx));}
   else if(k==APP){a=add(child(e,0));b=add(child(e,1));}
   else if(k==LAM)a=add(child(e,2));
   else if(k==LET){a=add(child(e,2));b=add(child(e,3));}
   else if(k==MDATA)a=add(child(e,1));
   nodes[i]={k,a,b,0};
  }
 }
};
extern "C" LEAN_EXPORT ClosureNativePacket* closure_native_v2_packet_prepare(b_lean_obj_arg e,U cap,U maxsteps){
 try {auto p=new ClosureNativePacket(e,cap,maxsteps);try{if(!cap||!maxsteps)p->why=INVALID;else p->prepare();}catch(std::bad_alloc const&){p->why=ALLOC;}return p;}catch(std::bad_alloc const&){return nullptr;}
}
extern "C" LEAN_EXPORT const CNNode* closure_native_v2_packet_nodes(const ClosureNativePacket* p,U* nn){*nn=p?U(p->nodes.size()):0;return p?p->nodes.data():nullptr;}
extern "C" LEAN_EXPORT U closure_native_v2_packet_error(const ClosureNativePacket* p){return p?p->why:U(ALLOC);}
extern "C" LEAN_EXPORT void closure_native_v2_packet_cpu(const ClosureNativePacket* p,CNEnv* envs,CNClosure* args,CNAnswer* answer){
 if(!p||p->why){*answer={p?p->why:U(ALLOC),0,none,0,0,0,none};return;}*answer=cn_reduce(p->nodes.data(),U(p->nodes.size()),0,envs,args,p->cap,p->maxsteps);
}
extern "C" LEAN_EXPORT lean_obj_res closure_native_v2_packet_quote(const ClosureNativePacket* p,const CNAnswer* answer,const CNEnv* entries){
 try {if(!p||p->why)return closure_native_result(lean_box(0),p?p->why:U(ALLOC),0,0,0);if(!answer||(!entries&&answer->envCount))return closure_native_result(lean_box(0),INVALID,0,0,0);Machine m(p->maxsteps,p->cap);return m.imported(p->native,*answer,entries);}catch(std::bad_alloc const&){return closure_native_result(lean_box(0),ALLOC,0,0,0);}
}
extern "C" LEAN_EXPORT void closure_native_v2_packet_destroy(ClosureNativePacket* p){delete p;}
extern "C" LEAN_EXPORT lean_obj_res closure_native_reduce_quote_v2(b_lean_obj_arg e,uint64_t stepLimit,uint64_t arenaLimit){
 if(!stepLimit||!arenaLimit||stepLimit>std::numeric_limits<U>::max()||arenaLimit>std::numeric_limits<U>::max())return closure_native_result(lean_box(0),INVALID,0,0,0);
 ClosureNativePacket* p=closure_native_v2_packet_prepare(e,U(arenaLimit),U(stepLimit));
 try {
  if(!p||p->why){auto r=closure_native_result(lean_box(0),closure_native_v2_packet_error(p),0,0,0);closure_native_v2_packet_destroy(p);return r;}
  std::vector<CNEnv> envs(static_cast<size_t>(arenaLimit));std::vector<CNClosure> args(static_cast<size_t>(arenaLimit));CNAnswer answer;
  closure_native_v2_packet_cpu(p,envs.data(),args.data(),&answer);auto result=closure_native_v2_packet_quote(p,&answer,envs.data());closure_native_v2_packet_destroy(p);return result;
 }catch(std::bad_alloc const&){closure_native_v2_packet_destroy(p);return closure_native_result(lean_box(0),ALLOC,0,0,0);}
}
