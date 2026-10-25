//! Cache data-structure microbenchmark, never whole-verifier throughput.
use gpu_smt_core::{CacheKey, Outcome, ResultCache, Status};
use gpu_smt_engine::MemoryCache;
use std::{hint::black_box, time::Instant};
fn main() {
    let cache = MemoryCache::default();
    let key = CacheKey {
        backend: "fixed-environment".into(),
        code: "complete original source".repeat(100),
        timeout_ms: 300000,
    };
    cache.insert(
        key.clone(),
        Outcome::operational(Status::Accepted, "benchmark native-outcome fixture"),
    );
    let start = Instant::now();
    let operations = 100000;
    for _ in 0..operations {
        black_box(cache.get(black_box(&key)));
    }
    println!(
        "exact completed-result lookups={operations}, elapsed_seconds={:.6}; excludes verifier and service work",
        start.elapsed().as_secs_f64()
    );
}
