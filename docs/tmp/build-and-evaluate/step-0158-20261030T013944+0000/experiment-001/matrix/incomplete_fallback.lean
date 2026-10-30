import DifferentialSupport
set_option maxHeartbeats 5000
theorem candidateProof : True := by first | failure_probe assumption | sorry
#audit_candidate
