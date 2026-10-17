"""Build native arithmetic stage instrumentation from pinned Mathlib 4.27 sources.
Root-only benchmark; original sources stay untouched. Thread CPU is measured
on the calling Lean worker; stages are sequential inside each tactic invocation.
"""
from pathlib import Path
import os, subprocess, json
R=Path('/workspaces/repository')
B=Path('/tmp/gpu-smt-goedel427-20261014')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017'); U.mkdir(exist_ok=True)
(U/'GpuArithmetic').mkdir(exist_ok=True)
sdk=B/'lean-4.27.0-linux'
math=B/'mathlib4/Mathlib/Tactic/Linarith'
head='''import Mathlib.Tactic.Linarith.Frontend
import Farkas.Native
import Farkas.Fast
open Lean Meta Elab Tactic Mathlib.Tactic.Linarith
namespace GpuArithmetic.Stages
@[extern "gpu_smt_thread_cpu_ns"] opaque threadCpuNs : IO UInt64
abbrev Costs := Std.HashMap String (Nat × Nat)
def timed (ref : IO.Ref Costs) (name : String) (act : MetaM α) : MetaM α := do
  let w ← IO.monoNanosNow
  let c ← threadCpuNs
  try act
  finally
    let dc := (← threadCpuNs).toNat - c.toNat
    let dw := (← IO.monoNanosNow) - w
    ref.modify fun m =>
      let old := m.getD name (0,0)
      m.insert name (old.1 + dc, old.2 + dw)

'''
ver=(math/'Verification.lean').read_text()
ver=ver[ver.index('def proveFalseByLinarith '):ver.rindex('end Mathlib.Tactic.Linarith')]
ver=ver.replace('``Linarith.lt_irrefl','``Mathlib.Tactic.Linarith.lt_irrefl')
ver=ver.replace('def proveFalseByLinarith (transparency','def proveFalseByLinarith (cost : IO.Ref Costs) (transparency',1)
ver=ver.replace('let l\' ← detailTrace','let l\' ← timed cost "linearize" <| detailTrace',1)
ver=ver.replace('detailTrace "mkNegOneLtZeroProof" <|','timed cost "linearize" <| detailTrace "mkNegOneLtZeroProof" <|',1)
ver=ver.replace('← detailTrace "linearFormsAndMaxVar" <|','← timed cost "linearize" <| detailTrace "linearFormsAndMaxVar" <|',1)
ver=ver.replace('withTraceNode `linarith (return m!"{exceptEmoji ·} Invoking oracle") do','timed cost "lp" <| withTraceNode `linarith (return m!"{exceptEmoji ·} Invoking oracle") do',1)
i=ver.index('      let (sm, zip, idxs) ←')
j=ver.index('\nwhere',i)
ver=ver[:i]+'      timed cost "certificate" do\n'+'\n'.join('  '+l for l in ver[i:j].splitlines())+ver[j:]
front=(math/'Frontend.lean').read_text()
front=front[front.index('def findLinarithContradiction '):front.index('\nend Linarith')]
front=front.replace('Linarith.removeNe','Mathlib.Tactic.Linarith.removeNe').replace('Linarith.splitConjunctions','Mathlib.Tactic.Linarith.splitConjunctions')
front=front.replace('def findLinarithContradiction (cfg','def findLinarithContradiction (cost : IO.Ref Costs) (cfg',1)
front=front.replace('def runLinarith (cfg','def runLinarith (cost : IO.Ref Costs) (cfg',1)
front=front.replace('partial def linarithUsedHyps (only_on','partial def linarithUsedHyps (cost : IO.Ref Costs) (only_on',1)
front=front.replace('partial def linarith (only_on','partial def linarith (cost : IO.Ref Costs) (only_on',1)
front=front.replace('proveFalseByLinarith cfg.', 'GpuArithmetic.Stages.proveFalseByLinarith cost cfg.')
front=front.replace('findLinarithContradiction cfg ', 'GpuArithmetic.Stages.findLinarithContradiction cost cfg ')
front=front.replace('linarithUsedHyps only_on', 'GpuArithmetic.Stages.linarithUsedHyps cost only_on')
front=front.replace('runLinarith cfg target_type','GpuArithmetic.Stages.runLinarith cost cfg target_type')
front=front.replace('let branches ← preprocess preprocessors g hyps','''preprocessors := preprocessors.map fun pp =>
    { pp with transform := fun g hs => timed cost (if pp.description == "nonlinear arithmetic extras" then "products" else "preprocess") (pp.transform g hs) }
  let branches ← preprocess preprocessors g hyps''')
