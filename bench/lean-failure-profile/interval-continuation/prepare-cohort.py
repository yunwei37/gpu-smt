"""Prepare explicit experimental traversal variants from retained native Syntax.

This is source preparation, not a failure detector or semantic-equivalence proof.
Original left-associated <;> stages and nested continuations can differ in state
history and resource-limited outcomes. Native candidates are never executed here.
"""
import argparse
import collections
import gzip
import json
from pathlib import Path

AND = "Lean.Parser.Tactic.«tactic_<;>_»"
INTERVAL = "Mathlib.Tactic.intervalCases"


def tokens(node):
    if node["atom"] is not None:
        return [(False, node["atom"])]
    if node["identifier"] is not None:
        return [(True, node["identifier"])]
    return [token for child in node["children"] for token in tokens(child)]


def interval(node):
    ts = tokens(node)
    return (node["kind"] == INTERVAL and len(ts) == 2
            and ts[0] == (False, "interval_cases") and ts[1][0])


def flatten(node):
    children = node["children"]
    if node["kind"] == AND:
        assert len(children) == 3 and children[1]["atom"] == "<;>"
        return flatten(children[0]) + [children[2]]
    return [node]


def proof_bodies(node):
    if node["kind"] == "Lean.Parser.Term.byTactic":
        yield node
    for child in node["children"]:
        yield from proof_bodies(child)


def sequence(node):
    while node["kind"] in ("Lean.Parser.Term.byTactic",
                           "Lean.Parser.Tactic.tacticSeq",
                           "Lean.Parser.Tactic.tacticSeq1Indented"):
        node = node["children"][1 if node["kind"] == "Lean.Parser.Term.byTactic" else 0]
    if node["kind"] != "null" or len(node["children"]) % 2 != 1:
        return None
    return node["children"][::2]


def identifiers(node):
    if node["identifier"] is not None:
        yield node
    for child in node["children"]:
        yield from identifiers(child)


def compressed(path, value):
    path.write_bytes(gzip.compress(
        (json.dumps(value, ensure_ascii=False) + "\n").encode(), mtime=0))


def apply(raw, edits):
    # Original-coordinate edits are nonoverlapping; exact bytes outside them stay.
    edits = sorted(edits, key=lambda e: e["start"])
    shift = 0
    for prior, following in zip(edits, edits[1:]):
        assert prior["end"] <= following["start"]
    changed = raw
    mapping = []
    for edit in edits:
        start, end = edit["start"], edit["end"]
        mapping.append(dict(original_start=start, original_end=end,
                            changed_start=start + shift,
                            changed_end=start + shift + len(edit["replacement"]),
                            original_text=raw[start:end].decode(),
                            replacement_text=edit["replacement"].decode()))
        shift += len(edit["replacement"]) - (end - start)
    for edit in reversed(edits):
        changed = changed[:edit["start"]] + edit["replacement"] + changed[edit["end"]:]
    restored = changed
    for edit in reversed(mapping):
        begin, end = edit["changed_start"], edit["changed_end"]
        assert restored[begin:end] == edit["replacement_text"].encode()
        restored = restored[:begin] + edit["original_text"].encode() + restored[end:]
    assert restored == raw
    return changed, mapping


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--sites", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    original = json.loads(gzip.decompress(args.inputs.read_bytes()))
    parsed = {row["id"]: row for row in json.loads(args.sites.read_text())}
    assert len(original["candidates"]) == 48
    assert len({c["id"] for c in original["candidates"]}) == 48
    args.out.mkdir(exist_ok=False)
    variants = {"import-control": [], "lazy": []}
    manifest, unsupported = [], []
    counts = collections.Counter()
    for candidate in original["candidates"]:
        row = parsed[candidate["id"]]
        assert not row["parse_errors"] and row["candidate_elaborated"] is False
        raw = candidate["code"].encode()
        for site in row["sites"]:
            assert raw[site["start_byte"]:site["end_byte"]] == site["text"].encode()
        chains = []
        for root in row["proof_bodies"]:
            for body in proof_bodies(root):
                steps = sequence(body)
                if not steps:
                    continue
                for rank, node in enumerate(steps):
                    parts = flatten(node)
                    leading = 0
                    while leading < len(parts) and interval(parts[leading]):
                        leading += 1
                    if not leading or leading == len(parts):
                        continue
                    if rank != len(steps) - 1:
                        unsupported.append(dict(id=candidate["id"],
                            start=node["start_byte"], reason="nonterminal chain; future tactic state unknown"))
                        continue
                    terms = []
                    for part in parts[:leading]:
                        names = list(identifiers(part))
                        assert len(names) == 1
                        name = names[0]
                        terms.append(raw[name["start_byte"]:name["end_byte"]])
                    tail = raw[parts[leading]["start_byte"]:node["end_byte"]]
                    replacement = b"(" + tail + b")"
                    for term in reversed(terms):
                        replacement = b"(interval_cases_then " + term + b" => " + replacement + b")"
                    chains.append(dict(start=node["start_byte"], end=node["end_byte"],
                        replacement=replacement, variables=[t.decode() for t in terms],
                        tail_kinds=[p["kind"] for p in parts[leading:]]))
                    counts[str(leading) + "_interval_chain"] += 1
        if not chains:
            unsupported.append(dict(id=candidate["id"], reason="no supported terminal chain"))
        header = row["header_end_byte"]
        assert 0 <= header <= min([c["start"] for c in chains] or [len(raw)])
        addition = b"\nimport IntervalContinuation\n\n"
        header_edit = dict(start=header, end=header, replacement=addition)
        control, control_mapping = apply(raw, [header_edit])
        lazy, lazy_mapping = apply(raw, [header_edit] + chains)
        for name, code in [("import-control", control), ("lazy", lazy)]:
            variants[name].append(dict(candidate, code=code.decode(), reuse=False))
        manifest.append(dict(id=candidate["id"], original_bytes=len(raw),
            chain_count=len(chains), interval_sites=sum(len(c["variables"]) for c in chains),
            chains=[{k:v for k,v in c.items() if k != "replacement"} for c in chains],
            import_edits=control_mapping, experimental_edits=lazy_mapping,
            inverse_restores_original_bytes=True))
    (args.out / "original.json.gz").write_bytes(args.inputs.read_bytes())
    for name, candidates in variants.items():
        compressed(args.out / (name + ".json.gz"), dict(original, candidates=candidates))
    compressed(args.out / "parser-inputs.json.gz",
        [dict(id=c["id"], code=c["code"]) for c in variants["lazy"]])
    report = dict(sources=48, prepared_chains=sum(x["chain_count"] for x in manifest),
        interval_sites=sum(x["interval_sites"] for x in manifest),
        chain_distribution=dict(counts), unsupported=unsupported, manifest=manifest,
        native_candidate_executions=0, generated_native_parse_status="pending",
        certified_global_failures=None, certified_timeout_fraction=None,
        semantic_equivalence_claim=False,
        scope="Native AST and exact inverse edits; experimental reassociation, not rejection.")
    (args.out / "preparation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    (args.out / "run-source.py").write_bytes(Path(__file__).read_bytes())
    print(json.dumps({k:v for k,v in report.items() if k != "manifest"}))


if __name__ == "__main__":
    main()
