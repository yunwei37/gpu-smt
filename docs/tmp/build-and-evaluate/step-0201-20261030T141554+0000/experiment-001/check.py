from pathlib import Path
import collections
import csv
import json
import os
import re
import resource
import statistics
import subprocess
import time

os.sched_setaffinity(0, {0, 1})
began = time.monotonic()
repository = Path('/workspaces/repository')
evidence = Path(__file__).parent
raw = Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30')

def checked_receipt(capture):
    receipt = json.loads((capture / 'receipt.json').read_text())
    assert receipt['exit'] == 0 and receipt['retired'] and receipt['signals_sent'] == 0
    assert receipt['cpu_affinity'] == '8-15' and receipt['native_jobs'] == 8
    stat = Path('/proc') / str(receipt['pid']) / 'stat'
    if stat.exists():
        assert stat.read_text().split(') ')[1].split()[19] != receipt['start_ticks']
    return receipt

def frozen_equal(capture, archive_path):
    archived = subprocess.check_output(['git', 'show', 'fd37172:' + archive_path], cwd=repository)
    assert (capture / 'source.lean').read_bytes() == archived

parallel = raw / 'captures/reflected-grid-v5-parallel'
parallel_receipt = checked_receipt(parallel)
frozen_equal(parallel, 'research/mechanisms-2026-10-30/reflected-grid-v5/parallel/source.lean')
text = (parallel / 'stdout.txt').read_text()
assert 'error:' not in text and 'sorryAx' not in text and 'ofReduceBool' not in text
groups = [tuple(map(int, values)) for values in re.findall(
    r'^M_GRID_GROUP (\d+) (\d+) (\d+) (\d+) (\d+)$', text, re.M)]
chunks = [tuple(map(int, values)) for values in re.findall(
    r'^M_GRID_CHUNK (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)$', text, re.M)]
assert len(groups) == 24 and len(chunks) == 384
assert {(round_id, workers, rep) for round_id, workers, rep, _, _ in groups} == {
    (round_id, workers, rep) for round_id in [0, 1] for workers in [1, 2, 4, 8] for rep in range(3)
}
details = []
for round_id, workers, repetition, elapsed, count in groups:
    assert count == 16
    rows = [(index, start, end) for rnd, wrk, rep, index, start, end in chunks
            if (rnd, wrk, rep) == (round_id, workers, repetition)]
    assert sorted(index for index, _, _ in rows) == list(range(16))
    assert all(end > start for _, start, end in rows)
    events = sorted([(start, 1) for _, start, end in rows] +
                    [(end, -1) for _, start, end in rows])
    active = peak = 0
    for timestamp, delta in events:
        active += delta
        assert active >= 0
        peak = max(peak, active)
    assert active == 0 and peak == workers
    for lane in range(workers):
        lane_intervals = sorted((start, end) for index, start, end in rows if index % workers == lane)
        assert all(first[1] <= second[0] for first, second in zip(lane_intervals, lane_intervals[1:]))
    span = max(end for _, _, end in rows) - min(start for _, start, _ in rows)
    assert span <= elapsed
    details.append({'round': round_id, 'tasks': workers, 'repetition': repetition,
                    'wall_s': elapsed / 1e9, 'observed_max_kernel_call_overlap': peak})
scaling = {}
for tasks in [1, 2, 4, 8]:
    values = [row['wall_s'] for row in details if row['tasks'] == tasks]
    scaling[str(tasks)] = {'groups': len(values), 'seconds': values,
                           'min_s': min(values), 'median_s': statistics.median(values), 'max_s': max(values)}
for record in scaling.values():
    record['ratio_of_medians'] = scaling['1']['median_s'] / record['median_s']

source_calls = []
for index in range(3):
    capture = raw / 'captures' / ('reflected-grid-v5-source-' + str(index))
    receipt = checked_receipt(capture)
    output = (capture / 'stdout.txt').read_text()
    final = re.findall(r'M_GRID_FINAL_KERNEL_NS (\d+)', output)
    assert len(final) == 1 and 'M_GRID_GROUP' not in output and 'error:' not in output
    source_calls.append({'wall_s': receipt['wall_s'], 'extra_final_recheck_s': int(final[0]) / 1e9})
assert len(source_calls) == 3

