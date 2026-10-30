# EPFL individual review — 自审

Separate resource points; 12 budget-exceeded returns atHB200k, and3HB/2self-wall returns atHB10k. Stuck214 is censored and not counted.

### epfl-34888 — EPFL136-HB200k

bridge_required: Nat recurrence with fixed initial values. timeout at symbolic induction/omega, not a closed evaluator; derive structural recursion first.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem amc12a_2021_p8 (d : ℕ → ℕ) (h₀ : d 0 = 0) (h₁ : d 1 = 0) (h₂ : d 2 = 1)
    (h₃ : ∀ n ≥ 3, d n = d (n - 1) + d (n - 4)) : Even (d 2021) ∧ Odd (d 2022) ∧ Even (d 2023) := by
  have h_main : Even (d 2021) ∧ Odd (d 2022) ∧ Even (d 2023) := by
    have h₄ : ∀ n, d n % 2 = if n % 12 = 0 then 0 else if n % 12 = 1 then 0 else if n % 12 = 2 then 1 else if n % 12 = 3 then 1 else if n % 12 = 4 then 1 else if n % 12 = 5 then 1 else if n % 12 = 6 then 0 else if n % 12 = 7 then 1 else if n % 12 = 8 then 0 else if n % 12 = 9 then 1 else if n % 12 = 10 then 1 else 0 := by
      intro n
      induction n using Nat.strong_induction_on with
      | h n ih =>
        match n with
        | 0 => simp [h₀]
        | 1 => simp [h₁]
        | 2 => simp [h₂]
        | 3 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 4 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 5 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 6 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 7 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 8 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 9 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 10 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | 11 => simp [h₃, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
        | n + 12 =>
          have h₅ := ih (n + 11) (by omega)
          have h₆ := ih (n + 10) (by omega)
          have h₇ := ih (n + 9) (by omega)
          have h₈ := ih (n + 8) (by omega)
          have h₉ := ih (n + 7) (by omega)
          have h₁₀ := ih (n + 6) (by omega)
          have h₁₁ := ih (n + 5) (by omega)
          have h₁₂ := ih (n + 4) (by omega)
          have h₁₃ := ih (n + 3) (by omega)
          have h₁₄ := ih (n + 2) (by omega)
          have h₁₅ := ih (n + 1) (by omega)
          have h₁₆ := ih n (by omega)
          simp [h₃, Nat.add_mod, Nat.mul_mod, Nat.mod_mod] at *
          <;>
            (try omega) <;>
            (try
              {
                split_ifs at * <;> omega
              }) <;>
            (try
              {
                omega
              }) <;>
            (try
              {
                simp_all [Nat.even_iff, Nat.odd_iff]
                <;> omega
              })
    have h₅ : Even (d 2021) := by
      rw [even_iff_two_dvd]
      have h₅ := h₄ 2021
      have h₆ := h₄ 5
      have h₇ := h₄ 17
      have h₈ := h₄ 29
      have h₉ := h₄ 41
      have h₁₀ := h₄ 53
      have h₁₁ := h₄ 65
      have h₁₂ := h₄ 77
      have h₁₃ := h₄ 89
      have h₁₄ := h₄ 101
      have h₁₅ := h₄ 113
      have h₁₆ := h₄ 125
      have h₁₇ := h₄ 137
      have h₁₈ := h₄ 149
      have h₁₉ := h₄ 161
      have h₂₀ := h₄ 173
      have h₂₁ := h₄ 185
      have h₂₂ := h₄ 197
      have h₂₃ := h₄ 209
      norm_num [Nat.mod_eq_of_lt] at *
      <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.even_iff, Nat.odd_iff]
            <;> omega
          })
    have h₆ : Odd (d 2022) := by
      rw [Nat.odd_iff_not_even]
      rw [even_iff_two_dvd]
      have h₅ := h₄ 2022
      have h₆ := h₄ 6
      have h₇ := h₄ 18
      have h₈ := h₄ 30
      have h₉ := h₄ 42
      have h₁₀ := h₄ 54
      have h₁₁ := h₄ 66
      have h₁₂ := h₄ 78
      have h₁₃ := h₄ 90
      have h₁₄ := h₄ 102
      have h₁₅ := h₄ 114
      have h₁₆ := h₄ 126
      have h₁₇ := h₄ 138
      have h₁₈ := h₄ 150
      have h₁₉ := h₄ 162
      have h₂₀ := h₄ 174
      have h₂₁ := h₄ 186
      have h₂₂ := h₄ 198
      have h₂₃ := h₄ 210
      norm_num [Nat.mod_eq_of_lt] at *
      <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.even_iff, Nat.odd_iff]
            <;> omega
          })
    have h₇ : Even (d 2023) := by
      rw [even_iff_two_dvd]
      have h₅ := h₄ 2023
      have h₆ := h₄ 7
      have h₇ := h₄ 19
      have h₈ := h₄ 31
      have h₉ := h₄ 43
      have h₁₀ := h₄ 55
      have h₁₁ := h₄ 67
      have h₁₂ := h₄ 79
      have h₁₃ := h₄ 91
      have h₁₄ := h₄ 103
      have h₁₅ := h₄ 115
      have h₁₆ := h₄ 127
      have h₁₇ := h₄ 139
      have h₁₈ := h₄ 151
      have h₁₉ := h₄ 163
      have h₂₀ := h₄ 175
      have h₂₁ := h₄ 187
      have h₂₂ := h₄ 199
      have h₂₃ := h₄ 211
      norm_num [Nat.mod_eq_of_lt] at *
      <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.even_iff, Nat.odd_iff]
            <;> omega
          })
    exact ⟨h₅, h₆, h₇⟩
  exact h_main
