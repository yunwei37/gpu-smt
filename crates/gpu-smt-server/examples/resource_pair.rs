//! Matched native fresh/prepared resource pair through the public engine API.
//! Run only after the owning research collection retires. This example adds
//! no scheduler/service and does not reproduce a third-party verifier system.
use gpu_smt_core::*;
use gpu_smt_engine::{Config, Engine, Fifo, HeadroomAdmission, MemoryCache, linux::ProcMonitor};
use gpu_smt_lean::{NativeRepl, PreparedRepl};
use gpu_smt_server::measurement::{Capture, compare};
use serde_json::{Value, json};
use std::{
    fs::{self, File},
    io::{BufWriter, Write},
    path::{Path, PathBuf},
    process::{Child, ChildStdin, Command, Stdio},
    sync::{Arc, Mutex},
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};

/// Compression is our child and therefore included in ProcMonitor ownership.
/// Every error path closes/kills/reaps it; partial output stays on disk.
struct Gzip {
    child: Child,
    input: Option<ChildStdin>,
}
impl Gzip {
    fn start(path: &Path) -> Result<Self, Box<dyn std::error::Error>> {
        let mut child = Command::new("gzip")
            .arg("-c")
            .stdin(Stdio::piped())
            .stdout(File::create_new(path)?)
            .spawn()?;
        let input = child.stdin.take();
        Ok(Self { child, input })
    }
    fn finish(mut self, capture: &Capture) -> Result<(), Box<dyn std::error::Error>> {
        serde_json::to_writer(
            self.input.as_mut().ok_or("compression input missing")?,
            capture,
        )?;
        self.input.take(); // EOF: drain final compressed bytes before the cell clock stops.
        if !self.child.wait()?.success() {
            return Err("capture compressor failed".into());
        }
        Ok(())
    }
}
impl Drop for Gzip {
    fn drop(&mut self) {
        self.input.take();
        if !matches!(self.child.try_wait(), Ok(Some(_))) {
            let _ = self.child.kill();
        }
        let _ = self.child.wait();
    }
}

/// Flush each physical attempt before returning it to the engine. The final
/// capture remains authoritative for queued cancellations and consumer latency;
/// this journal retains completed native attempts after an interrupted run.
struct JournalBackend {
    inner: Arc<dyn VerificationBackend>,
    output: Mutex<BufWriter<File>>,
    errors: Mutex<Vec<String>>,
}
impl JournalBackend {
    fn new(inner: Arc<dyn VerificationBackend>, path: &Path) -> Result<Self, std::io::Error> {
        Ok(Self {
            inner,
            output: Mutex::new(BufWriter::new(File::create_new(path)?)),
            errors: Mutex::new(Vec::new()),
        })
    }
    fn record(&self, c: &Candidate, outcome: &Outcome, exclusive: bool, seconds: f64) {
        let result = (|| -> Result<(), String> {
            let mut output = self.output.lock().map_err(|e| e.to_string())?;
            let row = json!({"id":c.id,"task_id":c.task_id,
                "attempt_timeout_ms":c.timeout_ms,"exclusive_retry":exclusive,
                "native_attempt_seconds":seconds,"outcome":outcome});
            serde_json::to_writer(&mut *output, &row).map_err(|e| e.to_string())?;
            writeln!(&mut *output).map_err(|e| e.to_string())?;
            output.flush().map_err(|e| e.to_string())
        })();
        if let Err(error) = result {
            self.errors
                .lock()
                .unwrap_or_else(|e| e.into_inner())
                .push(error);
        }
    }
    fn errors(&self) -> Vec<String> {
        self.errors
            .lock()
            .unwrap_or_else(|e| e.into_inner())
            .clone()
    }
}
#[async_trait::async_trait]
impl VerificationBackend for JournalBackend {
    fn identity(&self) -> String {
        self.inner.identity()
    }
    fn prepared_state_ready(&self) -> bool {
        self.inner.prepared_state_ready()
    }
    async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
        let start = Instant::now();
        let outcome = self.inner.verify(c, x).await;
        self.record(c, &outcome, false, start.elapsed().as_secs_f64());
        outcome
    }
    async fn verify_resource_retry(&self, c: &Candidate, x: Execution) -> Outcome {
        let start = Instant::now();
        let outcome = self.inner.verify_resource_retry(c, x).await;
        self.record(c, &outcome, true, start.elapsed().as_secs_f64());
        outcome
    }
    async fn shutdown(&self) {
        self.inner.shutdown().await;
    }
}

