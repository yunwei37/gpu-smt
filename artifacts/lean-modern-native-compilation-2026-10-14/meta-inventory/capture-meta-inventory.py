#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,importlib.util,json,os,resource,socket,sys
R=Path('/workspaces/repository')
D=R/'artifacts/lean-modern-native-compilation-2026-10-14'
ROOT=D/'meta-inventory'
E=R/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-033'
NATIVE=Path('/tmp/gpu-smt-meta-inventory-20261016/repl-meta-inventory')
spec=importlib.util.spec_from_file_location('capture',D/'native-cpu-sampling-capture.py')
cap=importlib.util.module_from_spec(spec);spec.loader.exec_module(cap)
original_environment=cap.environment
active_observations=None
def environment(method):
    env=original_environment(method)
    if active_observations is not None:
        env['LEAN_SERVER_REPL_PATH']=str(NATIVE)
        env['GPU_SMT_META_OBSERVER_DIR']=str(active_observations)
    else:
        env.pop('GPU_SMT_META_OBSERVER_DIR',None)
    return env
cap.environment=environment
def save(path,x):path.write_text(json.dumps(x,indent=2)+'\n')
def main():
    global active_observations
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['preflight','full']);args=ap.parse_args()
    os.sched_setaffinity(0,{0,1,2,3})
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    # Use only the original capture's private endpoint after proving it is unused.
    with socket.socket() as check:check.bind(('127.0.0.1',8012))
    out=ROOT/('preflight1' if args.action=='preflight' else 'full1')
    out.mkdir()
    inputs=D/('preflight-native-cpu-input.jsonl' if args.action=='preflight' else 'input.jsonl')
    (out/'declared-input.jsonl').write_bytes(inputs.read_bytes())
    states=[False,True] if args.action=='preflight' else [True]
    save(out/'scope.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source_capture=str(D/'native-cpu-sampling-capture.py'),action=args.action,
        original_environment_native=original_environment('compiled')['LEAN_SERVER_REPL_PATH'],
        observed_native=str(NATIVE),affinity=sorted(os.sched_getaffinity(0)),
        observer='constant-time borrowed Expr.data; outer wrapped per-thread CPU only',
        workload=str(inputs),endpoint='existing private8012; bind-probed unused',
        scope='Diagnostic, no speedup. Same original source/native HTTP capture with isolated binary/environment observer override. No active SDK/backend/capture modified.'))
    try:
        for enabled in states:
            label=('observed-controls' if enabled else 'original-controls') if args.action=='preflight' else 'goedel427-meta-inventory'
            active_observations=out/(label+'-observations') if enabled else None
            if active_observations is not None:active_observations.mkdir()
            print('NATIVE_BEGIN',label,flush=True)
            cap.capture(out,label,'preflight' if args.action=='preflight' else 'goedel427','compiled',False)
        save(out/'driver-terminal.json',dict(returncode=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    except BaseException as exc:
        save(out/'driver-terminal.json',dict(returncode=1,error_type=type(exc).__name__,error=str(exc),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
        raise
if __name__=='__main__':main()
