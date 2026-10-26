from pathlib import Path
import json,gzip,collections,importlib.util
r=Path('/workspaces/repository')
base=r/'artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/first-stage-map'
spec=importlib.util.spec_from_file_location('prep',r/'bench/lean-failure-profile/interval-continuation/prepare-cohort.py')
prep=importlib.util.module_from_spec(spec);spec.loader.exec_module(prep)
raw=json.loads(gzip.decompress((base/'compile-parse-003/sites.json.gz').read_bytes()))
rows={x['id']:x for x in raw}
manifest=json.loads((base/'original48-preparation/preparation.json').read_text())
MAP='GpuSmt.IntervalMap.«tacticInterval_cases_map_=>_»'
def walk(n):
 yield n
 for c in n['children']:yield from walk(c)
def unparen(n):
 while n['kind']=='Lean.Parser.Tactic.paren':
  seq=prep.sequence(n['children'][1]);assert seq is not None and len(seq)==1
  n=seq[0]
 return n
totals=collections.Counter()
for m in manifest['manifest']:
 row=rows[m['id']]
 assert not row['parse_errors'] and not row['candidate_elaborated']
 ns=[n for root in row['proof_bodies']for n in walk(root)]
 assert len([n for n in ns if n['kind']==MAP])==m['interval_sites']
 assert not any(n['kind']==prep.INTERVAL for n in ns)
 edit=m['experimental_edits'][-1]
 top=[n for n in ns if n['kind']in[prep.AND,'Lean.Parser.Tactic.paren']
      and n['start_byte']==edit['changed_start'] and n['end_byte']==edit['changed_end']]
 assert len(top)==1,(m['id'],len(top))
 chain=m['chains'][0]
 stages=prep.flatten(top[0])
 assert [n['kind']for n in stages[1:]]==chain['preserved_suffix_kinds']
 first=unparen(stages[0]);terms=[]
 while first['kind']==MAP:
  terms.append(first['children'][1]['identifier'])
  seq=prep.sequence(first['children'][3]);assert seq and len(seq)==1
  first=unparen(seq[0])
 assert terms==chain['variables']
 assert first['kind']==chain['first_stage_kind']
 totals[first['kind']]+=1
receipt=dict(sources=len(rows),mapped_calls=sum(x['interval_sites']for x in manifest['manifest']),
 parse_errors=0,candidate_elaborations=0,variable_order_exact=True,
 first_stage_only_nested=True,later_stage_kinds_preserved=True,
 inverse_byte_restoration_verified_by_preparer=True,first_stage_counts=dict(totals),
 staged_suffix_sources=sum(bool(c['preserved_suffix_kinds'])for m in manifest['manifest']for c in m['chains']),
 runtime_semantic_equivalence=None,reliable_failure_coverage=None,whole_flow_speedup=None)
(base/'parser-validation.json').write_text(json.dumps(receipt,indent=2)+chr(10))
(base/'validate-structure-source.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(receipt))
