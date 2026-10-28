
"""Replay completed captures; never execute native candidates."""
import gzip, importlib.util, json
from pathlib import Path
a=Path(__file__).resolve().parent
root=next(p for p in a.parents if (p/"Cargo.toml").is_file())
spec=importlib.util.spec_from_file_location("cmp",root/"bench/lean-warm-resource/compare.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
reference=a.parent/"warm-resource-qualification-20261028T044624Z"
old=mod.read_point(reference)
new=json.loads(gzip.decompress((a/"engine.stdout.gz").read_bytes()))
assert json.loads((a/"terminal.json").read_text())["state"]=="retry-frontier24-complete"
point={**old,"engine":new,"engine_exit":json.loads((a/"engine-exit.json").read_text())}
replayed=mod.compare(point)
saved=json.loads((a/"comparison.json").read_text())
assert all(saved[k]==v for k,v in replayed.items()), "Paired analysis replay differs"
previous={x["id"]:x for x in old["engine"]["results"]}
changes=[x["id"]for x in new["results"]if x["outcome"]!=previous[x["id"]]["outcome"]]
assert changes==saved["old_engine_raw_outcome_changed_ids"]
assert 1-point["engine_exit"]["external_seconds"]/old["engine_exit"]["external_seconds"]==saved["new_elapsed_reduction_vs_old_engine_fraction"]
assert 1-point["engine_exit"]["external_seconds"]/old["warm_exit"]["external_seconds"]==saved["new_elapsed_reduction_vs_retained_warm_fraction"]
print(json.dumps({"paired_fields_exact":True,"old_outcomes_exact":True,"elapsed_reductions_exact":True,"native_candidate_executions":0},indent=2))
