"""Offline analysis of completed stock-service cells; never an execution gate."""
from pathlib import Path
import argparse,json,statistics,zipfile,datetime,collections
R=Path('/workspaces/repository')
def native(body,status):
 try:
  result=body['results'][0]
  response=result.get('response')
  # Pinned backward.py injects measured check_response.time into this object.
  # Keep raw JSON unchanged; compare native fields separately from that timer.
  return {k:v for k,v in response.items() if k!='time'} if isinstance(response,dict) else {'http_status':status,'error':result.get('error')}
 except (KeyError,IndexError,TypeError):
  return {'http_status':status,'service_response':body}
def distribution(values):
 values=sorted(values)
 return dict(n=len(values),median=statistics.median(values),p95=values[int(.95*(len(values)-1))],p99=values[int(.99*(len(values)-1))]) if values else dict(n=0)
def load_cell(base,terminal):
 label=terminal['label'];folder=base/label
 archive=None
 if folder.is_dir():read=lambda name:(folder/name).read_bytes()
 else:
  archive=zipfile.ZipFile(base/(label+'.zip'))
  read=lambda name:archive.read(label+'/'+name)
 try:
  source=base.parent/'input.jsonl'
  originals=[json.loads(s) for s in source.read_bytes().splitlines() if s.strip()]
  rows=sorted([json.loads(s) for s in read('results.jsonl').splitlines() if s.strip()],key=lambda x:x['ordinal'])
  issues=[]
  if read('input.jsonl')!=source.read_bytes():issues.append('original input bytes differ')
  if len(rows)!=len(originals):issues.append('returned population differs')
  indices=[]
  native_rows={}
  legacy_rows={}
  for ordinal,row in enumerate(rows):
   indices.append(row['source_index'])
   if row.get('ordinal')!=ordinal or ordinal>=len(originals) or row['source_index']!=originals[ordinal]['index']:issues.append(dict(ordinal=ordinal,error='order/index differs'))
   try:body=json.loads(read(row['raw_response']))
   except (ValueError,UnicodeDecodeError):body=dict(non_json_bytes=read(row['raw_response']).hex())
   native_rows[row['source_index']]=native(body,row['status_code'])
   legacy_rows[row['source_index']]=body
  if len(set(indices))!=len(indices):issues.append('duplicate indices')
  try:resources=json.loads(read('resources-summary.json'))
  except (KeyError,FileNotFoundError):resources=None
  valid=not terminal['failure'] and len(rows)==terminal['expected']==len(originals) and not issues
  return dict(label=label,dataset=terminal['dataset'],method=terminal['method'],profile=terminal['profile'],valid_complete=valid,
   returned=len(rows),expected=len(originals),whole_seconds=terminal['whole_seconds'],
   terminal_attempts_per_second=len(rows)/terminal['whole_seconds'],counts=dict(collections.Counter(x['basic'] for x in rows)),
   request_latency_seconds=distribution([x['elapsed_seconds'] for x in rows]),source_issues=issues,server_returncode=terminal['server_returncode'],
   resources=resources,basic_rows={x['source_index']:x['basic'] for x in rows},native_rows=native_rows,legacy_rows=legacy_rows)
 finally:
  if archive:archive.close()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);args=ap.parse_args();out=args.root;base=out/'native-oracle-full1'
 if out.name=='lean-modern-native-compilation-2026-10-14':reference,candidate='aot','native'
 elif out.name=='lean-stock-service-2026-10-14':reference,candidate='warm','fresh'
 else:raise ValueError('unsupported raw acquisition')
 cells={}
 for path in sorted(base.glob('*.terminal.json')):
  terminal=json.loads(path.read_text())
  try:cells[terminal['label']]=load_cell(base,terminal)
  except (zipfile.BadZipFile,FileNotFoundError) as e:
   cells[terminal['label']]=dict(label=terminal['label'],valid_complete=False,raw_finalize_pending=str(e))
 pairs=[]
 for ds in ['goedel427']:
  for rep in range(3):
   names=[ds+f'-rep{rep}-'+method for method in [reference,candidate]]
   if not all(name in cells and cells[name]['valid_complete'] for name in names):continue
   a,b=[cells[name] for name in names]
   basics=[dict(source_index=i,reference=a['basic_rows'][i],candidate=b['basic_rows'].get(i)) for i in a['basic_rows'] if a['basic_rows'][i]!=b['basic_rows'].get(i)]
   artifacts=[i for i in a['native_rows'] if a['native_rows'][i]!=b['native_rows'].get(i)]
   legacy=[i for i in a['legacy_rows'] if a['legacy_rows'][i]!=b['legacy_rows'].get(i)]
   pairs.append(dict(dataset=ds,rep=rep,reference=reference,candidate=candidate,reference_seconds=a['whole_seconds'],candidate_seconds=b['whole_seconds'],
    wall_reduction_percent=100*(1-b['whole_seconds']/a['whole_seconds']),basic_differences=basics,native_payload_difference_indices=artifacts,raw_legacy_payload_difference_indices=legacy,
    qualification='full population/source order; response/artifact differences retained, no normalization'))
 summaries={}
 for ds in ['goedel427']:
  values=[x['wall_reduction_percent'] for x in pairs if x['dataset']==ds]
  summaries[ds]=dict(complete_primary_pairs=len(values),planned_primary_pairs=3,
   mean_wall_reduction_percent=statistics.mean(values) if values else None,
   observed_range_percent=[min(values),max(values)] if values else None,
   uncertainty='Observed whole-pair range only; not a confidence interval. Profiles are separate; no paired primary result from partial data.')
 public_cells={k:{f:v for f,v in cell.items() if f not in ['basic_rows','native_rows','legacy_rows']} for k,cell in cells.items()}
 result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reference=reference,candidate=candidate,
  completed_terminal_cells=len(cells),planned_cells=8,all_planned_complete=len(cells)==8 and all(x['valid_complete'] for x in cells.values()),
  cells=public_cells,primary_pairs=pairs,dataset_summaries=summaries,
  scope='Modern full-source HTTP verification uses four requests in flight and full released proofs/errors; author statuses are migration metadata, not a full generator trace. Overlapping request durations must not be summed as whole wall decomposition. Whole HTTP source verification includes input persistence/import/libraryload/startup/replacement/raw/logging/normalshutdown/EOF. Candidate clocks exclude softwarebuild and ZIP-afterclock. Request latency is closed-loop service response, not offered-load/queueing. Shared-background CPU/memory/disk/otherGPU owners remain.')
 (out/'native-oracle-complete-cells-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
 lines=['# Completed-cell result analysis','',result['scope'],'',f"Completed terminal cells: {len(cells)}/8. Only full returned populations enter pairs; current partial cells are excluded.",'',
 '| Dataset | Pair | Reference s | Candidate s | Wall reduction | Basic differences | Native payload differences |',
 '|---|---:|---:|---:|---:|---:|---:|']
 for x in pairs:
  lines.append(f"|{x['dataset']}|{x['rep']}|{x['reference_seconds']:.6f}|{x['candidate_seconds']:.6f}|{x['wall_reduction_percent']:.3f}%|{len(x['basic_differences'])}|{len(x['native_payload_difference_indices'])}|")
 if not pairs:lines+=['','No complete primary pair yet; no speedup conclusion.']
 lines+=['','Profile PSS is sampled from observed descendants with observer overhead; CPU figures are getrusage-based counter observations with exhaustive descendant coverage unestablished, not validated whole-tree CPU work. Neither establishes exclusive hardware or a replicated resource effect.',
  'Native fields exclude only the legacy adapter-inserted duration, proven by pinned backward.py. Raw duration/JSON remain retained; operational errors and internal IDs are not normalized. Matched basic outcomes alone do not establish artifact identity.',
  'Full-cohort data and their repetitions remain required before final result review, paper updates or RQ claims.']
 (out/'native-oracle-complete-cells-analysis.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({k:result[k] for k in ['completed_terminal_cells','all_planned_complete','dataset_summaries']},indent=2))
if __name__=='__main__':main()
