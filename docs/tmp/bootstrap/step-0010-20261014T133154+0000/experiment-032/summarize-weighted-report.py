"""Summarize exclusive perf leaf weights; no recording or native execution."""
import argparse
import collections
import datetime
import gzip
import json
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('report', type=Path, help='Completed tab-separated weighted perf report, gzip compressed')
parser.add_argument('output_prefix', type=Path)
args = parser.parse_args()
groups = {name: collections.defaultdict(lambda: [0, 0])
          for name in ('comm', 'tid_comm', 'native_dso')}
native_symbols = []
header = None
lost = None
reported_period = None
samples_label = None
samples = period = native_samples = native_period = 0
unknown_dso_period = unknown_symbol_period = 0
native_unknown_dso_period = native_unknown_symbol_period = 0
rows = 0
required = ('Samples', 'Period', 'Command', 'Pid:Command', 'Shared Object', 'Symbol')
with gzip.open(args.report, 'rt') as report:
    for line in report:
        text = line.rstrip('\n')
        if text.startswith('#'):
            content = text[1:].strip()
            if content.startswith('Total Lost Samples:'):
                lost = content.split(':', 1)[1].strip()
            if content.startswith('Event count (approx.):'):
                reported_period = int(content.split(':', 1)[1].strip())
            if content.startswith('Samples:'):
                samples_label = content
            if '\t' in content:
                fields = [field.strip() for field in content.split('\t')]
                if all(name in fields for name in required):
                    header = {name: fields.index(name) for name in required}
            continue
        if not text.strip():
            continue
        if header is None:
            raise ValueError('Data before the expected weighted report header')
        fields = [field.strip() for field in text.split('\t')]
        if len(fields) <= max(header.values()):
            raise ValueError('Incomplete report row: ' + repr(text))
        count, weight = (int(fields[header[name]]) for name in ('Samples', 'Period'))
        assert count >= 0 and weight >= 0
        comm, tid, dso, symbol = (fields[header[name]] for name in required[2:])
        samples += count
        period += weight
        rows += 1
        for key, value in (('comm', comm), ('tid_comm', tid)):
            group = groups[key][value]
            group[0] += count
            group[1] += weight
        unresolved_dso = dso == '[unknown]'
        unresolved_symbol = '[unknown]' in symbol or bool(
            re.fullmatch(r'(?:\[[.k]\]\s*)?0x[0-9a-fA-F]+', symbol))
        unknown_dso_period += weight if unresolved_dso else 0
        unknown_symbol_period += weight if unresolved_symbol else 0
        if comm == 'native-repl':
            native_samples += count
            native_period += weight
            group = groups['native_dso'][dso]
            group[0] += count
            group[1] += weight
            native_unknown_dso_period += weight if unresolved_dso else 0
            native_unknown_symbol_period += weight if unresolved_symbol else 0
            native_symbols.append({
                'tid_comm': tid, 'dso': dso, 'symbol': symbol,
                'samples': count, 'period': weight,
            })
assert header is not None, 'Missing weighted report header'
symbol_path = Path(str(args.output_prefix) + '.native-symbols.jsonl.gz')
with gzip.open(symbol_path, 'wt') as output:
    for row in sorted(native_symbols, key=lambda row: row['period'], reverse=True):
        output.write(json.dumps(row) + '\n')
def group_rows(key):
    denominator = native_period if key == 'native_dso' else period
    return [
        {'name': name, 'samples': value[0], 'period': value[1],
         'recorded_period_fraction': value[1] / denominator if denominator else None}
        for name, value in sorted(groups[key].items(), key=lambda item: item[1][1], reverse=True)
    ]
result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_report': str(args.report), 'exclusive_leaf_rows': rows,
    'samples': samples, 'summed_leaf_period': period,
    'reported_event_period_approx': reported_period,
    'leaf_period_matches_reported_event_period': period == reported_period,
    'reported_samples_label': samples_label, 'reported_lost_samples': lost,
    'native_comm': 'native-repl', 'native_samples': native_samples,
    'native_period': native_period,
    'native_recorded_period_fraction': native_period / period if period else None,
    'unknown_dso_period': unknown_dso_period,
    'unknown_symbol_period': unknown_symbol_period,
    'native_unknown_dso_period': native_unknown_dso_period,
    'native_unknown_symbol_period': native_unknown_symbol_period,
    'by_comm': group_rows('comm'), 'by_tid_comm': group_rows('tid_comm'),
    'native_by_dso': group_rows('native_dso'),
    'native_symbol_rows': str(symbol_path),
    'scope': (
        'Exclusive recorded user-CPU sample periods only. Unknowns remain in '
        'denominators; DSO and symbol unknown weights may overlap. The perf pid '
        'sort column contains task TIDs. TID/comm groups are not proof/source '
        'attribution or unique process lifetimes. Native includes runtime/library CPU, '
        'not only kernel checking. Sampling loss, attach gaps, startup and observer cost need the capture '
        'receipt. No inclusive callchain sum, whole-wall decomposition, '
        'GPU eligibility/Amdahl bound, speedup or corpus result from controls.'
    ),
}
Path(str(args.output_prefix) + '.summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: result[key] for key in (
    'exclusive_leaf_rows', 'samples', 'summed_leaf_period',
    'leaf_period_matches_reported_event_period', 'reported_lost_samples')}))
