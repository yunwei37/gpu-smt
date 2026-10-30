#!/usr/bin/env python3
"""Offline full EPFL evaluation characterization; no candidate generation or Lean calls."""
import argparse, collections, csv, json, pathlib, resource, sys, time
import pyarrow.parquet as pq
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'openai-math'))
from scan import masks, TOKENS
from inventory import write_csv
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--parquet',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    groups=collections.defaultdict(collections.Counter);errors=collections.Counter();tactics=collections.defaultdict(collections.Counter);rows=0;lexical_failures=0
    for batch in pq.ParquetFile(a.parquet).iter_batches(batch_size=512):
        for row in batch.to_pylist():
            rows+=1;benchmark=row['benchmark'];status=row['status'];model=row['prover_model'];version=row['lean_version']
            groups[(benchmark,model,version)].update({"programs":1,"valid":int(row['label']==1),"invalid":int(row['label']!=1),status:1,"source_bytes":len(row['source'].encode())})
            if row.get('error_kind'):errors[(benchmark,model,row['error_kind'])]+=1
            try:_,code=masks(row['source'])
            except ValueError:lexical_failures+=1;continue
            import re
            for token in TOKENS:
                n=len(re.findall(r'(?<![\w\'])'+token+r'(?![\w\'])',code))
                tactics[(benchmark,model,token)].update({"program_occurrences":int(n>0),"lexical_occurrences":n,"invalid_program_occurrences":int(n>0 and row['label']!=1)})
    group_rows=[{"benchmark":k[0],"prover_model":k[1],"lean_version":k[2],**dict(v)} for k,v in sorted(groups.items())]
    # Counter keys vary by group; serialize an explicit complete column list.
    columns=sorted(set().union(*(x.keys() for x in group_rows)))
    with (a.out/'verdicts.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(group_rows)
    write_csv(a.out/'error-kinds.csv',[{"benchmark":b,"prover_model":m,"error_kind":e,"programs":n} for (b,m,e),n in sorted(errors.items())])
    write_csv(a.out/'tactic-occurrences.csv',[{"benchmark":b,"prover_model":m,"tactic":t,**dict(v)} for (b,m,t),v in sorted(tactics.items())])
    result={"dataset":"EPFL-LARA/lean-evaluation-benchmark","revision":"0bbf31331bd1c726f539b311cce8b058a821f15c","programs_read":rows,
            "valid":sum(x['valid'] for x in group_rows),"invalid":sum(x['invalid'] for x in group_rows),"lexical_failures":lexical_failures,
            "versions":sorted({x['lean_version'] for x in group_rows}),"elapsed_s":time.monotonic()-start,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "no_native_processes":True,"native_budget_exceeded_count":None,"native_time_by_cause":None,"tail_concentration_1_6_percent":None,
            "limitations":["Reference labels include expected-theorem/forbidden-construct policy, not elaboration alone.",
                           "Publisher excludes timeouts, infrastructure exceptions, not_run and precheck failures; this is censored for tail-cost studies.",
                           "No original native timings or peak RSS columns; cannot test 1.6%/73% claim or assign causal over-budget time.",
                           "Tactic identifiers outside comments/strings are lexical occurrences, not executed call counts.",
                           "No explicit dataset license is present in the pinned README/card; do not infer a source-data license from related code."]}
    assert rows==68932 and result['valid']==28145 and result['invalid']==40787
    (a.out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