```

### epfl-43586 — EPFL136-HB200k

not_computable: Real.logb/log equations. symbolic nlinarith/definitional equality; no closed computable hot region.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem aime_1984_p5 (a b : ℝ) (h₀ : Real.logb 8 a + Real.logb 4 (b ^ 2) = 5)
  (h₁ : Real.logb 8 b + Real.logb 4 (a ^ 2) = 7) : a * b = 512 := by
  have h₂ : Real.logb 8 a = Real.log a / Real.log 8 := by
    rw [Real.logb]
    <;>
    simp [Real.logb]
    <;>
    ring
    <;>
    field_simp
    <;>
    ring
  have h₃ : Real.logb 4 (b ^ 2) = 2 * Real.log b / Real.log 4 := by
    have h₃ : Real.logb 4 (b ^ 2) = Real.log (b ^ 2) / Real.log 4 := by
      rw [Real.logb]
      <;>
      simp [Real.logb]
      <;>
      ring
      <;>
      field_simp
      <;>
      ring
    rw [h₃]
    have h₄ : Real.log (b ^ 2) = 2 * Real.log b := by
      rw [Real.log_pow]
      <;>
      ring
      <;>
      norm_num
    rw [h₄]
    <;>
    ring
    <;>
    field_simp
    <;>
    ring
  have h₄ : Real.logb 8 b = Real.log b / Real.log 8 := by
    rw [Real.logb]
    <;>
    simp [Real.logb]
    <;>
    ring
    <;>
    field_simp
    <;>
    ring
  have h₅ : Real.logb 4 (a ^ 2) = 2 * Real.log a / Real.log 4 := by
    have h₅ : Real.logb 4 (a ^ 2) = Real.log (a ^ 2) / Real.log 4 := by
      rw [Real.logb]
      <;> simp [Real.logb]
      <;> ring
      <;> field_simp
      <;> ring
    rw [h₅]
    have h₆ : Real.log (a ^ 2) = 2 * Real.log a := by
      rw [Real.log_pow] <;> ring
      <;> norm_num
    rw [h₆]
    <;> ring
    <;> field_simp
    <;> ring
  have h₆ : Real.log 8 = Real.log (2 ^ 3) := by
    norm_num
    <;>
    rfl
  have h₇ : Real.log 4 = Real.log (2 ^ 2) := by
    norm_num
    <;>
    rfl
  have h₈ : Real.log 8 = 3 * Real.log 2 := by
    have h₈ : Real.log 8 = Real.log (2 ^ 3) := h₆
    have h₉ : Real.log (2 ^ 3) = 3 * Real.log 2 := by
      rw [Real.log_pow]
      <;> norm_num
    linarith
  have h₉ : Real.log 4 = 2 * Real.log 2 := by
    have h₉ : Real.log 4 = Real.log (2 ^ 2) := by rw [h₇]
    have h₁₀ : Real.log (2 ^ 2) = 2 * Real.log 2 := by
      rw [Real.log_pow] <;> norm_num
    linarith
  have h₁₀ : Real.logb 8 a + Real.logb 4 (b ^ 2) = 5 := by
    exact h₀
  have h₁₁ : Real.logb 8 b + Real.logb 4 (a ^ 2) = 7 := by
    exact h₁
  have h₁₂ : Real.log a + 3 * Real.log b = 15 * Real.log 2 := by
    have h₁₂ : Real.logb 8 a + Real.logb 4 (b ^ 2) = 5 := h₁₀
    have h₁₃ : Real.logb 8 a = Real.log a / Real.log 8 := h₂
    have h₁₄ : Real.logb 4 (b ^ 2) = 2 * Real.log b / Real.log 4 := h₃
    have h₁₅ : Real.log 8 = 3 * Real.log 2 := h₈
    have h₁₆ : Real.log 4 = 2 * Real.log 2 := h₉
    have h₁₇ : Real.logb 8 a + Real.logb 4 (b ^ 2) = 5 := h₁₀
    have h₁₈ : Real.logb 8 a = Real.log a / Real.log 8 := h₂
    have h₁₉ : Real.logb 4 (b ^ 2) = 2 * Real.log b / Real.log 4 := h₃
    rw [h₁₈, h₁₉] at h₁₇
    have h₂₀ : (Real.log a / Real.log 8) + (2 * Real.log b / Real.log 4) = 5 := by linarith
    have h₂₁ : Real.log 8 = 3 * Real.log 2 := h₈
    have h₂₂ : Real.log 4 = 2 * Real.log 2 := h₉
    rw [h₂₁, h₂₂] at h₂₀
    have h₂₃ : (Real.log a / (3 * Real.log 2)) + (2 * Real.log b / (2 * Real.log 2)) = 5 := by simpa [h₁₅, h₁₆] using h₂₀
    have h₂₄ : Real.log 2 > 0 := Real.log_pos (by norm_num)
    have h₂₅ : Real.log a / (3 * Real.log 2) + (2 * Real.log b / (2 * Real.log 2)) = 5 := by simpa [h₁₅, h₁₆] using h₂₃
    have h₂₆ : Real.log a / (3 * Real.log 2) + (Real.log b / Real.log 2) = 5 := by
      have h₂₇ : 2 * Real.log b / (2 * Real.log 2) = Real.log b / Real.log 2 := by
        field_simp
        <;> ring
        <;> field_simp [h₂₄.ne']
        <;> ring
      rw [h₂₇] at h₂₅
      exact h₂₅
    have h₂₇ : Real.log a / (3 * Real.log 2) + Real.log b / Real.log 2 = 5 := by simpa using h₂₆
    have h₂₈ : Real.log a + 3 * Real.log b = 15 * Real.log 2 := by
      have h₂₉ : Real.log 2 > 0 := Real.log_pos (by norm_num)
      field_simp at h₂₇
      nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)]
    exact h₂₈
  have h₁₃ : Real.log b + 3 * Real.log a = 21 * Real.log 2 := by
    have h₁₃ : Real.logb 8 b + Real.logb 4 (a ^ 2) = 7 := h₁₁
    have h₁₄ : Real.logb 8 b = Real.log b / Real.log 8 := h₄
    have h₁₅ : Real.logb 4 (a ^ 2) = 2 * Real.log a / Real.log 4 := h₅
    have h₁₆ : Real.log 8 = 3 * Real.log 2 := h₈
    have h₁₇ : Real.log 4 = 2 * Real.log 2 := h₉
    have h₁₈ : Real.logb 8 b + Real.logb 4 (a ^ 2) = 7 := h₁₁
    rw [h₁₄, h₁₅] at h₁₈
    have h₁₉ : (Real.log b / Real.log 8) + (2 * Real.log a / Real.log 4) = 7 := by linarith
    rw [h₁₆, h₁₇] at h₁₉
    have h₂₀ : Real.log 2 > 0 := Real.log_pos (by norm_num)
    have h₂₁ : (Real.log b / (3 * Real.log 2)) + (2 * Real.log a / (2 * Real.log 2)) = 7 := by simpa [h₁₆, h₁₇] using h₁₉
    have h₂₂ : (Real.log b / (3 * Real.log 2)) + (Real.log a / Real.log 2) = 7 := by
      have h₂₃ : 2 * Real.log a / (2 * Real.log 2) = Real.log a / Real.log 2 := by
        field_simp
        <;> ring
        <;> field_simp [h₂₀.ne']
        <;> ring
      rw [h₂₃] at h₂₁
      exact h₂₁
    have h₂₃ : Real.log b + 3 * Real.log a = 21 * Real.log 2 := by
      have h₂₄ : Real.log 2 > 0 := Real.log_pos (by norm_num)
      field_simp at h₂₂
      nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)]
    exact h₂₃
  have h₁₄ : Real.log a = 6 * Real.log 2 := by
    have h₁₄ : Real.log a + 3 * Real.log b = 15 * Real.log 2 := h₁₂
    have h₁₅ : Real.log b + 3 * Real.log a = 21 * Real.log 2 := h₁₃
    have h₁₆ : Real.log 2 > 0 := Real.log_pos (by norm_num)
    have h₁₇ : Real.log a = 6 * Real.log 2 := by
      have h₁₈ : Real.log b = 3 * Real.log 2 := by
        nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)]
      nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)]
    exact h₁₇
  have h₁₅ : Real.log b = 3 * Real.log 2 := by
    have h₁₅ : Real.log b + 3 * Real.log a = 21 * Real.log 2 := h₁₃
    have h₁₆ : Real.log a = 6 * Real.log 2 := h₁₄
    have h₁₇ : Real.log b = 3 * Real.log 2 := by
      nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)]
    exact h₁₇
  have h₁₆ : a = 2 ^ 6 := by
    have h₁₆ : Real.log a = 6 * Real.log 2 := h₁₄
    have h₁₇ : a > 0 := by
      by_contra h
      have h₁₈ : a ≤ 0 := by linarith
      have h₁₉ : Real.log a ≤ 0 := by
        apply Real.log_nonpos
        <;> nlinarith
      nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)]
    have h₂₀ : Real.log a = 6 * Real.log 2 := h₁₄
    have h₂₁ : Real.log a = Real.log (2 ^ 6) := by
      have h₂₂ : Real.log (2 ^ 6) = 6 * Real.log 2 := by
        rw [Real.log_pow]
        <;> ring_nf
        <;> norm_num
      linarith
    have h₂₂ : a = 2 ^ 6 := by
      apply Real.log_injOn_pos (Set.mem_Ioi.mpr h₁₇) (Set.mem_Ioi.mpr (by positivity))
      linarith
    exact h₂₂
  have h₁₇ : b = 2 ^ 3 := by
    have h₁₇ : Real.log b = 3 * Real.log 2 := h₁₅
    have h₁₈ : b > 0 := by
      by_contra h
      have h₁₉ : b ≤ 0 := by linarith
      have h₂₀ : Real.log b ≤ 0 := by
        apply Real.log_nonpos
        <;> nlinarith
      nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)]
    have h₂₁ : Real.log b = 3 * Real.log 2 := h₁₅
    have h₂₂ : Real.log b = Real.log (2 ^ 3) := by
      have h₂₃ : Real.log (2 ^ 3) = 3 * Real.log 2 := by
        rw [Real.log_pow] <;> ring_nf <;> norm_num
      linarith
    have h₂₃ : b = 2 ^ 3 := by
      apply Real.log_injOn_pos (Set.mem_Ioi.mpr h₁₈) (Set.mem_Ioi.mpr (by positivity))
      linarith
    exact h₂₃
  have h₁₈ : a * b = 512 := by
    rw [h₁₆, h₁₇]
    <;> norm_num
    <;> ring_nf
    <;> norm_num
    <;>
    (try
      norm_num)
    <;>
    (try
      linarith [Real.log_pos (by norm_num : (1 : ℝ) < 2)])
    <;>
    (try
      simp_all [Real.logb, Real.log_pow])
    <;>
    (try
      ring_nf at * <;>
      nlinarith [Real.log_pos (by norm_num : (1 : ℝ) < 2), Real.log_pos (by norm_num : (1 : ℝ) < 2)])
  rw [h₁₈]
  <;> norm_num
```

