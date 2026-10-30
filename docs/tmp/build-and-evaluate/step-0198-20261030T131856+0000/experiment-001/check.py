from pathlib import Path
import os,json,csv,re,collections,time,resource
os.sched_setaffinity(0,{0,1});start=time.monotonic()
r=Path('/workspaces/repository');e=Path(__file__).parent
b=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/openai4341-grid-profile300')
rows=[json.loads(x)for x in (b/'results.jsonl').read_text().splitlines()];assert len(rows)==1;row=rows[0]
assert row['module']=='OAI.Analysis.PlanarPacking.Grid' and row['returncode']==-14 and row['status']=='wall_budget_exceeded' and row['profiled']
assert row['heartbeat_budget']==100000 and row['lean_memory_option_MiB']==8192 and row['self_wall_limit_s']==300
proc=Path('/proc')/str(row['pid'])/'stat'
if proc.exists():assert proc.read_text().split(') ')[1].split()[19]!=row['birth_ticks']
cap=json.loads((b/'capture-terminal.json').read_text());assert cap['exit_code']==0
mem=list(csv.DictReader((b/'memory.csv').open()));assert max(int(x['tree_rss_bytes'])for x in mem)==cap['sampled_tree_peak_bytes']==11688361984
events=[];partial=[]
for line in (b/'0000.log').read_text().splitlines():
 m=re.fullmatch(r'(.+?) took ([0-9.]+)(ms|s)',line)
 if m:events.append((m[1],float(m[2])/(1000 if m[3]=='ms' else 1)))
 elif line.strip():partial.append(line)
counts=dict(collections.Counter(k for k,v in events));assert counts=={'import':1,'type checking':491}
typed=[v for k,v in events if k=='type checking'];assert abs(sum(typed)-176.426)<1e-8
assert partial==['type checking']
published=list(csv.DictReader((r/'workloads/openai-math/grid-profile300/events.csv').open()))
assert len(published)==len(events) and all(x['label']==label and abs(float(x['reported_seconds'])-v)<1e-10 for x,(label,v)in zip(published,events))
data={'W_source':'d90d421','additional_native_calls':0,'module':row['module'],'raw_capture':str(b),'status':row['status'],'exit':row['returncode'],'native_retired':True,'native_wall_s':row['wall_s'],'native_user_CPU_s':row['user_cpu_s'],'native_system_CPU_s':row['system_cpu_s'],'native_peak_RSS_kib':row['peak_rss_kib'],'sampled_combined_tree_RSS_bytes':cap['sampled_tree_peak_bytes'],'capture_elapsed_s':cap['elapsed_s'],'completed_events':counts,'completed_type_checking_reported_sum_s':sum(typed),'unfinished_trailing_lines':partial,'minor_faults':row['minor_page_faults'],'major_faults':row['major_page_faults'],'voluntary_switches':row['voluntary_context_switches'],'involuntary_switches':row['involuntary_context_switches'],'same_unprofiled120s_denominator':False,'exclusive_phase_fraction':None,'root_elapsed_s':time.monotonic()-start,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'limits':['Profiler prints completed over-threshold events only; unfinished last work and unreported phases missing.','Cumulative/nested event times may overlap; sum cannot partition this300s ownwall.','Instrumented300s and earlier unprofiled120s are different censored points; no crossrun rescaling or borrowed1.13%overhead.','CPU,counters and requestedj1 do not isolate tactic,kernel,syscall or hardware cause.','Both interruptions preserve unknown unbounded compilation outcome and axiom closure.']}
(e/'reanalysis.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
