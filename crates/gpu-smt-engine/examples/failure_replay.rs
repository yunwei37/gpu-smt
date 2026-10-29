//! Simulated adapter usage only: no Lean, solver, source verdict or performance result.
use async_trait::async_trait;
use gpu_smt_core::{FailureReplayBackend, TacticCompletion};
use gpu_smt_engine::FailureCache;
use tokio_util::sync::CancellationToken;

struct Simulation;
#[async_trait]
impl FailureReplayBackend for Simulation {
    type Key = u64;
    type Record = (u64, u64, &'static str); // New goal,action heartbeats,error.
    type State = (u64, u64, Option<&'static str>);
    type Exception = &'static str;

    fn replay_input(&self, state: &Self::State) -> Option<(String, u64)> {
        Some(("simulation-only|generation1".into(), state.0))
    }
    async fn replay_failure(
        &self,
        state: &mut Self::State,
        scope: &str,
        key: &u64,
        record: &Self::Record,
        cancel: &CancellationToken,
    ) -> Result<Option<Self::Exception>, String> {
        if cancel.is_cancelled()
            || self.replay_input(state) != Some((scope.into(), *key))
            || state.1 < record.1
        {
            return Ok(None);
        }
        state.0 = record.0;
        state.1 -= record.1;
        state.2 = Some(record.2);
        Ok(Some(record.2))
    }
}

#[tokio::main]
async fn main() {
    let backend = Simulation;
    let cache = FailureCache::default();
    let mut state = (7, 100, None);
    let input = cache.capture(&backend, &state).unwrap();
    cache.remember(
        input,
        TacticCompletion::OrdinaryFailure((8, 9, "simulated ordinary failure")),
    );
    let replayed = cache
        .try_replay(&backend, &mut state, &CancellationToken::new())
        .await
        .unwrap();
    // A native adapter must rethrow this exception through its original native
    // backtracking path. Applying a failed transition is not tactic success.
    assert_eq!(replayed, Some("simulated ordinary failure"));
    assert_eq!(state, (8, 91, Some("simulated ordinary failure")));
    println!("simulation only: transition applied,9 action heartbeats charged;no verifier ran");
}
