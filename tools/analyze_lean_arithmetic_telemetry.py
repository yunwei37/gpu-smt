#!/usr/bin/env python3
"""Recompute observed arithmetic wall intervals and integer LP shapes.

Reads a finished capture and its original JSONL. Does not launch Lean, choose
inputs, weaken feedback comparison, estimate CPU time, or extrapolate GPU gains.
Nested scopes are merged by session/request before aggregation; absent durations
remain absent. Oracle and native-client LP rows are separate observation layers.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path


def union_ns(intervals):
    total = 0
    end = None
    for left, right in sorted(intervals):
        if end is None or left > end:
            total += right - left
            end = right
        elif right > end:
            total += right - end
            end = right
    return total


def analyze(telemetry, capture, out):
    intervals = defaultdict(lambda: defaultdict(list))
    counts, outcomes, issues, lp_rows = Counter(), Counter(), [], []
    calls, seen_requests = set(), set()
    for number, line in enumerate(telemetry.read_text().splitlines(), 1):
        try:
            row = json.loads(line)
            session, request, call = (row[k] for k in ['session', 'request', 'call'])
            if any(type(v) is not int or v < 0 for v in [session, request, call]):
                raise ValueError('invalid source identity')
            key = (session, request)
            seen_requests.add(request)
            calls.add((session, request, call))
            kind = row['ty']
            counts[kind] += 1
            if 'outcome' in row:
                outcomes[kind + ':' + row['outcome']] += 1
            def add(category, start, duration):
                if type(start) is not int or type(duration) is not int or start < 0 or duration < 0:
                    raise ValueError('invalid interval ' + category)
                intervals[key][category].append((start, start + duration))
            if 'ns' in row:
                add(kind, row['t'], row['ns'])
            if kind == 'fast':
                if 'nsTotal' in row:
                    add('fast_total', row['t'], row['nsTotal'])
                if 'nsParse' in row:
                    add('fast_parse', row['t'], row['nsParse'])
                    if row['tParse'] != row['t'] + row['nsParse']:
                        raise ValueError('fast parse endpoints differ')
                if 'nsOracle' in row:
                    add('fast_probe_with_product_generation', row['tParse'], row['nsOracle'])
                    if row['tOracle'] != row['tParse'] + row['nsOracle']:
                        raise ValueError('fast probe endpoints differ')
            if kind in ['oracle', 'native_oracle']:
                lp = row if kind == 'oracle' else row['lp']
                hyps, max_var = lp['hyps'], lp['maxVar']
                if type(max_var) is not int or max_var < 0 or not isinstance(hyps, list):
                    raise ValueError('invalid integer LP shape')
                atoms, coefficients = [], []
                for relation, terms in hyps:
                    if relation not in ['lt', 'le', 'eq']:
                        raise ValueError('invalid relation')
                    for atom, coefficient in terms:
                        if type(atom) is not int or atom < 0 or type(coefficient) is not int:
                            raise ValueError('noninteger protocol term')
                        atoms.append(atom); coefficients.append(coefficient)
                lp_rows.append(dict(line=number, session=session, request=request, call=call,
                    observation_layer=kind, phase=row.get('phase'), ok=row.get('ok'),
                    max_variable_index=max_var, hypotheses=len(hyps), terms=len(coefficients),
                    observed_nonconstant_atoms=len(set(atoms) - {0}),
                    max_abs_coefficient=max(map(abs, coefficients), default=0),
                    max_coefficient_bits=max((abs(v).bit_length() for v in coefficients), default=0)))
        except (KeyError, ValueError, TypeError) as error:
            issues.append(dict(line=number, error=repr(error)))
    per_request, total_union, total_sums = [], Counter(), Counter()
    for (session, request), categories in sorted(intervals.items()):
        union = {name: union_ns(values) for name, values in categories.items()}
        sums = {name: sum(b-a for a,b in values) for name, values in categories.items()}
        union['all_observed_arithmetic'] = union_ns([v for vs in categories.values() for v in vs])
        folder = capture / ('request-%08d' % request)
        result = json.loads((folder / 'result.json').read_text()) if (folder / 'result.json').exists() else None
        source = json.loads((folder / 'stdin.bin').read_text()) if (folder / 'stdin.bin').exists() else None
        latency = (result or {}).get('invocation_elapsed_ns')
        per_request.append(dict(session=session, request=request, source_index=(source or {}).get('index'),
            source_identity_matches=(source or {}).get('index') == request,
            capture_status=(result or {}).get('status'), candidate_elapsed_ns=latency,
            category_union_ns=union, category_sum_ns=sums,
            observed_union_exceeds_candidate=type(latency) is int and union['all_observed_arithmetic'] > latency))
        total_union.update(union); total_sums.update(sums)
    out.mkdir(parents=True, exist_ok=False)
    for name, rows in [('per-request.jsonl', per_request), ('integer-lp-observations.jsonl', lp_rows)]:
        with (out / name).open('x') as stream:
            for row in rows:
                stream.write(json.dumps(row) + '\n')
    summary = dict(telemetry=str(telemetry), capture=str(capture), row_counts=dict(counts),
        route_outcomes=dict(outcomes), observed_requests=len(seen_requests), observed_calls=len(calls),
        session_request_groups=len(per_request), summed_per_request_category_union_ns=dict(total_union),
        summed_raw_category_ns=dict(total_sums), integer_lp_observations=len(lp_rows),
        missing_or_mismatched_sources=sum(not x['source_identity_matches'] for x in per_request),
        observed_union_exceeds_candidate=sum(x['observed_union_exceeds_candidate'] for x in per_request),
        issues=issues, scope='observed wall intervals, not CPU; union removes overlap; instrumentation excludes some sink/serialization and missing event work; no zero for unlogged work, whole-run fraction, GPU ceiling or speedup; LP layers not unique problem counts')
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['telemetry', 'capture', 'out']:
        ap.add_argument('--' + name, type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(analyze(args.telemetry, args.capture, args.out), indent=2))


if __name__ == '__main__':
    main()
