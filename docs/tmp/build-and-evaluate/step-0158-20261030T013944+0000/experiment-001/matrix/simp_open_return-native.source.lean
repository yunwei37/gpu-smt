import DifferentialSupport
set_option maxHeartbeats 5000
theorem candidateProof : False := by               simp_all (config := { failIfUnchanged := false }) only; done
#audit_candidate
