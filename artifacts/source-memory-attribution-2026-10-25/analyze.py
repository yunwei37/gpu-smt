"""Infer sampled process occupancy, never true source allocation/high-water."""
import pathlib,collections,json,gzip,csv,bisect,runpy,datetime,time,os,threading,psutil,sys
R=pathlib.Path('/workspaces/repository');A=pathlib.Path(__file__).resolve().parent
RUN=R/'artifacts/lean-failure-profile-2026-10-25/full480'
os.sched_setaffinity(0,{8,9,10,11})
begin=time.monotonic();budget=48*1024**3;own=psutil.Process();old=psutil.Process(283334)
assert abs(old.create_time()-1792912973.05)<.01
stop=threading.Event();resource=[]
def watch():
 while not stop.is_set():
  procs={}
  for root in [own,old]:
   try:
    for p in [root]+root.children(recursive=True):
     try:procs[(p.pid,p.create_time())]=p.memory_info().rss
     except psutil.NoSuchProcess:pass
   except psutil.NoSuchProcess:pass
  n=sum(procs.values());resource.append(dict(seconds=time.monotonic()-begin,rss_bytes=n))
  if n>budget:
   (A/'analysis-pressure.json').write_text(json.dumps(dict(aggregate_rss_bytes=n,budget_bytes=budget,scope='Abort only this new offline analysis; preserve the original group'))+'\n')
   os._exit(137)
  stop.wait(1)
thread=threading.Thread(target=watch,daemon=True);thread.start()
selected=json.loads((RUN/'selected.json').read_text());wanted=set(selected['ids']);assert len(wanted)==480
terminal=json.loads((RUN/'profile/terminal.json').read_text())
assert terminal['state']=='complete'and terminal['returned']==480
def rows(path):
 with gzip.open(path,'rt')as f:
  for line in f:
   if line.strip():yield json.loads(line)
outcomes={v['proof_id']:v for v in rows(RUN/'profile/results.jsonl.gz')}
assert set(outcomes)==wanted
windows=collections.defaultdict(list)
for row in rows(RUN/'profile/http.jsonl.gz'):
 if row.get('event')!='response':continue
 request=json.loads(row['request']);items=request.get('snippets',[])
 if len(items)==1 and items[0]['id']in wanted:
  windows[items[0]['id']].append((row['start_ns'],row['end_ns']))
memory=[];births=collections.defaultdict(set);global_samples=0
for row in rows(RUN/'profile/memory-rss.jsonl.gz'):
 global_samples+=1
 workers=[]
 for p in row['processes']:
  if p.get('native_repl'):
   births[p['pid']].add(p['birth']);workers.append(dict(pid=p['pid'],birth=p['birth'],rss=p['rss']))
 memory.append(dict(time=row['time_ns'],total=row['total_rss_bytes'],workers=workers))
reader=runpy.run_path(str(R/'bench/lean-failure-profile/analyze.py'))['snapshots']
timelines={};streams=[];flags=collections.Counter()
def label(row):
 named={t['source_id']for t in row['threads']if t.get('source_id')not in ['',None,'unknown']}
 unknown_active=any(t.get('source_id')in ['',None,'unknown']and t.get('active')for t in row['threads'])
 if unknown_active:return None,None,'active_unknown_thread'
 if len(named)!=1:return None,None,'no_unique_thread_source'
 sid=next(iter(named))
 if sid not in wanted:return None,None,'outside_selected_sources'
 phases={t['phase']for t in row['threads']if t['source_id']==sid}
 if not phases or not phases<={'header','body'}:return None,None,'unusable_phase'
 return sid,next(iter(phases))if len(phases)==1 else'transition','eligible_label'
for path in sorted((RUN/'profiles').glob('*.jsonl.gz')):
 pid=int(path.name.split('.')[0]);states=[];last=None;previous=None;records=0;meta=None
 for row in reader(path):
  if '_stream_closed'in row:meta=row;continue
  assert row['pid']==pid
  records+=1
  if previous is not None and row['time_ns']<previous:raise RuntimeError('Nonmonotonic profile timeline')
  previous=row['time_ns']
  flags['sampler_error']=max(flags['sampler_error'],row.get('sampler_error',0))
  for t in row['threads']:
   for k in ['dropped_keys','truncated_keys','frame_overflows','clock_errors']:
    flags[k]=max(flags[k],t.get(k,0))
  info=(row['time_ns'],)+label(row)
  if not states or row['event']in ['sample','source_boundary']or info[1:]!=states[-1][1:]:
   states.append(info)
  last=info
 if last and(states[-1][0]!=last[0]):states.append(last)
 if states:timelines[pid]=([x[0]for x in states],states)
 streams.append(dict(path=str(path.relative_to(R)),pid=pid,records=records,retained_states=len(states),**(meta or{})))