tail='''
def run (nlin onlyOn : Bool) (args : List Expr) (cfg : LinarithConfig) : TacticM Unit := do
  if (← IO.getEnv "GPU_ARITHMETIC_PROFILE").isNone then throwUnsupportedSyntax
  let cost ← IO.mkRef ({} : Costs)
  let w ← IO.monoNanosNow
  let c ← threadCpuNs
  let cfg := if nlin then { cfg with preprocessors := cfg.preprocessors.concat nlinarithExtras } else cfg
  try
    commitIfNoEx do liftMetaFinishingTactic <| GpuArithmetic.Stages.linarith cost onlyOn args cfg
  finally
    let dc := (← threadCpuNs).toNat - c.toNat
    let dw := (← IO.monoNanosNow) - w
    if (← IO.getEnv "GPU_ARITHMETIC_PROFILE").isSome then
      let stats ← cost.get
      let source := (← getFileMap).source
      let fields := [("ty","\\"arithmetic-stages\\""),("source",Farkas.Telemetry.jstrEsc source),
        ("nlin",if nlin then "true" else "false"),("cpu_ns",toString dc),("wall_ns",toString dw),
        ("stages","{" ++ ",".intercalate (stats.toList.map fun (k,v) =>
          Farkas.Telemetry.jstrEsc k ++ ":[" ++ toString v.1 ++ "," ++ toString v.2 ++ "]") ++ "}")]
      Farkas.Telemetry.emit (Farkas.Telemetry.row fields)

elab_rules : tactic
  | `(tactic| linarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `linarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run false o.isSome args.toList cfg

elab_rules : tactic
  | `(tactic| nlinarith $[!%$bang]? $cfg:optConfig $[only%$o]? $[[$args,*]]?) => withMainContext do
    let args ← ((args.map (Syntax.TSepArray.getElems)).getD {}).mapM (elabTermWithoutNewMVars `nlinarith)
    let cfg := (← Mathlib.Tactic.elabLinarithConfig cfg).updateReducibility bang.isSome
    run true o.isSome args.toList cfg
end GpuArithmetic.Stages
'''
source=head+ver+front+tail
(U/'GpuArithmetic/Stages.lean').write_text(source)
(U/'clock.c').write_text('#include <lean/lean.h>\n#include <time.h>\nLEAN_EXPORT lean_obj_res gpu_smt_thread_cpu_ns(lean_obj_arg w) {struct timespec t; clock_gettime(CLOCK_THREAD_CPUTIME_ID,&t);return lean_io_result_mk_ok(lean_box_uint64((uint64_t)t.tv_sec*1000000000ULL+t.tv_nsec));}\nLEAN_EXPORT lean_obj_res l_GpuArithmetic_Stages_threadCpuNs(lean_obj_arg w) {return gpu_smt_thread_cpu_ns(w);}\n')
env=dict(os.environ)
env['PATH']=str(sdk/'bin')+':'+env['PATH']
paths=[str(U),str(F/'.lake/build/lib/lean'),str(B/'mathlib4/.lake/build/lib/lean')]
paths += [str(p/'.lake/build/lib/lean') for p in (B/'mathlib4/.lake/packages').iterdir() if p.is_dir()]
env['LEAN_PATH']=':'.join(paths)
with (U/'build.log').open('w') as log:
 def call(cmd):
  log.write(repr(cmd)+'\n');log.flush()
  subprocess.run(cmd,cwd=U,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 call(['lean','-o',str(U/'GpuArithmetic/Stages.olean'),'-c',str(U/'Stages.c'),str(U/'GpuArithmetic/Stages.lean')])
 call(['cc','-O3','-fPIC','-I'+str(sdk/'include'),'-c',str(U/'clock.c'),'-o',str(U/'clock.o')])
 cs=[str(F/'.lake/build/ir/Farkas'/ (m+'.c')) for m in ['Platform','Telemetry','Native','Fast']]
 call(['leanc','-O3','-shared','-fPIC',str(U/'Stages.c'),str(U/'clock.o'),*cs,'-o',str(U/'arithmetic.so')])
print(json.dumps({'built':str(U/'arithmetic.so')}),flush=True)
