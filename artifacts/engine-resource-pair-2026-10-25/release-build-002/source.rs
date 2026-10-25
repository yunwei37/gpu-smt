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
            let backend_identity=verifier.identity();
            let monitor=Arc::new(RecordingMonitor::new(&cell.join("rss-cpu.jsonl"))?);
            let engine=Engine::new(config.clone(),verifier,Arc::new(Fifo),
                monitor.clone(),Arc::new(HeadroomAdmission),Arc::new(MemoryCache::default()))?;
            let compressor=Gzip::start(&cell.join("capture.json.gz"))?;
            // Explicit startup/post-retirement observations also cover empty batches.
            monitor.sample(&[])?;
            let (verified,interrupted)={
                let result=engine.verify_batch(batch.clone());
                tokio::pin!(result);
                tokio::select! {
                    value=&mut result=>(value,false),
                    signal=tokio::signal::ctrl_c()=>{
                        signal?;
                        engine.shutdown().await;
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
            let terminal=json!({"state":if interrupted{"interrupted"}else{"complete"},
                "condition":condition,"external_cell_seconds":seconds,
                "clock_scope":"input decoding through native shutdown, capture serialization, compression and compressor retirement",
                "resources":config,"observations":monitor.report()?,
                "fixed_process_AS_cap":false,"interrupted":interrupted});
            fs::write(cell.join("terminal.json"),serde_json::to_vec_pretty(&terminal)?)?;
            lifecycle.push(seconds);
            captures.push(capture);
            drop(engine);
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
}