### epfl-53843 — EPFL136-HB200k

not_computable: symbolic Real.sqrt inequalities. nlinarith Simplex timeout; closed extraction inapplicable.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem imo_1962_p2 (x : ℝ) (h₀ : 0 ≤ 3 - x) (h₁ : 0 ≤ x + 1)
    (h₂ : 1 / 2 < Real.sqrt (3 - x) - Real.sqrt (x + 1)) : -1 ≤ x ∧ x < 1 - Real.sqrt 31 / 8 := by
  have h_neg_one_le_x : -1 ≤ x := by
    by_contra! h
    have h₃ : x + 1 ≤ 0 := by linarith
    have h₄ : Real.sqrt (x + 1) = 0 := by
      rw [Real.sqrt_eq_zero_of_nonpos] <;> linarith
    have h₅ : Real.sqrt (3 - x) ≥ 0 := Real.sqrt_nonneg (3 - x)
    nlinarith [Real.sqrt_nonneg (3 - x)]
  have h_x_lt : x < 1 - Real.sqrt 31 / 8 := by
    have h₃ : 1 / 2 < Real.sqrt (3 - x) - Real.sqrt (x + 1) := h₂
    have h₄ : Real.sqrt (3 - x) ≥ 0 := Real.sqrt_nonneg (3 - x)
    have h₅ : Real.sqrt (x + 1) ≥ 0 := Real.sqrt_nonneg (x + 1)
    have h₆ : Real.sqrt (3 - x) - Real.sqrt (x + 1) > 1 / 2 := by linarith
    have h₇ : x ≤ 3 := by linarith
    have h₈ : x ≥ -1 := by linarith
    have h₉ : (Real.sqrt (3 - x) - Real.sqrt (x + 1)) ^ 2 > (1 / 2) ^ 2 := by
      nlinarith [Real.sq_sqrt (show 0 ≤ 3 - x by linarith), Real.sq_sqrt (show 0 ≤ x + 1 by linarith)]
    have h₁₀ : 4 - 2 * Real.sqrt (3 - x) * Real.sqrt (x + 1) > 1 / 4 := by
      nlinarith [Real.sq_sqrt (show 0 ≤ 3 - x by linarith), Real.sq_sqrt (show 0 ≤ x + 1 by linarith)]
    have h₁₁ : 15 > 2 * Real.sqrt (3 - x) * Real.sqrt (x + 1) := by
      nlinarith [Real.sq_sqrt (show 0 ≤ 3 - x by linarith), Real.sq_sqrt (show 0 ≤ x + 1 by linarith)]
    have h₁₂ : 16 * x ^ 2 - 28 * x + 1 > 0 := by
      nlinarith [Real.sq_sqrt (show 0 ≤ 3 - x by linarith), Real.sq_sqrt (show 0 ≤ x + 1 by linarith),
        Real.sqrt_nonneg (3 - x), Real.sqrt_nonneg (x + 1),
        sq_nonneg (Real.sqrt (3 - x) - 2), sq_nonneg (Real.sqrt (x + 1) - 7 / 4),
        sq_nonneg (Real.sqrt (3 - x) - 7 / 4), sq_nonneg (Real.sqrt (x + 1) - 2)]
    have h₁₃ : x < 1 - Real.sqrt 31 / 8 := by
      by_contra! h₁₄
      have h₁₅ : x ≥ 1 - Real.sqrt 31 / 8 := by linarith
      have h₁₆ : 16 * x ^ 2 - 28 * x + 1 ≤ 0 := by
        nlinarith [Real.sqrt_nonneg 31, Real.sq_sqrt (show 0 ≤ 31 by norm_num),
          Real.sqrt_nonneg (3 - x), Real.sqrt_nonneg (x + 1),
          sq_nonneg (x - (7 - 3 * Real.sqrt 5) / 8),
          sq_nonneg (x - (7 + 3 * Real.sqrt 5) / 8)]
      nlinarith
    exact h₁₃
  exact ⟨h_neg_one_le_x, h_x_lt⟩
```

### epfl-58867 — EPFL136-HB200k

not_closed: arbitrary-dimensional Euclidean vector construction. aesop/type/elaboration failures; finite dimension is symbolic.

```lean
import Mathlib
set_option maxHeartbeats 800000
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
theorem exercise_1_18a
  (n : ℕ)
  (h : n > 1)
  (x : EuclideanSpace ℝ (Fin n))
  : ∃ (y : EuclideanSpace ℝ (Fin n)), y ≠ 0 ∧ (inner x y) = (0 : ℝ) := by
  have h_main : ∃ (y : EuclideanSpace ℝ (Fin n)), y ≠ 0 ∧ (inner x y) = (0 : ℝ) := by
    by_cases hx : x = 0
    · 
      use ![1, 0]
      constructor
      · 
        intro h
        have h₁ := congr_fun h 0
        have h₂ := congr_fun h 1
        simp [Function.funext_iff, Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ,
          Fin.val_zero, Fin.val_one] at h₁ h₂ ⊢
        <;> norm_num at h₁ h₂ ⊢ <;> aesop
      · 
        simp [hx, inner_zero_left, Fin.sum_univ_succ]
        <;>
        aesop
    · 
      use fun i => if i = 0 then x 1 else -x 0
      constructor
      · 
        intro h
        have h₁ := congr_fun h 0
        have h₂ := congr_fun h 1
        have h₃ : x ≠ 0 := hx
        simp [Function.funext_iff, Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ,
          Fin.val_zero, Fin.val_one] at h₁ h₂ ⊢
        <;>
        (try simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]) <;>
        (try
          {
            norm_num at *
            <;>
            (try
              {
                aesop
              })
            <;>
            (try
              {
                simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]
                <;>
                aesop
              })
          }) <;>
        (try
          {
            aesop
          })
        <;>
        (try
          {
            simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]
            <;>
            aesop
          })
      · 
        simp [inner_apply, Fin.sum_univ_succ, Fin.val_zero, Fin.val_one]
        <;>
        by_cases h₁ : n = 0 <;>
        simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]
        <;>
        (try ring_nf) <;>
        (try aesop) <;>
        (try
          {
            simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]
            <;>
            aesop
          })
        <;>
        (try
          {
            aesop
          })
        <;>
        (try
          {
            norm_num at *
            <;>
            aesop
          })
        <;>
        (try
          {
            simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]
            <;>
            aesop
          })
        <;>
        (try
          {
            aesop
          })
        <;>
        (try
          {
            simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]
            <;>
            aesop
          })
        <;>
        (try
          {
            aesop
          })
        <;>
        (try
          {
            simp_all [Fin.forall_fin_succ, Matrix.cons_val_zero, Matrix.cons_val_succ, Fin.val_zero, Fin.val_one]
            <;>
            aesop
          })
        <;>
        (try
          {
            aesop
          })
  exact h_main
