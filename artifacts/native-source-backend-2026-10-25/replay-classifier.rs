//! Reclassify retained actual CLI responses without running Lean.
use std::io::{self,BufRead};
fn main() {
    for line in io::stdin().lock().lines() {
        let row:serde_json::Value=serde_json::from_str(&line.unwrap()).unwrap();
        let outcome=gpu_smt_lean::classify_source(
            row["exit"].as_i64().map(|v|i32::try_from(v).unwrap()),
            row["stdout"].as_str().unwrap().into(),
            row["stderr"].as_str().unwrap().into());
        println!("{}",serde_json::json!({"source_id":row["source_id"],
            "status":format!("{:?}",outcome.status).to_ascii_lowercase(),"error":outcome.error}));
    }
}
