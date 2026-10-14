// Experimental conservative dependent-term checker, CPU/CUDA shared source.
// An undecided result is NOT rejection: the official CPU checker must handle it.
// No declaration is discharged by a hash or metadata-only predicate.
#ifndef __CUDACC__
#define __device__
#define __global__
#endif
typedef unsigned int U;
static const U LOCAL=0x80000000u, NONE=0xffffffffu;
enum { BAD=0, VAR=1, SORT=2, CONST=3, APP=4, LAM=5, PI=6, LET=7, NAT=8, STR=9 };
// flags: Sort's a is a numeric universe; Const's b refers to local literal levels.
struct Node { U tag,a,b,c,flags; };
struct Level { U tag,a,b; }; // zero/succ/max/imax/param
struct Decl { U kind,name,type,value,param_base,param_count; };
struct Graph { const Node *nodes; const Level *levels; const Decl *decls;
  const U *ulists,*params; U nn,nl,nd,nat_decl,string_decl; };
struct Answer { U verified,reason,steps,nodes; };
// Per-declaration working storage. Capacity/recursion exhaustion is fallback.
static const U CONTEXT=256, CACHE=512;
struct Machine {
  Graph g; Node *local; U *literal;
  U capacity,used,lit_used,current,steps,error;
  U context[CONTEXT],ctx_count,keys[CACHE],cached[CACHE];
  __device__ bool tick(U depth) {
    if (error) return false;
    if (depth>64 || ++steps>500000) { error=1; return false; }
    return true;
  }
  __device__ Node get(U i) {
    if ((i&LOCAL) && (i&~LOCAL)<used) return local[i&~LOCAL];
    if (!(i&LOCAL) && i<g.nn) return g.nodes[i];
    error=2; return {BAD,0,0,0,0};
  }
  __device__ U make(Node n) {
    if (used>=capacity) { error=3; return NONE; }
    U i=used++;local[i]=n;return i|LOCAL;
  }
  __device__ U sort(U n) { return make({SORT,n,0,0,1}); }
  __device__ U level(U id,const U *names,const U *values,U n,U depth) {
    if (!tick(depth) || id>=g.nl) {error=4;return 0;}
    Level l=g.levels[id];
    if (l.tag==0) return 0;
    if (l.tag==1) { U v=level(l.a,names,values,n,depth+1);if(v==NONE){error=4;return 0;}return v+1; }
    if (l.tag==2 || l.tag==3) {
      U a=level(l.a,names,values,n,depth+1),b=level(l.b,names,values,n,depth+1);
      return l.tag==3 && b==0 ? 0 : (a>b?a:b);
    }
    if (l.tag==4) {for(U i=0;i<n;i++)if(names[i]==l.a)return values[i];}
    error=4;return 0;
  }
  __device__ U uvalue(Node n,U i,const U *names,const U *values,U k,U depth) {
    if (i>=n.c) {error=4;return 0;}
    if(n.flags&1) {
      if(n.b+i>=lit_used){error=4;return 0;}return literal[n.b+i];
    }
    return level(g.ulists[n.b+i],names,values,k,depth+1);
  }
  __device__ U instantiate(U e,const U *names,const U *values,U k,U depth) {
    if(!tick(depth))return NONE;
    Node n=get(e);
    if(n.tag==SORT) return n.flags&1 ? e : sort(level(n.a,names,values,k,depth+1));
    if(n.tag==CONST) {
      if(lit_used+n.c>capacity*4){error=3;return NONE;}
      U begin=lit_used;lit_used+=n.c;
      for(U i=0;i<n.c;i++)literal[begin+i]=uvalue(n,i,names,values,k,depth+1);
      return make({CONST,n.a,begin,n.c,1});
    }
    if(n.tag==APP || n.tag==LAM || n.tag==PI) {
      n.a=instantiate(n.a,names,values,k,depth+1);
      n.b=instantiate(n.b,names,values,k,depth+1);return make(n);
    }
    if(n.tag==LET) {
      n.a=instantiate(n.a,names,values,k,depth+1);
      n.b=instantiate(n.b,names,values,k,depth+1);
      n.c=instantiate(n.c,names,values,k,depth+1);return make(n);
    }
    if(n.tag==BAD){error=5;return NONE;}
    return e;
  }
  __device__ U shift(U e,U amount,U cutoff,U depth) {
    if(!tick(depth))return NONE;Node n=get(e);
    if(n.tag==VAR) {if(n.a>=cutoff){if(n.a+amount<n.a){error=6;return NONE;}n.a+=amount;return make(n);}return e;}
    if(n.tag==APP){n.a=shift(n.a,amount,cutoff,depth+1);n.b=shift(n.b,amount,cutoff,depth+1);return make(n);}
    if(n.tag==PI || n.tag==LAM){n.a=shift(n.a,amount,cutoff,depth+1);n.b=shift(n.b,amount,cutoff+1,depth+1);return make(n);}
    if(n.tag==LET){n.a=shift(n.a,amount,cutoff,depth+1);n.b=shift(n.b,amount,cutoff,depth+1);n.c=shift(n.c,amount,cutoff+1,depth+1);return make(n);}
    if(n.tag==BAD){error=5;return NONE;}return e;
  }
  // Remove the binder at `depth`, replacing it by value lifted into that scope.
  __device__ U substitute(U e,U value,U bind,U depth) {
    if(!tick(depth))return NONE;Node n=get(e);
    if(n.tag==VAR){if(n.a==bind)return shift(value,bind,0,depth+1);if(n.a>bind){n.a--;return make(n);}return e;}
    if(n.tag==APP){n.a=substitute(n.a,value,bind,depth+1);n.b=substitute(n.b,value,bind,depth+1);return make(n);}
    if(n.tag==PI || n.tag==LAM){n.a=substitute(n.a,value,bind,depth+1);n.b=substitute(n.b,value,bind+1,depth+1);return make(n);}
    if(n.tag==LET){n.a=substitute(n.a,value,bind,depth+1);n.b=substitute(n.b,value,bind,depth+1);n.c=substitute(n.c,value,bind+1,depth+1);return make(n);}
    if(n.tag==BAD){error=5;return NONE;}return e;
  }
  __device__ U constant_type(U e,Node n,U depth) {
    if(n.a>=current || n.a>=g.nd){error=7;return NONE;}
    Decl d=g.decls[n.a];if(d.param_count!=n.c || n.c>32){error=4;return NONE;}
    U slot=e%CACHE;
    if(!(e&LOCAL) && keys[slot]==e)return cached[slot];
    U values[32];for(U i=0;i<n.c;i++)values[i]=uvalue(n,i,0,0,0,depth+1);
    U t=instantiate(d.type,g.params+d.param_base,values,n.c,depth+1);
    if(!(e&LOCAL) && !error){keys[slot]=e;cached[slot]=t;}
    return t;
  }
  __device__ U whnf(U e,U depth) {
    if(!tick(depth))return NONE;Node n=get(e);
    if(n.tag==LET)return whnf(substitute(n.c,n.b,0,depth+1),depth+1);
    if(n.tag==CONST && n.a<current && n.a<g.nd && g.decls[n.a].kind==1) {
      Decl d=g.decls[n.a];if(d.param_count!=n.c || n.c>32){error=4;return NONE;}
      U values[32];for(U i=0;i<n.c;i++)values[i]=uvalue(n,i,0,0,0,depth+1);
      return whnf(instantiate(d.value,g.params+d.param_base,values,n.c,depth+1),depth+1);
    }
    if(n.tag==APP){U f=whnf(n.a,depth+1);Node fn=get(f);
      if(fn.tag==LAM)return whnf(substitute(fn.b,n.b,0,depth+1),depth+1);
      return f==n.a ? e : make({APP,f,n.b,0,0});}
    return e;
  }
  __device__ bool equal(U a,U b,U depth) {
    if(!tick(depth))return false;if(a==b)return true;
    // Delta/beta/zeta conversion only. Missing iota/eta/proof irrelevance is
    // conservative fallback, not a claim that the expressions are unequal.
    a=whnf(a,depth+1);b=whnf(b,depth+1);if(error)return false;if(a==b)return true;
    Node x=get(a),y=get(b);if(x.tag!=y.tag)return false;
    if(x.tag==VAR || x.tag==NAT || x.tag==STR)return x.a==y.a;
    if(x.tag==SORT){U l=x.flags&1?x.a:level(x.a,0,0,0,depth+1),r=y.flags&1?y.a:level(y.a,0,0,0,depth+1);return !error && l==r;}
    if(x.tag==CONST){if(x.a!=y.a || x.c!=y.c)return false;for(U i=0;i<x.c;i++)if(uvalue(x,i,0,0,0,depth+1)!=uvalue(y,i,0,0,0,depth+1))return false;return !error;}
    if(x.tag==APP || x.tag==LAM || x.tag==PI)return equal(x.a,y.a,depth+1)&&equal(x.b,y.b,depth+1);
    return false;
  }
  __device__ U sort_of(U e,U depth){U t=whnf(infer(e,depth+1),depth+1);Node n=get(t);
    if(n.tag!=SORT){error=8;return 0;}return n.flags&1?n.a:level(n.a,0,0,0,depth+1);}
  __device__ U infer(U e,U depth) {
    if(!tick(depth))return NONE;Node n=get(e);
    if(n.tag==VAR){if(n.a>=ctx_count){error=6;return NONE;}return shift(context[ctx_count-1-n.a],n.a+1,0,depth+1);}
    if(n.tag==SORT){U l=n.flags&1?n.a:level(n.a,0,0,0,depth+1);if(l==NONE){error=4;return NONE;}return sort(l+1);}
    if(n.tag==CONST)return constant_type(e,n,depth+1);
    if(n.tag==NAT || n.tag==STR){U d=n.tag==NAT?g.nat_decl:g.string_decl;
      if(d==NONE || d>=current){error=7;return NONE;}return make({CONST,d,0,0,1});}
    if(n.tag==APP){U ft=whnf(infer(n.a,depth+1),depth+1);Node f=get(ft);
      if(f.tag!=PI){error=9;return NONE;}
      U at=infer(n.b,depth+1);if(!equal(at,f.a,depth+1)){error=10;return NONE;}
      return substitute(f.b,n.b,0,depth+1);}
    if(n.tag==LAM || n.tag==PI){U dom_level=sort_of(n.a,depth+1);
      if(ctx_count>=CONTEXT){error=1;return NONE;}context[ctx_count++]=n.a;
      if(n.tag==LAM){U bt=infer(n.b,depth+1);ctx_count--;return make({PI,n.a,bt,0,0});}
      U body_level=sort_of(n.b,depth+1);ctx_count--;return sort(body_level==0?0:(dom_level>body_level?dom_level:body_level));}
    if(n.tag==LET){sort_of(n.a,depth+1);U vt=infer(n.b,depth+1);
      if(!equal(vt,n.a,depth+1)){error=10;return NONE;}
      return infer(substitute(n.c,n.b,0,depth+1),depth+1);}
    error=5;return NONE;
  }
  __device__ Answer check(U declaration) {
    current=declaration;used=lit_used=ctx_count=steps=error=0;
    for(U i=0;i<CACHE;i++)keys[i]=NONE;
    if(current>=g.nd)return {0,7,0,0};Decl d=g.decls[current];
    // Polymorphic local declarations and inductive construction use CPU.
    if(d.param_count || (d.kind!=1 && d.kind!=2 && d.kind!=3))return {0,11,0,0};
    U type_level=sort_of(d.type,0);
    if(d.kind==2 && type_level!=0)return {0,12,steps,used};
    U inferred=infer(d.value,0);
    bool ok=equal(inferred,d.type,0);
    return {ok && !error ? 1u:0u,error?error:(ok?0u:10u),steps,used};
  }
};
#ifdef __CUDACC__
extern "C" __global__ void check_declarations(const Node *nodes,const Level *levels,
 const Decl *decls,const U *ulists,const U *params,const U *queries,U nq,
 U nn,U nl,U nd,U nat_decl,U string_decl,Node *work,U *literal,U capacity,Answer *answers) {
 U i=blockIdx.x*blockDim.x+threadIdx.x;if(i>=nq)return;
 Machine m;m.g={nodes,levels,decls,ulists,params,nn,nl,nd,nat_decl,string_decl};
 m.local=work+i*capacity;m.literal=literal+i*capacity*4;m.capacity=capacity;
 answers[i]=m.check(queries[i]);
}
#else
extern "C" void check_declarations_cpu(const Node *nodes,const Level *levels,
 const Decl *decls,const U *ulists,const U *params,const U *queries,U nq,
 U nn,U nl,U nd,U nat_decl,U string_decl,Node *work,U *literal,U capacity,Answer *answers) {
 for(U i=0;i<nq;i++){Machine m;m.g={nodes,levels,decls,ulists,params,nn,nl,nd,nat_decl,string_decl};
 m.local=work;m.literal=literal;m.capacity=capacity;answers[i]=m.check(queries[i]);}
}
#endif
