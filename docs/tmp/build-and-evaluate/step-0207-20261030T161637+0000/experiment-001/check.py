from pathlib import Path
import os,json,gzip,csv,subprocess,collections,re,ast,time,resource,datetime
r=Path('/workspaces/repository');os.chdir(r);os.sched_setaffinity(0,{0,1});start=time.monotonic()
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/'docs/tmp/build-and-evaluate'/('step-0207-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-paper-native64-repair-step.txt').write_text(str(s)+'\n')
m=r/'research/mechanisms-2026-10-30';base=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30')
def js(p):return json.loads(p.read_text())
def committed(f):return subprocess.check_output(['git','show','88edb9d:research/mechanisms-2026-10-30/'+f],text=True)
def retired(rec):
 try:
  z=Path(f"/proc/{rec['pid']}/stat").read_text().rsplit(')',1)[1].split();assert z[19]!=rec['start_ticks']
 except FileNotFoundError:pass
 return {'pid':rec['pid'],'birth':rec['start_ticks'],'same_live_identity':False}
ns={'re':re}
for file,names in [('run_candidate_recovery.py',{'mask_comments','rewrite'}),('candidate_certificate_auto.py',{'route','transform'}),('run_candidate_recovery_pair.py',{'finite'})]:
 for node in ast.parse(committed(file)).body:
  if isinstance(node,ast.FunctionDef)and node.name in names:exec(compile(ast.Module(body=[node],type_ignores=[]),'<frozen-pure-transform>','exec'),ns)
