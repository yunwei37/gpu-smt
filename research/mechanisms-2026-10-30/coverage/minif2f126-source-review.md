# Individual computational extraction review — 自审

Each selected original source reviewed; categories are opportunities, not accepted transformed candidates. Comments stripped for display only.

### minif2f-175 — mathd_numbertheory_3

closed_potential: closed sum of ten squares modulo10. structural finite sum equivalence/certificate not implemented.

```lean
theorem mathd_numbertheory_3 : (∑ x in Finset.range 10, (x + 1) ^ 2) % 10 = 5 := by
  simp_all only [Finset.sum_range_succ, pow_two, Nat.mul_mod, Nat.add_mod, Nat.mod_mod]
  norm_num
  <;> decide
```

### minif2f-579 — amc12a_2020_p10

not_closed: logarithmic hypotheses on symbolic n before interval_cases. Real.logb noncomputable and disputed n bounds; numeric digits suffix does not establish hot-path coverage.

```lean
theorem amc12a_2020_p10 (n : ℕ) (h₀ : 0 < n)
    (h₁ : Real.logb 2 (Real.logb 16 n) = Real.logb 4 (Real.logb 4 n)) :
    (List.sum (Nat.digits 10 n)) = 13 := by
  simp_all [Real.logb, Real.log_rpow, mul_comm]
  ring_nf at h₁
  have h₂ : n ≤ 16 ^ 4 := by
    apply Nat.le_of_not_lt
    intro h
    simp_all [Nat.log]
  have h₃ : n ≥ 16 ^ 4 := by linarith
  interval_cases n <;> simp_all (config := {decide := true})
```

### minif2f-663 — mathd_numbertheory_427

closed_potential: sum divisors500 then prime-divisor sum after a substitution. closed but requires divisor/primality certificate and proof bridge.

```lean
theorem mathd_numbertheory_427 (a : ℕ) (h₀ : a = ∑ k in Nat.divisors 500, k) :
    (∑ k in Finset.filter (fun x => Nat.Prime x) (Nat.divisors a), k) = 25 := by
  simp only [Finset.sum_eq_multiset_sum, Nat.divisors] at h₀ ⊢
  norm_num at h₀
  rw [h₀]
  norm_num
  rfl
```

### minif2f-664 — mathd_numbertheory_427

closed_potential: sum divisors500 then prime-divisor sum after a substitution. closed but requires divisor/primality certificate and proof bridge.

```lean
theorem mathd_numbertheory_427 (a : ℕ) (h₀ : a = ∑ k in Nat.divisors 500, k) :
    (∑ k in Finset.filter (fun x => Nat.Prime x) (Nat.divisors a), k) = 25 := by
  rw [h₀]
  simp only [Nat.divisors, Finset.sum_eq_multiset_sum, Finset.mem_filter, Finset.mem_range,
    Finset.mem_Ico, Finset.mem_singleton, Finset.sum_singleton, Finset.sum_range_succ,
    Finset.sum_range_one, Nat.cast_one, Nat.cast_zero, add_zero]
  norm_num
  rfl
```

### minif2f-806 — mathd_numbertheory_430

bounded_potential: 3-dimensional1..9 Nat grid of closed polynomial predicates. all inputs bounded in original assumptions; closed checker soundness not implemented.

```lean
theorem mathd_numbertheory_430 (a b c : ℕ) (h₀ : 1 ≤ a ∧ a ≤ 9) (h₁ : 1 ≤ b ∧ b ≤ 9)
    (h₂ : 1 ≤ c ∧ c ≤ 9) (h₃ : a ≠ b) (h₄ : a ≠ c) (h₅ : b ≠ c) (h₆ : a + b = c)
    (h₇ : 10 * a + a - b = 2 * c) (h₈ : c * b = 10 * a + a + a) : a + b + c = 8 := by
  have h₁ : a + b + c = 8 := by
    have : a ≤ 9 := by linarith
    have : b ≤ 9 := by linarith
    have : c ≤ 9 := by linarith
    interval_cases a <;> interval_cases b <;> interval_cases c <;>
      linarith
  exact h₁
```

### minif2f-960 — imo_1997_p5

not_closed: exponential equation with unbounded match tails. finite syntax of match does not bound x,y; symbolic simp/nlinarith.

```lean
theorem imo_1997_p5 (x y : ℕ) (h₀ : 0 < x ∧ 0 < y) (h₁ : x ^ y ^ 2 = y ^ x) :
    (x, y) = (1, 1) ∨ (x, y) = (16, 2) ∨ (x, y) = (27, 3) := by
  have : (x, y) = (1, 1) ∨ (x, y) = (16, 2) ∨ (x, y) = (27, 3) := by
    match x, y with
    | 0, 0 =>
      simp_all
    | 1, 1 =>
      simp_all
    | 16, 2 =>
      simp_all
    | 27, 3 =>
      simp_all
    | x + 17, y + 3 =>
      simp_all [Nat.pow_succ, Nat.pow_zero, Nat.pow_succ]
      <;> nlinarith
  exact this
```

### minif2f-970 — imo_1997_p5

proof_repair: asserts x<=1 or y<=1. (16,2) satisfies the original power equation but both exceed1; false auxiliary restriction.

```lean
theorem imo_1997_p5 (x y : ℕ) (h₀ : 0 < x ∧ 0 < y) (h₁ : x ^ y ^ 2 = y ^ x) :
    (x, y) = (1, 1) ∨ (x, y) = (16, 2) ∨ (x, y) = (27, 3) := by
  have h₂ : x ≤ 1 ∨ y ≤ 1 := by
    by_contra! h
    have : x ^ y ^ 2 > y ^ x := by
      calc
        x ^ y ^ 2 = x ^ 1 := by rw [pow_one]
        _ < y ^ x := h₁
    linarith
  have h₃ : x = 1 ∨ x = 16 ∨ x = 27 := by
    have : x ≤ 1 ∨ y ≤ 1 := h₂
    match x, y with
    | 0, 0 => contradiction
    | 0, 1 => contradiction
    | 1, 0 => contradiction
    | 1, 1 => simp_all
    | 1, 2 => contradiction
    | 2, 1 => contradiction
    | 2, 2 => contradiction
    | x + 3, 2 => simp_all
    | x + 3, 3 => contradiction
    | x + 4, 3 => contradiction
    | 3, x + 4 => contradiction
    | 3, 4 => contradiction
    | 4, 3 => contradiction
    | 4, 4 => contradiction
    | x + 5, 4 => simp_all
    | x + 5, 5 => contradiction
    | x + 6, 5 => contradiction
    | x + 6, 6 => contradiction
    | x + 7, 6 => contradiction
    | x + 7, 7 => contradiction
    | x + 8, 7 => contradiction
    | x + 8, 8 => contradiction
    | x + 9, 8 => contradiction
    | x + 9, 9 => contradiction
    | x + 10, 9 => contradiction
    | x + 10, 10 => contradiction
    | x + 11, 10 => contradiction
    | x + 11, 11 => contradiction
    | x + 12, 11 => contradiction
    | x + 12, 12 => contradiction
    | x + 13, 12 => contradiction
    | x + 13, 13 => contradiction
    | x + 14, 13 => contradiction
    | x + 14, 14 => contradiction
    | x + 15, 14 => contradiction
    | x + 15, 15 => contradiction
    | x + 16, 15 => contradiction
    | x + 16, 16 => contradiction
    | x + 17, 16 => contradiction
    | x + 17, 17 => contradiction
    | x + 18, 17 => contradiction
    | x + 18, 18 => contradiction
    | x + 19, 18 => contradiction
    | x + 19, 19 => contradiction
    | x + 20, 19 => contradiction
    | x + 20, 20 => contradiction
    | x + 21, 20 => contradiction
    | x + 21, 21 => contradiction
    | x + 22, 21 => contradiction
    | x + 22, 22 => contradiction
    | x + 23, 22 => contradiction
    | x + 23, 23 => contradiction
    | x + 24, 23 => contradiction
    | x + 24, 24 => contradiction
    | x + 25, 24 => contradiction
    | x + 25, 25 => contradiction
    | x + 26, 25 => contradiction
    | x + 26, 26 => contradiction
    | x + 27, 26 => contradiction
    | x + 27, 27 => simp_all
    | x + 28, 27 => contradiction
    | x + 28, 28 => contradiction
    | x + 29, 28 => contradiction
    | x + 30, 28 => contradiction
    | x + 30, 29 => contradiction
    | x + 31, 29 => contradiction
    | x + 31, 30 => contradiction
    | x + 32, 30 => contradiction
    | x + 32, 31 => contradiction
    | x + 33, 31 => contradiction
    | x + 33, 32 => contradiction
    | x + 34, 32 => contradiction
    | x + 34, 33 => contradiction
    | x + 35, 33 => contradiction
    | x + 35, 34 => contradiction
    | x + 36, 34 => contradiction
    | x + 36, 35 => contradiction
    | x + 37, 35 => contradiction
    | x + 37, 36 => contradiction
    | x + 38, 36 => contradiction
    | x + 38, 37 => contradiction
    | x + 39, 37 => contradiction
    | x + 39, 38 => contradiction
    | x + 40, 38 => contradiction
    | x + 40, 39 => contradiction
    | x + 41, 39 => contradiction
    | x + 41, 40 => contradiction
    | x + 42, 40 => contradiction
    | x + 42, 41 => contradiction
    | x + 43, 41 => contradiction
    | x + 43, 42 => contradiction
    | x + 44, 42 => contradiction
    | x + 44, 43 => contradiction
    | x + 45, 43 => contradiction
    | x + 45, 44 => contradiction
    | x + 46, 44 => contradiction
    | x + 46, 45 => contradiction
    | x + 47, 45 => contradiction
    | x + 47, 46 => contradiction
    | x + 48, 46 => contradiction
    | x + 48, 47 => contradiction
    | x + 49, 47 => contradiction
    | x + 49, 48 => contradiction
    | x + 50, 48 => contradiction
    | x + 50, 49 => contradiction
  rcases h₃ with (rfl | rfl | rfl) <;> simp_all
  <;> try simp_all [pow_succ, mul_assoc]
  <;> try linarith
  <;> try contradiction
```

### minif2f-998 — mathd_numbertheory_277

