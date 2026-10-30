//! Preview task-aware ordering only. No verifier, worker or native verdict starts.
use proofserve_core::{Batch, SchedulingPolicy};
use proofserve_engine::{Fifo, TaskInterleave};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let source = std::io::read_to_string(std::io::stdin())?;
    let batch: Batch = serde_json::from_str(&source)?;
    let policy = TaskInterleave::new(Fifo);
    let keys = policy.batch_priorities(&batch.candidates, batch.mode);
    let mut order: Vec<_> = (0..batch.candidates.len()).collect();
    order.sort_by_key(|i| (keys[*i], *i));
    let ids: Vec<_> = order.iter().map(|i| &batch.candidates[*i].id).collect();
    println!(
        "{}",
        serde_json::to_string(&serde_json::json!({
            "policy":"task-interleave", "mode":batch.mode, "ordered_ids":ids,
            "scope":"ordering preview only; no verification/admission or native outcome"
        }))?
    );
    Ok(())
}
