#!/usr/bin/env python3
"""Reconstruct native classified WHNF source intervals from ordinary raw logs.

No verifier launch. Missing begin/complete intervals remain censored. These
instrumented calling-thread counters do not establish GPU support or speedup.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import zipfile

METRICS = ('count', 'wall_ns', 'inclusive_thread_cpu_ns', 'exclusive_thread_cpu_ns')
TRANSPARENCY = ('reducible', 'instances', 'default', 'all')


def snapshots(text):
    current = None
    for line in text.splitlines():
        if line.startswith('meta_whnf_snapshot '):
            if current is not None:
                yield current
            fields = dict(re.findall(r'(\w+)=(\S+)', line))
            current = {'index': int(fields['checkpoint']), 'stage': fields['stage'],
                       'pid': int(fields['pid']), 'rows': {}}
        elif line.startswith('meta_whnf_classified '):
            if current is None:
                raise ValueError('counter row has no snapshot header')
            fields = dict(re.findall(r'(\w+)=(\S+)', line))
            if int(fields['checkpoint']) != current['index'] or fields['stage'] != current['stage']:
                raise ValueError('counter row differs from its snapshot')
            key = (int(fields['mask']), int(fields['success']))
            if key in current['rows']:
                raise ValueError('duplicate mask/outcome in one snapshot')
            current['rows'][key] = {m: int(fields[m]) for m in METRICS}
    if current is not None:
        yield current


def flags(mask):
    return dict(cache_enabled=bool(mask & 1), expression_mvars=bool(mask & 2),
                fvars=bool(mask & 4), custom_unfold=bool(mask & 8), level_mvars=bool(mask & 16),
                transparency=TRANSPARENCY[(mask >> 5) & 3])


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', type=Path, required=True)
    ap.add_argument('--label', default='proofnet-native-whnf-classified')
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--reference', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    # Require the actual whole terminal first; partial data cannot acquire a
    # completed comparison merely by running an analyzer.
    terminal_path = args.run/(args.label+'.terminal.json')
    terminal = json.loads(terminal_path.read_text())
    analysis = json.loads((args.run/(args.label+'.analysis.json')).read_text())
    expected = [json.loads(line) for line in args.inputs.read_text().splitlines()]
    reference = next(c for c in json.loads(args.reference.read_text())['cells']
                     if c['label']=='proofnet-rep0-native')
    archive = args.run/(args.label+'.zip')
    issues, intervals, process_rows, source_rows, basic_rows = [], [], [], [], {}
    totals = Counter()
    preparations = Counter()
    with zipfile.ZipFile(archive) as z:
        def read(name):
            return z.read(args.label+'/'+name)
        for ordinal, source in enumerate(expected):
            submitted = json.loads(read(f'request-{ordinal:08d}/stdin.bin'))
            if submitted != dict(index=ordinal, header=source['header'], code=source['code']):
                issues.append({'ordinal': ordinal, 'error': 'actual original input differs'})
            outcome = analysis['candidate_rows'][str(ordinal)]['outcome']
            basic_rows[str(source['index'])] = outcome if outcome in ('complete','rejected','incomplete') else 'operational'
        for member in z.namelist():
            if not member.endswith('/stderr.bin') or '/worker-' not in member:
                continue
            observed = list(snapshots(z.read(member).decode(errors='replace')))
            pending, first, completed, terminal_pids = {}, {}, Counter(), set()
            for snapshot in observed:
                pid, index, stage = snapshot['pid'], snapshot['index'], snapshot['stage']
                if stage != 'terminal' and not 0 <= index < len(expected):
                    issues.append({'member':member, 'pid':pid, 'index':index,
                                   'error':'frontend snapshot source ordinal outside original population'})
                if stage == 'terminal':
                    terminal_pids.add(pid)
                if stage == 'frontend_begin':
                    if pid not in first:
                        first[pid] = index
                        for (mask, success), values in snapshot['rows'].items():
                            for metric, value in values.items():
                                preparations[(mask, success, metric)] += value
                    key = (pid, index)
                    if key in pending:
                        issues.append({'member':member, 'pid':pid, 'index':index, 'error':'duplicate begin'})
                    pending[key] = snapshot
                elif stage == 'frontend_complete':
                    begin = pending.pop((pid,index), None)
                    if begin is None:
                        issues.append({'member':member, 'pid':pid, 'index':index, 'error':'complete lacks same-process begin'})
                        continue
                    completed[pid] += 1
                    source_totals = Counter()
                    valid = True
                    for mask, success in sorted(begin['rows'].keys() | snapshot['rows'].keys()):
                        before = begin['rows'].get((mask,success), {})
                        after = snapshot['rows'].get((mask,success), {})
                        delta = {m:after.get(m,0)-before.get(m,0) for m in METRICS}
                        if any(v < 0 for v in delta.values()):
                            valid = False
                            issues.append({'member':member, 'pid':pid, 'index':index,
                                           'mask':mask, 'success':success, 'error':'negative cumulative difference', 'delta':delta})
                        if any(delta.values()):
                            row = dict(member=member, pid=pid, source_index=index, mask=mask,
                                       success=success, **flags(mask), **delta)
                            source_rows.append(row)
                            for metric,value in delta.items():
                                totals[(mask,success,metric)] += value
                                source_totals[metric] += value
                    intervals.append(dict(member=member, pid=pid, source_index=index,
                                          valid_nonnegative_difference=valid,
                                          **{m:source_totals[m] for m in METRICS}))
            process_rows.append(dict(member=member, snapshots=len(observed),
                                     first_frontend_by_pid=first, completed_intervals_by_pid=dict(completed),
                                     terminal_pids=sorted(terminal_pids),
                                     censored_intervals=[dict(pid=p,source_index=i) for p,i in pending]))
        events = [json.loads(line) for line in read('events.jsonl').splitlines()]
        shutdown = [e for e in events if e.get('event')=='shutdown']
        completed_sources = shutdown[0].get('completed',[]) if len(shutdown)==1 else []
        if Counter(completed_sources) != Counter(range(len(expected))):
            issues.append('actual shutdown source population differs')
        resources = json.loads(read('resources-summary.json'))
    basic_differences = [dict(index=i,reference=reference['basic_rows'].get(i),observed=v)
                         for i,v in basic_rows.items() if reference['basic_rows'].get(i)!=v]
    if set(basic_rows)!=set(reference['basic_rows']):
        issues.append('basic reference source population differs')
    mask_rows = []
    for mask,success in sorted({(m,s) for m,s,_ in totals} | {(m,s) for m,s,_ in preparations}):
        mask_rows.append(dict(mask=mask,success=success,**flags(mask),
                              **{k:totals[(mask,success,k)] for k in METRICS},
                              first_begin_preparation={k:preparations[(mask,success,k)] for k in METRICS}))
    args.out.mkdir(exist_ok=False)
    for name,rows in [('source-mask-deltas.csv',source_rows),('source-intervals.csv',intervals)]:
        with (args.out/name).open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]) if rows else [])
            writer.writeheader();writer.writerows(rows)
    result = dict(run=str(args.run), terminal=terminal, expected_sources=len(expected),
                  original_basic_outcomes=dict(Counter(basic_rows.values())),
                  basic_reference=str(args.reference), basic_differences=basic_differences,
                  reference_valid_complete=reference['valid_complete'], issues=issues,
                  resources=resources, process_snapshots=process_rows,
                  observed_frontend_intervals=len(intervals), mask_deltas=mask_rows,
                  valid_whole_basic_diagnostic=terminal['returncode']==0 and not issues
                      and not basic_differences and reference['valid_complete'],
                  limitations=[
                    'raw flags describe input/policy, not actual device support',
                    'source deltas are same-process complete-minus-begin; censored intervals have no fabricated zero',
                    'first begin snapshots include inherited preparation and are not globally unique preparation totals',
                    'cache reuse can skip frontend checkpoints; no fabricated standalone zero-cost native run',
                    'multi-thread relaxed snapshots can be noncoherent and include crossing scopes',
                    'inclusive/wall sums overlap nesting; exclusive calling-thread CPU is not full process-tree CPU',
                    'hook overhead/compiler/resource-boundary effects and original failed/open work remain limitations',
                    'different acquisition/cache policy and instrumentation forbid headline speedup or GPU upper bound'],
                  sha256={str(p):digest(p) for p in [archive,args.inputs,args.reference,terminal_path,Path(__file__)]})
    (args.out/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(valid_whole_basic_diagnostic=result['valid_whole_basic_diagnostic'],
                         observed_frontend_intervals=len(intervals), basic_differences=basic_differences,
                         issues=issues, mask_deltas=mask_rows),indent=2))


if __name__ == '__main__':
    main()
