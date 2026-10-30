import DifferentialSupport
set_option maxHeartbeats 5000
theorem candidateProof : True := by failure_probe differentialMutation
#audit_candidate
