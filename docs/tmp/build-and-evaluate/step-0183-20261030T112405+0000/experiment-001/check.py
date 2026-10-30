from pathlib import Path
import collections,gzip,json,math,os,resource,time,sys,importlib,datetime
os.sched_setaffinity(0,{0,1});sys.dont_write_bytecode=True
t0=time.monotonic();root=Path('/workspaces/repository')
pair=root/'artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z'
m=root/'research/mechanisms-2026-10-30'
with gzip.open(pair/'engine.stdout.gz','rt') as f:d=json.load(f)
assert len(d['results'])==7808 and len({r['id'] for r in d['results']})==7808
rows=[{'id':r['id'],'cost':math.fsum(a['elapsed_seconds'] for a in r['attempts']),
       'peak':max(a['peak_rss_bytes'] for a in r['attempts']),'accepted':r['outcome']['status']=='accepted'} for r in d['results']]
engine=collections.Counter((r['attempts'][0]['status'],r['attempts'][-1]['status'])
                           for r in d['results'] if len(r['attempts'])>1)
assert all(len(r['attempts'])<=2 for r in d['results'])
warm=collections.defaultdict(list)
with gzip.open(pair/'warm/attempts.jsonl.gz','rt') as f:
 for l in f:
  x=json.loads(l);warm[x['id']].append(x)
assert len(warm)==7808 and all(1<=len(a)<=2 for a in warm.values())
assert all(not a[0]['exclusive'] and (len(a)==1 or a[-1]['exclusive']) for a in warm.values())
trans=collections.Counter((a[0]['status'],a[-1]['status']) for a in warm.values() if len(a)>1)
timeouts=[k for k,a in warm.items() if len(a)>1 and a[-1]['status']=='timeout_error']
snapshot=None
with gzip.open(pair/'warm/memory-rss.jsonl.gz','rt') as f:
 for l in f:
  x=json.loads(l);p=[p for p in x['processes'] if p.get('native_repl') and p['rss']>3*1024**3]
  if len(p)==4:
   snapshot={'time_ns':x['time_ns'],'total_rss_bytes':x['total_rss_bytes'],'repl_rss_bytes':[p['rss'] for p in p],
     'native_repl_count':x['native_repl_count'],'budget_bytes':x['budget_bytes']};break
assert snapshot and snapshot['total_rss_bytes']>8*1024**3
published=json.loads((m/'retained-analysis/memory-full-coverage-retry.json').read_text())
assert trans==collections.Counter({(x['from'],x['to']):x['count'] for x in published['warm_retry_transitions']})
assert engine==collections.Counter({(x['from'],x['to']):x['count'] for x in published['engine_retry_transitions']})
sys.path.insert(0,str(m));module=importlib.import_module('memory_retry_simulation')
matrix=[]
for cell in published['matrix']:
 b=cell['budget_bytes'];fit=[r for r in rows if 0<r['peak']<=b]
 assert len(fit)==cell['fit'] and len(rows)-len(fit)==cell['excluded']
 out=[]
 for scenario in cell['scenarios']:
  v=module.retry_model(fit,b,scenario['cleanup_s_per_preemption_scenario'])
  for k in ['terminal_coverage','original_accepted_retained_by_assumption','preemptions','lost_results']:
   assert v[k]==scenario[k],(k,v,scenario)
  assert math.isclose(v['makespan_proxy_s'],scenario['makespan_proxy_s'],rel_tol=1e-12,abs_tol=1e-7)
  out.append(v)
 matrix.append({'budget_GiB':b/1024**3,'fit':len(fit),'excluded':len(rows)-len(fit),'scenarios':out})
receipt={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_invocations':0,
 'sources':7808,'warm_attempts':sum(map(len,warm.values())),'engine_attempts':sum(len(r['attempts']) for r in d['results']),
 'warm_retry_transitions':[{'from':a,'to':b,'count':n} for (a,b),n in sorted(trans.items())],
 'engine_retry_transitions':[{'from':a,'to':b,'count':n} for (a,b),n in sorted(engine.items())],
 'warm_solo_timeout_ids':timeouts,'first_four_warm_above3GiB':snapshot,'recomputed_matrix':matrix,
 'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
out=Path(sys.argv[1]);out.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='recomputed_matrix'},indent=2))
