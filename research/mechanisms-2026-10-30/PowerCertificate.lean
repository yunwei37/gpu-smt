import Mathlib
set_option maxHeartbeats 200000
set_option maxRecDepth 10000
namespace MechanismPowerCertificate
theorem checked128 :
    ∀ x : Fin 16, ∀ t : Fin 8, 2 ≤ x.val ^ 3 → x.val ^ 3 ≠ t.val ^ 4 := by decide

theorem no_small (n x t : Nat) (hn : 2 ≤ n) (hlt : n < 4096)
    (hx : x ^ 3 = n) (ht : t ^ 4 = n) : False := by
  have xlt : x < 16 := by
    by_contra h
    have hle : 16 ≤ x := by omega
    have hp : (16 : Nat) ^ 3 ≤ x ^ 3 := by gcongr
    norm_num at hp
    omega
  have tlt : t < 8 := by
    by_contra h
    have hle : 8 ≤ t := by omega
    have hp : (8 : Nat) ^ 4 ≤ t ^ 4 := by gcongr
    norm_num at hp
    omega
  have checked := checked128 ⟨x,xlt⟩ ⟨t,tlt⟩ (by simpa [hx] using hn)
  exact checked (hx.trans ht.symm)

theorem lower (n : Nat) (hn : 2 ≤ n) (hc : ∃ x, x^3=n)
    (hf : ∃ t, t^4=n) : 4096 ≤ n := by
  by_contra h
  obtain ⟨x,hx⟩ := hc
  obtain ⟨t,ht⟩ := hf
  exact no_small n x t hn (by omega) hx ht
end MechanismPowerCertificate
#print axioms MechanismPowerCertificate.lower
