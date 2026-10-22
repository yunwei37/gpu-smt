"""Only closed reference1000: own-clock Lean/helper costs, no rescaled bounds."""
from pathlib import Path
import subprocess,sys,json,runpy,collections
O=Path(__file__).resolve().parent
p=O/'reference-full1000/terminal.json'
if not p.exists()or json.loads(p.read_text())['state']!='complete':
 raise SystemExit('Original1000 helper capture not terminal; do not read it as complete')
for argv in [[sys.executable,str(O/'analyze-full.py'),'reference-full1000'],
             [sys.executable,str(O/'analyze-reference-helper.py'),'full']]:
 z=subprocess.run(argv,capture_output=True,text=True)
 if z.returncode:raise RuntimeError(z.stderr or z.stdout)
lean=json.loads((O/'reference-stage-analysis.json').read_text())
helper=json.loads((O/'reference-full-analysis.json').read_text())
h=helper['profiles']['reference-full1000']
assert lean['own_profile_whole_seconds']==h['own_whole_seconds']
sys.argv=[str(O/'analyze-reference-helper.py'),'full']
M=runpy.run_path(str(O/'analyze-reference-helper.py'))
rows=M['rows'];ident=M['ident'];union=M['union']
lp_spans=collections.defaultdict(list)
for x in rows(O/'reference-full1000/native-stages.jsonl'):
 i=ident(x['source'])
 for name,a,b in x['spans']:
  if name=='lp':lp_spans[i].append((a,b))
pending={};owned=collections.defaultdict(list);unknown=[];outside=[]
for x in rows(O/'reference-full1000/native-helper-phases.jsonl'):
 if x.get('stage')!='native_reference_request':continue
 key=(x['pid'],x['tid'],x['id'])
 if x['event']=='begin':
  assert key not in pending;pending[key]=x
 else:
  a=pending.pop(key,None)
  if a is None:unknown.append(x);continue
  i=ident(a.get('source'))
  if i is None:unknown.append(x);continue
  span=(a['wall_ns'],x['wall_ns'])
  if not any(b<=span[0]<=span[1]<=e for b,e in lp_spans[i]):outside.append(dict(source=i,begin=span[0],end=span[1]))
  owned[i].append(span)
lp_wall=lean['stage_CPU_wall_seconds']['lp'][1]
covered=sum(union(v)for v in owned.values())
cpu_wall=lean['stage_CPU_wall_seconds']
whole=h['own_whole_seconds']
out=dict(scope='Complete original1000 own-instrumented-clock composition; root self-review. Not a GPU measurement or strict impossibility bound.',
 own_profile_whole_seconds=whole,
 native_outcome_difference_IDs=lean['native_outcome_difference_IDs'],
 raw_response_difference_IDs=lean['raw_response_difference_IDs'],
 stage_CPU_wall_seconds=cpu_wall,
 helper_stage_CPU_wall_count=h['stage_CPU_wall_count'],
 paired_helper_request_source_count=len(owned),
 pending_helper_requests=list(pending.values()),unknown_helper_requests=len(unknown),
 helper_requests_not_contained_in_own_Lean_LP=outside,
 helper_request_per_source_interval_union_sum_seconds=covered,
 LPwrapper_wall_not_covered_by_native_helper_request_seconds=(lp_wall-covered)if not outside else None,
 products_plus_FP_or_exact_fallback_envelope_accumulated_wall_seconds=cpu_wall['products'][1]+h['FP_solver_plus_exact_fallback_envelope_accumulated_wall_seconds'],
 product_LP_global_occupied_seconds=lean['product_LP_global_interval_union_seconds'],
 observed_LP_wrapper_wall_over_own_whole=lp_wall/whole,
 observed_product_wall_over_own_whole=cpu_wall['products'][1]/whole,
 actual_FP_matrix_shapes=h['actual_FP_matrix_shapes'],
 hypothetical_matrix_ready_to_answer_overlap_pair_count=len(h['matrix_ready_until_native_answer_cross_source_overlap_pairs']),
 maximum_simultaneously_open_matrix_windows=h['maximum_simultaneously_open_matrix_windows'],
 coverage_limits=['Accumulated concurrent wall fractions are not additive removable critical path.',
  'Exact fallback includes matrix construction, coefficient conversion and rational cleanup.',
  'Uncovered LPwrapper wall includes Lean packing/IPC/stock fallback/queueing; it is not measured communication alone.',
  'Outer elaboration,omega,configured/indirect stock paths and hard-death omissions remain unknown.',
  'Per-call nonlinear product provenance and exact-tableau shapes unavailable; no missing input becomes zero.',
  'Fixed-order/shared-host instrumentation controls are reported separately; no old denominator rescaling.'])
(O/'reference-combined-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
