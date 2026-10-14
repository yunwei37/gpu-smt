// SPDX-License-Identifier: Apache-2.0
#pragma once
#include "closure-native-packed-v2.h"

// Only prove that the packed reducer must decline. A demanded bound variable
// needs an environment lookup: leave that and every uncertain case unchanged.
// This walk does not evaluate arguments or construct a successful result.
inline bool cn_definitely_unsupported_head(const CNNode* nodes, uint32_t nn,
                                          uint32_t maxsteps) {
    uint32_t node = 0, pending = 0;
    for (uint32_t step = 0; step < nn && step < maxsteps; ++step) {
        if (node >= nn) return false;
        CNNode n = nodes[node];
        switch (n.kind) {
        case 0: return false;                         // environment-dependent
        case 10: node = n.a; break;                   // metadata
        case 8: node = n.b; break;                    // let body
        case 5: ++pending; node = n.a; break;          // application spine
        case 6:
            if (!pending) return false;              // usable lambda head
            --pending; node = n.a; break;             // beta body
        case 3: case 7: case 9: return pending != 0;   // applied terminal head
        default: return true;                        // unsupported demanded head
        }
    }
    return false;
}
