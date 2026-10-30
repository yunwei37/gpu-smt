//! HTTP adapters for the core Kimina check/legacy-verify contracts.
//! Unsupported debug/infotree options are rejected, not silently ignored.

#![warn(missing_docs)]
pub mod measurement;

use axum::{
    Json, Router,
    extract::{DefaultBodyLimit, State},
    http::StatusCode,
    routing::{get, post},
};
use proofserve_core::{Batch, Candidate, Mode, Status, Verification};
use proofserve_engine::Engine;
use serde::Deserialize;
use serde_json::{Value, json};

/// Build embeddable service routes sharing one global engine.
pub fn router(engine: Engine) -> Router {
    Router::new()
        .route("/health", get(health))
        .route("/v1/verify", post(native_batch))
        .route("/v1/verify/stream", post(native_stream))
        .route("/check", post(check))
        .route("/check/", post(check))
        .route("/verify", post(legacy))
        .route("/one_pass_verify_batch", post(legacy))
        // Full released populations exceed Axum's2MiB extractor default.
        // Actual process-memory admission/watchdog remains the resource contract.
        .layer(DefaultBodyLimit::disable())
        .with_state(engine)
}
async fn health(State(engine): State<Engine>) -> Result<Json<Value>, Error> {
    engine
        .health()
        .map_err(|e| (StatusCode::SERVICE_UNAVAILABLE, Json(json!({"error":e}))))?;
    Ok(Json(
        json!({"status":"ok","api_version":"0.1","native_backend_warm":engine.prepared_state_ready()}),
    ))
}
type Error = (StatusCode, Json<Value>);
fn error(e: impl ToString) -> Error {
    (
        StatusCode::BAD_REQUEST,
        Json(json!({"error":e.to_string()})),
    )
}
async fn native_batch(
    State(engine): State<Engine>,
    Json(batch): Json<Batch>,
) -> Result<Json<Value>, Error> {
    let results = engine.verify_batch(batch).await.map_err(error)?;
    Ok(Json(json!({"results":results})))
}
struct JsonLines(proofserve_engine::BatchStream);
impl futures_core::Stream for JsonLines {
    type Item = Result<axum::body::Bytes, std::io::Error>;
    fn poll_next(
        self: std::pin::Pin<&mut Self>,
        cx: &mut std::task::Context<'_>,
    ) -> std::task::Poll<Option<Self::Item>> {
        self.get_mut().0.poll_recv(cx).map(|event| {
            event.map(|event| {
                serde_json::to_vec(&event)
                    .map(|mut bytes| {
                        bytes.push(b'\n');
                        axum::body::Bytes::from(bytes)
                    })
                    .map_err(std::io::Error::other)
            })
        })
    }
}
async fn native_stream(
    State(engine): State<Engine>,
    Json(batch): Json<Batch>,
) -> Result<axum::response::Response, Error> {
    use axum::response::IntoResponse;
    let stream = engine.verify_stream(batch).map_err(error)?;
    Ok((
        [(axum::http::header::CONTENT_TYPE, "application/x-ndjson")],
        axum::body::Body::from_stream(JsonLines(stream)),
    )
        .into_response())
}