/// Persist final caller outcomes as they retire, independently of the physical
/// attempt log. Complete covers consumer rows, not backend shutdown/cell time.
async fn collect_results(
    mut stream: gpu_smt_engine::BatchStream,
    batch: &Batch,
    mut output: impl Write,
) -> std::io::Result<Vec<Verification>> {
    let mut results = vec![None; batch.candidates.len()];
    while let Some(event) = stream.recv().await {
        match &event {
            BatchEvent::Result {
                index,
                verification,
            } => {
                if results.get(*index).is_none_or(Option::is_some)
                    || batch.candidates[*index].id != verification.id
                {
                    return Err(std::io::Error::other("invalid consumer result index/ID"));
                }
            }
            BatchEvent::Complete { count }
                if *count != results.len() || results.iter().any(Option::is_none) =>
            {
                return Err(std::io::Error::other("incomplete consumer result count"));
            }
            _ => {}
        }
        serde_json::to_writer(&mut output, &event).map_err(std::io::Error::other)?;
        writeln!(&mut output)?;
        output.flush()?;
        match event {
            BatchEvent::Result {
                index,
                verification,
            } => results[index] = Some(verification),
            BatchEvent::Complete { .. } => {
                return Ok(results.into_iter().map(Option::unwrap).collect());
            }
            BatchEvent::Error { message } => return Err(std::io::Error::other(message)),
        }
    }
    Err(std::io::Error::other("consumer stream EOF before Complete"))
}

