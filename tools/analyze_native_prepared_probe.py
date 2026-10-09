#!/usr/bin/env python3
"""Inspect complete native responses and observed cancellation disposal."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from analyze_native_frontend_probe import observe, compare, digest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('out', type=Path)
    a = p.parse_args()
    root = a.out.resolve()
    job_list = json.loads((root / 'jobs.json').read_text())
    jobs = {j['index']: j for j in job_list}
    provenance = json.loads((root / 'provenance.json').read_text())
    rows = [json.loads(s) for s in (root / 'processes.jsonl').read_text().splitlines()]
    expected = {(r,m,i) for r in range(provenance['repetitions']) for m in provenance['modes'] for i in jobs}
    counts = Counter((r['repeat'],r['mode'],r['index']) for r in rows)
    observations, by_key = [], {}
    for row in rows:
        obs = dict(row)
        key = row['repeat'], row['mode'], row['index']
        try:
            obs.update(observe(root / row['stdout'], jobs[row['index']]))
            stderr = (root / row['stderr']).read_bytes()
            obs.update(stderr_sha256=digest(stderr), stderr_text=stderr.decode('utf8',errors='replace'))
        except (OSError, KeyError, ValueError) as exc:
            obs['analysis_error'] = str(exc)
        observations.append(obs)
        if counts[key] == 1 and 'analysis_error' not in obs:
            by_key[key] = obs
    differences = {}
    for obs in observations:
        if 'analysis_error' in obs:
            continue
        obs['comparisons'] = {}
        for ref in ('source', 'fresh', 'split', 'branch'):
            reference = by_key.get((obs['repeat'],ref,obs['index']))
            comp = compare(obs, reference)
            comp['stderr_bytes_equal'] = reference is not None and obs['stderr_sha256'] == reference['stderr_sha256']
            comp['returncode_equal'] = reference is not None and obs['returncode'] == reference['returncode']
            obs['comparisons'][ref] = comp
            if not comp.get('nonstatistics_exact_equal', False) or not comp['stderr_bytes_equal'] or not comp['returncode_equal']:
                differences.setdefault(obs['mode'] + '_vs_' + ref, []).append([obs['repeat'], obs['index']])
    cancellation_rows = [json.loads(s) for s in (root / 'cancellations.jsonl').read_text().splitlines()]
    cancellations = []
    for row in cancellation_rows:
        record = dict(row)
        path = root / row['directory'] / 'cancel.stdout'
        raw = path.read_bytes() if path.exists() else b''
        cost = row['cost']
        # SIGKILL wait status, not kill() return alone, establishes disposal.
        record.update(partial_stdout_bytes=len(raw), partial_stdout_sha256=digest(raw),
                      observed_done_markers=raw.count(b'<<DONE>>'),
                      observed_check_decisions=len(re.findall(rb'^(sat|unsat|unknown)\s*$', raw, re.M)),
                      landed=bool(cost and int(cost['done_marker']) == 1 and int(cost['kill_return']) == 0
                                  and int(cost['signal']) == 9 and int(cost['exit_code']) == -1
                                  and re.search(rb'^(sat|unsat|unknown)\s*$', raw, re.M)))
        cancellations.append(record)
    completion_path = root / 'completion.json'
    completion = json.loads(completion_path.read_text()) if completion_path.exists() else None
    summary = dict(expected_cells=len(expected), actual_cells=len(rows),
                   duplicate_jobs=[i for i,n in Counter(j['index'] for j in job_list).items() if n>1],
                   duplicate_cells=[list(k) for k,n in counts.items() if n>1],
                   missing_cells=[list(k) for k in sorted(expected-set(counts))],
                   unexpected_cells=[list(k) for k in sorted(set(counts)-expected)],
                   nonterminal_cells=[[o['repeat'],o['mode'],o['index']] for o in observations if not o['terminal']],
                   incomplete_frames=[[o['repeat'],o['mode'],o['index']] for o in observations if not o.get('complete_response_frames',False)],
                   incomplete_checks=[[o['repeat'],o['mode'],o['index']] for o in observations if not o.get('complete_checks',False)],
                   nonzero_exits=[[o['repeat'],o['mode'],o['index'],o['returncode']] for o in observations if o['returncode'] != 0],
                   differences=differences, cancellation_attempts=len(cancellations),
                   cancellation_landed=sum(r['landed'] for r in cancellations), completion=completion)
    summary['matrix_complete'] = not any(summary[k] for k in ('duplicate_jobs','duplicate_cells','missing_cells','unexpected_cells','nonterminal_cells')) and len(rows)==len(expected)
    summary['terminal_complete'] = summary['matrix_complete'] and completion is not None and completion.get('terminal') is True and completion.get('completed_cells')==len(expected)
    cancel_expected = {(r,g) for r in range(provenance['repetitions']) for g in provenance['cancel_selection']}
    cancel_counts = Counter((r['repeat'],r['group']) for r in cancellations)
    summary['cancellation_missing'] = [list(k) for k in sorted(cancel_expected-set(cancel_counts))]
    summary['cancellation_duplicates'] = [list(k) for k,n in cancel_counts.items() if n>1]
    summary['cancellation_unexpected'] = [list(k) for k in sorted(set(cancel_counts)-cancel_expected)]
    summary['cancellation_terminal_complete'] = len(cancellations)==len(cancel_expected) and not any(summary[k] for k in ('cancellation_missing','cancellation_duplicates','cancellation_unexpected')) and all(r['cost'] is not None and r['launcher_returncode']==0 for r in cancellations)
    summary['decisions_by_mode_repeat'] = {f'{m}-{r}': dict(Counter(d for o in observations if o['mode']==m and o['repeat']==r for d in o.get('decisions',[]))) for m in provenance['modes'] for r in range(provenance['repetitions'])}
    (root / 'analysis.json').write_text(json.dumps(observations,indent=2)+'\n')
    (root / 'cancellation-analysis.json').write_text(json.dumps(cancellations,indent=2)+'\n')
    (root / 'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
