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
 native_dir=a.run/'native'
 if(a.run/'reused-native.json').exists():native_dir=Path(json.loads((a.run/'reused-native.json').read_text())['directory'])
 if(native_dir/'terminal.json').exists():cells['native']={x['proof_id']:x for x in rawrows(native_dir/'results.jsonl')}
 latest={};streams=[];unknown=collections.Counter();events=0;flags=collections.Counter()
 sampled=collections.defaultdict(lambda:collections.Counter());previous_samples={}
 sampled_limits=collections.Counter()
 for file in sorted((a.run/'profiles').glob('*.jsonl.gz')):
  first=last=None;count=0;meta={}
  for q in snapshots(file):
   if '_stream_closed'in q:meta=q;continue
   events+=1;count+=1;first=first or q['time_ns'];last=q['time_ns']
   flags['sampler_error']=max(flags['sampler_error'],q.get('sampler_error',0))
   for t in q['threads']:
    sid=t['source_id'];phase=t['phase']
    for flag in ['dropped_keys','truncated_keys','frame_overflows','clock_errors']:
     flags[flag]=max(flags[flag],t.get(flag,0))
    if q['event']=='sample':
     ident=(q['pid'],t['tid']);prior=previous_samples.get(ident);previous_samples[ident]=(q['time_ns'],t)
     if prior:
      old_time,old=prior;dt=q['time_ns']-old_time;dc=t['thread_cpu_ns']-old['thread_cpu_ns']
      if dc<0:sampled_limits['negative_clock_intervals']+=1
      elif old['source_id']!=sid or old['phase']!=phase:sampled_limits['source_transition_intervals']+=1
      elif sid in wanted and phase=='body':
       if dt>2500000000:sampled_limits['long_sample_gaps']+=1;sampled_limits['long_gap_CPU_ns']+=dc
       else:
        stack=t['active'];component=stack[-1]['key']if stack else 'outside active profile boundary'
        tactic=next((f['key']for f in reversed(stack)if f['key'].startswith('tactic execution|')),'outside active tactic boundary')
        sampled[sid][('component',component)]+=dc;sampled[sid][('tactic',tactic)]+=dc
        sampled[sid][('observed','wall_ns')]+=dt
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
 sampling=[]
 for family in ['component','tactic']:
  counters=collections.Counter()
  for values in sampled.values():
   for(kind,key),value in values.items():
    if kind==family:counters[key]+=value
  sampling.append(dict(family=family,ranked=[dict(key=k,endpoint_weighted_thread_CPU_seconds=v/1e9)for k,v in counters.most_common()]))
 for row in per_source:
  row['sampled_CPU_weights']=[dict(family=k[0],key=k[1],nanoseconds=v)for k,v in sampled[row['source_id']].items()]
 ranked=[dict(key=k,**v)for k,v in sorted(totals.items(),key=lambda x:-x[1]['exclusive_cpu_ns'])]
 result=dict(source_count=len(wanted),sources_with_native_boundary_data=len(by_source),diagnostic_flags_maximum_over_threads=dict(flags),profile_status_counts=dict(collections.Counter(x['status']for x in cells['profile'].values())),status_changes_from_original=[dict(source_id=i,baseline=selected['baseline_statuses'][i],profile=cells['profile'][i]['status'])for i in selected['ids']if selected['baseline_statuses'][i]!=cells['profile'][i]['status']],ranked=ranked,open_frames=open_frames,profile_streams=streams,unknown_source_snapshot_counts=[dict(source_id=k[0],phase=k[1],records=v)for k,v in unknown.items()],events=events,sampled_endpoint_CPU_rankings=sampling,sampled_interval_limits=dict(sampled_limits),scope='Actual stock profileit/profileitM boundaries, child-subtracted thread CPU plus final observed open frames. Inclusive spans overlap. Endpoint-weighted1sCPU samples are approximate attribution; source transitions and long gaps are reported separately. This diagnostic is not a speedup, exhaustive source/CPU attribution, or removable critical-path fraction.')
 if 'native'in cells:
  def envelopes(directory):
   result={}
   for x in rawrows(directory/'http.jsonl'):
    if x.get('event')=='response':
     snippets=json.loads(x['request']).get('snippets',[])
     if len(snippets)==1 and snippets[0]['id']in wanted:
      sid=snippets[0]['id']
      if sid in result:raise RuntimeError('Retain retries; no ambiguous diagnostic comparison')
      result[sid]=(x['end_ns']-x['start_ns'])/1e9
   return result
  native_http=envelopes(native_dir);profile_http=envelopes(a.run/'profile')
  for row in per_source:
   sid=row['source_id'];row['fresh_native_HTTP_seconds']=native_http.get(sid)
   row['profile_HTTP_seconds']=profile_http.get(sid)
   row['fresh_native_body_seconds']=cells['native'][sid]['result'].get('time')
  result['fresh_native_profile_status_changes']=[dict(source_id=i,native=cells['native'][i]['status'],profile=cells['profile'][i]['status'])for i in selected['ids']if cells['native'][i]['status']!=cells['profile'][i]['status']]
  nt=json.loads((native_dir/'terminal.json').read_text());result['fresh_native_seconds']=nt['whole_lifecycle_seconds'];result['profile_seconds']=terminal['whole_lifecycle_seconds']
  result['extra_elapsed_percent']=(terminal['whole_lifecycle_seconds']/nt['whole_lifecycle_seconds']-1)*100
 # The full diagnostic still uses baseline-fixed groups, even if instrumentation
 # changes an outcome. Original failed-body zeroes are unavailable timings.
 reference=Path('/workspaces/repository/artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off')
 original={x['proof_id']:x for x in rawrows(reference/'results.jsonl')}
 profile_http=collections.defaultdict(list)
 for event in rawrows(a.run/'profile/http.jsonl'):
  if event.get('event')!='response':continue
  snippets=json.loads(event['request']).get('snippets',[])
  if len(snippets)==1 and snippets[0]['id']in wanted:
   profile_http[snippets[0]['id']].append((event['end_ns']-event['start_ns'])/1e9)
 for row in per_source:
  sid=row['source_id'];baseline=original[sid]
  if baseline['status']!=row['baseline_status']:raise RuntimeError('Baseline cohort status drift')
  row['baseline_reported_body_seconds']=None if baseline['status']=='resource_failure'else baseline['result'].get('time')
  if row['profile_status']=='resource_failure':row['profile_body_seconds']=None
  row['profile_HTTP_attempts']=len(profile_http[sid])
  row['profile_HTTP_seconds']=profile_http[sid][0]if len(profile_http[sid])==1 else None
  row['profile_HTTP_attempt_seconds']=profile_http[sid]
  row['has_body_profile_data']=any(k[2]==sid and k[3]=='body'for k in latest)
  if row['baseline_status']=='resource_failure':row['fresh_native_body_seconds']=None
 result['reference_native_directory']=str(reference)
 result['sources_with_body_profile_data']=sum(x['has_body_profile_data']for x in per_source)
 groups={}
 for name,cohort in [('all_selected',per_source)]+[
  ('baseline_'+status,[x for x in per_source if x['baseline_status']==status])
  for status in ['timeout_error','lean_error','resource_failure','valid']]:
  if not cohort:continue
  categories=collections.Counter();components=collections.Counter();tactics=collections.Counter()
  for row in cohort:
   for key,values in row['components'].items():
    categories[key.partition('|')[0]]+=values['exclusive_cpu_ns']
    components[key]+=values['exclusive_cpu_ns']
   for value in row['sampled_CPU_weights']:
    if value['family']=='tactic':tactics[value['key']]+=value['nanoseconds']
  groups[name]=dict(sources=len(cohort),
   profile_status_counts=dict(collections.Counter(x['profile_status']for x in cohort)),
   baseline_cumulative_HTTP_seconds=sum(x['baseline_HTTP_seconds']for x in cohort),
   baseline_reported_body_seconds_available=sum(x['baseline_reported_body_seconds']for x in cohort if x['baseline_reported_body_seconds']is not None),
   baseline_missing_body_timings=sum(x['baseline_reported_body_seconds']is None for x in cohort),
   profile_reported_body_seconds_available=sum(x['profile_body_seconds']for x in cohort if x['profile_body_seconds']is not None),
   profile_missing_body_timings=sum(x['profile_body_seconds']is None for x in cohort),
   profile_single_HTTP_seconds_available=sum(x['profile_HTTP_seconds']for x in cohort if x['profile_HTTP_seconds']is not None),
   profile_ambiguous_or_missing_HTTP_sources=[x['source_id']for x in cohort if x['profile_HTTP_seconds']is None],
   measured_category_exclusive_CPU_seconds=[dict(category=k,seconds=v/1e9)for k,v in categories.most_common()],
   measured_component_exclusive_CPU_seconds=[dict(key=k,seconds=v/1e9)for k,v in components.most_common()],
   sampled_tactic_endpoint_CPU_seconds=[dict(key=k,seconds=v/1e9)for k,v in tactics.most_common()])
 result['baseline_fixed_groups']=groups
 with(a.out/'per-source.csv').open('w',newline='')as f:
  fields=['source_id','baseline_status','profile_status','baseline_HTTP_seconds','baseline_reported_body_seconds',
   'profile_HTTP_seconds','profile_body_seconds','profile_HTTP_attempts','has_body_profile_data',
   'top_native_boundary','measured_exclusive_cpu_seconds']
  writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');writer.writeheader();writer.writerows(per_source)
 summary=['# Native failure-hotspot measurement — root self-review','',
  f"Completed diagnostic: {len(wanted)} selected sources; actual body-profile data for {result['sources_with_body_profile_data']}.",
  'Baseline-fixed groups retain the original timeout/error/resource classifications, even if profiled outcomes differ.',
  'This is a diagnostic, not a performance improvement or independent audit.','',
  'Counter CPU below includes completed child-subtracted runtime-boundary CPU and the last observed open-frame CPU.',
  'Inclusive wall/CPU spans overlap. One-second endpoint CPU attribution to active tactics is an estimate, not exact per-tactic time.',
  'Cumulative HTTP envelopes overlap across concurrent candidates and are not whole elapsed fractions.',
  'Resource-failure body clocks are missing, never zero-cost. Gzip termination/clock/table/sampling limits remain in result.json.','',
  '| Baseline group | Sources | Baseline cumulative HTTP (s) | Profile statuses | Missing baseline body clocks |',
  '|---|---:|---:|---|---:|']
 for name,g in groups.items():
  summary.append(f"| {name} | {g['sources']} | {g['baseline_cumulative_HTTP_seconds']:.6f} | {json.dumps(g['profile_status_counts'],sort_keys=True)} | {g['baseline_missing_body_timings']} |")
 for name,g in groups.items():
  summary+=['',f'## {name}: actual component CPU','',
   '| Stock profiler category | Observed exclusive thread CPU (s) |','|---|---:|']
  for value in g['measured_category_exclusive_CPU_seconds']:
   summary.append(f"| {value['category']} | {value['seconds']:.6f} |")
  summary+=['',f'### {name}: sampled active tactic attribution','',
   '| Actual innermost tactic kind | Endpoint-weighted thread CPU (s) |','|---|---:|']
  for value in g['sampled_tactic_endpoint_CPU_seconds'][:20]:
   summary.append(f"| {value['key'].replace('|',' / ')} | {value['seconds']:.6f} |")
 summary+=['','## Scope and remaining decisions','',
  f"Original-status changes: {len(result['status_changes_from_original'])}; all changed IDs remain in result.json.",
  f"Diagnostic capacity/clock flags: {json.dumps(result['diagnostic_flags_maximum_over_threads'],sort_keys=True)}.",
  f"Sampling transition/gap counts: {json.dumps(result['sampled_interval_limits'],sort_keys=True)}.",
  'Per-source.csv lists every selected attempt, original/profile outcome, observed cost, missing clock and top measured boundary.',
  'Per-source.json retains full named component and sampled tactic data; result.json retains open frames and stream completeness.',
  'Named tactic boundaries do not automatically expose nlinarith preprocessing, product generation, LP and certificate subphases.',
  'Any unmeasured internal subdivision remains unknown; do not borrow fractions from another corpus/version/run.',
  'Select the next own-method experiment from this completed distribution only after raw-result review.',
  'A small preflight may validate the analysis path but cannot select a whole-cohort dominant tactic.','']
 (a.out/'summary.md').write_text('\n'.join(summary))

 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 (a.out/'per-source.json').write_text(json.dumps(per_source,indent=2)+'\n')
 with(a.out/'ranked.csv').open('w',newline='')as f:
  if ranked:
   w=csv.DictWriter(f,fieldnames=list(ranked[0]),lineterminator='\n');w.writeheader();w.writerows(ranked)
 print(json.dumps({k:v for k,v in result.items()if k not in ['ranked','open_frames','profile_streams']},indent=2))
 print(json.dumps(ranked[:15],indent=2))
if __name__=='__main__':main()
