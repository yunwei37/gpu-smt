from pathlib import Path
import os,json,csv,subprocess,re,collections,time,resource,datetime
r=Path('/workspaces/repository');os.chdir(r);os.sched_setaffinity(0,{0,1});start=time.monotonic()
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/'docs/tmp/build-and-evaluate'/('step-0206-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-paper-type-cost-exposure-step.txt').write_text(str(s)+'\n')
base=Path('/workspaces/.agent-state/gpu-smt-captures/workloads');types=base/'openai4341-olean-types-363'
groups=collections.defaultdict(list);typed_modules=set();done=False
for l in(types/'native.log').open():
 if l.startswith('MODULE '):typed_modules.add(l.strip()[7:])
 elif l.startswith('AUDIT '):
  x=json.loads(l[6:])
  if x['decide_shaped_auxiliary']:groups[x['type_group']].append(x)
 elif l.startswith('DONE '):assert l.strip()=='DONE 363 363';done=True
assert done and len(typed_modules)==363
cross={k:v for k,v in groups.items()if len({x['module']for x in v})>1};assert len(cross)==919
module_keys=collections.defaultdict(set);module_decl=collections.Counter()
for k,v in cross.items():
 for x in v:module_keys[x['module']].add(k);module_decl[x['module']]+=1
d=base/'openai4341-strata-batch4'
rr=[json.loads(x)for x in(d/'results.jsonl').read_text().splitlines()]
term=json.loads((d/'terminal.json').read_text());assert term['rows']==len(rr)==326
calls=[x for x in rr if 'wall_s'in x];assert len(calls)==109 and len({x['module']for x in calls})==109
rows=[];classes=collections.defaultdict(list)
for x in calls:
 known=x['module']in typed_modules
 if x['status']=='compile_ok':
  assert known and x['returncode']==0
  cls='successful_module_with_observed_cross_module_type'if x['module']in module_keys else'successful_module_without_observed_cross_module_type'
 else:
  assert x['status']in ['budget_exceeded','wall_budget_exceeded']and not known
  cls='interrupted_module_without_completed_metadata'
 row={'module':x['module'],'native_status':x['status'],'class':cls,'native_wall_s':x['wall_s'],'metadata_present':known,
 'observed_cross_module_type_groups':len(module_keys.get(x['module'],set()))if known else None,
 'observed_cross_module_type_declarations':module_decl[x['module']]if known else None}
 rows.append(row);classes[cls].append(row)
T=sum(x['native_wall_s']for x in rows);expected={'successful_module_with_observed_cross_module_type':48,
 'successful_module_without_observed_cross_module_type':58,'interrupted_module_without_completed_metadata':3}
assert {k:len(v)for k,v in classes.items()}==expected
assert len(module_keys)==52
stats=[{'class':k,'native_calls':len(v),'native_wall_s':sum(x['native_wall_s']for x in v),
 'fraction_of_this_point_native_wall':sum(x['native_wall_s']for x in v)/T}for k,v in classes.items()]
A=next(x['native_wall_s']for x in stats if x['class']=='successful_module_with_observed_cross_module_type')
assert abs(T-1399.655780898407)<1e-8 and abs(A-454.2070825146511)<1e-8
profile=base/'openai4341-grid-profile300/0000.log'
lines=profile.read_text().splitlines()
events=[x for x in lines if x.startswith('type checking took ')]
assert len(events)==491 and all(re.fullmatch(r'type checking took [0-9.]+(?:ms|s)',x)for x in events)
assert lines[-1]=='type checking'
# Raw unlabelled phase timers have no declaration identity to join to these keys.
profile_scope={'completed_type_check_events':len(events),'events_with_declaration_identity':0,
 'unfinished_trailing_event':True,'same_point_as_109call_group':False,
 'type_group_checking_cost_identified':False}
result={'point':'openai4341-strata-batch4 only','native_calls':109,'total_native_wall_s':T,'classes':stats,
 'raw_metadata_read':'openai4341-olean-types-363','observed_cross_module_type_groups':919,'global_affected_modules':len(module_keys),
 'profile_scope':profile_scope,'observed_exposure_is_duplicate_check_cpu':False,
 'actual_cache_hit_rate':None,'measured_time_saved':None,'service_speedup':None,
 'uninvoked_modules_in_planned_fresh_closure':2984,
 'limits':['Whole-module wall is exposure,not repeated proof checking time;includes imports/elaboration/other proofs.',
 '3interrupted calls have unknown typed contents,not zero repeated work.',
 'Typed equality and physical earlier objects do not establish producer-state or cache eligibility.',
 '109completed calls form a bounded prefix;2984uninvoked modules retain unknown cost.',
 'No all-corpus/warm-service/GPU Amdahl bound,no point denominators combined.'],
 'new_native_runs':0,'root_elapsed_s':time.monotonic()-start,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'reanalysis.json').write_text(json.dumps(result,indent=2)+'\n')
for name,data in [('module-exposure.csv',rows),('class-costs.csv',stats)]:
 with(e/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
print('STEP',s);print(json.dumps(result,indent=2))
