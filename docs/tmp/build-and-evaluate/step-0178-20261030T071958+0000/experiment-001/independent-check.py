import os,pathlib,json,gzip,datetime,math,re,time,resource,subprocess
os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
ROOT=pathlib.Path('/workspaces/repository')
STEP=pathlib.Path(pathlib.Path('/workspaces/.agent-state/gpu-smt-paper-mechanism-integration-step.txt').read_text().strip())
COMMIT='e259a49';start=time.monotonic()
def frozen(path):
 return subprocess.check_output(['git','-c','gc.auto=0','show',COMMIT+':research/mechanisms-2026-10-30/'+path],cwd=ROOT,text=True)
published=json.loads(frozen('retained-analysis/observed-memory-thresholds.json'))
point=ROOT/published['source']
def records(name):
 if name=='warm':
  with gzip.open(point/'warm/memory-rss.jsonl.gz','rt') as f:
   for line in f:
    x=json.loads(line);yield int(x['time_ns']),int(x['total_rss_bytes'])
 else:
  epoch=datetime.datetime(1970,1,1,tzinfo=datetime.timezone.utc)
  with gzip.open(point/'engine.stderr.gz','rt') as f:
   for line in f:
    x=json.loads(line);d=x.get('fields',{})
    if d.get('message')!='owned RSS sample':continue
    t=datetime.datetime.fromisoformat(x['timestamp'].replace('Z','+00:00'))-epoch
    yield (t.days*86400+t.seconds)*10**9+t.microseconds*1000,int(d['rss_bytes'])
traces={}
for name in ['warm','engine']:
 rows=list(records(name));gaps=[b[0]-a[0] for a,b in zip(rows,rows[1:])]
 assert rows and min(gaps)>=0
 span_ns=rows[-1][0]-rows[0][0];span=span_ns/1e9
 ps=published['trace_comparison'][name]
 assert len(rows)==ps['samples']
 assert math.isclose(span,ps['covered_span_seconds'],abs_tol=1e-6)
 assert max(x[1] for x in rows)==ps['sampled_peak_RSS_bytes']
 cells=[]
 for B in [8,16,32,48]:
  budget=B*2**30;over_ns=sum(dt for (a,b),dt in zip(zip(rows,rows[1:]),gaps) if a[1]>budget)
  pc=next(x for x in ps['cells'] if x['total_budget_GiB']==B)
  assert math.isclose(over_ns/1e9,pc['held_sample_seconds_above_threshold'],rel_tol=1e-9,abs_tol=1e-5)
  assert math.isclose(over_ns/span_ns,pc['fraction_of_observed_span_above'],rel_tol=1e-8,abs_tol=1e-9)
  cells.append({'threshold_GiB':B,'left_held_seconds_above':over_ns/1e9,'own_trace_fraction_above':over_ns/span_ns})
 traces[name]={'samples':len(rows),'own_trace_span_s':span,'sample_peak_RSS_bytes':max(x[1] for x in rows),
               'max_sample_gap_s':max(gaps)/1e9,'zero_gaps':gaps.count(0),'cells':cells,
               'clock':'warm monotonic nanoseconds' if name=='warm' else 'engine UTC log microseconds'}
stdout=frozen('native/phobos-grid-kernel-samples/stdout.txt')
source=frozen('GridCertificate.lean')
receipt=json.loads(frozen('native/phobos-grid-kernel-samples/receipt.json'))
assert receipt['exit']==0 and receipt['retired'] and receipt['signals_sent']==0
times={name:int(ns) for name,ns in re.findall(r'M_GRID_KERNEL_NS (\w+) (\d+)',stdout)}
assert len(times)==5 and stdout.count('does not depend on any axioms')==5
estimated=json.loads(frozen('compute-reference/grid-kernel-estimate.json'))
assert not estimated['full_grid_certificate_executed']
shapes={'block32':(2,2,32,32),'block64':(2,2,64,64),'block128':(2,2,128,128),
        'solutionBlockLeft':(2,390,32,32),'solutionBlockRight':(390,2,32,32)}
grid=[]
for name,(m,n,w,h) in shapes.items():
 target=f'theorem {name} : rectangle {m} {n} {w} {h} = true := by decide'
 assert target in source
 hits=[(i,j) for i in range(m,m+h) for j in range(n,n+w) if i*j==2005]
 assert all(i+j==406 for i,j in hits)
 row=next(x for x in estimated['samples'] if x['name']==name)
 seconds=times[name]/1e9;prediction=seconds/(w*h)*4016016
 assert row['cells']==w*h and row['kernel_recheck_seconds']==seconds
 assert math.isclose(prediction,row['linear_4016016_cell_estimate_seconds'],rel_tol=1e-12)
 grid.append({'name':name,'cells':w*h,'warm_kernel_recheck_ns':times[name],
              'independently_evaluated_included_solutions':hits,'linear_only_full_grid_s':prediction})
ref=json.loads(frozen('compute-reference/receipt.json'))
c_grid=[]
for run in ref['runs']:
 assert run['exit_code']==0 and run['naturally_retired']
 c_grid.append(float(re.search(r'lattice_CPU_seconds=([0-9.]+)',run['stdout'])[1]))
assert [len(x['independently_evaluated_included_solutions']) for x in grid]==[0,0,0,1,1]
result={'M_commit':COMMIT,'native_runs_by_root':0,
 'RSS_trace_independent_integer_timestamp_check':traces,
 'grid_native_receipt':{k:receipt[k] for k in ['exit','retired','wall_s','native_cpu_seconds','native_kernel_peak_rss_bytes','sampled_peak_owned_rss_bytes']},
 'grid_blocks':grid,'warm_recheck_subtotal_s':sum(times.values())/1e9,
 'full_grid_cells':4016016,'full_grid_native_certificate_executed':False,
 'C_numeric_grid_CPU_seconds':c_grid,'C_is_not_a_verified_or_same_boundary_comparison':True,
 'limits':['This self-review launches no native verifier and does not rerun M code.',
           'Left-hold sample integration is descriptive; gaps and overshoots are retained.',
           'Different trace clocks remain separate; no new-budget throughput or outcome is inferred.',
           'Five warm kernel rechecks include two nonvacuous solution blocks but do not cover the full grid.',
           'Linear prediction is neither a measured full-grid cost nor a certified upper bound.',
           'C arithmetic timings exclude proof construction/checking and cannot establish GPU speedup.'],
 'root_affinity':sorted(os.sched_getaffinity(0)),'elapsed_s':time.monotonic()-start,
 'root_process_peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(STEP/'experiment-001/independent-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
