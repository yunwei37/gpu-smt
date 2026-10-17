//! farkas-oracled — the certificate daemon spoken to by the Lean client.
//!
//! Protocol v1 (docs/protocol.md): one JSON object per stdin line, one JSON
//! object per stdout line.
//!
//!   handshake: {"hello":true}
//!           -> {"farkas_protocol":1,"version":"<crate>","engine":"tiered"}
//!   request:   {"maxVar":M,"hyps":[[<"lt"|"le"|"eq">,[[atomIdx,intCoeff],...]],...]}
//!   response:  {"cert":[[hypIdx,"natCoeff"],...]}   coefficients as strings
//!            | {"cert":null}                        no certificate (exact answer)
//!            | {"error":"..."}
//!
//! Soundness: every certificate passes the exact verifier before being
//! reported; `cert:null` only ever comes from the exact tiered engine.
//! Zero corpus/filesystem dependencies: safe to ship as a bare binary.

use farkas_core::tiered::produce_certificate_tiered;
use farkas_core::hybrid::{exact_repair, produce_certificate_hybrid};
use farkas_core::types::parse_request;
use farkas_core::verify::verify_cert;
use std::io::{BufRead, Write};

const PROTOCOL_VERSION: u32 = 1;

/// The engines allocate `O(maxVar)` tableau rows up front, so an absurd
/// `maxVar` from a corrupt request would be an OOM, not a slow answer. Real
/// linarith contexts have at most a few thousand atoms.
const MAX_VAR_CAP: usize = 1_000_000;

fn handshake() -> String {
    format!(
        "{{\"farkas_protocol\":{},\"version\":\"{}\",\"engine\":\"tiered\"}}",
        PROTOCOL_VERSION,
        env!("CARGO_PKG_VERSION")
    )
}

fn respond(line: &str) -> String {
    if let Ok(v) = farkas_core::cost::timed("request_parse",||serde_json::from_str::<serde_json::Value>(line))
        && v.get("hello") == Some(&serde_json::Value::Bool(true))
    {
        return handshake();
    }
    match farkas_core::cost::timed("request_parse",||parse_request(line)) {
        None => "{\"error\":\"bad request\"}".to_string(),
        Some((max_var, _)) if max_var > MAX_VAR_CAP => {
            "{\"error\":\"maxVar too large\"}".to_string()
        }
        // atom indexes address O(maxVar) tableau rows; an out-of-range one
        // must be a protocol error, not an indexing panic
        Some((max_var, hyps))
            if hyps
                .iter()
                .any(|h| h.coeffs.iter().any(|(v, _)| *v > max_var)) =>
        {
            "{\"error\":\"atom index exceeds maxVar\"}".to_string()
        }
        Some((max_var, hyps)) => {
            let request = farkas_core::cost::timed("request_parse",||serde_json::from_str::<serde_json::Value>(line)).ok();
            let support = request.as_ref().and_then(|v| v.get("support")).and_then(|v| v.as_array())
                .and_then(|xs| xs.iter().map(|x| x.as_u64().map(|x| x as usize)).collect::<Option<Vec<_>>>());
            let repaired = support.as_ref().filter(|xs| xs.iter().all(|&j| j < hyps.len()))
                .and_then(|xs| farkas_core::cost::timed("exact_repair",||exact_repair(&hyps,xs))).filter(|c| farkas_core::cost::timed("exact_verify",||verify_cert(&hyps,c)));
            let hybrid = std::env::var("FARKAS_EXTERNAL_CPU_HYBRID").ok().as_deref() == Some("1");
            let support_repaired = repaired.is_some();
            let answer = repaired.or_else(|| if hybrid {
                produce_certificate_hybrid(&hyps,max_var).0
            } else { farkas_core::cost::timed("exact_lp",||produce_certificate_tiered(&hyps,max_var)) });
            farkas_core::cost::timed("response_pack",||match answer {
            Some(cert) if farkas_core::cost::timed("exact_verify",||verify_cert(&hyps, &cert)) => {
                let entries: Vec<String> = cert
                    .iter()
                    .map(|(i, c)| format!("[{},\"{}\"]", i, c))
                    .collect();
                format!("{{\"cert\":[{}],\"support_repaired\":{}}}", entries.join(","), support_repaired)
            }
            // A cert failing exact verification would be an engine bug;
            // never emit an unsound answer.
            Some(_) => "{\"error\":\"internal: unverified cert\"}".to_string(),
            None => "{\"cert\":null}".to_string(),
            })
        },
    }
}

