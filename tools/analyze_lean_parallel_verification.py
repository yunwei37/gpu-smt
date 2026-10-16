#!/usr/bin/env python3
"""Recompute the declared whole-corpus branch/snapshot comparison.

Reads original capture artifacts; never launches a verifier or changes a plan.
Partial conditions have no whole-run rate. Resource profiles and uninstrumented
performance remain separate. Missing candidate clocks are not inferred from
native operation duration or attributed to a verifier stage.
"""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from analyze_lean_preparation import canonical, differences, distribution, interpret, task_grouping
from analyze_lean_prepared import oracle


def read_json(path):
    return json.loads(path.read_bytes()) if path.exists() else None


def read_lines(path):
    rows, errors = [], []
    if path.exists():
        for number, line in enumerate(path.read_bytes().splitlines(), 1):
            try:
                rows.append(json.loads(line))
            except (ValueError, UnicodeDecodeError) as error:
                errors.append(dict(file=str(path), line=number, error=str(error)))
    return rows, errors


def process_time(path):
    values = {}
    if path.exists():
        for line in path.read_text().splitlines():
            for text, key in [('User time (seconds):', 'user_seconds'),
                              ('System time (seconds):', 'system_seconds'),
                              ('Maximum resident set size (kbytes):', 'individual_max_rss_kib'),
                              ('Exit status:', 'exit_status')]:
                if line.strip().startswith(text):
                    try:
                        values[key] = float(line.strip()[len(text):])
                    except ValueError:
                        pass
    if 'user_seconds' in values and 'system_seconds' in values:
        values['waited_tree_cpu_seconds'] = values['user_seconds'] + values['system_seconds']
    values['rss_scope'] = 'individual-process maximum; not process-tree physical memory'
    return values


def recompute_resources(folder):
    path = folder / 'resources.jsonl'
    if not path.exists():
        return None
    samples, incomplete, peak_pss, peak_private = 0, 0, 0, 0
    durations, intervals, errors = [], [], []
    previous = None
    with path.open('rb') as stream:
        for number, line in enumerate(stream, 1):
            try:
                row = json.loads(line)
                processes = row['processes']
                pss = sum(x['memory_kib'].get('Pss', 0) for x in processes)
                private = sum(x['memory_kib'].get('Private_Clean', 0) + x['memory_kib'].get('Private_Dirty', 0) for x in processes)
                if pss != row['total_kib']['Pss'] or private != row['total_kib']['Private_Clean'] + row['total_kib']['Private_Dirty']:
                    errors.append(dict(line=number, error='sample totals differ from original per-process observations'))
                samples += 1; incomplete += bool(row['errors'])
                peak_pss = max(peak_pss, pss); peak_private = max(peak_private, private)
                durations.append(row['observation_end_ns'] - row['monotonic_ns'])
                if previous is not None:
                    intervals.append(row['monotonic_ns'] - previous)
                previous = row['monotonic_ns']
            except (ValueError, KeyError, TypeError) as error:
                errors.append(dict(line=number, error=repr(error)))
    metrics = dict(samples=samples, incomplete_samples=incomplete,
        sampled_peak_total_pss_kib=peak_pss, sampled_peak_total_private_kib=peak_private,
        observation_duration_ns=distribution(durations), sample_start_interval_ns=distribution(intervals),
        errors=errors, scope='recomputed own-tree non-atomic sampled observations; not exact peaks or newly created sharing')
    recorded = read_json(folder / 'resources-summary.json')
    metrics['recorded_summary'] = recorded
    metrics['recorded_summary_differences'] = differences({k:metrics[k] for k in
        ['samples','incomplete_samples','sampled_peak_total_pss_kib','sampled_peak_total_private_kib']},
        {k:(recorded or {}).get(k) for k in ['samples','incomplete_samples','sampled_peak_total_pss_kib','sampled_peak_total_private_kib']})
    return metrics


def response_outcome(response, status):
    if status != 'response':
        return status
    return interpret(response, dict(status='exited', returncode=0), None, 'fresh')['outcome']


