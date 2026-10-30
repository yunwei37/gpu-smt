"""Reproduce the bounded reflected-grid pipeline on the retained phobos-vt point."""
from pathlib import Path
import argparse, json, os, time
import run_finite
from generate_grid_certificate import generate

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("label", help="fresh capture label on the existing PVC")
    p.add_argument("--measure-chunks", action="store_true",
                   help="also perform counterbalanced1/2/4/8-task kernel rechecks")
    a=p.parse_args()
    began=time.monotonic()
    gen=generate(run_finite.BUILD_ROOT/a.label)
    if a.measure_chunks: os.environ["M_GRID_MEASURE"]="1"
    else: os.environ.pop("M_GRID_MEASURE",None)
    code=run_finite.run(Path(gen["source"]),a.label,wall_seconds=120,jobs=8,cpus="8-15")
    terminal={"exit":code,"end_to_end_wall_s":time.monotonic()-began,
              "includes":"C compilation, scan, source emission, complete Lean invocation and capture IO",
              "additional_checks":"one final-theorem recheck; chunk groups only if requested",
              "measure_chunks":a.measure_chunks,"jobs":8,"cpus":"8-15"}
    (run_finite.CAPTURE_ROOT/a.label/"pipeline.json").write_text(json.dumps(terminal,indent=2)+"\n")
    print(json.dumps(terminal),flush=True)
    return code
if __name__=="__main__":raise SystemExit(main())
