from pathlib import Path
import json,gzip,collections,argparse
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/current-dual-phase-profile'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/current-dual-phase-profile')
def rows(p):
 with (gzip.open(p,'rt')if str(p).endswith('.gz')else open(p))as f:return[json.loads(l)for l in f]
q=U/'qualification64-with-requests'
result={'scope':'Original64, width8, four CPUs4--7,48GiB. Diagnostic telemetry, not a primary timing score. Current CPU-oracle private build; no altered search or candidate checking.'}
m={}
for method in ['fast-hybrid','oracle-highs']:
 d=q/('rep1-'+method);rs=rows(d/'responses.jsonl.gz');ts=rows(d/'candidate-times.jsonl');cost=rows(d/'lean-costs.jsonl.gz')
 ref=U/('qualification64-profile/rep1-fast-hybrid'if method=='fast-hybrid'else'qualification64-normal/rep1-oracle-highs')
 rr=rows(ref/'responses.jsonl.gz')
 by={x['proof_id']:x for x in rs};rb={x['proof_id']:x for x in rr}
 differences=[k for k in by if by[k]['response']!=rb[k]['response']or by[k]['outcome']!=rb[k]['outcome']]
 sources={x['source']for x in ts};assert len(ts)==len(sources)==64
 native=[x for x in cost if x['ty']=='cost-native-roundtrip'];direct=[x for x in cost if x['ty']=='cost-direct-roundtrip']
 unique=[(x['source'],x['call_id'])for x in native+direct];assert len(unique)==len(set(unique))
 for x in native:
  req=x['request'];assert req['source']==x['source']and req['call_id']==x['call_id']
  assert len(req['product_columns'])==len(req['hyps'])
 for x in direct:
  req=x['request'];ans=x['answer'];assert req['source']==x['source']and req['call_id']==x['call_id']
  assert len(ans['product_columns'])==ans['exact_certificate_shape']['cols']
  assert ans['exact_certificate_shape']['nnz']>=0
 checks=[x for x in cost if x['ty']=='cost-direct-check']
 assert {(x['source'],x['call_id'])for x in checks}=={(x['source'],x['call_id'])for x in direct}
 assert not differences
 assert all(x['source']in sources for x in cost if 'source'in x)
 assert all('source'in x or x['ty']in ['fast','product-application']for x in cost)
 term=json.loads((d/'terminal.json').read_text())
 m[method]={'counts':dict(collections.Counter(x['outcome']for x in rs)),'reference_full_JSON_and_verdict_differences':differences,
 'whole_seconds':term['whole_ns']/1e9,'spans':len(ts),'native_requests':len(native),'auxiliary_source_less_rows':sum('source'not in x for x in cost),'direct_requests':len(direct),
 'direct_cert_null':sum(x['answer']['cert']is None for x in direct),'direct_checks_accepted':sum(x['accepted']for x in checks),
 'all_request_and_source_IDs_joined':True,'telemetry_types':dict(collections.Counter(x['ty']for x in cost)),
 'native_exact_shapes':'rows=maxVar+2; cols=len(hyps); nnz=nonzero exact coefficients plus strictness coefficient. These are unscaled certificate-space dimensions, not float-solver model dimensions.',
 'diagnostic_gzip_bytes':(d/'lean-costs.jsonl.gz').stat().st_size,'observer_read_errors':term['sampling_read_errors']}
normal=json.loads((U/'qualification64-normal/terminal.json').read_text())['results'][0]['whole_ns']/1e9
result.update(methods=m,normal_CPU_whole_seconds=normal,profile_CPU_over_normal=m['oracle-highs']['whole_seconds']/normal,
 full1000_diagnostic_admitted=True,limitations=['sequential single short overhead comparison is not an unbiased overhead estimate',
 'native fallback LP worker internal cancelled compute remains opaque; roundtrip includes communication/exact repair/wait',
 'a phase occupancy union is not an independently eliminable whole-wall fraction',
 'numerical metadata scan and lossless gzip I/O charged to diagnostic whole clock; not included in published primary ratios'])
(A/'request-qualification-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
