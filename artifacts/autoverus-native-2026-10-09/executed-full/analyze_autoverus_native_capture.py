#!/usr/bin/env python3
"""Describe retained native replay observations; never execute inputs or decide gates."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
import statistics

from analyze_smt_trace import split_commands, command_head


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path, errors):
    try:
        return json.loads(path.read_bytes())
    except (OSError, ValueError, UnicodeError) as exc:
        errors.append(f'{path}: {exc}')
        return None


def semantic(value):
    if not isinstance(value, dict):
        raise ValueError('native stdout JSON is not an object')
    result = {k: v for k, v in value.items() if k != 'times-ms'}
    modules = value.get('times-ms', {}).get('smt', {}).get('smt-run-module-times', [])
    result['observed-function-identities'] = sorted([
        {'module': m.get('module'), 'functions': sorted([
            {k: f[k] for k in ('function', 'success') if k in f}
            for f in m.get('function-breakdown', [])], key=lambda f: json.dumps(f, sort_keys=True))}
        for m in modules], key=lambda m: str(m['module']))
    return result


def gnu_time(path, errors):
    fields = {'User time (seconds)': 'os_user_cpu_s',
              'System time (seconds)': 'os_system_cpu_s',
              'Maximum resident set size (kbytes)': 'os_maxrss_kib'}
    result = {}
    try:
        for line in path.read_text().splitlines():
            for label, key in fields.items():
                if line.strip().startswith(label + ':'):
                    result[key] = float(line.split(':', 1)[1].strip())
    except (OSError, ValueError) as exc:
        errors.append(f'{path}: {exc}')
    return result


def snapshot(call, trace, meta, errors):
    obs = meta.get('first_done')
    if obs is None:
        return
    call['snapshot_errors'] = obs.get('errors', [])
    for key in ('sampling_duration_s', 'launch_to_done_observed_s',
                'first_stdin_to_done_observed_s', 'stdin_forwarded_bytes',
                'clock_ticks_per_second'):
        call[key] = obs.get(key)
    directory = trace.parent / (trace.name.removesuffix('.meta.json') + '.first-done')
    def data(label):
        info = obs.get('files', {}).get(label)
        if info is None:
            return None
        try:
            return (directory / info['path']).read_bytes()
        except OSError as exc:
            errors.append(str(exc))
            return None
    raw = data('stat')
    if raw:
        try:
            fields = raw.decode().rsplit(')', 1)[1].split()
            ticks = int(fields[11]) + int(fields[12])
            call['live_process_cpu_ticks'] = ticks
            hz = obs.get('clock_ticks_per_second')
            if hz:
                call['tick_resolution_s'] = 1 / hz
                call['live_process_cpu_s'] = ticks / hz
                call['tick_quantization_interval_s'] = [max(0, ticks - 2) / hz, (ticks + 2) / hz]
        except (ValueError, IndexError, UnicodeError) as exc:
            errors.append(f'proc stat: {exc}')
    for label, keys in [('status', {'VmRSS': 'live_rss_kib'}),
                        ('smaps_rollup', {'Pss': 'live_pss_kib', 'Rss': 'smaps_rss_kib'})]:
        raw = data(label)
        if raw:
            try:
                for line in raw.decode().splitlines():
                    name, _, value = line.partition(':')
                    if name in keys:
                        call[keys[name]] = int(value.split()[0])
            except (ValueError, UnicodeError) as exc:
                errors.append(f'{label}: {exc}')
    tids = [key for key in obs.get('files', {}) if key.startswith('task-') and key.endswith('-schedstat')]
    times = []
    for tid in tids:
        raw = data(tid)
        try:
            times.append(int(raw.split()[0]) if raw else None)
        except (ValueError, IndexError) as exc:
            errors.append(f'{tid}: {exc}')
            times.append(None)
    call['live_tid_count_observed'] = len(tids)
    call['live_tid_schedstat_ns'] = sum(times) if times and all(x is not None for x in times) else None
    try:
        raw_input = trace.with_name(trace.name.removesuffix('.meta.json') + '.stdin.bin').read_bytes()
        n = obs['stdin_forwarded_bytes']
        if not isinstance(n, int) or n < 0 or n > len(raw_input):
            raise ValueError('first DONE prefix length unavailable/outside retained input')
        prefix = raw_input[:n]
        call['prefix_sha256'] = sha(prefix)
        raw_output = trace.with_name(trace.name.removesuffix('.meta.json') + '.stdout.bin').read_bytes()
        end = obs.get('stdout_marker_end_bytes')
        first_marker = re.search(rb'(?m)^<<DONE>>\n', raw_output)
        call['original_done_marker_matches'] = (isinstance(end, int) and first_marker is not None
            and first_marker.end() == end)
        call['prefix_bytes'] = n
        commands = split_commands(prefix.decode('utf-8', errors='strict'))
        checks = [command_head(c) for c in commands if command_head(c) in
                  ('check-sat', 'check-sat-assuming')]
        call['prefix_check_commands'] = checks
        call['prefix_has_no_checks'] = not checks
    except (OSError, ValueError, KeyError, UnicodeError) as exc:
        errors.append(f'prefix observation: {exc}')


def distribution(rows, key):
    values = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
    return {'observed': len(values), 'unknown': len(rows) - len(values),
            'sum_observed': sum(values) if values else None,
            'min': min(values) if values else None,
            'median': statistics.median(values) if values else None,
            'max': max(values) if values else None}


def write_rows(path, rows):
    keys = sorted({key for row in rows for key in row})
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, sort_keys=True) if isinstance(v, (list, dict)) else v
                             for k, v in row.items()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runroot', type=Path)
    parser.add_argument('--out', type=Path, help='ordinary analysis directory (default runroot/analysis)')
    args = parser.parse_args()
    root = args.runroot.resolve()
    errors = []
    metadata = read_json(root / 'metadata.json', errors)
    if metadata is None:
        parser.error('cannot read retained metadata.json')
    out = args.out or root / 'analysis'
    out.mkdir(parents=True, exist_ok=True)
    candidates = {c['index']: c for c in metadata['candidates']}
    cells, calls, observations = [], [], {}
    cell_groups = {}
    source_groups = {}
    for index in metadata['selected_indices']:
        source_groups.setdefault(candidates[index]['source_sha256'], []).append(index)
    for repeat in range(int(metadata['arguments']['repeat'])):
        for index in metadata['selected_indices']:
            candidate = candidates[index]
            for condition in ('direct', 'capture'):
                directory = root / f'repeat-{repeat}' / condition / f'{index:05d}'
                local_errors = []
                receipt = read_json(directory / 'receipt.json', local_errors)
                row = dict(repetition=repeat, candidate=index, condition=condition,
                           source_sha256=candidate['source_sha256'], source_bytes=candidate['bytes'],
                           source_relative_path=candidate['source_relative_path'], context_key=candidate['context_key'],
                           receipt=receipt, receipt_present=receipt is not None)
                try:
                    actual = Path(candidate['input']).read_bytes()
                    row.update(retained_source_sha256=sha(actual), retained_source_bytes=len(actual),
                               source_identity_matches=sha(actual) == candidate['source_sha256'] and len(actual) == candidate['bytes'])
                except OSError as exc:
                    local_errors.append(str(exc))
                if receipt:
                    for k in ('returncode', 'timed_out', 'complete', 'external_wall_s', 'exception'):
                        row[k] = receipt.get(k)
                row.update(gnu_time(directory / 'time.txt', local_errors))
                stdout = native = oracle = stderr = None
                try:
                    stdout = (directory / 'stdout.bin').read_bytes()
                    row['stdout_sha256'] = sha(stdout)
                    native = json.loads(stdout)
                    oracle = semantic(native)
                    row['native_json'] = native
                    row['semantic_observation'] = oracle
                except (OSError, ValueError, UnicodeError, AttributeError, TypeError) as exc:
                    local_errors.append(f'native JSON: {exc}')
                try:
                    stderr = (directory / 'stderr.bin').read_bytes()
                    row['stderr_sha256'] = sha(stderr)
                    row['stderr_bytes'] = len(stderr)
                except OSError as exc:
                    local_errors.append(str(exc))
                observations[(repeat, index, condition)] = (oracle, stderr, row)
                cell_calls = []
                if condition == 'capture':
                    for trace in sorted((directory / 'traces').glob('*.meta.json')):
                        call_errors = []
                        meta = read_json(trace, call_errors)
                        call = dict(repetition=repeat, candidate=index, context_key=candidate['context_key'],
                                    source_sha256=candidate['source_sha256'], trace=str(trace), metadata=meta)
                        if meta:
                            for k in ('argv', 'complete', 'returncode', 'elapsed_s', 'user_cpu_s',
                                      'system_cpu_s', 'maxrss_kib', 'invocation_kind', 'errors'):
                                call[k] = meta.get(k)
                            snapshot(call, trace, meta, call_errors)
                        call['analysis_errors'] = call_errors
                        calls.append(call)
                        cell_calls.append(call)
                row['analysis_errors'] = local_errors
                if condition == 'capture':
                    row['native_call_receipts'] = len(cell_calls)
                    row['native_calls_terminal_observed'] = sum(c.get('returncode') is not None for c in cell_calls)
                    for key in ('user_cpu_s', 'system_cpu_s'):
                        values = [c.get(key) for c in cell_calls]
                        row['native_sum_' + key] = (sum(values) if values and all(isinstance(v, (int, float)) for v in values) else None)
                cells.append(row)
                cell_groups.setdefault((index, condition), []).append(row)
    for row in cells:
        if row['condition'] != 'capture':
            continue
        oracle, stderr, _ = observations[(row['repetition'], row['candidate'], 'capture')]
        direct, direct_stderr, direct_row = observations[(row['repetition'], row['candidate'], 'direct')]
        row['non_time_json_equal_direct'] = oracle == direct if oracle is not None and direct is not None else None
        row['raw_stderr_equal_direct'] = stderr == direct_stderr if stderr is not None and direct_stderr is not None else None
        row['exit_equal_direct'] = (row['returncode'] == direct_row['returncode']
                                   if row.get('returncode') is not None and direct_row.get('returncode') is not None else None)
        comparisons = [row[k] for k in ('non_time_json_equal_direct', 'raw_stderr_equal_direct', 'exit_equal_direct')]
        row['comparison_identity'] = 'different' if False in comparisons else ('equal' if all(x is True for x in comparisons) else 'unknown')
    # Repetitions are observations of the same candidate, never reuse opportunities.
    seen = {}
    valid_preparation = []
    configuration = {k: metadata.get(k) for k in ('verus_sha256', 'z3_sha256', 'affinity', 'environment')}
    for call in calls:
        call['reuse_previous_candidates'] = []
        call['source_duplicate_previous_candidates'] = []
        paired_row = observations[(call['repetition'], call['candidate'], 'capture')][2]
        meta = call.get('metadata') or {}
        receipt = paired_row.get('receipt') or {}
        reasons = []
        if call.get('invocation_kind') != 'solver':
            reasons.append('not SMT solver invocation')
        if call.get('original_done_marker_matches') is not True:
            reasons.append('original first DONE marker missing or mismatched')
        if call.get('prefix_has_no_checks') is not True:
            reasons.append('no-check prefix not established')
        if call.get('prefix_sha256') is None or call.get('argv') is None:
            reasons.append('literal prefix or native argv missing')
        if meta.get('complete') is not True or call.get('returncode') != 0:
            reasons.append('native child incomplete or abnormal')
        for name in ('stdin', 'stdout', 'stderr'):
            stream = meta.get('streams', {}).get(name, {})
            if stream.get('eof') is not True or stream.get('forwarded_all') is not True:
                reasons.append(f'{name} stream incomplete')
        if not receipt.get('complete') or receipt.get('timed_out') or receipt.get('exception'):
            reasons.append('candidate receipt missing, incomplete or censored')
        if receipt.get('returncode') not in (0, 1):
            reasons.append('candidate abnormal exit')
        if paired_row.get('source_identity_matches') is not True:
            reasons.append('retained source identity unestablished')
        if call.get('errors') or call.get('snapshot_errors') or call.get('analysis_errors'):
            reasons.append('native capture, snapshot or analysis errors')
        for key in ('sampling_duration_s', 'live_process_cpu_s', 'live_tid_schedstat_ns',
                    'live_rss_kib', 'live_pss_kib', 'launch_to_done_observed_s',
                    'first_stdin_to_done_observed_s'):
            if not isinstance(call.get(key), (int, float)):
                reasons.append(f'required sampling metric missing: {key}')
        call['preparation_rejection_reasons'] = reasons
        call['valid_preparation_observation'] = not reasons
        call['feedback_comparison_identity'] = paired_row.get('comparison_identity', 'unknown')
        if reasons:
            call['reuse_observation'] = 'invalid or missing preparation observation'
            continue
        valid_preparation.append(call)
        key = json.dumps([call['repetition'], configuration, call['argv'], call['prefix_sha256'], call['prefix_bytes']], sort_keys=True)
        previous = [p for p in seen.get(key, []) if p['candidate'] < call['candidate']]
        call['reuse_previous_candidates'] = sorted({p['candidate'] for p in previous if p['source_sha256'] != call['source_sha256']})
        call['source_duplicate_previous_candidates'] = sorted({p['candidate'] for p in previous if p['source_sha256'] == call['source_sha256']})
        different = [p for p in previous if p['source_sha256'] != call['source_sha256']]
        call['reuse_same_context_candidates'] = sorted({p['candidate'] for p in different if p['context_key'] == call['context_key']})
        call['reuse_across_context_candidates'] = sorted({p['candidate'] for p in different if p['context_key'] != call['context_key']})
        call['reuse_observation'] = 'hit' if different else 'no previously seen different source'
        seen.setdefault(key, []).append(call)
    variance = []
    for index in metadata['selected_indices']:
        for condition in ('direct', 'capture'):
            group = cell_groups[(index, condition)]
            variance.append(dict(candidate=index, condition=condition, repetitions=[r['repetition'] for r in group],
                                 semantic_observations=[r.get('semantic_observation') for r in group],
                                 stderr_identities=[r.get('stderr_sha256') for r in group],
                                 exits=[r.get('returncode') for r in group],
                                 external_wall_s=distribution(group, 'external_wall_s')))
    hits = [c for c in calls if c.get('reuse_observation') == 'hit']
    summary = dict(expected_cells=len(cells), observed_receipts=sum(r['receipt_present'] for r in cells),
                   metadata_complete=metadata.get('complete'), errors=errors,
                   comparison_identities={status: [[r['candidate'], r['repetition']] for r in cells
                                          if r.get('comparison_identity') == status]
                                          for status in ('equal', 'different', 'unknown')},
                   cell_costs={condition: {k: distribution([r for r in cells if r['condition'] == condition], k)
                               for k in ('external_wall_s', 'os_user_cpu_s', 'os_system_cpu_s', 'os_maxrss_kib')}
                               for condition in ('direct', 'capture')},
                   native_call_count=len(calls), opportunity_hit_calls=len(hits),
                   native_all_lifetime_costs={k: distribution(calls, k) for k in
                                 ('user_cpu_s', 'system_cpu_s', 'maxrss_kib')},
                   all_snapshot_descriptions={k: distribution(calls, k) for k in
                                 ('live_process_cpu_s', 'live_tid_schedstat_ns', 'live_rss_kib', 'live_pss_kib')},
                   valid_preparation_count=len(valid_preparation),
                   invalid_or_missing_preparation_count=len(calls) - len(valid_preparation),
                   valid_preparation_costs={k: distribution(valid_preparation, k) for k in
                                 ('live_process_cpu_s', 'live_tid_schedstat_ns', 'live_rss_kib', 'live_pss_kib',
                                  'launch_to_done_observed_s', 'first_stdin_to_done_observed_s')},
                   valid_preparation_feedback_groups={identity: {
                       'calls': [[c['repetition'], c['candidate'], c['trace']] for c in valid_preparation
                                 if c['feedback_comparison_identity'] == identity],
                       'opportunity_hit_calls': [[c['repetition'], c['candidate'], c['trace']] for c in hits
                                 if c['feedback_comparison_identity'] == identity]}
                       for identity in ('equal', 'different', 'unknown')},
                   conditional_reused_observed_costs={k: distribution(hits, k) for k in
                                                   ('live_process_cpu_s', 'live_tid_schedstat_ns')},
                   source_duplicate_groups=[{'source_sha256': digest, 'candidates': sorted(indices)}
                       for digest, indices in source_groups.items() if len(indices) > 1])
    for name, value in [('cells', cells), ('native-calls', calls), ('repeat-variance', variance), ('summary', summary)]:
        (out / f'{name}.json').write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    write_rows(out / 'cells.csv', cells)
    write_rows(out / 'native-calls.csv', calls)
    (out / 'description.md').write_text(
        '# Retained native observations\n\n'
        f'Expected cells: {len(cells)}; receipts: {summary["observed_receipts"]}; native call receipts: {len(calls)}. '
        'All selected candidates, repetitions, paths, failures and missing cells remain in cells.json. '
        'Comparison identities describe equality of observations and do not establish semantic soundness.\n\n'
        'Primary whole-invocation costs are external wall time and GNU time user/system CPU and maximum RSS. '
        'Native wait4 costs include every retained native call, including version calls. Missing values are unknown; '
        'sums report observed coverage only. Native JSON milliseconds are truncated, overlapping subset diagnostics. '
        'smt-init excludes the initial prelude startup and main aggregates omit function buckets.\n\n'
        'First DONE prefixes are exact raw first N bytes after the original initial flush. Command inspection is observation only. '
        'Snapshots are sequential live process observations; errors and sampling duration are retained. Process ticks are quantized; '
        'the reported interval allows two tick truncations and is not a measurement-error bound. Live TID schedstat omits departed '
        'threads and must not substitute for process lifetime CPU. RSS/PSS are live snapshots, not peaks.\n\n'
        'Literal prefix plus native argv identity under the recorded fixed configuration identifies previously seen '
        'different candidates and source hashes, with exact source duplicates separate and context breakouts retained. '
        'Recurrence histories reset per repetition and use only earlier distinct candidate indices. Sorted saved corpus and repetitions are not historical traffic. Only explicitly valid preparation observations enter recurrence and preparation cost summaries; surviving partial metrics are separately descriptive. Feedback equality groups remain separate and do not prove soundness. Hit costs are conditional ideal-retention upper '
        'opportunities, not bounded service benefits; they imply no per-check uniformity or complete RQ answer. '
        'No verdict or gate is decided by this analysis.\n')
    print(out)


if __name__ == '__main__':
    main()
