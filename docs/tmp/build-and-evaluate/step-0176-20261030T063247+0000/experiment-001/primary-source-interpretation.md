# Primary-source interpretation — root self-review

Publisher pin:4eaee87548250b2682affda7d05d947c05554bae.
The root README describes mixed verification states;Lean README describes one
library and recommends small builds. Lean-toolchain selects4.34.1;Lake's
HodgeConjecture srcDir literal confirms W's source-root correction.

Lean4.34.1 Decide.lean evalDecideCore routes kernel mode to doKernel;the
ordinary call uses mkAuxLemma with its default caching. AuxLemma.lean checks a
branch-local key and existing level parameters before creating a declaration.
Its table is not an imported global result cache. No native timing/hit count
is inferred. The same decision frontend has a native-mode branch,so tactic-name
tokens alone do not establish axiom closure.

URLs:
https://github.com/openai/math/tree/4eaee87548250b2682affda7d05d947c05554bae
https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/lean/lakefile.lean
https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Elab/Tactic/Decide.lean
https://github.com/leanprover/lean4/blob/v4.34.1/src/Lean/Meta/Tactic/AuxLemma.lean
