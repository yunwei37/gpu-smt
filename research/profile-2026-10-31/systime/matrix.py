"""Finite user-requested matrix; one bounded native invocation per P-core lock."""
from pathlib import Path
import csv,json,os,sys,time,subprocess,select,importlib.util
ROOT=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
FROZEN=Path(__file__).resolve().parent
def alive(identity):
    try:return Path(f"/proc/{identity['pid']}/stat").read_text().rsplit(')',1)[1].split()[19]==str(identity['birth'])
    except OSError:return False
def main():
    os.sched_setaffinity(0,set(range(8,24)))
    start=time.time()
    spec=importlib.util.spec_from_file_location('frozen_systime_run',FROZEN/'run.py')
    run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
    planned=list(csv.DictReader((FROZEN/'matrix.csv').open()))
    prior=json.loads((ROOT/'UMoments9-baseline-plain-v2-controller.json').read_text())
    completed=[];stopped=None
    for cell in planned:
        module,config,mode=cell['module'],cell['config'],cell['mode'];rep=int(cell['rep'])
        target=ROOT/'runs'/f'{module}-{config}-{mode}-r{rep}'
        if cell['role']=='retain_or_fill_original_triplet' and alive(prior):
            print('retain original producer until real exit',prior,flush=True)
            fd=os.pidfd_open(prior['pid'])
            try:ready=select.select([fd],[],[],1800)[0]
            finally:os.close(fd)
            if not ready:stopped='original producer still live; no duplicate';break
        if (target/'result.json').exists():
            result=json.loads((target/'result.json').read_text())
            if not result.get('native_cgroup_retired') or not result.get('retired'):
                stopped='existing capture lacks native retirement; inspect '+str(target);break
            result['retained_existing']=True
        elif target.exists():
            stopped='existing partial capture preserved; inspect '+str(target);break
        else:
            print('START',json.dumps(cell),flush=True)
            try:result=run.run_one(module,config,mode,rep,1250,inputs_path=FROZEN/"inputs.json")
            except BaseException as exc:
                stopped=type(exc).__name__+': '+str(exc);print('MATRIX_STOP',stopped,flush=True);break
        completed.append({'sequence':int(cell['sequence']),'module':module,'config':config,'mode':mode,'rep':rep,
            'returncode':result.get('returncode'),'retired':result.get('retired'),'raw':str(target),
            'retained_existing':result.get('retained_existing',False)})
        with (FROZEN/'completed.jsonl').open('a') as f:f.write(json.dumps(completed[-1])+'\n')
        (FROZEN/'progress.json').write_text(json.dumps({'planned':len(planned),'completed':len(completed),'last':completed[-1]},indent=2)+'\n')
        # Operational/observer failure must not lead to overlapping native execution.
        # A normal Lean rejection or timeout is retained as an outcome, never retried automatically.
        if not result.get('native_cgroup_retired') or result.get('stop_reason'):
            stopped='native operational stop: '+str(result.get('stop_reason'));break
    terminal={'planned':len(planned),'completed':len(completed),'complete':len(completed)==len(planned) and stopped is None,
      'stop':stopped,'elapsed_wall_including_queue_s':time.time()-start,
      'scope':'per-cell self<=1200s; shared-lock queue waits separately retained; overall finite90-cell requested matrix'}
    (FROZEN/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
    print('TERMINAL',json.dumps(terminal),flush=True)
    return 0 if terminal['complete'] else 2
if __name__=='__main__':sys.exit(main())
