"""Recorded CPU numerical-path costs; explicitly not exhaustive LP or a GPU ceiling."""
from pathlib import Path
import collections,gzip,json,math
O=Path(__file__).resolve().parent
def rows(p):
    with (gzip.open(p,'rt') if p.suffix=='.gz' else p.open()) as z:
        for l in z:
            if l.strip():yield json.loads(l)
def body(code):
    ls=code.splitlines()
    while ls and (not ls[0].strip() or ls[0].startswith('import ')):ls.pop(0)
    return '\n'.join(ls).strip()
bybody=collections.defaultdict(list)
for a in rows(O/'full/original-input.jsonl.gz'):bybody[body(a['code'])].append(a['proof_id'])
def source_id(q):
    ids=bybody.get(body(q.get('source','')),[])
    return ids[0] if len(ids)==1 else None
def dist(xs):
    xs=sorted(xs)
    def p(q):
        if not xs:return None
        k=(len(xs)-1)*q;a=math.floor(k);b=math.ceil(k)
        return xs[a] if a==b else xs[a]*(b-k)+xs[b]*(k-a)
    return dict(observed=len(xs),p50=p(.5),p90=p(.9),p99=p(.99),maximum=p(1))
out={'scope':'Existing closed Power CPU numerical records only. Native/small/cancelled/product paths are not exhaustively timed. No GPU execution, all-LP fraction, strict Amdahl bound or project closure follows. Root self-review.',
     'repetitions':{}}
for rep in range(1,4):
    d=O/'full'/f'rep{rep}-power';data=list(rows(d/'support-calls.jsonl.gz'))
    qrows=[a for a in data if isinstance(a.get('input'),dict)]
    missing=[a for a in data if not isinstance(a.get('input'),dict)]
    errors=collections.Counter(a.get('reply',{}).get('error','').split(':',1)[0] for a in missing)
    decode_ids=[a['id'] for a in missing]
    known_timers=[a['reply']['solver_seconds'] for a in data if isinstance(a.get('reply',{}).get('solver_seconds'),(int,float))]
    pending={};stages=collections.defaultdict(lambda:dict(completed=0,wall_seconds=0.,caller_thread_CPU_seconds=0.))
    retired=[];unpaired=[]
    for a in rows(d/'support-calls.jsonl.gz.phases'):
        if a.get('event')=='process_retired':retired.append(a);continue
        k=(a['pid'],a['tid'],a['id'],a['stage'])
        if a['event']=='begin':
            assert k not in pending;pending[k]=a
        elif k in pending:
            b=pending.pop(k);v=stages[a['stage']];v['completed']+=1
            v['wall_seconds']+=(a['wall_ns']-b['wall_ns'])/1e9
            v['caller_thread_CPU_seconds']+=(a['thread_cpu_ns']-b['thread_cpu_ns'])/1e9
        else:unpaired.append(a)
    events=[]
    for a in qrows:
        i=source_id(a['input'])
        events.extend([(a['start_ns'],1,a['id'],i),(a['end_ns'],-1,a['id'],i)])
    active={};overlaps=[];max_active=0
    for t,direction,k,i in sorted(events):
        if direction<0:active.pop(k,None)
        else:
            for other,src in active.items():
                overlaps.append({'left_call':other,'right_call':k,'left_source':src,'right_source':i,
                     'different_known_sources':src is not None and i is not None and src!=i})
            active[k]=i;max_active=max(max_active,len(active))
    assert not active
    terminal=json.loads((d/'terminal.json').read_text())
    out['repetitions'][str(rep)]=dict(
        whole_Power_seconds=terminal['whole_lifecycle_seconds'],
        connection_records=len(data),decoded_requests=len(qrows),input_unavailable_records=len(missing),
        input_unavailable_record_IDs=decode_ids,input_unavailable_error_kinds=dict(errors),
        known_solver_timer_records=len(known_timers),known_solver_timer_sum_seconds=sum(known_timers),
        all_connection_envelope_sum_seconds=sum((a['end_ns']-a['start_ns'])/1e9 for a in data),
        all_connection_caller_thread_CPU_seconds=sum(a['thread_cpu_ns']/1e9 for a in data),
        decoded_source_attribution_unknown_IDs=[a['id'] for a in qrows if source_id(a['input']) is None],
        LP_rows=dist([a['rows'] for a in qrows if a.get('rows') is not None]),
        LP_columns=dist([a['cols'] for a in qrows if a.get('cols') is not None]),
        LP_nonzeros=dist([a['nnz'] for a in qrows if a.get('nnz') is not None]),
        recorded_phase_totals=dict(stages),unmatched_begin_events=list(pending.values()),unmatched_end_events=unpaired,
        maximum_decoded_service_interval_overlap=max_active,decoded_interval_overlap_pairs=overlaps,
        recorded_retired_processes=retired)
(O/'full-recorded-numerical-costs.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{x:y for x,y in v.items() if x not in ('input_unavailable_record_IDs','decoded_interval_overlap_pairs','recorded_retired_processes')} for k,v in out['repetitions'].items()},indent=2))
