//! Executable runtime hardware accounting, with no native proof workload.
use std::{
    collections::BTreeSet,
    io::Read,
    process::{Command, Stdio},
    time::Duration,
};
fn mask(text: &str) -> BTreeSet<usize> {
    let mut result = BTreeSet::new();
    for group in text.trim().split(',') {
        let parts: Vec<_> = group.split('-').collect();
        let a = parts[0].parse::<usize>().unwrap();
        let b = parts.get(1).map(|s| s.parse().unwrap()).unwrap_or(a);
        result.extend(a..=b);
    }
    result
}
#[test]
fn runtime_threads_inherit_the_same_cpu_budget() {
    let status = std::fs::read_to_string("/proc/self/status").unwrap();
    let eligible = mask(
        status
            .lines()
            .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
            .unwrap(),
    );
    let chosen: BTreeSet<_> = eligible.into_iter().take(2).collect();
    let args = chosen
        .iter()
        .map(usize::to_string)
        .collect::<Vec<_>>()
        .join(",");
    let mut child = Command::new(env!("CARGO_BIN_EXE_gpu-smt"))
        .args([
            "check",
            "--repl",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "affinity-only-no-verification",
            "--cpus",
            &args,
        ])
        .stdin(Stdio::piped())
        .stdout(Stdio::null())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let pid = child.id();
    let mut observed = vec![];
    for _ in 0..100 {
        if let Ok(entries) = std::fs::read_dir(format!("/proc/{pid}/task")) {
            observed = entries
                .filter_map(Result::ok)
                .filter_map(|e| std::fs::read_to_string(e.path().join("status")).ok())
                .filter_map(|s| {
                    s.lines()
                        .find_map(|l| l.strip_prefix("Cpus_allowed_list:"))
                        .map(mask)
                })
                .collect();
        }
        if observed.len() >= chosen.len() + 2 {
            break;
        }
        std::thread::sleep(Duration::from_millis(10));
    }
    let alive = child.try_wait().unwrap().is_none();
    if alive {
        child.kill().unwrap();
    }
    child.wait().unwrap();
    let mut errors = String::new();
    child
        .stderr
        .take()
        .unwrap()
        .read_to_string(&mut errors)
        .unwrap();
    assert!(alive, "CLI exited early: {errors}");
    assert!(
        observed.len() >= chosen.len() + 2,
        "runtime did not initialize: {errors}"
    );
    assert!(
        observed.iter().all(|cpus| *cpus == chosen),
        "{observed:?} outside {chosen:?}"
    );
}

#[test]
fn structured_resource_logs_do_not_corrupt_jsonl_results() {
    use std::io::{BufRead, Write};
    let mut child = Command::new(env!("CARGO_BIN_EXE_gpu-smt"))
        .args([
            "check",
            "--repl",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "jsonl-logging-no-native-proof",
        ])
        .env("RUST_LOG", "gpu_smt_engine::resources=info")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let mut input = child.stdin.take().unwrap();
    input.write_all(b"{\"candidates\":[]}\n").unwrap();
    input.flush().unwrap();
    let mut output = std::io::BufReader::new(child.stdout.take().unwrap());
    let mut line = String::new();
    output.read_line(&mut line).unwrap();
    std::thread::sleep(Duration::from_millis(30));
    drop(input);
    child.wait().unwrap();
    let mut errors = String::new();
    child
        .stderr
        .take()
        .unwrap()
        .read_to_string(&mut errors)
        .unwrap();
    let response: serde_json::Value = serde_json::from_str(&line).unwrap();
    assert_eq!(response["results"], serde_json::json!([]));
    assert!(
        errors
            .lines()
            .filter_map(|l| serde_json::from_str::<serde_json::Value>(l).ok())
            .any(|v| v["fields"]["rss_bytes"].is_u64()),
        "{errors}"
    );
}
