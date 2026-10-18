# Lean4.9 formal benchmark oracle adapter

[Plan](plan.md), [source](FormalOracle49.lean), [build](build.py),
[actual64 qualification](result-review.md), [raw/result](qualification-result.json).
Uses the unchanged formal SDK/data/native linarith library and existing Power
numerical binaries. The adapter runs Real/Rat natural-exponent export and native
certificate checks; unsupported cases restore state and use native preprocessing,
then stock tactics. No GPU gain is claimed. These modes are not the fully ported
4.27 Fast frontend or a whole upstream Kimina/SHRED service.

Reproduce: pinned Kimina venv Python build.py, then qualify.py; private build
directory and exact dependencies are recorded in build-receipt.json.
All64 responses are identical across modes; actual native/direct engagement
is88requests each. Selected clocks are not full-population performance.


The [complete original populations](full-populations/README.md) are now being
evaluated. Their unfinished cells do not extend the Goedel speedup claim.
