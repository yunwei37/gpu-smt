# Task-held-out ordering model — root self-review

All7,808original candidates remain in244task groups; five folds assign
producer_task_index modulo5, holding all32siblings out together.
Source-only features are comment-stripped size/lines, numeral digit counts
and tactic counts. Logistic success probability and ridge logHTTPtime use
defaultL2penalty1, unpenalized intercept; one fit, no hyperparameter search.
Scoring log(probability)-predictedlogtime affects ordering only, never
native acceptance or failure. CPU training command/memory and all model
coefficients/predictions are retained.

Held-out first-k solved tasks:
{"1": 92, "16": 135, "2": 105, "32": 142, "4": 114, "8": 125}

Original order:92/112/125/132/138/142 at k1/2/4/8/16/32.
This fit gives92/105/114/125/135/142. Its interleaved fixed-cost model takes
15051.031831s
(ratio1.440930),
worse than original-order cancellation14803.176432s and short-code
14659.452074s. It is not an improvement and no actual speed was measured.
Model fitting is retrospective on inspected data despite task-held-out labels;
do not call it fresh benchmark generalization.

Runtime model-score arithmetic matches every stored held-out prediction;
runtime ranking reads source/fold weights, not outcome/time labels.
However, this weak fit is not added as another long whole-population cell.
The currently planned native group remains all-candidate, original
first-success and short-code first-success. Learned ranking stays an
available component for evidence-driven improvement, not a stop condition
for scheduling or the other directions. Wrong predictions only reorder
native work; cancellation still requires an actual checked success.
First-success inference cannot replace per-candidate RL reward collection.
No ordinary lexical ranker novelty or independent audit is claimed.
