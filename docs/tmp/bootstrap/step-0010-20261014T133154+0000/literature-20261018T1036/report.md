# Arithmetic oracle novelty and GPU capacity: root source review

Observed2026-10-18UTC. Root sole executor;this is self-review,not an independent
audit. Previous goal turn is progress:completed full1000CPU comparison,pushed
source/data,paperandrealpositive/negativeGPUpreflights. This turn revalidates
the live full1000driver193488/child193489 and protectedprefix5256,then advances
this independent scientific question. No healthy capture is restarted.

## Claims and finite coverage boundary

Read the current user instructions,Initial Narrative,fourRQcontract and paper.
The user asks for OSDI-level systems contribution beyond existingLeanservices,
cache/snapshot work and ordinary CPUoptimization. The initial native prepared
state/independent candidate execution position remains intact. Numerical
primitives support RQ4;timing alone doesnot replace RQ1-3or create novelty.

C1:untrusted external arithmetic search,with exact positive and negative
certificates,can accelerate completeLeanverification. C2:manyindependent
smallLPs can be solved simultaneously onGPU,with per-LPcancellation.
C3:after strongnative reuse,the service can create enough independent
heterogeneous work to improve completeverification at equalCPU/memory.

Search covers same problem/mechanism/metric and formal-verification/LP/GPU
performance communities. It ends after primary evidence establishes risk and
the next decisive experiment;it isnot a global claim of absence. No concept
name or new acronym is proposed. No scientific scope is narrowed.

## Search nodes and verified primary evidence

1. Queries:Lean linarith external oracle HiGHS exact Farkas infeasibility
certificate;formally verified linear programming infeasibility certificate
checker Isabelle exact rational;Lean proof verification service oracle
certificate linarith acceleration. Revisions restrict to officialMathlib/
GitHub/arXiv rather than search-engine generated summaries.

Mathlib's source-native interface already separates certificate search from
proof reconstruction. The current PositiveVector documentation describes a
nonnegative nullspace vector with a positive strict coordinate. Generic
external-oracle/Lean-checker separation is therefore notnew.
https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Linarith/Oracle/SimplexAlgorithm/PositiveVector.html
https://github.com/leanprover-community/mathlib4/blob/master/Mathlib/Tactic/Linarith/Verification.lean

The live original Farkas repository at5a38a7e8502213cb644faa2e11a15429f0cf0f9a
already implements a native exact solver and proof-free probing followed by
stock proof construction on selected hypotheses. Its hybrid.rs explicitly
treats floating infeasibility as a hint requiring exactfallback. Our exact dual
capability adds a tested optimization relative to that implementation,but is
not the first external Lean oracle,exact repair or selective preprocessing.
https://github.com/lucifer1004/farkas/tree/5a38a7e8502213cb644faa2e11a15429f0cf0f9a
https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/oracle/native/src/hybrid.rs

2. Queries:formally verified LPcertificate infeasibility/unboundedness;Linear
Programming in Isabelle/HOL artifact. Primary proceedings and artifact verified.

Schaeffeler/Abdulaziz,Formally Verified Approximate Policy Iteration,AAAI2025,
section on LPcertification,uses external exactLPsolutions with verified
checking. It also formalizes infeasibility and unboundedness certificates.
The official artifact exports an Isabellechecker and includes a SoPlexwrapper.
Thus neither dual certificates nor a general trusted checker around an
untrustedLPsolver supplies our new systems contribution. Our present Rust
negative checker is tested code,not that formallyverified implementation.
https://ojs.aaai.org/index.php/AAAI/article/view/34868
https://ojs.aaai.org/index.php/AAAI/article/download/34868/37023
https://github.com/schaeffm/fmdp_isabelle
https://github.com/schaeffm/fmdp_isabelle/tree/main/isabelle/code/lp_cert

Parsert,Linear Programming in Isabelle/HOL,arXiv2403.19639v1(2024),constructs
a verified LPsolver using duality and existing simplex formalization. This is
a separate formal-solver alternative;the arXivpage alone doesnot establish a
conference acceptance. Citation-only precedent,not a need to reimplement an
Isabelleproject for our Leanbenchmark.
https://arxiv.org/abs/2403.19639
https://arxiv.org/html/2403.19639v1

