#!/usr/bin/env python3
"""Syntactic reuse across distinct captured Verus tasks in recorded run order.

No SAT equivalence or speedup is inferred. Project grouping is a trace-order
simulation; it does not rerun the verifier or model a production arrival stream.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from analyze_smt_trace import snapshot_queries, query_context, digest_query, lcp_len, distribution


def analyze(queries, window):
    seen = {}
    rows = []
    for i, q in enumerate(queries):
        previous = queries[max(0, i-window):i]
        eligible = [p for p in previous if p['task_id'] != q['task_id']]
        best_prefix = best_bytes = best_common = 0
        prefix_source = byte_source = None
        for p in eligible:
            prefix = lcp_len(q['context'], p['context'])
            common = q['counter'] & p['counter']
            shared_bytes = sum(q['sizes'][c]*n for c,n in common.items())
            if prefix > best_prefix:
                best_prefix, prefix_source = prefix, p['identity']
            if shared_bytes > best_bytes:
                best_bytes, byte_source = shared_bytes, p['identity']
            best_common = max(best_common, sum(common.values()))
        cross_exact = any(t != q['task_id'] for t in seen.get(q['digest'], set()))
        seen.setdefault(q['digest'], set()).add(q['task_id'])
        rows.append(dict(query=q['identity'], task_id=q['task_id'], project=q['project'],
                         eligible_previous_queries=len(eligible), cross_task_exact_ever=cross_exact,
                         context_commands=len(q['context']), context_bytes=q['bytes'],
                         prefix_commands=best_prefix,
                         prefix_fraction=best_prefix/max(1,len(q['context'])),
                         prefix_bytes=sum(q['sizes'][c] for c in q['context'][:best_prefix]),
                         prefix_source=prefix_source,
                         common_fraction=best_common/max(1,len(q['context'])),
                         common_bytes_fraction=best_bytes/max(1,q['bytes']), byte_source=byte_source))
    comparable = [r for r in rows if r['eligible_previous_queries']]
    return dict(window_queries=window, queries=len(rows), comparable_queries=len(comparable),
                exact_cross_task_hits=sum(r['cross_task_exact_ever'] for r in rows),
                comparable_distributions={k:distribution([r[k] for r in comparable]) for k in
                    ('prefix_commands','prefix_fraction','common_fraction','common_bytes_fraction')},
                total_context_bytes=sum(r['context_bytes'] for r in rows),
                total_shareable_prefix_bytes=sum(r['prefix_bytes'] for r in rows), rows=rows)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run_dir',type=Path); ap.add_argument('--json',type=Path,required=True)
    ap.add_argument('--windows',default='16,64,256')
    args=ap.parse_args()
    runs=[json.loads(l) for l in (args.run_dir/'runs.jsonl').read_text().splitlines()]
    queries=[]; files=[]; by_project={}; coverage=[]
    for run in runs:
        task=run['task_id']; project=run['project']; by_project.setdefault(project,[]).append(run)
        stdout=(args.run_dir/'logs'/f'{task}.stdout.txt').read_text()
        stderr=(args.run_dir/'logs'/f'{task}.stderr.txt').read_text()
        reports=re.findall(r'verification results:: (\d+) verified, (\d+) errors',stdout)
        error_codes=Counter(re.findall(r'error(?:\[([^\]]+)\])?:',stderr))
        coverage.append(dict(**run, verification_reports=reports,error_codes=dict(error_codes)))
        for path in sorted((args.run_dir/'traces'/task).glob('*.smt2')):
            files.append(dict(path=str(path.relative_to(args.run_dir)), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size))
            for index,query in enumerate(snapshot_queries(path)):
                # Intern exact normalized command identities as hashes to avoid
                # comparing/copying megabyte strings for every candidate pair.
                text=query_context(query)
                hashes=[hashlib.sha256(c.encode()).hexdigest() for c in text]
                sizes={h:len(c.encode('utf-8'))+1 for h,c in zip(hashes,text)}
                identity=f'{task}/{path.name}#{index}'
                queries.append(dict(task_id=task,project=project,identity=identity,context=hashes,
                                    counter=Counter(hashes),sizes=sizes,bytes=sum(sizes[h] for h in hashes),digest=digest_query(query)))
    orders={'observed_mixed':queries, 'project_grouped_simulation':sorted(queries,key=lambda q:q['project'])}
    result=dict(scope='exact normalized syntax, distinct task_id only; no semantic equivalence or measured speedup',
                run_order=[r['task_id'] for r in runs], tasks=len(runs),
                passed=sum(r['returncode']==0 for r in runs),
                failures_without_smt=sum(r['returncode']!=0 and not r['z3_sessions'] for r in runs),
                failures_with_smt=sum(r['returncode']!=0 and bool(r['z3_sessions']) for r in runs),
                tasks_with_smt=sum(bool(r['z3_sessions']) for r in runs),sessions=len(files),queries=len(queries),
                trace_bytes=sum(f['bytes'] for f in files),coverage=coverage,files=files,
                project_coverage={p:dict(tasks=len(rs),passed=sum(r['returncode']==0 for r in rs),with_smt=sum(bool(r['z3_sessions']) for r in rs)) for p,rs in by_project.items()},
                analyses={order:{str(w):analyze(qs,w) for w in map(int,args.windows.split(','))} for order,qs in orders.items()})
    args.json.write_text(json.dumps(result,indent=1)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('coverage','files','analyses','run_order')},indent=1))


if __name__=='__main__': main()
