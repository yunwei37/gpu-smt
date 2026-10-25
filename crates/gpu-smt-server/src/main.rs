//! Local engine executable. Library use does not require a network service.
use gpu_smt_core::Batch;
use gpu_smt_engine::{Config, Engine, Fifo, HeadroomAdmission, MemoryCache, linux::ProcMonitor};
use gpu_smt_lean::NativeRepl;
use std::{collections::HashMap, path::PathBuf, sync::Arc};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

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
            "gpu-smt <serve|check> --repl PATH --project DIR --environment ID [--cpus 8,9,10,11] [--worker-cores 1] [--memory-gib 48] [--listen 127.0.0.1:3000]"
        );
        return Ok(());
    }
    if !matches!(command.as_str(), "serve" | "check") {
        return Err("expected serve or check".into());
    }
    let mut options = HashMap::new();
    while let Some(key) = args.next() {
        if ![
            "--repl",
            "--project",
            "--environment",
            "--cpus",
            "--worker-cores",
            "--memory-gib",
            "--listen",
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
    let backend = NativeRepl {
        program: PathBuf::from(required("--repl")?).canonicalize()?,
        args: vec![],
        project: PathBuf::from(required("--project")?).canonicalize()?,
        environment: required("--environment")?,
    };
    gpu_smt_engine::linux::bind_current_thread(&config.cpus)?;
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(config.cpus.len())
        .enable_all()
        .build()?;
    runtime.block_on(run(command, options, config, backend))
}

async fn run(
    command: String,
    options: HashMap<String, String>,
    config: Config,
    backend: NativeRepl,
) -> Result<(), Box<dyn std::error::Error>> {
    let engine = Engine::new(
        config,
        Arc::new(backend),
        Arc::new(Fifo),
        Arc::new(ProcMonitor::default()),
        Arc::new(HeadroomAdmission),
        Arc::new(MemoryCache::default()),
    )?;
    if command == "check" {
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
