// SPDX-License-Identifier: Apache-2.0
#include "closure-native-packed.h"
// One packet operation. Context/transport ownership belongs to a future native
// provider; compilation alone does not execute or establish device engagement.
extern "C" __global__ void closure_native_reduce_device(const CNNode* nodes,uint32_t nn,uint32_t root,CNEnv* envs,CNClosure* args,uint32_t cap,uint32_t maxsteps,CNAnswer* answer){
 if(blockIdx.x==0&&threadIdx.x==0)*answer=cn_reduce(nodes,nn,root,envs,args,cap,maxsteps);
}
