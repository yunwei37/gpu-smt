#!/usr/bin/env python3
"""Collect only after real exit; publish mechanically derived O-line results."""
import os,sys,pathlib,subprocess,json,csv,statistics,time
from pathlib import Path
os.sched_setaffinity(0,set(range(8,16)))
repo=Path('/workspaces/repository')
out=repo/'research/profile-2026-10-31/startup-replay'
base=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay')
raw=base/'v2';cal=base/'calibration'
os.chdir(repo)
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
subprocess.run(['python3',str(out/'analyze.py'),str(raw),str(out)],check=True)
rows=[json.loads(x)for x in(raw/'results.jsonl').read_text().splitlines()]
cr=[json.loads(x)for x in(cal/'results.jsonl').read_text().splitlines()]if(cal/'results.jsonl').exists()else[]
def median(v):return statistics.median(v)if v else None
def csvwrite(name,data):
 if not data:return
 with(out/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
checks=[]
for r in rows:
 if r['mode']!='replay':continue
 empty=next((e for e in rows if e['mode']=='empty_replay'and e['module']==r['module']),None)
 checks.append(dict(module=r['module'],checker_returncode=r['returncode'],checker_stop=r['stop'],checker_total_s=r['wall_s'],
 empty_control_s=empty['wall_s']if empty else '',empty_returncode=empty['returncode']if empty else '',
 target_minus_empty_s=r['wall_s']-empty['wall_s']if empty and r['returncode']==empty['returncode']==0 else '',
 note='separate-process difference; not pure kernel CPU'))
csvwrite('checker-controls.csv',checks)
comparison=[]
for mode,module in dict.fromkeys((r['mode'],r.get('module','Mathlib'))for r in cr):
 a=[r for r in rows if r['mode']==mode and r.get('module','Mathlib')==module and r['returncode']==0]
 b=[r for r in cr if r['mode']==mode and r.get('module','Mathlib')==module and r['returncode']==0]
 if a and b:
  aa=median([r['wall_s']for r in a]);bb=median([r['wall_s']for r in b])
  comparison.append(dict(mode=mode,module=module,original_sampler_median_s=aa,own_descendants_sampler_median_s=bb,calibration_over_original=bb/aa,original_n=len(a),calibration_n=len(b)))
csvwrite('observer-calibration.csv',comparison)
hot=[]
for data in sorted(raw.glob('perf-*.data')):
 cmd=['perf','report','--stdio','--no-children','--percent-limit','1','--sort','symbol','-g','none','-i',str(data)]
 r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (raw/(data.stem+'.report.txt')).write_text(r.stdout)
 count=0
 for line in r.stdout.splitlines():
  z=line.strip().split()
  if len(z)>=3 and z[0].endswith('%'):
   try:value=float(z[0].rstrip('%'))
   except ValueError:continue
   hot.append(dict(profile=data.stem,overhead_pct=value,symbol=' '.join(z[1:]),report_returncode=r.returncode))
   count+=1
   if count>=20:break
csvwrite('perf-hotspots.csv',hot)
replay=[r for r in rows if r['mode']=='replay'];ok=[r for r in replay if r['returncode']==0 and not r['stop']]
ratios=[r['wall_s']/r['historical_build_s']for r in ok]
observer=[json.loads(x)for x in(cal/'observer.jsonl').read_text().splitlines()]if(cal/'observer.jsonl').exists()else[]
terminals={str(p.relative_to(base)):p.read_text()for p in base.glob('*/**/*terminal*')if p.is_file()}
summary=json.loads((raw/'analysis-summary.json').read_text())
text=f"""# Native kernel replay and finalized capture
Generated from actual retained records at {time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}.
Review: self-review. Raw data: {base}.
This report does not claim uninstrumented timings, a new checker, or acceleration.

## Terminal coverage
Startup: {summary['by_mode'].get('build',{})}, imports:
{summary['by_mode'].get('imports',{})}, Mathlib: {summary['by_mode'].get('mathlib',{})}.
Target-module replay returned {len(replay)}/28 records, {len(ok)} exit-zero uncensored.
Empty-module checker controls: {sum(r['mode']=='empty_replay'for r in rows)}/13 records.
Separate perf runs: {sum(r['mode']=='perf'for r in rows)} records;
{len(hot)} reported hotspot rows. Missing or failed cells are not successes.
Calibration: {len(cr)}/21 records; observer CPU sum
{sum(r['observer_cpu_self_s']for r in observer):.6f} seconds.
All native wall/stop/returncode fields are retained in the CSVs and PVC.

## Replay cost
For the {len(ok)} successful replay records, median total checker/historical-full-build
ratio is {median(ratios)}. The entire checker process is measured, including
path search, imports, target replay and cleanup. Imported declarations remain
trusted; upstream skips unsafe/partial declarations. Thus this is not the cost
of checking the entire dependency closure from empty state.
Only 13 short modules have new matched full-build repetitions; their separate
ratios are in kernel-replay.csv. The remaining build denominators are historical
A/Grid/Amplitudes runs, not a current randomized paired comparison.
Do not interpret the ratio as removable end-to-end work or a guaranteed speedup.

## Controls and observer costs
checker-controls.csv compares each available small target with a zero-declaration
module with the same direct imports. Differences are between separate processes;
they are not exclusive kernel time and may be negative.
observer-calibration.csv compares the original all-proc descendant scan with
own-task child discovery on historical min/median/max-sized short modules plus
Mathlib. It is a sequential calibration, not a randomized causal estimate.
The original startup observer/preparation cost was about 54.045 CPU seconds;
that overhead is not subtracted from reported wall time. The original and
calibration captures remain separate, including all memory samples.

## Perf interpretation
perf-hotspots.csv lists native perf self-sample symbol percentages, separately
for each import-only profile. The first four are user-space cycles only;
perf-all-mathlib includes user and kernel. Percentages are sampling distributions,
not whole-build elapsed fractions. Profiled wall times are not used as ordinary
timing repetitions. perf.data, reports, stderr/lost-sample diagnostics and exact
commands remain on PVC. No host sysctl or kernel module was changed.

## Startup scale and scope
The complete instrumented first startup matrix is analyzed in startup-analysis.md:
13 short selected modules, import median 1.355 s, cohort import/build ratio about
0.68. Scaling 163,000 identical imports illustrates serial 32.23–144.68 hours,
median 61.34 hours, not a population estimate or parallel build prediction.
The main dataset is conditional on historical small successful modules, with warm
OS page cache and explicit compiler artifacts, not a cold fresh machine.

## Non-success replay rows
"""
for r in replay:
 if r['returncode'] or r['stop']:text+=f"- {r['module']}: rc={r['returncode']}, stop={r['stop']}, wall={r['wall_s']:.3f}s.\n"
(out/'replay-analysis.md').write_text(text)
(raw/'finalization.json').write_text(json.dumps(dict(summary=summary,replays=len(replay),replay_success=len(ok),calibration_rows=len(cr),hotspot_rows=len(hot),terminal_files=terminals),indent=2))
# No shared checkout stashing: only these mechanically generated O result files.
paths=[str(p.relative_to(repo))for p in out.glob('*.csv')]+[str((out/'replay-analysis.md').relative_to(repo))]
for cmd in [['git','add','--']+paths,['git','-c','user.name=Yunwei 123','-c','user.email=yunwei356@gmail.com','commit','--only','-m','profile: retain completed native startup and kernel replay results','--']+paths]:
 r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);print(r.stdout,flush=True)
 if r.returncode:raise SystemExit(r.returncode)
r=subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);print(r.stdout,flush=True)
helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],check=True)
subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],check=True)
subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],check=True)
(raw/'published-result.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],text=True))