coverage=collections.Counter();assigned=collections.defaultdict(list);envelopes=collections.defaultdict(list);excluded_by_pid=collections.defaultdict(collections.Counter)
single_windows={sid:vs[0]for sid,vs in windows.items()if len(vs)==1}
for sample in memory:
 now=sample['time'];per_source=collections.defaultdict(list)
 for sid,(start,end)in single_windows.items():
  if start<=now<=end:
   envelopes[sid].append((now,sum(p['rss']for p in sample['workers']),sample['total']))
 for p in sample['workers']:
  pid=p['pid'];reason=None
  if len(births[pid])!=1:reason='ambiguous_pid_birth'
  elif pid not in timelines:reason='no_profile_timeline'
  else:
   times,states=timelines[pid];index=bisect.bisect_right(times,now)-1
   if index<0 or index+1>=len(states):reason='unbracketed_time'
   else:
    left,right=states[index],states[index+1]
    if left[1]is None or right[1]is None:reason='unusable_label_bracket'
    elif left[1]!=right[1]:reason='source_transition_bracket'
    elif right[0]-left[0]>2500000000:reason='over_2_5s_bracket_gap'
    elif left[1]not in single_windows:reason='missing_or_multiple_HTTP_envelopes'
    else:
     sid=left[1];start,end=single_windows[sid]
     if not start<=now<=end:reason='outside_source_HTTP_envelope'
     else:
      phase=left[2]if left[2]==right[2]else'transition'
      per_source[sid].append(dict(pid=pid,birth=p['birth'],rss=p['rss'],phase=phase))
  if reason:
   coverage[reason]+=1;excluded_by_pid[pid][reason]+=1
  else:coverage['bracket_inferred_worker_samples']+=1
 for sid,procs in per_source.items():
  assigned[sid].append(dict(time_ns=now,workers=procs,
   attributed_native_rss_bytes=sum(p['rss']for p in procs),whole_owned_rss_bytes=sample['total']))
def stats(vals):
 vals=sorted(vals)
 if not vals:return None
 import math
 return dict(n=len(vals),p50=vals[math.ceil(len(vals)*.5)-1],p90=vals[math.ceil(len(vals)*.9)-1],max=vals[-1])
per=[]
for sid in selected['ids']:
 samples=assigned[sid];env=envelopes[sid]
 error=str(outcomes[sid]['result'].get('error',''))
 peak=max(samples,key=lambda s:s['attributed_native_rss_bytes'])if samples else None
 workers=[p for s in samples for p in s['workers']]
 per.append(dict(source_id=sid,baseline_status=selected['baseline_statuses'][sid],profile_status=outcomes[sid]['status'],
  profile_HTTP_envelopes=len(windows[sid]),HTTP_seconds=(single_windows[sid][1]-single_windows[sid][0])/1e9 if sid in single_windows else None,
  bracket_inferred_snapshot_count=len(samples),native_process_identities=sorted({str(p['pid'])+'@'+str(p['birth'])for p in workers}),
  sampled_attributed_native_rss_max_bytes=peak['attributed_native_rss_bytes']if peak else None,
  sampled_single_worker_rss_max_bytes=max((p['rss']for p in workers),default=None),
  sampled_header_worker_rss_max_bytes=max((p['rss']for p in workers if p['phase']=='header'),default=None),
  sampled_body_worker_rss_max_bytes=max((p['rss']for p in workers if p['phase']=='body'),default=None),
  concurrent_sampled_native_envelope_max_bytes=max((x[1]for x in env),default=None),
  concurrent_sampled_whole_envelope_max_bytes=max((x[2]for x in env),default=None),
  process_phase_at_peak=sorted({p['phase']for p in peak['workers']})if peak else[],
  HTTP_memory_snapshots=len(env),reported_error_contains_bad_alloc='bad_alloc'in error))
