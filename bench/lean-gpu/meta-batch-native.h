// SPDX-License-Identifier: Apache-2.0
#pragma once
#include <lean/lean.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
/* Equation Array (Expr × Expr) is retained by the caller. Context arguments
   remain opaque native MetaM arguments. No Lean pointer may enter GPU memory.
   The provider owns packing/definitions/reduction and actual device evidence.
   Fill 1 only for positively established supported equality; 0 is unknown.
   Return 0 when unavailable. Never change the native contexts/assignments. */
int gpu_meta_batch_run(b_lean_obj_arg equations, const char *mode,
                      uint8_t *answers, size_t count,
                      b_lean_obj_arg a, b_lean_obj_arg b,
                      b_lean_obj_arg c, b_lean_obj_arg d);
#ifdef __cplusplus
}
#endif
