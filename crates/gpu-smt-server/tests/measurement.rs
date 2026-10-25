//! Differential accounting must expose semantic and resource differences.
use gpu_smt_core::*;
use gpu_smt_engine::Config;
use gpu_smt_server::measurement::{Capture, compare};
fn fixture() -> Capture {
    let batch: Batch = serde_json::from_value(serde_json::json!({"candidates":[
        {"id":"a","task_id":"t","code":"first"},
        {"id":"b","task_id":"t","code":"second"}]}))
    .unwrap();
    Capture {
        schema_version: 1,
        engine_version: "fixture".into(),
        environment: "pinned".into(),
        backend: "fixture".into(),
        policy: "fifo".into(),
        resources: Config {
            memory_bytes: 48 << 30,
            cpus: vec![8, 9, 10, 11],
            cores_per_worker: 1,
        },
        results: batch
            .candidates
            .iter()
            .map(|c| Verification {
                id: c.id.clone(),
                outcome: Outcome {
                    status: Status::Accepted,
                    response: Some(serde_json::json!({"env":0})),
                    error: None,
                },
                attempts: vec![],
                elapsed_seconds: 1.0,
                cached: false,
                coalesced: false,
            })
            .collect(),
        batch,
        started_unix_ms: 0,
        lifecycle_seconds: 2.0,
    }
}
#[test]
fn compares_sets_not_just_equal_accepted_counts() {
    let mut a = fixture();
    let mut b = fixture();
    a.results[0].outcome.status = Status::Rejected;
    b.results[1].outcome.status = Status::Rejected;
    b.lifecycle_seconds = 1.0;
    let v = compare(&a, &b).unwrap();
    assert_eq!(v["lifecycle_speedup"], 2.0);
    assert_eq!(v["accepted_set_only_baseline"], serde_json::json!(["b"]));
    assert_eq!(v["accepted_set_only_candidate"], serde_json::json!(["a"]));
    assert_eq!(v["all_candidate_statuses_equal"], false);
}
#[test]
fn refuses_population_or_hardware_clock_pooling() {
    let a = fixture();
    let mut b = a.clone();
    b.batch.candidates[0].code.push(' ');
    assert!(compare(&a, &b).is_err());
    b = a.clone();
    b.resources.memory_bytes /= 2;
    assert!(compare(&a, &b).is_err());
    b = a.clone();
    b.environment.push('x');
    assert!(compare(&a, &b).is_err());
    b = a.clone();
    b.results.pop();
    assert!(compare(&a, &b).is_err());
}
#[test]
fn first_success_does_not_claim_per_candidate_parity() {
    let a = fixture();
    let mut b = a.clone();
    b.batch.mode = Mode::FirstSuccess;
    b.results[1].outcome = Outcome::operational(Status::Cancelled, "checked sibling passed");
    let v = compare(&a, &b).unwrap();
    assert!(v["all_candidate_statuses_equal"].is_null());
    assert_eq!(v["all_candidate_status_parity_applicable"], false);
    assert_eq!(v["solved_tasks_only_baseline"], serde_json::json!([]));
    assert_eq!(v["solved_tasks_only_candidate"], serde_json::json!([]));
    assert_eq!(v["candidate"]["statuses"]["cancelled"], 1);
}
#[test]
fn records_retry_cost_and_operational_failure_in_tails() {
    let a = fixture();
    let mut b = a.clone();
    let attempt = Attempt {
        status: Status::Preempted,
        elapsed_seconds: 3.0,
        peak_rss_bytes: 99,
        exclusive: false,
        processes: vec![],
        preemption_rss_bytes: Some(100),
        backend_events: vec![],
    };
    b.results[0].attempts = vec![
        attempt,
        Attempt {
            status: Status::ResourceExhausted,
            elapsed_seconds: 4.0,
            peak_rss_bytes: 100,
            exclusive: true,
            processes: vec![],
            preemption_rss_bytes: Some(101),
            backend_events: vec![],
        },
    ];
    b.results[0].outcome = Outcome::operational(Status::ResourceExhausted, "solo budget");
    let v = compare(&a, &b).unwrap();
    assert_eq!(v["candidate"]["preemptions"], 1);
    assert_eq!(v["candidate"]["sampled_peak_attempt_rss_bytes"], 100);
    assert_eq!(v["candidate"]["peak_attempt_observed_rss_bytes"], 100);
    assert!(
        v["candidate"]["attempt_peak_rss_scope"]
            .as_str()
            .unwrap()
            .contains("backend supplements")
    );
    assert_eq!(v["candidate"]["attempt_seconds_per_candidate"]["max"], 7.0);
}

#[test]
fn task_availability_is_internal_and_keeps_unsolved_tasks_explicit() {
    let mut capture = fixture();
    capture.lifecycle_seconds = 4.0;
    capture.results[0].elapsed_seconds = 3.0;
    capture.results[1].elapsed_seconds = 0.5;
    let mut input = capture.batch.candidates[0].clone();
    input.id = "failed".into();
    input.task_id = Some("unsolved".into());
    input.code = "rejected source".into();
    capture.batch.candidates.push(input);
    let mut output = capture.results[0].clone();
    output.id = "failed".into();
    output.outcome.status = Status::Rejected;
    output.outcome.response = Some(serde_json::json!({
        "env":0, "messages":[{"severity":"error","data":"fixture error"}]
    }));
    capture.results.push(output);
    let report = compare(&capture, &capture).unwrap();
    let summary = &report["candidate"];
    assert_eq!(summary["declared_task_count"], 2);
    assert_eq!(summary["internal_task_first_success_seconds"]["t"], 0.5);
    assert_eq!(summary["internal_solved_task_latency_seconds"]["count"], 1);
    assert_eq!(summary["unsolved_tasks"], serde_json::json!(["unsolved"]));
    assert_eq!(summary["returned_candidates_per_second"], 0.75);
    assert!(
        summary["task_latency_scope"]
            .as_str()
            .unwrap()
            .contains("not streamed")
    );
    assert!(
        summary["candidates_per_second_scope"]
            .as_str()
            .unwrap()
            .contains("not fresh native")
    );
}
