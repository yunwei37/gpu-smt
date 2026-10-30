import DifferentialSupport
set_option maxHeartbeats 5000
theorem candidateProof : True := by failure_probe simp_all only [differentialUnknownLemma]
#audit_candidate
