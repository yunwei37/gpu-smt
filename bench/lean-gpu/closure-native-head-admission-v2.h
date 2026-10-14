// SPDX-License-Identifier: Apache-2.0
#pragma once
#include <lean/lean.h>
#include "closure-native-head-admission-v1.h"

// Same conservative rejection as the packed walk, on borrowed native Exprs.
// No argument evaluation, environment lookup, allocation or successful result.
inline bool cn_native_definitely_unsupported_head(b_lean_obj_arg expr,
                                                  uint32_t maxsteps) {
    lean_object* node = expr;
    uint32_t pending = 0;
    for (uint32_t step = 0; step < maxsteps; ++step) {
        if (!node || lean_is_scalar(node)) return false;
        switch (lean_obj_tag(node)) {
        case 0: return false;                         // demanded bound variable
        case 10: node = lean_ctor_get(node, 1); break; // metadata Expr
        case 8: node = lean_ctor_get(node, 3); break;  // let body
        case 5:
            if (pending == UINT32_MAX) return false;
            ++pending; node = lean_ctor_get(node, 0); break;
        case 6:
            if (!pending) return false;
            --pending; node = lean_ctor_get(node, 2); break;
        case 3: case 7: case 9: return pending != 0;
        default: return true;
        }
    }
    return false;
}
