"""Emit untrusted numeric values; every chunk is proved by stock kernel.
Parameters come from detected literal arithmetic, not theorem/task names."""
from pathlib import Path
import math,json,sys,time,re
sys.set_int_max_str_digits(100000)
def emit(out,factorials,powers,odd_ranges,chunk=100):
    out.mkdir(exist_ok=False);began=time.monotonic()
    lines=["import ClosedNatBase\nset_option maxHeartbeats 200000\nset_option maxRecDepth 10000\nopen scoped BigOperators\nnamespace MClosedNat\n"]
    boundaries={0}|set(factorials)
    boundaries|={i for n in factorials for i in range(chunk,n+1,chunk)}
    for n in sorted(boundaries):
        if not n:lines.append("theorem fac_0 : Nat.factorial 0 = 1 := rfl\n");continue
        a=max(i for i in boundaries if i<n);b=n-a
        v,w,res=math.factorial(a),math.prod(range(a+1,n+1)),math.factorial(n)
        lines.append(f"theorem fac_{n} : Nat.factorial {n} = {res} := by\n"
          f"  exact (factorial_step {a} {b} {v} {w} fac_{a} (by decide)).trans (by decide)\n")
    for base,exponent in powers:
        vals=sorted({0,exponent}|set(range(chunk,exponent+1,chunk)))
        lines.append(f"theorem pow_{base}_0 : ({base} : Nat)^0 = 1 := rfl\n")
        for a,bend in zip(vals,vals[1:]):
            b=bend-a;v,w,res=base**a,base**b,base**bend
            lines.append(f"theorem pow_{base}_{bend} : ({base} : Nat)^{bend} = {res} := by\n"
              f"  exact (power_step {base} {a} {b} {v} {w} pow_{base}_{a} (by decide)).trans (by decide)\n")
    for n in odd_ranges:
        vals=sorted({0,n}|set(range(chunk,n+1,chunk)))
        value=1
        lines.append(f"theorem odd_prefix_{n}_0 : (∏ k ∈ Finset.range 0, oddTerm k) = 1 := rfl\n")
        for a,bend in zip(vals,vals[1:]):
            b=bend-a;w=math.prod(k if k%2 else 1 for k in range(a,bend))
            result=value*w
            lines.append(f"theorem odd_prefix_{n}_{bend} : (∏ k ∈ Finset.range {bend}, oddTerm k) = {result} := by\n"
              f"  exact (prod_step oddTerm {a} {b} {value} {w} odd_prefix_{n}_{a} (by decide)).trans (by decide)\n")
            value=result
        lines.append(f"theorem odd_{n} : Finset.prod (Finset.filter (fun k : Nat => ¬Even k) (Finset.range {n})) id = {value} :=\n"
          f"  (odd_filter {n}).trans odd_prefix_{n}_{n}\n")
    lines.append("end MClosedNat\n")
    for n in factorials:lines.append(f"#print axioms MClosedNat.fac_{n}\n")
    for n in odd_ranges:lines.append(f"#print axioms MClosedNat.odd_{n}\n")
    f=out/"ClosedNatFacts.lean";f.write_text("".join(lines))
    meta={"factorials":factorials,"powers":powers,"odd_ranges":odd_ranges,"chunk":chunk,
      "untrusted_generator":True,"proof_source_bytes":f.stat().st_size,"generation_wall_s":time.monotonic()-began,
      "proof_obligation":"stock kernel checks every chunk+composition; raw numerals cannot accept without checked equality"}
    (out/"generation.json").write_text(json.dumps(meta,indent=2)+"\n")
    return f
if __name__=="__main__":
    root=Path("/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30")
    print(emit(root/"closed-nat-facts415-v1",[942,5000,10000],[(2,5000),(15,233),(5,234)],[10000]))
