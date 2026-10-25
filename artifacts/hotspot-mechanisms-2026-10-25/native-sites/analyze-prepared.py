"""Validate retained exact native syntax and source-edit mappings; no Lean run."""
from pathlib import Path
import json
a=Path(__file__).resolve().parent
items=json.loads((a/'compile-008/sites.json').read_text())
manifest=json.loads((a/'prepared-simp23/preparation.json').read_text())['manifest']
byid={x['id']:x for x in manifest}
count=0
for x in items:
    assert not x['parse_errors'],x
    source=byid[x['id'].split('/',1)[1]]
    wrappers=[s for s in x['sites']if s['kind']=='gpuSmtProfileSimpAll']
    inner=[s for s in x['sites']if s['kind']=='Lean.Parser.Tactic.simpAll']
    assert len(wrappers)==len(inner)==source['original_sites']
    assert all(s['inner_kind']=='Lean.Parser.Tactic.simpAll'for s in wrappers)
    assert sorted(s['start_byte']for s in inner)==sorted(
        s['instrumented_keyword_byte']for s in source['sites'])
    assert sorted(s['start_byte']for s in wrappers)==sorted(
        s['instrumented_wrapper_byte']for s in source['sites'])
    count+=len(wrappers)
print(json.dumps(dict(files=len(items),profile_wrappers=count,
    all_native_simpAll_inner=True,all_byte_mappings_match=True)))
