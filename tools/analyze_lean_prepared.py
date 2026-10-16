#!/usr/bin/env python3
"""Recompute source-matched native-response fidelity; never infer speedup.

Absent, malformed, timeout and producer-unknown rows stay in each full1024
source denominator. A terminal driver is not proof of complete responses.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from analyze_lean_preparation import canonical, differences, interpret


def load(path):
    return json.loads(path.read_bytes()) if path.exists() else None


def oracle(fresh, index, expected_code):
    folder = fresh / ('request-%08d' % index)
    result = load(folder / 'result.json')
    if result is None:
        return None, 'missing'
    try:
        submitted = load(folder / 'stdin.bin')
        if not isinstance(submitted, dict) or submitted.get('cmd') != expected_code:
            return None, 'oracle_source_mismatch'
    except (ValueError, KeyError, TypeError):
        return None, 'malformed_oracle_submission'
    response, parse_error = None, None
    try:
        response = load(folder / 'stdout.bin')
    except (ValueError, KeyError, TypeError) as error:
        parse_error = repr(error)
    outcome = interpret(response, result, parse_error, 'fresh')['outcome']
    if outcome not in ['complete', 'incomplete', 'rejected']:
        return None, outcome
    return response, outcome


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['run', 'fresh', 'pool', 'out']:
        ap.add_argument('--' + name, type=Path, required=True)
    args = ap.parse_args()
    codes = load(args.pool / 'to_inference_codes.json')
    tasks = load(args.pool / 'selected_tasks.json')
    if len(codes) != 1024 or len(tasks) != 32:
        ap.error('declared1024-source/32-task cohort required')
    args.out.mkdir(parents=True, exist_ok=False)
    observations = {i: oracle(args.fresh, i, codes[i]["code"]) for i in range(len(codes))}
    source = lambda i: dict(index=i, code=codes[i]['code'], header=tasks[i // 32]['header'])
    summary = dict(scope='functional source fidelity only; neither matched performance nor universal safety',
                   original_candidates=1024, producer_outcomes=dict(Counter(v[1] for v in observations.values())),
                   conditions={}, cancellation={}, runner=load(args.run / 'summary.json'))
    with (args.out / 'per-source.jsonl').open('x') as stream:
        for order in ['forward', 'reverse']:
            indices = list(range(1024)) if order == 'forward' else list(reversed(range(1024)))
            for method in ['prepared', 'snapshot']:
                label = method + '-' + order
                folder = args.run / label
                returned = {}
                actual_inputs = {}
                protocol_errors = []
                if method == 'prepared':
                    inp = folder / 'input.jsonl'
                    if inp.exists():
                        for ordinal, line in enumerate(inp.read_bytes().splitlines()):
                            actual_inputs[ordinal] = json.loads(line)
                    records = folder / 'results.jsonl'
                    if records.exists():
                        for line in records.read_bytes().splitlines():
                            r = json.loads(line)
                            if r['ordinal'] in returned:
                                protocol_errors.append('duplicate ordinal ' + str(r['ordinal']))
                            returned[r['ordinal']] = r
                counts = Counter()
                for ordinal, index in enumerate(indices):
                    response = None
                    native = None
                    observed_status = 'missing'
                    source_matches = False
                    if method == 'prepared':
                        source_matches = actual_inputs.get(ordinal) == source(index)
                        r = returned.get(ordinal)
                        if r is not None:
                            observed_status = r['status']
                            if r.get('source_index') != index:
                                observed_status = 'source_index_mismatch'
                            if observed_status == 'response':
                                native = r['native_response']['native']
                                response = native['response']
                    else:
                        request = folder / ('request-%08d' % ordinal)
                        inp = load(request / 'stdin.bin')
                        source_matches = inp == dict(index=ordinal, header=source(index)['header'], code=source(index)['code'])
                        result = load(request / 'result.json')
                        if result is not None:
                            observed_status = result['status']
                            if observed_status == 'response':
                                response = load(request / 'response.bin')
                                raw = load(request / 'native-record.bin')
                                native = raw['record']['native']
                    original, original_outcome = observations[index]
                    comparable = source_matches and observed_status == 'response' and isinstance(response, dict) and original is not None
                    delta = differences(canonical(original), canonical(response)) if comparable else None
                    classification = 'equal' if comparable and not delta else 'response_difference' if comparable else 'unknown'
                    counts[classification] += 1
                    if not source_matches:
                        counts['source_unobserved_or_mismatch'] += 1
                    if native is not None and native.get('import_diagnostics'):
                        counts['nonempty_import_diagnostics'] += 1
                    if native is not None and native.get('final_command_state') is not True:
                        counts['missing_native_finalization'] += 1
                    row = dict(condition=label, ordinal=ordinal, source_index=index, source_matches=source_matches,
                               native_status=observed_status, producer_outcome=original_outcome,
                               classification=classification, difference_paths=delta,
                               import_diagnostics=native.get('import_diagnostics') if native else None,
                               final_command_state=native.get('final_command_state') if native else None)
                    stream.write(json.dumps(row, ensure_ascii=False) + '\n')
                extra = sorted(set(returned) - set(range(1024)))
                summary['conditions'][label] = dict(expected_sources=1024, comparisons=dict(counts),
                    terminal_record_count=len(returned) if method == 'prepared' else len(list(folder.glob('request-*/result.json'))),
                    protocol_errors=protocol_errors, extra_ordinals=extra,
                    receipt=load(folder / 'receipt.json') if method == 'prepared' else None)
        for index in [0, 32, 64, 96, 128, 160]:
            for stage in ['frontend_begin', 'frontend_complete']:
                label = 'cancel-%d-%s' % (index, stage)
                folder = args.run / label
                receipt = load(folder / 'receipt.json')
                records = folder / 'results.jsonl'
                r = [json.loads(x) for x in records.read_bytes().splitlines()] if records.exists() else []
                control_input = folder / 'input.jsonl'
                observed_inputs = [json.loads(x) for x in control_input.read_bytes().splitlines()] if control_input.exists() else []
                control_sources_equal = observed_inputs == [source(index), source(index + 1)]
                controlled = bool(control_sources_equal and receipt and len(receipt.get('cancelled', [])) == 1 and len(r) == 2 and
                                  r[0]['source_index'] == index and r[0]['status'] == 'cancelled' and
                                  receipt['cancelled'][0]['stage'] == stage)
                sibling, outcome = observations[index + 1]
                sibling_native = r[1]['native_response']['native'] if len(r) == 2 and r[1]['status'] == 'response' else None
                delta = differences(canonical(sibling), canonical(sibling_native['response'])) if sibling is not None and sibling_native else None
                summary['cancellation'][label] = dict(control_source_bytes_equal=control_sources_equal,
                    actual_marker_disposal=controlled,
                    following_sibling_source_index=index + 1, following_sibling_oracle_outcome=outcome,
                    following_sibling_native_status=r[1]['status'] if len(r) == 2 else 'missing',
                    following_sibling_response_equal=bool(controlled and sibling is not None and sibling_native and not delta),
                    difference_paths=delta, receipt=receipt)
    (args.out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'runner'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
