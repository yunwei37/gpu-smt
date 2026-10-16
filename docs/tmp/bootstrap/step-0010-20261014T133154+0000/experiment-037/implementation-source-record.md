# E037 integrated setup implementation
Root implements only native Lean/GPU support paths; OMP author paths remain untouched.
Derived from published E036 native overlay and frozen closure interpreter, which remain unmodified in Git.
Native construction appends packed identities using typed-pointer identity maps; there is no post-parse expression DAG traversal. Raw-index overwrites preserve old parent identities because native typed pointers are immutable. This first implementation retains pointer maps during parsing; direct raw-slot emission has not been claimed.
Worker state hash-conses full terms, environments and levels with exact key comparisons. Completed operations use exact full operation/input/mode keys and per-declaration epochs. No in-flight/failed operation is cached as success; arrays remain private per worker. The shared MDATA mutation is removed. Body constant access is conservatively cutoff at the current declaration; all native checking remains enabled.
Original capacity/step defaults remain unchanged. Extra lookup-table memory and initialization, full parsing, final name fixups, host pass and native checks are all inside the measured process.
This is host setup, not GPU preflight, replacement qualification or an accelerated verdict.