def condition_rows(folder, method, expected):
    """Yield every source in the denominator, including missing/unknown rows."""
    issues = []
    returned = {}
    if method == 'branch':
        actual, errors = read_lines(folder / 'input.jsonl'); issues += errors
        records, errors = read_lines(folder / 'results.jsonl'); issues += errors
        for row in records:
            ordinal = row.get('ordinal')
            if ordinal in returned:
                issues.append(dict(error='duplicate terminal ordinal', ordinal=ordinal))
            returned[ordinal] = row
        extra = [i for i in returned if type(i) is not int or i not in range(len(expected))]
        if extra:
            issues.append(dict(error='extra terminal ordinals', ordinals=extra))
    else:
        actual = None
    rows = []
    for ordinal, source in enumerate(expected):
        native, response, record = None, None, None
        status, source_match = 'missing', False
        latency_ns, native_ns = None, None
        try:
            if method == 'branch':
                source_match = ordinal < len(actual) and actual[ordinal] == source
                record = returned.get(ordinal)
                if record is not None:
                    status = record.get('status', 'malformed_status')
                    if record.get('source_index') != source['index']:
                        status = 'source_index_mismatch'
                    native_ns = record.get('native_event', {}).get('elapsed_ns')
                    begin, end = record.get('admission_monotonic_ns'), record.get('terminal_observed_monotonic_ns')
                    if type(begin) is int and type(end) is int and end >= begin:
                        latency_ns = end - begin
                    if status == 'response':
                        payload = (folder / ('candidate-%08d.stdout.bin' % ordinal)).read_bytes()
                        envelope = json.loads(payload)
                        if envelope != record.get('native_response'):
                            issues.append(dict(error='native payload differs from result record', ordinal=ordinal))
                            status = 'native_payload_mismatch'
                        native = envelope['native']; response = native['response']
                        if native.get('index') != source['index']:
                            status = 'inner_source_index_mismatch'
            else:
                request = folder / ('request-%08d' % ordinal)
                source_match = read_json(request / 'stdin.bin') == dict(index=ordinal, code=source['code'], header=source['header'])
                record = read_json(request / 'result.json')
                if record is not None:
                    status = record.get('status', 'malformed_status')
                    if record.get('source_index') != ordinal:
                        status = 'source_index_mismatch'
                    latency_ns = record.get('invocation_elapsed_ns')
                    native_ns = record.get('native_operation_elapsed_ns')
                    if status == 'response':
                        envelope = read_json(request / 'native-record.bin')
                        native = envelope['record']['native']; response = read_json(request / 'response.bin')
                        if response != native['response']:
                            status = 'native_payload_mismatch'
                            issues.append(dict(error='native response differs from retained payload', ordinal=ordinal))
                        if native.get('index') != ordinal:
                            status = 'inner_source_index_mismatch'
            if record and record.get('error') and status == 'response':
                status = 'adapter_error'
        except (OSError, ValueError, KeyError, TypeError) as error:
            status = 'malformed_or_missing_capture'
            issues.append(dict(ordinal=ordinal, error=repr(error)))
        outcome = response_outcome(response, status)
        rows.append(dict(ordinal=ordinal, source_index=source['index'], source_matches=source_match,
            terminal_record=record is not None, native_status=status, outcome=outcome, response=response,
            admission_to_terminal_ns=latency_ns, native_operation_ns=native_ns,
            final_command_state=native.get('final_command_state') if isinstance(native, dict) else None,
            import_diagnostics=native.get('import_diagnostics') if isinstance(native, dict) else None,
            old_snapshot_supplied=native.get('old_snapshot_supplied') if isinstance(native, dict) else None,
            reused_command_snapshot_prefix=native.get('reused_command_snapshot_prefix') if isinstance(native, dict) else None))
    return rows, issues