struct Observations {
    last: Option<Instant>,
    output: BufWriter<File>,
    peak_rss: u64,
    max_registered: usize,
    samples: u64,
}
struct RecordingMonitor {
    inner: ProcMonitor,
    start: Instant,
    observations: Mutex<Observations>,
}
impl RecordingMonitor {
    fn new(path: &Path) -> Result<Self, Box<dyn std::error::Error>> {
        Ok(Self {
            inner: ProcMonitor::default(),
            start: Instant::now(),
            observations: Mutex::new(Observations {
                last: None,
                output: BufWriter::new(File::create_new(path)?),
                peak_rss: 0,
                max_registered: 0,
                samples: 0,
            }),
        })
    }
    fn report(&self) -> Result<Value, String> {
        let mut o = self.observations.lock().map_err(|e| e.to_string())?;
        o.output.flush().map_err(|e| e.to_string())?;
        Ok(json!({"sampled_peak_rss_bytes":o.peak_rss,
            "max_observed_registered_leaders":o.max_registered,"retained_samples":o.samples,
            "scope":"RSS includes this driver/engine and all owned native/compressor descendants; registered leaders are not proof of busy CPU cores"}))
    }
}
impl ResourceMonitor for RecordingMonitor {
    fn sample(&self, roots: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
        let sample = self.inner.sample(roots)?;
        let mut o = self.observations.lock().map_err(|e| e.to_string())?;
        o.peak_rss = o.peak_rss.max(sample.rss_bytes);
        o.max_registered = o.max_registered.max(sample.processes.len());
        // Admission can sample frequently; retain at most one diagnostic per
        // second, while the unchanged engine watchdog still samples each second.
        if o.last
            .is_none_or(|last| last.elapsed() >= Duration::from_secs(1))
        {
            let leaders: Vec<_> = sample
                .processes
                .iter()
                .map(|p| {
                    let raw = fs::read_to_string(format!("/proc/{}/stat", p.identity.pid)).ok();
                    let stat = raw
                        .as_deref()
                        .and_then(|s| s.rsplit_once(')').map(|(_, t)| t));
                    let fields = stat.map(|s| s.split_whitespace().collect::<Vec<_>>());
                    let cpu = fields.as_ref().and_then(|f| {
                        if f.get(19)?.parse::<u64>().ok()? != p.identity.start_ticks {
                            return None;
                        }
                        Some(json!({"user_ticks":f.get(11)?.parse::<u64>().ok()?,
                        "system_ticks":f.get(12)?.parse::<u64>().ok()?}))
                    });
                    let affinity = fs::read_to_string(format!("/proc/{}/status", p.identity.pid))
                        .ok()
                        .and_then(|s| {
                            s.lines()
                                .find_map(|l| l.strip_prefix("Cpus_allowed_list:").map(str::trim))
                                .map(str::to_owned)
                        });
                    let still_owned = gpu_smt_engine::linux::identity(p.identity.pid)
                        .is_ok_and(|identity| identity == p.identity);
                    json!({"identity":p.identity,"tree_rss_bytes":p.rss_bytes,
                    "cpu_ticks":if still_owned{cpu}else{None},
                    "allowed_cpus":if still_owned{affinity}else{None}})
                })
                .collect();
            let row = json!({"seconds":self.start.elapsed().as_secs_f64(),
                "aggregate_rss_bytes":sample.rss_bytes,"registered_leaders":leaders});
            serde_json::to_writer(&mut o.output, &row).map_err(|e| e.to_string())?;
            writeln!(&mut o.output).map_err(|e| e.to_string())?;
            o.output.flush().map_err(|e| e.to_string())?;
            o.last = Some(Instant::now());
            o.samples += 1;
        }
        Ok(sample)
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.len() == 1 && args[0] == "--help" {
        println!(
            "resource_pair INPUT.json REPL PROJECT PREPARED_HOST SYSROOT ENVIRONMENT RESOURCES.json OUTPUT_DIR"
        );
        return Ok(());
    }
    let [
        input,
        repl,
        project,
        host,
        sysroot,
        environment,
        resources,
        output,
    ] = args.as_slice()
    else {
        return Err("expected eight arguments; see --help".into());
    };
    let config: Config = serde_json::from_reader(File::open(resources)?)?;
    config.validate()?;
    gpu_smt_engine::linux::bind_current_thread(&config.cpus)?;
    tracing_subscriber::fmt()
        .json()
        .with_writer(std::io::stderr)
        .with_env_filter("gpu_smt_engine::resources=info")
        .init();
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(config.cpus.len())
        .enable_all()
        .build()?;
    let output = PathBuf::from(output);
    fs::create_dir(&output)?;
    let backend = NativeRepl {
        program: PathBuf::from(repl).canonicalize()?,
        args: vec![],
        project: PathBuf::from(project).canonicalize()?,
        environment: environment.clone(),
    };
    fs::write(
        output.join("manifest.json"),
        serde_json::to_vec_pretty(&json!({
            "input":input,"repl":backend.program,"project":backend.project,
            "prepared_host":host,"sysroot":sysroot,"environment":environment,
            "resources":config,"order":["native","prepared"],
            "LEAN_PATH":std::env::var("LEAN_PATH").ok(),
            "LEAN_SYSROOT":std::env::var("LEAN_SYSROOT").ok(),
            "one_collection_at_a_time":"caller must retire its previous owning collection before running",
            "scope":"same API/native input/resources; prior resource mechanisms are not novelty"
        }))?,
    )?;
    runtime.block_on(async {
        // Register before any native child starts; never signal another collection.
        let mut terminate=tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())?;
        let mut captures=Vec::new();
        let mut lifecycle=Vec::new();
        for condition in ["native","prepared"] {
            let cell=output.join(condition);fs::create_dir(&cell)?;
            let start=Instant::now();
            let started_unix_ms=SystemTime::now().duration_since(UNIX_EPOCH)?
                .as_millis().try_into()?;
            // Input decoding/validation is included independently in each cell.
            let batch:Batch=serde_json::from_reader(File::open(input)?)?;
            let verifier:Arc<dyn VerificationBackend>=if condition=="native" {
                Arc::new(backend.clone())
            } else {
                Arc::new(PreparedRepl::new(backend.clone(),
                    PathBuf::from(host).canonicalize()?,PathBuf::from(sysroot).canonicalize()?))
            };
            let verifier=Arc::new(JournalBackend::new(verifier,&cell.join("attempts.jsonl"))?);
            let backend_identity=verifier.identity();
            let monitor=Arc::new(RecordingMonitor::new(&cell.join("rss-cpu.jsonl"))?);
            let engine=Engine::new(config.clone(),verifier.clone(),Arc::new(Fifo),
                monitor.clone(),Arc::new(HeadroomAdmission),Arc::new(MemoryCache::default()))?;
            let compressor=Gzip::start(&cell.join("capture.json.gz"))?;
            // Explicit startup/post-retirement observations also cover empty batches.
            monitor.sample(&[])?;
            let (verified,interrupted)={
                // Open before stream submission so a setup fault launches no work.
                let output=BufWriter::new(File::create_new(cell.join("results.jsonl"))?);
                let stream=engine.verify_stream(batch.clone()).map_err(std::io::Error::other)?;
                let result=collect_results(stream,&batch,output);
                tokio::pin!(result);
                tokio::select! {
                    value=&mut result=>(value,false),
                    signal=async {
                        tokio::select! {
                            signal=tokio::signal::ctrl_c()=>signal,
                            _=terminate.recv()=>Ok(()),
                        }
                    }=>{
                        engine.shutdown().await;
                        signal?;
                        (result.await,true)
                    }
                }
            };
            engine.shutdown().await;
            monitor.sample(&[])?;
            let results=verified?;
            let capture=Capture {
                schema_version:1,engine_version:env!("CARGO_PKG_VERSION").into(),
                environment:environment.clone(),backend:backend_identity,
                policy:"fifo".into(),resources:config.clone(),batch,results,
                started_unix_ms,lifecycle_seconds:start.elapsed().as_secs_f64(),
            };
            compressor.finish(&capture)?;
            let seconds=start.elapsed().as_secs_f64();
            let journal_errors=verifier.errors();
            let terminal=json!({"state":if interrupted{"interrupted"}else if !journal_errors.is_empty(){"evidence_error"}else{"complete"},
                "journal_errors":journal_errors,
                "journal_scope":"flushed physical native attempts; no power-loss durability claim",
                "consumer_journal":"results.jsonl",
                "consumer_journal_scope":"flushed final caller BatchEvents; Complete covers consumer rows only, not idle-backend shutdown or whole-cell lifecycle; EOF without Complete is partial",
                "condition":condition,"external_cell_seconds":seconds,
                "clock_scope":"input decoding through native shutdown, capture serialization, compression and compressor retirement",
                "resources":config,"observations":monitor.report()?,
                "fixed_process_AS_cap":false,"interrupted":interrupted});
            fs::write(cell.join("terminal.json"),serde_json::to_vec_pretty(&terminal)?)?;
            lifecycle.push(seconds);
            captures.push(capture);
            drop(engine);
            if !journal_errors.is_empty() { return Err::<(),Box<dyn std::error::Error>>("attempt journal I/O failure; raw capture retained".into()); }
            if interrupted {return Err::<(),Box<dyn std::error::Error>>("pair interrupted; partial records retained".into());}
        }
        let mut summary=compare(&captures[0],&captures[1])?;
        summary["external_cell_seconds"]=json!({"native":lifecycle[0],"prepared":lifecycle[1]});
        summary["external_native_over_prepared"]=json!(lifecycle[0]/lifecycle[1]);
        summary["scope"]=json!("matched own-engine native/prepared support measurement; not a strongest-warm-baseline or novelty claim; no timer/source/oracle change");
        fs::write(output.join("comparison.json"),serde_json::to_vec_pretty(&summary)?)?;
        Ok::<(),Box<dyn std::error::Error>>(())
    })?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    fn temporary(label: &str) -> PathBuf {
        std::env::temp_dir().join(format!(
            "gpu-smt-resource-pair-{}-{}-{}",
            label,
            std::process::id(),
            SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos()
        ))
    }
    #[test]
    fn physical_attempt_is_readable_before_final_capture() {
        let path = temporary("journal");
        let backend: Arc<dyn VerificationBackend> = Arc::new(NativeRepl {
            program: "/not-run".into(),
            args: vec![],
            project: std::env::temp_dir(),
            environment: "journal-fixture".into(),
        });
        let journal = JournalBackend::new(backend, &path).unwrap();
        let candidate = Candidate {
            id: "proof".into(),
            task_id: Some("task".into()),
            code: "original".into(),
            timeout_ms: 300000,
            reuse: false,
        };
        let outcome = Outcome::operational(Status::ResourceExhausted, "native allocation failed");
        journal.record(&candidate, &outcome, false, 0.25);
        journal.record(&candidate, &outcome, true, 0.5);
        let rows: Vec<Value> = fs::read_to_string(&path)
            .unwrap()
            .lines()
            .map(|line| serde_json::from_str(line).unwrap())
            .collect();
        assert_eq!(rows.len(), 2);
        assert_eq!(rows[0]["id"], "proof");
        assert_eq!(rows[0]["outcome"]["error"], "native allocation failed");
        assert_eq!(rows[1]["exclusive_retry"], true);
        assert!(journal.errors().is_empty());
        drop(journal);
        fs::remove_file(path).unwrap();
    }
    #[test]
    fn compressed_capture_roundtrips_and_retires_child() {
        let path = temporary("gzip");
        let capture = Capture {
            schema_version: 1,
            engine_version: "test".into(),
            environment: "fixture".into(),
            backend: "fixture".into(),
            policy: "fifo".into(),
            resources: Config {
                memory_bytes: 48 * 1024 * 1024 * 1024,
                cpus: vec![0],
                cores_per_worker: 1,
            },
            batch: Batch {
                mode: Mode::All,
                candidates: vec![],
            },
            results: vec![],
            started_unix_ms: 0,
            lifecycle_seconds: 0.001,
        };
        let compressor = Gzip::start(&path).unwrap();
        let pid = compressor.child.id();
        compressor.finish(&capture).unwrap();
        assert!(!Path::new(&format!("/proc/{pid}")).exists());
        let decoded = Command::new("gzip")
            .args(["-dc"])
            .arg(&path)
            .output()
            .unwrap();
        assert!(decoded.status.success());
        let roundtrip: Capture = serde_json::from_slice(&decoded.stdout).unwrap();
        assert_eq!(roundtrip.environment, capture.environment);
        assert_eq!(
            roundtrip.resources.memory_bytes,
            capture.resources.memory_bytes
        );
        fs::remove_file(path).unwrap();
    }
    #[test]
    fn recording_monitor_uses_actual_owned_rss_and_flushes_observations() {
        let path = temporary("rss");
        let monitor = RecordingMonitor::new(&path).unwrap();
        let own = gpu_smt_engine::linux::identity(std::process::id()).unwrap();
        let sample = monitor.sample(&[own]).unwrap();
        assert!(sample.rss_bytes > 0);
        let report = monitor.report().unwrap();
        assert!(report["sampled_peak_rss_bytes"].as_u64().unwrap() > 0);
        let lines = fs::read_to_string(&path).unwrap();
        let row: Value = serde_json::from_str(lines.lines().next().unwrap()).unwrap();
        assert!(row["aggregate_rss_bytes"].as_u64().unwrap() > 0);
        assert_eq!(row["registered_leaders"].as_array().unwrap().len(), 1);
        drop(monitor);
        fs::remove_file(path).unwrap();
    }

