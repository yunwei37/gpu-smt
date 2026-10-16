# Round6 — sentence mechanics

Started 2026-10-16T01:43:36.350145+00:00; parent
Step0010BOOTSTRAPWRITE; entry Round5output. Root reads complete paper/style
skill and reviews every narrative sentence, applying explicit reviewed local
patches serially within each subsection. No independent reviewer.

## Findings and application

Should-fix: independent-clause semicolons and unlabeled colon transitions make
methodology/evidence paragraphs read as compact notes. Split those clauses or
use a direct conjunction. Two weak/vague subjects are replaced by their actual
antecedents (shared-process alternative and observed coverage percentage).
All scope-bearing negatives/hedges remain. TikZsyntax/diagramlabels, numbered
designgoals, macros and quantitative ranges are not narrative punctuation and
are left unchanged. No blanket regex/source rewrite is performed.

The exact local edits below are individually reviewed and applied as separate
standard patch operations; subsection order is Setup -> RQ1 -> RQ3 -> RQ4.

1. Experimental setup. Before: '244 miniF2F test tasks~\\cite{minif2f} and 186 ProofNet-lineage test tasks: 13,760 candidates.'
   After: '244 miniF2F test tasks~\\cite{minif2f} and 186 ProofNet-lineage test tasks, for a total of 13,760 candidates.'

2. Experimental setup. Before: 'The adapted SGLang generator executes one request at a time; official\nGoedel inference instead batches model inputs'
   After: 'The adapted SGLang generator executes one request at a time. Official\nGoedel inference instead batches model inputs'

3. Experimental setup. Before: 'before service startup and use four outstanding HTTP requests; they are not\nexact reproductions'
   After: 'before service startup and use four outstanding HTTP requests. They are not\nexact reproductions'

4. Experimental setup. Before: 'The operational group contains 41 timeouts and 14 decoder failures; an\nindividual native allocation-failure replay'
   After: 'The operational group contains 41 timeouts and 14 decoder failures. An\nindividual native allocation-failure replay'

5. Experimental setup. Before: 'outcome population; both axes are logarithmic.'
   After: 'outcome population. Both axes are logarithmic.'

6. Preparation sharing. Before: 'service executes 67 import headers and selects 29,683 started-REPL reuses;\nthe compiled route'
   After: 'service executes 67 import headers and selects 29,683 started-REPL reuses.\nThe compiled route'

7. Preparation sharing. Before: 'already reuses preparation; they do not measure its CPU or latency share.'
   After: 'already reuses preparation. They do not measure its CPU or latency share.'

8. Preparation sharing. Before: '\\texttt{LibrarySearch} query for \\texttt{True}; their initialization intervals'
   After: '\\texttt{LibrarySearch} query for \\texttt{True}. Their initialization intervals'

9. Latency throughput memory. Before: 'therefore characterize this modified preparation protocol; they do not measure'
   After: 'therefore characterize this modified preparation protocol. They do not measure'

10. Latency throughput memory. Before: 'each method and scheduled rate; lines join their arithmetic means, not pooled'
   After: 'each method and scheduled rate. Lines join their arithmetic means, not pooled'

11. Latency throughput memory. Before: 'within the measured implementation; they do not isolate process-cloning cost'
   After: 'within the measured implementation. They do not isolate process-cloning cost'

12. Latency throughput memory. Before: 'Stock whole times are 1,561.1, 1,618.0 and 1,889.7 seconds; branch times are'
   After: 'Stock whole times are 1,561.1, 1,618.0 and 1,889.7 seconds. Branch times are'

13. Latency throughput memory. Before: '\\texttt{getrusage} child totals. Those totals depend on completed waits~\\cite{getrusage};\nexhaustive descendant coverage'
   After: '\\texttt{getrusage} child totals. Those totals depend on completed waits~\\cite{getrusage}.\nExhaustive descendant coverage'

14. Latency throughput memory. Before: 'bounds; they show no stock-relative memory saving'
   After: 'bounds. They show no stock-relative memory saving'

15. Latency throughput memory. Before: 'measured time loss. The complete service frontier remains unfinished;\nthis result rejects'
   After: 'measured time loss. The complete service frontier remains unfinished.\nThis result rejects'

16. Latency throughput memory. Before: 'shared-process placement on the measured cohort. It is 22.64\\%, 18.72\\%'
   After: 'shared-process placement on the measured cohort. The shared-process alternative is 22.64\\%, 18.72\\%'

17. Latency throughput memory. Before: 'ends the shared process; the complete method checks every unreturned original'
   After: 'ends the shared process. The complete method checks every unreturned original'

18. Latency throughput memory. Before: 'in two pairs; one source in the other pair has internal metavariable-number'
   After: 'in two pairs. One source in the other pair has internal metavariable-number'

19. Heterogeneous execution. Before: 'Runtime import and library loading are charged; software build is excluded.'
   After: 'Runtime import and library loading are charged. Software build is excluded.'

20. Heterogeneous execution. Before: 'Native fields match on 29,725 sources after excluding the adapter timer;\n16 operational outcomes'
   After: 'Native fields match on 29,725 sources after excluding the adapter timer.\n16 operational outcomes'

