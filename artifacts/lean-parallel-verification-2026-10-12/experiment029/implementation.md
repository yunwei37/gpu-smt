# Direct implementation
Root adds the exact existing runSnapshotStreamCore candidate transition as an exported
function returning worker-local Root table and unchanged native record. All original
native parsing/elaboration/final checking/diagnostic/sorry/witness code is retained.
Embedding shares the first prepared imported-search roots, with native lthread workers.
No GPU execution, full soundness/independent review or performance is implied by build.
