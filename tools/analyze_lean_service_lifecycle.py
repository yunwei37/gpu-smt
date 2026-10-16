#!/usr/bin/env python3
"""Recompute complete native lifecycle comparisons from retained ordinary raw."""
import argparse
import collections
import json
from pathlib import Path
import re
import statistics
import sys
import zipfile

ROOT = Path('/workspaces/repository')
SOURCE = ROOT / 'artifacts/lean-service-lifecycle-2026-10-13/experiment020/executed-source'
sys.path.insert(0, str(SOURCE))
from analyze_lean_preparation import interpret


def basic(outcome):
    return outcome if outcome in ['complete', 'rejected', 'incomplete'] else 'operational'


class Raw:
    def __init__(self, directory, label):
        self.label = label
        self.directory = directory
        self.archive = zipfile.ZipFile(directory / (label + '.zip')) if (directory / (label + '.zip')).exists() else None

    def read(self, name):
        if self.archive:
            return self.archive.read(self.label + '/' + name)
        return (self.directory / self.label / name).read_bytes()

    def exists(self, name):
        return self.label + '/' + name in self.archive.namelist() if self.archive else (self.directory / self.label / name).exists()

    def close(self):
        if self.archive:
            self.archive.close()


def analyze_cell(directory, label, method, expected):
    terminal = json.loads((directory / (label + '.terminal.json')).read_text())
    raw = Raw(directory, label)
    rows, latencies, mismatches = {}, [], []
    old_snapshots = reused_prefixes = 0
    if method == 'warm':
        inputs = [json.loads(line) for line in raw.read('input.jsonl').splitlines()]
        if inputs != expected:
            mismatches.append('prepared input differs from original full projection')
        for line in raw.read('results.jsonl').splitlines():
            item = json.loads(line)
            i = item['source_index']
            record = (item.get('native_response') or {}).get('native') or {}
            frame = record.get('response')
            old_snapshots += bool(record.get('old_snapshot_supplied'))
            reused_prefixes += bool(record.get('reused_command_snapshot_prefix'))
            outcome = interpret(frame, {'status': item['status'], 'error': None}, None, 'warm')['outcome']
            if i in rows:
                mismatches.append({'duplicate': i})
            rows[i] = {'outcome': outcome, 'status': item['status']}
            latencies.append((item['terminal_observed_monotonic_ns'] - item['admission_monotonic_ns']) / 1e9)
        events = [json.loads(line) for line in raw.read('native-events.jsonl').splitlines()]
        engagement = {
            'worker_starts': sum(e.get('event') == 'worker_started' for e in events),
            'worker_exits': sum(e.get('event') == 'worker_exited' for e in events),
            'elective_retirements': sum(e.get('event') == 'worker_retirement' for e in events),
            'policy': [e for e in events if e.get('event') == 'worker_policy'],
            'seed_roots': [e.get('seed_roots') for e in events if e.get('event') == 'initialized'],
            'finish': [e for e in events if e.get('event') == 'finish'],
        }
    else:
        for i, inp in enumerate(expected):
            name = f'request-{i:08d}/'
            if not raw.exists(name + 'result.json'):
                continue
            result = json.loads(raw.read(name + 'result.json'))
            record = json.loads(raw.read(name + 'native-record.bin')).get('record', {}).get('native', {}) if result['status'] == 'response' else {}
            frame = record.get('response')
            old_snapshots += bool(record.get('old_snapshot_supplied'))
            reused_prefixes += bool(record.get('reused_command_snapshot_prefix'))
            rows[i] = {'outcome': interpret(frame, result, None, 'warm')['outcome'], 'status': result['status']}
            latencies.append(result.get('invocation_elapsed_ns', 0) / 1e9)
            if json.loads(raw.read(name + 'stdin.bin')) != inp:
                mismatches.append({'source': i, 'reason': 'native input differs from original projection'})
        events = [json.loads(line) for line in raw.read('events.jsonl').splitlines()]
        engagement = {'run': [e for e in events if e.get('event') == 'run'],
                      'elective_retirements': sum(e.get('reason') == 'retire_limit' for e in events)}
    engagement.update(native_old_snapshot_supplied=old_snapshots,
                      positive_reused_command_prefix=reused_prefixes)
    resources = json.loads(raw.read('resources-summary.json')) if raw.exists('resources-summary.json') else None
    raw.close()
    missing = [i for i in range(len(expected)) if i not in rows]
    extra = sorted(set(rows) - set(range(len(expected))))
    for i in missing:
        rows[i] = {'outcome': 'missing_result', 'status': 'missing_result'}
    elapsed = (terminal['end_ns'] - terminal['begin_ns']) / 1e9
    cpu = {}
    text = (directory / (label + '.process-time.txt')).read_text()
    for key, phrase in [('user_seconds', 'User time (seconds)'), ('system_seconds', 'System time (seconds)')]:
        match = re.search(re.escape(phrase) + r':\s*([0-9.]+)', text)
        cpu[key] = float(match.group(1)) if match else None
    cpu['total_seconds'] = sum(cpu.values()) if all(v is not None for v in cpu.values()) else None
    valid = terminal['returncode'] == 0 and not missing and not extra and not mismatches
    ordered = sorted(latencies)
    return {
        'label': label, 'valid_complete': valid, 'returncode': terminal['returncode'],
        'expected': len(expected), 'missing_indices': missing, 'extra_indices': extra,
        'source_issues': mismatches, 'whole_seconds': elapsed,
        'terminal_attempts_per_second': (len(expected) - len(missing)) / elapsed,
        'cpu': cpu, 'resources': resources, 'engagement': engagement,
        'latency_seconds': {'median': statistics.median(ordered) if ordered else None,
                            'p95': ordered[int(.95 * (len(ordered) - 1))] if ordered else None,
                            'p99': ordered[int(.99 * (len(ordered) - 1))] if ordered else None},
        'outcomes': dict(collections.Counter(row['outcome'] for row in rows.values())),
        'basic_rows': {i: basic(row['outcome']) for i, row in rows.items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--previous', type=Path, action='append', default=[])
    args = parser.parse_args()
    cells, missing, pairs = [], [], []
    for dataset, count, width in [('proofnet', 5952, 4), ('minif2f', 7808, 1)]:
        expected = [json.loads(line) for line in (ROOT / 'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs' / dataset / 'input.jsonl').read_text().splitlines()]
        for policy in [128, 512, count]:
            for repetition in [0, 1, 2, 'profile']:
                prefix = f'{dataset}-' + (f'rep{repetition}' if repetition != 'profile' else 'profile') + f'-life{policy}-w{width}-'
                result = {}
                for method in ['warm', 'snapshot']:
                    label = prefix + method
                    candidates = [args.run] + args.previous
                    directory = next((path for path in candidates if (path / (label + '.terminal.json')).exists() and (path / (label + '.terminal.json')).stat().st_size), args.run)
                    terminal_path = directory / (label + '.terminal.json')
                    if not terminal_path.exists() or not terminal_path.stat().st_size:
                        missing.append(label)
                        continue
                    cell = analyze_cell(directory, label, method, expected)
                    cell['raw_directory'] = str(directory)
                    cells.append(cell)
                    result[method] = cell
                if len(result) == 2:
                    proposed, baseline = result['warm'], result['snapshot']
                    differences = [i for i in range(count) if proposed['basic_rows'][i] != baseline['basic_rows'][i]]
                    valid = proposed['valid_complete'] and baseline['valid_complete'] and not differences
                    pairs.append({'dataset': dataset, 'lifetime': policy, 'repetition': repetition,
                                  'valid_complete_basic_pair': valid, 'basic_differences': differences,
                                  'wall_reduction_percent': 100 * (1 - proposed['whole_seconds'] / baseline['whole_seconds']) if valid else None,
                                  'profile': repetition == 'profile'})
    summaries = []
    for dataset, count in [('proofnet', 5952), ('minif2f', 7808)]:
        for policy in [128, 512, count]:
            group = [p for p in pairs if p['dataset'] == dataset and p['lifetime'] == policy and not p['profile']]
            values = [p['wall_reduction_percent'] for p in group if p['valid_complete_basic_pair']]
            summaries.append({'dataset': dataset, 'lifetime': policy, 'valid_primary_pairs': len(values),
                              'paired_reductions_percent': values,
                              'mean_paired_reduction_percent': statistics.mean(values) if len(values) == 3 else None,
                              'range_percent': [min(values), max(values)] if len(values) == 3 else None})
    report = {'planned_cells': 48, 'terminal_cells': len(cells), 'missing_cells': missing,
              'complete_planned_matrix': len(cells) == 48 and all(c['valid_complete'] for c in cells),
              'scope': 'whole formal native lifecycle; finite policies are explicit configurations, not service defaults; sampled resources and closed-loop latency only',
              'cells': cells, 'pairs': pairs, 'primary_summary': summaries}
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'terminal_cells': len(cells), 'missing_cells': len(missing),
                      'complete_planned_matrix': report['complete_planned_matrix']}))


if __name__ == '__main__':
    main()
