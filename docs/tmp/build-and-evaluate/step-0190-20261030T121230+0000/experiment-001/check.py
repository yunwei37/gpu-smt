from pathlib import Path
import os,sys,json,csv,collections,math,time,resource,datetime,signal
os.sched_setaffinity(0,{0,1});t0=time.monotonic();root=Path('/workspaces/repository')
raw=Path('/workspaces/.agent-state/gpu-smt-captures/workloads')
p=raw/'openai4341-native-expanded';rows=[json.loads(l) for l in (p/'results.jsonl').open()]
term=json.loads((p/'terminal.json').read_text());outer=json.loads((p/'capture-terminal.json').read_text())
assert len(rows)==128 and len({x['module'] for x in rows})==128 and term['rows']==128 and outer['exit_code']==0
counts=collections.Counter(x['status'] for x in rows);assert counts=={'compile_ok':81,'budget_exceeded':1,'dependency_not_compiled':46}
run=[x for x in rows if x['status']!='dependency_not_compiled'];skip=[x for x in rows if x['status']=='dependency_not_compiled']
for x in run:
 assert x['heartbeat_budget']==50000 and x['lean_memory_option_MiB']==8192 and x['threads']==1
 assert x['affinity']==list(range(8)) and x['sorry_warning'] is False
 assert x['returncode']==(0 if x['status']=='compile_ok' else 1)
 stat=Path('/proc')/str(x['pid'])/'stat'
 if stat.exists():assert stat.read_text().split(') ',1)[1].split()[19]!=x['birth_ticks']
for x in skip:assert 'wall_s' not in x or x['wall_s'] is None
published=list(csv.DictReader((root/'workloads/openai-math/native-expanded-4341/modules.csv').open()))
assert {x['module'] for x in rows}=={x['module'] for x in published}
for x in published:
 y=next(v for v in rows if v['module']==x['module']);assert x['status']==y['status']
 if x['status']=='dependency_not_compiled':assert x['wall_s']==x['returncode']==''
 else:assert math.isclose(float(x['wall_s']),y['wall_s'],rel_tol=1e-12)
mem=list(csv.DictReader((p/'memory.csv').open()))
peak=max(int(x['tree_rss_bytes']) for x in mem);assert peak==outer['sampled_tree_peak_bytes']
targets=list(csv.DictReader((root/'workloads/openai-math/native-expanded-4341/targets.csv').open()))
assert len(targets)==3 and len([t for t in targets if t['native_status']=='compile_ok'])==2
fail=[x for x in run if x['status']=='budget_exceeded'];assert len(fail)==1
log=Path(fail[0]['log']).read_text();assert 'whnf' in log and 'heartbeat' in log.lower()
ep=raw/'candidate-epfl-pending-v3';erows=[json.loads(l) for l in (ep/'results.jsonl').open()]
eterm=json.loads((ep/'terminal.json').read_text());eouter=json.loads((ep/'capture-terminal.json').read_text())
assert len(erows)==7 and eterm['rows']==eterm['planned_rows']==7 and eouter['exit_code']==0
ecount=collections.Counter(x['status'] for x in erows)
assert sorted(ecount.values())==[1,1,2,3],ecount
old=[json.loads(l) for l in (raw/'candidate-native-v1-snapshot-1109/results.jsonl').open()]
oldids={x['case_id'] for x in old if x['dataset']=='EPFL-evaluation'}
assert len(oldids)==136 and not(oldids&{x['case_id'] for x in erows}) and 'epfl-58969' not in {x['case_id'] for x in erows}
alarms=[]
for x in erows:
 assert x['native_version']=='4.15.0' and x['heartbeats']==10000 and x['native_memory_option_MiB']==6144
 if x['returncode']==-signal.SIGALRM:alarms.append({'id':x['case_id'],'wall_s':x['wall_s'],'returncode':x['returncode']})
assert len(alarms)==2 and all(x['wall_s']>=15 for x in alarms)
d={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_invocations':0,
 'module_states':dict(counts),'native_compiler_invocations':len(run),'native_process_wall_sum_s':math.fsum(x['wall_s'] for x in run),
 'native_user_cpu_sum_s':math.fsum(x['user_cpu_s'] for x in run),'native_system_cpu_sum_s':math.fsum(x['system_cpu_s'] for x in run),
 'source_budget_replacements_recorded':sum(x['replaced_source_budget_settings'] for x in run),
 'targets':targets,'budget_failure':fail[0],'combined_W_peak_RSS_bytes':peak,'capture_terminal':outer,'native_terminal':term,
 'later_EPFL7_counts':dict(ecount),'later_EPFL7_capture_terminal':eouter,'later_EPFL7_native_terminal':eterm,
 'later_EPFL7_alarm_returns':alarms,'original_frame_matched_budget_complete':False,'old_unreturned_not_labeled_failure':True,
 'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
