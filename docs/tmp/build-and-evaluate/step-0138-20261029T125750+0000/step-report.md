# Step0138 — Rust runtime panic must not become a cacheable rejection

BUILD_AND_EVALUATE;root only;the single8031cell continuation actually runs.
This step fulfills the user's OSS implementation/testing work while awaiting
data. It is engineering correctness,not a new paperRQresult or contribution.
Scope:Rustsource backend classifier,one regression and relevant docs only.

## EXPERIMENT_GATE
E138.1:read actual source classifier/nearbytests. Recognized JSON errors currently
win over a later nativeINTERNALPANIC,returning cacheableRejected despite
incomplete execution. A composed earlierJSONerror+actualNat.powpanic-marker
regression reproduces failure(exit101,leftRejected). No second native capture.
E138.2:recognized fatalpanic now returns BackendError/operational explanation
before ordinary JSONerror classification,after existing memory classification.
Rawstdout/stderr/messages remain;cacheablefalse. Ordinary errors/acceptance/
admissions and allnative flags are unchanged. Remove same-function checked
unwrap to satisfy clippywithout an allow attribute.
E138.3:75Rustall-targettests pass,6realnative tests ignored locally;fmt/clippy/
rustdocwarning checks pass. Failures retained:initialsingle-CPUrun cannot
satisfy existing2CPUwatchdog integration;final uses10–11,both allowed. Formatting/
lint repairs retained. Ownsupport/nativeRSS combined sampled during checks;
no newnativecollection,otherWorkspace or productionresource changes.

## WRITE_GATE
W138.1:API documents panic precedence and uncacheablepartialexecution.
Contributor guide states actualexisting2CPUintegration requirement. One typo in
continuation artifact corrected. No publicAPI,newflag,dependency or engine
layer changes. Currentdailyreflection links realblockingfaults and next
input/cost/state-replayevidence. PaperRQs/claims/numbers unchanged;no fullwriting/
milestonereview or freshpapercompilation claimed.

## REVIEW_GATE — same-thread self-review
Direction fixed:resourceengineering is not novelty. Reproduced correctness
boundary requires a narrow change;growth is onebranch/test and documentation,
not a newabstraction. Reduction removes checkedunwrap;rawoutputs/native source
unchanged. Alltests evidence is scoped,ignorednativecases explicitlyexcluded.
Priorfailednative capture kept;continuation source frozenaee0932does not read
this mutableRustimplementation. No falsewhole-statehit or time-saved number.
Commit/push this validatedboundary,inspect actualCI,and continue livecapture
until complete. No independent review/AIdelegation or projectcomplete claim.
