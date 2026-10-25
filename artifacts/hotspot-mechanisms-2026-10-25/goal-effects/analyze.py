"""Map the guarded local prototype to every retained original timeout source.

Static applicability is not a runtime witness,global failure or latency saving.
"""
from pathlib import Path
import collections,gzip,json
a=Path(__file__).resolve().parent
r=a.parents[2]
parsed=json.loads((a/'compile-002/sites.json').read_text())
source=json.loads(gzip.decompress((r/'artifacts/hotspot-mechanisms-2026-10-25/native-sites/inputs.json.gz').read_bytes()))
codes={x['id']:x for x in source}
AND='Lean.Parser.Tactic.«tactic_<;>_»'
def tokens(n):
    if n['atom']is not None:return [(False,n['atom'])]
    if n['identifier']is not None:return [(True,n['identifier'])]
    return sum((tokens(x)for x in n['children']),[])
def interval(n):
    return n['kind']=='Mathlib.Tactic.intervalCases'and len(tokens(n))==2 and tokens(n)[0]==(False,'interval_cases')and tokens(n)[1][0]
def tree(n):
    c=n['children']
    return interval(n)or(n['kind']==AND and len(c)==3 and tree(c[0])and tree(c[2]))
def omega(n):return n['kind']=='Lean.Parser.Tactic.omega'and tokens(n)==[(False,'omega')]
def close(n):
    c=n['children']
    return omega(n)or(n['kind']==AND and len(c)==3 and tree(c[0])and omega(c[2]))
def exact(n):
    t=tokens(n)
    return n['kind']=='Lean.Parser.Tactic.exact'and len(t)==2 and t[0]==(False,'exact')and t[1][0]
def steps(n):
    while n['kind']in ['Lean.Parser.Term.byTactic','Lean.Parser.Tactic.tacticSeq',
        'Lean.Parser.Tactic.tacticSeq1Indented']:
        c=n['children'];n=c[1]if n['kind']=='Lean.Parser.Term.byTactic'else c[0]
    if n['kind']!='null':return None
    c=n['children']
    if len(c)%2!=1:return None
    return c[::2]
def bodies(n,path=()):
    if n['kind']=='Lean.Parser.Term.byTactic':yield n,path
    for index,c in enumerate(n['children']):yield from bodies(c,path+(n['kind']+':'+str(index),))
rows=[]
for row in parsed:
    if codes[row['id']]['hotspot_group']=='control':continue
    assert not row['parse_errors']
    found=[];closers=[];body_count=0
    for root in row['proof_bodies']:
        for body,path in bodies(root):
            body_count+=1;seq=steps(body)
            if not seq:continue
            for index,n in enumerate(seq):
                if close(n):closers.append(dict(byte=n['start_byte'],is_last=index==len(seq)-1))
            if len(seq)>=2 and close(seq[-2])and exact(seq[-1]):
                found.append(dict(body_start=body['start_byte'],body_end=body['end_byte'],
                    close_start=seq[-2]['start_byte'],exact_start=seq[-1]['start_byte'],
                    enclosing_path=path,
                    note='static pair only;actual one-goal/native-handler guard required'))
    rows.append(dict(id=row['id'],group=codes[row['id']]['hotspot_group'],
        proof_bodies=body_count,structural_pairs=found,native_closing_chains=closers,
        disposition='runtime_guard_pending'if found else'unknown_under_this_rule',
        certified_global_failure=False))
counts=collections.defaultdict(collections.Counter)
for x in rows:
    c=counts[x['group']];c['sources']+=1;c['static_pair_sources']+=bool(x['structural_pairs'])
    c['static_pairs']+=len(x['structural_pairs'])
    c['sources_with_native_closer']+=bool(x['native_closing_chains'])
report=dict(sources=len(rows),groups={k:dict(v)for k,v in counts.items()},
    static_pair_ids=[x['id']for x in rows if x['structural_pairs']],
    certified_global_failures=0,native_original_proof_executions=0,
    scope='actual native syntax;local pair applicability only;no forced rejection')
(a/'cohort-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
(a/'per-source.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report))
