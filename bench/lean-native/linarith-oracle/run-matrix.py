"""Continue the admitted heavy-cohort comparison without a redundant CPU grid.
Retain the already-running first pair. Use the existing collector receipts, not goal polling.
"""
from pathlib import Path
import argparse, json, os, select, signal, subprocess, sys
R=Path('/workspaces/repository')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017')
OUT=U/'matched-top1000'
PY=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python')
RUN=R/'bench/lean-native/linarith-oracle/run-comparison.py'
def wait_file(path,pid):
    """Wait inside this experiment process; no agent/goal polling or new watcher."""
    if path.exists():return
    try:pidfd=os.pidfd_open(pid)
    except ProcessLookupError:
        if path.exists():return
        raise
    try:
        while not path.exists():
            # inotify instances are exhausted on this shared host (EMFILE).
            # Block on the collector exit event, and inspect its existing cell
            # file periodically; do not change host watch limits or settings.
            ready,_,_=select.select([pidfd],[],[],10)
            if ready and not path.exists():
                raise RuntimeError('collector ended before '+str(path))
    finally:os.close(pidfd)

def stop_redundant_tail(pid):
    p=Path('/proc')/str(pid)/'cmdline'
    if not p.exists():return
    cmd=p.read_bytes()
    parts=cmd.split(bytes([0]))
    if b'fast-highs' not in parts and b'native' not in parts:return
    if b'run-comparison.py' not in cmd or b'primary1' not in cmd:return
    pairs=[tuple(map(int,l.split())) for l in subprocess.check_output(['ps','-eo','pid=,ppid='],text=True).splitlines()]
    owned={pid}
    for _ in range(8):owned.update(p for p,parent in pairs if parent in owned)
    for p in sorted(owned,reverse=True):
        try:os.kill(p,signal.SIGTERM)
        except ProcessLookupError:pass
    (OUT/'primary1/canceled-redundant-controls.md').write_text(
      'First Fast/hybrid and direct-oracle cells completed before stopping the old queued grid. '
      'Any started stock/HiGHS tail is partial and retained, not timing evidence. '
      'Only after a qualifying direct-vs-strong-baseline result are further competitors useful.\n')
def run(label,methods,diagnostic=False):
    output = OUT/label
    if output.exists():
        terminals = [output/("rep1-"+method)/"terminal.json" for method in methods]
        if all(p.exists() and (lambda t: t["state"] == "complete" and t["attempts"] == 1000)(
            json.loads(p.read_text())) for p in terminals):
            print("PRESERVED_COMPLETE_CAPTURE", label, flush=True)
            return
        raise RuntimeError("preserve incomplete capture; use a separately recorded recovery directory: "+str(output))
    cmd=[str(PY),str(RUN),'--out',str(OUT/label),'--methods',*methods]
    if diagnostic:cmd.append('--diagnostic')
    with (OUT/(label+'.log')).open('wb') as log:
        subprocess.run(cmd,cwd=R,check=True,stdout=log,stderr=subprocess.STDOUT)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first_pair_pid", nargs="?", type=int)
    parser.add_argument("--resume-completed", action="store_true",
                        help="reuse restored closed pairs after collector loss; never rerun complete cells")
    args=parser.parse_args()
    if not args.resume_completed and args.first_pair_pid is None:
        parser.error("original first-pair pid or --resume-completed is required")
    pid=args.first_pair_pid
    for method in ['fast-hybrid','oracle']:
        path=OUT/'primary1'/('rep1-'+method)/'terminal.json'
        if args.resume_completed and not path.exists():
            raise RuntimeError("resume requires the preserved completed first pair: "+str(path))
        wait_file(path,pid)
        cell=json.loads(path.read_text())
        if cell['state']!='complete' or cell['attempts']!=1000:raise RuntimeError('first native pair incomplete')
    if not args.resume_completed:
        stop_redundant_tail(pid)
    run('primary2',['oracle','fast-hybrid'])
    run('primary3',['fast-hybrid','oracle'])
    # Requested four-stage native diagnostic, separate from primary timing.
    run('native-stages',['strong-profile','oracle'],True)
    times={}
    for method in ['fast-hybrid','oracle']:
        times[method]=sum(json.loads((OUT/('primary%d'%i)/('rep1-'+method)/'terminal.json').read_text())['whole_ns'] for i in [1,2,3])
    ratio=times['fast-hybrid']/times['oracle']
    print('THREE_PAIR_WHOLE_RATIO',ratio,'native agreement/result review still required',flush=True)
    # If this necessary comparison already misses the user threshold, faster
    # alternative baselines cannot turn it into a success; no further CPU grid.
    if ratio>1.5:
        for i,methods in [(1,['native','fast-highs']),(2,['fast-highs','native']),(3,['native','fast-highs'])]:
            run('controls%d'%i,methods)
    print('Admitted cohort capture ended; root result review and app automation decision required.',flush=True)
if __name__=='__main__':main()
