"""Analyze only completed native heavy-cohort cells. Pending is never failure or success."""
from pathlib import Path
import argparse, gzip, json, math
def read(path):
    with gzip.open(path,'rt') as f:return [json.loads(l) for l in f]
def percentile(values,p):
    if not values:return None
    values=sorted(values)
    return values[max(0,math.ceil(p*len(values))-1)]
def cell(path):
    if not (path/'terminal.json').exists():return None
    t=json.loads((path/'terminal.json').read_text())
    rows=read(path/'responses.jsonl.gz')
    by={x['proof_id']:x for x in rows}
    ordered_ids=[x['proof_id'] for x in rows]
    batches={}
    for row in rows:
        key=(row['worker'],row['batch_offset'])
        batches[key]=max(batches.get(key,0),row['batch_latency_ns']/1e9)
    latencies=list(batches.values())
    return {'path':str(path),'terminal':t,'rows':by,'ordered_ids':ordered_ids,
            'complete':t['state']=='complete' and len(rows)==len(by)==t['expected'],
            'summary':{
              'whole_seconds':t['whole_ns']/1e9,
              'cpu_seconds':sum(v['user']+v['system'] for v in t['cpu'].values()),
              'peak_observed_pss_bytes_with_collector':t['sampled_peak_fleet_pss_with_collector'],
              'counts':t['counts'],'workers':t['workers'],'batch_width':t['width'],
              'batches':len(batches),'offline_batch_p50_seconds':percentile(latencies,.5),
              'offline_batch_p95_seconds':percentile(latencies,.95),
              'offline_batch_max_seconds':max(latencies,default=None)}}
def compare(reference,candidate,expected_ids=None):
    common=reference['rows'].keys()&candidate['rows'].keys()
    same=reference['ordered_ids']==candidate['ordered_ids']
    expected=expected_ids is None or (reference['ordered_ids']==expected_ids and candidate['ordered_ids']==expected_ids)
    whole=reference['complete'] and candidate['complete'] and same and expected
    native=whole and all(x['response'] is not None and not x['operational_error'] for c in [reference,candidate] for x in c['rows'].values())
    return {'sources':len(common),'complete':whole,
      'same_original_source_order':same,'matches_frozen_cohort':expected,
      'all_native_responses_observed':native,
      'reference':reference['summary'],'prototype':candidate['summary'],
      'baseline_over_oracle_whole_ratio':reference['terminal']['whole_ns']/candidate['terminal']['whole_ns'] if whole else None,
      'verdict_differences':sorted(i for i in common if reference['rows'][i]['outcome']!=candidate['rows'][i]['outcome']),
      'full_response_differences':sorted(i for i in common if reference['rows'][i]['response']!=candidate['rows'][i]['response'])}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run',type=Path);p.add_argument('--input',type=Path,default=Path('/workspaces/repository/artifacts/linarith-oracle-2026-10-17/input-top1000.jsonl'));a=p.parse_args()
    expected_ids=[json.loads(l)['proof_id'] for l in a.input.read_text().splitlines()]
    if len(expected_ids)!=len(set(expected_ids)):raise ValueError('duplicate source ids in frozen input')
    result={'primary_pairs':[],'conditional_controls':[]};times={'oracle':0,'fast-hybrid':0}
    refs={};oracles={}
    for i in [1,2,3]:
        root=a.run/('primary%d'%i)
        ref=cell(root/'rep1-fast-hybrid');candidate=cell(root/'rep1-oracle')
        if not ref or not candidate:continue
        c=compare(ref,candidate,expected_ids);result['primary_pairs'].append({'repetition':i,**c})
        if c['complete']:
            times['oracle']+=candidate['terminal']['whole_ns'];times['fast-hybrid']+=ref['terminal']['whole_ns']
        refs[i]=ref;oracles[i]=candidate
    complete=len(result['primary_pairs'])==3 and all(x['complete'] for x in result['primary_pairs'])
    agreement=all(x['all_native_responses_observed'] and not x['verdict_differences'] for x in result['primary_pairs']) if complete else None
    ratio=times['fast-hybrid']/times['oracle'] if complete else None
    controls_needed=complete and ratio>1.5
    controls_complete=True;control_times={}
    if controls_needed:
        for i in [1,2,3]:
            for method in ['native','fast-highs']:
                ref=cell(a.run/('controls%d'%i)/('rep1-'+method))
                if not ref:controls_complete=False;continue
                c=compare(ref,oracles[i],expected_ids);controls_complete &= c['complete']
                result['conditional_controls'].append({'repetition':i,'method':method,**c})
                if c['complete']:control_times[method]=control_times.get(method,0)+ref['terminal']['whole_ns']
        if len(result['conditional_controls'])!=6:controls_complete=False
    fastest_ratio=min([ratio]+[v/times['oracle'] for v in control_times.values()]) if complete and controls_complete else None
    decision=None
    if complete and (not controls_needed or controls_complete):
        controls_ok=all(x['all_native_responses_observed'] and not x['verdict_differences'] for x in result['conditional_controls'])
        decision=bool(fastest_ratio>1.5) if agreement and controls_ok else None
    result['interpretation']={'three_main_pairs_complete':complete,'native_verdict_agreement':agreement,
       'aggregate_fast_hybrid_over_oracle_ratio':ratio,'conditional_competitors_required':controls_needed,
       'conditional_competitors_complete':controls_complete if controls_needed else None,
       'fastest_observed_native_aggregate_ratio':fastest_ratio,'user_1_5x_rule_met':decision,
       'validity':'pending' if not complete or (controls_needed and not controls_complete) else ('valid_native_outcomes' if agreement and all(x['all_native_responses_observed'] and not x['verdict_differences'] for x in result['conditional_controls']) else 'invalid_execution_or_verdict_disagreement'),
       'frozen_sources':len(expected_ids),
       'batch_tail_scope':'Original-order offline batches, not individual proof latency or online serving SLOs. No resampling/best-run selection.',
       'scope':'enriched1000-source cohort; report every repetition; phase diagnostics and root self-review still required. None=pending. No GPU work or general-impossibility inference.'}
    (a.run/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['interpretation'],indent=2))
if __name__=='__main__':main()
