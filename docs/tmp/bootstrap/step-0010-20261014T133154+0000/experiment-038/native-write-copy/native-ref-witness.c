#include <lean/lean.h>
#include <stdio.h>
#include <stdlib.h>
extern void lean_initialize_runtime_module(void);
extern lean_object* gpu_smt_prepare_refs(lean_object*);
extern lean_object* gpu_smt_branch_begin(uint8_t,lean_object*);
extern lean_object* gpu_smt_branch_end(uint64_t,lean_object*);
static uint64_t begin(void) {
 lean_object* result=gpu_smt_branch_begin(1,lean_box(0));
 if(!lean_io_result_is_ok(result))exit(2);
 uint64_t id=lean_unbox_uint64(lean_io_result_get_value(result));
 lean_dec(result);return id;
}
static void end(uint64_t id,const char* label) {
 lean_object* result=gpu_smt_branch_end(id,lean_box(0));
 if(!lean_io_result_is_ok(result))exit(3);
 printf("%s %s\n",label,lean_string_cstr(lean_io_result_get_value(result)));
 lean_dec(result);
}
static size_t value(lean_object* ref) {
 lean_object* result=lean_st_ref_get(ref);
 size_t v=lean_unbox(result);lean_dec(result);return v;
}
int main(void) {
 lean_initialize_runtime_module();
 lean_object* ref=lean_st_mk_ref(lean_box(0));
 lean_object* ready=gpu_smt_prepare_refs(lean_box(0));
 if(!lean_io_result_is_ok(ready))return 4;
 lean_dec(ready);
 uint64_t first=begin();
 if(value(ref)!=0)return 5;
 end(first,"READ_ONLY");
 uint64_t second=begin();
 if(value(ref)!=0)return 6;
 lean_object* set=lean_st_ref_set(ref,lean_box(7));lean_dec(set);
 if(value(ref)!=7)return 7;
 end(second,"FIRST_WRITE");
 if(value(ref)!=0)return 8;
 uint64_t third=begin();
 if(value(ref)!=0)return 9;
 end(third,"NEXT_BRANCH");
 lean_dec(ref);
 puts("VALUES initial=0 private=7 root=0 next=0");
 return 0;
}
