# Stock module profile observations

profile categories are rounded exclusive same-thread elapsed scopes, potentially overlapping across threads; shares are accumulated-category descriptions, not CPU/exact wall fractions; type checking includes addDecl/auxiliary declarations; import loads compiled dependencies, not transitive proof rechecking

| Module | Repeat | Normal wall (s) | Profile wall (s) | Delta (s) | Diagnostic identity |
|---|---:|---:|---:|---:|---|
| Mathlib/Algebra/Group/Basic.lean | 1 | 3.480965851 | 3.621971367 | 0.141005516 | True |
| Mathlib/Algebra/Group/Basic.lean | 2 | 3.502884924 | 3.580426162 | 0.077541238 | True |
| Mathlib/Algebra/Group/Basic.lean | 3 | 3.420168594 | 3.582611268 | 0.162442674 | True |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | 7.215609712 | 7.319432488 | 0.103822776 | True |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | 7.23508209 | 7.296526585 | 0.061444495 | True |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | 7.238186377 | 7.297709861 | 0.059523484 | True |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | 10.11410725 | 10.673256803 | 0.559149553 | True |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | 10.071323018 | 10.676250848 | 0.60492783 | True |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | 10.09238225 | 10.779354062 | 0.686971812 | True |
| Mathlib/Data/Nat/Prime.lean | 1 | 2.435032033 | 2.576165034 | 0.141133001 | True |
| Mathlib/Data/Nat/Prime.lean | 2 | 2.476751061 | 2.556121647 | 0.079370586 | True |
| Mathlib/Data/Nat/Prime.lean | 3 | 2.43740359 | 2.618990311 | 0.181586721 | True |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | 10.551762155 | 11.2286074 | 0.676845245 | True |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | 10.57206089 | 11.256459014 | 0.684398124 | True |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | 10.591445021 | 11.423700622 | 0.832255601 | True |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | 8.624557637 | 9.091411852 | 0.466854215 | True |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | 8.567222316 | 9.045852242 | 0.478629926 | True |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | 8.668278134 | 9.0661681 | 0.397889966 | True |

