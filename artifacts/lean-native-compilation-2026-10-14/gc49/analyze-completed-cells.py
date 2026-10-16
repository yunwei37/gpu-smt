"""Offline completed-cell analysis for the producer-compatible miniF2F GC matrix."""
from pathlib import Path
import collections
import datetime
import importlib.util
import json
import statistics
import zipfile

ROOT = Path('/workspaces/repository')
OUT = Path(__file__).parent
BASE = OUT / 'full1'
spec = importlib.util.spec_from_file_location(
    'completed_native_gc_cells',
    ROOT / 'artifacts/lean-modern-native-compilation-2026-10-14/analyze-gc2.py',
)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)

cells = {}
for path in sorted(BASE.glob('*.terminal.json')):
    terminal = json.loads(path.read_text())
    try:
        cells[terminal['label']] = native.load_cell(BASE, terminal)
    except (FileNotFoundError, zipfile.BadZipFile) as error:
        cells[terminal['label']] = {
            'label': terminal['label'], 'valid_complete': False,
            'raw_finalize_pending': str(error),
        }

pairs = []
for rep in range(3):
    labels = [f'minif2f-rep{rep}-{method}' for method in ('original', 'compiled')]
    if not all(label in cells and cells[label]['valid_complete'] for label in labels):
        continue
    reference, candidate = (cells[label] for label in labels)
    # These recorded fields describe the same capture; process identity/method vary.
    commands = [
        {key: value for key, value in cell['command'].items()
         if key not in ('pid', 'method')}
        for cell in (reference, candidate)
    ]
    changes = [
        {'source_index': index, 'reference': basic,
         'candidate': candidate['basic_rows'].get(index)}
        for index, basic in reference['basic_rows'].items()
        if basic != candidate['basic_rows'].get(index)
    ]
    pairs.append({
        'rep': rep,
        'commands_match_except_pid_method': commands[0] == commands[1],
        'reference_seconds': reference['whole_seconds'],
        'candidate_seconds': candidate['whole_seconds'],
        'wall_reduction_percent':
            100 * (1 - candidate['whole_seconds'] / reference['whole_seconds']),
        'basic_differences': changes,
        'basic_transition_counts': dict(collections.Counter(
            f"{item['reference']}->{item['candidate']}" for item in changes)),
        'native_payload_difference_indices': [
            index for index, body in reference['native_rows'].items()
            if body != candidate['native_rows'].get(index)
        ],
        'reference_request_latency': reference['request_latency_seconds'],
        'candidate_request_latency': candidate['request_latency_seconds'],
    })

qualified = [pair for pair in pairs if pair['commands_match_except_pid_method']]
values = [pair['wall_reduction_percent'] for pair in qualified]
result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': (
        'All original 7808 miniF2F source attempts, producer4.9 GC backend, '
        'selective native arithmetic compilation only in the candidate. '
        'Exact source bytes/order and native payloads use the existing loader; '
        'only adapter-inserted time is excluded from native comparison. '
        'Primary whole clocks include startup/import/loading, verification, '
        'HTTP/raw/logging, replacement and shutdown/EOF; build and ZIP are '
        'separate. Four closed-loop requests overlap. Shared background is '
        'not exclusive hardware; profiles are separate. No partial-clock '
        'gain, task pass@32, GPU benefit or final RQ/novelty claim.'
    ),
    'completed_terminal_cells': len(cells), 'planned_cells': 8,
    'completed_valid_cells': sum(bool(cell.get('valid_complete')) for cell in cells.values()),
    'all_planned_complete': len(cells) == 8 and all(
        cell.get('valid_complete') for cell in cells.values()),
    'primary_pairs': pairs,
    'qualified_primary_pairs': len(qualified),
    'mean_wall_reduction_percent': statistics.mean(values) if values else None,
    'observed_range_percent': [min(values), max(values)] if values else None,
    'uncertainty': 'Descriptive whole-pair range, not a confidence interval; three pairs and profiles are planned.',
    'cells': {
        label: {key: value for key, value in cell.items()
                if key not in ('basic_rows', 'native_rows', 'legacy_rows')}
        for label, cell in cells.items()
    },
}
(OUT / 'complete-cells-analysis.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: result[key] for key in (
    'completed_valid_cells', 'planned_cells', 'all_planned_complete',
    'qualified_primary_pairs', 'mean_wall_reduction_percent')}, indent=2))