/// Kimina source snippet.
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Snippet {
    /// Caller ID.
    pub id: String,
    /// Complete source.
    pub code: String,
}
fn timeout() -> f64 {
    300.0
}
fn yes() -> bool {
    true
}
/// Supported core Kimina /check body.
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CheckRequest {
    /// Batch sources.
    pub snippets: Vec<Snippet>,
    /// Native timeout seconds.
    #[serde(default = "timeout")]
    pub timeout: f64,
    /// False disables both completed reuse and coalescing.
    #[serde(default = "yes")]
    pub reuse: bool,
    /// Debug extensions are currently unsupported.
    #[serde(default)]
    pub debug: bool,
    /// Infotree extensions are currently unsupported.
    #[serde(default)]
    pub infotree: Option<Value>,
}
fn millis(t: f64) -> Result<u64, Error> {
    if !t.is_finite() || t <= 0.0 || t > u64::MAX as f64 / 1000.0 {
        return Err(error("invalid timeout"));
    }
    let n = (t * 1000.0) as u64;
    if n == 0 {
        return Err(error("timeout below millisecond resolution"));
    }
    Ok(n)
}
fn compatible(v: Verification) -> Value {
    let operational = match v.outcome.status {
        Status::Timeout => Some("Lean REPL command timed out".to_owned()),
        Status::ResourceExhausted => Some(format!(
            "resource_failure: {}",
            v.outcome.error.unwrap_or_default()
        )),
        Status::BackendError | Status::Cancelled | Status::Preempted => v.outcome.error,
        _ => None,
    };
    json!({"id":v.id,"time":v.elapsed_seconds,"response":v.outcome.response,"error":operational})
}
async fn check(
    State(engine): State<Engine>,
    Json(body): Json<CheckRequest>,
) -> Result<Json<Value>, Error> {
    if body.debug || body.infotree.is_some() {
        return Err(error("debug/infotree extensions are not supported"));
    }
    let ms = millis(body.timeout)?;
    let candidates = body
        .snippets
        .into_iter()
        .map(|s| Candidate {
            id: s.id,
            code: s.code,
            task_id: None,
            timeout_ms: ms,
            reuse: body.reuse,
        })
        .collect();
    let results = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates,
        })
        .await
        .map_err(error)?;
    Ok(Json(
        json!({"results":results.into_iter().map(compatible).collect::<Vec<_>>()}),
    ))
}
/// Legacy proof or code form with original numeric/string ID.
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LegacyCode {
    /// Numeric or string caller identity.
    pub custom_id: Value,
    /// Legacy proof source.
    #[serde(default)]
    pub proof: Option<String>,
    /// Alternative code source.
    #[serde(default)]
    pub code: Option<String>,
}
/// Core legacy /verify body.
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LegacyRequest {
    /// Original caller entries.
    pub codes: Vec<LegacyCode>,
    /// Timeout seconds.
    #[serde(default = "timeout")]
    pub timeout: f64,
    /// Disable completed/in-flight reuse.
    #[serde(default)]
    pub disable_cache: bool,
    /// Unsupported infotree extension.
    #[serde(default)]
    pub infotree_type: Option<Value>,
}
async fn legacy(
    State(engine): State<Engine>,
    Json(body): Json<LegacyRequest>,
) -> Result<Json<Value>, Error> {
    if body.infotree_type.is_some() {
        return Err(error("infotree extension is not supported"));
    }
    let ms = millis(body.timeout)?;
    let mut candidates = vec![];
    let mut ids = vec![];
    for (index, item) in body.codes.into_iter().enumerate() {
        if !item.custom_id.is_string() && !item.custom_id.is_number() {
            return Err(error("custom_id must be a string or number"));
        }
        let code = match (item.code, item.proof) {
            (Some(c), None) | (None, Some(c)) => c,
            (Some(c), Some(p)) if c == p => c,
            _ => return Err(error("provide one unambiguous code/proof")),
        };
        ids.push(item.custom_id);
        candidates.push(Candidate {
            id: index.to_string(),
            code,
            task_id: None,
            timeout_ms: ms,
            reuse: !body.disable_cache,
        });
    }
    let results = engine
        .verify_batch(Batch {
            mode: Mode::All,
            candidates,
        })
        .await
        .map_err(error)?;
    let results: Vec<_> = results
        .into_iter()
        .zip(ids)
        .map(|(v, id)| {
            let mut r = compatible(v);
            let map = r.as_object_mut().unwrap();
            map.remove("id");
            map.insert("custom_id".into(), id);
            let elapsed = map.get("time").cloned().unwrap_or(Value::Null);
            if let Some(response) = map.get_mut("response").and_then(Value::as_object_mut) {
                response.insert("time".into(), elapsed);
            }
            r
        })
        .collect();
    Ok(Json(json!({"results":results})))
}
