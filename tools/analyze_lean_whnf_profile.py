#!/usr/bin/env python3
"""Read whole native WHNF captures without launching or changing a verifier.

Terminal totals are process-local and may be inherited across preparation forks.
Missing terminal dumps are censored, not zero. Never compute a GPU speedup bound.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import zipfile


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', type=Path, required=True)
    ap.add_argument('--label', required=True)
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--reference', type=Path, required=True)
    ap.add_argument('--reference-label', default='proofnet-rep0-native')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    terminal = json.loads((args.run / (args.label + '.terminal.json')).read_text())
    analysis = json.loads((args.run / (args.label + '.analysis.json')).read_text())
    expected = [json.loads(line) for line in args.inputs.read_bytes().splitlines()]
    reference = json.loads(args.reference.read_text())
    ref = next(x for x in reference['cells'] if x['label'] == args.reference_label)
    archive = args.run / (args.label + '.zip')
    rows, issues, workers = {}, [], []
    counter_pattern = re.compile(r'^meta_whnf_profile\s+(.*)$')
    totals = Counter()
    with zipfile.ZipFile(archive) as z:
        def read(name):
            return z.read(args.label + '/' + name)
        for ordinal, source in enumerate(expected):
            directory = f'request-{ordinal:08d}/'
            original = json.loads(read(directory + 'stdin.bin'))
            if original != dict(index=ordinal, header=source['header'], code=source['code']):
                issues.append({'ordinal': ordinal, 'error': 'original input differs'})
            outcome = analysis['candidate_rows'][str(ordinal)]['outcome']
            rows[str(source['index'])] = outcome if outcome in ('complete', 'rejected', 'incomplete') else 'operational'
        for name in z.namelist():
            if not name.endswith('/stderr.bin') or '/worker-' not in name:
                continue
            parsed = []
            for line in z.read(name).decode(errors='replace').splitlines():
                match = counter_pattern.match(line)
                if not match:
                    continue
                try:
                    values = {k: int(v) for k, v in re.findall(r'(\w+)=([0-9]+)', match.group(1))}
                    parsed.append(values)
                except ValueError as error:
                    issues.append({'file': name, 'error': str(error)})
            endings = [r for r in parsed if r.get('terminal') == 1]
            if len(endings) not in (0, 4):
                issues.append({'file': name, 'error': 'unexpected terminal bucket count', 'count': len(endings)})
            workers.append({'stderr': name, 'terminal_dump_present': bool(endings),
                            'rows': endings, 'checkpoint_rows': len(parsed) - len(endings)})
            for item in endings:
                prefix = 'cache_admissible' if item['eligible'] else 'cache_inadmissible_or_level_mvar'
                prefix += '_success' if item['success'] else '_failure'
                for metric in ('count', 'wall_ns', 'inclusive_thread_cpu_ns', 'exclusive_thread_cpu_ns'):
                    totals[prefix + '.' + metric] += item[metric]
        resources = json.loads(read('resources-summary.json'))
        events = [json.loads(line) for line in read('events.jsonl').splitlines()]
        shutdown = [e for e in events if e.get('event') == 'shutdown']
        completed = shutdown[0].get('completed', []) if len(shutdown) == 1 else []
        if Counter(completed) != Counter(range(len(expected))):
            issues.append('terminal shutdown source coverage differs')
    differences = [{'index': i, 'reference': ref['basic_rows'].get(i), 'profile': value}
                   for i, value in rows.items() if ref['basic_rows'].get(i) != value]
    if set(rows) != set(ref['basic_rows']):
        issues.append('profile/reference original source indices differ')
    if len(workers) != analysis['engagement']['sessions']:
        issues.append('worker stderr coverage differs from sessions')
    result = {
        'run': str(args.run), 'label': args.label,
        'expected_sources': len(expected), 'original_basic_outcomes': dict(Counter(rows.values())),
        'whole_terminal': terminal, 'resources': resources,
        'basic_reference': str(args.reference), 'basic_reference_label': args.reference_label,
        'basic_reference_valid_complete': ref['valid_complete'],
        'basic_differences': differences, 'source_issues': issues,
        'valid_whole_diagnostic': terminal['returncode'] == 0 and not issues and not differences and ref['valid_complete'],
        'worker_dumps': workers, 'observed_terminal_sum': dict(totals),
        'missing_terminal_workers': [w['stderr'] for w in workers if not w['terminal_dump_present']],
        'limitations': [
            'initial binary has terminal dumps only; no source or preparation deltas',
            'totals are process-local and may contain inherited preparation work',
            'missing worker terminal dumps censor its completed and unfinished work',
            'eligibility means useCache and no level metavariable, not actual GPU support',
            'false bucket conflates local/expr mvars/custom unfolding/transparency and level mvars',
            'inclusive CPU and wall sums overlap nesting; exclusive CPU is only scoped calling-thread work',
            'instrumentation overhead and reference-sharing/compiler effects remain unqualified',
            'legacy caller rechecks duplicates, unlike current main success-only cache',
            'different affinity/width/profiling prevent headline timing or speedup comparison',
            'no total-CPU fraction, GPU bound, device execution, or native bridge qualification inferred'],
        'sha256': {str(p): sha(p) for p in (archive, args.reference, args.inputs, Path(__file__))}}
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('valid_whole_diagnostic', 'expected_sources', 'original_basic_outcomes',
                                          'basic_differences', 'source_issues', 'observed_terminal_sum', 'missing_terminal_workers')}, indent=2))


if __name__ == '__main__':
    main()
