#!/usr/bin/env python3
"""Ordinary E022 raw basic-result/provider analysis; never an execution gate."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import statistics
import sys
import zipfile
from functools import lru_cache

BASE = Path(__file__).resolve().parent
ROOT = Path('/workspaces/repository')
sys.path.insert(0, str(BASE / 'source1'))
from analyze_lean_preparation import interpret


def basic(outcome):
    return outcome if outcome in ('complete', 'rejected', 'incomplete') else 'operational'


class Raw:
    def __init__(self, run, label):
        self.folder = run / label
        self.label = label
        self.archive = zipfile.ZipFile(run / (label + '.zip')) if (run / (label + '.zip')).exists() else None

    def names(self):
        return [name[len(self.label) + 1:] for name in self.archive.namelist()] if self.archive else [str(p.relative_to(self.folder)) for p in self.folder.rglob('*') if p.is_file()]

    def read(self, name):
        return self.archive.read(self.label + '/' + name) if self.archive else (self.folder / name).read_bytes()

    def exists(self, name):
        return self.label + '/' + name in self.archive.namelist() if self.archive else (self.folder / name).exists()

    def close(self):
        if self.archive:
            self.archive.close()


def distribution(values):
    values = sorted(values)
    if not values:
        return {'n': 0}
    return {'n': len(values), 'median': statistics.median(values),
            'p95': values[int(.95 * (len(values) - 1))],
            'p99': values[int(.99 * (len(values) - 1))]}


COUNTERS = ('calls', 'supported', 'declined', 'cpu_calls', 'gpu_calls',
            'serialization_ns', 'initialization_ns', 'allocation_upload_ns',
            'launch_sync_ns', 'download_ns', 'quotation_ns', 'whole_provider_ns',
            'host_growth_calls', 'host_growth_ns')


def provider(raw):
    """Cumulative observations: one terminal, or per-field max, per actual PID.

    Native warm workers inherit stderr. Snapshot workers have separate stderr
    files. Both are read verbatim; repeated checkpoints are never summed.
    Missing terminal workers remain censored, including their original errors.
    """
    processes = defaultdict(list)
    errors = {}
    for name in raw.names():
        if not (name == 'stderr.bin' or name.endswith('/stderr.bin')):
            continue
        for number, line in enumerate(raw.read(name).splitlines(), 1):
            if not line.startswith(b'{'):
                continue
            try:
                item = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                continue
            if not str(item.get('event', '')).startswith('closure_native_'):
                continue
            item = dict(item, raw_file=name, raw_line=number)
            processes[item.get('pid')].append(item)
            if item.get('driver_error'):
                key = (item.get('pid'), item['driver_error'])
                if key not in errors:
                    errors[key] = {'pid': key[0], 'driver_error': key[1], 'observed_records': 0,
                                   'first_raw_observation': item}
                errors[key]['observed_records'] += 1
                errors[key]['last_raw_observation'] = item
    totals = Counter()
    per_pid = []
    for pid, events in sorted(processes.items(), key=lambda item: str(item[0])):
        terminal = [e for e in events if e['event'] == 'closure_native_provider_finished']
        # A driver failure may emit finished before the last declined counter is
        # updated. Maxima retain that later checkpoint, without double-counting.
        counters = {key: max(int(e.get(key, 0)) for e in events) for key in COUNTERS}
        totals.update(counters)
        ready = [e for e in events if e['event'] == 'closure_native_device_ready']
        per_pid.append({'pid': pid, 'terminal_observed': bool(terminal),
                        'checkpoint_records': sum(e['event'] == 'closure_native_provider_checkpoint' for e in events),
                        'cumulative_observation': counters,
                        'actual_rtx5090_ready': any('RTX 5090' in e.get('device', '') or 'RTX5090' in e.get('device', '') for e in ready),
                        'explicit_peak_bytes': max(int(e.get('explicit_peak_bytes', 0)) for e in events),
                        'host_scratch_bytes': max(int(e.get('host_scratch_bytes', 0)) for e in events),
                        'device_names': sorted({e.get('device') for e in events if e.get('device')}),
                        'raw_record_count': len(events),
                        'last_raw_observation': events[-1],
                        'terminal_raw_locations': [{'file': e['raw_file'], 'line': e['raw_line']} for e in terminal]})
    actual = any(p['actual_rtx5090_ready'] for p in per_pid)
    return {'observed_processes': len(per_pid), 'terminal_processes': sum(p['terminal_observed'] for p in per_pid),
            'censored_processes': [p['pid'] for p in per_pid if not p['terminal_observed']],
            'cumulative_per_pid_maxima_sum': dict(totals), 'per_pid': per_pid,
            'driver_errors': list(errors.values()), 'actual_rtx5090_ready': actual,
            'device_operation_and_native_readback_observed': actual and totals['gpu_calls'] > 0 and totals['supported'] > 0 and totals['cpu_calls'] == 0,
            'scope': 'native provider operation/readback, not full kernel GPU discharge; original final native kernel and declined-operation fallback remain',
            'memory_scope': 'per-process explicit allocation maxima are not simultaneous VRAM peak; context/module/JIT/default stack/driver/other owners excluded'}


def analyze_cell(run, label):
    terminal = json.loads((run / (label + '.terminal.json')).read_text())
    expected = [json.loads(line) for line in Path(terminal['input']).read_bytes().splitlines() if line.strip()]
    raw = Raw(run, label)
    issues = []
    expected_indices = {item['index'] for item in expected}
    expected_by_index = {item['index']: item for item in expected}
    rows = {}
    latencies = []
    cache_hits = 0
    try:
        captured = [json.loads(line) for line in raw.read('input.jsonl').splitlines() if line.strip()]
        if captured != expected:
            issues.append('captured original input differs')
        records = [json.loads(line) for line in raw.read('results.jsonl').splitlines() if line.strip()] if raw.exists('results.jsonl') else []
        for item in records:
            ordinal, index = item.get('ordinal'), item['source_index']
            if not isinstance(ordinal, int) or not 0 <= ordinal < len(expected) or expected[ordinal]['index'] != index:
                issues.append({'ordinal_index_mismatch': [ordinal, index]})
            if index in rows:
                issues.append({'duplicate_source_index': index})
            if terminal['method'] == 'snapshot-cache':
                native = ((item.get('record') or {}).get('record') or {}).get('native') or {}
                elapsed = item.get('seconds')
            else:
                native = (item.get('native_response') or {}).get('native') or {}
                elapsed = (item['terminal_observed_monotonic_ns'] - item['admission_monotonic_ns']) / 1e9
            original_index = item.get('cached_from_index') if item.get('cached') else index
            if item.get('cached'):
                original = expected_by_index.get(original_index)
                current = expected_by_index.get(index)
                prior = rows.get(original_index)
                if not original or not current or (original['header'], original['code']) != (current['header'], current['code']):
                    issues.append({'cached_original_source_differs': index, 'cached_from_index': original_index})
                if not prior or prior['outcome'] != 'complete':
                    issues.append({'cached_original_complete_record_missing': index, 'cached_from_index': original_index})
            if item['status'] == 'response' and native.get('index') != original_index:
                issues.append({'inner_native_index_mismatch': index, 'expected_native_index': original_index})
            outcome = interpret(native.get('response'), {'status': item['status'], 'error': item.get('error')}, None, 'warm')['outcome']
            rows[index] = {'outcome': outcome, 'basic': basic(outcome), 'status': item['status'],
                           'ordinal': ordinal, 'seconds': elapsed, 'cached': item.get('cached', False)}
            if elapsed is not None:
                latencies.append(elapsed)
            cache_hits += bool(item.get('cached'))
        receipt = json.loads(raw.read('receipt.json')) if raw.exists('receipt.json') else {}
        device = provider(raw)
        resources = json.loads(raw.read('resources-summary.json')) if raw.exists('resources-summary.json') else None
        events = []
        event_file = 'events.jsonl' if terminal['method'] == 'snapshot-cache' else 'native-events.jsonl'
        if raw.exists(event_file):
            events = [json.loads(line) for line in raw.read(event_file).splitlines() if line.strip()]
        engagement = {'success_cache_hits': cache_hits,
                      'worker_starts': sum(e.get('event') in ('worker_start', 'worker_started') for e in events),
                      'worker_exits': sum(e.get('event') in ('worker_exit', 'worker_exited') for e in events),
                      'elective_retirements': sum(e.get('event') == 'worker_retirement' for e in events),
                      'worker_policy': [e for e in events if e.get('event') == 'worker_policy']}
    finally:
        raw.close()
    missing, extra = sorted(expected_indices - rows.keys()), sorted(rows.keys() - expected_indices)
    whole = terminal['complete_wall_seconds']
    return {'label': label, 'dataset': terminal['dataset'], 'method': terminal['method'],
            'returncode': terminal['returncode'], 'expected': len(expected), 'returned': len(rows),
            'missing_indices': missing, 'extra_indices': extra, 'source_issues': issues,
            'valid_complete': terminal['returncode'] == 0 and not missing and not extra and not issues,
            'whole_seconds': whole, 'actual_affinity': terminal['cpu_set'], 'workers': terminal['worker_width'],
            'terminal_attempts_per_second': len(rows) / whole if whole else None,
            'latency_seconds': distribution(latencies), 'outcomes': dict(Counter(r['outcome'] for r in rows.values())),
            'basic_rows': {str(i): r['basic'] for i, r in rows.items()}, 'candidate_rows': rows,
            'receipt': receipt, 'engagement': engagement, 'provider': device, 'resources': resources}


@lru_cache(maxsize=None)
def original_operational(dataset, index):
    if dataset != 'proofnet' or str(index) != '5879':
        return False
    _, references = retained_references()
    return any(cell.get('label', '').startswith('proofnet-') and cell['basic_rows'].get('5879') == 'operational' for cell in references)


def compare(left, right):
    differences, recovered = [], []
    for index in left['basic_rows'].keys() & right['basic_rows'].keys():
        a, b = left['basic_rows'][index], right['basic_rows'][index]
        if a == 'operational' and b != 'operational' and original_operational(left['dataset'], index):
            recovered.append(index)
        elif a != b:
            differences.append({'source_index': index, 'left': a, 'right': b})
    return {'left': left['label'], 'right': right['label'], 'basic_differences': differences,
            'original_operational_recoveries': recovered,
            'valid_basic_comparison': left['valid_complete'] and right['valid_complete'] and not differences,
            'same_affinity': left['actual_affinity'] == right['actual_affinity'],
            'same_worker_width': left['workers'] == right['workers'],
            'valid_performance_comparison': left['valid_complete'] and right['valid_complete'] and not differences and left['actual_affinity'] == right['actual_affinity'] and left['workers'] == right['workers']}


def retained_references():
    path = ROOT / 'artifacts/lean-gpu-checking-2026-10-13/experiment021/current-analysis-20261013T1450.json'
    reference = json.loads(path.read_text()) if path.exists() else {}
    cells = [c for c in reference.get('cells', []) if c.get('method') == 'native' and c.get('valid_complete')]
    return path, cells


def analyze_runs(runs):
    cells, failures = [], []
    selected, retained_duplicate_labels = {}, []
    for run in runs:
        for terminal in sorted(run.glob('*.terminal.json')):
            label = terminal.name[:-len('.terminal.json')]
            if label in selected:
                retained_duplicate_labels.append({'label': label, 'selected_run': str(selected[label]), 'other_run': str(run)})
                continue
            selected[label] = run
            try:
                cells.append(dict(analyze_cell(run, label), raw_run=str(run)))
            except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
                failures.append({'label': label, 'raw_run': str(run), 'analysis_error': repr(exc)})
    comparisons = []
    for cell in cells:
        if cell['method'] in ('warm', 'snapshot-cache'):
            prefix = cell['label'][:-len('-' + cell['method'])]
            for other in cells:
                if other['label'].startswith(prefix + '-') and other['method'] in ('cpu', 'gpu'):
                    comparisons.append(compare(cell, other))
    path, references = retained_references()
    historical = []
    for cell in cells:
        ref = next((r for r in references if r.get('label', '').startswith(cell['dataset'] + '-')), None)
        if ref:
            difference, recovered = [], []
            for index, value in cell['basic_rows'].items():
                original = ref['basic_rows'].get(index)
                if original == 'operational' and value != 'operational' and original_operational(cell['dataset'], index):
                    recovered.append(index)
                elif original is not None and original != value:
                    difference.append({'source_index': index, 'reference': original, 'observed': value})
            historical.append({'label': cell['label'], 'reference': str(path), 'reference_cell': ref['label'],
                               'basic_differences': difference, 'original_operational_recoveries': recovered,
                               'comparison_scope': 'basic source outcome only; different historical acquisition/resources are not paired performance'})
    paired_effects = []
    by_label = {c['label']: c for c in cells}
    for dataset in ('proofnet', 'minif2f'):
        for block in ('rep0', 'rep1', 'rep2', 'profile'):
            prefix = dataset + '-' + block + '-'
            group = {m: by_label.get(prefix + m) for m in ('warm', 'snapshot-cache', 'cpu', 'gpu')}
            if not all(group.values()):
                continue
            matches = [compare(group[stock], group[method]) for stock in ('warm', 'snapshot-cache') for method in ('cpu', 'gpu')]
            matches.append(compare(group['warm'], group['snapshot-cache']))
            fair = all(c['valid_basic_comparison'] and c['same_affinity'] and c['same_worker_width'] for c in matches)
            gpu = group['gpu']
            ready = gpu['provider']['device_operation_and_native_readback_observed']
            baseline = min((group['warm'], group['snapshot-cache']), key=lambda c: c['whole_seconds'])
            reduction = 100 * (baseline['whole_seconds'] - gpu['whole_seconds']) / baseline['whole_seconds'] if fair and ready else None
            paired_effects.append({'dataset': dataset, 'block': block, 'role': 'single instrumented profile' if block == 'profile' else 'primary whole repetition',
                                   'valid_basic_resource_matched_block': fair, 'actual_device_operation_and_readback': ready,
                                   'stronger_complete_stock_method': baseline['method'],
                                   'stronger_stock_whole_seconds': baseline['whole_seconds'],
                                   'gpu_whole_seconds': gpu['whole_seconds'],
                                   'gpu_reduction_vs_stronger_stock_percent': reduction,
                                   'cpu_control_whole_seconds': group['cpu']['whole_seconds'],
                                   'cpu_control_provider': group['cpu']['provider']['cumulative_per_pid_maxima_sum'],
                                   'scope': 'same compiled CPU bridge is an algorithm/lifetime control, not the main competing CPU baseline; all native fallback/final kernel costs retained'})
    planned = [f'{dataset}-{block}-{method}' for dataset in ('proofnet', 'minif2f')
               for block in ('rep0', 'rep1', 'rep2', 'profile')
               for method in ('warm', 'snapshot-cache', 'cpu', 'gpu')]
    missing = [label for label in planned if label not in by_label]
    return {'cells': cells, 'analysis_errors': failures, 'matched_stock_comparisons': comparisons,
            'historical_basic_comparisons': historical,
            'paired_whole_effects': paired_effects,
            'selected_run_order': [str(run) for run in runs], 'retained_duplicate_labels': retained_duplicate_labels,
            'missing_full_cells': missing, 'terminal_full_cells': sum(label in by_label for label in planned),
            'complete_full_matrix': not missing and all(by_label[label]['valid_complete'] for label in planned),
            'mini_historical_reference': 'No complete E014 mini native oracle is currently present; preserve all mini rows and use matched stock methods. A later source-native reference can be compared separately.',
            'planned_full_cells': 32, 'planned_full_outcomes': 220160,
            'scope': 'full native checking with original fallback/final kernel; GPU label requires actual native provider ready/calls/supported and zero CPU algorithm calls, not compilation or CPU-only fallback'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, action='append', required=True,
                        help='repeat for original scopes; first supplied run wins a duplicate label, retained paths reported')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.write_text(json.dumps(analyze_runs(args.run), indent=2) + '\n')


if __name__ == '__main__':
    main()
