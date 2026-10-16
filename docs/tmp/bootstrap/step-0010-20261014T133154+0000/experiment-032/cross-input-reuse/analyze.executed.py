"""Reanalyze the same complete closed LP trace: exact source-body association and reuse separation.
No verifier, cache, GPU or service is run or changed.
"""
from pathlib import Path
import collections,datetime,gzip,importlib.util,json,resource,sys,time,zipfile
sys.set_int_max_str_digits(0)
R=Path('/workspaces/repository')
E=R/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-032'
OUT=Path(__file__).resolve().parent
OLD=json.loads((E/'fast-reference-oracle-reuse-full-integers.json').read_text())
INPUT=Path(OLD['input_source'])
SPLIT=Path('/tmp/gpu-smt-kimina-header-repair-20261014/server/split.py')
spec=importlib.util.spec_from_file_location('recorded_service_split',SPLIT)
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
originals=[json.loads(line) for line in INPUT.read_text().splitlines() if line.strip()]
bodies=collections.defaultdict(list)
for item in originals:bodies[module.split_snippet(item['code']).body].append(item['index'])
prior_sources=[json.loads(line) for line in gzip.open(E/'fast-reference-oracle-reuse-full-integers-sources.jsonl.gz','rt')]
events=[json.loads(line) for line in gzip.open(E/'fast-reference-oracle-reuse-full-integers-queries.jsonl.gz','rt')]
source_ids={};mapping=[];malformed=[];lp_count=0;lines=0;bytes_read=0
with zipfile.ZipFile(OLD['archive']) as z:
 with z.open(OLD['member']) as f:
  for raw in f:
   lines+=1;bytes_read+=len(raw)
   try:row=json.loads(raw)
   except (ValueError,UnicodeDecodeError) as exc:
    malformed.append({'line':lines,'error_type':type(exc).__name__,'error':str(exc)[:240]});continue
   if not isinstance(row,dict) or 'lp' not in row:continue
   lp_count+=1;source=row.get('source')
   if not isinstance(source,str):continue
   if source not in source_ids:
    sid=len(mapping);source_ids[source]=sid
    matches=bodies.get(source,[])
    assert prior_sources[sid]['source_id']==sid and prior_sources[sid]['characters']==len(source)
    mapping.append({'source_id':sid,'source_characters':len(source),'exact_native_body_input_indices':matches,'unique_original_input_index':matches[0] if len(matches)==1 else None})
assert lp_count==len(events)==OLD['lp_queries']
assert lines==OLD['trace_lines'] and bytes_read==OLD['processed_log_bytes']
assert len(mapping)==len(prior_sources)
assert [x['line'] for x in malformed]==[x['line'] for x in OLD['malformed_rows']]
with gzip.open(OUT/'source-map.jsonl.gz','wt') as f:
 for item in mapping:f.write(json.dumps(item)+'\n')
earliest={}
for event in events:
 sid=event['source_id']
 idx=mapping[sid]['unique_original_input_index'] if sid>=0 else None
 if idx is None or event['outcome']!='successful' or event['start_ns'] is None:continue
 key=(event['group_id'],idx);end=event['start_ns']+event['elapsed_ns']
 earliest[key]=min(earliest.get(key,end),end)
group_first=collections.defaultdict(list)
for (gid,idx),end in earliest.items():group_first[gid].append((end,idx))
for gid in group_first:group_first[gid]=sorted(group_first[gid])[:2]
parts=collections.defaultdict(lambda:{'calls':0,'sum_logged_call_elapsed_ns':0})
groups=collections.defaultdict(set);qualified=0
with gzip.open(OUT/'qualified-query-rows.jsonl.gz','wt') as f:
 for event in events:
  sid=event['source_id'];idx=mapping[sid]['unique_original_input_index'] if sid>=0 else None
  category='unqualified'
  same=False;other=False
  if idx is not None and event['outcome']=='successful' and event['start_ns'] is not None:
   qualified+=1;gid=event['group_id'];started=event['start_ns']
   same=earliest[(gid,idx)]<started
   choices=group_first[gid]
   prior=next((end for end,source in choices if source!=idx),None)
   other=prior is not None and prior<started
   category='both_prior' if same and other else 'cross_input_only' if other else 'same_input_only' if same else 'no_prior_success'
  elif event['outcome']!='successful':category='non_success'
  parts[category]['calls']+=1
  if event['elapsed_ns'] is not None:parts[category]['sum_logged_call_elapsed_ns']+=event['elapsed_ns']
  if idx is not None:groups[event['group_id']].add(idx)
  f.write(json.dumps({**event,'original_input_index':idx,'prior_success_same_input':same,'prior_success_other_input':other,'category':category})+'\n')
all_ns=sum(e['elapsed_ns'] or 0 for e in events)
assert sum(p['calls'] for p in parts.values())==len(events)
assert sum(p['sum_logged_call_elapsed_ns'] for p in parts.values())==all_ns==OLD['sum_logged_oracle_elapsed_ns']
for p in parts.values():p['fraction_of_parsed_logged_call_wall_sum']=p['sum_logged_call_elapsed_ns']/all_ns
profile=Path(OLD['archive']).with_suffix('.terminal.json')
terminal=json.loads(profile.read_text()) if profile.exists() else None
ratio=None
if terminal and terminal.get('whole_seconds'):
 ratio={key:part['sum_logged_call_elapsed_ns']/1e9/terminal['whole_seconds'] for key,part in parts.items()}
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'start_utc':utc,'role':'existing-data source association and decision screening, not executed cache/GPU/verifier experiment','original_prior_analysis':str(E/'fast-reference-oracle-reuse-full-integers.json'),'archive':OLD['archive'],'member':OLD['member'],'source_input':str(INPUT),'actual_splitter':str(SPLIT),'mapping_rule':'Exact equality of logged source and actual service split_snippet(original.code).body; no trimming, fuzzy match or source filtering. The current copied splitter is not proven immutable at capture time, but complete byte equality supplies the association. Duplicate input bodies remain ambiguous.','source_texts':len(mapping),'uniquely_mapped_source_texts':sum(m['unique_original_input_index'] is not None for m in mapping),'ambiguous_source_texts':sum(len(m['exact_native_body_input_indices'])>1 for m in mapping),'unmapped_source_texts':sum(not m['exact_native_body_input_indices'] for m in mapping),'lp_rows':len(events),'qualified_successful_timed_rows':qualified,'parsed_log_bytes':bytes_read,'parsed_log_lines':lines,'malformed_rows':malformed,'parts':dict(parts),'lp_groups_spanning_distinct_original_inputs':sum(len(v)>1 for v in groups.values()),'original_profile_terminal':str(profile) if terminal else None,'original_profile_whole_seconds':terminal.get('whole_seconds') if terminal else None,'logged_interval_sum_divided_by_profile_whole_seconds':ratio,'elapsed_analysis_seconds':time.monotonic()-start,'analysis_cpu_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,'limits':'Strict prior-ended-before-start timestamp predicate only, not actual cache availability/hit, publish delay, certificate compatibility or savings. Intervals overlap; interval sums and ratios are not CPU fractions, removable critical path or strict Amdahl bounds. Same-input means original input ID, not solver invocation; a hypothetical same-input cache is an optimistic comparison, not measured existing cache coverage. Other methods and RQs are not pooled.'}
(OUT/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
