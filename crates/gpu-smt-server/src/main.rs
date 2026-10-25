//! Local engine executable. Library use does not require a network service.
use gpu_smt_core::{Batch, VerificationBackend};
use gpu_smt_engine::{
    Config, Engine, Fifo, HeadroomAdmission, MemoryCache, SourceSize, TaskInterleave,
    linux::ProcMonitor,
};
use gpu_smt_lean::{NativeLean, NativeRepl};
use std::{
    collections::HashMap,
    path::PathBuf,
    sync::Arc,
    time::{Instant, SystemTime, UNIX_EPOCH},
};
use tokio::io::{AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader};

fn cpu_eligibility() -> Result<Vec<usize>, String> {
    let mut set = libc_cpu::CpuSet::new()?;
    set.cpus()
}
// Keep Linux ABI in one small public-free module; the engine has no affinity override.
mod libc_cpu {
    pub struct CpuSet(String);
    impl CpuSet {
        pub fn new() -> Result<Self, String> {
            let status = std::fs::read_to_string("/proc/self/status").map_err(|e| e.to_string())?;
            let line = status
                .lines()
                .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
                .ok_or("CPU eligibility unavailable")?;
            Ok(Self(line.trim().into()))
        }
        pub fn cpus(&mut self) -> Result<Vec<usize>, String> {
            let mut out = vec![];
            for group in self.0.split(',') {
                let mut ends = group.split('-');
                let start = ends
                    .next()
                    .unwrap()
                    .parse::<usize>()
                    .map_err(|e| e.to_string())?;
                let end = ends
                    .next()
                    .map(|s| s.parse::<usize>())
                    .transpose()
                    .map_err(|e| e.to_string())?
                    .unwrap_or(start);
                out.extend(start..=end);
            }
            Ok(out)
        }
    }
}
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let started = Instant::now();
    let started_unix_ms = SystemTime::now()
        .duration_since(UNIX_EPOCH)?
        .as_millis()
        .try_into()?;
    tracing_subscriber::fmt()
        .json()
        .with_writer(std::io::stderr)
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "gpu_smt_engine::resources=info".into()),
        )
        .init();
    let mut args = std::env::args().skip(1);
    let command = args.next().unwrap_or_else(|| "--help".into());
    if command == "--help" || command == "help" {
        println!(
            "gpu-smt <serve|check|measure> (--repl PATH | --lean PATH) --project DIR --environment ID [--cpus 8,9,10,11] [--worker-cores 1] [--memory-gib 48] [--policy fifo|source-size|task-interleave] [--prepared-host PATH --sysroot DIR] [--listen 127.0.0.1:3000]\ngpu-smt compare BASELINE.json CANDIDATE.json"
        );
        return Ok(());
    }
    if command == "compare" {
        let baseline = args.next().ok_or("baseline capture path required")?;
        let candidate = args.next().ok_or("candidate capture path required")?;
        if args.next().is_some() {
            return Err("compare takes exactly two capture paths".into());
        }
        let baseline = serde_json::from_slice(&std::fs::read(baseline)?)?;
        let candidate = serde_json::from_slice(&std::fs::read(candidate)?)?;
        let report = gpu_smt_server::measurement::compare(&baseline, &candidate)?;
        println!("{}", serde_json::to_string_pretty(&report)?);
        return Ok(());
    }
    if !matches!(command.as_str(), "serve" | "check" | "measure") {
        return Err("expected serve, check, measure or compare".into());
    }
    let mut options = HashMap::new();
    while let Some(key) = args.next() {
        if ![
            "--repl",
            "--lean",
            "--project",
            "--environment",
            "--cpus",
            "--worker-cores",
            "--memory-gib",
            "--listen",
            "--policy",
            "--prepared-host",
            "--sysroot",
        ]
        .contains(&key.as_str())
        {
            return Err(format!("unknown option {key}").into());
        }
        let value = args
            .next()
            .ok_or_else(|| format!("missing value for {key}"))?;
        if options.insert(key.clone(), value).is_some() {
            return Err(format!("duplicate {key}").into());
        }
    }
    let required = |key: &str| {
        options
            .get(key)
            .cloned()
            .ok_or_else(|| format!("{key} is required"))
    };
    let eligible = cpu_eligibility()?;
    let cpus = if let Some(text) = options.get("--cpus") {
        text.split(',')
            .map(str::parse::<usize>)
            .collect::<Result<Vec<_>, _>>()?
    } else {
        eligible.clone()
    };
    if cpus.iter().any(|cpu| !eligible.contains(cpu)) {
        return Err("CPU outside current eligibility".into());
    }
    let config = Config {
        memory_bytes: options
            .get("--memory-gib")
            .map(|s| s.parse::<u64>())
            .transpose()?
            .unwrap_or(48)
            .checked_mul(1024 * 1024 * 1024)
            .ok_or("memory size overflow")?,
        cpus,
        cores_per_worker: options
            .get("--worker-cores")
            .map(|s| s.parse())
            .transpose()?
            .unwrap_or(1),
    };
    let environment = required("--environment")?;
    let project = PathBuf::from(required("--project")?).canonicalize()?;
    let verifier: Arc<dyn VerificationBackend> =
        match (options.get("--repl"), options.get("--lean")) {
            (Some(program), None) => {
                let backend = NativeRepl {
                    program: PathBuf::from(program).canonicalize()?,
                    args: vec![],
                    project,
                    environment: environment.clone(),
                };
                match (options.get("--prepared-host"), options.get("--sysroot")) {
                    (None, None) => Arc::new(backend),
                    (Some(host), Some(sysroot)) => Arc::new(gpu_smt_lean::PreparedRepl::new(
                        backend,
                        PathBuf::from(host).canonicalize()?,
                        PathBuf::from(sysroot).canonicalize()?,
                    )),
                    _ => return Err("--prepared-host and --sysroot are required together".into()),
                }
            }
            (None, Some(program)) => {
                if options.contains_key("--prepared-host") || options.contains_key("--sysroot") {
                    return Err("prepared import parent requires --repl".into());
                }
                Arc::new(NativeLean {
                    program: PathBuf::from(program).canonicalize()?,
                    project,
                    environment: environment.clone(),
                })
            }
            _ => return Err("specify exactly one of --repl or --lean".into()),
        };
    gpu_smt_engine::linux::bind_current_thread(&config.cpus)?;
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(config.cpus.len())
        .enable_all()
        .build()?;
    runtime.block_on(run(
        command,
        options,
        config,
        verifier,
        environment,
        started,
        started_unix_ms,
    ))
}

