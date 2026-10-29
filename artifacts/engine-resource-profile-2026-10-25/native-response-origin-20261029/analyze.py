#!/usr/bin/env python3
"""Read-only response attribution using completed streams and installed service code.
Not a native run, serializer change, production normalization or correctness gate.
"""
import ast
import collections
import copy
import gzip
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAIR = ROOT / "artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z"
OLD = ROOT / "artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z"
DIFF = ROOT / "docs/tmp/build-and-evaluate/step-0118-20261029T052416+0000/native-response-differences.json.gz"
KIMINA = Path("/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d")

def read(path):
    if path.suffix == ".gz":
        with gzip.open(path, "rt") as stream:
            return json.load(stream)
    if path.exists():
        return json.loads(path.read_text())
    with gzip.open(path.with_name(path.name + ".gz"), "rt") as stream:
        return json.load(stream)

def secondary(payload):
    # Exactly the prior labelled comparison view; no extra message/position edit.
    if not isinstance(payload, dict):
        return payload
    result = dict(payload)
    result.pop("env", None)
    if result.get("ast") == []:
        result.pop("ast")
    return result

def analyze():
    differences = read(DIFF)
    old = read(OLD / "native/capture.json")
    current = read(PAIR / "engine.stdout")
    assert old["batch"] == current["batch"]
    inputs = {row["id"]: row for row in current["batch"]["candidates"]}
    fresh = {row["id"]: row for row in old["results"]}
    assert len(fresh) == len(inputs) == 7808
    classification = read(ROOT / "docs/tmp/build-and-evaluate/step-0118-20261029T052416+0000/response-difference-classification.json")
    optional = {row["id"] for row in classification["optional_field_examples"]}
    spec = importlib.util.spec_from_file_location("retained_kimina_split", KIMINA / "server/split.py")
    splitter = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = splitter
    spec.loader.exec_module(splitter)
    # This imports data models only: no Manager, REPL, router, native worker or HTTP request.
    sys.path.insert(0, str(KIMINA / "client"))
    from kimina_client.models import ReplResponse
    rows = []
    for difference in differences:
        identifier = difference["id"]
        native = fresh[identifier]["outcome"]
        engine = difference["raw_engine"]
        warm = difference["raw_warm"]
        split = splitter.split_snippet(inputs[identifier]["code"])
        native_equal = secondary(native.get("response")) == secondary(engine)
        warm_equal = secondary(native.get("response")) == secondary(warm)
        row = {
            "id": identifier, "fresh_status": native["status"],
            "fresh_matches_engine_after_only_env_empty_ast": native_equal,
            "fresh_matches_warm_after_only_env_empty_ast": warm_equal,
            "actual_service_header_line_count": split.header_line_count,
            "full_original_source_equal": inputs[identifier] in old["batch"]["candidates"],
        }
        assert native_equal and not warm_equal
        if identifier in optional:
            payload = copy.deepcopy(engine)
            original = copy.deepcopy(payload)
            response = ReplResponse(id=identifier, response=payload)
            replay = response.model_dump(exclude_none=True)["response"]
            assert payload == original
            row.update(
                category="optional_endPos_serialization",
                actual_installed_model_dump_matches_warm_after_two_fields=secondary(replay) == secondary(warm),
            )
            assert row["actual_installed_model_dump_matches_warm_after_two_fields"]
        else:
            changes = difference["secondary_view_differences"]
            assert changes and all(path.endswith("/data") for path, _, _ in changes)
            row.update(category="embedded_text_position",
                changed_message_fields=[path for path, _, _ in changes],
                offset_source="server/routers/check.py:_apply_header_offset shifts structured positions only",
                raw_data_unchanged=True)
        rows.append(row)
    coordinate_rows = []
    coordinate_pattern = re.compile(r"(?m)^([ \\t]+)([0-9]+):([0-9]+)(?= )")
    for difference in differences:
        if difference["id"] in optional:
            continue
        observations = []
        for path, warm_text, engine_text in difference["secondary_view_differences"]:
            assert path.endswith("/data")
            warm_positions = list(coordinate_pattern.finditer(warm_text))
            engine_positions = list(coordinate_pattern.finditer(engine_text))
            assert len(warm_positions) == len(engine_positions) > 0
            # An explanatory test only. Its output is never a verification response.
            assert coordinate_pattern.sub(r"\\1LINE:\\3", warm_text) == coordinate_pattern.sub(r"\\1LINE:\\3", engine_text)
            for warm_position, engine_position in zip(warm_positions, engine_positions):
                assert warm_position[1] == engine_position[1] and warm_position[3] == engine_position[3]
                offset = int(engine_position[2]) - int(warm_position[2])
                source_offset = next(row["actual_service_header_line_count"] for row in rows if row["id"] == difference["id"])
                assert offset == source_offset == 3
                observations.append({"path": path, "warm_body_line": int(warm_position[2]),
                    "engine_full_source_line": int(engine_position[2]), "column": int(warm_position[3])})
        coordinate_rows.append({"id": difference["id"], "coordinate_occurrences": observations})
    counts = dict(collections.Counter(row["category"] for row in rows))
    assert counts == {"embedded_text_position": 7, "optional_endPos_serialization": 16}
    source = KIMINA / "server/routers/check.py"
    tree = ast.parse(source.read_text())
    offset = next(node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "_apply_header_offset")
    # Preserve source for review, rather than invent a replacement response transformation.
    offset_source = ast.get_source_segment(source.read_text(), offset)
    return {
        "scope": "Post-run attribution of exactly23retained warm/prepared response differences",
        "count": len(rows), "counts": counts, "rows": rows,
        "installed_service_offset_function": offset_source,
        "embedded_coordinate_observations": coordinate_rows,
        "coordinate_scope": "Explanatory read-only text comparison, never a corrected/normalized native response.",
        "pydantic_version": __import__("pydantic").__version__,
        "fresh_context": {"backend": old["backend"], "environment": old["environment"],
            "scope": "Historical fresh run omitted the ordinary native Mathlib library and differs in resource lifecycle. Not fresh matched-context reexecution or timing evidence."},
        "current_context": {"backend": current["backend"], "environment": current["environment"]},
        "limits": [
            "All23historical-fresh comparisons remove only top-level env and empty ast, as already declared.",
            "No stored native message,position,optional field,error,result or accepted-set comparison is rewritten.",
            "Data-model serialization replay is pure Python; no native candidate or HTTP request is executed.",
            "Post-run installed source is observed now, not independently authenticated launch-time source.",
            "Cross-context historical corroboration does not replace a fresh same-context native artifact differential.",
            "No statement of arbitrary frontend/FFI/fork correctness, complete RQ2 coverage or independent audit.",
            "No performance clock or novel workload mechanism is measured.",
        ],
    }

if __name__ == "__main__":
    print(json.dumps(analyze(), ensure_ascii=False, indent=2))
