import DifferentialSupport
set_option maxHeartbeats 5000
theorem candidateProof : False := by failure_probe simp_all only
#audit_candidate
