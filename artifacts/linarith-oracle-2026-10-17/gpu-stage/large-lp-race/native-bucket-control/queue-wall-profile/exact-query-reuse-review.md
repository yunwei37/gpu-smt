# Exact numerical reuse is a stronger-baseline question,not a cache speedup

Self-review of the existing complete691.20/545.05second own-clock diagnostic.
The analyzer preserves numerical kind,coefficient order,strictness and all
input fields except source/call_id metadata. It performs no permutation,
subsumption,proof-state canonicalization or changes to observed solver work.

Native:13230requests,9080unique exactpayloads,4150already-completed historical
hits. Repeated-sourcegroups include5706requests in2410cross-sourcegroups.
Observed LPsearchCPU on historicalhits is132.870s of859.532s. Oracle:
10251requests,7662unique,2589historicalhits,75.227s LPsearchCPU of546.832s.
Every exactkey has identical non-timing answers;750oracle groups differ only
in the three numeric timing counters. This is not nondeterministic proof output.

These are exact observed request identities,not percentages of removable
end-to-endwall. A real cache would owe keying,lookup,resource accounting,
witness validation,queue changes and complete native behavior checks. These
observations cannot substitute for a measured cachecontrol or imply1.5x.

For the user-requested novelty comparison beyond existing services/caches,
ordinary exact-query reuse remains a credible CPUalternative. It also lowers
the supply of distinctLPs forGPU,and repeatedrequests must not be multiplied
to manufacturebatchsize. Do not call this characterization a newcache mechanism.
Do not mutate the active frozen full1000capture to enable caching midrun.
The current numerical cachecontrol is unmeasured and remains a ranked
baseline objection,not an invented completed result.