```

### epfl-31023 — EPFL136-HB200k

closed_potential: odd product below10000 vs factorial quotient. rfl reaches recursion depth; structural product/factorial and proved equivalence could apply, no prototype for huge integer kernel cost.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem amc12_2001_p5 :
    Finset.prod (Finset.filter (fun x => ¬Even x) (Finset.range 10000)) (id : ℕ → ℕ) =
      10000! / (2 ^ 5000 * 5000!) := by
  have h₁ : Finset.prod (Finset.filter (fun x => ¬Even x) (Finset.range 10000)) (id : ℕ → ℕ) = 10000! / (2 ^ 5000 * 5000!) := by
    have h₂ : Finset.prod (Finset.filter (fun x => ¬Even x) (Finset.range 10000)) (id : ℕ → ℕ) = ∏ k in Finset.filter (fun x => ¬Even x) (Finset.range 10000), k := by
      simp [Finset.prod_const]
    rw [h₂]
    have h₃ : ∏ k in Finset.filter (fun x => ¬Even x) (Finset.range 10000), k = 10000! / (2 ^ 5000 * 5000!) := by
      have h₄ : ∏ k in Finset.filter (fun x => ¬Even x) (Finset.range 10000), k = 10000! / (2 ^ 5000 * 5000!) := by
        rw [show (∏ k in Finset.filter (fun x => ¬Even x) (Finset.range 10000), k) = 10000! / (2 ^ 5000 * 5000!) by
          rfl]
      exact h₄
    rw [h₃]
  exact h₁
```

### epfl-27729 — EPFL136-HB200k

bridge_required: Int recurrence determines positive indices. attempted periodicity proof has prior error on free x0; extraction requires a new proved recurrence bridge and may repair the proof.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem aimeII_2001_p3 (x : ℕ → ℤ) (h₀ : x 1 = 211) (h₂ : x 2 = 375) (h₃ : x 3 = 420) (h₄ : x 4 = 523) (h₆ : ∀ n ≥ 5, x n = x (n - 1) - x (n - 2) + x (n - 3) - x (n - 4)) :
  x 531 + x 753 + x 975 = 898 := by
  have h_periodic : ∀ n, x (n + 10) = x n := by
    intro n
    induction n using Nat.strong_induction_on with
    | h n ih =>
      match n with
      | 0 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 1 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 2 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 3 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 4 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 5 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 6 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 7 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 8 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | 9 =>
        norm_num [h₀, h₂, h₃, h₄, h₆] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            (try omega) <;>
            (try ring_nf at * <;> omega) <;>
            (try linarith)
          }) <;>
        (try
          {
            simp_all [Nat.add_assoc]
            <;>
            omega
          })
        <;>
        omega
      | n + 10 =>
        have h₁ := ih n (by omega)
        have h₂ := ih (n + 1) (by omega)
        have h₃ := ih (n + 2) (by omega)
        have h₄ := ih (n + 3) (by omega)
        have h₅ := ih (n + 4) (by omega)
        have h₆ := ih (n + 5) (by omega)
        have h₇ := ih (n + 6) (by omega)
        have h₈ := ih (n + 7) (by omega)
        have h₉ := ih (n + 8) (by omega)
        have h₁₀ := ih (n + 9) (by omega)
        simp [Nat.add_assoc] at *
        <;>
        (try omega) <;>
        (try
          {
            simp_all [h₆, Nat.add_assoc]
            <;>
            ring_nf at *
            <;>
            omega
          }) <;>
        (try
          {
            omega
          }) <;>
        (try
          {
            linarith
          }) <;>
        (try
          {
            simp_all [h₆, Nat.add_assoc]
            <;>
            ring_nf at *
            <;>
            omega
          })
  have h_x531 : x 531 = 211 := by
    have h₁ : x 531 = 211 := by
      have h₂ : x 531 = x 1 := by
        have h₃ : x 531 = x 1 := by
          have h₄ : x 531 = x (1 + 10 * 53) := by norm_num
          rw [h₄]
          have h₅ : x (1 + 10 * 53) = x 1 := by
            rw [show 1 + 10 * 53 = 1 + 10 * 53 by rfl]
            rw [show 1 + 10 * 53 = 1 + 10 * 53 by rfl]
            have h₆ : ∀ n : ℕ, x (1 + 10 * n) = x 1 := by
              intro n
              induction n with
              | zero => simp [h₀]
              | succ n ih =>
                have h₇ := h_periodic (1 + 10 * n)
                simp [Nat.mul_add, Nat.add_mul, Nat.add_assoc] at *
                <;> simp_all [Nat.mul_add, Nat.add_mul, Nat.add_assoc]
                <;> ring_nf at *
                <;> omega
            exact h₆ 53
          rw [h₅]
        exact h₃
      rw [h₂]
      <;> simp [h₀]
    exact h₁
  have h_x753 : x 753 = 420 := by
    have h₁ : x 753 = 420 := by
      have h₂ : x 753 = x 3 := by
        have h₃ : x 753 = x (3 + 10 * 75) := by norm_num
        rw [h₃]
        have h₄ : x (3 + 10 * 75) = x 3 := by
          rw [show 3 + 10 * 75 = 3 + 10 * 75 by rfl]
          rw [show 3 + 10 * 75 = 3 + 10 * 75 by rfl]
          have h₅ : ∀ n : ℕ, x (3 + 10 * n) = x 3 := by
            intro n
            induction n with
            | zero => simp [h₃, h₀, h₂, h₄]
            | succ n ih =>
              have h₆ := h_periodic (3 + 10 * n)
              simp [Nat.mul_add, Nat.add_mul, Nat.add_assoc] at *
              <;> simp_all [Nat.mul_add, Nat.add_mul, Nat.add_assoc]
              <;> ring_nf at *
              <;> omega
          exact h₅ 75
        rw [h₄]
      rw [h₂]
      <;> simp [h₃]
    exact h₁
  have h_x975 : x 975 = 267 := by
    have h₁ : x 975 = 267 := by
      have h₂ : x 975 = x 5 := by
        have h₃ : x 975 = x (5 + 10 * 97) := by norm_num
        rw [h₃]
        have h₄ : x (5 + 10 * 97) = x 5 := by
          rw [show 5 + 10 * 97 = 5 + 10 * 97 by rfl]
          rw [show 5 + 10 * 97 = 5 + 10 * 97 by rfl]
          have h₅ : ∀ n : ℕ, x (5 + 10 * n) = x 5 := by
            intro n
            induction n with
            | zero => simp [h₀, h₂, h₃, h₄, h₆]
            | succ n ih =>
              have h₆ := h_periodic (5 + 10 * n)
              simp [Nat.mul_add, Nat.add_mul, Nat.add_assoc] at *
              <;> simp_all [Nat.mul_add, Nat.add_mul, Nat.add_assoc]
              <;> ring_nf at *
              <;> omega
          exact h₅ 97
        rw [h₄]
      rw [h₂]
      <;> simp [h₀, h₂, h₃, h₄, h₆]
      <;> norm_num
      <;> omega
    exact h₁
  have h_sum : x 531 + x 753 + x 975 = 898 := by
    rw [h_x531, h_x753, h_x975]
    <;> norm_num
    <;> rfl
  exact h_sum
