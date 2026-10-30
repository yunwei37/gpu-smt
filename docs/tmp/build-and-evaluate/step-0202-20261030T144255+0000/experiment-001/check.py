from pathlib import Path
import os,json,csv,subprocess,collections,time,resource,datetime
r=Path('/workspaces/repository');os.chdir(r);os.sched_setaffinity(0,{0,1});start=time.monotonic()
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000')
s=r/'docs/tmp/build-and-evaluate'/('step-0202-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-paper-workload-continuation-step.txt').write_text(str(s)+'\n')
base=Path('/workspaces/.agent-state/gpu-smt-captures/workloads')
def js(p):return json.loads(p.read_text())
def rows(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def identity(pid,birth):
 try:
  f=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
  return {'pid':pid,'expected_birth':str(birth),'current_birth':f[19],'same_live_identity':f[19]==str(birth),'state':f[0]}
 except FileNotFoundError:return {'pid':pid,'expected_birth':str(birth),'same_live_identity':False,'state':'absent'}
points={}
for name,count in [('openai4341-native-after-grid',24),('openai4341-amplitudes-j8-1200',1),('epfl-training12-native',12)]:
 d=base/name; rr=rows(d/'results.jsonl');assert len(rr)==count
 term=js(d/'terminal.json');cap=js(d/'capture-terminal.json');launch=js(d/'launch.json')
 assert cap['exit_code']==0
 ident=identity(launch['controller_pid'],launch['birth_ticks']);assert not ident['same_live_identity']
 mem=list(csv.DictReader((d/'memory.csv').open()))
 peak=max(int(x['tree_rss_bytes']) for x in mem);assert peak==cap['sampled_tree_peak_bytes']
 native=[x for x in rr if 'wall_s'in x]
 retired=[]
 for x in native:
  log=Path(x['log']).read_text(errors='replace')
  if x['status']=='compile_ok':assert x['returncode']==0 and "declaration uses 'sorry'"not in log
  if x['status']=='wall_budget_exceeded':assert x['returncode']==-14
  if x['status']=='budget_exceeded':
   assert 'maximum number of heartbeats'in log.lower() or 'deterministic timeout'in log.lower()
  if 'pid'in x:
   v=identity(x['pid'],x['birth_ticks']);assert not v['same_live_identity'];retired.append(v)
 points[name]={'rows':len(rr),'native_invocations':len(native),'statuses':dict(collections.Counter(x['status']for x in rr)),
 'native_wall_s':sum(x['wall_s']for x in native),'user_cpu_s':sum(x['user_cpu_s']for x in native),
 'system_cpu_s':sum(x['system_cpu_s']for x in native),'capture_elapsed_s':cap['elapsed_s'],'sampled_combined_peak_bytes':peak,
 'controller_identity':ident,'native_identities':retired,'memory_samples':len(mem),'terminal':term}
 if name=='epfl-training12-native': training=rr
 if name=='openai4341-native-after-grid': after=rr
 if name=='openai4341-amplitudes-j8-1200': amplitude=rr[0]
assert points['openai4341-native-after-grid']['statuses']=={'compile_ok':12,'wall_budget_exceeded':2,'dependency_not_compiled':10}
assert all(x['replaced_source_budget_settings']==0 for x in after if 'wall_s'in x)
assert amplitude['replaced_source_budget_settings']==0
amplitude_old=next(x for x in after if x['module']==amplitude['module'])
# Replay directory layout is discovered, never infer source equality from the CSV alone.
def source_file(d,mod):
 files=list((d/'source-replay').rglob(mod.rsplit('.',1)[-1]+'.lean'))
 assert len(files)==1,(str(d),files)
 return files[0]
a=source_file(base/'openai4341-native-after-grid',amplitude['module'])
b=source_file(base/'openai4341-amplitudes-j8-1200',amplitude['module'])
assert a.read_bytes()==b.read_bytes() and len(b.read_bytes())==2690420
for k in ['heartbeat_budget','lean_memory_option_MiB','threads','profiled','affinity']:assert amplitude[k]==amplitude_old[k]
objectpath=Path('/workspaces/.agent-state/gpu-smt-workloads/openai4341-oleans')/Path(*amplitude['module'].split('.')).with_suffix('.olean')
assert objectpath.exists()
assert sum(1 for x in after if 'wall_s'in x)==14
late=after[-1];assert late['status']=='wall_budget_exceeded' and 40<late['wall_s']<43 and late['self_wall_limit_s']==120
selection=js(base/'epfl-training12-native/selection.json')
assert len(training)==12 and collections.Counter(x['stratum']for x in training)=={'valid':4,'invalid_other':4,'invalid_budget_text':4}
assert all(x['source_budget_values_capped']==[0] and x['heartbeats']==10000 and x['threads']==2 for x in training)
cross=collections.Counter((x['publisher_valid'],x['status'])for x in training)
budget=sum(x['wall_s']for x in training if x['status']=='budget_exceeded')
assert cross=={(False,'budget_exceeded'):4,(False,'lean_error'):3,(False,'compile_ok'):1,(True,'budget_exceeded'):2,(True,'compile_ok'):2}
publisher=js(Path('/workspaces/.agent-state/gpu-smt-paper-recovery-20261030/epfl-training-publisher-audit.json'))['summaries']
counts=list(csv.DictReader((r/'workloads/candidates/epfl-training-provenance/publisher-counts.csv').open()))
for x in counts:
 assert publisher[x['publisher_stage']][x['publisher_metric']]==int(x['value']),(x,publisher[x['publisher_stage']])
assert 3586218+250000+142698-8457+391120+363420+111381==4836380
assert 2168417+2667963==4836380
result={'source_commits':{'training_construction':'7509dcc','native_after_grid':'a2b8c1a','training12':'b48e552','amplitudes':'48ffec4'},
'points':points,'training_selection':selection,
'training_cross':[{'publisher_valid':k[0],'native_status':k[1],'rows':v}for k,v in sorted(cross.items())],
'training_budget_wall_s':budget,'training_budget_fraction':budget/points['epfl-training12-native']['native_wall_s'],
'publisher_counts_verified':len(counts),'publisher_final_rows':4836380,'publisher_audit_bytes':9365,
'amplitudes_source_bytes_equal':True,'amplitudes_object_bytes':objectpath.stat().st_size,
'root_elapsed_s':time.monotonic()-start,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
'new_native_runs':0}
(e/'reanalysis.json').write_text(json.dumps(result,indent=2)+'\n')
(e/'native-points.csv').write_text('point,returned_rows,native_invocations,native_wall_s,capture_s,sampled_combined_peak_bytes\n'+''.join(f"{k},{v['rows']},{v['native_invocations']},{v['native_wall_s']},{v['capture_elapsed_s']},{v['sampled_combined_peak_bytes']}\n"for k,v in points.items()))
print('STEP',s)
print(json.dumps({k:v for k,v in result.items()if k not in ['points','training_selection']},indent=2))
print('POINTS',json.dumps({k:{a:b for a,b in v.items()if a not in ['native_identities','terminal']}for k,v in points.items()},indent=2))
