// Measurement only;typed Environment values from the pinned Lean4.9 runtime.
// Skip shared subgraphs. Compare immutable data,never a hash alone.
// Distinct closures/tasks/refs/thunks/external/MPZ values are conservative misses.
#include <lean/lean.h>
#include <cstring>
#include <vector>
#include <unordered_set>
#include <utility>
#include <cstdint>

namespace {
struct PairHash {
    size_t operator()(std::pair<lean_object *,lean_object *> p) const {
        return (reinterpret_cast<uintptr_t>(p.first) >> 3) ^
               (reinterpret_cast<uintptr_t>(p.second) << 1);
    }
};
bool equal(lean_object *a, lean_object *b) {
    std::vector<std::pair<lean_object *,lean_object *>> todo{{a,b}};
    std::unordered_set<std::pair<lean_object *,lean_object *>,PairHash> seen;
    while (!todo.empty()) {
        auto [x,y]=todo.back(); todo.pop_back();
        if (x==y) continue;
        if (lean_is_scalar(x) || lean_is_scalar(y)) return false;
        auto tag=lean_ptr_tag(x);
        if (tag!=lean_ptr_tag(y)) return false;
        if (!seen.emplace(x,y).second) continue;
        if (tag < LeanClosure) {
            unsigned n=lean_ctor_num_objs(x);
            if (n!=lean_ctor_num_objs(y)) return false;
            // The constructor header encodes pointer count and complete object
            // byte size. Padding differences may only create false negatives.
            size_t size=lean_object_byte_size(x);
            if (size!=lean_object_byte_size(y)) return false;
            size_t offset=sizeof(lean_object)+n*sizeof(void *);
            if (std::memcmp(reinterpret_cast<char *>(x)+offset,
                            reinterpret_cast<char *>(y)+offset,size-offset))
                return false;
            for(unsigned i=0;i<n;++i)
                todo.emplace_back(lean_ctor_get(x,i),lean_ctor_get(y,i));
        } else if (tag==LeanArray) {
            size_t n=lean_array_size(x);
            if(n!=lean_array_size(y)) return false;
            for(size_t i=0;i<n;++i)
                todo.emplace_back(lean_array_get_core(x,i),lean_array_get_core(y,i));
        } else if (tag==LeanString) {
            if(lean_string_size(x)!=lean_string_size(y) ||
               lean_string_len(x)!=lean_string_len(y) ||
               std::memcmp(lean_string_cstr(x),lean_string_cstr(y),
                           lean_string_size(x))) return false;
        } else if (tag==LeanScalarArray) {
            size_t n=lean_sarray_size(x),size=lean_sarray_elem_size(x);
            if(n!=lean_sarray_size(y) || size!=lean_sarray_elem_size(y) ||
               std::memcmp(lean_sarray_cptr(x),lean_sarray_cptr(y),n*size))
                return false;
        } else {
            return false;
        }
    }
    return true;
}
}
extern "C" LEAN_EXPORT uint8_t gpu_smt_environment_equal(
        b_lean_obj_arg a,b_lean_obj_arg b) {
    return equal(a,b);
}
