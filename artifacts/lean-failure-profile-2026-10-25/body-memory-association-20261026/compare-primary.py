"""Compare selection rules on the same archived samples; no new observations."""
from pathlib import Path
import gzip
import json
import math

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / "bench/lean-failure-profile/analyze.py").is_file())
HERE = Path(__file__).resolve().parent
PRIOR = ROOT / "artifacts/source-memory-attribution-2026-10-25"
old = json.loads((PRIOR / "result.json").read_text())
new = json.loads((HERE / "final/attribution.json").read_text())
oldrows = {x["source_id"]: x for x in old["per_source"]}
primary, body, current = {}, {}, {}
with gzip.open(PRIOR / "attributed-samples.jsonl.gz", "rt") as stream:
    for line in stream:
        sample = json.loads(line)
        for process in sample["workers"]:
            key = (sample["source_id"], sample["time_ns"], process["pid"], process["birth"])
            primary[key] = process["rss"]
            if process["phase"] == "body":
                body[key] = process["rss"]
with gzip.open(HERE / "final/attribution.samples.jsonl.gz", "rt") as stream:
    for line in stream:
        sample = json.loads(line)
        key = (sample["source_id"], sample["capture_upper_ns"], sample["pid"], sample["birth"])
        current[key] = sample["sampled_rss_bytes"]
groups = {}
for status in ["lean_error", "timeout_error", "resource_failure"]:
    rows = [x for x in new["sources"] if x["profile_status"] == status]
    observed = [x for x in rows if x["associated_samples"]]
    values = sorted(x["sampled_body_leader_peak_rss_bytes"] for x in observed)
    groups[status] = dict(sources=len(rows), observed=len(observed),
        prior_body_observed=sum(oldrows[x["source_id"]]["sampled_body_worker_rss_max_bytes"] is not None for x in rows),
        p50_nearest_rank_bytes=values[math.ceil(len(values)*.5)-1],
        max_bytes=max(values),
        sources_with_lower_max_than_prior_body=sum(x["sampled_body_leader_peak_rss_bytes"] < oldrows[x["source_id"]]["sampled_body_worker_rss_max_bytes"] for x in observed),
        sources_with_higher_max_than_prior_body=sum(x["sampled_body_leader_peak_rss_bytes"] > oldrows[x["source_id"]]["sampled_body_worker_rss_max_bytes"] for x in observed))
critical = [x for x in new["sources"] if x["profile_status"] in ["resource_failure", "timeout_error"]]
result = dict(primary_result=str((PRIOR/"result.json").relative_to(ROOT)),
    primary_worker_samples=len(primary), prior_body_worker_samples=len(body),
    window_body_samples=len(current),
    window_sample_keys_not_in_prior_body=len(set(current)-set(body)),
    same_key_RSS_mismatches=sum(body[k] != v for k,v in current.items() if k in body),
    critical_sources_with_identical_primary_maxima=sum(x["sampled_body_leader_peak_rss_bytes"] == oldrows[x["source_id"]]["sampled_single_worker_rss_max_bytes"] for x in critical),
    groups=groups,
    initially_overlooked_prior_step="step-0016-20261025T115728+0000",
    role="One sensitivity control of prior observations; not newly acquired labels or a model",
    scope="Sensitivity of the same archived data, not independent or new native observations.")
(HERE/"comparison.json").write_text(json.dumps(result,indent=2)+chr(10))
assert result["window_sample_keys_not_in_prior_body"] == 0
assert result["same_key_RSS_mismatches"] == 0
assert result["critical_sources_with_identical_primary_maxima"] == len(critical)
print(json.dumps(result))
