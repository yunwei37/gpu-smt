"""Reorder only twelve existing Grid cells; never create additional measurements."""
from pathlib import Path
import os,sys,json,csv,importlib.util,time
B=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
F=B/'matrix-v3'
def main():
    os.sched_setaffinity(0,set(range(8,16)))
    spec=importlib.util.spec_from_file_location('priority_frozen_run',F/'run.py')
    run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
    matrix=list(csv.DictReader((F/'matrix.csv').open()))
    cells=[]
    for rep in range(1,4):
        for mode in ['plain','stat','trace']:
            cells.append(next(x for x in matrix if x['module']=='Grid' and x['config']=='noM' and x['mode']==mode and int(x['rep'])==rep))
    cells.extend(next(x for x in matrix if x['module']=='Grid' and x['config']=='threads1' and x['mode']=='plain' and int(x['rep'])==rep) for rep in range(1,4))
    here=Path(__file__).resolve().parent
    (here/'selected-cells.json').write_text(json.dumps(cells,indent=2)+'\n')
    results=[];stop=None
    for x in cells:
        target=B/'runs'/f"Grid-{x['config']}-{x['mode']}-r{x['rep']}"
        if (target/'result.json').exists():
            rr=json.loads((target/'result.json').read_text())
            if not rr.get('retired') or not rr.get('native_cgroup_retired'):stop='existing native not retired';break
        elif target.exists():stop='another producer owns partial '+str(target);break
        else:
            print('PRIORITY_START',json.dumps(x),flush=True)
            try:rr=run.run_one('Grid',x['config'],x['mode'],int(x['rep']),1250,inputs_path=F/'inputs.json')
            except BaseException as e:stop=repr(e);break
        results.append({'sequence_in_original_matrix':int(x['sequence']),'raw':str(target),'returncode':rr.get('returncode'),'retired':rr.get('retired')})
        (here/'progress.json').write_text(json.dumps({'completed':len(results),'planned':12,'last':results[-1]},indent=2)+'\n')
        if not rr.get('retired') or not rr.get('native_cgroup_retired') or rr.get('stop_reason'):stop='native operational failure';break
    (here/'terminal.json').write_text(json.dumps({'complete':len(results)==12 and stop is None,'completed':len(results),'planned':12,'stop':stop},indent=2)+'\n')
    return 0 if stop is None else 2
if __name__=='__main__':sys.exit(main())
