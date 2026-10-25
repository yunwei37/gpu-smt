//! Reusable capture and paired-result accounting. No benchmark speedups are inferred
//! from fixture tests or from sums of overlapping candidate latencies.
use gpu_smt_core::{Batch, Mode, Status, Verification};
use gpu_smt_engine::Config;
use serde::{Deserialize, Serialize};
use serde_json::{Value, json};
use std::collections::{BTreeMap, BTreeSet};

/// One complete engine invocation, including inputs and operational outcomes.
#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Capture {
    /// Version of this record format, independent of engine package version.
    pub schema_version: u32,
    /// Engine package version.
    pub engine_version: String,
    /// Caller-pinned immutable native toolchain/project identity.
    pub environment: String,
    /// Actual executable/project/backend identity.
    pub backend: String,
    /// Built-in scheduling policy used in this capture.
    pub policy: String,
    /// Total actual RSS/CPU eligibility and per-worker assignment.
    pub resources: Config,
    /// Original exact sources, IDs, timeouts and reuse options.
    pub batch: Batch,
    /// Actual output for every caller, with attempts and native responses.
    pub results: Vec<Verification>,
    /// Start of executable main, Unix milliseconds.
    pub started_unix_ms: u64,
    /// Main entry through input, runtime, execution and backend shutdown.
    /// Excludes final capture serialization/output and OS executable loading.
    pub lifecycle_seconds: f64,
}
fn valid_time(n: f64) -> bool {
    n.is_finite() && n >= 0.0
}
fn indexed(c: &Capture) -> Result<BTreeMap<&str, &Verification>, String> {
    if c.schema_version != 1 || !valid_time(c.lifecycle_seconds) || c.lifecycle_seconds == 0.0 {
        return Err("unsupported capture schema or invalid lifecycle clock".into());
    }
    c.resources.validate()?;
    let ids: BTreeSet<_> = c.batch.candidates.iter().map(|v| v.id.as_str()).collect();
    let outputs: BTreeMap<_, _> = c.results.iter().map(|v| (v.id.as_str(), v)).collect();
    if ids.len() != c.batch.candidates.len()
        || outputs.len() != c.results.len()
        || ids != outputs.keys().copied().collect()
    {
        return Err("capture must contain unique, matching input and result IDs".into());
    }
    if c.results.iter().any(|v| {
        !valid_time(v.elapsed_seconds) || v.attempts.iter().any(|a| !valid_time(a.elapsed_seconds))
    }) {
        return Err("invalid candidate/attempt clock".into());
    }
    if c.batch
        .candidates
        .iter()
        .any(|v| v.timeout_ms == 0 || (c.batch.mode == Mode::FirstSuccess && v.task_id.is_none()))
    {
        return Err("invalid candidate timeout or first-success task identity".into());
    }
    Ok(outputs)
}
fn quantiles(mut values: Vec<f64>) -> Value {
    values.sort_by(f64::total_cmp);
    if values.is_empty() {
        return Value::Null;
    }
    let at = |n: usize| values[(values.len() * n).div_ceil(100).saturating_sub(1)];
    json!({"count":values.len(),"p50":at(50),"p90":at(90),"p99":at(99),"max":values.last()})
}
fn summarize(c: &Capture) -> Value {
    let mut counts = BTreeMap::<String, usize>::new();
    for v in &c.results {
        let key = serde_json::to_value(&v.outcome.status)
            .unwrap()
            .as_str()
            .unwrap()
            .to_owned();
        *counts.entry(key).or_default() += 1;
    }
    let accepted: BTreeSet<_> = c
        .results
        .iter()
        .filter(|v| v.outcome.status == Status::Accepted)
        .map(|v| v.id.as_str())
        .collect();
    let solved: BTreeSet<_> = c
        .batch
        .candidates
        .iter()
        .filter(|v| accepted.contains(v.id.as_str()))
        .filter_map(|v| v.task_id.as_deref())
        .collect();
    json!({
        "lifecycle_seconds":c.lifecycle_seconds,
        "candidates_per_second":c.results.len() as f64/c.lifecycle_seconds,
        "statuses":counts, "accepted_ids":accepted,"solved_tasks":solved,
        "cached":c.results.iter().filter(|v|v.cached).count(),
        "coalesced":c.results.iter().filter(|v|v.coalesced).count(),
        "attempts":c.results.iter().map(|v|v.attempts.len()).sum::<usize>(),
        "attempt_counts_scope":"per-caller histories; coalesced callers may repeat the same physical attempt",
        "fresh_fallback_event_rows":c.results.iter().flat_map(|v|&v.attempts)
            .flat_map(|a|&a.backend_events).filter(|e|e.stage=="fresh_fallback").count(),
        "preemptions":c.results.iter().flat_map(|v|&v.attempts)
            .filter(|a|a.status==Status::Preempted).count(),
        "sampled_peak_attempt_rss_bytes":c.results.iter().flat_map(|v|&v.attempts)
            .map(|a|a.peak_rss_bytes).max(),
        "completion_latency_seconds":quantiles(c.results.iter().map(|v|v.elapsed_seconds).collect()),
        "attempt_seconds_per_candidate":quantiles(c.results.iter().map(attempt_seconds).collect())
    })
}
fn attempt_seconds(v: &Verification) -> f64 {
    v.attempts.iter().map(|a| a.elapsed_seconds).sum()
}
fn solved_tasks(c: &Capture) -> BTreeSet<&str> {
    let accepted: BTreeSet<_> = c
        .results
        .iter()
        .filter(|v| v.outcome.status == Status::Accepted)
        .map(|v| v.id.as_str())
        .collect();
    c.batch
        .candidates
        .iter()
        .filter(|v| accepted.contains(v.id.as_str()))
        .filter_map(|v| v.task_id.as_deref())
        .collect()
}
/// Compare byte-identical candidate populations in the same pinned environment and
/// aggregate hardware domain. Different consumer modes compare task success only;
/// cancelled candidates never masquerade as native rejections.
pub fn compare(baseline: &Capture, candidate: &Capture) -> Result<Value, String> {
    let b = indexed(baseline)?;
    let c = indexed(candidate)?;
    if baseline.environment != candidate.environment {
        return Err("native environment pins differ".into());
    }
    let mut bc = baseline.resources.cpus.clone();
    let mut cc = candidate.resources.cpus.clone();
    bc.sort_unstable();
    cc.sort_unstable();
    if bc != cc || baseline.resources.memory_bytes != candidate.resources.memory_bytes {
        return Err(
            "aggregate CPU/RSS resource points differ; report these captures separately".into(),
        );
    }
    let sources: BTreeMap<_, _> = baseline
        .batch
        .candidates
        .iter()
        .map(|v| (v.id.as_str(), v))
        .collect();
    if sources.len() != candidate.batch.candidates.len()
        || candidate.batch.candidates.iter().any(|v| {
            sources.get(v.id.as_str()).is_none_or(|s| {
                s.code != v.code || s.timeout_ms != v.timeout_ms || s.task_id != v.task_id
            })
        })
    {
        return Err("candidate IDs, exact source, timeout or task populations differ".into());
    }
    let changed: Vec<_> =
        b.iter()
            .filter_map(|(id, left)| {
                let right = c[id];
                (left.outcome.status!=right.outcome.status).then(||
            json!({"id":id,"baseline":left.outcome.status,"candidate":right.outcome.status}))
            })
            .collect();
    let only_b: Vec<_> = b
        .iter()
        .filter(|(id, v)| {
            v.outcome.status == Status::Accepted && c[*id].outcome.status != Status::Accepted
        })
        .map(|(id, _)| *id)
        .collect();
    let only_c: Vec<_> = c
        .iter()
        .filter(|(id, v)| {
            v.outcome.status == Status::Accepted && b[*id].outcome.status != Status::Accepted
        })
        .map(|(id, _)| *id)
        .collect();
    let b_tasks = solved_tasks(baseline);
    let c_tasks = solved_tasks(candidate);
    let mut ranked: Vec<_> = b.values().copied().collect();
    ranked.sort_by(|l, r| {
        attempt_seconds(r)
            .total_cmp(&attempt_seconds(l))
            .then(l.id.cmp(&r.id))
    });
    let tails: Vec<_>=[1usize,10].into_iter().map(|percent|{
        let n=(ranked.len()*percent).div_ceil(100);
        let selected=&ranked[..n];
        json!({"baseline_slowest_percent":percent,
            "ranking":"sum of native attempt wall durations, excluding queue; overlapping sums are not lifecycle",
            "ids":selected.iter().map(|v|v.id.as_str()).collect::<Vec<_>>(),
            "baseline_attempt_seconds_sum":selected.iter().map(|v|attempt_seconds(v)).sum::<f64>(),
            "candidate_attempt_seconds_sum":selected.iter().map(|v|attempt_seconds(c[v.id.as_str()])).sum::<f64>(),
            "candidate_statuses":selected.iter().map(|v|json!({"id":v.id,"status":c[v.id.as_str()].outcome.status})).collect::<Vec<_>>()})
    }).collect();
    let same_all = baseline.batch.mode == Mode::All && candidate.batch.mode == Mode::All;
    let reuse_changed: Vec<_> = candidate
        .batch
        .candidates
        .iter()
        .filter(|v| sources[v.id.as_str()].reuse != v.reuse)
        .map(|v| v.id.as_str())
        .collect();
    Ok(json!({
        "baseline":summarize(baseline),"candidate":summarize(candidate),
        "lifecycle_speedup":baseline.lifecycle_seconds/candidate.lifecycle_seconds,
        "baseline_mode":baseline.batch.mode,"candidate_mode":candidate.batch.mode,
        "baseline_policy":baseline.policy,"candidate_policy":candidate.policy,
        "baseline_cores_per_worker":baseline.resources.cores_per_worker,
        "candidate_cores_per_worker":candidate.resources.cores_per_worker,
        "backend_identity_equal":baseline.backend==candidate.backend,
        "reuse_option_changed_ids":reuse_changed,
        "accepted_set_only_baseline":only_b,"accepted_set_only_candidate":only_c,
        "changed_statuses":changed,"all_candidate_status_parity_applicable":same_all,
        "all_candidate_statuses_equal":if same_all {Some(changed.is_empty())}else{None},
        "solved_tasks_only_baseline":b_tasks.difference(&c_tasks).collect::<Vec<_>>(),
        "solved_tasks_only_candidate":c_tasks.difference(&b_tasks).collect::<Vec<_>>(),
        "raw_payload_changed_ids":b.iter().filter(|(id,v)|v.outcome.response!=c[*id].outcome.response).map(|(id,_)|*id).collect::<Vec<_>>(),
        "tails":tails,
        "limits":"Lifecycle includes input/runtime/native retirement; excludes record serialization and executable loading. Keep external controller time and stderr resource logs. Pins and clocks are recorded claims, not independent authentication. First-success cancellation is not every-candidate RL parity. No speedup is admissible from ratios alone."
    }))
}
