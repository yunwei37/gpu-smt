from pathlib import Path
import csv, json

root = Path('/workspaces/.agent-state/gpu-smt-captures/workloads')
here = Path(__file__).parent
table = list(csv.DictReader((here / 'native-table.csv').open()))
pair = [json.loads(line) for line in (root / 'openai4341-profile-ab/results.jsonl').read_text().splitlines()]

def bounded(tag):
    rows = [json.loads(line) for line in (root / tag / 'results.jsonl').read_text().splitlines()]
    invoked = [row for row in rows if 'returncode' in row]
    return {
        'invoked': len(invoked),
        'compile': sum(row['status'] == 'compile_ok' for row in rows),
        'HB_stop': sum(row['status'] == 'budget_exceeded' for row in rows),
        'wall_stop': sum(row['status'] == 'wall_budget_exceeded' for row in rows),
        'uninvoked': sum(row['status'] == 'dependency_not_compiled' for row in rows),
        'compiler_wall_s': sum(row['wall_s'] for row in invoked),
    }

expected = []
for mode in ['baseline', 'profile_only']:
    rows = [row for row in pair if row['mode'] == mode]
    assert len(rows) == 7
    assert all(row['returncode'] == 0 and not row['sorry_warning'] for row in rows)
    assert all(row['heartbeats'] == 200000 for row in rows)
    expected.append({
        'invoked': 7, 'compile': 7, 'HB_stop': 0, 'wall_stop': 0, 'uninvoked': 0,
        'compiler_wall_s': sum(row['wall_s'] for row in rows),
    })
for tag in ['openai4341-native-expanded', 'openai4341-native-resume100k', 'openai4341-native-batch3', 'openai4341-grid-profile300']:
    expected.append(bounded(tag))

assert len(table) == len(expected) == 6
for printed, actual in zip(table, expected):
    for field in ['invoked', 'compile', 'HB_stop', 'wall_stop', 'uninvoked']:
        assert int(printed[field]) == actual[field], (printed['point'], field, actual)
    assert abs(float(printed['compiler_wall_s']) - actual['compiler_wall_s']) <= 0.0005

result = {
    'all_six_table_rows_match_retained_native_records': True,
    'wall_values_rounded_to_three_decimals': True,
    'exact_compiler_wall_s': [row['compiler_wall_s'] for row in expected],
    'additional_native_calls': 0,
}
(here / 'table-native-reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
