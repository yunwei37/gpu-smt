#!/usr/bin/env python3
"""Read existing complete native5 primary observations; never run a verifier."""
import argparse, importlib.util, json, statistics, datetime
from pathlib import Path
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("original_e022_analysis",BASE/"analyze.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.COUNTERS=module.COUNTERS+("host_declined","head_admission_ns")
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--run",type=Path,required=True);p.add_argument("--out",type=Path,required=True);args=p.parse_args()
 pairs=[];providers=[]
 for rep in range(3):
  cells={m:json.loads((args.run/f"proofnet-rep{rep}-{m}.analysis.json").read_text()) for m in ("warm","snapshot-cache","cpu","gpu")}
  stock=cells["warm"];issues=[]
  for m,c in cells.items():
   if not c["valid_complete"] or c["expected"]!=5952 or c["returned"]!=5952:issues.append(m+": incomplete original source population")
   if c["basic_rows"]!=stock["basic_rows"]:issues.append(m+": basic differences")
   if c["actual_affinity"]!=stock["actual_affinity"] or c["workers"]!=stock["workers"]:issues.append(m+": resources differ")
  fastest=min((c["whole_seconds"],m) for m,c in cells.items() if m!="gpu")
  row=dict(repetition=rep,issues=issues,valid=not issues,whole_seconds={m:c["whole_seconds"] for m,c in cells.items()},fastest_cpu_method=fastest[1],gpu_slowdown_percent=100*(cells["gpu"]["whole_seconds"]/fastest[0]-1) if not issues else None)
  pairs.append(row)
  raw=module.Raw(args.run,f"proofnet-rep{rep}-gpu")
  try:
   result=module.provider(raw);malformed=0
   for name in raw.names():
    if name=="stderr.bin" or name.endswith("/stderr.bin"):
     for line in raw.read(name).splitlines():
      if line.startswith(b"{"):
       try:json.loads(line)
       except (ValueError,UnicodeDecodeError):malformed+=1
   result.update(repetition=rep,malformed_json_lines=malformed,counter_limit="Per-PID cumulative maxima, not exact complete counters when terminal/interleaved records are missing. Nested timer sums are not exclusive whole-wall components.")
   providers.append(result)
  finally:raw.close()
 report=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=str(args.run),pairs=pairs,all_three_primary_blocks_valid=all(p["valid"] for p in pairs),provider_observations=providers,scope="Only three complete matched ProofNet primary blocks; separate profiles and mini remain pending. No cross-version causal timing inference or whole-kernel GPU discharge.")
 if report["all_three_primary_blocks_valid"]:
  values=[p["gpu_slowdown_percent"] for p in pairs];report["descriptive_gpu_slowdown_percent"]=dict(mean=statistics.mean(values),minimum=min(values),maximum=max(values),n=3,uncertainty="Observed repeat range, not a confidence interval")
 args.out.write_text(json.dumps(report,indent=2)+"\n")
if __name__=="__main__":main()
