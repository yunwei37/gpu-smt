// Lean compiler output
// Module: REPL.Main
// Imports: public import Init public import REPL.JSON public import REPL.Frontend public import REPL.Util.Path public import REPL.Lean.ContextInfo public import REPL.Lean.Environment public import REPL.Lean.InfoTree public import REPL.Lean.InfoTree.ToJson public import REPL.Snapshots
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
LEAN_EXPORT lean_object* lp_REPL_instToJsonSum__rEPL(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_JsonNumber_fromNat(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___at___00repl_loop_spec__9(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallel___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Json_getObjValAs_x3f___at___00Lean_Server_Test_Runner_Client_instFromJsonHyp_fromJson_spec__4(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_REPL_REPL_sorries___redArg___lam__2(lean_object*);
static lean_object* lp_REPL_REPL_splitArray___redArg___closed__2;
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__9(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_getCommandSnapshot(lean_object*, lean_object*);
lean_object* l_Std_Format_pretty(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_sorries___redArg___closed__0;
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__4;
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_unpickle_unsafe__7(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(lean_object*, lean_object*);
lean_object* l_Lean_Core_instMonadCoreM___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_mk_empty_array_with_capacity(lean_object*);
LEAN_EXPORT lean_object* _lean_main(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_pickleEnvironment_elim(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runBatchVerify___closed__0;
lean_object* l_Lean_Elab_processHeaderCore(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*, lean_object*, uint32_t, lean_object*, uint8_t, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_ppGoals(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallel(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__13;
static lean_object* lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
static lean_object* lp_REPL_instToJsonBatch___closed__0;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4_spec__4(size_t, size_t, lean_object*);
static lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__1;
lean_object* lp_REPL_REPL_CommandSnapshot_pickle(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_splitArray___redArg___closed__0;
lean_object* l_StateT_instMonad___redArg___lam__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tacticsGC___boxed(lean_object*, lean_object*);
lean_object* l_Lean_Json_mkObj(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_pickleEnvironment_elim___redArg(lean_object*, lean_object*);
lean_object* l_Lean_instMonadResolveNameOfMonadLift___redArg(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runBatchVerify___closed__2;
static lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__4;
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__1;
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0(lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__1(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__12;
LEAN_EXPORT lean_object* lp_REPL_REPL_Array_replicate(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__4;
LEAN_EXPORT lean_object* lp_REPL_instToJsonSum__rEPL___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
extern lean_object* l_Lean_instInhabitedFileMap_default;
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleCommandSnapshot___boxed(lean_object*, lean_object*, lean_object*);
uint8_t l_Lean_Exception_isInterrupt(lean_object*);
static lean_object* lp_REPL_REPL_sorries___redArg___lam__16___closed__3;
static lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2;
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__6;
LEAN_EXPORT lean_object* lp_REPL_Input_pickleProofSnapshot_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_parse(lean_object*);
lean_object* l_Lean_instMonadLogOfMonadLift___redArg(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__9;
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg(lean_object*, lean_object*, lean_object*);
lean_object* l_List_mapTR_loop___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_instToJsonBatch;
lean_object* lean_io_as_task(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_printFlush___redArg___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__5;
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___at___00REPL_runCommandAux_spec__1___boxed(lean_object*, lean_object*, lean_object*);
extern lean_object* l_Lean_Core_instMonadResolveNameCoreM;
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_runCommandGCAux_spec__0(lean_object*, lean_object*);
lean_object* lean_array_push(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___at___00repl_loop_spec__10___boxed(lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_Lean_Elab_InfoTree_retainSubstantive(lean_object*);
lean_object* l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__0(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_sorries___redArg___closed__1;
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__3;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___lam__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_REPL_REPL_runCommand___lam__0(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_REPL_Input_batchVerify_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t lean_usize_dec_eq(size_t, size_t);
LEAN_EXPORT lean_object* lp_REPL_REPL_runProofStep___boxed(lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_Lean_Elab_InfoTree_toJson(lean_object*, lean_object*);
lean_object* l_ReaderT_instFunctorOfMonad___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Elab_Command_mkState(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_Array_replicate___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__6(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_String_trim(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__2___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_instFromJsonBatch_fromJson(lean_object*);
lean_object* l_Lean_KVMap_setNat(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___at___00REPL_unpickleCommandSnapshot_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_proofStep_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tacticsGC(lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__4(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_tacticsGC_spec__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_io_getenv(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___at___00REPL_runCommandAux_spec__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l___private_Init_Data_List_Impl_0__List_flatMapTR_go___redArg(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__2;
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleProofSnapshot(lean_object*, lean_object*);
lean_object* lp_REPL_List_toJson___at___00REPL_instToJsonProofStepResponse_toJson_spec__1(lean_object*);
extern lean_object* l_instInhabitedError;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0(lean_object*, lean_object*, size_t, size_t, lean_object*);
lean_object* lean_array_fget_borrowed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__16(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_printFlush___at___00repl_loop_spec__1___boxed(lean_object*, lean_object*);
lean_object* l_ReaderT_instApplicativeOfMonad___redArg___lam__3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_parse___boxed(lean_object*, lean_object*);
lean_object* l_panic___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__12(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__3;
uint8_t l_List_isEmpty___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleEnvironment_elim___redArg(lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_pickle(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__0(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_repl_loop___closed__2;
lean_object* l_Lean_Elab_ContextInfo_ppGoals___boxed(lean_object*, lean_object*, lean_object*);
lean_object* l_List_filterTR_loop___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__0(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_command_elim(lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t lean_string_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_main___boxed(lean_object*, lean_object*);
static lean_object* lp_REPL_repl_loop___closed__0;
LEAN_EXPORT lean_object* lp_REPL_instFromJsonBatch;
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__3;
lean_object* lp_REPL_Lean_Elab_IO_processInput_unsafe__11(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Elab_CommandContextInfo_save___at___00Lean_Widget_goalToInteractive_spec__9___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_string_utf8_byte_size(lean_object*);
static lean_object* lp_REPL_REPL_sorries___redArg___lam__16___closed__1;
lean_object* lp_REPL_REPL_instFromJsonUnpickleEnvironment_fromJson(lean_object*);
lean_object* lp_REPL_REPL_instFromJsonProofStep_fromJson(lean_object*);
lean_object* lean_string_push(lean_object*, uint32_t);
lean_object* l_ReaderT_instMonad___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_processFile___boxed(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Parser_mkInputContext___redArg(lean_object*, lean_object*, uint8_t, lean_object*);
static lean_object* lp_REPL_REPL_tactics___redArg___closed__0;
lean_object* l_Lean_Core_instMonadOptionsCoreM___lam__0___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__2___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_get_stdout();
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleCommandSnapshot(lean_object*, lean_object*);
lean_object* lp_REPL_Lean_Elab_InfoTree_retainOriginal(lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__0;
static lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__5;
lean_object* lp_REPL_REPL_ProofSnapshot_ppGoals___boxed(lean_object*, lean_object*);
lean_object* l_List_foldl___at___00Array_appendList_spec__0___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_splitArray___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_IO_println___at___00repl_loop_spec__0(lean_object*);
lean_object* l_Lean_initSearchPath(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__0;
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__10;
static lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__0;
size_t lean_usize_of_nat(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_main___redArg();
static lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__0;
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAuxTimeout___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_ctorElim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandAux(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4(lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_pickle___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_parse___closed__0;
LEAN_EXPORT lean_object* lp_REPL_List_filterTR_loop___at___00REPL_sorriesGC_spec__3(lean_object*, lean_object*);
lean_object* l_Lean_findSysroot(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_getCommandSnapshot___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch___closed__0;
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runCommand___closed__0;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_sorriesGC_spec__2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_ctorElim(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_Lean_Elab_IO_withTimeout___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_newTraces(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifySequential___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_String_splitOnAux(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__10(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandGCAux_spec__1(size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__3(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_Lean_Elab_InfoTree_sorries(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tactics___at___00REPL_runCommandAux_spec__1_spec__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___lam__0___boxed(lean_object*, lean_object*);
lean_object* l_instMonadEST(lean_object*, lean_object*);
lean_object* lean_nat_div(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__0(lean_object*);
lean_object* l_Array_empty(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_instFromJsonUnpickleProofState_fromJson(lean_object*);
lean_object* lp_REPL_REPL_Message_of(lean_object*);
lean_object* l_Lean_Elab_HeaderSyntax_startPos(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_ppTactic___lam__0___closed__1;
LEAN_EXPORT lean_object* lp_REPL_instToJsonBatch_toJson(lean_object*);
static lean_object* lp_REPL_main___redArg___closed__0;
lean_object* l_List_range(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_getLines___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4_spec__4___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tacticsGC_spec__1___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_processFile(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommand___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tacticsGC_spec__1(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__2(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1;
static lean_object* lp_REPL_repl_loop___closed__6;
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__8(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandGCAux_spec__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__14;
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__5(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_ReaderT_instApplicativeOfMonad___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_instInhabitedOfMonad___redArg(lean_object*, lean_object*);
lean_object* l_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__3(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Elab_CommandContextInfo_save___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(lean_object*);
lean_object* l_List_replicateTR___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_splitArray(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__8;
lean_object* lean_array_to_list(lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_runString(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runBatchVerify(lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_newTraces___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAux(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__13;
lean_object* l_StateT_instMonad___redArg___lam__7(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t l_Option_instDecidableEq___redArg(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_repl___closed__1;
lean_object* lp_REPL_REPL_instToJsonTactic_toJson(lean_object*);
static lean_object* lp_REPL_REPL_runBatchVerify___closed__6;
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__8;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___lam__0(lean_object*, lean_object*);
static lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__1;
LEAN_EXPORT lean_object* lp_REPL_Input_ctorIdx___boxed(lean_object*);
static lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__6;
lean_object* lean_get_stdin();
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifySequential_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__4;
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_runMetaM___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_ppTactic___closed__0;
static lean_object* lp_REPL_REPL_runBatchVerify___closed__5;
static lean_object* lp_REPL_REPL_runBatchVerify___closed__3;
lean_object* lp_REPL_Lean_Elab_InfoTree_tactics(lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_runMetaM___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandAux_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_instFromJsonPickleEnvironment_fromJson(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___at___00repl_loop_spec__9___boxed(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__17;
LEAN_EXPORT lean_object* lp_REPL_instToJsonSum__rEPL___redArg___lam__0(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__7;
lean_object* l_Lean_Name_str___override(lean_object*, lean_object*);
lean_object* l_Lean_Core_instMonadCoreM___lam__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_List_mapM_loop___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
extern lean_object* l_Lean_Core_instMonadLogCoreM;
lean_object* l_StateT_instMonad___redArg___lam__9(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0(lean_object*, uint8_t, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__1(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_ppTactic___closed__4;
static lean_object* lp_REPL_repl_loop___closed__3;
uint8_t l_Lean_Elab_HeaderSyntax_isModule(lean_object*);
lean_object* l_Array_extract___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___lam__0(lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_instFromJsonBatchCommand_fromJson(lean_object*);
lean_object* l_StateT_bind(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_splitArray___redArg___closed__1;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandAux_spec__0(size_t, size_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorriesGC(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_ppTactic___closed__3;
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__2;
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__6;
lean_object* lean_task_get_own(lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__1;
lean_object* l_Lean_KVMap_setBool(lean_object*, lean_object*, uint8_t);
lean_object* l_Lean_Elab_HeaderSyntax_imports(lean_object*, uint8_t);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__5;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11(size_t, size_t, lean_object*);
lean_object* lp_REPL_REPL_Sorry_of(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_create(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_CommandSnapshot_pickle___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__5;
static lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
static lean_object* lp_REPL_REPL_sorries___redArg___lam__16___closed__0;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1(lean_object*, lean_object*, size_t, size_t, lean_object*);
static lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__0;
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifySequential(lean_object*, lean_object*, lean_object*);
lean_object* l_StateRefT_x27_lift___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_IO_println___at___00repl_loop_spec__0___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_repl___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAux___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_tactics___redArg___closed__1;
lean_object* lp_REPL_REPL_ProofSnapshot_newMessages(lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__9;
lean_object* l_Lean_Json_getObjValAs_x3f___at___00Lean_Server_Test_Runner_Client_instFromJsonSubexprInfo_fromJson_spec__1(lean_object*, lean_object*);
lean_object* l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(lean_object*, uint8_t);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__12;
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_IO_FS_readFile(lean_object*);
lean_object* lp_REPL_REPL_Tactic_of(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runBatchVerify___closed__1;
static lean_object* lp_REPL_REPL_sorries___redArg___lam__16___closed__2;
static lean_object* lp_REPL_panic___at___00REPL_sorriesGC_spec__1___closed__0;
LEAN_EXPORT lean_object* lp_REPL_Input_batchVerify_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_instFromJsonPickleProofState_fromJson(lean_object*);
lean_object* lp_REPL_REPL_instFromJsonCommand_fromJson(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_proofStep_elim(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__6;
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleProofSnapshot_elim___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_repl_loop___boxed(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__11;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandAux___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_ProofSnapshot_create___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lean_array_fget(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommand___lam__0___boxed(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_unpickleProofSnapshot___closed__0;
LEAN_EXPORT lean_object* lp_REPL_REPL_runBatchVerify___boxed(lean_object*, lean_object*, lean_object*);
extern lean_object* l_Lean_Meta_instMonadEnvMetaM;
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tactics___at___00REPL_runCommandAux_spec__1_spec__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_printFlush(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAuxTimeout(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___lam__0(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_file_elim___redArg(lean_object*, lean_object*);
lean_object* l_Lean_Meta_instMonadMetaM___lam__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Meta_instMonadMetaM___lam__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleProofSnapshot_elim(lean_object*, lean_object*, lean_object*, lean_object*);
extern lean_object* l_Lean_Core_instMonadNameGeneratorCoreM;
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__7;
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__7(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runProofStep___closed__0;
uint8_t lean_nat_dec_lt(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_main___redArg___boxed(lean_object*);
lean_object* lean_nat_mod(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___redArg(lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_instToJsonError_toJson(lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__11;
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__7;
static lean_object* lp_REPL_REPL_runCommandAux___closed__0;
lean_object* l_instInhabitedEST___redArg___lam__0___boxed(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__16;
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__15;
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___at___00repl_loop_spec__10(lean_object*, lean_object*);
static lean_object* lp_REPL_instToJsonBatch_toJson___closed__0;
static lean_object* lp_REPL_REPL_runBatchVerify___closed__4;
LEAN_EXPORT lean_object* lp_REPL_Input_file_elim(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_repl_loop___closed__5;
LEAN_EXPORT lean_object* lp_REPL_Input_pickleProofSnapshot_elim___redArg(lean_object*, lean_object*);
static lean_object* lp_REPL_repl_loop___closed__1;
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__6(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_ReaderT_instFunctorOfMonad___redArg___lam__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_getCommandSnapshot___closed__0;
lean_object* lean_panic_fn(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_ppTactic___closed__2;
lean_object* l_List_reverse___redArg(lean_object*);
static lean_object* lp_REPL_REPL_getCommandSnapshot___closed__1;
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__10;
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__8(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Array_append___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorriesGC_spec__1(lean_object*);
static lean_object* lp_REPL_REPL_runProofStep___closed__2;
lean_object* l_ReaderT_instApplicativeOfMonad___redArg___lam__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_printFlush___at___00repl_loop_spec__1(lean_object*);
lean_object* lp_REPL_List_mapTR_loop___at___00Lean_Elab_InfoTree_filter_spec__0(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_repl___closed__0;
lean_object* lp_REPL_REPL_ProofSnapshot_newInfoTrees(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__2(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t lean_string_memcmp(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_PersistentHashMap_mkEmptyEntriesArray(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_processFile___closed__0;
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(lean_object*, lean_object*);
lean_object* l_Lean_monadNameGeneratorLift___redArg(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_repl_loop(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runProofStep(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommand(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___closed__0;
lean_object* l_String_intercalate(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__3;
lean_object* lean_array_mk(lean_object*);
lean_object* l_Lean_PrettyPrinter_ppTactic(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallelNaive___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
size_t lean_usize_add(size_t, size_t);
lean_object* l_mkPanicMessageWithDecl(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__3(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_ppTactic___lam__0___closed__0;
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__3(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__15;
static lean_object* lp_REPL_REPL_ppTactic___closed__5;
lean_object* l_Lean_Elab_ContextInfo_ppGoals(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_printFlush___redArg(lean_object*, lean_object*);
lean_object* lean_array_uget(lean_object*, size_t);
size_t lean_array_size(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__5(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_ppTactic___closed__1;
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleEnvironment_elim(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic___lam__0(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___at___00REPL_unpickleCommandSnapshot_spec__0___boxed(lean_object*, lean_object*, lean_object*);
lean_object* lean_io_error_to_string(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__6(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_Lean_Elab_InfoTree_retainTacticInfo(lean_object*);
lean_object* l_Lean_Name_mkStr1(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_runCommandGCAux_spec__0___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_createProofStepReponse___redArg___closed__14;
static lean_object* lp_REPL_repl_loop___closed__4;
LEAN_EXPORT lean_object* lp_REPL_repl();
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifySequential_spec__0(lean_object*, lean_object*, size_t, size_t, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_command_elim___redArg(lean_object*, lean_object*);
lean_object* lean_string_append(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorriesGC_spec__1___boxed(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4(lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_List_toJson___at___00REPL_instToJsonProofStepResponse_toJson_spec__4(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
lean_object* lean_array_get_size(lean_object*);
lean_object* lean_load_dynlib(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__2(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_sorries___redArg___closed__2;
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__7(lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_batchVerifyParrallel___closed__0;
lean_object* l_Lean_Parser_parseHeader(lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__5(lean_object*, lean_object*);
uint8_t lean_usize_dec_lt(size_t, size_t);
static lean_object* lp_REPL_REPL_sorries___redArg___closed__3;
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__4(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_Message_of___boxed(lean_object*, lean_object*);
extern lean_object* l_Lean_Meta_instMonadMCtxMetaM;
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__11(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_sorriesGC___boxed(lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Json_parse(lean_object*);
lean_object* lean_nat_add(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_getLines();
static lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__2;
lean_object* lp_REPL_REPL_instFromJsonFile_fromJson(lean_object*);
static lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
lean_object* l_StateT_map(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
uint8_t l_Lean_Exception_isRuntime(lean_object*);
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__10;
static lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
lean_object* l_IO_print___at___00IO_println___at___00__private_Lean_Shell_0__Lean_ShellOptions_process_spec__3_spec__3(lean_object*);
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__9;
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__8;
lean_object* l_Lean_Json_pretty(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Array_toJson___at___00repl_loop_spec__11(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___lam__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_printFlush___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_Lean_Elab_ContextInfo_runMetaM___redArg(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runProofStep___closed__1;
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallelNaive(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_splitArray___redArg___closed__3;
lean_object* lean_array_uset(lean_object*, size_t, lean_object*);
lean_object* l_ReaderT_instMonadLift___lam__0___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_runCommandGCAux___closed__1;
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__9(lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* lp_REPL_REPL_CommandSnapshot_unpickle_unsafe__8(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleProofSnapshot___boxed(lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_main___redArg___closed__1;
static lean_object* lp_REPL_instFromJsonBatch_fromJson___closed__2;
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__13(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_REPL_Input_ctorIdx(lean_object*);
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot(lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_StateT_instMonad___redArg___lam__1(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
lean_object* l_StateT_pure(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
static lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0;
static lean_object* lp_REPL_parse___closed__1;
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_3);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; 
x_5 = lean_ctor_get(x_3, 0);
lean_dec(x_5);
lean_ctor_set(x_3, 0, x_1);
x_6 = lean_apply_2(x_2, lean_box(0), x_3);
return x_6;
}
else
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_7 = lean_ctor_get(x_3, 1);
lean_inc(x_7);
lean_dec(x_3);
x_8 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_8, 0, x_1);
lean_ctor_set(x_8, 1, x_7);
x_9 = lean_apply_2(x_2, lean_box(0), x_8);
return x_9;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___redArg___lam__1(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
uint8_t x_5; 
x_5 = !lean_is_exclusive(x_4);
if (x_5 == 0)
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; uint8_t x_9; 
x_6 = lean_ctor_get(x_4, 0);
x_7 = lean_ctor_get(x_4, 1);
x_8 = lean_ctor_get(x_6, 0);
lean_inc_ref(x_8);
lean_dec(x_6);
x_9 = !lean_is_exclusive(x_7);
if (x_9 == 0)
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_10 = lean_ctor_get(x_7, 0);
x_11 = lean_array_get_size(x_8);
lean_dec_ref(x_8);
lean_inc(x_1);
x_12 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0), 3, 2);
lean_closure_set(x_12, 0, x_11);
lean_closure_set(x_12, 1, x_1);
x_13 = lean_box(0);
x_14 = lean_array_push(x_10, x_2);
lean_ctor_set(x_7, 0, x_14);
lean_ctor_set(x_4, 0, x_13);
x_15 = lean_apply_2(x_1, lean_box(0), x_4);
x_16 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_15, x_12);
return x_16;
}
else
{
lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; 
x_17 = lean_ctor_get(x_7, 0);
x_18 = lean_ctor_get(x_7, 1);
lean_inc(x_18);
lean_inc(x_17);
lean_dec(x_7);
x_19 = lean_array_get_size(x_8);
lean_dec_ref(x_8);
lean_inc(x_1);
x_20 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0), 3, 2);
lean_closure_set(x_20, 0, x_19);
lean_closure_set(x_20, 1, x_1);
x_21 = lean_box(0);
x_22 = lean_array_push(x_17, x_2);
x_23 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_23, 0, x_22);
lean_ctor_set(x_23, 1, x_18);
lean_ctor_set(x_4, 1, x_23);
lean_ctor_set(x_4, 0, x_21);
x_24 = lean_apply_2(x_1, lean_box(0), x_4);
x_25 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_24, x_20);
return x_25;
}
}
else
{
lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; 
x_26 = lean_ctor_get(x_4, 0);
x_27 = lean_ctor_get(x_4, 1);
lean_inc(x_27);
lean_inc(x_26);
lean_dec(x_4);
x_28 = lean_ctor_get(x_26, 0);
lean_inc_ref(x_28);
lean_dec(x_26);
x_29 = lean_ctor_get(x_27, 0);
lean_inc_ref(x_29);
x_30 = lean_ctor_get(x_27, 1);
lean_inc_ref(x_30);
if (lean_is_exclusive(x_27)) {
 lean_ctor_release(x_27, 0);
 lean_ctor_release(x_27, 1);
 x_31 = x_27;
} else {
 lean_dec_ref(x_27);
 x_31 = lean_box(0);
}
x_32 = lean_array_get_size(x_28);
lean_dec_ref(x_28);
lean_inc(x_1);
x_33 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0), 3, 2);
lean_closure_set(x_33, 0, x_32);
lean_closure_set(x_33, 1, x_1);
x_34 = lean_box(0);
x_35 = lean_array_push(x_29, x_2);
if (lean_is_scalar(x_31)) {
 x_36 = lean_alloc_ctor(0, 2, 0);
} else {
 x_36 = x_31;
}
lean_ctor_set(x_36, 0, x_35);
lean_ctor_set(x_36, 1, x_30);
x_37 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_37, 0, x_34);
lean_ctor_set(x_37, 1, x_36);
x_38 = lean_apply_2(x_1, lean_box(0), x_37);
x_39 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_38, x_33);
return x_39;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_1);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_5 = lean_ctor_get(x_1, 0);
x_6 = lean_ctor_get(x_1, 1);
x_7 = lean_ctor_get(x_5, 1);
lean_inc(x_7);
lean_dec_ref(x_5);
lean_inc(x_6);
lean_inc(x_7);
x_8 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__1), 4, 3);
lean_closure_set(x_8, 0, x_7);
lean_closure_set(x_8, 1, x_2);
lean_closure_set(x_8, 2, x_6);
lean_inc_ref(x_3);
lean_ctor_set(x_1, 1, x_3);
lean_ctor_set(x_1, 0, x_3);
x_9 = lean_apply_2(x_7, lean_box(0), x_1);
x_10 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_9, x_8);
return x_10;
}
else
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_11 = lean_ctor_get(x_1, 0);
x_12 = lean_ctor_get(x_1, 1);
lean_inc(x_12);
lean_inc(x_11);
lean_dec(x_1);
x_13 = lean_ctor_get(x_11, 1);
lean_inc(x_13);
lean_dec_ref(x_11);
lean_inc(x_12);
lean_inc(x_13);
x_14 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__1), 4, 3);
lean_closure_set(x_14, 0, x_13);
lean_closure_set(x_14, 1, x_2);
lean_closure_set(x_14, 2, x_12);
lean_inc_ref(x_3);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_3);
lean_ctor_set(x_15, 1, x_3);
x_16 = lean_apply_2(x_13, lean_box(0), x_15);
x_17 = lean_apply_4(x_12, lean_box(0), lean_box(0), x_16, x_14);
return x_17;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_recordCommandSnapshot___redArg(x_2, x_3, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___redArg___lam__1(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
uint8_t x_5; 
x_5 = !lean_is_exclusive(x_4);
if (x_5 == 0)
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; uint8_t x_9; 
x_6 = lean_ctor_get(x_4, 0);
x_7 = lean_ctor_get(x_4, 1);
x_8 = lean_ctor_get(x_6, 1);
lean_inc_ref(x_8);
lean_dec(x_6);
x_9 = !lean_is_exclusive(x_7);
if (x_9 == 0)
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_10 = lean_ctor_get(x_7, 1);
x_11 = lean_array_get_size(x_8);
lean_dec_ref(x_8);
lean_inc(x_1);
x_12 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0), 3, 2);
lean_closure_set(x_12, 0, x_11);
lean_closure_set(x_12, 1, x_1);
x_13 = lean_box(0);
x_14 = lean_array_push(x_10, x_2);
lean_ctor_set(x_7, 1, x_14);
lean_ctor_set(x_4, 0, x_13);
x_15 = lean_apply_2(x_1, lean_box(0), x_4);
x_16 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_15, x_12);
return x_16;
}
else
{
lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; 
x_17 = lean_ctor_get(x_7, 0);
x_18 = lean_ctor_get(x_7, 1);
lean_inc(x_18);
lean_inc(x_17);
lean_dec(x_7);
x_19 = lean_array_get_size(x_8);
lean_dec_ref(x_8);
lean_inc(x_1);
x_20 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0), 3, 2);
lean_closure_set(x_20, 0, x_19);
lean_closure_set(x_20, 1, x_1);
x_21 = lean_box(0);
x_22 = lean_array_push(x_18, x_2);
x_23 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_23, 0, x_17);
lean_ctor_set(x_23, 1, x_22);
lean_ctor_set(x_4, 1, x_23);
lean_ctor_set(x_4, 0, x_21);
x_24 = lean_apply_2(x_1, lean_box(0), x_4);
x_25 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_24, x_20);
return x_25;
}
}
else
{
lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; 
x_26 = lean_ctor_get(x_4, 0);
x_27 = lean_ctor_get(x_4, 1);
lean_inc(x_27);
lean_inc(x_26);
lean_dec(x_4);
x_28 = lean_ctor_get(x_26, 1);
lean_inc_ref(x_28);
lean_dec(x_26);
x_29 = lean_ctor_get(x_27, 0);
lean_inc_ref(x_29);
x_30 = lean_ctor_get(x_27, 1);
lean_inc_ref(x_30);
if (lean_is_exclusive(x_27)) {
 lean_ctor_release(x_27, 0);
 lean_ctor_release(x_27, 1);
 x_31 = x_27;
} else {
 lean_dec_ref(x_27);
 x_31 = lean_box(0);
}
x_32 = lean_array_get_size(x_28);
lean_dec_ref(x_28);
lean_inc(x_1);
x_33 = lean_alloc_closure((void*)(lp_REPL_REPL_recordCommandSnapshot___redArg___lam__0), 3, 2);
lean_closure_set(x_33, 0, x_32);
lean_closure_set(x_33, 1, x_1);
x_34 = lean_box(0);
x_35 = lean_array_push(x_30, x_2);
if (lean_is_scalar(x_31)) {
 x_36 = lean_alloc_ctor(0, 2, 0);
} else {
 x_36 = x_31;
}
lean_ctor_set(x_36, 0, x_29);
lean_ctor_set(x_36, 1, x_35);
x_37 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_37, 0, x_34);
lean_ctor_set(x_37, 1, x_36);
x_38 = lean_apply_2(x_1, lean_box(0), x_37);
x_39 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_38, x_33);
return x_39;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_1);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_5 = lean_ctor_get(x_1, 0);
x_6 = lean_ctor_get(x_1, 1);
x_7 = lean_ctor_get(x_5, 1);
lean_inc(x_7);
lean_dec_ref(x_5);
lean_inc(x_6);
lean_inc(x_7);
x_8 = lean_alloc_closure((void*)(lp_REPL_REPL_recordProofSnapshot___redArg___lam__1), 4, 3);
lean_closure_set(x_8, 0, x_7);
lean_closure_set(x_8, 1, x_2);
lean_closure_set(x_8, 2, x_6);
lean_inc_ref(x_3);
lean_ctor_set(x_1, 1, x_3);
lean_ctor_set(x_1, 0, x_3);
x_9 = lean_apply_2(x_7, lean_box(0), x_1);
x_10 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_9, x_8);
return x_10;
}
else
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_11 = lean_ctor_get(x_1, 0);
x_12 = lean_ctor_get(x_1, 1);
lean_inc(x_12);
lean_inc(x_11);
lean_dec(x_1);
x_13 = lean_ctor_get(x_11, 1);
lean_inc(x_13);
lean_dec_ref(x_11);
lean_inc(x_12);
lean_inc(x_13);
x_14 = lean_alloc_closure((void*)(lp_REPL_REPL_recordProofSnapshot___redArg___lam__1), 4, 3);
lean_closure_set(x_14, 0, x_13);
lean_closure_set(x_14, 1, x_2);
lean_closure_set(x_14, 2, x_12);
lean_inc_ref(x_3);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_3);
lean_ctor_set(x_15, 1, x_3);
x_16 = lean_apply_2(x_13, lean_box(0), x_15);
x_17 = lean_apply_4(x_12, lean_box(0), lean_box(0), x_16, x_14);
return x_17;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_recordProofSnapshot___redArg(x_2, x_3, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__0(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_2 = lean_unsigned_to_nat(120u);
x_3 = lean_unsigned_to_nat(0u);
x_4 = l_Std_Format_pretty(x_1, x_2, x_3, x_3);
return x_4;
}
}
LEAN_EXPORT uint8_t lp_REPL_REPL_sorries___redArg___lam__2(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lean_ctor_get(x_1, 1);
x_3 = lean_ctor_get(x_2, 0);
if (lean_obj_tag(x_3) == 1)
{
lean_object* x_4; 
x_4 = lean_ctor_get(x_3, 1);
if (lean_obj_tag(x_4) == 0)
{
uint8_t x_5; 
x_5 = 0;
return x_5;
}
else
{
uint8_t x_6; 
x_6 = 1;
return x_6;
}
}
else
{
uint8_t x_7; 
x_7 = 1;
return x_7;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__2___boxed(lean_object* x_1) {
_start:
{
uint8_t x_2; lean_object* x_3; 
x_2 = lp_REPL_REPL_sorries___redArg___lam__2(x_1);
lean_dec_ref(x_1);
x_3 = lean_box(x_2);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("", 0, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_box(0);
x_2 = lp_REPL_REPL_sorries___redArg___closed__0;
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__1(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; 
x_6 = !lean_is_exclusive(x_5);
if (x_6 == 0)
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_7 = lean_ctor_get(x_5, 0);
x_8 = lean_ctor_get(x_1, 1);
lean_inc(x_8);
lean_dec_ref(x_1);
x_9 = lp_REPL_REPL_Sorry_of(x_2, x_3, x_4, x_7);
lean_ctor_set(x_5, 0, x_9);
x_10 = lean_apply_2(x_8, lean_box(0), x_5);
return x_10;
}
else
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_11 = lean_ctor_get(x_5, 0);
x_12 = lean_ctor_get(x_5, 1);
lean_inc(x_12);
lean_inc(x_11);
lean_dec(x_5);
x_13 = lean_ctor_get(x_1, 1);
lean_inc(x_13);
lean_dec_ref(x_1);
x_14 = lp_REPL_REPL_Sorry_of(x_2, x_3, x_4, x_11);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_14);
lean_ctor_set(x_15, 1, x_12);
x_16 = lean_apply_2(x_13, lean_box(0), x_15);
return x_16;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__3(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_3; 
x_3 = !lean_is_exclusive(x_2);
if (x_3 == 0)
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_4 = lean_ctor_get(x_2, 0);
x_5 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_5, 0, x_4);
lean_ctor_set(x_2, 0, x_5);
x_6 = lean_apply_2(x_1, lean_box(0), x_2);
return x_6;
}
else
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_7 = lean_ctor_get(x_2, 0);
x_8 = lean_ctor_get(x_2, 1);
lean_inc(x_8);
lean_inc(x_7);
lean_dec(x_2);
x_9 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_9, 0, x_7);
x_10 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_10, 0, x_9);
lean_ctor_set(x_10, 1, x_8);
x_11 = lean_apply_2(x_1, lean_box(0), x_10);
return x_11;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__4(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; 
x_6 = !lean_is_exclusive(x_4);
if (x_6 == 0)
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_7 = lean_ctor_get(x_4, 0);
x_8 = lean_ctor_get(x_4, 1);
x_9 = lean_ctor_get(x_1, 0);
x_10 = lean_ctor_get(x_1, 1);
lean_inc(x_10);
lean_inc_ref(x_9);
x_11 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__1), 5, 4);
lean_closure_set(x_11, 0, x_9);
lean_closure_set(x_11, 1, x_7);
lean_closure_set(x_11, 2, x_2);
lean_closure_set(x_11, 3, x_3);
if (lean_obj_tag(x_8) == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; 
lean_inc_ref(x_9);
lean_dec_ref(x_1);
x_12 = lean_ctor_get(x_9, 1);
lean_inc(x_12);
lean_dec_ref(x_9);
x_13 = lean_box(0);
lean_ctor_set(x_4, 1, x_5);
lean_ctor_set(x_4, 0, x_13);
x_14 = lean_apply_2(x_12, lean_box(0), x_4);
x_15 = lean_apply_4(x_10, lean_box(0), lean_box(0), x_14, x_11);
return x_15;
}
else
{
lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; 
lean_free_object(x_4);
x_16 = lean_ctor_get(x_8, 0);
lean_inc(x_16);
lean_dec_ref(x_8);
x_17 = lean_ctor_get(x_9, 1);
lean_inc(x_17);
x_18 = lp_REPL_REPL_recordProofSnapshot___redArg(x_1, x_16, x_5);
x_19 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__3), 2, 1);
lean_closure_set(x_19, 0, x_17);
lean_inc(x_10);
x_20 = lean_apply_4(x_10, lean_box(0), lean_box(0), x_18, x_19);
x_21 = lean_apply_4(x_10, lean_box(0), lean_box(0), x_20, x_11);
return x_21;
}
}
else
{
lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; 
x_22 = lean_ctor_get(x_4, 0);
x_23 = lean_ctor_get(x_4, 1);
lean_inc(x_23);
lean_inc(x_22);
lean_dec(x_4);
x_24 = lean_ctor_get(x_1, 0);
x_25 = lean_ctor_get(x_1, 1);
lean_inc(x_25);
lean_inc_ref(x_24);
x_26 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__1), 5, 4);
lean_closure_set(x_26, 0, x_24);
lean_closure_set(x_26, 1, x_22);
lean_closure_set(x_26, 2, x_2);
lean_closure_set(x_26, 3, x_3);
if (lean_obj_tag(x_23) == 0)
{
lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; 
lean_inc_ref(x_24);
lean_dec_ref(x_1);
x_27 = lean_ctor_get(x_24, 1);
lean_inc(x_27);
lean_dec_ref(x_24);
x_28 = lean_box(0);
x_29 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_29, 0, x_28);
lean_ctor_set(x_29, 1, x_5);
x_30 = lean_apply_2(x_27, lean_box(0), x_29);
x_31 = lean_apply_4(x_25, lean_box(0), lean_box(0), x_30, x_26);
return x_31;
}
else
{
lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; 
x_32 = lean_ctor_get(x_23, 0);
lean_inc(x_32);
lean_dec_ref(x_23);
x_33 = lean_ctor_get(x_24, 1);
lean_inc(x_33);
x_34 = lp_REPL_REPL_recordProofSnapshot___redArg(x_1, x_32, x_5);
x_35 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__3), 2, 1);
lean_closure_set(x_35, 0, x_33);
lean_inc(x_25);
x_36 = lean_apply_4(x_25, lean_box(0), lean_box(0), x_34, x_35);
x_37 = lean_apply_4(x_25, lean_box(0), lean_box(0), x_36, x_26);
return x_37;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__5(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; 
x_3 = lean_ctor_get(x_2, 0);
lean_inc(x_3);
x_4 = lean_ctor_get(x_2, 1);
lean_inc(x_4);
lean_dec_ref(x_2);
x_5 = lean_apply_2(x_1, x_3, x_4);
return x_5;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___lam__6___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("\n", 1, 1);
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__6(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
uint8_t x_7; 
x_7 = !lean_is_exclusive(x_6);
if (x_7 == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_8 = lean_ctor_get(x_6, 0);
x_9 = lean_ctor_get(x_6, 1);
x_10 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_11 = lean_box(0);
x_12 = l_List_mapTR_loop___redArg(x_1, x_8, x_11);
x_13 = l_String_intercalate(x_10, x_12);
x_14 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_14, 0, x_2);
lean_ctor_set(x_6, 1, x_14);
lean_ctor_set(x_6, 0, x_13);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_6);
lean_ctor_set(x_15, 1, x_9);
x_16 = lean_apply_2(x_3, lean_box(0), x_15);
x_17 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_16, x_5);
return x_17;
}
else
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; 
x_18 = lean_ctor_get(x_6, 0);
x_19 = lean_ctor_get(x_6, 1);
lean_inc(x_19);
lean_inc(x_18);
lean_dec(x_6);
x_20 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_21 = lean_box(0);
x_22 = l_List_mapTR_loop___redArg(x_1, x_18, x_21);
x_23 = l_String_intercalate(x_20, x_22);
x_24 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_24, 0, x_2);
x_25 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_25, 0, x_23);
lean_ctor_set(x_25, 1, x_24);
x_26 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_26, 0, x_25);
lean_ctor_set(x_26, 1, x_19);
x_27 = lean_apply_2(x_3, lean_box(0), x_26);
x_28 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_27, x_5);
return x_28;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__7(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; 
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_1);
x_5 = lean_apply_2(x_2, lean_box(0), x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__8(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; 
x_7 = lean_ctor_get(x_6, 0);
lean_inc(x_7);
x_8 = lean_ctor_get(x_6, 1);
lean_inc(x_8);
lean_dec_ref(x_6);
lean_inc(x_3);
lean_inc(x_2);
lean_inc(x_7);
x_9 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__6), 6, 5);
lean_closure_set(x_9, 0, x_1);
lean_closure_set(x_9, 1, x_7);
lean_closure_set(x_9, 2, x_2);
lean_closure_set(x_9, 3, x_3);
lean_closure_set(x_9, 4, x_4);
x_10 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_ppGoals___boxed), 2, 1);
lean_closure_set(x_10, 0, x_7);
x_11 = lean_apply_2(x_5, lean_box(0), x_10);
x_12 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__7), 3, 2);
lean_closure_set(x_12, 0, x_8);
lean_closure_set(x_12, 1, x_2);
lean_inc(x_3);
x_13 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_11, x_12);
x_14 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_13, x_9);
return x_14;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__9(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; 
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_1);
x_5 = lean_apply_2(x_2, lean_box(0), x_4);
return x_5;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("unreachable code has been reached", 33, 33);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("REPL.sorries", 12, 12);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("REPL.Main", 9, 9);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_1 = lp_REPL_REPL_sorries___redArg___lam__16___closed__2;
x_2 = lean_unsigned_to_nat(26u);
x_3 = lean_unsigned_to_nat(109u);
x_4 = lp_REPL_REPL_sorries___redArg___lam__16___closed__1;
x_5 = lp_REPL_REPL_sorries___redArg___lam__16___closed__0;
x_6 = l_mkPanicMessageWithDecl(x_5, x_4, x_3, x_2, x_1);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg___lam__16(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8) {
_start:
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; 
x_9 = lean_ctor_get(x_7, 1);
lean_inc(x_9);
x_10 = lean_ctor_get(x_9, 1);
lean_inc(x_10);
x_11 = lean_ctor_get(x_7, 0);
lean_inc(x_11);
lean_dec_ref(x_7);
x_12 = lean_ctor_get(x_9, 0);
lean_inc(x_12);
lean_dec(x_9);
x_13 = lean_ctor_get(x_10, 0);
lean_inc(x_13);
x_14 = lean_ctor_get(x_10, 1);
lean_inc(x_14);
lean_dec(x_10);
lean_inc_ref(x_1);
x_15 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__4), 5, 3);
lean_closure_set(x_15, 0, x_1);
lean_closure_set(x_15, 1, x_13);
lean_closure_set(x_15, 2, x_14);
if (lean_obj_tag(x_12) == 0)
{
lean_object* x_16; lean_object* x_17; uint8_t x_18; 
lean_dec_ref(x_6);
lean_dec(x_5);
x_16 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_16);
x_17 = lean_ctor_get(x_12, 0);
lean_inc(x_17);
lean_dec_ref(x_12);
x_18 = !lean_is_exclusive(x_1);
if (x_18 == 0)
{
lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; 
x_19 = lean_ctor_get(x_1, 1);
x_20 = lean_ctor_get(x_1, 0);
lean_dec(x_20);
x_21 = lean_ctor_get(x_16, 1);
lean_inc(x_21);
lean_dec_ref(x_16);
x_22 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__5), 2, 1);
lean_closure_set(x_22, 0, x_15);
lean_inc(x_3);
lean_inc(x_19);
lean_inc(x_21);
x_23 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__8), 6, 5);
lean_closure_set(x_23, 0, x_2);
lean_closure_set(x_23, 1, x_21);
lean_closure_set(x_23, 2, x_19);
lean_closure_set(x_23, 3, x_22);
lean_closure_set(x_23, 4, x_3);
x_24 = lean_box(0);
x_25 = lean_box(0);
lean_ctor_set_tag(x_1, 1);
lean_ctor_set(x_1, 1, x_25);
lean_ctor_set(x_1, 0, x_17);
x_26 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_create___boxed), 6, 5);
lean_closure_set(x_26, 0, x_11);
lean_closure_set(x_26, 1, x_24);
lean_closure_set(x_26, 2, x_4);
lean_closure_set(x_26, 3, x_1);
lean_closure_set(x_26, 4, x_25);
x_27 = lean_apply_2(x_3, lean_box(0), x_26);
x_28 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__9), 3, 2);
lean_closure_set(x_28, 0, x_8);
lean_closure_set(x_28, 1, x_21);
lean_inc(x_19);
x_29 = lean_apply_4(x_19, lean_box(0), lean_box(0), x_27, x_28);
x_30 = lean_apply_4(x_19, lean_box(0), lean_box(0), x_29, x_23);
return x_30;
}
else
{
lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; 
x_31 = lean_ctor_get(x_1, 1);
lean_inc(x_31);
lean_dec(x_1);
x_32 = lean_ctor_get(x_16, 1);
lean_inc(x_32);
lean_dec_ref(x_16);
x_33 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__5), 2, 1);
lean_closure_set(x_33, 0, x_15);
lean_inc(x_3);
lean_inc(x_31);
lean_inc(x_32);
x_34 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__8), 6, 5);
lean_closure_set(x_34, 0, x_2);
lean_closure_set(x_34, 1, x_32);
lean_closure_set(x_34, 2, x_31);
lean_closure_set(x_34, 3, x_33);
lean_closure_set(x_34, 4, x_3);
x_35 = lean_box(0);
x_36 = lean_box(0);
x_37 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_37, 0, x_17);
lean_ctor_set(x_37, 1, x_36);
x_38 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_create___boxed), 6, 5);
lean_closure_set(x_38, 0, x_11);
lean_closure_set(x_38, 1, x_35);
lean_closure_set(x_38, 2, x_4);
lean_closure_set(x_38, 3, x_37);
lean_closure_set(x_38, 4, x_36);
x_39 = lean_apply_2(x_3, lean_box(0), x_38);
x_40 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__9), 3, 2);
lean_closure_set(x_40, 0, x_8);
lean_closure_set(x_40, 1, x_32);
lean_inc(x_31);
x_41 = lean_apply_4(x_31, lean_box(0), lean_box(0), x_39, x_40);
x_42 = lean_apply_4(x_31, lean_box(0), lean_box(0), x_41, x_34);
return x_42;
}
}
else
{
lean_object* x_43; 
lean_dec_ref(x_2);
x_43 = lean_ctor_get(x_12, 1);
lean_inc(x_43);
if (lean_obj_tag(x_43) == 0)
{
lean_object* x_44; lean_object* x_45; lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; 
lean_dec_ref(x_12);
lean_dec(x_11);
lean_dec_ref(x_6);
lean_dec(x_4);
lean_dec(x_3);
x_44 = lean_ctor_get(x_1, 1);
lean_inc(x_44);
lean_dec_ref(x_1);
x_45 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__5), 2, 1);
lean_closure_set(x_45, 0, x_15);
x_46 = lp_REPL_REPL_sorries___redArg___lam__16___closed__3;
x_47 = l_panic___redArg(x_5, x_46);
x_48 = lean_apply_1(x_47, x_8);
x_49 = lean_apply_4(x_44, lean_box(0), lean_box(0), x_48, x_45);
return x_49;
}
else
{
lean_object* x_50; lean_object* x_51; uint8_t x_52; 
lean_dec(x_5);
x_50 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_50);
x_51 = lean_ctor_get(x_12, 0);
lean_inc_ref(x_51);
lean_dec_ref(x_12);
x_52 = !lean_is_exclusive(x_43);
if (x_52 == 0)
{
uint8_t x_53; 
x_53 = !lean_is_exclusive(x_1);
if (x_53 == 0)
{
lean_object* x_54; lean_object* x_55; lean_object* x_56; lean_object* x_57; lean_object* x_58; lean_object* x_59; lean_object* x_60; lean_object* x_61; lean_object* x_62; lean_object* x_63; lean_object* x_64; lean_object* x_65; 
x_54 = lean_ctor_get(x_43, 0);
x_55 = lean_ctor_get(x_1, 1);
x_56 = lean_ctor_get(x_1, 0);
lean_dec(x_56);
x_57 = lean_ctor_get(x_50, 1);
lean_inc(x_57);
lean_dec_ref(x_50);
x_58 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__5), 2, 1);
lean_closure_set(x_58, 0, x_15);
lean_inc(x_3);
lean_inc(x_55);
lean_inc(x_57);
x_59 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__8), 6, 5);
lean_closure_set(x_59, 0, x_6);
lean_closure_set(x_59, 1, x_57);
lean_closure_set(x_59, 2, x_55);
lean_closure_set(x_59, 3, x_58);
lean_closure_set(x_59, 4, x_3);
lean_ctor_set(x_43, 0, x_51);
x_60 = lean_box(0);
lean_ctor_set_tag(x_1, 1);
lean_ctor_set(x_1, 1, x_60);
lean_ctor_set(x_1, 0, x_54);
x_61 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_create___boxed), 6, 5);
lean_closure_set(x_61, 0, x_11);
lean_closure_set(x_61, 1, x_43);
lean_closure_set(x_61, 2, x_4);
lean_closure_set(x_61, 3, x_60);
lean_closure_set(x_61, 4, x_1);
x_62 = lean_apply_2(x_3, lean_box(0), x_61);
x_63 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__9), 3, 2);
lean_closure_set(x_63, 0, x_8);
lean_closure_set(x_63, 1, x_57);
lean_inc(x_55);
x_64 = lean_apply_4(x_55, lean_box(0), lean_box(0), x_62, x_63);
x_65 = lean_apply_4(x_55, lean_box(0), lean_box(0), x_64, x_59);
return x_65;
}
else
{
lean_object* x_66; lean_object* x_67; lean_object* x_68; lean_object* x_69; lean_object* x_70; lean_object* x_71; lean_object* x_72; lean_object* x_73; lean_object* x_74; lean_object* x_75; lean_object* x_76; lean_object* x_77; 
x_66 = lean_ctor_get(x_43, 0);
x_67 = lean_ctor_get(x_1, 1);
lean_inc(x_67);
lean_dec(x_1);
x_68 = lean_ctor_get(x_50, 1);
lean_inc(x_68);
lean_dec_ref(x_50);
x_69 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__5), 2, 1);
lean_closure_set(x_69, 0, x_15);
lean_inc(x_3);
lean_inc(x_67);
lean_inc(x_68);
x_70 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__8), 6, 5);
lean_closure_set(x_70, 0, x_6);
lean_closure_set(x_70, 1, x_68);
lean_closure_set(x_70, 2, x_67);
lean_closure_set(x_70, 3, x_69);
lean_closure_set(x_70, 4, x_3);
lean_ctor_set(x_43, 0, x_51);
x_71 = lean_box(0);
x_72 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_72, 0, x_66);
lean_ctor_set(x_72, 1, x_71);
x_73 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_create___boxed), 6, 5);
lean_closure_set(x_73, 0, x_11);
lean_closure_set(x_73, 1, x_43);
lean_closure_set(x_73, 2, x_4);
lean_closure_set(x_73, 3, x_71);
lean_closure_set(x_73, 4, x_72);
x_74 = lean_apply_2(x_3, lean_box(0), x_73);
x_75 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__9), 3, 2);
lean_closure_set(x_75, 0, x_8);
lean_closure_set(x_75, 1, x_68);
lean_inc(x_67);
x_76 = lean_apply_4(x_67, lean_box(0), lean_box(0), x_74, x_75);
x_77 = lean_apply_4(x_67, lean_box(0), lean_box(0), x_76, x_70);
return x_77;
}
}
else
{
lean_object* x_78; lean_object* x_79; lean_object* x_80; lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; lean_object* x_85; lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; lean_object* x_90; lean_object* x_91; 
x_78 = lean_ctor_get(x_43, 0);
lean_inc(x_78);
lean_dec(x_43);
x_79 = lean_ctor_get(x_1, 1);
lean_inc(x_79);
if (lean_is_exclusive(x_1)) {
 lean_ctor_release(x_1, 0);
 lean_ctor_release(x_1, 1);
 x_80 = x_1;
} else {
 lean_dec_ref(x_1);
 x_80 = lean_box(0);
}
x_81 = lean_ctor_get(x_50, 1);
lean_inc(x_81);
lean_dec_ref(x_50);
x_82 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__5), 2, 1);
lean_closure_set(x_82, 0, x_15);
lean_inc(x_3);
lean_inc(x_79);
lean_inc(x_81);
x_83 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__8), 6, 5);
lean_closure_set(x_83, 0, x_6);
lean_closure_set(x_83, 1, x_81);
lean_closure_set(x_83, 2, x_79);
lean_closure_set(x_83, 3, x_82);
lean_closure_set(x_83, 4, x_3);
x_84 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_84, 0, x_51);
x_85 = lean_box(0);
if (lean_is_scalar(x_80)) {
 x_86 = lean_alloc_ctor(1, 2, 0);
} else {
 x_86 = x_80;
 lean_ctor_set_tag(x_86, 1);
}
lean_ctor_set(x_86, 0, x_78);
lean_ctor_set(x_86, 1, x_85);
x_87 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_create___boxed), 6, 5);
lean_closure_set(x_87, 0, x_11);
lean_closure_set(x_87, 1, x_84);
lean_closure_set(x_87, 2, x_4);
lean_closure_set(x_87, 3, x_85);
lean_closure_set(x_87, 4, x_86);
x_88 = lean_apply_2(x_3, lean_box(0), x_87);
x_89 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__9), 3, 2);
lean_closure_set(x_89, 0, x_8);
lean_closure_set(x_89, 1, x_81);
lean_inc(x_79);
x_90 = lean_apply_4(x_79, lean_box(0), lean_box(0), x_88, x_89);
x_91 = lean_apply_4(x_79, lean_box(0), lean_box(0), x_90, x_83);
return x_91;
}
}
}
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(lp_REPL_Lean_Elab_InfoTree_sorries), 1, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_sorries___redArg___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; 
x_6 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__0), 1, 0);
x_7 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__2___boxed), 1, 0);
x_8 = lp_REPL_REPL_sorries___redArg___closed__1;
lean_inc_ref(x_1);
x_9 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_9, 0, x_1);
lean_inc_ref(x_1);
x_10 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_10, 0, x_1);
lean_inc_ref(x_1);
x_11 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_11, 0, x_1);
lean_inc_ref(x_1);
x_12 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_12, 0, x_1);
lean_inc_ref(x_1);
x_13 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_13, 0, lean_box(0));
lean_closure_set(x_13, 1, lean_box(0));
lean_closure_set(x_13, 2, x_1);
x_14 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_14, 0, x_13);
lean_ctor_set(x_14, 1, x_9);
lean_inc_ref(x_1);
x_15 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_15, 0, lean_box(0));
lean_closure_set(x_15, 1, lean_box(0));
lean_closure_set(x_15, 2, x_1);
x_16 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_16, 0, x_14);
lean_ctor_set(x_16, 1, x_15);
lean_ctor_set(x_16, 2, x_10);
lean_ctor_set(x_16, 3, x_11);
lean_ctor_set(x_16, 4, x_12);
lean_inc_ref(x_1);
x_17 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_17, 0, lean_box(0));
lean_closure_set(x_17, 1, lean_box(0));
lean_closure_set(x_17, 2, x_1);
x_18 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_18, 0, x_16);
lean_ctor_set(x_18, 1, x_17);
lean_inc_ref(x_18);
x_19 = l_instInhabitedOfMonad___redArg(x_18, x_8);
lean_inc_ref(x_6);
x_20 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__16), 8, 6);
lean_closure_set(x_20, 0, x_1);
lean_closure_set(x_20, 1, x_6);
lean_closure_set(x_20, 2, x_2);
lean_closure_set(x_20, 3, x_4);
lean_closure_set(x_20, 4, x_19);
lean_closure_set(x_20, 5, x_6);
x_21 = lp_REPL_REPL_sorries___redArg___closed__2;
x_22 = lp_REPL_REPL_sorries___redArg___closed__3;
x_23 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___redArg(x_21, x_3, x_22);
x_24 = lean_box(0);
x_25 = l_List_filterTR_loop___redArg(x_7, x_23, x_24);
x_26 = l_List_mapM_loop___redArg(x_18, x_20, x_25, x_24);
x_27 = lean_apply_1(x_26, x_5);
return x_27;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
lean_object* x_7; 
x_7 = lp_REPL_REPL_sorries___redArg(x_2, x_3, x_4, x_5, x_6);
return x_7;
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorriesGC_spec__1___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = l_instInhabitedError;
x_2 = lean_alloc_closure((void*)(l_instInhabitedEST___redArg___lam__0___boxed), 2, 1);
lean_closure_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorriesGC_spec__1(lean_object* x_1) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; 
x_3 = lp_REPL_panic___at___00REPL_sorriesGC_spec__1___closed__0;
x_4 = lean_panic_fn(x_3, x_1);
x_5 = lean_apply_1(x_4, lean_box(0));
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_sorriesGC_spec__2(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = lean_array_to_list(x_2);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lean_ctor_get(x_1, 0);
lean_inc(x_4);
x_5 = lean_ctor_get(x_1, 1);
lean_inc(x_5);
lean_dec_ref(x_1);
x_6 = lp_REPL_Lean_Elab_InfoTree_sorries(x_4);
x_7 = l_List_foldl___at___00Array_appendList_spec__0___redArg(x_2, x_6);
x_1 = x_5;
x_2 = x_7;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_List_filterTR_loop___at___00REPL_sorriesGC_spec__3(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = l_List_reverse___redArg(x_2);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_10; lean_object* x_11; 
x_4 = lean_ctor_get(x_1, 0);
lean_inc(x_4);
x_5 = lean_ctor_get(x_1, 1);
lean_inc(x_5);
if (lean_is_exclusive(x_1)) {
 lean_ctor_release(x_1, 0);
 lean_ctor_release(x_1, 1);
 x_6 = x_1;
} else {
 lean_dec_ref(x_1);
 x_6 = lean_box(0);
}
x_10 = lean_ctor_get(x_4, 1);
x_11 = lean_ctor_get(x_10, 0);
if (lean_obj_tag(x_11) == 1)
{
lean_object* x_12; 
x_12 = lean_ctor_get(x_11, 1);
if (lean_obj_tag(x_12) == 0)
{
lean_dec(x_6);
lean_dec(x_4);
x_1 = x_5;
goto _start;
}
else
{
goto block_9;
}
}
else
{
goto block_9;
}
block_9:
{
lean_object* x_7; 
if (lean_is_scalar(x_6)) {
 x_7 = lean_alloc_ctor(1, 2, 0);
} else {
 x_7 = x_6;
}
lean_ctor_set(x_7, 0, x_4);
lean_ctor_set(x_7, 1, x_2);
x_1 = x_5;
x_2 = x_7;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = l_List_reverse___redArg(x_2);
return x_3;
}
else
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_1);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_5 = lean_ctor_get(x_1, 0);
x_6 = lean_ctor_get(x_1, 1);
x_7 = lean_unsigned_to_nat(120u);
x_8 = lean_unsigned_to_nat(0u);
x_9 = l_Std_Format_pretty(x_5, x_7, x_8, x_8);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_9);
{
lean_object* _tmp_0 = x_6;
lean_object* _tmp_1 = x_1;
x_1 = _tmp_0;
x_2 = _tmp_1;
}
goto _start;
}
else
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_11 = lean_ctor_get(x_1, 0);
x_12 = lean_ctor_get(x_1, 1);
lean_inc(x_12);
lean_inc(x_11);
lean_dec(x_1);
x_13 = lean_unsigned_to_nat(120u);
x_14 = lean_unsigned_to_nat(0u);
x_15 = l_Std_Format_pretty(x_11, x_13, x_14, x_14);
x_16 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_16, 0, x_15);
lean_ctor_set(x_16, 1, x_2);
x_1 = x_12;
x_2 = x_16;
goto _start;
}
}
}
}
static lean_object* _init_lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("REPL.sorriesGC", 14, 14);
return x_1;
}
}
static lean_object* _init_lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_1 = lp_REPL_REPL_sorries___redArg___lam__16___closed__2;
x_2 = lean_unsigned_to_nat(26u);
x_3 = lean_unsigned_to_nat(125u);
x_4 = lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__0;
x_5 = lp_REPL_REPL_sorries___redArg___lam__16___closed__0;
x_6 = l_mkPanicMessageWithDecl(x_5, x_4, x_3, x_2, x_1);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
lean_object* x_5; lean_object* x_6; 
lean_dec(x_1);
x_5 = l_List_reverse___redArg(x_3);
x_6 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_6, 0, x_5);
return x_6;
}
else
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; uint8_t x_14; 
x_7 = lean_ctor_get(x_2, 0);
lean_inc(x_7);
x_8 = lean_ctor_get(x_7, 1);
lean_inc(x_8);
x_9 = lean_ctor_get(x_8, 1);
lean_inc(x_9);
x_10 = lean_ctor_get(x_2, 1);
lean_inc(x_10);
if (lean_is_exclusive(x_2)) {
 lean_ctor_release(x_2, 0);
 lean_ctor_release(x_2, 1);
 x_11 = x_2;
} else {
 lean_dec_ref(x_2);
 x_11 = lean_box(0);
}
x_12 = lean_ctor_get(x_7, 0);
lean_inc(x_12);
lean_dec(x_7);
x_13 = lean_ctor_get(x_8, 0);
lean_inc(x_13);
lean_dec(x_8);
x_14 = !lean_is_exclusive(x_9);
if (x_14 == 0)
{
lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; 
x_15 = lean_ctor_get(x_9, 0);
x_16 = lean_ctor_get(x_9, 1);
if (lean_obj_tag(x_13) == 0)
{
lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; 
x_24 = lean_ctor_get(x_13, 0);
lean_inc(x_24);
lean_dec_ref(x_13);
x_25 = lean_box(0);
x_26 = lean_box(0);
lean_ctor_set_tag(x_9, 1);
lean_ctor_set(x_9, 1, x_26);
lean_ctor_set(x_9, 0, x_24);
lean_inc(x_1);
x_27 = lp_REPL_REPL_ProofSnapshot_create(x_12, x_25, x_1, x_9, x_26);
if (lean_obj_tag(x_27) == 0)
{
lean_object* x_28; lean_object* x_29; 
x_28 = lean_ctor_get(x_27, 0);
lean_inc(x_28);
lean_dec_ref(x_27);
x_29 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_28);
if (lean_obj_tag(x_29) == 0)
{
lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; 
x_30 = lean_ctor_get(x_29, 0);
lean_inc(x_30);
lean_dec_ref(x_29);
x_31 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_32 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_30, x_26);
x_33 = l_String_intercalate(x_31, x_32);
x_17 = x_33;
x_18 = lean_box(0);
goto block_23;
}
else
{
uint8_t x_34; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_34 = !lean_is_exclusive(x_29);
if (x_34 == 0)
{
return x_29;
}
else
{
lean_object* x_35; lean_object* x_36; 
x_35 = lean_ctor_get(x_29, 0);
lean_inc(x_35);
lean_dec(x_29);
x_36 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_36, 0, x_35);
return x_36;
}
}
}
else
{
uint8_t x_37; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_37 = !lean_is_exclusive(x_27);
if (x_37 == 0)
{
return x_27;
}
else
{
lean_object* x_38; lean_object* x_39; 
x_38 = lean_ctor_get(x_27, 0);
lean_inc(x_38);
lean_dec(x_27);
x_39 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_39, 0, x_38);
return x_39;
}
}
}
else
{
lean_object* x_40; 
lean_free_object(x_9);
x_40 = lean_ctor_get(x_13, 1);
lean_inc(x_40);
if (lean_obj_tag(x_40) == 0)
{
lean_object* x_41; lean_object* x_42; 
lean_dec_ref(x_13);
lean_dec(x_12);
x_41 = lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__1;
x_42 = lp_REPL_panic___at___00REPL_sorriesGC_spec__1(x_41);
if (lean_obj_tag(x_42) == 0)
{
lean_object* x_43; lean_object* x_44; 
x_43 = lean_ctor_get(x_42, 0);
lean_inc(x_43);
lean_dec_ref(x_42);
x_44 = lean_ctor_get(x_43, 0);
lean_inc(x_44);
lean_dec(x_43);
x_17 = x_44;
x_18 = lean_box(0);
goto block_23;
}
else
{
uint8_t x_45; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_45 = !lean_is_exclusive(x_42);
if (x_45 == 0)
{
return x_42;
}
else
{
lean_object* x_46; lean_object* x_47; 
x_46 = lean_ctor_get(x_42, 0);
lean_inc(x_46);
lean_dec(x_42);
x_47 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_47, 0, x_46);
return x_47;
}
}
}
else
{
uint8_t x_48; 
x_48 = !lean_is_exclusive(x_13);
if (x_48 == 0)
{
lean_object* x_49; lean_object* x_50; uint8_t x_51; 
x_49 = lean_ctor_get(x_13, 0);
x_50 = lean_ctor_get(x_13, 1);
lean_dec(x_50);
x_51 = !lean_is_exclusive(x_40);
if (x_51 == 0)
{
lean_object* x_52; lean_object* x_53; lean_object* x_54; 
x_52 = lean_ctor_get(x_40, 0);
lean_ctor_set(x_40, 0, x_49);
x_53 = lean_box(0);
lean_ctor_set(x_13, 1, x_53);
lean_ctor_set(x_13, 0, x_52);
lean_inc(x_1);
x_54 = lp_REPL_REPL_ProofSnapshot_create(x_12, x_40, x_1, x_53, x_13);
if (lean_obj_tag(x_54) == 0)
{
lean_object* x_55; lean_object* x_56; 
x_55 = lean_ctor_get(x_54, 0);
lean_inc(x_55);
lean_dec_ref(x_54);
x_56 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_55);
if (lean_obj_tag(x_56) == 0)
{
lean_object* x_57; lean_object* x_58; lean_object* x_59; lean_object* x_60; 
x_57 = lean_ctor_get(x_56, 0);
lean_inc(x_57);
lean_dec_ref(x_56);
x_58 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_59 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_57, x_53);
x_60 = l_String_intercalate(x_58, x_59);
x_17 = x_60;
x_18 = lean_box(0);
goto block_23;
}
else
{
uint8_t x_61; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_61 = !lean_is_exclusive(x_56);
if (x_61 == 0)
{
return x_56;
}
else
{
lean_object* x_62; lean_object* x_63; 
x_62 = lean_ctor_get(x_56, 0);
lean_inc(x_62);
lean_dec(x_56);
x_63 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_63, 0, x_62);
return x_63;
}
}
}
else
{
uint8_t x_64; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_64 = !lean_is_exclusive(x_54);
if (x_64 == 0)
{
return x_54;
}
else
{
lean_object* x_65; lean_object* x_66; 
x_65 = lean_ctor_get(x_54, 0);
lean_inc(x_65);
lean_dec(x_54);
x_66 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_66, 0, x_65);
return x_66;
}
}
}
else
{
lean_object* x_67; lean_object* x_68; lean_object* x_69; lean_object* x_70; 
x_67 = lean_ctor_get(x_40, 0);
lean_inc(x_67);
lean_dec(x_40);
x_68 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_68, 0, x_49);
x_69 = lean_box(0);
lean_ctor_set(x_13, 1, x_69);
lean_ctor_set(x_13, 0, x_67);
lean_inc(x_1);
x_70 = lp_REPL_REPL_ProofSnapshot_create(x_12, x_68, x_1, x_69, x_13);
if (lean_obj_tag(x_70) == 0)
{
lean_object* x_71; lean_object* x_72; 
x_71 = lean_ctor_get(x_70, 0);
lean_inc(x_71);
lean_dec_ref(x_70);
x_72 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_71);
if (lean_obj_tag(x_72) == 0)
{
lean_object* x_73; lean_object* x_74; lean_object* x_75; lean_object* x_76; 
x_73 = lean_ctor_get(x_72, 0);
lean_inc(x_73);
lean_dec_ref(x_72);
x_74 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_75 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_73, x_69);
x_76 = l_String_intercalate(x_74, x_75);
x_17 = x_76;
x_18 = lean_box(0);
goto block_23;
}
else
{
lean_object* x_77; lean_object* x_78; lean_object* x_79; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_77 = lean_ctor_get(x_72, 0);
lean_inc(x_77);
if (lean_is_exclusive(x_72)) {
 lean_ctor_release(x_72, 0);
 x_78 = x_72;
} else {
 lean_dec_ref(x_72);
 x_78 = lean_box(0);
}
if (lean_is_scalar(x_78)) {
 x_79 = lean_alloc_ctor(1, 1, 0);
} else {
 x_79 = x_78;
}
lean_ctor_set(x_79, 0, x_77);
return x_79;
}
}
else
{
lean_object* x_80; lean_object* x_81; lean_object* x_82; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_80 = lean_ctor_get(x_70, 0);
lean_inc(x_80);
if (lean_is_exclusive(x_70)) {
 lean_ctor_release(x_70, 0);
 x_81 = x_70;
} else {
 lean_dec_ref(x_70);
 x_81 = lean_box(0);
}
if (lean_is_scalar(x_81)) {
 x_82 = lean_alloc_ctor(1, 1, 0);
} else {
 x_82 = x_81;
}
lean_ctor_set(x_82, 0, x_80);
return x_82;
}
}
}
else
{
lean_object* x_83; lean_object* x_84; lean_object* x_85; lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; 
x_83 = lean_ctor_get(x_13, 0);
lean_inc(x_83);
lean_dec(x_13);
x_84 = lean_ctor_get(x_40, 0);
lean_inc(x_84);
if (lean_is_exclusive(x_40)) {
 lean_ctor_release(x_40, 0);
 x_85 = x_40;
} else {
 lean_dec_ref(x_40);
 x_85 = lean_box(0);
}
if (lean_is_scalar(x_85)) {
 x_86 = lean_alloc_ctor(1, 1, 0);
} else {
 x_86 = x_85;
}
lean_ctor_set(x_86, 0, x_83);
x_87 = lean_box(0);
x_88 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_88, 0, x_84);
lean_ctor_set(x_88, 1, x_87);
lean_inc(x_1);
x_89 = lp_REPL_REPL_ProofSnapshot_create(x_12, x_86, x_1, x_87, x_88);
if (lean_obj_tag(x_89) == 0)
{
lean_object* x_90; lean_object* x_91; 
x_90 = lean_ctor_get(x_89, 0);
lean_inc(x_90);
lean_dec_ref(x_89);
x_91 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_90);
if (lean_obj_tag(x_91) == 0)
{
lean_object* x_92; lean_object* x_93; lean_object* x_94; lean_object* x_95; 
x_92 = lean_ctor_get(x_91, 0);
lean_inc(x_92);
lean_dec_ref(x_91);
x_93 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_94 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_92, x_87);
x_95 = l_String_intercalate(x_93, x_94);
x_17 = x_95;
x_18 = lean_box(0);
goto block_23;
}
else
{
lean_object* x_96; lean_object* x_97; lean_object* x_98; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_96 = lean_ctor_get(x_91, 0);
lean_inc(x_96);
if (lean_is_exclusive(x_91)) {
 lean_ctor_release(x_91, 0);
 x_97 = x_91;
} else {
 lean_dec_ref(x_91);
 x_97 = lean_box(0);
}
if (lean_is_scalar(x_97)) {
 x_98 = lean_alloc_ctor(1, 1, 0);
} else {
 x_98 = x_97;
}
lean_ctor_set(x_98, 0, x_96);
return x_98;
}
}
else
{
lean_object* x_99; lean_object* x_100; lean_object* x_101; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_99 = lean_ctor_get(x_89, 0);
lean_inc(x_99);
if (lean_is_exclusive(x_89)) {
 lean_ctor_release(x_89, 0);
 x_100 = x_89;
} else {
 lean_dec_ref(x_89);
 x_100 = lean_box(0);
}
if (lean_is_scalar(x_100)) {
 x_101 = lean_alloc_ctor(1, 1, 0);
} else {
 x_101 = x_100;
}
lean_ctor_set(x_101, 0, x_99);
return x_101;
}
}
}
}
block_23:
{
lean_object* x_19; lean_object* x_20; lean_object* x_21; 
x_19 = lean_box(0);
x_20 = lp_REPL_REPL_Sorry_of(x_17, x_15, x_16, x_19);
if (lean_is_scalar(x_11)) {
 x_21 = lean_alloc_ctor(1, 2, 0);
} else {
 x_21 = x_11;
}
lean_ctor_set(x_21, 0, x_20);
lean_ctor_set(x_21, 1, x_3);
x_2 = x_10;
x_3 = x_21;
goto _start;
}
}
else
{
lean_object* x_102; lean_object* x_103; lean_object* x_104; lean_object* x_105; 
x_102 = lean_ctor_get(x_9, 0);
x_103 = lean_ctor_get(x_9, 1);
lean_inc(x_103);
lean_inc(x_102);
lean_dec(x_9);
if (lean_obj_tag(x_13) == 0)
{
lean_object* x_111; lean_object* x_112; lean_object* x_113; lean_object* x_114; lean_object* x_115; 
x_111 = lean_ctor_get(x_13, 0);
lean_inc(x_111);
lean_dec_ref(x_13);
x_112 = lean_box(0);
x_113 = lean_box(0);
x_114 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_114, 0, x_111);
lean_ctor_set(x_114, 1, x_113);
lean_inc(x_1);
x_115 = lp_REPL_REPL_ProofSnapshot_create(x_12, x_112, x_1, x_114, x_113);
if (lean_obj_tag(x_115) == 0)
{
lean_object* x_116; lean_object* x_117; 
x_116 = lean_ctor_get(x_115, 0);
lean_inc(x_116);
lean_dec_ref(x_115);
x_117 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_116);
if (lean_obj_tag(x_117) == 0)
{
lean_object* x_118; lean_object* x_119; lean_object* x_120; lean_object* x_121; 
x_118 = lean_ctor_get(x_117, 0);
lean_inc(x_118);
lean_dec_ref(x_117);
x_119 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_120 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_118, x_113);
x_121 = l_String_intercalate(x_119, x_120);
x_104 = x_121;
x_105 = lean_box(0);
goto block_110;
}
else
{
lean_object* x_122; lean_object* x_123; lean_object* x_124; 
lean_dec(x_103);
lean_dec(x_102);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_122 = lean_ctor_get(x_117, 0);
lean_inc(x_122);
if (lean_is_exclusive(x_117)) {
 lean_ctor_release(x_117, 0);
 x_123 = x_117;
} else {
 lean_dec_ref(x_117);
 x_123 = lean_box(0);
}
if (lean_is_scalar(x_123)) {
 x_124 = lean_alloc_ctor(1, 1, 0);
} else {
 x_124 = x_123;
}
lean_ctor_set(x_124, 0, x_122);
return x_124;
}
}
else
{
lean_object* x_125; lean_object* x_126; lean_object* x_127; 
lean_dec(x_103);
lean_dec(x_102);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_125 = lean_ctor_get(x_115, 0);
lean_inc(x_125);
if (lean_is_exclusive(x_115)) {
 lean_ctor_release(x_115, 0);
 x_126 = x_115;
} else {
 lean_dec_ref(x_115);
 x_126 = lean_box(0);
}
if (lean_is_scalar(x_126)) {
 x_127 = lean_alloc_ctor(1, 1, 0);
} else {
 x_127 = x_126;
}
lean_ctor_set(x_127, 0, x_125);
return x_127;
}
}
else
{
lean_object* x_128; 
x_128 = lean_ctor_get(x_13, 1);
lean_inc(x_128);
if (lean_obj_tag(x_128) == 0)
{
lean_object* x_129; lean_object* x_130; 
lean_dec_ref(x_13);
lean_dec(x_12);
x_129 = lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__1;
x_130 = lp_REPL_panic___at___00REPL_sorriesGC_spec__1(x_129);
if (lean_obj_tag(x_130) == 0)
{
lean_object* x_131; lean_object* x_132; 
x_131 = lean_ctor_get(x_130, 0);
lean_inc(x_131);
lean_dec_ref(x_130);
x_132 = lean_ctor_get(x_131, 0);
lean_inc(x_132);
lean_dec(x_131);
x_104 = x_132;
x_105 = lean_box(0);
goto block_110;
}
else
{
lean_object* x_133; lean_object* x_134; lean_object* x_135; 
lean_dec(x_103);
lean_dec(x_102);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_133 = lean_ctor_get(x_130, 0);
lean_inc(x_133);
if (lean_is_exclusive(x_130)) {
 lean_ctor_release(x_130, 0);
 x_134 = x_130;
} else {
 lean_dec_ref(x_130);
 x_134 = lean_box(0);
}
if (lean_is_scalar(x_134)) {
 x_135 = lean_alloc_ctor(1, 1, 0);
} else {
 x_135 = x_134;
}
lean_ctor_set(x_135, 0, x_133);
return x_135;
}
}
else
{
lean_object* x_136; lean_object* x_137; lean_object* x_138; lean_object* x_139; lean_object* x_140; lean_object* x_141; lean_object* x_142; lean_object* x_143; 
x_136 = lean_ctor_get(x_13, 0);
lean_inc_ref(x_136);
if (lean_is_exclusive(x_13)) {
 lean_ctor_release(x_13, 0);
 lean_ctor_release(x_13, 1);
 x_137 = x_13;
} else {
 lean_dec_ref(x_13);
 x_137 = lean_box(0);
}
x_138 = lean_ctor_get(x_128, 0);
lean_inc(x_138);
if (lean_is_exclusive(x_128)) {
 lean_ctor_release(x_128, 0);
 x_139 = x_128;
} else {
 lean_dec_ref(x_128);
 x_139 = lean_box(0);
}
if (lean_is_scalar(x_139)) {
 x_140 = lean_alloc_ctor(1, 1, 0);
} else {
 x_140 = x_139;
}
lean_ctor_set(x_140, 0, x_136);
x_141 = lean_box(0);
if (lean_is_scalar(x_137)) {
 x_142 = lean_alloc_ctor(1, 2, 0);
} else {
 x_142 = x_137;
}
lean_ctor_set(x_142, 0, x_138);
lean_ctor_set(x_142, 1, x_141);
lean_inc(x_1);
x_143 = lp_REPL_REPL_ProofSnapshot_create(x_12, x_140, x_1, x_141, x_142);
if (lean_obj_tag(x_143) == 0)
{
lean_object* x_144; lean_object* x_145; 
x_144 = lean_ctor_get(x_143, 0);
lean_inc(x_144);
lean_dec_ref(x_143);
x_145 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_144);
if (lean_obj_tag(x_145) == 0)
{
lean_object* x_146; lean_object* x_147; lean_object* x_148; lean_object* x_149; 
x_146 = lean_ctor_get(x_145, 0);
lean_inc(x_146);
lean_dec_ref(x_145);
x_147 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_148 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_146, x_141);
x_149 = l_String_intercalate(x_147, x_148);
x_104 = x_149;
x_105 = lean_box(0);
goto block_110;
}
else
{
lean_object* x_150; lean_object* x_151; lean_object* x_152; 
lean_dec(x_103);
lean_dec(x_102);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_150 = lean_ctor_get(x_145, 0);
lean_inc(x_150);
if (lean_is_exclusive(x_145)) {
 lean_ctor_release(x_145, 0);
 x_151 = x_145;
} else {
 lean_dec_ref(x_145);
 x_151 = lean_box(0);
}
if (lean_is_scalar(x_151)) {
 x_152 = lean_alloc_ctor(1, 1, 0);
} else {
 x_152 = x_151;
}
lean_ctor_set(x_152, 0, x_150);
return x_152;
}
}
else
{
lean_object* x_153; lean_object* x_154; lean_object* x_155; 
lean_dec(x_103);
lean_dec(x_102);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_153 = lean_ctor_get(x_143, 0);
lean_inc(x_153);
if (lean_is_exclusive(x_143)) {
 lean_ctor_release(x_143, 0);
 x_154 = x_143;
} else {
 lean_dec_ref(x_143);
 x_154 = lean_box(0);
}
if (lean_is_scalar(x_154)) {
 x_155 = lean_alloc_ctor(1, 1, 0);
} else {
 x_155 = x_154;
}
lean_ctor_set(x_155, 0, x_153);
return x_155;
}
}
}
block_110:
{
lean_object* x_106; lean_object* x_107; lean_object* x_108; 
x_106 = lean_box(0);
x_107 = lp_REPL_REPL_Sorry_of(x_104, x_102, x_103, x_106);
if (lean_is_scalar(x_11)) {
 x_108 = lean_alloc_ctor(1, 2, 0);
} else {
 x_108 = x_11;
}
lean_ctor_set(x_108, 0, x_107);
lean_ctor_set(x_108, 1, x_3);
x_2 = x_10;
x_3 = x_108;
goto _start;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorriesGC(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; 
x_4 = lp_REPL_REPL_sorries___redArg___closed__3;
x_5 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_sorriesGC_spec__2(x_1, x_4);
x_6 = lean_box(0);
x_7 = lp_REPL_List_filterTR_loop___at___00REPL_sorriesGC_spec__3(x_5, x_6);
x_8 = lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4(x_2, x_7, x_6);
return x_8;
}
}
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorriesGC_spec__1___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_panic___at___00REPL_sorriesGC_spec__1(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorriesGC___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_sorriesGC(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4(x_1, x_2, x_3);
return x_5;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = l_Lean_PersistentHashMap_mkEmptyEntriesArray(lean_box(0), lean_box(0));
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_ppTactic___closed__0;
x_2 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(32u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_ppTactic___closed__2;
x_2 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___closed__4() {
_start:
{
size_t x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; 
x_1 = 5;
x_2 = lean_unsigned_to_nat(0u);
x_3 = lp_REPL_REPL_ppTactic___closed__2;
x_4 = lp_REPL_REPL_ppTactic___closed__3;
x_5 = lean_alloc_ctor(0, 4, sizeof(size_t)*1);
lean_ctor_set(x_5, 0, x_4);
lean_ctor_set(x_5, 1, x_3);
lean_ctor_set(x_5, 2, x_2);
lean_ctor_set(x_5, 3, x_2);
lean_ctor_set_usize(x_5, 4, x_1);
return x_5;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___closed__5() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = lean_box(1);
x_2 = lp_REPL_REPL_ppTactic___closed__4;
x_3 = lp_REPL_REPL_ppTactic___closed__1;
x_4 = lean_alloc_ctor(0, 3, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_2);
lean_ctor_set(x_4, 2, x_1);
return x_4;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___lam__0___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("<failed to pretty print>", 24, 24);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_ppTactic___lam__0___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_ppTactic___lam__0___closed__0;
x_2 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_7; 
x_7 = l_Lean_PrettyPrinter_ppTactic(x_1, x_4, x_5);
if (lean_obj_tag(x_7) == 0)
{
return x_7;
}
else
{
lean_object* x_8; uint8_t x_9; uint8_t x_16; 
x_8 = lean_ctor_get(x_7, 0);
lean_inc(x_8);
x_16 = l_Lean_Exception_isInterrupt(x_8);
if (x_16 == 0)
{
uint8_t x_17; 
x_17 = l_Lean_Exception_isRuntime(x_8);
x_9 = x_17;
goto block_15;
}
else
{
lean_dec(x_8);
x_9 = x_16;
goto block_15;
}
block_15:
{
if (x_9 == 0)
{
uint8_t x_10; 
x_10 = !lean_is_exclusive(x_7);
if (x_10 == 0)
{
lean_object* x_11; lean_object* x_12; 
x_11 = lean_ctor_get(x_7, 0);
lean_dec(x_11);
x_12 = lp_REPL_REPL_ppTactic___lam__0___closed__1;
lean_ctor_set_tag(x_7, 0);
lean_ctor_set(x_7, 0, x_12);
return x_7;
}
else
{
lean_object* x_13; lean_object* x_14; 
lean_dec(x_7);
x_13 = lp_REPL_REPL_ppTactic___lam__0___closed__1;
x_14 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_14, 0, x_13);
return x_14;
}
}
else
{
return x_7;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic___lam__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
lean_object* x_7; 
x_7 = lp_REPL_REPL_ppTactic___lam__0(x_1, x_2, x_3, x_4, x_5);
lean_dec(x_3);
lean_dec_ref(x_2);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_4 = lean_alloc_closure((void*)(lp_REPL_REPL_ppTactic___lam__0___boxed), 6, 1);
lean_closure_set(x_4, 0, x_2);
x_5 = lp_REPL_REPL_ppTactic___closed__5;
x_6 = l_Lean_Elab_ContextInfo_runMetaM___redArg(x_1, x_5, x_4);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_ppTactic___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_ppTactic(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7) {
_start:
{
uint8_t x_8; 
x_8 = !lean_is_exclusive(x_7);
if (x_8 == 0)
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_9 = lean_ctor_get(x_7, 0);
x_10 = lp_REPL_REPL_Tactic_of(x_1, x_2, x_3, x_4, x_9, x_5);
lean_ctor_set(x_7, 0, x_10);
x_11 = lean_apply_2(x_6, lean_box(0), x_7);
return x_11;
}
else
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_12 = lean_ctor_get(x_7, 0);
x_13 = lean_ctor_get(x_7, 1);
lean_inc(x_13);
lean_inc(x_12);
lean_dec(x_7);
x_14 = lp_REPL_REPL_Tactic_of(x_1, x_2, x_3, x_4, x_12, x_5);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_14);
lean_ctor_set(x_15, 1, x_13);
x_16 = lean_apply_2(x_6, lean_box(0), x_15);
return x_16;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__2(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10, lean_object* x_11) {
_start:
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; 
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
x_13 = lean_ctor_get(x_11, 1);
lean_inc(x_13);
lean_dec_ref(x_11);
lean_inc(x_2);
x_14 = l_Std_Format_pretty(x_12, x_1, x_2, x_2);
lean_inc(x_7);
x_15 = lean_alloc_closure((void*)(lp_REPL_REPL_tactics___redArg___lam__0), 7, 6);
lean_closure_set(x_15, 0, x_3);
lean_closure_set(x_15, 1, x_14);
lean_closure_set(x_15, 2, x_4);
lean_closure_set(x_15, 3, x_5);
lean_closure_set(x_15, 4, x_6);
lean_closure_set(x_15, 5, x_7);
x_16 = lp_REPL_REPL_recordProofSnapshot___redArg(x_8, x_9, x_13);
x_17 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__3), 2, 1);
lean_closure_set(x_17, 0, x_7);
lean_inc(x_10);
x_18 = lean_apply_4(x_10, lean_box(0), lean_box(0), x_16, x_17);
x_19 = lean_apply_4(x_10, lean_box(0), lean_box(0), x_18, x_15);
return x_19;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__2___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10, lean_object* x_11) {
_start:
{
lean_object* x_12; 
x_12 = lp_REPL_REPL_tactics___redArg___lam__2(x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_10, x_11);
lean_dec(x_1);
return x_12;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__1(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; 
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_1);
x_5 = lean_apply_2(x_2, lean_box(0), x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__3(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10, lean_object* x_11) {
_start:
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; 
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
x_13 = lean_ctor_get(x_11, 1);
lean_inc(x_13);
lean_dec_ref(x_11);
x_14 = lean_unsigned_to_nat(120u);
x_15 = lean_unsigned_to_nat(0u);
x_16 = l_Std_Format_pretty(x_12, x_14, x_15, x_15);
x_17 = l_String_trim(x_16);
lean_inc(x_7);
lean_inc(x_4);
x_18 = lean_alloc_closure((void*)(lp_REPL_REPL_tactics___redArg___lam__2___boxed), 11, 10);
lean_closure_set(x_18, 0, x_14);
lean_closure_set(x_18, 1, x_15);
lean_closure_set(x_18, 2, x_17);
lean_closure_set(x_18, 3, x_1);
lean_closure_set(x_18, 4, x_2);
lean_closure_set(x_18, 5, x_3);
lean_closure_set(x_18, 6, x_4);
lean_closure_set(x_18, 7, x_5);
lean_closure_set(x_18, 8, x_6);
lean_closure_set(x_18, 9, x_7);
x_19 = lean_alloc_closure((void*)(lp_REPL_REPL_ppTactic___boxed), 3, 2);
lean_closure_set(x_19, 0, x_8);
lean_closure_set(x_19, 1, x_9);
x_20 = lean_apply_2(x_10, lean_box(0), x_19);
x_21 = lean_alloc_closure((void*)(lp_REPL_REPL_tactics___redArg___lam__1), 3, 2);
lean_closure_set(x_21, 0, x_13);
lean_closure_set(x_21, 1, x_4);
lean_inc(x_7);
x_22 = lean_apply_4(x_7, lean_box(0), lean_box(0), x_20, x_21);
x_23 = lean_apply_4(x_7, lean_box(0), lean_box(0), x_22, x_18);
return x_23;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__5(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10, lean_object* x_11) {
_start:
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; 
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
x_13 = lean_ctor_get(x_11, 1);
lean_inc(x_13);
lean_dec_ref(x_11);
lean_inc(x_9);
lean_inc_ref(x_7);
lean_inc(x_6);
lean_inc(x_4);
x_14 = lean_alloc_closure((void*)(lp_REPL_REPL_tactics___redArg___lam__3), 11, 10);
lean_closure_set(x_14, 0, x_1);
lean_closure_set(x_14, 1, x_2);
lean_closure_set(x_14, 2, x_3);
lean_closure_set(x_14, 3, x_4);
lean_closure_set(x_14, 4, x_5);
lean_closure_set(x_14, 5, x_12);
lean_closure_set(x_14, 6, x_6);
lean_closure_set(x_14, 7, x_7);
lean_closure_set(x_14, 8, x_8);
lean_closure_set(x_14, 9, x_9);
x_15 = lean_alloc_closure((void*)(l_Lean_Elab_ContextInfo_ppGoals___boxed), 3, 2);
lean_closure_set(x_15, 0, x_7);
lean_closure_set(x_15, 1, x_10);
x_16 = lean_apply_2(x_9, lean_box(0), x_15);
x_17 = lean_alloc_closure((void*)(lp_REPL_REPL_tactics___redArg___lam__1), 3, 2);
lean_closure_set(x_17, 0, x_13);
lean_closure_set(x_17, 1, x_4);
lean_inc(x_6);
x_18 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_16, x_17);
x_19 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_18, x_14);
return x_19;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg___lam__6(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; 
x_5 = lean_ctor_get(x_3, 1);
lean_inc(x_5);
x_6 = lean_ctor_get(x_5, 1);
x_7 = lean_ctor_get(x_6, 1);
lean_inc(x_7);
x_8 = lean_ctor_get(x_7, 1);
lean_inc(x_8);
x_9 = lean_ctor_get(x_8, 1);
lean_inc(x_9);
x_10 = lean_ctor_get(x_1, 0);
x_11 = lean_ctor_get(x_3, 0);
lean_inc(x_11);
lean_dec_ref(x_3);
x_12 = lean_ctor_get(x_5, 0);
lean_inc(x_12);
lean_dec(x_5);
x_13 = lean_ctor_get(x_7, 0);
lean_inc(x_13);
lean_dec(x_7);
x_14 = lean_ctor_get(x_8, 0);
lean_inc(x_14);
lean_dec(x_8);
x_15 = lean_ctor_get(x_9, 0);
lean_inc(x_15);
x_16 = lean_ctor_get(x_9, 1);
lean_inc(x_16);
lean_dec(x_9);
x_17 = lean_ctor_get(x_1, 1);
lean_inc(x_17);
x_18 = lean_ctor_get(x_10, 1);
lean_inc(x_18);
lean_inc(x_13);
lean_inc(x_2);
lean_inc(x_11);
lean_inc(x_17);
lean_inc(x_18);
x_19 = lean_alloc_closure((void*)(lp_REPL_REPL_tactics___redArg___lam__5), 11, 10);
lean_closure_set(x_19, 0, x_14);
lean_closure_set(x_19, 1, x_15);
lean_closure_set(x_19, 2, x_16);
lean_closure_set(x_19, 3, x_18);
lean_closure_set(x_19, 4, x_1);
lean_closure_set(x_19, 5, x_17);
lean_closure_set(x_19, 6, x_11);
lean_closure_set(x_19, 7, x_12);
lean_closure_set(x_19, 8, x_2);
lean_closure_set(x_19, 9, x_13);
x_20 = lean_box(0);
x_21 = lean_box(0);
x_22 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_create___boxed), 6, 5);
lean_closure_set(x_22, 0, x_11);
lean_closure_set(x_22, 1, x_20);
lean_closure_set(x_22, 2, x_20);
lean_closure_set(x_22, 3, x_13);
lean_closure_set(x_22, 4, x_21);
x_23 = lean_apply_2(x_2, lean_box(0), x_22);
x_24 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__9), 3, 2);
lean_closure_set(x_24, 0, x_4);
lean_closure_set(x_24, 1, x_18);
lean_inc(x_17);
x_25 = lean_apply_4(x_17, lean_box(0), lean_box(0), x_23, x_24);
x_26 = lean_apply_4(x_17, lean_box(0), lean_box(0), x_25, x_19);
return x_26;
}
}
static lean_object* _init_lp_REPL_REPL_tactics___redArg___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(lp_REPL_Lean_Elab_InfoTree_tactics), 1, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_tactics___redArg___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; 
lean_inc_ref(x_1);
x_5 = lean_alloc_closure((void*)(lp_REPL_REPL_tactics___redArg___lam__6), 4, 2);
lean_closure_set(x_5, 0, x_1);
lean_closure_set(x_5, 1, x_2);
lean_inc_ref(x_1);
x_6 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_6, 0, x_1);
lean_inc_ref(x_1);
x_7 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_7, 0, x_1);
lean_inc_ref(x_1);
x_8 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_8, 0, x_1);
lean_inc_ref(x_1);
x_9 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_9, 0, x_1);
lean_inc_ref(x_1);
x_10 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_10, 0, lean_box(0));
lean_closure_set(x_10, 1, lean_box(0));
lean_closure_set(x_10, 2, x_1);
x_11 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_11, 0, x_10);
lean_ctor_set(x_11, 1, x_6);
lean_inc_ref(x_1);
x_12 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_12, 0, lean_box(0));
lean_closure_set(x_12, 1, lean_box(0));
lean_closure_set(x_12, 2, x_1);
x_13 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_13, 0, x_11);
lean_ctor_set(x_13, 1, x_12);
lean_ctor_set(x_13, 2, x_7);
lean_ctor_set(x_13, 3, x_8);
lean_ctor_set(x_13, 4, x_9);
x_14 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_14, 0, lean_box(0));
lean_closure_set(x_14, 1, lean_box(0));
lean_closure_set(x_14, 2, x_1);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_13);
lean_ctor_set(x_15, 1, x_14);
x_16 = lp_REPL_REPL_tactics___redArg___closed__0;
x_17 = lp_REPL_REPL_tactics___redArg___closed__1;
x_18 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___redArg(x_16, x_3, x_17);
x_19 = lean_box(0);
x_20 = l_List_mapM_loop___redArg(x_15, x_5, x_18, x_19);
x_21 = lean_apply_1(x_20, x_4);
return x_21;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_REPL_tactics___redArg(x_2, x_3, x_4, x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_tacticsGC_spec__0(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = lean_array_to_list(x_2);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lean_ctor_get(x_1, 0);
lean_inc(x_4);
x_5 = lean_ctor_get(x_1, 1);
lean_inc(x_5);
lean_dec_ref(x_1);
x_6 = lp_REPL_Lean_Elab_InfoTree_tactics(x_4);
x_7 = l_List_foldl___at___00Array_appendList_spec__0___redArg(x_2, x_6);
x_1 = x_5;
x_2 = x_7;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tacticsGC_spec__1(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_4; lean_object* x_5; 
x_4 = l_List_reverse___redArg(x_2);
x_5 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_5, 0, x_4);
return x_5;
}
else
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; uint8_t x_12; 
x_6 = lean_ctor_get(x_1, 0);
lean_inc(x_6);
x_7 = lean_ctor_get(x_6, 1);
lean_inc(x_7);
x_8 = lean_ctor_get(x_7, 1);
x_9 = lean_ctor_get(x_8, 1);
lean_inc(x_9);
x_10 = lean_ctor_get(x_9, 1);
lean_inc(x_10);
x_11 = lean_ctor_get(x_10, 1);
lean_inc(x_11);
x_12 = !lean_is_exclusive(x_1);
if (x_12 == 0)
{
lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; 
x_13 = lean_ctor_get(x_1, 1);
x_14 = lean_ctor_get(x_1, 0);
lean_dec(x_14);
x_15 = lean_ctor_get(x_6, 0);
lean_inc(x_15);
lean_dec(x_6);
x_16 = lean_ctor_get(x_7, 0);
lean_inc(x_16);
lean_dec(x_7);
x_17 = lean_ctor_get(x_9, 0);
lean_inc(x_17);
lean_dec(x_9);
x_18 = lean_ctor_get(x_10, 0);
lean_inc(x_18);
lean_dec(x_10);
x_19 = lean_ctor_get(x_11, 0);
lean_inc(x_19);
x_20 = lean_ctor_get(x_11, 1);
lean_inc(x_20);
lean_dec(x_11);
lean_inc(x_15);
x_21 = l_Lean_Elab_ContextInfo_ppGoals(x_15, x_17);
if (lean_obj_tag(x_21) == 0)
{
lean_object* x_22; lean_object* x_23; 
x_22 = lean_ctor_get(x_21, 0);
lean_inc(x_22);
lean_dec_ref(x_21);
x_23 = lp_REPL_REPL_ppTactic(x_15, x_16);
if (lean_obj_tag(x_23) == 0)
{
lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; 
x_24 = lean_ctor_get(x_23, 0);
lean_inc(x_24);
lean_dec_ref(x_23);
x_25 = lean_unsigned_to_nat(120u);
x_26 = lean_unsigned_to_nat(0u);
x_27 = l_Std_Format_pretty(x_22, x_25, x_26, x_26);
x_28 = l_String_trim(x_27);
x_29 = l_Std_Format_pretty(x_24, x_25, x_26, x_26);
x_30 = lean_box(0);
x_31 = lp_REPL_REPL_Tactic_of(x_28, x_29, x_18, x_19, x_30, x_20);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_31);
{
lean_object* _tmp_0 = x_13;
lean_object* _tmp_1 = x_1;
x_1 = _tmp_0;
x_2 = _tmp_1;
}
goto _start;
}
else
{
uint8_t x_33; 
lean_dec(x_22);
lean_dec(x_20);
lean_dec(x_19);
lean_dec(x_18);
lean_free_object(x_1);
lean_dec(x_13);
lean_dec(x_2);
x_33 = !lean_is_exclusive(x_23);
if (x_33 == 0)
{
return x_23;
}
else
{
lean_object* x_34; lean_object* x_35; 
x_34 = lean_ctor_get(x_23, 0);
lean_inc(x_34);
lean_dec(x_23);
x_35 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_35, 0, x_34);
return x_35;
}
}
}
else
{
uint8_t x_36; 
lean_dec(x_20);
lean_dec(x_19);
lean_dec(x_18);
lean_dec(x_16);
lean_dec(x_15);
lean_free_object(x_1);
lean_dec(x_13);
lean_dec(x_2);
x_36 = !lean_is_exclusive(x_21);
if (x_36 == 0)
{
return x_21;
}
else
{
lean_object* x_37; lean_object* x_38; 
x_37 = lean_ctor_get(x_21, 0);
lean_inc(x_37);
lean_dec(x_21);
x_38 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_38, 0, x_37);
return x_38;
}
}
}
else
{
lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; 
x_39 = lean_ctor_get(x_1, 1);
lean_inc(x_39);
lean_dec(x_1);
x_40 = lean_ctor_get(x_6, 0);
lean_inc(x_40);
lean_dec(x_6);
x_41 = lean_ctor_get(x_7, 0);
lean_inc(x_41);
lean_dec(x_7);
x_42 = lean_ctor_get(x_9, 0);
lean_inc(x_42);
lean_dec(x_9);
x_43 = lean_ctor_get(x_10, 0);
lean_inc(x_43);
lean_dec(x_10);
x_44 = lean_ctor_get(x_11, 0);
lean_inc(x_44);
x_45 = lean_ctor_get(x_11, 1);
lean_inc(x_45);
lean_dec(x_11);
lean_inc(x_40);
x_46 = l_Lean_Elab_ContextInfo_ppGoals(x_40, x_42);
if (lean_obj_tag(x_46) == 0)
{
lean_object* x_47; lean_object* x_48; 
x_47 = lean_ctor_get(x_46, 0);
lean_inc(x_47);
lean_dec_ref(x_46);
x_48 = lp_REPL_REPL_ppTactic(x_40, x_41);
if (lean_obj_tag(x_48) == 0)
{
lean_object* x_49; lean_object* x_50; lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; lean_object* x_57; 
x_49 = lean_ctor_get(x_48, 0);
lean_inc(x_49);
lean_dec_ref(x_48);
x_50 = lean_unsigned_to_nat(120u);
x_51 = lean_unsigned_to_nat(0u);
x_52 = l_Std_Format_pretty(x_47, x_50, x_51, x_51);
x_53 = l_String_trim(x_52);
x_54 = l_Std_Format_pretty(x_49, x_50, x_51, x_51);
x_55 = lean_box(0);
x_56 = lp_REPL_REPL_Tactic_of(x_53, x_54, x_43, x_44, x_55, x_45);
x_57 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_57, 0, x_56);
lean_ctor_set(x_57, 1, x_2);
x_1 = x_39;
x_2 = x_57;
goto _start;
}
else
{
lean_object* x_59; lean_object* x_60; lean_object* x_61; 
lean_dec(x_47);
lean_dec(x_45);
lean_dec(x_44);
lean_dec(x_43);
lean_dec(x_39);
lean_dec(x_2);
x_59 = lean_ctor_get(x_48, 0);
lean_inc(x_59);
if (lean_is_exclusive(x_48)) {
 lean_ctor_release(x_48, 0);
 x_60 = x_48;
} else {
 lean_dec_ref(x_48);
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
lean_object* x_62; lean_object* x_63; lean_object* x_64; 
lean_dec(x_45);
lean_dec(x_44);
lean_dec(x_43);
lean_dec(x_41);
lean_dec(x_40);
lean_dec(x_39);
lean_dec(x_2);
x_62 = lean_ctor_get(x_46, 0);
lean_inc(x_62);
if (lean_is_exclusive(x_46)) {
 lean_ctor_release(x_46, 0);
 x_63 = x_46;
} else {
 lean_dec_ref(x_46);
 x_63 = lean_box(0);
}
if (lean_is_scalar(x_63)) {
 x_64 = lean_alloc_ctor(1, 1, 0);
} else {
 x_64 = x_63;
}
lean_ctor_set(x_64, 0, x_62);
return x_64;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tacticsGC(lean_object* x_1) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_3 = lp_REPL_REPL_tactics___redArg___closed__1;
x_4 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_tacticsGC_spec__0(x_1, x_3);
x_5 = lean_box(0);
x_6 = lp_REPL_List_mapM_loop___at___00REPL_tacticsGC_spec__1(x_4, x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tacticsGC___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_REPL_tacticsGC(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tacticsGC_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_List_mapM_loop___at___00REPL_tacticsGC_spec__1(x_1, x_2);
return x_4;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = l_instMonadEST(lean_box(0), lean_box(0));
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = l_ReaderT_instMonad___redArg(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Lean_Core_instMonadCoreM___lam__0___boxed), 5, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__3() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Lean_Core_instMonadCoreM___lam__1___boxed), 7, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__4() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Lean_Meta_instMonadMetaM___lam__0___boxed), 7, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__5() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Lean_Meta_instMonadMetaM___lam__1___boxed), 9, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__7() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_StateRefT_x27_lift___boxed), 6, 3);
lean_closure_set(x_1, 0, lean_box(0));
lean_closure_set(x_1, 1, lean_box(0));
lean_closure_set(x_1, 2, lean_box(0));
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__8() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = l_Lean_Core_instMonadResolveNameCoreM;
x_2 = lp_REPL_REPL_createProofStepReponse___redArg___closed__7;
x_3 = l_Lean_instMonadResolveNameOfMonadLift___redArg(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__6() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_ReaderT_instMonadLift___lam__0___boxed), 3, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__9() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__8;
x_2 = lp_REPL_REPL_createProofStepReponse___redArg___closed__6;
x_3 = l_Lean_instMonadResolveNameOfMonadLift___redArg(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__10() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = l_Lean_Core_instMonadNameGeneratorCoreM;
x_2 = lp_REPL_REPL_createProofStepReponse___redArg___closed__7;
x_3 = l_Lean_monadNameGeneratorLift___redArg(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__11() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__10;
x_2 = lp_REPL_REPL_createProofStepReponse___redArg___closed__6;
x_3 = l_Lean_monadNameGeneratorLift___redArg(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__12() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = l_Lean_Core_instMonadLogCoreM;
x_2 = lp_REPL_REPL_createProofStepReponse___redArg___closed__7;
x_3 = l_Lean_instMonadLogOfMonadLift___redArg(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__13() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__12;
x_2 = lp_REPL_REPL_createProofStepReponse___redArg___closed__6;
x_3 = l_Lean_instMonadLogOfMonadLift___redArg(x_2, x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; 
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_1);
x_5 = lean_apply_2(x_2, lean_box(0), x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__1(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_6 = lean_ctor_get(x_1, 1);
lean_inc(x_6);
lean_dec_ref(x_1);
x_7 = lean_alloc_closure((void*)(lp_REPL_REPL_Message_of___boxed), 2, 1);
lean_closure_set(x_7, 0, x_4);
x_8 = lean_apply_2(x_2, lean_box(0), x_7);
x_9 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__0), 3, 2);
lean_closure_set(x_9, 0, x_5);
lean_closure_set(x_9, 1, x_6);
x_10 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_8, x_9);
return x_10;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__14() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__0), 1, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__15() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Lean_Core_instMonadOptionsCoreM___lam__0___boxed), 3, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__16() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__15;
x_2 = lean_alloc_closure((void*)(l_StateRefT_x27_lift___boxed), 6, 5);
lean_closure_set(x_2, 0, lean_box(0));
lean_closure_set(x_2, 1, lean_box(0));
lean_closure_set(x_2, 2, lean_box(0));
lean_closure_set(x_2, 3, lean_box(0));
lean_closure_set(x_2, 4, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__17() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__16;
x_2 = lean_alloc_closure((void*)(l_ReaderT_instMonadLift___lam__0___boxed), 3, 2);
lean_closure_set(x_2, 0, lean_box(0));
lean_closure_set(x_2, 1, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__3(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10, lean_object* x_11) {
_start:
{
lean_object* x_13; lean_object* x_14; 
x_13 = l_Lean_Elab_CommandContextInfo_save___redArg(x_1, x_2, x_3, x_4, x_5, x_6, x_7);
x_14 = lean_apply_5(x_13, x_8, x_9, x_10, x_11, lean_box(0));
return x_14;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10, lean_object* x_11, lean_object* x_12) {
_start:
{
lean_object* x_13; 
x_13 = lp_REPL_REPL_createProofStepReponse___redArg___lam__3(x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_10, x_11);
return x_13;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__2(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7) {
_start:
{
uint8_t x_8; 
x_8 = !lean_is_exclusive(x_7);
if (x_8 == 0)
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; 
x_9 = lean_ctor_get(x_7, 0);
x_10 = lean_box(0);
x_11 = l_List_mapTR_loop___redArg(x_1, x_9, x_10);
x_12 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_12, 0, x_2);
lean_ctor_set(x_12, 1, x_11);
lean_ctor_set(x_12, 2, x_3);
lean_ctor_set(x_12, 3, x_4);
lean_ctor_set(x_12, 4, x_5);
lean_ctor_set(x_7, 0, x_12);
x_13 = lean_apply_2(x_6, lean_box(0), x_7);
return x_13;
}
else
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; 
x_14 = lean_ctor_get(x_7, 0);
x_15 = lean_ctor_get(x_7, 1);
lean_inc(x_15);
lean_inc(x_14);
lean_dec(x_7);
x_16 = lean_box(0);
x_17 = l_List_mapTR_loop___redArg(x_1, x_14, x_16);
x_18 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_18, 0, x_2);
lean_ctor_set(x_18, 1, x_17);
lean_ctor_set(x_18, 2, x_3);
lean_ctor_set(x_18, 3, x_4);
lean_ctor_set(x_18, 4, x_5);
x_19 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_19, 0, x_18);
lean_ctor_set(x_19, 1, x_15);
x_20 = lean_apply_2(x_6, lean_box(0), x_19);
return x_20;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__5(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9) {
_start:
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_10 = lean_ctor_get(x_9, 0);
lean_inc(x_10);
x_11 = lean_ctor_get(x_9, 1);
lean_inc(x_11);
lean_dec_ref(x_9);
lean_inc(x_5);
x_12 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__2), 7, 6);
lean_closure_set(x_12, 0, x_1);
lean_closure_set(x_12, 1, x_10);
lean_closure_set(x_12, 2, x_2);
lean_closure_set(x_12, 3, x_3);
lean_closure_set(x_12, 4, x_4);
lean_closure_set(x_12, 5, x_5);
x_13 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_ppGoals___boxed), 2, 1);
lean_closure_set(x_13, 0, x_6);
x_14 = lean_apply_2(x_7, lean_box(0), x_13);
x_15 = lean_alloc_closure((void*)(lp_REPL_REPL_sorries___redArg___lam__7), 3, 2);
lean_closure_set(x_15, 0, x_11);
lean_closure_set(x_15, 1, x_5);
lean_inc(x_8);
x_16 = lean_apply_4(x_8, lean_box(0), lean_box(0), x_14, x_15);
x_17 = lean_apply_4(x_8, lean_box(0), lean_box(0), x_16, x_12);
return x_17;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__4(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9) {
_start:
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; 
x_10 = lean_ctor_get(x_9, 0);
lean_inc(x_10);
x_11 = lean_ctor_get(x_9, 1);
lean_inc(x_11);
lean_dec_ref(x_9);
lean_inc(x_7);
lean_inc_ref(x_5);
x_12 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__5), 9, 8);
lean_closure_set(x_12, 0, x_1);
lean_closure_set(x_12, 1, x_2);
lean_closure_set(x_12, 2, x_10);
lean_closure_set(x_12, 3, x_3);
lean_closure_set(x_12, 4, x_4);
lean_closure_set(x_12, 5, x_5);
lean_closure_set(x_12, 6, x_6);
lean_closure_set(x_12, 7, x_7);
x_13 = lp_REPL_REPL_recordProofSnapshot___redArg(x_8, x_5, x_11);
x_14 = lean_apply_4(x_7, lean_box(0), lean_box(0), x_13, x_12);
return x_14;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__6(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_7 = lean_box(0);
x_8 = lp_REPL_REPL_sorries___redArg(x_1, x_2, x_5, x_7, x_6);
x_9 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_8, x_4);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__7(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; 
x_3 = lean_ctor_get(x_2, 0);
lean_inc(x_3);
x_4 = lean_ctor_get(x_2, 1);
lean_inc(x_4);
lean_dec_ref(x_2);
x_5 = lean_apply_2(x_1, x_3, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__9(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_1);
lean_ctor_set(x_3, 1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__8(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; lean_object* x_7; uint8_t x_8; 
x_6 = lean_ctor_get(x_5, 0);
lean_inc(x_6);
x_7 = lean_ctor_get(x_5, 1);
lean_inc(x_7);
lean_dec_ref(x_5);
x_8 = !lean_is_exclusive(x_6);
if (x_8 == 0)
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_9 = lean_ctor_get(x_6, 0);
x_10 = lean_ctor_get(x_6, 1);
lean_dec(x_10);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_9);
x_12 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__9), 2, 1);
lean_closure_set(x_12, 0, x_11);
x_13 = lean_box(0);
x_14 = l_List_mapTR_loop___redArg(x_12, x_1, x_13);
lean_ctor_set(x_6, 1, x_7);
lean_ctor_set(x_6, 0, x_14);
x_15 = lean_apply_2(x_2, lean_box(0), x_6);
x_16 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_15, x_4);
return x_16;
}
else
{
lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; 
x_17 = lean_ctor_get(x_6, 0);
lean_inc(x_17);
lean_dec(x_6);
x_18 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_18, 0, x_17);
x_19 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__9), 2, 1);
lean_closure_set(x_19, 0, x_18);
x_20 = lean_box(0);
x_21 = l_List_mapTR_loop___redArg(x_19, x_1, x_20);
x_22 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_22, 0, x_21);
lean_ctor_set(x_22, 1, x_7);
x_23 = lean_apply_2(x_2, lean_box(0), x_22);
x_24 = lean_apply_4(x_3, lean_box(0), lean_box(0), x_23, x_4);
return x_24;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__10(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; 
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_1);
x_5 = lean_apply_2(x_2, lean_box(0), x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__11(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10) {
_start:
{
uint8_t x_11; 
x_11 = !lean_is_exclusive(x_10);
if (x_11 == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_12 = lean_ctor_get(x_10, 0);
x_13 = lean_ctor_get(x_10, 1);
lean_inc_ref(x_7);
lean_inc(x_6);
lean_inc(x_5);
lean_inc_ref(x_4);
lean_inc(x_3);
x_14 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__4), 9, 8);
lean_closure_set(x_14, 0, x_1);
lean_closure_set(x_14, 1, x_2);
lean_closure_set(x_14, 2, x_12);
lean_closure_set(x_14, 3, x_3);
lean_closure_set(x_14, 4, x_4);
lean_closure_set(x_14, 5, x_5);
lean_closure_set(x_14, 6, x_6);
lean_closure_set(x_14, 7, x_7);
lean_inc(x_6);
lean_inc(x_5);
x_15 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__6), 6, 4);
lean_closure_set(x_15, 0, x_7);
lean_closure_set(x_15, 1, x_5);
lean_closure_set(x_15, 2, x_6);
lean_closure_set(x_15, 3, x_14);
lean_inc(x_8);
x_16 = lp_REPL_REPL_ProofSnapshot_newInfoTrees(x_4, x_8);
if (lean_obj_tag(x_8) == 0)
{
lean_object* x_17; lean_object* x_18; lean_object* x_19; 
lean_dec_ref(x_9);
lean_dec(x_5);
x_17 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__7), 2, 1);
lean_closure_set(x_17, 0, x_15);
lean_ctor_set(x_10, 0, x_16);
x_18 = lean_apply_2(x_3, lean_box(0), x_10);
x_19 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_18, x_17);
return x_19;
}
else
{
lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; 
lean_free_object(x_10);
x_20 = lean_ctor_get(x_8, 0);
lean_inc(x_20);
lean_dec_ref(x_8);
x_21 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__7), 2, 1);
lean_closure_set(x_21, 0, x_15);
lean_inc(x_6);
lean_inc(x_3);
x_22 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__8), 5, 4);
lean_closure_set(x_22, 0, x_16);
lean_closure_set(x_22, 1, x_3);
lean_closure_set(x_22, 2, x_6);
lean_closure_set(x_22, 3, x_21);
x_23 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_runMetaM___boxed), 4, 3);
lean_closure_set(x_23, 0, lean_box(0));
lean_closure_set(x_23, 1, x_20);
lean_closure_set(x_23, 2, x_9);
x_24 = lean_apply_2(x_5, lean_box(0), x_23);
x_25 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__10), 3, 2);
lean_closure_set(x_25, 0, x_13);
lean_closure_set(x_25, 1, x_3);
lean_inc(x_6);
x_26 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_24, x_25);
x_27 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_26, x_22);
return x_27;
}
}
else
{
lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; 
x_28 = lean_ctor_get(x_10, 0);
x_29 = lean_ctor_get(x_10, 1);
lean_inc(x_29);
lean_inc(x_28);
lean_dec(x_10);
lean_inc_ref(x_7);
lean_inc(x_6);
lean_inc(x_5);
lean_inc_ref(x_4);
lean_inc(x_3);
x_30 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__4), 9, 8);
lean_closure_set(x_30, 0, x_1);
lean_closure_set(x_30, 1, x_2);
lean_closure_set(x_30, 2, x_28);
lean_closure_set(x_30, 3, x_3);
lean_closure_set(x_30, 4, x_4);
lean_closure_set(x_30, 5, x_5);
lean_closure_set(x_30, 6, x_6);
lean_closure_set(x_30, 7, x_7);
lean_inc(x_6);
lean_inc(x_5);
x_31 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__6), 6, 4);
lean_closure_set(x_31, 0, x_7);
lean_closure_set(x_31, 1, x_5);
lean_closure_set(x_31, 2, x_6);
lean_closure_set(x_31, 3, x_30);
lean_inc(x_8);
x_32 = lp_REPL_REPL_ProofSnapshot_newInfoTrees(x_4, x_8);
if (lean_obj_tag(x_8) == 0)
{
lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; 
lean_dec_ref(x_9);
lean_dec(x_5);
x_33 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__7), 2, 1);
lean_closure_set(x_33, 0, x_31);
x_34 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_34, 0, x_32);
lean_ctor_set(x_34, 1, x_29);
x_35 = lean_apply_2(x_3, lean_box(0), x_34);
x_36 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_35, x_33);
return x_36;
}
else
{
lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; 
x_37 = lean_ctor_get(x_8, 0);
lean_inc(x_37);
lean_dec_ref(x_8);
x_38 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__7), 2, 1);
lean_closure_set(x_38, 0, x_31);
lean_inc(x_6);
lean_inc(x_3);
x_39 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__8), 5, 4);
lean_closure_set(x_39, 0, x_32);
lean_closure_set(x_39, 1, x_3);
lean_closure_set(x_39, 2, x_6);
lean_closure_set(x_39, 3, x_38);
x_40 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_runMetaM___boxed), 4, 3);
lean_closure_set(x_40, 0, lean_box(0));
lean_closure_set(x_40, 1, x_37);
lean_closure_set(x_40, 2, x_9);
x_41 = lean_apply_2(x_5, lean_box(0), x_40);
x_42 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__10), 3, 2);
lean_closure_set(x_42, 0, x_29);
lean_closure_set(x_42, 1, x_3);
lean_inc(x_6);
x_43 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_41, x_42);
x_44 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_43, x_39);
return x_44;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__12(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; 
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_1);
x_5 = lean_apply_2(x_2, lean_box(0), x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg___lam__13(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9) {
_start:
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; 
x_10 = lean_ctor_get(x_9, 0);
lean_inc(x_10);
x_11 = lean_ctor_get(x_9, 1);
lean_inc(x_11);
lean_dec_ref(x_9);
x_12 = lean_ctor_get(x_1, 1);
lean_inc(x_12);
lean_dec_ref(x_1);
lean_inc(x_7);
lean_inc(x_5);
lean_inc(x_4);
lean_inc_ref(x_3);
lean_inc(x_12);
x_13 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__11), 10, 9);
lean_closure_set(x_13, 0, x_2);
lean_closure_set(x_13, 1, x_10);
lean_closure_set(x_13, 2, x_12);
lean_closure_set(x_13, 3, x_3);
lean_closure_set(x_13, 4, x_4);
lean_closure_set(x_13, 5, x_5);
lean_closure_set(x_13, 6, x_6);
lean_closure_set(x_13, 7, x_7);
lean_closure_set(x_13, 8, x_8);
x_14 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_newTraces___boxed), 3, 2);
lean_closure_set(x_14, 0, x_3);
lean_closure_set(x_14, 1, x_7);
x_15 = lean_apply_2(x_4, lean_box(0), x_14);
x_16 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__12), 3, 2);
lean_closure_set(x_16, 0, x_11);
lean_closure_set(x_16, 1, x_12);
lean_inc(x_5);
x_17 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_15, x_16);
x_18 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_17, x_13);
return x_18;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; uint8_t x_7; 
x_6 = lp_REPL_REPL_createProofStepReponse___redArg___closed__1;
x_7 = !lean_is_exclusive(x_6);
if (x_7 == 0)
{
lean_object* x_8; lean_object* x_9; uint8_t x_10; 
x_8 = lean_ctor_get(x_6, 0);
x_9 = lean_ctor_get(x_6, 1);
lean_dec(x_9);
x_10 = !lean_is_exclusive(x_8);
if (x_10 == 0)
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; uint8_t x_25; 
x_11 = lean_ctor_get(x_8, 0);
x_12 = lean_ctor_get(x_8, 2);
x_13 = lean_ctor_get(x_8, 3);
x_14 = lean_ctor_get(x_8, 4);
x_15 = lean_ctor_get(x_8, 1);
lean_dec(x_15);
x_16 = lp_REPL_REPL_createProofStepReponse___redArg___closed__2;
x_17 = lp_REPL_REPL_createProofStepReponse___redArg___closed__3;
lean_inc_ref(x_11);
x_18 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_18, 0, x_11);
x_19 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_19, 0, x_11);
x_20 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_20, 0, x_18);
lean_ctor_set(x_20, 1, x_19);
x_21 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_21, 0, x_14);
x_22 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_22, 0, x_13);
x_23 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_23, 0, x_12);
lean_ctor_set(x_8, 4, x_21);
lean_ctor_set(x_8, 3, x_22);
lean_ctor_set(x_8, 2, x_23);
lean_ctor_set(x_8, 1, x_16);
lean_ctor_set(x_8, 0, x_20);
lean_ctor_set(x_6, 1, x_17);
x_24 = l_ReaderT_instMonad___redArg(x_6);
x_25 = !lean_is_exclusive(x_24);
if (x_25 == 0)
{
lean_object* x_26; lean_object* x_27; uint8_t x_28; 
x_26 = lean_ctor_get(x_24, 0);
x_27 = lean_ctor_get(x_24, 1);
lean_dec(x_27);
x_28 = !lean_is_exclusive(x_26);
if (x_28 == 0)
{
lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; uint8_t x_47; 
x_29 = lean_ctor_get(x_26, 0);
x_30 = lean_ctor_get(x_26, 2);
x_31 = lean_ctor_get(x_26, 3);
x_32 = lean_ctor_get(x_26, 4);
x_33 = lean_ctor_get(x_26, 1);
lean_dec(x_33);
x_34 = lp_REPL_REPL_createProofStepReponse___redArg___closed__4;
x_35 = lp_REPL_REPL_createProofStepReponse___redArg___closed__5;
lean_inc_ref(x_29);
x_36 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_36, 0, x_29);
x_37 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_37, 0, x_29);
x_38 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_38, 0, x_36);
lean_ctor_set(x_38, 1, x_37);
x_39 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_39, 0, x_32);
x_40 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_40, 0, x_31);
x_41 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_41, 0, x_30);
lean_ctor_set(x_26, 4, x_39);
lean_ctor_set(x_26, 3, x_40);
lean_ctor_set(x_26, 2, x_41);
lean_ctor_set(x_26, 1, x_34);
lean_ctor_set(x_26, 0, x_38);
lean_ctor_set(x_24, 1, x_35);
x_42 = l_Lean_Meta_instMonadEnvMetaM;
x_43 = l_Lean_Meta_instMonadMCtxMetaM;
x_44 = lp_REPL_REPL_createProofStepReponse___redArg___closed__9;
x_45 = lp_REPL_REPL_createProofStepReponse___redArg___closed__11;
x_46 = lp_REPL_REPL_createProofStepReponse___redArg___closed__13;
x_47 = !lean_is_exclusive(x_46);
if (x_47 == 0)
{
lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; lean_object* x_57; lean_object* x_58; lean_object* x_59; lean_object* x_60; lean_object* x_61; lean_object* x_62; lean_object* x_63; lean_object* x_64; lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_68; lean_object* x_69; lean_object* x_70; lean_object* x_71; lean_object* x_72; lean_object* x_73; 
x_48 = lean_ctor_get(x_46, 0);
x_49 = lean_ctor_get(x_46, 4);
lean_dec(x_49);
x_50 = lean_ctor_get(x_46, 3);
lean_dec(x_50);
x_51 = lean_ctor_get(x_46, 2);
lean_dec(x_51);
x_52 = lean_ctor_get(x_46, 1);
lean_dec(x_52);
lean_inc_ref(x_1);
x_53 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_53, 0, x_1);
lean_inc_ref(x_1);
x_54 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_54, 0, x_1);
lean_inc_ref(x_1);
x_55 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_55, 0, x_1);
lean_inc_ref(x_1);
x_56 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_56, 0, x_1);
lean_inc_ref(x_1);
x_57 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_57, 0, lean_box(0));
lean_closure_set(x_57, 1, lean_box(0));
lean_closure_set(x_57, 2, x_1);
x_58 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_58, 0, x_57);
lean_ctor_set(x_58, 1, x_53);
lean_inc_ref(x_1);
x_59 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_59, 0, lean_box(0));
lean_closure_set(x_59, 1, lean_box(0));
lean_closure_set(x_59, 2, x_1);
lean_ctor_set(x_46, 4, x_56);
lean_ctor_set(x_46, 3, x_55);
lean_ctor_set(x_46, 2, x_54);
lean_ctor_set(x_46, 1, x_59);
lean_ctor_set(x_46, 0, x_58);
lean_inc_ref(x_1);
x_60 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_60, 0, lean_box(0));
lean_closure_set(x_60, 1, lean_box(0));
lean_closure_set(x_60, 2, x_1);
x_61 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_61, 0, x_46);
lean_ctor_set(x_61, 1, x_60);
x_62 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_62);
x_63 = lean_ctor_get(x_1, 1);
lean_inc(x_63);
lean_inc(x_63);
lean_inc(x_2);
lean_inc_ref(x_62);
x_64 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__1), 5, 3);
lean_closure_set(x_64, 0, x_62);
lean_closure_set(x_64, 1, x_2);
lean_closure_set(x_64, 2, x_63);
x_65 = lp_REPL_REPL_createProofStepReponse___redArg___closed__14;
x_66 = lp_REPL_REPL_createProofStepReponse___redArg___closed__17;
x_67 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed), 12, 7);
lean_closure_set(x_67, 0, x_24);
lean_closure_set(x_67, 1, x_42);
lean_closure_set(x_67, 2, x_43);
lean_closure_set(x_67, 3, x_66);
lean_closure_set(x_67, 4, x_44);
lean_closure_set(x_67, 5, x_45);
lean_closure_set(x_67, 6, x_48);
lean_inc(x_4);
lean_inc(x_63);
lean_inc_ref(x_3);
x_68 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__13), 9, 8);
lean_closure_set(x_68, 0, x_62);
lean_closure_set(x_68, 1, x_65);
lean_closure_set(x_68, 2, x_3);
lean_closure_set(x_68, 3, x_2);
lean_closure_set(x_68, 4, x_63);
lean_closure_set(x_68, 5, x_1);
lean_closure_set(x_68, 6, x_4);
lean_closure_set(x_68, 7, x_67);
x_69 = lp_REPL_REPL_ProofSnapshot_newMessages(x_3, x_4);
lean_dec(x_4);
lean_dec_ref(x_3);
x_70 = lean_box(0);
x_71 = l_List_mapM_loop___redArg(x_61, x_64, x_69, x_70);
x_72 = lean_apply_1(x_71, x_5);
x_73 = lean_apply_4(x_63, lean_box(0), lean_box(0), x_72, x_68);
return x_73;
}
else
{
lean_object* x_74; lean_object* x_75; lean_object* x_76; lean_object* x_77; lean_object* x_78; lean_object* x_79; lean_object* x_80; lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; lean_object* x_85; lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; lean_object* x_90; lean_object* x_91; lean_object* x_92; lean_object* x_93; lean_object* x_94; lean_object* x_95; lean_object* x_96; 
x_74 = lean_ctor_get(x_46, 0);
lean_inc(x_74);
lean_dec(x_46);
lean_inc_ref(x_1);
x_75 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_75, 0, x_1);
lean_inc_ref(x_1);
x_76 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_76, 0, x_1);
lean_inc_ref(x_1);
x_77 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_77, 0, x_1);
lean_inc_ref(x_1);
x_78 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_78, 0, x_1);
lean_inc_ref(x_1);
x_79 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_79, 0, lean_box(0));
lean_closure_set(x_79, 1, lean_box(0));
lean_closure_set(x_79, 2, x_1);
x_80 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_80, 0, x_79);
lean_ctor_set(x_80, 1, x_75);
lean_inc_ref(x_1);
x_81 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_81, 0, lean_box(0));
lean_closure_set(x_81, 1, lean_box(0));
lean_closure_set(x_81, 2, x_1);
x_82 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_82, 0, x_80);
lean_ctor_set(x_82, 1, x_81);
lean_ctor_set(x_82, 2, x_76);
lean_ctor_set(x_82, 3, x_77);
lean_ctor_set(x_82, 4, x_78);
lean_inc_ref(x_1);
x_83 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_83, 0, lean_box(0));
lean_closure_set(x_83, 1, lean_box(0));
lean_closure_set(x_83, 2, x_1);
x_84 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_84, 0, x_82);
lean_ctor_set(x_84, 1, x_83);
x_85 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_85);
x_86 = lean_ctor_get(x_1, 1);
lean_inc(x_86);
lean_inc(x_86);
lean_inc(x_2);
lean_inc_ref(x_85);
x_87 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__1), 5, 3);
lean_closure_set(x_87, 0, x_85);
lean_closure_set(x_87, 1, x_2);
lean_closure_set(x_87, 2, x_86);
x_88 = lp_REPL_REPL_createProofStepReponse___redArg___closed__14;
x_89 = lp_REPL_REPL_createProofStepReponse___redArg___closed__17;
x_90 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed), 12, 7);
lean_closure_set(x_90, 0, x_24);
lean_closure_set(x_90, 1, x_42);
lean_closure_set(x_90, 2, x_43);
lean_closure_set(x_90, 3, x_89);
lean_closure_set(x_90, 4, x_44);
lean_closure_set(x_90, 5, x_45);
lean_closure_set(x_90, 6, x_74);
lean_inc(x_4);
lean_inc(x_86);
lean_inc_ref(x_3);
x_91 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__13), 9, 8);
lean_closure_set(x_91, 0, x_85);
lean_closure_set(x_91, 1, x_88);
lean_closure_set(x_91, 2, x_3);
lean_closure_set(x_91, 3, x_2);
lean_closure_set(x_91, 4, x_86);
lean_closure_set(x_91, 5, x_1);
lean_closure_set(x_91, 6, x_4);
lean_closure_set(x_91, 7, x_90);
x_92 = lp_REPL_REPL_ProofSnapshot_newMessages(x_3, x_4);
lean_dec(x_4);
lean_dec_ref(x_3);
x_93 = lean_box(0);
x_94 = l_List_mapM_loop___redArg(x_84, x_87, x_92, x_93);
x_95 = lean_apply_1(x_94, x_5);
x_96 = lean_apply_4(x_86, lean_box(0), lean_box(0), x_95, x_91);
return x_96;
}
}
else
{
lean_object* x_97; lean_object* x_98; lean_object* x_99; lean_object* x_100; lean_object* x_101; lean_object* x_102; lean_object* x_103; lean_object* x_104; lean_object* x_105; lean_object* x_106; lean_object* x_107; lean_object* x_108; lean_object* x_109; lean_object* x_110; lean_object* x_111; lean_object* x_112; lean_object* x_113; lean_object* x_114; lean_object* x_115; lean_object* x_116; lean_object* x_117; lean_object* x_118; lean_object* x_119; lean_object* x_120; lean_object* x_121; lean_object* x_122; lean_object* x_123; lean_object* x_124; lean_object* x_125; lean_object* x_126; lean_object* x_127; lean_object* x_128; lean_object* x_129; lean_object* x_130; lean_object* x_131; lean_object* x_132; lean_object* x_133; lean_object* x_134; lean_object* x_135; lean_object* x_136; lean_object* x_137; lean_object* x_138; 
x_97 = lean_ctor_get(x_26, 0);
x_98 = lean_ctor_get(x_26, 2);
x_99 = lean_ctor_get(x_26, 3);
x_100 = lean_ctor_get(x_26, 4);
lean_inc(x_100);
lean_inc(x_99);
lean_inc(x_98);
lean_inc(x_97);
lean_dec(x_26);
x_101 = lp_REPL_REPL_createProofStepReponse___redArg___closed__4;
x_102 = lp_REPL_REPL_createProofStepReponse___redArg___closed__5;
lean_inc_ref(x_97);
x_103 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_103, 0, x_97);
x_104 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_104, 0, x_97);
x_105 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_105, 0, x_103);
lean_ctor_set(x_105, 1, x_104);
x_106 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_106, 0, x_100);
x_107 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_107, 0, x_99);
x_108 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_108, 0, x_98);
x_109 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_109, 0, x_105);
lean_ctor_set(x_109, 1, x_101);
lean_ctor_set(x_109, 2, x_108);
lean_ctor_set(x_109, 3, x_107);
lean_ctor_set(x_109, 4, x_106);
lean_ctor_set(x_24, 1, x_102);
lean_ctor_set(x_24, 0, x_109);
x_110 = l_Lean_Meta_instMonadEnvMetaM;
x_111 = l_Lean_Meta_instMonadMCtxMetaM;
x_112 = lp_REPL_REPL_createProofStepReponse___redArg___closed__9;
x_113 = lp_REPL_REPL_createProofStepReponse___redArg___closed__11;
x_114 = lp_REPL_REPL_createProofStepReponse___redArg___closed__13;
x_115 = lean_ctor_get(x_114, 0);
lean_inc(x_115);
if (lean_is_exclusive(x_114)) {
 lean_ctor_release(x_114, 0);
 lean_ctor_release(x_114, 1);
 lean_ctor_release(x_114, 2);
 lean_ctor_release(x_114, 3);
 lean_ctor_release(x_114, 4);
 x_116 = x_114;
} else {
 lean_dec_ref(x_114);
 x_116 = lean_box(0);
}
lean_inc_ref(x_1);
x_117 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_117, 0, x_1);
lean_inc_ref(x_1);
x_118 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_118, 0, x_1);
lean_inc_ref(x_1);
x_119 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_119, 0, x_1);
lean_inc_ref(x_1);
x_120 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_120, 0, x_1);
lean_inc_ref(x_1);
x_121 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_121, 0, lean_box(0));
lean_closure_set(x_121, 1, lean_box(0));
lean_closure_set(x_121, 2, x_1);
x_122 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_122, 0, x_121);
lean_ctor_set(x_122, 1, x_117);
lean_inc_ref(x_1);
x_123 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_123, 0, lean_box(0));
lean_closure_set(x_123, 1, lean_box(0));
lean_closure_set(x_123, 2, x_1);
if (lean_is_scalar(x_116)) {
 x_124 = lean_alloc_ctor(0, 5, 0);
} else {
 x_124 = x_116;
}
lean_ctor_set(x_124, 0, x_122);
lean_ctor_set(x_124, 1, x_123);
lean_ctor_set(x_124, 2, x_118);
lean_ctor_set(x_124, 3, x_119);
lean_ctor_set(x_124, 4, x_120);
lean_inc_ref(x_1);
x_125 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_125, 0, lean_box(0));
lean_closure_set(x_125, 1, lean_box(0));
lean_closure_set(x_125, 2, x_1);
x_126 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_126, 0, x_124);
lean_ctor_set(x_126, 1, x_125);
x_127 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_127);
x_128 = lean_ctor_get(x_1, 1);
lean_inc(x_128);
lean_inc(x_128);
lean_inc(x_2);
lean_inc_ref(x_127);
x_129 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__1), 5, 3);
lean_closure_set(x_129, 0, x_127);
lean_closure_set(x_129, 1, x_2);
lean_closure_set(x_129, 2, x_128);
x_130 = lp_REPL_REPL_createProofStepReponse___redArg___closed__14;
x_131 = lp_REPL_REPL_createProofStepReponse___redArg___closed__17;
x_132 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed), 12, 7);
lean_closure_set(x_132, 0, x_24);
lean_closure_set(x_132, 1, x_110);
lean_closure_set(x_132, 2, x_111);
lean_closure_set(x_132, 3, x_131);
lean_closure_set(x_132, 4, x_112);
lean_closure_set(x_132, 5, x_113);
lean_closure_set(x_132, 6, x_115);
lean_inc(x_4);
lean_inc(x_128);
lean_inc_ref(x_3);
x_133 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__13), 9, 8);
lean_closure_set(x_133, 0, x_127);
lean_closure_set(x_133, 1, x_130);
lean_closure_set(x_133, 2, x_3);
lean_closure_set(x_133, 3, x_2);
lean_closure_set(x_133, 4, x_128);
lean_closure_set(x_133, 5, x_1);
lean_closure_set(x_133, 6, x_4);
lean_closure_set(x_133, 7, x_132);
x_134 = lp_REPL_REPL_ProofSnapshot_newMessages(x_3, x_4);
lean_dec(x_4);
lean_dec_ref(x_3);
x_135 = lean_box(0);
x_136 = l_List_mapM_loop___redArg(x_126, x_129, x_134, x_135);
x_137 = lean_apply_1(x_136, x_5);
x_138 = lean_apply_4(x_128, lean_box(0), lean_box(0), x_137, x_133);
return x_138;
}
}
else
{
lean_object* x_139; lean_object* x_140; lean_object* x_141; lean_object* x_142; lean_object* x_143; lean_object* x_144; lean_object* x_145; lean_object* x_146; lean_object* x_147; lean_object* x_148; lean_object* x_149; lean_object* x_150; lean_object* x_151; lean_object* x_152; lean_object* x_153; lean_object* x_154; lean_object* x_155; lean_object* x_156; lean_object* x_157; lean_object* x_158; lean_object* x_159; lean_object* x_160; lean_object* x_161; lean_object* x_162; lean_object* x_163; lean_object* x_164; lean_object* x_165; lean_object* x_166; lean_object* x_167; lean_object* x_168; lean_object* x_169; lean_object* x_170; lean_object* x_171; lean_object* x_172; lean_object* x_173; lean_object* x_174; lean_object* x_175; lean_object* x_176; lean_object* x_177; lean_object* x_178; lean_object* x_179; lean_object* x_180; lean_object* x_181; lean_object* x_182; lean_object* x_183; 
x_139 = lean_ctor_get(x_24, 0);
lean_inc(x_139);
lean_dec(x_24);
x_140 = lean_ctor_get(x_139, 0);
lean_inc_ref(x_140);
x_141 = lean_ctor_get(x_139, 2);
lean_inc(x_141);
x_142 = lean_ctor_get(x_139, 3);
lean_inc(x_142);
x_143 = lean_ctor_get(x_139, 4);
lean_inc(x_143);
if (lean_is_exclusive(x_139)) {
 lean_ctor_release(x_139, 0);
 lean_ctor_release(x_139, 1);
 lean_ctor_release(x_139, 2);
 lean_ctor_release(x_139, 3);
 lean_ctor_release(x_139, 4);
 x_144 = x_139;
} else {
 lean_dec_ref(x_139);
 x_144 = lean_box(0);
}
x_145 = lp_REPL_REPL_createProofStepReponse___redArg___closed__4;
x_146 = lp_REPL_REPL_createProofStepReponse___redArg___closed__5;
lean_inc_ref(x_140);
x_147 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_147, 0, x_140);
x_148 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_148, 0, x_140);
x_149 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_149, 0, x_147);
lean_ctor_set(x_149, 1, x_148);
x_150 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_150, 0, x_143);
x_151 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_151, 0, x_142);
x_152 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_152, 0, x_141);
if (lean_is_scalar(x_144)) {
 x_153 = lean_alloc_ctor(0, 5, 0);
} else {
 x_153 = x_144;
}
lean_ctor_set(x_153, 0, x_149);
lean_ctor_set(x_153, 1, x_145);
lean_ctor_set(x_153, 2, x_152);
lean_ctor_set(x_153, 3, x_151);
lean_ctor_set(x_153, 4, x_150);
x_154 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_154, 0, x_153);
lean_ctor_set(x_154, 1, x_146);
x_155 = l_Lean_Meta_instMonadEnvMetaM;
x_156 = l_Lean_Meta_instMonadMCtxMetaM;
x_157 = lp_REPL_REPL_createProofStepReponse___redArg___closed__9;
x_158 = lp_REPL_REPL_createProofStepReponse___redArg___closed__11;
x_159 = lp_REPL_REPL_createProofStepReponse___redArg___closed__13;
x_160 = lean_ctor_get(x_159, 0);
lean_inc(x_160);
if (lean_is_exclusive(x_159)) {
 lean_ctor_release(x_159, 0);
 lean_ctor_release(x_159, 1);
 lean_ctor_release(x_159, 2);
 lean_ctor_release(x_159, 3);
 lean_ctor_release(x_159, 4);
 x_161 = x_159;
} else {
 lean_dec_ref(x_159);
 x_161 = lean_box(0);
}
lean_inc_ref(x_1);
x_162 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_162, 0, x_1);
lean_inc_ref(x_1);
x_163 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_163, 0, x_1);
lean_inc_ref(x_1);
x_164 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_164, 0, x_1);
lean_inc_ref(x_1);
x_165 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_165, 0, x_1);
lean_inc_ref(x_1);
x_166 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_166, 0, lean_box(0));
lean_closure_set(x_166, 1, lean_box(0));
lean_closure_set(x_166, 2, x_1);
x_167 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_167, 0, x_166);
lean_ctor_set(x_167, 1, x_162);
lean_inc_ref(x_1);
x_168 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_168, 0, lean_box(0));
lean_closure_set(x_168, 1, lean_box(0));
lean_closure_set(x_168, 2, x_1);
if (lean_is_scalar(x_161)) {
 x_169 = lean_alloc_ctor(0, 5, 0);
} else {
 x_169 = x_161;
}
lean_ctor_set(x_169, 0, x_167);
lean_ctor_set(x_169, 1, x_168);
lean_ctor_set(x_169, 2, x_163);
lean_ctor_set(x_169, 3, x_164);
lean_ctor_set(x_169, 4, x_165);
lean_inc_ref(x_1);
x_170 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_170, 0, lean_box(0));
lean_closure_set(x_170, 1, lean_box(0));
lean_closure_set(x_170, 2, x_1);
x_171 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_171, 0, x_169);
lean_ctor_set(x_171, 1, x_170);
x_172 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_172);
x_173 = lean_ctor_get(x_1, 1);
lean_inc(x_173);
lean_inc(x_173);
lean_inc(x_2);
lean_inc_ref(x_172);
x_174 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__1), 5, 3);
lean_closure_set(x_174, 0, x_172);
lean_closure_set(x_174, 1, x_2);
lean_closure_set(x_174, 2, x_173);
x_175 = lp_REPL_REPL_createProofStepReponse___redArg___closed__14;
x_176 = lp_REPL_REPL_createProofStepReponse___redArg___closed__17;
x_177 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed), 12, 7);
lean_closure_set(x_177, 0, x_154);
lean_closure_set(x_177, 1, x_155);
lean_closure_set(x_177, 2, x_156);
lean_closure_set(x_177, 3, x_176);
lean_closure_set(x_177, 4, x_157);
lean_closure_set(x_177, 5, x_158);
lean_closure_set(x_177, 6, x_160);
lean_inc(x_4);
lean_inc(x_173);
lean_inc_ref(x_3);
x_178 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__13), 9, 8);
lean_closure_set(x_178, 0, x_172);
lean_closure_set(x_178, 1, x_175);
lean_closure_set(x_178, 2, x_3);
lean_closure_set(x_178, 3, x_2);
lean_closure_set(x_178, 4, x_173);
lean_closure_set(x_178, 5, x_1);
lean_closure_set(x_178, 6, x_4);
lean_closure_set(x_178, 7, x_177);
x_179 = lp_REPL_REPL_ProofSnapshot_newMessages(x_3, x_4);
lean_dec(x_4);
lean_dec_ref(x_3);
x_180 = lean_box(0);
x_181 = l_List_mapM_loop___redArg(x_171, x_174, x_179, x_180);
x_182 = lean_apply_1(x_181, x_5);
x_183 = lean_apply_4(x_173, lean_box(0), lean_box(0), x_182, x_178);
return x_183;
}
}
else
{
lean_object* x_184; lean_object* x_185; lean_object* x_186; lean_object* x_187; lean_object* x_188; lean_object* x_189; lean_object* x_190; lean_object* x_191; lean_object* x_192; lean_object* x_193; lean_object* x_194; lean_object* x_195; lean_object* x_196; lean_object* x_197; lean_object* x_198; lean_object* x_199; lean_object* x_200; lean_object* x_201; lean_object* x_202; lean_object* x_203; lean_object* x_204; lean_object* x_205; lean_object* x_206; lean_object* x_207; lean_object* x_208; lean_object* x_209; lean_object* x_210; lean_object* x_211; lean_object* x_212; lean_object* x_213; lean_object* x_214; lean_object* x_215; lean_object* x_216; lean_object* x_217; lean_object* x_218; lean_object* x_219; lean_object* x_220; lean_object* x_221; lean_object* x_222; lean_object* x_223; lean_object* x_224; lean_object* x_225; lean_object* x_226; lean_object* x_227; lean_object* x_228; lean_object* x_229; lean_object* x_230; lean_object* x_231; lean_object* x_232; lean_object* x_233; lean_object* x_234; lean_object* x_235; lean_object* x_236; lean_object* x_237; lean_object* x_238; lean_object* x_239; lean_object* x_240; lean_object* x_241; lean_object* x_242; lean_object* x_243; 
x_184 = lean_ctor_get(x_8, 0);
x_185 = lean_ctor_get(x_8, 2);
x_186 = lean_ctor_get(x_8, 3);
x_187 = lean_ctor_get(x_8, 4);
lean_inc(x_187);
lean_inc(x_186);
lean_inc(x_185);
lean_inc(x_184);
lean_dec(x_8);
x_188 = lp_REPL_REPL_createProofStepReponse___redArg___closed__2;
x_189 = lp_REPL_REPL_createProofStepReponse___redArg___closed__3;
lean_inc_ref(x_184);
x_190 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_190, 0, x_184);
x_191 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_191, 0, x_184);
x_192 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_192, 0, x_190);
lean_ctor_set(x_192, 1, x_191);
x_193 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_193, 0, x_187);
x_194 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_194, 0, x_186);
x_195 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_195, 0, x_185);
x_196 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_196, 0, x_192);
lean_ctor_set(x_196, 1, x_188);
lean_ctor_set(x_196, 2, x_195);
lean_ctor_set(x_196, 3, x_194);
lean_ctor_set(x_196, 4, x_193);
lean_ctor_set(x_6, 1, x_189);
lean_ctor_set(x_6, 0, x_196);
x_197 = l_ReaderT_instMonad___redArg(x_6);
x_198 = lean_ctor_get(x_197, 0);
lean_inc_ref(x_198);
if (lean_is_exclusive(x_197)) {
 lean_ctor_release(x_197, 0);
 lean_ctor_release(x_197, 1);
 x_199 = x_197;
} else {
 lean_dec_ref(x_197);
 x_199 = lean_box(0);
}
x_200 = lean_ctor_get(x_198, 0);
lean_inc_ref(x_200);
x_201 = lean_ctor_get(x_198, 2);
lean_inc(x_201);
x_202 = lean_ctor_get(x_198, 3);
lean_inc(x_202);
x_203 = lean_ctor_get(x_198, 4);
lean_inc(x_203);
if (lean_is_exclusive(x_198)) {
 lean_ctor_release(x_198, 0);
 lean_ctor_release(x_198, 1);
 lean_ctor_release(x_198, 2);
 lean_ctor_release(x_198, 3);
 lean_ctor_release(x_198, 4);
 x_204 = x_198;
} else {
 lean_dec_ref(x_198);
 x_204 = lean_box(0);
}
x_205 = lp_REPL_REPL_createProofStepReponse___redArg___closed__4;
x_206 = lp_REPL_REPL_createProofStepReponse___redArg___closed__5;
lean_inc_ref(x_200);
x_207 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_207, 0, x_200);
x_208 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_208, 0, x_200);
x_209 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_209, 0, x_207);
lean_ctor_set(x_209, 1, x_208);
x_210 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_210, 0, x_203);
x_211 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_211, 0, x_202);
x_212 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_212, 0, x_201);
if (lean_is_scalar(x_204)) {
 x_213 = lean_alloc_ctor(0, 5, 0);
} else {
 x_213 = x_204;
}
lean_ctor_set(x_213, 0, x_209);
lean_ctor_set(x_213, 1, x_205);
lean_ctor_set(x_213, 2, x_212);
lean_ctor_set(x_213, 3, x_211);
lean_ctor_set(x_213, 4, x_210);
if (lean_is_scalar(x_199)) {
 x_214 = lean_alloc_ctor(0, 2, 0);
} else {
 x_214 = x_199;
}
lean_ctor_set(x_214, 0, x_213);
lean_ctor_set(x_214, 1, x_206);
x_215 = l_Lean_Meta_instMonadEnvMetaM;
x_216 = l_Lean_Meta_instMonadMCtxMetaM;
x_217 = lp_REPL_REPL_createProofStepReponse___redArg___closed__9;
x_218 = lp_REPL_REPL_createProofStepReponse___redArg___closed__11;
x_219 = lp_REPL_REPL_createProofStepReponse___redArg___closed__13;
x_220 = lean_ctor_get(x_219, 0);
lean_inc(x_220);
if (lean_is_exclusive(x_219)) {
 lean_ctor_release(x_219, 0);
 lean_ctor_release(x_219, 1);
 lean_ctor_release(x_219, 2);
 lean_ctor_release(x_219, 3);
 lean_ctor_release(x_219, 4);
 x_221 = x_219;
} else {
 lean_dec_ref(x_219);
 x_221 = lean_box(0);
}
lean_inc_ref(x_1);
x_222 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_222, 0, x_1);
lean_inc_ref(x_1);
x_223 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_223, 0, x_1);
lean_inc_ref(x_1);
x_224 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_224, 0, x_1);
lean_inc_ref(x_1);
x_225 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_225, 0, x_1);
lean_inc_ref(x_1);
x_226 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_226, 0, lean_box(0));
lean_closure_set(x_226, 1, lean_box(0));
lean_closure_set(x_226, 2, x_1);
x_227 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_227, 0, x_226);
lean_ctor_set(x_227, 1, x_222);
lean_inc_ref(x_1);
x_228 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_228, 0, lean_box(0));
lean_closure_set(x_228, 1, lean_box(0));
lean_closure_set(x_228, 2, x_1);
if (lean_is_scalar(x_221)) {
 x_229 = lean_alloc_ctor(0, 5, 0);
} else {
 x_229 = x_221;
}
lean_ctor_set(x_229, 0, x_227);
lean_ctor_set(x_229, 1, x_228);
lean_ctor_set(x_229, 2, x_223);
lean_ctor_set(x_229, 3, x_224);
lean_ctor_set(x_229, 4, x_225);
lean_inc_ref(x_1);
x_230 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_230, 0, lean_box(0));
lean_closure_set(x_230, 1, lean_box(0));
lean_closure_set(x_230, 2, x_1);
x_231 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_231, 0, x_229);
lean_ctor_set(x_231, 1, x_230);
x_232 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_232);
x_233 = lean_ctor_get(x_1, 1);
lean_inc(x_233);
lean_inc(x_233);
lean_inc(x_2);
lean_inc_ref(x_232);
x_234 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__1), 5, 3);
lean_closure_set(x_234, 0, x_232);
lean_closure_set(x_234, 1, x_2);
lean_closure_set(x_234, 2, x_233);
x_235 = lp_REPL_REPL_createProofStepReponse___redArg___closed__14;
x_236 = lp_REPL_REPL_createProofStepReponse___redArg___closed__17;
x_237 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed), 12, 7);
lean_closure_set(x_237, 0, x_214);
lean_closure_set(x_237, 1, x_215);
lean_closure_set(x_237, 2, x_216);
lean_closure_set(x_237, 3, x_236);
lean_closure_set(x_237, 4, x_217);
lean_closure_set(x_237, 5, x_218);
lean_closure_set(x_237, 6, x_220);
lean_inc(x_4);
lean_inc(x_233);
lean_inc_ref(x_3);
x_238 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__13), 9, 8);
lean_closure_set(x_238, 0, x_232);
lean_closure_set(x_238, 1, x_235);
lean_closure_set(x_238, 2, x_3);
lean_closure_set(x_238, 3, x_2);
lean_closure_set(x_238, 4, x_233);
lean_closure_set(x_238, 5, x_1);
lean_closure_set(x_238, 6, x_4);
lean_closure_set(x_238, 7, x_237);
x_239 = lp_REPL_REPL_ProofSnapshot_newMessages(x_3, x_4);
lean_dec(x_4);
lean_dec_ref(x_3);
x_240 = lean_box(0);
x_241 = l_List_mapM_loop___redArg(x_231, x_234, x_239, x_240);
x_242 = lean_apply_1(x_241, x_5);
x_243 = lean_apply_4(x_233, lean_box(0), lean_box(0), x_242, x_238);
return x_243;
}
}
else
{
lean_object* x_244; lean_object* x_245; lean_object* x_246; lean_object* x_247; lean_object* x_248; lean_object* x_249; lean_object* x_250; lean_object* x_251; lean_object* x_252; lean_object* x_253; lean_object* x_254; lean_object* x_255; lean_object* x_256; lean_object* x_257; lean_object* x_258; lean_object* x_259; lean_object* x_260; lean_object* x_261; lean_object* x_262; lean_object* x_263; lean_object* x_264; lean_object* x_265; lean_object* x_266; lean_object* x_267; lean_object* x_268; lean_object* x_269; lean_object* x_270; lean_object* x_271; lean_object* x_272; lean_object* x_273; lean_object* x_274; lean_object* x_275; lean_object* x_276; lean_object* x_277; lean_object* x_278; lean_object* x_279; lean_object* x_280; lean_object* x_281; lean_object* x_282; lean_object* x_283; lean_object* x_284; lean_object* x_285; lean_object* x_286; lean_object* x_287; lean_object* x_288; lean_object* x_289; lean_object* x_290; lean_object* x_291; lean_object* x_292; lean_object* x_293; lean_object* x_294; lean_object* x_295; lean_object* x_296; lean_object* x_297; lean_object* x_298; lean_object* x_299; lean_object* x_300; lean_object* x_301; lean_object* x_302; lean_object* x_303; lean_object* x_304; lean_object* x_305; lean_object* x_306; 
x_244 = lean_ctor_get(x_6, 0);
lean_inc(x_244);
lean_dec(x_6);
x_245 = lean_ctor_get(x_244, 0);
lean_inc_ref(x_245);
x_246 = lean_ctor_get(x_244, 2);
lean_inc(x_246);
x_247 = lean_ctor_get(x_244, 3);
lean_inc(x_247);
x_248 = lean_ctor_get(x_244, 4);
lean_inc(x_248);
if (lean_is_exclusive(x_244)) {
 lean_ctor_release(x_244, 0);
 lean_ctor_release(x_244, 1);
 lean_ctor_release(x_244, 2);
 lean_ctor_release(x_244, 3);
 lean_ctor_release(x_244, 4);
 x_249 = x_244;
} else {
 lean_dec_ref(x_244);
 x_249 = lean_box(0);
}
x_250 = lp_REPL_REPL_createProofStepReponse___redArg___closed__2;
x_251 = lp_REPL_REPL_createProofStepReponse___redArg___closed__3;
lean_inc_ref(x_245);
x_252 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_252, 0, x_245);
x_253 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_253, 0, x_245);
x_254 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_254, 0, x_252);
lean_ctor_set(x_254, 1, x_253);
x_255 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_255, 0, x_248);
x_256 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_256, 0, x_247);
x_257 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_257, 0, x_246);
if (lean_is_scalar(x_249)) {
 x_258 = lean_alloc_ctor(0, 5, 0);
} else {
 x_258 = x_249;
}
lean_ctor_set(x_258, 0, x_254);
lean_ctor_set(x_258, 1, x_250);
lean_ctor_set(x_258, 2, x_257);
lean_ctor_set(x_258, 3, x_256);
lean_ctor_set(x_258, 4, x_255);
x_259 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_259, 0, x_258);
lean_ctor_set(x_259, 1, x_251);
x_260 = l_ReaderT_instMonad___redArg(x_259);
x_261 = lean_ctor_get(x_260, 0);
lean_inc_ref(x_261);
if (lean_is_exclusive(x_260)) {
 lean_ctor_release(x_260, 0);
 lean_ctor_release(x_260, 1);
 x_262 = x_260;
} else {
 lean_dec_ref(x_260);
 x_262 = lean_box(0);
}
x_263 = lean_ctor_get(x_261, 0);
lean_inc_ref(x_263);
x_264 = lean_ctor_get(x_261, 2);
lean_inc(x_264);
x_265 = lean_ctor_get(x_261, 3);
lean_inc(x_265);
x_266 = lean_ctor_get(x_261, 4);
lean_inc(x_266);
if (lean_is_exclusive(x_261)) {
 lean_ctor_release(x_261, 0);
 lean_ctor_release(x_261, 1);
 lean_ctor_release(x_261, 2);
 lean_ctor_release(x_261, 3);
 lean_ctor_release(x_261, 4);
 x_267 = x_261;
} else {
 lean_dec_ref(x_261);
 x_267 = lean_box(0);
}
x_268 = lp_REPL_REPL_createProofStepReponse___redArg___closed__4;
x_269 = lp_REPL_REPL_createProofStepReponse___redArg___closed__5;
lean_inc_ref(x_263);
x_270 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__0), 6, 1);
lean_closure_set(x_270, 0, x_263);
x_271 = lean_alloc_closure((void*)(l_ReaderT_instFunctorOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_271, 0, x_263);
x_272 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_272, 0, x_270);
lean_ctor_set(x_272, 1, x_271);
x_273 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_273, 0, x_266);
x_274 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__3), 6, 1);
lean_closure_set(x_274, 0, x_265);
x_275 = lean_alloc_closure((void*)(l_ReaderT_instApplicativeOfMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_275, 0, x_264);
if (lean_is_scalar(x_267)) {
 x_276 = lean_alloc_ctor(0, 5, 0);
} else {
 x_276 = x_267;
}
lean_ctor_set(x_276, 0, x_272);
lean_ctor_set(x_276, 1, x_268);
lean_ctor_set(x_276, 2, x_275);
lean_ctor_set(x_276, 3, x_274);
lean_ctor_set(x_276, 4, x_273);
if (lean_is_scalar(x_262)) {
 x_277 = lean_alloc_ctor(0, 2, 0);
} else {
 x_277 = x_262;
}
lean_ctor_set(x_277, 0, x_276);
lean_ctor_set(x_277, 1, x_269);
x_278 = l_Lean_Meta_instMonadEnvMetaM;
x_279 = l_Lean_Meta_instMonadMCtxMetaM;
x_280 = lp_REPL_REPL_createProofStepReponse___redArg___closed__9;
x_281 = lp_REPL_REPL_createProofStepReponse___redArg___closed__11;
x_282 = lp_REPL_REPL_createProofStepReponse___redArg___closed__13;
x_283 = lean_ctor_get(x_282, 0);
lean_inc(x_283);
if (lean_is_exclusive(x_282)) {
 lean_ctor_release(x_282, 0);
 lean_ctor_release(x_282, 1);
 lean_ctor_release(x_282, 2);
 lean_ctor_release(x_282, 3);
 lean_ctor_release(x_282, 4);
 x_284 = x_282;
} else {
 lean_dec_ref(x_282);
 x_284 = lean_box(0);
}
lean_inc_ref(x_1);
x_285 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_285, 0, x_1);
lean_inc_ref(x_1);
x_286 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_286, 0, x_1);
lean_inc_ref(x_1);
x_287 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_287, 0, x_1);
lean_inc_ref(x_1);
x_288 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_288, 0, x_1);
lean_inc_ref(x_1);
x_289 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_289, 0, lean_box(0));
lean_closure_set(x_289, 1, lean_box(0));
lean_closure_set(x_289, 2, x_1);
x_290 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_290, 0, x_289);
lean_ctor_set(x_290, 1, x_285);
lean_inc_ref(x_1);
x_291 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_291, 0, lean_box(0));
lean_closure_set(x_291, 1, lean_box(0));
lean_closure_set(x_291, 2, x_1);
if (lean_is_scalar(x_284)) {
 x_292 = lean_alloc_ctor(0, 5, 0);
} else {
 x_292 = x_284;
}
lean_ctor_set(x_292, 0, x_290);
lean_ctor_set(x_292, 1, x_291);
lean_ctor_set(x_292, 2, x_286);
lean_ctor_set(x_292, 3, x_287);
lean_ctor_set(x_292, 4, x_288);
lean_inc_ref(x_1);
x_293 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_293, 0, lean_box(0));
lean_closure_set(x_293, 1, lean_box(0));
lean_closure_set(x_293, 2, x_1);
x_294 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_294, 0, x_292);
lean_ctor_set(x_294, 1, x_293);
x_295 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_295);
x_296 = lean_ctor_get(x_1, 1);
lean_inc(x_296);
lean_inc(x_296);
lean_inc(x_2);
lean_inc_ref(x_295);
x_297 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__1), 5, 3);
lean_closure_set(x_297, 0, x_295);
lean_closure_set(x_297, 1, x_2);
lean_closure_set(x_297, 2, x_296);
x_298 = lp_REPL_REPL_createProofStepReponse___redArg___closed__14;
x_299 = lp_REPL_REPL_createProofStepReponse___redArg___closed__17;
x_300 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__3___boxed), 12, 7);
lean_closure_set(x_300, 0, x_277);
lean_closure_set(x_300, 1, x_278);
lean_closure_set(x_300, 2, x_279);
lean_closure_set(x_300, 3, x_299);
lean_closure_set(x_300, 4, x_280);
lean_closure_set(x_300, 5, x_281);
lean_closure_set(x_300, 6, x_283);
lean_inc(x_4);
lean_inc(x_296);
lean_inc_ref(x_3);
x_301 = lean_alloc_closure((void*)(lp_REPL_REPL_createProofStepReponse___redArg___lam__13), 9, 8);
lean_closure_set(x_301, 0, x_295);
lean_closure_set(x_301, 1, x_298);
lean_closure_set(x_301, 2, x_3);
lean_closure_set(x_301, 3, x_2);
lean_closure_set(x_301, 4, x_296);
lean_closure_set(x_301, 5, x_1);
lean_closure_set(x_301, 6, x_4);
lean_closure_set(x_301, 7, x_300);
x_302 = lp_REPL_REPL_ProofSnapshot_newMessages(x_3, x_4);
lean_dec(x_4);
lean_dec_ref(x_3);
x_303 = lean_box(0);
x_304 = l_List_mapM_loop___redArg(x_294, x_297, x_302, x_303);
x_305 = lean_apply_1(x_304, x_5);
x_306 = lean_apply_4(x_296, lean_box(0), lean_box(0), x_305, x_301);
return x_306;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
lean_object* x_7; 
x_7 = lp_REPL_REPL_createProofStepReponse___redArg(x_2, x_3, x_4, x_5, x_6);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_3);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; 
x_5 = lean_ctor_get(x_3, 0);
lean_dec(x_5);
x_6 = lean_ctor_get(x_1, 0);
lean_inc(x_6);
x_7 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_7, 0, x_6);
x_8 = lean_box(0);
x_9 = lean_box(0);
x_10 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_10, 0, x_7);
lean_ctor_set(x_10, 1, x_8);
lean_ctor_set(x_10, 2, x_8);
lean_ctor_set(x_10, 3, x_8);
lean_ctor_set(x_10, 4, x_9);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_10);
lean_ctor_set(x_3, 0, x_11);
x_12 = lean_apply_2(x_2, lean_box(0), x_3);
return x_12;
}
else
{
lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; 
x_13 = lean_ctor_get(x_3, 1);
lean_inc(x_13);
lean_dec(x_3);
x_14 = lean_ctor_get(x_1, 0);
lean_inc(x_14);
x_15 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_15, 0, x_14);
x_16 = lean_box(0);
x_17 = lean_box(0);
x_18 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_18, 0, x_15);
lean_ctor_set(x_18, 1, x_16);
lean_ctor_set(x_18, 2, x_16);
lean_ctor_set(x_18, 3, x_16);
lean_ctor_set(x_18, 4, x_17);
x_19 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_19, 0, x_18);
x_20 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_20, 0, x_19);
lean_ctor_set(x_20, 1, x_13);
x_21 = lean_apply_2(x_2, lean_box(0), x_20);
return x_21;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__0(x_1, x_2, x_3);
lean_dec_ref(x_1);
return x_4;
}
}
static lean_object* _init_lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("Unknown environment.", 20, 20);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0;
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__1(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_3);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; 
x_5 = lean_ctor_get(x_3, 0);
lean_dec(x_5);
lean_ctor_set(x_3, 0, x_1);
x_6 = lean_apply_2(x_2, lean_box(0), x_3);
return x_6;
}
else
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_7 = lean_ctor_get(x_3, 1);
lean_inc(x_7);
lean_dec(x_3);
x_8 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_8, 0, x_1);
lean_ctor_set(x_8, 1, x_7);
x_9 = lean_apply_2(x_2, lean_box(0), x_8);
return x_9;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__2(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; lean_object* x_5; 
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_3);
lean_ctor_set(x_4, 1, x_1);
x_5 = lean_apply_2(x_2, lean_box(0), x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
uint8_t x_7; 
x_7 = !lean_is_exclusive(x_6);
if (x_7 == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; uint8_t x_14; 
x_8 = lean_ctor_get(x_6, 0);
x_9 = lean_ctor_get(x_6, 1);
x_10 = lean_ctor_get(x_8, 0);
lean_inc_ref(x_10);
lean_dec(x_8);
x_11 = lean_ctor_get(x_1, 0);
lean_inc(x_11);
x_12 = lean_ctor_get(x_1, 1);
lean_inc_ref(x_12);
lean_dec_ref(x_1);
x_13 = lean_array_get_size(x_10);
x_14 = lean_nat_dec_lt(x_11, x_13);
if (x_14 == 0)
{
lean_object* x_15; lean_object* x_16; 
lean_dec_ref(x_12);
lean_dec(x_11);
lean_dec_ref(x_10);
lean_dec(x_5);
lean_dec(x_4);
lean_dec(x_3);
x_15 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
lean_ctor_set(x_6, 0, x_15);
x_16 = lean_apply_2(x_2, lean_box(0), x_6);
return x_16;
}
else
{
lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; 
lean_free_object(x_6);
x_17 = lean_array_fget(x_10, x_11);
lean_dec(x_11);
lean_dec_ref(x_10);
x_18 = lean_alloc_closure((void*)(lp_REPL_REPL_CommandSnapshot_pickle___boxed), 3, 2);
lean_closure_set(x_18, 0, x_17);
lean_closure_set(x_18, 1, x_12);
x_19 = lean_apply_2(x_3, lean_box(0), x_18);
x_20 = lean_box(0);
lean_inc(x_2);
x_21 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__1), 3, 2);
lean_closure_set(x_21, 0, x_20);
lean_closure_set(x_21, 1, x_2);
x_22 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__2), 3, 2);
lean_closure_set(x_22, 0, x_9);
lean_closure_set(x_22, 1, x_2);
lean_inc(x_4);
x_23 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_19, x_22);
lean_inc(x_4);
x_24 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_23, x_21);
x_25 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_24, x_5);
return x_25;
}
}
else
{
lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; uint8_t x_32; 
x_26 = lean_ctor_get(x_6, 0);
x_27 = lean_ctor_get(x_6, 1);
lean_inc(x_27);
lean_inc(x_26);
lean_dec(x_6);
x_28 = lean_ctor_get(x_26, 0);
lean_inc_ref(x_28);
lean_dec(x_26);
x_29 = lean_ctor_get(x_1, 0);
lean_inc(x_29);
x_30 = lean_ctor_get(x_1, 1);
lean_inc_ref(x_30);
lean_dec_ref(x_1);
x_31 = lean_array_get_size(x_28);
x_32 = lean_nat_dec_lt(x_29, x_31);
if (x_32 == 0)
{
lean_object* x_33; lean_object* x_34; lean_object* x_35; 
lean_dec_ref(x_30);
lean_dec(x_29);
lean_dec_ref(x_28);
lean_dec(x_5);
lean_dec(x_4);
lean_dec(x_3);
x_33 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
x_34 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_34, 0, x_33);
lean_ctor_set(x_34, 1, x_27);
x_35 = lean_apply_2(x_2, lean_box(0), x_34);
return x_35;
}
else
{
lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; 
x_36 = lean_array_fget(x_28, x_29);
lean_dec(x_29);
lean_dec_ref(x_28);
x_37 = lean_alloc_closure((void*)(lp_REPL_REPL_CommandSnapshot_pickle___boxed), 3, 2);
lean_closure_set(x_37, 0, x_36);
lean_closure_set(x_37, 1, x_30);
x_38 = lean_apply_2(x_3, lean_box(0), x_37);
x_39 = lean_box(0);
lean_inc(x_2);
x_40 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__1), 3, 2);
lean_closure_set(x_40, 0, x_39);
lean_closure_set(x_40, 1, x_2);
x_41 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__2), 3, 2);
lean_closure_set(x_41, 0, x_27);
lean_closure_set(x_41, 1, x_2);
lean_inc(x_4);
x_42 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_38, x_41);
lean_inc(x_4);
x_43 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_42, x_40);
x_44 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_43, x_5);
return x_44;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
uint8_t x_5; 
x_5 = !lean_is_exclusive(x_1);
if (x_5 == 0)
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; 
x_6 = lean_ctor_get(x_1, 0);
x_7 = lean_ctor_get(x_1, 1);
x_8 = lean_ctor_get(x_6, 1);
lean_inc(x_8);
lean_dec_ref(x_6);
lean_inc(x_8);
lean_inc_ref(x_3);
x_9 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__0___boxed), 3, 2);
lean_closure_set(x_9, 0, x_3);
lean_closure_set(x_9, 1, x_8);
lean_inc(x_7);
lean_inc(x_8);
x_10 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3), 6, 5);
lean_closure_set(x_10, 0, x_3);
lean_closure_set(x_10, 1, x_8);
lean_closure_set(x_10, 2, x_2);
lean_closure_set(x_10, 3, x_7);
lean_closure_set(x_10, 4, x_9);
lean_inc_ref(x_4);
lean_ctor_set(x_1, 1, x_4);
lean_ctor_set(x_1, 0, x_4);
x_11 = lean_apply_2(x_8, lean_box(0), x_1);
x_12 = lean_apply_4(x_7, lean_box(0), lean_box(0), x_11, x_10);
return x_12;
}
else
{
lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; 
x_13 = lean_ctor_get(x_1, 0);
x_14 = lean_ctor_get(x_1, 1);
lean_inc(x_14);
lean_inc(x_13);
lean_dec(x_1);
x_15 = lean_ctor_get(x_13, 1);
lean_inc(x_15);
lean_dec_ref(x_13);
lean_inc(x_15);
lean_inc_ref(x_3);
x_16 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__0___boxed), 3, 2);
lean_closure_set(x_16, 0, x_3);
lean_closure_set(x_16, 1, x_15);
lean_inc(x_14);
lean_inc(x_15);
x_17 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3), 6, 5);
lean_closure_set(x_17, 0, x_3);
lean_closure_set(x_17, 1, x_15);
lean_closure_set(x_17, 2, x_2);
lean_closure_set(x_17, 3, x_14);
lean_closure_set(x_17, 4, x_16);
lean_inc_ref(x_4);
x_18 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_18, 0, x_4);
lean_ctor_set(x_18, 1, x_4);
x_19 = lean_apply_2(x_15, lean_box(0), x_18);
x_20 = lean_apply_4(x_14, lean_box(0), lean_box(0), x_19, x_17);
return x_20;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_REPL_pickleCommandSnapshot___redArg(x_2, x_3, x_4, x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___at___00REPL_unpickleCommandSnapshot_spec__0(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_2);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_5 = lean_ctor_get(x_2, 0);
x_6 = lean_array_get_size(x_5);
x_7 = lean_array_push(x_5, x_1);
lean_ctor_set(x_2, 0, x_7);
x_8 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_8, 0, x_6);
lean_ctor_set(x_8, 1, x_2);
x_9 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_9, 0, x_8);
return x_9;
}
else
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_10 = lean_ctor_get(x_2, 0);
x_11 = lean_ctor_get(x_2, 1);
lean_inc(x_11);
lean_inc(x_10);
lean_dec(x_2);
x_12 = lean_array_get_size(x_10);
x_13 = lean_array_push(x_10, x_1);
x_14 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_14, 0, x_13);
lean_ctor_set(x_14, 1, x_11);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_12);
lean_ctor_set(x_15, 1, x_14);
x_16 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_16, 0, x_15);
return x_16;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleCommandSnapshot(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_CommandSnapshot_unpickle_unsafe__8(x_1);
if (lean_obj_tag(x_4) == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; uint8_t x_8; 
x_5 = lean_ctor_get(x_4, 0);
lean_inc(x_5);
lean_dec_ref(x_4);
x_6 = lean_ctor_get(x_5, 0);
lean_inc(x_6);
lean_dec(x_5);
x_7 = lp_REPL_REPL_recordCommandSnapshot___at___00REPL_unpickleCommandSnapshot_spec__0(x_6, x_2);
x_8 = !lean_is_exclusive(x_7);
if (x_8 == 0)
{
lean_object* x_9; uint8_t x_10; 
x_9 = lean_ctor_get(x_7, 0);
x_10 = !lean_is_exclusive(x_9);
if (x_10 == 0)
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; 
x_11 = lean_ctor_get(x_9, 0);
x_12 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_12, 0, x_11);
x_13 = lean_box(0);
x_14 = lean_box(0);
x_15 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_15, 0, x_12);
lean_ctor_set(x_15, 1, x_13);
lean_ctor_set(x_15, 2, x_13);
lean_ctor_set(x_15, 3, x_13);
lean_ctor_set(x_15, 4, x_14);
lean_ctor_set(x_9, 0, x_15);
return x_7;
}
else
{
lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; 
x_16 = lean_ctor_get(x_9, 0);
x_17 = lean_ctor_get(x_9, 1);
lean_inc(x_17);
lean_inc(x_16);
lean_dec(x_9);
x_18 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_18, 0, x_16);
x_19 = lean_box(0);
x_20 = lean_box(0);
x_21 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_21, 0, x_18);
lean_ctor_set(x_21, 1, x_19);
lean_ctor_set(x_21, 2, x_19);
lean_ctor_set(x_21, 3, x_19);
lean_ctor_set(x_21, 4, x_20);
x_22 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_22, 0, x_21);
lean_ctor_set(x_22, 1, x_17);
lean_ctor_set(x_7, 0, x_22);
return x_7;
}
}
else
{
lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; 
x_23 = lean_ctor_get(x_7, 0);
lean_inc(x_23);
lean_dec(x_7);
x_24 = lean_ctor_get(x_23, 0);
lean_inc(x_24);
x_25 = lean_ctor_get(x_23, 1);
lean_inc(x_25);
if (lean_is_exclusive(x_23)) {
 lean_ctor_release(x_23, 0);
 lean_ctor_release(x_23, 1);
 x_26 = x_23;
} else {
 lean_dec_ref(x_23);
 x_26 = lean_box(0);
}
x_27 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_27, 0, x_24);
x_28 = lean_box(0);
x_29 = lean_box(0);
x_30 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_30, 0, x_27);
lean_ctor_set(x_30, 1, x_28);
lean_ctor_set(x_30, 2, x_28);
lean_ctor_set(x_30, 3, x_28);
lean_ctor_set(x_30, 4, x_29);
if (lean_is_scalar(x_26)) {
 x_31 = lean_alloc_ctor(0, 2, 0);
} else {
 x_31 = x_26;
}
lean_ctor_set(x_31, 0, x_30);
lean_ctor_set(x_31, 1, x_25);
x_32 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_32, 0, x_31);
return x_32;
}
}
else
{
uint8_t x_33; 
lean_dec_ref(x_2);
x_33 = !lean_is_exclusive(x_4);
if (x_33 == 0)
{
return x_4;
}
else
{
lean_object* x_34; lean_object* x_35; 
x_34 = lean_ctor_get(x_4, 0);
lean_inc(x_34);
lean_dec(x_4);
x_35 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_35, 0, x_34);
return x_35;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordCommandSnapshot___at___00REPL_unpickleCommandSnapshot_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_recordCommandSnapshot___at___00REPL_unpickleCommandSnapshot_spec__0(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleCommandSnapshot___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_unpickleCommandSnapshot(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__0(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_3; 
x_3 = !lean_is_exclusive(x_2);
if (x_3 == 0)
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_4 = lean_ctor_get(x_2, 0);
x_5 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_5, 0, x_4);
lean_ctor_set(x_2, 0, x_5);
x_6 = lean_apply_2(x_1, lean_box(0), x_2);
return x_6;
}
else
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_7 = lean_ctor_get(x_2, 0);
x_8 = lean_ctor_get(x_2, 1);
lean_inc(x_8);
lean_inc(x_7);
lean_dec(x_2);
x_9 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_9, 0, x_7);
x_10 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_10, 0, x_9);
lean_ctor_set(x_10, 1, x_8);
x_11 = lean_apply_2(x_1, lean_box(0), x_10);
return x_11;
}
}
}
static lean_object* _init_lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("Unknown proof State.", 20, 20);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__0;
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__1(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_7 = lean_ctor_get(x_6, 1);
lean_inc(x_7);
lean_dec_ref(x_6);
x_8 = lean_box(0);
x_9 = lp_REPL_REPL_createProofStepReponse___redArg(x_1, x_2, x_3, x_8, x_7);
x_10 = lean_apply_4(x_4, lean_box(0), lean_box(0), x_9, x_5);
return x_10;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7) {
_start:
{
uint8_t x_8; 
x_8 = !lean_is_exclusive(x_7);
if (x_8 == 0)
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; uint8_t x_15; 
x_9 = lean_ctor_get(x_7, 0);
x_10 = lean_ctor_get(x_7, 1);
x_11 = lean_ctor_get(x_9, 1);
lean_inc_ref(x_11);
lean_dec(x_9);
x_12 = lean_ctor_get(x_1, 0);
lean_inc(x_12);
x_13 = lean_ctor_get(x_1, 1);
lean_inc_ref(x_13);
lean_dec_ref(x_1);
x_14 = lean_array_get_size(x_11);
x_15 = lean_nat_dec_lt(x_12, x_14);
if (x_15 == 0)
{
lean_object* x_16; lean_object* x_17; 
lean_dec_ref(x_13);
lean_dec(x_12);
lean_dec_ref(x_11);
lean_dec(x_6);
lean_dec(x_5);
lean_dec(x_4);
lean_dec_ref(x_3);
x_16 = lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1;
lean_ctor_set(x_7, 0, x_16);
x_17 = lean_apply_2(x_2, lean_box(0), x_7);
return x_17;
}
else
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; 
lean_free_object(x_7);
x_18 = lean_array_fget(x_11, x_12);
lean_dec(x_12);
lean_dec_ref(x_11);
lean_inc(x_5);
lean_inc(x_18);
lean_inc(x_4);
x_19 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleProofSnapshot___redArg___lam__1), 6, 5);
lean_closure_set(x_19, 0, x_3);
lean_closure_set(x_19, 1, x_4);
lean_closure_set(x_19, 2, x_18);
lean_closure_set(x_19, 3, x_5);
lean_closure_set(x_19, 4, x_6);
x_20 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_pickle___boxed), 3, 2);
lean_closure_set(x_20, 0, x_18);
lean_closure_set(x_20, 1, x_13);
x_21 = lean_apply_2(x_4, lean_box(0), x_20);
x_22 = lean_box(0);
lean_inc(x_2);
x_23 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__1), 3, 2);
lean_closure_set(x_23, 0, x_22);
lean_closure_set(x_23, 1, x_2);
x_24 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__2), 3, 2);
lean_closure_set(x_24, 0, x_10);
lean_closure_set(x_24, 1, x_2);
lean_inc(x_5);
x_25 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_21, x_24);
lean_inc(x_5);
x_26 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_25, x_23);
x_27 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_26, x_19);
return x_27;
}
}
else
{
lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; uint8_t x_34; 
x_28 = lean_ctor_get(x_7, 0);
x_29 = lean_ctor_get(x_7, 1);
lean_inc(x_29);
lean_inc(x_28);
lean_dec(x_7);
x_30 = lean_ctor_get(x_28, 1);
lean_inc_ref(x_30);
lean_dec(x_28);
x_31 = lean_ctor_get(x_1, 0);
lean_inc(x_31);
x_32 = lean_ctor_get(x_1, 1);
lean_inc_ref(x_32);
lean_dec_ref(x_1);
x_33 = lean_array_get_size(x_30);
x_34 = lean_nat_dec_lt(x_31, x_33);
if (x_34 == 0)
{
lean_object* x_35; lean_object* x_36; lean_object* x_37; 
lean_dec_ref(x_32);
lean_dec(x_31);
lean_dec_ref(x_30);
lean_dec(x_6);
lean_dec(x_5);
lean_dec(x_4);
lean_dec_ref(x_3);
x_35 = lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1;
x_36 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_36, 0, x_35);
lean_ctor_set(x_36, 1, x_29);
x_37 = lean_apply_2(x_2, lean_box(0), x_36);
return x_37;
}
else
{
lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; lean_object* x_47; 
x_38 = lean_array_fget(x_30, x_31);
lean_dec(x_31);
lean_dec_ref(x_30);
lean_inc(x_5);
lean_inc(x_38);
lean_inc(x_4);
x_39 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleProofSnapshot___redArg___lam__1), 6, 5);
lean_closure_set(x_39, 0, x_3);
lean_closure_set(x_39, 1, x_4);
lean_closure_set(x_39, 2, x_38);
lean_closure_set(x_39, 3, x_5);
lean_closure_set(x_39, 4, x_6);
x_40 = lean_alloc_closure((void*)(lp_REPL_REPL_ProofSnapshot_pickle___boxed), 3, 2);
lean_closure_set(x_40, 0, x_38);
lean_closure_set(x_40, 1, x_32);
x_41 = lean_apply_2(x_4, lean_box(0), x_40);
x_42 = lean_box(0);
lean_inc(x_2);
x_43 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__1), 3, 2);
lean_closure_set(x_43, 0, x_42);
lean_closure_set(x_43, 1, x_2);
x_44 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__2), 3, 2);
lean_closure_set(x_44, 0, x_29);
lean_closure_set(x_44, 1, x_2);
lean_inc(x_5);
x_45 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_41, x_44);
lean_inc(x_5);
x_46 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_45, x_43);
x_47 = lean_apply_4(x_5, lean_box(0), lean_box(0), x_46, x_39);
return x_47;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; 
x_5 = lean_ctor_get(x_1, 0);
x_6 = lean_ctor_get(x_1, 1);
lean_inc(x_6);
x_7 = lean_ctor_get(x_5, 1);
lean_inc(x_7);
lean_inc(x_7);
x_8 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleProofSnapshot___redArg___lam__0), 2, 1);
lean_closure_set(x_8, 0, x_7);
lean_inc(x_6);
lean_inc(x_7);
x_9 = lean_alloc_closure((void*)(lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4), 7, 6);
lean_closure_set(x_9, 0, x_3);
lean_closure_set(x_9, 1, x_7);
lean_closure_set(x_9, 2, x_1);
lean_closure_set(x_9, 3, x_2);
lean_closure_set(x_9, 4, x_6);
lean_closure_set(x_9, 5, x_8);
lean_inc_ref(x_4);
x_10 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_10, 0, x_4);
lean_ctor_set(x_10, 1, x_4);
x_11 = lean_apply_2(x_7, lean_box(0), x_10);
x_12 = lean_apply_4(x_6, lean_box(0), lean_box(0), x_11, x_9);
return x_12;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_REPL_pickleProofSnapshot___redArg(x_2, x_3, x_4, x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_2);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_5 = lean_ctor_get(x_2, 1);
x_6 = lean_array_get_size(x_5);
x_7 = lean_array_push(x_5, x_1);
lean_ctor_set(x_2, 1, x_7);
x_8 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_8, 0, x_6);
lean_ctor_set(x_8, 1, x_2);
x_9 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_9, 0, x_8);
return x_9;
}
else
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_10 = lean_ctor_get(x_2, 0);
x_11 = lean_ctor_get(x_2, 1);
lean_inc(x_11);
lean_inc(x_10);
lean_dec(x_2);
x_12 = lean_array_get_size(x_11);
x_13 = lean_array_push(x_11, x_1);
x_14 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_14, 0, x_10);
lean_ctor_set(x_14, 1, x_13);
x_15 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_15, 0, x_12);
lean_ctor_set(x_15, 1, x_14);
x_16 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_16, 0, x_15);
return x_16;
}
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__1), 6, 1);
lean_closure_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__4), 6, 1);
lean_closure_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__7), 6, 1);
lean_closure_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = lean_alloc_closure((void*)(l_StateT_instMonad___redArg___lam__9), 6, 1);
lean_closure_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__4() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = lean_alloc_closure((void*)(l_StateT_map), 8, 3);
lean_closure_set(x_2, 0, lean_box(0));
lean_closure_set(x_2, 1, lean_box(0));
lean_closure_set(x_2, 2, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__5() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = lean_alloc_closure((void*)(l_StateT_pure), 6, 3);
lean_closure_set(x_2, 0, lean_box(0));
lean_closure_set(x_2, 1, lean_box(0));
lean_closure_set(x_2, 2, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__6() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_createProofStepReponse___redArg___closed__0;
x_2 = lean_alloc_closure((void*)(l_StateT_bind), 8, 3);
lean_closure_set(x_2, 0, lean_box(0));
lean_closure_set(x_2, 1, lean_box(0));
lean_closure_set(x_2, 2, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_4 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__0;
x_5 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__1;
x_6 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__2;
x_7 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__3;
x_8 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__4;
x_9 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_9, 0, x_8);
lean_ctor_set(x_9, 1, x_4);
x_10 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__5;
x_11 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_11, 0, x_9);
lean_ctor_set(x_11, 1, x_10);
lean_ctor_set(x_11, 2, x_5);
lean_ctor_set(x_11, 3, x_6);
lean_ctor_set(x_11, 4, x_7);
x_12 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__6;
x_13 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_13, 0, x_11);
lean_ctor_set(x_13, 1, x_12);
x_14 = lp_REPL_REPL_sorries___redArg___closed__1;
x_15 = l_instInhabitedOfMonad___redArg(x_13, x_14);
x_16 = lean_panic_fn(x_15, x_1);
x_17 = lean_apply_2(x_16, x_2, lean_box(0));
return x_17;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__3(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; 
lean_dec(x_1);
x_6 = l_List_reverse___redArg(x_3);
x_7 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_7, 0, x_6);
lean_ctor_set(x_7, 1, x_4);
x_8 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_8, 0, x_7);
return x_8;
}
else
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; uint8_t x_22; 
x_9 = lean_ctor_get(x_2, 0);
lean_inc(x_9);
x_10 = lean_ctor_get(x_2, 1);
lean_inc(x_10);
if (lean_is_exclusive(x_2)) {
 lean_ctor_release(x_2, 0);
 lean_ctor_release(x_2, 1);
 x_11 = x_2;
} else {
 lean_dec_ref(x_2);
 x_11 = lean_box(0);
}
x_18 = lean_ctor_get(x_9, 1);
lean_inc(x_18);
x_19 = lean_ctor_get(x_18, 1);
lean_inc(x_19);
x_20 = lean_ctor_get(x_9, 0);
lean_inc(x_20);
lean_dec(x_9);
x_21 = lean_ctor_get(x_18, 0);
lean_inc(x_21);
lean_dec(x_18);
x_22 = !lean_is_exclusive(x_19);
if (x_22 == 0)
{
lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; 
x_23 = lean_ctor_get(x_19, 0);
x_24 = lean_ctor_get(x_19, 1);
if (lean_obj_tag(x_21) == 0)
{
lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; 
x_41 = lean_ctor_get(x_21, 0);
lean_inc(x_41);
lean_dec_ref(x_21);
x_42 = lean_box(0);
x_43 = lean_box(0);
lean_ctor_set_tag(x_19, 1);
lean_ctor_set(x_19, 1, x_43);
lean_ctor_set(x_19, 0, x_41);
lean_inc(x_1);
x_44 = lp_REPL_REPL_ProofSnapshot_create(x_20, x_42, x_1, x_19, x_43);
if (lean_obj_tag(x_44) == 0)
{
lean_object* x_45; lean_object* x_46; 
x_45 = lean_ctor_get(x_44, 0);
lean_inc(x_45);
lean_dec_ref(x_44);
lean_inc(x_45);
x_46 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_45);
if (lean_obj_tag(x_46) == 0)
{
lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; 
x_47 = lean_ctor_get(x_46, 0);
lean_inc(x_47);
lean_dec_ref(x_46);
x_48 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_49 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_47, x_43);
x_50 = l_String_intercalate(x_48, x_49);
x_25 = x_50;
x_26 = x_45;
x_27 = x_4;
x_28 = lean_box(0);
goto block_40;
}
else
{
uint8_t x_51; 
lean_dec(x_45);
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_51 = !lean_is_exclusive(x_46);
if (x_51 == 0)
{
return x_46;
}
else
{
lean_object* x_52; lean_object* x_53; 
x_52 = lean_ctor_get(x_46, 0);
lean_inc(x_52);
lean_dec(x_46);
x_53 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_53, 0, x_52);
return x_53;
}
}
}
else
{
uint8_t x_54; 
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_54 = !lean_is_exclusive(x_44);
if (x_54 == 0)
{
return x_44;
}
else
{
lean_object* x_55; lean_object* x_56; 
x_55 = lean_ctor_get(x_44, 0);
lean_inc(x_55);
lean_dec(x_44);
x_56 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_56, 0, x_55);
return x_56;
}
}
}
else
{
lean_object* x_57; 
lean_free_object(x_19);
x_57 = lean_ctor_get(x_21, 1);
lean_inc(x_57);
if (lean_obj_tag(x_57) == 0)
{
lean_object* x_58; lean_object* x_59; 
lean_dec_ref(x_21);
lean_dec(x_20);
x_58 = lp_REPL_REPL_sorries___redArg___lam__16___closed__3;
x_59 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2(x_58, x_4);
if (lean_obj_tag(x_59) == 0)
{
lean_object* x_60; lean_object* x_61; lean_object* x_62; 
x_60 = lean_ctor_get(x_59, 0);
lean_inc(x_60);
lean_dec_ref(x_59);
x_61 = lean_ctor_get(x_60, 0);
lean_inc(x_61);
x_62 = lean_ctor_get(x_61, 1);
if (lean_obj_tag(x_62) == 0)
{
lean_object* x_63; lean_object* x_64; lean_object* x_65; lean_object* x_66; 
x_63 = lean_ctor_get(x_60, 1);
lean_inc(x_63);
lean_dec(x_60);
x_64 = lean_ctor_get(x_61, 0);
lean_inc(x_64);
lean_dec(x_61);
x_65 = lean_box(0);
x_66 = lp_REPL_REPL_Sorry_of(x_64, x_23, x_24, x_65);
x_12 = x_66;
x_13 = x_63;
x_14 = lean_box(0);
goto block_17;
}
else
{
lean_object* x_67; lean_object* x_68; lean_object* x_69; 
lean_inc_ref(x_62);
x_67 = lean_ctor_get(x_60, 1);
lean_inc(x_67);
lean_dec(x_60);
x_68 = lean_ctor_get(x_61, 0);
lean_inc(x_68);
lean_dec(x_61);
x_69 = lean_ctor_get(x_62, 0);
lean_inc(x_69);
lean_dec_ref(x_62);
x_25 = x_68;
x_26 = x_69;
x_27 = x_67;
x_28 = lean_box(0);
goto block_40;
}
}
else
{
uint8_t x_70; 
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_70 = !lean_is_exclusive(x_59);
if (x_70 == 0)
{
return x_59;
}
else
{
lean_object* x_71; lean_object* x_72; 
x_71 = lean_ctor_get(x_59, 0);
lean_inc(x_71);
lean_dec(x_59);
x_72 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_72, 0, x_71);
return x_72;
}
}
}
else
{
uint8_t x_73; 
x_73 = !lean_is_exclusive(x_21);
if (x_73 == 0)
{
lean_object* x_74; lean_object* x_75; uint8_t x_76; 
x_74 = lean_ctor_get(x_21, 0);
x_75 = lean_ctor_get(x_21, 1);
lean_dec(x_75);
x_76 = !lean_is_exclusive(x_57);
if (x_76 == 0)
{
lean_object* x_77; lean_object* x_78; lean_object* x_79; 
x_77 = lean_ctor_get(x_57, 0);
lean_ctor_set(x_57, 0, x_74);
x_78 = lean_box(0);
lean_ctor_set(x_21, 1, x_78);
lean_ctor_set(x_21, 0, x_77);
lean_inc(x_1);
x_79 = lp_REPL_REPL_ProofSnapshot_create(x_20, x_57, x_1, x_78, x_21);
if (lean_obj_tag(x_79) == 0)
{
lean_object* x_80; lean_object* x_81; 
x_80 = lean_ctor_get(x_79, 0);
lean_inc(x_80);
lean_dec_ref(x_79);
lean_inc(x_80);
x_81 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_80);
if (lean_obj_tag(x_81) == 0)
{
lean_object* x_82; lean_object* x_83; lean_object* x_84; lean_object* x_85; 
x_82 = lean_ctor_get(x_81, 0);
lean_inc(x_82);
lean_dec_ref(x_81);
x_83 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_84 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_82, x_78);
x_85 = l_String_intercalate(x_83, x_84);
x_25 = x_85;
x_26 = x_80;
x_27 = x_4;
x_28 = lean_box(0);
goto block_40;
}
else
{
uint8_t x_86; 
lean_dec(x_80);
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_86 = !lean_is_exclusive(x_81);
if (x_86 == 0)
{
return x_81;
}
else
{
lean_object* x_87; lean_object* x_88; 
x_87 = lean_ctor_get(x_81, 0);
lean_inc(x_87);
lean_dec(x_81);
x_88 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_88, 0, x_87);
return x_88;
}
}
}
else
{
uint8_t x_89; 
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_89 = !lean_is_exclusive(x_79);
if (x_89 == 0)
{
return x_79;
}
else
{
lean_object* x_90; lean_object* x_91; 
x_90 = lean_ctor_get(x_79, 0);
lean_inc(x_90);
lean_dec(x_79);
x_91 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_91, 0, x_90);
return x_91;
}
}
}
else
{
lean_object* x_92; lean_object* x_93; lean_object* x_94; lean_object* x_95; 
x_92 = lean_ctor_get(x_57, 0);
lean_inc(x_92);
lean_dec(x_57);
x_93 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_93, 0, x_74);
x_94 = lean_box(0);
lean_ctor_set(x_21, 1, x_94);
lean_ctor_set(x_21, 0, x_92);
lean_inc(x_1);
x_95 = lp_REPL_REPL_ProofSnapshot_create(x_20, x_93, x_1, x_94, x_21);
if (lean_obj_tag(x_95) == 0)
{
lean_object* x_96; lean_object* x_97; 
x_96 = lean_ctor_get(x_95, 0);
lean_inc(x_96);
lean_dec_ref(x_95);
lean_inc(x_96);
x_97 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_96);
if (lean_obj_tag(x_97) == 0)
{
lean_object* x_98; lean_object* x_99; lean_object* x_100; lean_object* x_101; 
x_98 = lean_ctor_get(x_97, 0);
lean_inc(x_98);
lean_dec_ref(x_97);
x_99 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_100 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_98, x_94);
x_101 = l_String_intercalate(x_99, x_100);
x_25 = x_101;
x_26 = x_96;
x_27 = x_4;
x_28 = lean_box(0);
goto block_40;
}
else
{
lean_object* x_102; lean_object* x_103; lean_object* x_104; 
lean_dec(x_96);
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_102 = lean_ctor_get(x_97, 0);
lean_inc(x_102);
if (lean_is_exclusive(x_97)) {
 lean_ctor_release(x_97, 0);
 x_103 = x_97;
} else {
 lean_dec_ref(x_97);
 x_103 = lean_box(0);
}
if (lean_is_scalar(x_103)) {
 x_104 = lean_alloc_ctor(1, 1, 0);
} else {
 x_104 = x_103;
}
lean_ctor_set(x_104, 0, x_102);
return x_104;
}
}
else
{
lean_object* x_105; lean_object* x_106; lean_object* x_107; 
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_105 = lean_ctor_get(x_95, 0);
lean_inc(x_105);
if (lean_is_exclusive(x_95)) {
 lean_ctor_release(x_95, 0);
 x_106 = x_95;
} else {
 lean_dec_ref(x_95);
 x_106 = lean_box(0);
}
if (lean_is_scalar(x_106)) {
 x_107 = lean_alloc_ctor(1, 1, 0);
} else {
 x_107 = x_106;
}
lean_ctor_set(x_107, 0, x_105);
return x_107;
}
}
}
else
{
lean_object* x_108; lean_object* x_109; lean_object* x_110; lean_object* x_111; lean_object* x_112; lean_object* x_113; lean_object* x_114; 
x_108 = lean_ctor_get(x_21, 0);
lean_inc(x_108);
lean_dec(x_21);
x_109 = lean_ctor_get(x_57, 0);
lean_inc(x_109);
if (lean_is_exclusive(x_57)) {
 lean_ctor_release(x_57, 0);
 x_110 = x_57;
} else {
 lean_dec_ref(x_57);
 x_110 = lean_box(0);
}
if (lean_is_scalar(x_110)) {
 x_111 = lean_alloc_ctor(1, 1, 0);
} else {
 x_111 = x_110;
}
lean_ctor_set(x_111, 0, x_108);
x_112 = lean_box(0);
x_113 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_113, 0, x_109);
lean_ctor_set(x_113, 1, x_112);
lean_inc(x_1);
x_114 = lp_REPL_REPL_ProofSnapshot_create(x_20, x_111, x_1, x_112, x_113);
if (lean_obj_tag(x_114) == 0)
{
lean_object* x_115; lean_object* x_116; 
x_115 = lean_ctor_get(x_114, 0);
lean_inc(x_115);
lean_dec_ref(x_114);
lean_inc(x_115);
x_116 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_115);
if (lean_obj_tag(x_116) == 0)
{
lean_object* x_117; lean_object* x_118; lean_object* x_119; lean_object* x_120; 
x_117 = lean_ctor_get(x_116, 0);
lean_inc(x_117);
lean_dec_ref(x_116);
x_118 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_119 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_117, x_112);
x_120 = l_String_intercalate(x_118, x_119);
x_25 = x_120;
x_26 = x_115;
x_27 = x_4;
x_28 = lean_box(0);
goto block_40;
}
else
{
lean_object* x_121; lean_object* x_122; lean_object* x_123; 
lean_dec(x_115);
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_121 = lean_ctor_get(x_116, 0);
lean_inc(x_121);
if (lean_is_exclusive(x_116)) {
 lean_ctor_release(x_116, 0);
 x_122 = x_116;
} else {
 lean_dec_ref(x_116);
 x_122 = lean_box(0);
}
if (lean_is_scalar(x_122)) {
 x_123 = lean_alloc_ctor(1, 1, 0);
} else {
 x_123 = x_122;
}
lean_ctor_set(x_123, 0, x_121);
return x_123;
}
}
else
{
lean_object* x_124; lean_object* x_125; lean_object* x_126; 
lean_dec(x_24);
lean_dec(x_23);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_124 = lean_ctor_get(x_114, 0);
lean_inc(x_124);
if (lean_is_exclusive(x_114)) {
 lean_ctor_release(x_114, 0);
 x_125 = x_114;
} else {
 lean_dec_ref(x_114);
 x_125 = lean_box(0);
}
if (lean_is_scalar(x_125)) {
 x_126 = lean_alloc_ctor(1, 1, 0);
} else {
 x_126 = x_125;
}
lean_ctor_set(x_126, 0, x_124);
return x_126;
}
}
}
}
block_40:
{
lean_object* x_29; uint8_t x_30; 
x_29 = lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(x_26, x_27);
x_30 = !lean_is_exclusive(x_29);
if (x_30 == 0)
{
lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; 
x_31 = lean_ctor_get(x_29, 0);
x_32 = lean_ctor_get(x_31, 0);
lean_inc(x_32);
x_33 = lean_ctor_get(x_31, 1);
lean_inc(x_33);
lean_dec(x_31);
lean_ctor_set_tag(x_29, 1);
lean_ctor_set(x_29, 0, x_32);
x_34 = lp_REPL_REPL_Sorry_of(x_25, x_23, x_24, x_29);
x_12 = x_34;
x_13 = x_33;
x_14 = lean_box(0);
goto block_17;
}
else
{
lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; 
x_35 = lean_ctor_get(x_29, 0);
lean_inc(x_35);
lean_dec(x_29);
x_36 = lean_ctor_get(x_35, 0);
lean_inc(x_36);
x_37 = lean_ctor_get(x_35, 1);
lean_inc(x_37);
lean_dec(x_35);
x_38 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_38, 0, x_36);
x_39 = lp_REPL_REPL_Sorry_of(x_25, x_23, x_24, x_38);
x_12 = x_39;
x_13 = x_37;
x_14 = lean_box(0);
goto block_17;
}
}
}
else
{
lean_object* x_127; lean_object* x_128; lean_object* x_129; lean_object* x_130; lean_object* x_131; lean_object* x_132; 
x_127 = lean_ctor_get(x_19, 0);
x_128 = lean_ctor_get(x_19, 1);
lean_inc(x_128);
lean_inc(x_127);
lean_dec(x_19);
if (lean_obj_tag(x_21) == 0)
{
lean_object* x_141; lean_object* x_142; lean_object* x_143; lean_object* x_144; lean_object* x_145; 
x_141 = lean_ctor_get(x_21, 0);
lean_inc(x_141);
lean_dec_ref(x_21);
x_142 = lean_box(0);
x_143 = lean_box(0);
x_144 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_144, 0, x_141);
lean_ctor_set(x_144, 1, x_143);
lean_inc(x_1);
x_145 = lp_REPL_REPL_ProofSnapshot_create(x_20, x_142, x_1, x_144, x_143);
if (lean_obj_tag(x_145) == 0)
{
lean_object* x_146; lean_object* x_147; 
x_146 = lean_ctor_get(x_145, 0);
lean_inc(x_146);
lean_dec_ref(x_145);
lean_inc(x_146);
x_147 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_146);
if (lean_obj_tag(x_147) == 0)
{
lean_object* x_148; lean_object* x_149; lean_object* x_150; lean_object* x_151; 
x_148 = lean_ctor_get(x_147, 0);
lean_inc(x_148);
lean_dec_ref(x_147);
x_149 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_150 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_148, x_143);
x_151 = l_String_intercalate(x_149, x_150);
x_129 = x_151;
x_130 = x_146;
x_131 = x_4;
x_132 = lean_box(0);
goto block_140;
}
else
{
lean_object* x_152; lean_object* x_153; lean_object* x_154; 
lean_dec(x_146);
lean_dec(x_128);
lean_dec(x_127);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_152 = lean_ctor_get(x_147, 0);
lean_inc(x_152);
if (lean_is_exclusive(x_147)) {
 lean_ctor_release(x_147, 0);
 x_153 = x_147;
} else {
 lean_dec_ref(x_147);
 x_153 = lean_box(0);
}
if (lean_is_scalar(x_153)) {
 x_154 = lean_alloc_ctor(1, 1, 0);
} else {
 x_154 = x_153;
}
lean_ctor_set(x_154, 0, x_152);
return x_154;
}
}
else
{
lean_object* x_155; lean_object* x_156; lean_object* x_157; 
lean_dec(x_128);
lean_dec(x_127);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_155 = lean_ctor_get(x_145, 0);
lean_inc(x_155);
if (lean_is_exclusive(x_145)) {
 lean_ctor_release(x_145, 0);
 x_156 = x_145;
} else {
 lean_dec_ref(x_145);
 x_156 = lean_box(0);
}
if (lean_is_scalar(x_156)) {
 x_157 = lean_alloc_ctor(1, 1, 0);
} else {
 x_157 = x_156;
}
lean_ctor_set(x_157, 0, x_155);
return x_157;
}
}
else
{
lean_object* x_158; 
x_158 = lean_ctor_get(x_21, 1);
lean_inc(x_158);
if (lean_obj_tag(x_158) == 0)
{
lean_object* x_159; lean_object* x_160; 
lean_dec_ref(x_21);
lean_dec(x_20);
x_159 = lp_REPL_REPL_sorries___redArg___lam__16___closed__3;
x_160 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2(x_159, x_4);
if (lean_obj_tag(x_160) == 0)
{
lean_object* x_161; lean_object* x_162; lean_object* x_163; 
x_161 = lean_ctor_get(x_160, 0);
lean_inc(x_161);
lean_dec_ref(x_160);
x_162 = lean_ctor_get(x_161, 0);
lean_inc(x_162);
x_163 = lean_ctor_get(x_162, 1);
if (lean_obj_tag(x_163) == 0)
{
lean_object* x_164; lean_object* x_165; lean_object* x_166; lean_object* x_167; 
x_164 = lean_ctor_get(x_161, 1);
lean_inc(x_164);
lean_dec(x_161);
x_165 = lean_ctor_get(x_162, 0);
lean_inc(x_165);
lean_dec(x_162);
x_166 = lean_box(0);
x_167 = lp_REPL_REPL_Sorry_of(x_165, x_127, x_128, x_166);
x_12 = x_167;
x_13 = x_164;
x_14 = lean_box(0);
goto block_17;
}
else
{
lean_object* x_168; lean_object* x_169; lean_object* x_170; 
lean_inc_ref(x_163);
x_168 = lean_ctor_get(x_161, 1);
lean_inc(x_168);
lean_dec(x_161);
x_169 = lean_ctor_get(x_162, 0);
lean_inc(x_169);
lean_dec(x_162);
x_170 = lean_ctor_get(x_163, 0);
lean_inc(x_170);
lean_dec_ref(x_163);
x_129 = x_169;
x_130 = x_170;
x_131 = x_168;
x_132 = lean_box(0);
goto block_140;
}
}
else
{
lean_object* x_171; lean_object* x_172; lean_object* x_173; 
lean_dec(x_128);
lean_dec(x_127);
lean_dec(x_11);
lean_dec(x_10);
lean_dec(x_3);
lean_dec(x_1);
x_171 = lean_ctor_get(x_160, 0);
lean_inc(x_171);
if (lean_is_exclusive(x_160)) {
 lean_ctor_release(x_160, 0);
 x_172 = x_160;
} else {
 lean_dec_ref(x_160);
 x_172 = lean_box(0);
}
if (lean_is_scalar(x_172)) {
 x_173 = lean_alloc_ctor(1, 1, 0);
} else {
 x_173 = x_172;
}
lean_ctor_set(x_173, 0, x_171);
return x_173;
}
}
else
{
lean_object* x_174; lean_object* x_175; lean_object* x_176; lean_object* x_177; lean_object* x_178; lean_object* x_179; lean_object* x_180; lean_object* x_181; 
x_174 = lean_ctor_get(x_21, 0);
lean_inc_ref(x_174);
if (lean_is_exclusive(x_21)) {
 lean_ctor_release(x_21, 0);
 lean_ctor_release(x_21, 1);
 x_175 = x_21;
} else {
 lean_dec_ref(x_21);
 x_175 = lean_box(0);
}
x_176 = lean_ctor_get(x_158, 0);
lean_inc(x_176);
if (lean_is_exclusive(x_158)) {
 lean_ctor_release(x_158, 0);
 x_177 = x_158;
} else {
 lean_dec_ref(x_158);
 x_177 = lean_box(0);
}
if (lean_is_scalar(x_177)) {
 x_178 = lean_alloc_ctor(1, 1, 0);
} else {
 x_178 = x_177;
}
lean_ctor_set(x_178, 0, x_174);
x_179 = lean_box(0);
if (lean_is_scalar(x_175)) {
 x_180 = lean_alloc_ctor(1, 2, 0);
} else {
 x_180 = x_175;
}
lean_ctor_set(x_180, 0, x_176);
lean_ctor_set(x_180, 1, x_179);
lean_inc(x_1);
x_181 = lp_REPL_REPL_ProofSnapshot_create(x_20, x_178, x_1, x_179, x_180);
if (lean_obj_tag(x_181) == 0)
{
lean_object* x_182; lean_object* x_183; 
x_182 = lean_ctor_get(x_181, 0);
lean_inc(x_182);
lean_dec_ref(x_181);
lean_inc(x_182);
x_183 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_182);
if (lean_obj_tag(x_183) == 0)
{
lean_object* x_184; lean_object* x_185; lean_object* x_186; lean_object* x_187; 
x_184 = lean_ctor_get(x_183, 0);
lean_inc(x_184);
lean_dec_ref(x_183);
x_185 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_186 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_184, x_179);
x_187 = l_String_intercalate(x_185, x_186);
x_129 = x_187;
x_130 = x_182;
x_131 = x_4;
x_132 = lean_box(0);
goto block_140;
}
else
{
lean_object* x_188; lean_object* x_189; lean_object* x_190; 
lean_dec(x_182);
lean_dec(x_128);
lean_dec(x_127);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_188 = lean_ctor_get(x_183, 0);
lean_inc(x_188);
if (lean_is_exclusive(x_183)) {
 lean_ctor_release(x_183, 0);
 x_189 = x_183;
} else {
 lean_dec_ref(x_183);
 x_189 = lean_box(0);
}
if (lean_is_scalar(x_189)) {
 x_190 = lean_alloc_ctor(1, 1, 0);
} else {
 x_190 = x_189;
}
lean_ctor_set(x_190, 0, x_188);
return x_190;
}
}
else
{
lean_object* x_191; lean_object* x_192; lean_object* x_193; 
lean_dec(x_128);
lean_dec(x_127);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_4);
lean_dec(x_3);
lean_dec(x_1);
x_191 = lean_ctor_get(x_181, 0);
lean_inc(x_191);
if (lean_is_exclusive(x_181)) {
 lean_ctor_release(x_181, 0);
 x_192 = x_181;
} else {
 lean_dec_ref(x_181);
 x_192 = lean_box(0);
}
if (lean_is_scalar(x_192)) {
 x_193 = lean_alloc_ctor(1, 1, 0);
} else {
 x_193 = x_192;
}
lean_ctor_set(x_193, 0, x_191);
return x_193;
}
}
}
block_140:
{
lean_object* x_133; lean_object* x_134; lean_object* x_135; lean_object* x_136; lean_object* x_137; lean_object* x_138; lean_object* x_139; 
x_133 = lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(x_130, x_131);
x_134 = lean_ctor_get(x_133, 0);
lean_inc(x_134);
if (lean_is_exclusive(x_133)) {
 lean_ctor_release(x_133, 0);
 x_135 = x_133;
} else {
 lean_dec_ref(x_133);
 x_135 = lean_box(0);
}
x_136 = lean_ctor_get(x_134, 0);
lean_inc(x_136);
x_137 = lean_ctor_get(x_134, 1);
lean_inc(x_137);
lean_dec(x_134);
if (lean_is_scalar(x_135)) {
 x_138 = lean_alloc_ctor(1, 1, 0);
} else {
 x_138 = x_135;
 lean_ctor_set_tag(x_138, 1);
}
lean_ctor_set(x_138, 0, x_136);
x_139 = lp_REPL_REPL_Sorry_of(x_129, x_127, x_128, x_138);
x_12 = x_139;
x_13 = x_137;
x_14 = lean_box(0);
goto block_17;
}
}
block_17:
{
lean_object* x_15; 
if (lean_is_scalar(x_11)) {
 x_15 = lean_alloc_ctor(1, 2, 0);
} else {
 x_15 = x_11;
}
lean_ctor_set(x_15, 0, x_12);
lean_ctor_set(x_15, 1, x_3);
x_2 = x_10;
x_3 = x_15;
x_4 = x_13;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_5 = lp_REPL_REPL_sorries___redArg___closed__3;
x_6 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_sorriesGC_spec__2(x_1, x_5);
x_7 = lean_box(0);
x_8 = lp_REPL_List_filterTR_loop___at___00REPL_sorriesGC_spec__3(x_6, x_7);
x_9 = lp_REPL_List_mapM_loop___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__3(x_2, x_8, x_7, x_3);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_5 = l_List_reverse___redArg(x_2);
x_6 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_6, 0, x_5);
lean_ctor_set(x_6, 1, x_3);
x_7 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_7, 0, x_6);
return x_7;
}
else
{
uint8_t x_8; 
x_8 = !lean_is_exclusive(x_1);
if (x_8 == 0)
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; 
x_9 = lean_ctor_get(x_1, 0);
x_10 = lean_ctor_get(x_1, 1);
x_11 = lp_REPL_REPL_Message_of(x_9);
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
lean_dec_ref(x_11);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_12);
{
lean_object* _tmp_0 = x_10;
lean_object* _tmp_1 = x_1;
x_1 = _tmp_0;
x_2 = _tmp_1;
}
goto _start;
}
else
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; 
x_14 = lean_ctor_get(x_1, 0);
x_15 = lean_ctor_get(x_1, 1);
lean_inc(x_15);
lean_inc(x_14);
lean_dec(x_1);
x_16 = lp_REPL_REPL_Message_of(x_14);
x_17 = lean_ctor_get(x_16, 0);
lean_inc(x_17);
lean_dec_ref(x_16);
x_18 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_18, 0, x_17);
lean_ctor_set(x_18, 1, x_2);
x_1 = x_15;
x_2 = x_18;
goto _start;
}
}
}
}
static lean_object* _init_lp_REPL_REPL_unpickleProofSnapshot___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0;
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(l_Lean_Elab_CommandContextInfo_save___at___00Lean_Widget_goalToInteractive_spec__9___boxed), 5, 0);
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_5 = lp_REPL_REPL_ProofSnapshot_newMessages(x_1, x_2);
x_6 = lean_box(0);
x_7 = lp_REPL_List_mapM_loop___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__0(x_5, x_6, x_3);
if (lean_obj_tag(x_7) == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_8 = lean_ctor_get(x_7, 0);
lean_inc(x_8);
lean_dec_ref(x_7);
x_9 = lean_ctor_get(x_8, 0);
lean_inc(x_9);
x_10 = lean_ctor_get(x_8, 1);
lean_inc(x_10);
lean_dec(x_8);
lean_inc(x_2);
lean_inc_ref(x_1);
x_11 = lp_REPL_REPL_ProofSnapshot_newTraces(x_1, x_2);
if (lean_obj_tag(x_11) == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_54; 
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
lean_dec_ref(x_11);
lean_inc(x_2);
lean_inc_ref(x_1);
x_54 = lp_REPL_REPL_ProofSnapshot_newInfoTrees(x_1, x_2);
if (lean_obj_tag(x_2) == 0)
{
x_13 = x_54;
x_14 = x_10;
x_15 = lean_box(0);
goto block_53;
}
else
{
uint8_t x_55; 
x_55 = !lean_is_exclusive(x_2);
if (x_55 == 0)
{
lean_object* x_56; lean_object* x_57; lean_object* x_58; 
x_56 = lean_ctor_get(x_2, 0);
x_57 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___closed__0;
x_58 = lp_REPL_REPL_ProofSnapshot_runMetaM___redArg(x_56, x_57);
if (lean_obj_tag(x_58) == 0)
{
lean_object* x_59; lean_object* x_60; lean_object* x_61; 
x_59 = lean_ctor_get(x_58, 0);
lean_inc(x_59);
lean_dec_ref(x_58);
x_60 = lean_ctor_get(x_59, 0);
lean_inc(x_60);
lean_dec(x_59);
lean_ctor_set_tag(x_2, 0);
lean_ctor_set(x_2, 0, x_60);
x_61 = lp_REPL_List_mapTR_loop___at___00Lean_Elab_InfoTree_filter_spec__0(x_2, x_54, x_6);
x_13 = x_61;
x_14 = x_10;
x_15 = lean_box(0);
goto block_53;
}
else
{
uint8_t x_62; 
lean_free_object(x_2);
lean_dec(x_54);
lean_dec(x_12);
lean_dec(x_10);
lean_dec(x_9);
lean_dec_ref(x_1);
x_62 = !lean_is_exclusive(x_58);
if (x_62 == 0)
{
return x_58;
}
else
{
lean_object* x_63; lean_object* x_64; 
x_63 = lean_ctor_get(x_58, 0);
lean_inc(x_63);
lean_dec(x_58);
x_64 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_64, 0, x_63);
return x_64;
}
}
}
else
{
lean_object* x_65; lean_object* x_66; lean_object* x_67; 
x_65 = lean_ctor_get(x_2, 0);
lean_inc(x_65);
lean_dec(x_2);
x_66 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___closed__0;
x_67 = lp_REPL_REPL_ProofSnapshot_runMetaM___redArg(x_65, x_66);
if (lean_obj_tag(x_67) == 0)
{
lean_object* x_68; lean_object* x_69; lean_object* x_70; lean_object* x_71; 
x_68 = lean_ctor_get(x_67, 0);
lean_inc(x_68);
lean_dec_ref(x_67);
x_69 = lean_ctor_get(x_68, 0);
lean_inc(x_69);
lean_dec(x_68);
x_70 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_70, 0, x_69);
x_71 = lp_REPL_List_mapTR_loop___at___00Lean_Elab_InfoTree_filter_spec__0(x_70, x_54, x_6);
x_13 = x_71;
x_14 = x_10;
x_15 = lean_box(0);
goto block_53;
}
else
{
lean_object* x_72; lean_object* x_73; lean_object* x_74; 
lean_dec(x_54);
lean_dec(x_12);
lean_dec(x_10);
lean_dec(x_9);
lean_dec_ref(x_1);
x_72 = lean_ctor_get(x_67, 0);
lean_inc(x_72);
if (lean_is_exclusive(x_67)) {
 lean_ctor_release(x_67, 0);
 x_73 = x_67;
} else {
 lean_dec_ref(x_67);
 x_73 = lean_box(0);
}
if (lean_is_scalar(x_73)) {
 x_74 = lean_alloc_ctor(1, 1, 0);
} else {
 x_74 = x_73;
}
lean_ctor_set(x_74, 0, x_72);
return x_74;
}
}
}
block_53:
{
lean_object* x_16; lean_object* x_17; 
x_16 = lean_box(0);
x_17 = lp_REPL_REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1(x_13, x_16, x_14);
if (lean_obj_tag(x_17) == 0)
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; uint8_t x_23; 
x_18 = lean_ctor_get(x_17, 0);
lean_inc(x_18);
lean_dec_ref(x_17);
x_19 = lean_ctor_get(x_18, 0);
lean_inc(x_19);
x_20 = lean_ctor_get(x_18, 1);
lean_inc(x_20);
lean_dec(x_18);
lean_inc_ref(x_1);
x_21 = lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(x_1, x_20);
x_22 = lean_ctor_get(x_21, 0);
lean_inc(x_22);
lean_dec_ref(x_21);
x_23 = !lean_is_exclusive(x_22);
if (x_23 == 0)
{
lean_object* x_24; lean_object* x_25; lean_object* x_26; 
x_24 = lean_ctor_get(x_22, 0);
x_25 = lean_ctor_get(x_22, 1);
x_26 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_1);
if (lean_obj_tag(x_26) == 0)
{
uint8_t x_27; 
x_27 = !lean_is_exclusive(x_26);
if (x_27 == 0)
{
lean_object* x_28; lean_object* x_29; lean_object* x_30; 
x_28 = lean_ctor_get(x_26, 0);
x_29 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_28, x_6);
x_30 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_30, 0, x_24);
lean_ctor_set(x_30, 1, x_29);
lean_ctor_set(x_30, 2, x_9);
lean_ctor_set(x_30, 3, x_19);
lean_ctor_set(x_30, 4, x_12);
lean_ctor_set(x_22, 0, x_30);
lean_ctor_set(x_26, 0, x_22);
return x_26;
}
else
{
lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; 
x_31 = lean_ctor_get(x_26, 0);
lean_inc(x_31);
lean_dec(x_26);
x_32 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_31, x_6);
x_33 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_33, 0, x_24);
lean_ctor_set(x_33, 1, x_32);
lean_ctor_set(x_33, 2, x_9);
lean_ctor_set(x_33, 3, x_19);
lean_ctor_set(x_33, 4, x_12);
lean_ctor_set(x_22, 0, x_33);
x_34 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_34, 0, x_22);
return x_34;
}
}
else
{
uint8_t x_35; 
lean_free_object(x_22);
lean_dec(x_25);
lean_dec(x_24);
lean_dec(x_19);
lean_dec(x_12);
lean_dec(x_9);
x_35 = !lean_is_exclusive(x_26);
if (x_35 == 0)
{
return x_26;
}
else
{
lean_object* x_36; lean_object* x_37; 
x_36 = lean_ctor_get(x_26, 0);
lean_inc(x_36);
lean_dec(x_26);
x_37 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_37, 0, x_36);
return x_37;
}
}
}
else
{
lean_object* x_38; lean_object* x_39; lean_object* x_40; 
x_38 = lean_ctor_get(x_22, 0);
x_39 = lean_ctor_get(x_22, 1);
lean_inc(x_39);
lean_inc(x_38);
lean_dec(x_22);
x_40 = lp_REPL_REPL_ProofSnapshot_ppGoals(x_1);
if (lean_obj_tag(x_40) == 0)
{
lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; 
x_41 = lean_ctor_get(x_40, 0);
lean_inc(x_41);
if (lean_is_exclusive(x_40)) {
 lean_ctor_release(x_40, 0);
 x_42 = x_40;
} else {
 lean_dec_ref(x_40);
 x_42 = lean_box(0);
}
x_43 = lp_REPL_List_mapTR_loop___at___00REPL_sorriesGC_spec__0(x_41, x_6);
x_44 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_44, 0, x_38);
lean_ctor_set(x_44, 1, x_43);
lean_ctor_set(x_44, 2, x_9);
lean_ctor_set(x_44, 3, x_19);
lean_ctor_set(x_44, 4, x_12);
x_45 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_45, 0, x_44);
lean_ctor_set(x_45, 1, x_39);
if (lean_is_scalar(x_42)) {
 x_46 = lean_alloc_ctor(0, 1, 0);
} else {
 x_46 = x_42;
}
lean_ctor_set(x_46, 0, x_45);
return x_46;
}
else
{
lean_object* x_47; lean_object* x_48; lean_object* x_49; 
lean_dec(x_39);
lean_dec(x_38);
lean_dec(x_19);
lean_dec(x_12);
lean_dec(x_9);
x_47 = lean_ctor_get(x_40, 0);
lean_inc(x_47);
if (lean_is_exclusive(x_40)) {
 lean_ctor_release(x_40, 0);
 x_48 = x_40;
} else {
 lean_dec_ref(x_40);
 x_48 = lean_box(0);
}
if (lean_is_scalar(x_48)) {
 x_49 = lean_alloc_ctor(1, 1, 0);
} else {
 x_49 = x_48;
}
lean_ctor_set(x_49, 0, x_47);
return x_49;
}
}
}
else
{
uint8_t x_50; 
lean_dec(x_12);
lean_dec(x_9);
lean_dec_ref(x_1);
x_50 = !lean_is_exclusive(x_17);
if (x_50 == 0)
{
return x_17;
}
else
{
lean_object* x_51; lean_object* x_52; 
x_51 = lean_ctor_get(x_17, 0);
lean_inc(x_51);
lean_dec(x_17);
x_52 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_52, 0, x_51);
return x_52;
}
}
}
}
else
{
uint8_t x_75; 
lean_dec(x_10);
lean_dec(x_9);
lean_dec(x_2);
lean_dec_ref(x_1);
x_75 = !lean_is_exclusive(x_11);
if (x_75 == 0)
{
return x_11;
}
else
{
lean_object* x_76; lean_object* x_77; 
x_76 = lean_ctor_get(x_11, 0);
lean_inc(x_76);
lean_dec(x_11);
x_77 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_77, 0, x_76);
return x_77;
}
}
}
else
{
uint8_t x_78; 
lean_dec(x_2);
lean_dec_ref(x_1);
x_78 = !lean_is_exclusive(x_7);
if (x_78 == 0)
{
return x_7;
}
else
{
lean_object* x_79; lean_object* x_80; 
x_79 = lean_ctor_get(x_7, 0);
lean_inc(x_79);
lean_dec(x_7);
x_80 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_80, 0, x_79);
return x_80;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleProofSnapshot(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_1);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_5 = lean_ctor_get(x_1, 0);
x_6 = lean_ctor_get(x_1, 1);
if (lean_obj_tag(x_6) == 0)
{
lean_object* x_38; 
lean_free_object(x_1);
x_38 = lean_box(0);
x_7 = x_38;
x_8 = x_2;
x_9 = lean_box(0);
goto block_37;
}
else
{
uint8_t x_39; 
x_39 = !lean_is_exclusive(x_6);
if (x_39 == 0)
{
lean_object* x_40; lean_object* x_41; lean_object* x_42; uint8_t x_43; 
x_40 = lean_ctor_get(x_6, 0);
x_41 = lean_ctor_get(x_2, 0);
x_42 = lean_array_get_size(x_41);
x_43 = lean_nat_dec_lt(x_40, x_42);
if (x_43 == 0)
{
lean_object* x_44; lean_object* x_45; 
lean_free_object(x_6);
lean_dec(x_40);
lean_dec_ref(x_5);
x_44 = lp_REPL_REPL_unpickleProofSnapshot___closed__0;
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_44);
x_45 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_45, 0, x_1);
return x_45;
}
else
{
lean_object* x_46; 
lean_free_object(x_1);
x_46 = lean_array_fget_borrowed(x_41, x_40);
lean_dec(x_40);
lean_inc(x_46);
lean_ctor_set(x_6, 0, x_46);
x_7 = x_6;
x_8 = x_2;
x_9 = lean_box(0);
goto block_37;
}
}
else
{
lean_object* x_47; lean_object* x_48; lean_object* x_49; uint8_t x_50; 
x_47 = lean_ctor_get(x_6, 0);
lean_inc(x_47);
lean_dec(x_6);
x_48 = lean_ctor_get(x_2, 0);
x_49 = lean_array_get_size(x_48);
x_50 = lean_nat_dec_lt(x_47, x_49);
if (x_50 == 0)
{
lean_object* x_51; lean_object* x_52; 
lean_dec(x_47);
lean_dec_ref(x_5);
x_51 = lp_REPL_REPL_unpickleProofSnapshot___closed__0;
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_51);
x_52 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_52, 0, x_1);
return x_52;
}
else
{
lean_object* x_53; lean_object* x_54; 
lean_free_object(x_1);
x_53 = lean_array_fget_borrowed(x_48, x_47);
lean_dec(x_47);
lean_inc(x_53);
x_54 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_54, 0, x_53);
x_7 = x_54;
x_8 = x_2;
x_9 = lean_box(0);
goto block_37;
}
}
}
block_37:
{
lean_object* x_10; 
x_10 = lp_REPL_REPL_ProofSnapshot_unpickle_unsafe__7(x_5, x_7);
if (lean_obj_tag(x_10) == 0)
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; 
x_11 = lean_ctor_get(x_10, 0);
lean_inc(x_11);
lean_dec_ref(x_10);
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
lean_dec(x_11);
x_13 = lean_box(0);
x_14 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_12, x_13, x_8);
if (lean_obj_tag(x_14) == 0)
{
uint8_t x_15; 
x_15 = !lean_is_exclusive(x_14);
if (x_15 == 0)
{
lean_object* x_16; uint8_t x_17; 
x_16 = lean_ctor_get(x_14, 0);
x_17 = !lean_is_exclusive(x_16);
if (x_17 == 0)
{
lean_object* x_18; lean_object* x_19; 
x_18 = lean_ctor_get(x_16, 0);
x_19 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_19, 0, x_18);
lean_ctor_set(x_16, 0, x_19);
return x_14;
}
else
{
lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; 
x_20 = lean_ctor_get(x_16, 0);
x_21 = lean_ctor_get(x_16, 1);
lean_inc(x_21);
lean_inc(x_20);
lean_dec(x_16);
x_22 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_22, 0, x_20);
x_23 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_23, 0, x_22);
lean_ctor_set(x_23, 1, x_21);
lean_ctor_set(x_14, 0, x_23);
return x_14;
}
}
else
{
lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; 
x_24 = lean_ctor_get(x_14, 0);
lean_inc(x_24);
lean_dec(x_14);
x_25 = lean_ctor_get(x_24, 0);
lean_inc(x_25);
x_26 = lean_ctor_get(x_24, 1);
lean_inc(x_26);
if (lean_is_exclusive(x_24)) {
 lean_ctor_release(x_24, 0);
 lean_ctor_release(x_24, 1);
 x_27 = x_24;
} else {
 lean_dec_ref(x_24);
 x_27 = lean_box(0);
}
x_28 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_28, 0, x_25);
if (lean_is_scalar(x_27)) {
 x_29 = lean_alloc_ctor(0, 2, 0);
} else {
 x_29 = x_27;
}
lean_ctor_set(x_29, 0, x_28);
lean_ctor_set(x_29, 1, x_26);
x_30 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_30, 0, x_29);
return x_30;
}
}
else
{
uint8_t x_31; 
x_31 = !lean_is_exclusive(x_14);
if (x_31 == 0)
{
return x_14;
}
else
{
lean_object* x_32; lean_object* x_33; 
x_32 = lean_ctor_get(x_14, 0);
lean_inc(x_32);
lean_dec(x_14);
x_33 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_33, 0, x_32);
return x_33;
}
}
}
else
{
uint8_t x_34; 
lean_dec_ref(x_8);
x_34 = !lean_is_exclusive(x_10);
if (x_34 == 0)
{
return x_10;
}
else
{
lean_object* x_35; lean_object* x_36; 
x_35 = lean_ctor_get(x_10, 0);
lean_inc(x_35);
lean_dec(x_10);
x_36 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_36, 0, x_35);
return x_36;
}
}
}
}
else
{
lean_object* x_55; lean_object* x_56; lean_object* x_57; lean_object* x_58; lean_object* x_59; 
x_55 = lean_ctor_get(x_1, 0);
x_56 = lean_ctor_get(x_1, 1);
lean_inc(x_56);
lean_inc(x_55);
lean_dec(x_1);
if (lean_obj_tag(x_56) == 0)
{
lean_object* x_80; 
x_80 = lean_box(0);
x_57 = x_80;
x_58 = x_2;
x_59 = lean_box(0);
goto block_79;
}
else
{
lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; uint8_t x_85; 
x_81 = lean_ctor_get(x_56, 0);
lean_inc(x_81);
if (lean_is_exclusive(x_56)) {
 lean_ctor_release(x_56, 0);
 x_82 = x_56;
} else {
 lean_dec_ref(x_56);
 x_82 = lean_box(0);
}
x_83 = lean_ctor_get(x_2, 0);
x_84 = lean_array_get_size(x_83);
x_85 = lean_nat_dec_lt(x_81, x_84);
if (x_85 == 0)
{
lean_object* x_86; lean_object* x_87; lean_object* x_88; 
lean_dec(x_82);
lean_dec(x_81);
lean_dec_ref(x_55);
x_86 = lp_REPL_REPL_unpickleProofSnapshot___closed__0;
x_87 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_87, 0, x_86);
lean_ctor_set(x_87, 1, x_2);
x_88 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_88, 0, x_87);
return x_88;
}
else
{
lean_object* x_89; lean_object* x_90; 
x_89 = lean_array_fget_borrowed(x_83, x_81);
lean_dec(x_81);
lean_inc(x_89);
if (lean_is_scalar(x_82)) {
 x_90 = lean_alloc_ctor(1, 1, 0);
} else {
 x_90 = x_82;
}
lean_ctor_set(x_90, 0, x_89);
x_57 = x_90;
x_58 = x_2;
x_59 = lean_box(0);
goto block_79;
}
}
block_79:
{
lean_object* x_60; 
x_60 = lp_REPL_REPL_ProofSnapshot_unpickle_unsafe__7(x_55, x_57);
if (lean_obj_tag(x_60) == 0)
{
lean_object* x_61; lean_object* x_62; lean_object* x_63; lean_object* x_64; 
x_61 = lean_ctor_get(x_60, 0);
lean_inc(x_61);
lean_dec_ref(x_60);
x_62 = lean_ctor_get(x_61, 0);
lean_inc(x_62);
lean_dec(x_61);
x_63 = lean_box(0);
x_64 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_62, x_63, x_58);
if (lean_obj_tag(x_64) == 0)
{
lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_68; lean_object* x_69; lean_object* x_70; lean_object* x_71; lean_object* x_72; 
x_65 = lean_ctor_get(x_64, 0);
lean_inc(x_65);
if (lean_is_exclusive(x_64)) {
 lean_ctor_release(x_64, 0);
 x_66 = x_64;
} else {
 lean_dec_ref(x_64);
 x_66 = lean_box(0);
}
x_67 = lean_ctor_get(x_65, 0);
lean_inc(x_67);
x_68 = lean_ctor_get(x_65, 1);
lean_inc(x_68);
if (lean_is_exclusive(x_65)) {
 lean_ctor_release(x_65, 0);
 lean_ctor_release(x_65, 1);
 x_69 = x_65;
} else {
 lean_dec_ref(x_65);
 x_69 = lean_box(0);
}
x_70 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_70, 0, x_67);
if (lean_is_scalar(x_69)) {
 x_71 = lean_alloc_ctor(0, 2, 0);
} else {
 x_71 = x_69;
}
lean_ctor_set(x_71, 0, x_70);
lean_ctor_set(x_71, 1, x_68);
if (lean_is_scalar(x_66)) {
 x_72 = lean_alloc_ctor(0, 1, 0);
} else {
 x_72 = x_66;
}
lean_ctor_set(x_72, 0, x_71);
return x_72;
}
else
{
lean_object* x_73; lean_object* x_74; lean_object* x_75; 
x_73 = lean_ctor_get(x_64, 0);
lean_inc(x_73);
if (lean_is_exclusive(x_64)) {
 lean_ctor_release(x_64, 0);
 x_74 = x_64;
} else {
 lean_dec_ref(x_64);
 x_74 = lean_box(0);
}
if (lean_is_scalar(x_74)) {
 x_75 = lean_alloc_ctor(1, 1, 0);
} else {
 x_75 = x_74;
}
lean_ctor_set(x_75, 0, x_73);
return x_75;
}
}
else
{
lean_object* x_76; lean_object* x_77; lean_object* x_78; 
lean_dec_ref(x_58);
x_76 = lean_ctor_get(x_60, 0);
lean_inc(x_76);
if (lean_is_exclusive(x_60)) {
 lean_ctor_release(x_60, 0);
 x_77 = x_60;
} else {
 lean_dec_ref(x_60);
 x_77 = lean_box(0);
}
if (lean_is_scalar(x_77)) {
 x_78 = lean_alloc_ctor(1, 1, 0);
} else {
 x_78 = x_77;
}
lean_ctor_set(x_78, 0, x_76);
return x_78;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_List_mapM_loop___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__0(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_unpickleProofSnapshot___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_unpickleProofSnapshot(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__3___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_List_mapM_loop___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__3(x_1, x_2, x_3, x_4);
return x_6;
}
}
static lean_object* _init_lp_REPL_REPL_getCommandSnapshot___closed__0() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = 0;
x_2 = lean_box(0);
x_3 = lean_box(x_1);
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_2);
lean_ctor_set(x_4, 1, x_3);
return x_4;
}
}
static lean_object* _init_lp_REPL_REPL_getCommandSnapshot___closed__1() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = 1;
x_2 = lean_box(0);
x_3 = lean_box(x_1);
x_4 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_4, 0, x_2);
lean_ctor_set(x_4, 1, x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_getCommandSnapshot(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_4 = lp_REPL_REPL_getCommandSnapshot___closed__0;
x_5 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_5, 0, x_4);
lean_ctor_set(x_5, 1, x_2);
x_6 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_6, 0, x_5);
return x_6;
}
else
{
uint8_t x_7; 
x_7 = !lean_is_exclusive(x_1);
if (x_7 == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; uint8_t x_11; 
x_8 = lean_ctor_get(x_1, 0);
x_9 = lean_ctor_get(x_2, 0);
x_10 = lean_array_get_size(x_9);
x_11 = lean_nat_dec_lt(x_8, x_10);
if (x_11 == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; 
lean_free_object(x_1);
lean_dec(x_8);
x_12 = lp_REPL_REPL_getCommandSnapshot___closed__1;
x_13 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_13, 0, x_12);
lean_ctor_set(x_13, 1, x_2);
x_14 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_14, 0, x_13);
return x_14;
}
else
{
lean_object* x_15; uint8_t x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; 
x_15 = lean_array_fget_borrowed(x_9, x_8);
lean_dec(x_8);
lean_inc(x_15);
lean_ctor_set(x_1, 0, x_15);
x_16 = 0;
x_17 = lean_box(x_16);
x_18 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_18, 0, x_1);
lean_ctor_set(x_18, 1, x_17);
x_19 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_19, 0, x_18);
lean_ctor_set(x_19, 1, x_2);
x_20 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_20, 0, x_19);
return x_20;
}
}
else
{
lean_object* x_21; lean_object* x_22; lean_object* x_23; uint8_t x_24; 
x_21 = lean_ctor_get(x_1, 0);
lean_inc(x_21);
lean_dec(x_1);
x_22 = lean_ctor_get(x_2, 0);
x_23 = lean_array_get_size(x_22);
x_24 = lean_nat_dec_lt(x_21, x_23);
if (x_24 == 0)
{
lean_object* x_25; lean_object* x_26; lean_object* x_27; 
lean_dec(x_21);
x_25 = lp_REPL_REPL_getCommandSnapshot___closed__1;
x_26 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_26, 0, x_25);
lean_ctor_set(x_26, 1, x_2);
x_27 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_27, 0, x_26);
return x_27;
}
else
{
lean_object* x_28; lean_object* x_29; uint8_t x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; 
x_28 = lean_array_fget_borrowed(x_22, x_21);
lean_dec(x_21);
lean_inc(x_28);
x_29 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_29, 0, x_28);
x_30 = 0;
x_31 = lean_box(x_30);
x_32 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_32, 0, x_29);
lean_ctor_set(x_32, 1, x_31);
x_33 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_33, 0, x_32);
lean_ctor_set(x_33, 1, x_2);
x_34 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_34, 0, x_33);
return x_34;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_getCommandSnapshot___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_getCommandSnapshot(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = lean_array_to_list(x_2);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lean_ctor_get(x_1, 0);
lean_inc(x_4);
x_5 = lean_ctor_get(x_1, 1);
lean_inc(x_5);
lean_dec_ref(x_1);
x_6 = lp_REPL_Lean_Elab_InfoTree_retainTacticInfo(x_4);
x_7 = l_List_foldl___at___00Array_appendList_spec__0___redArg(x_2, x_6);
x_1 = x_5;
x_2 = x_7;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__3(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = lean_array_to_list(x_2);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lean_ctor_get(x_1, 0);
lean_inc(x_4);
x_5 = lean_ctor_get(x_1, 1);
lean_inc(x_5);
lean_dec_ref(x_1);
x_6 = lp_REPL_Lean_Elab_InfoTree_retainSubstantive(x_4);
x_7 = l_List_foldl___at___00Array_appendList_spec__0___redArg(x_2, x_6);
x_1 = x_5;
x_2 = x_7;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__4(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_3; 
x_3 = lean_array_to_list(x_2);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lean_ctor_get(x_1, 0);
lean_inc(x_4);
x_5 = lean_ctor_get(x_1, 1);
lean_inc(x_5);
lean_dec_ref(x_1);
x_6 = lp_REPL_Lean_Elab_InfoTree_retainOriginal(x_4);
x_7 = l_List_foldl___at___00Array_appendList_spec__0___redArg(x_2, x_6);
x_1 = x_5;
x_2 = x_7;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_runCommandGCAux_spec__0(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_4; lean_object* x_5; 
x_4 = l_List_reverse___redArg(x_2);
x_5 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_5, 0, x_4);
return x_5;
}
else
{
uint8_t x_6; 
x_6 = !lean_is_exclusive(x_1);
if (x_6 == 0)
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; 
x_7 = lean_ctor_get(x_1, 0);
x_8 = lean_ctor_get(x_1, 1);
x_9 = lp_REPL_REPL_Message_of(x_7);
x_10 = lean_ctor_get(x_9, 0);
lean_inc(x_10);
lean_dec_ref(x_9);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_10);
{
lean_object* _tmp_0 = x_8;
lean_object* _tmp_1 = x_1;
x_1 = _tmp_0;
x_2 = _tmp_1;
}
goto _start;
}
else
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_12 = lean_ctor_get(x_1, 0);
x_13 = lean_ctor_get(x_1, 1);
lean_inc(x_13);
lean_inc(x_12);
lean_dec(x_1);
x_14 = lp_REPL_REPL_Message_of(x_12);
x_15 = lean_ctor_get(x_14, 0);
lean_inc(x_15);
lean_dec_ref(x_14);
x_16 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_16, 0, x_15);
lean_ctor_set(x_16, 1, x_2);
x_1 = x_13;
x_2 = x_16;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandGCAux_spec__1(size_t x_1, size_t x_2, lean_object* x_3) {
_start:
{
uint8_t x_5; 
x_5 = lean_usize_dec_lt(x_2, x_1);
if (x_5 == 0)
{
lean_object* x_6; 
x_6 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_6, 0, x_3);
return x_6;
}
else
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_7 = lean_array_uget(x_3, x_2);
x_8 = lean_box(0);
x_9 = lp_REPL_Lean_Elab_InfoTree_toJson(x_7, x_8);
if (lean_obj_tag(x_9) == 0)
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; size_t x_13; size_t x_14; lean_object* x_15; 
x_10 = lean_ctor_get(x_9, 0);
lean_inc(x_10);
lean_dec_ref(x_9);
x_11 = lean_unsigned_to_nat(0u);
x_12 = lean_array_uset(x_3, x_2, x_11);
x_13 = 1;
x_14 = lean_usize_add(x_2, x_13);
x_15 = lean_array_uset(x_12, x_2, x_10);
x_2 = x_14;
x_3 = x_15;
goto _start;
}
else
{
uint8_t x_17; 
lean_dec_ref(x_3);
x_17 = !lean_is_exclusive(x_9);
if (x_17 == 0)
{
return x_9;
}
else
{
lean_object* x_18; lean_object* x_19; 
x_18 = lean_ctor_get(x_9, 0);
lean_inc(x_18);
lean_dec(x_9);
x_19 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_19, 0, x_18);
return x_19;
}
}
}
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("autoImplicit", 12, 12);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_REPL_runCommandGCAux___closed__0;
x_2 = lean_box(0);
x_3 = l_Lean_Name_str___override(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__2() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = 0;
x_2 = lp_REPL_REPL_runCommandGCAux___closed__1;
x_3 = lean_box(0);
x_4 = l_Lean_KVMap_setBool(x_3, x_2, x_1);
return x_4;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__3() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("maxHeartbeats", 13, 13);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__4() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_REPL_runCommandGCAux___closed__3;
x_2 = lean_box(0);
x_3 = l_Lean_Name_str___override(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__5() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_1 = lean_unsigned_to_nat(800000u);
x_2 = lp_REPL_REPL_runCommandGCAux___closed__4;
x_3 = lp_REPL_REPL_runCommandGCAux___closed__2;
x_4 = l_Lean_KVMap_setNat(x_3, x_2, x_1);
return x_4;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__6() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("full", 4, 4);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__7() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("tactics", 7, 7);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__8() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("original", 8, 8);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__9() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("substantive", 11, 11);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runCommandGCAux___closed__10() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAux(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_4 = lean_ctor_get(x_2, 0);
lean_inc_ref(x_4);
x_5 = lean_ctor_get(x_2, 2);
lean_inc_ref(x_5);
lean_dec_ref(x_2);
x_6 = lean_box(0);
x_7 = lp_REPL_REPL_runCommandGCAux___closed__5;
x_8 = lean_box(0);
lean_inc(x_1);
x_9 = lp_REPL_Lean_Elab_IO_processInput_unsafe__11(x_5, x_1, x_7, x_8);
if (lean_obj_tag(x_9) == 0)
{
lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; 
x_10 = lean_ctor_get(x_9, 0);
lean_inc(x_10);
lean_dec_ref(x_9);
x_11 = lean_ctor_get(x_10, 1);
lean_inc(x_11);
lean_dec(x_10);
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
x_13 = lean_ctor_get(x_11, 1);
lean_inc(x_13);
lean_dec(x_11);
x_14 = lp_REPL_List_mapM_loop___at___00REPL_runCommandGCAux_spec__0(x_12, x_6);
if (lean_obj_tag(x_14) == 0)
{
lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_63; lean_object* x_64; lean_object* x_66; 
x_15 = lean_ctor_get(x_14, 0);
lean_inc(x_15);
if (lean_is_exclusive(x_14)) {
 lean_ctor_release(x_14, 0);
 x_16 = x_14;
} else {
 lean_dec_ref(x_14);
 x_16 = lean_box(0);
}
if (lean_obj_tag(x_1) == 0)
{
x_66 = x_8;
goto block_82;
}
else
{
uint8_t x_83; 
x_83 = !lean_is_exclusive(x_1);
if (x_83 == 0)
{
lean_object* x_84; lean_object* x_85; 
x_84 = lean_ctor_get(x_1, 0);
x_85 = lean_ctor_get(x_84, 0);
lean_inc_ref(x_85);
lean_dec(x_84);
lean_ctor_set(x_1, 0, x_85);
x_66 = x_1;
goto block_82;
}
else
{
lean_object* x_86; lean_object* x_87; lean_object* x_88; 
x_86 = lean_ctor_get(x_1, 0);
lean_inc(x_86);
lean_dec(x_1);
x_87 = lean_ctor_get(x_86, 0);
lean_inc_ref(x_87);
lean_dec(x_86);
x_88 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_88, 0, x_87);
x_66 = x_88;
goto block_82;
}
}
block_24:
{
lean_object* x_21; lean_object* x_22; lean_object* x_23; 
x_21 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_21, 0, x_8);
lean_ctor_set(x_21, 1, x_15);
lean_ctor_set(x_21, 2, x_17);
lean_ctor_set(x_21, 3, x_18);
lean_ctor_set(x_21, 4, x_19);
x_22 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_22, 0, x_21);
if (lean_is_scalar(x_16)) {
 x_23 = lean_alloc_ctor(0, 1, 0);
} else {
 x_23 = x_16;
}
lean_ctor_set(x_23, 0, x_22);
return x_23;
}
block_40:
{
uint8_t x_29; 
x_29 = l_List_isEmpty___redArg(x_28);
if (x_29 == 0)
{
lean_object* x_30; size_t x_31; size_t x_32; lean_object* x_33; 
x_30 = lean_array_mk(x_28);
x_31 = lean_array_size(x_30);
x_32 = 0;
x_33 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandGCAux_spec__1(x_31, x_32, x_30);
if (lean_obj_tag(x_33) == 0)
{
lean_object* x_34; lean_object* x_35; lean_object* x_36; 
x_34 = lean_ctor_get(x_33, 0);
lean_inc(x_34);
lean_dec_ref(x_33);
x_35 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_35, 0, x_34);
x_36 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_36, 0, x_35);
x_17 = x_25;
x_18 = x_27;
x_19 = x_36;
x_20 = lean_box(0);
goto block_24;
}
else
{
uint8_t x_37; 
lean_dec(x_27);
lean_dec(x_25);
lean_dec(x_16);
lean_dec(x_15);
x_37 = !lean_is_exclusive(x_33);
if (x_37 == 0)
{
return x_33;
}
else
{
lean_object* x_38; lean_object* x_39; 
x_38 = lean_ctor_get(x_33, 0);
lean_inc(x_38);
lean_dec(x_33);
x_39 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_39, 0, x_38);
return x_39;
}
}
}
else
{
lean_dec(x_28);
x_17 = x_25;
x_18 = x_27;
x_19 = x_8;
x_20 = lean_box(0);
goto block_24;
}
}
block_62:
{
lean_object* x_44; 
x_44 = lean_ctor_get(x_4, 1);
lean_inc(x_44);
lean_dec_ref(x_4);
if (lean_obj_tag(x_44) == 1)
{
lean_object* x_45; lean_object* x_46; uint8_t x_47; 
x_45 = lean_ctor_get(x_44, 0);
lean_inc(x_45);
lean_dec_ref(x_44);
x_46 = lp_REPL_REPL_runCommandGCAux___closed__6;
x_47 = lean_string_dec_eq(x_45, x_46);
if (x_47 == 0)
{
lean_object* x_48; uint8_t x_49; 
x_48 = lp_REPL_REPL_runCommandGCAux___closed__7;
x_49 = lean_string_dec_eq(x_45, x_48);
if (x_49 == 0)
{
lean_object* x_50; uint8_t x_51; 
x_50 = lp_REPL_REPL_runCommandGCAux___closed__8;
x_51 = lean_string_dec_eq(x_45, x_50);
if (x_51 == 0)
{
lean_object* x_52; uint8_t x_53; 
x_52 = lp_REPL_REPL_runCommandGCAux___closed__9;
x_53 = lean_string_dec_eq(x_45, x_52);
lean_dec(x_45);
if (x_53 == 0)
{
lean_dec(x_13);
x_25 = x_41;
x_26 = lean_box(0);
x_27 = x_42;
x_28 = x_6;
goto block_40;
}
else
{
lean_object* x_54; lean_object* x_55; lean_object* x_56; 
x_54 = lp_REPL_REPL_runCommandGCAux___closed__10;
x_55 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(x_13, x_54);
x_56 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__3(x_55, x_54);
x_25 = x_41;
x_26 = lean_box(0);
x_27 = x_42;
x_28 = x_56;
goto block_40;
}
}
else
{
lean_object* x_57; lean_object* x_58; lean_object* x_59; 
lean_dec(x_45);
x_57 = lp_REPL_REPL_runCommandGCAux___closed__10;
x_58 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(x_13, x_57);
x_59 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__4(x_58, x_57);
x_25 = x_41;
x_26 = lean_box(0);
x_27 = x_42;
x_28 = x_59;
goto block_40;
}
}
else
{
lean_object* x_60; lean_object* x_61; 
lean_dec(x_45);
x_60 = lp_REPL_REPL_runCommandGCAux___closed__10;
x_61 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(x_13, x_60);
x_25 = x_41;
x_26 = lean_box(0);
x_27 = x_42;
x_28 = x_61;
goto block_40;
}
}
else
{
lean_dec(x_45);
x_25 = x_41;
x_26 = lean_box(0);
x_27 = x_42;
x_28 = x_13;
goto block_40;
}
}
else
{
lean_dec(x_44);
lean_dec(x_13);
x_25 = x_41;
x_26 = lean_box(0);
x_27 = x_42;
x_28 = x_6;
goto block_40;
}
}
block_65:
{
x_41 = x_63;
x_42 = x_6;
x_43 = lean_box(0);
goto block_62;
}
block_82:
{
lean_object* x_67; 
lean_inc(x_13);
x_67 = lp_REPL_REPL_sorriesGC(x_13, x_66);
if (lean_obj_tag(x_67) == 0)
{
lean_object* x_68; 
x_68 = lean_ctor_get(x_4, 0);
if (lean_obj_tag(x_68) == 1)
{
lean_object* x_69; uint8_t x_70; 
x_69 = lean_ctor_get(x_68, 0);
x_70 = lean_unbox(x_69);
if (x_70 == 1)
{
lean_object* x_71; lean_object* x_72; 
x_71 = lean_ctor_get(x_67, 0);
lean_inc(x_71);
lean_dec_ref(x_67);
lean_inc(x_13);
x_72 = lp_REPL_REPL_tacticsGC(x_13);
if (lean_obj_tag(x_72) == 0)
{
lean_object* x_73; 
x_73 = lean_ctor_get(x_72, 0);
lean_inc(x_73);
lean_dec_ref(x_72);
x_41 = x_71;
x_42 = x_73;
x_43 = lean_box(0);
goto block_62;
}
else
{
uint8_t x_74; 
lean_dec(x_71);
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_13);
lean_dec_ref(x_4);
x_74 = !lean_is_exclusive(x_72);
if (x_74 == 0)
{
return x_72;
}
else
{
lean_object* x_75; lean_object* x_76; 
x_75 = lean_ctor_get(x_72, 0);
lean_inc(x_75);
lean_dec(x_72);
x_76 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_76, 0, x_75);
return x_76;
}
}
}
else
{
lean_object* x_77; 
x_77 = lean_ctor_get(x_67, 0);
lean_inc(x_77);
lean_dec_ref(x_67);
x_63 = x_77;
x_64 = lean_box(0);
goto block_65;
}
}
else
{
lean_object* x_78; 
x_78 = lean_ctor_get(x_67, 0);
lean_inc(x_78);
lean_dec_ref(x_67);
x_63 = x_78;
x_64 = lean_box(0);
goto block_65;
}
}
else
{
uint8_t x_79; 
lean_dec(x_16);
lean_dec(x_15);
lean_dec(x_13);
lean_dec_ref(x_4);
x_79 = !lean_is_exclusive(x_67);
if (x_79 == 0)
{
return x_67;
}
else
{
lean_object* x_80; lean_object* x_81; 
x_80 = lean_ctor_get(x_67, 0);
lean_inc(x_80);
lean_dec(x_67);
x_81 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_81, 0, x_80);
return x_81;
}
}
}
}
else
{
uint8_t x_89; 
lean_dec(x_13);
lean_dec_ref(x_4);
lean_dec(x_1);
x_89 = !lean_is_exclusive(x_14);
if (x_89 == 0)
{
return x_14;
}
else
{
lean_object* x_90; lean_object* x_91; 
x_90 = lean_ctor_get(x_14, 0);
lean_inc(x_90);
lean_dec(x_14);
x_91 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_91, 0, x_90);
return x_91;
}
}
}
else
{
uint8_t x_92; 
lean_dec_ref(x_4);
lean_dec(x_1);
x_92 = !lean_is_exclusive(x_9);
if (x_92 == 0)
{
lean_object* x_93; lean_object* x_94; lean_object* x_95; 
x_93 = lean_ctor_get(x_9, 0);
x_94 = lean_io_error_to_string(x_93);
x_95 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_95, 0, x_94);
lean_ctor_set_tag(x_9, 0);
lean_ctor_set(x_9, 0, x_95);
return x_9;
}
else
{
lean_object* x_96; lean_object* x_97; lean_object* x_98; lean_object* x_99; 
x_96 = lean_ctor_get(x_9, 0);
lean_inc(x_96);
lean_dec(x_9);
x_97 = lean_io_error_to_string(x_96);
x_98 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_98, 0, x_97);
x_99 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_99, 0, x_98);
return x_99;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_runCommandGCAux_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_List_mapM_loop___at___00REPL_runCommandGCAux_spec__0(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandGCAux_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
size_t x_5; size_t x_6; lean_object* x_7; 
x_5 = lean_unbox_usize(x_1);
lean_dec(x_1);
x_6 = lean_unbox_usize(x_2);
lean_dec(x_2);
x_7 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandGCAux_spec__1(x_5, x_6, x_3);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAux___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_runCommandGCAux(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAuxTimeout(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_5 = lean_alloc_closure((void*)(lp_REPL_REPL_runCommandGCAux___boxed), 3, 2);
lean_closure_set(x_5, 0, x_1);
lean_closure_set(x_5, 1, x_2);
x_6 = lean_unsigned_to_nat(0u);
x_7 = lp_REPL_Lean_Elab_IO_withTimeout___redArg(x_5, x_3, x_6);
if (lean_obj_tag(x_7) == 0)
{
uint8_t x_8; 
x_8 = !lean_is_exclusive(x_7);
if (x_8 == 0)
{
lean_object* x_9; 
x_9 = lean_ctor_get(x_7, 0);
if (lean_obj_tag(x_9) == 0)
{
uint8_t x_10; 
x_10 = !lean_is_exclusive(x_9);
if (x_10 == 0)
{
lean_object* x_11; lean_object* x_12; 
x_11 = lean_ctor_get(x_9, 0);
x_12 = lean_io_error_to_string(x_11);
lean_ctor_set_tag(x_9, 1);
lean_ctor_set(x_9, 0, x_12);
return x_7;
}
else
{
lean_object* x_13; lean_object* x_14; lean_object* x_15; 
x_13 = lean_ctor_get(x_9, 0);
lean_inc(x_13);
lean_dec(x_9);
x_14 = lean_io_error_to_string(x_13);
x_15 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_15, 0, x_14);
lean_ctor_set(x_7, 0, x_15);
return x_7;
}
}
else
{
lean_object* x_16; 
x_16 = lean_ctor_get(x_9, 0);
lean_inc(x_16);
lean_dec_ref(x_9);
lean_ctor_set(x_7, 0, x_16);
return x_7;
}
}
else
{
lean_object* x_17; 
x_17 = lean_ctor_get(x_7, 0);
lean_inc(x_17);
lean_dec(x_7);
if (lean_obj_tag(x_17) == 0)
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; 
x_18 = lean_ctor_get(x_17, 0);
lean_inc(x_18);
if (lean_is_exclusive(x_17)) {
 lean_ctor_release(x_17, 0);
 x_19 = x_17;
} else {
 lean_dec_ref(x_17);
 x_19 = lean_box(0);
}
x_20 = lean_io_error_to_string(x_18);
if (lean_is_scalar(x_19)) {
 x_21 = lean_alloc_ctor(1, 1, 0);
} else {
 x_21 = x_19;
 lean_ctor_set_tag(x_21, 1);
}
lean_ctor_set(x_21, 0, x_20);
x_22 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_22, 0, x_21);
return x_22;
}
else
{
lean_object* x_23; lean_object* x_24; 
x_23 = lean_ctor_get(x_17, 0);
lean_inc(x_23);
lean_dec_ref(x_17);
x_24 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_24, 0, x_23);
return x_24;
}
}
}
else
{
uint8_t x_25; 
x_25 = !lean_is_exclusive(x_7);
if (x_25 == 0)
{
return x_7;
}
else
{
lean_object* x_26; lean_object* x_27; 
x_26 = lean_ctor_get(x_7, 0);
lean_inc(x_26);
lean_dec(x_7);
x_27 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_27, 0, x_26);
return x_27;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandGCAuxTimeout___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_runCommandGCAuxTimeout(x_1, x_2, x_3);
lean_dec(x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tactics___at___00REPL_runCommandAux_spec__1_spec__1(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_5 = l_List_reverse___redArg(x_2);
x_6 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_6, 0, x_5);
lean_ctor_set(x_6, 1, x_3);
x_7 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_7, 0, x_6);
return x_7;
}
else
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; uint8_t x_14; 
x_8 = lean_ctor_get(x_1, 0);
lean_inc(x_8);
x_9 = lean_ctor_get(x_8, 1);
lean_inc(x_9);
x_10 = lean_ctor_get(x_9, 1);
x_11 = lean_ctor_get(x_10, 1);
lean_inc(x_11);
x_12 = lean_ctor_get(x_11, 1);
lean_inc(x_12);
x_13 = lean_ctor_get(x_12, 1);
lean_inc(x_13);
x_14 = !lean_is_exclusive(x_1);
if (x_14 == 0)
{
lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; 
x_15 = lean_ctor_get(x_1, 1);
x_16 = lean_ctor_get(x_1, 0);
lean_dec(x_16);
x_17 = lean_ctor_get(x_8, 0);
lean_inc(x_17);
lean_dec(x_8);
x_18 = lean_ctor_get(x_9, 0);
lean_inc(x_18);
lean_dec(x_9);
x_19 = lean_ctor_get(x_11, 0);
lean_inc(x_19);
lean_dec(x_11);
x_20 = lean_ctor_get(x_12, 0);
lean_inc(x_20);
lean_dec(x_12);
x_21 = lean_ctor_get(x_13, 0);
lean_inc(x_21);
x_22 = lean_ctor_get(x_13, 1);
lean_inc(x_22);
lean_dec(x_13);
x_23 = lean_box(0);
x_24 = lean_box(0);
lean_inc(x_19);
lean_inc(x_17);
x_25 = lp_REPL_REPL_ProofSnapshot_create(x_17, x_23, x_23, x_19, x_24);
if (lean_obj_tag(x_25) == 0)
{
lean_object* x_26; lean_object* x_27; 
x_26 = lean_ctor_get(x_25, 0);
lean_inc(x_26);
lean_dec_ref(x_25);
lean_inc(x_17);
x_27 = l_Lean_Elab_ContextInfo_ppGoals(x_17, x_19);
if (lean_obj_tag(x_27) == 0)
{
lean_object* x_28; lean_object* x_29; 
x_28 = lean_ctor_get(x_27, 0);
lean_inc(x_28);
lean_dec_ref(x_27);
x_29 = lp_REPL_REPL_ppTactic(x_17, x_18);
if (lean_obj_tag(x_29) == 0)
{
lean_object* x_30; lean_object* x_31; uint8_t x_32; 
x_30 = lean_ctor_get(x_29, 0);
lean_inc(x_30);
lean_dec_ref(x_29);
x_31 = lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(x_26, x_3);
x_32 = !lean_is_exclusive(x_31);
if (x_32 == 0)
{
lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; 
x_33 = lean_ctor_get(x_31, 0);
x_34 = lean_ctor_get(x_33, 0);
lean_inc(x_34);
x_35 = lean_ctor_get(x_33, 1);
lean_inc(x_35);
lean_dec(x_33);
x_36 = lean_unsigned_to_nat(120u);
x_37 = lean_unsigned_to_nat(0u);
x_38 = l_Std_Format_pretty(x_28, x_36, x_37, x_37);
x_39 = l_String_trim(x_38);
x_40 = l_Std_Format_pretty(x_30, x_36, x_37, x_37);
lean_ctor_set_tag(x_31, 1);
lean_ctor_set(x_31, 0, x_34);
x_41 = lp_REPL_REPL_Tactic_of(x_39, x_40, x_20, x_21, x_31, x_22);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_41);
{
lean_object* _tmp_0 = x_15;
lean_object* _tmp_1 = x_1;
lean_object* _tmp_2 = x_35;
x_1 = _tmp_0;
x_2 = _tmp_1;
x_3 = _tmp_2;
}
goto _start;
}
else
{
lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; lean_object* x_52; 
x_43 = lean_ctor_get(x_31, 0);
lean_inc(x_43);
lean_dec(x_31);
x_44 = lean_ctor_get(x_43, 0);
lean_inc(x_44);
x_45 = lean_ctor_get(x_43, 1);
lean_inc(x_45);
lean_dec(x_43);
x_46 = lean_unsigned_to_nat(120u);
x_47 = lean_unsigned_to_nat(0u);
x_48 = l_Std_Format_pretty(x_28, x_46, x_47, x_47);
x_49 = l_String_trim(x_48);
x_50 = l_Std_Format_pretty(x_30, x_46, x_47, x_47);
x_51 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_51, 0, x_44);
x_52 = lp_REPL_REPL_Tactic_of(x_49, x_50, x_20, x_21, x_51, x_22);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_52);
{
lean_object* _tmp_0 = x_15;
lean_object* _tmp_1 = x_1;
lean_object* _tmp_2 = x_45;
x_1 = _tmp_0;
x_2 = _tmp_1;
x_3 = _tmp_2;
}
goto _start;
}
}
else
{
uint8_t x_54; 
lean_dec(x_28);
lean_dec(x_26);
lean_dec(x_22);
lean_dec(x_21);
lean_dec(x_20);
lean_free_object(x_1);
lean_dec(x_15);
lean_dec_ref(x_3);
lean_dec(x_2);
x_54 = !lean_is_exclusive(x_29);
if (x_54 == 0)
{
return x_29;
}
else
{
lean_object* x_55; lean_object* x_56; 
x_55 = lean_ctor_get(x_29, 0);
lean_inc(x_55);
lean_dec(x_29);
x_56 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_56, 0, x_55);
return x_56;
}
}
}
else
{
uint8_t x_57; 
lean_dec(x_26);
lean_dec(x_22);
lean_dec(x_21);
lean_dec(x_20);
lean_dec(x_18);
lean_dec(x_17);
lean_free_object(x_1);
lean_dec(x_15);
lean_dec_ref(x_3);
lean_dec(x_2);
x_57 = !lean_is_exclusive(x_27);
if (x_57 == 0)
{
return x_27;
}
else
{
lean_object* x_58; lean_object* x_59; 
x_58 = lean_ctor_get(x_27, 0);
lean_inc(x_58);
lean_dec(x_27);
x_59 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_59, 0, x_58);
return x_59;
}
}
}
else
{
uint8_t x_60; 
lean_dec(x_22);
lean_dec(x_21);
lean_dec(x_20);
lean_dec(x_19);
lean_dec(x_18);
lean_dec(x_17);
lean_free_object(x_1);
lean_dec(x_15);
lean_dec_ref(x_3);
lean_dec(x_2);
x_60 = !lean_is_exclusive(x_25);
if (x_60 == 0)
{
return x_25;
}
else
{
lean_object* x_61; lean_object* x_62; 
x_61 = lean_ctor_get(x_25, 0);
lean_inc(x_61);
lean_dec(x_25);
x_62 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_62, 0, x_61);
return x_62;
}
}
}
else
{
lean_object* x_63; lean_object* x_64; lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_68; lean_object* x_69; lean_object* x_70; lean_object* x_71; lean_object* x_72; 
x_63 = lean_ctor_get(x_1, 1);
lean_inc(x_63);
lean_dec(x_1);
x_64 = lean_ctor_get(x_8, 0);
lean_inc(x_64);
lean_dec(x_8);
x_65 = lean_ctor_get(x_9, 0);
lean_inc(x_65);
lean_dec(x_9);
x_66 = lean_ctor_get(x_11, 0);
lean_inc(x_66);
lean_dec(x_11);
x_67 = lean_ctor_get(x_12, 0);
lean_inc(x_67);
lean_dec(x_12);
x_68 = lean_ctor_get(x_13, 0);
lean_inc(x_68);
x_69 = lean_ctor_get(x_13, 1);
lean_inc(x_69);
lean_dec(x_13);
x_70 = lean_box(0);
x_71 = lean_box(0);
lean_inc(x_66);
lean_inc(x_64);
x_72 = lp_REPL_REPL_ProofSnapshot_create(x_64, x_70, x_70, x_66, x_71);
if (lean_obj_tag(x_72) == 0)
{
lean_object* x_73; lean_object* x_74; 
x_73 = lean_ctor_get(x_72, 0);
lean_inc(x_73);
lean_dec_ref(x_72);
lean_inc(x_64);
x_74 = l_Lean_Elab_ContextInfo_ppGoals(x_64, x_66);
if (lean_obj_tag(x_74) == 0)
{
lean_object* x_75; lean_object* x_76; 
x_75 = lean_ctor_get(x_74, 0);
lean_inc(x_75);
lean_dec_ref(x_74);
x_76 = lp_REPL_REPL_ppTactic(x_64, x_65);
if (lean_obj_tag(x_76) == 0)
{
lean_object* x_77; lean_object* x_78; lean_object* x_79; lean_object* x_80; lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; lean_object* x_85; lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; lean_object* x_90; 
x_77 = lean_ctor_get(x_76, 0);
lean_inc(x_77);
lean_dec_ref(x_76);
x_78 = lp_REPL_REPL_recordProofSnapshot___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__1(x_73, x_3);
x_79 = lean_ctor_get(x_78, 0);
lean_inc(x_79);
if (lean_is_exclusive(x_78)) {
 lean_ctor_release(x_78, 0);
 x_80 = x_78;
} else {
 lean_dec_ref(x_78);
 x_80 = lean_box(0);
}
x_81 = lean_ctor_get(x_79, 0);
lean_inc(x_81);
x_82 = lean_ctor_get(x_79, 1);
lean_inc(x_82);
lean_dec(x_79);
x_83 = lean_unsigned_to_nat(120u);
x_84 = lean_unsigned_to_nat(0u);
x_85 = l_Std_Format_pretty(x_75, x_83, x_84, x_84);
x_86 = l_String_trim(x_85);
x_87 = l_Std_Format_pretty(x_77, x_83, x_84, x_84);
if (lean_is_scalar(x_80)) {
 x_88 = lean_alloc_ctor(1, 1, 0);
} else {
 x_88 = x_80;
 lean_ctor_set_tag(x_88, 1);
}
lean_ctor_set(x_88, 0, x_81);
x_89 = lp_REPL_REPL_Tactic_of(x_86, x_87, x_67, x_68, x_88, x_69);
x_90 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_90, 0, x_89);
lean_ctor_set(x_90, 1, x_2);
x_1 = x_63;
x_2 = x_90;
x_3 = x_82;
goto _start;
}
else
{
lean_object* x_92; lean_object* x_93; lean_object* x_94; 
lean_dec(x_75);
lean_dec(x_73);
lean_dec(x_69);
lean_dec(x_68);
lean_dec(x_67);
lean_dec(x_63);
lean_dec_ref(x_3);
lean_dec(x_2);
x_92 = lean_ctor_get(x_76, 0);
lean_inc(x_92);
if (lean_is_exclusive(x_76)) {
 lean_ctor_release(x_76, 0);
 x_93 = x_76;
} else {
 lean_dec_ref(x_76);
 x_93 = lean_box(0);
}
if (lean_is_scalar(x_93)) {
 x_94 = lean_alloc_ctor(1, 1, 0);
} else {
 x_94 = x_93;
}
lean_ctor_set(x_94, 0, x_92);
return x_94;
}
}
else
{
lean_object* x_95; lean_object* x_96; lean_object* x_97; 
lean_dec(x_73);
lean_dec(x_69);
lean_dec(x_68);
lean_dec(x_67);
lean_dec(x_65);
lean_dec(x_64);
lean_dec(x_63);
lean_dec_ref(x_3);
lean_dec(x_2);
x_95 = lean_ctor_get(x_74, 0);
lean_inc(x_95);
if (lean_is_exclusive(x_74)) {
 lean_ctor_release(x_74, 0);
 x_96 = x_74;
} else {
 lean_dec_ref(x_74);
 x_96 = lean_box(0);
}
if (lean_is_scalar(x_96)) {
 x_97 = lean_alloc_ctor(1, 1, 0);
} else {
 x_97 = x_96;
}
lean_ctor_set(x_97, 0, x_95);
return x_97;
}
}
else
{
lean_object* x_98; lean_object* x_99; lean_object* x_100; 
lean_dec(x_69);
lean_dec(x_68);
lean_dec(x_67);
lean_dec(x_66);
lean_dec(x_65);
lean_dec(x_64);
lean_dec(x_63);
lean_dec_ref(x_3);
lean_dec(x_2);
x_98 = lean_ctor_get(x_72, 0);
lean_inc(x_98);
if (lean_is_exclusive(x_72)) {
 lean_ctor_release(x_72, 0);
 x_99 = x_72;
} else {
 lean_dec_ref(x_72);
 x_99 = lean_box(0);
}
if (lean_is_scalar(x_99)) {
 x_100 = lean_alloc_ctor(1, 1, 0);
} else {
 x_100 = x_99;
}
lean_ctor_set(x_100, 0, x_98);
return x_100;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___at___00REPL_runCommandAux_spec__1(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lp_REPL_REPL_tactics___redArg___closed__1;
x_5 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_tacticsGC_spec__0(x_1, x_4);
x_6 = lean_box(0);
x_7 = lp_REPL_List_mapM_loop___at___00REPL_tactics___at___00REPL_runCommandAux_spec__1_spec__1(x_5, x_6, x_2);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandAux_spec__0(size_t x_1, size_t x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
uint8_t x_6; 
x_6 = lean_usize_dec_lt(x_2, x_1);
if (x_6 == 0)
{
lean_object* x_7; lean_object* x_8; 
x_7 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_7, 0, x_3);
lean_ctor_set(x_7, 1, x_4);
x_8 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_8, 0, x_7);
return x_8;
}
else
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_9 = lean_array_uget(x_3, x_2);
x_10 = lean_box(0);
x_11 = lp_REPL_Lean_Elab_InfoTree_toJson(x_9, x_10);
if (lean_obj_tag(x_11) == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; size_t x_15; size_t x_16; lean_object* x_17; 
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
lean_dec_ref(x_11);
x_13 = lean_unsigned_to_nat(0u);
x_14 = lean_array_uset(x_3, x_2, x_13);
x_15 = 1;
x_16 = lean_usize_add(x_2, x_15);
x_17 = lean_array_uset(x_14, x_2, x_12);
x_2 = x_16;
x_3 = x_17;
goto _start;
}
else
{
uint8_t x_19; 
lean_dec_ref(x_4);
lean_dec_ref(x_3);
x_19 = !lean_is_exclusive(x_11);
if (x_19 == 0)
{
return x_11;
}
else
{
lean_object* x_20; lean_object* x_21; 
x_20 = lean_ctor_get(x_11, 0);
lean_inc(x_20);
lean_dec(x_11);
x_21 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_21, 0, x_20);
return x_21;
}
}
}
}
}
static lean_object* _init_lp_REPL_REPL_runCommandAux___closed__0() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_1 = 0;
x_2 = lean_box(0);
x_3 = lean_unsigned_to_nat(1u);
x_4 = lean_box(0);
x_5 = lean_box(0);
x_6 = lean_unsigned_to_nat(0u);
x_7 = l_Lean_instInhabitedFileMap_default;
x_8 = lp_REPL_REPL_sorries___redArg___closed__0;
x_9 = lean_alloc_ctor(0, 10, 1);
lean_ctor_set(x_9, 0, x_8);
lean_ctor_set(x_9, 1, x_7);
lean_ctor_set(x_9, 2, x_6);
lean_ctor_set(x_9, 3, x_6);
lean_ctor_set(x_9, 4, x_5);
lean_ctor_set(x_9, 5, x_4);
lean_ctor_set(x_9, 6, x_3);
lean_ctor_set(x_9, 7, x_2);
lean_ctor_set(x_9, 8, x_4);
lean_ctor_set(x_9, 9, x_4);
lean_ctor_set_uint8(x_9, sizeof(void*)*10, x_1);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandAux(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_6 = lean_ctor_get(x_3, 0);
lean_inc_ref(x_6);
x_7 = lean_ctor_get(x_3, 2);
lean_inc_ref(x_7);
lean_dec_ref(x_3);
x_8 = lean_box(0);
x_9 = lp_REPL_REPL_runCommandGCAux___closed__5;
x_10 = lean_box(0);
lean_inc(x_2);
x_11 = lp_REPL_Lean_Elab_IO_processInput_unsafe__11(x_7, x_2, x_9, x_10);
if (lean_obj_tag(x_11) == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_12 = lean_ctor_get(x_11, 0);
lean_inc(x_12);
lean_dec_ref(x_11);
x_13 = lean_ctor_get(x_12, 1);
lean_inc(x_13);
x_14 = lean_ctor_get(x_12, 0);
lean_inc(x_14);
lean_dec(x_12);
x_15 = lean_ctor_get(x_13, 0);
lean_inc(x_15);
x_16 = lean_ctor_get(x_13, 1);
lean_inc(x_16);
lean_dec(x_13);
x_17 = lp_REPL_List_mapM_loop___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__0(x_15, x_8, x_4);
if (lean_obj_tag(x_17) == 0)
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; lean_object* x_57; lean_object* x_62; lean_object* x_63; lean_object* x_64; lean_object* x_65; lean_object* x_66; lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; lean_object* x_104; lean_object* x_105; lean_object* x_106; lean_object* x_108; 
x_18 = lean_ctor_get(x_17, 0);
lean_inc(x_18);
lean_dec_ref(x_17);
x_19 = lean_ctor_get(x_18, 0);
lean_inc(x_19);
x_20 = lean_ctor_get(x_18, 1);
lean_inc(x_20);
if (lean_is_exclusive(x_18)) {
 lean_ctor_release(x_18, 0);
 lean_ctor_release(x_18, 1);
 x_21 = x_18;
} else {
 lean_dec_ref(x_18);
 x_21 = lean_box(0);
}
if (lean_obj_tag(x_2) == 0)
{
x_108 = x_10;
goto block_130;
}
else
{
uint8_t x_131; 
x_131 = !lean_is_exclusive(x_2);
if (x_131 == 0)
{
lean_object* x_132; lean_object* x_133; 
x_132 = lean_ctor_get(x_2, 0);
x_133 = lean_ctor_get(x_132, 0);
lean_inc_ref(x_133);
lean_dec(x_132);
lean_ctor_set(x_2, 0, x_133);
x_108 = x_2;
goto block_130;
}
else
{
lean_object* x_134; lean_object* x_135; lean_object* x_136; 
x_134 = lean_ctor_get(x_2, 0);
lean_inc(x_134);
lean_dec(x_2);
x_135 = lean_ctor_get(x_134, 0);
lean_inc_ref(x_135);
lean_dec(x_134);
x_136 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_136, 0, x_135);
x_108 = x_136;
goto block_130;
}
}
block_52:
{
lean_object* x_28; lean_object* x_29; uint8_t x_30; 
if (lean_is_scalar(x_21)) {
 x_28 = lean_alloc_ctor(0, 2, 0);
} else {
 x_28 = x_21;
}
lean_ctor_set(x_28, 0, x_14);
lean_ctor_set(x_28, 1, x_27);
x_29 = lp_REPL_REPL_recordCommandSnapshot___at___00REPL_unpickleCommandSnapshot_spec__0(x_28, x_22);
x_30 = !lean_is_exclusive(x_29);
if (x_30 == 0)
{
lean_object* x_31; uint8_t x_32; 
x_31 = lean_ctor_get(x_29, 0);
x_32 = !lean_is_exclusive(x_31);
if (x_32 == 0)
{
lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; 
x_33 = lean_ctor_get(x_31, 0);
x_34 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_34, 0, x_33);
x_35 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_35, 0, x_34);
lean_ctor_set(x_35, 1, x_19);
lean_ctor_set(x_35, 2, x_26);
lean_ctor_set(x_35, 3, x_24);
lean_ctor_set(x_35, 4, x_23);
x_36 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_36, 0, x_35);
lean_ctor_set(x_31, 0, x_36);
return x_29;
}
else
{
lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; lean_object* x_42; 
x_37 = lean_ctor_get(x_31, 0);
x_38 = lean_ctor_get(x_31, 1);
lean_inc(x_38);
lean_inc(x_37);
lean_dec(x_31);
x_39 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_39, 0, x_37);
x_40 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_40, 0, x_39);
lean_ctor_set(x_40, 1, x_19);
lean_ctor_set(x_40, 2, x_26);
lean_ctor_set(x_40, 3, x_24);
lean_ctor_set(x_40, 4, x_23);
x_41 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_41, 0, x_40);
x_42 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_42, 0, x_41);
lean_ctor_set(x_42, 1, x_38);
lean_ctor_set(x_29, 0, x_42);
return x_29;
}
}
else
{
lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; 
x_43 = lean_ctor_get(x_29, 0);
lean_inc(x_43);
lean_dec(x_29);
x_44 = lean_ctor_get(x_43, 0);
lean_inc(x_44);
x_45 = lean_ctor_get(x_43, 1);
lean_inc(x_45);
if (lean_is_exclusive(x_43)) {
 lean_ctor_release(x_43, 0);
 lean_ctor_release(x_43, 1);
 x_46 = x_43;
} else {
 lean_dec_ref(x_43);
 x_46 = lean_box(0);
}
x_47 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_47, 0, x_44);
x_48 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_48, 0, x_47);
lean_ctor_set(x_48, 1, x_19);
lean_ctor_set(x_48, 2, x_26);
lean_ctor_set(x_48, 3, x_24);
lean_ctor_set(x_48, 4, x_23);
x_49 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_49, 0, x_48);
if (lean_is_scalar(x_46)) {
 x_50 = lean_alloc_ctor(0, 2, 0);
} else {
 x_50 = x_46;
}
lean_ctor_set(x_50, 0, x_49);
lean_ctor_set(x_50, 1, x_45);
x_51 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_51, 0, x_50);
return x_51;
}
}
block_61:
{
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_58; 
x_58 = lp_REPL_REPL_runCommandAux___closed__0;
x_22 = x_56;
x_23 = x_55;
x_24 = x_53;
x_25 = lean_box(0);
x_26 = x_54;
x_27 = x_58;
goto block_52;
}
else
{
lean_object* x_59; lean_object* x_60; 
x_59 = lean_ctor_get(x_1, 0);
lean_inc(x_59);
lean_dec_ref(x_1);
x_60 = lean_ctor_get(x_59, 1);
lean_inc_ref(x_60);
lean_dec(x_59);
x_22 = x_56;
x_23 = x_55;
x_24 = x_53;
x_25 = lean_box(0);
x_26 = x_54;
x_27 = x_60;
goto block_52;
}
}
block_80:
{
uint8_t x_67; 
x_67 = l_List_isEmpty___redArg(x_66);
if (x_67 == 0)
{
lean_object* x_68; size_t x_69; size_t x_70; lean_object* x_71; 
x_68 = lean_array_mk(x_66);
x_69 = lean_array_size(x_68);
x_70 = 0;
x_71 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandAux_spec__0(x_69, x_70, x_68, x_62);
if (lean_obj_tag(x_71) == 0)
{
lean_object* x_72; lean_object* x_73; lean_object* x_74; lean_object* x_75; lean_object* x_76; 
x_72 = lean_ctor_get(x_71, 0);
lean_inc(x_72);
lean_dec_ref(x_71);
x_73 = lean_ctor_get(x_72, 0);
lean_inc(x_73);
x_74 = lean_ctor_get(x_72, 1);
lean_inc(x_74);
lean_dec(x_72);
x_75 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_75, 0, x_73);
x_76 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_76, 0, x_75);
x_53 = x_63;
x_54 = x_64;
x_55 = x_76;
x_56 = x_74;
x_57 = lean_box(0);
goto block_61;
}
else
{
uint8_t x_77; 
lean_dec(x_64);
lean_dec(x_63);
lean_dec(x_21);
lean_dec(x_19);
lean_dec(x_14);
lean_dec(x_1);
x_77 = !lean_is_exclusive(x_71);
if (x_77 == 0)
{
return x_71;
}
else
{
lean_object* x_78; lean_object* x_79; 
x_78 = lean_ctor_get(x_71, 0);
lean_inc(x_78);
lean_dec(x_71);
x_79 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_79, 0, x_78);
return x_79;
}
}
}
else
{
lean_dec(x_66);
x_53 = x_63;
x_54 = x_64;
x_55 = x_10;
x_56 = x_62;
x_57 = lean_box(0);
goto block_61;
}
}
block_103:
{
lean_object* x_85; 
x_85 = lean_ctor_get(x_6, 1);
lean_inc(x_85);
lean_dec_ref(x_6);
if (lean_obj_tag(x_85) == 1)
{
lean_object* x_86; lean_object* x_87; uint8_t x_88; 
x_86 = lean_ctor_get(x_85, 0);
lean_inc(x_86);
lean_dec_ref(x_85);
x_87 = lp_REPL_REPL_runCommandGCAux___closed__6;
x_88 = lean_string_dec_eq(x_86, x_87);
if (x_88 == 0)
{
lean_object* x_89; uint8_t x_90; 
x_89 = lp_REPL_REPL_runCommandGCAux___closed__7;
x_90 = lean_string_dec_eq(x_86, x_89);
if (x_90 == 0)
{
lean_object* x_91; uint8_t x_92; 
x_91 = lp_REPL_REPL_runCommandGCAux___closed__8;
x_92 = lean_string_dec_eq(x_86, x_91);
if (x_92 == 0)
{
lean_object* x_93; uint8_t x_94; 
x_93 = lp_REPL_REPL_runCommandGCAux___closed__9;
x_94 = lean_string_dec_eq(x_86, x_93);
lean_dec(x_86);
if (x_94 == 0)
{
lean_dec(x_16);
x_62 = x_83;
x_63 = x_82;
x_64 = x_81;
x_65 = lean_box(0);
x_66 = x_8;
goto block_80;
}
else
{
lean_object* x_95; lean_object* x_96; lean_object* x_97; 
x_95 = lp_REPL_REPL_runCommandGCAux___closed__10;
x_96 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(x_16, x_95);
x_97 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__3(x_96, x_95);
x_62 = x_83;
x_63 = x_82;
x_64 = x_81;
x_65 = lean_box(0);
x_66 = x_97;
goto block_80;
}
}
else
{
lean_object* x_98; lean_object* x_99; lean_object* x_100; 
lean_dec(x_86);
x_98 = lp_REPL_REPL_runCommandGCAux___closed__10;
x_99 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(x_16, x_98);
x_100 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__4(x_99, x_98);
x_62 = x_83;
x_63 = x_82;
x_64 = x_81;
x_65 = lean_box(0);
x_66 = x_100;
goto block_80;
}
}
else
{
lean_object* x_101; lean_object* x_102; 
lean_dec(x_86);
x_101 = lp_REPL_REPL_runCommandGCAux___closed__10;
x_102 = lp_REPL___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00REPL_runCommandGCAux_spec__2(x_16, x_101);
x_62 = x_83;
x_63 = x_82;
x_64 = x_81;
x_65 = lean_box(0);
x_66 = x_102;
goto block_80;
}
}
else
{
lean_dec(x_86);
x_62 = x_83;
x_63 = x_82;
x_64 = x_81;
x_65 = lean_box(0);
x_66 = x_16;
goto block_80;
}
}
else
{
lean_dec(x_85);
lean_dec(x_16);
x_62 = x_83;
x_63 = x_82;
x_64 = x_81;
x_65 = lean_box(0);
x_66 = x_8;
goto block_80;
}
}
block_107:
{
x_81 = x_104;
x_82 = x_8;
x_83 = x_105;
x_84 = lean_box(0);
goto block_103;
}
block_130:
{
lean_object* x_109; 
lean_inc(x_16);
x_109 = lp_REPL_REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1(x_16, x_108, x_20);
if (lean_obj_tag(x_109) == 0)
{
lean_object* x_110; lean_object* x_111; 
x_110 = lean_ctor_get(x_109, 0);
lean_inc(x_110);
lean_dec_ref(x_109);
x_111 = lean_ctor_get(x_6, 0);
if (lean_obj_tag(x_111) == 1)
{
lean_object* x_112; uint8_t x_113; 
x_112 = lean_ctor_get(x_111, 0);
x_113 = lean_unbox(x_112);
if (x_113 == 1)
{
lean_object* x_114; lean_object* x_115; lean_object* x_116; 
x_114 = lean_ctor_get(x_110, 0);
lean_inc(x_114);
x_115 = lean_ctor_get(x_110, 1);
lean_inc(x_115);
lean_dec(x_110);
lean_inc(x_16);
x_116 = lp_REPL_REPL_tactics___at___00REPL_runCommandAux_spec__1(x_16, x_115);
if (lean_obj_tag(x_116) == 0)
{
lean_object* x_117; lean_object* x_118; lean_object* x_119; 
x_117 = lean_ctor_get(x_116, 0);
lean_inc(x_117);
lean_dec_ref(x_116);
x_118 = lean_ctor_get(x_117, 0);
lean_inc(x_118);
x_119 = lean_ctor_get(x_117, 1);
lean_inc(x_119);
lean_dec(x_117);
x_81 = x_114;
x_82 = x_118;
x_83 = x_119;
x_84 = lean_box(0);
goto block_103;
}
else
{
uint8_t x_120; 
lean_dec(x_114);
lean_dec(x_21);
lean_dec(x_19);
lean_dec(x_16);
lean_dec(x_14);
lean_dec_ref(x_6);
lean_dec(x_1);
x_120 = !lean_is_exclusive(x_116);
if (x_120 == 0)
{
return x_116;
}
else
{
lean_object* x_121; lean_object* x_122; 
x_121 = lean_ctor_get(x_116, 0);
lean_inc(x_121);
lean_dec(x_116);
x_122 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_122, 0, x_121);
return x_122;
}
}
}
else
{
lean_object* x_123; lean_object* x_124; 
x_123 = lean_ctor_get(x_110, 0);
lean_inc(x_123);
x_124 = lean_ctor_get(x_110, 1);
lean_inc(x_124);
lean_dec(x_110);
x_104 = x_123;
x_105 = x_124;
x_106 = lean_box(0);
goto block_107;
}
}
else
{
lean_object* x_125; lean_object* x_126; 
x_125 = lean_ctor_get(x_110, 0);
lean_inc(x_125);
x_126 = lean_ctor_get(x_110, 1);
lean_inc(x_126);
lean_dec(x_110);
x_104 = x_125;
x_105 = x_126;
x_106 = lean_box(0);
goto block_107;
}
}
else
{
uint8_t x_127; 
lean_dec(x_21);
lean_dec(x_19);
lean_dec(x_16);
lean_dec(x_14);
lean_dec_ref(x_6);
lean_dec(x_1);
x_127 = !lean_is_exclusive(x_109);
if (x_127 == 0)
{
return x_109;
}
else
{
lean_object* x_128; lean_object* x_129; 
x_128 = lean_ctor_get(x_109, 0);
lean_inc(x_128);
lean_dec(x_109);
x_129 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_129, 0, x_128);
return x_129;
}
}
}
}
else
{
uint8_t x_137; 
lean_dec(x_16);
lean_dec(x_14);
lean_dec_ref(x_6);
lean_dec(x_2);
lean_dec(x_1);
x_137 = !lean_is_exclusive(x_17);
if (x_137 == 0)
{
return x_17;
}
else
{
lean_object* x_138; lean_object* x_139; 
x_138 = lean_ctor_get(x_17, 0);
lean_inc(x_138);
lean_dec(x_17);
x_139 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_139, 0, x_138);
return x_139;
}
}
}
else
{
uint8_t x_140; 
lean_dec_ref(x_6);
lean_dec(x_2);
lean_dec(x_1);
x_140 = !lean_is_exclusive(x_11);
if (x_140 == 0)
{
lean_object* x_141; lean_object* x_142; lean_object* x_143; lean_object* x_144; 
x_141 = lean_ctor_get(x_11, 0);
x_142 = lean_io_error_to_string(x_141);
x_143 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_143, 0, x_142);
x_144 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_144, 0, x_143);
lean_ctor_set(x_144, 1, x_4);
lean_ctor_set_tag(x_11, 0);
lean_ctor_set(x_11, 0, x_144);
return x_11;
}
else
{
lean_object* x_145; lean_object* x_146; lean_object* x_147; lean_object* x_148; lean_object* x_149; 
x_145 = lean_ctor_get(x_11, 0);
lean_inc(x_145);
lean_dec(x_11);
x_146 = lean_io_error_to_string(x_145);
x_147 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_147, 0, x_146);
x_148 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_148, 0, x_147);
lean_ctor_set(x_148, 1, x_4);
x_149 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_149, 0, x_148);
return x_149;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_tactics___at___00REPL_runCommandAux_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_tactics___at___00REPL_runCommandAux_spec__1(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandAux_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
size_t x_6; size_t x_7; lean_object* x_8; 
x_6 = lean_unbox_usize(x_1);
lean_dec(x_1);
x_7 = lean_unbox_usize(x_2);
lean_dec(x_2);
x_8 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runCommandAux_spec__0(x_6, x_7, x_3, x_4);
return x_8;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_mapM_loop___at___00REPL_tactics___at___00REPL_runCommandAux_spec__1_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_List_mapM_loop___at___00REPL_tactics___at___00REPL_runCommandAux_spec__1_spec__1(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommandAux___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_REPL_runCommandAux(x_1, x_2, x_3, x_4);
return x_6;
}
}
LEAN_EXPORT uint8_t lp_REPL_REPL_runCommand___lam__0(uint8_t x_1, uint8_t x_2) {
_start:
{
if (x_1 == 0)
{
if (x_2 == 0)
{
uint8_t x_3; 
x_3 = 1;
return x_3;
}
else
{
return x_1;
}
}
else
{
return x_2;
}
}
}
static lean_object* _init_lp_REPL_REPL_runCommand___closed__0() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; 
x_1 = 1;
x_2 = lean_box(x_1);
x_3 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_3, 0, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommand___lam__0___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_3; uint8_t x_4; uint8_t x_5; lean_object* x_6; 
x_3 = lean_unbox(x_1);
x_4 = lean_unbox(x_2);
x_5 = lp_REPL_REPL_runCommand___lam__0(x_3, x_4);
x_6 = lean_box(x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommand(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; uint8_t x_7; 
x_4 = lean_ctor_get(x_1, 1);
x_5 = lean_ctor_get(x_1, 3);
lean_inc(x_4);
x_6 = lp_REPL_REPL_getCommandSnapshot(x_4, x_2);
x_7 = !lean_is_exclusive(x_6);
if (x_7 == 0)
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; uint8_t x_11; 
x_8 = lean_ctor_get(x_6, 0);
x_9 = lean_ctor_get(x_8, 0);
lean_inc(x_9);
x_10 = lean_ctor_get(x_9, 1);
x_11 = lean_unbox(x_10);
if (x_11 == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
lean_free_object(x_6);
x_12 = lean_ctor_get(x_8, 1);
lean_inc(x_12);
lean_dec(x_8);
x_13 = lean_ctor_get(x_9, 0);
lean_inc(x_13);
if (lean_is_exclusive(x_9)) {
 lean_ctor_release(x_9, 0);
 lean_ctor_release(x_9, 1);
 x_14 = x_9;
} else {
 lean_dec_ref(x_9);
 x_14 = lean_box(0);
}
x_15 = lean_alloc_closure((void*)(lp_REPL_REPL_runCommand___lam__0___boxed), 2, 0);
if (lean_obj_tag(x_13) == 0)
{
lean_object* x_31; 
x_31 = lean_box(0);
x_16 = x_31;
goto block_30;
}
else
{
lean_object* x_32; lean_object* x_33; lean_object* x_34; 
x_32 = lean_ctor_get(x_13, 0);
x_33 = lean_ctor_get(x_32, 0);
lean_inc_ref(x_33);
x_34 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_34, 0, x_33);
x_16 = x_34;
goto block_30;
}
block_30:
{
lean_object* x_17; uint8_t x_18; 
x_17 = lp_REPL_REPL_runCommand___closed__0;
lean_inc(x_5);
x_18 = l_Option_instDecidableEq___redArg(x_15, x_5, x_17);
if (x_18 == 0)
{
lean_object* x_19; 
lean_dec(x_14);
x_19 = lp_REPL_REPL_runCommandAux(x_13, x_16, x_1, x_12);
return x_19;
}
else
{
lean_object* x_20; 
lean_dec(x_13);
x_20 = lp_REPL_REPL_runCommandGCAux(x_16, x_1);
if (lean_obj_tag(x_20) == 0)
{
uint8_t x_21; 
x_21 = !lean_is_exclusive(x_20);
if (x_21 == 0)
{
lean_object* x_22; lean_object* x_23; 
x_22 = lean_ctor_get(x_20, 0);
if (lean_is_scalar(x_14)) {
 x_23 = lean_alloc_ctor(0, 2, 0);
} else {
 x_23 = x_14;
}
lean_ctor_set(x_23, 0, x_22);
lean_ctor_set(x_23, 1, x_12);
lean_ctor_set(x_20, 0, x_23);
return x_20;
}
else
{
lean_object* x_24; lean_object* x_25; lean_object* x_26; 
x_24 = lean_ctor_get(x_20, 0);
lean_inc(x_24);
lean_dec(x_20);
if (lean_is_scalar(x_14)) {
 x_25 = lean_alloc_ctor(0, 2, 0);
} else {
 x_25 = x_14;
}
lean_ctor_set(x_25, 0, x_24);
lean_ctor_set(x_25, 1, x_12);
x_26 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_26, 0, x_25);
return x_26;
}
}
else
{
uint8_t x_27; 
lean_dec(x_14);
lean_dec(x_12);
x_27 = !lean_is_exclusive(x_20);
if (x_27 == 0)
{
return x_20;
}
else
{
lean_object* x_28; lean_object* x_29; 
x_28 = lean_ctor_get(x_20, 0);
lean_inc(x_28);
lean_dec(x_20);
x_29 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_29, 0, x_28);
return x_29;
}
}
}
}
}
else
{
uint8_t x_35; 
lean_dec_ref(x_1);
x_35 = !lean_is_exclusive(x_9);
if (x_35 == 0)
{
lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; 
x_36 = lean_ctor_get(x_9, 1);
lean_dec(x_36);
x_37 = lean_ctor_get(x_9, 0);
lean_dec(x_37);
x_38 = lean_ctor_get(x_8, 1);
lean_inc(x_38);
lean_dec(x_8);
x_39 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
lean_ctor_set(x_9, 1, x_38);
lean_ctor_set(x_9, 0, x_39);
lean_ctor_set(x_6, 0, x_9);
return x_6;
}
else
{
lean_object* x_40; lean_object* x_41; lean_object* x_42; 
lean_dec(x_9);
x_40 = lean_ctor_get(x_8, 1);
lean_inc(x_40);
lean_dec(x_8);
x_41 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
x_42 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_42, 0, x_41);
lean_ctor_set(x_42, 1, x_40);
lean_ctor_set(x_6, 0, x_42);
return x_6;
}
}
}
else
{
lean_object* x_43; lean_object* x_44; lean_object* x_45; uint8_t x_46; 
x_43 = lean_ctor_get(x_6, 0);
lean_inc(x_43);
lean_dec(x_6);
x_44 = lean_ctor_get(x_43, 0);
lean_inc(x_44);
x_45 = lean_ctor_get(x_44, 1);
x_46 = lean_unbox(x_45);
if (x_46 == 0)
{
lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; 
x_47 = lean_ctor_get(x_43, 1);
lean_inc(x_47);
lean_dec(x_43);
x_48 = lean_ctor_get(x_44, 0);
lean_inc(x_48);
if (lean_is_exclusive(x_44)) {
 lean_ctor_release(x_44, 0);
 lean_ctor_release(x_44, 1);
 x_49 = x_44;
} else {
 lean_dec_ref(x_44);
 x_49 = lean_box(0);
}
x_50 = lean_alloc_closure((void*)(lp_REPL_REPL_runCommand___lam__0___boxed), 2, 0);
if (lean_obj_tag(x_48) == 0)
{
lean_object* x_64; 
x_64 = lean_box(0);
x_51 = x_64;
goto block_63;
}
else
{
lean_object* x_65; lean_object* x_66; lean_object* x_67; 
x_65 = lean_ctor_get(x_48, 0);
x_66 = lean_ctor_get(x_65, 0);
lean_inc_ref(x_66);
x_67 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_67, 0, x_66);
x_51 = x_67;
goto block_63;
}
block_63:
{
lean_object* x_52; uint8_t x_53; 
x_52 = lp_REPL_REPL_runCommand___closed__0;
lean_inc(x_5);
x_53 = l_Option_instDecidableEq___redArg(x_50, x_5, x_52);
if (x_53 == 0)
{
lean_object* x_54; 
lean_dec(x_49);
x_54 = lp_REPL_REPL_runCommandAux(x_48, x_51, x_1, x_47);
return x_54;
}
else
{
lean_object* x_55; 
lean_dec(x_48);
x_55 = lp_REPL_REPL_runCommandGCAux(x_51, x_1);
if (lean_obj_tag(x_55) == 0)
{
lean_object* x_56; lean_object* x_57; lean_object* x_58; lean_object* x_59; 
x_56 = lean_ctor_get(x_55, 0);
lean_inc(x_56);
if (lean_is_exclusive(x_55)) {
 lean_ctor_release(x_55, 0);
 x_57 = x_55;
} else {
 lean_dec_ref(x_55);
 x_57 = lean_box(0);
}
if (lean_is_scalar(x_49)) {
 x_58 = lean_alloc_ctor(0, 2, 0);
} else {
 x_58 = x_49;
}
lean_ctor_set(x_58, 0, x_56);
lean_ctor_set(x_58, 1, x_47);
if (lean_is_scalar(x_57)) {
 x_59 = lean_alloc_ctor(0, 1, 0);
} else {
 x_59 = x_57;
}
lean_ctor_set(x_59, 0, x_58);
return x_59;
}
else
{
lean_object* x_60; lean_object* x_61; lean_object* x_62; 
lean_dec(x_49);
lean_dec(x_47);
x_60 = lean_ctor_get(x_55, 0);
lean_inc(x_60);
if (lean_is_exclusive(x_55)) {
 lean_ctor_release(x_55, 0);
 x_61 = x_55;
} else {
 lean_dec_ref(x_55);
 x_61 = lean_box(0);
}
if (lean_is_scalar(x_61)) {
 x_62 = lean_alloc_ctor(1, 1, 0);
} else {
 x_62 = x_61;
}
lean_ctor_set(x_62, 0, x_60);
return x_62;
}
}
}
}
else
{
lean_object* x_68; lean_object* x_69; lean_object* x_70; lean_object* x_71; lean_object* x_72; 
lean_dec_ref(x_1);
if (lean_is_exclusive(x_44)) {
 lean_ctor_release(x_44, 0);
 lean_ctor_release(x_44, 1);
 x_68 = x_44;
} else {
 lean_dec_ref(x_44);
 x_68 = lean_box(0);
}
x_69 = lean_ctor_get(x_43, 1);
lean_inc(x_69);
lean_dec(x_43);
x_70 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
if (lean_is_scalar(x_68)) {
 x_71 = lean_alloc_ctor(0, 2, 0);
} else {
 x_71 = x_68;
}
lean_ctor_set(x_71, 0, x_70);
lean_ctor_set(x_71, 1, x_69);
x_72 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_72, 0, x_71);
return x_72;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runCommand___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_runCommand(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_Array_replicate___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; lean_object* x_4; 
x_3 = l_List_replicateTR___redArg(x_1, x_2);
x_4 = lean_array_mk(x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_Array_replicate(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_Array_replicate___redArg(x_2, x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7) {
_start:
{
if (lean_obj_tag(x_6) == 0)
{
return x_7;
}
else
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; uint8_t x_21; 
x_8 = lean_ctor_get(x_6, 0);
x_9 = lean_ctor_get(x_6, 1);
x_10 = lean_ctor_get(x_7, 0);
lean_inc(x_10);
x_11 = lean_ctor_get(x_7, 1);
lean_inc(x_11);
if (lean_is_exclusive(x_7)) {
 lean_ctor_release(x_7, 0);
 lean_ctor_release(x_7, 1);
 x_12 = x_7;
} else {
 lean_dec_ref(x_7);
 x_12 = lean_box(0);
}
x_21 = lean_nat_dec_lt(x_8, x_3);
if (x_21 == 0)
{
x_13 = x_4;
goto block_20;
}
else
{
x_13 = x_5;
goto block_20;
}
block_20:
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; 
x_14 = lean_nat_add(x_11, x_1);
x_15 = lean_nat_add(x_14, x_13);
lean_dec(x_14);
lean_inc(x_15);
x_16 = l_Array_extract___redArg(x_2, x_11, x_15);
x_17 = lean_array_push(x_10, x_16);
if (lean_is_scalar(x_12)) {
 x_18 = lean_alloc_ctor(0, 2, 0);
} else {
 x_18 = x_12;
}
lean_ctor_set(x_18, 0, x_17);
lean_ctor_set(x_18, 1, x_15);
x_6 = x_9;
x_7 = x_18;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10) {
_start:
{
lean_object* x_11; 
x_11 = lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___redArg(x_2, x_3, x_4, x_5, x_6, x_8, x_9);
return x_11;
}
}
static lean_object* _init_lp_REPL_REPL_splitArray___redArg___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_splitArray___redArg___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lp_REPL_REPL_splitArray___redArg___closed__0;
x_3 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_3, 0, x_2);
lean_ctor_set(x_3, 1, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_REPL_splitArray___redArg___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_splitArray___redArg___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(1u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_splitArray___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; uint8_t x_4; 
x_3 = lean_unsigned_to_nat(0u);
x_4 = lean_nat_dec_le(x_2, x_3);
if (x_4 == 0)
{
lean_object* x_5; uint8_t x_6; 
x_5 = lean_unsigned_to_nat(1u);
x_6 = lean_nat_dec_eq(x_2, x_5);
if (x_6 == 0)
{
lean_object* x_7; uint8_t x_8; 
x_7 = lean_array_get_size(x_1);
x_8 = lean_nat_dec_eq(x_7, x_3);
if (x_8 == 0)
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; 
x_9 = lean_nat_div(x_7, x_2);
x_10 = lean_nat_mod(x_7, x_2);
x_11 = l_List_range(x_2);
x_12 = lp_REPL_REPL_splitArray___redArg___closed__1;
x_13 = lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___redArg(x_9, x_1, x_10, x_3, x_5, x_11, x_12);
lean_dec(x_11);
lean_dec(x_10);
lean_dec_ref(x_1);
lean_dec(x_9);
x_14 = lean_ctor_get(x_13, 0);
lean_inc(x_14);
lean_dec_ref(x_13);
return x_14;
}
else
{
lean_object* x_15; lean_object* x_16; 
lean_dec_ref(x_1);
x_15 = lp_REPL_REPL_splitArray___redArg___closed__2;
x_16 = lp_REPL_REPL_Array_replicate___redArg(x_2, x_15);
return x_16;
}
}
else
{
lean_object* x_17; lean_object* x_18; 
lean_dec(x_2);
x_17 = lp_REPL_REPL_splitArray___redArg___closed__3;
x_18 = lean_array_push(x_17, x_1);
return x_18;
}
}
else
{
lean_object* x_19; 
lean_dec(x_2);
lean_dec_ref(x_1);
x_19 = lp_REPL_REPL_splitArray___redArg___closed__0;
return x_19;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_splitArray(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_splitArray___redArg(x_2, x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7, lean_object* x_8, lean_object* x_9, lean_object* x_10) {
_start:
{
lean_object* x_11; 
x_11 = lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0(x_1, x_2, x_3, x_4, x_5, x_6, x_7, x_8, x_9, x_10);
lean_dec(x_8);
lean_dec(x_7);
lean_dec(x_6);
lean_dec(x_5);
lean_dec(x_4);
lean_dec_ref(x_3);
lean_dec(x_2);
return x_11;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___redArg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6, lean_object* x_7) {
_start:
{
lean_object* x_8; 
x_8 = lp_REPL_List_forIn_x27_loop___at___00REPL_splitArray_spec__0___redArg(x_1, x_2, x_3, x_4, x_5, x_6, x_7);
lean_dec(x_6);
lean_dec(x_5);
lean_dec(x_4);
lean_dec(x_3);
lean_dec_ref(x_2);
lean_dec(x_1);
return x_8;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifySequential_spec__0(lean_object* x_1, lean_object* x_2, size_t x_3, size_t x_4, lean_object* x_5) {
_start:
{
uint8_t x_7; 
x_7 = lean_usize_dec_lt(x_4, x_3);
if (x_7 == 0)
{
lean_object* x_8; 
lean_dec_ref(x_2);
x_8 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_8, 0, x_5);
return x_8;
}
else
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; 
x_9 = lean_array_uget(x_5, x_4);
x_10 = lean_unsigned_to_nat(0u);
x_11 = lean_array_uset(x_5, x_4, x_10);
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_22; lean_object* x_23; 
lean_inc_ref(x_2);
x_22 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_22, 0, x_2);
x_23 = lp_REPL_REPL_runCommandGCAux(x_22, x_9);
x_12 = x_23;
goto block_21;
}
else
{
lean_object* x_24; lean_object* x_25; lean_object* x_26; 
x_24 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_2);
x_25 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_25, 0, x_2);
x_26 = lp_REPL_REPL_runCommandGCAuxTimeout(x_25, x_9, x_24);
x_12 = x_26;
goto block_21;
}
block_21:
{
if (lean_obj_tag(x_12) == 0)
{
lean_object* x_13; size_t x_14; size_t x_15; lean_object* x_16; 
x_13 = lean_ctor_get(x_12, 0);
lean_inc(x_13);
lean_dec_ref(x_12);
x_14 = 1;
x_15 = lean_usize_add(x_4, x_14);
x_16 = lean_array_uset(x_11, x_4, x_13);
x_4 = x_15;
x_5 = x_16;
goto _start;
}
else
{
uint8_t x_18; 
lean_dec_ref(x_11);
lean_dec_ref(x_2);
x_18 = !lean_is_exclusive(x_12);
if (x_18 == 0)
{
return x_12;
}
else
{
lean_object* x_19; lean_object* x_20; 
x_19 = lean_ctor_get(x_12, 0);
lean_inc(x_19);
lean_dec(x_12);
x_20 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_20, 0, x_19);
return x_20;
}
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifySequential(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
size_t x_5; size_t x_6; lean_object* x_7; 
x_5 = lean_array_size(x_2);
x_6 = 0;
x_7 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifySequential_spec__0(x_3, x_1, x_5, x_6, x_2);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifySequential___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_batchVerifySequential(x_1, x_2, x_3);
lean_dec(x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifySequential_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
size_t x_7; size_t x_8; lean_object* x_9; 
x_7 = lean_unbox_usize(x_3);
lean_dec(x_3);
x_8 = lean_unbox_usize(x_4);
lean_dec(x_4);
x_9 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifySequential_spec__0(x_1, x_2, x_7, x_8, x_5);
lean_dec(x_1);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___lam__0(lean_object* x_1) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; 
x_3 = lean_io_error_to_string(x_1);
x_4 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_4, 0, x_3);
x_5 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_5, 0, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_5; 
if (lean_obj_tag(x_1) == 0)
{
lean_object* x_13; lean_object* x_14; 
x_13 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_13, 0, x_2);
x_14 = lp_REPL_REPL_runCommandGCAux(x_13, x_3);
x_5 = x_14;
goto block_12;
}
else
{
uint8_t x_15; 
x_15 = !lean_is_exclusive(x_1);
if (x_15 == 0)
{
lean_object* x_16; lean_object* x_17; 
x_16 = lean_ctor_get(x_1, 0);
lean_ctor_set(x_1, 0, x_2);
x_17 = lp_REPL_REPL_runCommandGCAuxTimeout(x_1, x_3, x_16);
lean_dec(x_16);
x_5 = x_17;
goto block_12;
}
else
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; 
x_18 = lean_ctor_get(x_1, 0);
lean_inc(x_18);
lean_dec(x_1);
x_19 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_19, 0, x_2);
x_20 = lp_REPL_REPL_runCommandGCAuxTimeout(x_19, x_3, x_18);
lean_dec(x_18);
x_5 = x_20;
goto block_12;
}
}
block_12:
{
if (lean_obj_tag(x_5) == 0)
{
uint8_t x_6; 
x_6 = !lean_is_exclusive(x_5);
if (x_6 == 0)
{
lean_ctor_set_tag(x_5, 1);
return x_5;
}
else
{
lean_object* x_7; lean_object* x_8; 
x_7 = lean_ctor_get(x_5, 0);
lean_inc(x_7);
lean_dec(x_5);
x_8 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_8, 0, x_7);
return x_8;
}
}
else
{
uint8_t x_9; 
x_9 = !lean_is_exclusive(x_5);
if (x_9 == 0)
{
lean_ctor_set_tag(x_5, 0);
return x_5;
}
else
{
lean_object* x_10; lean_object* x_11; 
x_10 = lean_ctor_get(x_5, 0);
lean_inc(x_10);
lean_dec(x_5);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_10);
return x_11;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___lam__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___lam__0(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0(lean_object* x_1, lean_object* x_2, size_t x_3, size_t x_4, lean_object* x_5) {
_start:
{
uint8_t x_7; 
x_7 = lean_usize_dec_lt(x_4, x_3);
if (x_7 == 0)
{
lean_object* x_8; 
lean_dec_ref(x_2);
lean_dec(x_1);
x_8 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_8, 0, x_5);
return x_8;
}
else
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; size_t x_14; size_t x_15; lean_object* x_16; 
x_9 = lean_array_uget(x_5, x_4);
lean_inc_ref(x_2);
lean_inc(x_1);
x_10 = lean_alloc_closure((void*)(lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___lam__0___boxed), 4, 3);
lean_closure_set(x_10, 0, x_1);
lean_closure_set(x_10, 1, x_2);
lean_closure_set(x_10, 2, x_9);
x_11 = lean_unsigned_to_nat(0u);
x_12 = lean_io_as_task(x_10, x_11);
x_13 = lean_array_uset(x_5, x_4, x_11);
x_14 = 1;
x_15 = lean_usize_add(x_4, x_14);
x_16 = lean_array_uset(x_13, x_4, x_12);
x_4 = x_15;
x_5 = x_16;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1(size_t x_1, size_t x_2, lean_object* x_3) {
_start:
{
uint8_t x_5; 
x_5 = lean_usize_dec_lt(x_2, x_1);
if (x_5 == 0)
{
lean_object* x_6; 
x_6 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_6, 0, x_3);
return x_6;
}
else
{
lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_17; 
x_7 = lean_array_uget(x_3, x_2);
x_8 = lean_unsigned_to_nat(0u);
x_9 = lean_array_uset(x_3, x_2, x_8);
x_17 = lean_task_get_own(x_7);
if (lean_obj_tag(x_17) == 0)
{
lean_object* x_18; lean_object* x_19; 
x_18 = lean_ctor_get(x_17, 0);
lean_inc(x_18);
lean_dec_ref(x_17);
x_19 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___lam__0(x_18);
if (lean_obj_tag(x_19) == 0)
{
lean_object* x_20; 
x_20 = lean_ctor_get(x_19, 0);
lean_inc(x_20);
lean_dec_ref(x_19);
x_10 = x_20;
x_11 = lean_box(0);
goto block_16;
}
else
{
lean_object* x_21; lean_object* x_22; 
x_21 = lean_ctor_get(x_19, 0);
lean_inc(x_21);
lean_dec_ref(x_19);
x_22 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___lam__0(x_21);
if (lean_obj_tag(x_22) == 0)
{
lean_object* x_23; 
x_23 = lean_ctor_get(x_22, 0);
lean_inc(x_23);
lean_dec_ref(x_22);
x_10 = x_23;
x_11 = lean_box(0);
goto block_16;
}
else
{
uint8_t x_24; 
lean_dec_ref(x_9);
x_24 = !lean_is_exclusive(x_22);
if (x_24 == 0)
{
return x_22;
}
else
{
lean_object* x_25; lean_object* x_26; 
x_25 = lean_ctor_get(x_22, 0);
lean_inc(x_25);
lean_dec(x_22);
x_26 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_26, 0, x_25);
return x_26;
}
}
}
}
else
{
lean_object* x_27; 
x_27 = lean_ctor_get(x_17, 0);
lean_inc(x_27);
lean_dec_ref(x_17);
x_10 = x_27;
x_11 = lean_box(0);
goto block_16;
}
block_16:
{
size_t x_12; size_t x_13; lean_object* x_14; 
x_12 = 1;
x_13 = lean_usize_add(x_2, x_12);
x_14 = lean_array_uset(x_9, x_2, x_10);
x_2 = x_13;
x_3 = x_14;
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallelNaive(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
size_t x_5; size_t x_6; lean_object* x_7; 
x_5 = lean_array_size(x_2);
x_6 = 0;
x_7 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0(x_3, x_1, x_5, x_6, x_2);
if (lean_obj_tag(x_7) == 0)
{
lean_object* x_8; size_t x_9; lean_object* x_10; 
x_8 = lean_ctor_get(x_7, 0);
lean_inc(x_8);
lean_dec_ref(x_7);
x_9 = lean_array_size(x_8);
x_10 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1(x_9, x_6, x_8);
return x_10;
}
else
{
uint8_t x_11; 
x_11 = !lean_is_exclusive(x_7);
if (x_11 == 0)
{
return x_7;
}
else
{
lean_object* x_12; lean_object* x_13; 
x_12 = lean_ctor_get(x_7, 0);
lean_inc(x_12);
lean_dec(x_7);
x_13 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_13, 0, x_12);
return x_13;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___lam__0___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___lam__0(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallelNaive___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_batchVerifyParrallelNaive(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
size_t x_7; size_t x_8; lean_object* x_9; 
x_7 = lean_unbox_usize(x_3);
lean_dec(x_3);
x_8 = lean_unbox_usize(x_4);
lean_dec(x_4);
x_9 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__0(x_1, x_2, x_7, x_8, x_5);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
size_t x_5; size_t x_6; lean_object* x_7; 
x_5 = lean_unbox_usize(x_1);
lean_dec(x_1);
x_6 = lean_unbox_usize(x_2);
lean_dec(x_2);
x_7 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallelNaive_spec__1(x_5, x_6, x_3);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___lam__0(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lean_io_error_to_string(x_2);
x_5 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_5, 0, x_4);
x_6 = lp_REPL_REPL_Array_replicate___redArg(x_1, x_5);
x_7 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_7, 0, x_6);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_REPL_batchVerifySequential(x_1, x_2, x_3);
if (lean_obj_tag(x_5) == 0)
{
uint8_t x_6; 
x_6 = !lean_is_exclusive(x_5);
if (x_6 == 0)
{
lean_ctor_set_tag(x_5, 1);
return x_5;
}
else
{
lean_object* x_7; lean_object* x_8; 
x_7 = lean_ctor_get(x_5, 0);
lean_inc(x_7);
lean_dec(x_5);
x_8 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_8, 0, x_7);
return x_8;
}
}
else
{
uint8_t x_9; 
x_9 = !lean_is_exclusive(x_5);
if (x_9 == 0)
{
lean_ctor_set_tag(x_5, 0);
return x_5;
}
else
{
lean_object* x_10; lean_object* x_11; 
x_10 = lean_ctor_get(x_5, 0);
lean_inc(x_10);
lean_dec(x_5);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_10);
return x_11;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___lam__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___lam__0(x_1, x_2, x_3);
lean_dec(x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0(lean_object* x_1, lean_object* x_2, size_t x_3, size_t x_4, lean_object* x_5) {
_start:
{
uint8_t x_7; 
x_7 = lean_usize_dec_lt(x_4, x_3);
if (x_7 == 0)
{
lean_object* x_8; 
lean_dec(x_2);
lean_dec_ref(x_1);
x_8 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_8, 0, x_5);
return x_8;
}
else
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; size_t x_14; size_t x_15; lean_object* x_16; 
x_9 = lean_array_uget(x_5, x_4);
lean_inc(x_2);
lean_inc_ref(x_1);
x_10 = lean_alloc_closure((void*)(lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___lam__0___boxed), 4, 3);
lean_closure_set(x_10, 0, x_1);
lean_closure_set(x_10, 1, x_9);
lean_closure_set(x_10, 2, x_2);
x_11 = lean_unsigned_to_nat(0u);
x_12 = lean_io_as_task(x_10, x_11);
x_13 = lean_array_uset(x_5, x_4, x_11);
x_14 = 1;
x_15 = lean_usize_add(x_4, x_14);
x_16 = lean_array_uset(x_13, x_4, x_12);
x_4 = x_15;
x_5 = x_16;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1(lean_object* x_1, lean_object* x_2, size_t x_3, size_t x_4, lean_object* x_5) {
_start:
{
lean_object* x_7; lean_object* x_8; uint8_t x_14; 
x_14 = lean_usize_dec_eq(x_3, x_4);
if (x_14 == 0)
{
lean_object* x_15; lean_object* x_16; 
x_15 = lean_array_uget(x_2, x_3);
x_16 = lean_task_get_own(x_15);
if (lean_obj_tag(x_16) == 0)
{
lean_object* x_17; lean_object* x_18; 
x_17 = lean_ctor_get(x_16, 0);
lean_inc(x_17);
lean_dec_ref(x_16);
lean_inc(x_1);
x_18 = lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___lam__0(x_1, x_17);
if (lean_obj_tag(x_18) == 0)
{
lean_object* x_19; 
x_19 = lean_ctor_get(x_18, 0);
lean_inc(x_19);
lean_dec_ref(x_18);
x_7 = x_19;
x_8 = lean_box(0);
goto block_13;
}
else
{
lean_object* x_20; lean_object* x_21; 
x_20 = lean_ctor_get(x_18, 0);
lean_inc(x_20);
lean_dec_ref(x_18);
lean_inc(x_1);
x_21 = lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___lam__0(x_1, x_20);
if (lean_obj_tag(x_21) == 0)
{
lean_object* x_22; 
x_22 = lean_ctor_get(x_21, 0);
lean_inc(x_22);
lean_dec_ref(x_21);
x_7 = x_22;
x_8 = lean_box(0);
goto block_13;
}
else
{
lean_dec_ref(x_5);
lean_dec(x_1);
return x_21;
}
}
}
else
{
lean_object* x_23; 
x_23 = lean_ctor_get(x_16, 0);
lean_inc(x_23);
lean_dec_ref(x_16);
x_7 = x_23;
x_8 = lean_box(0);
goto block_13;
}
}
else
{
lean_object* x_24; 
lean_dec(x_1);
x_24 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_24, 0, x_5);
return x_24;
}
block_13:
{
lean_object* x_9; size_t x_10; size_t x_11; 
x_9 = l_Array_append___redArg(x_5, x_7);
lean_dec_ref(x_7);
x_10 = 1;
x_11 = lean_usize_add(x_3, x_10);
x_3 = x_11;
x_5 = x_9;
goto _start;
}
}
}
static lean_object* _init_lp_REPL_REPL_batchVerifyParrallel___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = l_Array_empty(lean_box(0));
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallel(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_6; 
if (lean_obj_tag(x_3) == 0)
{
lean_object* x_34; lean_object* x_35; uint8_t x_36; 
x_34 = lean_unsigned_to_nat(50u);
x_35 = lean_array_get_size(x_2);
x_36 = lean_nat_dec_le(x_34, x_35);
if (x_36 == 0)
{
x_6 = x_34;
goto block_33;
}
else
{
x_6 = x_35;
goto block_33;
}
}
else
{
lean_object* x_37; 
x_37 = lean_ctor_get(x_3, 0);
lean_inc(x_37);
lean_dec_ref(x_3);
x_6 = x_37;
goto block_33;
}
block_33:
{
lean_object* x_7; size_t x_8; size_t x_9; lean_object* x_10; 
lean_inc(x_6);
x_7 = lp_REPL_REPL_splitArray___redArg(x_2, x_6);
x_8 = lean_array_size(x_7);
x_9 = 0;
x_10 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0(x_1, x_4, x_8, x_9, x_7);
if (lean_obj_tag(x_10) == 0)
{
uint8_t x_11; 
x_11 = !lean_is_exclusive(x_10);
if (x_11 == 0)
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; uint8_t x_16; 
x_12 = lean_ctor_get(x_10, 0);
x_13 = lp_REPL_REPL_batchVerifyParrallel___closed__0;
x_14 = lean_unsigned_to_nat(0u);
x_15 = lean_array_get_size(x_12);
x_16 = lean_nat_dec_lt(x_14, x_15);
if (x_16 == 0)
{
lean_dec(x_12);
lean_dec(x_6);
lean_ctor_set(x_10, 0, x_13);
return x_10;
}
else
{
uint8_t x_17; 
x_17 = lean_nat_dec_le(x_15, x_15);
if (x_17 == 0)
{
lean_dec(x_12);
lean_dec(x_6);
lean_ctor_set(x_10, 0, x_13);
return x_10;
}
else
{
size_t x_18; lean_object* x_19; 
lean_free_object(x_10);
x_18 = lean_usize_of_nat(x_15);
x_19 = lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1(x_6, x_12, x_9, x_18, x_13);
lean_dec(x_12);
return x_19;
}
}
}
else
{
lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; uint8_t x_24; 
x_20 = lean_ctor_get(x_10, 0);
lean_inc(x_20);
lean_dec(x_10);
x_21 = lp_REPL_REPL_batchVerifyParrallel___closed__0;
x_22 = lean_unsigned_to_nat(0u);
x_23 = lean_array_get_size(x_20);
x_24 = lean_nat_dec_lt(x_22, x_23);
if (x_24 == 0)
{
lean_object* x_25; 
lean_dec(x_20);
lean_dec(x_6);
x_25 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_25, 0, x_21);
return x_25;
}
else
{
uint8_t x_26; 
x_26 = lean_nat_dec_le(x_23, x_23);
if (x_26 == 0)
{
lean_object* x_27; 
lean_dec(x_20);
lean_dec(x_6);
x_27 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_27, 0, x_21);
return x_27;
}
else
{
size_t x_28; lean_object* x_29; 
x_28 = lean_usize_of_nat(x_23);
x_29 = lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1(x_6, x_20, x_9, x_28, x_21);
lean_dec(x_20);
return x_29;
}
}
}
}
else
{
uint8_t x_30; 
lean_dec(x_6);
x_30 = !lean_is_exclusive(x_10);
if (x_30 == 0)
{
return x_10;
}
else
{
lean_object* x_31; lean_object* x_32; 
x_31 = lean_ctor_get(x_10, 0);
lean_inc(x_31);
lean_dec(x_10);
x_32 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_32, 0, x_31);
return x_32;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___lam__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___lam__0(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
size_t x_7; size_t x_8; lean_object* x_9; 
x_7 = lean_unbox_usize(x_3);
lean_dec(x_3);
x_8 = lean_unbox_usize(x_4);
lean_dec(x_4);
x_9 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_batchVerifyParrallel_spec__0(x_1, x_2, x_7, x_8, x_5);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
size_t x_7; size_t x_8; lean_object* x_9; 
x_7 = lean_unbox_usize(x_3);
lean_dec(x_3);
x_8 = lean_unbox_usize(x_4);
lean_dec(x_4);
x_9 = lp_REPL___private_Init_Data_Array_Basic_0__Array_foldlMUnsafe_fold___at___00REPL_batchVerifyParrallel_spec__1(x_1, x_2, x_7, x_8, x_5);
lean_dec_ref(x_2);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_batchVerifyParrallel___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_REPL_batchVerifyParrallel(x_1, x_2, x_3, x_4);
return x_6;
}
}
static lean_object* _init_lp_REPL_REPL_processFile___closed__0() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; 
x_1 = 0;
x_2 = lean_box(x_1);
x_3 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_3, 0, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_processFile(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_11; lean_object* x_12; lean_object* x_13; 
x_11 = lean_ctor_get(x_1, 0);
x_12 = lean_ctor_get(x_1, 1);
x_13 = l_IO_FS_readFile(x_12);
if (lean_obj_tag(x_13) == 0)
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; 
x_14 = lean_ctor_get(x_13, 0);
lean_inc(x_14);
lean_dec_ref(x_13);
x_15 = lean_box(0);
x_16 = lp_REPL_REPL_processFile___closed__0;
lean_inc_ref(x_11);
x_17 = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(x_17, 0, x_11);
lean_ctor_set(x_17, 1, x_15);
lean_ctor_set(x_17, 2, x_14);
lean_ctor_set(x_17, 3, x_16);
lean_inc_ref(x_2);
x_18 = lp_REPL_REPL_runCommand(x_17, x_2);
if (lean_obj_tag(x_18) == 0)
{
lean_dec_ref(x_2);
return x_18;
}
else
{
lean_object* x_19; 
x_19 = lean_ctor_get(x_18, 0);
lean_inc(x_19);
lean_dec_ref(x_18);
x_4 = x_19;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_20; 
x_20 = lean_ctor_get(x_13, 0);
lean_inc(x_20);
lean_dec_ref(x_13);
x_4 = x_20;
x_5 = lean_box(0);
goto block_10;
}
block_10:
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; 
x_6 = lean_io_error_to_string(x_4);
x_7 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_7, 0, x_6);
x_8 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_8, 0, x_7);
lean_ctor_set(x_8, 1, x_2);
x_9 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_9, 0, x_8);
return x_9;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_processFile___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_processFile(x_1, x_2);
lean_dec_ref(x_1);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0(lean_object* x_1, uint8_t x_2, size_t x_3, size_t x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; 
x_6 = lean_usize_dec_lt(x_4, x_3);
if (x_6 == 0)
{
lean_dec_ref(x_1);
return x_5;
}
else
{
lean_object* x_7; uint8_t x_8; 
x_7 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_7);
x_8 = !lean_is_exclusive(x_7);
if (x_8 == 0)
{
lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; size_t x_18; size_t x_19; lean_object* x_20; 
x_9 = lean_ctor_get(x_7, 3);
lean_dec(x_9);
x_10 = lean_ctor_get(x_7, 2);
lean_dec(x_10);
x_11 = lean_ctor_get(x_7, 1);
lean_dec(x_11);
x_12 = lean_array_uget(x_5, x_4);
x_13 = lean_unsigned_to_nat(0u);
x_14 = lean_array_uset(x_5, x_4, x_13);
x_15 = lean_box(0);
x_16 = lean_box(x_2);
x_17 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_17, 0, x_16);
lean_ctor_set(x_7, 3, x_17);
lean_ctor_set(x_7, 2, x_12);
lean_ctor_set(x_7, 1, x_15);
x_18 = 1;
x_19 = lean_usize_add(x_4, x_18);
x_20 = lean_array_uset(x_14, x_4, x_7);
x_4 = x_19;
x_5 = x_20;
goto _start;
}
else
{
lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; size_t x_30; size_t x_31; lean_object* x_32; 
x_22 = lean_ctor_get(x_7, 0);
lean_inc(x_22);
lean_dec(x_7);
x_23 = lean_array_uget(x_5, x_4);
x_24 = lean_unsigned_to_nat(0u);
x_25 = lean_array_uset(x_5, x_4, x_24);
x_26 = lean_box(0);
x_27 = lean_box(x_2);
x_28 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_28, 0, x_27);
x_29 = lean_alloc_ctor(0, 4, 0);
lean_ctor_set(x_29, 0, x_22);
lean_ctor_set(x_29, 1, x_26);
lean_ctor_set(x_29, 2, x_23);
lean_ctor_set(x_29, 3, x_28);
x_30 = 1;
x_31 = lean_usize_add(x_4, x_30);
x_32 = lean_array_uset(x_25, x_4, x_29);
x_4 = x_31;
x_5 = x_32;
goto _start;
}
}
}
}
static lean_object* _init_lp_REPL_REPL_runBatchVerify___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("naive", 5, 5);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runBatchVerify___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("parrallel", 9, 9);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runBatchVerify___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("<input>", 7, 7);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runBatchVerify___closed__3() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_sorries___redArg___closed__0;
x_2 = lean_string_utf8_byte_size(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_runBatchVerify___closed__4() {
_start:
{
lean_object* x_1; uint8_t x_2; lean_object* x_3; lean_object* x_4; lean_object* x_5; 
x_1 = lp_REPL_REPL_runBatchVerify___closed__3;
x_2 = 1;
x_3 = lp_REPL_REPL_runBatchVerify___closed__2;
x_4 = lp_REPL_REPL_sorries___redArg___closed__0;
x_5 = l_Lean_Parser_mkInputContext___redArg(x_4, x_3, x_2, x_1);
return x_5;
}
}
static lean_object* _init_lp_REPL_REPL_runBatchVerify___closed__5() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_REPL_runBatchVerify___closed__6() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0;
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runBatchVerify(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_25; 
x_4 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_4);
x_5 = lean_ctor_get(x_1, 1);
x_6 = lean_ctor_get(x_1, 2);
lean_inc_ref(x_6);
lean_inc(x_5);
x_25 = lp_REPL_REPL_getCommandSnapshot(x_5, x_2);
if (lean_obj_tag(x_25) == 0)
{
uint8_t x_26; 
x_26 = !lean_is_exclusive(x_25);
if (x_26 == 0)
{
lean_object* x_27; uint8_t x_28; 
x_27 = lean_ctor_get(x_25, 0);
x_28 = !lean_is_exclusive(x_27);
if (x_28 == 0)
{
lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; lean_object* x_36; uint8_t x_94; 
x_29 = lean_ctor_get(x_27, 0);
x_30 = lean_ctor_get(x_27, 1);
x_31 = lean_ctor_get(x_29, 0);
lean_inc(x_31);
x_32 = lean_ctor_get(x_29, 1);
lean_inc(x_32);
if (lean_is_exclusive(x_29)) {
 lean_ctor_release(x_29, 0);
 lean_ctor_release(x_29, 1);
 x_33 = x_29;
} else {
 lean_dec_ref(x_29);
 x_33 = lean_box(0);
}
x_94 = lean_unbox(x_32);
if (x_94 == 0)
{
lean_free_object(x_27);
lean_free_object(x_25);
if (lean_obj_tag(x_31) == 0)
{
uint8_t x_95; lean_object* x_96; lean_object* x_97; 
x_95 = 1;
x_96 = lp_REPL_REPL_runBatchVerify___closed__4;
x_97 = l_Lean_Parser_parseHeader(x_96);
if (lean_obj_tag(x_97) == 0)
{
lean_object* x_98; lean_object* x_99; lean_object* x_100; lean_object* x_101; lean_object* x_102; uint32_t x_103; lean_object* x_104; lean_object* x_105; lean_object* x_106; lean_object* x_107; uint8_t x_108; lean_object* x_109; lean_object* x_110; uint8_t x_111; lean_object* x_112; 
x_98 = lean_ctor_get(x_97, 0);
lean_inc(x_98);
lean_dec_ref(x_97);
x_99 = lean_ctor_get(x_98, 1);
lean_inc(x_99);
x_100 = lean_ctor_get(x_98, 0);
lean_inc(x_100);
lean_dec(x_98);
x_101 = lean_ctor_get(x_99, 1);
lean_inc(x_101);
lean_dec(x_99);
x_102 = lean_box(0);
x_103 = 0;
x_104 = lp_REPL_REPL_runBatchVerify___closed__5;
x_105 = lean_box(0);
x_106 = l_Lean_Elab_HeaderSyntax_startPos(x_100);
lean_inc(x_100);
x_107 = l_Lean_Elab_HeaderSyntax_imports(x_100, x_95);
x_108 = l_Lean_Elab_HeaderSyntax_isModule(x_100);
lean_dec(x_100);
x_109 = lean_box(0);
x_110 = lean_box(1);
x_111 = lean_unbox(x_32);
x_112 = l_Lean_Elab_processHeaderCore(x_106, x_107, x_108, x_102, x_101, x_96, x_103, x_104, x_111, x_105, x_109, x_110);
lean_dec(x_106);
if (lean_obj_tag(x_112) == 0)
{
lean_object* x_113; lean_object* x_114; lean_object* x_115; lean_object* x_116; 
x_113 = lean_ctor_get(x_112, 0);
lean_inc(x_113);
lean_dec_ref(x_112);
x_114 = lean_ctor_get(x_113, 0);
lean_inc(x_114);
x_115 = lean_ctor_get(x_113, 1);
lean_inc(x_115);
lean_dec(x_113);
x_116 = l_Lean_Elab_Command_mkState(x_114, x_115, x_102);
x_34 = x_116;
x_35 = x_30;
x_36 = lean_box(0);
goto block_93;
}
else
{
uint8_t x_117; 
lean_dec(x_33);
lean_dec(x_32);
lean_dec(x_30);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_117 = !lean_is_exclusive(x_112);
if (x_117 == 0)
{
return x_112;
}
else
{
lean_object* x_118; lean_object* x_119; 
x_118 = lean_ctor_get(x_112, 0);
lean_inc(x_118);
lean_dec(x_112);
x_119 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_119, 0, x_118);
return x_119;
}
}
}
else
{
uint8_t x_120; 
lean_dec(x_33);
lean_dec(x_32);
lean_dec(x_30);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_120 = !lean_is_exclusive(x_97);
if (x_120 == 0)
{
return x_97;
}
else
{
lean_object* x_121; lean_object* x_122; 
x_121 = lean_ctor_get(x_97, 0);
lean_inc(x_121);
lean_dec(x_97);
x_122 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_122, 0, x_121);
return x_122;
}
}
}
else
{
lean_object* x_123; lean_object* x_124; 
x_123 = lean_ctor_get(x_31, 0);
lean_inc(x_123);
lean_dec_ref(x_31);
x_124 = lean_ctor_get(x_123, 0);
lean_inc_ref(x_124);
lean_dec(x_123);
x_34 = x_124;
x_35 = x_30;
x_36 = lean_box(0);
goto block_93;
}
}
else
{
lean_object* x_125; 
lean_dec(x_33);
lean_dec(x_32);
lean_dec(x_31);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_125 = lp_REPL_REPL_runBatchVerify___closed__6;
lean_ctor_set(x_27, 0, x_125);
return x_25;
}
block_93:
{
lean_object* x_37; lean_object* x_38; lean_object* x_39; size_t x_40; size_t x_41; uint8_t x_42; lean_object* x_43; 
x_37 = lean_ctor_get(x_4, 1);
lean_inc(x_37);
x_38 = lean_ctor_get(x_4, 2);
x_39 = lean_ctor_get(x_4, 3);
x_40 = lean_array_size(x_6);
x_41 = 0;
x_42 = lean_unbox(x_32);
lean_dec(x_32);
x_43 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0(x_1, x_42, x_40, x_41, x_6);
if (lean_obj_tag(x_37) == 0)
{
lean_dec(x_33);
x_7 = x_34;
x_8 = x_43;
x_9 = x_35;
x_10 = lean_box(0);
goto block_24;
}
else
{
uint8_t x_44; 
x_44 = !lean_is_exclusive(x_37);
if (x_44 == 0)
{
lean_object* x_45; lean_object* x_46; uint8_t x_47; 
x_45 = lean_ctor_get(x_37, 0);
x_46 = lp_REPL_REPL_runBatchVerify___closed__0;
x_47 = lean_string_dec_eq(x_45, x_46);
if (x_47 == 0)
{
lean_object* x_48; uint8_t x_49; 
x_48 = lp_REPL_REPL_runBatchVerify___closed__1;
x_49 = lean_string_dec_eq(x_45, x_48);
lean_dec(x_45);
if (x_49 == 0)
{
lean_free_object(x_37);
lean_dec(x_33);
x_7 = x_34;
x_8 = x_43;
x_9 = x_35;
x_10 = lean_box(0);
goto block_24;
}
else
{
lean_object* x_50; 
lean_inc(x_39);
lean_inc(x_38);
lean_dec_ref(x_4);
x_50 = lp_REPL_REPL_batchVerifyParrallel(x_34, x_43, x_38, x_39);
if (lean_obj_tag(x_50) == 0)
{
uint8_t x_51; 
x_51 = !lean_is_exclusive(x_50);
if (x_51 == 0)
{
lean_object* x_52; lean_object* x_53; 
x_52 = lean_ctor_get(x_50, 0);
lean_ctor_set_tag(x_37, 0);
lean_ctor_set(x_37, 0, x_52);
if (lean_is_scalar(x_33)) {
 x_53 = lean_alloc_ctor(0, 2, 0);
} else {
 x_53 = x_33;
}
lean_ctor_set(x_53, 0, x_37);
lean_ctor_set(x_53, 1, x_35);
lean_ctor_set(x_50, 0, x_53);
return x_50;
}
else
{
lean_object* x_54; lean_object* x_55; lean_object* x_56; 
x_54 = lean_ctor_get(x_50, 0);
lean_inc(x_54);
lean_dec(x_50);
lean_ctor_set_tag(x_37, 0);
lean_ctor_set(x_37, 0, x_54);
if (lean_is_scalar(x_33)) {
 x_55 = lean_alloc_ctor(0, 2, 0);
} else {
 x_55 = x_33;
}
lean_ctor_set(x_55, 0, x_37);
lean_ctor_set(x_55, 1, x_35);
x_56 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_56, 0, x_55);
return x_56;
}
}
else
{
uint8_t x_57; 
lean_free_object(x_37);
lean_dec_ref(x_35);
lean_dec(x_33);
x_57 = !lean_is_exclusive(x_50);
if (x_57 == 0)
{
return x_50;
}
else
{
lean_object* x_58; lean_object* x_59; 
x_58 = lean_ctor_get(x_50, 0);
lean_inc(x_58);
lean_dec(x_50);
x_59 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_59, 0, x_58);
return x_59;
}
}
}
}
else
{
lean_object* x_60; 
lean_dec(x_45);
lean_inc(x_39);
lean_dec_ref(x_4);
x_60 = lp_REPL_REPL_batchVerifyParrallelNaive(x_34, x_43, x_39);
if (lean_obj_tag(x_60) == 0)
{
uint8_t x_61; 
x_61 = !lean_is_exclusive(x_60);
if (x_61 == 0)
{
lean_object* x_62; lean_object* x_63; 
x_62 = lean_ctor_get(x_60, 0);
lean_ctor_set_tag(x_37, 0);
lean_ctor_set(x_37, 0, x_62);
if (lean_is_scalar(x_33)) {
 x_63 = lean_alloc_ctor(0, 2, 0);
} else {
 x_63 = x_33;
}
lean_ctor_set(x_63, 0, x_37);
lean_ctor_set(x_63, 1, x_35);
lean_ctor_set(x_60, 0, x_63);
return x_60;
}
else
{
lean_object* x_64; lean_object* x_65; lean_object* x_66; 
x_64 = lean_ctor_get(x_60, 0);
lean_inc(x_64);
lean_dec(x_60);
lean_ctor_set_tag(x_37, 0);
lean_ctor_set(x_37, 0, x_64);
if (lean_is_scalar(x_33)) {
 x_65 = lean_alloc_ctor(0, 2, 0);
} else {
 x_65 = x_33;
}
lean_ctor_set(x_65, 0, x_37);
lean_ctor_set(x_65, 1, x_35);
x_66 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_66, 0, x_65);
return x_66;
}
}
else
{
uint8_t x_67; 
lean_free_object(x_37);
lean_dec_ref(x_35);
lean_dec(x_33);
x_67 = !lean_is_exclusive(x_60);
if (x_67 == 0)
{
return x_60;
}
else
{
lean_object* x_68; lean_object* x_69; 
x_68 = lean_ctor_get(x_60, 0);
lean_inc(x_68);
lean_dec(x_60);
x_69 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_69, 0, x_68);
return x_69;
}
}
}
}
else
{
lean_object* x_70; lean_object* x_71; uint8_t x_72; 
x_70 = lean_ctor_get(x_37, 0);
lean_inc(x_70);
lean_dec(x_37);
x_71 = lp_REPL_REPL_runBatchVerify___closed__0;
x_72 = lean_string_dec_eq(x_70, x_71);
if (x_72 == 0)
{
lean_object* x_73; uint8_t x_74; 
x_73 = lp_REPL_REPL_runBatchVerify___closed__1;
x_74 = lean_string_dec_eq(x_70, x_73);
lean_dec(x_70);
if (x_74 == 0)
{
lean_dec(x_33);
x_7 = x_34;
x_8 = x_43;
x_9 = x_35;
x_10 = lean_box(0);
goto block_24;
}
else
{
lean_object* x_75; 
lean_inc(x_39);
lean_inc(x_38);
lean_dec_ref(x_4);
x_75 = lp_REPL_REPL_batchVerifyParrallel(x_34, x_43, x_38, x_39);
if (lean_obj_tag(x_75) == 0)
{
lean_object* x_76; lean_object* x_77; lean_object* x_78; lean_object* x_79; lean_object* x_80; 
x_76 = lean_ctor_get(x_75, 0);
lean_inc(x_76);
if (lean_is_exclusive(x_75)) {
 lean_ctor_release(x_75, 0);
 x_77 = x_75;
} else {
 lean_dec_ref(x_75);
 x_77 = lean_box(0);
}
x_78 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_78, 0, x_76);
if (lean_is_scalar(x_33)) {
 x_79 = lean_alloc_ctor(0, 2, 0);
} else {
 x_79 = x_33;
}
lean_ctor_set(x_79, 0, x_78);
lean_ctor_set(x_79, 1, x_35);
if (lean_is_scalar(x_77)) {
 x_80 = lean_alloc_ctor(0, 1, 0);
} else {
 x_80 = x_77;
}
lean_ctor_set(x_80, 0, x_79);
return x_80;
}
else
{
lean_object* x_81; lean_object* x_82; lean_object* x_83; 
lean_dec_ref(x_35);
lean_dec(x_33);
x_81 = lean_ctor_get(x_75, 0);
lean_inc(x_81);
if (lean_is_exclusive(x_75)) {
 lean_ctor_release(x_75, 0);
 x_82 = x_75;
} else {
 lean_dec_ref(x_75);
 x_82 = lean_box(0);
}
if (lean_is_scalar(x_82)) {
 x_83 = lean_alloc_ctor(1, 1, 0);
} else {
 x_83 = x_82;
}
lean_ctor_set(x_83, 0, x_81);
return x_83;
}
}
}
else
{
lean_object* x_84; 
lean_dec(x_70);
lean_inc(x_39);
lean_dec_ref(x_4);
x_84 = lp_REPL_REPL_batchVerifyParrallelNaive(x_34, x_43, x_39);
if (lean_obj_tag(x_84) == 0)
{
lean_object* x_85; lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; 
x_85 = lean_ctor_get(x_84, 0);
lean_inc(x_85);
if (lean_is_exclusive(x_84)) {
 lean_ctor_release(x_84, 0);
 x_86 = x_84;
} else {
 lean_dec_ref(x_84);
 x_86 = lean_box(0);
}
x_87 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_87, 0, x_85);
if (lean_is_scalar(x_33)) {
 x_88 = lean_alloc_ctor(0, 2, 0);
} else {
 x_88 = x_33;
}
lean_ctor_set(x_88, 0, x_87);
lean_ctor_set(x_88, 1, x_35);
if (lean_is_scalar(x_86)) {
 x_89 = lean_alloc_ctor(0, 1, 0);
} else {
 x_89 = x_86;
}
lean_ctor_set(x_89, 0, x_88);
return x_89;
}
else
{
lean_object* x_90; lean_object* x_91; lean_object* x_92; 
lean_dec_ref(x_35);
lean_dec(x_33);
x_90 = lean_ctor_get(x_84, 0);
lean_inc(x_90);
if (lean_is_exclusive(x_84)) {
 lean_ctor_release(x_84, 0);
 x_91 = x_84;
} else {
 lean_dec_ref(x_84);
 x_91 = lean_box(0);
}
if (lean_is_scalar(x_91)) {
 x_92 = lean_alloc_ctor(1, 1, 0);
} else {
 x_92 = x_91;
}
lean_ctor_set(x_92, 0, x_90);
return x_92;
}
}
}
}
}
}
else
{
lean_object* x_126; lean_object* x_127; lean_object* x_128; lean_object* x_129; lean_object* x_130; lean_object* x_131; lean_object* x_132; lean_object* x_133; uint8_t x_166; 
x_126 = lean_ctor_get(x_27, 0);
x_127 = lean_ctor_get(x_27, 1);
lean_inc(x_127);
lean_inc(x_126);
lean_dec(x_27);
x_128 = lean_ctor_get(x_126, 0);
lean_inc(x_128);
x_129 = lean_ctor_get(x_126, 1);
lean_inc(x_129);
if (lean_is_exclusive(x_126)) {
 lean_ctor_release(x_126, 0);
 lean_ctor_release(x_126, 1);
 x_130 = x_126;
} else {
 lean_dec_ref(x_126);
 x_130 = lean_box(0);
}
x_166 = lean_unbox(x_129);
if (x_166 == 0)
{
lean_free_object(x_25);
if (lean_obj_tag(x_128) == 0)
{
uint8_t x_167; lean_object* x_168; lean_object* x_169; 
x_167 = 1;
x_168 = lp_REPL_REPL_runBatchVerify___closed__4;
x_169 = l_Lean_Parser_parseHeader(x_168);
if (lean_obj_tag(x_169) == 0)
{
lean_object* x_170; lean_object* x_171; lean_object* x_172; lean_object* x_173; lean_object* x_174; uint32_t x_175; lean_object* x_176; lean_object* x_177; lean_object* x_178; lean_object* x_179; uint8_t x_180; lean_object* x_181; lean_object* x_182; uint8_t x_183; lean_object* x_184; 
x_170 = lean_ctor_get(x_169, 0);
lean_inc(x_170);
lean_dec_ref(x_169);
x_171 = lean_ctor_get(x_170, 1);
lean_inc(x_171);
x_172 = lean_ctor_get(x_170, 0);
lean_inc(x_172);
lean_dec(x_170);
x_173 = lean_ctor_get(x_171, 1);
lean_inc(x_173);
lean_dec(x_171);
x_174 = lean_box(0);
x_175 = 0;
x_176 = lp_REPL_REPL_runBatchVerify___closed__5;
x_177 = lean_box(0);
x_178 = l_Lean_Elab_HeaderSyntax_startPos(x_172);
lean_inc(x_172);
x_179 = l_Lean_Elab_HeaderSyntax_imports(x_172, x_167);
x_180 = l_Lean_Elab_HeaderSyntax_isModule(x_172);
lean_dec(x_172);
x_181 = lean_box(0);
x_182 = lean_box(1);
x_183 = lean_unbox(x_129);
x_184 = l_Lean_Elab_processHeaderCore(x_178, x_179, x_180, x_174, x_173, x_168, x_175, x_176, x_183, x_177, x_181, x_182);
lean_dec(x_178);
if (lean_obj_tag(x_184) == 0)
{
lean_object* x_185; lean_object* x_186; lean_object* x_187; lean_object* x_188; 
x_185 = lean_ctor_get(x_184, 0);
lean_inc(x_185);
lean_dec_ref(x_184);
x_186 = lean_ctor_get(x_185, 0);
lean_inc(x_186);
x_187 = lean_ctor_get(x_185, 1);
lean_inc(x_187);
lean_dec(x_185);
x_188 = l_Lean_Elab_Command_mkState(x_186, x_187, x_174);
x_131 = x_188;
x_132 = x_127;
x_133 = lean_box(0);
goto block_165;
}
else
{
lean_object* x_189; lean_object* x_190; lean_object* x_191; 
lean_dec(x_130);
lean_dec(x_129);
lean_dec(x_127);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_189 = lean_ctor_get(x_184, 0);
lean_inc(x_189);
if (lean_is_exclusive(x_184)) {
 lean_ctor_release(x_184, 0);
 x_190 = x_184;
} else {
 lean_dec_ref(x_184);
 x_190 = lean_box(0);
}
if (lean_is_scalar(x_190)) {
 x_191 = lean_alloc_ctor(1, 1, 0);
} else {
 x_191 = x_190;
}
lean_ctor_set(x_191, 0, x_189);
return x_191;
}
}
else
{
lean_object* x_192; lean_object* x_193; lean_object* x_194; 
lean_dec(x_130);
lean_dec(x_129);
lean_dec(x_127);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_192 = lean_ctor_get(x_169, 0);
lean_inc(x_192);
if (lean_is_exclusive(x_169)) {
 lean_ctor_release(x_169, 0);
 x_193 = x_169;
} else {
 lean_dec_ref(x_169);
 x_193 = lean_box(0);
}
if (lean_is_scalar(x_193)) {
 x_194 = lean_alloc_ctor(1, 1, 0);
} else {
 x_194 = x_193;
}
lean_ctor_set(x_194, 0, x_192);
return x_194;
}
}
else
{
lean_object* x_195; lean_object* x_196; 
x_195 = lean_ctor_get(x_128, 0);
lean_inc(x_195);
lean_dec_ref(x_128);
x_196 = lean_ctor_get(x_195, 0);
lean_inc_ref(x_196);
lean_dec(x_195);
x_131 = x_196;
x_132 = x_127;
x_133 = lean_box(0);
goto block_165;
}
}
else
{
lean_object* x_197; lean_object* x_198; 
lean_dec(x_130);
lean_dec(x_129);
lean_dec(x_128);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_197 = lp_REPL_REPL_runBatchVerify___closed__6;
x_198 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_198, 0, x_197);
lean_ctor_set(x_198, 1, x_127);
lean_ctor_set(x_25, 0, x_198);
return x_25;
}
block_165:
{
lean_object* x_134; lean_object* x_135; lean_object* x_136; size_t x_137; size_t x_138; uint8_t x_139; lean_object* x_140; 
x_134 = lean_ctor_get(x_4, 1);
lean_inc(x_134);
x_135 = lean_ctor_get(x_4, 2);
x_136 = lean_ctor_get(x_4, 3);
x_137 = lean_array_size(x_6);
x_138 = 0;
x_139 = lean_unbox(x_129);
lean_dec(x_129);
x_140 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0(x_1, x_139, x_137, x_138, x_6);
if (lean_obj_tag(x_134) == 0)
{
lean_dec(x_130);
x_7 = x_131;
x_8 = x_140;
x_9 = x_132;
x_10 = lean_box(0);
goto block_24;
}
else
{
lean_object* x_141; lean_object* x_142; lean_object* x_143; uint8_t x_144; 
x_141 = lean_ctor_get(x_134, 0);
lean_inc(x_141);
if (lean_is_exclusive(x_134)) {
 lean_ctor_release(x_134, 0);
 x_142 = x_134;
} else {
 lean_dec_ref(x_134);
 x_142 = lean_box(0);
}
x_143 = lp_REPL_REPL_runBatchVerify___closed__0;
x_144 = lean_string_dec_eq(x_141, x_143);
if (x_144 == 0)
{
lean_object* x_145; uint8_t x_146; 
x_145 = lp_REPL_REPL_runBatchVerify___closed__1;
x_146 = lean_string_dec_eq(x_141, x_145);
lean_dec(x_141);
if (x_146 == 0)
{
lean_dec(x_142);
lean_dec(x_130);
x_7 = x_131;
x_8 = x_140;
x_9 = x_132;
x_10 = lean_box(0);
goto block_24;
}
else
{
lean_object* x_147; 
lean_inc(x_136);
lean_inc(x_135);
lean_dec_ref(x_4);
x_147 = lp_REPL_REPL_batchVerifyParrallel(x_131, x_140, x_135, x_136);
if (lean_obj_tag(x_147) == 0)
{
lean_object* x_148; lean_object* x_149; lean_object* x_150; lean_object* x_151; lean_object* x_152; 
x_148 = lean_ctor_get(x_147, 0);
lean_inc(x_148);
if (lean_is_exclusive(x_147)) {
 lean_ctor_release(x_147, 0);
 x_149 = x_147;
} else {
 lean_dec_ref(x_147);
 x_149 = lean_box(0);
}
if (lean_is_scalar(x_142)) {
 x_150 = lean_alloc_ctor(0, 1, 0);
} else {
 x_150 = x_142;
 lean_ctor_set_tag(x_150, 0);
}
lean_ctor_set(x_150, 0, x_148);
if (lean_is_scalar(x_130)) {
 x_151 = lean_alloc_ctor(0, 2, 0);
} else {
 x_151 = x_130;
}
lean_ctor_set(x_151, 0, x_150);
lean_ctor_set(x_151, 1, x_132);
if (lean_is_scalar(x_149)) {
 x_152 = lean_alloc_ctor(0, 1, 0);
} else {
 x_152 = x_149;
}
lean_ctor_set(x_152, 0, x_151);
return x_152;
}
else
{
lean_object* x_153; lean_object* x_154; lean_object* x_155; 
lean_dec(x_142);
lean_dec_ref(x_132);
lean_dec(x_130);
x_153 = lean_ctor_get(x_147, 0);
lean_inc(x_153);
if (lean_is_exclusive(x_147)) {
 lean_ctor_release(x_147, 0);
 x_154 = x_147;
} else {
 lean_dec_ref(x_147);
 x_154 = lean_box(0);
}
if (lean_is_scalar(x_154)) {
 x_155 = lean_alloc_ctor(1, 1, 0);
} else {
 x_155 = x_154;
}
lean_ctor_set(x_155, 0, x_153);
return x_155;
}
}
}
else
{
lean_object* x_156; 
lean_dec(x_141);
lean_inc(x_136);
lean_dec_ref(x_4);
x_156 = lp_REPL_REPL_batchVerifyParrallelNaive(x_131, x_140, x_136);
if (lean_obj_tag(x_156) == 0)
{
lean_object* x_157; lean_object* x_158; lean_object* x_159; lean_object* x_160; lean_object* x_161; 
x_157 = lean_ctor_get(x_156, 0);
lean_inc(x_157);
if (lean_is_exclusive(x_156)) {
 lean_ctor_release(x_156, 0);
 x_158 = x_156;
} else {
 lean_dec_ref(x_156);
 x_158 = lean_box(0);
}
if (lean_is_scalar(x_142)) {
 x_159 = lean_alloc_ctor(0, 1, 0);
} else {
 x_159 = x_142;
 lean_ctor_set_tag(x_159, 0);
}
lean_ctor_set(x_159, 0, x_157);
if (lean_is_scalar(x_130)) {
 x_160 = lean_alloc_ctor(0, 2, 0);
} else {
 x_160 = x_130;
}
lean_ctor_set(x_160, 0, x_159);
lean_ctor_set(x_160, 1, x_132);
if (lean_is_scalar(x_158)) {
 x_161 = lean_alloc_ctor(0, 1, 0);
} else {
 x_161 = x_158;
}
lean_ctor_set(x_161, 0, x_160);
return x_161;
}
else
{
lean_object* x_162; lean_object* x_163; lean_object* x_164; 
lean_dec(x_142);
lean_dec_ref(x_132);
lean_dec(x_130);
x_162 = lean_ctor_get(x_156, 0);
lean_inc(x_162);
if (lean_is_exclusive(x_156)) {
 lean_ctor_release(x_156, 0);
 x_163 = x_156;
} else {
 lean_dec_ref(x_156);
 x_163 = lean_box(0);
}
if (lean_is_scalar(x_163)) {
 x_164 = lean_alloc_ctor(1, 1, 0);
} else {
 x_164 = x_163;
}
lean_ctor_set(x_164, 0, x_162);
return x_164;
}
}
}
}
}
}
else
{
lean_object* x_199; lean_object* x_200; lean_object* x_201; lean_object* x_202; lean_object* x_203; lean_object* x_204; lean_object* x_205; lean_object* x_206; lean_object* x_207; lean_object* x_208; uint8_t x_241; 
x_199 = lean_ctor_get(x_25, 0);
lean_inc(x_199);
lean_dec(x_25);
x_200 = lean_ctor_get(x_199, 0);
lean_inc(x_200);
x_201 = lean_ctor_get(x_199, 1);
lean_inc(x_201);
if (lean_is_exclusive(x_199)) {
 lean_ctor_release(x_199, 0);
 lean_ctor_release(x_199, 1);
 x_202 = x_199;
} else {
 lean_dec_ref(x_199);
 x_202 = lean_box(0);
}
x_203 = lean_ctor_get(x_200, 0);
lean_inc(x_203);
x_204 = lean_ctor_get(x_200, 1);
lean_inc(x_204);
if (lean_is_exclusive(x_200)) {
 lean_ctor_release(x_200, 0);
 lean_ctor_release(x_200, 1);
 x_205 = x_200;
} else {
 lean_dec_ref(x_200);
 x_205 = lean_box(0);
}
x_241 = lean_unbox(x_204);
if (x_241 == 0)
{
lean_dec(x_202);
if (lean_obj_tag(x_203) == 0)
{
uint8_t x_242; lean_object* x_243; lean_object* x_244; 
x_242 = 1;
x_243 = lp_REPL_REPL_runBatchVerify___closed__4;
x_244 = l_Lean_Parser_parseHeader(x_243);
if (lean_obj_tag(x_244) == 0)
{
lean_object* x_245; lean_object* x_246; lean_object* x_247; lean_object* x_248; lean_object* x_249; uint32_t x_250; lean_object* x_251; lean_object* x_252; lean_object* x_253; lean_object* x_254; uint8_t x_255; lean_object* x_256; lean_object* x_257; uint8_t x_258; lean_object* x_259; 
x_245 = lean_ctor_get(x_244, 0);
lean_inc(x_245);
lean_dec_ref(x_244);
x_246 = lean_ctor_get(x_245, 1);
lean_inc(x_246);
x_247 = lean_ctor_get(x_245, 0);
lean_inc(x_247);
lean_dec(x_245);
x_248 = lean_ctor_get(x_246, 1);
lean_inc(x_248);
lean_dec(x_246);
x_249 = lean_box(0);
x_250 = 0;
x_251 = lp_REPL_REPL_runBatchVerify___closed__5;
x_252 = lean_box(0);
x_253 = l_Lean_Elab_HeaderSyntax_startPos(x_247);
lean_inc(x_247);
x_254 = l_Lean_Elab_HeaderSyntax_imports(x_247, x_242);
x_255 = l_Lean_Elab_HeaderSyntax_isModule(x_247);
lean_dec(x_247);
x_256 = lean_box(0);
x_257 = lean_box(1);
x_258 = lean_unbox(x_204);
x_259 = l_Lean_Elab_processHeaderCore(x_253, x_254, x_255, x_249, x_248, x_243, x_250, x_251, x_258, x_252, x_256, x_257);
lean_dec(x_253);
if (lean_obj_tag(x_259) == 0)
{
lean_object* x_260; lean_object* x_261; lean_object* x_262; lean_object* x_263; 
x_260 = lean_ctor_get(x_259, 0);
lean_inc(x_260);
lean_dec_ref(x_259);
x_261 = lean_ctor_get(x_260, 0);
lean_inc(x_261);
x_262 = lean_ctor_get(x_260, 1);
lean_inc(x_262);
lean_dec(x_260);
x_263 = l_Lean_Elab_Command_mkState(x_261, x_262, x_249);
x_206 = x_263;
x_207 = x_201;
x_208 = lean_box(0);
goto block_240;
}
else
{
lean_object* x_264; lean_object* x_265; lean_object* x_266; 
lean_dec(x_205);
lean_dec(x_204);
lean_dec(x_201);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_264 = lean_ctor_get(x_259, 0);
lean_inc(x_264);
if (lean_is_exclusive(x_259)) {
 lean_ctor_release(x_259, 0);
 x_265 = x_259;
} else {
 lean_dec_ref(x_259);
 x_265 = lean_box(0);
}
if (lean_is_scalar(x_265)) {
 x_266 = lean_alloc_ctor(1, 1, 0);
} else {
 x_266 = x_265;
}
lean_ctor_set(x_266, 0, x_264);
return x_266;
}
}
else
{
lean_object* x_267; lean_object* x_268; lean_object* x_269; 
lean_dec(x_205);
lean_dec(x_204);
lean_dec(x_201);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_267 = lean_ctor_get(x_244, 0);
lean_inc(x_267);
if (lean_is_exclusive(x_244)) {
 lean_ctor_release(x_244, 0);
 x_268 = x_244;
} else {
 lean_dec_ref(x_244);
 x_268 = lean_box(0);
}
if (lean_is_scalar(x_268)) {
 x_269 = lean_alloc_ctor(1, 1, 0);
} else {
 x_269 = x_268;
}
lean_ctor_set(x_269, 0, x_267);
return x_269;
}
}
else
{
lean_object* x_270; lean_object* x_271; 
x_270 = lean_ctor_get(x_203, 0);
lean_inc(x_270);
lean_dec_ref(x_203);
x_271 = lean_ctor_get(x_270, 0);
lean_inc_ref(x_271);
lean_dec(x_270);
x_206 = x_271;
x_207 = x_201;
x_208 = lean_box(0);
goto block_240;
}
}
else
{
lean_object* x_272; lean_object* x_273; lean_object* x_274; 
lean_dec(x_205);
lean_dec(x_204);
lean_dec(x_203);
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_272 = lp_REPL_REPL_runBatchVerify___closed__6;
if (lean_is_scalar(x_202)) {
 x_273 = lean_alloc_ctor(0, 2, 0);
} else {
 x_273 = x_202;
}
lean_ctor_set(x_273, 0, x_272);
lean_ctor_set(x_273, 1, x_201);
x_274 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_274, 0, x_273);
return x_274;
}
block_240:
{
lean_object* x_209; lean_object* x_210; lean_object* x_211; size_t x_212; size_t x_213; uint8_t x_214; lean_object* x_215; 
x_209 = lean_ctor_get(x_4, 1);
lean_inc(x_209);
x_210 = lean_ctor_get(x_4, 2);
x_211 = lean_ctor_get(x_4, 3);
x_212 = lean_array_size(x_6);
x_213 = 0;
x_214 = lean_unbox(x_204);
lean_dec(x_204);
x_215 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0(x_1, x_214, x_212, x_213, x_6);
if (lean_obj_tag(x_209) == 0)
{
lean_dec(x_205);
x_7 = x_206;
x_8 = x_215;
x_9 = x_207;
x_10 = lean_box(0);
goto block_24;
}
else
{
lean_object* x_216; lean_object* x_217; lean_object* x_218; uint8_t x_219; 
x_216 = lean_ctor_get(x_209, 0);
lean_inc(x_216);
if (lean_is_exclusive(x_209)) {
 lean_ctor_release(x_209, 0);
 x_217 = x_209;
} else {
 lean_dec_ref(x_209);
 x_217 = lean_box(0);
}
x_218 = lp_REPL_REPL_runBatchVerify___closed__0;
x_219 = lean_string_dec_eq(x_216, x_218);
if (x_219 == 0)
{
lean_object* x_220; uint8_t x_221; 
x_220 = lp_REPL_REPL_runBatchVerify___closed__1;
x_221 = lean_string_dec_eq(x_216, x_220);
lean_dec(x_216);
if (x_221 == 0)
{
lean_dec(x_217);
lean_dec(x_205);
x_7 = x_206;
x_8 = x_215;
x_9 = x_207;
x_10 = lean_box(0);
goto block_24;
}
else
{
lean_object* x_222; 
lean_inc(x_211);
lean_inc(x_210);
lean_dec_ref(x_4);
x_222 = lp_REPL_REPL_batchVerifyParrallel(x_206, x_215, x_210, x_211);
if (lean_obj_tag(x_222) == 0)
{
lean_object* x_223; lean_object* x_224; lean_object* x_225; lean_object* x_226; lean_object* x_227; 
x_223 = lean_ctor_get(x_222, 0);
lean_inc(x_223);
if (lean_is_exclusive(x_222)) {
 lean_ctor_release(x_222, 0);
 x_224 = x_222;
} else {
 lean_dec_ref(x_222);
 x_224 = lean_box(0);
}
if (lean_is_scalar(x_217)) {
 x_225 = lean_alloc_ctor(0, 1, 0);
} else {
 x_225 = x_217;
 lean_ctor_set_tag(x_225, 0);
}
lean_ctor_set(x_225, 0, x_223);
if (lean_is_scalar(x_205)) {
 x_226 = lean_alloc_ctor(0, 2, 0);
} else {
 x_226 = x_205;
}
lean_ctor_set(x_226, 0, x_225);
lean_ctor_set(x_226, 1, x_207);
if (lean_is_scalar(x_224)) {
 x_227 = lean_alloc_ctor(0, 1, 0);
} else {
 x_227 = x_224;
}
lean_ctor_set(x_227, 0, x_226);
return x_227;
}
else
{
lean_object* x_228; lean_object* x_229; lean_object* x_230; 
lean_dec(x_217);
lean_dec_ref(x_207);
lean_dec(x_205);
x_228 = lean_ctor_get(x_222, 0);
lean_inc(x_228);
if (lean_is_exclusive(x_222)) {
 lean_ctor_release(x_222, 0);
 x_229 = x_222;
} else {
 lean_dec_ref(x_222);
 x_229 = lean_box(0);
}
if (lean_is_scalar(x_229)) {
 x_230 = lean_alloc_ctor(1, 1, 0);
} else {
 x_230 = x_229;
}
lean_ctor_set(x_230, 0, x_228);
return x_230;
}
}
}
else
{
lean_object* x_231; 
lean_dec(x_216);
lean_inc(x_211);
lean_dec_ref(x_4);
x_231 = lp_REPL_REPL_batchVerifyParrallelNaive(x_206, x_215, x_211);
if (lean_obj_tag(x_231) == 0)
{
lean_object* x_232; lean_object* x_233; lean_object* x_234; lean_object* x_235; lean_object* x_236; 
x_232 = lean_ctor_get(x_231, 0);
lean_inc(x_232);
if (lean_is_exclusive(x_231)) {
 lean_ctor_release(x_231, 0);
 x_233 = x_231;
} else {
 lean_dec_ref(x_231);
 x_233 = lean_box(0);
}
if (lean_is_scalar(x_217)) {
 x_234 = lean_alloc_ctor(0, 1, 0);
} else {
 x_234 = x_217;
 lean_ctor_set_tag(x_234, 0);
}
lean_ctor_set(x_234, 0, x_232);
if (lean_is_scalar(x_205)) {
 x_235 = lean_alloc_ctor(0, 2, 0);
} else {
 x_235 = x_205;
}
lean_ctor_set(x_235, 0, x_234);
lean_ctor_set(x_235, 1, x_207);
if (lean_is_scalar(x_233)) {
 x_236 = lean_alloc_ctor(0, 1, 0);
} else {
 x_236 = x_233;
}
lean_ctor_set(x_236, 0, x_235);
return x_236;
}
else
{
lean_object* x_237; lean_object* x_238; lean_object* x_239; 
lean_dec(x_217);
lean_dec_ref(x_207);
lean_dec(x_205);
x_237 = lean_ctor_get(x_231, 0);
lean_inc(x_237);
if (lean_is_exclusive(x_231)) {
 lean_ctor_release(x_231, 0);
 x_238 = x_231;
} else {
 lean_dec_ref(x_231);
 x_238 = lean_box(0);
}
if (lean_is_scalar(x_238)) {
 x_239 = lean_alloc_ctor(1, 1, 0);
} else {
 x_239 = x_238;
}
lean_ctor_set(x_239, 0, x_237);
return x_239;
}
}
}
}
}
}
else
{
uint8_t x_275; 
lean_dec_ref(x_6);
lean_dec_ref(x_4);
lean_dec_ref(x_1);
x_275 = !lean_is_exclusive(x_25);
if (x_275 == 0)
{
return x_25;
}
else
{
lean_object* x_276; lean_object* x_277; 
x_276 = lean_ctor_get(x_25, 0);
lean_inc(x_276);
lean_dec(x_25);
x_277 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_277, 0, x_276);
return x_277;
}
}
block_24:
{
lean_object* x_11; lean_object* x_12; 
x_11 = lean_ctor_get(x_4, 3);
lean_inc(x_11);
lean_dec_ref(x_4);
x_12 = lp_REPL_REPL_batchVerifySequential(x_7, x_8, x_11);
lean_dec(x_11);
if (lean_obj_tag(x_12) == 0)
{
uint8_t x_13; 
x_13 = !lean_is_exclusive(x_12);
if (x_13 == 0)
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_14 = lean_ctor_get(x_12, 0);
x_15 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_15, 0, x_14);
x_16 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_16, 0, x_15);
lean_ctor_set(x_16, 1, x_9);
lean_ctor_set(x_12, 0, x_16);
return x_12;
}
else
{
lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; 
x_17 = lean_ctor_get(x_12, 0);
lean_inc(x_17);
lean_dec(x_12);
x_18 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_18, 0, x_17);
x_19 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_19, 0, x_18);
lean_ctor_set(x_19, 1, x_9);
x_20 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_20, 0, x_19);
return x_20;
}
}
else
{
uint8_t x_21; 
lean_dec_ref(x_9);
x_21 = !lean_is_exclusive(x_12);
if (x_21 == 0)
{
return x_12;
}
else
{
lean_object* x_22; lean_object* x_23; 
x_22 = lean_ctor_get(x_12, 0);
lean_inc(x_22);
lean_dec(x_12);
x_23 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_23, 0, x_22);
return x_23;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
uint8_t x_6; size_t x_7; size_t x_8; lean_object* x_9; 
x_6 = lean_unbox(x_2);
x_7 = lean_unbox_usize(x_3);
lean_dec(x_3);
x_8 = lean_unbox_usize(x_4);
lean_dec(x_4);
x_9 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00REPL_runBatchVerify_spec__0(x_1, x_6, x_7, x_8, x_5);
return x_9;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runBatchVerify___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_runBatchVerify(x_1, x_2);
return x_4;
}
}
static lean_object* _init_lp_REPL_REPL_runProofStep___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("Lean error:\n", 12, 12);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runProofStep___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("Unknown proof state.", 20, 20);
return x_1;
}
}
static lean_object* _init_lp_REPL_REPL_runProofStep___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_REPL_runProofStep___closed__1;
x_2 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_2, 0, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runProofStep(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; uint8_t x_13; 
x_13 = !lean_is_exclusive(x_1);
if (x_13 == 0)
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; uint8_t x_18; 
x_14 = lean_ctor_get(x_2, 1);
x_15 = lean_ctor_get(x_1, 0);
x_16 = lean_ctor_get(x_1, 1);
x_17 = lean_array_get_size(x_14);
x_18 = lean_nat_dec_lt(x_15, x_17);
if (x_18 == 0)
{
lean_object* x_19; lean_object* x_20; 
lean_dec_ref(x_16);
lean_dec(x_15);
x_19 = lp_REPL_REPL_runProofStep___closed__2;
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_19);
x_20 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_20, 0, x_1);
return x_20;
}
else
{
lean_object* x_21; lean_object* x_22; 
lean_free_object(x_1);
x_21 = lean_array_fget_borrowed(x_14, x_15);
lean_dec(x_15);
lean_inc(x_21);
x_22 = lp_REPL_REPL_ProofSnapshot_runString(x_21, x_16);
if (lean_obj_tag(x_22) == 0)
{
uint8_t x_23; 
x_23 = !lean_is_exclusive(x_22);
if (x_23 == 0)
{
lean_object* x_24; lean_object* x_25; 
x_24 = lean_ctor_get(x_22, 0);
lean_inc(x_21);
lean_ctor_set_tag(x_22, 1);
lean_ctor_set(x_22, 0, x_21);
lean_inc_ref(x_2);
x_25 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_24, x_22, x_2);
if (lean_obj_tag(x_25) == 0)
{
uint8_t x_26; 
lean_dec_ref(x_2);
x_26 = !lean_is_exclusive(x_25);
if (x_26 == 0)
{
lean_object* x_27; uint8_t x_28; 
x_27 = lean_ctor_get(x_25, 0);
x_28 = !lean_is_exclusive(x_27);
if (x_28 == 0)
{
lean_object* x_29; lean_object* x_30; 
x_29 = lean_ctor_get(x_27, 0);
x_30 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_30, 0, x_29);
lean_ctor_set(x_27, 0, x_30);
return x_25;
}
else
{
lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; 
x_31 = lean_ctor_get(x_27, 0);
x_32 = lean_ctor_get(x_27, 1);
lean_inc(x_32);
lean_inc(x_31);
lean_dec(x_27);
x_33 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_33, 0, x_31);
x_34 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_34, 0, x_33);
lean_ctor_set(x_34, 1, x_32);
lean_ctor_set(x_25, 0, x_34);
return x_25;
}
}
else
{
lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; 
x_35 = lean_ctor_get(x_25, 0);
lean_inc(x_35);
lean_dec(x_25);
x_36 = lean_ctor_get(x_35, 0);
lean_inc(x_36);
x_37 = lean_ctor_get(x_35, 1);
lean_inc(x_37);
if (lean_is_exclusive(x_35)) {
 lean_ctor_release(x_35, 0);
 lean_ctor_release(x_35, 1);
 x_38 = x_35;
} else {
 lean_dec_ref(x_35);
 x_38 = lean_box(0);
}
x_39 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_39, 0, x_36);
if (lean_is_scalar(x_38)) {
 x_40 = lean_alloc_ctor(0, 2, 0);
} else {
 x_40 = x_38;
}
lean_ctor_set(x_40, 0, x_39);
lean_ctor_set(x_40, 1, x_37);
x_41 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_41, 0, x_40);
return x_41;
}
}
else
{
lean_object* x_42; 
x_42 = lean_ctor_get(x_25, 0);
lean_inc(x_42);
lean_dec_ref(x_25);
x_4 = x_42;
x_5 = lean_box(0);
goto block_12;
}
}
else
{
lean_object* x_43; lean_object* x_44; lean_object* x_45; 
x_43 = lean_ctor_get(x_22, 0);
lean_inc(x_43);
lean_dec(x_22);
lean_inc(x_21);
x_44 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_44, 0, x_21);
lean_inc_ref(x_2);
x_45 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_43, x_44, x_2);
if (lean_obj_tag(x_45) == 0)
{
lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; lean_object* x_52; lean_object* x_53; 
lean_dec_ref(x_2);
x_46 = lean_ctor_get(x_45, 0);
lean_inc(x_46);
if (lean_is_exclusive(x_45)) {
 lean_ctor_release(x_45, 0);
 x_47 = x_45;
} else {
 lean_dec_ref(x_45);
 x_47 = lean_box(0);
}
x_48 = lean_ctor_get(x_46, 0);
lean_inc(x_48);
x_49 = lean_ctor_get(x_46, 1);
lean_inc(x_49);
if (lean_is_exclusive(x_46)) {
 lean_ctor_release(x_46, 0);
 lean_ctor_release(x_46, 1);
 x_50 = x_46;
} else {
 lean_dec_ref(x_46);
 x_50 = lean_box(0);
}
x_51 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_51, 0, x_48);
if (lean_is_scalar(x_50)) {
 x_52 = lean_alloc_ctor(0, 2, 0);
} else {
 x_52 = x_50;
}
lean_ctor_set(x_52, 0, x_51);
lean_ctor_set(x_52, 1, x_49);
if (lean_is_scalar(x_47)) {
 x_53 = lean_alloc_ctor(0, 1, 0);
} else {
 x_53 = x_47;
}
lean_ctor_set(x_53, 0, x_52);
return x_53;
}
else
{
lean_object* x_54; 
x_54 = lean_ctor_get(x_45, 0);
lean_inc(x_54);
lean_dec_ref(x_45);
x_4 = x_54;
x_5 = lean_box(0);
goto block_12;
}
}
}
else
{
lean_object* x_55; 
x_55 = lean_ctor_get(x_22, 0);
lean_inc(x_55);
lean_dec_ref(x_22);
x_4 = x_55;
x_5 = lean_box(0);
goto block_12;
}
}
}
else
{
lean_object* x_56; lean_object* x_57; lean_object* x_58; lean_object* x_59; uint8_t x_60; 
x_56 = lean_ctor_get(x_2, 1);
x_57 = lean_ctor_get(x_1, 0);
x_58 = lean_ctor_get(x_1, 1);
lean_inc(x_58);
lean_inc(x_57);
lean_dec(x_1);
x_59 = lean_array_get_size(x_56);
x_60 = lean_nat_dec_lt(x_57, x_59);
if (x_60 == 0)
{
lean_object* x_61; lean_object* x_62; lean_object* x_63; 
lean_dec_ref(x_58);
lean_dec(x_57);
x_61 = lp_REPL_REPL_runProofStep___closed__2;
x_62 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_62, 0, x_61);
lean_ctor_set(x_62, 1, x_2);
x_63 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_63, 0, x_62);
return x_63;
}
else
{
lean_object* x_64; lean_object* x_65; 
x_64 = lean_array_fget_borrowed(x_56, x_57);
lean_dec(x_57);
lean_inc(x_64);
x_65 = lp_REPL_REPL_ProofSnapshot_runString(x_64, x_58);
if (lean_obj_tag(x_65) == 0)
{
lean_object* x_66; lean_object* x_67; lean_object* x_68; lean_object* x_69; 
x_66 = lean_ctor_get(x_65, 0);
lean_inc(x_66);
if (lean_is_exclusive(x_65)) {
 lean_ctor_release(x_65, 0);
 x_67 = x_65;
} else {
 lean_dec_ref(x_65);
 x_67 = lean_box(0);
}
lean_inc(x_64);
if (lean_is_scalar(x_67)) {
 x_68 = lean_alloc_ctor(1, 1, 0);
} else {
 x_68 = x_67;
 lean_ctor_set_tag(x_68, 1);
}
lean_ctor_set(x_68, 0, x_64);
lean_inc_ref(x_2);
x_69 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_66, x_68, x_2);
if (lean_obj_tag(x_69) == 0)
{
lean_object* x_70; lean_object* x_71; lean_object* x_72; lean_object* x_73; lean_object* x_74; lean_object* x_75; lean_object* x_76; lean_object* x_77; 
lean_dec_ref(x_2);
x_70 = lean_ctor_get(x_69, 0);
lean_inc(x_70);
if (lean_is_exclusive(x_69)) {
 lean_ctor_release(x_69, 0);
 x_71 = x_69;
} else {
 lean_dec_ref(x_69);
 x_71 = lean_box(0);
}
x_72 = lean_ctor_get(x_70, 0);
lean_inc(x_72);
x_73 = lean_ctor_get(x_70, 1);
lean_inc(x_73);
if (lean_is_exclusive(x_70)) {
 lean_ctor_release(x_70, 0);
 lean_ctor_release(x_70, 1);
 x_74 = x_70;
} else {
 lean_dec_ref(x_70);
 x_74 = lean_box(0);
}
x_75 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_75, 0, x_72);
if (lean_is_scalar(x_74)) {
 x_76 = lean_alloc_ctor(0, 2, 0);
} else {
 x_76 = x_74;
}
lean_ctor_set(x_76, 0, x_75);
lean_ctor_set(x_76, 1, x_73);
if (lean_is_scalar(x_71)) {
 x_77 = lean_alloc_ctor(0, 1, 0);
} else {
 x_77 = x_71;
}
lean_ctor_set(x_77, 0, x_76);
return x_77;
}
else
{
lean_object* x_78; 
x_78 = lean_ctor_get(x_69, 0);
lean_inc(x_78);
lean_dec_ref(x_69);
x_4 = x_78;
x_5 = lean_box(0);
goto block_12;
}
}
else
{
lean_object* x_79; 
x_79 = lean_ctor_get(x_65, 0);
lean_inc(x_79);
lean_dec_ref(x_65);
x_4 = x_79;
x_5 = lean_box(0);
goto block_12;
}
}
}
block_12:
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_6 = lp_REPL_REPL_runProofStep___closed__0;
x_7 = lean_io_error_to_string(x_4);
x_8 = lean_string_append(x_6, x_7);
lean_dec_ref(x_7);
x_9 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_9, 0, x_8);
x_10 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_10, 0, x_9);
lean_ctor_set(x_10, 1, x_2);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_10);
return x_11;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_runProofStep___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_runProofStep(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_getLines() {
_start:
{
lean_object* x_2; lean_object* x_3; lean_object* x_4; 
x_2 = lean_get_stdin();
x_3 = lean_ctor_get(x_2, 3);
lean_inc_ref(x_3);
lean_dec_ref(x_2);
x_4 = lean_apply_1(x_3, lean_box(0));
if (lean_obj_tag(x_4) == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; uint8_t x_9; 
x_5 = lean_ctor_get(x_4, 0);
lean_inc(x_5);
lean_inc(x_5);
x_6 = l_String_trim(x_5);
x_7 = lean_string_utf8_byte_size(x_6);
lean_dec_ref(x_6);
x_8 = lean_unsigned_to_nat(0u);
x_9 = lean_nat_dec_eq(x_7, x_8);
if (x_9 == 0)
{
lean_object* x_10; 
lean_dec_ref(x_4);
x_10 = lp_REPL_getLines();
if (lean_obj_tag(x_10) == 0)
{
uint8_t x_11; 
x_11 = !lean_is_exclusive(x_10);
if (x_11 == 0)
{
lean_object* x_12; lean_object* x_13; 
x_12 = lean_ctor_get(x_10, 0);
x_13 = lean_string_append(x_5, x_12);
lean_dec(x_12);
lean_ctor_set(x_10, 0, x_13);
return x_10;
}
else
{
lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_14 = lean_ctor_get(x_10, 0);
lean_inc(x_14);
lean_dec(x_10);
x_15 = lean_string_append(x_5, x_14);
lean_dec(x_14);
x_16 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_16, 0, x_15);
return x_16;
}
}
else
{
lean_dec(x_5);
return x_10;
}
}
else
{
lean_dec(x_5);
return x_4;
}
}
else
{
return x_4;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_getLines___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_REPL_getLines();
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_instToJsonSum__rEPL___redArg___lam__0(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
if (lean_obj_tag(x_3) == 0)
{
lean_object* x_4; lean_object* x_5; 
lean_dec_ref(x_2);
x_4 = lean_ctor_get(x_3, 0);
lean_inc(x_4);
lean_dec_ref(x_3);
x_5 = lean_apply_1(x_1, x_4);
return x_5;
}
else
{
lean_object* x_6; lean_object* x_7; 
lean_dec_ref(x_1);
x_6 = lean_ctor_get(x_3, 0);
lean_inc(x_6);
lean_dec_ref(x_3);
x_7 = lean_apply_1(x_2, x_6);
return x_7;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_instToJsonSum__rEPL___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lean_alloc_closure((void*)(lp_REPL_instToJsonSum__rEPL___redArg___lam__0), 3, 2);
lean_closure_set(x_3, 0, x_1);
lean_closure_set(x_3, 1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_instToJsonSum__rEPL(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_instToJsonSum__rEPL___redArg(x_3, x_4);
return x_5;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("header", 6, 6);
return x_1;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("Batch", 5, 5);
return x_1;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__2() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__1;
x_2 = l_Lean_Name_mkStr1(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__3() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; 
x_1 = 1;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__2;
x_3 = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__4() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked(".", 1, 1);
return x_1;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__5() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__4;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__3;
x_3 = lean_string_append(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__6() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__0;
x_2 = l_Lean_Name_mkStr1(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__7() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; 
x_1 = 1;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__6;
x_3 = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__8() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__7;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__5;
x_3 = lean_string_append(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__9() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked(": ", 2, 2);
return x_1;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__10() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__9;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__8;
x_3 = lean_string_append(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__11() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("proofs", 6, 6);
return x_1;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__12() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__11;
x_2 = l_Lean_Name_mkStr1(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__13() {
_start:
{
uint8_t x_1; lean_object* x_2; lean_object* x_3; 
x_1 = 1;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__12;
x_3 = l_Lean_Name_toStringWithToken___at___00Lean_Name_toString_spec__0(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__14() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__13;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__5;
x_3 = lean_string_append(x_2, x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch_fromJson___closed__15() {
_start:
{
lean_object* x_1; lean_object* x_2; lean_object* x_3; 
x_1 = lp_REPL_instFromJsonBatch_fromJson___closed__9;
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__14;
x_3 = lean_string_append(x_2, x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_instFromJsonBatch_fromJson(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lp_REPL_instFromJsonBatch_fromJson___closed__0;
lean_inc(x_1);
x_3 = l_Lean_Json_getObjValAs_x3f___at___00Lean_Server_Test_Runner_Client_instFromJsonSubexprInfo_fromJson_spec__1(x_1, x_2);
if (lean_obj_tag(x_3) == 0)
{
uint8_t x_4; 
lean_dec(x_1);
x_4 = !lean_is_exclusive(x_3);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_5 = lean_ctor_get(x_3, 0);
x_6 = lp_REPL_instFromJsonBatch_fromJson___closed__10;
x_7 = lean_string_append(x_6, x_5);
lean_dec(x_5);
lean_ctor_set(x_3, 0, x_7);
return x_3;
}
else
{
lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_8 = lean_ctor_get(x_3, 0);
lean_inc(x_8);
lean_dec(x_3);
x_9 = lp_REPL_instFromJsonBatch_fromJson___closed__10;
x_10 = lean_string_append(x_9, x_8);
lean_dec(x_8);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_10);
return x_11;
}
}
else
{
if (lean_obj_tag(x_3) == 0)
{
uint8_t x_12; 
lean_dec(x_1);
x_12 = !lean_is_exclusive(x_3);
if (x_12 == 0)
{
lean_ctor_set_tag(x_3, 0);
return x_3;
}
else
{
lean_object* x_13; lean_object* x_14; 
x_13 = lean_ctor_get(x_3, 0);
lean_inc(x_13);
lean_dec(x_3);
x_14 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_14, 0, x_13);
return x_14;
}
}
else
{
lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_15 = lean_ctor_get(x_3, 0);
lean_inc(x_15);
lean_dec_ref(x_3);
x_16 = lp_REPL_instFromJsonBatch_fromJson___closed__11;
x_17 = l_Lean_Json_getObjValAs_x3f___at___00Lean_Server_Test_Runner_Client_instFromJsonHyp_fromJson_spec__4(x_1, x_16);
if (lean_obj_tag(x_17) == 0)
{
uint8_t x_18; 
lean_dec(x_15);
x_18 = !lean_is_exclusive(x_17);
if (x_18 == 0)
{
lean_object* x_19; lean_object* x_20; lean_object* x_21; 
x_19 = lean_ctor_get(x_17, 0);
x_20 = lp_REPL_instFromJsonBatch_fromJson___closed__15;
x_21 = lean_string_append(x_20, x_19);
lean_dec(x_19);
lean_ctor_set(x_17, 0, x_21);
return x_17;
}
else
{
lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; 
x_22 = lean_ctor_get(x_17, 0);
lean_inc(x_22);
lean_dec(x_17);
x_23 = lp_REPL_instFromJsonBatch_fromJson___closed__15;
x_24 = lean_string_append(x_23, x_22);
lean_dec(x_22);
x_25 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_25, 0, x_24);
return x_25;
}
}
else
{
if (lean_obj_tag(x_17) == 0)
{
uint8_t x_26; 
lean_dec(x_15);
x_26 = !lean_is_exclusive(x_17);
if (x_26 == 0)
{
lean_ctor_set_tag(x_17, 0);
return x_17;
}
else
{
lean_object* x_27; lean_object* x_28; 
x_27 = lean_ctor_get(x_17, 0);
lean_inc(x_27);
lean_dec(x_17);
x_28 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_28, 0, x_27);
return x_28;
}
}
else
{
uint8_t x_29; 
x_29 = !lean_is_exclusive(x_17);
if (x_29 == 0)
{
lean_object* x_30; lean_object* x_31; 
x_30 = lean_ctor_get(x_17, 0);
x_31 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_31, 0, x_15);
lean_ctor_set(x_31, 1, x_30);
lean_ctor_set(x_17, 0, x_31);
return x_17;
}
else
{
lean_object* x_32; lean_object* x_33; lean_object* x_34; 
x_32 = lean_ctor_get(x_17, 0);
lean_inc(x_32);
lean_dec(x_17);
x_33 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_33, 0, x_15);
lean_ctor_set(x_33, 1, x_32);
x_34 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_34, 0, x_33);
return x_34;
}
}
}
}
}
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(lp_REPL_instFromJsonBatch_fromJson), 1, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_instFromJsonBatch() {
_start:
{
lean_object* x_1; 
x_1 = lp_REPL_instFromJsonBatch___closed__0;
return x_1;
}
}
static lean_object* _init_lp_REPL_instToJsonBatch_toJson___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_instToJsonBatch_toJson(lean_object* x_1) {
_start:
{
uint8_t x_2; 
x_2 = !lean_is_exclusive(x_1);
if (x_2 == 0)
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; 
x_3 = lean_ctor_get(x_1, 0);
x_4 = lean_ctor_get(x_1, 1);
x_5 = lp_REPL_instFromJsonBatch_fromJson___closed__0;
x_6 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_6, 0, x_3);
lean_ctor_set(x_1, 1, x_6);
lean_ctor_set(x_1, 0, x_5);
x_7 = lean_box(0);
x_8 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_8, 0, x_1);
lean_ctor_set(x_8, 1, x_7);
x_9 = lp_REPL_instFromJsonBatch_fromJson___closed__11;
x_10 = l_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__3(x_4);
x_11 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_11, 0, x_9);
lean_ctor_set(x_11, 1, x_10);
x_12 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_12, 0, x_11);
lean_ctor_set(x_12, 1, x_7);
x_13 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_13, 0, x_12);
lean_ctor_set(x_13, 1, x_7);
x_14 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_14, 0, x_8);
lean_ctor_set(x_14, 1, x_13);
x_15 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_16 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_14, x_15);
x_17 = l_Lean_Json_mkObj(x_16);
return x_17;
}
else
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; 
x_18 = lean_ctor_get(x_1, 0);
x_19 = lean_ctor_get(x_1, 1);
lean_inc(x_19);
lean_inc(x_18);
lean_dec(x_1);
x_20 = lp_REPL_instFromJsonBatch_fromJson___closed__0;
x_21 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_21, 0, x_18);
x_22 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_22, 0, x_20);
lean_ctor_set(x_22, 1, x_21);
x_23 = lean_box(0);
x_24 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_24, 0, x_22);
lean_ctor_set(x_24, 1, x_23);
x_25 = lp_REPL_instFromJsonBatch_fromJson___closed__11;
x_26 = l_Array_toJson___at___00Lean_Server_Test_Runner_Client_instToJsonHyp_toJson_spec__3(x_19);
x_27 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_27, 0, x_25);
lean_ctor_set(x_27, 1, x_26);
x_28 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_28, 0, x_27);
lean_ctor_set(x_28, 1, x_23);
x_29 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_29, 0, x_28);
lean_ctor_set(x_29, 1, x_23);
x_30 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_30, 0, x_24);
lean_ctor_set(x_30, 1, x_29);
x_31 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_32 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_30, x_31);
x_33 = l_Lean_Json_mkObj(x_32);
return x_33;
}
}
}
static lean_object* _init_lp_REPL_instToJsonBatch___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_alloc_closure((void*)(lp_REPL_instToJsonBatch_toJson), 1, 0);
return x_1;
}
}
static lean_object* _init_lp_REPL_instToJsonBatch() {
_start:
{
lean_object* x_1; 
x_1 = lp_REPL_instToJsonBatch___closed__0;
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_ctorIdx(lean_object* x_1) {
_start:
{
switch (lean_obj_tag(x_1)) {
case 0:
{
lean_object* x_2; 
x_2 = lean_unsigned_to_nat(0u);
return x_2;
}
case 1:
{
lean_object* x_3; 
x_3 = lean_unsigned_to_nat(1u);
return x_3;
}
case 2:
{
lean_object* x_4; 
x_4 = lean_unsigned_to_nat(2u);
return x_4;
}
case 3:
{
lean_object* x_5; 
x_5 = lean_unsigned_to_nat(3u);
return x_5;
}
case 4:
{
lean_object* x_6; 
x_6 = lean_unsigned_to_nat(4u);
return x_6;
}
case 5:
{
lean_object* x_7; 
x_7 = lean_unsigned_to_nat(5u);
return x_7;
}
case 6:
{
lean_object* x_8; 
x_8 = lean_unsigned_to_nat(6u);
return x_8;
}
default: 
{
lean_object* x_9; 
x_9 = lean_unsigned_to_nat(7u);
return x_9;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_ctorIdx___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_REPL_Input_ctorIdx(x_1);
lean_dec_ref(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_ctorElim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; lean_object* x_4; 
x_3 = lean_ctor_get(x_1, 0);
lean_inc_ref(x_3);
lean_dec_ref(x_1);
x_4 = lean_apply_1(x_2, x_3);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_ctorElim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_Input_ctorElim___redArg(x_3, x_5);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_ctorElim___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_6; 
x_6 = lp_REPL_Input_ctorElim(x_1, x_2, x_3, x_4, x_5);
lean_dec(x_2);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_command_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_command_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_file_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_file_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_proofStep_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_proofStep_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_pickleEnvironment_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_pickleEnvironment_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleEnvironment_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleEnvironment_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_pickleProofSnapshot_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_pickleProofSnapshot_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleProofSnapshot_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_unpickleProofSnapshot_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_batchVerify_elim(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_Input_ctorElim___redArg(x_2, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_Input_batchVerify_elim___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_Input_ctorElim___redArg(x_1, x_2);
return x_3;
}
}
static lean_object* _init_lp_REPL_parse___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("Could not parse JSON:\n", 22, 22);
return x_1;
}
}
static lean_object* _init_lp_REPL_parse___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("Could not parse as a valid JSON command:\n", 41, 41);
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_parse(lean_object* x_1) {
_start:
{
lean_object* x_3; 
x_3 = l_Lean_Json_parse(x_1);
if (lean_obj_tag(x_3) == 0)
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_3);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; lean_object* x_10; lean_object* x_11; 
x_5 = lean_ctor_get(x_3, 0);
x_6 = lp_REPL_parse___closed__0;
x_7 = lean_string_append(x_6, x_5);
lean_dec(x_5);
x_8 = lp_REPL_REPL_instToJsonError_toJson(x_7);
x_9 = lean_unsigned_to_nat(80u);
x_10 = l_Lean_Json_pretty(x_8, x_9);
lean_ctor_set_tag(x_3, 18);
lean_ctor_set(x_3, 0, x_10);
x_11 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_11, 0, x_3);
return x_11;
}
else
{
lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; 
x_12 = lean_ctor_get(x_3, 0);
lean_inc(x_12);
lean_dec(x_3);
x_13 = lp_REPL_parse___closed__0;
x_14 = lean_string_append(x_13, x_12);
lean_dec(x_12);
x_15 = lp_REPL_REPL_instToJsonError_toJson(x_14);
x_16 = lean_unsigned_to_nat(80u);
x_17 = l_Lean_Json_pretty(x_15, x_16);
x_18 = lean_alloc_ctor(18, 1, 0);
lean_ctor_set(x_18, 0, x_17);
x_19 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_19, 0, x_18);
return x_19;
}
}
else
{
uint8_t x_20; 
x_20 = !lean_is_exclusive(x_3);
if (x_20 == 0)
{
lean_object* x_21; lean_object* x_22; 
x_21 = lean_ctor_get(x_3, 0);
lean_inc(x_21);
x_22 = lp_REPL_REPL_instFromJsonProofStep_fromJson(x_21);
if (lean_obj_tag(x_22) == 0)
{
uint8_t x_23; 
lean_free_object(x_3);
x_23 = !lean_is_exclusive(x_22);
if (x_23 == 0)
{
lean_object* x_24; lean_object* x_25; 
x_24 = lean_ctor_get(x_22, 0);
lean_dec(x_24);
lean_inc(x_21);
x_25 = lp_REPL_REPL_instFromJsonPickleEnvironment_fromJson(x_21);
if (lean_obj_tag(x_25) == 0)
{
uint8_t x_26; 
lean_free_object(x_22);
x_26 = !lean_is_exclusive(x_25);
if (x_26 == 0)
{
lean_object* x_27; lean_object* x_28; 
x_27 = lean_ctor_get(x_25, 0);
lean_dec(x_27);
lean_inc(x_21);
x_28 = lp_REPL_REPL_instFromJsonUnpickleEnvironment_fromJson(x_21);
if (lean_obj_tag(x_28) == 0)
{
uint8_t x_29; 
lean_free_object(x_25);
x_29 = !lean_is_exclusive(x_28);
if (x_29 == 0)
{
lean_object* x_30; lean_object* x_31; 
x_30 = lean_ctor_get(x_28, 0);
lean_dec(x_30);
lean_inc(x_21);
x_31 = lp_REPL_REPL_instFromJsonPickleProofState_fromJson(x_21);
if (lean_obj_tag(x_31) == 0)
{
uint8_t x_32; 
lean_free_object(x_28);
x_32 = !lean_is_exclusive(x_31);
if (x_32 == 0)
{
lean_object* x_33; lean_object* x_34; 
x_33 = lean_ctor_get(x_31, 0);
lean_dec(x_33);
lean_inc(x_21);
x_34 = lp_REPL_REPL_instFromJsonUnpickleProofState_fromJson(x_21);
if (lean_obj_tag(x_34) == 0)
{
uint8_t x_35; 
lean_free_object(x_31);
x_35 = !lean_is_exclusive(x_34);
if (x_35 == 0)
{
lean_object* x_36; lean_object* x_37; 
x_36 = lean_ctor_get(x_34, 0);
lean_dec(x_36);
lean_inc(x_21);
x_37 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_21);
if (lean_obj_tag(x_37) == 0)
{
uint8_t x_38; 
lean_free_object(x_34);
x_38 = !lean_is_exclusive(x_37);
if (x_38 == 0)
{
lean_object* x_39; lean_object* x_40; 
x_39 = lean_ctor_get(x_37, 0);
lean_dec(x_39);
lean_inc(x_21);
x_40 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_21);
if (lean_obj_tag(x_40) == 0)
{
uint8_t x_41; 
lean_free_object(x_37);
x_41 = !lean_is_exclusive(x_40);
if (x_41 == 0)
{
lean_object* x_42; lean_object* x_43; 
x_42 = lean_ctor_get(x_40, 0);
lean_dec(x_42);
x_43 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_43) == 0)
{
uint8_t x_44; 
x_44 = !lean_is_exclusive(x_43);
if (x_44 == 0)
{
lean_object* x_45; lean_object* x_46; lean_object* x_47; lean_object* x_48; lean_object* x_49; lean_object* x_50; 
x_45 = lean_ctor_get(x_43, 0);
x_46 = lp_REPL_parse___closed__1;
x_47 = lean_string_append(x_46, x_45);
lean_dec(x_45);
x_48 = lp_REPL_REPL_instToJsonError_toJson(x_47);
x_49 = lean_unsigned_to_nat(80u);
x_50 = l_Lean_Json_pretty(x_48, x_49);
lean_ctor_set_tag(x_43, 18);
lean_ctor_set(x_43, 0, x_50);
lean_ctor_set_tag(x_40, 1);
lean_ctor_set(x_40, 0, x_43);
return x_40;
}
else
{
lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; lean_object* x_57; 
x_51 = lean_ctor_get(x_43, 0);
lean_inc(x_51);
lean_dec(x_43);
x_52 = lp_REPL_parse___closed__1;
x_53 = lean_string_append(x_52, x_51);
lean_dec(x_51);
x_54 = lp_REPL_REPL_instToJsonError_toJson(x_53);
x_55 = lean_unsigned_to_nat(80u);
x_56 = l_Lean_Json_pretty(x_54, x_55);
x_57 = lean_alloc_ctor(18, 1, 0);
lean_ctor_set(x_57, 0, x_56);
lean_ctor_set_tag(x_40, 1);
lean_ctor_set(x_40, 0, x_57);
return x_40;
}
}
else
{
uint8_t x_58; 
x_58 = !lean_is_exclusive(x_43);
if (x_58 == 0)
{
lean_ctor_set(x_40, 0, x_43);
return x_40;
}
else
{
lean_object* x_59; lean_object* x_60; 
x_59 = lean_ctor_get(x_43, 0);
lean_inc(x_59);
lean_dec(x_43);
x_60 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_60, 0, x_59);
lean_ctor_set(x_40, 0, x_60);
return x_40;
}
}
}
else
{
lean_object* x_61; 
lean_dec(x_40);
x_61 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_61) == 0)
{
lean_object* x_62; lean_object* x_63; lean_object* x_64; lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_68; lean_object* x_69; lean_object* x_70; 
x_62 = lean_ctor_get(x_61, 0);
lean_inc(x_62);
if (lean_is_exclusive(x_61)) {
 lean_ctor_release(x_61, 0);
 x_63 = x_61;
} else {
 lean_dec_ref(x_61);
 x_63 = lean_box(0);
}
x_64 = lp_REPL_parse___closed__1;
x_65 = lean_string_append(x_64, x_62);
lean_dec(x_62);
x_66 = lp_REPL_REPL_instToJsonError_toJson(x_65);
x_67 = lean_unsigned_to_nat(80u);
x_68 = l_Lean_Json_pretty(x_66, x_67);
if (lean_is_scalar(x_63)) {
 x_69 = lean_alloc_ctor(18, 1, 0);
} else {
 x_69 = x_63;
 lean_ctor_set_tag(x_69, 18);
}
lean_ctor_set(x_69, 0, x_68);
x_70 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_70, 0, x_69);
return x_70;
}
else
{
lean_object* x_71; lean_object* x_72; lean_object* x_73; lean_object* x_74; 
x_71 = lean_ctor_get(x_61, 0);
lean_inc(x_71);
if (lean_is_exclusive(x_61)) {
 lean_ctor_release(x_61, 0);
 x_72 = x_61;
} else {
 lean_dec_ref(x_61);
 x_72 = lean_box(0);
}
if (lean_is_scalar(x_72)) {
 x_73 = lean_alloc_ctor(1, 1, 0);
} else {
 x_73 = x_72;
}
lean_ctor_set(x_73, 0, x_71);
x_74 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_74, 0, x_73);
return x_74;
}
}
}
else
{
uint8_t x_75; 
lean_dec(x_21);
x_75 = !lean_is_exclusive(x_40);
if (x_75 == 0)
{
lean_ctor_set_tag(x_40, 7);
lean_ctor_set(x_37, 0, x_40);
return x_37;
}
else
{
lean_object* x_76; lean_object* x_77; 
x_76 = lean_ctor_get(x_40, 0);
lean_inc(x_76);
lean_dec(x_40);
x_77 = lean_alloc_ctor(7, 1, 0);
lean_ctor_set(x_77, 0, x_76);
lean_ctor_set(x_37, 0, x_77);
return x_37;
}
}
}
else
{
lean_object* x_78; 
lean_dec(x_37);
lean_inc(x_21);
x_78 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_21);
if (lean_obj_tag(x_78) == 0)
{
lean_object* x_79; lean_object* x_80; 
if (lean_is_exclusive(x_78)) {
 lean_ctor_release(x_78, 0);
 x_79 = x_78;
} else {
 lean_dec_ref(x_78);
 x_79 = lean_box(0);
}
x_80 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_80) == 0)
{
lean_object* x_81; lean_object* x_82; lean_object* x_83; lean_object* x_84; lean_object* x_85; lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; 
x_81 = lean_ctor_get(x_80, 0);
lean_inc(x_81);
if (lean_is_exclusive(x_80)) {
 lean_ctor_release(x_80, 0);
 x_82 = x_80;
} else {
 lean_dec_ref(x_80);
 x_82 = lean_box(0);
}
x_83 = lp_REPL_parse___closed__1;
x_84 = lean_string_append(x_83, x_81);
lean_dec(x_81);
x_85 = lp_REPL_REPL_instToJsonError_toJson(x_84);
x_86 = lean_unsigned_to_nat(80u);
x_87 = l_Lean_Json_pretty(x_85, x_86);
if (lean_is_scalar(x_82)) {
 x_88 = lean_alloc_ctor(18, 1, 0);
} else {
 x_88 = x_82;
 lean_ctor_set_tag(x_88, 18);
}
lean_ctor_set(x_88, 0, x_87);
if (lean_is_scalar(x_79)) {
 x_89 = lean_alloc_ctor(1, 1, 0);
} else {
 x_89 = x_79;
 lean_ctor_set_tag(x_89, 1);
}
lean_ctor_set(x_89, 0, x_88);
return x_89;
}
else
{
lean_object* x_90; lean_object* x_91; lean_object* x_92; lean_object* x_93; 
x_90 = lean_ctor_get(x_80, 0);
lean_inc(x_90);
if (lean_is_exclusive(x_80)) {
 lean_ctor_release(x_80, 0);
 x_91 = x_80;
} else {
 lean_dec_ref(x_80);
 x_91 = lean_box(0);
}
if (lean_is_scalar(x_91)) {
 x_92 = lean_alloc_ctor(1, 1, 0);
} else {
 x_92 = x_91;
}
lean_ctor_set(x_92, 0, x_90);
if (lean_is_scalar(x_79)) {
 x_93 = lean_alloc_ctor(0, 1, 0);
} else {
 x_93 = x_79;
}
lean_ctor_set(x_93, 0, x_92);
return x_93;
}
}
else
{
lean_object* x_94; lean_object* x_95; lean_object* x_96; lean_object* x_97; 
lean_dec(x_21);
x_94 = lean_ctor_get(x_78, 0);
lean_inc(x_94);
if (lean_is_exclusive(x_78)) {
 lean_ctor_release(x_78, 0);
 x_95 = x_78;
} else {
 lean_dec_ref(x_78);
 x_95 = lean_box(0);
}
if (lean_is_scalar(x_95)) {
 x_96 = lean_alloc_ctor(7, 1, 0);
} else {
 x_96 = x_95;
 lean_ctor_set_tag(x_96, 7);
}
lean_ctor_set(x_96, 0, x_94);
x_97 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_97, 0, x_96);
return x_97;
}
}
}
else
{
uint8_t x_98; 
lean_dec(x_21);
x_98 = !lean_is_exclusive(x_37);
if (x_98 == 0)
{
lean_ctor_set_tag(x_37, 0);
lean_ctor_set(x_34, 0, x_37);
return x_34;
}
else
{
lean_object* x_99; lean_object* x_100; 
x_99 = lean_ctor_get(x_37, 0);
lean_inc(x_99);
lean_dec(x_37);
x_100 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_100, 0, x_99);
lean_ctor_set(x_34, 0, x_100);
return x_34;
}
}
}
else
{
lean_object* x_101; 
lean_dec(x_34);
lean_inc(x_21);
x_101 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_21);
if (lean_obj_tag(x_101) == 0)
{
lean_object* x_102; lean_object* x_103; 
if (lean_is_exclusive(x_101)) {
 lean_ctor_release(x_101, 0);
 x_102 = x_101;
} else {
 lean_dec_ref(x_101);
 x_102 = lean_box(0);
}
lean_inc(x_21);
x_103 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_21);
if (lean_obj_tag(x_103) == 0)
{
lean_object* x_104; lean_object* x_105; 
lean_dec(x_102);
if (lean_is_exclusive(x_103)) {
 lean_ctor_release(x_103, 0);
 x_104 = x_103;
} else {
 lean_dec_ref(x_103);
 x_104 = lean_box(0);
}
x_105 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_105) == 0)
{
lean_object* x_106; lean_object* x_107; lean_object* x_108; lean_object* x_109; lean_object* x_110; lean_object* x_111; lean_object* x_112; lean_object* x_113; lean_object* x_114; 
x_106 = lean_ctor_get(x_105, 0);
lean_inc(x_106);
if (lean_is_exclusive(x_105)) {
 lean_ctor_release(x_105, 0);
 x_107 = x_105;
} else {
 lean_dec_ref(x_105);
 x_107 = lean_box(0);
}
x_108 = lp_REPL_parse___closed__1;
x_109 = lean_string_append(x_108, x_106);
lean_dec(x_106);
x_110 = lp_REPL_REPL_instToJsonError_toJson(x_109);
x_111 = lean_unsigned_to_nat(80u);
x_112 = l_Lean_Json_pretty(x_110, x_111);
if (lean_is_scalar(x_107)) {
 x_113 = lean_alloc_ctor(18, 1, 0);
} else {
 x_113 = x_107;
 lean_ctor_set_tag(x_113, 18);
}
lean_ctor_set(x_113, 0, x_112);
if (lean_is_scalar(x_104)) {
 x_114 = lean_alloc_ctor(1, 1, 0);
} else {
 x_114 = x_104;
 lean_ctor_set_tag(x_114, 1);
}
lean_ctor_set(x_114, 0, x_113);
return x_114;
}
else
{
lean_object* x_115; lean_object* x_116; lean_object* x_117; lean_object* x_118; 
x_115 = lean_ctor_get(x_105, 0);
lean_inc(x_115);
if (lean_is_exclusive(x_105)) {
 lean_ctor_release(x_105, 0);
 x_116 = x_105;
} else {
 lean_dec_ref(x_105);
 x_116 = lean_box(0);
}
if (lean_is_scalar(x_116)) {
 x_117 = lean_alloc_ctor(1, 1, 0);
} else {
 x_117 = x_116;
}
lean_ctor_set(x_117, 0, x_115);
if (lean_is_scalar(x_104)) {
 x_118 = lean_alloc_ctor(0, 1, 0);
} else {
 x_118 = x_104;
}
lean_ctor_set(x_118, 0, x_117);
return x_118;
}
}
else
{
lean_object* x_119; lean_object* x_120; lean_object* x_121; lean_object* x_122; 
lean_dec(x_21);
x_119 = lean_ctor_get(x_103, 0);
lean_inc(x_119);
if (lean_is_exclusive(x_103)) {
 lean_ctor_release(x_103, 0);
 x_120 = x_103;
} else {
 lean_dec_ref(x_103);
 x_120 = lean_box(0);
}
if (lean_is_scalar(x_120)) {
 x_121 = lean_alloc_ctor(7, 1, 0);
} else {
 x_121 = x_120;
 lean_ctor_set_tag(x_121, 7);
}
lean_ctor_set(x_121, 0, x_119);
if (lean_is_scalar(x_102)) {
 x_122 = lean_alloc_ctor(0, 1, 0);
} else {
 x_122 = x_102;
}
lean_ctor_set(x_122, 0, x_121);
return x_122;
}
}
else
{
lean_object* x_123; lean_object* x_124; lean_object* x_125; lean_object* x_126; 
lean_dec(x_21);
x_123 = lean_ctor_get(x_101, 0);
lean_inc(x_123);
if (lean_is_exclusive(x_101)) {
 lean_ctor_release(x_101, 0);
 x_124 = x_101;
} else {
 lean_dec_ref(x_101);
 x_124 = lean_box(0);
}
if (lean_is_scalar(x_124)) {
 x_125 = lean_alloc_ctor(0, 1, 0);
} else {
 x_125 = x_124;
 lean_ctor_set_tag(x_125, 0);
}
lean_ctor_set(x_125, 0, x_123);
x_126 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_126, 0, x_125);
return x_126;
}
}
}
else
{
uint8_t x_127; 
lean_dec(x_21);
x_127 = !lean_is_exclusive(x_34);
if (x_127 == 0)
{
lean_ctor_set_tag(x_34, 6);
lean_ctor_set(x_31, 0, x_34);
return x_31;
}
else
{
lean_object* x_128; lean_object* x_129; 
x_128 = lean_ctor_get(x_34, 0);
lean_inc(x_128);
lean_dec(x_34);
x_129 = lean_alloc_ctor(6, 1, 0);
lean_ctor_set(x_129, 0, x_128);
lean_ctor_set(x_31, 0, x_129);
return x_31;
}
}
}
else
{
lean_object* x_130; 
lean_dec(x_31);
lean_inc(x_21);
x_130 = lp_REPL_REPL_instFromJsonUnpickleProofState_fromJson(x_21);
if (lean_obj_tag(x_130) == 0)
{
lean_object* x_131; lean_object* x_132; 
if (lean_is_exclusive(x_130)) {
 lean_ctor_release(x_130, 0);
 x_131 = x_130;
} else {
 lean_dec_ref(x_130);
 x_131 = lean_box(0);
}
lean_inc(x_21);
x_132 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_21);
if (lean_obj_tag(x_132) == 0)
{
lean_object* x_133; lean_object* x_134; 
lean_dec(x_131);
if (lean_is_exclusive(x_132)) {
 lean_ctor_release(x_132, 0);
 x_133 = x_132;
} else {
 lean_dec_ref(x_132);
 x_133 = lean_box(0);
}
lean_inc(x_21);
x_134 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_21);
if (lean_obj_tag(x_134) == 0)
{
lean_object* x_135; lean_object* x_136; 
lean_dec(x_133);
if (lean_is_exclusive(x_134)) {
 lean_ctor_release(x_134, 0);
 x_135 = x_134;
} else {
 lean_dec_ref(x_134);
 x_135 = lean_box(0);
}
x_136 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_136) == 0)
{
lean_object* x_137; lean_object* x_138; lean_object* x_139; lean_object* x_140; lean_object* x_141; lean_object* x_142; lean_object* x_143; lean_object* x_144; lean_object* x_145; 
x_137 = lean_ctor_get(x_136, 0);
lean_inc(x_137);
if (lean_is_exclusive(x_136)) {
 lean_ctor_release(x_136, 0);
 x_138 = x_136;
} else {
 lean_dec_ref(x_136);
 x_138 = lean_box(0);
}
x_139 = lp_REPL_parse___closed__1;
x_140 = lean_string_append(x_139, x_137);
lean_dec(x_137);
x_141 = lp_REPL_REPL_instToJsonError_toJson(x_140);
x_142 = lean_unsigned_to_nat(80u);
x_143 = l_Lean_Json_pretty(x_141, x_142);
if (lean_is_scalar(x_138)) {
 x_144 = lean_alloc_ctor(18, 1, 0);
} else {
 x_144 = x_138;
 lean_ctor_set_tag(x_144, 18);
}
lean_ctor_set(x_144, 0, x_143);
if (lean_is_scalar(x_135)) {
 x_145 = lean_alloc_ctor(1, 1, 0);
} else {
 x_145 = x_135;
 lean_ctor_set_tag(x_145, 1);
}
lean_ctor_set(x_145, 0, x_144);
return x_145;
}
else
{
lean_object* x_146; lean_object* x_147; lean_object* x_148; lean_object* x_149; 
x_146 = lean_ctor_get(x_136, 0);
lean_inc(x_146);
if (lean_is_exclusive(x_136)) {
 lean_ctor_release(x_136, 0);
 x_147 = x_136;
} else {
 lean_dec_ref(x_136);
 x_147 = lean_box(0);
}
if (lean_is_scalar(x_147)) {
 x_148 = lean_alloc_ctor(1, 1, 0);
} else {
 x_148 = x_147;
}
lean_ctor_set(x_148, 0, x_146);
if (lean_is_scalar(x_135)) {
 x_149 = lean_alloc_ctor(0, 1, 0);
} else {
 x_149 = x_135;
}
lean_ctor_set(x_149, 0, x_148);
return x_149;
}
}
else
{
lean_object* x_150; lean_object* x_151; lean_object* x_152; lean_object* x_153; 
lean_dec(x_21);
x_150 = lean_ctor_get(x_134, 0);
lean_inc(x_150);
if (lean_is_exclusive(x_134)) {
 lean_ctor_release(x_134, 0);
 x_151 = x_134;
} else {
 lean_dec_ref(x_134);
 x_151 = lean_box(0);
}
if (lean_is_scalar(x_151)) {
 x_152 = lean_alloc_ctor(7, 1, 0);
} else {
 x_152 = x_151;
 lean_ctor_set_tag(x_152, 7);
}
lean_ctor_set(x_152, 0, x_150);
if (lean_is_scalar(x_133)) {
 x_153 = lean_alloc_ctor(0, 1, 0);
} else {
 x_153 = x_133;
}
lean_ctor_set(x_153, 0, x_152);
return x_153;
}
}
else
{
lean_object* x_154; lean_object* x_155; lean_object* x_156; lean_object* x_157; 
lean_dec(x_21);
x_154 = lean_ctor_get(x_132, 0);
lean_inc(x_154);
if (lean_is_exclusive(x_132)) {
 lean_ctor_release(x_132, 0);
 x_155 = x_132;
} else {
 lean_dec_ref(x_132);
 x_155 = lean_box(0);
}
if (lean_is_scalar(x_155)) {
 x_156 = lean_alloc_ctor(0, 1, 0);
} else {
 x_156 = x_155;
 lean_ctor_set_tag(x_156, 0);
}
lean_ctor_set(x_156, 0, x_154);
if (lean_is_scalar(x_131)) {
 x_157 = lean_alloc_ctor(0, 1, 0);
} else {
 x_157 = x_131;
}
lean_ctor_set(x_157, 0, x_156);
return x_157;
}
}
else
{
lean_object* x_158; lean_object* x_159; lean_object* x_160; lean_object* x_161; 
lean_dec(x_21);
x_158 = lean_ctor_get(x_130, 0);
lean_inc(x_158);
if (lean_is_exclusive(x_130)) {
 lean_ctor_release(x_130, 0);
 x_159 = x_130;
} else {
 lean_dec_ref(x_130);
 x_159 = lean_box(0);
}
if (lean_is_scalar(x_159)) {
 x_160 = lean_alloc_ctor(6, 1, 0);
} else {
 x_160 = x_159;
 lean_ctor_set_tag(x_160, 6);
}
lean_ctor_set(x_160, 0, x_158);
x_161 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_161, 0, x_160);
return x_161;
}
}
}
else
{
uint8_t x_162; 
lean_dec(x_21);
x_162 = !lean_is_exclusive(x_31);
if (x_162 == 0)
{
lean_ctor_set_tag(x_31, 5);
lean_ctor_set(x_28, 0, x_31);
return x_28;
}
else
{
lean_object* x_163; lean_object* x_164; 
x_163 = lean_ctor_get(x_31, 0);
lean_inc(x_163);
lean_dec(x_31);
x_164 = lean_alloc_ctor(5, 1, 0);
lean_ctor_set(x_164, 0, x_163);
lean_ctor_set(x_28, 0, x_164);
return x_28;
}
}
}
else
{
lean_object* x_165; 
lean_dec(x_28);
lean_inc(x_21);
x_165 = lp_REPL_REPL_instFromJsonPickleProofState_fromJson(x_21);
if (lean_obj_tag(x_165) == 0)
{
lean_object* x_166; lean_object* x_167; 
if (lean_is_exclusive(x_165)) {
 lean_ctor_release(x_165, 0);
 x_166 = x_165;
} else {
 lean_dec_ref(x_165);
 x_166 = lean_box(0);
}
lean_inc(x_21);
x_167 = lp_REPL_REPL_instFromJsonUnpickleProofState_fromJson(x_21);
if (lean_obj_tag(x_167) == 0)
{
lean_object* x_168; lean_object* x_169; 
lean_dec(x_166);
if (lean_is_exclusive(x_167)) {
 lean_ctor_release(x_167, 0);
 x_168 = x_167;
} else {
 lean_dec_ref(x_167);
 x_168 = lean_box(0);
}
lean_inc(x_21);
x_169 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_21);
if (lean_obj_tag(x_169) == 0)
{
lean_object* x_170; lean_object* x_171; 
lean_dec(x_168);
if (lean_is_exclusive(x_169)) {
 lean_ctor_release(x_169, 0);
 x_170 = x_169;
} else {
 lean_dec_ref(x_169);
 x_170 = lean_box(0);
}
lean_inc(x_21);
x_171 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_21);
if (lean_obj_tag(x_171) == 0)
{
lean_object* x_172; lean_object* x_173; 
lean_dec(x_170);
if (lean_is_exclusive(x_171)) {
 lean_ctor_release(x_171, 0);
 x_172 = x_171;
} else {
 lean_dec_ref(x_171);
 x_172 = lean_box(0);
}
x_173 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_173) == 0)
{
lean_object* x_174; lean_object* x_175; lean_object* x_176; lean_object* x_177; lean_object* x_178; lean_object* x_179; lean_object* x_180; lean_object* x_181; lean_object* x_182; 
x_174 = lean_ctor_get(x_173, 0);
lean_inc(x_174);
if (lean_is_exclusive(x_173)) {
 lean_ctor_release(x_173, 0);
 x_175 = x_173;
} else {
 lean_dec_ref(x_173);
 x_175 = lean_box(0);
}
x_176 = lp_REPL_parse___closed__1;
x_177 = lean_string_append(x_176, x_174);
lean_dec(x_174);
x_178 = lp_REPL_REPL_instToJsonError_toJson(x_177);
x_179 = lean_unsigned_to_nat(80u);
x_180 = l_Lean_Json_pretty(x_178, x_179);
if (lean_is_scalar(x_175)) {
 x_181 = lean_alloc_ctor(18, 1, 0);
} else {
 x_181 = x_175;
 lean_ctor_set_tag(x_181, 18);
}
lean_ctor_set(x_181, 0, x_180);
if (lean_is_scalar(x_172)) {
 x_182 = lean_alloc_ctor(1, 1, 0);
} else {
 x_182 = x_172;
 lean_ctor_set_tag(x_182, 1);
}
lean_ctor_set(x_182, 0, x_181);
return x_182;
}
else
{
lean_object* x_183; lean_object* x_184; lean_object* x_185; lean_object* x_186; 
x_183 = lean_ctor_get(x_173, 0);
lean_inc(x_183);
if (lean_is_exclusive(x_173)) {
 lean_ctor_release(x_173, 0);
 x_184 = x_173;
} else {
 lean_dec_ref(x_173);
 x_184 = lean_box(0);
}
if (lean_is_scalar(x_184)) {
 x_185 = lean_alloc_ctor(1, 1, 0);
} else {
 x_185 = x_184;
}
lean_ctor_set(x_185, 0, x_183);
if (lean_is_scalar(x_172)) {
 x_186 = lean_alloc_ctor(0, 1, 0);
} else {
 x_186 = x_172;
}
lean_ctor_set(x_186, 0, x_185);
return x_186;
}
}
else
{
lean_object* x_187; lean_object* x_188; lean_object* x_189; lean_object* x_190; 
lean_dec(x_21);
x_187 = lean_ctor_get(x_171, 0);
lean_inc(x_187);
if (lean_is_exclusive(x_171)) {
 lean_ctor_release(x_171, 0);
 x_188 = x_171;
} else {
 lean_dec_ref(x_171);
 x_188 = lean_box(0);
}
if (lean_is_scalar(x_188)) {
 x_189 = lean_alloc_ctor(7, 1, 0);
} else {
 x_189 = x_188;
 lean_ctor_set_tag(x_189, 7);
}
lean_ctor_set(x_189, 0, x_187);
if (lean_is_scalar(x_170)) {
 x_190 = lean_alloc_ctor(0, 1, 0);
} else {
 x_190 = x_170;
}
lean_ctor_set(x_190, 0, x_189);
return x_190;
}
}
else
{
lean_object* x_191; lean_object* x_192; lean_object* x_193; lean_object* x_194; 
lean_dec(x_21);
x_191 = lean_ctor_get(x_169, 0);
lean_inc(x_191);
if (lean_is_exclusive(x_169)) {
 lean_ctor_release(x_169, 0);
 x_192 = x_169;
} else {
 lean_dec_ref(x_169);
 x_192 = lean_box(0);
}
if (lean_is_scalar(x_192)) {
 x_193 = lean_alloc_ctor(0, 1, 0);
} else {
 x_193 = x_192;
 lean_ctor_set_tag(x_193, 0);
}
lean_ctor_set(x_193, 0, x_191);
if (lean_is_scalar(x_168)) {
 x_194 = lean_alloc_ctor(0, 1, 0);
} else {
 x_194 = x_168;
}
lean_ctor_set(x_194, 0, x_193);
return x_194;
}
}
else
{
lean_object* x_195; lean_object* x_196; lean_object* x_197; lean_object* x_198; 
lean_dec(x_21);
x_195 = lean_ctor_get(x_167, 0);
lean_inc(x_195);
if (lean_is_exclusive(x_167)) {
 lean_ctor_release(x_167, 0);
 x_196 = x_167;
} else {
 lean_dec_ref(x_167);
 x_196 = lean_box(0);
}
if (lean_is_scalar(x_196)) {
 x_197 = lean_alloc_ctor(6, 1, 0);
} else {
 x_197 = x_196;
 lean_ctor_set_tag(x_197, 6);
}
lean_ctor_set(x_197, 0, x_195);
if (lean_is_scalar(x_166)) {
 x_198 = lean_alloc_ctor(0, 1, 0);
} else {
 x_198 = x_166;
}
lean_ctor_set(x_198, 0, x_197);
return x_198;
}
}
else
{
lean_object* x_199; lean_object* x_200; lean_object* x_201; lean_object* x_202; 
lean_dec(x_21);
x_199 = lean_ctor_get(x_165, 0);
lean_inc(x_199);
if (lean_is_exclusive(x_165)) {
 lean_ctor_release(x_165, 0);
 x_200 = x_165;
} else {
 lean_dec_ref(x_165);
 x_200 = lean_box(0);
}
if (lean_is_scalar(x_200)) {
 x_201 = lean_alloc_ctor(5, 1, 0);
} else {
 x_201 = x_200;
 lean_ctor_set_tag(x_201, 5);
}
lean_ctor_set(x_201, 0, x_199);
x_202 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_202, 0, x_201);
return x_202;
}
}
}
else
{
uint8_t x_203; 
lean_dec(x_21);
x_203 = !lean_is_exclusive(x_28);
if (x_203 == 0)
{
lean_ctor_set_tag(x_28, 4);
lean_ctor_set(x_25, 0, x_28);
return x_25;
}
else
{
lean_object* x_204; lean_object* x_205; 
x_204 = lean_ctor_get(x_28, 0);
lean_inc(x_204);
lean_dec(x_28);
x_205 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_205, 0, x_204);
lean_ctor_set(x_25, 0, x_205);
return x_25;
}
}
}
else
{
lean_object* x_206; 
lean_dec(x_25);
lean_inc(x_21);
x_206 = lp_REPL_REPL_instFromJsonUnpickleEnvironment_fromJson(x_21);
if (lean_obj_tag(x_206) == 0)
{
lean_object* x_207; lean_object* x_208; 
if (lean_is_exclusive(x_206)) {
 lean_ctor_release(x_206, 0);
 x_207 = x_206;
} else {
 lean_dec_ref(x_206);
 x_207 = lean_box(0);
}
lean_inc(x_21);
x_208 = lp_REPL_REPL_instFromJsonPickleProofState_fromJson(x_21);
if (lean_obj_tag(x_208) == 0)
{
lean_object* x_209; lean_object* x_210; 
lean_dec(x_207);
if (lean_is_exclusive(x_208)) {
 lean_ctor_release(x_208, 0);
 x_209 = x_208;
} else {
 lean_dec_ref(x_208);
 x_209 = lean_box(0);
}
lean_inc(x_21);
x_210 = lp_REPL_REPL_instFromJsonUnpickleProofState_fromJson(x_21);
if (lean_obj_tag(x_210) == 0)
{
lean_object* x_211; lean_object* x_212; 
lean_dec(x_209);
if (lean_is_exclusive(x_210)) {
 lean_ctor_release(x_210, 0);
 x_211 = x_210;
} else {
 lean_dec_ref(x_210);
 x_211 = lean_box(0);
}
lean_inc(x_21);
x_212 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_21);
if (lean_obj_tag(x_212) == 0)
{
lean_object* x_213; lean_object* x_214; 
lean_dec(x_211);
if (lean_is_exclusive(x_212)) {
 lean_ctor_release(x_212, 0);
 x_213 = x_212;
} else {
 lean_dec_ref(x_212);
 x_213 = lean_box(0);
}
lean_inc(x_21);
x_214 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_21);
if (lean_obj_tag(x_214) == 0)
{
lean_object* x_215; lean_object* x_216; 
lean_dec(x_213);
if (lean_is_exclusive(x_214)) {
 lean_ctor_release(x_214, 0);
 x_215 = x_214;
} else {
 lean_dec_ref(x_214);
 x_215 = lean_box(0);
}
x_216 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_216) == 0)
{
lean_object* x_217; lean_object* x_218; lean_object* x_219; lean_object* x_220; lean_object* x_221; lean_object* x_222; lean_object* x_223; lean_object* x_224; lean_object* x_225; 
x_217 = lean_ctor_get(x_216, 0);
lean_inc(x_217);
if (lean_is_exclusive(x_216)) {
 lean_ctor_release(x_216, 0);
 x_218 = x_216;
} else {
 lean_dec_ref(x_216);
 x_218 = lean_box(0);
}
x_219 = lp_REPL_parse___closed__1;
x_220 = lean_string_append(x_219, x_217);
lean_dec(x_217);
x_221 = lp_REPL_REPL_instToJsonError_toJson(x_220);
x_222 = lean_unsigned_to_nat(80u);
x_223 = l_Lean_Json_pretty(x_221, x_222);
if (lean_is_scalar(x_218)) {
 x_224 = lean_alloc_ctor(18, 1, 0);
} else {
 x_224 = x_218;
 lean_ctor_set_tag(x_224, 18);
}
lean_ctor_set(x_224, 0, x_223);
if (lean_is_scalar(x_215)) {
 x_225 = lean_alloc_ctor(1, 1, 0);
} else {
 x_225 = x_215;
 lean_ctor_set_tag(x_225, 1);
}
lean_ctor_set(x_225, 0, x_224);
return x_225;
}
else
{
lean_object* x_226; lean_object* x_227; lean_object* x_228; lean_object* x_229; 
x_226 = lean_ctor_get(x_216, 0);
lean_inc(x_226);
if (lean_is_exclusive(x_216)) {
 lean_ctor_release(x_216, 0);
 x_227 = x_216;
} else {
 lean_dec_ref(x_216);
 x_227 = lean_box(0);
}
if (lean_is_scalar(x_227)) {
 x_228 = lean_alloc_ctor(1, 1, 0);
} else {
 x_228 = x_227;
}
lean_ctor_set(x_228, 0, x_226);
if (lean_is_scalar(x_215)) {
 x_229 = lean_alloc_ctor(0, 1, 0);
} else {
 x_229 = x_215;
}
lean_ctor_set(x_229, 0, x_228);
return x_229;
}
}
else
{
lean_object* x_230; lean_object* x_231; lean_object* x_232; lean_object* x_233; 
lean_dec(x_21);
x_230 = lean_ctor_get(x_214, 0);
lean_inc(x_230);
if (lean_is_exclusive(x_214)) {
 lean_ctor_release(x_214, 0);
 x_231 = x_214;
} else {
 lean_dec_ref(x_214);
 x_231 = lean_box(0);
}
if (lean_is_scalar(x_231)) {
 x_232 = lean_alloc_ctor(7, 1, 0);
} else {
 x_232 = x_231;
 lean_ctor_set_tag(x_232, 7);
}
lean_ctor_set(x_232, 0, x_230);
if (lean_is_scalar(x_213)) {
 x_233 = lean_alloc_ctor(0, 1, 0);
} else {
 x_233 = x_213;
}
lean_ctor_set(x_233, 0, x_232);
return x_233;
}
}
else
{
lean_object* x_234; lean_object* x_235; lean_object* x_236; lean_object* x_237; 
lean_dec(x_21);
x_234 = lean_ctor_get(x_212, 0);
lean_inc(x_234);
if (lean_is_exclusive(x_212)) {
 lean_ctor_release(x_212, 0);
 x_235 = x_212;
} else {
 lean_dec_ref(x_212);
 x_235 = lean_box(0);
}
if (lean_is_scalar(x_235)) {
 x_236 = lean_alloc_ctor(0, 1, 0);
} else {
 x_236 = x_235;
 lean_ctor_set_tag(x_236, 0);
}
lean_ctor_set(x_236, 0, x_234);
if (lean_is_scalar(x_211)) {
 x_237 = lean_alloc_ctor(0, 1, 0);
} else {
 x_237 = x_211;
}
lean_ctor_set(x_237, 0, x_236);
return x_237;
}
}
else
{
lean_object* x_238; lean_object* x_239; lean_object* x_240; lean_object* x_241; 
lean_dec(x_21);
x_238 = lean_ctor_get(x_210, 0);
lean_inc(x_238);
if (lean_is_exclusive(x_210)) {
 lean_ctor_release(x_210, 0);
 x_239 = x_210;
} else {
 lean_dec_ref(x_210);
 x_239 = lean_box(0);
}
if (lean_is_scalar(x_239)) {
 x_240 = lean_alloc_ctor(6, 1, 0);
} else {
 x_240 = x_239;
 lean_ctor_set_tag(x_240, 6);
}
lean_ctor_set(x_240, 0, x_238);
if (lean_is_scalar(x_209)) {
 x_241 = lean_alloc_ctor(0, 1, 0);
} else {
 x_241 = x_209;
}
lean_ctor_set(x_241, 0, x_240);
return x_241;
}
}
else
{
lean_object* x_242; lean_object* x_243; lean_object* x_244; lean_object* x_245; 
lean_dec(x_21);
x_242 = lean_ctor_get(x_208, 0);
lean_inc(x_242);
if (lean_is_exclusive(x_208)) {
 lean_ctor_release(x_208, 0);
 x_243 = x_208;
} else {
 lean_dec_ref(x_208);
 x_243 = lean_box(0);
}
if (lean_is_scalar(x_243)) {
 x_244 = lean_alloc_ctor(5, 1, 0);
} else {
 x_244 = x_243;
 lean_ctor_set_tag(x_244, 5);
}
lean_ctor_set(x_244, 0, x_242);
if (lean_is_scalar(x_207)) {
 x_245 = lean_alloc_ctor(0, 1, 0);
} else {
 x_245 = x_207;
}
lean_ctor_set(x_245, 0, x_244);
return x_245;
}
}
else
{
lean_object* x_246; lean_object* x_247; lean_object* x_248; lean_object* x_249; 
lean_dec(x_21);
x_246 = lean_ctor_get(x_206, 0);
lean_inc(x_246);
if (lean_is_exclusive(x_206)) {
 lean_ctor_release(x_206, 0);
 x_247 = x_206;
} else {
 lean_dec_ref(x_206);
 x_247 = lean_box(0);
}
if (lean_is_scalar(x_247)) {
 x_248 = lean_alloc_ctor(4, 1, 0);
} else {
 x_248 = x_247;
 lean_ctor_set_tag(x_248, 4);
}
lean_ctor_set(x_248, 0, x_246);
x_249 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_249, 0, x_248);
return x_249;
}
}
}
else
{
uint8_t x_250; 
lean_dec(x_21);
x_250 = !lean_is_exclusive(x_25);
if (x_250 == 0)
{
lean_ctor_set_tag(x_25, 3);
lean_ctor_set(x_22, 0, x_25);
return x_22;
}
else
{
lean_object* x_251; lean_object* x_252; 
x_251 = lean_ctor_get(x_25, 0);
lean_inc(x_251);
lean_dec(x_25);
x_252 = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(x_252, 0, x_251);
lean_ctor_set(x_22, 0, x_252);
return x_22;
}
}
}
else
{
lean_object* x_253; 
lean_dec(x_22);
lean_inc(x_21);
x_253 = lp_REPL_REPL_instFromJsonPickleEnvironment_fromJson(x_21);
if (lean_obj_tag(x_253) == 0)
{
lean_object* x_254; lean_object* x_255; 
if (lean_is_exclusive(x_253)) {
 lean_ctor_release(x_253, 0);
 x_254 = x_253;
} else {
 lean_dec_ref(x_253);
 x_254 = lean_box(0);
}
lean_inc(x_21);
x_255 = lp_REPL_REPL_instFromJsonUnpickleEnvironment_fromJson(x_21);
if (lean_obj_tag(x_255) == 0)
{
lean_object* x_256; lean_object* x_257; 
lean_dec(x_254);
if (lean_is_exclusive(x_255)) {
 lean_ctor_release(x_255, 0);
 x_256 = x_255;
} else {
 lean_dec_ref(x_255);
 x_256 = lean_box(0);
}
lean_inc(x_21);
x_257 = lp_REPL_REPL_instFromJsonPickleProofState_fromJson(x_21);
if (lean_obj_tag(x_257) == 0)
{
lean_object* x_258; lean_object* x_259; 
lean_dec(x_256);
if (lean_is_exclusive(x_257)) {
 lean_ctor_release(x_257, 0);
 x_258 = x_257;
} else {
 lean_dec_ref(x_257);
 x_258 = lean_box(0);
}
lean_inc(x_21);
x_259 = lp_REPL_REPL_instFromJsonUnpickleProofState_fromJson(x_21);
if (lean_obj_tag(x_259) == 0)
{
lean_object* x_260; lean_object* x_261; 
lean_dec(x_258);
if (lean_is_exclusive(x_259)) {
 lean_ctor_release(x_259, 0);
 x_260 = x_259;
} else {
 lean_dec_ref(x_259);
 x_260 = lean_box(0);
}
lean_inc(x_21);
x_261 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_21);
if (lean_obj_tag(x_261) == 0)
{
lean_object* x_262; lean_object* x_263; 
lean_dec(x_260);
if (lean_is_exclusive(x_261)) {
 lean_ctor_release(x_261, 0);
 x_262 = x_261;
} else {
 lean_dec_ref(x_261);
 x_262 = lean_box(0);
}
lean_inc(x_21);
x_263 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_21);
if (lean_obj_tag(x_263) == 0)
{
lean_object* x_264; lean_object* x_265; 
lean_dec(x_262);
if (lean_is_exclusive(x_263)) {
 lean_ctor_release(x_263, 0);
 x_264 = x_263;
} else {
 lean_dec_ref(x_263);
 x_264 = lean_box(0);
}
x_265 = lp_REPL_REPL_instFromJsonFile_fromJson(x_21);
if (lean_obj_tag(x_265) == 0)
{
lean_object* x_266; lean_object* x_267; lean_object* x_268; lean_object* x_269; lean_object* x_270; lean_object* x_271; lean_object* x_272; lean_object* x_273; lean_object* x_274; 
x_266 = lean_ctor_get(x_265, 0);
lean_inc(x_266);
if (lean_is_exclusive(x_265)) {
 lean_ctor_release(x_265, 0);
 x_267 = x_265;
} else {
 lean_dec_ref(x_265);
 x_267 = lean_box(0);
}
x_268 = lp_REPL_parse___closed__1;
x_269 = lean_string_append(x_268, x_266);
lean_dec(x_266);
x_270 = lp_REPL_REPL_instToJsonError_toJson(x_269);
x_271 = lean_unsigned_to_nat(80u);
x_272 = l_Lean_Json_pretty(x_270, x_271);
if (lean_is_scalar(x_267)) {
 x_273 = lean_alloc_ctor(18, 1, 0);
} else {
 x_273 = x_267;
 lean_ctor_set_tag(x_273, 18);
}
lean_ctor_set(x_273, 0, x_272);
if (lean_is_scalar(x_264)) {
 x_274 = lean_alloc_ctor(1, 1, 0);
} else {
 x_274 = x_264;
 lean_ctor_set_tag(x_274, 1);
}
lean_ctor_set(x_274, 0, x_273);
return x_274;
}
else
{
lean_object* x_275; lean_object* x_276; lean_object* x_277; lean_object* x_278; 
x_275 = lean_ctor_get(x_265, 0);
lean_inc(x_275);
if (lean_is_exclusive(x_265)) {
 lean_ctor_release(x_265, 0);
 x_276 = x_265;
} else {
 lean_dec_ref(x_265);
 x_276 = lean_box(0);
}
if (lean_is_scalar(x_276)) {
 x_277 = lean_alloc_ctor(1, 1, 0);
} else {
 x_277 = x_276;
}
lean_ctor_set(x_277, 0, x_275);
if (lean_is_scalar(x_264)) {
 x_278 = lean_alloc_ctor(0, 1, 0);
} else {
 x_278 = x_264;
}
lean_ctor_set(x_278, 0, x_277);
return x_278;
}
}
else
{
lean_object* x_279; lean_object* x_280; lean_object* x_281; lean_object* x_282; 
lean_dec(x_21);
x_279 = lean_ctor_get(x_263, 0);
lean_inc(x_279);
if (lean_is_exclusive(x_263)) {
 lean_ctor_release(x_263, 0);
 x_280 = x_263;
} else {
 lean_dec_ref(x_263);
 x_280 = lean_box(0);
}
if (lean_is_scalar(x_280)) {
 x_281 = lean_alloc_ctor(7, 1, 0);
} else {
 x_281 = x_280;
 lean_ctor_set_tag(x_281, 7);
}
lean_ctor_set(x_281, 0, x_279);
if (lean_is_scalar(x_262)) {
 x_282 = lean_alloc_ctor(0, 1, 0);
} else {
 x_282 = x_262;
}
lean_ctor_set(x_282, 0, x_281);
return x_282;
}
}
else
{
lean_object* x_283; lean_object* x_284; lean_object* x_285; lean_object* x_286; 
lean_dec(x_21);
x_283 = lean_ctor_get(x_261, 0);
lean_inc(x_283);
if (lean_is_exclusive(x_261)) {
 lean_ctor_release(x_261, 0);
 x_284 = x_261;
} else {
 lean_dec_ref(x_261);
 x_284 = lean_box(0);
}
if (lean_is_scalar(x_284)) {
 x_285 = lean_alloc_ctor(0, 1, 0);
} else {
 x_285 = x_284;
 lean_ctor_set_tag(x_285, 0);
}
lean_ctor_set(x_285, 0, x_283);
if (lean_is_scalar(x_260)) {
 x_286 = lean_alloc_ctor(0, 1, 0);
} else {
 x_286 = x_260;
}
lean_ctor_set(x_286, 0, x_285);
return x_286;
}
}
else
{
lean_object* x_287; lean_object* x_288; lean_object* x_289; lean_object* x_290; 
lean_dec(x_21);
x_287 = lean_ctor_get(x_259, 0);
lean_inc(x_287);
if (lean_is_exclusive(x_259)) {
 lean_ctor_release(x_259, 0);
 x_288 = x_259;
} else {
 lean_dec_ref(x_259);
 x_288 = lean_box(0);
}
if (lean_is_scalar(x_288)) {
 x_289 = lean_alloc_ctor(6, 1, 0);
} else {
 x_289 = x_288;
 lean_ctor_set_tag(x_289, 6);
}
lean_ctor_set(x_289, 0, x_287);
if (lean_is_scalar(x_258)) {
 x_290 = lean_alloc_ctor(0, 1, 0);
} else {
 x_290 = x_258;
}
lean_ctor_set(x_290, 0, x_289);
return x_290;
}
}
else
{
lean_object* x_291; lean_object* x_292; lean_object* x_293; lean_object* x_294; 
lean_dec(x_21);
x_291 = lean_ctor_get(x_257, 0);
lean_inc(x_291);
if (lean_is_exclusive(x_257)) {
 lean_ctor_release(x_257, 0);
 x_292 = x_257;
} else {
 lean_dec_ref(x_257);
 x_292 = lean_box(0);
}
if (lean_is_scalar(x_292)) {
 x_293 = lean_alloc_ctor(5, 1, 0);
} else {
 x_293 = x_292;
 lean_ctor_set_tag(x_293, 5);
}
lean_ctor_set(x_293, 0, x_291);
if (lean_is_scalar(x_256)) {
 x_294 = lean_alloc_ctor(0, 1, 0);
} else {
 x_294 = x_256;
}
lean_ctor_set(x_294, 0, x_293);
return x_294;
}
}
else
{
lean_object* x_295; lean_object* x_296; lean_object* x_297; lean_object* x_298; 
lean_dec(x_21);
x_295 = lean_ctor_get(x_255, 0);
lean_inc(x_295);
if (lean_is_exclusive(x_255)) {
 lean_ctor_release(x_255, 0);
 x_296 = x_255;
} else {
 lean_dec_ref(x_255);
 x_296 = lean_box(0);
}
if (lean_is_scalar(x_296)) {
 x_297 = lean_alloc_ctor(4, 1, 0);
} else {
 x_297 = x_296;
 lean_ctor_set_tag(x_297, 4);
}
lean_ctor_set(x_297, 0, x_295);
if (lean_is_scalar(x_254)) {
 x_298 = lean_alloc_ctor(0, 1, 0);
} else {
 x_298 = x_254;
}
lean_ctor_set(x_298, 0, x_297);
return x_298;
}
}
else
{
lean_object* x_299; lean_object* x_300; lean_object* x_301; lean_object* x_302; 
lean_dec(x_21);
x_299 = lean_ctor_get(x_253, 0);
lean_inc(x_299);
if (lean_is_exclusive(x_253)) {
 lean_ctor_release(x_253, 0);
 x_300 = x_253;
} else {
 lean_dec_ref(x_253);
 x_300 = lean_box(0);
}
if (lean_is_scalar(x_300)) {
 x_301 = lean_alloc_ctor(3, 1, 0);
} else {
 x_301 = x_300;
 lean_ctor_set_tag(x_301, 3);
}
lean_ctor_set(x_301, 0, x_299);
x_302 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_302, 0, x_301);
return x_302;
}
}
}
else
{
uint8_t x_303; 
lean_dec(x_21);
x_303 = !lean_is_exclusive(x_22);
if (x_303 == 0)
{
lean_ctor_set_tag(x_22, 2);
lean_ctor_set_tag(x_3, 0);
lean_ctor_set(x_3, 0, x_22);
return x_3;
}
else
{
lean_object* x_304; lean_object* x_305; 
x_304 = lean_ctor_get(x_22, 0);
lean_inc(x_304);
lean_dec(x_22);
x_305 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_305, 0, x_304);
lean_ctor_set_tag(x_3, 0);
lean_ctor_set(x_3, 0, x_305);
return x_3;
}
}
}
else
{
lean_object* x_306; lean_object* x_307; 
x_306 = lean_ctor_get(x_3, 0);
lean_inc(x_306);
lean_dec(x_3);
lean_inc(x_306);
x_307 = lp_REPL_REPL_instFromJsonProofStep_fromJson(x_306);
if (lean_obj_tag(x_307) == 0)
{
lean_object* x_308; lean_object* x_309; 
if (lean_is_exclusive(x_307)) {
 lean_ctor_release(x_307, 0);
 x_308 = x_307;
} else {
 lean_dec_ref(x_307);
 x_308 = lean_box(0);
}
lean_inc(x_306);
x_309 = lp_REPL_REPL_instFromJsonPickleEnvironment_fromJson(x_306);
if (lean_obj_tag(x_309) == 0)
{
lean_object* x_310; lean_object* x_311; 
lean_dec(x_308);
if (lean_is_exclusive(x_309)) {
 lean_ctor_release(x_309, 0);
 x_310 = x_309;
} else {
 lean_dec_ref(x_309);
 x_310 = lean_box(0);
}
lean_inc(x_306);
x_311 = lp_REPL_REPL_instFromJsonUnpickleEnvironment_fromJson(x_306);
if (lean_obj_tag(x_311) == 0)
{
lean_object* x_312; lean_object* x_313; 
lean_dec(x_310);
if (lean_is_exclusive(x_311)) {
 lean_ctor_release(x_311, 0);
 x_312 = x_311;
} else {
 lean_dec_ref(x_311);
 x_312 = lean_box(0);
}
lean_inc(x_306);
x_313 = lp_REPL_REPL_instFromJsonPickleProofState_fromJson(x_306);
if (lean_obj_tag(x_313) == 0)
{
lean_object* x_314; lean_object* x_315; 
lean_dec(x_312);
if (lean_is_exclusive(x_313)) {
 lean_ctor_release(x_313, 0);
 x_314 = x_313;
} else {
 lean_dec_ref(x_313);
 x_314 = lean_box(0);
}
lean_inc(x_306);
x_315 = lp_REPL_REPL_instFromJsonUnpickleProofState_fromJson(x_306);
if (lean_obj_tag(x_315) == 0)
{
lean_object* x_316; lean_object* x_317; 
lean_dec(x_314);
if (lean_is_exclusive(x_315)) {
 lean_ctor_release(x_315, 0);
 x_316 = x_315;
} else {
 lean_dec_ref(x_315);
 x_316 = lean_box(0);
}
lean_inc(x_306);
x_317 = lp_REPL_REPL_instFromJsonCommand_fromJson(x_306);
if (lean_obj_tag(x_317) == 0)
{
lean_object* x_318; lean_object* x_319; 
lean_dec(x_316);
if (lean_is_exclusive(x_317)) {
 lean_ctor_release(x_317, 0);
 x_318 = x_317;
} else {
 lean_dec_ref(x_317);
 x_318 = lean_box(0);
}
lean_inc(x_306);
x_319 = lp_REPL_REPL_instFromJsonBatchCommand_fromJson(x_306);
if (lean_obj_tag(x_319) == 0)
{
lean_object* x_320; lean_object* x_321; 
lean_dec(x_318);
if (lean_is_exclusive(x_319)) {
 lean_ctor_release(x_319, 0);
 x_320 = x_319;
} else {
 lean_dec_ref(x_319);
 x_320 = lean_box(0);
}
x_321 = lp_REPL_REPL_instFromJsonFile_fromJson(x_306);
if (lean_obj_tag(x_321) == 0)
{
lean_object* x_322; lean_object* x_323; lean_object* x_324; lean_object* x_325; lean_object* x_326; lean_object* x_327; lean_object* x_328; lean_object* x_329; lean_object* x_330; 
x_322 = lean_ctor_get(x_321, 0);
lean_inc(x_322);
if (lean_is_exclusive(x_321)) {
 lean_ctor_release(x_321, 0);
 x_323 = x_321;
} else {
 lean_dec_ref(x_321);
 x_323 = lean_box(0);
}
x_324 = lp_REPL_parse___closed__1;
x_325 = lean_string_append(x_324, x_322);
lean_dec(x_322);
x_326 = lp_REPL_REPL_instToJsonError_toJson(x_325);
x_327 = lean_unsigned_to_nat(80u);
x_328 = l_Lean_Json_pretty(x_326, x_327);
if (lean_is_scalar(x_323)) {
 x_329 = lean_alloc_ctor(18, 1, 0);
} else {
 x_329 = x_323;
 lean_ctor_set_tag(x_329, 18);
}
lean_ctor_set(x_329, 0, x_328);
if (lean_is_scalar(x_320)) {
 x_330 = lean_alloc_ctor(1, 1, 0);
} else {
 x_330 = x_320;
 lean_ctor_set_tag(x_330, 1);
}
lean_ctor_set(x_330, 0, x_329);
return x_330;
}
else
{
lean_object* x_331; lean_object* x_332; lean_object* x_333; lean_object* x_334; 
x_331 = lean_ctor_get(x_321, 0);
lean_inc(x_331);
if (lean_is_exclusive(x_321)) {
 lean_ctor_release(x_321, 0);
 x_332 = x_321;
} else {
 lean_dec_ref(x_321);
 x_332 = lean_box(0);
}
if (lean_is_scalar(x_332)) {
 x_333 = lean_alloc_ctor(1, 1, 0);
} else {
 x_333 = x_332;
}
lean_ctor_set(x_333, 0, x_331);
if (lean_is_scalar(x_320)) {
 x_334 = lean_alloc_ctor(0, 1, 0);
} else {
 x_334 = x_320;
}
lean_ctor_set(x_334, 0, x_333);
return x_334;
}
}
else
{
lean_object* x_335; lean_object* x_336; lean_object* x_337; lean_object* x_338; 
lean_dec(x_306);
x_335 = lean_ctor_get(x_319, 0);
lean_inc(x_335);
if (lean_is_exclusive(x_319)) {
 lean_ctor_release(x_319, 0);
 x_336 = x_319;
} else {
 lean_dec_ref(x_319);
 x_336 = lean_box(0);
}
if (lean_is_scalar(x_336)) {
 x_337 = lean_alloc_ctor(7, 1, 0);
} else {
 x_337 = x_336;
 lean_ctor_set_tag(x_337, 7);
}
lean_ctor_set(x_337, 0, x_335);
if (lean_is_scalar(x_318)) {
 x_338 = lean_alloc_ctor(0, 1, 0);
} else {
 x_338 = x_318;
}
lean_ctor_set(x_338, 0, x_337);
return x_338;
}
}
else
{
lean_object* x_339; lean_object* x_340; lean_object* x_341; lean_object* x_342; 
lean_dec(x_306);
x_339 = lean_ctor_get(x_317, 0);
lean_inc(x_339);
if (lean_is_exclusive(x_317)) {
 lean_ctor_release(x_317, 0);
 x_340 = x_317;
} else {
 lean_dec_ref(x_317);
 x_340 = lean_box(0);
}
if (lean_is_scalar(x_340)) {
 x_341 = lean_alloc_ctor(0, 1, 0);
} else {
 x_341 = x_340;
 lean_ctor_set_tag(x_341, 0);
}
lean_ctor_set(x_341, 0, x_339);
if (lean_is_scalar(x_316)) {
 x_342 = lean_alloc_ctor(0, 1, 0);
} else {
 x_342 = x_316;
}
lean_ctor_set(x_342, 0, x_341);
return x_342;
}
}
else
{
lean_object* x_343; lean_object* x_344; lean_object* x_345; lean_object* x_346; 
lean_dec(x_306);
x_343 = lean_ctor_get(x_315, 0);
lean_inc(x_343);
if (lean_is_exclusive(x_315)) {
 lean_ctor_release(x_315, 0);
 x_344 = x_315;
} else {
 lean_dec_ref(x_315);
 x_344 = lean_box(0);
}
if (lean_is_scalar(x_344)) {
 x_345 = lean_alloc_ctor(6, 1, 0);
} else {
 x_345 = x_344;
 lean_ctor_set_tag(x_345, 6);
}
lean_ctor_set(x_345, 0, x_343);
if (lean_is_scalar(x_314)) {
 x_346 = lean_alloc_ctor(0, 1, 0);
} else {
 x_346 = x_314;
}
lean_ctor_set(x_346, 0, x_345);
return x_346;
}
}
else
{
lean_object* x_347; lean_object* x_348; lean_object* x_349; lean_object* x_350; 
lean_dec(x_306);
x_347 = lean_ctor_get(x_313, 0);
lean_inc(x_347);
if (lean_is_exclusive(x_313)) {
 lean_ctor_release(x_313, 0);
 x_348 = x_313;
} else {
 lean_dec_ref(x_313);
 x_348 = lean_box(0);
}
if (lean_is_scalar(x_348)) {
 x_349 = lean_alloc_ctor(5, 1, 0);
} else {
 x_349 = x_348;
 lean_ctor_set_tag(x_349, 5);
}
lean_ctor_set(x_349, 0, x_347);
if (lean_is_scalar(x_312)) {
 x_350 = lean_alloc_ctor(0, 1, 0);
} else {
 x_350 = x_312;
}
lean_ctor_set(x_350, 0, x_349);
return x_350;
}
}
else
{
lean_object* x_351; lean_object* x_352; lean_object* x_353; lean_object* x_354; 
lean_dec(x_306);
x_351 = lean_ctor_get(x_311, 0);
lean_inc(x_351);
if (lean_is_exclusive(x_311)) {
 lean_ctor_release(x_311, 0);
 x_352 = x_311;
} else {
 lean_dec_ref(x_311);
 x_352 = lean_box(0);
}
if (lean_is_scalar(x_352)) {
 x_353 = lean_alloc_ctor(4, 1, 0);
} else {
 x_353 = x_352;
 lean_ctor_set_tag(x_353, 4);
}
lean_ctor_set(x_353, 0, x_351);
if (lean_is_scalar(x_310)) {
 x_354 = lean_alloc_ctor(0, 1, 0);
} else {
 x_354 = x_310;
}
lean_ctor_set(x_354, 0, x_353);
return x_354;
}
}
else
{
lean_object* x_355; lean_object* x_356; lean_object* x_357; lean_object* x_358; 
lean_dec(x_306);
x_355 = lean_ctor_get(x_309, 0);
lean_inc(x_355);
if (lean_is_exclusive(x_309)) {
 lean_ctor_release(x_309, 0);
 x_356 = x_309;
} else {
 lean_dec_ref(x_309);
 x_356 = lean_box(0);
}
if (lean_is_scalar(x_356)) {
 x_357 = lean_alloc_ctor(3, 1, 0);
} else {
 x_357 = x_356;
 lean_ctor_set_tag(x_357, 3);
}
lean_ctor_set(x_357, 0, x_355);
if (lean_is_scalar(x_308)) {
 x_358 = lean_alloc_ctor(0, 1, 0);
} else {
 x_358 = x_308;
}
lean_ctor_set(x_358, 0, x_357);
return x_358;
}
}
else
{
lean_object* x_359; lean_object* x_360; lean_object* x_361; lean_object* x_362; 
lean_dec(x_306);
x_359 = lean_ctor_get(x_307, 0);
lean_inc(x_359);
if (lean_is_exclusive(x_307)) {
 lean_ctor_release(x_307, 0);
 x_360 = x_307;
} else {
 lean_dec_ref(x_307);
 x_360 = lean_box(0);
}
if (lean_is_scalar(x_360)) {
 x_361 = lean_alloc_ctor(2, 1, 0);
} else {
 x_361 = x_360;
 lean_ctor_set_tag(x_361, 2);
}
lean_ctor_set(x_361, 0, x_359);
x_362 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_362, 0, x_361);
return x_362;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_parse___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_parse(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_printFlush___redArg(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; 
x_4 = lean_get_stdout();
x_5 = lean_ctor_get(x_4, 0);
lean_inc_ref(x_5);
x_6 = lean_ctor_get(x_4, 4);
lean_inc_ref(x_6);
lean_dec_ref(x_4);
x_7 = lean_apply_1(x_1, x_2);
x_8 = lean_apply_2(x_6, x_7, lean_box(0));
if (lean_obj_tag(x_8) == 0)
{
lean_object* x_9; 
lean_dec_ref(x_8);
x_9 = lean_apply_1(x_5, lean_box(0));
return x_9;
}
else
{
lean_dec_ref(x_5);
return x_8;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_printFlush(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_printFlush___redArg(x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_printFlush___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_printFlush(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_printFlush___redArg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_printFlush___redArg(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4_spec__4(size_t x_1, size_t x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; 
x_4 = lean_usize_dec_lt(x_2, x_1);
if (x_4 == 0)
{
return x_3;
}
else
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; size_t x_9; size_t x_10; lean_object* x_11; 
x_5 = lean_array_uget(x_3, x_2);
x_6 = lean_unsigned_to_nat(0u);
x_7 = lean_array_uset(x_3, x_2, x_6);
x_8 = lp_REPL_REPL_instToJsonTactic_toJson(x_5);
x_9 = 1;
x_10 = lean_usize_add(x_2, x_9);
x_11 = lean_array_uset(x_7, x_2, x_8);
x_2 = x_10;
x_3 = x_11;
goto _start;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4(lean_object* x_1) {
_start:
{
size_t x_2; size_t x_3; lean_object* x_4; lean_object* x_5; 
x_2 = lean_array_size(x_1);
x_3 = 0;
x_4 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4_spec__4(x_2, x_3, x_1);
x_5 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_5, 0, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4(lean_object* x_1) {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lean_array_mk(x_1);
x_3 = lp_REPL_Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4(x_2);
return x_3;
}
}
static lean_object* _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("messages", 8, 8);
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
lean_object* x_3; 
lean_dec_ref(x_1);
x_3 = lean_box(0);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lp_REPL_List_toJson___at___00REPL_instToJsonProofStepResponse_toJson_spec__1(x_2);
x_5 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_5, 0, x_1);
lean_ctor_set(x_5, 1, x_4);
x_6 = lean_box(0);
x_7 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_7, 0, x_5);
lean_ctor_set(x_7, 1, x_6);
return x_7;
}
}
}
static lean_object* _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("sorries", 7, 7);
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
lean_object* x_3; 
lean_dec_ref(x_1);
x_3 = lean_box(0);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lp_REPL_List_toJson___at___00REPL_instToJsonProofStepResponse_toJson_spec__4(x_2);
x_5 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_5, 0, x_1);
lean_ctor_set(x_5, 1, x_4);
x_6 = lean_box(0);
x_7 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_7, 0, x_5);
lean_ctor_set(x_7, 1, x_6);
return x_7;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
lean_object* x_3; 
lean_dec_ref(x_1);
x_3 = lean_box(0);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lp_REPL_List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4(x_2);
x_5 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_5, 0, x_1);
lean_ctor_set(x_5, 1, x_4);
x_6 = lean_box(0);
x_7 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_7, 0, x_5);
lean_ctor_set(x_7, 1, x_6);
return x_7;
}
}
}
static lean_object* _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("infotree", 8, 8);
return x_1;
}
}
static lean_object* _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("env", 3, 3);
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11(size_t x_1, size_t x_2, lean_object* x_3) {
_start:
{
uint8_t x_4; 
x_4 = lean_usize_dec_lt(x_2, x_1);
if (x_4 == 0)
{
return x_3;
}
else
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; 
x_5 = lean_array_uget(x_3, x_2);
x_6 = lean_unsigned_to_nat(0u);
x_7 = lean_array_uset(x_3, x_2, x_6);
if (lean_obj_tag(x_5) == 0)
{
lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_35; 
x_29 = lean_ctor_get(x_5, 0);
lean_inc(x_29);
lean_dec_ref(x_5);
x_30 = lean_ctor_get(x_29, 0);
lean_inc(x_30);
x_31 = lean_ctor_get(x_29, 1);
lean_inc(x_31);
x_32 = lean_ctor_get(x_29, 2);
lean_inc(x_32);
x_33 = lean_ctor_get(x_29, 3);
lean_inc(x_33);
x_34 = lean_ctor_get(x_29, 4);
lean_inc(x_34);
lean_dec(x_29);
if (lean_obj_tag(x_30) == 0)
{
lean_object* x_49; 
x_49 = lean_box(0);
x_35 = x_49;
goto block_48;
}
else
{
uint8_t x_50; 
x_50 = !lean_is_exclusive(x_30);
if (x_50 == 0)
{
lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; 
x_51 = lean_ctor_get(x_30, 0);
x_52 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_53 = l_Lean_JsonNumber_fromNat(x_51);
lean_ctor_set_tag(x_30, 2);
lean_ctor_set(x_30, 0, x_53);
x_54 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_54, 0, x_52);
lean_ctor_set(x_54, 1, x_30);
x_55 = lean_box(0);
x_56 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_56, 0, x_54);
lean_ctor_set(x_56, 1, x_55);
x_35 = x_56;
goto block_48;
}
else
{
lean_object* x_57; lean_object* x_58; lean_object* x_59; lean_object* x_60; lean_object* x_61; lean_object* x_62; lean_object* x_63; 
x_57 = lean_ctor_get(x_30, 0);
lean_inc(x_57);
lean_dec(x_30);
x_58 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_59 = l_Lean_JsonNumber_fromNat(x_57);
x_60 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_60, 0, x_59);
x_61 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_61, 0, x_58);
lean_ctor_set(x_61, 1, x_60);
x_62 = lean_box(0);
x_63 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_63, 0, x_61);
lean_ctor_set(x_63, 1, x_62);
x_35 = x_63;
goto block_48;
}
}
block_48:
{
lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; 
x_36 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_37 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_36, x_31);
x_38 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_39 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_38, x_32);
x_40 = lp_REPL_REPL_runCommandGCAux___closed__7;
x_41 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(x_40, x_33);
if (lean_obj_tag(x_34) == 0)
{
lean_object* x_42; 
x_42 = lean_box(0);
x_14 = x_39;
x_15 = x_35;
x_16 = x_37;
x_17 = x_41;
x_18 = x_42;
goto block_28;
}
else
{
lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; lean_object* x_47; 
x_43 = lean_ctor_get(x_34, 0);
lean_inc(x_43);
lean_dec_ref(x_34);
x_44 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2;
x_45 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_45, 0, x_44);
lean_ctor_set(x_45, 1, x_43);
x_46 = lean_box(0);
x_47 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_47, 0, x_45);
lean_ctor_set(x_47, 1, x_46);
x_14 = x_39;
x_15 = x_35;
x_16 = x_37;
x_17 = x_41;
x_18 = x_47;
goto block_28;
}
}
}
else
{
lean_object* x_64; lean_object* x_65; 
x_64 = lean_ctor_get(x_5, 0);
lean_inc(x_64);
lean_dec_ref(x_5);
x_65 = lp_REPL_REPL_instToJsonError_toJson(x_64);
x_8 = x_65;
goto block_13;
}
block_13:
{
size_t x_9; size_t x_10; lean_object* x_11; 
x_9 = 1;
x_10 = lean_usize_add(x_2, x_9);
x_11 = lean_array_uset(x_7, x_2, x_8);
x_2 = x_10;
x_3 = x_11;
goto _start;
}
block_28:
{
lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; lean_object* x_27; 
x_19 = lean_box(0);
x_20 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_20, 0, x_18);
lean_ctor_set(x_20, 1, x_19);
x_21 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_21, 0, x_17);
lean_ctor_set(x_21, 1, x_20);
x_22 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_22, 0, x_14);
lean_ctor_set(x_22, 1, x_21);
x_23 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_23, 0, x_16);
lean_ctor_set(x_23, 1, x_22);
x_24 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_24, 0, x_15);
lean_ctor_set(x_24, 1, x_23);
x_25 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_26 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_24, x_25);
x_27 = l_Lean_Json_mkObj(x_26);
x_8 = x_27;
goto block_13;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_Array_toJson___at___00repl_loop_spec__11(lean_object* x_1) {
_start:
{
size_t x_2; size_t x_3; lean_object* x_4; lean_object* x_5; 
x_2 = lean_array_size(x_1);
x_3 = 0;
x_4 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11(x_2, x_3, x_1);
x_5 = lean_alloc_ctor(4, 1, 0);
lean_ctor_set(x_5, 0, x_4);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_IO_println___at___00repl_loop_spec__0(lean_object* x_1) {
_start:
{
lean_object* x_3; lean_object* x_4; uint32_t x_5; lean_object* x_6; lean_object* x_7; 
x_3 = lean_unsigned_to_nat(80u);
x_4 = l_Lean_Json_pretty(x_1, x_3);
x_5 = 10;
x_6 = lean_string_push(x_4, x_5);
x_7 = l_IO_print___at___00IO_println___at___00__private_Lean_Shell_0__Lean_ShellOptions_process_spec__3_spec__3(x_6);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(lean_object* x_1, lean_object* x_2) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
lean_object* x_3; 
lean_dec_ref(x_1);
x_3 = lean_box(0);
return x_3;
}
else
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; lean_object* x_7; 
x_4 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_2);
x_5 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_5, 0, x_1);
lean_ctor_set(x_5, 1, x_4);
x_6 = lean_box(0);
x_7 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_7, 0, x_5);
lean_ctor_set(x_7, 1, x_6);
return x_7;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_printFlush___at___00repl_loop_spec__1(lean_object* x_1) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_3 = lean_get_stdout();
x_4 = lean_ctor_get(x_3, 0);
lean_inc_ref(x_4);
x_5 = lean_ctor_get(x_3, 4);
lean_inc_ref(x_5);
lean_dec_ref(x_3);
x_6 = lean_apply_2(x_5, x_1, lean_box(0));
if (lean_obj_tag(x_6) == 0)
{
lean_object* x_7; 
lean_dec_ref(x_6);
x_7 = lean_apply_1(x_4, lean_box(0));
return x_7;
}
else
{
lean_dec_ref(x_4);
return x_6;
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___at___00repl_loop_spec__9(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_1);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; uint8_t x_9; 
x_5 = lean_ctor_get(x_2, 0);
x_6 = lean_ctor_get(x_1, 0);
x_7 = lean_ctor_get(x_1, 1);
x_8 = lean_array_get_size(x_5);
x_9 = lean_nat_dec_lt(x_6, x_8);
if (x_9 == 0)
{
lean_object* x_10; lean_object* x_11; 
lean_dec_ref(x_7);
lean_dec(x_6);
x_10 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_10);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_1);
return x_11;
}
else
{
lean_object* x_12; lean_object* x_13; 
x_12 = lean_array_fget_borrowed(x_5, x_6);
lean_inc(x_12);
x_13 = lp_REPL_REPL_CommandSnapshot_pickle(x_12, x_7);
if (lean_obj_tag(x_13) == 0)
{
uint8_t x_14; 
x_14 = !lean_is_exclusive(x_13);
if (x_14 == 0)
{
lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_18; lean_object* x_19; lean_object* x_20; 
x_15 = lean_ctor_get(x_13, 0);
lean_dec(x_15);
x_16 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_16, 0, x_6);
x_17 = lean_box(0);
x_18 = lean_box(0);
x_19 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_19, 0, x_16);
lean_ctor_set(x_19, 1, x_17);
lean_ctor_set(x_19, 2, x_17);
lean_ctor_set(x_19, 3, x_17);
lean_ctor_set(x_19, 4, x_18);
x_20 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_20, 0, x_19);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_20);
lean_ctor_set(x_13, 0, x_1);
return x_13;
}
else
{
lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; 
lean_dec(x_13);
x_21 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_21, 0, x_6);
x_22 = lean_box(0);
x_23 = lean_box(0);
x_24 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_24, 0, x_21);
lean_ctor_set(x_24, 1, x_22);
lean_ctor_set(x_24, 2, x_22);
lean_ctor_set(x_24, 3, x_22);
lean_ctor_set(x_24, 4, x_23);
x_25 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_25, 0, x_24);
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_25);
x_26 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_26, 0, x_1);
return x_26;
}
}
else
{
uint8_t x_27; 
lean_free_object(x_1);
lean_dec(x_6);
lean_dec_ref(x_2);
x_27 = !lean_is_exclusive(x_13);
if (x_27 == 0)
{
return x_13;
}
else
{
lean_object* x_28; lean_object* x_29; 
x_28 = lean_ctor_get(x_13, 0);
lean_inc(x_28);
lean_dec(x_13);
x_29 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_29, 0, x_28);
return x_29;
}
}
}
}
else
{
lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; uint8_t x_34; 
x_30 = lean_ctor_get(x_2, 0);
x_31 = lean_ctor_get(x_1, 0);
x_32 = lean_ctor_get(x_1, 1);
lean_inc(x_32);
lean_inc(x_31);
lean_dec(x_1);
x_33 = lean_array_get_size(x_30);
x_34 = lean_nat_dec_lt(x_31, x_33);
if (x_34 == 0)
{
lean_object* x_35; lean_object* x_36; lean_object* x_37; 
lean_dec_ref(x_32);
lean_dec(x_31);
x_35 = lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1;
x_36 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_36, 0, x_35);
lean_ctor_set(x_36, 1, x_2);
x_37 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_37, 0, x_36);
return x_37;
}
else
{
lean_object* x_38; lean_object* x_39; 
x_38 = lean_array_fget_borrowed(x_30, x_31);
lean_inc(x_38);
x_39 = lp_REPL_REPL_CommandSnapshot_pickle(x_38, x_32);
if (lean_obj_tag(x_39) == 0)
{
lean_object* x_40; lean_object* x_41; lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; lean_object* x_47; 
if (lean_is_exclusive(x_39)) {
 lean_ctor_release(x_39, 0);
 x_40 = x_39;
} else {
 lean_dec_ref(x_39);
 x_40 = lean_box(0);
}
x_41 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_41, 0, x_31);
x_42 = lean_box(0);
x_43 = lean_box(0);
x_44 = lean_alloc_ctor(0, 5, 0);
lean_ctor_set(x_44, 0, x_41);
lean_ctor_set(x_44, 1, x_42);
lean_ctor_set(x_44, 2, x_42);
lean_ctor_set(x_44, 3, x_42);
lean_ctor_set(x_44, 4, x_43);
x_45 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_45, 0, x_44);
x_46 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_46, 0, x_45);
lean_ctor_set(x_46, 1, x_2);
if (lean_is_scalar(x_40)) {
 x_47 = lean_alloc_ctor(0, 1, 0);
} else {
 x_47 = x_40;
}
lean_ctor_set(x_47, 0, x_46);
return x_47;
}
else
{
lean_object* x_48; lean_object* x_49; lean_object* x_50; 
lean_dec(x_31);
lean_dec_ref(x_2);
x_48 = lean_ctor_get(x_39, 0);
lean_inc(x_48);
if (lean_is_exclusive(x_39)) {
 lean_ctor_release(x_39, 0);
 x_49 = x_39;
} else {
 lean_dec_ref(x_39);
 x_49 = lean_box(0);
}
if (lean_is_scalar(x_49)) {
 x_50 = lean_alloc_ctor(1, 1, 0);
} else {
 x_50 = x_49;
}
lean_ctor_set(x_50, 0, x_48);
return x_50;
}
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___at___00repl_loop_spec__10(lean_object* x_1, lean_object* x_2) {
_start:
{
uint8_t x_4; 
x_4 = !lean_is_exclusive(x_1);
if (x_4 == 0)
{
lean_object* x_5; lean_object* x_6; lean_object* x_7; lean_object* x_8; uint8_t x_9; 
x_5 = lean_ctor_get(x_2, 1);
x_6 = lean_ctor_get(x_1, 0);
x_7 = lean_ctor_get(x_1, 1);
x_8 = lean_array_get_size(x_5);
x_9 = lean_nat_dec_lt(x_6, x_8);
if (x_9 == 0)
{
lean_object* x_10; lean_object* x_11; 
lean_dec_ref(x_7);
lean_dec(x_6);
x_10 = lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1;
lean_ctor_set(x_1, 1, x_2);
lean_ctor_set(x_1, 0, x_10);
x_11 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_11, 0, x_1);
return x_11;
}
else
{
lean_object* x_12; lean_object* x_13; 
lean_free_object(x_1);
x_12 = lean_array_fget(x_5, x_6);
lean_dec(x_6);
lean_inc(x_12);
x_13 = lp_REPL_REPL_ProofSnapshot_pickle(x_12, x_7);
if (lean_obj_tag(x_13) == 0)
{
lean_object* x_14; lean_object* x_15; 
lean_dec_ref(x_13);
x_14 = lean_box(0);
x_15 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_12, x_14, x_2);
if (lean_obj_tag(x_15) == 0)
{
uint8_t x_16; 
x_16 = !lean_is_exclusive(x_15);
if (x_16 == 0)
{
lean_object* x_17; uint8_t x_18; 
x_17 = lean_ctor_get(x_15, 0);
x_18 = !lean_is_exclusive(x_17);
if (x_18 == 0)
{
lean_object* x_19; lean_object* x_20; 
x_19 = lean_ctor_get(x_17, 0);
x_20 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_20, 0, x_19);
lean_ctor_set(x_17, 0, x_20);
return x_15;
}
else
{
lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; 
x_21 = lean_ctor_get(x_17, 0);
x_22 = lean_ctor_get(x_17, 1);
lean_inc(x_22);
lean_inc(x_21);
lean_dec(x_17);
x_23 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_23, 0, x_21);
x_24 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_24, 0, x_23);
lean_ctor_set(x_24, 1, x_22);
lean_ctor_set(x_15, 0, x_24);
return x_15;
}
}
else
{
lean_object* x_25; lean_object* x_26; lean_object* x_27; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; 
x_25 = lean_ctor_get(x_15, 0);
lean_inc(x_25);
lean_dec(x_15);
x_26 = lean_ctor_get(x_25, 0);
lean_inc(x_26);
x_27 = lean_ctor_get(x_25, 1);
lean_inc(x_27);
if (lean_is_exclusive(x_25)) {
 lean_ctor_release(x_25, 0);
 lean_ctor_release(x_25, 1);
 x_28 = x_25;
} else {
 lean_dec_ref(x_25);
 x_28 = lean_box(0);
}
x_29 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_29, 0, x_26);
if (lean_is_scalar(x_28)) {
 x_30 = lean_alloc_ctor(0, 2, 0);
} else {
 x_30 = x_28;
}
lean_ctor_set(x_30, 0, x_29);
lean_ctor_set(x_30, 1, x_27);
x_31 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_31, 0, x_30);
return x_31;
}
}
else
{
uint8_t x_32; 
x_32 = !lean_is_exclusive(x_15);
if (x_32 == 0)
{
return x_15;
}
else
{
lean_object* x_33; lean_object* x_34; 
x_33 = lean_ctor_get(x_15, 0);
lean_inc(x_33);
lean_dec(x_15);
x_34 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_34, 0, x_33);
return x_34;
}
}
}
else
{
uint8_t x_35; 
lean_dec(x_12);
lean_dec_ref(x_2);
x_35 = !lean_is_exclusive(x_13);
if (x_35 == 0)
{
return x_13;
}
else
{
lean_object* x_36; lean_object* x_37; 
x_36 = lean_ctor_get(x_13, 0);
lean_inc(x_36);
lean_dec(x_13);
x_37 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_37, 0, x_36);
return x_37;
}
}
}
}
else
{
lean_object* x_38; lean_object* x_39; lean_object* x_40; lean_object* x_41; uint8_t x_42; 
x_38 = lean_ctor_get(x_2, 1);
x_39 = lean_ctor_get(x_1, 0);
x_40 = lean_ctor_get(x_1, 1);
lean_inc(x_40);
lean_inc(x_39);
lean_dec(x_1);
x_41 = lean_array_get_size(x_38);
x_42 = lean_nat_dec_lt(x_39, x_41);
if (x_42 == 0)
{
lean_object* x_43; lean_object* x_44; lean_object* x_45; 
lean_dec_ref(x_40);
lean_dec(x_39);
x_43 = lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1;
x_44 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_44, 0, x_43);
lean_ctor_set(x_44, 1, x_2);
x_45 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_45, 0, x_44);
return x_45;
}
else
{
lean_object* x_46; lean_object* x_47; 
x_46 = lean_array_fget(x_38, x_39);
lean_dec(x_39);
lean_inc(x_46);
x_47 = lp_REPL_REPL_ProofSnapshot_pickle(x_46, x_40);
if (lean_obj_tag(x_47) == 0)
{
lean_object* x_48; lean_object* x_49; 
lean_dec_ref(x_47);
x_48 = lean_box(0);
x_49 = lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0(x_46, x_48, x_2);
if (lean_obj_tag(x_49) == 0)
{
lean_object* x_50; lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_55; lean_object* x_56; lean_object* x_57; 
x_50 = lean_ctor_get(x_49, 0);
lean_inc(x_50);
if (lean_is_exclusive(x_49)) {
 lean_ctor_release(x_49, 0);
 x_51 = x_49;
} else {
 lean_dec_ref(x_49);
 x_51 = lean_box(0);
}
x_52 = lean_ctor_get(x_50, 0);
lean_inc(x_52);
x_53 = lean_ctor_get(x_50, 1);
lean_inc(x_53);
if (lean_is_exclusive(x_50)) {
 lean_ctor_release(x_50, 0);
 lean_ctor_release(x_50, 1);
 x_54 = x_50;
} else {
 lean_dec_ref(x_50);
 x_54 = lean_box(0);
}
x_55 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_55, 0, x_52);
if (lean_is_scalar(x_54)) {
 x_56 = lean_alloc_ctor(0, 2, 0);
} else {
 x_56 = x_54;
}
lean_ctor_set(x_56, 0, x_55);
lean_ctor_set(x_56, 1, x_53);
if (lean_is_scalar(x_51)) {
 x_57 = lean_alloc_ctor(0, 1, 0);
} else {
 x_57 = x_51;
}
lean_ctor_set(x_57, 0, x_56);
return x_57;
}
else
{
lean_object* x_58; lean_object* x_59; lean_object* x_60; 
x_58 = lean_ctor_get(x_49, 0);
lean_inc(x_58);
if (lean_is_exclusive(x_49)) {
 lean_ctor_release(x_49, 0);
 x_59 = x_49;
} else {
 lean_dec_ref(x_49);
 x_59 = lean_box(0);
}
if (lean_is_scalar(x_59)) {
 x_60 = lean_alloc_ctor(1, 1, 0);
} else {
 x_60 = x_59;
}
lean_ctor_set(x_60, 0, x_58);
return x_60;
}
}
else
{
lean_object* x_61; lean_object* x_62; lean_object* x_63; 
lean_dec(x_46);
lean_dec_ref(x_2);
x_61 = lean_ctor_get(x_47, 0);
lean_inc(x_61);
if (lean_is_exclusive(x_47)) {
 lean_ctor_release(x_47, 0);
 x_62 = x_47;
} else {
 lean_dec_ref(x_47);
 x_62 = lean_box(0);
}
if (lean_is_scalar(x_62)) {
 x_63 = lean_alloc_ctor(1, 1, 0);
} else {
 x_63 = x_62;
}
lean_ctor_set(x_63, 0, x_61);
return x_63;
}
}
}
}
}
static lean_object* _init_lp_REPL_repl_loop___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("proofState", 10, 10);
return x_1;
}
}
static lean_object* _init_lp_REPL_repl_loop___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("goals", 5, 5);
return x_1;
}
}
static lean_object* _init_lp_REPL_repl_loop___closed__2() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("traces", 6, 6);
return x_1;
}
}
static lean_object* _init_lp_REPL_repl_loop___closed__3() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("--", 2, 2);
return x_1;
}
}
static lean_object* _init_lp_REPL_repl_loop___closed__4() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_repl_loop___closed__3;
x_2 = lean_string_utf8_byte_size(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_repl_loop___closed__5() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("#", 1, 1);
return x_1;
}
}
static lean_object* _init_lp_REPL_repl_loop___closed__6() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_repl_loop___closed__5;
x_2 = lean_string_utf8_byte_size(x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_repl_loop(lean_object* x_1) {
_start:
{
lean_object* x_3; lean_object* x_4; lean_object* x_5; lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; lean_object* x_17; lean_object* x_28; lean_object* x_29; lean_object* x_30; lean_object* x_31; lean_object* x_32; lean_object* x_33; lean_object* x_34; lean_object* x_48; lean_object* x_49; lean_object* x_50; lean_object* x_51; lean_object* x_52; lean_object* x_53; lean_object* x_54; lean_object* x_65; lean_object* x_66; lean_object* x_67; lean_object* x_68; lean_object* x_69; lean_object* x_70; lean_object* x_71; lean_object* x_85; lean_object* x_86; lean_object* x_87; lean_object* x_88; lean_object* x_89; lean_object* x_90; lean_object* x_91; lean_object* x_102; lean_object* x_103; lean_object* x_104; lean_object* x_105; lean_object* x_106; lean_object* x_107; lean_object* x_108; lean_object* x_122; lean_object* x_123; lean_object* x_124; lean_object* x_125; lean_object* x_126; lean_object* x_127; lean_object* x_128; lean_object* x_139; lean_object* x_140; lean_object* x_141; lean_object* x_142; lean_object* x_143; lean_object* x_144; lean_object* x_145; lean_object* x_159; 
x_159 = lp_REPL_getLines();
if (lean_obj_tag(x_159) == 0)
{
uint8_t x_160; 
x_160 = !lean_is_exclusive(x_159);
if (x_160 == 0)
{
lean_object* x_161; lean_object* x_697; uint8_t x_698; 
x_161 = lean_ctor_get(x_159, 0);
x_697 = lp_REPL_REPL_sorries___redArg___closed__0;
x_698 = lean_string_dec_eq(x_161, x_697);
if (x_698 == 0)
{
lean_object* x_699; lean_object* x_700; lean_object* x_701; uint8_t x_702; 
lean_free_object(x_159);
x_699 = lp_REPL_repl_loop___closed__5;
x_700 = lean_string_utf8_byte_size(x_161);
x_701 = lp_REPL_repl_loop___closed__6;
x_702 = lean_nat_dec_le(x_701, x_700);
if (x_702 == 0)
{
goto block_696;
}
else
{
lean_object* x_703; uint8_t x_704; 
x_703 = lean_unsigned_to_nat(0u);
x_704 = lean_string_memcmp(x_161, x_699, x_703, x_703, x_701);
if (x_704 == 0)
{
goto block_696;
}
else
{
lean_dec(x_161);
goto _start;
}
}
}
else
{
lean_object* x_706; 
lean_dec(x_161);
lean_dec_ref(x_1);
x_706 = lean_box(0);
lean_ctor_set(x_159, 0, x_706);
return x_159;
}
block_688:
{
lean_object* x_162; 
x_162 = lp_REPL_parse(x_161);
if (lean_obj_tag(x_162) == 0)
{
lean_object* x_163; 
x_163 = lean_ctor_get(x_162, 0);
lean_inc(x_163);
lean_dec_ref(x_162);
switch (lean_obj_tag(x_163)) {
case 0:
{
lean_object* x_164; lean_object* x_165; 
x_164 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_164);
lean_dec_ref(x_163);
x_165 = lp_REPL_REPL_runCommand(x_164, x_1);
if (lean_obj_tag(x_165) == 0)
{
lean_object* x_166; lean_object* x_167; 
x_166 = lean_ctor_get(x_165, 0);
lean_inc(x_166);
lean_dec_ref(x_165);
x_167 = lean_ctor_get(x_166, 0);
if (lean_obj_tag(x_167) == 0)
{
lean_object* x_168; lean_object* x_169; 
x_168 = lean_ctor_get(x_167, 0);
lean_inc(x_168);
x_169 = lean_ctor_get(x_168, 0);
lean_inc(x_169);
if (lean_obj_tag(x_169) == 0)
{
lean_object* x_170; lean_object* x_171; lean_object* x_172; lean_object* x_173; lean_object* x_174; lean_object* x_175; 
x_170 = lean_ctor_get(x_166, 1);
lean_inc(x_170);
lean_dec(x_166);
x_171 = lean_ctor_get(x_168, 1);
lean_inc(x_171);
x_172 = lean_ctor_get(x_168, 2);
lean_inc(x_172);
x_173 = lean_ctor_get(x_168, 3);
lean_inc(x_173);
x_174 = lean_ctor_get(x_168, 4);
lean_inc(x_174);
lean_dec(x_168);
x_175 = lean_box(0);
x_28 = lean_box(0);
x_29 = x_171;
x_30 = x_172;
x_31 = x_173;
x_32 = x_174;
x_33 = x_170;
x_34 = x_175;
goto block_47;
}
else
{
uint8_t x_176; 
x_176 = !lean_is_exclusive(x_166);
if (x_176 == 0)
{
lean_object* x_177; lean_object* x_178; lean_object* x_179; lean_object* x_180; lean_object* x_181; lean_object* x_182; uint8_t x_183; 
x_177 = lean_ctor_get(x_166, 1);
x_178 = lean_ctor_get(x_166, 0);
lean_dec(x_178);
x_179 = lean_ctor_get(x_168, 1);
lean_inc(x_179);
x_180 = lean_ctor_get(x_168, 2);
lean_inc(x_180);
x_181 = lean_ctor_get(x_168, 3);
lean_inc(x_181);
x_182 = lean_ctor_get(x_168, 4);
lean_inc(x_182);
lean_dec(x_168);
x_183 = !lean_is_exclusive(x_169);
if (x_183 == 0)
{
lean_object* x_184; lean_object* x_185; lean_object* x_186; lean_object* x_187; lean_object* x_188; 
x_184 = lean_ctor_get(x_169, 0);
x_185 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_186 = l_Lean_JsonNumber_fromNat(x_184);
lean_ctor_set_tag(x_169, 2);
lean_ctor_set(x_169, 0, x_186);
lean_ctor_set(x_166, 1, x_169);
lean_ctor_set(x_166, 0, x_185);
x_187 = lean_box(0);
x_188 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_188, 0, x_166);
lean_ctor_set(x_188, 1, x_187);
x_28 = lean_box(0);
x_29 = x_179;
x_30 = x_180;
x_31 = x_181;
x_32 = x_182;
x_33 = x_177;
x_34 = x_188;
goto block_47;
}
else
{
lean_object* x_189; lean_object* x_190; lean_object* x_191; lean_object* x_192; lean_object* x_193; lean_object* x_194; 
x_189 = lean_ctor_get(x_169, 0);
lean_inc(x_189);
lean_dec(x_169);
x_190 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_191 = l_Lean_JsonNumber_fromNat(x_189);
x_192 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_192, 0, x_191);
lean_ctor_set(x_166, 1, x_192);
lean_ctor_set(x_166, 0, x_190);
x_193 = lean_box(0);
x_194 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_194, 0, x_166);
lean_ctor_set(x_194, 1, x_193);
x_28 = lean_box(0);
x_29 = x_179;
x_30 = x_180;
x_31 = x_181;
x_32 = x_182;
x_33 = x_177;
x_34 = x_194;
goto block_47;
}
}
else
{
lean_object* x_195; lean_object* x_196; lean_object* x_197; lean_object* x_198; lean_object* x_199; lean_object* x_200; lean_object* x_201; lean_object* x_202; lean_object* x_203; lean_object* x_204; lean_object* x_205; lean_object* x_206; lean_object* x_207; 
x_195 = lean_ctor_get(x_166, 1);
lean_inc(x_195);
lean_dec(x_166);
x_196 = lean_ctor_get(x_168, 1);
lean_inc(x_196);
x_197 = lean_ctor_get(x_168, 2);
lean_inc(x_197);
x_198 = lean_ctor_get(x_168, 3);
lean_inc(x_198);
x_199 = lean_ctor_get(x_168, 4);
lean_inc(x_199);
lean_dec(x_168);
x_200 = lean_ctor_get(x_169, 0);
lean_inc(x_200);
if (lean_is_exclusive(x_169)) {
 lean_ctor_release(x_169, 0);
 x_201 = x_169;
} else {
 lean_dec_ref(x_169);
 x_201 = lean_box(0);
}
x_202 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_203 = l_Lean_JsonNumber_fromNat(x_200);
if (lean_is_scalar(x_201)) {
 x_204 = lean_alloc_ctor(2, 1, 0);
} else {
 x_204 = x_201;
 lean_ctor_set_tag(x_204, 2);
}
lean_ctor_set(x_204, 0, x_203);
x_205 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_205, 0, x_202);
lean_ctor_set(x_205, 1, x_204);
x_206 = lean_box(0);
x_207 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_207, 0, x_205);
lean_ctor_set(x_207, 1, x_206);
x_28 = lean_box(0);
x_29 = x_196;
x_30 = x_197;
x_31 = x_198;
x_32 = x_199;
x_33 = x_195;
x_34 = x_207;
goto block_47;
}
}
}
else
{
lean_object* x_208; lean_object* x_209; lean_object* x_210; 
lean_inc_ref(x_167);
x_208 = lean_ctor_get(x_166, 1);
lean_inc(x_208);
lean_dec(x_166);
x_209 = lean_ctor_get(x_167, 0);
lean_inc(x_209);
lean_dec_ref(x_167);
x_210 = lp_REPL_REPL_instToJsonError_toJson(x_209);
x_3 = x_210;
x_4 = x_208;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
uint8_t x_211; 
x_211 = !lean_is_exclusive(x_165);
if (x_211 == 0)
{
return x_165;
}
else
{
lean_object* x_212; lean_object* x_213; 
x_212 = lean_ctor_get(x_165, 0);
lean_inc(x_212);
lean_dec(x_165);
x_213 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_213, 0, x_212);
return x_213;
}
}
}
case 1:
{
lean_object* x_214; lean_object* x_215; 
x_214 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_214);
lean_dec_ref(x_163);
x_215 = lp_REPL_REPL_processFile(x_214, x_1);
lean_dec_ref(x_214);
if (lean_obj_tag(x_215) == 0)
{
lean_object* x_216; lean_object* x_217; 
x_216 = lean_ctor_get(x_215, 0);
lean_inc(x_216);
lean_dec_ref(x_215);
x_217 = lean_ctor_get(x_216, 0);
if (lean_obj_tag(x_217) == 0)
{
lean_object* x_218; lean_object* x_219; 
x_218 = lean_ctor_get(x_217, 0);
lean_inc(x_218);
x_219 = lean_ctor_get(x_218, 0);
lean_inc(x_219);
if (lean_obj_tag(x_219) == 0)
{
lean_object* x_220; lean_object* x_221; lean_object* x_222; lean_object* x_223; lean_object* x_224; lean_object* x_225; 
x_220 = lean_ctor_get(x_216, 1);
lean_inc(x_220);
lean_dec(x_216);
x_221 = lean_ctor_get(x_218, 1);
lean_inc(x_221);
x_222 = lean_ctor_get(x_218, 2);
lean_inc(x_222);
x_223 = lean_ctor_get(x_218, 3);
lean_inc(x_223);
x_224 = lean_ctor_get(x_218, 4);
lean_inc(x_224);
lean_dec(x_218);
x_225 = lean_box(0);
x_65 = x_220;
x_66 = x_221;
x_67 = x_222;
x_68 = x_223;
x_69 = x_224;
x_70 = lean_box(0);
x_71 = x_225;
goto block_84;
}
else
{
uint8_t x_226; 
x_226 = !lean_is_exclusive(x_216);
if (x_226 == 0)
{
lean_object* x_227; lean_object* x_228; lean_object* x_229; lean_object* x_230; lean_object* x_231; lean_object* x_232; uint8_t x_233; 
x_227 = lean_ctor_get(x_216, 1);
x_228 = lean_ctor_get(x_216, 0);
lean_dec(x_228);
x_229 = lean_ctor_get(x_218, 1);
lean_inc(x_229);
x_230 = lean_ctor_get(x_218, 2);
lean_inc(x_230);
x_231 = lean_ctor_get(x_218, 3);
lean_inc(x_231);
x_232 = lean_ctor_get(x_218, 4);
lean_inc(x_232);
lean_dec(x_218);
x_233 = !lean_is_exclusive(x_219);
if (x_233 == 0)
{
lean_object* x_234; lean_object* x_235; lean_object* x_236; lean_object* x_237; lean_object* x_238; 
x_234 = lean_ctor_get(x_219, 0);
x_235 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_236 = l_Lean_JsonNumber_fromNat(x_234);
lean_ctor_set_tag(x_219, 2);
lean_ctor_set(x_219, 0, x_236);
lean_ctor_set(x_216, 1, x_219);
lean_ctor_set(x_216, 0, x_235);
x_237 = lean_box(0);
x_238 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_238, 0, x_216);
lean_ctor_set(x_238, 1, x_237);
x_65 = x_227;
x_66 = x_229;
x_67 = x_230;
x_68 = x_231;
x_69 = x_232;
x_70 = lean_box(0);
x_71 = x_238;
goto block_84;
}
else
{
lean_object* x_239; lean_object* x_240; lean_object* x_241; lean_object* x_242; lean_object* x_243; lean_object* x_244; 
x_239 = lean_ctor_get(x_219, 0);
lean_inc(x_239);
lean_dec(x_219);
x_240 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_241 = l_Lean_JsonNumber_fromNat(x_239);
x_242 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_242, 0, x_241);
lean_ctor_set(x_216, 1, x_242);
lean_ctor_set(x_216, 0, x_240);
x_243 = lean_box(0);
x_244 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_244, 0, x_216);
lean_ctor_set(x_244, 1, x_243);
x_65 = x_227;
x_66 = x_229;
x_67 = x_230;
x_68 = x_231;
x_69 = x_232;
x_70 = lean_box(0);
x_71 = x_244;
goto block_84;
}
}
else
{
lean_object* x_245; lean_object* x_246; lean_object* x_247; lean_object* x_248; lean_object* x_249; lean_object* x_250; lean_object* x_251; lean_object* x_252; lean_object* x_253; lean_object* x_254; lean_object* x_255; lean_object* x_256; lean_object* x_257; 
x_245 = lean_ctor_get(x_216, 1);
lean_inc(x_245);
lean_dec(x_216);
x_246 = lean_ctor_get(x_218, 1);
lean_inc(x_246);
x_247 = lean_ctor_get(x_218, 2);
lean_inc(x_247);
x_248 = lean_ctor_get(x_218, 3);
lean_inc(x_248);
x_249 = lean_ctor_get(x_218, 4);
lean_inc(x_249);
lean_dec(x_218);
x_250 = lean_ctor_get(x_219, 0);
lean_inc(x_250);
if (lean_is_exclusive(x_219)) {
 lean_ctor_release(x_219, 0);
 x_251 = x_219;
} else {
 lean_dec_ref(x_219);
 x_251 = lean_box(0);
}
x_252 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_253 = l_Lean_JsonNumber_fromNat(x_250);
if (lean_is_scalar(x_251)) {
 x_254 = lean_alloc_ctor(2, 1, 0);
} else {
 x_254 = x_251;
 lean_ctor_set_tag(x_254, 2);
}
lean_ctor_set(x_254, 0, x_253);
x_255 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_255, 0, x_252);
lean_ctor_set(x_255, 1, x_254);
x_256 = lean_box(0);
x_257 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_257, 0, x_255);
lean_ctor_set(x_257, 1, x_256);
x_65 = x_245;
x_66 = x_246;
x_67 = x_247;
x_68 = x_248;
x_69 = x_249;
x_70 = lean_box(0);
x_71 = x_257;
goto block_84;
}
}
}
else
{
lean_object* x_258; lean_object* x_259; lean_object* x_260; 
lean_inc_ref(x_217);
x_258 = lean_ctor_get(x_216, 1);
lean_inc(x_258);
lean_dec(x_216);
x_259 = lean_ctor_get(x_217, 0);
lean_inc(x_259);
lean_dec_ref(x_217);
x_260 = lp_REPL_REPL_instToJsonError_toJson(x_259);
x_3 = x_260;
x_4 = x_258;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
uint8_t x_261; 
x_261 = !lean_is_exclusive(x_215);
if (x_261 == 0)
{
return x_215;
}
else
{
lean_object* x_262; lean_object* x_263; 
x_262 = lean_ctor_get(x_215, 0);
lean_inc(x_262);
lean_dec(x_215);
x_263 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_263, 0, x_262);
return x_263;
}
}
}
case 2:
{
lean_object* x_264; lean_object* x_265; 
x_264 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_264);
lean_dec_ref(x_163);
x_265 = lp_REPL_REPL_runProofStep(x_264, x_1);
if (lean_obj_tag(x_265) == 0)
{
lean_object* x_266; lean_object* x_267; 
x_266 = lean_ctor_get(x_265, 0);
lean_inc(x_266);
lean_dec_ref(x_265);
x_267 = lean_ctor_get(x_266, 0);
lean_inc(x_267);
if (lean_obj_tag(x_267) == 0)
{
uint8_t x_268; 
x_268 = !lean_is_exclusive(x_267);
if (x_268 == 0)
{
uint8_t x_269; 
x_269 = !lean_is_exclusive(x_266);
if (x_269 == 0)
{
lean_object* x_270; lean_object* x_271; lean_object* x_272; lean_object* x_273; lean_object* x_274; lean_object* x_275; lean_object* x_276; lean_object* x_277; lean_object* x_278; lean_object* x_279; lean_object* x_280; lean_object* x_281; lean_object* x_282; lean_object* x_283; lean_object* x_284; lean_object* x_285; lean_object* x_286; lean_object* x_287; lean_object* x_288; lean_object* x_289; lean_object* x_290; lean_object* x_291; lean_object* x_292; lean_object* x_293; lean_object* x_294; lean_object* x_295; lean_object* x_296; lean_object* x_297; lean_object* x_298; lean_object* x_299; 
x_270 = lean_ctor_get(x_267, 0);
x_271 = lean_ctor_get(x_266, 1);
x_272 = lean_ctor_get(x_266, 0);
lean_dec(x_272);
x_273 = lean_ctor_get(x_270, 0);
lean_inc(x_273);
x_274 = lean_ctor_get(x_270, 1);
lean_inc(x_274);
x_275 = lean_ctor_get(x_270, 2);
lean_inc(x_275);
x_276 = lean_ctor_get(x_270, 3);
lean_inc(x_276);
x_277 = lean_ctor_get(x_270, 4);
lean_inc(x_277);
lean_dec(x_270);
x_278 = lp_REPL_repl_loop___closed__0;
x_279 = l_Lean_JsonNumber_fromNat(x_273);
lean_ctor_set_tag(x_267, 2);
lean_ctor_set(x_267, 0, x_279);
lean_ctor_set(x_266, 1, x_267);
lean_ctor_set(x_266, 0, x_278);
x_280 = lean_box(0);
x_281 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_281, 0, x_266);
lean_ctor_set(x_281, 1, x_280);
x_282 = lp_REPL_repl_loop___closed__1;
x_283 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_274);
x_284 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_284, 0, x_282);
lean_ctor_set(x_284, 1, x_283);
x_285 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_285, 0, x_284);
lean_ctor_set(x_285, 1, x_280);
x_286 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_287 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_286, x_275);
x_288 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_289 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_288, x_276);
x_290 = lp_REPL_repl_loop___closed__2;
x_291 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_290, x_277);
x_292 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_292, 0, x_291);
lean_ctor_set(x_292, 1, x_280);
x_293 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_293, 0, x_289);
lean_ctor_set(x_293, 1, x_292);
x_294 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_294, 0, x_287);
lean_ctor_set(x_294, 1, x_293);
x_295 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_295, 0, x_285);
lean_ctor_set(x_295, 1, x_294);
x_296 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_296, 0, x_281);
lean_ctor_set(x_296, 1, x_295);
x_297 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_298 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_296, x_297);
x_299 = l_Lean_Json_mkObj(x_298);
x_3 = x_299;
x_4 = x_271;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_300; lean_object* x_301; lean_object* x_302; lean_object* x_303; lean_object* x_304; lean_object* x_305; lean_object* x_306; lean_object* x_307; lean_object* x_308; lean_object* x_309; lean_object* x_310; lean_object* x_311; lean_object* x_312; lean_object* x_313; lean_object* x_314; lean_object* x_315; lean_object* x_316; lean_object* x_317; lean_object* x_318; lean_object* x_319; lean_object* x_320; lean_object* x_321; lean_object* x_322; lean_object* x_323; lean_object* x_324; lean_object* x_325; lean_object* x_326; lean_object* x_327; lean_object* x_328; lean_object* x_329; 
x_300 = lean_ctor_get(x_267, 0);
x_301 = lean_ctor_get(x_266, 1);
lean_inc(x_301);
lean_dec(x_266);
x_302 = lean_ctor_get(x_300, 0);
lean_inc(x_302);
x_303 = lean_ctor_get(x_300, 1);
lean_inc(x_303);
x_304 = lean_ctor_get(x_300, 2);
lean_inc(x_304);
x_305 = lean_ctor_get(x_300, 3);
lean_inc(x_305);
x_306 = lean_ctor_get(x_300, 4);
lean_inc(x_306);
lean_dec(x_300);
x_307 = lp_REPL_repl_loop___closed__0;
x_308 = l_Lean_JsonNumber_fromNat(x_302);
lean_ctor_set_tag(x_267, 2);
lean_ctor_set(x_267, 0, x_308);
x_309 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_309, 0, x_307);
lean_ctor_set(x_309, 1, x_267);
x_310 = lean_box(0);
x_311 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_311, 0, x_309);
lean_ctor_set(x_311, 1, x_310);
x_312 = lp_REPL_repl_loop___closed__1;
x_313 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_303);
x_314 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_314, 0, x_312);
lean_ctor_set(x_314, 1, x_313);
x_315 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_315, 0, x_314);
lean_ctor_set(x_315, 1, x_310);
x_316 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_317 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_316, x_304);
x_318 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_319 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_318, x_305);
x_320 = lp_REPL_repl_loop___closed__2;
x_321 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_320, x_306);
x_322 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_322, 0, x_321);
lean_ctor_set(x_322, 1, x_310);
x_323 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_323, 0, x_319);
lean_ctor_set(x_323, 1, x_322);
x_324 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_324, 0, x_317);
lean_ctor_set(x_324, 1, x_323);
x_325 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_325, 0, x_315);
lean_ctor_set(x_325, 1, x_324);
x_326 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_326, 0, x_311);
lean_ctor_set(x_326, 1, x_325);
x_327 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_328 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_326, x_327);
x_329 = l_Lean_Json_mkObj(x_328);
x_3 = x_329;
x_4 = x_301;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_330; lean_object* x_331; lean_object* x_332; lean_object* x_333; lean_object* x_334; lean_object* x_335; lean_object* x_336; lean_object* x_337; lean_object* x_338; lean_object* x_339; lean_object* x_340; lean_object* x_341; lean_object* x_342; lean_object* x_343; lean_object* x_344; lean_object* x_345; lean_object* x_346; lean_object* x_347; lean_object* x_348; lean_object* x_349; lean_object* x_350; lean_object* x_351; lean_object* x_352; lean_object* x_353; lean_object* x_354; lean_object* x_355; lean_object* x_356; lean_object* x_357; lean_object* x_358; lean_object* x_359; lean_object* x_360; lean_object* x_361; 
x_330 = lean_ctor_get(x_267, 0);
lean_inc(x_330);
lean_dec(x_267);
x_331 = lean_ctor_get(x_266, 1);
lean_inc(x_331);
if (lean_is_exclusive(x_266)) {
 lean_ctor_release(x_266, 0);
 lean_ctor_release(x_266, 1);
 x_332 = x_266;
} else {
 lean_dec_ref(x_266);
 x_332 = lean_box(0);
}
x_333 = lean_ctor_get(x_330, 0);
lean_inc(x_333);
x_334 = lean_ctor_get(x_330, 1);
lean_inc(x_334);
x_335 = lean_ctor_get(x_330, 2);
lean_inc(x_335);
x_336 = lean_ctor_get(x_330, 3);
lean_inc(x_336);
x_337 = lean_ctor_get(x_330, 4);
lean_inc(x_337);
lean_dec(x_330);
x_338 = lp_REPL_repl_loop___closed__0;
x_339 = l_Lean_JsonNumber_fromNat(x_333);
x_340 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_340, 0, x_339);
if (lean_is_scalar(x_332)) {
 x_341 = lean_alloc_ctor(0, 2, 0);
} else {
 x_341 = x_332;
}
lean_ctor_set(x_341, 0, x_338);
lean_ctor_set(x_341, 1, x_340);
x_342 = lean_box(0);
x_343 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_343, 0, x_341);
lean_ctor_set(x_343, 1, x_342);
x_344 = lp_REPL_repl_loop___closed__1;
x_345 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_334);
x_346 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_346, 0, x_344);
lean_ctor_set(x_346, 1, x_345);
x_347 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_347, 0, x_346);
lean_ctor_set(x_347, 1, x_342);
x_348 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_349 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_348, x_335);
x_350 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_351 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_350, x_336);
x_352 = lp_REPL_repl_loop___closed__2;
x_353 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_352, x_337);
x_354 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_354, 0, x_353);
lean_ctor_set(x_354, 1, x_342);
x_355 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_355, 0, x_351);
lean_ctor_set(x_355, 1, x_354);
x_356 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_356, 0, x_349);
lean_ctor_set(x_356, 1, x_355);
x_357 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_357, 0, x_347);
lean_ctor_set(x_357, 1, x_356);
x_358 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_358, 0, x_343);
lean_ctor_set(x_358, 1, x_357);
x_359 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_360 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_358, x_359);
x_361 = l_Lean_Json_mkObj(x_360);
x_3 = x_361;
x_4 = x_331;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_362; lean_object* x_363; lean_object* x_364; 
x_362 = lean_ctor_get(x_266, 1);
lean_inc(x_362);
lean_dec(x_266);
x_363 = lean_ctor_get(x_267, 0);
lean_inc(x_363);
lean_dec_ref(x_267);
x_364 = lp_REPL_REPL_instToJsonError_toJson(x_363);
x_3 = x_364;
x_4 = x_362;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
uint8_t x_365; 
x_365 = !lean_is_exclusive(x_265);
if (x_365 == 0)
{
return x_265;
}
else
{
lean_object* x_366; lean_object* x_367; 
x_366 = lean_ctor_get(x_265, 0);
lean_inc(x_366);
lean_dec(x_265);
x_367 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_367, 0, x_366);
return x_367;
}
}
}
case 3:
{
lean_object* x_368; lean_object* x_369; 
x_368 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_368);
lean_dec_ref(x_163);
x_369 = lp_REPL_REPL_pickleCommandSnapshot___at___00repl_loop_spec__9(x_368, x_1);
if (lean_obj_tag(x_369) == 0)
{
lean_object* x_370; lean_object* x_371; 
x_370 = lean_ctor_get(x_369, 0);
lean_inc(x_370);
lean_dec_ref(x_369);
x_371 = lean_ctor_get(x_370, 0);
if (lean_obj_tag(x_371) == 0)
{
lean_object* x_372; lean_object* x_373; 
x_372 = lean_ctor_get(x_371, 0);
lean_inc(x_372);
x_373 = lean_ctor_get(x_372, 0);
lean_inc(x_373);
if (lean_obj_tag(x_373) == 0)
{
lean_object* x_374; lean_object* x_375; lean_object* x_376; lean_object* x_377; lean_object* x_378; lean_object* x_379; 
x_374 = lean_ctor_get(x_370, 1);
lean_inc(x_374);
lean_dec(x_370);
x_375 = lean_ctor_get(x_372, 1);
lean_inc(x_375);
x_376 = lean_ctor_get(x_372, 2);
lean_inc(x_376);
x_377 = lean_ctor_get(x_372, 3);
lean_inc(x_377);
x_378 = lean_ctor_get(x_372, 4);
lean_inc(x_378);
lean_dec(x_372);
x_379 = lean_box(0);
x_102 = x_374;
x_103 = x_375;
x_104 = x_376;
x_105 = x_377;
x_106 = x_378;
x_107 = lean_box(0);
x_108 = x_379;
goto block_121;
}
else
{
uint8_t x_380; 
x_380 = !lean_is_exclusive(x_370);
if (x_380 == 0)
{
lean_object* x_381; lean_object* x_382; lean_object* x_383; lean_object* x_384; lean_object* x_385; lean_object* x_386; uint8_t x_387; 
x_381 = lean_ctor_get(x_370, 1);
x_382 = lean_ctor_get(x_370, 0);
lean_dec(x_382);
x_383 = lean_ctor_get(x_372, 1);
lean_inc(x_383);
x_384 = lean_ctor_get(x_372, 2);
lean_inc(x_384);
x_385 = lean_ctor_get(x_372, 3);
lean_inc(x_385);
x_386 = lean_ctor_get(x_372, 4);
lean_inc(x_386);
lean_dec(x_372);
x_387 = !lean_is_exclusive(x_373);
if (x_387 == 0)
{
lean_object* x_388; lean_object* x_389; lean_object* x_390; lean_object* x_391; lean_object* x_392; 
x_388 = lean_ctor_get(x_373, 0);
x_389 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_390 = l_Lean_JsonNumber_fromNat(x_388);
lean_ctor_set_tag(x_373, 2);
lean_ctor_set(x_373, 0, x_390);
lean_ctor_set(x_370, 1, x_373);
lean_ctor_set(x_370, 0, x_389);
x_391 = lean_box(0);
x_392 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_392, 0, x_370);
lean_ctor_set(x_392, 1, x_391);
x_102 = x_381;
x_103 = x_383;
x_104 = x_384;
x_105 = x_385;
x_106 = x_386;
x_107 = lean_box(0);
x_108 = x_392;
goto block_121;
}
else
{
lean_object* x_393; lean_object* x_394; lean_object* x_395; lean_object* x_396; lean_object* x_397; lean_object* x_398; 
x_393 = lean_ctor_get(x_373, 0);
lean_inc(x_393);
lean_dec(x_373);
x_394 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_395 = l_Lean_JsonNumber_fromNat(x_393);
x_396 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_396, 0, x_395);
lean_ctor_set(x_370, 1, x_396);
lean_ctor_set(x_370, 0, x_394);
x_397 = lean_box(0);
x_398 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_398, 0, x_370);
lean_ctor_set(x_398, 1, x_397);
x_102 = x_381;
x_103 = x_383;
x_104 = x_384;
x_105 = x_385;
x_106 = x_386;
x_107 = lean_box(0);
x_108 = x_398;
goto block_121;
}
}
else
{
lean_object* x_399; lean_object* x_400; lean_object* x_401; lean_object* x_402; lean_object* x_403; lean_object* x_404; lean_object* x_405; lean_object* x_406; lean_object* x_407; lean_object* x_408; lean_object* x_409; lean_object* x_410; lean_object* x_411; 
x_399 = lean_ctor_get(x_370, 1);
lean_inc(x_399);
lean_dec(x_370);
x_400 = lean_ctor_get(x_372, 1);
lean_inc(x_400);
x_401 = lean_ctor_get(x_372, 2);
lean_inc(x_401);
x_402 = lean_ctor_get(x_372, 3);
lean_inc(x_402);
x_403 = lean_ctor_get(x_372, 4);
lean_inc(x_403);
lean_dec(x_372);
x_404 = lean_ctor_get(x_373, 0);
lean_inc(x_404);
if (lean_is_exclusive(x_373)) {
 lean_ctor_release(x_373, 0);
 x_405 = x_373;
} else {
 lean_dec_ref(x_373);
 x_405 = lean_box(0);
}
x_406 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_407 = l_Lean_JsonNumber_fromNat(x_404);
if (lean_is_scalar(x_405)) {
 x_408 = lean_alloc_ctor(2, 1, 0);
} else {
 x_408 = x_405;
 lean_ctor_set_tag(x_408, 2);
}
lean_ctor_set(x_408, 0, x_407);
x_409 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_409, 0, x_406);
lean_ctor_set(x_409, 1, x_408);
x_410 = lean_box(0);
x_411 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_411, 0, x_409);
lean_ctor_set(x_411, 1, x_410);
x_102 = x_399;
x_103 = x_400;
x_104 = x_401;
x_105 = x_402;
x_106 = x_403;
x_107 = lean_box(0);
x_108 = x_411;
goto block_121;
}
}
}
else
{
lean_object* x_412; lean_object* x_413; lean_object* x_414; 
lean_inc_ref(x_371);
x_412 = lean_ctor_get(x_370, 1);
lean_inc(x_412);
lean_dec(x_370);
x_413 = lean_ctor_get(x_371, 0);
lean_inc(x_413);
lean_dec_ref(x_371);
x_414 = lp_REPL_REPL_instToJsonError_toJson(x_413);
x_3 = x_414;
x_4 = x_412;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
uint8_t x_415; 
x_415 = !lean_is_exclusive(x_369);
if (x_415 == 0)
{
return x_369;
}
else
{
lean_object* x_416; lean_object* x_417; 
x_416 = lean_ctor_get(x_369, 0);
lean_inc(x_416);
lean_dec(x_369);
x_417 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_417, 0, x_416);
return x_417;
}
}
}
case 4:
{
lean_object* x_418; lean_object* x_419; 
x_418 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_418);
lean_dec_ref(x_163);
x_419 = lp_REPL_REPL_unpickleCommandSnapshot(x_418, x_1);
if (lean_obj_tag(x_419) == 0)
{
lean_object* x_420; lean_object* x_421; lean_object* x_422; 
x_420 = lean_ctor_get(x_419, 0);
lean_inc(x_420);
lean_dec_ref(x_419);
x_421 = lean_ctor_get(x_420, 0);
lean_inc(x_421);
x_422 = lean_ctor_get(x_421, 0);
lean_inc(x_422);
if (lean_obj_tag(x_422) == 0)
{
lean_object* x_423; lean_object* x_424; lean_object* x_425; lean_object* x_426; lean_object* x_427; lean_object* x_428; 
x_423 = lean_ctor_get(x_420, 1);
lean_inc(x_423);
lean_dec(x_420);
x_424 = lean_ctor_get(x_421, 1);
lean_inc(x_424);
x_425 = lean_ctor_get(x_421, 2);
lean_inc(x_425);
x_426 = lean_ctor_get(x_421, 3);
lean_inc(x_426);
x_427 = lean_ctor_get(x_421, 4);
lean_inc(x_427);
lean_dec(x_421);
x_428 = lean_box(0);
x_139 = lean_box(0);
x_140 = x_423;
x_141 = x_424;
x_142 = x_425;
x_143 = x_426;
x_144 = x_427;
x_145 = x_428;
goto block_158;
}
else
{
uint8_t x_429; 
x_429 = !lean_is_exclusive(x_420);
if (x_429 == 0)
{
lean_object* x_430; lean_object* x_431; lean_object* x_432; lean_object* x_433; lean_object* x_434; lean_object* x_435; uint8_t x_436; 
x_430 = lean_ctor_get(x_420, 1);
x_431 = lean_ctor_get(x_420, 0);
lean_dec(x_431);
x_432 = lean_ctor_get(x_421, 1);
lean_inc(x_432);
x_433 = lean_ctor_get(x_421, 2);
lean_inc(x_433);
x_434 = lean_ctor_get(x_421, 3);
lean_inc(x_434);
x_435 = lean_ctor_get(x_421, 4);
lean_inc(x_435);
lean_dec(x_421);
x_436 = !lean_is_exclusive(x_422);
if (x_436 == 0)
{
lean_object* x_437; lean_object* x_438; lean_object* x_439; lean_object* x_440; lean_object* x_441; 
x_437 = lean_ctor_get(x_422, 0);
x_438 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_439 = l_Lean_JsonNumber_fromNat(x_437);
lean_ctor_set_tag(x_422, 2);
lean_ctor_set(x_422, 0, x_439);
lean_ctor_set(x_420, 1, x_422);
lean_ctor_set(x_420, 0, x_438);
x_440 = lean_box(0);
x_441 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_441, 0, x_420);
lean_ctor_set(x_441, 1, x_440);
x_139 = lean_box(0);
x_140 = x_430;
x_141 = x_432;
x_142 = x_433;
x_143 = x_434;
x_144 = x_435;
x_145 = x_441;
goto block_158;
}
else
{
lean_object* x_442; lean_object* x_443; lean_object* x_444; lean_object* x_445; lean_object* x_446; lean_object* x_447; 
x_442 = lean_ctor_get(x_422, 0);
lean_inc(x_442);
lean_dec(x_422);
x_443 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_444 = l_Lean_JsonNumber_fromNat(x_442);
x_445 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_445, 0, x_444);
lean_ctor_set(x_420, 1, x_445);
lean_ctor_set(x_420, 0, x_443);
x_446 = lean_box(0);
x_447 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_447, 0, x_420);
lean_ctor_set(x_447, 1, x_446);
x_139 = lean_box(0);
x_140 = x_430;
x_141 = x_432;
x_142 = x_433;
x_143 = x_434;
x_144 = x_435;
x_145 = x_447;
goto block_158;
}
}
else
{
lean_object* x_448; lean_object* x_449; lean_object* x_450; lean_object* x_451; lean_object* x_452; lean_object* x_453; lean_object* x_454; lean_object* x_455; lean_object* x_456; lean_object* x_457; lean_object* x_458; lean_object* x_459; lean_object* x_460; 
x_448 = lean_ctor_get(x_420, 1);
lean_inc(x_448);
lean_dec(x_420);
x_449 = lean_ctor_get(x_421, 1);
lean_inc(x_449);
x_450 = lean_ctor_get(x_421, 2);
lean_inc(x_450);
x_451 = lean_ctor_get(x_421, 3);
lean_inc(x_451);
x_452 = lean_ctor_get(x_421, 4);
lean_inc(x_452);
lean_dec(x_421);
x_453 = lean_ctor_get(x_422, 0);
lean_inc(x_453);
if (lean_is_exclusive(x_422)) {
 lean_ctor_release(x_422, 0);
 x_454 = x_422;
} else {
 lean_dec_ref(x_422);
 x_454 = lean_box(0);
}
x_455 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_456 = l_Lean_JsonNumber_fromNat(x_453);
if (lean_is_scalar(x_454)) {
 x_457 = lean_alloc_ctor(2, 1, 0);
} else {
 x_457 = x_454;
 lean_ctor_set_tag(x_457, 2);
}
lean_ctor_set(x_457, 0, x_456);
x_458 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_458, 0, x_455);
lean_ctor_set(x_458, 1, x_457);
x_459 = lean_box(0);
x_460 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_460, 0, x_458);
lean_ctor_set(x_460, 1, x_459);
x_139 = lean_box(0);
x_140 = x_448;
x_141 = x_449;
x_142 = x_450;
x_143 = x_451;
x_144 = x_452;
x_145 = x_460;
goto block_158;
}
}
}
else
{
uint8_t x_461; 
x_461 = !lean_is_exclusive(x_419);
if (x_461 == 0)
{
return x_419;
}
else
{
lean_object* x_462; lean_object* x_463; 
x_462 = lean_ctor_get(x_419, 0);
lean_inc(x_462);
lean_dec(x_419);
x_463 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_463, 0, x_462);
return x_463;
}
}
}
case 5:
{
lean_object* x_464; lean_object* x_465; 
x_464 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_464);
lean_dec_ref(x_163);
x_465 = lp_REPL_REPL_pickleProofSnapshot___at___00repl_loop_spec__10(x_464, x_1);
if (lean_obj_tag(x_465) == 0)
{
lean_object* x_466; lean_object* x_467; 
x_466 = lean_ctor_get(x_465, 0);
lean_inc(x_466);
lean_dec_ref(x_465);
x_467 = lean_ctor_get(x_466, 0);
lean_inc(x_467);
if (lean_obj_tag(x_467) == 0)
{
uint8_t x_468; 
x_468 = !lean_is_exclusive(x_467);
if (x_468 == 0)
{
uint8_t x_469; 
x_469 = !lean_is_exclusive(x_466);
if (x_469 == 0)
{
lean_object* x_470; lean_object* x_471; lean_object* x_472; lean_object* x_473; lean_object* x_474; lean_object* x_475; lean_object* x_476; lean_object* x_477; lean_object* x_478; lean_object* x_479; lean_object* x_480; lean_object* x_481; lean_object* x_482; lean_object* x_483; lean_object* x_484; lean_object* x_485; lean_object* x_486; lean_object* x_487; lean_object* x_488; lean_object* x_489; lean_object* x_490; lean_object* x_491; lean_object* x_492; lean_object* x_493; lean_object* x_494; lean_object* x_495; lean_object* x_496; lean_object* x_497; lean_object* x_498; lean_object* x_499; 
x_470 = lean_ctor_get(x_467, 0);
x_471 = lean_ctor_get(x_466, 1);
x_472 = lean_ctor_get(x_466, 0);
lean_dec(x_472);
x_473 = lean_ctor_get(x_470, 0);
lean_inc(x_473);
x_474 = lean_ctor_get(x_470, 1);
lean_inc(x_474);
x_475 = lean_ctor_get(x_470, 2);
lean_inc(x_475);
x_476 = lean_ctor_get(x_470, 3);
lean_inc(x_476);
x_477 = lean_ctor_get(x_470, 4);
lean_inc(x_477);
lean_dec(x_470);
x_478 = lp_REPL_repl_loop___closed__0;
x_479 = l_Lean_JsonNumber_fromNat(x_473);
lean_ctor_set_tag(x_467, 2);
lean_ctor_set(x_467, 0, x_479);
lean_ctor_set(x_466, 1, x_467);
lean_ctor_set(x_466, 0, x_478);
x_480 = lean_box(0);
x_481 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_481, 0, x_466);
lean_ctor_set(x_481, 1, x_480);
x_482 = lp_REPL_repl_loop___closed__1;
x_483 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_474);
x_484 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_484, 0, x_482);
lean_ctor_set(x_484, 1, x_483);
x_485 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_485, 0, x_484);
lean_ctor_set(x_485, 1, x_480);
x_486 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_487 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_486, x_475);
x_488 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_489 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_488, x_476);
x_490 = lp_REPL_repl_loop___closed__2;
x_491 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_490, x_477);
x_492 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_492, 0, x_491);
lean_ctor_set(x_492, 1, x_480);
x_493 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_493, 0, x_489);
lean_ctor_set(x_493, 1, x_492);
x_494 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_494, 0, x_487);
lean_ctor_set(x_494, 1, x_493);
x_495 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_495, 0, x_485);
lean_ctor_set(x_495, 1, x_494);
x_496 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_496, 0, x_481);
lean_ctor_set(x_496, 1, x_495);
x_497 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_498 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_496, x_497);
x_499 = l_Lean_Json_mkObj(x_498);
x_3 = x_499;
x_4 = x_471;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_500; lean_object* x_501; lean_object* x_502; lean_object* x_503; lean_object* x_504; lean_object* x_505; lean_object* x_506; lean_object* x_507; lean_object* x_508; lean_object* x_509; lean_object* x_510; lean_object* x_511; lean_object* x_512; lean_object* x_513; lean_object* x_514; lean_object* x_515; lean_object* x_516; lean_object* x_517; lean_object* x_518; lean_object* x_519; lean_object* x_520; lean_object* x_521; lean_object* x_522; lean_object* x_523; lean_object* x_524; lean_object* x_525; lean_object* x_526; lean_object* x_527; lean_object* x_528; lean_object* x_529; 
x_500 = lean_ctor_get(x_467, 0);
x_501 = lean_ctor_get(x_466, 1);
lean_inc(x_501);
lean_dec(x_466);
x_502 = lean_ctor_get(x_500, 0);
lean_inc(x_502);
x_503 = lean_ctor_get(x_500, 1);
lean_inc(x_503);
x_504 = lean_ctor_get(x_500, 2);
lean_inc(x_504);
x_505 = lean_ctor_get(x_500, 3);
lean_inc(x_505);
x_506 = lean_ctor_get(x_500, 4);
lean_inc(x_506);
lean_dec(x_500);
x_507 = lp_REPL_repl_loop___closed__0;
x_508 = l_Lean_JsonNumber_fromNat(x_502);
lean_ctor_set_tag(x_467, 2);
lean_ctor_set(x_467, 0, x_508);
x_509 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_509, 0, x_507);
lean_ctor_set(x_509, 1, x_467);
x_510 = lean_box(0);
x_511 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_511, 0, x_509);
lean_ctor_set(x_511, 1, x_510);
x_512 = lp_REPL_repl_loop___closed__1;
x_513 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_503);
x_514 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_514, 0, x_512);
lean_ctor_set(x_514, 1, x_513);
x_515 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_515, 0, x_514);
lean_ctor_set(x_515, 1, x_510);
x_516 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_517 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_516, x_504);
x_518 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_519 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_518, x_505);
x_520 = lp_REPL_repl_loop___closed__2;
x_521 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_520, x_506);
x_522 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_522, 0, x_521);
lean_ctor_set(x_522, 1, x_510);
x_523 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_523, 0, x_519);
lean_ctor_set(x_523, 1, x_522);
x_524 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_524, 0, x_517);
lean_ctor_set(x_524, 1, x_523);
x_525 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_525, 0, x_515);
lean_ctor_set(x_525, 1, x_524);
x_526 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_526, 0, x_511);
lean_ctor_set(x_526, 1, x_525);
x_527 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_528 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_526, x_527);
x_529 = l_Lean_Json_mkObj(x_528);
x_3 = x_529;
x_4 = x_501;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_530; lean_object* x_531; lean_object* x_532; lean_object* x_533; lean_object* x_534; lean_object* x_535; lean_object* x_536; lean_object* x_537; lean_object* x_538; lean_object* x_539; lean_object* x_540; lean_object* x_541; lean_object* x_542; lean_object* x_543; lean_object* x_544; lean_object* x_545; lean_object* x_546; lean_object* x_547; lean_object* x_548; lean_object* x_549; lean_object* x_550; lean_object* x_551; lean_object* x_552; lean_object* x_553; lean_object* x_554; lean_object* x_555; lean_object* x_556; lean_object* x_557; lean_object* x_558; lean_object* x_559; lean_object* x_560; lean_object* x_561; 
x_530 = lean_ctor_get(x_467, 0);
lean_inc(x_530);
lean_dec(x_467);
x_531 = lean_ctor_get(x_466, 1);
lean_inc(x_531);
if (lean_is_exclusive(x_466)) {
 lean_ctor_release(x_466, 0);
 lean_ctor_release(x_466, 1);
 x_532 = x_466;
} else {
 lean_dec_ref(x_466);
 x_532 = lean_box(0);
}
x_533 = lean_ctor_get(x_530, 0);
lean_inc(x_533);
x_534 = lean_ctor_get(x_530, 1);
lean_inc(x_534);
x_535 = lean_ctor_get(x_530, 2);
lean_inc(x_535);
x_536 = lean_ctor_get(x_530, 3);
lean_inc(x_536);
x_537 = lean_ctor_get(x_530, 4);
lean_inc(x_537);
lean_dec(x_530);
x_538 = lp_REPL_repl_loop___closed__0;
x_539 = l_Lean_JsonNumber_fromNat(x_533);
x_540 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_540, 0, x_539);
if (lean_is_scalar(x_532)) {
 x_541 = lean_alloc_ctor(0, 2, 0);
} else {
 x_541 = x_532;
}
lean_ctor_set(x_541, 0, x_538);
lean_ctor_set(x_541, 1, x_540);
x_542 = lean_box(0);
x_543 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_543, 0, x_541);
lean_ctor_set(x_543, 1, x_542);
x_544 = lp_REPL_repl_loop___closed__1;
x_545 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_534);
x_546 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_546, 0, x_544);
lean_ctor_set(x_546, 1, x_545);
x_547 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_547, 0, x_546);
lean_ctor_set(x_547, 1, x_542);
x_548 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_549 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_548, x_535);
x_550 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_551 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_550, x_536);
x_552 = lp_REPL_repl_loop___closed__2;
x_553 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_552, x_537);
x_554 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_554, 0, x_553);
lean_ctor_set(x_554, 1, x_542);
x_555 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_555, 0, x_551);
lean_ctor_set(x_555, 1, x_554);
x_556 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_556, 0, x_549);
lean_ctor_set(x_556, 1, x_555);
x_557 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_557, 0, x_547);
lean_ctor_set(x_557, 1, x_556);
x_558 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_558, 0, x_543);
lean_ctor_set(x_558, 1, x_557);
x_559 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_560 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_558, x_559);
x_561 = l_Lean_Json_mkObj(x_560);
x_3 = x_561;
x_4 = x_531;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_562; lean_object* x_563; lean_object* x_564; 
x_562 = lean_ctor_get(x_466, 1);
lean_inc(x_562);
lean_dec(x_466);
x_563 = lean_ctor_get(x_467, 0);
lean_inc(x_563);
lean_dec_ref(x_467);
x_564 = lp_REPL_REPL_instToJsonError_toJson(x_563);
x_3 = x_564;
x_4 = x_562;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
uint8_t x_565; 
x_565 = !lean_is_exclusive(x_465);
if (x_565 == 0)
{
return x_465;
}
else
{
lean_object* x_566; lean_object* x_567; 
x_566 = lean_ctor_get(x_465, 0);
lean_inc(x_566);
lean_dec(x_465);
x_567 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_567, 0, x_566);
return x_567;
}
}
}
case 6:
{
lean_object* x_568; lean_object* x_569; 
x_568 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_568);
lean_dec_ref(x_163);
x_569 = lp_REPL_REPL_unpickleProofSnapshot(x_568, x_1);
if (lean_obj_tag(x_569) == 0)
{
lean_object* x_570; lean_object* x_571; 
x_570 = lean_ctor_get(x_569, 0);
lean_inc(x_570);
lean_dec_ref(x_569);
x_571 = lean_ctor_get(x_570, 0);
lean_inc(x_571);
if (lean_obj_tag(x_571) == 0)
{
uint8_t x_572; 
x_572 = !lean_is_exclusive(x_571);
if (x_572 == 0)
{
uint8_t x_573; 
x_573 = !lean_is_exclusive(x_570);
if (x_573 == 0)
{
lean_object* x_574; lean_object* x_575; lean_object* x_576; lean_object* x_577; lean_object* x_578; lean_object* x_579; lean_object* x_580; lean_object* x_581; lean_object* x_582; lean_object* x_583; lean_object* x_584; lean_object* x_585; lean_object* x_586; lean_object* x_587; lean_object* x_588; lean_object* x_589; lean_object* x_590; lean_object* x_591; lean_object* x_592; lean_object* x_593; lean_object* x_594; lean_object* x_595; lean_object* x_596; lean_object* x_597; lean_object* x_598; lean_object* x_599; lean_object* x_600; lean_object* x_601; lean_object* x_602; lean_object* x_603; 
x_574 = lean_ctor_get(x_571, 0);
x_575 = lean_ctor_get(x_570, 1);
x_576 = lean_ctor_get(x_570, 0);
lean_dec(x_576);
x_577 = lean_ctor_get(x_574, 0);
lean_inc(x_577);
x_578 = lean_ctor_get(x_574, 1);
lean_inc(x_578);
x_579 = lean_ctor_get(x_574, 2);
lean_inc(x_579);
x_580 = lean_ctor_get(x_574, 3);
lean_inc(x_580);
x_581 = lean_ctor_get(x_574, 4);
lean_inc(x_581);
lean_dec(x_574);
x_582 = lp_REPL_repl_loop___closed__0;
x_583 = l_Lean_JsonNumber_fromNat(x_577);
lean_ctor_set_tag(x_571, 2);
lean_ctor_set(x_571, 0, x_583);
lean_ctor_set(x_570, 1, x_571);
lean_ctor_set(x_570, 0, x_582);
x_584 = lean_box(0);
x_585 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_585, 0, x_570);
lean_ctor_set(x_585, 1, x_584);
x_586 = lp_REPL_repl_loop___closed__1;
x_587 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_578);
x_588 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_588, 0, x_586);
lean_ctor_set(x_588, 1, x_587);
x_589 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_589, 0, x_588);
lean_ctor_set(x_589, 1, x_584);
x_590 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_591 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_590, x_579);
x_592 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_593 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_592, x_580);
x_594 = lp_REPL_repl_loop___closed__2;
x_595 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_594, x_581);
x_596 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_596, 0, x_595);
lean_ctor_set(x_596, 1, x_584);
x_597 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_597, 0, x_593);
lean_ctor_set(x_597, 1, x_596);
x_598 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_598, 0, x_591);
lean_ctor_set(x_598, 1, x_597);
x_599 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_599, 0, x_589);
lean_ctor_set(x_599, 1, x_598);
x_600 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_600, 0, x_585);
lean_ctor_set(x_600, 1, x_599);
x_601 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_602 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_600, x_601);
x_603 = l_Lean_Json_mkObj(x_602);
x_3 = x_603;
x_4 = x_575;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_604; lean_object* x_605; lean_object* x_606; lean_object* x_607; lean_object* x_608; lean_object* x_609; lean_object* x_610; lean_object* x_611; lean_object* x_612; lean_object* x_613; lean_object* x_614; lean_object* x_615; lean_object* x_616; lean_object* x_617; lean_object* x_618; lean_object* x_619; lean_object* x_620; lean_object* x_621; lean_object* x_622; lean_object* x_623; lean_object* x_624; lean_object* x_625; lean_object* x_626; lean_object* x_627; lean_object* x_628; lean_object* x_629; lean_object* x_630; lean_object* x_631; lean_object* x_632; lean_object* x_633; 
x_604 = lean_ctor_get(x_571, 0);
x_605 = lean_ctor_get(x_570, 1);
lean_inc(x_605);
lean_dec(x_570);
x_606 = lean_ctor_get(x_604, 0);
lean_inc(x_606);
x_607 = lean_ctor_get(x_604, 1);
lean_inc(x_607);
x_608 = lean_ctor_get(x_604, 2);
lean_inc(x_608);
x_609 = lean_ctor_get(x_604, 3);
lean_inc(x_609);
x_610 = lean_ctor_get(x_604, 4);
lean_inc(x_610);
lean_dec(x_604);
x_611 = lp_REPL_repl_loop___closed__0;
x_612 = l_Lean_JsonNumber_fromNat(x_606);
lean_ctor_set_tag(x_571, 2);
lean_ctor_set(x_571, 0, x_612);
x_613 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_613, 0, x_611);
lean_ctor_set(x_613, 1, x_571);
x_614 = lean_box(0);
x_615 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_615, 0, x_613);
lean_ctor_set(x_615, 1, x_614);
x_616 = lp_REPL_repl_loop___closed__1;
x_617 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_607);
x_618 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_618, 0, x_616);
lean_ctor_set(x_618, 1, x_617);
x_619 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_619, 0, x_618);
lean_ctor_set(x_619, 1, x_614);
x_620 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_621 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_620, x_608);
x_622 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_623 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_622, x_609);
x_624 = lp_REPL_repl_loop___closed__2;
x_625 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_624, x_610);
x_626 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_626, 0, x_625);
lean_ctor_set(x_626, 1, x_614);
x_627 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_627, 0, x_623);
lean_ctor_set(x_627, 1, x_626);
x_628 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_628, 0, x_621);
lean_ctor_set(x_628, 1, x_627);
x_629 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_629, 0, x_619);
lean_ctor_set(x_629, 1, x_628);
x_630 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_630, 0, x_615);
lean_ctor_set(x_630, 1, x_629);
x_631 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_632 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_630, x_631);
x_633 = l_Lean_Json_mkObj(x_632);
x_3 = x_633;
x_4 = x_605;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_634; lean_object* x_635; lean_object* x_636; lean_object* x_637; lean_object* x_638; lean_object* x_639; lean_object* x_640; lean_object* x_641; lean_object* x_642; lean_object* x_643; lean_object* x_644; lean_object* x_645; lean_object* x_646; lean_object* x_647; lean_object* x_648; lean_object* x_649; lean_object* x_650; lean_object* x_651; lean_object* x_652; lean_object* x_653; lean_object* x_654; lean_object* x_655; lean_object* x_656; lean_object* x_657; lean_object* x_658; lean_object* x_659; lean_object* x_660; lean_object* x_661; lean_object* x_662; lean_object* x_663; lean_object* x_664; lean_object* x_665; 
x_634 = lean_ctor_get(x_571, 0);
lean_inc(x_634);
lean_dec(x_571);
x_635 = lean_ctor_get(x_570, 1);
lean_inc(x_635);
if (lean_is_exclusive(x_570)) {
 lean_ctor_release(x_570, 0);
 lean_ctor_release(x_570, 1);
 x_636 = x_570;
} else {
 lean_dec_ref(x_570);
 x_636 = lean_box(0);
}
x_637 = lean_ctor_get(x_634, 0);
lean_inc(x_637);
x_638 = lean_ctor_get(x_634, 1);
lean_inc(x_638);
x_639 = lean_ctor_get(x_634, 2);
lean_inc(x_639);
x_640 = lean_ctor_get(x_634, 3);
lean_inc(x_640);
x_641 = lean_ctor_get(x_634, 4);
lean_inc(x_641);
lean_dec(x_634);
x_642 = lp_REPL_repl_loop___closed__0;
x_643 = l_Lean_JsonNumber_fromNat(x_637);
x_644 = lean_alloc_ctor(2, 1, 0);
lean_ctor_set(x_644, 0, x_643);
if (lean_is_scalar(x_636)) {
 x_645 = lean_alloc_ctor(0, 2, 0);
} else {
 x_645 = x_636;
}
lean_ctor_set(x_645, 0, x_642);
lean_ctor_set(x_645, 1, x_644);
x_646 = lean_box(0);
x_647 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_647, 0, x_645);
lean_ctor_set(x_647, 1, x_646);
x_648 = lp_REPL_repl_loop___closed__1;
x_649 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_638);
x_650 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_650, 0, x_648);
lean_ctor_set(x_650, 1, x_649);
x_651 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_651, 0, x_650);
lean_ctor_set(x_651, 1, x_646);
x_652 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_653 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_652, x_639);
x_654 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_655 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_654, x_640);
x_656 = lp_REPL_repl_loop___closed__2;
x_657 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_656, x_641);
x_658 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_658, 0, x_657);
lean_ctor_set(x_658, 1, x_646);
x_659 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_659, 0, x_655);
lean_ctor_set(x_659, 1, x_658);
x_660 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_660, 0, x_653);
lean_ctor_set(x_660, 1, x_659);
x_661 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_661, 0, x_651);
lean_ctor_set(x_661, 1, x_660);
x_662 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_662, 0, x_647);
lean_ctor_set(x_662, 1, x_661);
x_663 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_664 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_662, x_663);
x_665 = l_Lean_Json_mkObj(x_664);
x_3 = x_665;
x_4 = x_635;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_666; lean_object* x_667; lean_object* x_668; 
x_666 = lean_ctor_get(x_570, 1);
lean_inc(x_666);
lean_dec(x_570);
x_667 = lean_ctor_get(x_571, 0);
lean_inc(x_667);
lean_dec_ref(x_571);
x_668 = lp_REPL_REPL_instToJsonError_toJson(x_667);
x_3 = x_668;
x_4 = x_666;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
uint8_t x_669; 
x_669 = !lean_is_exclusive(x_569);
if (x_669 == 0)
{
return x_569;
}
else
{
lean_object* x_670; lean_object* x_671; 
x_670 = lean_ctor_get(x_569, 0);
lean_inc(x_670);
lean_dec(x_569);
x_671 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_671, 0, x_670);
return x_671;
}
}
}
default: 
{
lean_object* x_672; lean_object* x_673; 
x_672 = lean_ctor_get(x_163, 0);
lean_inc_ref(x_672);
lean_dec_ref(x_163);
x_673 = lp_REPL_REPL_runBatchVerify(x_672, x_1);
if (lean_obj_tag(x_673) == 0)
{
lean_object* x_674; lean_object* x_675; 
x_674 = lean_ctor_get(x_673, 0);
lean_inc(x_674);
lean_dec_ref(x_673);
x_675 = lean_ctor_get(x_674, 0);
lean_inc(x_675);
if (lean_obj_tag(x_675) == 0)
{
lean_object* x_676; lean_object* x_677; lean_object* x_678; 
x_676 = lean_ctor_get(x_674, 1);
lean_inc(x_676);
lean_dec(x_674);
x_677 = lean_ctor_get(x_675, 0);
lean_inc(x_677);
lean_dec_ref(x_675);
x_678 = lp_REPL_Array_toJson___at___00repl_loop_spec__11(x_677);
x_3 = x_678;
x_4 = x_676;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_679; lean_object* x_680; lean_object* x_681; 
x_679 = lean_ctor_get(x_674, 1);
lean_inc(x_679);
lean_dec(x_674);
x_680 = lean_ctor_get(x_675, 0);
lean_inc(x_680);
lean_dec_ref(x_675);
x_681 = lp_REPL_REPL_instToJsonError_toJson(x_680);
x_3 = x_681;
x_4 = x_679;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
uint8_t x_682; 
x_682 = !lean_is_exclusive(x_673);
if (x_682 == 0)
{
return x_673;
}
else
{
lean_object* x_683; lean_object* x_684; 
x_683 = lean_ctor_get(x_673, 0);
lean_inc(x_683);
lean_dec(x_673);
x_684 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_684, 0, x_683);
return x_684;
}
}
}
}
}
else
{
uint8_t x_685; 
lean_dec_ref(x_1);
x_685 = !lean_is_exclusive(x_162);
if (x_685 == 0)
{
return x_162;
}
else
{
lean_object* x_686; lean_object* x_687; 
x_686 = lean_ctor_get(x_162, 0);
lean_inc(x_686);
lean_dec(x_162);
x_687 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_687, 0, x_686);
return x_687;
}
}
}
block_696:
{
lean_object* x_689; lean_object* x_690; lean_object* x_691; uint8_t x_692; 
x_689 = lp_REPL_repl_loop___closed__3;
x_690 = lean_string_utf8_byte_size(x_161);
x_691 = lp_REPL_repl_loop___closed__4;
x_692 = lean_nat_dec_le(x_691, x_690);
if (x_692 == 0)
{
goto block_688;
}
else
{
lean_object* x_693; uint8_t x_694; 
x_693 = lean_unsigned_to_nat(0u);
x_694 = lean_string_memcmp(x_161, x_689, x_693, x_693, x_691);
if (x_694 == 0)
{
goto block_688;
}
else
{
lean_dec(x_161);
goto _start;
}
}
}
}
else
{
lean_object* x_707; lean_object* x_988; uint8_t x_989; 
x_707 = lean_ctor_get(x_159, 0);
lean_inc(x_707);
lean_dec(x_159);
x_988 = lp_REPL_REPL_sorries___redArg___closed__0;
x_989 = lean_string_dec_eq(x_707, x_988);
if (x_989 == 0)
{
lean_object* x_990; lean_object* x_991; lean_object* x_992; uint8_t x_993; 
x_990 = lp_REPL_repl_loop___closed__5;
x_991 = lean_string_utf8_byte_size(x_707);
x_992 = lp_REPL_repl_loop___closed__6;
x_993 = lean_nat_dec_le(x_992, x_991);
if (x_993 == 0)
{
goto block_987;
}
else
{
lean_object* x_994; uint8_t x_995; 
x_994 = lean_unsigned_to_nat(0u);
x_995 = lean_string_memcmp(x_707, x_990, x_994, x_994, x_992);
if (x_995 == 0)
{
goto block_987;
}
else
{
lean_dec(x_707);
goto _start;
}
}
}
else
{
lean_object* x_997; lean_object* x_998; 
lean_dec(x_707);
lean_dec_ref(x_1);
x_997 = lean_box(0);
x_998 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_998, 0, x_997);
return x_998;
}
block_979:
{
lean_object* x_708; 
x_708 = lp_REPL_parse(x_707);
if (lean_obj_tag(x_708) == 0)
{
lean_object* x_709; 
x_709 = lean_ctor_get(x_708, 0);
lean_inc(x_709);
lean_dec_ref(x_708);
switch (lean_obj_tag(x_709)) {
case 0:
{
lean_object* x_710; lean_object* x_711; 
x_710 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_710);
lean_dec_ref(x_709);
x_711 = lp_REPL_REPL_runCommand(x_710, x_1);
if (lean_obj_tag(x_711) == 0)
{
lean_object* x_712; lean_object* x_713; 
x_712 = lean_ctor_get(x_711, 0);
lean_inc(x_712);
lean_dec_ref(x_711);
x_713 = lean_ctor_get(x_712, 0);
if (lean_obj_tag(x_713) == 0)
{
lean_object* x_714; lean_object* x_715; 
x_714 = lean_ctor_get(x_713, 0);
lean_inc(x_714);
x_715 = lean_ctor_get(x_714, 0);
lean_inc(x_715);
if (lean_obj_tag(x_715) == 0)
{
lean_object* x_716; lean_object* x_717; lean_object* x_718; lean_object* x_719; lean_object* x_720; lean_object* x_721; 
x_716 = lean_ctor_get(x_712, 1);
lean_inc(x_716);
lean_dec(x_712);
x_717 = lean_ctor_get(x_714, 1);
lean_inc(x_717);
x_718 = lean_ctor_get(x_714, 2);
lean_inc(x_718);
x_719 = lean_ctor_get(x_714, 3);
lean_inc(x_719);
x_720 = lean_ctor_get(x_714, 4);
lean_inc(x_720);
lean_dec(x_714);
x_721 = lean_box(0);
x_28 = lean_box(0);
x_29 = x_717;
x_30 = x_718;
x_31 = x_719;
x_32 = x_720;
x_33 = x_716;
x_34 = x_721;
goto block_47;
}
else
{
lean_object* x_722; lean_object* x_723; lean_object* x_724; lean_object* x_725; lean_object* x_726; lean_object* x_727; lean_object* x_728; lean_object* x_729; lean_object* x_730; lean_object* x_731; lean_object* x_732; lean_object* x_733; lean_object* x_734; lean_object* x_735; 
x_722 = lean_ctor_get(x_712, 1);
lean_inc(x_722);
if (lean_is_exclusive(x_712)) {
 lean_ctor_release(x_712, 0);
 lean_ctor_release(x_712, 1);
 x_723 = x_712;
} else {
 lean_dec_ref(x_712);
 x_723 = lean_box(0);
}
x_724 = lean_ctor_get(x_714, 1);
lean_inc(x_724);
x_725 = lean_ctor_get(x_714, 2);
lean_inc(x_725);
x_726 = lean_ctor_get(x_714, 3);
lean_inc(x_726);
x_727 = lean_ctor_get(x_714, 4);
lean_inc(x_727);
lean_dec(x_714);
x_728 = lean_ctor_get(x_715, 0);
lean_inc(x_728);
if (lean_is_exclusive(x_715)) {
 lean_ctor_release(x_715, 0);
 x_729 = x_715;
} else {
 lean_dec_ref(x_715);
 x_729 = lean_box(0);
}
x_730 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_731 = l_Lean_JsonNumber_fromNat(x_728);
if (lean_is_scalar(x_729)) {
 x_732 = lean_alloc_ctor(2, 1, 0);
} else {
 x_732 = x_729;
 lean_ctor_set_tag(x_732, 2);
}
lean_ctor_set(x_732, 0, x_731);
if (lean_is_scalar(x_723)) {
 x_733 = lean_alloc_ctor(0, 2, 0);
} else {
 x_733 = x_723;
}
lean_ctor_set(x_733, 0, x_730);
lean_ctor_set(x_733, 1, x_732);
x_734 = lean_box(0);
x_735 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_735, 0, x_733);
lean_ctor_set(x_735, 1, x_734);
x_28 = lean_box(0);
x_29 = x_724;
x_30 = x_725;
x_31 = x_726;
x_32 = x_727;
x_33 = x_722;
x_34 = x_735;
goto block_47;
}
}
else
{
lean_object* x_736; lean_object* x_737; lean_object* x_738; 
lean_inc_ref(x_713);
x_736 = lean_ctor_get(x_712, 1);
lean_inc(x_736);
lean_dec(x_712);
x_737 = lean_ctor_get(x_713, 0);
lean_inc(x_737);
lean_dec_ref(x_713);
x_738 = lp_REPL_REPL_instToJsonError_toJson(x_737);
x_3 = x_738;
x_4 = x_736;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_739; lean_object* x_740; lean_object* x_741; 
x_739 = lean_ctor_get(x_711, 0);
lean_inc(x_739);
if (lean_is_exclusive(x_711)) {
 lean_ctor_release(x_711, 0);
 x_740 = x_711;
} else {
 lean_dec_ref(x_711);
 x_740 = lean_box(0);
}
if (lean_is_scalar(x_740)) {
 x_741 = lean_alloc_ctor(1, 1, 0);
} else {
 x_741 = x_740;
}
lean_ctor_set(x_741, 0, x_739);
return x_741;
}
}
case 1:
{
lean_object* x_742; lean_object* x_743; 
x_742 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_742);
lean_dec_ref(x_709);
x_743 = lp_REPL_REPL_processFile(x_742, x_1);
lean_dec_ref(x_742);
if (lean_obj_tag(x_743) == 0)
{
lean_object* x_744; lean_object* x_745; 
x_744 = lean_ctor_get(x_743, 0);
lean_inc(x_744);
lean_dec_ref(x_743);
x_745 = lean_ctor_get(x_744, 0);
if (lean_obj_tag(x_745) == 0)
{
lean_object* x_746; lean_object* x_747; 
x_746 = lean_ctor_get(x_745, 0);
lean_inc(x_746);
x_747 = lean_ctor_get(x_746, 0);
lean_inc(x_747);
if (lean_obj_tag(x_747) == 0)
{
lean_object* x_748; lean_object* x_749; lean_object* x_750; lean_object* x_751; lean_object* x_752; lean_object* x_753; 
x_748 = lean_ctor_get(x_744, 1);
lean_inc(x_748);
lean_dec(x_744);
x_749 = lean_ctor_get(x_746, 1);
lean_inc(x_749);
x_750 = lean_ctor_get(x_746, 2);
lean_inc(x_750);
x_751 = lean_ctor_get(x_746, 3);
lean_inc(x_751);
x_752 = lean_ctor_get(x_746, 4);
lean_inc(x_752);
lean_dec(x_746);
x_753 = lean_box(0);
x_65 = x_748;
x_66 = x_749;
x_67 = x_750;
x_68 = x_751;
x_69 = x_752;
x_70 = lean_box(0);
x_71 = x_753;
goto block_84;
}
else
{
lean_object* x_754; lean_object* x_755; lean_object* x_756; lean_object* x_757; lean_object* x_758; lean_object* x_759; lean_object* x_760; lean_object* x_761; lean_object* x_762; lean_object* x_763; lean_object* x_764; lean_object* x_765; lean_object* x_766; lean_object* x_767; 
x_754 = lean_ctor_get(x_744, 1);
lean_inc(x_754);
if (lean_is_exclusive(x_744)) {
 lean_ctor_release(x_744, 0);
 lean_ctor_release(x_744, 1);
 x_755 = x_744;
} else {
 lean_dec_ref(x_744);
 x_755 = lean_box(0);
}
x_756 = lean_ctor_get(x_746, 1);
lean_inc(x_756);
x_757 = lean_ctor_get(x_746, 2);
lean_inc(x_757);
x_758 = lean_ctor_get(x_746, 3);
lean_inc(x_758);
x_759 = lean_ctor_get(x_746, 4);
lean_inc(x_759);
lean_dec(x_746);
x_760 = lean_ctor_get(x_747, 0);
lean_inc(x_760);
if (lean_is_exclusive(x_747)) {
 lean_ctor_release(x_747, 0);
 x_761 = x_747;
} else {
 lean_dec_ref(x_747);
 x_761 = lean_box(0);
}
x_762 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_763 = l_Lean_JsonNumber_fromNat(x_760);
if (lean_is_scalar(x_761)) {
 x_764 = lean_alloc_ctor(2, 1, 0);
} else {
 x_764 = x_761;
 lean_ctor_set_tag(x_764, 2);
}
lean_ctor_set(x_764, 0, x_763);
if (lean_is_scalar(x_755)) {
 x_765 = lean_alloc_ctor(0, 2, 0);
} else {
 x_765 = x_755;
}
lean_ctor_set(x_765, 0, x_762);
lean_ctor_set(x_765, 1, x_764);
x_766 = lean_box(0);
x_767 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_767, 0, x_765);
lean_ctor_set(x_767, 1, x_766);
x_65 = x_754;
x_66 = x_756;
x_67 = x_757;
x_68 = x_758;
x_69 = x_759;
x_70 = lean_box(0);
x_71 = x_767;
goto block_84;
}
}
else
{
lean_object* x_768; lean_object* x_769; lean_object* x_770; 
lean_inc_ref(x_745);
x_768 = lean_ctor_get(x_744, 1);
lean_inc(x_768);
lean_dec(x_744);
x_769 = lean_ctor_get(x_745, 0);
lean_inc(x_769);
lean_dec_ref(x_745);
x_770 = lp_REPL_REPL_instToJsonError_toJson(x_769);
x_3 = x_770;
x_4 = x_768;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_771; lean_object* x_772; lean_object* x_773; 
x_771 = lean_ctor_get(x_743, 0);
lean_inc(x_771);
if (lean_is_exclusive(x_743)) {
 lean_ctor_release(x_743, 0);
 x_772 = x_743;
} else {
 lean_dec_ref(x_743);
 x_772 = lean_box(0);
}
if (lean_is_scalar(x_772)) {
 x_773 = lean_alloc_ctor(1, 1, 0);
} else {
 x_773 = x_772;
}
lean_ctor_set(x_773, 0, x_771);
return x_773;
}
}
case 2:
{
lean_object* x_774; lean_object* x_775; 
x_774 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_774);
lean_dec_ref(x_709);
x_775 = lp_REPL_REPL_runProofStep(x_774, x_1);
if (lean_obj_tag(x_775) == 0)
{
lean_object* x_776; lean_object* x_777; 
x_776 = lean_ctor_get(x_775, 0);
lean_inc(x_776);
lean_dec_ref(x_775);
x_777 = lean_ctor_get(x_776, 0);
lean_inc(x_777);
if (lean_obj_tag(x_777) == 0)
{
lean_object* x_778; lean_object* x_779; lean_object* x_780; lean_object* x_781; lean_object* x_782; lean_object* x_783; lean_object* x_784; lean_object* x_785; lean_object* x_786; lean_object* x_787; lean_object* x_788; lean_object* x_789; lean_object* x_790; lean_object* x_791; lean_object* x_792; lean_object* x_793; lean_object* x_794; lean_object* x_795; lean_object* x_796; lean_object* x_797; lean_object* x_798; lean_object* x_799; lean_object* x_800; lean_object* x_801; lean_object* x_802; lean_object* x_803; lean_object* x_804; lean_object* x_805; lean_object* x_806; lean_object* x_807; lean_object* x_808; lean_object* x_809; lean_object* x_810; 
x_778 = lean_ctor_get(x_777, 0);
lean_inc(x_778);
if (lean_is_exclusive(x_777)) {
 lean_ctor_release(x_777, 0);
 x_779 = x_777;
} else {
 lean_dec_ref(x_777);
 x_779 = lean_box(0);
}
x_780 = lean_ctor_get(x_776, 1);
lean_inc(x_780);
if (lean_is_exclusive(x_776)) {
 lean_ctor_release(x_776, 0);
 lean_ctor_release(x_776, 1);
 x_781 = x_776;
} else {
 lean_dec_ref(x_776);
 x_781 = lean_box(0);
}
x_782 = lean_ctor_get(x_778, 0);
lean_inc(x_782);
x_783 = lean_ctor_get(x_778, 1);
lean_inc(x_783);
x_784 = lean_ctor_get(x_778, 2);
lean_inc(x_784);
x_785 = lean_ctor_get(x_778, 3);
lean_inc(x_785);
x_786 = lean_ctor_get(x_778, 4);
lean_inc(x_786);
lean_dec(x_778);
x_787 = lp_REPL_repl_loop___closed__0;
x_788 = l_Lean_JsonNumber_fromNat(x_782);
if (lean_is_scalar(x_779)) {
 x_789 = lean_alloc_ctor(2, 1, 0);
} else {
 x_789 = x_779;
 lean_ctor_set_tag(x_789, 2);
}
lean_ctor_set(x_789, 0, x_788);
if (lean_is_scalar(x_781)) {
 x_790 = lean_alloc_ctor(0, 2, 0);
} else {
 x_790 = x_781;
}
lean_ctor_set(x_790, 0, x_787);
lean_ctor_set(x_790, 1, x_789);
x_791 = lean_box(0);
x_792 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_792, 0, x_790);
lean_ctor_set(x_792, 1, x_791);
x_793 = lp_REPL_repl_loop___closed__1;
x_794 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_783);
x_795 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_795, 0, x_793);
lean_ctor_set(x_795, 1, x_794);
x_796 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_796, 0, x_795);
lean_ctor_set(x_796, 1, x_791);
x_797 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_798 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_797, x_784);
x_799 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_800 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_799, x_785);
x_801 = lp_REPL_repl_loop___closed__2;
x_802 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_801, x_786);
x_803 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_803, 0, x_802);
lean_ctor_set(x_803, 1, x_791);
x_804 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_804, 0, x_800);
lean_ctor_set(x_804, 1, x_803);
x_805 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_805, 0, x_798);
lean_ctor_set(x_805, 1, x_804);
x_806 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_806, 0, x_796);
lean_ctor_set(x_806, 1, x_805);
x_807 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_807, 0, x_792);
lean_ctor_set(x_807, 1, x_806);
x_808 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_809 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_807, x_808);
x_810 = l_Lean_Json_mkObj(x_809);
x_3 = x_810;
x_4 = x_780;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_811; lean_object* x_812; lean_object* x_813; 
x_811 = lean_ctor_get(x_776, 1);
lean_inc(x_811);
lean_dec(x_776);
x_812 = lean_ctor_get(x_777, 0);
lean_inc(x_812);
lean_dec_ref(x_777);
x_813 = lp_REPL_REPL_instToJsonError_toJson(x_812);
x_3 = x_813;
x_4 = x_811;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_814; lean_object* x_815; lean_object* x_816; 
x_814 = lean_ctor_get(x_775, 0);
lean_inc(x_814);
if (lean_is_exclusive(x_775)) {
 lean_ctor_release(x_775, 0);
 x_815 = x_775;
} else {
 lean_dec_ref(x_775);
 x_815 = lean_box(0);
}
if (lean_is_scalar(x_815)) {
 x_816 = lean_alloc_ctor(1, 1, 0);
} else {
 x_816 = x_815;
}
lean_ctor_set(x_816, 0, x_814);
return x_816;
}
}
case 3:
{
lean_object* x_817; lean_object* x_818; 
x_817 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_817);
lean_dec_ref(x_709);
x_818 = lp_REPL_REPL_pickleCommandSnapshot___at___00repl_loop_spec__9(x_817, x_1);
if (lean_obj_tag(x_818) == 0)
{
lean_object* x_819; lean_object* x_820; 
x_819 = lean_ctor_get(x_818, 0);
lean_inc(x_819);
lean_dec_ref(x_818);
x_820 = lean_ctor_get(x_819, 0);
if (lean_obj_tag(x_820) == 0)
{
lean_object* x_821; lean_object* x_822; 
x_821 = lean_ctor_get(x_820, 0);
lean_inc(x_821);
x_822 = lean_ctor_get(x_821, 0);
lean_inc(x_822);
if (lean_obj_tag(x_822) == 0)
{
lean_object* x_823; lean_object* x_824; lean_object* x_825; lean_object* x_826; lean_object* x_827; lean_object* x_828; 
x_823 = lean_ctor_get(x_819, 1);
lean_inc(x_823);
lean_dec(x_819);
x_824 = lean_ctor_get(x_821, 1);
lean_inc(x_824);
x_825 = lean_ctor_get(x_821, 2);
lean_inc(x_825);
x_826 = lean_ctor_get(x_821, 3);
lean_inc(x_826);
x_827 = lean_ctor_get(x_821, 4);
lean_inc(x_827);
lean_dec(x_821);
x_828 = lean_box(0);
x_102 = x_823;
x_103 = x_824;
x_104 = x_825;
x_105 = x_826;
x_106 = x_827;
x_107 = lean_box(0);
x_108 = x_828;
goto block_121;
}
else
{
lean_object* x_829; lean_object* x_830; lean_object* x_831; lean_object* x_832; lean_object* x_833; lean_object* x_834; lean_object* x_835; lean_object* x_836; lean_object* x_837; lean_object* x_838; lean_object* x_839; lean_object* x_840; lean_object* x_841; lean_object* x_842; 
x_829 = lean_ctor_get(x_819, 1);
lean_inc(x_829);
if (lean_is_exclusive(x_819)) {
 lean_ctor_release(x_819, 0);
 lean_ctor_release(x_819, 1);
 x_830 = x_819;
} else {
 lean_dec_ref(x_819);
 x_830 = lean_box(0);
}
x_831 = lean_ctor_get(x_821, 1);
lean_inc(x_831);
x_832 = lean_ctor_get(x_821, 2);
lean_inc(x_832);
x_833 = lean_ctor_get(x_821, 3);
lean_inc(x_833);
x_834 = lean_ctor_get(x_821, 4);
lean_inc(x_834);
lean_dec(x_821);
x_835 = lean_ctor_get(x_822, 0);
lean_inc(x_835);
if (lean_is_exclusive(x_822)) {
 lean_ctor_release(x_822, 0);
 x_836 = x_822;
} else {
 lean_dec_ref(x_822);
 x_836 = lean_box(0);
}
x_837 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_838 = l_Lean_JsonNumber_fromNat(x_835);
if (lean_is_scalar(x_836)) {
 x_839 = lean_alloc_ctor(2, 1, 0);
} else {
 x_839 = x_836;
 lean_ctor_set_tag(x_839, 2);
}
lean_ctor_set(x_839, 0, x_838);
if (lean_is_scalar(x_830)) {
 x_840 = lean_alloc_ctor(0, 2, 0);
} else {
 x_840 = x_830;
}
lean_ctor_set(x_840, 0, x_837);
lean_ctor_set(x_840, 1, x_839);
x_841 = lean_box(0);
x_842 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_842, 0, x_840);
lean_ctor_set(x_842, 1, x_841);
x_102 = x_829;
x_103 = x_831;
x_104 = x_832;
x_105 = x_833;
x_106 = x_834;
x_107 = lean_box(0);
x_108 = x_842;
goto block_121;
}
}
else
{
lean_object* x_843; lean_object* x_844; lean_object* x_845; 
lean_inc_ref(x_820);
x_843 = lean_ctor_get(x_819, 1);
lean_inc(x_843);
lean_dec(x_819);
x_844 = lean_ctor_get(x_820, 0);
lean_inc(x_844);
lean_dec_ref(x_820);
x_845 = lp_REPL_REPL_instToJsonError_toJson(x_844);
x_3 = x_845;
x_4 = x_843;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_846; lean_object* x_847; lean_object* x_848; 
x_846 = lean_ctor_get(x_818, 0);
lean_inc(x_846);
if (lean_is_exclusive(x_818)) {
 lean_ctor_release(x_818, 0);
 x_847 = x_818;
} else {
 lean_dec_ref(x_818);
 x_847 = lean_box(0);
}
if (lean_is_scalar(x_847)) {
 x_848 = lean_alloc_ctor(1, 1, 0);
} else {
 x_848 = x_847;
}
lean_ctor_set(x_848, 0, x_846);
return x_848;
}
}
case 4:
{
lean_object* x_849; lean_object* x_850; 
x_849 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_849);
lean_dec_ref(x_709);
x_850 = lp_REPL_REPL_unpickleCommandSnapshot(x_849, x_1);
if (lean_obj_tag(x_850) == 0)
{
lean_object* x_851; lean_object* x_852; lean_object* x_853; 
x_851 = lean_ctor_get(x_850, 0);
lean_inc(x_851);
lean_dec_ref(x_850);
x_852 = lean_ctor_get(x_851, 0);
lean_inc(x_852);
x_853 = lean_ctor_get(x_852, 0);
lean_inc(x_853);
if (lean_obj_tag(x_853) == 0)
{
lean_object* x_854; lean_object* x_855; lean_object* x_856; lean_object* x_857; lean_object* x_858; lean_object* x_859; 
x_854 = lean_ctor_get(x_851, 1);
lean_inc(x_854);
lean_dec(x_851);
x_855 = lean_ctor_get(x_852, 1);
lean_inc(x_855);
x_856 = lean_ctor_get(x_852, 2);
lean_inc(x_856);
x_857 = lean_ctor_get(x_852, 3);
lean_inc(x_857);
x_858 = lean_ctor_get(x_852, 4);
lean_inc(x_858);
lean_dec(x_852);
x_859 = lean_box(0);
x_139 = lean_box(0);
x_140 = x_854;
x_141 = x_855;
x_142 = x_856;
x_143 = x_857;
x_144 = x_858;
x_145 = x_859;
goto block_158;
}
else
{
lean_object* x_860; lean_object* x_861; lean_object* x_862; lean_object* x_863; lean_object* x_864; lean_object* x_865; lean_object* x_866; lean_object* x_867; lean_object* x_868; lean_object* x_869; lean_object* x_870; lean_object* x_871; lean_object* x_872; lean_object* x_873; 
x_860 = lean_ctor_get(x_851, 1);
lean_inc(x_860);
if (lean_is_exclusive(x_851)) {
 lean_ctor_release(x_851, 0);
 lean_ctor_release(x_851, 1);
 x_861 = x_851;
} else {
 lean_dec_ref(x_851);
 x_861 = lean_box(0);
}
x_862 = lean_ctor_get(x_852, 1);
lean_inc(x_862);
x_863 = lean_ctor_get(x_852, 2);
lean_inc(x_863);
x_864 = lean_ctor_get(x_852, 3);
lean_inc(x_864);
x_865 = lean_ctor_get(x_852, 4);
lean_inc(x_865);
lean_dec(x_852);
x_866 = lean_ctor_get(x_853, 0);
lean_inc(x_866);
if (lean_is_exclusive(x_853)) {
 lean_ctor_release(x_853, 0);
 x_867 = x_853;
} else {
 lean_dec_ref(x_853);
 x_867 = lean_box(0);
}
x_868 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3;
x_869 = l_Lean_JsonNumber_fromNat(x_866);
if (lean_is_scalar(x_867)) {
 x_870 = lean_alloc_ctor(2, 1, 0);
} else {
 x_870 = x_867;
 lean_ctor_set_tag(x_870, 2);
}
lean_ctor_set(x_870, 0, x_869);
if (lean_is_scalar(x_861)) {
 x_871 = lean_alloc_ctor(0, 2, 0);
} else {
 x_871 = x_861;
}
lean_ctor_set(x_871, 0, x_868);
lean_ctor_set(x_871, 1, x_870);
x_872 = lean_box(0);
x_873 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_873, 0, x_871);
lean_ctor_set(x_873, 1, x_872);
x_139 = lean_box(0);
x_140 = x_860;
x_141 = x_862;
x_142 = x_863;
x_143 = x_864;
x_144 = x_865;
x_145 = x_873;
goto block_158;
}
}
else
{
lean_object* x_874; lean_object* x_875; lean_object* x_876; 
x_874 = lean_ctor_get(x_850, 0);
lean_inc(x_874);
if (lean_is_exclusive(x_850)) {
 lean_ctor_release(x_850, 0);
 x_875 = x_850;
} else {
 lean_dec_ref(x_850);
 x_875 = lean_box(0);
}
if (lean_is_scalar(x_875)) {
 x_876 = lean_alloc_ctor(1, 1, 0);
} else {
 x_876 = x_875;
}
lean_ctor_set(x_876, 0, x_874);
return x_876;
}
}
case 5:
{
lean_object* x_877; lean_object* x_878; 
x_877 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_877);
lean_dec_ref(x_709);
x_878 = lp_REPL_REPL_pickleProofSnapshot___at___00repl_loop_spec__10(x_877, x_1);
if (lean_obj_tag(x_878) == 0)
{
lean_object* x_879; lean_object* x_880; 
x_879 = lean_ctor_get(x_878, 0);
lean_inc(x_879);
lean_dec_ref(x_878);
x_880 = lean_ctor_get(x_879, 0);
lean_inc(x_880);
if (lean_obj_tag(x_880) == 0)
{
lean_object* x_881; lean_object* x_882; lean_object* x_883; lean_object* x_884; lean_object* x_885; lean_object* x_886; lean_object* x_887; lean_object* x_888; lean_object* x_889; lean_object* x_890; lean_object* x_891; lean_object* x_892; lean_object* x_893; lean_object* x_894; lean_object* x_895; lean_object* x_896; lean_object* x_897; lean_object* x_898; lean_object* x_899; lean_object* x_900; lean_object* x_901; lean_object* x_902; lean_object* x_903; lean_object* x_904; lean_object* x_905; lean_object* x_906; lean_object* x_907; lean_object* x_908; lean_object* x_909; lean_object* x_910; lean_object* x_911; lean_object* x_912; lean_object* x_913; 
x_881 = lean_ctor_get(x_880, 0);
lean_inc(x_881);
if (lean_is_exclusive(x_880)) {
 lean_ctor_release(x_880, 0);
 x_882 = x_880;
} else {
 lean_dec_ref(x_880);
 x_882 = lean_box(0);
}
x_883 = lean_ctor_get(x_879, 1);
lean_inc(x_883);
if (lean_is_exclusive(x_879)) {
 lean_ctor_release(x_879, 0);
 lean_ctor_release(x_879, 1);
 x_884 = x_879;
} else {
 lean_dec_ref(x_879);
 x_884 = lean_box(0);
}
x_885 = lean_ctor_get(x_881, 0);
lean_inc(x_885);
x_886 = lean_ctor_get(x_881, 1);
lean_inc(x_886);
x_887 = lean_ctor_get(x_881, 2);
lean_inc(x_887);
x_888 = lean_ctor_get(x_881, 3);
lean_inc(x_888);
x_889 = lean_ctor_get(x_881, 4);
lean_inc(x_889);
lean_dec(x_881);
x_890 = lp_REPL_repl_loop___closed__0;
x_891 = l_Lean_JsonNumber_fromNat(x_885);
if (lean_is_scalar(x_882)) {
 x_892 = lean_alloc_ctor(2, 1, 0);
} else {
 x_892 = x_882;
 lean_ctor_set_tag(x_892, 2);
}
lean_ctor_set(x_892, 0, x_891);
if (lean_is_scalar(x_884)) {
 x_893 = lean_alloc_ctor(0, 2, 0);
} else {
 x_893 = x_884;
}
lean_ctor_set(x_893, 0, x_890);
lean_ctor_set(x_893, 1, x_892);
x_894 = lean_box(0);
x_895 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_895, 0, x_893);
lean_ctor_set(x_895, 1, x_894);
x_896 = lp_REPL_repl_loop___closed__1;
x_897 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_886);
x_898 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_898, 0, x_896);
lean_ctor_set(x_898, 1, x_897);
x_899 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_899, 0, x_898);
lean_ctor_set(x_899, 1, x_894);
x_900 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_901 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_900, x_887);
x_902 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_903 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_902, x_888);
x_904 = lp_REPL_repl_loop___closed__2;
x_905 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_904, x_889);
x_906 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_906, 0, x_905);
lean_ctor_set(x_906, 1, x_894);
x_907 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_907, 0, x_903);
lean_ctor_set(x_907, 1, x_906);
x_908 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_908, 0, x_901);
lean_ctor_set(x_908, 1, x_907);
x_909 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_909, 0, x_899);
lean_ctor_set(x_909, 1, x_908);
x_910 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_910, 0, x_895);
lean_ctor_set(x_910, 1, x_909);
x_911 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_912 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_910, x_911);
x_913 = l_Lean_Json_mkObj(x_912);
x_3 = x_913;
x_4 = x_883;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_914; lean_object* x_915; lean_object* x_916; 
x_914 = lean_ctor_get(x_879, 1);
lean_inc(x_914);
lean_dec(x_879);
x_915 = lean_ctor_get(x_880, 0);
lean_inc(x_915);
lean_dec_ref(x_880);
x_916 = lp_REPL_REPL_instToJsonError_toJson(x_915);
x_3 = x_916;
x_4 = x_914;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_917; lean_object* x_918; lean_object* x_919; 
x_917 = lean_ctor_get(x_878, 0);
lean_inc(x_917);
if (lean_is_exclusive(x_878)) {
 lean_ctor_release(x_878, 0);
 x_918 = x_878;
} else {
 lean_dec_ref(x_878);
 x_918 = lean_box(0);
}
if (lean_is_scalar(x_918)) {
 x_919 = lean_alloc_ctor(1, 1, 0);
} else {
 x_919 = x_918;
}
lean_ctor_set(x_919, 0, x_917);
return x_919;
}
}
case 6:
{
lean_object* x_920; lean_object* x_921; 
x_920 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_920);
lean_dec_ref(x_709);
x_921 = lp_REPL_REPL_unpickleProofSnapshot(x_920, x_1);
if (lean_obj_tag(x_921) == 0)
{
lean_object* x_922; lean_object* x_923; 
x_922 = lean_ctor_get(x_921, 0);
lean_inc(x_922);
lean_dec_ref(x_921);
x_923 = lean_ctor_get(x_922, 0);
lean_inc(x_923);
if (lean_obj_tag(x_923) == 0)
{
lean_object* x_924; lean_object* x_925; lean_object* x_926; lean_object* x_927; lean_object* x_928; lean_object* x_929; lean_object* x_930; lean_object* x_931; lean_object* x_932; lean_object* x_933; lean_object* x_934; lean_object* x_935; lean_object* x_936; lean_object* x_937; lean_object* x_938; lean_object* x_939; lean_object* x_940; lean_object* x_941; lean_object* x_942; lean_object* x_943; lean_object* x_944; lean_object* x_945; lean_object* x_946; lean_object* x_947; lean_object* x_948; lean_object* x_949; lean_object* x_950; lean_object* x_951; lean_object* x_952; lean_object* x_953; lean_object* x_954; lean_object* x_955; lean_object* x_956; 
x_924 = lean_ctor_get(x_923, 0);
lean_inc(x_924);
if (lean_is_exclusive(x_923)) {
 lean_ctor_release(x_923, 0);
 x_925 = x_923;
} else {
 lean_dec_ref(x_923);
 x_925 = lean_box(0);
}
x_926 = lean_ctor_get(x_922, 1);
lean_inc(x_926);
if (lean_is_exclusive(x_922)) {
 lean_ctor_release(x_922, 0);
 lean_ctor_release(x_922, 1);
 x_927 = x_922;
} else {
 lean_dec_ref(x_922);
 x_927 = lean_box(0);
}
x_928 = lean_ctor_get(x_924, 0);
lean_inc(x_928);
x_929 = lean_ctor_get(x_924, 1);
lean_inc(x_929);
x_930 = lean_ctor_get(x_924, 2);
lean_inc(x_930);
x_931 = lean_ctor_get(x_924, 3);
lean_inc(x_931);
x_932 = lean_ctor_get(x_924, 4);
lean_inc(x_932);
lean_dec(x_924);
x_933 = lp_REPL_repl_loop___closed__0;
x_934 = l_Lean_JsonNumber_fromNat(x_928);
if (lean_is_scalar(x_925)) {
 x_935 = lean_alloc_ctor(2, 1, 0);
} else {
 x_935 = x_925;
 lean_ctor_set_tag(x_935, 2);
}
lean_ctor_set(x_935, 0, x_934);
if (lean_is_scalar(x_927)) {
 x_936 = lean_alloc_ctor(0, 2, 0);
} else {
 x_936 = x_927;
}
lean_ctor_set(x_936, 0, x_933);
lean_ctor_set(x_936, 1, x_935);
x_937 = lean_box(0);
x_938 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_938, 0, x_936);
lean_ctor_set(x_938, 1, x_937);
x_939 = lp_REPL_repl_loop___closed__1;
x_940 = lp_REPL_List_toJson___at___00Lean_Elab_TacticInfo_instToJsonJson_toJson_spec__1(x_929);
x_941 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_941, 0, x_939);
lean_ctor_set(x_941, 1, x_940);
x_942 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_942, 0, x_941);
lean_ctor_set(x_942, 1, x_937);
x_943 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_944 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_943, x_930);
x_945 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_946 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_945, x_931);
x_947 = lp_REPL_repl_loop___closed__2;
x_948 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__8(x_947, x_932);
x_949 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_949, 0, x_948);
lean_ctor_set(x_949, 1, x_937);
x_950 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_950, 0, x_946);
lean_ctor_set(x_950, 1, x_949);
x_951 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_951, 0, x_944);
lean_ctor_set(x_951, 1, x_950);
x_952 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_952, 0, x_942);
lean_ctor_set(x_952, 1, x_951);
x_953 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_953, 0, x_938);
lean_ctor_set(x_953, 1, x_952);
x_954 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_955 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_953, x_954);
x_956 = l_Lean_Json_mkObj(x_955);
x_3 = x_956;
x_4 = x_926;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_957; lean_object* x_958; lean_object* x_959; 
x_957 = lean_ctor_get(x_922, 1);
lean_inc(x_957);
lean_dec(x_922);
x_958 = lean_ctor_get(x_923, 0);
lean_inc(x_958);
lean_dec_ref(x_923);
x_959 = lp_REPL_REPL_instToJsonError_toJson(x_958);
x_3 = x_959;
x_4 = x_957;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_960; lean_object* x_961; lean_object* x_962; 
x_960 = lean_ctor_get(x_921, 0);
lean_inc(x_960);
if (lean_is_exclusive(x_921)) {
 lean_ctor_release(x_921, 0);
 x_961 = x_921;
} else {
 lean_dec_ref(x_921);
 x_961 = lean_box(0);
}
if (lean_is_scalar(x_961)) {
 x_962 = lean_alloc_ctor(1, 1, 0);
} else {
 x_962 = x_961;
}
lean_ctor_set(x_962, 0, x_960);
return x_962;
}
}
default: 
{
lean_object* x_963; lean_object* x_964; 
x_963 = lean_ctor_get(x_709, 0);
lean_inc_ref(x_963);
lean_dec_ref(x_709);
x_964 = lp_REPL_REPL_runBatchVerify(x_963, x_1);
if (lean_obj_tag(x_964) == 0)
{
lean_object* x_965; lean_object* x_966; 
x_965 = lean_ctor_get(x_964, 0);
lean_inc(x_965);
lean_dec_ref(x_964);
x_966 = lean_ctor_get(x_965, 0);
lean_inc(x_966);
if (lean_obj_tag(x_966) == 0)
{
lean_object* x_967; lean_object* x_968; lean_object* x_969; 
x_967 = lean_ctor_get(x_965, 1);
lean_inc(x_967);
lean_dec(x_965);
x_968 = lean_ctor_get(x_966, 0);
lean_inc(x_968);
lean_dec_ref(x_966);
x_969 = lp_REPL_Array_toJson___at___00repl_loop_spec__11(x_968);
x_3 = x_969;
x_4 = x_967;
x_5 = lean_box(0);
goto block_10;
}
else
{
lean_object* x_970; lean_object* x_971; lean_object* x_972; 
x_970 = lean_ctor_get(x_965, 1);
lean_inc(x_970);
lean_dec(x_965);
x_971 = lean_ctor_get(x_966, 0);
lean_inc(x_971);
lean_dec_ref(x_966);
x_972 = lp_REPL_REPL_instToJsonError_toJson(x_971);
x_3 = x_972;
x_4 = x_970;
x_5 = lean_box(0);
goto block_10;
}
}
else
{
lean_object* x_973; lean_object* x_974; lean_object* x_975; 
x_973 = lean_ctor_get(x_964, 0);
lean_inc(x_973);
if (lean_is_exclusive(x_964)) {
 lean_ctor_release(x_964, 0);
 x_974 = x_964;
} else {
 lean_dec_ref(x_964);
 x_974 = lean_box(0);
}
if (lean_is_scalar(x_974)) {
 x_975 = lean_alloc_ctor(1, 1, 0);
} else {
 x_975 = x_974;
}
lean_ctor_set(x_975, 0, x_973);
return x_975;
}
}
}
}
else
{
lean_object* x_976; lean_object* x_977; lean_object* x_978; 
lean_dec_ref(x_1);
x_976 = lean_ctor_get(x_708, 0);
lean_inc(x_976);
if (lean_is_exclusive(x_708)) {
 lean_ctor_release(x_708, 0);
 x_977 = x_708;
} else {
 lean_dec_ref(x_708);
 x_977 = lean_box(0);
}
if (lean_is_scalar(x_977)) {
 x_978 = lean_alloc_ctor(1, 1, 0);
} else {
 x_978 = x_977;
}
lean_ctor_set(x_978, 0, x_976);
return x_978;
}
}
block_987:
{
lean_object* x_980; lean_object* x_981; lean_object* x_982; uint8_t x_983; 
x_980 = lp_REPL_repl_loop___closed__3;
x_981 = lean_string_utf8_byte_size(x_707);
x_982 = lp_REPL_repl_loop___closed__4;
x_983 = lean_nat_dec_le(x_982, x_981);
if (x_983 == 0)
{
goto block_979;
}
else
{
lean_object* x_984; uint8_t x_985; 
x_984 = lean_unsigned_to_nat(0u);
x_985 = lean_string_memcmp(x_707, x_980, x_984, x_984, x_982);
if (x_985 == 0)
{
goto block_979;
}
else
{
lean_dec(x_707);
goto _start;
}
}
}
}
}
else
{
uint8_t x_999; 
lean_dec_ref(x_1);
x_999 = !lean_is_exclusive(x_159);
if (x_999 == 0)
{
return x_159;
}
else
{
lean_object* x_1000; lean_object* x_1001; 
x_1000 = lean_ctor_get(x_159, 0);
lean_inc(x_1000);
lean_dec(x_159);
x_1001 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_1001, 0, x_1000);
return x_1001;
}
}
block_10:
{
lean_object* x_6; 
x_6 = lp_REPL_IO_println___at___00repl_loop_spec__0(x_3);
if (lean_obj_tag(x_6) == 0)
{
lean_object* x_7; lean_object* x_8; 
lean_dec_ref(x_6);
x_7 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_8 = lp_REPL_printFlush___at___00repl_loop_spec__1(x_7);
if (lean_obj_tag(x_8) == 0)
{
lean_dec_ref(x_8);
x_1 = x_4;
goto _start;
}
else
{
lean_dec_ref(x_4);
return x_8;
}
}
else
{
lean_dec_ref(x_4);
return x_6;
}
}
block_27:
{
lean_object* x_18; lean_object* x_19; lean_object* x_20; lean_object* x_21; lean_object* x_22; lean_object* x_23; lean_object* x_24; lean_object* x_25; lean_object* x_26; 
x_18 = lean_box(0);
x_19 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_19, 0, x_17);
lean_ctor_set(x_19, 1, x_18);
x_20 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_20, 0, x_13);
lean_ctor_set(x_20, 1, x_19);
x_21 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_21, 0, x_14);
lean_ctor_set(x_21, 1, x_20);
x_22 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_22, 0, x_16);
lean_ctor_set(x_22, 1, x_21);
x_23 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_23, 0, x_12);
lean_ctor_set(x_23, 1, x_22);
x_24 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_25 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_23, x_24);
x_26 = l_Lean_Json_mkObj(x_25);
x_3 = x_26;
x_4 = x_15;
x_5 = lean_box(0);
goto block_10;
}
block_47:
{
lean_object* x_35; lean_object* x_36; lean_object* x_37; lean_object* x_38; lean_object* x_39; lean_object* x_40; 
x_35 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_36 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_35, x_29);
x_37 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_38 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_37, x_30);
x_39 = lp_REPL_REPL_runCommandGCAux___closed__7;
x_40 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(x_39, x_31);
if (lean_obj_tag(x_32) == 0)
{
lean_object* x_41; 
x_41 = lean_box(0);
x_11 = lean_box(0);
x_12 = x_34;
x_13 = x_40;
x_14 = x_38;
x_15 = x_33;
x_16 = x_36;
x_17 = x_41;
goto block_27;
}
else
{
lean_object* x_42; lean_object* x_43; lean_object* x_44; lean_object* x_45; lean_object* x_46; 
x_42 = lean_ctor_get(x_32, 0);
lean_inc(x_42);
lean_dec_ref(x_32);
x_43 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2;
x_44 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_44, 0, x_43);
lean_ctor_set(x_44, 1, x_42);
x_45 = lean_box(0);
x_46 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_46, 0, x_44);
lean_ctor_set(x_46, 1, x_45);
x_11 = lean_box(0);
x_12 = x_34;
x_13 = x_40;
x_14 = x_38;
x_15 = x_33;
x_16 = x_36;
x_17 = x_46;
goto block_27;
}
}
block_64:
{
lean_object* x_55; lean_object* x_56; lean_object* x_57; lean_object* x_58; lean_object* x_59; lean_object* x_60; lean_object* x_61; lean_object* x_62; lean_object* x_63; 
x_55 = lean_box(0);
x_56 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_56, 0, x_54);
lean_ctor_set(x_56, 1, x_55);
x_57 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_57, 0, x_49);
lean_ctor_set(x_57, 1, x_56);
x_58 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_58, 0, x_48);
lean_ctor_set(x_58, 1, x_57);
x_59 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_59, 0, x_53);
lean_ctor_set(x_59, 1, x_58);
x_60 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_60, 0, x_52);
lean_ctor_set(x_60, 1, x_59);
x_61 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_62 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_60, x_61);
x_63 = l_Lean_Json_mkObj(x_62);
x_3 = x_63;
x_4 = x_50;
x_5 = lean_box(0);
goto block_10;
}
block_84:
{
lean_object* x_72; lean_object* x_73; lean_object* x_74; lean_object* x_75; lean_object* x_76; lean_object* x_77; 
x_72 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_73 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_72, x_66);
x_74 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_75 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_74, x_67);
x_76 = lp_REPL_REPL_runCommandGCAux___closed__7;
x_77 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(x_76, x_68);
if (lean_obj_tag(x_69) == 0)
{
lean_object* x_78; 
x_78 = lean_box(0);
x_48 = x_75;
x_49 = x_77;
x_50 = x_65;
x_51 = lean_box(0);
x_52 = x_71;
x_53 = x_73;
x_54 = x_78;
goto block_64;
}
else
{
lean_object* x_79; lean_object* x_80; lean_object* x_81; lean_object* x_82; lean_object* x_83; 
x_79 = lean_ctor_get(x_69, 0);
lean_inc(x_79);
lean_dec_ref(x_69);
x_80 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2;
x_81 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_81, 0, x_80);
lean_ctor_set(x_81, 1, x_79);
x_82 = lean_box(0);
x_83 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_83, 0, x_81);
lean_ctor_set(x_83, 1, x_82);
x_48 = x_75;
x_49 = x_77;
x_50 = x_65;
x_51 = lean_box(0);
x_52 = x_71;
x_53 = x_73;
x_54 = x_83;
goto block_64;
}
}
block_101:
{
lean_object* x_92; lean_object* x_93; lean_object* x_94; lean_object* x_95; lean_object* x_96; lean_object* x_97; lean_object* x_98; lean_object* x_99; lean_object* x_100; 
x_92 = lean_box(0);
x_93 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_93, 0, x_91);
lean_ctor_set(x_93, 1, x_92);
x_94 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_94, 0, x_86);
lean_ctor_set(x_94, 1, x_93);
x_95 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_95, 0, x_87);
lean_ctor_set(x_95, 1, x_94);
x_96 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_96, 0, x_90);
lean_ctor_set(x_96, 1, x_95);
x_97 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_97, 0, x_88);
lean_ctor_set(x_97, 1, x_96);
x_98 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_99 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_97, x_98);
x_100 = l_Lean_Json_mkObj(x_99);
x_3 = x_100;
x_4 = x_85;
x_5 = lean_box(0);
goto block_10;
}
block_121:
{
lean_object* x_109; lean_object* x_110; lean_object* x_111; lean_object* x_112; lean_object* x_113; lean_object* x_114; 
x_109 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_110 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_109, x_103);
x_111 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_112 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_111, x_104);
x_113 = lp_REPL_REPL_runCommandGCAux___closed__7;
x_114 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(x_113, x_105);
if (lean_obj_tag(x_106) == 0)
{
lean_object* x_115; 
x_115 = lean_box(0);
x_85 = x_102;
x_86 = x_114;
x_87 = x_112;
x_88 = x_108;
x_89 = lean_box(0);
x_90 = x_110;
x_91 = x_115;
goto block_101;
}
else
{
lean_object* x_116; lean_object* x_117; lean_object* x_118; lean_object* x_119; lean_object* x_120; 
x_116 = lean_ctor_get(x_106, 0);
lean_inc(x_116);
lean_dec_ref(x_106);
x_117 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2;
x_118 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_118, 0, x_117);
lean_ctor_set(x_118, 1, x_116);
x_119 = lean_box(0);
x_120 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_120, 0, x_118);
lean_ctor_set(x_120, 1, x_119);
x_85 = x_102;
x_86 = x_114;
x_87 = x_112;
x_88 = x_108;
x_89 = lean_box(0);
x_90 = x_110;
x_91 = x_120;
goto block_101;
}
}
block_138:
{
lean_object* x_129; lean_object* x_130; lean_object* x_131; lean_object* x_132; lean_object* x_133; lean_object* x_134; lean_object* x_135; lean_object* x_136; lean_object* x_137; 
x_129 = lean_box(0);
x_130 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_130, 0, x_128);
lean_ctor_set(x_130, 1, x_129);
x_131 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_131, 0, x_122);
lean_ctor_set(x_131, 1, x_130);
x_132 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_132, 0, x_126);
lean_ctor_set(x_132, 1, x_131);
x_133 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_133, 0, x_123);
lean_ctor_set(x_133, 1, x_132);
x_134 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_134, 0, x_127);
lean_ctor_set(x_134, 1, x_133);
x_135 = lp_REPL_instToJsonBatch_toJson___closed__0;
x_136 = l___private_Init_Data_List_Impl_0__List_flatMapTR_go___at___00Lean_Server_Test_Runner_Client_instToJsonSubexprInfo_toJson_spec__1(x_134, x_135);
x_137 = l_Lean_Json_mkObj(x_136);
x_3 = x_137;
x_4 = x_125;
x_5 = lean_box(0);
goto block_10;
}
block_158:
{
lean_object* x_146; lean_object* x_147; lean_object* x_148; lean_object* x_149; lean_object* x_150; lean_object* x_151; 
x_146 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0;
x_147 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__2(x_146, x_141);
x_148 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1;
x_149 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__3(x_148, x_142);
x_150 = lp_REPL_REPL_runCommandGCAux___closed__7;
x_151 = lp_REPL_REPL_Json_nonemptyList___at___00repl_loop_spec__4(x_150, x_143);
if (lean_obj_tag(x_144) == 0)
{
lean_object* x_152; 
x_152 = lean_box(0);
x_122 = x_151;
x_123 = x_147;
x_124 = lean_box(0);
x_125 = x_140;
x_126 = x_149;
x_127 = x_145;
x_128 = x_152;
goto block_138;
}
else
{
lean_object* x_153; lean_object* x_154; lean_object* x_155; lean_object* x_156; lean_object* x_157; 
x_153 = lean_ctor_get(x_144, 0);
lean_inc(x_153);
lean_dec_ref(x_144);
x_154 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2;
x_155 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_155, 0, x_154);
lean_ctor_set(x_155, 1, x_153);
x_156 = lean_box(0);
x_157 = lean_alloc_ctor(1, 2, 0);
lean_ctor_set(x_157, 0, x_155);
lean_ctor_set(x_157, 1, x_156);
x_122 = x_151;
x_123 = x_147;
x_124 = lean_box(0);
x_125 = x_140;
x_126 = x_149;
x_127 = x_145;
x_128 = x_157;
goto block_138;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_IO_println___at___00repl_loop_spec__0___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_IO_println___at___00repl_loop_spec__0(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_printFlush___at___00repl_loop_spec__1___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_printFlush___at___00repl_loop_spec__1(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4_spec__4___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
size_t x_4; size_t x_5; lean_object* x_6; 
x_4 = lean_unbox_usize(x_1);
lean_dec(x_1);
x_5 = lean_unbox_usize(x_2);
lean_dec(x_2);
x_6 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00List_toJson___at___00REPL_Json_nonemptyList___at___00repl_loop_spec__4_spec__4_spec__4_spec__4(x_4, x_5, x_3);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleCommandSnapshot___at___00repl_loop_spec__9___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_pickleCommandSnapshot___at___00repl_loop_spec__9(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL_REPL_pickleProofSnapshot___at___00repl_loop_spec__10___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
lean_object* x_4; 
x_4 = lp_REPL_REPL_pickleProofSnapshot___at___00repl_loop_spec__10(x_1, x_2);
return x_4;
}
}
LEAN_EXPORT lean_object* lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
size_t x_4; size_t x_5; lean_object* x_6; 
x_4 = lean_unbox_usize(x_1);
lean_dec(x_1);
x_5 = lean_unbox_usize(x_2);
lean_dec(x_2);
x_6 = lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11(x_4, x_5, x_3);
return x_6;
}
}
LEAN_EXPORT lean_object* lp_REPL_repl_loop___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = lp_REPL_repl_loop(x_1);
return x_3;
}
}
static lean_object* _init_lp_REPL_repl___closed__0() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lean_unsigned_to_nat(0u);
x_2 = lean_mk_empty_array_with_capacity(x_1);
return x_2;
}
}
static lean_object* _init_lp_REPL_repl___closed__1() {
_start:
{
lean_object* x_1; lean_object* x_2; 
x_1 = lp_REPL_repl___closed__0;
x_2 = lean_alloc_ctor(0, 2, 0);
lean_ctor_set(x_2, 0, x_1);
lean_ctor_set(x_2, 1, x_1);
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_repl() {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lp_REPL_repl___closed__1;
x_3 = lp_REPL_repl_loop(x_2);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_repl___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_REPL_repl();
return x_2;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg(lean_object* x_1, lean_object* x_2, lean_object* x_3) {
_start:
{
if (lean_obj_tag(x_2) == 0)
{
lean_object* x_5; 
x_5 = lean_alloc_ctor(0, 1, 0);
lean_ctor_set(x_5, 0, x_3);
return x_5;
}
else
{
lean_object* x_6; lean_object* x_7; lean_object* x_8; lean_object* x_9; uint8_t x_10; 
x_6 = lean_ctor_get(x_2, 0);
lean_inc(x_6);
x_7 = lean_ctor_get(x_2, 1);
lean_inc(x_7);
lean_dec_ref(x_2);
x_8 = lean_string_utf8_byte_size(x_6);
x_9 = lean_unsigned_to_nat(0u);
x_10 = lean_nat_dec_eq(x_8, x_9);
if (x_10 == 0)
{
lean_object* x_11; 
x_11 = lean_load_dynlib(x_6);
if (lean_obj_tag(x_11) == 0)
{
lean_dec_ref(x_11);
{
lean_object* _tmp_1 = x_7;
lean_object* _tmp_2 = x_1;
x_2 = _tmp_1;
x_3 = _tmp_2;
}
goto _start;
}
else
{
lean_dec(x_7);
return x_11;
}
}
else
{
lean_dec(x_6);
{
lean_object* _tmp_1 = x_7;
lean_object* _tmp_2 = x_1;
x_2 = _tmp_1;
x_3 = _tmp_2;
}
goto _start;
}
}
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5) {
_start:
{
lean_object* x_7; 
x_7 = lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg(x_1, x_3, x_4);
return x_7;
}
}
static lean_object* _init_lp_REPL_main___redArg___closed__0() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("lean", 4, 4);
return x_1;
}
}
static lean_object* _init_lp_REPL_main___redArg___closed__1() {
_start:
{
lean_object* x_1; 
x_1 = lean_mk_string_unchecked("LEAN_SERVER_NATIVE_DYNLIB", 25, 25);
return x_1;
}
}
LEAN_EXPORT lean_object* lp_REPL_main___redArg() {
_start:
{
lean_object* x_2; lean_object* x_3; 
x_2 = lp_REPL_main___redArg___closed__0;
x_3 = l_Lean_findSysroot(x_2);
if (lean_obj_tag(x_3) == 0)
{
lean_object* x_4; lean_object* x_5; lean_object* x_6; 
x_4 = lean_ctor_get(x_3, 0);
lean_inc(x_4);
lean_dec_ref(x_3);
x_5 = lean_box(0);
x_6 = l_Lean_initSearchPath(x_4, x_5);
if (lean_obj_tag(x_6) == 0)
{
lean_object* x_7; lean_object* x_8; 
lean_dec_ref(x_6);
x_7 = lp_REPL_main___redArg___closed__1;
x_8 = lean_io_getenv(x_7);
if (lean_obj_tag(x_8) == 1)
{
lean_object* x_9; lean_object* x_10; 
x_9 = lean_ctor_get(x_8, 0);
lean_inc(x_9);
lean_dec_ref(x_8);
x_10 = l_IO_FS_readFile(x_9);
lean_dec(x_9);
if (lean_obj_tag(x_10) == 0)
{
lean_object* x_11; lean_object* x_12; lean_object* x_13; lean_object* x_14; lean_object* x_15; lean_object* x_16; 
x_11 = lean_ctor_get(x_10, 0);
lean_inc(x_11);
lean_dec_ref(x_10);
x_12 = lp_REPL_REPL_sorries___redArg___lam__6___closed__0;
x_13 = lean_unsigned_to_nat(0u);
x_14 = l_String_splitOnAux(x_11, x_12, x_13, x_13, x_13, x_5);
lean_dec(x_11);
x_15 = lean_box(0);
x_16 = lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg(x_15, x_14, x_15);
if (lean_obj_tag(x_16) == 0)
{
lean_object* x_17; 
lean_dec_ref(x_16);
x_17 = lp_REPL_repl();
return x_17;
}
else
{
return x_16;
}
}
else
{
uint8_t x_18; 
x_18 = !lean_is_exclusive(x_10);
if (x_18 == 0)
{
return x_10;
}
else
{
lean_object* x_19; lean_object* x_20; 
x_19 = lean_ctor_get(x_10, 0);
lean_inc(x_19);
lean_dec(x_10);
x_20 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_20, 0, x_19);
return x_20;
}
}
}
else
{
lean_object* x_21; 
lean_dec(x_8);
x_21 = lp_REPL_repl();
return x_21;
}
}
else
{
return x_6;
}
}
else
{
uint8_t x_22; 
x_22 = !lean_is_exclusive(x_3);
if (x_22 == 0)
{
return x_3;
}
else
{
lean_object* x_23; lean_object* x_24; 
x_23 = lean_ctor_get(x_3, 0);
lean_inc(x_23);
lean_dec(x_3);
x_24 = lean_alloc_ctor(1, 1, 0);
lean_ctor_set(x_24, 0, x_23);
return x_24;
}
}
}
}
LEAN_EXPORT lean_object* _lean_main(lean_object* x_1) {
_start:
{
lean_object* x_3; 
lean_dec(x_1);
x_3 = lp_REPL_main___redArg();
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4, lean_object* x_5, lean_object* x_6) {
_start:
{
lean_object* x_7; 
x_7 = lp_REPL_List_forIn_x27_loop___at___00main_spec__0(x_1, x_2, x_3, x_4, x_5);
lean_dec(x_2);
return x_7;
}
}
LEAN_EXPORT lean_object* lp_REPL_main___boxed(lean_object* x_1, lean_object* x_2) {
_start:
{
lean_object* x_3; 
x_3 = _lean_main(x_1);
return x_3;
}
}
LEAN_EXPORT lean_object* lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg___boxed(lean_object* x_1, lean_object* x_2, lean_object* x_3, lean_object* x_4) {
_start:
{
lean_object* x_5; 
x_5 = lp_REPL_List_forIn_x27_loop___at___00main_spec__0___redArg(x_1, x_2, x_3);
return x_5;
}
}
LEAN_EXPORT lean_object* lp_REPL_main___redArg___boxed(lean_object* x_1) {
_start:
{
lean_object* x_2; 
x_2 = lp_REPL_main___redArg();
return x_2;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_REPL_REPL_JSON(uint8_t builtin);
lean_object* initialize_REPL_REPL_Frontend(uint8_t builtin);
lean_object* initialize_REPL_REPL_Util_Path(uint8_t builtin);
lean_object* initialize_REPL_REPL_Lean_ContextInfo(uint8_t builtin);
lean_object* initialize_REPL_REPL_Lean_Environment(uint8_t builtin);
lean_object* initialize_REPL_REPL_Lean_InfoTree(uint8_t builtin);
lean_object* initialize_REPL_REPL_Lean_InfoTree_ToJson(uint8_t builtin);
lean_object* initialize_REPL_REPL_Snapshots(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_REPL_REPL_Main(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_JSON(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Frontend(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Util_Path(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Lean_ContextInfo(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Lean_Environment(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Lean_InfoTree(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Lean_InfoTree_ToJson(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_REPL_REPL_Snapshots(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_REPL_REPL_sorries___redArg___closed__0 = _init_lp_REPL_REPL_sorries___redArg___closed__0();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___closed__0);
lp_REPL_REPL_sorries___redArg___closed__1 = _init_lp_REPL_REPL_sorries___redArg___closed__1();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___closed__1);
lp_REPL_REPL_sorries___redArg___lam__6___closed__0 = _init_lp_REPL_REPL_sorries___redArg___lam__6___closed__0();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___lam__6___closed__0);
lp_REPL_REPL_sorries___redArg___lam__16___closed__2 = _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__2();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___lam__16___closed__2);
lp_REPL_REPL_sorries___redArg___lam__16___closed__1 = _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__1();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___lam__16___closed__1);
lp_REPL_REPL_sorries___redArg___lam__16___closed__0 = _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__0();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___lam__16___closed__0);
lp_REPL_REPL_sorries___redArg___lam__16___closed__3 = _init_lp_REPL_REPL_sorries___redArg___lam__16___closed__3();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___lam__16___closed__3);
lp_REPL_REPL_sorries___redArg___closed__2 = _init_lp_REPL_REPL_sorries___redArg___closed__2();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___closed__2);
lp_REPL_REPL_sorries___redArg___closed__3 = _init_lp_REPL_REPL_sorries___redArg___closed__3();
lean_mark_persistent(lp_REPL_REPL_sorries___redArg___closed__3);
lp_REPL_panic___at___00REPL_sorriesGC_spec__1___closed__0 = _init_lp_REPL_panic___at___00REPL_sorriesGC_spec__1___closed__0();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorriesGC_spec__1___closed__0);
lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__0 = _init_lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__0();
lean_mark_persistent(lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__0);
lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__1 = _init_lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__1();
lean_mark_persistent(lp_REPL_List_mapM_loop___at___00REPL_sorriesGC_spec__4___closed__1);
lp_REPL_REPL_ppTactic___closed__0 = _init_lp_REPL_REPL_ppTactic___closed__0();
lean_mark_persistent(lp_REPL_REPL_ppTactic___closed__0);
lp_REPL_REPL_ppTactic___closed__1 = _init_lp_REPL_REPL_ppTactic___closed__1();
lean_mark_persistent(lp_REPL_REPL_ppTactic___closed__1);
lp_REPL_REPL_ppTactic___closed__2 = _init_lp_REPL_REPL_ppTactic___closed__2();
lean_mark_persistent(lp_REPL_REPL_ppTactic___closed__2);
lp_REPL_REPL_ppTactic___closed__3 = _init_lp_REPL_REPL_ppTactic___closed__3();
lean_mark_persistent(lp_REPL_REPL_ppTactic___closed__3);
lp_REPL_REPL_ppTactic___closed__4 = _init_lp_REPL_REPL_ppTactic___closed__4();
lean_mark_persistent(lp_REPL_REPL_ppTactic___closed__4);
lp_REPL_REPL_ppTactic___closed__5 = _init_lp_REPL_REPL_ppTactic___closed__5();
lean_mark_persistent(lp_REPL_REPL_ppTactic___closed__5);
lp_REPL_REPL_ppTactic___lam__0___closed__0 = _init_lp_REPL_REPL_ppTactic___lam__0___closed__0();
lean_mark_persistent(lp_REPL_REPL_ppTactic___lam__0___closed__0);
lp_REPL_REPL_ppTactic___lam__0___closed__1 = _init_lp_REPL_REPL_ppTactic___lam__0___closed__1();
lean_mark_persistent(lp_REPL_REPL_ppTactic___lam__0___closed__1);
lp_REPL_REPL_tactics___redArg___closed__0 = _init_lp_REPL_REPL_tactics___redArg___closed__0();
lean_mark_persistent(lp_REPL_REPL_tactics___redArg___closed__0);
lp_REPL_REPL_tactics___redArg___closed__1 = _init_lp_REPL_REPL_tactics___redArg___closed__1();
lean_mark_persistent(lp_REPL_REPL_tactics___redArg___closed__1);
lp_REPL_REPL_createProofStepReponse___redArg___closed__0 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__0();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__0);
lp_REPL_REPL_createProofStepReponse___redArg___closed__1 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__1();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__1);
lp_REPL_REPL_createProofStepReponse___redArg___closed__2 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__2();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__2);
lp_REPL_REPL_createProofStepReponse___redArg___closed__3 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__3();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__3);
lp_REPL_REPL_createProofStepReponse___redArg___closed__4 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__4();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__4);
lp_REPL_REPL_createProofStepReponse___redArg___closed__5 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__5();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__5);
lp_REPL_REPL_createProofStepReponse___redArg___closed__7 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__7();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__7);
lp_REPL_REPL_createProofStepReponse___redArg___closed__8 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__8();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__8);
lp_REPL_REPL_createProofStepReponse___redArg___closed__6 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__6();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__6);
lp_REPL_REPL_createProofStepReponse___redArg___closed__9 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__9();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__9);
lp_REPL_REPL_createProofStepReponse___redArg___closed__10 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__10();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__10);
lp_REPL_REPL_createProofStepReponse___redArg___closed__11 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__11();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__11);
lp_REPL_REPL_createProofStepReponse___redArg___closed__12 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__12();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__12);
lp_REPL_REPL_createProofStepReponse___redArg___closed__13 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__13();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__13);
lp_REPL_REPL_createProofStepReponse___redArg___closed__14 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__14();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__14);
lp_REPL_REPL_createProofStepReponse___redArg___closed__15 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__15();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__15);
lp_REPL_REPL_createProofStepReponse___redArg___closed__16 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__16();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__16);
lp_REPL_REPL_createProofStepReponse___redArg___closed__17 = _init_lp_REPL_REPL_createProofStepReponse___redArg___closed__17();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___redArg___closed__17);
lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0 = _init_lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0();
lean_mark_persistent(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__0);
lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1 = _init_lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1();
lean_mark_persistent(lp_REPL_REPL_pickleCommandSnapshot___redArg___lam__3___closed__1);
lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__0 = _init_lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__0();
lean_mark_persistent(lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__0);
lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1 = _init_lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1();
lean_mark_persistent(lp_REPL_REPL_pickleProofSnapshot___redArg___lam__4___closed__1);
lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__0 = _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__0();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__0);
lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__1 = _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__1();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__1);
lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__2 = _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__2();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__2);
lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__3 = _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__3();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__3);
lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__4 = _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__4();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__4);
lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__5 = _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__5();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__5);
lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__6 = _init_lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__6();
lean_mark_persistent(lp_REPL_panic___at___00REPL_sorries___at___00REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0_spec__1_spec__2___closed__6);
lp_REPL_REPL_unpickleProofSnapshot___closed__0 = _init_lp_REPL_REPL_unpickleProofSnapshot___closed__0();
lean_mark_persistent(lp_REPL_REPL_unpickleProofSnapshot___closed__0);
lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___closed__0 = _init_lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___closed__0();
lean_mark_persistent(lp_REPL_REPL_createProofStepReponse___at___00REPL_unpickleProofSnapshot_spec__0___closed__0);
lp_REPL_REPL_getCommandSnapshot___closed__0 = _init_lp_REPL_REPL_getCommandSnapshot___closed__0();
lean_mark_persistent(lp_REPL_REPL_getCommandSnapshot___closed__0);
lp_REPL_REPL_getCommandSnapshot___closed__1 = _init_lp_REPL_REPL_getCommandSnapshot___closed__1();
lean_mark_persistent(lp_REPL_REPL_getCommandSnapshot___closed__1);
lp_REPL_REPL_runCommandGCAux___closed__0 = _init_lp_REPL_REPL_runCommandGCAux___closed__0();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__0);
lp_REPL_REPL_runCommandGCAux___closed__1 = _init_lp_REPL_REPL_runCommandGCAux___closed__1();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__1);
lp_REPL_REPL_runCommandGCAux___closed__2 = _init_lp_REPL_REPL_runCommandGCAux___closed__2();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__2);
lp_REPL_REPL_runCommandGCAux___closed__3 = _init_lp_REPL_REPL_runCommandGCAux___closed__3();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__3);
lp_REPL_REPL_runCommandGCAux___closed__4 = _init_lp_REPL_REPL_runCommandGCAux___closed__4();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__4);
lp_REPL_REPL_runCommandGCAux___closed__5 = _init_lp_REPL_REPL_runCommandGCAux___closed__5();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__5);
lp_REPL_REPL_runCommandGCAux___closed__6 = _init_lp_REPL_REPL_runCommandGCAux___closed__6();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__6);
lp_REPL_REPL_runCommandGCAux___closed__7 = _init_lp_REPL_REPL_runCommandGCAux___closed__7();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__7);
lp_REPL_REPL_runCommandGCAux___closed__8 = _init_lp_REPL_REPL_runCommandGCAux___closed__8();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__8);
lp_REPL_REPL_runCommandGCAux___closed__9 = _init_lp_REPL_REPL_runCommandGCAux___closed__9();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__9);
lp_REPL_REPL_runCommandGCAux___closed__10 = _init_lp_REPL_REPL_runCommandGCAux___closed__10();
lean_mark_persistent(lp_REPL_REPL_runCommandGCAux___closed__10);
lp_REPL_REPL_runCommandAux___closed__0 = _init_lp_REPL_REPL_runCommandAux___closed__0();
lean_mark_persistent(lp_REPL_REPL_runCommandAux___closed__0);
lp_REPL_REPL_runCommand___closed__0 = _init_lp_REPL_REPL_runCommand___closed__0();
lean_mark_persistent(lp_REPL_REPL_runCommand___closed__0);
lp_REPL_REPL_splitArray___redArg___closed__0 = _init_lp_REPL_REPL_splitArray___redArg___closed__0();
lean_mark_persistent(lp_REPL_REPL_splitArray___redArg___closed__0);
lp_REPL_REPL_splitArray___redArg___closed__1 = _init_lp_REPL_REPL_splitArray___redArg___closed__1();
lean_mark_persistent(lp_REPL_REPL_splitArray___redArg___closed__1);
lp_REPL_REPL_splitArray___redArg___closed__2 = _init_lp_REPL_REPL_splitArray___redArg___closed__2();
lean_mark_persistent(lp_REPL_REPL_splitArray___redArg___closed__2);
lp_REPL_REPL_splitArray___redArg___closed__3 = _init_lp_REPL_REPL_splitArray___redArg___closed__3();
lean_mark_persistent(lp_REPL_REPL_splitArray___redArg___closed__3);
lp_REPL_REPL_batchVerifyParrallel___closed__0 = _init_lp_REPL_REPL_batchVerifyParrallel___closed__0();
lean_mark_persistent(lp_REPL_REPL_batchVerifyParrallel___closed__0);
lp_REPL_REPL_processFile___closed__0 = _init_lp_REPL_REPL_processFile___closed__0();
lean_mark_persistent(lp_REPL_REPL_processFile___closed__0);
lp_REPL_REPL_runBatchVerify___closed__0 = _init_lp_REPL_REPL_runBatchVerify___closed__0();
lean_mark_persistent(lp_REPL_REPL_runBatchVerify___closed__0);
lp_REPL_REPL_runBatchVerify___closed__1 = _init_lp_REPL_REPL_runBatchVerify___closed__1();
lean_mark_persistent(lp_REPL_REPL_runBatchVerify___closed__1);
lp_REPL_REPL_runBatchVerify___closed__2 = _init_lp_REPL_REPL_runBatchVerify___closed__2();
lean_mark_persistent(lp_REPL_REPL_runBatchVerify___closed__2);
lp_REPL_REPL_runBatchVerify___closed__3 = _init_lp_REPL_REPL_runBatchVerify___closed__3();
lean_mark_persistent(lp_REPL_REPL_runBatchVerify___closed__3);
lp_REPL_REPL_runBatchVerify___closed__4 = _init_lp_REPL_REPL_runBatchVerify___closed__4();
lean_mark_persistent(lp_REPL_REPL_runBatchVerify___closed__4);
lp_REPL_REPL_runBatchVerify___closed__5 = _init_lp_REPL_REPL_runBatchVerify___closed__5();
lean_mark_persistent(lp_REPL_REPL_runBatchVerify___closed__5);
lp_REPL_REPL_runBatchVerify___closed__6 = _init_lp_REPL_REPL_runBatchVerify___closed__6();
lean_mark_persistent(lp_REPL_REPL_runBatchVerify___closed__6);
lp_REPL_REPL_runProofStep___closed__0 = _init_lp_REPL_REPL_runProofStep___closed__0();
lean_mark_persistent(lp_REPL_REPL_runProofStep___closed__0);
lp_REPL_REPL_runProofStep___closed__1 = _init_lp_REPL_REPL_runProofStep___closed__1();
lean_mark_persistent(lp_REPL_REPL_runProofStep___closed__1);
lp_REPL_REPL_runProofStep___closed__2 = _init_lp_REPL_REPL_runProofStep___closed__2();
lean_mark_persistent(lp_REPL_REPL_runProofStep___closed__2);
lp_REPL_instFromJsonBatch_fromJson___closed__0 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__0();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__0);
lp_REPL_instFromJsonBatch_fromJson___closed__1 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__1();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__1);
lp_REPL_instFromJsonBatch_fromJson___closed__2 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__2();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__2);
lp_REPL_instFromJsonBatch_fromJson___closed__3 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__3();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__3);
lp_REPL_instFromJsonBatch_fromJson___closed__4 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__4();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__4);
lp_REPL_instFromJsonBatch_fromJson___closed__5 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__5();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__5);
lp_REPL_instFromJsonBatch_fromJson___closed__6 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__6();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__6);
lp_REPL_instFromJsonBatch_fromJson___closed__7 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__7();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__7);
lp_REPL_instFromJsonBatch_fromJson___closed__8 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__8();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__8);
lp_REPL_instFromJsonBatch_fromJson___closed__9 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__9();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__9);
lp_REPL_instFromJsonBatch_fromJson___closed__10 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__10();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__10);
lp_REPL_instFromJsonBatch_fromJson___closed__11 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__11();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__11);
lp_REPL_instFromJsonBatch_fromJson___closed__12 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__12();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__12);
lp_REPL_instFromJsonBatch_fromJson___closed__13 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__13();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__13);
lp_REPL_instFromJsonBatch_fromJson___closed__14 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__14();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__14);
lp_REPL_instFromJsonBatch_fromJson___closed__15 = _init_lp_REPL_instFromJsonBatch_fromJson___closed__15();
lean_mark_persistent(lp_REPL_instFromJsonBatch_fromJson___closed__15);
lp_REPL_instFromJsonBatch___closed__0 = _init_lp_REPL_instFromJsonBatch___closed__0();
lean_mark_persistent(lp_REPL_instFromJsonBatch___closed__0);
lp_REPL_instFromJsonBatch = _init_lp_REPL_instFromJsonBatch();
lean_mark_persistent(lp_REPL_instFromJsonBatch);
lp_REPL_instToJsonBatch_toJson___closed__0 = _init_lp_REPL_instToJsonBatch_toJson___closed__0();
lean_mark_persistent(lp_REPL_instToJsonBatch_toJson___closed__0);
lp_REPL_instToJsonBatch___closed__0 = _init_lp_REPL_instToJsonBatch___closed__0();
lean_mark_persistent(lp_REPL_instToJsonBatch___closed__0);
lp_REPL_instToJsonBatch = _init_lp_REPL_instToJsonBatch();
lean_mark_persistent(lp_REPL_instToJsonBatch);
lp_REPL_parse___closed__0 = _init_lp_REPL_parse___closed__0();
lean_mark_persistent(lp_REPL_parse___closed__0);
lp_REPL_parse___closed__1 = _init_lp_REPL_parse___closed__1();
lean_mark_persistent(lp_REPL_parse___closed__1);
lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0 = _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0();
lean_mark_persistent(lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__0);
lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1 = _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1();
lean_mark_persistent(lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__1);
lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2 = _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2();
lean_mark_persistent(lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__2);
lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3 = _init_lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3();
lean_mark_persistent(lp_REPL___private_Init_Data_Array_Basic_0__Array_mapMUnsafe_map___at___00Array_toJson___at___00repl_loop_spec__11_spec__11___closed__3);
lp_REPL_repl_loop___closed__0 = _init_lp_REPL_repl_loop___closed__0();
lean_mark_persistent(lp_REPL_repl_loop___closed__0);
lp_REPL_repl_loop___closed__1 = _init_lp_REPL_repl_loop___closed__1();
lean_mark_persistent(lp_REPL_repl_loop___closed__1);
lp_REPL_repl_loop___closed__2 = _init_lp_REPL_repl_loop___closed__2();
lean_mark_persistent(lp_REPL_repl_loop___closed__2);
lp_REPL_repl_loop___closed__3 = _init_lp_REPL_repl_loop___closed__3();
lean_mark_persistent(lp_REPL_repl_loop___closed__3);
lp_REPL_repl_loop___closed__4 = _init_lp_REPL_repl_loop___closed__4();
lean_mark_persistent(lp_REPL_repl_loop___closed__4);
lp_REPL_repl_loop___closed__5 = _init_lp_REPL_repl_loop___closed__5();
lean_mark_persistent(lp_REPL_repl_loop___closed__5);
lp_REPL_repl_loop___closed__6 = _init_lp_REPL_repl_loop___closed__6();
lean_mark_persistent(lp_REPL_repl_loop___closed__6);
lp_REPL_repl___closed__0 = _init_lp_REPL_repl___closed__0();
lean_mark_persistent(lp_REPL_repl___closed__0);
lp_REPL_repl___closed__1 = _init_lp_REPL_repl___closed__1();
lean_mark_persistent(lp_REPL_repl___closed__1);
lp_REPL_main___redArg___closed__0 = _init_lp_REPL_main___redArg___closed__0();
lean_mark_persistent(lp_REPL_main___redArg___closed__0);
lp_REPL_main___redArg___closed__1 = _init_lp_REPL_main___redArg___closed__1();
lean_mark_persistent(lp_REPL_main___redArg___closed__1);
return lean_io_result_mk_ok(lean_box(0));
}
extern lean_object* initialize_implementation_NativeBranchBackend(uint8_t builtin);
extern lean_object* gpu_smt_native_backend(lean_object*);
char ** lean_setup_args(int argc, char ** argv);
void lean_initialize();

  #if defined(WIN32) || defined(_WIN32)
  #include <windows.h>
  #endif

  int main(int argc, char ** argv) {
  #if defined(WIN32) || defined(_WIN32)
  SetErrorMode(SEM_FAILCRITICALERRORS);
  SetConsoleOutputCP(CP_UTF8);
  #endif
  lean_object* in; lean_object* res;
argv = lean_setup_args(argc, argv);
lean_initialize();
lean_set_panic_messages(false);
res = initialize_implementation_NativeBranchBackend(1 /* builtin */);
lean_set_panic_messages(true);
lean_io_mark_end_initialization();
if (lean_io_result_is_ok(res)) {
lean_dec_ref(res);
lean_init_task_manager();
in = lean_box(0);
int i = argc;
while (i > 1) {
 lean_object* n;
 i--;
 n = lean_alloc_ctor(1,2,0); lean_ctor_set(n, 0, lean_mk_string(argv[i])); lean_ctor_set(n, 1, in);
 in = n;
}
res = gpu_smt_native_backend(in);
}
lean_finalize_task_manager();
if (lean_io_result_is_ok(res)) {
  int ret = 0;
  lean_dec_ref(res);
  return ret;
} else {
  lean_io_result_show_error(res);
  lean_dec_ref(res);
  return 1;
}
}
#ifdef __cplusplus
}
#endif
