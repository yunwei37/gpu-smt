#!/usr/bin/env python3
"""Collect corrected stock-checker measurements without changing prior failures."""
import os,json,csv,statistics,subprocess,time
from pathlib import Path
os.sched_setaffinity(0,set(range(8,16)))
repo=Path('/workspaces/repository');os.chdir(repo)
out=repo/'research/profile-2026-10-31/startup-replay'
raw=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/startup-replay/repair-v3')
terminal=json.loads((raw/'terminal.json').read_text())
rows=[json.loads(x)for x in(raw/'results.jsonl').read_text().splitlines()]
paired={r['module']:r for r in csv.DictReader((out/'startup-paired.csv').open())}
old={r['module']:r for r in json.loads((raw/'targets.json').read_text())}
data=[]
for r in rows:
 baseline=float(paired[r['module']]['build_median_s'])if r['module']in paired else old.get(r['module'],{}).get('wall_s')
 historical=old.get(r['module'],{}).get('wall_s')
 data.append(dict(module=r['module'],kind=r['kind'],fresh=r['fresh'],returncode=r['returncode'],stop=r['stop']or'',success=r['success'],
 target_replay_announced=r['target_replay_announced'],wall_s=r['wall_s'],user_s=r['user_s'],system_s=r['system_s'],
 peak_rss_kib=r['peak_rss_kib'],sampled_tree_rss_max_bytes=r['sampled_tree_rss_max_bytes'],minor_faults=r['minor_faults'],major_faults=r['major_faults'],
 observer_cpu_self_s=r['observer_cpu_self_s'],comparison_build_s=baseline if baseline is not None else'',
 comparison_build_scope='prior paired 3-repeat P-core matrix'if r['module']in paired else'historical Grid/Amplitudes'if historical else'not measured',
 replay_over_build=r['wall_s']/baseline if baseline and r['success']and not r['fresh']else'',
 historical_build_s=historical if historical else'',historical_ratio=r['wall_s']/historical if historical and r['success']and not r['fresh']else'',
 bound_s=r['limit_s']))
def write(name,data):
 if not data:return
 with(out/name).open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
write('repaired-kernel-replay.csv',data)
scope=[]
for f in rows:
 if not f['fresh']:continue
 b=next((r for r in rows if r['module']==f['module']and not r['fresh']and r['kind']!='preflight'),None)
 if not b:continue
 scope.append(dict(module=f['module'],import_relative_success=b['success'],import_relative_s=b['wall_s'],
 fresh_success=f['success'],fresh_s=f['wall_s'],fresh_stop=f['stop']or'',fresh_returncode=f['returncode'],
 fresh_over_import_relative=f['wall_s']/b['wall_s']if f['success']and b['success']else'',
 fresh_peak_rss_kib=f['peak_rss_kib'],default_peak_rss_kib=b['peak_rss_kib'],fresh_bound_s=f['limit_s']))
write('replay-scope-comparison.csv',scope)
targets=[r for r in data if r['kind']=='target'];ok=[r for r in targets if r['success']]
short=[r for r in ok if r['module']in paired]
def med(k,rs):return statistics.median(r[k]for r in rs)if rs else 'unavailable'
text=f"""# Repaired native kernel replay results
Generated {time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}; review: self-review.
This supersedes the failed v2 module-enumeration attempt, whose data remain intact.
Raw data: {raw}. Version: {(raw/'version.txt').read_text().strip()}.
Terminal: {terminal}.

## Repair qualification
Every one of the 28 prior targets and 13 prior empty controls failed lookup,
not kernel checking. The symlink realpath escaped the checker search roots.
Ordinary hardlinks inside a correctly named artifact tree repair enumeration.
The separate unmeasured E-core functional control exited0, announced the exact
NearPinDeletion target and printed no stderr. Formal timing then rechecked that
same target under the shared P-core lock; the batch could start only on success.
These are stock 4.34.1 leanchecker runs, with matching LEAN_SYSROOT and no custom
kernel or patched checker. --fresh was not used as a path fix.

## Import-relative replay versus construction
Returned {len(targets)}/15 requested target records; {len(ok)} uncensored exit-zero
replays. All numeric ratios below use only qualified successes.
Of thirteen short modules with prior 3-repeat build medians, {len(short)} succeeded.
Their checker process wall median is {med('wall_s',short)} seconds; median
checker/full-build ratio is {med('replay_over_build',short)}.
This process duration includes CLI module discovery, dependency import, target
kernel replay and cleanup. It is **not exclusive kernel CPU**. The thirteen build
denominators come from the earlier P-core paired startup matrix and include its
observer cost; they are not contemporaneous randomized build/replay pairs.
Read observer-calibration.csv and startup-analysis.md before generalizing.
Grid and Amplitudes ratios use their separately retained historical standard
build durations. They are explicitly labelled in the CSV and are not substituted
into the thirteen-module matched-build median.
"""
for r in targets:
 text+=f"- {r['module']}: success={r['success']}, wall={r['wall_s']:.6f}s, peak RSS={r['peak_rss_kib']/1024**2:.3f}GiB, replay/build={r['replay_over_build']}, stop={r['stop']or'none'}.\n"
