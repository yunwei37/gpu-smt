from pathlib import Path
import os,json,csv,collections,subprocess,time,resource,datetime,re
r=Path('/workspaces/repository');os.chdir(r);os.sched_setaffinity(0,{0,1});start=time.monotonic()
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/'docs/tmp/build-and-evaluate'/('step-0205-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-paper-expanded-metadata-step.txt').write_text(str(s)+'\n')
base=Path('/workspaces/.agent-state/gpu-smt-captures/workloads')
def js(p):return json.loads(p.read_text())
def ledger(p):return [json.loads(x)for x in p.read_text().splitlines()if x]
def retired(pid,birth):
 try:
  z=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split()
  assert z[19]!=str(birth),(pid,birth,z[0])
 except FileNotFoundError:pass
 return {'pid':pid,'birth':str(birth),'same_live_identity':False}
points={};all_native=[]
for name in ['openai4341-strata-batch4','openai4341-authored-recovery']:
 d=base/name;rr=ledger(d/'results.jsonl');t=js(d/'terminal.json');c=js(d/'capture-terminal.json');la=js(d/'launch.json')
 assert c['exit_code']==0 and t['rows']==len(rr)and len({x['module']for x in rr})==len(rr)
 identity=retired(la['controller_pid'],la['birth_ticks'])
 calls=[x for x in rr if 'wall_s'in x];native=[]
 for x in rr:
  if x['status']=='dependency_not_compiled':assert 'returncode'not in x and 'wall_s'not in x;continue
  native.append(retired(x['pid'],x['birth_ticks']))
  log=Path(x['log']).read_text()
  assert x['replaced_source_budget_settings']==0 and x['threads']==8 and x['lean_memory_option_MiB']==8192 and x['affinity']==list(range(8))
  if x['status']=='compile_ok':assert x['returncode']==0 and not x['sorry_warning']and "declaration uses 'sorry'"not in log
  elif x['status']=='wall_budget_exceeded':assert x['returncode']==-14
  elif x['status']=='budget_exceeded':assert x['returncode']==1 and 'maximum number of heartbeats (100000)'in log
  else:raise AssertionError(x)
 mem=list(csv.DictReader((d/'memory.csv').open()));peak=max(int(x['tree_rss_bytes'])for x in mem);assert peak==c['sampled_tree_peak_bytes']
 counts=dict(collections.Counter(x['status']for x in rr))
 assert counts==t['statuses']
 points[name]={'rows':len(rr),'actual_native_calls':len(calls),'statuses':counts,'closure':t['closure_modules'],
 'planned_fresh':t['planned_fresh_modules'],'dependency_uninvoked':counts.get('dependency_not_compiled',0),
 'not_started':t['planned_fresh_modules']-len(rr),'total_uninvoked':t['planned_fresh_modules']-len(calls),
 'native_wall_s':sum(x['wall_s']for x in calls),'native_user_s':sum(x['user_cpu_s']for x in calls),
 'native_system_s':sum(x['system_cpu_s']for x in calls),'internal_group_s':t['elapsed_s'],'capture_s':c['elapsed_s'],
 'combined_sample_peak_bytes':peak,'controller':identity,'native_identities':native}
 all_native+=calls
after=ledger(base/'openai4341-strata-batch4/results.jsonl');recovery=ledger(base/'openai4341-authored-recovery/results.jsonl')
assert len(after)==326 and sum('wall_s'in x for x in after)==109
assert points['openai4341-strata-batch4']['not_started']==2767
pairs=[]
for x in recovery:
 y=next(z for z in after if z['module']==x['module']);assert y['status']=='budget_exceeded'and x['status']=='compile_ok'
 a=base/'openai4341-strata-batch4/source-replay'/x['path'];b=base/'openai4341-authored-recovery/source-replay'/x['path']
 original=Path('/workspaces/.agent-state/gpu-smt-workloads/openai-math-4eaee875')/x['path']
 assert a.read_bytes()==b.read_bytes()==original.read_bytes()
 pairs.append({'module':x['module'],'old_100k_status':y['status'],'old_100k_wall_s':y['wall_s'],'authored_status':x['status'],
 'authored_wall_s':x['wall_s'],'same_original_source_bytes':True})