```

### epfl-2994 — EPFL136-HB200k

closed_potential: 942! modulo15^233 and5^234. rfl reaches recursion depth; big-integer modular evaluator certificate not implemented.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem mathd_numbertheory_43 : IsGreatest { n : ℕ | 15 ^ n ∣ 942! } 233 := by
  have h_main₁ : 15 ^ 233 ∣ 942! := by
    apply Nat.dvd_of_mod_eq_zero
    rfl
  have h_main₂ : ∀ (n : ℕ), n ∈ { n : ℕ | 15 ^ n ∣ 942! } → n ≤ 233 := by
    intro n hn
    have h₁ : 15 ^ n ∣ 942! := by simpa using hn
    have h₂ : n ≤ 233 := by
      by_contra h
      have h₃ : n ≥ 234 := by
        omega
      have h₄ : 15 ^ n ∣ 942! := h₁
      have h₅ : 5 ^ n ∣ 942! := by
        exact dvd_trans (by
          exact dvd_pow (by norm_num) (by omega)
          ) h₄
      have h₆ : ¬(5 ^ 234 ∣ 942!) := by
        norm_num [Nat.dvd_iff_mod_eq_zero, Nat.factorial_succ, Nat.pow_succ, Nat.mul_assoc]
        <;> rfl
      have h₇ : 5 ^ 234 ∣ 5 ^ n := by
        apply pow_dvd_pow _
        omega
      have h₈ : 5 ^ n ∣ 942! := h₅
      have h₉ : 5 ^ 234 ∣ 942! := dvd_trans h₇ h₈
      exact h₆ h₉
    exact h₂
  have h_final : IsGreatest { n : ℕ | 15 ^ n ∣ 942! } 233 := by
    refine' ⟨h_main₁, _⟩
    intro n hn
    have h₁ : n ≤ 233 := h_main₂ n hn
    exact h₁
  exact h_final
```

### epfl-1576 — EPFL136-HB200k

not_computable: bounded sums of floor(Real.logb2 k). Real.logb has no executable instance; a proved integer log equivalence would be a new bridge, not current closed code.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem aime_1994_p4 (n : ℕ) (h₀ : 0 < n)
  (h₁ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) = 1994) : n = 312 := by
  have h₂ : n = 312 := by
    have h₃ : n ≤ 512 := by
      by_contra! h
      have h₄ : n ≥ 513 := by linarith
      have h₅ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) > 1994 := by
        have h₆ : ∀ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k) ≥ 0 := by
          intro k hk
          have h₇ : (1 : ℝ) ≤ (k : ℝ) := by
            have h₈ : 1 ∈ Finset.Icc 1 n := by
              apply Finset.mem_Icc.mpr
              <;> norm_num <;>
                (try omega) <;>
                (try linarith)
            have h₉ : (k : ℕ) ∈ Finset.Icc 1 n := hk
            have h₁₀ : 1 ≤ (k : ℕ) := by
              simp [Finset.mem_Icc] at h₉
              linarith
            exact_mod_cast h₁₀
          have h₁₁ : Real.logb 2 (k : ℝ) = Real.log (k : ℝ) / Real.log 2 := by
            simp [Real.logb]
          have h₁₂ : Real.logb 2 (k : ℝ) ≥ 0 := by
            have h₁₃ : Real.log (k : ℝ) ≥ 0 := by
              apply Real.log_nonneg
              <;> norm_num at h₇ ⊢ <;>
                (try omega) <;>
                (try linarith)
            have h₁₄ : Real.log 2 > 0 := Real.log_pos (by norm_num)
            have h₁₅ : Real.log (k : ℝ) / Real.log 2 ≥ 0 := by
              exact div_nonneg h₁₃ (le_of_lt h₁₄)
            linarith
          have h₁₆ : Int.floor (Real.logb 2 (k : ℝ)) ≥ 0 := by
            have h₁₇ : (Int.floor (Real.logb 2 (k : ℝ)) : ℝ) ≤ Real.logb 2 (k : ℝ) := by
              exact Int.floor_le (Real.logb 2 (k : ℝ))
            have h₁₈ : (Int.floor (Real.logb 2 (k : ℝ)) : ℝ) ≥ 0 := by
              linarith
            exact_mod_cast h₁₈
          simpa [Real.logb] using h₁₆
        have h₇ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) ≥ (∑ k in Finset.Icc 1 n, 0 : ℤ) := by
          apply Finset.sum_le_sum
          intro k hk
          exact h₆ k hk
        have h₈ : (∑ k in Finset.Icc 1 n, (0 : ℤ)) = 0 := by
          simp
        have h₉ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) ≥ 0 := by
          linarith
        have h₁₀ : (∑ k ∈ Finset.Icc 1 512, Int.floor (Real.logb 2 k)) = 4096 := by
          rfl
        have h₁₁ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) ≥ (∑ k ∈ Finset.Icc 1 512, Int.floor (Real.logb 2 k)) := by
          have h₁₂ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) ≥ (∑ k ∈ Finset.Icc 1 512, Int.floor (Real.logb 2 k)) := by
            have h₁₃ : (∑ k ∈ Finset.Icc 1 512, Int.floor (Real.logb 2 k)) ≤ (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) := by
              have h₁₄ : (∑ k ∈ Finset.Icc 1 512, Int.floor (Real.logb 2 k)) ≤ (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) := by
                apply Finset.sum_le_sum_of_subset_of_nonneg
                · intro x hx
                  simp only [Finset.mem_Icc] at hx ⊢
                  <;>
                    (try omega) <;>
                    (try
                      {
                        norm_num at hx ⊢
                        <;>
                        (try omega)
                      }) <;>
                    (try
                      {
                        linarith
                      })
                · intro x _ _
                  have h₁₅ : (Int.floor (Real.logb 2 x) : ℤ) ≥ 0 := by
                    have h₁₆ : (1 : ℝ) ≤ (x : ℝ) := by
                      have h₁₇ : 1 ∈ Finset.Icc 1 n := by
                        apply Finset.mem_Icc.mpr
                        <;> norm_num <;>
                          (try omega) <;>
                          (try linarith)
                      have h₁₈ : (x : ℕ) ∈ Finset.Icc 1 n := by simpa using hx
                      have h₁₉ : 1 ≤ (x : ℕ) := by
                        simp [Finset.mem_Icc] at h₁₈
                        linarith
                      exact_mod_cast h₁₉
                    have h₂₀ : Real.logb 2 (x : ℝ) = Real.log (x : ℝ) / Real.log 2 := by
                      simp [Real.logb]
                    have h₂₁ : Real.logb 2 (x : ℝ) ≥ 0 := by
                      have h₂₂ : Real.log (x : ℝ) ≥ 0 := by
                        apply Real.log_nonneg
                        <;> norm_num at h₁₆ ⊢ <;>
                          (try omega) <;>
                          (try linarith)
                      have h₂₃ : Real.log 2 > 0 := Real.log_pos (by norm_num)
                      have h₂₄ : Real.log (x : ℝ) / Real.log 2 ≥ 0 := by
                        exact div_nonneg h₂₂ (le_of_lt h₂₃)
                      linarith
                    have h₂₅ : Int.floor (Real.logb 2 (x : ℝ)) ≥ 0 := by
                      have h₂₆ : (Int.floor (Real.logb 2 (x : ℝ)) : ℝ) ≤ Real.logb 2 (x : ℝ) := by
                        exact Int.floor_le (Real.logb 2 (x : ℝ))
                      have h₂₇ : (Int.floor (Real.logb 2 (x : ℝ)) : ℝ) ≥ 0 := by
                        linarith
                      exact_mod_cast h₂₇
                    simpa [Real.logb] using h₂₅
                  exact by
                    simpa [Real.logb] using h₁₅
              exact h₁₄
            linarith
          linarith
        have h₁₂ : (∑ k ∈ Finset.Icc 1 512, Int.floor (Real.logb 2 k)) = 4096 := by
          rfl
        have h₁₃ : (∑ k ∈ Finset.Icc 1 n, Int.floor (Real.logb 2 k)) ≥ 4096 := by
          linarith
        linarith
      linarith
    interval_cases n <;> norm_num [Finset.sum_Icc_succ_top, Int.floor_eq_iff, Real.logb_eq_iff_rpow_eq] at h₁ ⊢ <;>
      (try contradiction) <;>
      (try norm_num at h₁ ⊢) <;>
      (try linarith) <;>
      (try
        {
          simp_all [Finset.sum_Icc_succ_top, Int.floor_eq_iff, Real.logb_eq_iff_rpow_eq]
          <;> norm_num at *
          <;> linarith
        })
  exact h₂
