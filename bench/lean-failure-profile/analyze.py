"""Rank actual native runtime-boundary timings; retain open timeout frames."""
from pathlib import Path
import argparse,collections,csv,gzip,json,zlib
def rawrows(p):
 p=p if p.exists()else p.with_name(p.name+'.gz')
 with(gzip.open(p,'rt')if p.suffix=='.gz'else p.open())as f:
  for line in f:
   if line.strip():yield json.loads(line)
def snapshots(path):
 # SIGTERM/SIGKILL does not run gzip finalizers. Z_SYNC_FLUSH records survive;
 # missing trailer is recorded explicitly, never called a complete gzip stream.
 d=zlib.decompressobj(31);pending=b''
 with path.open('rb')as stream:
  while block:=stream.read(65536):
   pending+=d.decompress(block)
   while b'\n'in pending:
    line,pending=pending.split(b'\n',1)
    if line:yield json.loads(line)
 yield dict(_stream_closed=d.eof,_trailing_partial_bytes=len(pending))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args();a.out.mkdir(exist_ok=False)
 selected=json.loads((a.run/'selected.json').read_text());wanted=set(selected['ids'])
 terminal=json.loads((a.run/'profile/terminal.json').read_text())
 if terminal['state']!='complete'or terminal['returned']!=len(wanted):raise RuntimeError('Preserve partial run; not final hotspot distribution')
 cells={'profile':{x['proof_id']:x for x in rawrows(a.run/'profile/results.jsonl')}}
 if(a.run/'native/terminal.json').exists():cells['native']={x['proof_id']:x for x in rawrows(a.run/'native/results.jsonl')}
 latest={};streams=[];unknown=collections.Counter();events=0
 for file in sorted((a.run/'profiles').glob('*.jsonl.gz')):
  first=last=None;count=0;meta={}
  for q in snapshots(file):
   if '_stream_closed'in q:meta=q;continue
   events+=1;count+=1;first=first or q['time_ns'];last=q['time_ns']
   for t in q['threads']:
    sid=t['source_id'];phase=t['phase']
    if sid not in wanted:unknown[(sid,phase)]+=1;continue
    latest[(q['pid'],t['tid'],sid,phase)]=(q['time_ns'],t)
  streams.append(dict(path=str(file),records=count,first_ns=first,last_ns=last,**meta))
 by_source=collections.defaultdict(lambda:collections.defaultdict(lambda:dict(calls=0,wall_ns=0,inclusive_cpu_ns=0,exclusive_cpu_ns=0,open_frames=0)))
 open_frames=[]
 for(pid,tid,sid,phase),(time_ns,t)in latest.items():
  for key,v in t['totals'].items():
   b=by_source[sid][key];b['calls']+=v[0];b['wall_ns']+=v[1];b['inclusive_cpu_ns']+=v[2];b['exclusive_cpu_ns']+=v[3]
  cpu=t['thread_cpu_ns'];stack=t['active']
  for i,f in enumerate(stack):
   inclusive=max(0,cpu-f['start_cpu_ns']);active_child=max(0,cpu-stack[i+1]['start_cpu_ns'])if i+1<len(stack)else 0
   exclusive=max(0,inclusive-f['completed_child_cpu_ns']-active_child)
   b=by_source[sid][f['key']];b['wall_ns']+=max(0,time_ns-f['start_ns'])
   b['inclusive_cpu_ns']+=inclusive;b['exclusive_cpu_ns']+=exclusive;b['open_frames']+=1
   open_frames.append(dict(source_id=sid,pid=pid,tid=tid,phase=phase,key=f['key'],snapshot_ns=time_ns,observed_open_wall_ns=max(0,time_ns-f['start_ns']),observed_open_exclusive_cpu_ns=exclusive))
 totals=collections.defaultdict(lambda:dict(calls=0,wall_ns=0,inclusive_cpu_ns=0,exclusive_cpu_ns=0,open_frames=0,sources=0))
 per_source=[]
 for sid in selected['ids']:
  components=by_source[sid]
  for key,values in components.items():
   x=totals[key];x['sources']+=1
   for k,v in values.items():x[k]+=v
  ranked=sorted(components.items(),key=lambda x:-x[1]['exclusive_cpu_ns'])
  per_source.append(dict(source_id=sid,baseline_status=selected['baseline_statuses'][sid],profile_status=cells['profile'][sid]['status'],baseline_HTTP_seconds=selected['baseline_HTTP_seconds'][sid],profile_body_seconds=cells['profile'][sid]['result'].get('time'),measured_exclusive_cpu_seconds=sum(x['exclusive_cpu_ns']for x in components.values())/1e9,top_native_boundary=ranked[0][0]if ranked else None,components=components))
 ranked=[dict(key=k,**v)for k,v in sorted(totals.items(),key=lambda x:-x[1]['exclusive_cpu_ns'])]
 result=dict(source_count=len(wanted),sources_with_native_boundary_data=len(by_source),profile_status_counts=dict(collections.Counter(x['status']for x in cells['profile'].values())),status_changes_from_original=[dict(source_id=i,baseline=selected['baseline_statuses'][i],profile=cells['profile'][i]['status'])for i in selected['ids']if selected['baseline_statuses'][i]!=cells['profile'][i]['status']],ranked=ranked,open_frames=open_frames,profile_streams=streams,unknown_source_snapshot_counts=[dict(source_id=k[0],phase=k[1],records=v)for k,v in unknown.items()],events=events,scope='Actual stock profileit/profileitM boundaries, child-subtracted thread CPU plus final observed open frames. Inclusive spans overlap. This diagnostic is not a speedup, exhaustive source/CPU attribution, or removable critical-path fraction.')
 if 'native'in cells:
  result['fresh_native_profile_status_changes']=[dict(source_id=i,native=cells['native'][i]['status'],profile=cells['profile'][i]['status'])for i in selected['ids']if cells['native'][i]['status']!=cells['profile'][i]['status']]
  nt=json.loads((a.run/'native/terminal.json').read_text());result['fresh_native_seconds']=nt['whole_lifecycle_seconds'];result['profile_seconds']=terminal['whole_lifecycle_seconds']
  result['extra_elapsed_percent']=(terminal['whole_lifecycle_seconds']/nt['whole_lifecycle_seconds']-1)*100
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 (a.out/'per-source.json').write_text(json.dumps(per_source,indent=2)+'\n')
 with(a.out/'ranked.csv').open('w',newline='')as f:
  if ranked:
   w=csv.DictWriter(f,fieldnames=list(ranked[0]),lineterminator='\n');w.writeheader();w.writerows(ranked)
 print(json.dumps({k:v for k,v in result.items()if k not in ['ranked','open_frames','profile_streams']},indent=2))
 print(json.dumps(ranked[:15],indent=2))
if __name__=='__main__':main()
