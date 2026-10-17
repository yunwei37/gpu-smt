from pathlib import Path
import urllib.request,json
n=Path(__file__).resolve().parent
pin='a6616e99534ce777dcebfd56566eaaffb63997a8'
base='https://raw.githubusercontent.com/memo-ozdincer/shred/'+pin+'/'
def get(name):
 with urllib.request.urlopen(base+name,timeout=45) as f:return json.load(f)
a=get('reports/c0_certificate_prevalence_d030.json')
b=get('reports/c0_opportunity_decomposition.json')
c=get('reports/c0_rl_retention_gate.json')
x=a['strata']['representative'];y=a['strata']['enriched']
result={'upstream_revision':pin,'scope':'recomputed published upstream aggregates only; no Lean replay, raw-pair replication, GPU execution or imported gate','representative':{'proposals':x['proposals'],'verdict_agreements':x['verdict_agreements'],'baseline_cpu_seconds':x['baseline_cpu_seconds'],'cached_cpu_seconds':x['cached_cpu_seconds'],'cpu_saved_fraction':1-x['cached_cpu_seconds']/x['baseline_cpu_seconds'],'cpu_equivalent_ratio':x['baseline_cpu_seconds']/x['cached_cpu_seconds']},'rooted_prefix_diagnostic':{'observed_cpu_denominator_seconds':b['baseline']['full_cpu_seconds_with_telemetry'],'estimated_repeated_cpu_seconds':b['registered_exact_rooted_prefix']['saved_cpu_seconds_mean_representative'],'fraction':b['registered_exact_rooted_prefix']['saved_cpu_seconds_mean_representative']/b['baseline']['full_cpu_seconds_with_telemetry'],'scope':b['baseline']['warning'],'registered_proposals':b['counts']['proposals'],'process_failures':b['counts']['full_process_failures']},'enriched':{'proposals':y['proposals'],'verdict_disagreements':len(y['verdict_disagreements']),'cpu_saved_fraction':y['paired_cpu_saved_fraction'],'scope':'selected expensive group, incomplete enriched study; not a generalized valid win'},'rl_overlap':{'proposals':c['overlap']['proposals'],'cpu_saved_fraction':1-c['overlap']['cached_cpu_seconds']/c['overlap']['baseline_cpu_seconds'],'scope':'existing overlap subset, not new held-out C1 execution'}}
(n/'upstream-aggregate-recomputation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
