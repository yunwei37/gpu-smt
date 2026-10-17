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
 uint64_t a=begin();
 lean_object* escaped=lean_st_mk_ref(lean_box(11));
 unsigned tag_a=lean_ptr_other(escaped);
 if(!tag_a)return 10;
 lean_object* wrapper=lean_alloc_ctor(0,1,0);
 lean_ctor_set(wrapper,0,escaped);
 end(a,"ESCAPED_OWNER");
 uint64_t b=begin();
 lean_object* local=lean_st_mk_ref(lean_box(12));
 unsigned tag_b=lean_ptr_other(local);
 if(!tag_b||tag_b==tag_a)return 11;
 lean_dec(local);
 end(b,"OTHER_OWNER");
 // Constructor deletion enqueues its ref field: actual runtime set_next must
 // preserve the owner byte before gpu_smt_ref_freed retires the tagged ref.
 lean_dec(wrapper);
 uint64_t c=begin();
 lean_object* reused=lean_st_mk_ref(lean_box(13));
 unsigned tag_c=lean_ptr_other(reused);
 if(tag_c!=tag_a)return 12;
 lean_dec(reused);
 end(c,"REUSED_OWNER");
 printf("TAGS escaped=%u other=%u reused=%u queued_delete=complete\n",
        tag_a,tag_b,tag_c);
 return 0;
}
