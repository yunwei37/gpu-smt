"""Analyze only completed native heavy-cohort cells. Pending is never failure or success."""
from pathlib import Path
import argparse, gzip, json
def read(path):
    with gzip.open(path,'rt') as f:return [json.loads(l) for l in f]
def cell(path):
    if not (path/'terminal.json').exists():return None
    t=json.loads((path/'terminal.json').read_text())
    rows=read(path/'responses.jsonl.gz')
    return {'path':str(path),'terminal':t,'rows':{x['proof_id']:x for x in rows},
            'complete':t['state']=='complete' and len(rows)==t['expected']}
def compare(reference,candidate):
    common=reference['rows'].keys()&candidate['rows'].keys()
    whole=reference['complete'] and candidate['complete']
    native=whole and all(x['response'] is not None and not x['operational_error'] for c in [reference,candidate] for x in c['rows'].values())
    return {'sources':len(common),'complete':whole,'all_native_responses_observed':native,
      'baseline_over_oracle_whole_ratio':reference['terminal']['whole_ns']/candidate['terminal']['whole_ns'] if whole else None,
      'verdict_differences':[i for i in common if reference['rows'][i]['outcome']!=candidate['rows'][i]['outcome']],
      'full_response_differences':[i for i in common if reference['rows'][i]['response']!=candidate['rows'][i]['response']]}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run',type=Path);a=p.parse_args()
    result={'primary_pairs':[],'conditional_controls':[]};times={'oracle':0,'fast-hybrid':0}
    refs={};oracles={}
    for i in [1,2,3]:
        root=a.run/('primary%d'%i)
        ref=cell(root/'rep1-fast-hybrid');candidate=cell(root/'rep1-oracle')
        if not ref or not candidate:continue
        c=compare(ref,candidate);result['primary_pairs'].append({'repetition':i,**c})
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
                c=compare(ref,oracles[i]);controls_complete &= c['complete']
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
       'scope':'enriched1000-source cohort; report every repetition; phase diagnostics and root self-review still required. None=pending. No GPU work or general-impossibility inference.'}
    (a.run/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['interpretation'],indent=2))
if __name__=='__main__':main()
