#!/usr/bin/env python3
"""Stream all four published APRIL test files; no proof generation or Lean execution."""
import argparse,collections,csv,json,pathlib,re,resource,sys,time,urllib.request
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'openai-math'))
from scan import masks,TOKENS
from inventory import write_csv
REVISION='4e3075279b4aedfb28fe435d08a8caf76272586d'
BUDGET=re.compile(r'maxHeartbeats|deterministic.*timeout|maxRecDepth',re.I)
CATEGORIES=[
 ('unknown_identifier',r'unknown identifier|unknown constant'),
 ('type_mismatch',r'type mismatch|application type mismatch'),
 ('unsolved_goals',r'unsolved goals'),
 ('tactic_failure',r'tactic .* failed|tactic failed'),
 ('budget_diagnostic',BUDGET.pattern),
 ('syntax',r'unexpected token|expected token|expected .*token|unterminated')]
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();subsets=[];errors=collections.Counter();tactics=collections.defaultdict(collections.Counter);lexical=0
    for subset in ['lme','mlme','thme','tme']:
        counts=collections.Counter()
        url=f'https://huggingface.co/datasets/uw-math-ai/APRIL/resolve/{REVISION}/test/{subset}_test.jsonl'
        with urllib.request.urlopen(url,timeout=45) as stream:
            for line in stream:
                if not line.strip():continue
                row=json.loads(line);counts['rows']+=1;error=row.get('error','') or ''
                counts['recorded_error_rows']+=int(bool(error));counts['budget_diagnostic_rows']+=int(bool(BUDGET.search(error)))
                kind=next((k for k,p in CATEGORIES if re.search(p,error,re.I)),'other_recorded_error')
                errors[(subset,kind)]+=1
                try:_,code=masks(row['incorrect_proof'])
                except ValueError:lexical+=1;continue
                for token in TOKENS:
                    n=len(re.findall(r"(?<![\w'])"+token+r"(?![\w'])",code))
                    tactics[(subset,token)].update({'program_occurrences':int(n>0),'lexical_occurrences':n})
        subsets.append({'subset':subset,**dict(counts)})
    assert sum(x['rows'] for x in subsets)==1835
    write_csv(a.out/'subsets.csv',subsets)
    write_csv(a.out/'recorded-errors.csv',[{'subset':s,'diagnostic_category':k,'records':n} for (s,k),n in sorted(errors.items())])
    write_csv(a.out/'tactics.csv',[{'subset':s,'tactic':t,**dict(v)} for (s,t),v in sorted(tactics.items())])
    summary={'dataset':'uw-math-ai/APRIL','revision':REVISION,'license':'Apache-2.0 per pinned card','subset':'four original test files only','rows_read':sum(x['rows'] for x in subsets),'lexical_errors':lexical,'native_runs':0,'lean_version':'not pinned by the inspected card','peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'elapsed_s':time.monotonic()-start,'native_time_by_cause':None,'tail_concentration_1_6_percent':None,'classification':'First matching diagnostic category; nonexclusive budget substring count is separate. These are diagnostics, not proven root causes.','selection':'Publisher-created proof mutations, not natural prover arrival streams.'}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
