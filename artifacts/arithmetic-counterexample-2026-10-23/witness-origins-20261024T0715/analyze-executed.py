"""Exact/source interpretation of the existing13witnesses; no Lean/GPU run."""
from pathlib import Path
from fractions import Fraction as Q
import collections,csv,gzip,json,math,re,runpy
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
OUT=Path(__file__).parent
coverage=json.loads((A/'coverage-snapshot-20261024T0543/partial-coverage.json').read_text())
witnesses=coverage['witnesses'];wanted={x['source_id']for x in witnesses}
with gzip.open(R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz','rt')as stream:
 originals={'minif2f-'+str(x['index']):x for x in map(json.loads,stream)if 'minif2f-'+str(x['index'])in wanted}
with(A/'failure-entry-costs-20261024T0602/response-entry-costs.csv').open()as stream:
 costs={x['source_id']:x for x in csv.DictReader(stream)}
verify=runpy.run_path(str(R/'bench/lean-counterexample/worker.py'))['verify']
sites={
 'minif2f-379':'wrong auxiliary equality x = 25*z/14',
 'minif2f-802':'wrong auxiliary equality b = 2',
 'minif2f-812':'wrong auxiliary equality a = 3',
 'minif2f-813':'nested wrong auxiliary equality a = 2',
 'minif2f-814':'wrong auxiliary equality b = 6',
 'minif2f-815':'wrong auxiliary equality a = 2',
 'minif2f-938':'unnecessarily strict bound after apply le_of_lt',
 'minif2f-2323':'lower-bound obligations or final goal after simp drops square/cube relations',
 'minif2f-2982':'wrong auxiliary equality a = 3',
 'minif2f-2988':'wrong auxiliary equality a = 5',
 'minif2f-2993':'wrong auxiliary equality a = 3',
}
rows=[]
for w in witnesses:
 sid=w['source_id'];ast=w['ast'];point=[Q(int(n),int(d))for n,d in w['witness']['point']]
 assert verify(ast,point)
 names=[x['name']for x in ast['variables']]
 assert len(set(names))==len(names)
 values=dict(zip(names,point));code=originals[sid]['code']
 theorem=re.search(r'\btheorem\s+(\S+)',code).group(1)
 if theorem=='mathd_algebra_33':
  x,y,z=(values[n]for n in ['x','y','z'])
  assumptions=x!=0 and 2*x==5*y and 7*y==10*z
  conclusion=z/x==Q(7,25)
  detail='x='+str(x)+',y='+str(y)+',z='+str(z)+'; original z/x='+str(z/x)
  kind='wrong_auxiliary_equality'
 elif theorem=='mathd_numbertheory_430':
  a,b,c=(values[n]for n in ['a','b','c'])
  assert all(x.denominator==1 and x>=0 for x in [a,b,c])
  assumptions=all(1<=x<=9 for x in [a,b,c])and len({a,b,c})==3 and a+b==c and max(Q(0),11*a-b)==2*c and c*b==12*a
  conclusion=a+b+c==8
  detail='a='+str(a)+',b='+str(b)+',c='+str(c)+'; original sum='+str(a+b+c)
  kind='wrong_auxiliary_equality'
 elif theorem=='mathd_algebra_137':
  x=values['x'];assert x.denominator==1 and x>=0
  assumptions=x+Q(4,100)*x==598;conclusion=x==575
  detail='x='+str(x)+'; original enrollment equation and x=575 hold'
  kind='unnecessarily_strict_bound'
 elif theorem=='amc12b_2002_p7':
  a=values['a'];b=values.get('b',a+1);c=values.get('c',b+1)
  assert all(x.denominator==1 and x>=0 for x in [a,b,c])
  assumptions=a>0 and b>0 and c>0 and b==a+1 and c==b+1 and a*b*c==8*(a+b+c)
  conclusion=a*a+b*b+c*c==77
  detail='a='+str(a)+',b='+str(b)+',c='+str(c)+'; original sum of squares='+str(a*a+b*b+c*c)
  kind='wrong_auxiliary_equality'
 elif theorem=='mathd_numbertheory_5':
  n=values['n'];assert n.denominator==1 and n>=0
  # Every retained n here is not a perfect square, so the original existential
  # conjunction is false without guessing an existential cube witness.
  square=math.isqrt(n.numerator);assert square*square!=n
  assumptions=False;conclusion=n>=64
  detail='n='+str(n)+'; isqrt(n)^2='+str(square*square)+'; original square-existence premise fails'
  kind='original_conclusion_with_weakened_context'if ast['goal']==['le',['q','64','1'],['v',names.index('n')]]else'unsupported_derived_lower_bound'
 else:raise RuntimeError('Unexpected original theorem; inspect source before classifying')
 original_refuted=assumptions and not conclusion
 assert not original_refuted
 native=costs[sid];assert native['status']=='lean_error'
 rows.append(dict(source_id=sid,theorem=theorem,entry_ns=w['entry_ns'],origin=kind,site=sites[sid],
  exact_witness=[[str(x.numerator),str(x.denominator)]for x in point],variables=names,
  original_assumptions_hold=assumptions,original_conclusion_holds=conclusion,
  original_statement_refuted=original_refuted,detail=detail,
  observed_HTTP_seconds=float(native['HTTP_seconds']),observed_status=native['status']))
source_rows=[]
for sid in sorted(wanted,key=lambda x:int(x.split('-')[-1])):
 selected=[x for x in rows if x['source_id']==sid]
 source_rows.append(dict(source_id=sid,theorem=selected[0]['theorem'],witness_entries=len(selected),
  original_statement_refuted=any(x['original_statement_refuted']for x in selected),
  kinds=sorted({x['origin']for x in selected}),observed_status=selected[0]['observed_status'],
  observed_HTTP_seconds=selected[0]['observed_HTTP_seconds']))
summary=dict(scope='Complete interpretation of13already-found witnesses in a fixed partial snapshot, not a complete7808prevalence or performance result.',
 witness_entries=len(rows),witness_sources=len(source_rows),theorem_families=len({x['theorem']for x in rows}),
 source_family_counts=dict(collections.Counter(x['theorem']for x in source_rows)),
 entry_origin_counts=dict(collections.Counter(x['origin']for x in rows)),
 original_assumptions_and_conclusion_true_entries=sum(x['original_assumptions_hold']and x['original_conclusion_holds']for x in rows),
 original_assumptions_false_entries=sum(not x['original_assumptions_hold']for x in rows),
 witnesses_refuting_original_statement=sum(x['original_statement_refuted']for x in rows),
 source_HTTP_sum_seconds=sum(x['observed_HTTP_seconds']for x in source_rows),
 source_HTTP_min_seconds=min(x['observed_HTTP_seconds']for x in source_rows),
 source_HTTP_max_seconds=max(x['observed_HTTP_seconds']for x in source_rows),
 timeout_sources=0,limitations=['The classification covers only the already-detected finite-sampling positives, not all failures or all false goals.',
 'Ten checked points satisfy the original assumptions and conclusion; three fail an original existential premise. This does not prove the original theorem universally.',
 'The original statement equations are read directly from the retained source and manually encoded in this analysis; they are not a general Lean semantic parser or a native proof.',
 'No exact counterexample to a current proof obligation is a license to reject every proof of the original theorem.',
 'Per-source HTTP spans are charged once, even when a candidate has multiple witnesses. Their sum can overlap and is not avoided wall time.',
 'Some proof entries occur after Lean error recovery; native off/on acceptance and complete timing still require the planned paired run.'])
(OUT/'result.json').write_text(json.dumps(summary,indent=2)+'\n')
(OUT/'witness-origins.jsonl.gz').write_bytes(gzip.compress((''.join(json.dumps(x,separators=(',',':'))+'\n'for x in rows)).encode(),mtime=0))
(OUT/'selected-original-sources.jsonl.gz').write_bytes(gzip.compress((''.join(json.dumps(originals[sid],separators=(',',':'))+'\n'for sid in sorted(wanted))).encode(),mtime=0))
with(OUT/'sources.csv').open('w',newline='')as stream:
 writer=csv.DictWriter(stream,fieldnames=list(source_rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(source_rows)
print(json.dumps(summary,indent=2))
