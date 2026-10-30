use async_trait::async_trait;
use axum::{body::Body, http::Request};
use http_body_util::BodyExt;
use proofserve_core::*;
use proofserve_engine::*;
use serde_json::{Value, json};
use std::sync::Arc;
use tower::ServiceExt;

struct NativeFixture;
#[async_trait]
impl VerificationBackend for NativeFixture {
    fn identity(&self) -> String {
        "http-contract-fixture".into()
    }
    async fn verify(&self, _: &Candidate, _: Execution) -> Outcome {
        Outcome {
            status: Status::Accepted,
            response: Some(json!({"env":0,"messages":[]})),
            error: None,
        }
    }
}
struct Monitor;
impl ResourceMonitor for Monitor {
    fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        Ok(ResourceSnapshot::default())
    }
}
fn engine() -> Engine {
    Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0],
            cores_per_worker: 1,
        },
        Arc::new(NativeFixture),
        Arc::new(Fifo),
        Arc::new(Monitor),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap()
}
async fn post(path: &str, body: Value) -> (u16, Value) {
    let engine = engine();
    let response = proofserve::router(engine.clone())
        .oneshot(
            Request::builder()
                .method("POST")
                .uri(path)
                .header("content-type", "application/json")
                .body(Body::from(body.to_string()))
                .unwrap(),
        )
        .await
        .unwrap();
    let status = response.status().as_u16();
    let data = response.into_body().collect().await.unwrap().to_bytes();
    engine.shutdown().await;
    (status, serde_json::from_slice(&data).unwrap_or(Value::Null))
}
#[tokio::test]
async fn core_kimina_and_legacy_shapes() {
    let (status, value) = post(
        "/check",
        json!({"snippets":[{"id":"a","code":"fixture"}],"reuse":false}),
    )
    .await;
    assert_eq!(status, 200);
    assert_eq!(value["results"][0]["id"], "a");
    assert_eq!(value["results"][0]["response"]["env"], 0);
    let (status, value) = post(
        "/verify",
        json!({"codes":[{"custom_id":42,"proof":"fixture"}]}),
    )
    .await;
    assert_eq!(status, 200);
    assert_eq!(value["results"][0]["custom_id"], 42);
    assert!(value["results"][0]["response"]["time"].is_number());
}
#[tokio::test]
async fn unsupported_extensions_are_rejected() {
    assert_eq!(
        post("/check", json!({"snippets":[],"debug":true})).await.0,
        400
    );
    assert_eq!(
        post("/check", json!({"snippets":[],"unknown":true}))
            .await
            .0,
        422
    );
    assert_eq!(
        post(
            "/verify",
            json!({"codes":[{"custom_id":1,"code":"x","proof":"y"}]})
        )
        .await
        .0,
        400
    );
}

#[tokio::test]
async fn batches_larger_than_default_extractor_limit_reach_the_engine() {
    // The retained original7808Batch is14,834,061bytes. This protocol fixture
    // crosses the actual default2MiB cutoff without running a verifier.
    let code = "fixture".repeat(350_000);
    let (status, value) = post(
        "/v1/verify",
        json!({"candidates":[{"id":"large","code":code,"reuse":false}]}),
    )
    .await;
    assert_eq!(status, 200, "valid large Batch rejected before scheduling");
    assert_eq!(value["results"][0]["id"], "large");
}

// The controlled backend has no physical RSS. Declare its test-only forecast
// so the existing conservative unknown-cost policy can admit two fixture jobs.
struct DeliveryPolicy;
impl SchedulingPolicy for DeliveryPolicy {
    fn priority(&self, _: &Candidate) -> u64 {
        0
    }
    fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
        Some(1)
    }
}

