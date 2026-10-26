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

#[test]
fn measure_capture_and_compare_round_trip_retire_native_fixture() {
    use std::io::Write;
    use std::os::unix::fs::PermissionsExt;
    let path =
        std::env::temp_dir().join(format!("gpu-smt-measure-fixture-{}.py", std::process::id()));
    let mut fixture = std::fs::OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&path)
        .unwrap();
    fixture.write_all(b"#!/usr/bin/python3\nimport sys\nwhile sys.stdin.readline().strip(): pass\nprint('{\"env\":0}',flush=True)\nprint('',flush=True)\nsys.stdin.read()\n").unwrap();
    drop(fixture);
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o700)).unwrap();
    for policy in ["source-size", "task-interleave"] {
        let mut child = Command::new(env!("CARGO_BIN_EXE_gpu-smt"))
            .args([
                "measure",
                "--repl",
                path.to_str().unwrap(),
                "--project",
                "/tmp",
                "--environment",
                "fixture-not-a-native-proof",
                "--policy",
                policy,
            ])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .unwrap();
        let mut stdin = child.stdin.take().unwrap();
        stdin.write_all(br#"{"candidates":[{"id":"a","code":"a","reuse":false},{"id":"b","code":"b","reuse":false}]}"#).unwrap();
        drop(stdin);
        let result = child.wait_with_output().unwrap();
        assert!(
            result.status.success(),
            "{}",
            String::from_utf8_lossy(&result.stderr)
        );
        let capture: gpu_smt_server::measurement::Capture =
            serde_json::from_slice(&result.stdout).unwrap();
        assert_eq!(capture.policy, policy);
        assert_eq!(capture.results.len(), 2);
        for v in &capture.results {
            assert_eq!(v.outcome.status, gpu_smt_core::Status::Accepted);
            assert_eq!(v.attempts.len(), 1);
            for p in &v.attempts[0].processes {
                assert!(!std::path::Path::new(&format!("/proc/{}", p.pid)).exists());
            }
        }
        assert!(capture.lifecycle_seconds > 0.0);
        assert_eq!(
            gpu_smt_server::measurement::compare(&capture, &capture).unwrap()["lifecycle_speedup"],
            1.0
        );
    }
    std::fs::remove_file(&path).unwrap();
}

#[test]
fn native_source_arguments_reach_process_and_capture_identity() {
    use std::io::Write;
    let fixture = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("gpu-smt-lean/tests/fixtures/source.py");
    let mut child = Command::new(env!("CARGO_BIN_EXE_gpu-smt"))
        .args([
            "measure",
            "--lean",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "source-argv-fixture-not-Lean",
            "--lean-arg",
            fixture.to_str().unwrap(),
            "--lean-arg",
            "--tstack=400000",
            "--lean-arg",
            "one argument with spaces",
        ])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let code = "original α\r\n";
    child
        .stdin
        .take()
        .unwrap()
        .write_all(
            serde_json::to_string(&serde_json::json!({"candidates":[
            {"id":"argv","code":code,"reuse":false}]}))
            .unwrap()
            .as_bytes(),
        )
        .unwrap();
    let output = child.wait_with_output().unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let capture: gpu_smt_server::measurement::Capture =
        serde_json::from_slice(&output.stdout).unwrap();
    assert!(capture.backend.contains("--tstack=400000"));
    assert_eq!(
        capture.results[0].outcome.status,
        gpu_smt_core::Status::Accepted
    );
    let result = capture.results[0].outcome.response.as_ref().unwrap();
    let detail: serde_json::Value =
        serde_json::from_str(result["messages"][0]["data"].as_str().unwrap()).unwrap();
    assert_eq!(detail["source"], code);
    assert_eq!(
        detail["argv"],
        serde_json::json!([
            "--tstack=400000",
            "one argument with spaces",
            "--json",
            "--stdin"
        ])
    );
    for process in capture.results[0]
        .attempts
        .iter()
        .flat_map(|a| &a.processes)
    {
        assert!(!std::path::Path::new(&format!("/proc/{}", process.pid)).exists());
    }
}

#[test]
fn original_source_file_mode_reaches_native_file_context() {
    use std::io::Write;
    let path =
        std::env::temp_dir().join(format!("gpu-smt-cli-original-{}.lean", std::process::id()));
    let code = "unchanged original α\n";
    std::fs::write(&path, code).unwrap();
    let fixture = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .unwrap()
        .join("gpu-smt-lean/tests/fixtures/source.py");
    let mut child = Command::new(env!("CARGO_BIN_EXE_gpu-smt"))
        .args([
            "measure",
            "--lean",
            "/usr/bin/python3",
            "--project",
            "/tmp",
            "--environment",
            "file-fixture-not-Lean",
            "--lean-arg",
            fixture.to_str().unwrap(),
            "--source-file",
            path.to_str().unwrap(),
        ])
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    child
        .stdin
        .take()
        .unwrap()
        .write_all(
            serde_json::to_string(&serde_json::json!({"candidates":[
                {"id":"original","code":code,"reuse":false}
            ]}))
            .unwrap()
            .as_bytes(),
        )
        .unwrap();
    let output = child.wait_with_output().unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let capture: gpu_smt_server::measurement::Capture =
        serde_json::from_slice(&output.stdout).unwrap();
    assert!(capture.backend.contains("source-file:"));
    assert_eq!(
        capture.results[0].outcome.status,
        gpu_smt_core::Status::Accepted
    );
    let result = capture.results[0].outcome.response.as_ref().unwrap();
    let detail: serde_json::Value =
        serde_json::from_str(result["messages"][0]["data"].as_str().unwrap()).unwrap();
    assert_eq!(detail["source"], code);
    assert_eq!(
        detail["argv"],
        serde_json::json!(["--json", path.to_str().unwrap()])
    );
    for process in capture.results[0]
        .attempts
        .iter()
        .flat_map(|a| &a.processes)
    {
        assert!(!std::path::Path::new(&format!("/proc/{}", process.pid)).exists());
    }
    std::fs::remove_file(path).unwrap();
}