    struct GateBackend {
        started: tokio::sync::Notify,
        release: tokio::sync::Notify,
        active: std::sync::atomic::AtomicUsize,
    }
    #[async_trait::async_trait]
    impl VerificationBackend for GateBackend {
        fn identity(&self) -> String {
            "consumer-retention-fixture-not-Lean".into()
        }
        async fn verify(&self, c: &Candidate, x: Execution) -> Outcome {
            use std::sync::atomic::Ordering;
            self.active.fetch_add(1, Ordering::SeqCst);
            let status = if c.id == "slow" {
                self.started.notify_one();
                tokio::select! {
                    _ = self.release.notified() => Status::Rejected,
                    _ = x.cancel.cancelled() => Status::Cancelled,
                }
            } else {
                Status::Accepted
            };
            self.active.fetch_sub(1, Ordering::SeqCst);
            Outcome::operational(status, "controlled fixture only")
        }
    }
    struct FixtureResources;
    impl ResourceMonitor for FixtureResources {
        fn sample(&self, _: &[ProcessIdentity]) -> Result<ResourceSnapshot, String> {
            Ok(ResourceSnapshot::default())
        }
    }
    impl SchedulingPolicy for FixtureResources {
        fn priority(&self, _: &Candidate) -> u64 {
            0
        }
        fn predicted_rss(&self, _: &Candidate) -> Option<u64> {
            Some(1)
        }
    }
    fn journal_fixture() -> (Engine, Arc<GateBackend>, Batch) {
        let backend = Arc::new(GateBackend {
            started: tokio::sync::Notify::new(),
            release: tokio::sync::Notify::new(),
            active: std::sync::atomic::AtomicUsize::new(0),
        });
        let engine = Engine::new(
            Config {
                memory_bytes: 100,
                cpus: vec![0, 1],
                cores_per_worker: 1,
            },
            backend.clone(),
            Arc::new(FixtureResources),
            Arc::new(FixtureResources),
            Arc::new(HeadroomAdmission),
            Arc::new(MemoryCache::default()),
        )
        .unwrap();
        let batch = Batch {
            mode: Mode::All,
            candidates: ["slow", "fast"]
                .into_iter()
                .map(|id| Candidate {
                    id: id.into(),
                    task_id: None,
                    code: id.into(),
                    timeout_ms: 300000,
                    reuse: false,
                })
                .collect(),
        };
        (engine, backend, batch)
    }