bounded_potential: bounded product756/gcd/lcm grid. must retain gcd/lcm hypotheses and prove bounds/bridge.

```lean
theorem mathd_numbertheory_277 (m n : ℕ) (h₀ : Nat.gcd m n = 6) (h₁ : Nat.lcm m n = 126) :
    60 ≤ m + n := by
  have h₂ : m * n = 756 := by
    rw [← Nat.gcd_mul_lcm]
    simp [h₀, h₁]
  have h₃ : m + n ≥ 60 := by
    apply Nat.le_of_not_lt
    intro h
    have : m ≤ 756 := by linarith
    have : n ≤ 756 := by linarith
    interval_cases m <;> interval_cases n <;> norm_num at h₂ <;> omega
  exact h₃
```

### minif2f-1000 — mathd_numbertheory_277

bounded_potential: bounded product756/gcd/lcm grid. must retain gcd/lcm hypotheses and prove bounds/bridge.

```lean
theorem mathd_numbertheory_277 (m n : ℕ) (h₀ : Nat.gcd m n = 6) (h₁ : Nat.lcm m n = 126) :
    60 ≤ m + n := by
  have : 6 * 126 = m * n := by rw [← h₀, ← h₁]
  have h₂ : m + n ≥ 60 := by
    apply Nat.le_of_not_lt
    intro h
    have : m ≤ 756 := by linarith
    have : n ≤ 756 := by linarith
    interval_cases m <;> interval_cases n <;> simp_all
  exact h₂
```

### minif2f-1005 — mathd_numbertheory_277

bounded_potential: bounded product756/gcd/lcm grid. must retain gcd/lcm hypotheses and prove bounds/bridge.

```lean
theorem mathd_numbertheory_277 (m n : ℕ) (h₀ : Nat.gcd m n = 6) (h₁ : Nat.lcm m n = 126) :
    60 ≤ m + n := by
  have h₂ : m * n = Nat.gcd m n * Nat.lcm m n := by simp [Nat.gcd_mul_lcm]
  rw [h₀, h₁] at h₂
  norm_num at h₂
  apply Nat.le_of_not_lt
  intro h
  have h₃ : m ≤ 756 := by linarith
  have h₄ : n ≤ 756 := by linarith
  interval_cases m <;> interval_cases n <;> norm_num at h₂ ⊢
  <;> try linarith
```

### minif2f-1021 — mathd_numbertheory_277

bounded_potential: bounded product756/gcd/lcm grid. must retain gcd/lcm hypotheses and prove bounds/bridge.

```lean
theorem mathd_numbertheory_277 (m n : ℕ) (h₀ : Nat.gcd m n = 6) (h₁ : Nat.lcm m n = 126) :
    60 ≤ m + n := by
  have : 6 * 126 = m * n := by rw [← Nat.gcd_mul_lcm]
  have h₂ : m ≤ 756 := Nat.le_of_dvd (by norm_num) this
  have h₃ : n ≤ 756 := Nat.le_of_dvd (by norm_num) this
  have h₄ : m + n ≥ 60 := by
    apply Nat.le_of_not_lt
    intro h
    have : m ≤ 756 := Nat.le_of_dvd (by norm_num) this
    have : n ≤ 756 := Nat.le_of_dvd (by norm_num) this
    interval_cases m <;> interval_cases n <;> norm_num at h <;> omega
  exact h₄
```

### minif2f-1467 — mathd_numbertheory_451

not_closed: finite outer n range contains unbounded existential m. bounded outer syntax does not close existential search; divisors symbolic.

```lean
theorem mathd_numbertheory_451 (S : Finset ℕ)
    (h₀ :
      ∀ n : ℕ,
        n ∈ S ↔
          2010 ≤ n ∧ n ≤ 2019 ∧ ∃ m, (Nat.divisors m).card = 4 ∧ (∑ p in Nat.divisors m, p) = n) :
    (∑ k in S, k) = 2016 := by
  have : S = {2010, 2012, 2016} := by
    ext n
    simp [h₀, Nat.divisors]
    constructor
    · intro h
      match n with
      | 2010 => simp
      | 2011 => contradiction
      | 2012 => simp
      | 2013 => contradiction
      | 2014 => contradiction
      | 2015 => contradiction
      | 2016 => simp
      | 2017 => contradiction
      | 2018 => contradiction
      | 2019 => contradiction
    · intro h
      match n with
      | 2010 => simp
      | 2012 => simp
      | 2016 => simp
  rw [this]
  simp
```

### minif2f-1816 — numbertheory_fxeq4powxp6powxp9powx_f2powmdvdf2pown

not_closed: symbolic exponent divisibility. unbounded m,n; repeated simp is not closed finite evaluation.

```lean
theorem numbertheory_fxeq4powxp6powxp9powx_f2powmdvdf2pown (m n : ℕ) (f : ℕ → ℕ)
    (h₀ : ∀ x, f x = 4 ^ x + 6 ^ x + 9 ^ x) (h₁ : 0 < m ∧ 0 < n) (h₂ : m ≤ n) :
    f (2 ^ m) ∣ f (2 ^ n) := by
  apply Nat.dvd_of_mod_eq_zero
  rw [h₀] at *
  simp_all [pow_succ, Nat.mul_mod, Nat.add_mod, Nat.pow_mod]
  <;> simp [Nat.pow_succ, Nat.mul_mod, Nat.add_mod, Nat.pow_mod]
  <;> simp [h₀]
  <;> simp_all [pow_succ, Nat.mul_mod, Nat.add_mod, Nat.pow_mod]
  <;> simp_all [h₀]
  <;> simp_all [pow_succ, Nat.mul_mod, Nat.add_mod, Nat.pow_mod]
  <;> simp_all [h₀]
  <;> simp_all [pow_succ, Nat.mul_mod, Nat.add_mod, Nat.pow_mod]
  <;> simp_all [h₀]
```

### minif2f-1841 — imo_1992_p1

bounded_potential: bounded integer triple divisibility grid. must prove exhaustive bounds; Int signed evaluation/sound bridge not implemented.

```lean
theorem imo_1992_p1 (p q r : ℤ) (h₀ : 1 < p ∧ p < q ∧ q < r)
    (h₁ : (p - 1) * (q - 1) * (r - 1) ∣ p * q * r - 1) :
    (p, q, r) = (2, 4, 8) ∨ (p, q, r) = (3, 5, 15) := by
  norm_num at h₀
  norm_num at h₁
  have : p ≤ 20 := by
    nlinarith
  have : q ≤ 20 := by
    nlinarith
  have : r ≤ 20 := by
    nlinarith
  have : p ≥ 2 := by
    nlinarith
  have : q ≥ 2 := by
    nlinarith
  have : r ≥ 2 := by
    nlinarith
  interval_cases p <;> interval_cases q <;> interval_cases r <;> simp_all
  <;> norm_num
  <;> omega
```

### minif2f-1846 — imo_1992_p1

not_closed: rcases over integers retains symbolic tails. cannot equate nested rcases to finite exhaustive grid.

```lean
theorem imo_1992_p1 (p q r : ℤ) (h₀ : 1 < p ∧ p < q ∧ q < r)
    (h₁ : (p - 1) * (q - 1) * (r - 1) ∣ p * q * r - 1) :
    (p, q, r) = (2, 4, 8) ∨ (p, q, r) = (3, 5, 15) := by
  norm_num
  rcases p with (_ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _) <;>
  rcases q with (_ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _) <;>
  rcases r with (_ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _ | _) <;>
  simp_all [mul_assoc] <;>
  norm_num at h₁ <;>
  omega
```

### minif2f-1885 — imo_1982_p1

not_closed: symbolic function with disjunctive recurrence constraints. hypotheses do not uniquely define closed function values; omega over symbolic applications.

```lean
theorem imo_1982_p1 (f : ℕ → ℕ)
    (h₀ : ∀ m n, 0 < m ∧ 0 < n → f (m + n) - f m - f n = 0 ∨ f (m + n) - f m - f n = 1)
    (h₁ : f 2 = 0) (h₂ : 0 < f 3) (h₃ : f 9999 = 3333) : f 1982 = 660 := by
  have h₄ := h₀ 0 0
  have h₅ := h₀ 0 1
  have h₆ := h₀ 1 1
  have h₇ := h₀ 2 0
  have h₈ := h₀ 2 1
  have h₉ := h₀ 1 2
  have h₁₀ := h₀ 0 2
  have h₁₁ := h₀ 3 0
  have h₁₂ := h₀ 1 3
  have h₁₃ := h₀ 2 2
  have h₁₄ := h₀ 3 1
  have h₁₅ := h₀ 2 3
  have h₁₆ := h₀ 1 4
  have h₁₇ := h₀ 4 0
  have h₁₈ := h₀ 0 3
  have h₁₉ := h₀ 1 5
  have h₂₀ := h₀ 5 0
  have h₂₁ := h₀ 0 4
  have h₂₂ := h₀ 1 6
  have h₂₃ := h₀ 6 0
  have h₂₄ := h₀ 0 5
  have h₂₅ := h₀ 1 7
  have h₂₆ := h₀ 7 0
  have h₂₇ := h₀ 0 6
  have h₂₈ := h₀ 1 8
  have h₂₉ := h₀ 8 0
  have h₃₀ := h₀ 0 7
  have h₃₁ := h₀ 1 9
  have h₃₂ := h₀ 9 0
  have h₃₃ := h₀ 0 8
  have h₃₄ := h₀ 1 10
  have h₃₅ := h₀ 10 0
  have h₃₆ := h₀ 0 9
  have h₃₇ := h₀ 1 11
  have h₃₈ := h₀ 11 0
  have h₃₉ := h₀ 0 10
  have h₄₀ := h₀ 1 12
  have h₄₁ := h₀ 12 0
  have h₄₂ := h₀ 0 11
  have h₄₃ := h₀ 1 13
  have h₄₄ := h₀ 13 0
  have h₄₅ := h₀ 0 12
  have h₄₆ := h₀ 1 14
  have h₄₇ := h₀ 14 0
  have h₄₈ := h₀ 0 13
  have h₄₉ := h₀ 1 15
  have h₅₀ := h₀ 15 0
  have h₅₁ := h₀ 0 14
  have h₅₂ := h₀ 1 16
  have h₅₃ := h₀ 16 0
  have h₅₄ := h₀ 0 15
  have h₅₅ := h₀ 1 17
  have h₅₆ := h₀ 17 0
  have h₅₇ := h₀ 0 16
  have h₅₈ := h₀ 1 18
  have h₅₉ := h₀ 18 0
  have h₆₀ := h₀ 0 17
  have h₆₁ := h₀ 1 19
  have h₆₂ := h₀ 19 0
  have h₆₃ := h₀ 0 18
  have h₆₄ := h₀ 1 20
  have h₆₅ := h₀ 20 0
  have h₆₆ := h₀ 0 19
  have h₆₇ := h₀ 1 21
  have h₆₈ := h₀ 21 0
  have h₆₉ := h₀ 0 20
  have h₇₀ := h₀ 1 22
  have h₇₁ := h₀ 22 0
  have h₇₂ := h₀ 0 21
  have h₇₃ := h₀ 1 23
  have h₇₄ := h₀ 23 0
  have h₇₅ := h₀ 0 22
  have h₇₆ := h₀ 1 24
  have h₇₇ := h₀ 24 0
  have h₇₈ := h₀ 0 23
  have h₇₉ := h₀ 1 25
  have h₈₀ := h₀ 25 0
  have h₈₁ := h₀ 0 24
  have h₈₂ := h₀ 1 26
  have h₈₃ := h₀ 26 0
  have h₈₄ := h₀ 0 25
  have h₈₅ := h₀ 1 27
  have h₈₆ := h₀ 27 0
  have h₈₇ := h₀ 0 26
  have h₈₈ := h₀ 1 28
  have h₈₉ := h₀ 28 0
  have h₉₀ := h₀ 0 27
  have h₉₁ := h₀ 1 29
  have h₉₂ := h₀ 29 0
  have h₉₃ := h₀ 0 28
  have h₉₄ := h₀ 1 30
  have h₉₅ := h₀ 30 0
  norm_num at *
  omega
```