groups={}
for status in sorted({x['profile_status']for x in per}):
 subset=[x for x in per if x['profile_status']==status]
 groups[status]=dict(sources=len(subset),with_inferred_samples=sum(x['bracket_inferred_snapshot_count']>0 for x in subset),
  source_ids_without_inferred_samples=[x['source_id']for x in subset if not x['bracket_inferred_snapshot_count']],
  sampled_single_worker_rss_max_bytes=stats([x['sampled_single_worker_rss_max_bytes']for x in subset if x['sampled_single_worker_rss_max_bytes']is not None]),
  sampled_attributed_native_rss_max_bytes=stats([x['sampled_attributed_native_rss_max_bytes']for x in subset if x['sampled_attributed_native_rss_max_bytes']is not None]),
  reported_bad_alloc_count=sum(x['reported_error_contains_bad_alloc']for x in subset))
result=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),selected_sources=len(wanted),original_statuses=dict(collections.Counter(selected['baseline_statuses'].values())),profile_statuses=dict(collections.Counter(x['profile_status']for x in per)),
  same_run_profile_lifecycle_seconds=terminal['whole_lifecycle_seconds'],global_memory_snapshots=global_samples,
  native_worker_samples=sum(len(x['workers'])for x in memory),attribution_counts=dict(coverage),groups=groups,per_source=per,
  PID_birth_representation='psutil create_time Unix seconds, not Rust kernel start ticks',status_changes_from_baseline=[dict(source_id=x['source_id'],baseline=x['baseline_status'],profile=x['profile_status'])for x in per if x['baseline_status']!=x['profile_status']],profile_streams=streams,profile_flags_maximum=dict(flags),profile_PID_birth_ambiguities={str(k):sorted(v)for k,v in births.items()if len(v)!=1},
  method='Same-process PID/unique observed birth and adjacent source-label agreement, <=2.5s bracketing gap, same-clock single HTTP envelope. Includes retained state, not source-only allocations.',
  limitations=['1s RSS samples can miss allocation bursts and true peaks.','Native profile ownership labels update at profile boundaries, not every allocation; bracket attribution is inferred, not exact allocation ownership.',
  'Concurrent RSS envelopes are totals at sampled times, never per-source peaks or bounds on unobserved maxima.',
  'Warm process history, imports, diagnostic tables and instrumentation remain in occupancy.',
  'Selected480are failed/slow observations only; not a representative complete7808population.',
  'All records retain old2worker/24GiB AS/48GiB sampled total point; fixed AS failures are not labels for >24GiB or >48GiB RSS.',
  'Unclosed gzip streams/unknown intervals/missing observations remain explicit. No source peak is filled with zero.',
  'This is an offline diagnostic, not a source predictor, runtime speedup, Amdahl bound or independent audit.'])
assert sum(coverage.values())==result['native_worker_samples']
(A/'result.json').write_text(json.dumps(result,indent=2)+'\n')
with(A/'per-source.csv').open('w',newline='')as f:
 writer=csv.DictWriter(f,fieldnames=list(per[0]),lineterminator='\n')
 writer.writeheader()
 for row in per:
  writer.writerow({k:json.dumps(v)if isinstance(v,list)else v for k,v in row.items()})
(A/'attributed-samples.jsonl.gz').write_bytes(gzip.compress((''.join(json.dumps(dict(source_id=sid,**sample))+'\n'for sid,samples in assigned.items()for sample in samples)).encode(),mtime=0))
stop.set();thread.join()
(A/'analysis-resources.json').write_text(json.dumps(dict(peak_sampled_aggregate_owned_rss_bytes=max(x['rss_bytes']for x in resource),samples=resource,budget_bytes=budget,
 scope='Only this offline process and verified original group; no new native acquisition or fixed AS cap. Abort only new analysis on pressure, preserving old capture.'),indent=2)+'\n')
print(json.dumps(dict(groups=groups,attribution=result['attribution_counts'],streams=len(streams),unclosed_streams=sum(not x.get('_stream_closed')for x in streams),flags=dict(flags),analysis_seconds=time.monotonic()-begin),indent=2),flush=True)
