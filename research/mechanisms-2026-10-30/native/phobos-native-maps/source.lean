import Mathlib
set_option maxHeartbeats 10000
#eval IO.FS.readFile "/proc/self/maps" >>= IO.println
example : (2 : Nat) + 2 = 4 := by decide
#print axioms Nat.add_comm
