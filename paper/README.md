# Paper draft

The current draft is:

- `paper/main.tex`
- `paper/refs.bib`

Working title:

> **VeriServe: SLO-Aware Verification Serving with Cross-Job State Reuse**

The draft is intentionally written as a systems paper rather than a GPU-SMT paper. GPU execution is an optional heterogeneous backend; the main claim is cross-job solver-state reuse plus SLO-aware scheduling around unmodified backends.

## Build

A standard TeX installation is sufficient:

```bash
cd paper
latexmk -pdf main.tex
```

or:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The current LaTeX source has been syntax-checked with `pdflatex -halt-on-error`.

## Current paper status

Already drafted:

- abstract and problem statement;
- design constraints;
- context graph and state hierarchy;
- fork/COW snapshots;
- SLO-aware scheduler;
- optional GPU path;
- preliminary synthetic and public SMT-LIB experiments;
- evaluation plan;
- related work;
- limitations/falsification criteria.

Still missing before submission-quality:

- large real workload characterization (especially VeruSAGE-Bench);
- end-to-end VeriServe daemon/runtime implementation;
- scheduler evaluation under controlled offered load and deadlines;
- comparison against warm process pools, result caches, existing frontend caches, and Mallob where experimentally meaningful;
- GPU results only if a real workload class justifies them;
- polished figures and artifact instructions.

## Submission target

The current framing is intended to be strong enough to evaluate against an OSDI-style bar, but the draft does **not** assume OSDI acceptance. The decisive evidence will be the real-workload study and whether the final runtime moves both p99 latency and throughput/cost frontiers on real verification applications.