pipeline_capture = raw / 'captures/reflected-grid-v6-pipeline'
receipt = checked_receipt(pipeline_capture)
frozen_equal(pipeline_capture, 'research/mechanisms-2026-10-30/reflected-grid-v6/source.lean')
pipeline = json.loads((raw / 'reflected-grid-v6-terminal.json').read_text())
assert pipeline['exit'] == 0
generation = json.loads((raw / 'generated/reflected-grid-v6/generation.json').read_text())
assert generation['solution_pairs'] == [[5, 401], [401, 5]]
generated = Path(generation['source'])
assert generated.read_bytes() == (pipeline_capture / 'source.lean').read_bytes()
output = (pipeline_capture / 'stdout.txt').read_text()
assert 'M_GRID_GROUP' not in output and 'M_GRID_CHUNK' not in output
assert 'error:' not in output and 'sorryAx' not in output and 'ofReduceBool' not in output
for name in ['row_sound', 'full_rows', 'mathd_numbertheory_541']:
    assert f"'MechanismReflectedGrid.{name}' depends on axioms: [propext, Quot.sound]" in output
phases = {name: int(value) for name, value in re.findall(r'^M_GRID_PHASE (\S+) (\d+)$', output, re.M)}
assert set(phases) == {'before_chunks', 'after_chunks', 'after_assembly', 'after_final_theorem'}
phase_costs = {
    'initial_chunk_declarations_s': (phases['after_chunks'] - phases['before_chunks']) / 1e9,
    'coverage_assembly_s': (phases['after_assembly'] - phases['after_chunks']) / 1e9,
    'final_theorem_construction_s': (phases['after_final_theorem'] - phases['after_assembly']) / 1e9,
    'extra_final_recheck_s': int(re.findall(r'M_GRID_FINAL_KERNEL_NS (\d+)', output)[0]) / 1e9,
}
assert all(value > 0 for value in phase_costs.values())
peak = max(json.loads(line)['owned_rss_bytes'] for line in (pipeline_capture / 'memory.jsonl').open())
assert peak == receipt['sampled_peak_owned_rss_bytes'] == 566886400
assert receipt['native_cpu_scope'] == 'RUSAGE_CHILDREN delta for this serial run'
assert 'cumulative' in receipt['native_kernel_peak_rss_scope']
assert generation['generation_wall_s_before_receipt'] + receipt['wall_s'] <= pipeline['end_to_end_wall_s']

result = {
    'source_commit': 'fd37172',
    'additional_native_calls_by_root': 0,
    'v5_native_processes_returned_and_retired': 4,
    'v5_source_call_walls_and_extra_rechecks': source_calls,
    'v5_groups': 24, 'v5_extra_chunk_checks': 384,
    'actual_overlap_matches_tasks_in_all_groups': True,
    'scaling': scaling,
    'v6_whole_pipeline_s': pipeline['end_to_end_wall_s'],
    'v6_generation_and_emission_s': generation['generation_wall_s_before_receipt'],
    'v6_C_compile_s': generation['compile_wall_s'],
    'v6_numeric_process_wall_s': generation['scan_process_wall_s'],
    'v6_native_invocation_wall_s': receipt['wall_s'],
    'v6_native_CPU_delta_s': receipt['native_cpu_seconds'],
    'v6_phase_windows': phase_costs,
    'v6_sampled_own_tree_peak_bytes': peak,
    'numeric_payload': generation['solution_pairs'],
    'axioms': ['propext', 'Quot.sound'],
    'v5_cpu_and_highwater_scope': 'Legacy cumulative controller fields; not used as per-native evidence.',
    'v6_highwater_scope': receipt['native_kernel_peak_rss_scope'],
    'limits': [
        'Ratios describe additional kernel rechecks of already available proof values, not initial elaboration or service throughput.',
        'All24groups in both orders retained; six observations per task count, not independent full-pipeline trials.',
        'Do not apply recheck scaling to the initial chunk phase that also includes elaboration and proof construction.',
        'One complete pipeline includes generation, source emission, imports and one extra final-theorem recheck; no optimized cost inferred by subtraction.',
        'New proof/algorithm does not establish original candidate verdict parity or49candidate recoveries.',
        'Ordinary reflection and parallel checking are prior techniques; no generic compiler or production adapter enabled.',
    ],
    'root_elapsed_s': time.monotonic() - began,
    'root_maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}
(evidence / 'reanalysis.json').write_text(json.dumps(result, indent=2) + '\n')
(evidence / 'overlap-groups.json').write_text(json.dumps(details, indent=2) + '\n')
print(json.dumps(result, indent=2))
