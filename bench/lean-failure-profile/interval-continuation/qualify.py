"""Run bounded native development controls, retaining diagnostics and aggregate RSS.

Requires psutil from the existing Workspace environment. This is a tactic
qualification test, not a population acquisition or performance benchmark.
The existing acquisition owner is observed but never modified or terminated.
"""
import argparse, gzip, json, os, signal, subprocess, time
from pathlib import Path
import psutil

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--sdk',type=Path,required=True)
    a.add_argument('--project',type=Path,required=True)
    a.add_argument('--module-dir',type=Path,required=True)
    a.add_argument('--inputs',type=Path,required=True)
    a.add_argument('--expectations',type=Path,required=True)
    a.add_argument('--out',type=Path,required=True)
    a.add_argument('--existing-owner',type=int)
    a.add_argument('--existing-birth',type=float)
    args=a.parse_args()
    args.out.mkdir(exist_ok=False)
    os.sched_setaffinity(0,{11})
    root=psutil.Process()
    old=None
    if args.existing_owner:
        try:
            q=psutil.Process(args.existing_owner)
            if abs(q.create_time()-args.existing_birth)>.01:
                raise RuntimeError('existing owner identity changed')
            old=q
        except psutil.NoSuchProcess:
            pass
    env=dict(os.environ,PATH=str(args.sdk/'bin')+os.pathsep+os.environ['PATH'],
             LEAN_SYSROOT=str(args.sdk))
    raw=subprocess.check_output([str(args.sdk/'bin/lake'),'env','printenv','LEAN_PATH'],
                                cwd=args.project,env=env,text=True)
    env['LEAN_PATH']=str(args.module_dir)+os.pathsep+raw.strip()
    rows=json.loads(gzip.open(args.inputs,'rt').read())['candidates']
    expect={x['id']:x for x in json.loads(args.expectations.read_text())}
    budget=48*1024**3
    samples=[];results=[];errors=[]
    def sample():
        owned={}
        for owner in [root]+([old]if old else[]):
            try:
                for q in [owner]+owner.children(recursive=True):
                    try:
                        owned[(q.pid,q.create_time())]=q.memory_info().rss
                    except psutil.NoSuchProcess:
                        pass
            except psutil.NoSuchProcess:
                pass
        total=sum(owned.values())
        samples.append(dict(monotonic=time.monotonic(),rss_bytes=total,
            processes=[dict(pid=k[0],birth=k[1],rss_bytes=v)for k,v in owned.items()]))
        return total
    start=time.monotonic()
    for row in rows:
        if sample()>=budget:
            errors.append('no aggregate headroom; remaining development tests not started')
            break
        source=args.out/(row['id']+'.lean')
        source.write_text(row['code'])
        log=args.out/(row['id']+'.jsonl')
        cmd=[str(args.sdk/'bin/lean'),'--json','--stdin']
        begin=time.monotonic();pressure=False
        with source.open('rb')as inp,log.open('wb')as out:
            proc=subprocess.Popen(cmd,cwd=args.project,env=env,stdin=inp,
                stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
            try:
                while True:
                    if sample()>budget and proc.poll()is None:
                        pressure=True
                        os.killpg(proc.pid,signal.SIGKILL)
                    if proc.poll()is not None:break
                    time.sleep(1)
            finally:
                if proc.poll()is None:os.killpg(proc.pid,signal.SIGKILL)
                code=proc.wait()
        diagnostics=[];observations=[]
        for line in log.read_text().splitlines():
            try:
                if line.startswith('[gpu-smt-simp-stage] '):
                    observations.append(json.loads(line[len('[gpu-smt-simp-stage] '):]))
                elif line.startswith('[gpu-smt-closed-tail] '):
                    observations.append(json.loads(line[len('[gpu-smt-closed-tail] '):]))
                elif line.startswith('[gpu-smt-interval-stage] '):
                    observations.append(json.loads(line[len('[gpu-smt-interval-stage] '):]))
                else:diagnostics.append(json.loads(line))
            except json.JSONDecodeError:
                errors.append(dict(id=row['id'],non_json=line))
        severity=[d.get('severity')for d in diagnostics]
        admitted=any('sorry'in str(d.get('data',''))for d in diagnostics)
        status=('resource_interrupted'if pressure else'rejected'if code!=0 or
                'error'in severity else'incomplete'if admitted else'accepted')
        result=dict(id=row['id'],pair=expect[row['id']]['pair'],status=status,
            expected=expect[row['id']]['expected_status'],exit=code,
            seconds=time.monotonic()-begin,command=cmd,cwd=str(args.project),
            diagnostic_count=len(diagnostics),phase_observations=observations,
            pressure_aborted_new_test_only=pressure)
        results.append(result)
        print(json.dumps(result),flush=True)
        if pressure:break
    terminal=dict(completed=len(results),planned=len(rows),
        mismatches=[x for x in results if x['status']!=x['expected']],
        seconds=time.monotonic()-start,peak_combined_rss_bytes=max(x['rss_bytes']for x in samples),
        budget_bytes=budget,sampling_seconds=1,monitor_errors=errors,
        existing_owner=old.pid if old else None,development_controls_only=True,
        isolated_performance=False,results=results)
    (args.out/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
    (args.out/'memory.jsonl.gz').write_bytes(gzip.compress(
        ''.join(json.dumps(x)+'\n'for x in samples).encode(),mtime=0))
    (args.out/'run-source.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(terminal),flush=True)

if __name__=='__main__':main()