def analyze_condition(folder, method, expected, observations, driver_record=None):
    rows, issues = condition_rows(folder, method, expected)
    comparisons = Counter()
    for row, original in zip(rows, observations):
        response, oracle_outcome = original
        comparable = row['source_matches'] and row['outcome'] in ['complete', 'incomplete', 'rejected'] and response is not None
        delta = differences(canonical(response), canonical(row['response'])) if comparable else None
        row.update(oracle_outcome=oracle_outcome, comparison='equal' if comparable and not delta else
                   'response_difference' if comparable else 'unknown', difference_paths=delta)
        comparisons[row['comparison']] += 1
    events, errors = read_lines(folder / ('native-events.jsonl' if method == 'branch' else 'events.jsonl')); issues += errors
    receipt = read_json(folder / 'receipt.json') if method == 'branch' else None
    if method == 'branch':
        native_terminal = bool(receipt and receipt.get('returncode') == 0 and receipt.get('reason') == 'native_exit'
            and not receipt.get('error') and not receipt.get('signals') and not receipt.get('active_children')
            and not receipt.get('unfinished_preparation'))
        provenance = receipt
    else:
        shutdown = [x for x in events if x.get('event') == 'shutdown']
        done = [x.get('source_index') for x in events if x.get('event') == 'whole_job_end']
        native_terminal = len(shutdown) == 1 and not shutdown[0].get('interrupted_signals') and Counter(done) == Counter(range(len(expected)))
        runs = [x for x in events if x.get('event') == 'run']; provenance = runs[0] if len(runs) == 1 else None
    driver_record = driver_record or {}
    whole_ns = driver_record.get('whole_command_elapsed_ns')
    if whole_ns is None and type(driver_record.get('begin_monotonic_ns')) is int and type(driver_record.get('end_monotonic_ns')) is int:
        whole_ns = driver_record['end_monotonic_ns'] - driver_record['begin_monotonic_ns']
    whole_complete = bool(native_terminal and all(x['terminal_record'] for x in rows)
        and driver_record.get('status') == 'terminal' and driver_record.get('returncode') == 0
        and type(whole_ns) is int and whole_ns > 0)
    resources = recompute_resources(folder)
    responses = sum(x['native_status'] == 'response' and x['outcome'] in ['complete', 'incomplete', 'rejected'] for x in rows)
    metrics = dict(whole_command_elapsed_ns=whole_ns if whole_complete else None,
        terminal_attempts_per_second=len(expected) * 1e9 / whole_ns if whole_complete else None,
        native_responses_per_second=responses * 1e9 / whole_ns if whole_complete else None,
        admission_to_terminal_distribution=distribution(x['admission_to_terminal_ns'] for x in rows),
        native_operation_distribution=distribution(x['native_operation_ns'] for x in rows),
        candidate_clock_missing=sum(x['terminal_record'] and x['admission_to_terminal_ns'] is None for x in rows))
    summary = dict(expected_sources=len(expected), terminal_records=sum(x['terminal_record'] for x in rows),
        native_terminal=native_terminal, whole_condition_complete=whole_complete,
        comparisons=dict(comparisons), outcomes=dict(Counter(x['outcome'] for x in rows)),
        sources_unobserved_or_mismatched=sum(not x['source_matches'] for x in rows),
        nonfinal_native_responses=sum(x['native_status'] == 'response' and x['final_command_state'] is not True for x in rows),
        snapshot_supplied=sum(x['old_snapshot_supplied'] is True for x in rows),
        protocol_issues=issues, driver=driver_record, provenance=provenance, metrics=metrics, resources=resources,
        process_time=process_time(folder.parent / (folder.name + '.process-time.txt')),
        scope='whole external command; profiles separate; partial/unknown rows retained; missing candidate clocks not inferred')
    return rows, summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['run', 'inputs', 'fresh', 'out']:
        ap.add_argument('--' + name, type=Path, required=True)
    args = ap.parse_args()
    codes = read_json(args.inputs / 'to_inference_codes.json'); tasks = read_json(args.inputs / 'selected_tasks.json')
    contexts, grouping = task_grouping(tasks, codes)
    expected = [dict(index=i, code=c['code'], header=contexts[i]['header']) for i, c in enumerate(codes)]
    observations = [oracle(args.fresh, i, c['code']) for i, c in enumerate(codes)]
    driver = read_json(args.run / 'summary.json') or {}
    args.out.mkdir(parents=True, exist_ok=False)
    conditions = {}
    with (args.out / 'per-input.csv').open('x', newline='') as stream:
        keys = ['condition', 'ordinal', 'source_index', 'source_matches', 'terminal_record', 'native_status', 'outcome',
                'oracle_outcome', 'comparison', 'difference_paths', 'admission_to_terminal_ns', 'native_operation_ns',
                'final_command_state', 'old_snapshot_supplied', 'reused_command_snapshot_prefix']
        writer = csv.DictWriter(stream, fieldnames=keys, extrasaction='ignore'); writer.writeheader()
        for arm in ['performance', 'resources']:
            for repeat in range(3):
                for width in [1, 2, 4]:
                    for method in ['branch', 'snapshot']:
                        label = f'{arm}-rep{repeat}-w{width}-{method}'
                        rows, summary = analyze_condition(args.run / label, method, expected, observations,
                            driver.get('cases', {}).get(label))
                        summary.update(arm=arm, repeat=repeat, width=width, method=method)
                        conditions[label] = summary
                        for row in rows:
                            row['condition'] = label
                            row['difference_paths'] = json.dumps(row['difference_paths'])
                            writer.writerow(row)
    pairs = []
    for arm in ['performance', 'resources']:
        for width in [1, 2, 4]:
            for repeat in range(3):
                left = conditions[f'{arm}-rep{repeat}-w{width}-branch']; right = conditions[f'{arm}-rep{repeat}-w{width}-snapshot']
                ratio = None
                if arm == 'performance' and left['whole_condition_complete'] and right['whole_condition_complete']:
                    ratio = right['metrics']['whole_command_elapsed_ns'] / left['metrics']['whole_command_elapsed_ns']
                pairs.append(dict(arm=arm, width=width, repeat=repeat, snapshot_over_branch_whole_time=ratio,
                    branch_complete=left['whole_condition_complete'], snapshot_complete=right['whole_condition_complete'],
                    branch_feedback=left['comparisons'], snapshot_feedback=right['comparisons']))
    summary = dict(scope='one complete dataset within the unchanged two-dataset72-condition experiment; no service/RQ closure',
        input_grouping=grouping, source_count=len(codes), oracle_outcomes=dict(Counter(x[1] for x in observations)),
        conditions=conditions, pairs=pairs, all36conditions_complete=all(x['whole_condition_complete'] for x in conditions.values()),
        comparison_policy='existing canonical/differences; only uncontinued env/proofState handles ignored',
        limitations=['three repetitions are individual paired observations, not tight significance',
            'resource profiles never supply uninstrumented throughput or a simultaneous memory/performance frontier',
            'original unknown/missing feedback is not equality or rejection',
            'native elapsed duration is not a replacement for unobserved admission-to-terminal clocks'])
    (args.out / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
    lines = ['# Whole Lean branch/snapshot capture analysis', '', summary['scope'], '',
        f"Sources: {len(codes)}. Whole conditions complete: {sum(x['whole_condition_complete'] for x in conditions.values())}/36.",
        f"Original oracle outcomes: {summary['oracle_outcomes']}", '',
        '| Condition | Whole complete | Responses / s | Equal | Different | Unknown | Missing candidate clocks |',
        '|---|---|---|---:|---:|---:|---:|']
    for label, item in conditions.items():
        m=item['metrics']; c=item['comparisons']
        rate=m['native_responses_per_second'] if item['arm']=='performance' else None
        lines.append(f"| {label} | {item['whole_condition_complete']} | {rate} | {c.get('equal',0)} | {c.get('response_difference',0)} | {c.get('unknown',0)} | {m['candidate_clock_missing']} |")
    lines += ['', *summary['limitations'], '', 'Raw resources, CPU, commands, individual repeats and exceptions: summary.json. Full source denominator: per-input.csv.']
    (args.out / 'README.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['conditions','pairs']}, indent=2))


if __name__ == '__main__':
    main()
