from pathlib import Path
import os,sys,json,csv,math,resource,time,datetime
os.sched_setaffinity(0,{0,1});t0=time.monotonic()
root=Path('/workspaces/repository');raw=Path('/workspaces/.agent-state/gpu-smt-captures/workloads')
old=[json.loads(l) for l in (raw/'openai4341-native-expanded/results.jsonl').open()]
p=raw/'openai4341-native-resume100k';rows=[json.loads(l) for l in (p/'results.jsonl').open()]
term=json.loads((p/'terminal.json').read_text());outer=json.loads((p/'capture-terminal.json').read_text())
assert len(rows)==47 and len({r['module'] for r in rows})==47 and outer['exit_code']==0
prior_success={x['module'] for x in old if x['status']=='compile_ok'}
prior_blocked={x['module'] for x in old if x['status']!='compile_ok'}
new_success={x['module'] for x in rows}
assert len(prior_success)==81 and len(prior_blocked)==47 and new_success==prior_blocked and not(prior_success&new_success)
all_success=prior_success|new_success;assert len(all_success)==128
for x in rows:
 assert x['status']=='compile_ok' and x['returncode']==0 and not x['sorry_warning']
 assert x['heartbeat_budget']==100000 and x['lean_memory_option_MiB']==8192 and x['threads']==1
 stat=Path('/proc')/str(x['pid'])/'stat'
 if stat.exists():assert stat.read_text().split(') ',1)[1].split()[19]!=x['birth_ticks']
pub=list(csv.DictReader((root/'workloads/openai-math/native-resume100k-4341/modules.csv').open()))
assert len(pub)==47
for x in pub:
 y=next(r for r in rows if r['module']==x['module'])
 assert x['status']==y['status'] and math.isclose(float(x['wall_s']),y['wall_s'],rel_tol=1e-12)
targets=[x['module'] for x in csv.DictReader((root/'workloads/openai-math/native-expanded-4341/targets.csv').open())]
assert len(targets)==3 and set(targets)<=all_success
pilot=[json.loads(l) for l in (raw/'openai4341-profile-ab/results.jsonl').open()]
pilotids={x['module'] for x in pilot};assert len(pilotids)==7 and len(pilotids|all_success)==135
mem=list(csv.DictReader((p/'memory.csv').open()));peak=max(int(x['tree_rss_bytes']) for x in mem)
assert peak==outer['sampled_tree_peak_bytes']
first=next(x for x in rows if x['module'].endswith('.ProjectionCoordinates'))
d={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_invocations':0,
 'prior_50k_successful_dependencies':len(prior_success),'incremental_100k_actual_calls':len(rows),'incremental_100k_successes':len(new_success),
 'distinct_closure_modules_now_successful_across_points':len(all_success),'target_endpoints_available':targets,
 'old50k_failed_or_uninvoked_preserved':True,'single_budget_fresh_full_capture_claimed':False,
 'native_process_wall_sum_s':math.fsum(x['wall_s'] for x in rows),'native_user_cpu_sum_s':math.fsum(x['user_cpu_s'] for x in rows),
 'native_system_cpu_sum_s':math.fsum(x['system_cpu_s'] for x in rows),'combined_W_sampled_peak_bytes':peak,
 'unique_objects_including_prior_pilot':len(pilotids|all_success),'rechecked_dependency':first,
 'capture_terminal':outer,'native_terminal':term,'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
