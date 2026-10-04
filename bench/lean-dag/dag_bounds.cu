// Scoped primitive: loose-bound-variable metadata, not a Lean proof checker.
// Input expressions have validated backward child indices; the host launches
// one wave at each DAG depth to provide dependency ordering.
extern "C" __global__ void dag_bounds(const unsigned* nodes, const unsigned* order,
                                    unsigned* out, unsigned begin, unsigned end) {
  unsigned p = begin + blockIdx.x * blockDim.x + threadIdx.x;
  if (p >= end) return;
  unsigned i = order[p];
  const unsigned* n = nodes + 5ULL*i;
  unsigned a = n[1], b = n[2], c = n[3], value = 0;
  switch (n[0]) {
    case 1: value = n[4] + 1; break;
    case 2: value = out[a] > out[b] ? out[a] : out[b]; break;
    case 3: { unsigned body = out[b] ? out[b]-1 : 0;
              value = out[a] > body ? out[a] : body; break; }
    case 4: { unsigned body = out[c] ? out[c]-1 : 0;
              value = out[a] > out[b] ? out[a] : out[b];
              value = value > body ? value : body; break; }
    case 5: value = out[a]; break;
  }
  out[i] = value;
}