```

### epfl-6919 — EPFL136-HB200k

closed_potential: finite rational harmonic sum embedded in Real. recursion-depth at norm_num sum expansion; rational embedding equivalence required, unsupported by current Nat-only prototypes.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem imo_1979_p1 (p q : ℕ) (h₀ : 0 < q)
  (h₁ : (∑ k ∈ Finset.Icc (1 : ℕ) 1319, (-1 : ℝ) ^ (k + 1) * ((1 : ℝ) / k)) = p / q) : 1979 ∣ p := by
  have h₂ : 1979 ∣ p := by
    norm_num [Finset.sum_Icc_succ_top] at h₁
    <;>
    (try contradiction) <;>
    (try norm_num at h₁) <;>
    (try
      {
        field_simp [h₀.ne'] at h₁
        ring_nf at h₁
        norm_cast at h₁
        <;>
        (try omega) <;>
        (try
          {
            norm_num at h₁
            <;>
            ring_nf at h₁
            <;>
            norm_cast at h₁
            <;>
            omega
          })
      }) <;>
    (try
      {
        norm_num at h₁
        <;>
        ring_nf at h₁
        <;>
        norm_cast at h₁
        <;>
        omega
      })
    <;>
    (try
      {
        norm_num at h₁ ⊢
        <;>
        ring_nf at h₁ ⊢
        <;>
        norm_cast at h₁ ⊢
        <;>
        omega
      })
    <;>
    (try
      {
        norm_num [Finset.sum_Icc_succ_top] at h₁ ⊢
        <;>
        ring_nf at h₁ ⊢
        <;>
        norm_cast at h₁ ⊢
        <;>
        omega
      })
  exact h₂
```

### epfl-47766 — EPFL136-HB200k

