// SPDX-License-Identifier: Apache-2.0
// Tiny development controls, not a benchmark or independent kernel oracle.
#include "closure-checker.cu"
#include <vector>
#include <stdio.h>
#include <stdlib.h>
struct Harness {
 std::vector<Term> ts;std::vector<Env> es;std::vector<LVal> ls;std::vector<Frame> fs;
 Node nodes[64]{};Level levels[16]{};Decl ds[16]{};Rule rs[8]{};U us[16]{};U ps[16]{};
 Harness():ts(32768),es(32768),ls(32768),fs(2048){levels[0]={0,0,0};levels[1]={1,0,0};levels[2]={4,101,0};levels[3]={1,2,0};}
 Machine machine(){Input in{nodes,levels,ds,rs,us,ps,64,16,16,8,0,N,1,2,16,16};Scratch z{ts.data(),es.data(),ls.data(),fs.data(),32768,2048};Machine m{in,z,0,0,0,0,0,0,0,0,1000000,0};m.lv(0);return m;}
};
static unsigned count=0;
void expect(bool b,const char* name){if(!b){fprintf(stderr,"FAILED: %s\n",name);exit(1);}printf("PASS %s\n",name);++count;}
int main(){
 Harness h;
 // Original closure binder environments: lambda x => lambda y => x.
 h.nodes[0]={2,1,0,0,0};h.nodes[1]={1,1,0,0,0};h.nodes[2]={5,0,1,0,0};h.nodes[3]={5,0,2,0,0};
 {auto m=h.machine();U v=m.term(NAT,17),w=m.term(NAT,31);m.run(W,m.app(m.app(m.closure(3),v),w));expect(!m.error&&m.z.terms[m.ret].tag==NAT&&m.z.terms[m.ret].a==17,"nested original closure beta/binder ordering");}
 {auto m=h.machine();U s=m.term(SORT,m.lv(1,0),1),x=m.neutral(s),y=m.neutral(s);U body=m.app(x,y);U lambda=m.term(LAM,s,body,m.z.terms[x].a);U out=m.bind(lambda==N?0:m.z.terms[lambda].b,m.z.terms[lambda].c,m.term(NAT,41));out=m.subst(out,m.env(m.z.terms[y].a,m.term(NAT,43),N));m.run(W,out);Term a=m.z.terms[m.ret];expect(!m.error&&a.tag==APP&&m.z.terms[m.mat(a.a)].a==41&&m.z.terms[m.mat(a.b)].a==43,"delayed neutral substitution composition");}
 // Symbolic universe u+1 instantiated through declaration constant levels.
 h.ds[3]={7,201,4,N,0,1};h.ps[0]=101;h.us[0]=1;h.nodes[4]={2,3,0,0,0};h.nodes[5]={3,3,0,1,0};
 {auto m=h.machine();m.run(I,m.closure(5));m.run(W,m.ret);U l=m.z.terms[m.ret].a;expect(!m.error&&m.z.levels[l].tag==1&&m.z.levels[m.z.levels[l].a].tag==1,"symbolic universe substitution to concrete successor");}
 {auto m=h.machine();U env=m.env(101,m.term(SORT,m.lv(4,777),1),N);m.run(L,3,env);expect(!m.error&&m.z.levels[m.ret].tag==1&&m.z.levels[m.z.levels[m.ret].a].a==777,"symbolic universe preserved under instantiation");}
 {auto m=h.machine();m.run(L,2,N);expect(m.error==LEVEL_PARAM,"undeclared universe parameter first-error fallback");}
 // Identity over Type, inferred dependent Pi uses neutral abstraction.
 h.nodes[6]={1,0,0,0,0};h.nodes[7]={5,0,6,0,0};
 {auto m=h.machine();m.run(I,m.closure(7));Term p=m.z.terms[m.ret];expect(!m.error&&p.tag==PI&&m.z.terms[m.mat(p.b)].tag==SORT,"lambda inference builds delayed Pi body");}
 // Original let annotation must be checked before zeta during inference.
 h.nodes[8]={8,4,0,0,0};h.nodes[9]={7,0,8,6,0};h.ds[0]={4,300,0,N,0,0};
 {auto m=h.machine();m.run(I,m.closure(9));expect(m.error!=OK,"invalid let annotation cannot discharge after zeta");}
 {auto m=h.machine();m.run(W,m.closure(9));expect(!m.error&&m.z.terms[m.ret].tag==NAT&&m.z.terms[m.ret].a==4,"WHNF zeta demand separate from checking");}
 // Nat recursor computation from constructor fields, including extra args.
 h.ds[1]={5,301,0,N,0,0,0,0,0};h.ds[2]={5,302,0,N,0,0,0,1,0};
 h.ds[4]={6,303,0,N,0,0,0,0,0,0,0,0,0,2};h.rs[0]={1,0,8};h.rs[1]={2,1,7};
 {auto m=h.machine();U rec=m.constant(4),major=m.app(m.constant(2),m.term(NAT,19));m.run(W,m.app(rec,major));expect(!m.error&&m.z.terms[m.ret].tag==NAT&&m.z.terms[m.ret].a==19,"recursor actual iota rule and field binding");}
 {auto m=h.machine();m.run(W,m.app(m.constant(4),m.term(NAT,0)));expect(!m.error&&m.z.terms[m.ret].tag==NAT&&m.z.terms[m.ret].a==4,"recursor literal major converted to zero constructor");}
 {auto m=h.machine();m.run(E,m.term(NAT,2),m.app(m.constant(2),m.term(NAT,1)));expect(!m.error&&m.ret==1,"Nat literal/constructor conversion");}
 // Projection reduction must honor the actual parent inductive and field offset.
 h.ds[5]={5,401,0,N,0,0,1,2,6};
 {auto m=h.machine();U c=m.app(m.app(m.app(m.constant(5),m.term(NAT,8)),m.term(NAT,11)),m.term(NAT,13));m.run(W,m.term(PROJ,6,1,c));expect(!m.error&&m.z.terms[m.ret].tag==NAT&&m.z.terms[m.ret].a==13,"projection metadata parameter/field offset");}
 {auto m=h.machine();U c=m.app(m.app(m.app(m.constant(5),m.term(NAT,8)),m.term(NAT,11)),m.term(NAT,13));m.run(W,m.term(PROJ,7,1,c));expect(m.error==UNSUPPORTED,"projection wrong inductive conservative fallback");}
 // Opaque values are checked but do not unfold in kernel WHNF.
 h.ds[6]={3,501,0,8,0,0};h.ds[7]={1,502,0,8,0,0};h.ds[8]={2,503,0,8,0,0};
 {auto m=h.machine();m.run(W,m.constant(6));expect(!m.error&&m.z.terms[m.ret].tag==CONST,"opaque constant kernel transparency");}
 {auto m=h.machine();m.run(W,m.constant(7));expect(!m.error&&m.z.terms[m.ret].tag==NAT,"definition delta");}
 {auto m=h.machine();m.run(W,m.constant(8));expect(!m.error&&m.z.terms[m.ret].tag==NAT,"theorem delta at kernel configuration");}
 {auto m=h.machine();U s=m.term(SORT,m.lv(1,0),1),x=m.neutral(s),f=m.neutral(m.term(PI,s,s,m.z.terms[x].a));U lam=m.term(LAM,s,m.app(f,x),m.z.terms[x].a);m.run(E,lam,f);expect(!m.error&&m.ret==1,"function eta conversion");}
 // Proof irrelevance over the same opaque proposition.
 h.ds[9]={7,601,10,N,0,0};h.nodes[10]={2,0,0,0,0};h.nodes[11]={3,9,0,0,0};h.ds[10]={7,602,11,N,0,0};h.ds[11]={7,603,11,N,0,0};
 {auto m=h.machine();m.run(E,m.constant(10),m.constant(11));expect(!m.error&&m.ret==1,"proof irrelevance same proposition");}
 {auto m=h.machine();m.z.fcap=1;m.run(I,m.closure(7));expect(m.error==FRAME_LIMIT,"explicit continuation capacity fallback");}
 // Complete safe definition checks type formation, body and conversion.
 h.nodes[12]={6,0,0,0,0};h.ds[12]={1,701,12,7,0,0};
 {auto m=h.machine();m.run(CHECK,12);expect(!m.error&&m.ret==1,"safe complete identity declaration check");}
 h.ds[12].value=8;
 {auto m=h.machine();m.run(CHECK,12);expect(m.error!=OK,"ill-typed complete declaration fallback");}
 printf("%u development controls passed; no GPU executed, no benchmark result\n",count);
}