### minif2f-1886 — imo_1982_p1

not_closed: symbolic function with disjunctive recurrence constraints. hypotheses do not uniquely define closed function values; omega over symbolic applications.

```lean
theorem imo_1982_p1 (f : ℕ → ℕ)
    (h₀ : ∀ m n, 0 < m ∧ 0 < n → f (m + n) - f m - f n = 0 ∨ f (m + n) - f m - f n = 1)
    (h₁ : f 2 = 0) (h₂ : 0 < f 3) (h₃ : f 9999 = 3333) : f 1982 = 660 := by
  have h₄ := h₀ 1 1
  have h₅ := h₀ 1 2
  have h₆ := h₀ 2 1
  have h₇ := h₀ 2 2
  have h₈ := h₀ 0 1
  have h₉ := h₀ 1 0
  have h₁₀ := h₀ 2 0
  have h₁₁ := h₀ 0 2
  have h₁₂ := h₀ 3 0
  have h₁₃ := h₀ 0 3
  have h₁₄ := h₀ 3 1
  have h₁₅ := h₀ 1 3
  have h₁₆ := h₀ 2 3
  have h₁₇ := h₀ 3 2
  have h₁₈ := h₀ 4 1
  have h₁₉ := h₀ 1 4
  have h₂₀ := h₀ 2 4
  have h₂₁ := h₀ 4 2
  have h₂₂ := h₀ 3 4
  have h₂₃ := h₀ 4 3
  have h₂₄ := h₀ 6 1
  have h₂₅ := h₀ 1 6
  have h₂₆ := h₀ 2 6
  have h₂₇ := h₀ 6 2
  have h₂₈ := h₀ 3 6
  have h₂₉ := h₀ 6 3
  have h₃₀ := h₀ 4 6
  have h₃₁ := h₀ 6 4
  have h₃₂ := h₀ 5 1
  have h₃₃ := h₀ 1 5
  have h₃₄ := h₀ 2 5
  have h₃₅ := h₀ 5 2
  have h₃₆ := h₀ 3 5
  have h₃₇ := h₀ 5 3
  have h₃₈ := h₀ 4 5
  have h₃₉ := h₀ 5 4
  have h₄₀ := h₀ 6 2
  have h₄₁ := h₀ 2 6
  have h₄₂ := h₀ 6 3
  have h₄₃ := h₀ 3 6
  have h₄₄ := h₀ 6 4
  have h₄₅ := h₀ 4 6
  have h₄₆ := h₀ 6 5
  have h₄₇ := h₀ 5 6
  norm_num at h₄ h₅ h₆ h₇ h₈ h₉ h₁₀ h₁₁ h₁₂ h₁₃ h₁₄ h₁₅ h₁₆ h₁₇ h₁₈ h₁₉ h₂₀ h₂₁ h₂₂ h₂₃ h₂₄ h₂₅ h₂₆ h₂₇ h₂₈ h₂₉ h₃₀ h₃₁ h₃₂ h₃₃ h₃₄ h₃₅ h₃₆ h₃₇ h₃₈ h₃₉ h₄₀ h₄₁ h₄₂ h₄₃ h₄₄ h₄₅ h₄₆ h₄₇
  omega
```

### minif2f-2401 — mathd_numbertheory_483

proof_repair: asserts Fibonacci residues have period2. a1=a2=1 and the recurrence force a3=2, contradicting period2 at1; target mod4 statement may still be true.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  have h₃ := h₂ 0
  have h₄ := h₂ 1
  have h₅ := h₂ 2
  have h₆ := h₂ 3
  have h₇ := h₂ 4
  have h₈ := h₂ 5
  have h₉ := h₂ 6
  have h₁₀ := h₂ 7
  have h₁₁ := h₂ 8
  have h₁₂ := h₂ 9
  have h₁₃ := h₂ 10
  have h₁₄ : ∀ n : ℕ, a (n + 2) % 4 = a (n + 1) % 4 + a n % 4 ∨
    a (n + 2) % 4 = a (n + 1) % 4 - a n % 4 := by
    intro n
    omega
  have h₁₅ : ∃ k : ℕ, k > 0 ∧ ∀ n : ℕ, a (n + k) % 4 = a n % 4 := by
    use 2
    constructor
    norm_num
    intro n
    simpa [h₁, h₂] using h₂ (n + 2)
  have h₁₆ : ∀ n : ℕ, a (n + 2) % 4 = a n % 4 := by
    intro n
    induction' n with n ih
    simpa [h₁] using h₁₅
    simpa [h₂, h₁₅] using h₂ (n + 1)
  have h₁₇ : a 100 % 4 = a 2 % 4 := by
    simpa [h₁₆] using h₁₅ 1
  simp_all
```

### minif2f-2403 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  simp_all [Nat.add_mod, Nat.mod_eq_of_lt]
  <;> norm_num
  <;> linarith
```

### minif2f-2404 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  have h₃ : ∀ n, a (n + 6) % 4 = a n % 4 := by
    intro n
    simp [h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_eq_of_lt]
  simp [h₀, h₁, h₂, h₃] at *
```

### minif2f-2409 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  norm_num
  simp_all [Nat.add_mod, Nat.mul_mod]
  <;> linarith
```

### minif2f-2412 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  have h₃ := h₂ 0
  have h₄ := h₂ 1
  have h₅ := h₂ 2
  have h₆ := h₂ 3
  have h₇ := h₂ 4
  have h₈ := h₂ 5
  simp_all [h₀, h₁]
  <;> linarith
```

### minif2f-2414 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  norm_num [h₀, h₁] at h₂
  simp [h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_eq_of_lt, Nat.mod_mod]
  <;> rfl
```

### minif2f-2419 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  simp [h₀, h₁, h₂] at *
  norm_num
  <;> linarith [h₂ 0, h₂ 1, h₂ 2, h₂ 3, h₂ 4, h₂ 5, h₂ 6, h₂ 7, h₂ 8, h₂ 9]
```

### minif2f-2421 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  norm_num
  simp_all [h₂]
  <;> linarith
  <;> simp_all [h₂]
  <;> linarith
```

### minif2f-2423 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  simp_all [Nat.add_mod, Nat.mul_mod, Nat.mod_mod]
  <;> linarith
  <;> simp_all [h₂]
  <;> linarith
  <;> simp_all [h₂]
  <;> linarith
  <;> simp_all [h₂]
  <;> linarith
  <;> simp_all [h₂]
  <;> linarith
  <;> simp_all [h₂]
  <;> linarith
  <;> simp_all [h₂]
  <;> linarith
```

### minif2f-2424 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  simp [h₀, h₁, h₂, Nat.add_mod, Nat.mul_mod, Nat.mod_mod] at *
  <;> rfl
```

### minif2f-2429 — mathd_numbertheory_483

bridge_required: recurrence determines positive Fibonacci values. current expensive simp works over symbolic function/quantified recurrence; first prove equivalence to structural evaluator; not closed input now.

```lean
theorem mathd_numbertheory_483 (a : ℕ → ℕ) (h₀ : a 1 = 1) (h₁ : a 2 = 1)
    (h₂ : ∀ n, a (n + 2) = a (n + 1) + a n) : a 100 % 4 = 3 := by
  norm_num [h₀, h₁] at *
  <;> simp_all [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
```

### minif2f-2498 — mathd_numbertheory_495

not_closed: symbolic gcd/lcm and congruences. unbounded variables; no certified finite reduction.

```lean
theorem mathd_numbertheory_495 (a b : ℕ) (h₀ : 0 < a ∧ 0 < b) (h₁ : a % 10 = 2) (h₂ : b % 10 = 4)
    (h₃ : Nat.gcd a b = 6) : 108 ≤ Nat.lcm a b := by
  simp_all [Nat.lcm, Nat.gcd, Nat.gcd_eq_right]
  omega
  <;> assumption
  <;> assumption
```

### minif2f-3101 — amc12_2000_p12

bounded_potential: finite Nat triple from sum12. rcases leaves unbounded tail constructors; use proved a,m,c<=12 and checked finite bridge.

