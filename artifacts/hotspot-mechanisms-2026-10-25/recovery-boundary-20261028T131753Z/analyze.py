from pathlib import Path
import gzip,json,collections

a=Path(__file__).resolve().parent
root=next(p for p in a.parents if (p/'Cargo.toml').exists())
original=root/'artifacts/hotspot-mechanisms-2026-10-25/original71-native-20261026T125951Z'
def ndjson(path):
    return [json.loads(line)for line in gzip.decompress(path.read_bytes()).splitlines()if line.strip()]
control=original/'failfast-controls6'
inputs=ndjson(control/'input.jsonl.gz')
outputs=ndjson(control/'results.jsonl.gz')
candidates=[c for batch in inputs for c in batch['candidates']]
results=[row for batch in outputs for row in batch['results']]
assert len(candidates)==len(results)==6
by_id={row['id']:row for row in results}
assert len(by_id)==6 and set(by_id)=={c['id']for c in candidates}
assert all(not row['cached']and not row['coalesced']and len(row['attempts'])==1 for row in results)
pairs=[]
for stem in ['recovery-context','ordinary-backtracking','already-failed-have']:
    left,right=by_id[stem+'-native'],by_id[stem+'-wrapped']
    pairs.append({
        'control':stem,'native_status':left['outcome']['status'],
        'wrapped_status':right['outcome']['status'],
        'native_exit_code':left['outcome']['response']['exit_code'],
        'wrapped_exit_code':right['outcome']['response']['exit_code'],
        'wrapped_error_messages':[v.get('data')for v in right['outcome']['response']['messages']if v.get('severity')=='error'],
    })
assert pairs[0]['native_status']=='accepted'and pairs[0]['wrapped_status']=='rejected'
assert 'requires recovery context'in pairs[0]['wrapped_error_messages']
assert pairs[1]['native_status']==pairs[1]['wrapped_status']=='accepted'
assert pairs[2]['native_status']==pairs[2]['wrapped_status']=='rejected'
# This is an intentionally recovery-sensitive native control, not real traffic.
source={c['id']:c['code']for c in candidates}
assert 'unless (← read).recover'in source['recovery-context-native']
assert 'failfast_native'in source['recovery-context-wrapped']
native_inputs=ndjson(original/'native71/input.jsonl.gz')
ids={c['id']for batch in native_inputs for c in batch['candidates']}
parsed=json.loads((root/'artifacts/hotspot-mechanisms-2026-10-25/native-sites/compile-005/sites.json').read_text())
rows=[v for v in parsed if v['id']in ids]
assert len(ids)==len(rows)==71 and {v['id']for v in rows}==ids
assert all(not v['parse_errors']and not v['candidate_elaborated']for v in rows)
command_rows=[{
    'id':v['id'],'command_kinds':v['command_kinds'],
    'declaration_count':v['command_kinds'].count('Lean.Parser.Command.declaration'),
    'last_command_kind':v['command_kinds'][-1],
    'theorem_ancestor_in_sites':any('Lean.Parser.Command.theorem'in s['ancestors']for s in v['sites']),
}for v in rows]
assert all(v['declaration_count']==1 and v['last_command_kind']=='Lean.Parser.Command.declaration'and v['theorem_ancestor_in_sites']for v in command_rows)
return_value={
    'scope':'offline existing native controls and source-native parse-table reuse;zero new candidate executions',
    'selected_RQ':'RQ2: Does branching from prepared native state preserve verifier responses and requested artifacts while isolating candidates and cancellation?',
    'native_controls':6,'pairs':pairs,
    'synthetic_control_not_released_workload':True,
    'generic_recovery_wrapper_transparent':False,
    'ordinary_workload_failure_rate_or_speedup':None,
    'target_originals':71,'source_native_parse_errors':0,
    'one_final_theorem_declaration':len(command_rows),
    'later_top_level_proof_declarations_after_target':0,
    'static_command_rows':command_rows,
    'top_level_scope':'For errors discovered in the final theorem,a hook only after that command cannot skip later proof declarations. This is not measured early-failure coverage or a proof about errors in the setup prefix.',
    'native_control_raw':str(control.relative_to(root)),
    'native_parser_raw':'artifacts/hotspot-mechanisms-2026-10-25/native-sites/compile-005/sites.json',
    'native71_reference':str((original/'native71').relative_to(root)),
}
if __name__=='__main__':
    print(json.dumps(return_value,ensure_ascii=False,indent=2))
