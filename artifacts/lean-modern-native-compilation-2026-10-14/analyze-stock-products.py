from pathlib import Path
import argparse,importlib.util,json,statistics,zipfile,collections,datetime
D=Path(__file__).parent
ap=argparse.ArgumentParser();ap.add_argument('--preflight',action='store_true');args=ap.parse_args()
B=D/'stock-products-preflight1/cells' if args.preflight else D/'stock-products-full1'
spec=importlib.util.spec_from_file_location('completed_stock_cell',D/'analyze-native-oracle.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cells={};engagement={}
for p in sorted(B.glob('*.terminal.json')):
 t=json.loads(p.read_text())
 try:cells[t['label']]=m.load_cell(B,t)
 except (FileNotFoundError,zipfile.BadZipFile) as e:
  cells[t['label']]={'valid_complete':False,'raw_finalize_pending':str(e)};continue
 label=t['label'];folder=B/label
 try:
  if folder.is_dir():data=(folder/'product-applications.jsonl').read_text()
  else:
   with zipfile.ZipFile(B/(label+'.zip')) as z:data=z.read(label+'/product-applications.jsonl').decode()
  rows=[json.loads(x) for x in data.splitlines() if x.strip()]
  engagement[label]={'product_invocations':len(rows),'built':sum(x.get('built',0) for x in rows),'reused':sum(x.get('reused',0) for x in rows),'products':sum(x.get('products',0) for x in rows)}
 except (FileNotFoundError,KeyError):pass
pairs=[]
for rep in range(1 if args.preflight else 3):
 names=['stock','products'] if args.preflight else [f'goedel427-rep{rep}-'+x for x in ['stock','products']]
 if not all(n in cells and cells[n].get('valid_complete') for n in names):continue
 a,b=[cells[n] for n in names]
 basics=[{'source_index':i,'reference':x,'candidate':b['basic_rows'].get(i)} for i,x in a['basic_rows'].items() if x!=b['basic_rows'].get(i)]
 native=[i for i,x in a['native_rows'].items() if x!=b['native_rows'].get(i)]
 pairs.append({'rep':rep,'reference_seconds':a['whole_seconds'],'candidate_seconds':b['whole_seconds'],'wall_reduction_percent':100*(1-b['whole_seconds']/a['whole_seconds']),'basic_differences':basics,'native_payload_differences_excluding_only_adapter_time':native,'reference_request_latency':a['request_latency_seconds'],'candidate_request_latency':b['request_latency_seconds']})
planned=2 if args.preflight else 8
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Original native arithmetic solver/configuration plus whole-library native compilation; candidate only replaces nlinarith product construction. Allsource bytes/native fields retained. Preflight is dependency engagement, not primary performance. Shared background; profiles separate; no partial clocks/cross-affinity or cross-version ratios.','preflight':args.preflight,'completed_valid_cells':sum(bool(x.get('valid_complete')) for x in cells.values()),'planned_cells':planned,'all_planned_complete':len(cells)==planned and all(x.get('valid_complete') for x in cells.values()),'pairs':pairs,'mean_wall_reduction_percent':statistics.mean(x['wall_reduction_percent'] for x in pairs) if pairs and not args.preflight else None,'engagement':engagement,'cells':{k:{f:v for f,v in c.items() if f not in ['basic_rows','native_rows','legacy_rows']} for k,c in cells.items()}}
target=D/('stock-products-preflight1-analysis.json' if args.preflight else 'stock-products-complete-cells-analysis.json')
target.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['preflight','completed_valid_cells','planned_cells','all_planned_complete','mean_wall_reduction_percent','engagement']}))
