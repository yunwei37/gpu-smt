# Corrected-family profiling qualification and full capture

2026-10-18 UTC; owning-thread self-review, no independent audit.

The corrected headers now import CostBaseline alone for strong native and CostOracle for the direct oracle, rather than stacking the legacy arithmetic family. Cost binaries are generated into a separate private build tree from the immutable retained inputs. Existing active primary binaries, source/build tree and collection protocol are untouched.

A 24-source matched run on CPU4–7 returns identical full native JSON for each diagnostic versus its uninstrumented same-method control. Native wall is 35.704257430 s without instrumentation and 36.648442563 s with it (+2.644%). Oracle wall is 26.455438096 s versus 27.148719011 s (+2.621%). This single qualification pair is not a general overhead estimate or a speedup result. No subtraction of logging overhead is applied.

All 231 native LP calls have source/call identity, shape and product ancestry. The oracle has 115 direct calls plus 10 native fallback calls with complete identities/shape/product metadata, including failed branches. Both all-call analyses report complete attribution. Complete JSON rows are serialized across writers to prevent the previous large-row interleaving fault. Initial build faults and their forward repairs are retained.

On these **24 sources only**, all numeric LP wall sums to 16.165224663 s of the native diagnostic's own 36.648442563 s (44.1089%). Adding all Lean product construction gives the deliberately generous fixed-work zero-cost deletion sum 21.171471945 s. Its conditional elapsed lower bound is 15.476970618 s, a 2.367934x optimistic ceiling. This overcounts overlap, additionally removes product proof construction beyond a floating GPU guarantee, and assumes unchanged certificates/fallback/noneligible work. It does not establish a universal scheduler bound or a 1,000-source result. It cannot justify GPU closure.

The new full original1,000-source strong-native/oracle phase capture is running on CPU4–7 with its own wall denominator (full1000-launch.json). The 2,234.69 s primary used CPU12–15 and did not collect these phases; these runs are the same corrected implementation family, **not the identical historical run**. Their durations are kept separate. The full input still has default300 s request/finalization and48 GiB address space. Existing paired CPU and prefix captures remain active.

Next result: close the native diagnostic, check source parity and phase coverage, then calculate its own wall shares and zero-cost bounds. Do not infer a completed bound from this qualification. The admitted race/batching mechanism proceeds in parallel because current evidence does not exclude1.5x.