text+="""
## --fresh scope samples
Default replay trusts imported declarations and rechecks target-module constants.
--fresh loads the target, then replays its entire loaded constant map into an
empty kernel environment: it can be much more expensive and is not comparable
to reconstructing only one source module. Both modes skip unsafe and partial
declarations in upstream Kernel.Environment.replay and reuse the stock kernel;
neither is an independently implemented checker. Fresh mode does not mean cold
OS page cache. All samples are separate bounded process invocations.
"""
for r in scope:
 text+=f"- {r['module']}: default={r['import_relative_s']:.6f}s; fresh success={r['fresh_success']}, observed={r['fresh_s']:.6f}s, bound={r['fresh_bound_s']:.3f}s, stop={r['fresh_stop']or'none'}, ratio={r['fresh_over_import_relative']}.\n"
text+="""
Censored fresh runs are only observed resource/time limits; no successful replay
duration or exact build ratio is imputed for them. A timeout's observed wall is
not a successful fresh-check cost. Full stdout/stderr and RSS samples are on PVC.

## Measurement and limitations
The submission observed W holder37246 and existing M waiter11027; O joined after
M. Actual kernel lock state at acquisition is in launch.json. The whole measured
matrix holds one existing P-core lock, with affinity0-7, eight runtime workers,
a 1,700s internal block deadline and per-cell bounds. Actual RSS sampling reserves
128MiB for its parent inside the12GiB allocation. Child user/system CPU, wait4
maximum RSS, sampled tree RSS and observer CPU remain distinct columns.
No host settings, other pods, old captures or other lines' paths were changed.
"""
(out/'repaired-replay-analysis.md').write_text(text)
# This is a historical failure report; retain its contents and add only a pointer.
p=out/'replay-analysis.md';oldtext=p.read_text()
banner='> Historical failed lookup attempt: see [corrected replay results](repaired-replay-analysis.md).\n\n'
if not oldtext.startswith(banner):p.write_text(banner+oldtext)
paths=[str((out/f).relative_to(repo))for f in ['repaired-kernel-replay.csv','replay-scope-comparison.csv','repaired-replay-analysis.md','replay-analysis.md']if(out/f).exists()]
(raw/'collection-summary.json').write_text(json.dumps(dict(target_records=len(targets),successful_targets=len(ok),successful_short_modules=len(short),scope_samples=scope,paths=paths),indent=2))
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
for cmd in [['git','add','--']+paths,['git','-c','user.name=Yunwei 123','-c','user.email=yunwei356@gmail.com','commit','--only','-m','profile: retain corrected kernel replay and fresh scope measurements','--']+paths]:
 r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);print(r.stdout,flush=True)
 if r.returncode:raise SystemExit(r.returncode)
r=subprocess.run(['git','pull','--rebase','--no-autostash','origin','main'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);print(r.stdout,flush=True)
helper="!python3 -c 'import os; print(\"username=x-access-token\"); print(\"password=\"+os.environ[\"ENVBUILDER_GIT_PASSWORD\"])'"
subprocess.run(['git','-c','credential.helper='+helper,'fetch','origin','main'],check=True)
subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],check=True)
subprocess.run(['git','-c','credential.helper='+helper,'push','origin','main'],check=True)
(raw/'published-result.txt').write_text(subprocess.check_output(['git','rev-parse','HEAD'],text=True))