```lean
theorem amc12_2000_p12 (a m c : ℕ) (h₀ : a + m + c = 12) :
    a * m * c + a * m + m * c + a * c ≤ 112 := by
  rcases a with (_ | _ | _ | _ | _ | _ | _ | _ | _) <;>
  rcases m with (_ | _ | _ | _ | _ | _ | _ | _ | _) <;>
  rcases c with (_ | _ | _ | _ | _ | _ | _ | _ | _) <;>
  simp_all [add_assoc, add_comm, mul_comm, Nat.mul_assoc]
  <;> nlinarith
```

### minif2f-3587 — amc12a_2021_p14

not_computable: closed Real.logb sums. closed does not imply executable: requires analytic logarithm lemmas before reflection.

```lean
theorem amc12a_2021_p14 :
    ((∑ k in Finset.Icc 1 20, Real.logb (5 ^ k) (3 ^ k ^ 2)) *
        ∑ k in Finset.Icc 1 100, Real.logb (9 ^ k) (25 ^ k)) = 21000 := by
  simp_all [Finset.sum_Icc_succ_top, mul_add, mul_comm, mul_left_comm]
  norm_cast
  ring_nf
  <;> norm_num
  <;> rfl
```

### minif2f-3610 — amc12a_2021_p14

not_computable: closed Real.logb sums. closed does not imply executable: requires analytic logarithm lemmas before reflection.

```lean
theorem amc12a_2021_p14 :
    ((∑ k in Finset.Icc 1 20, Real.logb (5 ^ k) (3 ^ k ^ 2)) *
        ∑ k in Finset.Icc 1 100, Real.logb (9 ^ k) (25 ^ k)) = 21000 := by
  simp_all [Real.logb, Real.log_rpow]
  simp_all [Finset.sum_Icc_succ_top, mul_add, mul_comm]
  ring_nf
  norm_num
  <;> rfl
```

### minif2f-3681 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n : ℕ => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
      (Finset.Icc 1000 9999) := by
    ext n
    simp [Nat.lt_succ_iff, h₀]
    omega
  rw [h₁]
  simp [Finset.filter_eq, Finset.Icc]
  rfl
```

### minif2f-3682 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n ↦ n % 5 = 0 ∧ (∀ d ∈ Nat.digits 10 n, Even d)) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Nat.lt_succ_iff, Nat.le_add_left]
    omega
  rw [this]
  rfl
```

### minif2f-3683 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n ↦ 5 ∣ n) (Finset.filter (fun n ↦ ∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) (Finset.Icc 1000 9999)) := by
    ext n
    simp [h₀]
    refine' ⟨_, fun h => ⟨_, _, _, h⟩⟩
    · rintro ⟨h₁, _, h₃, h₄⟩
      exact (Nat.mod_eq_of_lt (Nat.mod_lt _ (zero_lt_succ _))).symm
    · rcases h with (rfl | rfl | rfl | rfl) <;> norm_num
  rw [h₁]
  simp only [Finset.card_filter, Nat.card_Icc, Nat.add_sub_cancel, Finset.card_range, Finset.card_product]
  norm_num
  rfl
```

### minif2f-3685 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n ↦ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext n
    simp [h₀, Finset.mem_range]
    omega
  rw [this]
  rfl
```

### minif2f-3686 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n ↦ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.Icc 1000 9999) := by
    ext n
    simp [Nat.le_of_lt, h₀]
    omega
  rw [h₁]
  rfl
```

### minif2f-3687 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext
    simp [h₀, Nat.mod_eq_of_lt]
    omega
  rw [h₁]
  rfl
```

