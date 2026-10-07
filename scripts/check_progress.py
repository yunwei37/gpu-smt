#!/usr/bin/env python3
"""Diagnostic progress reporter for auto-research-orchestrator projects.

Reports discrete progress facts from a research repository and warns on
stagnation signals. Output is a diagnostic aid ONLY:

- it never gates, blocks, or authorizes a research transition;
- it is not a control plane and must not grow machine-readable verdicts;
- thresholds are parameters here, not rules in the skill.

Intended consumers:
  1. the REVIEW gate's meta-review (waste and drift questions);
  2. an external scheduler that runs this script on a timer and wakes a
     full session (through the resume protocol) only when the exit code
     is non-zero.

Exit codes: 0 = no warnings, 1 = at least one warning.
All content checks are heuristic; the authoritative state is always the
Markdown reports themselves.
"""

import argparse
import re
import sys
import time
from pathlib import Path

HOUR = 3600.0


def newest_mtime(path: Path) -> float:
    """Newest mtime of path itself or any file under it; 0.0 if absent."""
    if not path.exists():
        return 0.0
    if path.is_file():
        return path.stat().st_mtime
    best = 0.0
    for p in path.rglob("*"):
        if p.is_file():
            best = max(best, p.stat().st_mtime)
    return best


def age_hours(mtime: float, now: float) -> float:
    return (now - mtime) / HOUR if mtime else float("inf")


def fmt_age(mtime: float, now: float) -> str:
    if not mtime:
        return "missing"
    h = age_hours(mtime, now)
    return f"{h / 24:.1f}d ago" if h >= 48 else f"{h:.1f}h ago"


def step_dirs(repo: Path):
    tmp = repo / "docs" / "tmp"
    if not tmp.is_dir():
        return []
    phases = ("bootstrap", "build-and-evaluate", "writing")
    return [
        step
        for phase in phases
        for step in sorted((tmp / phase).glob("step-*"))
        if step.is_dir()
    ]


def count_rq_facts(evaluation: Path):
    """Heuristic RQ facts from docs/evaluation.md: (rq_ids, unanswered_count)."""
    if not evaluation.is_file():
        return set(), 0
    text = evaluation.read_text(errors="replace")
    rq_ids = set(re.findall(r"\bRQ\d+\b", text))
    unanswered = len(re.findall(r"\bunanswered\b|\bunresolved\b|\bTODO\b", text, re.I))
    return rq_ids, unanswered


def _name_marker(step: Path, *tokens: str) -> bool:
    """True when any token appears in a file or directory name under the step.
    Covers both the current flat layout and the legacy per-gate layout."""
    tokens = tuple(t.lower() for t in tokens)
    return any(
        any(t in p.name.lower() for t in tokens) for p in step.rglob("*")
    )


def consecutive_bootstrap_idea_skips(steps) -> int:
    """Consecutive BOOTSTRAP steps whose REVIEW gate skipped idea changes.
    The skip marker is a file name in the legacy layout and a step-report
    line in the flat layout."""
    n = 0
    bootstrap_steps = [s for s in steps if s.parent.name == "bootstrap"]
    for step in reversed(bootstrap_steps):
        found = _name_marker(step, "idea-unchanged", "idea_unchanged")
        report = step / "step-report.md"
        if not found and report.is_file():
            text = report.read_text(errors="replace").lower()
            found = "idea-unchanged" in text or "idea unchanged" in text
        if found:
            n += 1
        else:
            break
    return n


def forbidden_full_writes(steps) -> int:
    """Count post-BOOTSTRAP steps whose file tree contains a full writing run
    (an iter-refine-writing round directory; name match only, so prose
    mentions in step-report.md cannot false-positive)."""
    return sum(
        1
        for step in steps
        if step.parent.name != "bootstrap"
        and _name_marker(step, "iter-refine-writing")
    )


def open_author_questions(qfile: Path) -> int:
    """Heuristic count of '## ' entries without a resolved marker."""
    if not qfile.is_file():
        return 0
    open_count = 0
    for section in re.split(r"^## ", qfile.read_text(errors="replace"), flags=re.M)[1:]:
        if not re.search(r"\bresolved\b|\banswered\b", section, re.I):
            open_count += 1
    return open_count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=".", help="research repository root")
    ap.add_argument("--max-idle-hours", type=float, default=24.0,
                    help="warn when the newest report is older than this")
    ap.add_argument("--stale-steps", type=int, default=3,
                    help="warn after this many steps without new evidence")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    now = time.time()
    warnings = []

    steps = step_dirs(repo)
    reports_mtime = newest_mtime(repo / "docs" / "tmp")
    eval_path = repo / "docs" / "evaluation.md"
    eval_mtime = newest_mtime(eval_path)
    idea_mtime = newest_mtime(repo / "docs" / "idea-story.md")
    paper_mtime = newest_mtime(repo / "docs" / "paper")
    qfile = repo / "docs" / "questions-for-author.md"

    rq_ids, unanswered = count_rq_facts(eval_path)
    idea_skips = consecutive_bootstrap_idea_skips(steps)
    full_write_violations = forbidden_full_writes(steps)
    open_qs = open_author_questions(qfile)
    steps_since_evidence = sum(1 for d in steps if d.stat().st_mtime > eval_mtime)

    print(f"repo:                    {repo}")
    print(f"steps:                   {len(steps)}"
          + (f" (latest: {steps[-1].parent.name}/{steps[-1].name})" if steps else ""))
    print(f"newest report:           {fmt_age(reports_mtime, now)}")
    print(f"evaluation.md changed:   {fmt_age(eval_mtime, now)}")
    print(f"idea-story.md changed:   {fmt_age(idea_mtime, now)}")
    print(f"paper changed:           {fmt_age(paper_mtime, now)}")
    print(f"RQ ids seen / open TODO: {len(rq_ids)} / {unanswered}  (heuristic)")
    print(f"BOOTSTRAP idea skips:    {idea_skips}")
    print(f"forbidden full writes:   {full_write_violations}")
    print(f"open author questions:   {open_qs}")

    if steps and age_hours(reports_mtime, now) > args.max_idle_hours:
        warnings.append(f"no new report for {age_hours(reports_mtime, now):.0f}h "
                        f"(limit {args.max_idle_hours:.0f}h): session may be dead; resume")
    if steps and steps_since_evidence >= args.stale_steps:
        warnings.append(f"{steps_since_evidence} step dirs created since evaluation.md "
                        f"last changed: steps may be spinning without new evidence")
    if idea_skips >= args.stale_steps:
        warnings.append(f"{idea_skips} consecutive BOOTSTRAP idea-unchanged skips: "
                        "check whether BOOTSTRAP is ready to freeze")
    if full_write_violations:
        warnings.append(f"{full_write_violations} post-BOOTSTRAP steps ran full writing: "
                        "phase writing permissions were violated")
    if qfile.is_file() and steps and qfile.stat().st_mtime > reports_mtime:
        warnings.append("questions-for-author.md changed after the newest report: "
                        "possible new author answer; wake a session to ingest it")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  - {w}")
        return 1
    print("\nOK: no stagnation signals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
