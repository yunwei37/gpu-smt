# Upstream primitive,not a new method
Pinned SDK Init/ShareCommon.lean and Lean/Util/ShareCommon.lean;
https://raw.githubusercontent.com/leanprover/lean4/v4.9.0-rc1/src/runtime/sharecommon.cpp
read2026-10-29. Upstream canonicalizes constructor/array/string data;
it leaves closure/ref/task/thunk/external/MPZ objects by identity. Equality is
not hash-only. Observation canonicalizes a retained copy under the same resource
watchdog,outside the registry lock;the candidate environment is not replaced.
Unknown nonshared opaque values may still cause conservative misses. Do not call
generic upstream sharing novelty or authorize tactic-result replay with it.
