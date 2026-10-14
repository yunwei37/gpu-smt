"""Read-only native diagnostics aggregation; outputs are observations, not gate state."""
import collections,hashlib,json,re,sys
from pathlib import Path
root=Path(__file__).resolve().parent
run=root/'full-proofnet'
repo=Path('/workspaces/repository')
codes=json.loads((repo/'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs/proofnet/codes.json').read_text())
baseline=json.loads((repo/'artifacts/lean-gpu-checking-2026-10-13/experiment022/full4-proofnet/proofnet-rep0-warm.analysis.json').read_text())['basic_rows']
observed=collections.Counter();names=collections.defaultdict(set);unique_names=collections.defaultdict(set);reported=collections.Counter()
coverage=[];differences=[];errors=[];missing=[];seen_code=set()
for index in range(len(codes)):
    folder=run/f'request-{index:08d}'
    p=folder/'result.json'
    if not p.exists():missing.append(index);continue
    result=json.loads(p.read_text())
    digest=hashlib.sha256(codes[index]['code'].encode()).hexdigest()
    unique=digest not in seen_code;seen_code.add(digest)
    outcome='system_error'
    messages=[]
    if result['status']=='response':
        try:
            response=json.loads((folder/'response.bin').read_bytes())
            messages=response.get('messages',[])
            outcome='rejected' if any(x.get('severity')=='error' for x in messages) else 'incomplete' if response.get('sorries') else 'complete'
        except Exception as exc:errors.append({'index':index,'error':repr(exc)})
    observed[outcome]+=1
    if outcome!=baseline[str(index)]:differences.append({'index':index,'native':baseline[str(index)],'diagnostic':outcome})
    entries=0;sections=collections.Counter()
    for message in messages:
        text=message.get('data','')
        if 'control threshold for reporting counters' not in text:continue
        current=None
        for line in text.splitlines():
            marker=re.match(r'^\s*\[(reduction|type_class|def_eq|kernel)\]\s*(.*)',line)
            if marker:
                current=marker.group(1)+':'+marker.group(2).split('(max:')[0].strip()
                continue
            pair=re.match(r'^\s*(.+?)\s*↦\s*(\d+)',line)
            if pair and current:
                label=current+' | '+pair.group(1).strip()
                count=int(pair.group(2));entries+=1;sections[current]+=1
                reported[label]+=count;names[label].add(index)
                if unique:unique_names[label].add(digest)
    coverage.append({'index':index,'outcome':outcome,'distinct_source_bytes':unique,'reported_entries':entries,'sections':dict(sections)})
events=[json.loads(line) for line in (run/'events.jsonl').open()]
shutdown=[e for e in events if e['event']=='shutdown']
replacements=[e for e in events if e['event']=='replacement']
report={'expected':len(codes),'returned':len(coverage),'missing':missing,'outcomes':dict(observed),'native_outcome_differences':differences,'parse_errors':errors,'shutdown':shutdown[-1] if shutdown else None,'process_replacements':replacements,'complete_acquisition':not missing and bool(shutdown),'diagnostic_sources':sum(x['reported_entries']>0 for x in coverage),'unique_source_bytes':len(seen_code),'name_coverage':[{'displayed_name':n,'sources_with_report':len(ids),'distinct_sources_with_report':len(unique_names[n]),'sum_reported_counts':reported[n]} for n,ids in sorted(names.items(),key=lambda x:-len(x[1]))],'coverage':coverage,'limitations':['Native reporting threshold retained; low-frequency counters censored','displayed names are prettyprinted and may alias; not canonical declaration IDs','diagnostics can be reused with unchanged native snapshots; sum_reported_counts is not actual work','source coverage and distinct-byte coverage do not prove exclusive cost, GPU eligibility, cache safety or speedup','no instrumentation timing is compared with native6 primary wall times','negative, operational and absent diagnostics remain visible']}
(root/'full-proofnet-diagnostic-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['expected','returned','complete_acquisition','outcomes','diagnostic_sources','unique_source_bytes']}))
print('basic differences',len(differences),'top',report['name_coverage'][:8])
