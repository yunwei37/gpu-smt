from pathlib import Path
import collections
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
capture = Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/captures/reflected-grid-v4')
published_source = subprocess.check_output(
    ['git', 'show', '540cfc2:research/mechanisms-2026-10-30/ReflectedGridCertificate.lean'],
    cwd=repository,
)
source = (capture / 'source.lean').read_bytes()
assert source == published_source
source_text = source.decode()
assert 'native_decide' not in source_text
assert 'sorry' not in source_text
assert not re.search(r'^\s*axiom\s', source_text, re.M)
chunks = [(int(i), int(first), int(width)) for i, first, width in re.findall(
    r'theorem chunk(\d+) : block (\d+) (\d+) = true := by decide', source_text)]
assert len(chunks) == 16
assert [i for i, _, _ in chunks] == list(range(16))
covered = [value for _, first, width in chunks for value in range(first, first + width)]
assert covered == list(range(2, 2006))
assert len(covered) == 2004 and 2004 * 2004 == 4016016
assert '(m n : Nat) (hm : 1 < m) (hn : 1 < n)' in source_text
assert '(prod : m * n = 2005) : m + n = 406' in source_text
assert 'Nat.mul_div_right n hm' in source_text
assert 'block_sound 2 2004 (m - 2) index full_rows' in source_text
assert 'env.addDeclCore 1000000' in source_text
assert 'for workers in [1, 2, 4, 8]' in source_text
assert 'for repetition in [:5]' in source_text

receipt = json.loads((capture / 'receipt.json').read_text())
assert receipt['exit'] == 0 and receipt['retired'] and receipt['signals_sent'] == 0
assert receipt['cpu_affinity'] == '8-15' and receipt['native_jobs'] == 8
stat = Path('/proc') / str(receipt['pid']) / 'stat'
if stat.exists():
    assert stat.read_text().split(') ')[1].split()[19] != receipt['start_ticks']
sampled_peak = max(json.loads(line)['owned_rss_bytes']
                   for line in (capture / 'memory.jsonl').open())
assert sampled_peak == receipt['sampled_peak_owned_rss_bytes'] == 572776448

text = (capture / 'stdout.txt').read_text()
assert 'error:' not in text and 'sorryAx' not in text and 'ofReduceBool' not in text
expected_axioms = [
    'MechanismReflectedGrid.row_sound',
    'MechanismReflectedGrid.full_rows',
    'MechanismReflectedGrid.mathd_numbertheory_541',
]
for name in expected_axioms:
    assert f"'{name}' depends on axioms: [propext, Quot.sound]" in text
group_rows = [tuple(map(int, match)) for match in re.findall(
    r'^M_GRID_GROUP (\d+) (\d+) (\d+) (\d+)$', text, re.M)]
chunk_rows = [tuple(map(int, match)) for match in re.findall(
    r'^M_GRID_CHUNK (\d+) (\d+) (\d+) (\d+)$', text, re.M)]
assert len(group_rows) == 20 and len(chunk_rows) == 320
assert {(workers, rep) for workers, rep, _, _ in group_rows} == {
    (workers, rep) for workers in [1, 2, 4, 8] for rep in range(5)
}
assert all(count == 16 for _, _, _, count in group_rows)
for workers, repetition, _, _ in group_rows:
    ids = [index for w, rep, index, _ in chunk_rows
           if w == workers and rep == repetition]
    assert sorted(ids) == list(range(16))

summary = {}
for workers in [1, 2, 4, 8]:
    values = [nanoseconds / 1e9 for w, _, nanoseconds, _ in group_rows if w == workers]
    summary[str(workers)] = {
        'ordered_group_seconds': values,
        'median_group_seconds': statistics.median(values),
    }
published = json.loads(subprocess.check_output(
    ['git', 'show', '540cfc2:research/mechanisms-2026-10-30/reflected-grid-v4-result.json'],
    cwd=repository, text=True))
for workers, values in summary.items():
    assert values['ordered_group_seconds'] == published['summary'][workers]['seconds']
    assert values['median_group_seconds'] == published['summary'][workers]['median_seconds']
result = {
    'source_commit': '540cfc2',
    'executed_source_equals_published_snapshot': True,
    'working_source_not_used': True,
    'additional_native_calls_by_root': 0,
    'full_original_proposition_compiler_checked': True,
    'row_indices_checked': 2004,
    'logical_square_cells_covered': 4016016,
    'literal_kernel_cell_evaluations': 'not measured; proof uses one quotient per row',
    'initial_concrete_chunks': 16,
    'extra_chunk_rechecks': 320,
    'recheck_groups': 20,
    'whole_native_wall_seconds': receipt['wall_s'],
    'whole_native_CPU_seconds': receipt['native_cpu_seconds'],
    'native_wait4_high_water_RSS_bytes': receipt['native_kernel_peak_rss_bytes'],
    'sampled_owned_tree_peak_bytes': sampled_peak,
    'actual_CPU_affinity': receipt['cpu_affinity'],
    'legacy_hardware_point_field': receipt['hardware_point'],
    'axioms_of_audited_bridges_and_final_theorem': ['propext', 'Quot.sound'],
    'ordered_group_results': summary,
    'sum_disjoint_extra_group_windows_s': sum(row[2] for row in group_rows) / 1e9,
    'limits': [
        'Embedded two-pair payload is checked, but external payload generation cost is not measured here.',
        'A new proof of the original proposition is not unchanged-candidate verdict parity.',
        'Initial declarations are checked sequentially; later tasks only recheck existing proof values.',
        'Returned environments are discarded, not merged; no production elaborator or proof-state replay is enabled.',
        'One process orders workers1,2,4,8 with five groups each; all startup repetitions retained.',
        'Early two eight-task groups are near serial; cause of later faster groups is unestablished.',
        'No causal parallel speedup, scaling curve, historical48GiB speedup or full7808 benefit claimed.',
        'Actual argv/explicit affinity8-15 override stale generic hardware_point CPU8-11 text.',
    ],
    'root_elapsed_s': time.monotonic() - began,
    'root_maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
}
(evidence / 'reanalysis.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