    #[tokio::test]
    async fn consumer_rows_survive_a_held_peer_and_an_interrupted_collector() {
        for complete in [true, false] {
            let (engine, backend, batch) = journal_fixture();
            let path = temporary("consumer");
            let output = BufWriter::new(File::create_new(&path).unwrap());
            let stream = engine.verify_stream(batch.clone()).unwrap();
            let collector =
                tokio::spawn(async move { collect_results(stream, &batch, output).await });
            tokio::time::timeout(Duration::from_secs(2), backend.started.notified())
                .await
                .unwrap();
            let until = Instant::now() + Duration::from_secs(2);
            let prefix = loop {
                let prefix = fs::read_to_string(&path).unwrap();
                if prefix.ends_with('\n') {
                    break prefix;
                }
                assert!(
                    Instant::now() < until,
                    "completed fast result was not flushed"
                );
                tokio::time::sleep(Duration::from_millis(10)).await;
            };
            let first: Value = serde_json::from_str(prefix.lines().next().unwrap()).unwrap();
            assert_eq!(first["event"], "result");
            assert_eq!(first["index"], 1);
            assert_eq!(first["verification"]["id"], "fast");
            assert_eq!(first["verification"]["outcome"]["status"], "accepted");
            assert!(
                !collector.is_finished(),
                "held peer must still be unresolved"
            );
            if complete {
                backend.release.notify_one();
                let results = collector.await.unwrap().unwrap();
                assert_eq!(
                    results.iter().map(|v| v.id.as_str()).collect::<Vec<_>>(),
                    ["slow", "fast"]
                );
                assert_eq!(results[0].outcome.status, Status::Rejected);
                assert_eq!(results[1].outcome.status, Status::Accepted);
                assert!(results.iter().all(|v| v.attempts.len() == 1));
            } else {
                collector.abort();
                assert!(collector.await.unwrap_err().is_cancelled());
            }
            engine.shutdown().await;
            assert_eq!(backend.active.load(std::sync::atomic::Ordering::SeqCst), 0);
            let rows: Vec<Value> = fs::read_to_string(&path)
                .unwrap()
                .lines()
                .map(|line| serde_json::from_str(line).unwrap())
                .collect();
            assert_eq!(
                rows.iter().filter(|r| r["event"] == "complete").count(),
                usize::from(complete)
            );
            assert_eq!(rows.len(), if complete { 3 } else { 1 });
            if complete {
                assert_eq!(rows.last().unwrap()["count"], 2);
            }
            fs::remove_file(path).unwrap();
        }
    }

    #[tokio::test]
    async fn consumer_write_failure_propagates_after_owned_work_retires() {
        struct FailedOutput;
        impl Write for FailedOutput {
            fn write(&mut self, _: &[u8]) -> std::io::Result<usize> {
                Err(std::io::Error::other("controlled journal write failure"))
            }
            fn flush(&mut self) -> std::io::Result<()> {
                Ok(())
            }
        }
        let (engine, backend, batch) = journal_fixture();
        let stream = engine.verify_stream(batch.clone()).unwrap();
        let result = collect_results(stream, &batch, FailedOutput).await;
        // Same unconditional cleanup boundary as the example's cell.
        engine.shutdown().await;
        assert!(
            result
                .unwrap_err()
                .to_string()
                .contains("controlled journal write failure")
        );
        assert_eq!(backend.active.load(std::sync::atomic::Ordering::SeqCst), 0);
    }
}
