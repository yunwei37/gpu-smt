#!/usr/bin/env python3
"""Isolate additional SMT scope from cross-job history on real Verus traces.

Every path starts a fresh bundled Z3 executable. Original options/limits stay
fixed. Status differences are negative results, not semantic-preserving gains.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from analyze_smt_trace import split_commands, command_head
from verus_session_replay import decisions


def leading_options(commands):
    count=0
    for c in commands:
        if command_head(c)!='set-option':break
        count+=1
    return count


def scoped_commands(commands, prefix_count):
    return commands[:prefix_count]+['(push 1)']+commands[prefix_count:]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run-dir',type=Path,required=True)
    ap.add_argument('--replay-dir',type=Path,required=True)
    ap.add_argument('--z3',required=True);ap.add_argument('--cores',default='8')
    ap.add_argument('--repeat',type=int,default=2);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    config=json.loads((args.replay_dir/'config.json').read_text())
    oldruns=json.loads((args.replay_dir/'runs.json').read_text())
    baseline=next(r for r in oldruns if r['mode']=='cold' and r['repeat']==0)['records']
    oldpool=next(r for r in oldruns if r['mode']=='prefix_pool' and r['repeat']==0)['records']
    pool_status={r['trace']:r['statuses'] for r in oldpool}
    jobs=[]
    for row in baseline:
        path=args.run_dir/'traces'/row['task_id']/Path(row['trace']).name
        commands=split_commands(path.read_text());k=leading_options(commands)
        group=hashlib.sha256('\n'.join(commands[:k]).encode()).hexdigest()
        jobs.append(dict(record=row,commands=commands,options=k,prefix=config['groups'][group]['prefix_commands'],input_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    metadata=dict(z3=args.z3,z3_sha256=hashlib.sha256(Path(args.z3).read_bytes()).hexdigest(),cores=args.cores,repeat=args.repeat,
                  scope='fresh executable per session; sole intervention is extra push before declarations or before suffix',
                  diagnostics='get-info :reason-unknown immediately after every check; original resource limits unchanged')
    (args.out/'config.json').write_text(json.dumps(metadata,indent=1)+'\n')
    runs=[]
    for rep in range(args.repeat):
        modes=['original','extra_outer_scope','prefix_scope_fresh']
        if rep%2:modes.reverse()
        for mode in modes:
            start=time.perf_counter();records=[]
            for j in jobs:
                commands=j['commands']
                if mode=='extra_outer_scope':commands=scoped_commands(commands,j['options'])
                if mode=='prefix_scope_fresh':commands=scoped_commands(commands,j['prefix'])
                instrumented=[]
                for c in commands:
                    instrumented.append(c)
                    if command_head(c)=='check-sat':instrumented.append('(get-info :reason-unknown)')
                t=time.perf_counter()
                p=subprocess.run(['taskset','-c',args.cores,args.z3,'-in','-smt2'],input='\n'.join(instrumented)+'\n',text=True,capture_output=True,timeout=120)
                if p.returncode or p.stderr:raise RuntimeError(p.stderr+p.stdout)
                statuses=decisions(p.stdout)
                if len(statuses)!=len(j['record']['statuses']):raise RuntimeError('missing decisions')
                record=dict(task_id=j['record']['task_id'],trace=j['record']['trace'],input_sha256=j['input_sha256'],
                            seconds=time.perf_counter()-t,statuses=statuses,baseline_statuses=j['record']['statuses'],
                            matches_baseline=statuses==j['record']['statuses'],
                            matches_reused_pool=statuses==pool_status[j['record']['trace']],
                            unknown_reasons=re.findall(r'\(:reason-unknown "([^"\n]*)"\)',p.stdout),
                            output_sha256=hashlib.sha256(p.stdout.encode()).hexdigest())
                if not record['matches_baseline']:record['mismatch_output']=p.stdout
                records.append(record)
                with (args.out/'sessions.jsonl').open('a') as f:f.write(json.dumps(dict(mode=mode,repeat=rep,**record))+'\n')
            runs.append(dict(mode=mode,repeat=rep,makespan_s=time.perf_counter()-start,records=records))
            (args.out/'runs.json').write_text(json.dumps(runs,indent=1)+'\n')
            print(mode,rep,len(records),'baseline mismatches',sum(not r['matches_baseline'] for r in records),
                  'reused-pool mismatches',sum(not r['matches_reused_pool'] for r in records),flush=True)


if __name__=='__main__':main()
