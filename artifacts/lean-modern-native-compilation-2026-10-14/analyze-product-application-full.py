from pathlib import Path
import importlib.util,json,datetime,statistics,zipfile
D=Path(__file__).parent;B=D/'product-application-full1'
spec=importlib.util.spec_from_file_location('completed_native_cell_analysis',D/'analyze-native-oracle.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cells={}
for p in sorted(B.glob('*.terminal.json')):
 t=json.loads(p.read_text())
 try:cells[t['label']]=m.load_cell(B,t)
 except (FileNotFoundError,zipfile.BadZipFile) as e:
  cells[t['label']]={'valid_complete':False,'raw_finalize_pending':str(e)}
pairs=[]
for rep in range(3):
 names=[f'goedel427-rep{rep}-{method}' for method in ['fast','fast-products']]
 if not all(n in cells and cells[n].get('valid_complete') for n in names):continue
 a,b=[cells[n] for n in names]
 pairs.append({'rep':rep,'reference_seconds':a['whole_seconds'],'candidate_seconds':b['whole_seconds'],
  'wall_reduction_percent':100*(1-b['whole_seconds']/a['whole_seconds']),
  'basic_differences':[i for i,x in a['basic_rows'].items() if x!=b['basic_rows'].get(i)],
  'native_payload_differences_excluding_only_adapter_time':[i for i,x in a['native_rows'].items() if x!=b['native_rows'].get(i)],
  'reference_throughput':a['terminal_attempts_per_second'],'candidate_throughput':b['terminal_attempts_per_second'],
  'reference_request_latency':a['request_latency_seconds'],'candidate_request_latency':b['request_latency_seconds']})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'planned_cells':8,'completed_valid_cells':sum(bool(c.get('valid_complete')) for c in cells.values()),
 'all_planned_complete':len(cells)==8 and all(c.get('valid_complete') for c in cells.values()),
 'primary_pairs':pairs,'mean_wall_reduction_percent':statistics.mean(x['wall_reduction_percent'] for x in pairs) if pairs else None,
 'observed_pair_range_percent':[min(x['wall_reduction_percent'] for x in pairs),max(x['wall_reduction_percent'] for x in pairs)] if pairs else None,
 'cells':{k:{f:v for f,v in c.items() if f not in ['basic_rows','native_rows','legacy_rows']} for k,c in cells.items()},
 'scope':'all29750original source bytes per cell, three alternating primary pairs; separate observer/resource profiles; shared background/defaultCPUeligibility; no partial clocks or across-affinity ratios. Native payload differences exclude only backward adapter duration, not diagnostic IDs. Entire matrix and result review required for full performance.'}
(D/'product-application-complete-cells-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['completed_valid_cells','all_planned_complete','mean_wall_reduction_percent','observed_pair_range_percent']}))