21. Heterogeneous execution. Before: 'This observation strengthens an established CPU baseline; it does not establish'
   After: 'This observation strengthens an established CPU baseline. It does not establish'

22. Heterogeneous execution. Before: 'and 12,539.74 versus 11,192.98 seconds: 7.61\\% and 10.74\\% less whole elapsed.'
   After: 'and 12,539.74 versus 11,192.98 seconds, reductions of 7.61\\% and 10.74\\% in whole elapsed time.'

23. Heterogeneous execution. Before: 'native diagnostic differences; remaining payloads match except the adapter'
   After: 'native diagnostic differences. Remaining payloads match except the adapter'

24. Heterogeneous execution. Before: 'Closed-loop request p99 also falls in each pair: 10.56 to 10.09, 12.16 to'
   After: 'Closed-loop request p99 also falls in each pair, from 10.56 to 10.09, 12.16 to'

25. Heterogeneous execution. Before: 'matching native payloads; no complete/rejected transition occurs.'
   After: 'matching native payloads. No complete/rejected transition occurs.'

26. Heterogeneous execution. Before: 'with reuse: 0.59\\% longer, then 5.11\\% lower. Their signs differ.'
   After: 'with reuse, corresponding to 0.59\\% longer, then 5.11\\% lower. Their signs differ.'

27. Heterogeneous execution. Before: 'its matched block; they do not establish the globally strongest CPU method,'
   After: 'its matched block. They do not establish the globally strongest CPU method,'

28. Heterogeneous execution. Before: '10,531.82, 13,112.67 and 15,097.58 seconds; candidate times are'
   After: '10,531.82, 13,112.67 and 15,097.58 seconds. Candidate times are'

29. Heterogeneous execution. Before: 'stable general advantage: pair signs differ and the same-code references drift.'
   After: 'stable general advantage. Pair signs differ and the same-code references drift.'

30. Heterogeneous execution. Before: 'replicated peaks; this pair shows no measured memory saving.'
   After: 'replicated peaks. This pair shows no measured memory saving.'

31. Heterogeneous execution. Before: 'These complete comparisons preserve a competent CPU competitor; they do not'
   After: 'These complete comparisons preserve a competent CPU competitor. They do not'

32. Heterogeneous execution. Before: 'installed Lean4.27 source~\\cite{lean427MetaDefEq}; it is not a pure C++ kernel'
   After: 'installed Lean4.27 source~\\cite{lean427MetaDefEq}. It is not a pure C++ kernel'

33. Heterogeneous execution. Before: '20.05\\% of native exclusive recorded period; that pair is not an exhaustive'
   After: '20.05\\% of native exclusive recorded period. That pair is not an exhaustive'

34. Heterogeneous execution. Before: 'This capture characterizes the compiled original arithmetic route; residual'
   After: 'This capture characterizes the compiled original arithmetic route. Residual'

35. Heterogeneous execution. Before: 'exclusive cores; GPU time slicing shares the device with another Workspace.'
   After: 'exclusive cores. GPU time slicing shares the device with another Workspace.'

36. Heterogeneous execution. Before: 'This is coverage by call count, not the fraction of verification time that'
   After: 'The percentage measures coverage by call count, not the fraction of verification time that'

37. Heterogeneous execution. Before: 'across workers; subtracting them from whole-corpus makespan would not'
   After: 'across workers. Subtracting them from whole-corpus makespan would not'

38. Heterogeneous execution. Before: 'They do not establish whether GPU sharing caused the slowdown; no matched'
   After: 'They do not establish whether GPU sharing caused the slowdown. No matched'

39. Heterogeneous execution. Before: '5,161,250 and 6,315,211 KiB. These are single instrumented conditions:\none-second non-atomic sampling'
   After: '5,161,250 and 6,315,211 KiB. These are single instrumented conditions.\nOne-second non-atomic sampling'

40. Heterogeneous execution. Before: 'replace the primary comparisons or establish replicated memory uncertainty;\nGPU context/driver'
   After: 'replace the primary comparisons or establish replicated memory uncertainty.\nGPU context/driver'

## Verification and disposition

Completed 2026-10-16T01:43:39.445379+00:00.
40targeted edits; exact reviewed patches in round-6-reviewed-edit.diff.
Each preserves quantitative/citation-occurrence multisets and all technical
clauses/qualifiers. No RQ, source input, data, statistic or native process
changes. Actualcompile {'returncode': 0, 'pages': 'Pages:           14', 'pdf_bytes': 177208}, no error/overfull/undefined. Existingunderfull
warnings are retained. No Mustfix remains in the checked sentence mechanics.

Consider: force every technical sentence below seven subject-to-verb words.
Reject literal enforcement where it would sever a required technical qualifier;
keep explicit actors and split actual ambiguities, not arbitrary wordcount.
Consider: shorten resultlimitations. Reject removal of scope-bearing caveats.
Three impactful categories are clause separation, explicit metric subjects
and clearer result transitions. Next Round7 wordchoice.
