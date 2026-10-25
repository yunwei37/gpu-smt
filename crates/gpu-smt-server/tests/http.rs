use async_trait::async_trait;
use axum::{body::Body, http::Request};
use gpu_smt_core::*;
use gpu_smt_engine::*;
use http_body_util::BodyExt;
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
    let response = gpu_smt_server::router(engine.clone())
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
