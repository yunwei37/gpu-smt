// SPDX-License-Identifier: Apache-2.0
// Native caller/provider bridge. Caller owns packet until destroy, including
// across device transfer/synchronization and quotation. No Lean pointer goes
// to a GPU: only CNNode/CNEnv/CNClosure/CNAnswer POD records are transported.
#pragma once
#include <lean/lean.h>
#include "closure-native-packed-v2.h"
struct ClosureNativePacket;
extern "C" {
ClosureNativePacket* closure_native_v2_packet_prepare(b_lean_obj_arg e,uint32_t cap,uint32_t maxsteps);
const CNNode* closure_native_v2_packet_nodes(const ClosureNativePacket*,uint32_t* nn);
uint32_t closure_native_v2_packet_error(const ClosureNativePacket*);
void closure_native_v2_packet_cpu(const ClosureNativePacket*,CNEnv*,CNClosure*,CNAnswer*);
// Validation/readback is not a substitute for independently qualifying device
// answers. Malformed/unsupported results decline; caller may demand CPU match.
lean_obj_res closure_native_v2_packet_quote(const ClosureNativePacket*,const CNAnswer*,const CNEnv*);
void closure_native_v2_packet_destroy(ClosureNativePacket*);
}