bridge_required: Complex.I finite sum after an unproved n bound. can in principle reduce to integer pairs but actual timeout precedes finite enumeration in symbolic proof.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem amc12a_2009_p15 (n : ℕ) (h₀ : 0 < n)
  (h₁ : (∑ k ∈ Finset.Icc 1 n, ↑k * Complex.I ^ k) = 48 + 49 * Complex.I) : n = 97 := by
  have h_main : n = 97 := by
    have h₂ : n = 97 := by
      have h₃ := h₁
      have h₄ : n ≤ 97 := by
        by_contra! h
        have h₅ : n ≥ 98 := by linarith
        have h₆ : (∑ k ∈ Finset.Icc 1 n, (k : ℂ) * Complex.I ^ k) ≠ 48 + 49 * Complex.I := by
          have h₇ : n ≥ 98 := by linarith
          have h₈ : (∑ k ∈ Finset.Icc 1 n, (k : ℂ) * Complex.I ^ k) ≠ 48 + 49 * Complex.I := by
            intro h₉
            have h₁₀ : n ≥ 98 := by linarith
            have h₁₁ : (∑ k ∈ Finset.Icc 1 n, (k : ℂ) * Complex.I ^ k) = 48 + 49 * Complex.I := by simpa using h₉
            have h₁₂ : n ≤ 100 := by
              by_contra! h₁₃
              have h₁₄ : n ≥ 101 := by linarith
              have h₁₅ : (∑ k ∈ Finset.Icc 1 n, (k : ℂ) * Complex.I ^ k) ≠ 48 + 49 * Complex.I := by
                simp_all [Finset.sum_Icc_succ_top, Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three,
                  pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc]
                <;>
                  norm_num at * <;>
                  ring_nf at * <;>
                  norm_cast at * <;>
                  simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero,
                    mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc]
                <;>
                  norm_num at * <;>
                  (try omega) <;>
                  (try {
                    rcases n with (_ | _ | _ | _ | _ | _ | _ | _ | _ | _ | n) <;> simp_all [Finset.sum_Icc_succ_top, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
                      ring_nf at * <;> norm_cast at * <;> simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
                        norm_num at * <;> omega
                  }) <;>
                  (try {
                    rcases n with (_ | _ | _ | _ | _ | _ | _ | _ | _ | _ | n) <;> simp_all [Finset.sum_Icc_succ_top, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
                      ring_nf at * <;> norm_cast at * <;> simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
                        norm_num at * <;> omega
                  })
              aesop
            have h₁₆ : n ≤ 100 := by linarith
            interval_cases n <;> norm_num [Finset.sum_Icc_succ_top, Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] at h₁₁ ⊢ <;>
              simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
                norm_num at * <;>
                  (try omega) <;>
                  (try {
                    ring_nf at * <;>
                    norm_cast at * <;>
                    simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
                      norm_num at * <;>
                        omega
                  }) <;>
                  (try {
                    aesop
                  }) <;>
                  (try {
                    aesop
                  })
            <;> aesop
          exact h₈
        simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc]
        <;> aesop
      have h₅ : n ≤ 97 := by linarith
      interval_cases n <;> norm_num [Finset.sum_Icc_succ_top, Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] at h₁ ⊢ <;>
        simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
        norm_num at * <;>
        (try omega) <;>
        (try {
          ring_nf at * <;>
          norm_cast at * <;>
          simp_all [Complex.ext_iff, pow_add, pow_mul, pow_two, pow_three, pow_one, pow_zero, mul_one, mul_zero, add_zero, zero_add, mul_neg, mul_assoc] <;>
            norm_num at * <;>
            omega
        }) <;>
        (try {
          aesop
        }) <;>
        (try {
          aesop
        })
      <;> aesop
    exact h₂
  exact h_main
```

### epfl-47248 — EPFL136-HB200k

bridge_required: Int recurrence with fixed positive initial values. prior linarith error plus symbolic periodicity timeout; target extraction needs new bridge, no source-preserving claim.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem aimeII_2001_p3 (x : ℕ → ℤ) (h₀ : x 1 = 211) (h₂ : x 2 = 375) (h₃ : x 3 = 420)
  (h₄ : x 4 = 523) (h₆ : ∀ n ≥ 5, x n = x (n - 1) - x (n - 2) + x (n - 3) - x (n - 4)) :
  x 531 + x 753 + x 975 = 898 := by
  have h₇ : x 5 = 267 := by
    have h₇₁ : x 5 = x 4 - x 3 + x 2 - x 1 := by
      have h₇₂ := h₆ 5
      norm_num at h₇₂ ⊢
      <;> linarith
    rw [h₇₁]
    norm_num [h₀, h₂, h₃, h₄]
    <;> linarith
  have h₈ : x 6 = -211 := by
    have h₈₁ : x 6 = x 5 - x 4 + x 3 - x 2 := by
      have h₈₂ := h₆ 6
      norm_num at h₈₂ ⊢
      <;> linarith
    rw [h₈₁]
    norm_num [h₇, h₄, h₃, h₂]
    <;> linarith
  have h₉ : x 7 = -375 := by
    have h₉₁ : x 7 = x 6 - x 5 + x 4 - x 3 := by
      have h₉₂ := h₆ 7
      norm_num at h₉₂ ⊢
      <;> linarith
    rw [h₉₁]
    norm_num [h₈, h₇, h₄, h₃]
    <;> linarith
  have h₁₀ : x 8 = -420 := by
    have h₁₀₁ : x 8 = x 7 - x 6 + x 5 - x 4 := by
      have h₁₀₂ := h₆ 8
      norm_num at h₁₀₂ ⊢
      <;> linarith
    rw [h₁₀₁]
    norm_num [h₉, h₈, h₇, h₄]
    <;> linarith
  have h₁₁ : x 9 = -523 := by
    have h₁₁₁ : x 9 = x 8 - x 7 + x 6 - x 5 := by
      have h₁₁₂ := h₆ 9
      norm_num at h₁₁₂ ⊢
      <;> linarith
    rw [h₁₁₁]
    norm_num [h₁₀, h₉, h₈, h₇]
    <;> linarith
  have h₁₂ : x 10 = -267 := by
    have h₁₂₁ : x 10 = x 9 - x 8 + x 7 - x 6 := by
      have h₁₂₂ := h₆ 10
      norm_num at h₁₂₂ ⊢
      <;> linarith
    rw [h₁₂₁]
    norm_num [h₁₁, h₁₀, h₉, h₈]
    <;> linarith
  have h₁₃ : x 11 = 221 := by
    have h₁₃₁ : x 11 = x 10 - x 9 + x 8 - x 7 := by
      have h₁₃₂ := h₆ 11
      norm_num at h₁₃₂ ⊢
      <;> linarith
    rw [h₁₃₁]
    norm_num [h₁₂, h₁₁, h₁₀, h₉]
    <;> linarith
  have h₁₄ : x 12 = 385 := by
    have h₁₄₁ : x 12 = x 11 - x 10 + x 9 - x 8 := by
      have h₁₄₂ := h₆ 12
      norm_num at h₁₄₂ ⊢
      <;> linarith
    rw [h₁₄₁]
    norm_num [h₁₃, h₁₂, h₁₁, h₁₀]
    <;> linarith
  have h₁₅ : x 13 = 420 := by
    have h₁₅₁ : x 13 = x 12 - x 11 + x 10 - x 9 := by
      have h₁₅₂ := h₆ 13
      norm_num at h₁₅₂ ⊢
      <;> linarith
    rw [h₁₅₁]
    norm_num [h₁₄, h₁₃, h₁₂, h₁₁]
    <;> linarith
  have h₁₆ : x 14 = 523 := by
    have h₁₆₁ : x 14 = x 13 - x 12 + x 11 - x 10 := by
      have h₁₆₂ := h₆ 14
      norm_num at h₁₆₂ ⊢
      <;> linarith
    rw [h₁₆₁]
    norm_num [h₁₅, h₁₄, h₁₃, h₁₂]
    <;> linarith
  have h₁₇ : x 15 = 267 := by
    have h₁₇₁ : x 15 = x 14 - x 13 + x 12 - x 11 := by
      have h₁₇₂ := h₆ 15
      norm_num at h₁₇₂ ⊢
      <;> linarith
    rw [h₁₇₁]
    norm_num [h₁₆, h₁₅, h₁₄, h₁₃]
    <;> linarith
  have h₁₈ : x 531 = 420 := by
    have h₁₈₁ : x 531 = x 3 := by
      have h₁₈₂ : ∀ n : ℕ, x (12 * n + 3) = x 3 := by
        intro n
        induction n with
        | zero => simp [h₃]
        | succ n ih =>
          simp [Nat.mul_succ, h₆, ih]
          <;> ring_nf at * <;> omega
      have h₁₈₃ : 531 = 12 * 44 + 3 := by norm_num
      rw [h₁₈₃]
      exact h₁₈₂ 44
    rw [h₁₈₁]
    <;> simp [h₃]
    <;> ring_nf at * <;> omega
  have h₁₉ : x 753 = -523 := by
    have h₁₉₁ : x 753 = x 9 := by
      have h₁₉₂ : ∀ n : ℕ, x (12 * n + 9) = x 9 := by
        intro n
        induction n with
        | zero => simp [h₁₁]
        | succ n ih =>
          simp [Nat.mul_succ, h₆, ih]
          <;> ring_nf at * <;> omega
      have h₁₉₃ : 753 = 12 * 62 + 9 := by norm_num
      rw [h₁₉₃]
      exact h₁₉₂ 62
    rw [h₁₉₁]
    <;> simp [h₁₁]
    <;> ring_nf at * <;> omega
  have h₂₀ : x 975 = 420 := by
    have h₂₀₁ : x 975 = x 3 := by
      have h₂₀₂ : ∀ n : ℕ, x (12 * n + 3) = x 3 := by
        intro n
        induction n with
        | zero => simp [h₃]
        | succ n ih =>
          simp [Nat.mul_succ, h₆, ih]
          <;> ring_nf at * <;> omega
      have h₂₀₃ : 975 = 12 * 81 + 3 := by norm_num
      rw [h₂₀₃]
      exact h₂₀₂ 81
    rw [h₂₀₁]
    <;> simp [h₃]
    <;> ring_nf at * <;> omega
  have h₂₁ : x 531 + x 753 + x 975 = 898 := by
    rw [h₁₈, h₁₉, h₂₀]
    <;> norm_num
    <;> linarith
  linarith
```

### epfl-45746 — EPFL136-HB200k

not_closed: bounded sums but u2/u3 unconstrained. recurrence only constrains u(n+2) for n>=2; missing initial values prevent closed extraction.

```lean
import Mathlib
import Aesop
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
set_option maxHeartbeats 800000
open BigOperators Real Nat Topology Rat
theorem amc12a_2002_p21 (u : ℕ → ℕ) (h₀ : u 0 = 4) (h₁ : u 1 = 7)
    (h₂ : ∀ n ≥ 2, u (n + 2) = (u n + u (n + 1)) % 10) :
    ∀ n, (∑ k ∈ Finset.range n, u k) > 10000 → 1999 ≤ n := by
  have h_main : ∀ n, (∑ k ∈ Finset.range n, u k) > 10000 → 1999 ≤ n := by
    intro n hn
    have h₃ : 1999 ≤ n := by
      by_contra h
      have h₄ : n ≤ 1998 := by linarith
      have h₅ : n ≤ 1998 := by linarith
      have h₆ : (∑ k ∈ Finset.range n, u k) ≤ 10000 := by
        have h₇ : n ≤ 1998 := by linarith
        interval_cases n <;> norm_num [Finset.sum_range_succ, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod] at hn ⊢ <;>
          (try omega) <;>
          (try contradiction) <;>
          (try norm_num at hn ⊢) <;>
          (try omega) <;>
          (try
            {
              rcases n with (_ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | n) <;>
              simp_all [Finset.sum_range_succ, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod] <;>
              norm_num <;>
              omega
            }) <;>
          (try
            {
              rcases n with (_ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | n) <;>
              simp_all [Finset.sum_range_succ, h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod] <;>
              norm_num <;>
              omega
            })
        <;>
        omega
      linarith
    exact h₃
  exact h_main
```

### epfl-62942 — EPFLpending7-HB10k

not_closed: symbolic polynomial root sets. dependent elaboration/aesop; no numeric finite closed computation.

```lean
import Mathlib
set_option maxHeartbeats 800000
open Fintype Complex Polynomial LinearMap FiniteDimensional Module Module.End
open scoped BigOperators
open Fintype Complex Polynomial LinearMap FiniteDimensional Module Module.End
open scoped BigOperators
theorem exercise_4_4 (p : Polynomial ℂ) :
  p.degree = @card (rootSet p ℂ) (rootSetFintype p ℂ) ↔
  Disjoint
  (@card (rootSet p ℂ) (rootSetFintype p ℂ))
  (@card (rootSet (derivative p) ℂ) (rootSetFintype (derivative p) ℂ)) := by
  have h_main : p.degree = @card (rootSet p ℂ) (rootSetFintype p ℂ) ↔ Disjoint (@card (rootSet p ℂ) (rootSetFintype p ℂ)) (@card (rootSet (derivative p) ℂ) (rootSetFintype (derivative p) ℂ)) := by
    constructor
    · 
      intro h
      have h₁ := h
      simp_all [rootSet, Finset.disjoint_left, Finset.mem_coe, Set.mem_setOf_eq]
      <;>
      (try
        {
          cases p
          <;> simp_all [rootSet, Finset.disjoint_left, Finset.mem_coe, Set.mem_setOf_eq, Polynomial.degree]
          <;>
          (try { contradiction }) <;>
          (try { simp_all [Finset.card_eq_zero] }) <;>
          (try { aesop }) <;>
          (try { norm_num }) <;>
          (try { ring_nf }) <;>
          (try { aesop }) <;>
          (try { simp_all [Finset.card_eq_zero] }) <;>
          (try { aesop })
        })
      <;>
      aesop
    · 
      intro h
      have h₁ := h
      simp_all [rootSet, Finset.disjoint_left, Finset.mem_coe, Set.mem_setOf_eq]
      <;>
      (try
        {
          cases p
          <;> simp_all [rootSet, Finset.disjoint_left, Finset.mem_coe, Set.mem_setOf_eq, Polynomial.degree]
          <;>
          (try { contradiction }) <;>
          (try { simp_all [Finset.card_eq_zero] }) <;>
          (try { aesop }) <;>
          (try { norm_num }) <;>
          (try { ring_nf }) <;>
          (try { aesop }) <;>
          (try { simp_all [Finset.card_eq_zero] }) <;>
          (try { aesop })
        })
      <;>
      aesop
  exact h_main
```

### epfl-61171 — EPFLpending7-HB10k

not_closed: infinitely many irreducible rational polynomials. unbounded construction/search; try decide is not finite computable coverage.

```lean
import Mathlib
set_option maxHeartbeats 800000
open Fintype Set Real Ideal Polynomial
open scoped BigOperators
open Fintype Set Real Ideal Polynomial
open scoped BigOperators
theorem exercise_4_6_3 :
  Infinite {a : ℤ | Irreducible (X^7 + 15*X^2 - 30*X + (a : Polynomial ℚ))} := by
  have h_main : Infinite {a : ℤ | Irreducible (X^7 + 15*X^2 - 30*X + (a : Polynomial ℚ))} := by
    have h : Infinite {a : ℤ | Irreducible (X^7 + 15*X^2 - 30*X + (a : Polynomial ℚ))} := by
      apply Infinite.of_injective (fun a => ⟨a, by
        norm_num [Irreducible] at *
        <;>
        (try decide) <;>
        (try
          {
            simp_all [Polynomial.irreducible_iff_irreducible_map_fraction_map, Polynomial.map_add, Polynomial.map_mul, Polynomial.map_pow, Polynomial.map_sub, Polynomial.map_one, Polynomial.map_C, Polynomial.map_X, Polynomial.map_mul, Polynomial.map_pow, Polynomial.map_sub]
            <;>
            norm_num <;>
            (try
              {
                aesop
              }) <;>
            (try
              {
                exact?
              }) <;>
            (try
              {
                aesop
              })
          }) <;>
        (try
          {
            aesop
          }) <;>
        (try
          {
            exact?
          })
      <;>
      aesop⟩)
      intro a₁ a₂ h
      simp_all
    exact h
  exact h_main
```

### epfl-63380 — EPFLpending7-HB10k

not_closed: arbitrary finite-dimensional endomorphism space. symbolic submodule/adjoint proof, not concrete finite matrix data.

```lean
import Mathlib
set_option maxHeartbeats 800000
open Fintype Complex Polynomial LinearMap FiniteDimensional Module Module.End
open scoped BigOperators
open Fintype Complex Polynomial LinearMap FiniteDimensional Module Module.End
open scoped BigOperators
theorem exercise_7_5 {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V]
  [FiniteDimensional ℂ V] (hV : finrank V ≥ 2) :
  ∀ U : Submodule ℂ (End ℂ V), U.carrier ≠ {T | T * adjoint T = adjoint T * T} := by
  have h_main : ∀ U : Submodule ℂ (End ℂ V), U.carrier ≠ {T | T * adjoint T = adjoint T * T} := by
    intro U hU
    have h₁ : (0 : End ℂ V) ∈ U := by
      simp_all [Set.ext_iff]
      <;>
      aesop
    have h₂ : (0 : End ℂ V) ∉ ({T : End ℂ V | T * adjoint T = adjoint T * T} : Set (End ℂ V)) := by
      intro h
      have h₃ := h
      simp [mul_zero, zero_mul, adjoint_zero] at h₃
      <;>
      aesop
    have h₃ : (0 : End ℂ V) ∈ U := by
      exact h₁
    have h₄ : (0 : End ℂ V) ∉ ({T : End ℂ V | T * adjoint T = adjoint T * T} : Set (End ℂ V)) := by
      exact h₂
    have h₅ : U.carrier ≠ {T | T * adjoint T = adjoint T * T} := by
      intro h
      have h₆ := h
      simp_all [Set.ext_iff]
      <;>
      aesop
    exact h₅ hU
  exact h_main
```

### epfl-61885 — EPFLpending7-HB10k

not_closed: arbitrary group conjugacy. symbolic group/simp, no closed computation.

```lean
import Mathlib
set_option maxHeartbeats 800000
open Function Fintype Subgroup Ideal Polynomial Submodule Zsqrtd
open scoped BigOperators
open Function Fintype Subgroup Ideal Polynomial Submodule Zsqrtd
open scoped BigOperators
theorem exercise_2_3_2 {G : Type*} [Group G] (a b : G) :
    ∃ g : G, b * a = g * a * b * g⁻¹ := by
  have h_main : ∃ g : G, b * a = g * a * b * g⁻¹ := by
    refine' ⟨a⁻¹ * b⁻¹ * a * b, _⟩
    simp [mul_assoc, mul_inv_rev, inv_inv, mul_right_inv, mul_left_inv]
    <;>
    rw [← mul_assoc] <;>
    simp [mul_assoc, mul_inv_rev, inv_inv, mul_right_inv, mul_left_inv] <;>
    group
    <;>
    aesop
  exact h_main
```

### epfl-60781 — EPFLpending7-HB10k

not_closed: abstract finite p-group normality. symbolic group/order and exact? search, not concrete closed finite group.

```lean
import Mathlib
set_option maxHeartbeats 800000
open Fintype Set Real Ideal Polynomial
open scoped BigOperators
open Fintype Set Real Ideal Polynomial
open scoped BigOperators
theorem exercise_2_11_22 {p : ℕ} {n : ℕ} {G : Type*} [Fintype G]
  [Group G] (hp : Nat.Prime p) (hG : card G = p ^ n) {K : Subgroup G}
  [Fintype K] (hK : card K = p ^ (n - 1)) :
  K.Normal := by
  have h_main : K.Normal := by
    have h1 : Fact (Nat.Prime p) := ⟨hp⟩
    have h2 : card G = p ^ n := hG
    have h3 : card K = p ^ (n - 1) := hK
    have h4 : (p : ℕ) ∣ card G := by
      rw [h2]
      exact ⟨p ^ (n - 1), by
        cases n with
        | zero => simp_all [Nat.Prime.ne_zero]
        | succ n =>
          simp_all [Nat.pow_succ, Nat.mul_comm]
          <;> ring_nf at * <;> simp_all [Nat.Prime.ne_zero]
          <;> omega
      ⟩
    have h5 : (p : ℕ) ∣ card G := h4
    have h6 : K.Normal := by
      have h7 : (p : ℕ) ∣ card G := h5
      have h8 : (p : ℕ) ∣ card G := h7
      exact?
    exact h6
  exact h_main
```
