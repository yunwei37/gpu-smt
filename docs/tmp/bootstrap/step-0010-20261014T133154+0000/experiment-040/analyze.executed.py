from pathlib import Path
import collections,csv,json,statistics
r=Path('/workspaces/repository');s=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000';e=s/'experiment-040'
ref=list(csv.DictReader((s/'experiment-036/native-support-v3-official-init.csv').open()))
assert len(ref)==59626
sets={}
for tag,path in [('on',e/'reclaim-on-official-init.csv'),('off',e/'reclaim-off-official-init.csv'),('oldcanonical',s/'experiment-037/canonical-fused-official-init.csv')]:
 rows=list(csv.DictReader(path.open()));assert len(rows)==len(ref)
 assert all(a['declaration_index']==b['declaration_index'] and a['kind']==b['kind'] for a,b in zip(ref,rows))
 assert [int(x['declaration_index']) for x in rows]==list(range(59626))
 bodies=[(a,b) for a,b in zip(ref,rows) if a['kind']!='native-only']
 reasons=collections.defaultdict(lambda:{'count':0,'reference_cpu_ns':0})
 pos=set();total=sum(int(a['native_body_thread_cpu_ns']) for a,b in bodies)
 for a,b in bodies:
  q=reasons[b['host_reason']];q['count']+=1;q['reference_cpu_ns']+=int(a['native_body_thread_cpu_ns'])
  if b['host_positive']=='1': assert b['host_reason']=='0';pos.add(int(b['declaration_index']))
 data={'rows':len(rows),'bodies':len(bodies),'positives':len(pos),'reference_total_cpu_ns':total,'reference_positive_cpu_ns':reasons['0']['reference_cpu_ns'],'reference_positive_fraction':reasons['0']['reference_cpu_ns']/total,'reasons':dict(reasons),'max_steps':max(int(b['host_steps']) for a,b in bodies)}
 data['heaps']={k:{'max':max(int(b[k]) for a,b in bodies),'median':statistics.median(int(b[k]) for a,b in bodies)} for k in ['host_terms','host_frames','host_envs','host_levels']}
 sets[tag]=(rows,pos,data)
out={'scope':'E040 complete Init host setup. Fixed E036 body-thread CPU is descriptive cross-build weighting, never removable wall/GPU bound. All native bodies still run. One sequential observation per condition.','conditions':{k:v[2] for k,v in sets.items()}}
out['transitions']={}
for a,b in [('off','on'),('oldcanonical','on'),('oldcanonical','off')]:
 lost=sets[a][1]-sets[b][1];gained=sets[b][1]-sets[a][1]
 out['transitions'][a+'->'+b]={'gained_count':len(gained),'lost_count':len(lost),'gained_reference_cpu_ns':sum(int(ref[i]['native_body_thread_cpu_ns']) for i in gained),'lost_reference_cpu_ns':sum(int(ref[i]['native_body_thread_cpu_ns']) for i in lost),'lost_indices':sorted(lost),'reason_pairs':dict(collections.Counter(x['host_reason']+'->'+y['host_reason'] for x,y in zip(sets[a][0],sets[b][0]) if x['kind']!='native-only'))}
(e/'whole-analysis.json').write_text(json.dumps(out,indent=2)+'\n')


# Complete non-timing identity check of the disabled collection control.
old=sets['oldcanonical'][0];off=sets['off'][0]
nonclock=[k for k in old[0] if k!='native_body_thread_cpu_ns']
assert all(all(a[k]==b[k] for k in nonclock) for a,b in zip(old,off))
out['disabled_vs_previous_nonclock_columns_equal']=True
out['terminals']={}
for tag in ['on','off']:
 terminal=json.loads((e/f'reclaim-{tag}-official-init.terminal.json').read_text())
 stdout=(e/f'reclaim-{tag}-official-init.stdout').read_text()
 assert terminal['exit']==0 and terminal['input_bytes']==347555345
 assert stdout.strip()=='Checked 59626 declarations with no errors'
 resource={}
 for line in (e/f'reclaim-{tag}-official-init.resources.txt').read_text().splitlines():
  if ': ' in line:
   k,v=line.strip().split(': ',1);resource[k]=v
 out['terminals'][tag]={'whole_seconds':terminal['whole_seconds'],'native_stdout':stdout.strip(),'resources':resource}
out['observed_whole_on_over_off']=out['terminals']['on']['whole_seconds']/out['terminals']['off']['whole_seconds']
(e/'whole-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print('Completed terminal and disabled-control identity checks; no independent audit implied.')
