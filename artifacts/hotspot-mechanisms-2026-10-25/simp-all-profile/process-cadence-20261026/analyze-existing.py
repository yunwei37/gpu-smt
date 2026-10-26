from pathlib import Path
import json,csv,sys
r=Path('/workspaces/repository');out=Path(sys.argv[1])
if out.exists():raise RuntimeError('Fresh analysis output required')
out.mkdir()
root=r/'artifacts/lean-failure-profile-2026-10-25/full480-analysis'
d=json.loads((root/'result.json').read_text())
h=json.loads((r/'artifacts/hotspot-mechanisms-2026-10-25/result.json').read_text())
source={v['source_id']:v for v in json.loads((root/'per-source.json').read_text())}
ids=h['dominant_groups']['simp_all']['ids'];assert len(ids)==23 and len(set(ids))==23
assert all(v==0 for v in d['diagnostic_flags_maximum_over_threads'].values())
rows=[]
for sid in ids:
 row=source[sid];assert row['profile_status']=='timeout_error'and row['profile_HTTP_attempts']==1
 frames=[f for f in d['open_frames']if f['source_id']==sid and f['phase']=='body'and f['key']=='simp|']
 assert len(frames)==1
 f=frames[0];group=[g for g in d['open_frames']if all(g[k]==f[k]for k in ['source_id','pid','tid','phase','snapshot_ns'])]
 at=group.index(f)
 ancestors=[g['key']for g in group[:at]if g['key'].startswith('tactic execution|')]
 assert ancestors and ancestors[-1]=='tactic execution|Lean.Parser.Tactic.simpAll'
 rows.append(dict(source_id=sid,pid=f['pid'],tid=f['tid'],snapshot_ns=f['snapshot_ns'],
  cumulative_completed_simp_calls=row['components']['simp|']['calls'],
  cumulative_completed_simp_all_calls=row['components']['tactic execution|Lean.Parser.Tactic.simpAll']['calls'],
  last_open_simp_wall_ns=f['observed_open_wall_ns'],
  last_open_simp_exclusive_thread_CPU_ns=f['observed_open_exclusive_cpu_ns'],
  active_ancestry=[g['key']for g in group[:at]]))
short=[x for x in rows if x['last_open_simp_wall_ns']<1000000000]
long=[x for x in rows if x['last_open_simp_wall_ns']>=1000000000]
result=dict(sources=23,rows=rows,clock_scope='Existing final observed body-open frames; non-atomic native clock samples, censored not completion. Counts are cumulative per selected source, not isolated last-invocation or round counts.',
 short_final_open_call=dict(count=len(short),range_wall_ns=[min(x['last_open_simp_wall_ns']for x in short),max(x['last_open_simp_wall_ns']for x in short)],range_cumulative_simp_calls=[min(x['cumulative_completed_simp_calls']for x in short),max(x['cumulative_completed_simp_calls']for x in short)]),
 long_final_open_call=dict(count=len(long),range_wall_ns=[min(x['last_open_simp_wall_ns']for x in long),max(x['last_open_simp_wall_ns']for x in long)]),
 split_scope='One second is the existing diagnostic cadence, used for descriptive table only, never a failure/admission rule. Observed ranges are far apart.',
 many_completed_outer_calls=[dict(source_id=x['source_id'],completed=x['cumulative_completed_simp_all_calls'])for x in short if x['cumulative_completed_simp_all_calls']>1],
 native_candidate_executions=0,independent_or_new_native_data=False,
 scope='Complete reuse of fixed23 selected native timeouts from completed480. Not whole-population prevalence, performance, per-phase causal blame or a cycle/rejection certificate.')
(out/'result.json').write_text(json.dumps(result,indent=2)+chr(10))
with(out/'per-source.csv').open('w',newline='')as f:
 fields=[k for k in rows[0]if k!='active_ancestry'];writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows({k:x[k]for k in fields}for x in rows)
print(json.dumps({k:v for k,v in result.items()if k!='rows'},indent=2),flush=True)
