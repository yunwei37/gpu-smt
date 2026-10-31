# Precision extension for the largest observed variance stratum

**Prepared, not launched.** No new CPU observations or tightened CI claimed.
The standard-artifact26/42pilot identifies cell size0–50/depth11–100/
no-kernel-token (45,251modules) as the largest observed variance.
Its two CPU observations produce74.1775h and a fragile cell-only nominal95%
interval[0,623.1803]h. This extension measures more random sources in that
cell rather than rerunning these same two files.

Original42random draws remain the primary all-source frame.
Seed20261031, Python random.Random(seed).sample(sorted(remainder),6)
draws six distinct modules uniformly from45,249cell members after excluding
the original two pilot modules. Source sizes use original cut4400bytes;
native import depth11–100; lexical decide+kernel count=0.
No dependency-ease filtering or replacement was applied, including the
2,116fresh-dependency source in AbelianModuli.

## Conditional estimator, separate from original42

Condition on the observed pilot and the decision to investigate this cell.
Let R=45,249, n=6 and y_i be native user+system CPU with the same pinned
SDK/library/outputs/M9216/j8/source options.
Estimate the whole-cell total as:
T_hat = y_pilot1+y_pilot2+R*mean(y_new).
Conditional design variance estimate:
R^2*(1-n/R)*s_new^2/n.
A nominal95%t interval with df5 may be reported **only if all six draws
complete**, with the same heavy-tail/model limitations.
This keeps the pilot observations as known members, not a naive pooled
adaptive n=8 sample. It makes no optional-sampling/global coverage claim.

The two excluded original pilot modules are:
- OAI.NumberTheory.PadicHodge.IntegralComparison.OrderedCech.ReindexSingle
- OAI.Analysis.PDE.Weak.Elliptic.InteriorH1Derivative

targets.csv contains closure counts at planning time, not predicted CPU.
Unselected dependency compiles have zero sampling weight. Small-cell
nonnormality and long proof tails remain possible. This panel does not
resolve missing draws in other cells and cannot create a finite global CI.
All-source163,097 and default OAI-root130,834 remain distinct populations.
