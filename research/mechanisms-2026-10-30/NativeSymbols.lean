import Lean
set_option maxHeartbeats 10000
@[extern "m_lookup_symbol"] opaque lookupSymbol : String → IO String
@[extern "m_set_phase"] opaque setPhase : UInt64 → IO Unit
#eval do
  setPhase 1
  for symbol in ["l_Lean_Elab_Tactic_evalSimp", "l_Lean_Elab_Tactic_evalSimpAll",
      "l_Lean_Elab_Tactic_evalDecide", "l_Lean_Elab_Tactic_Omega_omegaTactic"] do
    IO.println s!"{symbol}: {← lookupSymbol symbol}"
  setPhase 0
example : (2 : Nat) + 2 = 4 := by decide
#print axioms Nat.add_comm
