#!/usr/bin/env python3
"""Static analysis of explicitly materialized Parquet row groups, never timing."""
import argparse, collections, csv, hashlib, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "openai-math"))
from scan import masks

TACTICS = ("decide", "native_decide", "bv_decide", "simp", "simp_all", "norm_num",
           "omega", "grind", "linarith", "nlinarith", "interval_cases", "aesop",
           "rfl", "exact?")
TOKEN = re.compile(r"(?<![\w'])(" + "|".join(re.escape(x) for x in TACTICS) + r")(?![\w'])")
ERROR = re.compile(r"-- type: error, msg:(.*?)(?=</feedback>)", re.S)
BUDGET = re.compile(r"maximum number of heartbeats|deterministic timeout|maximum recursion depth|out of memory|excessive memory|bad_alloc", re.I)

def error_bucket(message):
    if "MemoryError:" in message or "Memory usage is too high" in message: return "publisher_memory_or_restart_diagnostic"
    if BUDGET.search(message): return "explicit_native_budget_text"
    if "no goals to be solved" in message: return "no_goals"
    if "unsolved goals" in message: return "unsolved_goals"
    if any(x in message for x in ("unknown identifier", "unknown constant", "unknown namespace")): return "unknown_name"
    if any(x in message for x in ("unexpected token", "unexpected identifier", "unexpected end of input", "expected token", "unterminated")): return "parser"
    if any(x in message for x in ("type mismatch", "failed to synthesize", "application type mismatch", "function expected", "typeclass instance problem is stuck", "invalid field notation", "expected type", "has type", "failed to infer", "structure expected", "numerals are data")): return "typing_or_instance"
    if "made no progress" in message: return "rewrite_no_progress"
    if "proved that the proposition" in message: return "tactic_reported_refutation"
    if any(x in message.lower() for x in ("failed", "failure", "could not prove")): return "tactic_failure"
    return "other"

def quantile(values, q):
    values = sorted(values)
    pos = (len(values)-1)*q
    lo = int(pos); hi = min(lo+1, len(values)-1)
    return values[lo] + (values[hi]-values[lo])*(pos-lo)

def write(path, rows):
    if not rows: return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0], lineterminator="\n")
        w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("parquet", type=pathlib.Path)
    ap.add_argument("--row-group", type=int, action="append", required=True)
    ap.add_argument("--out", type=pathlib.Path, required=True)
    args=ap.parse_args()
    import pyarrow.parquet as pq
    pf=pq.ParquetFile(args.parquet)
    expected=sum(pf.metadata.row_group(i).num_rows for i in args.row_group)
    counts=collections.Counter(); errors=collections.Counter(); tactics=collections.Counter()
    lengths=collections.defaultdict(list); keys=collections.defaultdict(collections.Counter)
    feedback=collections.Counter()
    for batch in pf.iter_batches(batch_size=128, row_groups=args.row_group, use_threads=False):
        for row in batch.to_pylist():
            label="valid" if row["isValid"] else "invalid"
            source=row["source_code"]; annotated=row["validation"]
            counts[label]+=1; lengths[label].append(len(source.encode()))
            keys[hashlib.blake2b(source.encode(), digest_size=32).digest()][label]+=1
            feedback[(label,"annotated_equal_source")]+=annotated==source
            feedback[(label,"contains_feedback")]+="<feedback>" in annotated
            feedback[(label,"no_goals_state")]+="-- proof state:\n" in annotated and "no goals" in annotated
            messages=ERROR.findall(annotated)
            feedback[(label,"has_error_block")]+=bool(messages)
            feedback[(label,"has_budget_error_block")]+=any(BUDGET.search(x) for x in messages)
            bucket=error_bucket(messages[0]) if messages else "no_error_block"
            errors[(label,bucket)]+=1
            try: code=masks(source)[1]
            except ValueError:
                feedback[(label,"lexically_unclosed_comment")]+=1
                continue
            tc=collections.Counter(TOKEN.findall(code))
            for tactic,n in tc.items():
                tactics[(label,tactic,"occurrences")]+=n
                tactics[(label,tactic,"rows")]+=1
    assert sum(counts.values())==expected
    args.out.mkdir(parents=True,exist_ok=True)
    write(args.out/"labels.csv",[{"label":k,"rows":counts[k],"fraction":counts[k]/expected} for k in ("valid","invalid")])
    write(args.out/"first-error.csv",[{"label":l,"first_error_surface":e,"rows":n} for (l,e),n in sorted(errors.items())])
    write(args.out/"tactics.csv",[{"label":l,"tactic":t,"measure":m,"value":n} for (l,t,m),n in sorted(tactics.items())])
    write(args.out/"feedback.csv",[{"label":l,"measure":m,"rows":n} for (l,m),n in sorted(feedback.items())])
    write(args.out/"source-sizes.csv",[{"label":l,"rows":len(v),"total_bytes":sum(v),"p50_bytes":quantile(v,.5),"p90_bytes":quantile(v,.9),"p99_bytes":quantile(v,.99),"max_bytes":max(v)} for l,v in sorted(lengths.items())])
    summary={"selected_row_groups":args.row_group,"rows":expected,"unique_exact_sources":len(keys),"extra_exact_source_rows":sum(sum(v.values())-1 for v in keys.values()),"keys_with_both_labels":sum(len(v)>1 for v in keys.values()),"scope":"requested materialized physical groups; sampling design supplied separately; no native timing"}
    (args.out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary),flush=True)

if __name__=="__main__": main()
