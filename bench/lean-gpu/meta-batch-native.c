// SPDX-License-Identifier: Apache-2.0
// Native argument-frontier bridge. The optional reduction provider is separate;
// absence means stock fallback, never fabricated device engagement.
#include "meta-batch-native.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <inttypes.h>
#include <stdatomic.h>

extern lean_obj_res gpu_meta_batch_collect(lean_obj_arg, lean_obj_arg);
extern lean_obj_res gpu_meta_batch_return_true(
    lean_obj_arg, lean_obj_arg, lean_obj_arg,
    lean_obj_arg, lean_obj_arg, lean_obj_arg);
extern lean_obj_res gpu_meta_batch_original_defeq(
    lean_obj_arg, lean_obj_arg, lean_obj_arg,
    lean_obj_arg, lean_obj_arg, lean_obj_arg);
#pragma weak gpu_meta_batch_run

struct batch_frame {
    lean_object *equations;
    uint8_t *answers;
    size_t count;
    struct batch_frame *previous;
};
static _Thread_local struct batch_frame *active;
static atomic_uint_fast64_t frontiers, equations, positives, consumed;

static int ready(lean_object *t, lean_object *s) {
    for (struct batch_frame *f = active; f; f = f->previous) {
        for (size_t i = 0; i < f->count; ++i) {
            if (f->answers[i] != 1) continue;
            lean_object *pair = lean_array_cptr(f->equations)[i];
            lean_object *left = lean_ctor_get(pair, 0);
            lean_object *right = lean_ctor_get(pair, 1);
            if ((t == left && s == right) || (t == right && s == left))
                return 1;
        }
    }
    return 0;
}

LEAN_EXPORT lean_obj_res lean_is_expr_def_eq(
        lean_obj_arg t, lean_obj_arg s, lean_obj_arg a,
        lean_obj_arg b, lean_obj_arg c, lean_obj_arg d) {
    if (active && ready(t, s)) {
        atomic_fetch_add(&consumed, 1);
        return gpu_meta_batch_return_true(t, s, a, b, c, d);
    }
    const char *mode = getenv("LEAN_GPU_META_BATCH_MODE");
    if (active || !gpu_meta_batch_run || !mode ||
        (strcmp(mode, "cpu") && strcmp(mode, "gpu")))
        return gpu_meta_batch_original_defeq(t, s, a, b, c, d);

    // Retain independently: the compiled collector consumes its input references.
    lean_inc(t); lean_inc(s);
    lean_object *pairs = gpu_meta_batch_collect(t, s);
    size_t count = lean_array_size(pairs);
    // A singleton repeats the already failed scalar-device constructor.
    if (count < 2) {
        lean_dec(pairs);
        return gpu_meta_batch_original_defeq(t, s, a, b, c, d);
    }
    uint8_t *answers = calloc(count, sizeof(uint8_t));
    if (!answers) {
        lean_dec(pairs);
        return gpu_meta_batch_original_defeq(t, s, a, b, c, d);
    }
    atomic_fetch_add(&frontiers, 1);
    atomic_fetch_add(&equations, count);
    int engaged = gpu_meta_batch_run(pairs, mode, answers, count, a, b, c, d);
    size_t yes = 0;
    if (engaged)
        for (size_t i = 0; i < count; ++i) yes += answers[i] == 1;
    atomic_fetch_add(&positives, yes);
    struct batch_frame frame = {pairs, answers, count, active};
    if (yes) active = &frame;
    lean_object *result = gpu_meta_batch_original_defeq(t, s, a, b, c, d);
    if (yes) active = frame.previous;
    // Pair references outlive native continuation: cached pointer keys cannot
    // accidentally match a newly allocated Expr at a recycled address.
    free(answers);
    lean_dec(pairs);
    return result;
}

__attribute__((destructor)) static void report_batch(void) {
    const char *mode = getenv("LEAN_GPU_META_BATCH_MODE");
    if (!mode || (strcmp(mode, "cpu") && strcmp(mode, "gpu"))) return;
    fprintf(stderr, "{\"event\":\"native_meta_batch_finished\","
        "\"mode\":\"%s\",\"provider_linked\":%s,"
        "\"frontiers\":%" PRIu64 ",\"equations\":%" PRIu64 ","
        "\"positive_answers\":%" PRIu64 ",\"consumed_answers\":%" PRIu64 "}\n",
        mode, gpu_meta_batch_run ? "true" : "false",
        (uint64_t)atomic_load(&frontiers),
        (uint64_t)atomic_load(&equations),
        (uint64_t)atomic_load(&positives),
        (uint64_t)atomic_load(&consumed));
}
