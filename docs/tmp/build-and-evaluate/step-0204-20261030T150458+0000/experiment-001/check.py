from pathlib import Path
import os,json,csv,subprocess,collections,datetime,time,resource,re,ast
r=Path('/workspaces/repository');os.chdir(r);os.sched_setaffinity(0,{0,1});start=time.monotonic()
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S+0000');s=r/'docs/tmp/build-and-evaluate'/('step-0204-'+stamp);e=s/'experiment-001';e.mkdir(parents=True)
Path('/workspaces/.agent-state/gpu-smt-paper-label-control-step.txt').write_text(str(s)+'\n')
b=Path('/workspaces/.agent-state/gpu-smt-captures/workloads/epfl-label-controls')
rows=[json.loads(x)for x in(b/'results.jsonl').read_text().splitlines()]
variants=[json.loads(x)for x in(b/'variants.jsonl').read_text().splitlines()]
term=json.loads((b/'terminal.json').read_text());cap=json.loads((b/'capture-terminal.json').read_text());launch=json.loads((b/'launch.json').read_text())
assert term['rows']==term['planned_rows']==len(rows)==len(variants)==6
assert cap['exit_code']==0 and cap['sampling_interval_s']==1
try:
 f=Path(f"/proc/{launch['pid']}/stat").read_text().rsplit(')',1)[1].split();assert f[19]!=launch['birth']
except FileNotFoundError:pass
source0=(b/'0.lean').read_text()
# Reuse a frozen pure lexical routine without importing any native runner.
raw=subprocess.check_output(['git','show','23f8ac1:research/mechanisms-2026-10-30/run_candidate_recovery.py'],text=True)
ns={}
node=next(x for x in ast.parse(raw).body if isinstance(x,ast.FunctionDef)and x.name=='mask_comments')
exec(compile(ast.Module(body=[node],type_ignores=[]),'<pure-lexer>','exec'),ns)
for i,(v,x)in enumerate(zip(variants,rows)):
 assert x['index']==i and x['case_id']=='training-rg0-row19776' and x['publisher_valid']is False
 limit=v['heartbeat_limit']
 def cap_option(m):
  n=int(m[2].replace('_',''))
  return m[1]+str(limit)if limit!=0 and(n==0 or n>limit)else m[0]
 source=re.sub(r'(?m)^([ \t]*set_option[ \t]+maxHeartbeats[ \t]+)([0-9_]+)',cap_option,v['source'])
 assert (b/f'{i}.lean').read_text()==source
 assert x['threads']==2 and x['native_memory_option_MiB']==6144 and x['self_wall_limit_s']==20
 log=(b/f'{i}.log').read_text()
 if i==3:assert x['returncode']==1 and x['status']=='budget_exceeded' and 'maximum recursion depth has been reached'in log
 else:assert x['returncode']==0 and x['status']=='compile_ok' and 'error:'not in log and "declaration uses 'sorry'"not in log
 if i in [3,4,5]:assert source==source0
assert (b/'2.lean').read_text()==source0.replace('set_option maxHeartbeats 0','set_option maxHeartbeats 800000')
norm=lambda x:''.join(ns['mask_comments'](x).split())
assert norm((b/'1.lean').read_text())==norm(source0)
prelude=Path('/workspaces/.agent-state/gpu-smt-workloads/toolchains/lean-4.15.0-linux/src/lean/Init/Prelude.lean')
lines=prelude.read_text().splitlines();default=next((i+1,l)for i,l in enumerate(lines)if 'def defaultMaxRecDepth :='in l)
assert default[1].strip()=='def defaultMaxRecDepth := 512'
memory=list(csv.DictReader((b/'memory.csv').open()));peak=max(int(x['tree_rss_bytes'])for x in memory);assert peak==cap['sampled_tree_peak_bytes']
published=list(csv.DictReader((r/'workloads/candidates/epfl-label-reproducibility/native-controls.csv').open()))
for x,y in zip(rows,published):
 assert x['variant']==y['variant'] and x['status']==y['status'] and x['wall_s']==float(y['wall_s'])
summary={'source_commit':'34b3650','rows':6,'statuses':dict(collections.Counter(x['status']for x in rows)),
 'wall_sum_s':sum(x['wall_s']for x in rows),'min_wall_s':min(x['wall_s']for x in rows),'max_wall_s':max(x['wall_s']for x in rows),
 'capture_elapsed_s':cap['elapsed_s'],'sampled_combined_peak_bytes':peak,'memory_samples':len(memory),
 'controller_retired':True,'native_wait4_per_return':True,'native_individual_pid_birth_not_recorded':True,
 'default_recursion_depth':512,'default_source':str(prelude),'default_source_line':default[0],
 'annotated_and_original_code_equal_ignoring_comments_whitespace':True,'exact_original_producer_cause':None,
 'new_native_runs':0,'root_elapsed_s':time.monotonic()-start,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(e/'reanalysis.json').write_text(json.dumps(summary,indent=2)+'\n')
with(e/'controls.csv').open('w',newline='')as f:
 fields=['variant','heartbeat_limit','max_rec_depth_requested','annotation_comments_present','returncode','status','wall_s']
 w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
print('STEP',s);print(json.dumps(summary,indent=2))
