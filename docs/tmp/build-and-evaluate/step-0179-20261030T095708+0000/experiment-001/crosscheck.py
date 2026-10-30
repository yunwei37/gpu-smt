import csv,gzip,io,json,math,os,resource,subprocess,time
from pathlib import Path
os.sched_setaffinity(0,{0,1})
resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3))
r=Path('/workspaces/repository');s=Path(Path('/workspaces/.agent-state/gpu-smt-paper-outcome-cost-step.txt').read_text().strip());e=s/'experiment-001';start=time.monotonic()
frozen=lambda rev,path:subprocess.check_output(['git','show',rev+':'+path],cwd=r).decode()
with gzip.open(r/'artifacts/autoverus-native-2026-10-09/full/analysis/cells.json.gz','rt') as f: cells=json.load(f)
published=list(csv.DictReader(io.StringIO(frozen('ea41025','workloads/candidates/autoverus-outcome-time.csv'))))
result=[]
for rep in range(3):
 rows=[x for x in cells if x['condition']=='direct' and x['repetition']==rep]
 assert len(rows)==len({x['candidate'] for x in rows})==3566
 assert all(x['complete'] and not x['timed_out'] for x in rows)
 wall=lambda xs:math.fsum(x['external_wall_s'] for x in xs)
 den=wall(rows)
 groups={}
 for row in rows:
  native=(row.get('native_json') or {}).get('verification-results') or {}
  key=(row['returncode'],str(native.get('success','missing')),str(native.get('encountered-vir-error','missing')))
  groups.setdefault(key,[]).append(row)
 for (rc,success,vir),members in groups.items():
  report=next(p for p in published if int(p['repetition'])==rep and int(p['returncode'])==rc and p['native_json_success']==success and p['native_json_encountered_vir_error']==vir)
  assert len(members)==int(report['candidates'])
  assert math.isclose(wall(members),float(report['process_wall_s']),abs_tol=1e-8,rel_tol=1e-12)
  assert math.isclose(den,float(report['denominator_process_wall_s']),abs_tol=1e-8,rel_tol=1e-12)
 nonzero=[x for x in rows if x['returncode']!=0]
 false=[x for x in rows if ((x.get('native_json') or {}).get('verification-results') or {}).get('success') is False]
 success_exit1=groups[(1,'True','False')]
 tail=sorted(rows,key=lambda x:x['external_wall_s'],reverse=True)[:math.ceil(.016*len(rows))]
 assert len(nonzero)==3376 and len(false)==2940 and len(success_exit1)==419
 result.append({'repetition':rep,'candidates':3566,'process_wall_s':den,'nonzero_candidates':len(nonzero),'nonzero_wall_s':wall(nonzero),'nonzero_wall_fraction':wall(nonzero)/den,'native_json_false_candidates':len(false),'native_json_false_wall_s':wall(false),'native_json_false_wall_fraction':wall(false)/den,'json_success_exit1_candidates':len(success_exit1),'json_success_exit1_wall_s':wall(success_exit1),'json_success_exit1_wall_fraction':wall(success_exit1)/den,'tail_candidates':len(tail),'tail_wall_fraction':wall(tail)/den,'exit101_missing_json':len(groups[(101,'missing','missing')]),'cross_tab_cells':len(groups)})
# Verify bounded sampling conservation without interpreting assumed time/RSS coefficients.
base='workloads/openai-math/build-planning-4eaee875/'
summary=json.loads(frozen('ea41025',base+'phaseA-summary.json'))
targets=list(csv.DictReader(io.StringIO(frozen('ea41025',base+'phaseA-targets.csv'))))
assert len(targets)==summary['phaseA_targets']==53
planning={'phaseA_targets':53,'probability_targets':summary['phaseA_probability_targets'],'internal_closure_modules':summary['phaseA_closure_modules'],'internal_source_bytes':summary['phaseA_closure_source_bytes'],'external_import_modules':summary['external_import_modules'],'native_RSS_unknown':summary['native_RSS_unknown'],'native_build_or_cost_evidence':False,'coefficients_calibrated':False}
# The M controls are engagement only, not a native workload cost or speedup.
prefix='research/mechanisms-2026-10-30/native/phobos-dag-core-control-v4/'
receipt=json.loads(frozen('949622a',prefix+'receipt.json'))
native=[json.loads(line.removeprefix('M_DAG ')) for line in frozen('949622a',prefix+'stdout.txt').splitlines() if line.startswith('M_DAG ')]
assert {x['id'] for x in native}=={'independent','coupled'} and all(not x['hasErrors'] for x in native)
def count(nodes,tactic_only=False):
 return sum((1 if 'kind' in n and (not tactic_only or n['kind'].startswith('Lean.Parser.Tactic.')) else 0)+count(n.get('children',[]),tactic_only) for n in nodes)
controls=[{'id':x['id'],'all_trace_kind_nodes':count(x['traces']),'all_info_kind_nodes':count(x['infos']),'tactic_trace_nodes':count(x['traces'],True),'tactic_info_nodes':count(x['infos'],True),'wall_ns':x['wallNanoseconds'],'cpu_ns':x['cpuNanoseconds']} for x in native]
assert [(x['tactic_trace_nodes'],x['tactic_info_nodes']) for x in controls]==[(28,18),(9,6)]
data={'W_commit':'ea410258484b8dc27471cd6cc173448099bc9be5','M_commit':'949622a78524a9726fbc68aa54a5bf052594cb4f','native_runs_by_root':0,'retained_direct_cells_reanalysis':result,'planning_scope':planning,'M_control_nodes':controls,'M_native_receipt':receipt,'limits':['Summed individual process walls are not service makespan or generation time.','Nonzero process exit and partial native JSON are different observations, neither defines reusable advance failure.','Tiny dependency controls do not establish a critical path or parallel speedup.','Static build scenarios are uncalibrated and not native execution evidence.'],'elapsed_s':time.monotonic()-start,'root_affinity':sorted(os.sched_getaffinity(0)),'root_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'outcome-cost-check.json').write_text(json.dumps(data,indent=2)+'\n')
with (e/'outcome-cost.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(result[0]),lineterminator='\n');w.writeheader();w.writerows(result)
print(json.dumps(data,indent=2))