pair=r/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
inputs={x['id']:x for x in json.load(gzip.open(pair/'input7808.json.gz','rt'))['candidates']};assert len(inputs)==7808
families={'amc12a_2020_p4':'digits','mathd_numbertheory_541':'grid'}
frame={k:x for k,x in inputs.items()if x['task_id']in families};assert len(frame)==64
routes={k:ns['route'](x['code'])for k,x in inputs.items()}
assert collections.Counter(routes.values())=={None:7745,'digits':32,'grid':31}
assert all(k in frame for k,v in routes.items()if v is not None)
assert [k for k in frame if routes[k]is None]==['minif2f-7206']
archived=[]
with gzip.open(m/'automation/native64/results128.jsonl.gz','rt')as f:archived=[json.loads(l)for l in f]
rows=[];groups=[]
for tag,n,collector in [('candidate-recovery49-pair-v3',98,'run_candidate_recovery_pair.py'),('candidate-auto-extra15-pair-v1',30,'run_candidate_auto_extra.py')]:
 d=base/tag;t=js(d/'terminal.json');p=js(d/'plan.json');rr=[json.loads(l)for l in(d/'results.jsonl').read_text().splitlines()]
 assert t['complete'] and t['completed_units']==t['planned_units']==len(rr)==n and not t['stopped']
 assert (d/'collector.py').read_text()==committed(collector)
 assert p['self_wall_s']==16 and p['heartbeats']==200000 and p['jobs']==1 and p['native_memory_MiB']==8192 and p['cpus']=='8-11'
 expected=[]
 for i,k in enumerate(p['ids']):
  for mode in (['original','certificate']if i%2==0 else['certificate','original']):expected.append((k,mode))
 assert [(x['id'],x['mode'])for x in rr]==expected
 groups.append({'label':tag,'sources':n//2,'units':n,'group_wall_s':t['group_wall_s'],'complete':True});rows+=rr
assert rows==archived and len({(x['id'],x['mode'])for x in rows})==128
assert {x['id']for x in rows}==set(frame)
identities=[];accepted=[];axioms={};native_cpu_scope=set()
for x in rows:
 cap=Path(x['capture']);rec=js(cap/'receipt.json')
 assert rec['retired'] and rec['internal_wall_seconds']==16 and rec['native_jobs']==1 and rec['native_memory_MiB']==8192 and rec['signals_sent']==0
 assert rec['cpu_affinity']=='8,9,10,11'and rec['native_T_flag']==50000000
 assert rec['wall_s']==x['wall_s'] and rec['native_cpu_seconds']==x['cpu_s'] and rec['sampled_peak_owned_rss_bytes']==x['sampled_peak_owned_rss_bytes']
 identities.append(retired(rec));native_cpu_scope.add(rec['native_cpu_scope'])
 src=inputs[x['id']]['code']
 if x['mode']=='certificate':src,meta=ns['transform'](src)
 src=ns['finite'](src)+'\n#print axioms '+x['task']+'\n'
 assert (cap/'source.lean').read_text()==src,(x['id'],x['mode'])
 stdout=(cap/'stdout.txt').read_text();stderr=(cap/'stderr.txt').read_text()
 if x['status']=='accepted':
  assert x['mode']=='certificate'and rec['exit']==0 and 'error:'not in stdout+stderr and 'sorryAx'not in stdout+stderr
  assert "declaration uses 'sorry'"not in stdout+stderr
  matches=re.findall("'"+re.escape(x['task'])+r"' depends on axioms: \[([^]]*)\]",stdout);assert len(matches)==1
  ax={a.strip()for a in matches[0].split(',')if a.strip()};assert ax<={'propext','Quot.sound','Classical.choice'}
  axioms[x['id']]=sorted(ax);accepted.append(x['id'])
 elif x['status']=='lean_error':assert rec['exit']in[0,1]and 'error:'in stdout+stderr
 else:
  assert x['status']=='budget_exceeded'
  assert rec['exit']in[124,-14]or any(z in(stdout+stderr).lower()for z in ['maximum number of heartbeats','maximum recursion depth'])
assert len(accepted)==31
data={(x['id'],x['mode']):x for x in rows};flow=collections.Counter()
pairs=[]
for k in sorted(frame,key=lambda x:int(x.split('-')[-1])):
 a,b=data[k,'original'],data[k,'certificate'];flow[a['status']+' -> '+b['status']]+=1
 pairs.append({'id':k,'task':b['task'],'original':a['status'],'certificate':b['status'],'original_wall_s':a['wall_s'],'certificate_wall_s':b['wall_s'],
 'source_route':routes[k],'final_axioms':';'.join(axioms.get(k,[]))if b['status']=='accepted'else None})
assert flow=={'budget_exceeded -> accepted':31,'budget_exceeded -> lean_error':16,'budget_exceeded -> budget_exceeded':4,'lean_error -> lean_error':13}
costs={mode:{'statuses':dict(collections.Counter(x['status']for x in rows if x['mode']==mode)),
 'native_wall_s':sum(x['wall_s']for x in rows if x['mode']==mode),'native_cpu_s':sum(x['cpu_s']for x in rows if x['mode']==mode),
 'sampled_own_tree_peak_bytes':max(x['sampled_peak_owned_rss_bytes']for x in rows if x['mode']==mode)}for mode in ['original','certificate']}
published=js(m/'automation/native64/summary.json')
assert dict(flow)==published['flow']
assert all(costs[k]['native_wall_s']==published['mode_wall_sum_s'][k]for k in costs)
# Verify frozen compiled proof-module source and copied module, not a later working tree.
prep=[]
for label,source in [('candidate-certificate-proofs-v10','CertificateProofs.lean'),('candidate-certificate-build-v12','CertificateMethods.lean')]:
 cap=base/'captures'/label;rec=js(cap/'receipt.json')
 assert rec['exit']==0 and rec['retired']and(cap/'source.lean').read_text()==committed(source)
 retired(rec);prep.append({'label':label,'source':source,'wall_s':rec['wall_s'],'source_commit':'88edb9d','outside_candidate_phase':True})
 assert Path(rec['argv'][rec['argv'].index('-o')+1]).read_bytes()==(base/'generated/candidate-certificate-v12'/source.replace('.lean','.olean')).read_bytes()
controls=js(m/'automation/native64/controls.json')['records'];assert len(controls)==4
normalized=collections.defaultdict(dict);control_out=[]
for c in controls:
 cap=Path(c['capture']);rec=js(cap/'receipt.json');assert rec['retired']and rec['exit']==1;retired(rec)
 stdout=(cap/'stdout.txt').read_text();stderr=(cap/'stderr.txt').read_text();assert not stderr and 'error:'in stdout
 delta=c['line_map_added_import']
 def repl(match):return '<source>:'+str(int(match[1])-delta)+':'
 clean=re.sub(r'/workspaces/[^\n]*?\.lean:(\d+):',repl,stdout)
 normalized[c['control']][c['mode']]=clean
 control_out.append({'control':c['control'],'mode':c['mode'],'exit':rec['exit'],'retired':True,'added_import_lines':delta})
assert all(v['original']==v['certificate']for v in normalized.values())and len(normalized)==2
historic=json.load(gzip.open(pair/'engine.stdout.gz','rt'))['results']
historic_tasks={inputs[x['id']]['task_id']for x in historic if x['outcome']['status']=='accepted'}
assert len(historic_tasks)==142 and set(families).isdisjoint(historic_tasks)
out={'source_commits':['562a80e','88edb9d'],'groups':groups,'sources':64,'native_units':128,'route_counts':{'none':7745,'digits':32,'grid':31},
 'detected_headers_in_full_catalog':63,'malformed_unsupported':'minif2f-7206','flow':dict(flow),'costs':costs,
 'accepted_ids':accepted,'accepted_axioms':axioms,'verified_tasks':sorted(families),'historical_tasks':142,
 'new_task_goals_absent_historical_acceptance':True,'ordinary_error_to_accept':0,'controls':control_out,'negative_source_mapped_stdout_equal':True,
 'module_setup':prep,'all128_native_identities_retired':True,'native_cpu_scope':sorted(native_cpu_scope),
 'same_source_acceptance_parity':False,'full7808_service_speedup':None,'source_mode':'opt-in specialized proof repair, not original-proof result preservation',
 'new_native_runs':0,'root_elapsed_s':time.monotonic()-start,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'reanalysis.json').write_text(json.dumps(out,indent=2)+'\n')
with(e/'paired64.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(pairs[0]),lineterminator='\n');w.writeheader();w.writerows(pairs)
(e/'controls.json').write_text(json.dumps(control_out,indent=2)+'\n')
print('STEP',s);print(json.dumps({k:v for k,v in out.items()if k not in ['accepted_ids','accepted_axioms']},indent=2))
