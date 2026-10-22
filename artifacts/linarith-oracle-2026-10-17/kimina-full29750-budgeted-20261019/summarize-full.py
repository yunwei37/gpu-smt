"""Root-only second reader of closed raw records, plus same-resource population strata."""
from pathlib import Path
import collections,csv,gzip,json,math
O=Path(__file__).resolve().parent
R=O.parents[2]
J=json.loads((O/'full-closed-analysis.json').read_text())
def rows(p):
    with (gzip.open(p,'rt') if p.suffix=='.gz' else p.open()) as s:
        for line in s:
            if line.strip():yield json.loads(line)
original=list(rows(O/'full/original-input.jsonl.gz'))
ids=[a['proof_id'] for a in original]
assert len(ids)==len(set(ids))==29750
selected={a['proof_id'] for a in rows(O.parent/'input-top1000.jsonl')}
assert len(selected)==1000 and selected<=set(ids)
clock={'native':0.,'power':0.}
out={'scope':'Root self-review from closed raw files and existing CSV. No new experiment, no independent audit, no GPU bound. Stratum spans overlap and are not isolated clocks.','cells':{},'pairs':{},'selected_sources':len(selected)}
changed={}
timeout_sets=[]
for rep in range(1,4):
    arm={}
    for method in ('native','power'):
        label=f'rep{rep}-{method}';d=O/'full'/label
        raw=list(rows(d/'results.jsonl.gz'))
        assert [a['proof_id'] for a in raw]==ids
        t=json.loads((d/'terminal.json').read_text())
        assert len(raw)==t['returned']==t['expected']==29750 and t['state']=='complete'
        counts=dict(collections.Counter(a['status'] for a in raw))
        assert counts==t['counts']
        assert not t['owned_live_descendants_after_shutdown']
        clock[method]+=t['whole_lifecycle_seconds']
        timeout_sets.append({a['proof_id'] for a in raw if a['status']=='timeout_error'})
        arm[method]={a['proof_id']:a for a in raw}
        out['cells'][label]={'whole_seconds':t['whole_lifecycle_seconds'],'raw_status_counts':counts,
            'peak_sampled_RSS_GiB':t['memory_watchdog']['peak_sampled_owned_rss_bytes']/2**30,
            'max_live_REPL':t['memory_watchdog']['peak_sampled_native_repl_count'],
            'kills':t['memory_watchdog']['kills'],'monitor_error':t['memory_watchdog']['error']}
    diffs=[i for i in ids if arm['native'][i]['status']!=arm['power'][i]['status']]
    assert diffs==[d['proof_id'] for d in J['pairs'][str(rep)]['native_outcome_differences']]
    for i in diffs:changed.setdefault(i,{})[str(rep)]={m:arm[m][i] for m in arm}
    paired=[]
    with (O/'full-paired-sources.csv').open() as s:
        for a in csv.DictReader(s):
            if a['pair']==str(rep):paired.append(a)
    assert len(paired)==29750
    strata={}
    groups={'original_selected_1000':lambda a:a['proof_id'] in selected,
            'remaining_28750':lambda a:a['proof_id'] not in selected,
            'all_timeout_sources':lambda a:a['native_outcome']=='timeout',
            'same_complete_sources':lambda a:a['native_outcome']==a['power_outcome']=='complete'}
    for name,pred in groups.items():
        subset=[a for a in paired if pred(a)]
        n=sum(float(a['native_HTTP_envelope_seconds']) for a in subset)
        p=sum(float(a['power_HTTP_envelope_seconds']) for a in subset)
        strata[name]={'sources':len(subset),'native_overlapping_HTTP_seconds':n,
                      'power_overlapping_HTTP_seconds':p,'ratio_of_envelope_sums':n/p if p else None}
    out['pairs'][str(rep)]={'whole_ratio':J['pairs'][str(rep)]['whole_native_over_power_observed'],
        'changed_IDs':diffs,'strata':strata,
        'tails':{q:{'sources':len(v['source_IDs']),
             'native_overlapping_HTTP_seconds':v['overlapping_envelope_sums_seconds']['native'],
             'power_overlapping_HTTP_seconds':v['overlapping_envelope_sums_seconds']['power'],
             'ratio':v['overlapping_envelope_sums_seconds']['native']/v['overlapping_envelope_sums_seconds']['power']}
             for q,v in J['pairs'][str(rep)]['matched_native_ranked_HTTP_tails'].items()}}
assert all(x==timeout_sets[0] for x in timeout_sets)
out['identical_timeout_IDs_all_six_cells']=sorted(timeout_sets[0])
out['whole_clock_sums']=clock
out['ratio_of_whole_sums']=clock['native']/clock['power']
assert math.isclose(out['ratio_of_whole_sums'],J['whole_ratio_of_complete_sums_observed'],rel_tol=1e-14)
out['elapsed_reduction_percent']=100*(1-clock['power']/clock['native'])
out['persistent_HTTP_regression_sources']=len(J['Power_HTTP_regression_IDs_in_all_three_pairs'])
out['all_rows']=6*29750
(O/'full-root-recomputation.json').write_text(json.dumps(out,indent=2)+'\n')
e={'scope':'Actual original released source plus returned diagnostics, all three observations. Rejection-to-completion is a tactic coverage change, not transparent outcome equivalence or a proved new theorem/solver algorithm.',
   'sources':[a for a in original if a['proof_id'] in changed],'raw_records':changed}
(O/'outcome-change-evidence.json').write_text(json.dumps(e,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,indent=2))