last=after[-1];assert last['status']=='wall_budget_exceeded'and 7<last['wall_s']<9 and last['self_wall_limit_s']==300
tags=['openai4341-native','openai4341-native-expanded','openai4341-native-resume100k','openai4341-native-batch3','openai4341-grid-j8-1200','openai4341-native-after-grid','openai4341-amplitudes-j8-1200','openai4341-strata-batch4']
objectset={x['module']for tag in tags for x in ledger(base/tag/'results.jsonl')if x['status']=='compile_ok'}
assert len(objectset)==363
before_reader=set(objectset);objectset|={x['module']for x in recovery if x['status']=='compile_ok'};assert len(objectset)==365
obj=Path('/workspaces/.agent-state/gpu-smt-workloads/openai4341-oleans')
assert all((obj/Path(*m.split('.')).with_suffix('.olean')).exists()for m in objectset)
frame=list(csv.DictReader((r/'workloads/openai-math/build-planning-4eaee875/sample-targets.csv').open()));assert len(frame)==53
available=[x['module']for x in frame if x['module']in objectset]
d=base/'openai4341-olean-types-363';inputs=[x.split('\t')for x in(d/'inputs.tsv').read_text().splitlines()]
assert {x[0]for x in inputs}==before_reader and len(inputs)==363
for module,p in inputs:assert Path(p)==obj/Path(*module.split('.')).with_suffix('.olean') and Path(p).exists()
rt=js(d/'terminal.json');rc=js(d/'capture-terminal.json');rl=js(d/'launch.json')
assert rt['returncode']==rc['exit_code']==0 and rt['wall_s']<30
reader_identity=retired(rl['pid'],rl['birth'])
theorems=0;aux=0;modules=[];expr=set();groups=collections.defaultdict(list);decide=collections.defaultdict(list)
tail=None
with(d/'native.log').open()as f:
 for line in f:
  if line.startswith('MODULE '):modules.append(line.strip()[7:])
  elif line.startswith('AUDIT '):
   x=json.loads(line[6:]);theorems+=1;assert x['module']==modules[-1]and x['axioms']is None
   if x['auxiliary_name']:
    aux+=1;expr.add(x['expr_group']);groups[x['type_group']].append(x)
   if x['decide_shaped_auxiliary']:assert x['auxiliary_name']and x['proof_value_head']=='of_decide_eq_true';decide[x['type_group']].append(x)
  elif line.startswith('DONE '):tail=line.strip()
assert tail=='DONE 363 363'and len(modules)==363 and set(modules)==before_reader
assert theorems==89268 and aux==47989 and len(expr)==44528 and len(groups)==44532
n_dec=sum(len(v)for v in decide.values());assert n_dec==45661 and len(decide)==42610
assert len({x['name']for v in decide.values()for x in v})==n_dec
cross=[(k,v)for k,v in decide.items()if len({x['module']for x in v})>1];assert len(cross)==919
mem=list(csv.DictReader((d/'memory.csv').open()));assert max(int(x['tree_rss_bytes'])for x in mem)==rc['sampled_tree_peak_bytes']
md={'modules':len(modules),'theorems':theorems,'auxiliary_names':aux,'native_Expr_keys':len(expr),'level_private_groups':len(groups),
 'auxiliary_cross_module_groups':sum(len({x['module']for x in v})>1 for v in groups.values()),
 'decide_shaped_auxiliaries':n_dec,'decide_type_groups':len(decide),'decide_duplicate_entries':n_dec-len(decide),
 'decide_repeated_groups':sum(len(v)>1 for v in decide.values()),'decide_cross_module_groups':len(cross),
 'decide_distinct_module_key_pairs':len({(x['module'],k)for k,v in decide.items()for x in v}),
 'decide_global_distinct_declaration_names':len({x['name']for v in decide.values()for x in v}),
 'within_module_extra_declarations':n_dec-len({(x['module'],k)for k,v in decide.items()for x in v}),
 'cross_module_extra_module_key_pairs':len({(x['module'],k)for k,v in decide.items()for x in v})-len(decide),
 'decide_modules':len({x['module']for v in decide.values()for x in v}),
 'native_wall_s':rt['wall_s'],'capture_s':rc['elapsed_s'],'combined_sample_peak_bytes':rc['sampled_tree_peak_bytes'],
 'native_peak_rss_kib':rt['peak_rss_kib'],'controller':reader_identity,'imported_axioms_audited':False,'actual_kernel_cache_misses_measured':False}
with(e/'decision-type-groups.csv').open('w',newline='')as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['native_type_group','declarations','distinct_modules','example_declaration'])
 for k,v in sorted(decide.items()):
  if len(v)>1:w.writerow([k,len(v),len({x['module']for x in v}),v[0]['name']])
(e/'executed-type-reader.lean').write_bytes((d/'OleanTypes.lean').read_bytes())
summary={'source':'completed source-native W captures; no new native launch by root','points':points,
 'authored_pairs':pairs,'last_residual_wall_call':last,'compiled_object_union_before_authored':363,
 'compiled_object_union_after_authored':365,'original_frame_endpoints_available':len(available),'available_endpoints':available,'metadata':md,
 'root_elapsed_s':time.monotonic()-start,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'new_native_runs':0}
(e/'reanalysis.json').write_text(json.dumps(summary,indent=2)+'\n')
for name in ['openai4341-strata-batch4','openai4341-authored-recovery','openai4341-olean-types-363']:
 (e/(name+'-terminal.json')).write_bytes((base/name/'terminal.json').read_bytes())
print('STEP',s);print(json.dumps({k:v for k,v in summary.items()if k not in ['points','last_residual_wall_call']},indent=2))
print('POINTS',json.dumps({k:{a:b for a,b in v.items()if a!='native_identities'}for k,v in points.items()},indent=2))
