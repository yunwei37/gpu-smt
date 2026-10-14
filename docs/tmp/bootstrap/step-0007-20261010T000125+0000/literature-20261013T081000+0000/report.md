# Bounded worker replacement: primary-source and baseline handoff

2026-10-13, BOOTSTRAP step0007 EXPERIMENT, parent E94. Full human instruction log, Initial Narrative and current paper were read. This finite follow-up concerns RQ3, not a replacement of the Lean-first/full-verification/SMT/device research objective.

## Questions and declared boundary

The name-free claim is that retaining native preparation across worker replacement can change complete verification cost beyond an already competent warm full-snapshot pool. The questions are whether a published service actually exposes finite worker lifetimes, whether unlimited reuse is already the default, and which comparison distinguishes preparation retention from imposing an artificial weakness on the baseline. Coverage ends after official settings, manager and worker code resolve policy/measurement/fairness, and existing accepted systems precedents resolve mechanism overlap. No new broad novelty survey or unchanged citation campaign is needed.

## Search and verification

Queries on 2026-10-13: `site:github.com/project-numina/kimina-lean-server max_requests max_repl_uses repl_config` and `site:github.com/project-numina/kimina-lean-server max_repl_mem max_repl_times`. Opened official README, settings and source tree. The web source-tree API failed; public GitHub API/raw downloads supplied complete source files, pinned to fb2393de3461db35eda4c714e3fd21187e92ec90. Local links: [commit](primary-commit.json), [settings](source-server-settings.py), [manager](source-server-manager.py), [worker](source-server-repl.py), [README](source-README.md). Official pinned [settings](https://github.com/project-numina/kimina-lean-server/blob/fb2393de3461db35eda4c714e3fd21187e92ec90/server/settings.py) was independently opened again. Search hits on idle-server failures and Lean4.9 timeout fixes were leads only: no diagnosis of our slow workers or evidence of general instability follows.

Verified source findings:

- `max_repl_uses=-1` is unlimited by default. Worker exhaustion explicitly handles negative limits; headers are excluded from body use count. Finite retirement is a supported configuration, not a default frequency or demonstrated production frequency.
- Actual settings have memory default12GiB, while README says8G. Source version and documentation disagree; neither is silently transplanted into our version-aligned native experiment.
- Worker execution requests `gc=true` after the header, and the manager reuses header-indexed workers. This is an established competent competitor, not an accumulating naive session.
- Source applies RLIMIT_AS and records process-tree memory/CPU. Our existing default-native capture does not reproduce that memory limit, network admission or manager. The comparison must be described as a matched native lifecycle mechanism study, not official Kimina performance reproduction.

For same-mechanism/venue coverage, reused the complete retained graph/persistence/zygote audit [20261012 report](../literature-20261012T205800+0000/report.md) and independently opened the official [SOCK ATC2018 proceedings page](https://www.usenix.org/conference/atc18/presentation/oakes). Its paper already evaluates shared prepared process trees, end-to-end provisioning, throughput and memory. Bare fork/COW, preparation caches and retirement therefore have high same-mechanism risk. Native logical snapshots and modern stock disk snapshots remain strong comparison families. This source question does not reduce that novelty risk.

## Contradiction review and coverage conclusion

The source contradicts the proposed shortcut of calling a small fixed use count the service default. Root drops that premise. Unlimited reuse must remain a strong numerical control alongside explicitly configured finite policies. No observed deployment distribution justifies claiming the chosen frequencies are representative. The claim question is narrower than the paper: does retaining preparation help when actual policy requires replacement, and what is its price when replacement is absent? Both outcomes can change the implementation decision without changing RQ3 or declaring a new contribution.

All declared policy, mechanism, fairness and metric branches are resolved sufficiently to plan this discriminator. Remaining uncertainties are actual replacement cost, private memory growth, complete native outcomes, resource competition and formal-corpus sensitivity. These require matched complete execution, not more source inspection. Bounded placement, cancellation, online arrivals and SMT remain wider unresolved paper obligations.

## Experiment handoff

Use one strongest main baseline: the same-version, same-binary optimized full-snapshot warm pool, receiving the same persistence/import/index optimization and native default runtime. The competing position is that existing reuse is sufficient even when workers are replaced. A matched numerical run is needed because neither the publication nor our E016 unlimited-lifetime runs measure those costs on complete original5952/7808 candidate pools.

Integrate finite128/512 body-use policies and no elective replacement into one matrix, with both methods at the same policy. The finite values correspond to4/16 original32-candidate batches and are configurations, not official defaults. Include all source outcomes, all initialization, EOF/wait/replacement, host CPU and total fleet PSS. Prepare only the first actual public header in the parent; later headers must arrive in candidate workers without lookahead advantage. Strong same-binary native full snapshots are supported in the exact4.9 APIs; modern stock serialization is cited separately, not inferred in that old SDK.

The accepted-paper experimental precedent is SOCK's full provisioning/resource comparison; standard wall latency, whole throughput, CPU and proportional memory are reused, not its reported factors. Actual formal benchmark lineage, fixed Goedel proof candidates and native adapters come from already-qualified E002/E014/E016, not generated fixtures. Configuration/transport differ from official Kimina and must be disclosed. Root chooses the scope and admission; this handoff is evidence, not an instruction or approval.

## Novelty and root disposition

No thesis, RQ, narrative or paper term changed. High same-mechanism risk remains. The larger contribution requires a demonstrated complete behavior/resource/service frontier beyond competent reuse and dynamic complete heterogeneous checking, not retirement or retained metadata alone. Positive conditional data would justify integrating retention into that service; absent or adverse data would reject this mechanism as an acceleration explanation. Neither result answers the full RQ or establishes OSDI novelty. Canonical related-work frontier is updated with this policy correction and handoff.
