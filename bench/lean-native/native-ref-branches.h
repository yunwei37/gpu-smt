// SPDX-License-Identifier: Apache-2.0
#pragma once
#include <lean/lean.h>
#ifdef __cplusplus
extern "C" {
#endif
void gpu_smt_abort_fallback(const char*);
int gpu_smt_branch_active();
void gpu_smt_note_fallback(const char*);
lean_object* gpu_smt_effect_error(const char*);
lean_object* gpu_smt_resolve_ref_read(lean_object*);
lean_object* gpu_smt_resolve_ref(lean_object*);
lean_object* gpu_smt_resolve_thunk(lean_object*);
void gpu_smt_ref_created(lean_object*);
void gpu_smt_ref_freed(lean_object*);
void gpu_smt_task_created(void*,int);
void gpu_smt_task_retired(void*);
void* gpu_smt_task_enter(void*,void**);
void gpu_smt_task_leave(void*,void*);
#ifdef __cplusplus
}
struct gpu_smt_task_scope {
 void *saved{},*context{};
 explicit gpu_smt_task_scope(void* task){context=gpu_smt_task_enter(task,&saved);}
 ~gpu_smt_task_scope(){gpu_smt_task_leave(context,saved);}
};
#endif