| Module | Repeat | Cumulative category | Original display |
|---|---:|---|---:|
| Mathlib/Algebra/Group/Basic.lean | 1 | aesop | 21.6ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | attribute application | 4.75ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | compilation | 2.61ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | elaboration | 378ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | import | 223ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | initialization | 23.3ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | interpretation | 1.22s |
| Mathlib/Algebra/Group/Basic.lean | 1 | linting | 32ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | parsing | 49.3ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | simp | 425ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | tactic execution | 210ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | type checking | 175ms |
| Mathlib/Algebra/Group/Basic.lean | 1 | typeclass inference | 692ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | attribute application | 21.7ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | compilation | 96.1ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | elaboration | 1.85s |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | import | 389ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | initialization | 23.3ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | interpretation | 715ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | linting | 34.1ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | parsing | 42.9ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | simp | 472ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | tactic execution | 248ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | type checking | 311ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 1 | typeclass inference | 2.92s |
| Mathlib/Data/Nat/Prime.lean | 1 | attribute application | 1.87ms |
| Mathlib/Data/Nat/Prime.lean | 1 | compilation | 8.18ms |
| Mathlib/Data/Nat/Prime.lean | 1 | elaboration | 282ms |
| Mathlib/Data/Nat/Prime.lean | 1 | import | 284ms |
| Mathlib/Data/Nat/Prime.lean | 1 | initialization | 23.2ms |
| Mathlib/Data/Nat/Prime.lean | 1 | interpretation | 367ms |
| Mathlib/Data/Nat/Prime.lean | 1 | linting | 30.1ms |
| Mathlib/Data/Nat/Prime.lean | 1 | parsing | 28.4ms |
| Mathlib/Data/Nat/Prime.lean | 1 | simp | 637ms |
| Mathlib/Data/Nat/Prime.lean | 1 | tactic execution | 251ms |
| Mathlib/Data/Nat/Prime.lean | 1 | type checking | 92.7ms |
| Mathlib/Data/Nat/Prime.lean | 1 | typeclass inference | 404ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | aesop | 22.2ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | attribute application | 11.8ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | compilation | 1.03ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | dsimp | 8.08ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | elaboration | 888ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | import | 463ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | initialization | 23.3ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | interpretation | 674ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | linting | 49.3ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | norm_num | 0.142ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | parsing | 37ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | simp | 764ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | tactic execution | 846ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | type checking | 600ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 1 | typeclass inference | 6.64s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | aesop | 608ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | attribute application | 12.5ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | compilation | 71ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | dsimp | 1.78ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | elaboration | 2.97s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | import | 523ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | initialization | 23.3ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | interpretation | 1.98s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | linting | 102ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | norm_num | 362ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | parsing | 52.5ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | ring | 166ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | simp | 630ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | tactic execution | 497ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | type checking | 399ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 1 | typeclass inference | 2.06s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | attribute application | 4.42ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | compilation | 68.8ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | dsimp | 0.711ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | elaboration | 679ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | import | 600ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | initialization | 23.2ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | interpretation | 1.14s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | linting | 45.2ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | norm_num | 1.23ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | parsing | 48.7ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | simp | 1.44s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | tactic execution | 551ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | type checking | 362ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 1 | typeclass inference | 3.91s |
| Mathlib/Algebra/Group/Basic.lean | 2 | aesop | 20.8ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | attribute application | 4.65ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | compilation | 2.66ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | elaboration | 372ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | import | 210ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | initialization | 23.3ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | interpretation | 1.2s |
| Mathlib/Algebra/Group/Basic.lean | 2 | linting | 31.6ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | parsing | 47.3ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | simp | 424ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | tactic execution | 207ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | type checking | 173ms |
| Mathlib/Algebra/Group/Basic.lean | 2 | typeclass inference | 689ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | attribute application | 21.8ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | compilation | 95.4ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | elaboration | 1.84s |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | import | 391ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | initialization | 23.5ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | interpretation | 712ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | linting | 33.9ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | parsing | 42.5ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | simp | 472ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | tactic execution | 247ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | type checking | 311ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 2 | typeclass inference | 2.91s |
| Mathlib/Data/Nat/Prime.lean | 2 | attribute application | 1.86ms |
| Mathlib/Data/Nat/Prime.lean | 2 | compilation | 8.1ms |
| Mathlib/Data/Nat/Prime.lean | 2 | elaboration | 279ms |
| Mathlib/Data/Nat/Prime.lean | 2 | import | 272ms |
| Mathlib/Data/Nat/Prime.lean | 2 | initialization | 22.9ms |
| Mathlib/Data/Nat/Prime.lean | 2 | interpretation | 361ms |
| Mathlib/Data/Nat/Prime.lean | 2 | linting | 29.9ms |
| Mathlib/Data/Nat/Prime.lean | 2 | parsing | 27.5ms |
| Mathlib/Data/Nat/Prime.lean | 2 | simp | 636ms |
| Mathlib/Data/Nat/Prime.lean | 2 | tactic execution | 249ms |
| Mathlib/Data/Nat/Prime.lean | 2 | type checking | 91.9ms |
| Mathlib/Data/Nat/Prime.lean | 2 | typeclass inference | 403ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | aesop | 22.5ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | attribute application | 11.9ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | compilation | 1.07ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | dsimp | 8.25ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | elaboration | 890ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | import | 471ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | initialization | 23.3ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | interpretation | 672ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | linting | 49.7ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | norm_num | 0.139ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | parsing | 36.9ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | simp | 762ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | tactic execution | 848ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | type checking | 600ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 2 | typeclass inference | 6.65s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | aesop | 606ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | attribute application | 12.4ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | compilation | 70ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | dsimp | 1.86ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | elaboration | 2.98s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | import | 523ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | initialization | 23.1ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | interpretation | 1.98s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | linting | 102ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | norm_num | 362ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | parsing | 52.1ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | ring | 167ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | simp | 631ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | tactic execution | 495ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | type checking | 398ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 2 | typeclass inference | 2.06s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | attribute application | 4.44ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | compilation | 68.7ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | dsimp | 0.7ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | elaboration | 675ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | import | 597ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | initialization | 23.2ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | interpretation | 1.13s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | linting | 44.9ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | norm_num | 1.2ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | parsing | 48.1ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | simp | 1.43s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | tactic execution | 548ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | type checking | 357ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 2 | typeclass inference | 3.89s |
| Mathlib/Algebra/Group/Basic.lean | 3 | aesop | 20.8ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | attribute application | 4.59ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | compilation | 2.54ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | elaboration | 372ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | import | 214ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | initialization | 23.2ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | interpretation | 1.2s |
| Mathlib/Algebra/Group/Basic.lean | 3 | linting | 31.5ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | parsing | 47.2ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | simp | 422ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | tactic execution | 207ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | type checking | 172ms |
| Mathlib/Algebra/Group/Basic.lean | 3 | typeclass inference | 688ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | attribute application | 21.8ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | compilation | 96ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | elaboration | 1.84s |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | import | 387ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | initialization | 23.3ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | interpretation | 710ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | linting | 33.9ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | parsing | 42.5ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | simp | 471ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | tactic execution | 247ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | type checking | 310ms |
| Mathlib/Algebra/Polynomial/Basic.lean | 3 | typeclass inference | 2.92s |
| Mathlib/Data/Nat/Prime.lean | 3 | attribute application | 1.9ms |
| Mathlib/Data/Nat/Prime.lean | 3 | compilation | 8.19ms |
| Mathlib/Data/Nat/Prime.lean | 3 | elaboration | 290ms |
| Mathlib/Data/Nat/Prime.lean | 3 | import | 286ms |
| Mathlib/Data/Nat/Prime.lean | 3 | initialization | 23.6ms |
| Mathlib/Data/Nat/Prime.lean | 3 | interpretation | 375ms |
| Mathlib/Data/Nat/Prime.lean | 3 | linting | 30.9ms |
| Mathlib/Data/Nat/Prime.lean | 3 | parsing | 30.3ms |
| Mathlib/Data/Nat/Prime.lean | 3 | simp | 641ms |
| Mathlib/Data/Nat/Prime.lean | 3 | tactic execution | 257ms |
| Mathlib/Data/Nat/Prime.lean | 3 | type checking | 94ms |
| Mathlib/Data/Nat/Prime.lean | 3 | typeclass inference | 409ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | aesop | 23ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | attribute application | 12.2ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | compilation | 1.03ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | dsimp | 8.17ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | elaboration | 917ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | import | 464ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | initialization | 23.5ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | interpretation | 683ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | linting | 50.4ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | norm_num | 0.142ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | parsing | 38ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | simp | 771ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | tactic execution | 855ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | type checking | 617ms |
| Mathlib/LinearAlgebra/FiniteDimensional.lean | 3 | typeclass inference | 6.76s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | aesop | 614ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | attribute application | 12.9ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | compilation | 71.2ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | dsimp | 1.88ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | elaboration | 3.01s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | import | 521ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | initialization | 23.2ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | interpretation | 2.01s |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | linting | 102ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | norm_num | 362ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | parsing | 57.5ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | ring | 167ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | simp | 633ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | tactic execution | 499ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | type checking | 402ms |
| Mathlib/Analysis/SpecialFunctions/Trigonometric/Basic.lean | 3 | typeclass inference | 2.08s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | attribute application | 4.46ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | compilation | 68.9ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | dsimp | 0.712ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | elaboration | 678ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | import | 603ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | initialization | 23.3ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | interpretation | 1.14s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | linting | 45ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | norm_num | 1.22ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | parsing | 48.6ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | simp | 1.43s |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | tactic execution | 550ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | type checking | 360ms |
| Mathlib/MeasureTheory/Integral/IntervalIntegral.lean | 3 | typeclass inference | 3.9s |

Raw display units/values, unknown categories, CPU/maxRSS, all failures and diagnostics remain in `cells.jsonl`; counts, completeness, issues and paired repeated values are in `summary.json`. RSS is not PSS. No correctness, GPU readiness, Amdahl bound or service-speed claim follows from category totals.
