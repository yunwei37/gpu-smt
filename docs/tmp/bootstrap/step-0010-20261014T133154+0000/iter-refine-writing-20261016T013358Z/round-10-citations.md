# Round10 — citations

Started 2026-10-16T01:52:26.183300+00:00; parent
Step0010BOOTSTRAPWRITE; entry Round9output. Root reads the complete current
paper, bibliography and check-paper-citations skill. This is a full citation
run because some recently added references lack the complete five-field
annotation block, not a pass3-only shortcut. No fake Skill-tool invocation or
independent reviewer isclaimed.

The required unmodified workspace verify_bib.py runs first on all entries.
Actual stdout/stderr and returncode stay in this round. A URL's200response
proves existence only; primary-source metadata and claim context still need
manual inspection. Existing completed verification can be reused for unchanged
older entries; partial/new annotations cannot simply be labeled verified
without the required script passing for those entries.

Missing/incomplete entry annotation fields at entry: [('minif2f', ['VERIFIED', 'REAL', 'PDF', 'ABSTRACT', 'USED_FOR']), ('farkasSource', ['VERIFIED', 'PDF', 'ABSTRACT']), ('highsSimplex', ['VERIFIED', 'PDF', 'ABSTRACT']), ('getrusage', ['VERIFIED', 'PDF', 'ABSTRACT']), ('perfReport', ['VERIFIED', 'PDF', 'ABSTRACT']), ('lean427MetaDefEq', ['VERIFIED', 'PDF', 'ABSTRACT'])].
Manual evidence/checks, any errors/fixes and final actual result follow.

## Actual entry-check errors and source repair

The unmodified initialchecker returns1 with fourerrors. It compares miniF2F's
publishedICLR2022year to firstpreprint2021 when titleAPIs areunavailable.
Keep the correct2022year and reference the official publishedOpenReviewPDF.
The actual downloaded arXivv2PDF itself carries Published-at-ICLR2022,
matching allthreeauthors/title. Ordinary OpenReviewPDFdownload returns403 and
the forumshowsbrowserverification; that failure staysrecorded, no bypass.
This optionaldownload doesnotjustify changing the real publicationdate.

Three misc source/manual entries gain2026explicitly as accessyear, not an
invented publicationdate, matching existing bibliography convention. The
separately reviewed patches remain in round-10-bibliography-reviewed-edit.diff.
No performancevalue or scientificclaim changes. The corrected standardchecker
is nowrun on all37entries without modifying its logic.

## Stable published-record fallback

DBLP's actual published record conf/iclr/ZhengHP22 identifies the same three
authors, title and ICLR2022 venue. The primary OpenReview page was also visibly
retrieved in the ordinary browser after its initial verification page loaded;
it shows Published28January2022 and ICLR2022Poster. No CAPTCHA/login action,
cookie/header manipulation or bypass occurred. The earlier urllib403 remains.
The bibliography URL now points to the real stable DBLP published record;
the paper's downloaded author-v2PDF and primary publication observation are
retained. Ordinary urllib returns202 for the DBLP page, so that response alone
does not verify metadata; actual indexed publication metadata plus primary
OpenReview/PDF supply that manual check. Correct2022year is unchanged.
The unmodified standardchecker now reruns because this URL actually changed.

## Pass3 missing first-use provenance

The first retained ProofNet-lineage task mention needs its existing origin/
Lean4-port citations. First Goedel model mention gains the existing official
project workflow provenance. SGLang/vLLM first mentions name borrowed inference
software; their official repositories/README are directly retrievedHTTP200 and
read. Two source-artifact references are added for framework identity only.
Accessyear2026 is explicit, not a publication claim. No external accuracy/
speedup is imported. Native stream counts/source numbers remain read-only.

## Manual passes and disposition

Pass1: the unmodified39entry checker returns0, zeroerrors/zerowarnings.
Thirty-one unchanged older entries retain their existing complete manual
annotations. Eight new/partial entries now have full annotations after actual
checker success plus primary/source inspection. All39entries have the five
fields; no invented or hallucinated source is found. This is not a claim that
every API compared metadata: many used URLfallback and manual provenance.
The DBLP202 caveat remains beside direct primarypublication/PDF evidence.

The miniF2F author-v2PDF and HiGHS publisherPDF were downloaded and their full
abstracts/introductions read. miniF2F correctly cites publishedICLR2022 rather
than firstpreprint2021. HiGHS correctly cites the2018issue, with online2017
distinguished. Source/manual entries assert accessyear, not publicationdate.
FarkasREADME describes exact/native and numeric-support/stock-proof paths.
The actual pinned Lean MetaM declaration and export identify Meta equality;
neither the source nor perf manual supports a pure-kernel or GPUfraction.

Pass2: root reads all current citation contexts in the complete manuscript.
Lean/REPL/snapshot/service sources support their specific stage/reuse interfaces;
Linuxfork/PSS/affinity/resource manuals support the stated process/accounting
scope; Verus/VeruSAGE/Mathlib/Arena/ProofNet/Goedel sources identify their
distinct workloads; Farkas/HiGHS/checker sources identify competitors rather
than supplying our timing values; caching/serverless papers support prior
mechanisms. No cited external result is substituted for our native captures.
No inaccurate scientific claim requires rewriting in this round.

Pass2.5: published/preprint and workshop/main-conference boundaries are checked
against the retained annotations and new primarymetadata. Existing Kimina/
AXLE workshop scopes remain. Original artifact sources are cited directly
rather than using a secondary performance comparison as our evidence.
No identity-revealing selfcitation wording or unexplained citation chain is
found in the read manuscript. Finite primary-domain notice searches for
miniF2F/HiGHS and named recent Lean/serverless works return no notices;
this is a bounded notice search, not proof that none can exist.

Pass3: four first-use sites gain provenance: Goedel model/project, original
ProofNet plus its Lean4port, SGLang and vLLM. Five source-key occurrences are
added; all preexisting cited-key occurrences remain. Two new artifact entries
identify the frameworks only, with no borrowed accuracy or speed claim.
All quantitative manuscript values and fourRQmeanings are unchanged.
Own measured tables/claims point to our evaluation, not external bibliography.
No unrelated missing-citation expansion or literature-scope rewrite ismade.

Root personally reviews/fixes under the human no-delegation instruction;
no independent reviewer or Skill-tool call is fabricated. The standardchecker
was not changed. Existing API/403/patch failures remain in the round logs.
Remaining parent work is Round11 cumulative entry-baseline preservation and
paper rendering. This local citation result does not close any researchRQ.

Completed 2026-10-16T02:13:43.572625+00:00. Actual Tectonic evidence: {"returncode": 0, "pages": "Pages:           14", "pdf_bytes": 178083}. No error/overfull/undefined diagnostic; inherited underfull warnings remain. Main source citations and bibliography changes are in the reviewed diffs. Next: Round11 restoration-only cumulative audit.
