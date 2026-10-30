from pathlib import Path
import os,subprocess,json,csv,gzip,collections,time,resource,datetime,ast,re
r=Path('/workspaces/repository');os.chdir(r);os.sched_setaffinity(0,{0,1});start=time.monotonic()
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/'docs/tmp/build-and-evaluate'/('step-0203-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-paper-candidate-hook-step.txt').write_text(str(s)+'\n')
root=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30')
d=root/'candidate-recovery49-v2';qual=r/'research/mechanisms-2026-10-30/candidate-certificate-qualification'
def js(p):return json.loads(p.read_text())
def committed(path):return subprocess.check_output(['git','show','23f8ac1:research/mechanisms-2026-10-30/'+path],text=True)
def retired(rec):
 pid=rec['pid'];birth=rec['start_ticks']
 try: f=Path(f'/proc/{pid}/stat').read_text().rsplit(')',1)[1].split();assert f[19]!=str(birth),(pid,birth)
 except FileNotFoundError:pass
 return {'pid':pid,'birth':birth,'same_live_identity':False}
controls=[]
for name,code in [('candidate-certificate-build-v5',0),('candidate-certificate-positive-v5',0),('candidate-certificate-negative-v5',1),('candidate-certificate-negative-original-v5',1)]:
 q=qual/name;rec=js(q/'receipt.json');assert rec['exit']==code and rec['retired']
 text=(q/'source.lean').read_text()
 filename=Path(rec['source']).name
 assert text==committed(filename),(name,filename)
 controls.append({'label':name,'exit':code,'wall_s':rec['wall_s'],'retirement':retired(rec),'source_commit':'23f8ac1'})
clean=lambda x:re.sub(r"/workspaces/[^\n]*?\.lean","<source>","\n".join(l for l in x.splitlines()if not l.startswith("M_CERT_")))
new=(qual/'candidate-certificate-negative-v5/stdout.txt').read_text();old=(qual/'candidate-certificate-negative-original-v5/stdout.txt').read_text()
assert clean(new)==clean(old)
positive=(qual/'candidate-certificate-positive-v5/stdout.txt').read_text()
assert positive.splitlines()==['M_CERT_UNSUPPORTED digits','M_CERT_HIT digits','M_CERT_HIT grid']
assert 'M_CERT_FALLBACK digits'in new and 'M_CERT_FALLBACK grid'in new
term=js(d/'terminal.json');plan=js(d/'plan.json');rr=[json.loads(l)for l in(d/'results.jsonl').read_text().splitlines()]
assert term=={'completed':23,'planned':49,'group_wall_s':314.44709873665124,'complete':False}
assert len(rr)==23 and len({x['id']for x in rr})==23 and [x['id']for x in rr]==plan['ids'][:23]
assert 'pending synthetic goals'in(d/'STOP').read_text()
frozen=(d/'collector.py').read_text();assert frozen==committed('run_candidate_recovery.py')
tree=ast.parse(frozen);ns={'re':re}
for node in tree.body:
 if isinstance(node,ast.FunctionDef)and node.name in ['mask_comments','rewrite']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<frozen-pure-rewrite>','exec'),ns)
pair=r/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
inputs={x['id']:x for x in json.load(gzip.open(pair/'input7808.json.gz','rt'))['candidates']}
expected={x['id']:x for x in csv.DictReader((r/'research/mechanisms-2026-10-30/coverage/minif2f126.csv').open())if x['category']=='checked_family'}
assert set(expected)==set(plan['ids'])
derived=[];native_identities=[]
for x in rr:
 cap=Path(x['capture']);rec=js(cap/'receipt.json');stdout=(cap/'stdout.txt').read_text();stderr=(cap/'stderr.txt').read_text()
 source,edits=ns['rewrite'](inputs[x['id']]['code'],x['family'])
 source+='\n#print axioms '+inputs[x['id']]['task_id']+'\n'
 assert (d/(x['id']+'.lean')).read_text()==source
 assert (cap/'source.lean').read_text()==source and x['edits']==edits
 assert rec['retired'] and rec['wall_s']==x['wall_s'];native_identities.append(retired(rec))
 assert x['hits']==stdout.count('M_CERT_HIT') and x['fallbacks']==stdout.count('M_CERT_FALLBACK')
 if x['status']=='accepted':
  assert rec['exit']==0 and not stderr and 'error:'not in stdout and 'sorryAx'not in stdout
  axioms=re.findall(r'depends on axioms: \[([^]]*)\]',stdout);assert len(axioms)==1
  assert set(z.strip()for z in axioms[0].split(','))<= {'propext','Quot.sound','Classical.choice'}
 if x['status']=='lean_error':assert rec['exit']==1 and 'error:'in stdout and 'sorryAx'in stdout
 derived.append({'id':x['id'],'transformed_status':x['status'],'hits':x['hits'],'fallbacks':x['fallbacks'],
 'has_sorryAx':'sorryAx'in stdout,'source_rewrite_matches_frozen_rule':True,
 'is_original_rejection_certified':False,'wall_s':x['wall_s']})
counts=dict(collections.Counter(x['status']for x in rr));assert counts=={'lean_error':7,'budget_exceeded':6,'accepted':10}
summary={'source_commit':'23f8ac1','terminal':term,'stop_reason':(d/'STOP').read_text(),
 'completed_controls':controls,'negative_diagnostics_equal_after_only_paths_markers':True,
 'partial_transformed_statuses':counts,'planned_but_not_returned':26,'partial_native_wall_s':sum(x['wall_s']for x in rr),
 'all_returned_sources_equal_frozen_transform':True,'all_recorded_native_retired':True,'native_identities':native_identities,
 'accepted_transformed_proofs_with_no_sorryAx':10,'full_49_recovery_rate':None,'original_native_rejection_equivalence':False,
 'root_elapsed_s':time.monotonic()-start,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'new_native_runs':0}
(e/'reanalysis.json').write_text(json.dumps(summary,indent=2)+'\n')
(e/'partial-terminal.json').write_text(json.dumps(term,indent=2)+'\n')
(e/'stop-reason.txt').write_text((d/'STOP').read_text())
with(e/'source-audit.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=list(derived[0]),lineterminator='\n');w.writeheader();w.writerows(derived)
print('STEP',s);print(json.dumps({k:v for k,v in summary.items()if k not in ['native_identities','completed_controls']},indent=2))
