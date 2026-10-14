// SPDX-License-Identifier: Apache-2.0
// Separate native-compatible beta/zeta packet ABI. Not frozen closure W.
#pragma once
#include <stdint.h>
#ifdef __CUDACC__
#define CN_HD __host__ __device__
#else
#define CN_HD
#endif
struct CNNode {uint32_t kind,a,b,c;};
struct CNClosure {uint32_t node,env;};
struct CNEnv {uint32_t node,env,next;};
struct CNAnswer {uint32_t reason,node,env,envCount,argPeak,steps,terminalKind;};
static constexpr uint32_t CN_NONE=0xffffffffu;
// Input is an immutable source-native AST mapping, captured only after host
// eligibility excludes loose variables. Untouched free/metavariable/level
// identities are preserved; any demanded stateful head declines. No mutation.
CN_HD inline CNAnswer cn_reduce(const CNNode* nodes,uint32_t nn,uint32_t root,CNEnv* envs,CNClosure* args,uint32_t cap,uint32_t maxsteps){
 CNClosure t{root,CN_NONE};uint32_t nenv=0,narg=0,peak=0,steps=0,why=0,terminal=CN_NONE;
 while(!why){if(steps>=maxsteps){why=1;break;}++steps;if(t.node>=nn){why=5;break;}CNNode n=nodes[t.node];
  if(n.kind==0){uint32_t e=t.env,k=n.a;while(e!=CN_NONE&&k){if(steps>=maxsteps){why=1;break;}++steps;if(e>=nenv){why=5;break;}e=envs[e].next;--k;}if(why)break;if(e==CN_NONE){why=3;break;}if(e>=nenv){why=5;break;}t={envs[e].node,envs[e].env};continue;}
  if(n.kind==10){t.node=n.a;continue;}
  if(n.kind==8){if(nenv>=cap){why=2;break;}envs[nenv]={n.a,t.env,t.env};t={n.b,nenv++};continue;}
  if(n.kind==5){if(narg>=cap){why=2;break;}args[narg++]={n.b,t.env};if(narg>peak)peak=narg;t.node=n.a;continue;}
  if(n.kind==6){if(!narg){terminal=n.kind;break;}if(nenv>=cap){why=2;break;}CNClosure a=args[--narg];envs[nenv]={a.node,a.env,t.env};t={n.a,nenv++};continue;}
  if(n.kind==3||n.kind==7||n.kind==9){if(narg){why=4;break;}terminal=n.kind;break;}
  why=4;break;
 }
 return {why,t.node,t.env,nenv,peak,steps,terminal};
}
