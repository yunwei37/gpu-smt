#!/usr/bin/env python3
"""Recompute complete formal verification comparisons from retained raw captures."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import statistics
import sys
import zipfile

ROOT = Path('/workspaces/repository')
sys.path.insert(0, str(ROOT / 'bench'))
from analyze_lean_preparation import interpret


def basic(outcome):
    return outcome if outcome in ('complete', 'rejected', 'incomplete') else 'operational'


class Raw:
    def __init__(self, folder, label):
        self.folder, self.label = folder, label
        archive = folder / (label + '.zip')
        self.archive = zipfile.ZipFile(archive) if archive.exists() else None

    def read(self, name):
        if self.archive:
            return self.archive.read(self.label + '/' + name)
        return (self.folder / self.label / name).read_bytes()

    def exists(self, name):
        if self.archive:
            return self.label + '/' + name in self.archive.namelist()
        return (self.folder / self.label / name).exists()

    def close(self):
        if self.archive:
            self.archive.close()


def cell(folder, label, method, expected):
    terminal = json.loads((folder / (label + '.terminal.json')).read_text())
    raw = Raw(folder, label)
    issues = []
    actual_inputs = [json.loads(line) for line in raw.read('input.jsonl').splitlines()]
    if actual_inputs != expected:
        issues.append('captured original input population differs')
    receipt = json.loads(raw.read('receipt.json'))
    records = [json.loads(line) for line in raw.read('results.jsonl').splitlines()]
    rows, latencies = {}, []
    engagement = Counter()
    backend_codes, device_errors = Counter(), []
    stage_ns = Counter()
    cache = {}
    for item in records:
        index = item['source_index']
        if index in rows:
            issues.append({'duplicate_index': index})
        ordinal = item['ordinal']
        if not 0 <= ordinal < len(expected) or expected[ordinal]['index'] != index:
            issues.append({'wrong_original_ordinal': ordinal, 'index': index})
            continue
        source = expected[ordinal]
        key = (source['header'], source['code'])
        if item.get('cached'):
            old = cache.get(key)
            if old is None or old['source_index'] != item.get('cached_from_index'):
                issues.append({'invalid_success_cache_reference': index})
            engagement['success_cache_hits'] += 1
        status = item['status']
        if status != 'response':
            outcome = status
        elif method == 'native':
            native = (item.get('record') or {}).get('record', {}).get('native', {})
            outcome = interpret(native.get('response'), {'status': status, 'error': None}, None, 'warm')['outcome']
            if not item.get('cached'):
                engagement['native_old_snapshot_supplied'] += bool(native.get('old_snapshot_supplied'))
                engagement['native_reused_command_prefix'] += bool(native.get('reused_command_snapshot_prefix'))
        else:
            value = item['record']['result']
            backend = value.get('backend') or {}
            checked = backend.get('checked') or {}
            code = checked.get('code')
            if code == 3 and not value.get('native_fallback'):
                outcome = 'backend_operational_failure'
            elif value.get('has_errors'):
                outcome = 'rejected'
            elif value.get('has_sorry'):
                outcome = 'incomplete'
            elif value.get('native_fallback'):
                native = backend.get('native_fallback') or {}
                outcome = interpret(native.get('response'), {'status': status, 'error': None}, None, 'warm')['outcome']
            elif code == 0 and (backend.get('exit') or {}).get('wait_status') == 0 and backend.get('all_local_declarations_exported'):
                outcome = 'complete'
            else:
                outcome = 'rejected'
            if value.get('producer_proof_accepted') is not False:
                issues.append({'producer_acceptance_field': index})
            if not item.get('cached'):
                engagement['actual_deferred_additions'] += int(value.get('actual_deferred_additions', 0))
                engagement['native_fallback_sources'] += bool(value.get('native_fallback'))
                engagement['external_checked_sources'] += bool(checked)
                engagement['exported_declarations'] += int(checked.get('declarations', 0))
                engagement['actual_gpu_requested_sources'] += bool(checked.get('actual_gpu_requested'))
                engagement['device_discharged_declarations'] += int(checked.get('device_discharged', 0))
                backend_codes[str(code)] += 1
                if checked.get('device_error'):
                    device_errors.append({'index': index, 'error': checked['device_error']})
                for key_ns in ('frontend_ns', 'export_ns', 'archive_ns'):
                    stage_ns[key_ns] += int(value.get(key_ns, 0))
                for key_ns in ('parse_ns', 'check_ns', 'device_ns'):
                    stage_ns[key_ns] += int(checked.get(key_ns, 0))
        if outcome != item['outcome']:
            issues.append({'stored_outcome_difference': index, 'stored': item['outcome'], 'recomputed': outcome})
        rows[index] = outcome
        if outcome == 'complete' and not item.get('cached'):
            cache[(source['header'], source['code'])] = item
        latencies.append((item['terminal_monotonic_ns'] - item['admission_monotonic_ns']) / 1e9)
    events = [json.loads(line) for line in raw.read('events.jsonl').splitlines()]
    engagement['worker_starts'] = sum(event.get('event') == 'worker_start' for event in events)
    engagement['worker_exits'] = sum(event.get('event') == 'worker_exit' for event in events)
    finalizations = []
    for event in events:
        if event.get('event') == 'worker_exit' and event.get('cleanup', {}).get('graceful_eof') and event.get('returncode') != 0:
            issues.append({'failed_final_eof': event['worker'], 'returncode': event['returncode']})
        if method != 'native' and event.get('event') == 'worker_start':
            name = Path(event['directory']).name + '/stdout.bin'
            for line in raw.read(name).splitlines():
                try:
                    record = json.loads(line)
                except (ValueError, UnicodeDecodeError):
                    continue
                if 'backend_finished' in record:
                    finalizations.append(record['backend_finished'])
                    if record['backend_finished'].get('device_finish_error'):
                        device_errors.append({'stage': 'final_eof', 'error': record['backend_finished']['device_finish_error']})
    preparations = [event['record'] for event in events if event.get('event') == 'backend_stage']
    prefixes = [stage['backend_preparation'] for stage in preparations if 'backend_preparation' in stage]
    type_preparations = [stage for stage in preparations if 'public_statement_types' in stage]
    if method != 'native' and not any(prefix.get('prefix_verified') is True for prefix in prefixes):
        issues.append('no independently verified imported prefix')
    if method != 'native' and any(stage['unavailable_statement_types'] == stage['public_statement_types'] for stage in type_preparations):
        issues.append('all public statement types unavailable; planned preparation did not engage')
    resources = json.loads(raw.read('resources-summary.json')) if raw.exists('resources-summary.json') else None
    raw.close()
    indices = {item['index'] for item in expected}
    missing, extra = sorted(indices - rows.keys()), sorted(rows.keys() - indices)
    whole = (terminal['end_ns'] - terminal['begin_ns']) / 1e9
    cpu = {}
    text = (folder / (label + '.process-time.txt')).read_text()
    for name, phrase in [('user_seconds', 'User time (seconds)'), ('system_seconds', 'System time (seconds)')]:
        match = re.search(re.escape(phrase) + r':\s*([0-9.]+)', text)
        cpu[name] = float(match[1]) if match else None
    cpu['total_seconds'] = sum(cpu.values()) if all(value is not None for value in cpu.values()) else None
    ordered = sorted(latencies)
    valid = terminal['returncode'] == 0 and not missing and not extra and not issues and receipt.get('finished_inputs') == len(expected) and not receipt.get('signals')
    return {'label': label, 'method': method, 'valid_complete': valid,
            'actual_affinity': receipt.get('affinity'), 'workers': receipt.get('jobs'),
            'returncode': terminal['returncode'], 'source_issues': issues,
            'expected': len(expected), 'returned': len(records),
            'missing_indices': missing, 'extra_indices': extra,
            'whole_seconds': whole, 'whole_cpu': cpu,
            'terminal_attempts_per_second': len(records) / whole,
            'latency_seconds': {'median': statistics.median(ordered) if ordered else None,
                                'p95': ordered[int(.95 * (len(ordered) - 1))] if ordered else None,
                                'p99': ordered[int(.99 * (len(ordered) - 1))] if ordered else None},
            'resources': resources, 'engagement': dict(engagement),
            'backend_codes': dict(backend_codes), 'device_errors': device_errors,
            'stage_ns': dict(stage_ns), 'backend_preparations': prefixes,
            'public_type_preparations': type_preparations,
            'backend_finalizations': finalizations,
            'outcomes': dict(Counter(rows.values())),
            'basic_rows': {index: basic(outcome) for index, outcome in rows.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--experiment', type=Path, required=True)
    parser.add_argument('--preflight', action='store_true')
    parser.add_argument('--preflight-attempt', type=int, default=1)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--previous', type=Path, action='append', default=[], help='retained whole cells from prior run directories; current terminal wins')
    parser.add_argument('--run', type=Path, help='current recovery CPU directory')
    args = parser.parse_args()
    cells, missing_cells, comparisons = [], [], []
    for dataset in ('proofnet', 'minif2f'):
        preflight_inputs = 'inputs/preflight3' if args.preflight_attempt == 3 else 'inputs/preflight'
        input_dir = args.experiment / preflight_inputs / dataset if args.preflight else ROOT / 'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs' / dataset
        expected = [json.loads(line) for line in (input_dir / 'input.jsonl').read_text().splitlines()]
        for repetition in (['preflight'] if args.preflight else [0, 1, 2, 'profile']):
            group = {}
            for method in ('native', 'cpu', 'gpu'):
                label = dataset + '-' + method if args.preflight else dataset + '-' + ('profile' if repetition == 'profile' else f'rep{repetition}') + '-' + method
                folder = args.experiment / f'preflight{args.preflight_attempt}' if args.preflight else args.experiment / ('full1-gpu' if method == 'gpu' else 'full1-cpu')
                if not args.preflight and args.run and method != 'gpu':
                    folder = args.run
                    candidates = [folder] + args.previous
                    folder = next((path for path in candidates if (path / (label + '.terminal.json')).exists() and (path / (label + '.terminal.json')).stat().st_size), folder)
                terminal_path = folder / (label + '.terminal.json')
                if not terminal_path.exists() or not terminal_path.stat().st_size:
                    missing_cells.append(label)
                    continue
                result = cell(folder, label, method, expected)
                result.update(dataset=dataset, repetition=repetition)
                cells.append(result)
                group[method] = result
            if 'native' in group:
                native = group['native']
                for method in ('cpu', 'gpu'):
                    if method not in group:
                        continue
                    other = group[method]
                    differences, recovered = [], []
                    for index in native['basic_rows'].keys() & other['basic_rows'].keys():
                        left, right = native['basic_rows'][index], other['basic_rows'][index]
                        if left != right:
                            (recovered if left == 'operational' and right != 'operational' else differences).append({'index': index, 'native': left, method: right})
                    comparisons.append({'dataset': dataset, 'repetition': repetition, 'method': method,
                                        'valid_basic_comparison': native['valid_complete'] and other['valid_complete'] and not differences,
                                        'same_actual_affinity': native['actual_affinity'] == other['actual_affinity'],
                                        'same_worker_width': native['workers'] == other['workers'],
                                        'valid_performance_comparison': native['valid_complete'] and other['valid_complete'] and not differences and native['actual_affinity'] == other['actual_affinity'] and native['workers'] == other['workers'],
                                        'basic_differences': differences, 'recovered_native_operational_sources': recovered})
    matrix_size = 6 if args.preflight else 24
    summaries = []
    if not args.preflight:
        for dataset in ('proofnet', 'minif2f'):
            reductions = []
            for repetition in range(3):
                group = {item['method']: item for item in cells if item['dataset'] == dataset and item['repetition'] == repetition}
                matches = [item for item in comparisons if item['dataset'] == dataset and item['repetition'] == repetition]
                if len(group) == 3 and all(item['valid_complete'] for item in group.values()) and len(matches) == 2 and all(item['valid_basic_comparison'] for item in matches) and group['gpu']['engagement'].get('device_discharged_declarations', 0) > 0:
                    best = min(group[method]['whole_seconds'] for method in ('native', 'cpu'))
                    reductions.append(100 * (1 - group['gpu']['whole_seconds'] / best))
            summaries.append({'dataset': dataset, 'valid_primary_triplets': len(reductions),
                              'gpu_wall_reductions_vs_faster_complete_cpu_percent': reductions,
                              'mean_percent': statistics.mean(reductions) if len(reductions) == 3 else None,
                              'range_percent': [min(reductions), max(reductions)] if len(reductions) == 3 else None})
    report = {'planned_cells': matrix_size, 'terminal_cells': len(cells), 'missing_cells': missing_cells,
              'complete_planned_matrix': len(cells) == matrix_size and all(item['valid_complete'] for item in cells),
              'scope': 'complete fixed formal source verification; no generation/proving accuracy, fragment-only gain, GPU isolation or significance claim',
              'cells': cells, 'comparisons': comparisons, 'primary_summary': summaries}
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'terminal_cells': len(cells), 'missing_cells': len(missing_cells), 'complete_planned_matrix': report['complete_planned_matrix']}))


if __name__ == '__main__':
    main()