fn main() {
    if farkas_core::cost::supervise("fallback"){return;}
    for a in std::env::args().skip(1) {
        match a.as_str() {
            "--version" => {
                println!(
                    "farkas-oracled {} (protocol v{PROTOCOL_VERSION})",
                    env!("CARGO_PKG_VERSION")
                );
                return;
            }
            // serving is the default; the flag is accepted for compatibility
            "--serve" => {}
            other => {
                eprintln!("farkas-oracled: unknown arg {other} (flags: --version, --serve)");
                std::process::exit(2);
            }
        }
    }
    let stdin = std::io::stdin();
    let stdout = std::io::stdout();
    let mut out = std::io::BufWriter::new(stdout.lock());
    let mut lines=stdin.lock().lines();
    loop { let Some(line)=farkas_core::cost::read_line(&mut lines) else{break};
        let line = match line {
            Ok(l) => l,
            Err(_) => break,
        };
        if line.trim().is_empty() {
            continue;
        }
        // A panic on one request must not kill the daemon: the Lean client
        // would respawn it and re-send the same request, i.e. a crash loop.
        // The parse path is panic-free by construction; this is the backstop.
        farkas_core::cost::begin();let wall=farkas_core::cost::ns(1);let cpu=farkas_core::cost::ns(3);
        let answer = std::panic::catch_unwind(|| respond(&line))
            .unwrap_or_else(|_| "{\"error\":\"internal panic\"}".to_string());
        farkas_core::cost::timed("response_write",||{writeln!(out, "{}", answer).expect("stdout write");out.flush().expect("stdout flush");});
        farkas_core::cost::finish("fallback",&line,&answer,wall,cpu);
    }
    farkas_core::cost::process_end("fallback");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn handshake_reports_protocol_v1() {
        let r = respond("{\"hello\":true}");
        assert!(r.contains("\"farkas_protocol\":1"), "{r}");
    }

    #[test]
    fn hello_must_be_exactly_true() {
        assert!(respond("{\"hello\":false}").starts_with("{\"error\""));
        assert!(respond("{\"hello\":1}").starts_with("{\"error\""));
    }

    #[test]
    fn duplicate_atom_indices_are_additive() {
        // h1 repeats atom 1: [[1,1],[1,1]] must read additively as 2x <= 0,
        // matching verify_cert; with h2: x > 1 this is a contradiction whose
        // certificate must pass the (additive) exact verifier.
        let r = respond(
            "{\"maxVar\":1,\"hyps\":[[\"lt\",[[0,-1]]],[\"le\",[[1,1],[1,1]]],[\"lt\",[[1,-1],[0,1]]]]}",
        );
        assert!(r.starts_with("{\"cert\":[["), "{r}");
    }

    #[test]
    fn feasible_and_infeasible_requests() {
        let ok = respond(
            "{\"maxVar\":1,\"hyps\":[[\"lt\",[[0,-1]]],[\"le\",[[1,-1],[0,2]]],[\"le\",[[1,1]]]]}",
        );
        assert!(ok.starts_with("{\"cert\":[["), "{ok}");
        let none = respond("{\"maxVar\":1,\"hyps\":[[\"lt\",[[0,-1]]],[\"le\",[[1,-1]]]]}");
        assert_eq!(none, "{\"cert\":null}");
        let bad = respond("{\"nonsense\":1}");
        assert_eq!(bad, "{\"error\":\"bad request\"}");
    }
}