struct DeliveryGate {
    started: tokio::sync::Notify,
    release: tokio::sync::Notify,
}
#[async_trait]
impl VerificationBackend for DeliveryGate {
    fn identity(&self) -> String {
        "http-delivery-fixture-not-Lean".into()
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        if c.code == "hold" {
            self.started.notify_one();
            tokio::select! {
                _ = self.release.notified() => {}
                _ = x.cancel.cancelled() =>
                    return Outcome::operational(Status::Cancelled, "fixture retired"),
            }
        }
        Outcome {
            status: Status::Accepted,
            response: Some(json!({"messages":[]})),
            error: None,
        }
    }
}
#[tokio::test]
async fn ndjson_delivers_a_result_before_slow_peer_releases() {
    let gate = Arc::new(DeliveryGate {
        started: tokio::sync::Notify::new(),
        release: tokio::sync::Notify::new(),
    });
    let engine = Engine::new(
        Config {
            memory_bytes: 100,
            cpus: vec![0, 1],
            cores_per_worker: 1,
        },
        gate.clone(),
        Arc::new(DeliveryPolicy),
        Arc::new(Monitor),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let response = proofserve::router(engine.clone())
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/v1/verify/stream")
                .header("content-type", "application/json")
                .body(Body::from(
                    json!({"candidates":[
                {"id":"slow","code":"hold","reuse":false},
                {"id":"fast","code":"fast","reuse":false}]})
                    .to_string(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.status(), 200);
    assert_eq!(response.headers()["content-type"], "application/x-ndjson");
    gate.started.notified().await;
    let mut body = response.into_body();
    let frame = tokio::time::timeout(std::time::Duration::from_secs(5), body.frame())
        .await
        .unwrap()
        .unwrap()
        .unwrap()
        .into_data()
        .unwrap();
    let first: Value = serde_json::from_slice(&frame).unwrap();
    assert_eq!(first["event"], "result");
    assert_eq!(first["index"], 1);
    assert_eq!(first["verification"]["id"], "fast");
    assert_eq!(first["verification"]["outcome"]["status"], "accepted");
    gate.release.notify_one();
    let rest = body.collect().await.unwrap().to_bytes();
    let rows: Vec<Value> = std::str::from_utf8(&rest)
        .unwrap()
        .lines()
        .map(|line| serde_json::from_str(line).unwrap())
        .collect();
    assert_eq!(rows.len(), 2);
    assert_eq!(rows[0]["verification"]["id"], "slow");
    assert_eq!(rows[1], json!({"event":"complete","count":2}));
    let (status, _) = post(
        "/v1/verify/stream",
        json!({"candidates":[
        {"id":"duplicate","code":"a"},{"id":"duplicate","code":"b"}]}),
    )
    .await;
    assert_eq!(status, 400);
    engine.shutdown().await;
}

struct RecordingNativeMonitor {
    seen: std::sync::Mutex<Vec<ProcessIdentity>>,
}
impl ResourceMonitor for RecordingNativeMonitor {
    fn sample(&self, roots: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        let mut seen = self.seen.lock().unwrap();
        for p in roots {
            if !seen.contains(p) {
                seen.push(p.clone());
            }
        }
        proofserve_engine::linux::ProcMonitor::default().sample(roots)
    }
}
#[tokio::test]
async fn dropped_http_stream_retires_real_owned_subprocess_before_shutdown() {
    let mask = std::fs::read_to_string("/proc/self/status").unwrap();
    let cpu = mask
        .lines()
        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
        .unwrap()
        .trim()
        .split([',', '-'])
        .next()
        .unwrap()
        .parse()
        .unwrap();
    let monitor = Arc::new(RecordingNativeMonitor {
        seen: Default::default(),
    });
    let fixture = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("proofserve-lean/tests/fixtures/repl.py");
    let backend = proofserve_lean::NativeRepl {
        program: "/usr/bin/python3".into(),
        args: vec![fixture.to_string_lossy().into_owned()],
        project: std::env::temp_dir(),
        environment: "stream-drop-process-fixture-not-Lean".into(),
    };
    let engine = Engine::new(
        Config {
            memory_bytes: 1 << 30,
            cpus: vec![cpu],
            cores_per_worker: 1,
        },
        Arc::new(backend),
        Arc::new(Fifo),
        monitor.clone(),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )
    .unwrap();
    let response = proofserve::router(engine.clone())
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/v1/verify/stream")
                .header("content-type", "application/json")
                .body(Body::from(
                    json!({"candidates":[
                {"id":"slow","code":"slow","reuse":false}]})
                    .to_string(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.status(), 200);
    tokio::time::timeout(std::time::Duration::from_secs(5), async {
        while monitor.seen.lock().unwrap().is_empty() {
            tokio::time::sleep(std::time::Duration::from_millis(10)).await;
        }
    })
    .await
    .unwrap();
    let owned = monitor.seen.lock().unwrap().clone();
    drop(response); // Disconnect; do not mask cancellation by shutting engine down.
    tokio::time::timeout(std::time::Duration::from_secs(5), async {
        while owned
            .iter()
            .any(|p| proofserve_engine::linux::identity(p.pid).is_ok())
        {
            tokio::time::sleep(std::time::Duration::from_millis(10)).await;
        }
    })
    .await
    .unwrap();
    assert!(!owned.is_empty());
    engine.shutdown().await;
}
