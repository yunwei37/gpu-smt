# Round6: language-sentence

Started 2026-10-07T22:18:42.242Z; reviewer returned 2026-10-07T22:19:18.242Z; root completed 2026-10-07T22:19:54.146979+00:00. Parent step0001 WRITE_GATE. Source diff baseline c027495eacbba4461a64fd70099d2880c55ad6e1; original entry tree remains0cf6486e5a40cc0d7740462ddfb69d2e945144a5. Fresh read-only reviewer gpt-6.1-sol loaded full paper/bib and requested full skill sources through filesystem adaptation (no Skill tool). No reviewer edits/Git/build. Evidence/source journal rollout-2026-10-07T22-18-42-01a11872-8abf-78b3-9fe4-4eeb679fe88b.jsonl.

## Root dispositions and verification

All seven Should-fix applied: six independent semicolons split into sentences, cancellation ownership/termination/release connected. Consider abstract long subject rejected: splitting adds tenth sentence and breaks role correspondence; current grammatical subject acceptable. Consider complete-cost subject applied in Design, RQ2/RQ3 goal mappings combined while exact four RQs retained. No Must-fix, quantitative changes or content loss. Nine local sentence constructions changed, including merged cancellation and mapping pairs.

Root reviewed subsection-sized apply_patch edits and source diff. make -C docs/paper exits0. Pages:           7; citation commands 27, never decreased; four RQs match entry tree verbatim; no quantitative value invented or changed. Scope conditions and negative/mixed-result permission protected. Paper SHA256 a6f69bfa4ee7978e1c05cddc550698d2b690eb9b3ffd334969e9dd231b3674b1. Intended incomplete submission, not final venue compliance or answered RQs. Next serial round after this full compile/check.

## Verbatim independent reviewer return

Read the full `main.tex`, `references.bib`, and both requested skills through the filesystem. Read-only review; no edits, Git operations, or builds.

**Must-fix**

None. No dangling modifiers, accidental narrative fragments, weak “It is / There are” openings, or unlabeled narrative colons were found. Missing-results placeholders and contribution-list fragments are intentional. The numbered design-goal colon is permitted.

**Should-fix**

1. **Introduction, L36 — independent clauses joined by a semicolon.**  
   Quote: “Supported quiescent boundaries, untouched candidate suffixes and bounded prepared-state lifetimes address runtime compatibility and memory use; unsupported boundaries use native execution.”  
   Fix: “Supported quiescent boundaries, untouched candidate suffixes and bounded prepared-state lifetimes address runtime compatibility and memory use. Unsupported boundaries use native execution.”

2. **Background / Verification stages and outcomes, L48 — independent-clause semicolon.**  
   Quote: “Kernel checking validates proof terms against the dependent type theory; post-export checker replay begins after the source frontend has already run.”  
   Fix: “Kernel checking validates proof terms against the dependent type theory. Post-export checker replay begins after the source frontend has already run.”

3. **Design / Architecture overview, L96 — independent-clause semicolon.**  
   Quote: “A supported branch executes on CPU, with supported device operations where available; an unsupported boundary uses native execution.”  
   Fix: “A supported branch executes on CPU, with supported device operations where available. An unsupported boundary uses native execution.”

4. **Evaluation / Experimental setup, L156 — independent-clause semicolon.**  
   Quote: “Published proofs and deliberate invalid or incomplete variants are controls for behavior; they do not supply generated-traffic locality.”  
   Fix: “Published proofs and deliberate invalid or incomplete variants are controls for behavior. They do not supply generated-traffic locality.”  
   Preserve the limitation.

5. **Evaluation / Experimental setup, L160 — independent-clause semicolon.**  
   Quote: “Affinity specifies permitted CPUs and is recorded with topology and competing-work observations; affinity alone is not CPU isolation.”  
   Fix: “Affinity specifies permitted CPUs and is recorded with topology and competing-work observations. Affinity alone is not CPU isolation.”  
   Preserve the qualification.

6. **Evaluation / Heterogeneous execution, L177 — independent-clause semicolon.**  
   Quote: “We identify whether each complete measurement begins with source verification or post-export checking; post-export results answer only the latter boundary.”  
   Fix: “We identify whether each complete measurement begins with source verification or post-export checking. Post-export results answer only the latter boundary.”  
   Preserve “only.”

7. **Design / Branch lifetime and cancellation, L111 — four short declaratives read as notes.**  
   Quote: “Candidate mutation should not extend … Each branch owns … Cancellation stops … The prepared parent remains …”  
   Local fix: retain the opening requirement, then connect branch ownership to termination: “Each branch owns mutable candidate state and terminates after producing its response, while cancellation stops that branch and releases its private memory. The prepared parent remains available only while it passes the configured retention policy.”  
   This preserves ownership, cancellation, release, and retention conditions.

**Consider**

8. **Abstract, L15 — long coordinated subject delays the verb.**  
   Quote: “Established result caches, persistent environments, proof-state snapshots and bounded warm services recover substantial reuse, requiring a matched equal-resource comparison after their existing savings.”  
   Fix: “Established reuse mechanisms recover substantial reuse through result caches, persistent environments, proof-state snapshots and bounded warm services. A matched equal-resource comparison must account for these existing savings.”  
   The original is grammatical; this makes the comparison obligation easier to parse without removing mechanisms.

9. **Design / Heterogeneous checking, L127 — long list precedes a passive verb and leaves accounting implicit.**  
   Quote: “Device initialization, representation construction, upload, download and queueing are included.”  
   Fix: “Complete verification includes device initialization, representation construction, upload, download and queueing.”  
   This supplies the measurement subject already established in the preceding paragraph.

10. **Evaluation overview, L148 — repetitive short RQ mappings.**  
    Quote: “RQ1 tests … RQ2 tests … RQ3 tests … RQ4 tests …”  
    Local fix: combine only the adjacent RQ2/RQ3 mappings: “RQ2 tests behavior preservation and isolation, the first two design goals, while RQ3 tests the third goal, the equal-resource service frontier.”  
    Keep the four numbered RQs verbatim. Explicit mapping is useful, so retaining the existing version is also defensible.

**Counts:** 0 Must-fix, 7 Should-fix, 3 Consider. The highest-value changes are the six semicolon replacements, connecting the cancellation paragraph, and clarifying the complete-verification accounting sentence. No claim, RQ, quantitative value, protected hedge, result placeholder, or limitation needs alteration for this round.
