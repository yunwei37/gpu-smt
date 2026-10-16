// Lean compiler output
// Module: implementation.NativeBranchBackend
// Imports: public import Init public import REPL.Main
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* l_Lean_JsonNumber_fromNat(lean_object*);
static lean_object* l_NativeBranchBackend_run___redArg___closed__4;
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NativeBranchBackend_run___redArg___boxed(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__4;
static lean_object* l_NativeBranchBackend_execute___closed__1;
lean_object* l_Lean_Json_compress(lean_object*);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute(lean_object*, uint8_t, lean_object*, lean_object*);
lean_object* lean_uint32_to_nat(uint32_t);
static lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___closed__0;
LEAN_EXPORT lean_object* l_NativeBranchBackend_batch___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NativeBranchBackend_batch_spec__1(lean_object*, size_t, size_t, lean_object*);
lean_object* l_Lean_Json_mkObj(lean_object*);
lean_object* lp_REPL_parse(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__5;
lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lean_io_as_task(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__32;
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_array_push(lean_object*, lean_object*);
lean_object* l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_batch___closed__4;
lean_object* l_IO_ofExcept___at___00Lean_Server_FileWorker_handleImportCompletionRequest_spec__0___redArg(lean_object*);
LEAN_EXPORT lean_object* l_NativeBranchBackend_prepareRefs___boxed(lean_object*);
lean_object* l_String_Slice_trimAscii(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__29;
lean_object* lean_io_getenv(lean_object*);
lean_object* gpu_smt_branch_begin(uint8_t);
LEAN_EXPORT lean_object* l_NativeBranchBackend_beginBranch___boxed(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__9;
static lean_object* l_NativeBranchBackend_run___redArg___closed__7;
static lean_object* l_NativeBranchBackend_batch___closed__3;
lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__17;
LEAN_EXPORT lean_object* l_NativeBranchBackend_run___redArg();
lean_object* lean_string_utf8_byte_size(lean_object*);
lean_object* l_Lean_Json_getObjVal_x3f(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__23;
static lean_object* l_NativeBranchBackend_execute___closed__34;
static lean_object* l_NativeBranchBackend_execute___closed__12;
static lean_object* l_NativeBranchBackend_run___redArg___closed__6;
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute___lam__0___boxed(lean_object*);
lean_object* l_Lean_initSearchPath(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__7;
static lean_object* l_NativeBranchBackend_execute___closed__25;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NativeBranchBackend_batch_spec__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NativeBranchBackend_run___boxed(lean_object*, lean_object*);
lean_object* l_Lean_findSysroot(lean_object*);
lean_object* l_String_splitOnAux(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__21;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* gpu_smt_branch_end(uint64_t);
static lean_object* l_NativeBranchBackend_execute___closed__10;
static lean_object* l_NativeBranchBackend_execute___closed__38;
static lean_object* l_NativeBranchBackend_execute___closed__0;
lean_object* l_Lean_Json_getObjValAs_x3f___at___00Lean_Lsp_instFromJsonShowDocumentClientCapabilities_fromJson_spec__0(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_run___redArg___closed__2;
static lean_object* l_NativeBranchBackend_execute___closed__31;
static lean_object* l_NativeBranchBackend_execute___closed__26;
static lean_object* l_NativeBranchBackend_execute___closed__3;
lean_object* lean_io_mono_nanos_now();
static lean_object* l_NativeBranchBackend_execute___closed__11;
lean_object* lean_get_stderr();
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg(lean_object*, uint8_t, lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_run___redArg___closed__5;
lean_object* l_IO_Process_output(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__22;
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* gpu_smt_prepare_refs();
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_run___redArg___closed__0;
static lean_object* l_NativeBranchBackend_run___redArg___closed__1;
lean_object* lp_REPL_REPL_instToJsonCommand_toJson(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__19;
lean_object* lp_REPL_REPL_instFromJsonBatchCommand_fromJson(lean_object*);
lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___lam__0(lean_object*, uint8_t, lean_object*, lean_object*);
lean_object* lean_task_get_own(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__16;
static lean_object* l_NativeBranchBackend_execute___closed__20;
static lean_object* l_NativeBranchBackend_execute___closed__27;
static lean_object* l_NativeBranchBackend_execute___closed__13;
static lean_object* l_NativeBranchBackend_execute___closed__14;
LEAN_EXPORT lean_object* l_NativeBranchBackend_endBranch___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg(lean_object*, lean_object*);
lean_object* l_IO_FS_readFile(lean_object*);
uint8_t l_Option_instBEq_beq___at___00Lean_forEachModuleInDir___at___00ImportCompletion_collectAvailableImportsFromSrcSearchPath_spec__0_spec__0(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__28;
static lean_object* l_NativeBranchBackend_execute___closed__39;
lean_object* lp_REPL_REPL_instFromJsonCommand_fromJson(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__36;
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0(lean_object*, uint8_t, lean_object*, uint8_t, lean_object*, size_t, size_t, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0(lean_object*, uint8_t, lean_object*, lean_object*, lean_object*);
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
lean_object* lp_REPL_REPL_instToJsonError_toJson(lean_object*);
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t lean_uint32_dec_eq(uint32_t, uint32_t);
static lean_object* l_NativeBranchBackend_run___redArg___closed__8;
lean_object* l_String_Slice_toString(lean_object*);
LEAN_EXPORT lean_object* l_NativeBranchBackend_batch(lean_object*, uint8_t, lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__8;
static lean_object* l_NativeBranchBackend_execute___closed__33;
static lean_object* l_NativeBranchBackend_execute___closed__30;
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute___lam__0();
static lean_object* l_NativeBranchBackend_execute___closed__37;
lean_object* lean_nat_sub(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_batch___closed__1;
static lean_object* l_NativeBranchBackend_execute___closed__2;
static lean_object* l_NativeBranchBackend_execute___closed__24;
lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(lean_object*, lean_object*);
lean_object* lp_REPL_REPL_runCommand(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_batch___closed__6;
static lean_object* l_NativeBranchBackend_execute___closed__15;
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NativeBranchBackend_emitLine___boxed(lean_object*, lean_object*);
size_t lean_usize_add(size_t, size_t);
static lean_object* l_NativeBranchBackend_execute___closed__18;
lean_object* lean_array_uget(lean_object*, size_t);
size_t lean_array_size(lean_object*);
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg___boxed(lean_object*, lean_object*, lean_object*);
lean_object* lean_io_error_to_string(lean_object*);
static lean_object* l_NativeBranchBackend_run___redArg___closed__3;
LEAN_EXPORT lean_object* gpu_smt_native_backend(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__6;
lean_object* l_IO_FS_Stream_putStrLn(lean_object*, lean_object*);
static lean_object* l_NativeBranchBackend_batch___closed__5;
lean_object* lean_string_append(lean_object*, lean_object*);
uint8_t lean_usize_dec_lt(size_t, size_t);
lean_object* l_Lean_Json_parse(lean_object*);
static lean_object* l_NativeBranchBackend_execute___closed__35;
lean_object* lean_nat_add(lean_object*, lean_object*);
lean_object* lp_REPL_getLines();
lean_object* l_IO_ofExcept___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0___redArg(lean_object*);
lean_object* gpu_smt_emit_line(lean_object*);
static lean_object* l_NativeBranchBackend_batch___closed__2;
static lean_object* l_NativeBranchBackend_batch___closed__0;
lean_object* lean_array_uset(lean_object*, size_t, lean_object*);
uint8_t l_Option_instBEq_beq___at___00__private_Lean_Elab_Quotation_0__Lean_Elab_Term_Quotation_getHeadInfo_spec__11(lean_object*, lean_object*);
LEAN_EXPORT lean_object* l_NativeBranchBackend_prepareRefs___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = gpu_smt_prepare_refs();
return x_2;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_beginBranch___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_3; lean_object* x_4; 
x_3 = lean_unbox(x_1);
x_4 = gpu_smt_branch_begin(x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_endBranch___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
uint64_t x_3; lean_object* x_4; 
x_3 = lean_unbox_uint64(x_1);
lean_dec(x_1);
x_4 = gpu_smt_branch_end(x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_emitLine___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = gpu_smt_emit_line(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_4; 
x_4 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_4, 0, x_2);
return x_4;
}
else
{
lean_object* x_5; lean_object* x_6; uint8_t x_7; 
x_5 = lean_ctor_get(x_1, 0);
lean_inc(x_5);
x_6 = lean_ctor_get(x_1, 1);
lean_inc(x_6);
lean_dec_ref(x_1);
x_7 = !lean_is_exclusive(x_2);
if (x_7 == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_8 = lean_ctor_get(x_2, 0);
x_9 = lean_ctor_get(x_2, 1);
x_10 = l_Lean_Json_parse(x_5);
if (lean_obj_tag(x_10) == 1)
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; 
lean_dec(x_8);
x_11 = lean_ctor_get(x_10, 0);
lean_inc(x_11);
lean_dec_ref(x_10);
x_12 = lean_unsigned_to_nat(1u);
x_13 = lean_nat_add(x_9, x_12);
lean_dec(x_9);
lean_ctor_set(x_2, 1, x_13);
lean_ctor_set(x_2, 0, x_11);
x_1 = x_6;
goto _start;
}
else
{
lean_dec_ref(x_10);
x_1 = x_6;
goto _start;
}
}
else
{
lean_object* x_16; lean_object* x_17; lean_object* x_18; 
x_16 = lean_ctor_get(x_2, 0);
x_17 = lean_ctor_get(x_2, 1);
lean_inc(x_17);
lean_inc(x_16);
lean_dec(x_2);
x_18 = l_Lean_Json_parse(x_5);
if (lean_obj_tag(x_18) == 1)
{
lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; 
lean_dec(x_16);
x_19 = lean_ctor_get(x_18, 0);
lean_inc(x_19);
lean_dec_ref(x_18);
x_20 = lean_unsigned_to_nat(1u);
x_21 = lean_nat_add(x_17, x_20);
lean_dec(x_17);
x_22 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_22, 0, x_19);
lean_ctor_set(x_22, 1, x_21);
x_1 = x_6;
x_2 = x_22;
goto _start;
}
else
{
lean_object* x_24; 
lean_dec_ref(x_18);
x_24 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_24, 0, x_16);
lean_ctor_set(x_24, 1, x_17);
x_1 = x_6;
x_2 = x_24;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_6; 
x_6 = l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg(x_2, x_3);
return x_6;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute___lam__0() {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lean_io_mono_nanos_now();
x_3 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_3, 0, x_2);
return x_3;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("fallback_result", 15, 15);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("completed_ns", 12, 12);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("internal_ready_ns", 17, 17);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__3() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("released_ns", 11, 11);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__4() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("response", 8, 8);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__5() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("branch", 6, 6);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__6() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("discarded_response", 18, 18);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__7() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("error", 5, 5);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__8() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("original fallback path is not configured", 40, 40);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__9() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_execute___closed__8;
x_2 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__10() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = l_NativeBranchBackend_execute___closed__9;
x_2 = l_NativeBranchBackend_execute___closed__7;
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__11() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_box(0);
x_2 = l_NativeBranchBackend_execute___closed__10;
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__12() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_execute___closed__11;
x_2 = l_Lean_Json_mkObj(x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__13() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("exit_code", 9, 9);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__14() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("stdout", 6, 6);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__15() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("stderr", 6, 6);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__16() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("original fallback terminated without candidate response", 55, 55);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__17() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_execute___closed__16;
x_2 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__18() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("fallback", 8, 8);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__19() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("GPU_SMT_FALLBACK_REPL", 21, 21);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__20() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("GPU_SMT_FALLBACK_LIBRARY_PATH", 29, 29);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__21() {
_start:
{
uint8_t x_1; lean_object* x_2; 
x_1 = 1;
x_2 = lean_alloc_ctor(0, 0, 3);
lean_ctor_set_uint8(x_2, 0, x_1);
lean_ctor_set_uint8(x_2, 1, x_1);
lean_ctor_set_uint8(x_2, 2, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__22() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__23() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("LD_LIBRARY_PATH", 15, 15);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__24() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("GPU_SMT_BRANCH_OFF", 18, 18);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__25() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_box(0);
x_2 = l_NativeBranchBackend_execute___closed__24;
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__26() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(2u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__27() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("\n\n", 2, 2);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__28() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("original fallback returned no native frame", 42, 42);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__29() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_execute___closed__28;
x_2 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__30() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = l_NativeBranchBackend_execute___closed__29;
x_2 = l_NativeBranchBackend_execute___closed__7;
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__31() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_box(0);
x_2 = l_NativeBranchBackend_execute___closed__30;
x_3 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__32() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_execute___closed__31;
x_2 = l_Lean_Json_mkObj(x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__33() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = l_NativeBranchBackend_execute___closed__32;
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__34() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__35() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("messages", 8, 8);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__36() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("sorries", 7, 7);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__37() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("tactics", 7, 7);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__38() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("infotree", 8, 8);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_execute___closed__39() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("env", 3, 3);
return x_1;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute(lean_object* x_1, uint8_t x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_6; lean_object* x_7; 
lean_inc_ref(x_4);
x_6 = l_Lean_Json_parse(x_4);
x_7 = l_IO_ofExcept___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0___redArg(x_6);
if (lean_obj_tag(x_7) == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_8 = lean_ctor_get(x_7, 0);
lean_inc(x_8);
if (lean_is_exclusive(x_7)) {
 lean_ctor_release(x_7, 0);
 x_9 = x_7;
} else {
 lean_dec_ref(x_7);
 x_9 = lean_box(0);
}
x_10 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_8);
x_11 = l_IO_ofExcept___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0___redArg(x_10);
if (lean_obj_tag(x_11) == 0)
{
lean_object* x_12; lean_object* x_13; 
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
lean_dec_ref(x_11);
x_13 = l_NativeBranchBackend_execute___lam__0();
if (lean_obj_tag(x_13) == 0)
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; uint8_t x_54; lean_object* x_55; lean_object* x_56; lean_object* x_57; lean_object* x_58; lean_object* x_59; lean_object* x_60; lean_object* x_61; lean_object* x_62; uint8_t x_70; lean_object* x_71; lean_object* x_72; lean_object* x_73; lean_object* x_74; lean_object* x_75; lean_object* x_76; uint8_t x_79; lean_object* x_80; lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; lean_object* x_85; uint32_t x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; lean_object* x_90; uint8_t x_107; lean_object* x_108; lean_object* x_109; lean_object* x_110; lean_object* x_111; lean_object* x_112; lean_object* x_113; lean_object* x_114; lean_object* x_115; uint32_t x_116; lean_object* x_117; lean_object* x_118; lean_object* x_124; lean_object* x_125; lean_object* x_126; lean_object* x_127; lean_object* x_128; uint8_t x_129; lean_object* x_132; lean_object* x_133; lean_object* x_134; lean_object* x_135; lean_object* x_136; lean_object* x_257; 
x_14 = lean_ctor_get(x_13, 0);
lean_inc(x_14);
if (lean_is_exclusive(x_13)) {
 lean_ctor_release(x_13, 0);
 x_15 = x_13;
} else {
 lean_dec_ref(x_13);
 x_15 = lean_box(0);
}
x_257 = gpu_smt_branch_begin(x_2);
if (lean_obj_tag(x_257) == 0)
{
lean_object* x_258; lean_object* x_259; lean_object* x_260; lean_object* x_281; 
x_258 = lean_ctor_get(x_257, 0);
lean_inc(x_258);
lean_dec_ref(x_257);
x_281 = lp_REPL_REPL_runCommand(x_12, x_1);
if (lean_obj_tag(x_281) == 0)
{
lean_object* x_282; lean_object* x_283; lean_object* x_284; lean_object* x_285; lean_object* x_286; lean_object* x_287; lean_object* x_298; lean_object* x_299; 
x_282 = lean_ctor_get(x_281, 0);
lean_inc(x_282);
lean_dec_ref(x_281);
x_298 = lean_ctor_get(x_282, 0);
lean_inc(x_298);
if (lean_is_exclusive(x_282)) {
 lean_ctor_release(x_282, 0);
 lean_ctor_release(x_282, 1);
 x_299 = x_282;
} else {
 lean_dec_ref(x_282);
 x_299 = lean_box(0);
}
if (lean_obj_tag(x_298) == 0)
{
lean_object* x_300; lean_object* x_301; lean_object* x_302; lean_object* x_303; lean_object* x_304; lean_object* x_305; lean_object* x_306; 
x_300 = lean_ctor_get(x_298, 0);
lean_inc(x_300);
lean_dec_ref(x_298);
x_301 = lean_ctor_get(x_300, 0);
lean_inc(x_301);
x_302 = lean_ctor_get(x_300, 1);
lean_inc(x_302);
x_303 = lean_ctor_get(x_300, 2);
lean_inc(x_303);
x_304 = lean_ctor_get(x_300, 3);
lean_inc(x_304);
x_305 = lean_ctor_get(x_300, 4);
lean_inc(x_305);
lean_dec(x_300);
if (lean_obj_tag(x_301) == 0)
{
lean_object* x_320; 
x_320 = lean_box(0);
x_306 = x_320;
goto block_319;
}
else
{
uint8_t x_321; 
x_321 = !lean_is_exclusive(x_301);
if (x_321 == 0)
{
lean_object* x_322; lean_object* x_323; lean_object* x_324; lean_object* x_325; lean_object* x_326; lean_object* x_327; 
x_322 = lean_ctor_get(x_301, 0);
x_323 = l_NativeBranchBackend_execute___closed__39;
x_324 = l_Lean_JsonNumber_fromNat(x_322);
lean_ctor_set_tag(x_301, 2);
lean_ctor_set(x_301, 0, x_324);
x_325 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_325, 0, x_323);
lean_ctor_set(x_325, 1, x_301);
x_326 = lean_box(0);
x_327 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_327, 0, x_325);
lean_ctor_set(x_327, 1, x_326);
x_306 = x_327;
goto block_319;
}
else
{
lean_object* x_328; lean_object* x_329; lean_object* x_330; lean_object* x_331; lean_object* x_332; lean_object* x_333; lean_object* x_334; 
x_328 = lean_ctor_get(x_301, 0);
lean_inc(x_328);
lean_dec(x_301);
x_329 = l_NativeBranchBackend_execute___closed__39;
x_330 = l_Lean_JsonNumber_fromNat(x_328);
x_331 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_331, 0, x_330);
x_332 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_332, 0, x_329);
lean_ctor_set(x_332, 1, x_331);
x_333 = lean_box(0);
x_334 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_334, 0, x_332);
lean_ctor_set(x_334, 1, x_333);
x_306 = x_334;
goto block_319;
}
}
block_319:
{
lean_object* x_307; lean_object* x_308; lean_object* x_309; lean_object* x_310; lean_object* x_311; lean_object* x_312; 
x_307 = l_NativeBranchBackend_execute___closed__35;
x_308 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_307, x_302);
x_309 = l_NativeBranchBackend_execute___closed__36;
x_310 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_309, x_303);
x_311 = l_NativeBranchBackend_execute___closed__37;
x_312 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(x_311, x_304);
if (lean_obj_tag(x_305) == 0)
{
lean_object* x_313; 
lean_dec(x_299);
x_313 = lean_box(0);
x_283 = x_306;
x_284 = x_312;
x_285 = x_308;
x_286 = x_310;
x_287 = x_313;
goto block_297;
}
else
{
lean_object* x_314; lean_object* x_315; lean_object* x_316; lean_object* x_317; lean_object* x_318; 
x_314 = lean_ctor_get(x_305, 0);
lean_inc(x_314);
lean_dec_ref(x_305);
x_315 = l_NativeBranchBackend_execute___closed__38;
if (lean_is_scalar(x_299)) {
 x_316 = lean_alloc_ctor(0, 2, 0);
} else {
 x_316 = x_299;
}
lean_ctor_set(x_316, 0, x_315);
lean_ctor_set(x_316, 1, x_314);
x_317 = lean_box(0);
x_318 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_318, 0, x_316);
lean_ctor_set(x_318, 1, x_317);
x_283 = x_306;
x_284 = x_312;
x_285 = x_308;
x_286 = x_310;
x_287 = x_318;
goto block_297;
}
}
}
else
{
lean_object* x_335; lean_object* x_336; 
lean_dec(x_299);
x_335 = lean_ctor_get(x_298, 0);
lean_inc(x_335);
lean_dec_ref(x_298);
x_336 = lp_REPL_REPL_instToJsonError_toJson(x_335);
x_259 = x_336;
x_260 = lean_box(0);
goto block_280;
}
block_297:
{
lean_object* x_288; lean_object* x_289; lean_object* x_290; lean_object* x_291; lean_object* x_292; lean_object* x_293; lean_object* x_294; lean_object* x_295; lean_object* x_296; 
x_288 = lean_box(0);
x_289 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_289, 0, x_287);
lean_ctor_set(x_289, 1, x_288);
x_290 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_290, 0, x_284);
lean_ctor_set(x_290, 1, x_289);
x_291 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_291, 0, x_286);
lean_ctor_set(x_291, 1, x_290);
x_292 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_292, 0, x_285);
lean_ctor_set(x_292, 1, x_291);
x_293 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_293, 0, x_283);
lean_ctor_set(x_293, 1, x_292);
x_294 = l_NativeBranchBackend_execute___closed__34;
x_295 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_293, x_294);
x_296 = l_Lean_Json_mkObj(x_295);
x_259 = x_296;
x_260 = lean_box(0);
goto block_280;
}
}
else
{
uint8_t x_337; 
x_337 = !lean_is_exclusive(x_281);
if (x_337 == 0)
{
lean_object* x_338; lean_object* x_339; lean_object* x_340; lean_object* x_341; lean_object* x_342; lean_object* x_343; lean_object* x_344; 
x_338 = lean_ctor_get(x_281, 0);
x_339 = l_NativeBranchBackend_execute___closed__7;
x_340 = lean_io_error_to_string(x_338);
lean_ctor_set_tag(x_281, 3);
lean_ctor_set(x_281, 0, x_340);
x_341 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_341, 0, x_339);
lean_ctor_set(x_341, 1, x_281);
x_342 = lean_box(0);
x_343 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_343, 0, x_341);
lean_ctor_set(x_343, 1, x_342);
x_344 = l_Lean_Json_mkObj(x_343);
x_259 = x_344;
x_260 = lean_box(0);
goto block_280;
}
else
{
lean_object* x_345; lean_object* x_346; lean_object* x_347; lean_object* x_348; lean_object* x_349; lean_object* x_350; lean_object* x_351; lean_object* x_352; 
x_345 = lean_ctor_get(x_281, 0);
lean_inc(x_345);
lean_dec(x_281);
x_346 = l_NativeBranchBackend_execute___closed__7;
x_347 = lean_io_error_to_string(x_345);
x_348 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_348, 0, x_347);
x_349 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_349, 0, x_346);
lean_ctor_set(x_349, 1, x_348);
x_350 = lean_box(0);
x_351 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_351, 0, x_349);
lean_ctor_set(x_351, 1, x_350);
x_352 = l_Lean_Json_mkObj(x_351);
x_259 = x_352;
x_260 = lean_box(0);
goto block_280;
}
}
block_280:
{
lean_object* x_261; 
x_261 = l_NativeBranchBackend_execute___lam__0();
if (lean_obj_tag(x_261) == 0)
{
lean_object* x_262; uint64_t x_263; lean_object* x_264; 
x_262 = lean_ctor_get(x_261, 0);
lean_inc(x_262);
lean_dec_ref(x_261);
x_263 = lean_unbox_uint64(x_258);
lean_dec(x_258);
x_264 = gpu_smt_branch_end(x_263);
if (lean_obj_tag(x_264) == 0)
{
lean_object* x_265; lean_object* x_266; 
x_265 = lean_ctor_get(x_264, 0);
lean_inc(x_265);
lean_dec_ref(x_264);
x_266 = l_NativeBranchBackend_execute___lam__0();
if (lean_obj_tag(x_266) == 0)
{
lean_object* x_267; lean_object* x_268; 
x_267 = lean_ctor_get(x_266, 0);
lean_inc(x_267);
lean_dec_ref(x_266);
x_268 = l_Lean_Json_parse(x_265);
if (lean_obj_tag(x_268) == 0)
{
lean_object* x_269; 
lean_dec_ref(x_268);
x_269 = lean_box(0);
x_132 = x_259;
x_133 = lean_box(0);
x_134 = x_262;
x_135 = x_267;
x_136 = x_269;
goto block_256;
}
else
{
lean_object* x_270; 
x_270 = lean_ctor_get(x_268, 0);
lean_inc(x_270);
lean_dec_ref(x_268);
x_132 = x_259;
x_133 = lean_box(0);
x_134 = x_262;
x_135 = x_267;
x_136 = x_270;
goto block_256;
}
}
else
{
uint8_t x_271; 
lean_dec(x_265);
lean_dec(x_262);
lean_dec(x_259);
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_9);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_271 = !lean_is_exclusive(x_266);
if (x_271 == 0)
{
return x_266;
}
else
{
lean_object* x_272; lean_object* x_273; 
x_272 = lean_ctor_get(x_266, 0);
lean_inc(x_272);
lean_dec(x_266);
x_273 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_273, 0, x_272);
return x_273;
}
}
}
else
{
uint8_t x_274; 
lean_dec(x_262);
lean_dec(x_259);
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_9);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_274 = !lean_is_exclusive(x_264);
if (x_274 == 0)
{
return x_264;
}
else
{
lean_object* x_275; lean_object* x_276; 
x_275 = lean_ctor_get(x_264, 0);
lean_inc(x_275);
lean_dec(x_264);
x_276 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_276, 0, x_275);
return x_276;
}
}
}
else
{
uint8_t x_277; 
lean_dec(x_259);
lean_dec(x_258);
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_9);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_277 = !lean_is_exclusive(x_261);
if (x_277 == 0)
{
return x_261;
}
else
{
lean_object* x_278; lean_object* x_279; 
x_278 = lean_ctor_get(x_261, 0);
lean_inc(x_278);
lean_dec(x_261);
x_279 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_279, 0, x_278);
return x_279;
}
}
}
}
else
{
uint8_t x_353; 
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_12);
lean_dec(x_9);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_353 = !lean_is_exclusive(x_257);
if (x_353 == 0)
{
return x_257;
}
else
{
lean_object* x_354; lean_object* x_355; 
x_354 = lean_ctor_get(x_257, 0);
lean_inc(x_354);
lean_dec(x_257);
x_355 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_355, 0, x_354);
return x_355;
}
}
block_53:
{
lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; lean_object* x_52; 
x_25 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_25, 0, x_19);
lean_ctor_set(x_25, 1, x_24);
x_26 = l_NativeBranchBackend_execute___closed__0;
x_27 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_27, 0, x_26);
lean_ctor_set(x_27, 1, x_23);
x_28 = l_NativeBranchBackend_execute___closed__1;
x_29 = lean_nat_sub(x_18, x_14);
lean_dec(x_18);
x_30 = l_Lean_JsonNumber_fromNat(x_29);
if (lean_is_scalar(x_9)) {
 x_31 = lean_alloc_ctor(2, 1, 0);
} else {
 x_31 = x_9;
 lean_ctor_set_tag(x_31, 2);
}
lean_ctor_set(x_31, 0, x_30);
x_32 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_32, 0, x_28);
lean_ctor_set(x_32, 1, x_31);
x_33 = l_NativeBranchBackend_execute___closed__2;
x_34 = lean_nat_sub(x_21, x_14);
lean_dec(x_21);
x_35 = l_Lean_JsonNumber_fromNat(x_34);
x_36 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_36, 0, x_35);
x_37 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_37, 0, x_33);
lean_ctor_set(x_37, 1, x_36);
x_38 = l_NativeBranchBackend_execute___closed__3;
x_39 = lean_nat_sub(x_20, x_14);
lean_dec(x_14);
lean_dec(x_20);
x_40 = l_Lean_JsonNumber_fromNat(x_39);
x_41 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_41, 0, x_40);
x_42 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_42, 0, x_38);
lean_ctor_set(x_42, 1, x_41);
x_43 = lean_box(0);
x_44 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_44, 0, x_42);
lean_ctor_set(x_44, 1, x_43);
x_45 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_45, 0, x_37);
lean_ctor_set(x_45, 1, x_44);
x_46 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_46, 0, x_32);
lean_ctor_set(x_46, 1, x_45);
x_47 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_47, 0, x_27);
lean_ctor_set(x_47, 1, x_46);
x_48 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_48, 0, x_25);
lean_ctor_set(x_48, 1, x_47);
x_49 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_49, 0, x_22);
lean_ctor_set(x_49, 1, x_48);
x_50 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_50, 0, x_17);
lean_ctor_set(x_50, 1, x_49);
x_51 = l_Lean_Json_mkObj(x_50);
if (lean_is_scalar(x_15)) {
 x_52 = lean_alloc_ctor(0, 1, 0);
} else {
 x_52 = x_15;
}
lean_ctor_set(x_52, 0, x_51);
return x_52;
}
block_69:
{
lean_object* x_63; lean_object* x_64; lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_68; 
x_63 = lean_io_mono_nanos_now();
x_64 = l_NativeBranchBackend_execute___closed__4;
x_65 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_65, 0, x_64);
lean_ctor_set(x_65, 1, x_61);
x_66 = l_NativeBranchBackend_execute___closed__5;
x_67 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_67, 0, x_66);
lean_ctor_set(x_67, 1, x_56);
x_68 = l_NativeBranchBackend_execute___closed__6;
if (x_54 == 0)
{
lean_dec(x_55);
x_16 = lean_box(0);
x_17 = x_65;
x_18 = x_63;
x_19 = x_68;
x_20 = x_59;
x_21 = x_58;
x_22 = x_67;
x_23 = x_60;
x_24 = x_57;
goto block_53;
}
else
{
lean_dec(x_57);
x_16 = lean_box(0);
x_17 = x_65;
x_18 = x_63;
x_19 = x_68;
x_20 = x_59;
x_21 = x_58;
x_22 = x_67;
x_23 = x_60;
x_24 = x_55;
goto block_53;
}
}
block_78:
{
lean_object* x_77; 
x_77 = l_NativeBranchBackend_execute___closed__12;
lean_inc(x_73);
x_54 = x_70;
x_55 = x_72;
x_56 = x_71;
x_57 = x_73;
x_58 = x_75;
x_59 = x_74;
x_60 = x_73;
x_61 = x_77;
x_62 = lean_box(0);
goto block_69;
}
block_106:
{
lean_object* x_91; lean_object* x_92; lean_object* x_93; lean_object* x_94; lean_object* x_95; lean_object* x_96; lean_object* x_97; lean_object* x_98; lean_object* x_99; lean_object* x_100; lean_object* x_101; lean_object* x_102; lean_object* x_103; lean_object* x_104; lean_object* x_105; 
x_91 = l_NativeBranchBackend_execute___closed__13;
x_92 = lean_uint32_to_nat(x_86);
x_93 = l_Lean_JsonNumber_fromNat(x_92);
x_94 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_94, 0, x_93);
x_95 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_95, 0, x_91);
lean_ctor_set(x_95, 1, x_94);
x_96 = l_NativeBranchBackend_execute___closed__14;
x_97 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_97, 0, x_84);
x_98 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_98, 0, x_96);
lean_ctor_set(x_98, 1, x_97);
x_99 = l_NativeBranchBackend_execute___closed__15;
x_100 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_100, 0, x_82);
x_101 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_101, 0, x_99);
lean_ctor_set(x_101, 1, x_100);
x_102 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_102, 0, x_101);
lean_ctor_set(x_102, 1, x_85);
x_103 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_103, 0, x_98);
lean_ctor_set(x_103, 1, x_102);
x_104 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_104, 0, x_95);
lean_ctor_set(x_104, 1, x_103);
x_105 = l_Lean_Json_mkObj(x_104);
x_54 = x_79;
x_55 = x_81;
x_56 = x_80;
x_57 = x_83;
x_58 = x_88;
x_59 = x_87;
x_60 = x_105;
x_61 = x_89;
x_62 = lean_box(0);
goto block_69;
}
block_123:
{
lean_object* x_119; lean_object* x_120; lean_object* x_121; lean_object* x_122; 
x_119 = l_NativeBranchBackend_execute___closed__17;
x_120 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_120, 0, x_108);
lean_ctor_set(x_120, 1, x_119);
lean_inc(x_115);
x_121 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_121, 0, x_120);
lean_ctor_set(x_121, 1, x_115);
x_122 = l_Lean_Json_mkObj(x_121);
x_79 = x_107;
x_80 = x_110;
x_81 = x_109;
x_82 = x_112;
x_83 = x_113;
x_84 = x_114;
x_85 = x_115;
x_86 = x_116;
x_87 = x_118;
x_88 = x_117;
x_89 = x_122;
x_90 = lean_box(0);
goto block_106;
}
block_131:
{
lean_object* x_130; 
x_130 = lean_box(0);
lean_inc(x_125);
x_54 = x_129;
x_55 = x_125;
x_56 = x_124;
x_57 = x_130;
x_58 = x_128;
x_59 = x_127;
x_60 = x_130;
x_61 = x_125;
x_62 = lean_box(0);
goto block_69;
}
block_256:
{
lean_object* x_137; lean_object* x_138; 
x_137 = l_NativeBranchBackend_execute___closed__18;
lean_inc(x_136);
x_138 = l_Lean_Json_getObjValAs_x3f___at___00Lean_Lsp_instFromJsonShowDocumentClientCapabilities_fromJson_spec__0(x_136, x_137);
if (lean_obj_tag(x_138) == 0)
{
uint8_t x_139; 
lean_dec_ref(x_138);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_139 = 0;
x_124 = x_136;
x_125 = x_132;
x_126 = lean_box(0);
x_127 = x_135;
x_128 = x_134;
x_129 = x_139;
goto block_131;
}
else
{
lean_object* x_140; uint8_t x_141; 
x_140 = lean_ctor_get(x_138, 0);
lean_inc(x_140);
lean_dec_ref(x_138);
x_141 = lean_unbox(x_140);
if (x_141 == 0)
{
uint8_t x_142; 
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_142 = lean_unbox(x_140);
lean_dec(x_140);
x_124 = x_136;
x_125 = x_132;
x_126 = lean_box(0);
x_127 = x_135;
x_128 = x_134;
x_129 = x_142;
goto block_131;
}
else
{
lean_object* x_143; lean_object* x_144; lean_object* x_145; lean_object* x_146; lean_object* x_147; 
x_143 = l_NativeBranchBackend_execute___closed__19;
x_144 = lean_io_getenv(x_143);
x_145 = l_NativeBranchBackend_execute___closed__20;
x_146 = lean_io_getenv(x_145);
x_147 = lean_box(0);
if (lean_obj_tag(x_144) == 1)
{
if (lean_obj_tag(x_146) == 1)
{
uint8_t x_148; 
x_148 = !lean_is_exclusive(x_144);
if (x_148 == 0)
{
lean_object* x_149; lean_object* x_150; lean_object* x_151; lean_object* x_152; lean_object* x_153; lean_object* x_154; lean_object* x_155; lean_object* x_156; lean_object* x_157; lean_object* x_158; lean_object* x_159; lean_object* x_160; uint8_t x_161; lean_object* x_162; uint8_t x_163; lean_object* x_164; lean_object* x_165; lean_object* x_166; lean_object* x_167; lean_object* x_168; lean_object* x_169; lean_object* x_170; lean_object* x_171; lean_object* x_172; lean_object* x_173; lean_object* x_174; lean_object* x_175; lean_object* x_176; 
x_149 = lean_ctor_get(x_144, 0);
x_150 = l_NativeBranchBackend_execute___closed__21;
x_151 = lean_unsigned_to_nat(0u);
x_152 = l_NativeBranchBackend_execute___closed__22;
x_153 = lean_box(0);
x_154 = l_NativeBranchBackend_execute___closed__23;
x_155 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_155, 0, x_154);
lean_ctor_set(x_155, 1, x_146);
x_156 = l_NativeBranchBackend_execute___closed__25;
x_157 = lean_unsigned_to_nat(2u);
x_158 = l_NativeBranchBackend_execute___closed__26;
x_159 = lean_array_push(x_158, x_155);
x_160 = lean_array_push(x_159, x_156);
x_161 = 0;
x_162 = lean_alloc_ctor(0, 5, 2);
lean_ctor_set(x_162, 0, x_150);
lean_ctor_set(x_162, 1, x_149);
lean_ctor_set(x_162, 2, x_152);
lean_ctor_set(x_162, 3, x_153);
lean_ctor_set(x_162, 4, x_160);
x_163 = lean_unbox(x_140);
lean_ctor_set_uint8(x_162, sizeof(void*)*5, x_163);
lean_ctor_set_uint8(x_162, sizeof(void*)*5 + 1, x_161);
x_164 = lean_string_utf8_byte_size(x_3);
x_165 = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(x_165, 0, x_3);
lean_ctor_set(x_165, 1, x_151);
lean_ctor_set(x_165, 2, x_164);
x_166 = l_String_Slice_trimAscii(x_165);
lean_dec_ref(x_165);
x_167 = l_String_Slice_toString(x_166);
lean_dec_ref(x_166);
x_168 = l_NativeBranchBackend_execute___closed__27;
x_169 = lean_string_append(x_167, x_168);
x_170 = lean_string_utf8_byte_size(x_4);
x_171 = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(x_171, 0, x_4);
lean_ctor_set(x_171, 1, x_151);
lean_ctor_set(x_171, 2, x_170);
x_172 = l_String_Slice_trimAscii(x_171);
lean_dec_ref(x_171);
x_173 = l_String_Slice_toString(x_172);
lean_dec_ref(x_172);
x_174 = lean_string_append(x_169, x_173);
lean_dec_ref(x_173);
x_175 = lean_string_append(x_174, x_168);
lean_ctor_set(x_144, 0, x_175);
x_176 = l_IO_Process_output(x_162, x_144);
lean_dec_ref(x_144);
if (lean_obj_tag(x_176) == 0)
{
lean_object* x_177; uint32_t x_178; lean_object* x_179; lean_object* x_180; lean_object* x_181; lean_object* x_182; lean_object* x_183; lean_object* x_184; lean_object* x_185; 
x_177 = lean_ctor_get(x_176, 0);
lean_inc(x_177);
lean_dec_ref(x_176);
x_178 = lean_ctor_get_uint32(x_177, sizeof(void*)*2);
x_179 = lean_ctor_get(x_177, 0);
lean_inc_ref(x_179);
x_180 = lean_ctor_get(x_177, 1);
lean_inc_ref(x_180);
lean_dec(x_177);
x_181 = l_NativeBranchBackend_execute___closed__7;
x_182 = lean_box(0);
x_183 = l_String_splitOnAux(x_179, x_168, x_151, x_151, x_151, x_182);
x_184 = l_NativeBranchBackend_execute___closed__33;
x_185 = l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg(x_183, x_184);
if (lean_obj_tag(x_185) == 0)
{
lean_object* x_186; lean_object* x_187; lean_object* x_188; uint32_t x_189; uint8_t x_190; 
x_186 = lean_ctor_get(x_185, 0);
lean_inc(x_186);
lean_dec_ref(x_185);
x_187 = lean_ctor_get(x_186, 0);
lean_inc(x_187);
x_188 = lean_ctor_get(x_186, 1);
lean_inc(x_188);
lean_dec(x_186);
x_189 = 0;
x_190 = lean_uint32_dec_eq(x_178, x_189);
if (x_190 == 0)
{
uint8_t x_191; 
lean_dec(x_188);
lean_dec(x_187);
x_191 = lean_unbox(x_140);
lean_dec(x_140);
x_107 = x_191;
x_108 = x_181;
x_109 = x_132;
x_110 = x_136;
x_111 = lean_box(0);
x_112 = x_180;
x_113 = x_147;
x_114 = x_179;
x_115 = x_182;
x_116 = x_178;
x_117 = x_134;
x_118 = x_135;
goto block_123;
}
else
{
uint8_t x_192; 
x_192 = lean_nat_dec_lt(x_188, x_157);
lean_dec(x_188);
if (x_192 == 0)
{
uint8_t x_193; 
x_193 = lean_unbox(x_140);
lean_dec(x_140);
x_79 = x_193;
x_80 = x_136;
x_81 = x_132;
x_82 = x_180;
x_83 = x_147;
x_84 = x_179;
x_85 = x_182;
x_86 = x_178;
x_87 = x_135;
x_88 = x_134;
x_89 = x_187;
x_90 = lean_box(0);
goto block_106;
}
else
{
uint8_t x_194; 
lean_dec(x_187);
x_194 = lean_unbox(x_140);
lean_dec(x_140);
x_107 = x_194;
x_108 = x_181;
x_109 = x_132;
x_110 = x_136;
x_111 = lean_box(0);
x_112 = x_180;
x_113 = x_147;
x_114 = x_179;
x_115 = x_182;
x_116 = x_178;
x_117 = x_134;
x_118 = x_135;
goto block_123;
}
}
}
else
{
uint8_t x_195; 
lean_dec_ref(x_180);
lean_dec_ref(x_179);
lean_dec(x_140);
lean_dec(x_136);
lean_dec(x_135);
lean_dec(x_134);
lean_dec(x_132);
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_9);
x_195 = !lean_is_exclusive(x_185);
if (x_195 == 0)
{
return x_185;
}
else
{
lean_object* x_196; lean_object* x_197; 
x_196 = lean_ctor_get(x_185, 0);
lean_inc(x_196);
lean_dec(x_185);
x_197 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_197, 0, x_196);
return x_197;
}
}
}
else
{
uint8_t x_198; 
lean_dec(x_140);
lean_dec(x_136);
lean_dec(x_135);
lean_dec(x_134);
lean_dec(x_132);
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_9);
x_198 = !lean_is_exclusive(x_176);
if (x_198 == 0)
{
return x_176;
}
else
{
lean_object* x_199; lean_object* x_200; 
x_199 = lean_ctor_get(x_176, 0);
lean_inc(x_199);
lean_dec(x_176);
x_200 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_200, 0, x_199);
return x_200;
}
}
}
else
{
lean_object* x_201; lean_object* x_202; lean_object* x_203; lean_object* x_204; lean_object* x_205; lean_object* x_206; lean_object* x_207; lean_object* x_208; lean_object* x_209; lean_object* x_210; lean_object* x_211; lean_object* x_212; uint8_t x_213; lean_object* x_214; uint8_t x_215; lean_object* x_216; lean_object* x_217; lean_object* x_218; lean_object* x_219; lean_object* x_220; lean_object* x_221; lean_object* x_222; lean_object* x_223; lean_object* x_224; lean_object* x_225; lean_object* x_226; lean_object* x_227; lean_object* x_228; lean_object* x_229; 
x_201 = lean_ctor_get(x_144, 0);
lean_inc(x_201);
lean_dec(x_144);
x_202 = l_NativeBranchBackend_execute___closed__21;
x_203 = lean_unsigned_to_nat(0u);
x_204 = l_NativeBranchBackend_execute___closed__22;
x_205 = lean_box(0);
x_206 = l_NativeBranchBackend_execute___closed__23;
x_207 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_207, 0, x_206);
lean_ctor_set(x_207, 1, x_146);
x_208 = l_NativeBranchBackend_execute___closed__25;
x_209 = lean_unsigned_to_nat(2u);
x_210 = l_NativeBranchBackend_execute___closed__26;
x_211 = lean_array_push(x_210, x_207);
x_212 = lean_array_push(x_211, x_208);
x_213 = 0;
x_214 = lean_alloc_ctor(0, 5, 2);
lean_ctor_set(x_214, 0, x_202);
lean_ctor_set(x_214, 1, x_201);
lean_ctor_set(x_214, 2, x_204);
lean_ctor_set(x_214, 3, x_205);
lean_ctor_set(x_214, 4, x_212);
x_215 = lean_unbox(x_140);
lean_ctor_set_uint8(x_214, sizeof(void*)*5, x_215);
lean_ctor_set_uint8(x_214, sizeof(void*)*5 + 1, x_213);
x_216 = lean_string_utf8_byte_size(x_3);
x_217 = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(x_217, 0, x_3);
lean_ctor_set(x_217, 1, x_203);
lean_ctor_set(x_217, 2, x_216);
x_218 = l_String_Slice_trimAscii(x_217);
lean_dec_ref(x_217);
x_219 = l_String_Slice_toString(x_218);
lean_dec_ref(x_218);
x_220 = l_NativeBranchBackend_execute___closed__27;
x_221 = lean_string_append(x_219, x_220);
x_222 = lean_string_utf8_byte_size(x_4);
x_223 = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(x_223, 0, x_4);
lean_ctor_set(x_223, 1, x_203);
lean_ctor_set(x_223, 2, x_222);
x_224 = l_String_Slice_trimAscii(x_223);
lean_dec_ref(x_223);
x_225 = l_String_Slice_toString(x_224);
lean_dec_ref(x_224);
x_226 = lean_string_append(x_221, x_225);
lean_dec_ref(x_225);
x_227 = lean_string_append(x_226, x_220);
x_228 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_228, 0, x_227);
x_229 = l_IO_Process_output(x_214, x_228);
lean_dec_ref(x_228);
if (lean_obj_tag(x_229) == 0)
{
lean_object* x_230; uint32_t x_231; lean_object* x_232; lean_object* x_233; lean_object* x_234; lean_object* x_235; lean_object* x_236; lean_object* x_237; lean_object* x_238; 
x_230 = lean_ctor_get(x_229, 0);
lean_inc(x_230);
lean_dec_ref(x_229);
x_231 = lean_ctor_get_uint32(x_230, sizeof(void*)*2);
x_232 = lean_ctor_get(x_230, 0);
lean_inc_ref(x_232);
x_233 = lean_ctor_get(x_230, 1);
lean_inc_ref(x_233);
lean_dec(x_230);
x_234 = l_NativeBranchBackend_execute___closed__7;
x_235 = lean_box(0);
x_236 = l_String_splitOnAux(x_232, x_220, x_203, x_203, x_203, x_235);
x_237 = l_NativeBranchBackend_execute___closed__33;
x_238 = l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg(x_236, x_237);
if (lean_obj_tag(x_238) == 0)
{
lean_object* x_239; lean_object* x_240; lean_object* x_241; uint32_t x_242; uint8_t x_243; 
x_239 = lean_ctor_get(x_238, 0);
lean_inc(x_239);
lean_dec_ref(x_238);
x_240 = lean_ctor_get(x_239, 0);
lean_inc(x_240);
x_241 = lean_ctor_get(x_239, 1);
lean_inc(x_241);
lean_dec(x_239);
x_242 = 0;
x_243 = lean_uint32_dec_eq(x_231, x_242);
if (x_243 == 0)
{
uint8_t x_244; 
lean_dec(x_241);
lean_dec(x_240);
x_244 = lean_unbox(x_140);
lean_dec(x_140);
x_107 = x_244;
x_108 = x_234;
x_109 = x_132;
x_110 = x_136;
x_111 = lean_box(0);
x_112 = x_233;
x_113 = x_147;
x_114 = x_232;
x_115 = x_235;
x_116 = x_231;
x_117 = x_134;
x_118 = x_135;
goto block_123;
}
else
{
uint8_t x_245; 
x_245 = lean_nat_dec_lt(x_241, x_209);
lean_dec(x_241);
if (x_245 == 0)
{
uint8_t x_246; 
x_246 = lean_unbox(x_140);
lean_dec(x_140);
x_79 = x_246;
x_80 = x_136;
x_81 = x_132;
x_82 = x_233;
x_83 = x_147;
x_84 = x_232;
x_85 = x_235;
x_86 = x_231;
x_87 = x_135;
x_88 = x_134;
x_89 = x_240;
x_90 = lean_box(0);
goto block_106;
}
else
{
uint8_t x_247; 
lean_dec(x_240);
x_247 = lean_unbox(x_140);
lean_dec(x_140);
x_107 = x_247;
x_108 = x_234;
x_109 = x_132;
x_110 = x_136;
x_111 = lean_box(0);
x_112 = x_233;
x_113 = x_147;
x_114 = x_232;
x_115 = x_235;
x_116 = x_231;
x_117 = x_134;
x_118 = x_135;
goto block_123;
}
}
}
else
{
lean_object* x_248; lean_object* x_249; lean_object* x_250; 
lean_dec_ref(x_233);
lean_dec_ref(x_232);
lean_dec(x_140);
lean_dec(x_136);
lean_dec(x_135);
lean_dec(x_134);
lean_dec(x_132);
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_9);
x_248 = lean_ctor_get(x_238, 0);
lean_inc(x_248);
if (lean_is_exclusive(x_238)) {
 lean_ctor_release(x_238, 0);
 x_249 = x_238;
} else {
 lean_dec_ref(x_238);
 x_249 = lean_box(0);
}
if (lean_is_scalar(x_249)) {
 x_250 = lean_alloc_ctor(1, 1, 0);
} else {
 x_250 = x_249;
}
lean_ctor_set(x_250, 0, x_248);
return x_250;
}
}
else
{
lean_object* x_251; lean_object* x_252; lean_object* x_253; 
lean_dec(x_140);
lean_dec(x_136);
lean_dec(x_135);
lean_dec(x_134);
lean_dec(x_132);
lean_dec(x_15);
lean_dec(x_14);
lean_dec(x_9);
x_251 = lean_ctor_get(x_229, 0);
lean_inc(x_251);
if (lean_is_exclusive(x_229)) {
 lean_ctor_release(x_229, 0);
 x_252 = x_229;
} else {
 lean_dec_ref(x_229);
 x_252 = lean_box(0);
}
if (lean_is_scalar(x_252)) {
 x_253 = lean_alloc_ctor(1, 1, 0);
} else {
 x_253 = x_252;
}
lean_ctor_set(x_253, 0, x_251);
return x_253;
}
}
}
else
{
uint8_t x_254; 
lean_dec(x_146);
lean_dec_ref(x_144);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_254 = lean_unbox(x_140);
lean_dec(x_140);
x_70 = x_254;
x_71 = x_136;
x_72 = x_132;
x_73 = x_147;
x_74 = x_135;
x_75 = x_134;
x_76 = lean_box(0);
goto block_78;
}
}
else
{
uint8_t x_255; 
lean_dec(x_146);
lean_dec(x_144);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_255 = lean_unbox(x_140);
lean_dec(x_140);
x_70 = x_255;
x_71 = x_136;
x_72 = x_132;
x_73 = x_147;
x_74 = x_135;
x_75 = x_134;
x_76 = lean_box(0);
goto block_78;
}
}
}
}
}
else
{
uint8_t x_356; 
lean_dec(x_12);
lean_dec(x_9);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_356 = !lean_is_exclusive(x_13);
if (x_356 == 0)
{
return x_13;
}
else
{
lean_object* x_357; lean_object* x_358; 
x_357 = lean_ctor_get(x_13, 0);
lean_inc(x_357);
lean_dec(x_13);
x_358 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_358, 0, x_357);
return x_358;
}
}
}
else
{
uint8_t x_359; 
lean_dec(x_9);
lean_dec_ref(x_4);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_359 = !lean_is_exclusive(x_11);
if (x_359 == 0)
{
return x_11;
}
else
{
lean_object* x_360; lean_object* x_361; 
x_360 = lean_ctor_get(x_11, 0);
lean_inc(x_360);
lean_dec(x_11);
x_361 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_361, 0, x_360);
return x_361;
}
}
}
else
{
lean_dec_ref(x_4);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
return x_7;
}
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0(x_1, x_2, x_3, x_4);
lean_dec(x_1);
return x_6;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute___lam__0___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = l_NativeBranchBackend_execute___lam__0();
return x_2;
}
}
LEAN_EXPORT lean_object* l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = l_List_forIn_x27_loop___at___00NativeBranchBackend_execute_spec__0___redArg(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_execute___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; lean_object* x_7; 
x_6 = lean_unbox(x_2);
x_7 = l_NativeBranchBackend_execute(x_1, x_6, x_3, x_4);
return x_7;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___lam__0(lean_object* x_1, uint8_t x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_6; 
x_6 = l_NativeBranchBackend_execute(x_1, x_2, x_3, x_4);
if (lean_obj_tag(x_6) == 0)
{
uint8_t x_7; 
x_7 = !lean_is_exclusive(x_6);
if (x_7 == 0)
{
lean_ctor_set_tag(x_6, 1);
return x_6;
}
else
{
lean_object* x_8; lean_object* x_9; 
x_8 = lean_ctor_get(x_6, 0);
lean_inc(x_8);
lean_dec(x_6);
x_9 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_9, 0, x_8);
return x_9;
}
}
else
{
uint8_t x_10; 
x_10 = !lean_is_exclusive(x_6);
if (x_10 == 0)
{
lean_ctor_set_tag(x_6, 0);
return x_6;
}
else
{
lean_object* x_11; lean_object* x_12; 
x_11 = lean_ctor_get(x_6, 0);
lean_inc(x_11);
lean_dec(x_6);
x_12 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_12, 0, x_11);
return x_12;
}
}
}
}
static lean_object* _init_l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___lam__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; lean_object* x_7; 
x_6 = lean_unbox(x_2);
x_7 = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___lam__0(x_1, x_6, x_3, x_4);
return x_7;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0(lean_object* x_1, uint8_t x_2, lean_object* x_3, uint8_t x_4, lean_object* x_5, size_t x_6, size_t x_7, lean_object* x_8) {
_start:
{
uint8_t x_10; 
x_10 = lean_usize_dec_lt(x_7, x_6);
if (x_10 == 0)
{
lean_object* x_11; 
lean_dec_ref(x_5);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_8);
return x_11;
}
else
{
lean_object* x_12; uint8_t x_13; 
x_12 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_12);
x_13 = !lean_is_exclusive(x_12);
if (x_13 == 0)
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; size_t x_28; size_t x_29; lean_object* x_30; 
x_14 = lean_ctor_get(x_12, 3);
lean_dec(x_14);
x_15 = lean_ctor_get(x_12, 2);
lean_dec(x_15);
x_16 = lean_ctor_get(x_12, 1);
lean_dec(x_16);
x_17 = lean_array_uget(x_8, x_7);
x_18 = lean_unsigned_to_nat(0u);
x_19 = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0;
x_20 = lean_box(x_2);
x_21 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_21, 0, x_20);
lean_ctor_set(x_12, 3, x_21);
lean_ctor_set(x_12, 2, x_17);
lean_ctor_set(x_12, 1, x_19);
x_22 = lp_REPL_REPL_instToJsonCommand_toJson(x_12);
x_23 = l_Lean_Json_compress(x_22);
x_24 = lean_box(x_4);
lean_inc_ref(x_5);
lean_inc_ref(x_3);
x_25 = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___lam__0___boxed), 5, 4);
lean_closure_set(x_25, 0, x_3);
lean_closure_set(x_25, 1, x_24);
lean_closure_set(x_25, 2, x_5);
lean_closure_set(x_25, 3, x_23);
x_26 = lean_io_as_task(x_25, x_18);
x_27 = lean_array_uset(x_8, x_7, x_18);
x_28 = 1;
x_29 = lean_usize_add(x_7, x_28);
x_30 = lean_array_uset(x_27, x_7, x_26);
x_7 = x_29;
x_8 = x_30;
goto _start;
}
else
{
lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; size_t x_45; size_t x_46; lean_object* x_47; 
x_32 = lean_ctor_get(x_12, 0);
lean_inc(x_32);
lean_dec(x_12);
x_33 = lean_array_uget(x_8, x_7);
x_34 = lean_unsigned_to_nat(0u);
x_35 = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0;
x_36 = lean_box(x_2);
x_37 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_37, 0, x_36);
x_38 = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(x_38, 0, x_32);
lean_ctor_set(x_38, 1, x_35);
lean_ctor_set(x_38, 2, x_33);
lean_ctor_set(x_38, 3, x_37);
x_39 = lp_REPL_REPL_instToJsonCommand_toJson(x_38);
x_40 = l_Lean_Json_compress(x_39);
x_41 = lean_box(x_4);
lean_inc_ref(x_5);
lean_inc_ref(x_3);
x_42 = lean_alloc_closure((void*)(l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___lam__0___boxed), 5, 4);
lean_closure_set(x_42, 0, x_3);
lean_closure_set(x_42, 1, x_41);
lean_closure_set(x_42, 2, x_5);
lean_closure_set(x_42, 3, x_40);
x_43 = lean_io_as_task(x_42, x_34);
x_44 = lean_array_uset(x_8, x_7, x_34);
x_45 = 1;
x_46 = lean_usize_add(x_7, x_45);
x_47 = lean_array_uset(x_44, x_7, x_43);
x_7 = x_46;
x_8 = x_47;
goto _start;
}
}
}
}
static lean_object* _init_l_NativeBranchBackend_batch___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("this experiment supports the prepared env=0 naive batch without internal timeout", 80, 80);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_batch___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_batch___closed__0;
x_2 = lean_alloc_ctor(18, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_batch___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_batch___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_batch___closed__2;
x_2 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_2, 0, x_1);
lean_ctor_set(x_2, 1, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_batch___closed__4() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("gpu_smt_batch", 13, 13);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_batch___closed__5() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("naive", 5, 5);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_batch___closed__6() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_batch___closed__5;
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NativeBranchBackend_batch_spec__1(lean_object* x_1, size_t x_2, size_t x_3, lean_object* x_4) {
_start:
{
uint8_t x_6; 
x_6 = lean_usize_dec_lt(x_3, x_2);
if (x_6 == 0)
{
lean_object* x_7; 
x_7 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_7, 0, x_4);
return x_7;
}
else
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_8 = lean_array_uget(x_1, x_3);
x_9 = lean_task_get_own(x_8);
x_10 = l_IO_ofExcept___at___00Lean_Server_FileWorker_handleImportCompletionRequest_spec__0___redArg(x_9);
if (lean_obj_tag(x_10) == 0)
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; lean_object* x_63; lean_object* x_64; lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_74; lean_object* x_75; lean_object* x_76; lean_object* x_77; lean_object* x_84; lean_object* x_85; lean_object* x_86; lean_object* x_93; lean_object* x_100; lean_object* x_101; 
x_11 = lean_ctor_get(x_10, 0);
lean_inc(x_11);
lean_dec_ref(x_10);
x_12 = lean_ctor_get(x_4, 0);
lean_inc(x_12);
x_13 = lean_ctor_get(x_4, 1);
lean_inc(x_13);
if (lean_is_exclusive(x_4)) {
 lean_ctor_release(x_4, 0);
 lean_ctor_release(x_4, 1);
 x_14 = x_4;
} else {
 lean_dec_ref(x_4);
 x_14 = lean_box(0);
}
x_100 = l_NativeBranchBackend_execute___closed__4;
lean_inc(x_11);
x_101 = l_Lean_Json_getObjVal_x3f(x_11, x_100);
if (lean_obj_tag(x_101) == 0)
{
lean_object* x_102; 
lean_dec_ref(x_101);
x_102 = lean_box(0);
x_93 = x_102;
goto block_99;
}
else
{
lean_object* x_103; 
x_103 = lean_ctor_get(x_101, 0);
lean_inc(x_103);
lean_dec_ref(x_101);
x_93 = x_103;
goto block_99;
}
block_37:
{
lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; size_t x_34; size_t x_35; 
x_23 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_23, 0, x_18);
lean_ctor_set(x_23, 1, x_22);
x_24 = lean_box(0);
x_25 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_25, 0, x_23);
lean_ctor_set(x_25, 1, x_24);
x_26 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_26, 0, x_20);
lean_ctor_set(x_26, 1, x_25);
x_27 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_27, 0, x_21);
lean_ctor_set(x_27, 1, x_26);
x_28 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_28, 0, x_17);
lean_ctor_set(x_28, 1, x_27);
x_29 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_29, 0, x_19);
lean_ctor_set(x_29, 1, x_28);
x_30 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_30, 0, x_16);
lean_ctor_set(x_30, 1, x_29);
x_31 = l_Lean_Json_mkObj(x_30);
x_32 = lean_array_push(x_12, x_31);
if (lean_is_scalar(x_14)) {
 x_33 = lean_alloc_ctor(0, 2, 0);
} else {
 x_33 = x_14;
}
lean_ctor_set(x_33, 0, x_32);
lean_ctor_set(x_33, 1, x_15);
x_34 = 1;
x_35 = lean_usize_add(x_3, x_34);
x_3 = x_35;
x_4 = x_33;
goto _start;
}
block_50:
{
lean_object* x_45; lean_object* x_46; lean_object* x_47; 
x_45 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_45, 0, x_41);
lean_ctor_set(x_45, 1, x_44);
x_46 = l_NativeBranchBackend_execute___closed__0;
x_47 = l_Lean_Json_getObjVal_x3f(x_11, x_46);
if (lean_obj_tag(x_47) == 0)
{
lean_object* x_48; 
lean_dec_ref(x_47);
x_48 = lean_box(0);
x_15 = x_40;
x_16 = x_39;
x_17 = x_38;
x_18 = x_46;
x_19 = x_42;
x_20 = x_45;
x_21 = x_43;
x_22 = x_48;
goto block_37;
}
else
{
lean_object* x_49; 
x_49 = lean_ctor_get(x_47, 0);
lean_inc(x_49);
lean_dec_ref(x_47);
x_15 = x_40;
x_16 = x_39;
x_17 = x_38;
x_18 = x_46;
x_19 = x_42;
x_20 = x_45;
x_21 = x_43;
x_22 = x_49;
goto block_37;
}
}
block_62:
{
lean_object* x_57; lean_object* x_58; lean_object* x_59; 
x_57 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_57, 0, x_54);
lean_ctor_set(x_57, 1, x_56);
x_58 = l_NativeBranchBackend_execute___closed__6;
lean_inc(x_11);
x_59 = l_Lean_Json_getObjVal_x3f(x_11, x_58);
if (lean_obj_tag(x_59) == 0)
{
lean_object* x_60; 
lean_dec_ref(x_59);
x_60 = lean_box(0);
x_38 = x_53;
x_39 = x_52;
x_40 = x_51;
x_41 = x_58;
x_42 = x_55;
x_43 = x_57;
x_44 = x_60;
goto block_50;
}
else
{
lean_object* x_61; 
x_61 = lean_ctor_get(x_59, 0);
lean_inc(x_61);
lean_dec_ref(x_59);
x_38 = x_53;
x_39 = x_52;
x_40 = x_51;
x_41 = x_58;
x_42 = x_55;
x_43 = x_57;
x_44 = x_61;
goto block_50;
}
}
block_73:
{
lean_object* x_68; lean_object* x_69; lean_object* x_70; 
x_68 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_68, 0, x_66);
lean_ctor_set(x_68, 1, x_67);
x_69 = l_NativeBranchBackend_execute___closed__3;
lean_inc(x_11);
x_70 = l_Lean_Json_getObjVal_x3f(x_11, x_69);
if (lean_obj_tag(x_70) == 0)
{
lean_object* x_71; 
lean_dec_ref(x_70);
x_71 = lean_box(0);
x_51 = x_64;
x_52 = x_63;
x_53 = x_68;
x_54 = x_69;
x_55 = x_65;
x_56 = x_71;
goto block_62;
}
else
{
lean_object* x_72; 
x_72 = lean_ctor_get(x_70, 0);
lean_inc(x_72);
lean_dec_ref(x_70);
x_51 = x_64;
x_52 = x_63;
x_53 = x_68;
x_54 = x_69;
x_55 = x_65;
x_56 = x_72;
goto block_62;
}
}
block_83:
{
lean_object* x_78; lean_object* x_79; lean_object* x_80; 
x_78 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_78, 0, x_76);
lean_ctor_set(x_78, 1, x_77);
x_79 = l_NativeBranchBackend_execute___closed__2;
lean_inc(x_11);
x_80 = l_Lean_Json_getObjVal_x3f(x_11, x_79);
if (lean_obj_tag(x_80) == 0)
{
lean_object* x_81; 
lean_dec_ref(x_80);
x_81 = lean_box(0);
x_63 = x_75;
x_64 = x_74;
x_65 = x_78;
x_66 = x_79;
x_67 = x_81;
goto block_73;
}
else
{
lean_object* x_82; 
x_82 = lean_ctor_get(x_80, 0);
lean_inc(x_82);
lean_dec_ref(x_80);
x_63 = x_75;
x_64 = x_74;
x_65 = x_78;
x_66 = x_79;
x_67 = x_82;
goto block_73;
}
}
block_92:
{
lean_object* x_87; lean_object* x_88; lean_object* x_89; 
x_87 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_87, 0, x_85);
lean_ctor_set(x_87, 1, x_86);
x_88 = l_NativeBranchBackend_execute___closed__1;
lean_inc(x_11);
x_89 = l_Lean_Json_getObjVal_x3f(x_11, x_88);
if (lean_obj_tag(x_89) == 0)
{
lean_object* x_90; 
lean_dec_ref(x_89);
x_90 = lean_box(0);
x_74 = x_84;
x_75 = x_87;
x_76 = x_88;
x_77 = x_90;
goto block_83;
}
else
{
lean_object* x_91; 
x_91 = lean_ctor_get(x_89, 0);
lean_inc(x_91);
lean_dec_ref(x_89);
x_74 = x_84;
x_75 = x_87;
x_76 = x_88;
x_77 = x_91;
goto block_83;
}
}
block_99:
{
lean_object* x_94; lean_object* x_95; lean_object* x_96; 
x_94 = lean_array_push(x_13, x_93);
x_95 = l_NativeBranchBackend_execute___closed__5;
lean_inc(x_11);
x_96 = l_Lean_Json_getObjVal_x3f(x_11, x_95);
if (lean_obj_tag(x_96) == 0)
{
lean_object* x_97; 
lean_dec_ref(x_96);
x_97 = lean_box(0);
x_84 = x_94;
x_85 = x_95;
x_86 = x_97;
goto block_92;
}
else
{
lean_object* x_98; 
x_98 = lean_ctor_get(x_96, 0);
lean_inc(x_98);
lean_dec_ref(x_96);
x_84 = x_94;
x_85 = x_95;
x_86 = x_98;
goto block_92;
}
}
}
else
{
uint8_t x_104; 
lean_dec_ref(x_4);
x_104 = !lean_is_exclusive(x_10);
if (x_104 == 0)
{
return x_10;
}
else
{
lean_object* x_105; lean_object* x_106; 
x_105 = lean_ctor_get(x_10, 0);
lean_inc(x_105);
lean_dec(x_10);
x_106 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_106, 0, x_105);
return x_106;
}
}
}
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_batch(lean_object* x_1, uint8_t x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_6; lean_object* x_7; 
x_6 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_4);
x_7 = l_IO_ofExcept___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0___redArg(x_6);
if (lean_obj_tag(x_7) == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_13; lean_object* x_14; lean_object* x_15; uint8_t x_16; lean_object* x_70; uint8_t x_71; 
x_8 = lean_ctor_get(x_7, 0);
lean_inc(x_8);
if (lean_is_exclusive(x_7)) {
 lean_ctor_release(x_7, 0);
 x_9 = x_7;
} else {
 lean_dec_ref(x_7);
 x_9 = lean_box(0);
}
x_13 = lean_ctor_get(x_8, 0);
x_14 = lean_ctor_get(x_8, 1);
x_15 = lean_ctor_get(x_8, 2);
lean_inc_ref(x_15);
x_70 = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0;
x_71 = l_Option_instBEq_beq___at___00__private_Lean_Elab_Quotation_0__Lean_Elab_Term_Quotation_getHeadInfo_spec__11(x_14, x_70);
if (x_71 == 0)
{
x_16 = x_71;
goto block_69;
}
else
{
lean_object* x_72; lean_object* x_73; uint8_t x_74; 
x_72 = lean_ctor_get(x_13, 1);
x_73 = l_NativeBranchBackend_batch___closed__6;
x_74 = l_Option_instBEq_beq___at___00Lean_forEachModuleInDir___at___00ImportCompletion_collectAvailableImportsFromSrcSearchPath_spec__0_spec__0(x_72, x_73);
x_16 = x_74;
goto block_69;
}
block_12:
{
lean_object* x_10; lean_object* x_11; 
x_10 = l_NativeBranchBackend_batch___closed__1;
if (lean_is_scalar(x_9)) {
 x_11 = lean_alloc_ctor(1, 1, 0);
} else {
 x_11 = x_9;
 lean_ctor_set_tag(x_11, 1);
}
lean_ctor_set(x_11, 0, x_10);
return x_11;
}
block_69:
{
if (x_16 == 0)
{
lean_dec_ref(x_15);
lean_dec(x_8);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
goto block_12;
}
else
{
lean_object* x_17; 
x_17 = lean_ctor_get(x_13, 3);
if (lean_obj_tag(x_17) == 0)
{
size_t x_18; size_t x_19; lean_object* x_20; 
lean_dec(x_9);
x_18 = lean_array_size(x_15);
x_19 = 0;
x_20 = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0(x_8, x_16, x_1, x_2, x_3, x_18, x_19, x_15);
if (lean_obj_tag(x_20) == 0)
{
lean_object* x_21; lean_object* x_22; size_t x_23; lean_object* x_24; 
x_21 = lean_ctor_get(x_20, 0);
lean_inc(x_21);
lean_dec_ref(x_20);
x_22 = l_NativeBranchBackend_batch___closed__3;
x_23 = lean_array_size(x_21);
x_24 = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NativeBranchBackend_batch_spec__1(x_21, x_23, x_19, x_22);
lean_dec(x_21);
if (lean_obj_tag(x_24) == 0)
{
lean_object* x_25; uint8_t x_26; 
x_25 = lean_ctor_get(x_24, 0);
lean_inc(x_25);
lean_dec_ref(x_24);
x_26 = !lean_is_exclusive(x_25);
if (x_26 == 0)
{
lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; 
x_27 = lean_ctor_get(x_25, 0);
x_28 = lean_ctor_get(x_25, 1);
x_29 = lean_get_stderr();
x_30 = l_NativeBranchBackend_batch___closed__4;
x_31 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_31, 0, x_27);
lean_ctor_set(x_25, 1, x_31);
lean_ctor_set(x_25, 0, x_30);
x_32 = lean_box(0);
x_33 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_33, 0, x_25);
lean_ctor_set(x_33, 1, x_32);
x_34 = l_Lean_Json_mkObj(x_33);
x_35 = l_Lean_Json_compress(x_34);
lean_inc_ref(x_29);
x_36 = l_IO_FS_Stream_putStrLn(x_29, x_35);
if (lean_obj_tag(x_36) == 0)
{
lean_object* x_37; lean_object* x_38; 
lean_dec_ref(x_36);
x_37 = lean_ctor_get(x_29, 0);
lean_inc_ref(x_37);
lean_dec_ref(x_29);
x_38 = lean_apply_1(x_37, lean_box(0));
if (lean_obj_tag(x_38) == 0)
{
uint8_t x_39; 
x_39 = !lean_is_exclusive(x_38);
if (x_39 == 0)
{
lean_object* x_40; lean_object* x_41; lean_object* x_42; 
x_40 = lean_ctor_get(x_38, 0);
lean_dec(x_40);
lean_ctor_set_tag(x_38, 4);
lean_ctor_set(x_38, 0, x_28);
x_41 = l_Lean_Json_compress(x_38);
x_42 = gpu_smt_emit_line(x_41);
return x_42;
}
else
{
lean_object* x_43; lean_object* x_44; lean_object* x_45; 
lean_dec(x_38);
x_43 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_43, 0, x_28);
x_44 = l_Lean_Json_compress(x_43);
x_45 = gpu_smt_emit_line(x_44);
return x_45;
}
}
else
{
lean_dec(x_28);
return x_38;
}
}
else
{
lean_dec_ref(x_29);
lean_dec(x_28);
return x_36;
}
}
else
{
lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; 
x_46 = lean_ctor_get(x_25, 0);
x_47 = lean_ctor_get(x_25, 1);
lean_inc(x_47);
lean_inc(x_46);
lean_dec(x_25);
x_48 = lean_get_stderr();
x_49 = l_NativeBranchBackend_batch___closed__4;
x_50 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_50, 0, x_46);
x_51 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_51, 0, x_49);
lean_ctor_set(x_51, 1, x_50);
x_52 = lean_box(0);
x_53 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_53, 0, x_51);
lean_ctor_set(x_53, 1, x_52);
x_54 = l_Lean_Json_mkObj(x_53);
x_55 = l_Lean_Json_compress(x_54);
lean_inc_ref(x_48);
x_56 = l_IO_FS_Stream_putStrLn(x_48, x_55);
if (lean_obj_tag(x_56) == 0)
{
lean_object* x_57; lean_object* x_58; 
lean_dec_ref(x_56);
x_57 = lean_ctor_get(x_48, 0);
lean_inc_ref(x_57);
lean_dec_ref(x_48);
x_58 = lean_apply_1(x_57, lean_box(0));
if (lean_obj_tag(x_58) == 0)
{
lean_object* x_59; lean_object* x_60; lean_object* x_61; lean_object* x_62; 
if (lean_is_exclusive(x_58)) {
 lean_ctor_release(x_58, 0);
 x_59 = x_58;
} else {
 lean_dec_ref(x_58);
 x_59 = lean_box(0);
}
if (lean_is_scalar(x_59)) {
 x_60 = lean_alloc_ctor(4, 1, 0);
} else {
 x_60 = x_59;
 lean_ctor_set_tag(x_60, 4);
}
lean_ctor_set(x_60, 0, x_47);
x_61 = l_Lean_Json_compress(x_60);
x_62 = gpu_smt_emit_line(x_61);
return x_62;
}
else
{
lean_dec(x_47);
return x_58;
}
}
else
{
lean_dec_ref(x_48);
lean_dec(x_47);
return x_56;
}
}
}
else
{
uint8_t x_63; 
x_63 = !lean_is_exclusive(x_24);
if (x_63 == 0)
{
return x_24;
}
else
{
lean_object* x_64; lean_object* x_65; 
x_64 = lean_ctor_get(x_24, 0);
lean_inc(x_64);
lean_dec(x_24);
x_65 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_65, 0, x_64);
return x_65;
}
}
}
else
{
uint8_t x_66; 
x_66 = !lean_is_exclusive(x_20);
if (x_66 == 0)
{
return x_20;
}
else
{
lean_object* x_67; lean_object* x_68; 
x_67 = lean_ctor_get(x_20, 0);
lean_inc(x_67);
lean_dec(x_20);
x_68 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_68, 0, x_67);
return x_68;
}
}
}
else
{
lean_dec_ref(x_15);
lean_dec(x_8);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
goto block_12;
}
}
}
}
else
{
uint8_t x_75; 
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_75 = !lean_is_exclusive(x_7);
if (x_75 == 0)
{
return x_7;
}
else
{
lean_object* x_76; lean_object* x_77; 
x_76 = lean_ctor_get(x_7, 0);
lean_inc(x_76);
lean_dec(x_7);
x_77 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_77, 0, x_76);
return x_77;
}
}
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9) {
_start:
{
uint8_t x_10; uint8_t x_11; size_t x_12; size_t x_13; lean_object* x_14; 
x_10 = lean_unbox(x_2);
x_11 = lean_unbox(x_4);
x_12 = lean_unbox_usize(x_6);
lean_dec(x_6);
x_13 = lean_unbox_usize(x_7);
lean_dec(x_7);
x_14 = l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0(x_1, x_10, x_3, x_11, x_5, x_12, x_13, x_8);
return x_14;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_batch___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; lean_object* x_7; 
x_6 = lean_unbox(x_2);
x_7 = l_NativeBranchBackend_batch(x_1, x_6, x_3, x_4);
return x_7;
}
}
LEAN_EXPORT lean_object* l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NativeBranchBackend_batch_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
size_t x_6; size_t x_7; lean_object* x_8; 
x_6 = lean_unbox_usize(x_2);
lean_dec(x_2);
x_7 = lean_unbox_usize(x_3);
lean_dec(x_3);
x_8 = l___private_Init_Data_Array_Basic_0__Array_forIn_x27Unsafe_loop___at___00NativeBranchBackend_batch_spec__1(x_1, x_6, x_7, x_4);
lean_dec_ref(x_1);
return x_8;
}
}
static lean_object* _init_l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("cmds", 4, 4);
return x_1;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg(lean_object* x_1, uint8_t x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_getLines();
if (lean_obj_tag(x_6) == 0)
{
uint8_t x_7; 
x_7 = !lean_is_exclusive(x_6);
if (x_7 == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; uint8_t x_15; 
x_8 = lean_ctor_get(x_6, 0);
x_9 = lean_unsigned_to_nat(0u);
x_10 = lean_string_utf8_byte_size(x_8);
lean_inc(x_8);
x_11 = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(x_11, 0, x_8);
lean_ctor_set(x_11, 1, x_9);
lean_ctor_set(x_11, 2, x_10);
x_12 = l_String_Slice_trimAscii(x_11);
lean_dec_ref(x_11);
x_13 = l_String_Slice_toString(x_12);
lean_dec_ref(x_12);
x_14 = lean_string_utf8_byte_size(x_13);
lean_dec_ref(x_13);
x_15 = lean_nat_dec_eq(x_14, x_9);
if (x_15 == 0)
{
lean_object* x_16; lean_object* x_17; 
lean_free_object(x_6);
lean_inc(x_8);
x_16 = l_Lean_Json_parse(x_8);
x_17 = l_IO_ofExcept___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0___redArg(x_16);
if (lean_obj_tag(x_17) == 0)
{
lean_object* x_18; lean_object* x_22; lean_object* x_23; 
x_18 = lean_ctor_get(x_17, 0);
lean_inc(x_18);
lean_dec_ref(x_17);
x_22 = l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___closed__0;
lean_inc(x_18);
x_23 = l_Lean_Json_getObjVal_x3f(x_18, x_22);
if (lean_obj_tag(x_23) == 0)
{
lean_dec_ref(x_23);
if (x_15 == 0)
{
lean_object* x_24; 
lean_dec(x_18);
lean_inc_ref(x_3);
lean_inc_ref(x_1);
x_24 = l_NativeBranchBackend_execute(x_1, x_2, x_3, x_8);
if (lean_obj_tag(x_24) == 0)
{
lean_object* x_25; lean_object* x_26; lean_object* x_27; 
x_25 = lean_ctor_get(x_24, 0);
lean_inc(x_25);
lean_dec_ref(x_24);
x_26 = l_Lean_Json_compress(x_25);
x_27 = gpu_smt_emit_line(x_26);
if (lean_obj_tag(x_27) == 0)
{
lean_dec_ref(x_27);
goto _start;
}
else
{
lean_dec_ref(x_3);
lean_dec_ref(x_1);
return x_27;
}
}
else
{
uint8_t x_29; 
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_29 = !lean_is_exclusive(x_24);
if (x_29 == 0)
{
return x_24;
}
else
{
lean_object* x_30; lean_object* x_31; 
x_30 = lean_ctor_get(x_24, 0);
lean_inc(x_30);
lean_dec(x_24);
x_31 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_31, 0, x_30);
return x_31;
}
}
}
else
{
lean_dec(x_8);
goto block_21;
}
}
else
{
lean_dec_ref(x_23);
lean_dec(x_8);
goto block_21;
}
block_21:
{
lean_object* x_19; 
lean_inc_ref(x_3);
lean_inc_ref(x_1);
x_19 = l_NativeBranchBackend_batch(x_1, x_2, x_3, x_18);
if (lean_obj_tag(x_19) == 0)
{
lean_dec_ref(x_19);
goto _start;
}
else
{
lean_dec_ref(x_3);
lean_dec_ref(x_1);
return x_19;
}
}
}
else
{
uint8_t x_32; 
lean_dec(x_8);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_32 = !lean_is_exclusive(x_17);
if (x_32 == 0)
{
return x_17;
}
else
{
lean_object* x_33; lean_object* x_34; 
x_33 = lean_ctor_get(x_17, 0);
lean_inc(x_33);
lean_dec(x_17);
x_34 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_34, 0, x_33);
return x_34;
}
}
}
else
{
lean_dec(x_8);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
lean_ctor_set(x_6, 0, x_4);
return x_6;
}
}
else
{
lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; uint8_t x_42; 
x_35 = lean_ctor_get(x_6, 0);
lean_inc(x_35);
lean_dec(x_6);
x_36 = lean_unsigned_to_nat(0u);
x_37 = lean_string_utf8_byte_size(x_35);
lean_inc(x_35);
x_38 = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(x_38, 0, x_35);
lean_ctor_set(x_38, 1, x_36);
lean_ctor_set(x_38, 2, x_37);
x_39 = l_String_Slice_trimAscii(x_38);
lean_dec_ref(x_38);
x_40 = l_String_Slice_toString(x_39);
lean_dec_ref(x_39);
x_41 = lean_string_utf8_byte_size(x_40);
lean_dec_ref(x_40);
x_42 = lean_nat_dec_eq(x_41, x_36);
if (x_42 == 0)
{
lean_object* x_43; lean_object* x_44; 
lean_inc(x_35);
x_43 = l_Lean_Json_parse(x_35);
x_44 = l_IO_ofExcept___at___00__private_Lean_Shell_0__Lean_shellMain_spec__0___redArg(x_43);
if (lean_obj_tag(x_44) == 0)
{
lean_object* x_45; lean_object* x_49; lean_object* x_50; 
x_45 = lean_ctor_get(x_44, 0);
lean_inc(x_45);
lean_dec_ref(x_44);
x_49 = l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___closed__0;
lean_inc(x_45);
x_50 = l_Lean_Json_getObjVal_x3f(x_45, x_49);
if (lean_obj_tag(x_50) == 0)
{
lean_dec_ref(x_50);
if (x_42 == 0)
{
lean_object* x_51; 
lean_dec(x_45);
lean_inc_ref(x_3);
lean_inc_ref(x_1);
x_51 = l_NativeBranchBackend_execute(x_1, x_2, x_3, x_35);
if (lean_obj_tag(x_51) == 0)
{
lean_object* x_52; lean_object* x_53; lean_object* x_54; 
x_52 = lean_ctor_get(x_51, 0);
lean_inc(x_52);
lean_dec_ref(x_51);
x_53 = l_Lean_Json_compress(x_52);
x_54 = gpu_smt_emit_line(x_53);
if (lean_obj_tag(x_54) == 0)
{
lean_dec_ref(x_54);
goto _start;
}
else
{
lean_dec_ref(x_3);
lean_dec_ref(x_1);
return x_54;
}
}
else
{
lean_object* x_56; lean_object* x_57; lean_object* x_58; 
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_56 = lean_ctor_get(x_51, 0);
lean_inc(x_56);
if (lean_is_exclusive(x_51)) {
 lean_ctor_release(x_51, 0);
 x_57 = x_51;
} else {
 lean_dec_ref(x_51);
 x_57 = lean_box(0);
}
if (lean_is_scalar(x_57)) {
 x_58 = lean_alloc_ctor(1, 1, 0);
} else {
 x_58 = x_57;
}
lean_ctor_set(x_58, 0, x_56);
return x_58;
}
}
else
{
lean_dec(x_35);
goto block_48;
}
}
else
{
lean_dec_ref(x_50);
lean_dec(x_35);
goto block_48;
}
block_48:
{
lean_object* x_46; 
lean_inc_ref(x_3);
lean_inc_ref(x_1);
x_46 = l_NativeBranchBackend_batch(x_1, x_2, x_3, x_45);
if (lean_obj_tag(x_46) == 0)
{
lean_dec_ref(x_46);
goto _start;
}
else
{
lean_dec_ref(x_3);
lean_dec_ref(x_1);
return x_46;
}
}
}
else
{
lean_object* x_59; lean_object* x_60; lean_object* x_61; 
lean_dec(x_35);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_59 = lean_ctor_get(x_44, 0);
lean_inc(x_59);
if (lean_is_exclusive(x_44)) {
 lean_ctor_release(x_44, 0);
 x_60 = x_44;
} else {
 lean_dec_ref(x_44);
 x_60 = lean_box(0);
}
if (lean_is_scalar(x_60)) {
 x_61 = lean_alloc_ctor(1, 1, 0);
} else {
 x_61 = x_60;
}
lean_ctor_set(x_61, 0, x_59);
return x_61;
}
}
else
{
lean_object* x_62; 
lean_dec(x_35);
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_62 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_62, 0, x_4);
return x_62;
}
}
}
else
{
uint8_t x_63; 
lean_dec_ref(x_3);
lean_dec_ref(x_1);
x_63 = !lean_is_exclusive(x_6);
if (x_63 == 0)
{
return x_6;
}
else
{
lean_object* x_64; lean_object* x_65; 
x_64 = lean_ctor_get(x_6, 0);
lean_inc(x_64);
lean_dec(x_6);
x_65 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_65, 0, x_64);
return x_65;
}
}
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_run___redArg___closed__0;
x_2 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_2, 0, x_1);
lean_ctor_set(x_2, 1, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("first command must prepare the original import root", 51, 51);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_run___redArg___closed__2;
x_2 = lean_alloc_ctor(18, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__4() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("1", 1, 1);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__5() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_NativeBranchBackend_run___redArg___closed__4;
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__6() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("lean", 4, 4);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__7() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("LEAN_SERVER_NATIVE_DYNLIB", 25, 25);
return x_1;
}
}
static lean_object* _init_l_NativeBranchBackend_run___redArg___closed__8() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("\n", 1, 1);
return x_1;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_run___redArg() {
_start:
{
uint8_t x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_15; lean_object* x_16; uint8_t x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; uint8_t x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_58; uint8_t x_59; lean_object* x_170; lean_object* x_178; lean_object* x_179; 
x_178 = l_NativeBranchBackend_run___redArg___closed__6;
x_179 = l_Lean_findSysroot(x_178);
if (lean_obj_tag(x_179) == 0)
{
lean_object* x_180; lean_object* x_181; lean_object* x_182; 
x_180 = lean_ctor_get(x_179, 0);
lean_inc(x_180);
lean_dec_ref(x_179);
x_181 = lean_box(0);
x_182 = l_Lean_initSearchPath(x_180, x_181);
if (lean_obj_tag(x_182) == 0)
{
lean_object* x_183; lean_object* x_184; 
lean_dec_ref(x_182);
x_183 = l_NativeBranchBackend_run___redArg___closed__7;
x_184 = lean_io_getenv(x_183);
if (lean_obj_tag(x_184) == 1)
{
lean_object* x_185; lean_object* x_186; 
x_185 = lean_ctor_get(x_184, 0);
lean_inc(x_185);
lean_dec_ref(x_184);
x_186 = l_IO_FS_readFile(x_185);
lean_dec(x_185);
if (lean_obj_tag(x_186) == 0)
{
lean_object* x_187; lean_object* x_188; lean_object* x_189; lean_object* x_190; lean_object* x_191; lean_object* x_192; 
x_187 = lean_ctor_get(x_186, 0);
lean_inc(x_187);
lean_dec_ref(x_186);
x_188 = l_NativeBranchBackend_run___redArg___closed__8;
x_189 = lean_unsigned_to_nat(0u);
x_190 = l_String_splitOnAux(x_187, x_188, x_189, x_189, x_189, x_181);
lean_dec(x_187);
x_191 = lean_box(0);
x_192 = lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg(x_191, x_190, x_191);
if (lean_obj_tag(x_192) == 0)
{
lean_dec_ref(x_192);
x_170 = lean_box(0);
goto block_177;
}
else
{
return x_192;
}
}
else
{
uint8_t x_193; 
x_193 = !lean_is_exclusive(x_186);
if (x_193 == 0)
{
return x_186;
}
else
{
lean_object* x_194; lean_object* x_195; 
x_194 = lean_ctor_get(x_186, 0);
lean_inc(x_194);
lean_dec(x_186);
x_195 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_195, 0, x_194);
return x_195;
}
}
}
else
{
lean_dec(x_184);
x_170 = lean_box(0);
goto block_177;
}
}
else
{
return x_182;
}
}
else
{
uint8_t x_196; 
x_196 = !lean_is_exclusive(x_179);
if (x_196 == 0)
{
return x_179;
}
else
{
lean_object* x_197; lean_object* x_198; 
x_197 = lean_ctor_get(x_179, 0);
lean_inc(x_197);
lean_dec(x_179);
x_198 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_198, 0, x_197);
return x_198;
}
}
block_14:
{
lean_object* x_7; lean_object* x_8; 
x_7 = l_Lean_Json_compress(x_6);
x_8 = gpu_smt_emit_line(x_7);
if (lean_obj_tag(x_8) == 0)
{
lean_object* x_9; lean_object* x_10; 
lean_dec_ref(x_8);
x_9 = lean_box(0);
x_10 = l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg(x_3, x_2, x_4, x_9);
if (lean_obj_tag(x_10) == 0)
{
uint8_t x_11; 
x_11 = !lean_is_exclusive(x_10);
if (x_11 == 0)
{
lean_object* x_12; 
x_12 = lean_ctor_get(x_10, 0);
lean_dec(x_12);
lean_ctor_set(x_10, 0, x_9);
return x_10;
}
else
{
lean_object* x_13; 
lean_dec(x_10);
x_13 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_13, 0, x_9);
return x_13;
}
}
else
{
return x_10;
}
}
else
{
lean_dec_ref(x_4);
lean_dec_ref(x_3);
return x_8;
}
}
block_34:
{
lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; 
x_25 = lean_box(0);
x_26 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_26, 0, x_24);
lean_ctor_set(x_26, 1, x_25);
x_27 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_27, 0, x_23);
lean_ctor_set(x_27, 1, x_26);
x_28 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_28, 0, x_20);
lean_ctor_set(x_28, 1, x_27);
x_29 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_29, 0, x_22);
lean_ctor_set(x_29, 1, x_28);
x_30 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_30, 0, x_19);
lean_ctor_set(x_30, 1, x_29);
x_31 = lean_mk_empty_array_with_capacity(x_15);
x_32 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_30, x_31);
x_33 = l_Lean_Json_mkObj(x_32);
x_2 = x_17;
x_3 = x_16;
x_4 = x_18;
x_5 = lean_box(0);
x_6 = x_33;
goto block_14;
}
block_57:
{
lean_object* x_45; lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; 
x_45 = l_NativeBranchBackend_execute___closed__35;
x_46 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_45, x_36);
x_47 = l_NativeBranchBackend_execute___closed__36;
x_48 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_47, x_37);
x_49 = l_NativeBranchBackend_execute___closed__37;
x_50 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(x_49, x_38);
if (lean_obj_tag(x_39) == 0)
{
lean_object* x_51; 
x_51 = lean_box(0);
x_15 = x_35;
x_16 = x_41;
x_17 = x_40;
x_18 = x_42;
x_19 = x_44;
x_20 = x_48;
x_21 = lean_box(0);
x_22 = x_46;
x_23 = x_50;
x_24 = x_51;
goto block_34;
}
else
{
lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; 
x_52 = lean_ctor_get(x_39, 0);
lean_inc(x_52);
lean_dec_ref(x_39);
x_53 = l_NativeBranchBackend_execute___closed__38;
x_54 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_54, 0, x_53);
lean_ctor_set(x_54, 1, x_52);
x_55 = lean_box(0);
x_56 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_56, 0, x_54);
lean_ctor_set(x_56, 1, x_55);
x_15 = x_35;
x_16 = x_41;
x_17 = x_40;
x_18 = x_42;
x_19 = x_44;
x_20 = x_48;
x_21 = lean_box(0);
x_22 = x_46;
x_23 = x_50;
x_24 = x_56;
goto block_34;
}
}
block_169:
{
lean_object* x_60; 
x_60 = lp_REPL_getLines();
if (lean_obj_tag(x_60) == 0)
{
lean_object* x_61; lean_object* x_62; 
x_61 = lean_ctor_get(x_60, 0);
lean_inc(x_61);
lean_dec_ref(x_60);
lean_inc(x_61);
x_62 = lp_REPL_parse(x_61);
if (lean_obj_tag(x_62) == 0)
{
uint8_t x_63; 
x_63 = !lean_is_exclusive(x_62);
if (x_63 == 0)
{
lean_object* x_64; 
x_64 = lean_ctor_get(x_62, 0);
if (lean_obj_tag(x_64) == 0)
{
lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_68; 
lean_free_object(x_62);
x_65 = lean_ctor_get(x_64, 0);
lean_inc_ref(x_65);
lean_dec_ref(x_64);
x_66 = lean_unsigned_to_nat(0u);
x_67 = l_NativeBranchBackend_run___redArg___closed__1;
x_68 = lp_REPL_REPL_runCommand(x_65, x_67);
if (lean_obj_tag(x_68) == 0)
{
lean_object* x_69; uint8_t x_70; 
x_69 = lean_ctor_get(x_68, 0);
lean_inc(x_69);
lean_dec_ref(x_68);
x_70 = !lean_is_exclusive(x_69);
if (x_70 == 0)
{
lean_object* x_71; lean_object* x_72; lean_object* x_73; 
x_71 = lean_ctor_get(x_69, 0);
x_72 = lean_ctor_get(x_69, 1);
x_73 = gpu_smt_prepare_refs();
if (lean_obj_tag(x_73) == 0)
{
lean_dec_ref(x_73);
if (lean_obj_tag(x_71) == 0)
{
lean_object* x_74; lean_object* x_75; 
x_74 = lean_ctor_get(x_71, 0);
lean_inc(x_74);
lean_dec_ref(x_71);
x_75 = lean_ctor_get(x_74, 0);
lean_inc(x_75);
if (lean_obj_tag(x_75) == 0)
{
lean_object* x_76; lean_object* x_77; lean_object* x_78; lean_object* x_79; lean_object* x_80; 
lean_free_object(x_69);
x_76 = lean_ctor_get(x_74, 1);
lean_inc(x_76);
x_77 = lean_ctor_get(x_74, 2);
lean_inc(x_77);
x_78 = lean_ctor_get(x_74, 3);
lean_inc(x_78);
x_79 = lean_ctor_get(x_74, 4);
lean_inc(x_79);
lean_dec(x_74);
x_80 = lean_box(0);
x_35 = x_66;
x_36 = x_76;
x_37 = x_77;
x_38 = x_78;
x_39 = x_79;
x_40 = x_59;
x_41 = x_72;
x_42 = x_61;
x_43 = lean_box(0);
x_44 = x_80;
goto block_57;
}
else
{
lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; uint8_t x_85; 
x_81 = lean_ctor_get(x_74, 1);
lean_inc(x_81);
x_82 = lean_ctor_get(x_74, 2);
lean_inc(x_82);
x_83 = lean_ctor_get(x_74, 3);
lean_inc(x_83);
x_84 = lean_ctor_get(x_74, 4);
lean_inc(x_84);
lean_dec(x_74);
x_85 = !lean_is_exclusive(x_75);
if (x_85 == 0)
{
lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; lean_object* x_90; 
x_86 = lean_ctor_get(x_75, 0);
x_87 = l_NativeBranchBackend_execute___closed__39;
x_88 = l_Lean_JsonNumber_fromNat(x_86);
lean_ctor_set_tag(x_75, 2);
lean_ctor_set(x_75, 0, x_88);
lean_ctor_set(x_69, 1, x_75);
lean_ctor_set(x_69, 0, x_87);
x_89 = lean_box(0);
x_90 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_90, 0, x_69);
lean_ctor_set(x_90, 1, x_89);
x_35 = x_66;
x_36 = x_81;
x_37 = x_82;
x_38 = x_83;
x_39 = x_84;
x_40 = x_59;
x_41 = x_72;
x_42 = x_61;
x_43 = lean_box(0);
x_44 = x_90;
goto block_57;
}
else
{
lean_object* x_91; lean_object* x_92; lean_object* x_93; lean_object* x_94; lean_object* x_95; lean_object* x_96; 
x_91 = lean_ctor_get(x_75, 0);
lean_inc(x_91);
lean_dec(x_75);
x_92 = l_NativeBranchBackend_execute___closed__39;
x_93 = l_Lean_JsonNumber_fromNat(x_91);
x_94 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_94, 0, x_93);
lean_ctor_set(x_69, 1, x_94);
lean_ctor_set(x_69, 0, x_92);
x_95 = lean_box(0);
x_96 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_96, 0, x_69);
lean_ctor_set(x_96, 1, x_95);
x_35 = x_66;
x_36 = x_81;
x_37 = x_82;
x_38 = x_83;
x_39 = x_84;
x_40 = x_59;
x_41 = x_72;
x_42 = x_61;
x_43 = lean_box(0);
x_44 = x_96;
goto block_57;
}
}
}
else
{
lean_object* x_97; lean_object* x_98; 
lean_free_object(x_69);
x_97 = lean_ctor_get(x_71, 0);
lean_inc(x_97);
lean_dec_ref(x_71);
x_98 = lp_REPL_REPL_instToJsonError_toJson(x_97);
x_2 = x_59;
x_3 = x_72;
x_4 = x_61;
x_5 = lean_box(0);
x_6 = x_98;
goto block_14;
}
}
else
{
lean_free_object(x_69);
lean_dec(x_72);
lean_dec(x_71);
lean_dec(x_61);
return x_73;
}
}
else
{
lean_object* x_99; lean_object* x_100; lean_object* x_101; 
x_99 = lean_ctor_get(x_69, 0);
x_100 = lean_ctor_get(x_69, 1);
lean_inc(x_100);
lean_inc(x_99);
lean_dec(x_69);
x_101 = gpu_smt_prepare_refs();
if (lean_obj_tag(x_101) == 0)
{
lean_dec_ref(x_101);
if (lean_obj_tag(x_99) == 0)
{
lean_object* x_102; lean_object* x_103; 
x_102 = lean_ctor_get(x_99, 0);
lean_inc(x_102);
lean_dec_ref(x_99);
x_103 = lean_ctor_get(x_102, 0);
lean_inc(x_103);
if (lean_obj_tag(x_103) == 0)
{
lean_object* x_104; lean_object* x_105; lean_object* x_106; lean_object* x_107; lean_object* x_108; 
x_104 = lean_ctor_get(x_102, 1);
lean_inc(x_104);
x_105 = lean_ctor_get(x_102, 2);
lean_inc(x_105);
x_106 = lean_ctor_get(x_102, 3);
lean_inc(x_106);
x_107 = lean_ctor_get(x_102, 4);
lean_inc(x_107);
lean_dec(x_102);
x_108 = lean_box(0);
x_35 = x_66;
x_36 = x_104;
x_37 = x_105;
x_38 = x_106;
x_39 = x_107;
x_40 = x_59;
x_41 = x_100;
x_42 = x_61;
x_43 = lean_box(0);
x_44 = x_108;
goto block_57;
}
else
{
lean_object* x_109; lean_object* x_110; lean_object* x_111; lean_object* x_112; lean_object* x_113; lean_object* x_114; lean_object* x_115; lean_object* x_116; lean_object* x_117; lean_object* x_118; lean_object* x_119; lean_object* x_120; 
x_109 = lean_ctor_get(x_102, 1);
lean_inc(x_109);
x_110 = lean_ctor_get(x_102, 2);
lean_inc(x_110);
x_111 = lean_ctor_get(x_102, 3);
lean_inc(x_111);
x_112 = lean_ctor_get(x_102, 4);
lean_inc(x_112);
lean_dec(x_102);
x_113 = lean_ctor_get(x_103, 0);
lean_inc(x_113);
if (lean_is_exclusive(x_103)) {
 lean_ctor_release(x_103, 0);
 x_114 = x_103;
} else {
 lean_dec_ref(x_103);
 x_114 = lean_box(0);
}
x_115 = l_NativeBranchBackend_execute___closed__39;
x_116 = l_Lean_JsonNumber_fromNat(x_113);
if (lean_is_scalar(x_114)) {
 x_117 = lean_alloc_ctor(2, 1, 0);
} else {
 x_117 = x_114;
 lean_ctor_set_tag(x_117, 2);
}
lean_ctor_set(x_117, 0, x_116);
x_118 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_118, 0, x_115);
lean_ctor_set(x_118, 1, x_117);
x_119 = lean_box(0);
x_120 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_120, 0, x_118);
lean_ctor_set(x_120, 1, x_119);
x_35 = x_66;
x_36 = x_109;
x_37 = x_110;
x_38 = x_111;
x_39 = x_112;
x_40 = x_59;
x_41 = x_100;
x_42 = x_61;
x_43 = lean_box(0);
x_44 = x_120;
goto block_57;
}
}
else
{
lean_object* x_121; lean_object* x_122; 
x_121 = lean_ctor_get(x_99, 0);
lean_inc(x_121);
lean_dec_ref(x_99);
x_122 = lp_REPL_REPL_instToJsonError_toJson(x_121);
x_2 = x_59;
x_3 = x_100;
x_4 = x_61;
x_5 = lean_box(0);
x_6 = x_122;
goto block_14;
}
}
else
{
lean_dec(x_100);
lean_dec(x_99);
lean_dec(x_61);
return x_101;
}
}
}
else
{
uint8_t x_123; 
lean_dec(x_61);
x_123 = !lean_is_exclusive(x_68);
if (x_123 == 0)
{
return x_68;
}
else
{
lean_object* x_124; lean_object* x_125; 
x_124 = lean_ctor_get(x_68, 0);
lean_inc(x_124);
lean_dec(x_68);
x_125 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_125, 0, x_124);
return x_125;
}
}
}
else
{
lean_object* x_126; 
lean_dec(x_64);
lean_dec(x_61);
x_126 = l_NativeBranchBackend_run___redArg___closed__3;
lean_ctor_set_tag(x_62, 1);
lean_ctor_set(x_62, 0, x_126);
return x_62;
}
}
else
{
lean_object* x_127; 
x_127 = lean_ctor_get(x_62, 0);
lean_inc(x_127);
lean_dec(x_62);
if (lean_obj_tag(x_127) == 0)
{
lean_object* x_128; lean_object* x_129; lean_object* x_130; lean_object* x_131; 
x_128 = lean_ctor_get(x_127, 0);
lean_inc_ref(x_128);
lean_dec_ref(x_127);
x_129 = lean_unsigned_to_nat(0u);
x_130 = l_NativeBranchBackend_run___redArg___closed__1;
x_131 = lp_REPL_REPL_runCommand(x_128, x_130);
if (lean_obj_tag(x_131) == 0)
{
lean_object* x_132; lean_object* x_133; lean_object* x_134; lean_object* x_135; lean_object* x_136; 
x_132 = lean_ctor_get(x_131, 0);
lean_inc(x_132);
lean_dec_ref(x_131);
x_133 = lean_ctor_get(x_132, 0);
lean_inc(x_133);
x_134 = lean_ctor_get(x_132, 1);
lean_inc(x_134);
if (lean_is_exclusive(x_132)) {
 lean_ctor_release(x_132, 0);
 lean_ctor_release(x_132, 1);
 x_135 = x_132;
} else {
 lean_dec_ref(x_132);
 x_135 = lean_box(0);
}
x_136 = gpu_smt_prepare_refs();
if (lean_obj_tag(x_136) == 0)
{
lean_dec_ref(x_136);
if (lean_obj_tag(x_133) == 0)
{
lean_object* x_137; lean_object* x_138; 
x_137 = lean_ctor_get(x_133, 0);
lean_inc(x_137);
lean_dec_ref(x_133);
x_138 = lean_ctor_get(x_137, 0);
lean_inc(x_138);
if (lean_obj_tag(x_138) == 0)
{
lean_object* x_139; lean_object* x_140; lean_object* x_141; lean_object* x_142; lean_object* x_143; 
lean_dec(x_135);
x_139 = lean_ctor_get(x_137, 1);
lean_inc(x_139);
x_140 = lean_ctor_get(x_137, 2);
lean_inc(x_140);
x_141 = lean_ctor_get(x_137, 3);
lean_inc(x_141);
x_142 = lean_ctor_get(x_137, 4);
lean_inc(x_142);
lean_dec(x_137);
x_143 = lean_box(0);
x_35 = x_129;
x_36 = x_139;
x_37 = x_140;
x_38 = x_141;
x_39 = x_142;
x_40 = x_59;
x_41 = x_134;
x_42 = x_61;
x_43 = lean_box(0);
x_44 = x_143;
goto block_57;
}
else
{
lean_object* x_144; lean_object* x_145; lean_object* x_146; lean_object* x_147; lean_object* x_148; lean_object* x_149; lean_object* x_150; lean_object* x_151; lean_object* x_152; lean_object* x_153; lean_object* x_154; lean_object* x_155; 
x_144 = lean_ctor_get(x_137, 1);
lean_inc(x_144);
x_145 = lean_ctor_get(x_137, 2);
lean_inc(x_145);
x_146 = lean_ctor_get(x_137, 3);
lean_inc(x_146);
x_147 = lean_ctor_get(x_137, 4);
lean_inc(x_147);
lean_dec(x_137);
x_148 = lean_ctor_get(x_138, 0);
lean_inc(x_148);
if (lean_is_exclusive(x_138)) {
 lean_ctor_release(x_138, 0);
 x_149 = x_138;
} else {
 lean_dec_ref(x_138);
 x_149 = lean_box(0);
}
x_150 = l_NativeBranchBackend_execute___closed__39;
x_151 = l_Lean_JsonNumber_fromNat(x_148);
if (lean_is_scalar(x_149)) {
 x_152 = lean_alloc_ctor(2, 1, 0);
} else {
 x_152 = x_149;
 lean_ctor_set_tag(x_152, 2);
}
lean_ctor_set(x_152, 0, x_151);
if (lean_is_scalar(x_135)) {
 x_153 = lean_alloc_ctor(0, 2, 0);
} else {
 x_153 = x_135;
}
lean_ctor_set(x_153, 0, x_150);
lean_ctor_set(x_153, 1, x_152);
x_154 = lean_box(0);
x_155 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_155, 0, x_153);
lean_ctor_set(x_155, 1, x_154);
x_35 = x_129;
x_36 = x_144;
x_37 = x_145;
x_38 = x_146;
x_39 = x_147;
x_40 = x_59;
x_41 = x_134;
x_42 = x_61;
x_43 = lean_box(0);
x_44 = x_155;
goto block_57;
}
}
else
{
lean_object* x_156; lean_object* x_157; 
lean_dec(x_135);
x_156 = lean_ctor_get(x_133, 0);
lean_inc(x_156);
lean_dec_ref(x_133);
x_157 = lp_REPL_REPL_instToJsonError_toJson(x_156);
x_2 = x_59;
x_3 = x_134;
x_4 = x_61;
x_5 = lean_box(0);
x_6 = x_157;
goto block_14;
}
}
else
{
lean_dec(x_135);
lean_dec(x_134);
lean_dec(x_133);
lean_dec(x_61);
return x_136;
}
}
else
{
lean_object* x_158; lean_object* x_159; lean_object* x_160; 
lean_dec(x_61);
x_158 = lean_ctor_get(x_131, 0);
lean_inc(x_158);
if (lean_is_exclusive(x_131)) {
 lean_ctor_release(x_131, 0);
 x_159 = x_131;
} else {
 lean_dec_ref(x_131);
 x_159 = lean_box(0);
}
if (lean_is_scalar(x_159)) {
 x_160 = lean_alloc_ctor(1, 1, 0);
} else {
 x_160 = x_159;
}
lean_ctor_set(x_160, 0, x_158);
return x_160;
}
}
else
{
lean_object* x_161; lean_object* x_162; 
lean_dec(x_127);
lean_dec(x_61);
x_161 = l_NativeBranchBackend_run___redArg___closed__3;
x_162 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_162, 0, x_161);
return x_162;
}
}
}
else
{
uint8_t x_163; 
lean_dec(x_61);
x_163 = !lean_is_exclusive(x_62);
if (x_163 == 0)
{
return x_62;
}
else
{
lean_object* x_164; lean_object* x_165; 
x_164 = lean_ctor_get(x_62, 0);
lean_inc(x_164);
lean_dec(x_62);
x_165 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_165, 0, x_164);
return x_165;
}
}
}
else
{
uint8_t x_166; 
x_166 = !lean_is_exclusive(x_60);
if (x_166 == 0)
{
return x_60;
}
else
{
lean_object* x_167; lean_object* x_168; 
x_167 = lean_ctor_get(x_60, 0);
lean_inc(x_167);
lean_dec(x_60);
x_168 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_168, 0, x_167);
return x_168;
}
}
}
block_177:
{
lean_object* x_171; lean_object* x_172; lean_object* x_173; uint8_t x_174; 
x_171 = l_NativeBranchBackend_execute___closed__24;
x_172 = lean_io_getenv(x_171);
x_173 = l_NativeBranchBackend_run___redArg___closed__5;
x_174 = l_Option_instBEq_beq___at___00Lean_forEachModuleInDir___at___00ImportCompletion_collectAvailableImportsFromSrcSearchPath_spec__0_spec__0(x_172, x_173);
lean_dec(x_172);
if (x_174 == 0)
{
uint8_t x_175; 
x_175 = 1;
x_58 = lean_box(0);
x_59 = x_175;
goto block_169;
}
else
{
uint8_t x_176; 
x_176 = 0;
x_58 = lean_box(0);
x_59 = x_176;
goto block_169;
}
}
}
}
LEAN_EXPORT lean_object* gpu_smt_native_backend(lean_object* x_1) {
_start:
{
lean_object* x_3; 
lean_dec(x_1);
x_3 = l_NativeBranchBackend_run___redArg();
return x_3;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0(lean_object* x_1, uint8_t x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_7; 
x_7 = l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg(x_1, x_2, x_3, x_4);
return x_7;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_run___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = gpu_smt_native_backend(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
uint8_t x_7; lean_object* x_8; 
x_7 = lean_unbox(x_2);
x_8 = l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0(x_1, x_7, x_3, x_4, x_5);
return x_8;
}
}
LEAN_EXPORT lean_object* l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; lean_object* x_7; 
x_6 = lean_unbox(x_2);
x_7 = l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg(x_1, x_6, x_3, x_4);
return x_7;
}
}
LEAN_EXPORT lean_object* l_NativeBranchBackend_run___redArg___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = l_NativeBranchBackend_run___redArg();
return x_2;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_REPL_REPL_Main(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_implementation_NativeBranchBackend(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Main(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
l_NativeBranchBackend_execute___closed__0 = _init_l_NativeBranchBackend_execute___closed__0();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__0);
l_NativeBranchBackend_execute___closed__1 = _init_l_NativeBranchBackend_execute___closed__1();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__1);
l_NativeBranchBackend_execute___closed__2 = _init_l_NativeBranchBackend_execute___closed__2();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__2);
l_NativeBranchBackend_execute___closed__3 = _init_l_NativeBranchBackend_execute___closed__3();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__3);
l_NativeBranchBackend_execute___closed__4 = _init_l_NativeBranchBackend_execute___closed__4();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__4);
l_NativeBranchBackend_execute___closed__5 = _init_l_NativeBranchBackend_execute___closed__5();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__5);
l_NativeBranchBackend_execute___closed__6 = _init_l_NativeBranchBackend_execute___closed__6();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__6);
l_NativeBranchBackend_execute___closed__7 = _init_l_NativeBranchBackend_execute___closed__7();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__7);
l_NativeBranchBackend_execute___closed__8 = _init_l_NativeBranchBackend_execute___closed__8();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__8);
l_NativeBranchBackend_execute___closed__9 = _init_l_NativeBranchBackend_execute___closed__9();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__9);
l_NativeBranchBackend_execute___closed__10 = _init_l_NativeBranchBackend_execute___closed__10();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__10);
l_NativeBranchBackend_execute___closed__11 = _init_l_NativeBranchBackend_execute___closed__11();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__11);
l_NativeBranchBackend_execute___closed__12 = _init_l_NativeBranchBackend_execute___closed__12();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__12);
l_NativeBranchBackend_execute___closed__13 = _init_l_NativeBranchBackend_execute___closed__13();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__13);
l_NativeBranchBackend_execute___closed__14 = _init_l_NativeBranchBackend_execute___closed__14();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__14);
l_NativeBranchBackend_execute___closed__15 = _init_l_NativeBranchBackend_execute___closed__15();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__15);
l_NativeBranchBackend_execute___closed__16 = _init_l_NativeBranchBackend_execute___closed__16();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__16);
l_NativeBranchBackend_execute___closed__17 = _init_l_NativeBranchBackend_execute___closed__17();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__17);
l_NativeBranchBackend_execute___closed__18 = _init_l_NativeBranchBackend_execute___closed__18();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__18);
l_NativeBranchBackend_execute___closed__19 = _init_l_NativeBranchBackend_execute___closed__19();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__19);
l_NativeBranchBackend_execute___closed__20 = _init_l_NativeBranchBackend_execute___closed__20();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__20);
l_NativeBranchBackend_execute___closed__21 = _init_l_NativeBranchBackend_execute___closed__21();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__21);
l_NativeBranchBackend_execute___closed__22 = _init_l_NativeBranchBackend_execute___closed__22();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__22);
l_NativeBranchBackend_execute___closed__23 = _init_l_NativeBranchBackend_execute___closed__23();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__23);
l_NativeBranchBackend_execute___closed__24 = _init_l_NativeBranchBackend_execute___closed__24();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__24);
l_NativeBranchBackend_execute___closed__25 = _init_l_NativeBranchBackend_execute___closed__25();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__25);
l_NativeBranchBackend_execute___closed__26 = _init_l_NativeBranchBackend_execute___closed__26();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__26);
l_NativeBranchBackend_execute___closed__27 = _init_l_NativeBranchBackend_execute___closed__27();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__27);
l_NativeBranchBackend_execute___closed__28 = _init_l_NativeBranchBackend_execute___closed__28();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__28);
l_NativeBranchBackend_execute___closed__29 = _init_l_NativeBranchBackend_execute___closed__29();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__29);
l_NativeBranchBackend_execute___closed__30 = _init_l_NativeBranchBackend_execute___closed__30();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__30);
l_NativeBranchBackend_execute___closed__31 = _init_l_NativeBranchBackend_execute___closed__31();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__31);
l_NativeBranchBackend_execute___closed__32 = _init_l_NativeBranchBackend_execute___closed__32();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__32);
l_NativeBranchBackend_execute___closed__33 = _init_l_NativeBranchBackend_execute___closed__33();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__33);
l_NativeBranchBackend_execute___closed__34 = _init_l_NativeBranchBackend_execute___closed__34();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__34);
l_NativeBranchBackend_execute___closed__35 = _init_l_NativeBranchBackend_execute___closed__35();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__35);
l_NativeBranchBackend_execute___closed__36 = _init_l_NativeBranchBackend_execute___closed__36();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__36);
l_NativeBranchBackend_execute___closed__37 = _init_l_NativeBranchBackend_execute___closed__37();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__37);
l_NativeBranchBackend_execute___closed__38 = _init_l_NativeBranchBackend_execute___closed__38();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__38);
l_NativeBranchBackend_execute___closed__39 = _init_l_NativeBranchBackend_execute___closed__39();
lean_mark_persistent(l_NativeBranchBackend_execute___closed__39);
l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0 = _init_l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0();
lean_mark_persistent(l___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00NativeBranchBackend_batch_spec__0___closed__0);
l_NativeBranchBackend_batch___closed__0 = _init_l_NativeBranchBackend_batch___closed__0();
lean_mark_persistent(l_NativeBranchBackend_batch___closed__0);
l_NativeBranchBackend_batch___closed__1 = _init_l_NativeBranchBackend_batch___closed__1();
lean_mark_persistent(l_NativeBranchBackend_batch___closed__1);
l_NativeBranchBackend_batch___closed__2 = _init_l_NativeBranchBackend_batch___closed__2();
lean_mark_persistent(l_NativeBranchBackend_batch___closed__2);
l_NativeBranchBackend_batch___closed__3 = _init_l_NativeBranchBackend_batch___closed__3();
lean_mark_persistent(l_NativeBranchBackend_batch___closed__3);
l_NativeBranchBackend_batch___closed__4 = _init_l_NativeBranchBackend_batch___closed__4();
lean_mark_persistent(l_NativeBranchBackend_batch___closed__4);
l_NativeBranchBackend_batch___closed__5 = _init_l_NativeBranchBackend_batch___closed__5();
lean_mark_persistent(l_NativeBranchBackend_batch___closed__5);
l_NativeBranchBackend_batch___closed__6 = _init_l_NativeBranchBackend_batch___closed__6();
lean_mark_persistent(l_NativeBranchBackend_batch___closed__6);
l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___closed__0 = _init_l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___closed__0();
lean_mark_persistent(l___private_Init_While_0__Lean_Loop_forIn_loop___at___00NativeBranchBackend_run_spec__0___redArg___closed__0);
l_NativeBranchBackend_run___redArg___closed__0 = _init_l_NativeBranchBackend_run___redArg___closed__0();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__0);
l_NativeBranchBackend_run___redArg___closed__1 = _init_l_NativeBranchBackend_run___redArg___closed__1();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__1);
l_NativeBranchBackend_run___redArg___closed__2 = _init_l_NativeBranchBackend_run___redArg___closed__2();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__2);
l_NativeBranchBackend_run___redArg___closed__3 = _init_l_NativeBranchBackend_run___redArg___closed__3();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__3);
l_NativeBranchBackend_run___redArg___closed__4 = _init_l_NativeBranchBackend_run___redArg___closed__4();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__4);
l_NativeBranchBackend_run___redArg___closed__5 = _init_l_NativeBranchBackend_run___redArg___closed__5();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__5);
l_NativeBranchBackend_run___redArg___closed__6 = _init_l_NativeBranchBackend_run___redArg___closed__6();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__6);
l_NativeBranchBackend_run___redArg___closed__7 = _init_l_NativeBranchBackend_run___redArg___closed__7();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__7);
l_NativeBranchBackend_run___redArg___closed__8 = _init_l_NativeBranchBackend_run___redArg___closed__8();
lean_mark_persistent(l_NativeBranchBackend_run___redArg___closed__8);
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
