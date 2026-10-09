#!/usr/bin/env python3
"""Summarize retained native observations; raw stdout remains the reference."""
import argparse
from collections import Counter
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('raw', type=Path)
a = p.parse_args()
rows = json.loads((a.raw / 'analysis.json').read_text())
groups = []
differences = []
models = []
for repeat, mode in sorted({(r['repeat'], r['mode']) for r in rows}):
    subset = [r for r in rows if (r['repeat'], r['mode']) == (repeat, mode)]
    contrast = {}
    for ref in ('release', 'source', 'lazy'):
        compared = [r for r in subset if ref in r.get('comparisons', {})]
        if not compared:
            continue
        contrast[ref] = dict(
            decision_differences=[r['index'] for r in compared if not r['comparisons'][ref].get('decisions_equal', False)],
            nonstatistics_differences=[r['index'] for r in compared if not r['comparisons'][ref].get('nonstatistics_exact_equal', False)])
        for r in compared:
            diffs = [f for f in r['comparisons'][ref].get('response_comparison', []) if not f['statistics'] and not f['exact_equal']]
            if diffs:
                differences.append(dict(repeat=repeat, mode=mode, index=r['index'], reference=ref, differing_response_commands=diffs))
    groups.append(dict(repeat=repeat, mode=mode, streams=len(subset),
                       decisions=dict(Counter(d for r in subset for d in r.get('decisions', []))),
                       incomplete_checks=[r['index'] for r in subset if not r.get('complete_checks')],
                       incomplete_frames=[r['index'] for r in subset if not r.get('complete_response_frames')],
                       nonzero_exits=[r['index'] for r in subset if r['returncode']],
                       error_streams=[r['index'] for r in subset if r.get('errors')],
                       stderr_streams=[r['index'] for r in subset if r.get('stderr_text')],
                       observed_affinities=dict(Counter(str(r.get('actual_affinity')) for r in subset)),
                       contrasts=contrast))
    for r in subset:
        for f in r.get('response_frames', []):
            if f['head'] == 'get-model':
                models.append(dict(repeat=repeat, mode=mode, index=r['index'], command_index=f['command_index'],
                                   available=f['model_available'], sha256=f['sha256'], errors=f['errors'], stdout=r['stdout']))
print(json.dumps(dict(groups=groups, differences=differences, models=models), indent=2))