async fn run(
    command: String,
    options: HashMap<String, String>,
    config: Config,
    verifier: Arc<dyn VerificationBackend>,
    environment: String,
    started: Instant,
    started_unix_ms: u64,
) -> Result<(), Box<dyn std::error::Error>> {
    let policy_name = options
        .get("--policy")
        .map(String::as_str)
        .unwrap_or("fifo");
    let policy: Arc<dyn gpu_smt_core::SchedulingPolicy> = match policy_name {
        "fifo" => Arc::new(Fifo),
        "source-size" => Arc::new(SourceSize),
        "task-interleave" => Arc::new(TaskInterleave::new(Fifo)),
        _ => return Err("unknown scheduling policy".into()),
    };
    let backend_identity = verifier.identity();
    let engine = Engine::new(
        config.clone(),
        verifier,
        policy,
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )?;
    if command == "measure" {
        let mut source = String::new();
        tokio::io::stdin().read_to_string(&mut source).await?;
        let batch: Batch = serde_json::from_str(&source)?;
        let results = engine.verify_batch(batch.clone()).await?;
        engine.shutdown().await;
        let capture = gpu_smt_server::measurement::Capture {
            schema_version: 1,
            engine_version: env!("CARGO_PKG_VERSION").into(),
            environment,
            backend: backend_identity,
            policy: policy_name.into(),
            resources: config,
            batch,
            results,
            started_unix_ms,
            lifecycle_seconds: started.elapsed().as_secs_f64(),
        };
        let mut stdout = tokio::io::stdout();
        stdout
            .write_all(serde_json::to_string(&capture)?.as_bytes())
            .await?;
        stdout.write_all(b"\n").await?;
        stdout.flush().await?;
    } else if command == "check" {
        let mut lines = BufReader::new(tokio::io::stdin()).lines();
        let mut stdout = tokio::io::stdout();
        while let Some(line) = lines.next_line().await? {
            let response = match serde_json::from_str::<Batch>(&line) {
                Ok(batch) => match engine.verify_batch(batch).await {
                    Ok(results) => serde_json::json!({"results":results}),
                    Err(error) => serde_json::json!({"error":error}),
                },
                Err(error) => serde_json::json!({"error":error.to_string()}),
            };
            stdout
                .write_all(serde_json::to_string(&response)?.as_bytes())
                .await?;
            stdout.write_all(b"\n").await?;
            stdout.flush().await?;
        }
        engine.shutdown().await;
    } else {
        let listener = tokio::net::TcpListener::bind(
            options
                .get("--listen")
                .map(String::as_str)
                .unwrap_or("127.0.0.1:3000"),
        )
        .await?;
        let shutdown = engine.clone();
        axum::serve(listener, gpu_smt_server::router(engine))
            .with_graceful_shutdown(async move {
                let _ = tokio::signal::ctrl_c().await;
                shutdown.shutdown().await;
            })
            .await?;
    }
    Ok(())
}