3. Queries:GPUbatched smallLPsimplex;exactpaper title+code;BLPGsourcecode;
AmitGurung/RajarshiRayGPUartifact. Secondaryleads only lead to primaryPDF.

Gurung/Ray,Simultaneous Solving of Batched Linear Programs on a GPU,
ICPE2019,DOI10.1145/3297663.3310308,already assigns oneCUDAblock perLP,
uses coalesced tableauoperations and evaluates Netlib plus a reachability
application. Its batch-size results show that small batches can lose.
The reported implementation restricts infeasible-start problem dimensions
through its thread layout;our larger real matrices cannot simply be omitted
to fit it. Offlinebatch/oldCPU comparisons donot predict Leanend-to-endgain.
Our one-block-per-LPdesign is implementation reuse of an established pattern,
not first-batched-simplex novelty.
https://research.spec.org/icpe_proceedings/2019/proceedings/p59.pdf
https://doi.org/10.1145/3297663.3310308
https://arxiv.org/abs/1802.08557

The primary paper names bitbucket.org/rajgurung777/simplexprojects as source.
The browser cannotreadit and an actual request fromtheowningWorkspace to
api.bitbucket.org/2.0/repositories/rajgurung777/simplexprojects returns404.
This establishes presentaccessfailure,not why it is unavailable. The authors'
XSpeed GitLab repository is accessible and exposes GLPK/LPwrapper paths in
its first treepage;that alone isnot recovered batchedGPUsource. No substitute
fork is called official and no first/optimalGPUsolver claim is made.
https://bitbucket.org/rajgurung777/simplexprojects
https://gitlab.com/raj.ray84/XSpeed

## Risk,contradictions and root disposition

C1andC2have high same-mechanism risk. Reject first-externaloracle,firstdual
certificate andfirstGPUbatchprimitive claims. The rootimplementednegative
termination is real relative to the retainedFarkascode,but its mathematics
and exact-checker architecture have prior art. GPUcancellation/ray checking
are integration mechanisms whose whole-system value must still be measured.

C3is an open systems hypothesis,not an established contribution. Current
actualGPUbatchesmostlycontain2-3sources,eightnativequeuesboundavailability,
and the strengthenedCPUHiGHS competitor removes much numericalsearchtime.
The first specific uncertainty is whether sufficient request supply can
change that resultatfixedCPU/memory. The rootadmits one matched32queue
capacity preflight,not a thread/precisiongrid or another narrowkernel.
It uses originalfirst64sources,maxsame32tasks,CPU8-11,48GiB and strongnative/
CPUtwo-sided/GPUtwo-sided paths. Mainfull1000on0-3andprefix20-23preserved.
The version/capacitychange is test-local,not retainedserviceconfiguration.

Positive:admit fresh full1000atthiscapacity beforeclaimingGPUgain.
Negative:boundthisimplementation/capacity;do not infer universalGPUimpossibility.
Mixed/invalid:retain all resourcefailures/nativechanges and resolve thatactual
protocolfault;do not silentlyfilterhardLPs. RQ1-3and SMT/servicepromise remain.

## Baseline handoff

- Original compatible Farkas/nativeprepared execution remains a numerical
mainbaseline;existingproof-free preprocessing cannotbe counted as ours.
- CPUHiGHSsuccess-only and exacttwo-sidedCPUreplace weak numerical
competitors;they answer whetherGPUaddsvalue beyond currentCPUpractice.
- BLPGis citation-only until officialsource isrecoverable and compatible.
Do notaddsequentialGLPK/CPLEXrows solelytoinflate baselinecount.
- VerifiedLPcheckersare citation-onlysame-mechanism precedents,not numerical
Leanverification baselines. WholeRQs still require nativewarm/snapshot/SHRED
competitors already recorded in the project's prior-art map.
- Reuse ICPE's batch-supply/whole-application distinction and exact per-LP
shape reporting. Do notborrow its headline speedup or syntheticduplicatework
as Leanresults. Native/CPU/GPUmustreceiveidenticalcandidatecapacity.

Canonicalupdate contains onlythisroot's appended nonoverlapping section;
earlierother-authoruncommitted material ispreserved. Detailed search/history
stayhere;no separatebibliographydatabase or per-paper notes are created.
No independent audit,fullWRITEcycle,finalRQclosure orOSDIacceptanceclaimed.
