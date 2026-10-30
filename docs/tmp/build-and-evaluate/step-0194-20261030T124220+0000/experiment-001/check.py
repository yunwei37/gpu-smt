from pathlib import Path
import json,os,time,resource
os.sched_setaffinity(0,{0,1});start=time.monotonic()
r=Path('/workspaces/repository');p=Path(__file__).parent
root=r/'research/mechanisms-2026-10-30/accepted-original-analysis'
models=json.loads((root/'local-model-per-source.json').read_text())
raw=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/captures/accepted-original-s0-linked-on')
rows=[json.loads(line[6:]) for line in (raw/'stdout.txt').open()if line.startswith('M_DAG ')]
byid={x['id']:x for x in rows};assert len(rows)==len(byid)==len(models)==50 and {x['id']for x in models}==set(byid)
receipt=json.loads((raw/'receipt.json').read_text());assert receipt['exit']==0 and receipt['retired']
full=receipt['wall_s'];cpu=sum(x['cpuNanoseconds']/1e9 for x in rows);body=sum(x['wallNanoseconds']/1e9 for x in rows);outside=full-body;assert outside>=0
finite={};candidate=[]
for cores in [1,2,4,8]:
 key=str(cores);saved_cpu=sum(x['finite_core_island_models'][key]['saved_cpu_s']for x in models)
 # Model sensitivity only: retain each source's measured wall/CPU multiplier.
 saved_wall=sum(x['finite_core_island_models'][key]['saved_cpu_s']*byid[x['id']]['wallNanoseconds']/byid[x['id']]['cpuNanoseconds'] for x in models)
 assert 0<=saved_wall<body and 0<=saved_cpu<cpu
 finite[key]={'modeled_CPU_equivalent_reduction_s':saved_cpu,'body_CPU_model_ratio':cpu/(cpu-saved_cpu),'modeled_wall_reduction_s':saved_wall,'full_process_wall_model_s':full-saved_wall,'full_process_wall_model_ratio':full/(full-saved_wall)}
for x in models:
 if x['finite_core_island_models']['8']['saved_cpu_s']>0:
  candidate.append({'id':x['id'],'body_CPU_s':x['body_cpu_s'],'saved_CPU_equivalent_8core_s':x['finite_core_island_models']['8']['saved_cpu_s'],'saved_wall_8core_s':x['finite_core_island_models']['8']['saved_cpu_s']*byid[x['id']]['wallNanoseconds']/byid[x['id']]['cpuNanoseconds']})
candidate.sort(key=lambda x:x['saved_CPU_equivalent_8core_s'],reverse=True)
out={'source':'9b67361','native_returns':50,'additional_native_calls':0,'raw_capture':str(raw),'complete_process_wall_s':full,'candidate_body_wall_s':body,'candidate_body_CPU_s':cpu,'outside_body_wall_s':outside,'outside_body_wall_fraction':outside/full,'finite_core_sensitivity':finite,'eligible_sources_ranked':candidate,'top3_fraction_of_modeled_CPU_reduction':sum(x['saved_CPU_equivalent_8core_s']for x in candidate[:3])/finite['8']['modeled_CPU_equivalent_reduction_s'],'assumptions':['Retain every source original body wall/CPU ratio when mapping its CPU-span opportunity to wall.','Keep all measured work outside candidate-body timers serial and unchanged.','No parallel runtime, overhead, scheduler, memory admission, diagnostic or heartbeat reconciliation costs measured.','This single ordered serial SDK capture is not a precompiled warm-service clock.','No transfer to other candidates, failures, full7808 or other hardware; not a general Amdahl impossibility bound.','Top3 concentration is retrospective, not a scheduling predictor.']}
out.update(root_elapsed_s=time.monotonic()-start,root_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(p/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