### minif2f-3688 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n ↦ 5 ∣ n) (Finset.filter (fun n ↦ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 1000 ≤ n ∧ n ≤ 9999) (Finset.range 10000)) := by
    ext n
    simp [h₀, Nat.mod_eq_of_lt]
    omega
  rw [h₁]
  simp only [Finset.card, Finset.filter_eq', Finset.mem_filter, Finset.mem_range, Finset.card_range]
  rfl
```

### minif2f-3689 — amc12a_2020_p4

proof_repair: filter omits5-divisibility. even-digit4-digit set has500 members, not100; false intermediate equality.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n => ∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Finset.mem_Icc, Nat.even_iff]
    omega
  rw [this]
  rfl
```

### minif2f-3690 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter
    (fun n => ∀ d : ℕ, d ∈ Nat.digits 10 n → Even d ∧ 5 ∣ n)
    (Finset.Icc 1000 9999) := by
    ext
    simp [h₀, Nat.lt_succ_iff]
    omega
  rw [h₁]
  rfl
```

### minif2f-3691 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext n
    simp [h₀, Nat.lt_succ_iff]
    omega
  rw [this]
  rfl
```

### minif2f-3692 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n : ℕ => 5 ∣ n ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d)) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Finset.mem_filter, Finset.mem_Icc]
    omega
  rw [this]
  rfl
```

### minif2f-3693 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n ↦ n ≥ 1000 ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext n
    simp [h₀, Nat.lt_succ_iff]
    omega
  rw [this]
  rfl
```

### minif2f-3694 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
      (Finset.range 10000) := by
    ext n
    simp [h₀, Nat.lt_succ_iff]
    omega
  simp [h₁]
  rfl
```

### minif2f-3695 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
      (Finset.range (10000)) := by
    ext n
    simp [h₀, Finset.mem_filter, Finset.mem_range, le_of_lt]
    omega
  simp_rw [h₁]
  rfl
```

### minif2f-3697 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => n % 10 = 0 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d)) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, ← Nat.lt_succ_iff, Nat.le_of_dvd zero_lt_one]
    omega
  rw [h₁]
  rfl
```

### minif2f-3698 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n => 5 ∣ n ∧ ∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, ← Nat.mod_eq_of_lt (show 1000 < 10000 from by norm_num)]
    omega
  rw [this]
  rfl
```

### minif2f-3699 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n => n % 5 = 0) (Finset.filter (fun n => ∀ d ∈ Nat.digits 10 n, Even d) (Finset.Icc 1000 9999)) := by
    ext n
    simp [h₀, Nat.even_iff]
    omega
  simp [this]
  rfl
```

### minif2f-3700 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext n
    simp [h₀, Nat.lt_succ_iff]
    omega
  rw [this]
  rfl
```

### minif2f-3701 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n : ℕ => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
    (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Finset.mem_Icc]
    omega
  rw [h₁]
  rfl
```

### minif2f-3702 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter
    (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
    (Finset.range 10000) := by
    ext n
    simp [h₀, Finset.mem_filter, Finset.mem_range]
    omega
  rw [h₁]
  simp only [Finset.card, Finset.filter_eq, Finset.mem_filter, Finset.mem_range, Finset.card_range,
    Nat.div_self (Nat.zero_lt_succ _)]
  rfl
```

### minif2f-3703 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 5 ∣ n) (Finset.filter (fun n => ∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) (Finset.Icc 1000 9999)) := by
    ext n
    simp [h₀, Nat.even_iff]
    refine' ⟨_, fun h => ⟨h.2.2.1, h.2.2.2⟩⟩
    simp_all
  rw [h₁]
  simp only [Finset.card_filter, Nat.card_Icc, Nat.card_eq_fintype_card, Finset.card_range,
    Nat.add_zero, Nat.zero_eq, Finset.card_range]
  rfl
```

### minif2f-3704 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
      (Finset.range 10000) := by
    ext
    simp [h₀, Finset.mem_filter, Finset.mem_range]
  simp [h₁]
  rfl
  <;> simp [h₀, Nat.zero_le]
  <;> simp [h₀, Nat.zero_le]
  <;> simp [h₀, Nat.zero_le]
```

### minif2f-3705 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Nat.lt_succ_iff, Nat.le_add_right]
    constructor <;> intro h <;>
    rcases h with ⟨h₁, h₂, h₃, h₄⟩ <;>
    simp_all [Nat.even_iff]
  rw [h₁]
  rfl
```

### minif2f-3706 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext n
    simp [h₀, Finset.mem_filter, Finset.mem_range, Nat.lt_succ_iff]
    omega
  rw [h₁]
  rfl
```

### minif2f-3707 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun x : ℕ => 1000 ≤ x ∧ x ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 x → Even d) ∧ 5 ∣ x) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Finset.mem_Icc]
    <;> omega
  rw [h₁]
  rfl
```

### minif2f-3708 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n : ℕ =>
      n ≥ 1000 ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n)
      (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Finset.mem_Icc]
    omega
  rw [this]
  rfl
```

### minif2f-3709 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have : S = Finset.filter (fun n => 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext n
    simp [h₀, Nat.lt_succ_iff]
    omega
  rw [this]
  rfl
```

### minif2f-3710 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => 5 ∣ n ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d)) (Finset.Icc 1000 9999) := by
    ext n
    simp [h₀, Finset.mem_Icc, and_comm, Nat.mod_eq_of_lt]
    omega
  rw [h₁]
  simp only [Finset.card_filter]
  rfl
```

### minif2f-3711 — amc12a_2020_p4

checked_family: digits/filter/card after set equality. DigitsCertificate proves the original goal family; candidate prefix/diagnostic preservation not qualified.

```lean
theorem amc12a_2020_p4 (S : Finset ℕ)
    (h₀ : ∀ n : ℕ, n ∈ S ↔ 1000 ≤ n ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) :
    S.card = 100 := by
  have h₁ : S = Finset.filter (fun n => n ≥ 1000 ∧ n ≤ 9999 ∧ (∀ d : ℕ, d ∈ Nat.digits 10 n → Even d) ∧ 5 ∣ n) (Finset.range 10000) := by
    ext
    simp [h₀]
    omega
  rw [h₁]
  rfl
```

### minif2f-4336 — aime_1984_p1

not_closed: symbolic rational sequence sums. u0 remains free; algebraic cancellation/proof needed, not closed evaluation.

```lean
theorem aime_1984_p1 (u : ℕ → ℚ) (h₀ : ∀ n, u (n + 1) = u n + 1)
    (h₁ : (∑ k in Finset.range 98, u k.succ) = 137) :
    (∑ k in Finset.range 49, u (2 * k.succ)) = 93 := by
  simp_all [Finset.sum_range_succ, add_comm]
  norm_num
  linarith
```

### minif2f-4339 — aime_1984_p1

not_closed: symbolic rational sequence sums. u0 remains free; algebraic cancellation/proof needed, not closed evaluation.

```lean
theorem aime_1984_p1 (u : ℕ → ℚ) (h₀ : ∀ n, u (n + 1) = u n + 1)
    (h₁ : (∑ k in Finset.range 98, u k.succ) = 137) :
    (∑ k in Finset.range 49, u (2 * k.succ)) = 93 := by
  simp_all [Finset.sum_range_succ, add_comm, add_left_comm]
  linarith
```

### minif2f-4544 — amc12a_2003_p23

proof_repair: closed divisor/card expression appears after incorrect set equality. false auxiliary set equality; cannot accept original source by computing a different final theorem.

```lean
theorem amc12a_2003_p23 (S : Finset ℕ)
    (h₀ : ∀ k : ℕ, k ∈ S ↔ 0 < k ∧ (k * k : ℕ) ∣ ∏ i in Finset.Icc 1 9, i !) : S.card = 672 := by
  have : S = Finset.filter (fun x : ℕ => 0 < x) (Nat.divisors (∏ i in Finset.Icc 1 9, i !)) := by
    ext k
    simp [Finset.mem_Icc, Finset.mem_filter, Nat.succ_le_iff, Nat.lt_succ_iff, h₀, Nat.dvd_iff_mod_eq_zero]
  rw [this]
  rfl
```

### minif2f-4552 — amc12a_2003_p23

proof_repair: closed divisor/card expression appears after incorrect set equality. false auxiliary set equality; cannot accept original source by computing a different final theorem.

```lean
theorem amc12a_2003_p23 (S : Finset ℕ)
    (h₀ : ∀ k : ℕ, k ∈ S ↔ 0 < k ∧ (k * k : ℕ) ∣ ∏ i in Finset.Icc 1 9, i !) : S.card = 672 := by
  have h₁ : S = Finset.filter (fun x => 0 < x) (Nat.divisors 9!) := by
    ext x
    simp only [Nat.dvd_factorial_iff, mem_Icc, Finset.mem_filter, mem_Icc,
      and_self_iff, mem_range, Nat.divisors, Finset.mem_Ico]
    constructor <;> intro h
    · have : 0 < x := pos_of_gt h.1
      simp only [Nat.cast_id, Finset.filter_val, Finset.card_mk,
        Finset.card_filter] at *
      rw [Nat.lt_succ_iff] at *
      nlinarith
    · have : x ≤ 9 := h.2
      simp only [Nat.cast_id, Finset.mem_Ico, Finset.mem_filter, Finset.card_mk,
        Finset.card_filter] at *
      rw [Nat.lt_succ_iff] at *
      nlinarith
  rw [h₁]
  simp only [Nat.cast_id, Finset.card_mk, Nat.cast_zero, add_zero, Finset.card_filter,
    Finset.card_range]
  rfl
```

### minif2f-4570 — amc12a_2003_p23

proof_repair: closed divisor/card expression appears after incorrect set equality. false auxiliary set equality; cannot accept original source by computing a different final theorem.

```lean
theorem amc12a_2003_p23 (S : Finset ℕ)
    (h₀ : ∀ k : ℕ, k ∈ S ↔ 0 < k ∧ (k * k : ℕ) ∣ ∏ i in Finset.Icc 1 9, i !) : S.card = 672 := by
  have h₁ : S = Finset.filter (fun k => 0 < k ∧ (k * k : ℕ) ∣ ∏ i in Finset.Icc 1 9, i !) (Finset.Icc 1 99999999) := by
    ext x
    simp [Finset.mem_filter, Finset.mem_Icc, Nat.dvd_iff_mod_eq_zero]
    constructor
    · intro h
      exact h
    · intro h
      simp [h]
  rw [h₁]
  rfl
```

### minif2f-4878 — mathd_numbertheory_711

bounded_potential: bounded product896/gcd/lcm grid. product alone insufficient:28,32 sum60<72; retain gcd8/lcm112.

```lean
theorem mathd_numbertheory_711 (m n : ℕ) (h₀ : 0 < m ∧ 0 < n) (h₁ : Nat.gcd m n = 8)
    (h₂ : Nat.lcm m n = 112) : 72 ≤ m + n := by
  have h₃ := Nat.gcd_mul_lcm m n
  rw [h₁, h₂] at h₃
  norm_num at h₃
  apply Nat.le_of_not_lt
  intro h
  have h₄ : m < 896 := by linarith
  have h₅ : n < 896 := by linarith
  interval_cases m <;> interval_cases n <;> norm_num at h₁ h₂ h₃ <;> omega
```

### minif2f-4894 — mathd_numbertheory_711

bounded_potential: bounded product896/gcd/lcm grid. product alone insufficient:28,32 sum60<72; retain gcd8/lcm112.

```lean
theorem mathd_numbertheory_711 (m n : ℕ) (h₀ : 0 < m ∧ 0 < n) (h₁ : Nat.gcd m n = 8)
    (h₂ : Nat.lcm m n = 112) : 72 ≤ m + n := by
  have h₃ : m * n = 8 * 112 := by
    simp [Nat.gcd_mul_lcm]
    linarith
  have h₄ : m ≤ 896 := by
    nlinarith
  have h₅ : n ≤ 896 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> norm_num at h₁ h₂ h₃ <;> omega
```

### minif2f-4895 — mathd_numbertheory_711

bounded_potential: bounded product896/gcd/lcm grid. product alone insufficient:28,32 sum60<72; retain gcd8/lcm112.

```lean
theorem mathd_numbertheory_711 (m n : ℕ) (h₀ : 0 < m ∧ 0 < n) (h₁ : Nat.gcd m n = 8)
    (h₂ : Nat.lcm m n = 112) : 72 ≤ m + n := by
  have h₃ : m * n = Nat.gcd m n * Nat.lcm m n := by
    rw [Nat.gcd_mul_lcm]
  rw [h₁, h₂] at h₃
  norm_num at h₃
  have h₄ : m ≤ 904 := by
    nlinarith
  have h₅ : n ≤ 904 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> norm_num at h₃ <;> omega
```

### minif2f-4992 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have h₂ : i * m * o = 2001 := by assumption
  have h₃ : i ≤ 671 := by
    nlinarith [mul_pos (Nat.pos_of_ne_zero fun h => h₀.1 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.1 (by rw [h])),
      mul_pos (Nat.pos_of_ne_zero fun h => h₀.2.2 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.1 (by rw [h])),
      mul_pos (Nat.pos_of_ne_zero fun h => h₀.1 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.2 (by rw [h]))]
  have h₄ : m ≤ 671 := by
    nlinarith [mul_pos (Nat.pos_of_ne_zero fun h => h₀.1 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.1 (by rw [h])),
      mul_pos (Nat.pos_of_ne_zero fun h => h₀.2.2 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.1 (by rw [h])),
      mul_pos (Nat.pos_of_ne_zero fun h => h₀.1 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.2 (by rw [h]))]
  have h₅ : o ≤ 671 := by
    nlinarith [mul_pos (Nat.pos_of_ne_zero fun h => h₀.1 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.1 (by rw [h])),
      mul_pos (Nat.pos_of_ne_zero fun h => h₀.2.2 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.1 (by rw [h])),
      mul_pos (Nat.pos_of_ne_zero fun h => h₀.1 (by rw [h])) (Nat.pos_of_ne_zero fun h => h₀.2.2 (by rw [h]))]
  interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all
```

### minif2f-4993 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have : i ≤ 2001 := Nat.le_of_dvd (by norm_num) (Nat.dvd_of_mod_eq_zero (by simpa [mul_mod] using h₁))
  have : m ≤ 2001 := Nat.le_of_dvd (by norm_num) (Nat.dvd_of_mod_eq_zero (by simpa [mul_mod] using h₁))
  have : o ≤ 2001 := Nat.le_of_dvd (by norm_num) (Nat.dvd_of_mod_eq_zero (by simpa [mul_mod] using h₁))
  interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all
```

### minif2f-4997 — amc12_2000_p1

proof_repair: asserts each factor<=40. (667,3,1) satisfies original assumptions and violates asserted bound; Lean witness already retained.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have h₂ : i ≤ 40 := by
    nlinarith
  have h₃ : m ≤ 40 := by
    nlinarith
  have h₄ : o ≤ 40 := by
    nlinarith
  interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all (config := {decide := true})
  <;> try linarith
```

### minif2f-5006 — amc12_2000_p1

proof_repair: asserts each factor<=31. (667,3,1) refutes auxiliary bound; original final goal remains true.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have : i ≤ 31 := by
    nlinarith [mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all)),
      mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all)),
      mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all))]
  have : m ≤ 31 := by
    nlinarith [mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all)),
      mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all)),
      mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all))]
  have : o ≤ 31 := by
    nlinarith [mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all)),
      mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all)),
      mul_pos (Nat.pos_of_ne_zero (by intro h; simp_all)) (Nat.pos_of_ne_zero (by intro h; simp_all))]
  interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all
```

### minif2f-5009 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  contrapose! h₀
  have h₂ : i ≤ 2001 := by
    nlinarith
  have h₃ : m ≤ 2001 := by
    nlinarith
  have h₄ : o ≤ 2001 := by
    nlinarith
  interval_cases i <;> interval_cases m <;> interval_cases o <;> norm_num at h₁ ⊢
  <;> linarith
```

### minif2f-5011 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have h₂ : i ≤ 671 := by
    nlinarith [mul_pos (Nat.zero_lt_one.trans_le h₀.1.le) (Nat.zero_lt_one.trans_le h₀.2.1.le),
      mul_pos (Nat.zero_lt_one.trans_le h₀.2.1.le) (Nat.zero_lt_one.trans_le h₀.2.2.le),
      mul_pos (Nat.zero_lt_one.trans_le h₀.2.2.le) (Nat.zero_lt_one.trans_le h₀.1.le)]
  have h₃ : m ≤ 671 := by
    nlinarith [mul_pos (Nat.zero_lt_one.trans_le h₀.1.le) (Nat.zero_lt_one.trans_le h₀.2.1.le),
      mul_pos (Nat.zero_lt_one.trans_le h₀.2.1.le) (Nat.zero_lt_one.trans_le h₀.2.2.le),
      mul_pos (Nat.zero_lt_one.trans_le h₀.2.2.le) (Nat.zero_lt_one.trans_le h₀.1.le)]
  have h₄ : o ≤ 671 := by
    nlinarith [mul_pos (Nat.zero_lt_one.trans_le h₀.1.le) (Nat.zero_lt_one.trans_le h₀.2.1.le),
      mul_pos (Nat.zero_lt_one.trans_le h₀.2.1.le) (Nat.zero_lt_one.trans_le h₀.2.2.le),
      mul_pos (Nat.zero_lt_one.trans_le h₀.2.2.le) (Nat.zero_lt_one.trans_le h₀.1.le)]
  interval_cases i <;> interval_cases m <;> interval_cases o <;> norm_num at h₁ <;> omega
```

### minif2f-5015 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have h₁ := h₀.2.1
  have h₂ := h₀.2.2
  have h₃ := h₀.1
  have : i ≤ 2001 := Nat.le_of_dvd (by norm_num) (Nat.dvd_of_mul_left_eq h₁)
  have : m ≤ 2001 := Nat.le_of_dvd (by norm_num) (Nat.dvd_of_mul_left_eq h₁)
  have : o ≤ 2001 := Nat.le_of_dvd (by norm_num) (Nat.dvd_of_mul_left_eq h₂)
  interval_cases i <;> interval_cases m <;> interval_cases o <;> norm_num at h₁ <;> norm_num
  <;> linarith
```

### minif2f-5016 — amc12_2000_p1

proof_repair: asserts each factor<=44. (667,3,1) refutes auxiliary bound; original final goal remains true.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have h₂ : i ≤ 44 := by
    apply Nat.le_of_not_lt
    intro hi
    have : i ≤ 44 := by nlinarith
    nlinarith
  have h₃ : m ≤ 44 := by
    apply Nat.le_of_not_lt
    intro hm
    have : m ≤ 44 := by nlinarith
    nlinarith
  have h₄ : o ≤ 44 := by
    apply Nat.le_of_not_lt
    intro ho
    have : o ≤ 44 := by nlinarith
    nlinarith
  interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all
```

### minif2f-5017 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have : i * m * o = 2001 := h₁
  have : i + m + o ≤ 671 := by
    have h₂ : i ≤ 2001 := by nlinarith
    have h₃ : m ≤ 2001 := by nlinarith
    have h₄ : o ≤ 2001 := by nlinarith
    interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all
  simpa
```

### minif2f-5020 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  apply le_of_not_gt
  intro h
  have h₂ : i + m + o ≥ 672 := by linarith
  have h₃ : i ≤ 671 := by nlinarith
  have h₄ : m ≤ 671 := by nlinarith
  have h₅ : o ≤ 671 := by nlinarith
  interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all
```

### minif2f-5023 — amc12_2000_p1

bounded_potential: finite distinct factor triples of2001. bounds and source errors require checking; no end-to-end source integration.

```lean
theorem amc12_2000_p1 (i m o : ℕ) (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i) (h₁ : i * m * o = 2001) :
    i + m + o ≤ 671 := by
  have : i ≤ 2001 := by
    apply Nat.le_of_dvd (show 0 < 2001 by norm_num)
    simp [h₀]
  have : m ≤ 2001 := by
    apply Nat.le_of_dvd (show 0 < 2001 by norm_num)
    simp [h₀]
  have : o ≤ 2001 := by
    apply Nat.le_of_dvd (show 0 < 2001 by norm_num)
    simp [h₀]
  interval_cases i <;> interval_cases m <;> interval_cases o <;> simp_all
  <;> omega
```

### minif2f-5381 — amc12a_2020_p15

not_computable: complex roots/absolute value/square root. symbolic complex and Real.sqrt proof search.

```lean
theorem amc12a_2020_p15 (a b : ℂ) (h₀ : a ^ 3 - 8 = 0) (h₁ : b ^ 3 - 8 * b ^ 2 - 8 * b + 64 = 0) :
    Complex.abs (a - b) ≤ 2 * Real.sqrt 21 := by
  ring_nf at h₀ h₁
  ring_nf
  norm_num
  simpa [Complex.abs, Complex.normSq] using
    calc
      Complex.abs (a - b) ≤ Complex.abs (2 - 2) + Complex.abs (2 * Complex.I - (-2 * Complex.I)) :=
        Complex.abs.add_le _ _
      _ = 0 + 4 := by norm_num
      _ = 4 := by norm_num
      _ ≤ 2 * Real.sqrt 21 := by
        rw [← Real.sqrt_sq (show 0 ≤ (2 : ℝ) by norm_num)]
        norm_num
        nlinarith [Real.sqrt_nonneg 21]
```

### minif2f-5399 — amc12a_2020_p15

not_computable: complex roots/absolute value/square root. symbolic complex and Real.sqrt proof search.

```lean
theorem amc12a_2020_p15 (a b : ℂ) (h₀ : a ^ 3 - 8 = 0) (h₁ : b ^ 3 - 8 * b ^ 2 - 8 * b + 64 = 0) :
    Complex.abs (a - b) ≤ 2 * Real.sqrt 21 := by
  simp_all only [Complex.ext_iff, pow_three, Complex.ofReal_add, Complex.ofReal_mul,
    Complex.ofReal_sub, Complex.ofReal_pow]
  ring_nf at *
  norm_num at *
  apply le_trans (Complex.abs.add_le _ _)
  simp [Complex.abs, Complex.normSq, Complex.ofReal_mul, Complex.ofReal_add,
    Complex.ofReal_sub, Complex.ofReal_pow]
  norm_num
  nlinarith [sq_sqrt (show (0 : ℝ) ≤ 21 by norm_num),
    sq_nonneg (2 - 4),
    sq_nonneg (2 + 4)]
```

### minif2f-5913 — numbertheory_3pow2pownm1mod2pownp3eq2pownp2

not_closed: symbolic power modular identity. unbounded induction parameter.

```lean
theorem numbertheory_3pow2pownm1mod2pownp3eq2pownp2 (n : ℕ) (h₀ : 0 < n) :
    (3 ^ 2 ^ n - 1) % 2 ^ (n + 3) = 2 ^ (n + 2) := by
  rw [← Nat.mod_add_div (3 ^ 2 ^ n) (2 ^ (n + 3))]
  simp [pow_mod, Nat.mul_mod, Nat.pow_mod, Nat.mod_eq_of_lt, h₀]
  induction' n with n hn
  <;> simp_all [pow_mod, Nat.mul_mod, Nat.pow_mod, Nat.mod_eq_of_lt, Nat.succ_pos]
  <;> omega
```

### minif2f-5919 — numbertheory_3pow2pownm1mod2pownp3eq2pownp2

not_closed: symbolic power modular identity. unbounded induction parameter.

```lean
theorem numbertheory_3pow2pownm1mod2pownp3eq2pownp2 (n : ℕ) (h₀ : 0 < n) :
    (3 ^ 2 ^ n - 1) % 2 ^ (n + 3) = 2 ^ (n + 2) := by
  rw [← Nat.mod_add_div (3 ^ 2 ^ n) (2 ^ (n + 3))]
  norm_num
  induction' h₀ with n hn
  · simp
  · simp_all [Nat.pow_succ, Nat.mul_mod, Nat.pow_mod, Nat.mod_mod]
```

### minif2f-5952 — amc12_2001_p21

bounded_potential: bounded4-variable Nat polynomial grid. candidate bounds differ; no certified source bridge or actual cheap grid established.

```lean
theorem amc12_2001_p21 (a b c d : ℕ) (h₀ : a * b * c * d = 8!) (h₁ : a * b + a + b = 524)
    (h₂ : b * c + b + c = 146) (h₃ : c * d + c + d = 104) : ↑a - ↑d = (10 : ℤ) := by
  norm_num [factorial, h₀] at h₁ h₂ h₃
  ring_nf at h₁ h₂ h₃ ⊢
  have h₄ : a < 100 := by
    nlinarith
  have h₅ : b < 100 := by
    nlinarith
  have h₆ : c < 100 := by
    nlinarith
  have h₇ : d < 100 := by
    nlinarith
  interval_cases a <;> interval_cases b <;> interval_cases c <;> interval_cases d <;>
    omega
```

### minif2f-5954 — amc12_2001_p21

bounded_potential: bounded4-variable Nat polynomial grid. candidate bounds differ; no certified source bridge or actual cheap grid established.

```lean
theorem amc12_2001_p21 (a b c d : ℕ) (h₀ : a * b * c * d = 8!) (h₁ : a * b + a + b = 524)
    (h₂ : b * c + b + c = 146) (h₃ : c * d + c + d = 104) : ↑a - ↑d = (10 : ℤ) := by
  have h₄ : 8! = 40320 := by norm_num [Nat.factorial]
  have h₅ : a ≤ 64 := by nlinarith
  have h₆ : b ≤ 64 := by nlinarith
  have h₇ : c ≤ 64 := by nlinarith
  have h₈ : d ≤ 64 := by nlinarith
  interval_cases a <;> interval_cases b <;> interval_cases c <;> interval_cases d <;>
    simp_all (config := {decide := true})
```

### minif2f-5960 — amc12_2001_p21

bounded_potential: bounded4-variable Nat polynomial grid. candidate bounds differ; no certified source bridge or actual cheap grid established.

```lean
theorem amc12_2001_p21 (a b c d : ℕ) (h₀ : a * b * c * d = 8!) (h₁ : a * b + a + b = 524)
    (h₂ : b * c + b + c = 146) (h₃ : c * d + c + d = 104) : ↑a - ↑d = (10 : ℤ) := by
  norm_num
  norm_num [Nat.factorial] at h₀
  norm_num [Nat.factorial]
  have h₁ : a ≤ 24 := by
    nlinarith
  have h₂ : b ≤ 30 := by
    nlinarith
  have h₃ : c ≤ 40 := by
    nlinarith
  have h₄ : d ≤ 10 := by
    nlinarith
  interval_cases a <;> interval_cases b <;> interval_cases c <;> interval_cases d <;>
    norm_num at h₁ h₂ h₃ h₄ <;> omega
```

### minif2f-5964 — amc12_2001_p21

bounded_potential: bounded4-variable Nat polynomial grid. candidate bounds differ; no certified source bridge or actual cheap grid established.

```lean
theorem amc12_2001_p21 (a b c d : ℕ) (h₀ : a * b * c * d = 8!) (h₁ : a * b + a + b = 524)
    (h₂ : b * c + b + c = 146) (h₃ : c * d + c + d = 104) : ↑a - ↑d = (10 : ℤ) := by
  norm_num [Nat.factorial] at h₀ h₁ h₂ h₃
  have h₄ : a ≤ 49 := by
    nlinarith [mul_pos (Nat.succ_pos a) (Nat.succ_pos b), mul_pos (Nat.succ_pos b) (Nat.succ_pos c),
      mul_pos (Nat.succ_pos c) (Nat.succ_pos d)]
  have h₅ : b ≤ 49 := by
    nlinarith [mul_pos (Nat.succ_pos a) (Nat.succ_pos b), mul_pos (Nat.succ_pos b) (Nat.succ_pos c),
      mul_pos (Nat.succ_pos c) (Nat.succ_pos d)]
  have h₆ : c ≤ 49 := by
    nlinarith [mul_pos (Nat.succ_pos a) (Nat.succ_pos b), mul_pos (Nat.succ_pos b) (Nat.succ_pos c),
      mul_pos (Nat.succ_pos c) (Nat.succ_pos d)]
  have h₇ : d ≤ 49 := by
    nlinarith [mul_pos (Nat.succ_pos a) (Nat.succ_pos b), mul_pos (Nat.succ_pos b) (Nat.succ_pos c),
      mul_pos (Nat.succ_pos c) (Nat.succ_pos d)]
  interval_cases a <;> interval_cases b <;> interval_cases c <;> interval_cases d <;> omega
```

### minif2f-5980 — amc12_2001_p21

bounded_potential: bounded4-variable Nat polynomial grid. candidate bounds differ; no certified source bridge or actual cheap grid established.

```lean
theorem amc12_2001_p21 (a b c d : ℕ) (h₀ : a * b * c * d = 8!) (h₁ : a * b + a + b = 524)
    (h₂ : b * c + b + c = 146) (h₃ : c * d + c + d = 104) : ↑a - ↑d = (10 : ℤ) := by
  norm_num
  norm_num [factorial] at h₀ h₁ h₂ h₃
  have : a ≤ 98 := by
    nlinarith
  have : b ≤ 98 := by
    nlinarith
  have : c ≤ 98 := by
    nlinarith
  have : d ≤ 98 := by
    nlinarith
  interval_cases a <;> interval_cases b <;> interval_cases c <;> interval_cases d <;>
    omega
```

### minif2f-6209 — amc12a_2021_p12

not_computable: symbolic complex polynomial/real coefficients. root and positivity assumptions require symbolic proof.

```lean
theorem amc12a_2021_p12 (a b c d : ℝ) (f : ℂ → ℂ)
    (h₀ : ∀ z, f z = z ^ 6 - 10 * z ^ 5 + a * z ^ 4 + b * z ^ 3 + c * z ^ 2 + d * z + 16)
    (h₁ : ∀ z, f z = 0 → z.im = 0 ∧ 0 < z.re ∧ ↑(Int.floor z.re) = z.re) : b = -88 := by
  have : f (1 : ℂ) = 0 := by rw [h₀]; norm_num
  have : f (2 : ℂ) = 0 := by rw [h₀]; norm_num
  have : f (1 + Complex.I * Real.sqrt 3) = 0 := by simpa [h₀] using h₁ (1 + Complex.I * Real.sqrt 3) (by simpa [h₀] using (by ring))
  have : f (1 + Complex.I * Real.sqrt 3) = 0 := by simpa [h₀] using h₁ (1 + Complex.I * Real.sqrt 3) (by simpa [h₀] using (by ring))
  have : f (1 - Complex.I * Real.sqrt 3) = 0 := by simpa [h₀] using h₁ (1 - Complex.I * Real.sqrt 3) (by simpa [h₀] using (by ring))
  have : f (1 - Complex.I * Real.sqrt 3) = 0 := by simpa [h₀] using h₁ (1 - Complex.I * Real.sqrt 3) (by simpa [h₀] using (by ring))
  simp_all [Complex.ext_iff, pow_succ, mul_add, mul_sub, mul_one, mul_neg, sub_neg_eq_add]
  norm_num
  linarith
```

### minif2f-6373 — mathd_algebra_289

bounded_potential: bounded prime/polynomial grid. m,n grid alone leaves k,t symbolic in some candidates; full elimination/bridge required.

```lean
theorem mathd_algebra_289 (k t m n : ℕ) (h₀ : Nat.Prime m ∧ Nat.Prime n) (h₁ : t < k)
    (h₂ : (k ^ 2 : ℤ) - m * k + n = 0) (h₃ : (t ^ 2 : ℤ) - m * t + n = 0) :
    m ^ n + n ^ m + k ^ t + t ^ k = 20 := by
  have : m < 100 := by
    cases' Nat.Prime.eq_two_or_odd h₀.1 with hm hm <;>
    cases' Nat.Prime.eq_two_or_odd h₀.2 with hn hn <;>
    nlinarith
  have : n < 100 := by
    cases' Nat.Prime.eq_two_or_odd h₀.1 with hm hm <;>
    cases' Nat.Prime.eq_two_or_odd h₀.2 with hn hn <;>
    nlinarith
  interval_cases m <;> interval_cases n <;> simp_all (config := {decide := true})
  <;> linarith
```

### minif2f-6383 — mathd_algebra_289

bounded_potential: bounded prime/polynomial grid. m,n grid alone leaves k,t symbolic in some candidates; full elimination/bridge required.

```lean
theorem mathd_algebra_289 (k t m n : ℕ) (h₀ : Nat.Prime m ∧ Nat.Prime n) (h₁ : t < k)
    (h₂ : (k ^ 2 : ℤ) - m * k + n = 0) (h₃ : (t ^ 2 : ℤ) - m * t + n = 0) :
    m ^ n + n ^ m + k ^ t + t ^ k = 20 := by
  have hm' : m ≤ 20 := by
    nlinarith [h₀.1.one_lt, h₀.2.one_lt]
  have hn' : n ≤ 20 := by
    nlinarith [h₀.1.one_lt, h₀.2.one_lt]
  have hmn' : m * n ≤ 400 := by
    nlinarith
  have h₁' : k ≤ 20 := by
    nlinarith
  have h₂' : t ≤ 20 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> interval_cases k <;> interval_cases t <;> simp_all
  <;> try contradiction
```

### minif2f-6398 — mathd_algebra_289

bounded_potential: bounded prime/polynomial grid. m,n grid alone leaves k,t symbolic in some candidates; full elimination/bridge required.

```lean
theorem mathd_algebra_289 (k t m n : ℕ) (h₀ : Nat.Prime m ∧ Nat.Prime n) (h₁ : t < k)
    (h₂ : (k ^ 2 : ℤ) - m * k + n = 0) (h₃ : (t ^ 2 : ℤ) - m * t + n = 0) :
    m ^ n + n ^ m + k ^ t + t ^ k = 20 := by
  norm_num [sq, Nat.Prime] at h₀ h₂ h₃ <;> norm_num [h₀]
  all_goals
    rcases m with (_ | _ | _ | _ | _ | _ | _ | _ | _) <;>
    rcases n with (_ | _ | _ | _ | _ | _ | _ | _ | _) <;>
    rcases k with (_ | _ | _ | _ | _ | _ | _ | _ | _) <;>
    rcases t with (_ | _ | _ | _ | _ | _ | _ | _ | _) <;>
    simp_all [Nat.Prime, Nat.succ_le_iff] <;>
    nlinarith
```

### minif2f-6807 — numbertheory_aoddbdiv4asqpbsqmod8eq1

not_closed: symbolic integer modular polynomial. could design residue-class theorem but current calls not closed; not counted.

```lean
theorem numbertheory_aoddbdiv4asqpbsqmod8eq1 (a : ℤ) (b : ℕ) (h₀ : Odd a) (h₁ : 4 ∣ b) :
    (a ^ 2 + b ^ 2) % 8 = 1 := by
  cases' h₀ with k hk
  cases' h₁ with m hm
  simp_all [Int.add_emod, Int.mul_emod, pow_two]
  ring_nf
  omega
```

### minif2f-7108 — mathd_algebra_158

not_closed: finite sums with symbolic a and commutative rewriting. small closed sub-sum is not evidence that dominant rewrite work can be extracted.

```lean
theorem mathd_algebra_158 (a : ℕ) (h₀ : Even a)
    (h₁ : ↑(∑ k in Finset.range 8, 2 * k + 1) - ↑(∑ k in Finset.range 5, a + 2 * k) = (4 : ℤ)) :
    a = 8 := by
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add, add_zero,
    Nat.cast_zero, Nat.cast_one, Nat.cast_add, Nat.cast_mul, Nat.cast_succ,
    add_left_neg, add_assoc, add_comm, add_left_comm, sub_eq_add_neg,
    Int.ofNat_add, Int.ofNat_mul, Int.ofNat_one, Int.ofNat_zero, neg_add_rev,
    neg_neg, neg_zero] at h₁
  ring_nf at h₁
  zify at h₁
  omega
```

### minif2f-7129 — mathd_algebra_158

not_closed: finite sums with symbolic a and commutative rewriting. small closed sub-sum is not evidence that dominant rewrite work can be extracted.

```lean
theorem mathd_algebra_158 (a : ℕ) (h₀ : Even a)
    (h₁ : ↑(∑ k in Finset.range 8, 2 * k + 1) - ↑(∑ k in Finset.range 5, a + 2 * k) = (4 : ℤ)) :
    a = 8 := by
  simp_all only [Finset.sum_range_succ, Finset.sum_range_one, add_assoc, add_right_comm,
    add_left_comm, Nat.cast_one, Nat.cast_zero, Nat.cast_add, Nat.cast_mul, Nat.cast_succ,
    Nat.cast_sub, Nat.cast_pow]
  ring_nf at h₁
  omega
```

### minif2f-7200 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have h₃ : m ≤ 2005 := by
    nlinarith
  have h₄ : n ≤ 2005 := by
    nlinarith
  have h₅ : m + n = 406 := by
    interval_cases m <;> interval_cases n <;> omega
  exact h₅
```

### minif2f-7202 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m * n = 2005 := h₂
  have h₃ : m + n = 406 := by
    have h₃ : m ≤ 406 := by
      nlinarith
    have h₄ : n ≤ 406 := by
      nlinarith
    interval_cases m <;> interval_cases n <;> simp_all
  exact h₃
```

### minif2f-7203 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have h : m ≤ 2005 := by
    nlinarith
  have h' : n ≤ 2005 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> norm_num at h₁ h₂ ⊢
```

### minif2f-7205 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m * n = 2005 := by linarith
  have : m + n = 406 := by
    have : m ≤ 401 := by
      nlinarith
    have : n ≤ 401 := by
      nlinarith
    interval_cases m <;> interval_cases n <;> norm_num at this <;> omega
  exact this
```

### minif2f-7207 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m * n = 2005 := by assumption
  have : m + n = 406 := by
    have : m ≤ 2005 := by nlinarith
    have : n ≤ 2005 := by nlinarith
    interval_cases m <;> interval_cases n <;> omega
  exact this
```

### minif2f-7208 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m + n = 406 := by
    have h₃ : m ≤ 2005 := by
      nlinarith
    have h₄ : n ≤ 2005 := by
      nlinarith
    interval_cases m <;> interval_cases n <;> omega
  simpa
```

### minif2f-7210 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have mpos : 0 < m := by linarith
  have npos : 0 < n := by linarith
  have sum_is_406 : m + n = 406 := by
    have h₃ : m ≤ 406 := by nlinarith
    have h₄ : n ≤ 406 := by nlinarith
    interval_cases m <;> interval_cases n <;> omega
  exact sum_is_406
```

### minif2f-7212 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m + n = 406 := by
    have : m ≤ 2005 := by nlinarith
    have : n ≤ 2005 := by nlinarith
    interval_cases m <;> interval_cases n <;> omega
  exact this
```

### minif2f-7213 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have h₀ : m ≤ 2005 := by
    apply Nat.le_of_not_lt
    intro h
    have : m * n > 2005 := by nlinarith
    linarith
  have h₁ : n ≤ 2005 := by
    apply Nat.le_of_not_lt
    intro h
    have : m * n > 2005 := by nlinarith
    linarith
  interval_cases m <;> interval_cases n <;> norm_num at h₂ ⊢
```

### minif2f-7216 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have h : m + n = 406 := by
    have : m ≤ 2005 := by nlinarith
    have : n ≤ 2005 := by nlinarith
    interval_cases m <;> interval_cases n <;> norm_num at h₂
    <;> try linarith
  exact h
```

### minif2f-7217 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m + n = 406 := by
    have : m < 406 := by
      apply Nat.lt_of_not_ge
      intro h
      have : m * n ≥ 2005 := by
        nlinarith
      linarith
    have : n < 406 := by
      apply Nat.lt_of_not_ge
      intro h
      have : m * n ≥ 2005 := by
        nlinarith
      linarith
    interval_cases m <;> interval_cases n <;> norm_num at h₂
    <;> omega
  exact this
```

### minif2f-7218 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have h₃ : m + n = 406 := by
    have : m ≤ 2005 := by nlinarith
    have : n ≤ 2005 := by nlinarith
    interval_cases m <;> interval_cases n <;> simp_all
  exact h₃
```

### minif2f-7219 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have m₁ : m ≤ 2005 := by
    nlinarith
  have n₁ : n ≤ 2005 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> norm_num at h₂
  <;> try linarith
  <;> try norm_num
  <;> try ring
```

### minif2f-7221 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m + n = 406 := by
    have : m * n = 2005 := by assumption
    have : m + n = 406 := by
      have : m ≤ 2005 := by nlinarith
      have : n ≤ 2005 := by nlinarith
      interval_cases m <;> interval_cases n <;> omega
    assumption
  assumption
```

### minif2f-7223 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m + n = 406 := by
    have : m * n = 2005 := h₂
    have : m ≤ 2005 := by nlinarith
    have : n ≤ 2005 := by nlinarith
    interval_cases m <;> interval_cases n <;> omega
  simpa using this
```

### minif2f-7224 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m * n = 2005 := h₂
  have : m ≤ 406 := by
    nlinarith
  have : n ≤ 406 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> simp_all
```

### minif2f-7225 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have hm : 1 < m := by linarith
  have hn : 1 < n := by linarith
  have hm1 : m ≤ 2005 := by nlinarith
  have hn1 : n ≤ 2005 := by nlinarith
  interval_cases m <;> interval_cases n <;> norm_num at h₂ <;> omega
```

### minif2f-7226 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m ≤ 2005 := by
    nlinarith
  have : n ≤ 2005 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> norm_num at h₂
  <;> linarith
```

### minif2f-7229 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : 1 < m ∧ 1 < n := by
    constructor
    · exact h₀
    · exact h₁
  have h₃ : m ≤ 2005 := by
    nlinarith
  have h₄ : n ≤ 2005 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> simp_all
```

### minif2f-7230 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : 2 ≤ m := by
    apply le_of_not_gt
    intro hm
    apply lt_irrefl 1
    linarith
  have : 2 ≤ n := by
    apply le_of_not_gt
    intro hn
    apply lt_irrefl 1
    linarith
  have : m + n = 406 := by
    have : m ≤ 401 := by
      nlinarith
    have : n ≤ 401 := by
      nlinarith
    interval_cases m <;> interval_cases n <;> norm_num at h₂
  exact this
```

### minif2f-7231 — mathd_numbertheory_541

checked_family: bounded Nat product grid after proved bounds. ReflectedGridCertificate proves original goal family and full grid; no source-preserving replacement measurement.

```lean
theorem mathd_numbertheory_541 (m n : ℕ) (h₀ : 1 < m) (h₁ : 1 < n) (h₂ : m * n = 2005) :
    m + n = 406 := by
  have : m ≤ 2005 := by
    nlinarith
  have : n ≤ 2005 := by
    nlinarith
  interval_cases m <;> interval_cases n <;> norm_num at h₂
  <;> simp_all
```

### minif2f-7521 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  rcases h₁ with ⟨x, hx⟩
  rcases h₂ with ⟨t, ht⟩
  apply Nat.le_of_not_lt
  intro h
  have hx' : x < 4096 := by
    nlinarith [pow_two x, pow_two (x - 1)]
  have ht' : t < 4096 := by
    nlinarith [pow_two t, pow_two (t - 1)]
  interval_cases x <;> interval_cases t <;> omega
```

### minif2f-7525 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  obtain ⟨x, hx⟩ := h₁
  obtain ⟨t, ht⟩ := h₂
  apply le_of_not_lt
  intro h
  have hx' : x < 4096 := by linarith [pow_two x, pow_two t]
  have ht' : t < 4096 := by linarith [pow_two x, pow_two t]
  interval_cases x <;> interval_cases t <;> omega
```

### minif2f-7530 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  obtain ⟨x, hx⟩ := h₁
  obtain ⟨t, ht⟩ := h₂
  apply le_of_not_lt
  intro h
  have h₃ : x ≤ 4096 := by
    nlinarith [pow_two x, pow_two t, pow_two (x - t)]
  have h₄ : t ≤ 4096 := by
    nlinarith [pow_two x, pow_two t, pow_two (x - t)]
  interval_cases x <;> interval_cases t <;> omega
```

### minif2f-7532 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  obtain ⟨x, hx⟩ := h₁
  obtain ⟨t, ht⟩ := h₂
  have h₃ : n ≥ 4096 := by
    apply Nat.le_of_not_lt
    intro h
    have h₄ : x ≤ 4096 := by linarith
    have h₅ : t ≤ 4096 := by linarith
    interval_cases x <;> interval_cases t <;> omega
  exact h₃
```

### minif2f-7533 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  cases' h₁ with x hx
  cases' h₂ with t ht
  have : 4096 ≤ n := by
    apply Nat.le_of_not_lt
    intro h
    have h₁ : x ≤ 4096 := by linarith
    have h₂ : t ≤ 4096 := by linarith
    have h₃ : x ≤ 4096 := by linarith
    have h₄ : t ≤ 4096 := by linarith
    interval_cases x <;> interval_cases t <;> omega
  exact this
```

### minif2f-7537 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  rcases h₁ with ⟨x, hx⟩
  rcases h₂ with ⟨t, ht⟩
  apply le_of_not_lt
  intro h
  have hx' : x < 4096 := by
    nlinarith [pow_two x, pow_two (x + 1)]
  have ht' : t < 4096 := by
    nlinarith [pow_two t, pow_two (t + 1)]
  interval_cases x <;> interval_cases t <;> omega
```

### minif2f-7542 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  cases' h₁ with x hx
  cases' h₂ with t ht
  have h₃ : 4096 ≤ n := by
    apply Nat.le_of_not_lt
    intro h₄
    have h₅ : x ≤ 4096 := by
      nlinarith [pow_two x, pow_two (x - 1)]
    have h₆ : t ≤ 4096 := by
      nlinarith [pow_two t, pow_two (t - 1)]
    interval_cases x <;> interval_cases t <;> omega
  exact h₃
```

### minif2f-7551 — mathd_numbertheory_296

bounded_potential: bounded cube/fourth-power grid under n<4096. must eliminate or quantify n and prove witness bounds; no compiled certificate yet.

```lean
theorem mathd_numbertheory_296 (n : ℕ) (h₀ : 2 ≤ n) (h₁ : ∃ x, x ^ 3 = n) (h₂ : ∃ t, t ^ 4 = n) :
    4096 ≤ n := by
  rcases h₁ with ⟨x, hx⟩
  rcases h₂ with ⟨t, ht⟩
  apply le_of_not_lt
  intro h
  have hn : n ≤ 4095 := by linarith
  have h₁ : n < 4096 := by linarith
  interval_cases n <;> simp_all [pow_succ]
```

### minif2f-7771 — mathd_numbertheory_582

not_closed: symbolic Nat modular sum. unbounded n; residue reduction needs new symbolic bridge.

```lean
theorem mathd_numbertheory_582 (n : ℕ) (h₀ : 0 < n) (h₁ : 3 ∣ n) :
    (n + 4 + (n + 6) + (n + 8)) % 9 = 0 := by
  simp_all [Nat.add_mod, Nat.mul_mod, Nat.mod_mod, Nat.mod_eq_of_lt]
  <;> omega
```
