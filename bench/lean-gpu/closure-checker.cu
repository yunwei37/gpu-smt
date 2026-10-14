// SPDX-License-Identifier: Apache-2.0
// Closure/continuation implementation, 2026. Semantic references and boundaries:
// Lean 4.9.0-rc1 be6c4894e0a6 src/kernel/{type_checker.cpp,inductive.h};
// sokonanoda 7645b1e1fcac
// src/frontend/parser.rs. Algorithmic rules are reimplemented, not copied code.
#include <stdint.h>
#ifdef __CUDACC__
#define HD __host__ __device__
#else
#define HD
#endif
using U=uint32_t;
static constexpr U N=0xffffffffu;
// Every runtime array is caller allocated. No recursive C++ calls, heap or device
// stack recursion. IDs include closure environments; no cache keyed only by AST.
struct Node {U tag,a,b,c,d;};
struct Level {U tag,a,b;};
struct Decl {U kind,name,type,value,po,pn,np,nf,ind,ni,nm,minor,ro,rn,flags,ctor;};
struct Rule {U ctor,nfields,rhs;};
struct Term {U tag,a,b,c,e,u,s;};
struct Env {U key,value,next;};
struct LVal {U tag,a,b;};
struct Frame {U op,pc,x,y,mode,a,b,c,d,i,j,k;};
struct Answer {U verified,reason,steps,terms,frames,envs,levels;};
struct Input {const Node* nodes;const Level* levels;const Decl* decls;const Rule* rules;const U* ulists;const U* params;U nn,nl,nd,nr,nat,string_,zero,succ,nu,np;};
struct Scratch {Term* terms;Env* envs;LVal* levels;Frame* frames;U cap,fcap;};
enum {REF=0,LOCAL=1,SORT=2,CONST=3,APP=4,LAM=5,PI=6,LET=7,NAT=8,STRING=9,PROJ=10,MDATA=11};
enum {W=1,I=2,E=3,L=4,LE=5,CHECK=6};
enum {OK=0,CAPACITY=1,BAD_REFERENCE=2,UNSUPPORTED=3,LOOSE_VAR=4,LEVEL_PARAM=5,UNSAFE=6,NOT_SORT=7,NOT_PI=8,NOT_EQUAL=9,STEP_LIMIT=10,FRAME_LIMIT=11,PARTIAL_WHNF=12};
struct Machine {
 Input in;Scratch z;U nt,ne,nl,sp,steps,error,ret,fresh,maxsteps,peaksp;
 HD void fail(U r){if(!error)error=r;}
 HD U term(U tag,U a=0,U b=0,U c=N,U e=N,U u=N,U s=N){if(nt>=z.cap){fail(CAPACITY);return 0;}U id=nt++;z.terms[id]={tag,a,b,c,e,u,s};return id;}
 HD U env(U key,U val,U next){if(ne>=z.cap){fail(CAPACITY);return N;}U id=ne++;z.envs[id]={key,val,next};return id;}
 HD U lv(U tag,U a=0,U b=0){
  if(tag==2){if(a==b)return a;
  if(z.levels[a].tag==0)return b;
  if(z.levels[b].tag==0)return a;
  if(a>b){U t=a;a=b;b=t;}}
  if(tag==3){if(z.levels[b].tag==0)return b;if(z.levels[b].tag==1)return lv_max(a,b);}
  for(U k=0;k<nl;k++){LVal t=z.levels[k];if(t.tag==tag&&t.a==a&&t.b==b)return k;}
  if(nl>=z.cap){fail(CAPACITY);return 0;}U id=nl++;z.levels[id]={tag,a,b};return id;
 }
 HD U lv_max(U a,U b){ // no recursive call from lv; max canonical constructor
  if(a==b)return a;
  if(z.levels[a].tag==0)return b;
  if(z.levels[b].tag==0)return a;
  if(a>b){U t=a;a=b;b=t;}
  for(U k=0;k<nl;k++){LVal t=z.levels[k];if(t.tag==2&&t.a==a&&t.b==b)return k;}
  if(nl>=z.cap){fail(CAPACITY);return 0;}U id=nl++;z.levels[id]={2,a,b};return id;
 }
 HD U closure(U node,U e=N,U u=N){return term(REF,node,0,N,e,u);}
 // Concatenate substitutions preserving newest-to-oldest lexical composition.
 HD U concat(U a,U b){U rev=N;for(U p=a;p!=N;p=z.envs[p].next)rev=env(z.envs[p].key,z.envs[p].value,rev);for(U p=rev;p!=N;p=z.envs[p].next)b=env(z.envs[p].key,z.envs[p].value,b);return b;}
 HD U subst(U t,U s){if(s==N)return t;if(t>=nt){fail(BAD_REFERENCE);return 0;}Term v=z.terms[t];v.s=concat(s,v.s);U q=term(v.tag,v.a,v.b,v.c,v.e,v.u,v.s);return q;}
 HD U mat(U id){ // demand-driven shallow exposure; never copies an AST subtree
  for(U count=0;count<maxsteps&&!error;count++){
   if(id>=nt){fail(BAD_REFERENCE);return 0;}Term t=z.terms[id];
   if(t.tag==LOCAL&&t.s!=N){U pre=N,p=t.s;for(;p!=N;p=z.envs[p].next){Env v=z.envs[p];if(v.key==t.a)break;pre=env(v.key,v.value,pre);}if(p!=N){U forward=N;for(U q=pre;q!=N;q=z.envs[q].next)forward=env(z.envs[q].key,z.envs[q].value,forward);id=subst(z.envs[p].value,forward);continue;}return term(LOCAL,t.a,subst(t.b,t.s),N,N,N);}
   if(t.tag!=REF){if(t.s==N)return id;U a=t.a,b=t.b,c=t.c;switch(t.tag){case APP:case LAM:case PI:a=subst(a,t.s);b=subst(b,t.s);break;case LET:a=subst(a,t.s);b=subst(b,t.s);c=subst(c,t.s);break;case PROJ:c=subst(c,t.s);break;default:break;}return term(t.tag,a,b,c,t.e,t.u);}
   if(t.a>=in.nn){fail(BAD_REFERENCE);return 0;}Node n=in.nodes[t.a];
   if(n.tag==1){U p=t.e,k=n.a;while(p!=N&&k){p=z.envs[p].next;--k;}if(p==N){fail(LOOSE_VAR);return 0;}id=subst(z.envs[p].value,t.s);continue;}
   if(n.tag==11){id=closure(n.a,t.e,t.u);z.terms[id].s=t.s;continue;}
   if(n.tag==7)return term(LET,subst(closure(n.a,t.e,t.u),t.s),subst(closure(n.b,t.e,t.u),t.s),subst(closure(n.c,t.e,t.u),t.s));
   U a=n.a,b=n.b,c=n.c;
   switch(n.tag){
    case 2:return term(SORT,a,0,N,N,t.u,t.s); // source level, resolved by L operation
    case 3:return term(CONST,a,b,c,N,t.u,t.s);
    case 4:case 5:case 6:a=subst(closure(a,t.e,t.u),t.s);b=subst(closure(b,t.e,t.u),t.s);return term(n.tag,a,b,N,N,t.u);
    case 8:case 9:return term(n.tag,a,b);
    case 10:return term(PROJ,a,b,subst(closure(c,t.e,t.u),t.s));
    default:fail(UNSUPPORTED);return 0;
   }
  }fail(STEP_LIMIT);return 0;
 }
 HD U bind(U body,U binder,U val){if(binder!=N)return subst(body,env(binder,val,N));Term t=z.terms[body];if(t.tag!=REF){fail(UNSUPPORTED);return 0;}return subst(closure(t.a,env(N,val,t.e),t.u),t.s);}
 HD U neutral(U type){return term(LOCAL,fresh++,type);}
 HD U app(U f,U a){return term(APP,f,a);}
 HD bool push(U op,U x,U y=0,U mode=0){if(sp>=z.fcap){fail(FRAME_LIMIT);return false;}z.frames[sp++]={op,0,x,y,mode,0,0,0,0,0,0,0};if(sp>peaksp)peaksp=sp;return true;}
 HD void done(U v){ret=v;if(sp)--sp;}
 HD U constant(U d,U ue=N){return term(CONST,d,0,0,N,ue);}
 HD U const_ue(Term t){
  if(t.a>=in.nd){fail(BAD_REFERENCE);return N;}Decl d=in.decls[t.a];if(d.po>in.np||d.pn>in.np-d.po||t.b>in.nu||t.c>in.nu-t.b){fail(BAD_REFERENCE);return N;}if(t.c!=d.pn){fail(BAD_REFERENCE);return N;}
  // Each level is a source closure resolved by explicit L frames later. Store
  // source index and enclosing universe env as a pair encoded in a SORT term.
  U u=N;for(U k=0;k<d.pn;k++)u=env(in.params[d.po+k],term(SORT,in.ulists[t.b+k],0,N,N,t.u),u);return u;
 }
 HD U nth_arg(U t,U idx,U* head=nullptr,U* arity=nullptr){U n=0,q=mat(t);while(!error&&z.terms[q].tag==APP){++n;q=mat(z.terms[q].a);}if(head)*head=q;if(arity)*arity=n;if(idx>=n)return N;q=mat(t);for(U k=n-1;k>idx;k--)q=mat(z.terms[q].a);return z.terms[q].b;}
 HD U apply_prefix(U rhs,U t,U count){for(U k=0;k<count&&!error;k++)rhs=app(rhs,nth_arg(t,k));return rhs;}
 HD void run(U op,U x,U y=0){push(op,x,y);while(sp&&!error){if(++steps>maxsteps){fail(STEP_LIMIT);break;}Frame &f=z.frames[sp-1];
  if(f.op==L){ // symbolic universe instantiation with explicit continuations
   if(f.pc==0){if(f.x>=in.nl){fail(BAD_REFERENCE);continue;}Level l=in.levels[f.x];f.a=l.tag;f.b=l.b;if(l.tag==0){done(lv(0));continue;}if(l.tag==4){U p=f.y;while(p!=N&&z.envs[p].key!=l.a)p=z.envs[p].next;if(p==N){fail(LEVEL_PARAM);continue;}Term v=z.terms[z.envs[p].value];if(v.b==1){done(v.a);continue;}f.pc=3;push(L,v.a,v.u);continue;}f.pc=1;push(L,l.a,f.y);continue;}
   if(f.pc==3){done(ret);continue;}if(f.pc==1){f.c=ret;if(f.a==1){done(lv(1,ret));continue;}f.pc=2;push(L,f.b,f.y);continue;}done(lv(f.a,f.c,ret));continue;
  }
  if(f.op==LE){if(f.x==f.y){done(1);continue;}LVal a=z.levels[f.x],b=z.levels[f.y];if(f.pc==0){if(a.tag!=b.tag){done(0);continue;}if(a.tag==0){done(1);continue;}if(a.tag==4){done(a.a==b.a);continue;}f.pc=1;push(LE,a.a,b.a);continue;}if(!ret){done(0);continue;}if(f.pc==1&&(a.tag==2||a.tag==3)){f.pc=2;push(LE,a.b,b.b);continue;}done(ret);continue;}
  if(f.op==W){
   if(f.pc==0){f.x=mat(f.x);Term t=z.terms[f.x];
    if(t.tag==SORT){if(t.b==1){done(f.x);continue;}f.pc=9;push(L,t.a,t.u);continue;}
    if(t.tag==CONST){if(t.a>=in.nd){fail(BAD_REFERENCE);continue;}Decl d=in.decls[t.a];if(d.flags&1){fail(UNSAFE);continue;}if(d.kind==1||d.kind==2){U ue=const_ue(t);f.x=closure(d.value,N,ue);continue;}done(f.x);continue;}
    if(t.tag==LET){f.x=bind(t.c,N,t.b);continue;}
    if(t.tag==APP){f.pc=1;push(W,t.a);continue;}
    if(t.tag==PROJ){f.pc=4;push(W,t.c);continue;}done(f.x);continue;
   }
   if(f.pc==9){done(term(SORT,ret,1));continue;}
   if(f.pc==1){Term a=z.terms[ret],t=z.terms[f.x];if(a.tag==LAM){f.x=bind(a.b,a.c,t.b);f.pc=0;continue;}f.a=app(ret,t.b);U head,n;nth_arg(f.a,0,&head,&n);Term h=z.terms[head];if(h.tag!=CONST||h.a>=in.nd||in.decls[h.a].kind!=6){done(f.a);continue;}Decl d=in.decls[h.a];if(d.ro>in.nr||d.rn>in.nr-d.ro){fail(BAD_REFERENCE);continue;}U major=d.np+d.ni+d.nm+d.minor;if(n<=major){done(f.a);continue;}f.b=head;f.c=major;f.d=n;f.pc=2;push(W,nth_arg(f.a,major));continue;}
   if(f.pc==2){Term h=z.terms[f.b];Decl d=in.decls[h.a];if(d.ro>in.nr||d.rn>in.nr-d.ro){fail(BAD_REFERENCE);continue;}U major=ret;Term m=z.terms[major];if(m.tag==NAT){if(in.zero==N||in.succ==N){fail(UNSUPPORTED);continue;}major=m.a==0?constant(in.zero):app(constant(in.succ),term(NAT,m.a-1));}U ch,cn;nth_arg(major,0,&ch,&cn);Term ct=z.terms[ch];U rule=N;if(ct.tag==CONST)for(U k=0;k<d.rn;k++)if(in.rules[d.ro+k].ctor==ct.a){rule=d.ro+k;break;}if(rule==N){ // K/structure/quotient reductions require more rules: leave stuck.
      done(f.a);continue;}
    Rule r=in.rules[rule];if(cn<r.nfields){fail(UNSUPPORTED);continue;}U rhs=closure(r.rhs,N,const_ue(h));rhs=apply_prefix(rhs,f.a,d.np+d.nm+d.minor);for(U k=cn-r.nfields;k<cn;k++)rhs=app(rhs,nth_arg(major,k));for(U k=f.c+1;k<f.d;k++)rhs=app(rhs,nth_arg(f.a,k));f.x=rhs;f.pc=0;continue;}
   if(f.pc==4){Term p=z.terms[f.x];U h,n;nth_arg(ret,0,&h,&n);Term c=z.terms[h];if(c.tag==CONST&&c.a<in.nd&&in.decls[c.a].kind==5){Decl d=in.decls[c.a];if(d.ind!=p.a||p.b>=d.nf||d.np+p.b>=n){fail(UNSUPPORTED);continue;}f.x=nth_arg(ret,d.np+p.b);f.pc=0;continue;}done(term(PROJ,p.a,p.b,ret));continue;}
  }
  if(f.op==I){
   if(f.pc==0){f.x=mat(f.x);Term t=z.terms[f.x];
    if(t.tag==LOCAL){done(t.b);continue;}if(t.tag==SORT){f.pc=1;push(W,f.x);continue;}
    if(t.tag==CONST){if(t.a>=in.nd){fail(BAD_REFERENCE);continue;}Decl d=in.decls[t.a];if(d.flags&1){fail(UNSAFE);continue;}f.a=const_ue(t);f.i=0;f.pc=50;continue;}
    if(t.tag==NAT||t.tag==STRING){U d=t.tag==NAT?in.nat:in.string_;if(d==N){fail(UNSUPPORTED);continue;}done(constant(d));continue;}
    if(t.tag==LET){f.pc=40;push(I,t.a);continue;}
    if(t.tag==APP){f.pc=2;push(I,t.a);continue;}
    if(t.tag==LAM||t.tag==PI){f.a=t.a;f.pc=6;push(I,t.a);continue;}
    if(t.tag==PROJ){f.pc=12;push(I,t.c);continue;}fail(UNSUPPORTED);continue;
   }
   if(f.pc==50){Term t=z.terms[f.x];if(f.i==t.c){done(closure(in.decls[t.a].type,N,f.a));continue;}f.pc=51;push(L,in.ulists[t.b+f.i],t.u);continue;}
   if(f.pc==51){++f.i;f.pc=50;continue;}
   if(f.pc==40){f.pc=41;push(W,ret);continue;}
   if(f.pc==41){if(z.terms[ret].tag!=SORT){fail(NOT_SORT);continue;}f.pc=42;push(I,z.terms[f.x].b);continue;}
   if(f.pc==42){f.pc=43;push(E,ret,z.terms[f.x].a);continue;}
   if(f.pc==43){if(!ret){fail(NOT_EQUAL);continue;}Term t=z.terms[f.x];f.pc=44;push(I,bind(t.c,N,t.b));continue;}
   if(f.pc==44){done(ret);continue;}
   if(f.pc==1){Term t=z.terms[ret];done(term(SORT,lv(1,t.a),1));continue;}
   if(f.pc==2){f.pc=3;push(W,ret);continue;}
   if(f.pc==3){Term t=z.terms[ret];if(t.tag!=PI){fail(NOT_PI);continue;}f.a=ret;f.pc=4;push(I,z.terms[f.x].b);continue;}
   if(f.pc==4){f.pc=5;push(E,ret,z.terms[f.a].a);continue;}
   if(f.pc==5){if(!ret){fail(NOT_EQUAL);continue;}Term p=z.terms[f.a];done(bind(p.b,p.c,z.terms[f.x].b));continue;}
   if(f.pc==6){f.pc=7;push(W,ret);continue;}
   if(f.pc==7){Term s=z.terms[ret];if(s.tag!=SORT){fail(NOT_SORT);continue;}f.d=s.a;f.b=neutral(f.a);Term t=z.terms[f.x];f.pc=8;push(I,bind(t.b,t.c,f.b));continue;}
   if(f.pc==8){if(z.terms[f.x].tag==LAM){done(term(PI,f.a,ret,z.terms[f.b].a));continue;}f.pc=10;push(W,ret);continue;}
   if(f.pc==10){Term s=z.terms[ret];if(s.tag!=SORT){fail(NOT_SORT);continue;}done(term(SORT,lv(3,f.d,s.a),1));continue;}
   // Projection inference uses the genuine constructor telescope, binding
   // preceding fields to projections. Prop structures conservatively fallback.
   if(f.pc==12){f.pc=13;push(W,ret);continue;}
   if(f.pc==13){f.a=ret;Term p=z.terms[f.x];U h,n;nth_arg(ret,0,&h,&n);Term ht=z.terms[h];if(ht.tag!=CONST||ht.a!=p.a||ht.a>=in.nd){fail(UNSUPPORTED);continue;}Decl d=in.decls[ht.a];if(d.kind!=4||d.ctor>=in.nd||d.ni||d.flags&6||p.b>=in.decls[d.ctor].nf||n!=d.np){fail(UNSUPPORTED);continue;}f.b=closure(in.decls[d.ctor].type,N,const_ue(ht));f.i=0;f.j=d.np;f.k=p.b;f.pc=14;push(I,f.a);continue;}
   if(f.pc==14){f.pc=15;push(W,ret);continue;}
   if(f.pc==15){Term s=z.terms[ret];if(s.tag!=SORT||z.levels[s.a].tag==0){fail(UNSUPPORTED);continue;}f.pc=16;push(W,f.b);continue;}
   if(f.pc==16){Term p=z.terms[ret];if(p.tag!=PI){fail(NOT_PI);continue;}if(f.i==f.j+f.k){done(p.a);continue;}U arg=f.i<f.j?nth_arg(f.a,f.i):term(PROJ,z.terms[f.x].a,f.i-f.j,z.terms[f.x].c);f.b=bind(p.b,p.c,arg);++f.i;push(W,f.b);continue;}
  }
  if(f.op==E){
   if(f.pc==0){if(f.x==f.y){done(1);continue;}f.pc=1;push(W,f.x);continue;}
   if(f.pc==1){f.a=ret;f.pc=2;push(W,f.y);continue;}
   if(f.pc==2){f.b=ret;Term a=z.terms[f.a],b=z.terms[f.b];if(f.a==f.b){done(1);continue;}
    if(a.tag==SORT&&b.tag==SORT){f.pc=3;push(LE,a.a,b.a);continue;}
    if(a.tag==LOCAL&&b.tag==LOCAL&&a.a==b.a){done(1);continue;}
    if(a.tag==NAT&&b.tag==NAT&&a.a==b.a){done(1);continue;}
    if(a.tag==STRING&&b.tag==STRING&&a.a==b.a){done(1);continue;}
    if(a.tag==NAT||b.tag==NAT){Term n=a.tag==NAT?a:b;U other=a.tag==NAT?f.b:f.a,h,arity;nth_arg(other,0,&h,&arity);Term c=z.terms[h];if(c.tag==CONST&&c.a==in.zero&&arity==0&&n.a==0){done(1);continue;}if(c.tag==CONST&&c.a==in.succ&&arity==1&&n.a>0){f.pc=3;push(E,term(NAT,n.a-1),nth_arg(other,0),f.mode);continue;}}
    if(a.tag==CONST&&b.tag==CONST&&a.a==b.a&&a.c==b.c){f.i=0;f.pc=20;continue;}
    if(a.tag==APP&&b.tag==APP){f.pc=4;push(E,a.a,b.a,f.mode);continue;}
    if((a.tag==PI&&b.tag==PI)||(a.tag==LAM&&b.tag==LAM)){f.pc=6;push(E,a.a,b.a,f.mode);continue;}
    if(a.tag==PROJ&&b.tag==PROJ&&a.a==b.a&&a.b==b.b){f.pc=3;push(E,a.c,b.c,f.mode);continue;}
    if(a.tag==LAM||b.tag==LAM){f.c=a.tag==LAM?f.b:f.a;f.d=a.tag==LAM?0:1;f.pc=60;push(I,f.c);continue;}
    f.pc=30;continue;
   }
   if(f.pc==60){f.pc=61;push(W,ret);continue;}
   if(f.pc==61){Term other_type=z.terms[ret];if(other_type.tag!=PI){f.pc=30;continue;}Term lambda=z.terms[f.d?f.b:f.a];f.pc=62;push(E,lambda.a,other_type.a,f.mode);continue;}
   if(f.pc==62){if(!ret){f.pc=30;continue;}Term a=z.terms[f.a],b=z.terms[f.b],l=f.d?b:a;U v=neutral(l.a);U x=f.d?app(f.a,v):bind(a.b,a.c,v),y=f.d?bind(b.b,b.c,v):app(f.b,v);f.pc=3;push(E,x,y,f.mode);continue;}
   if(f.pc==3){if(ret){done(1);continue;}f.pc=30;continue;}
   if(f.pc==4){if(!ret){f.pc=30;continue;}f.pc=3;push(E,z.terms[f.a].b,z.terms[f.b].b,f.mode);continue;}
   if(f.pc==6){if(!ret){f.pc=30;continue;}Term a=z.terms[f.a],b=z.terms[f.b];U v=neutral(a.a);f.pc=3;push(E,bind(a.b,a.c,v),bind(b.b,b.c,v),f.mode);continue;}
   if(f.pc==20){Term a=z.terms[f.a];if(f.i==a.c){done(1);continue;}f.pc=21;push(L,in.ulists[a.b+f.i],a.u);continue;}
   if(f.pc==21){f.c=ret;Term b=z.terms[f.b];f.pc=22;push(L,in.ulists[b.b+f.i],b.u);continue;}
   if(f.pc==22){f.pc=23;push(LE,f.c,ret);continue;}
   if(f.pc==23){if(!ret){f.pc=30;continue;}++f.i;f.pc=20;continue;}
   if(f.pc==30){if(f.mode){done(0);continue;}f.pc=31;push(I,f.a);continue;}
   if(f.pc==31){f.c=ret;f.pc=32;push(I,ret);continue;}
   if(f.pc==32){f.pc=33;push(W,ret);continue;}
   if(f.pc==33){Term s=z.terms[ret];if(s.tag!=SORT||z.levels[s.a].tag!=0){done(0);continue;}f.pc=34;push(I,f.b);continue;}
   if(f.pc==34){f.pc=35;push(E,f.c,ret,1);continue;}if(f.pc==35){done(ret);continue;}
  }
  if(f.op==CHECK){if(f.x>=in.nd){fail(BAD_REFERENCE);continue;}Decl d=in.decls[f.x];if(f.pc==0){if(d.kind<1||d.kind>3||d.flags&1){fail(UNSUPPORTED);continue;}U ue=N;for(U k=0;k<d.pn;k++)ue=env(in.params[d.po+k],term(SORT,lv(4,in.params[d.po+k]),1),ue);f.a=closure(d.type,N,ue);f.b=closure(d.value,N,ue);f.pc=1;push(I,f.a);continue;}if(f.pc==1){f.pc=2;push(W,ret);continue;}if(f.pc==2){if(z.terms[ret].tag!=SORT){fail(NOT_SORT);continue;}if(d.kind==2&&z.levels[z.terms[ret].a].tag!=0){fail(UNSUPPORTED);continue;}f.pc=3;push(I,f.b);continue;}if(f.pc==3){f.pc=4;push(E,ret,f.a);continue;}if(!ret){fail(NOT_EQUAL);continue;}done(1);continue;}
 } }
};
HD Answer execute(Input in,Scratch scratch,U op,U x,U y,U maxsteps){Machine m{in,scratch,0,0,0,0,0,0,0,0,maxsteps,0};m.lv(0);m.run(op,x,y);return {m.error==0&&m.ret!=0,m.error,m.steps,m.nt,m.peaksp,m.ne,m.nl};}
extern "C" void closure_check_cpu(Input in,Scratch z,const U* queries,U nq,Answer* answers,U maxsteps){for(U q=0;q<nq;q++)answers[q]=execute(in,z,CHECK,queries[q],0,maxsteps);}
// Dynamic operation API: closed exported expression IDs, kernel configuration.
// Results are caller-owned closure values, not native Lean Expr objects.
extern "C" Answer closure_operation_cpu(Input in,Scratch z,U op,U x,U y,U maxsteps,U* result){Machine m{in,z,0,0,0,0,0,0,0,0,maxsteps,0};m.lv(0);if(op!=W&&op!=I&&op!=E)m.fail(UNSUPPORTED);U a=m.closure(x),b=m.closure(y);m.run(op,a,b);if(op==E&&!m.ret)m.fail(NOT_EQUAL);if(op==W)m.fail(PARTIAL_WHNF);*result=m.ret;return {m.error==0,m.error,m.steps,m.nt,m.peaksp,m.ne,m.nl};}
#ifdef __CUDACC__
extern "C" __global__ void closure_check_device(Input in,Term* terms,Env* envs,LVal* levels,Frame* frames,U cap,U fcap,const U* queries,U nq,Answer* answers,U maxsteps){U q=blockIdx.x*blockDim.x+threadIdx.x;if(q>=nq)return;Scratch z{terms+(uint64_t)q*cap,envs+(uint64_t)q*cap,levels+(uint64_t)q*cap,frames+(uint64_t)q*fcap,cap,fcap};answers[q]=execute(in,z,CHECK,queries[q],0,maxsteps);}
extern "C" __global__ void closure_operations_device(Input in,Term* terms,Env* envs,LVal* levels,Frame* frames,U cap,U fcap,const U* ops,const U* xs,const U* ys,U nq,Answer* answers,U* results,U maxsteps){U q=blockIdx.x*blockDim.x+threadIdx.x;if(q>=nq)return;Scratch z{terms+(uint64_t)q*cap,envs+(uint64_t)q*cap,levels+(uint64_t)q*cap,frames+(uint64_t)q*fcap,cap,fcap};Machine m{in,z,0,0,0,0,0,0,0,0,maxsteps,0};m.lv(0);U op=ops[q];if(op!=W&&op!=I&&op!=E)m.fail(UNSUPPORTED);m.run(op,m.closure(xs[q]),m.closure(ys[q]));if(op==E&&!m.ret)m.fail(NOT_EQUAL);if(op==W)m.fail(PARTIAL_WHNF);results[q]=m.ret;answers[q]={m.error==0,m.error,m.steps,m.nt,m.peaksp,m.ne,m.nl};}
#endif
