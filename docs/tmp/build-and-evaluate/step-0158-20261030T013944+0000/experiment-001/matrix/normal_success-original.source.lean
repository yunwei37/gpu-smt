import DifferentialSupport
set_option maxHeartbeats 5000
theorem candidateProof : True := by failure_probe exact True.intro
#audit_candidate
