from pathlib import Path
import zipfile,json,re,statistics,collections,datetime
D=Path(__file__).parent;B=D/'product-application-full1'
original=[json.loads(l) for l in (D/'input.jsonl').read_text().splitlines()]
raw={}
for method in ['fast','fast-products']:
 label='goedel427-rep0-'+method
 with zipfile.ZipFile(B/(label+'.zip')) as z:
  raw[method]={r['source_index']:r for r in map(json.loads,z.read(label+'/results.jsonl').splitlines())}
def distribution(values):
 values=sorted(values)
 return {'n':len(values),'p50_s':statistics.median(values),'p95_s':values[int(.95*(len(values)-1))],'p99_s':values[int(.99*(len(values)-1))]} if values else {'n':0}
groups=collections.defaultdict(list)
for item in original:
 index=item['index'];text=item['code']
 group='text nlinarith' if re.search(r'\bnlinarith\b',text) else 'text linarith without nlinarith' if re.search(r'\blinarith\b',text) else 'neither tactic name in source text'
 a,b=raw['fast'][index],raw['fast-products'][index]
 groups[group].append({'source_index':index,'reference_seconds':a['elapsed_seconds'],'candidate_seconds':b['elapsed_seconds'],'reference_basic':a['basic'],'candidate_basic':b['basic']})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All29750 original complete first-pair rows; source-text strata only, not dynamic mechanism coverage. Names may appear in comments and indirect tactic calls are possible. Shared-background closed-loop latencies are neither kernel CPU costs nor makespan components. No source/outcome removal from the primary whole result. One pair does not isolate causal effect.','groups':{}}
for group,rows in groups.items():
 same=[r for r in rows if r['reference_basic']==r['candidate_basic']]
 out['groups'][group]={'all_sources':len(rows),'reference_latency':distribution([r['reference_seconds'] for r in rows]),'candidate_latency':distribution([r['candidate_seconds'] for r in rows]),'reference_outcomes':dict(collections.Counter(r['reference_basic'] for r in rows)),'candidate_outcomes':dict(collections.Counter(r['candidate_basic'] for r in rows)),'basic_changed_indices':[r['source_index'] for r in rows if r['reference_basic']!=r['candidate_basic']],'same_basic_request_latency_reference':distribution([r['reference_seconds'] for r in same]),'same_basic_request_latency_candidate':distribution([r['candidate_seconds'] for r in same])}
(D/'product-application-first-pair-source-strata.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'sources':sum(x['all_sources'] for x in out['groups'].values()),'groups':{k:v['all_sources'] for k,v in out['groups'].items()}}))
