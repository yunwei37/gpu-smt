"""Instrument the executed Fast/hybrid strong baseline without changing its selection.
Generated files and separate diagnostic .so stay outside the repository.
"""
from pathlib import Path
import os,subprocess
R=Path('/workspaces/repository');U=Path('/tmp/gpu-smt-linarith-oracle-20261017')
T=Path('/tmp/gpu-smt-goedel427-20261014')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
s=(F/'Farkas/Fast.lean').read_text()
s=s.replace('import Farkas.Native','import Farkas.Native\nimport GpuArithmetic.Stages')
s=s.replace('namespace Farkas.Fast','namespace GpuArithmetic.FastProfile').replace('end Farkas.Fast','end GpuArithmetic.FastProfile')
s=s.replace('Farkas.Fast.runP','GpuArithmetic.FastProfile.runP')
s=s.replace('Telemetry.', 'Farkas.Telemetry.')
s=s.replace('private def runProbe (hyps','private def runProbe (cost : IO.Ref GpuArithmetic.Stages.Costs) (hyps')
s=s.replace('private def probeAndRestrict (nlin','private def probeAndRestrict (cost : IO.Ref GpuArithmetic.Stages.Costs) (nlin')
s=s.replace('def tryFast (nlin','def tryFast (cost : IO.Ref GpuArithmetic.Stages.Costs) (nlin')
s=s.replace('(probeAndRestrict nlin','(probeAndRestrict cost nlin')
s=s.replace('g.withContext do\n    if (← Farkas.findBinary)', 'g.withContext do\n    let cost ← IO.mkRef ({} : GpuArithmetic.Stages.Costs)\n    if (← Farkas.findBinary)')
s=s.replace('← runProbe hyps maxVar','← GpuArithmetic.Stages.timed cost "lp" (runProbe cost hyps maxVar)')
start=s.index('private def probeAndRestrict')
body=s[start:]
body=body.replace('g.withContext do\n', 'g.withContext do\n      let prepWall ← IO.monoNanosNow\n      let prepCpu ← GpuArithmetic.Stages.threadCpuNs\n',1)
body=body.replace('let tParse ← IO.monoNanosNow','''let tParse ← IO.monoNanosNow
      let prepCpuEnd ← GpuArithmetic.Stages.threadCpuNs
      cost.modify fun m =>
        let old := m.getD "preprocess" (0,0)
        m.insert "preprocess" (old.1 + prepCpuEnd.toNat - prepCpu.toNat, old.2 + tParse - prepWall)''',1)
old='''          let pool := hyps
          let mut prods : List ProbeHyp := []
          for (a, i) in pool.zipIdx do
            for (b, j) in pool.zipIdx do
              if i ≤ j then
                if let some p ← runP (probeProduct a b) then
                  prods := prods.cons p
          hyps := hyps ++ prods'''
new='''          let pool := hyps
          let prods ← GpuArithmetic.Stages.timed cost "products" do
            let mut prods : List ProbeHyp := []
            for (a, i) in pool.zipIdx do
              for (b, j) in pool.zipIdx do
                if i ≤ j then
                  if let some p ← runP (probeProduct a b) then
                    prods := prods.cons p
            return prods
          hyps := hyps ++ prods'''
assert old in body;body=body.replace(old,new,1)
body=body.replace('Mathlib.Tactic.Linarith.linarith true s cfg g','GpuArithmetic.Stages.linarith cost true s cfg g',1)
s=s[:start]+body
(U/'GpuArithmetic/FastProfile.lean').write_text(s)
base=(R/'bench/lean-native/linarith-oracle/Baseline.lean').read_text()
base=base.replace('import Farkas.Fast','import GpuArithmetic.FastProfile')
base=base.replace('namespace GpuArithmetic.Baseline','namespace GpuArithmetic.StrongProfile').replace('end GpuArithmetic.Baseline','end GpuArithmetic.StrongProfile')
base=base.replace('if (← IO.getEnv "GPU_ARITHMETIC_BASELINE").isNone','if (← IO.getEnv "GPU_ARITHMETIC_STRONG_PROFILE").isNone',1)
base=base.replace('  let saved ← saveState','''  let cost ← IO.mkRef ({} : GpuArithmetic.Stages.Costs)
  let cpu0 ← GpuArithmetic.Stages.threadCpuNs
  let wall0 ← IO.monoNanosNow
  try
    runInstrumented cost nlin onlyOn args cfg
  finally
    let dc := (← GpuArithmetic.Stages.threadCpuNs).toNat - cpu0.toNat
    let dw := (← IO.monoNanosNow) - wall0
    let stats ← cost.get
    let source := (← getFileMap).source
    Farkas.Telemetry.emit (Farkas.Telemetry.row [
      ("ty",Farkas.Telemetry.jstrEsc "strong-arithmetic-stages"),
      ("source",Farkas.Telemetry.jstrEsc source),
      ("cpu_ns",toString dc),("wall_ns",toString dw),
      ("stages","{" ++ ",".intercalate (stats.toList.map fun (k,v) =>
        Farkas.Telemetry.jstrEsc k ++ ":[" ++ toString v.1 ++ "," ++ toString v.2 ++ "]") ++ "}")])
where
 runInstrumented (cost : IO.Ref GpuArithmetic.Stages.Costs)
     (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  let saved ← saveState''',1)
i=base.index('  let saved ← saveState');j=base.index('\nelab_rules',i)
base=base[:i]+'\n'.join(' '+l for l in base[i:j].splitlines())+base[j:]
base=base.replace('Farkas.Fast.tryFast nlin','GpuArithmetic.FastProfile.tryFast cost nlin')
base=base.replace('Mathlib.Tactic.Linarith.linarith onlyOn args','GpuArithmetic.Stages.linarith cost onlyOn args')
(U/'GpuArithmetic/StrongProfile.lean').write_text(base)
env=dict(os.environ);env['PATH']=str(T/'lean-4.27.0-linux/bin')+':'+env['PATH']
env['LEAN_PATH']=':'.join([str(U),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean') for p in (T/'mathlib4/.lake/packages').iterdir() if p.is_dir()])
for name in ['FastProfile','StrongProfile']:
 subprocess.run(['lean','-o',str(U/'GpuArithmetic'/ (name+'.olean')),'-c',str(U/(name+'.c')),str(U/'GpuArithmetic'/(name+'.lean'))],env=env,cwd=U,check=True)
subprocess.run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',str(U/'FastProfile.c'),str(U/'StrongProfile.c'),'-o',str(U/'strong-profile.so')],env=env,cwd=U,check=True)
print('Built separate strong-profile.so; existing primary library unchanged.',flush=True)
