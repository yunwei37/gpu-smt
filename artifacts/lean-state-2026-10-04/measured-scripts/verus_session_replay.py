#!/usr/bin/env python3
"""Replay real captured Verus sessions: cold, warm reset, shared-prefix pool.

Records every SAT/UNSAT/UNKNOWN response against the fresh executable baseline;
any mismatch disqualifies that path from a semantic-fidelity/speedup claim.
This tests post-capture solver replay, not full Verus verification, arrival
latency, models/proofs, or equivalence to a historical Verus backend version.
"""
import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import sys
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from analyze_smt_trace import split_commands, command_head, int_arg, lcp_len


def decisions(output):
    if '(error ' in output: raise RuntimeError('Z3 protocol error: '+output[:2000])
    return re.findall(r'^(sat|unsat|unknown)\s*$',output,re.M)


class Session:
    def __init__(self,exe,cores):
        self.p=subprocess.Popen(['taskset','-c',cores,exe,'-in','-smt2'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.sel=selectors.DefaultSelector()
        self.sel.register(self.p.stdout,selectors.EVENT_READ,'out')
        self.sel.register(self.p.stderr,selectors.EVENT_READ,'err')
        self.number=0

    def call(self,text):
        self.number+=1; marker=f'GPU_SMT_REPLAY_END_{self.number}'
        payload=(text+'\n(echo "'+marker+'")\n').encode()
        errors=[]
        def write():
            try: self.p.stdin.write(payload);self.p.stdin.flush()
            except Exception as e: errors.append(e)
        thread=threading.Thread(target=write);thread.start()
        out=b'';err=b'';start=time.perf_counter()
        while marker.encode() not in out:
            events=self.sel.select(1)
            if time.perf_counter()-start>120: raise TimeoutError('solver protocol timeout')
            for key,_ in events:
                chunk=os.read(key.fileobj.fileno(),65536)
                if not chunk: raise RuntimeError('Z3 terminated: '+err.decode(errors='replace'))
                if key.data=='out':out+=chunk
                else:err+=chunk
        thread.join()
        if errors:raise errors[0]
        return out.decode(),err.decode()

    def close(self):
        self.p.stdin.close();self.p.wait(timeout=30);self.sel.close()
        if self.p.returncode:raise RuntimeError('Z3 process failed')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run_dir',type=Path);ap.add_argument('--z3',required=True)
    ap.add_argument('--cores',default='8');ap.add_argument('--repeat',type=int,default=3)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    tasks=[json.loads(l) for l in (args.run_dir/'runs.jsonl').read_text().splitlines()]
    jobs=[]; groups=defaultdict(list)
    for task in tasks:
        for path in sorted((args.run_dir/'traces'/task['task_id']).glob('*.smt2')):
            commands=split_commands(path.read_text())
            if any(command_head(c) in ('reset','reset-assertions','check-sat-assuming','exit') or ':global-decls' in c for c in commands):
                raise ValueError('unsupported stream command: '+str(path))
            depth=0
            for c in commands:
                if command_head(c)=='push':depth+=int_arg(c)
                if command_head(c)=='pop':depth-=int_arg(c)
                if depth<0:raise ValueError('unbalanced scope')
            options=[]
            for c in commands:
                if command_head(c)!='set-option':break
                options.append(c)
            group=hashlib.sha256('\n'.join(options).encode()).hexdigest()
            job=dict(task_id=task['task_id'],trace=str(path),commands=commands,group=group,depth=depth)
            jobs.append(job);groups[group].append(job)
    prefixes={}
    for group,js in groups.items():
        prefix=js[0]['commands'][:]
        # Only hoist original commands before any observable solver request or
        # scope change. All suffixes run under a fresh, popped job scope.
        for j in js:prefix=prefix[:lcp_len(prefix,j['commands'])]
        for i,c in enumerate(prefix):
            if command_head(c) not in ('set-option','assert') and not command_head(c).startswith(('declare-','define-')):
                prefix=prefix[:i];break
        prefixes[group]=prefix
    config=dict(z3=args.z3,z3_sha256=hashlib.sha256(Path(args.z3).read_bytes()).hexdigest(),
                version=subprocess.check_output([args.z3,'--version'],text=True).strip(),cores=args.cores,repeat=args.repeat,
                groups={g:dict(sessions=len(js),tasks=len(set(j['task_id'] for j in js)),prefix_commands=len(prefixes[g]),prefix_bytes=sum(len(c.encode())+1 for c in prefixes[g])) for g,js in groups.items()},
                scope='post-capture exact stream replay; per-query status parity only')
    (args.out/'config.json').write_text(json.dumps(config,indent=1)+'\n')
    baseline={};runs=[]
    for rep in range(args.repeat):
        modes=['cold','warm_reset','prefix_pool']
        if rep%2:modes.reverse()
        for mode in modes:
            start=time.perf_counter();pool={};records=[];setup=[]
            try:
                if mode!='cold':
                    for group in (groups if mode=='prefix_pool' else ['reset']):
                        t=time.perf_counter();s=Session(args.z3,args.cores);pool[group]=s
                        if mode=='prefix_pool':
                            out,err=s.call('\n'.join(prefixes[group]));decisions(out)
                            if err:raise RuntimeError(err)
                        setup.append(dict(group=group,seconds=time.perf_counter()-t))
                for j in jobs:
                    t=time.perf_counter()
                    if mode=='cold':
                        p=subprocess.run(['taskset','-c',args.cores,args.z3,'-in','-smt2'],input='\n'.join(j['commands'])+'\n',text=True,capture_output=True,timeout=120)
                        if p.returncode:raise RuntimeError(p.stderr+p.stdout)
                        out,err=p.stdout,p.stderr
                    elif mode=='warm_reset':
                        out,err=pool['reset'].call('(reset)\n'+'\n'.join(j['commands']))
                    else:
                        group=j['group'];suffix=j['commands'][len(prefixes[group]):]
                        out,err=pool[group].call('(push 1)\n'+'\n'.join(suffix)+f'\n(pop {j["depth"]+1})')
                    elapsed=time.perf_counter()-t;statuses=decisions(out)
                    if err:raise RuntimeError(err)
                    expected=sum(command_head(c)=='check-sat' for c in j['commands'])
                    if len(statuses)!=expected:raise RuntimeError('missing solver decisions')
                    if mode=='cold' and rep==0:baseline[j['trace']]=statuses
                    matches=statuses==baseline[j['trace']]
                    record=dict(task_id=j['task_id'],trace=j['trace'],seconds=elapsed,statuses=statuses,
                                expected_statuses=baseline[j['trace']],matches_baseline=matches,
                                output_sha256=hashlib.sha256(out.encode()).hexdigest())
                    if not matches: record['mismatch_output']=out
                    records.append(record)
                    with (args.out/'sessions.jsonl').open('a') as f:f.write(json.dumps(dict(mode=mode,repeat=rep,**record))+'\n')
            finally:
                for s in pool.values():s.close()
            runs.append(dict(mode=mode,repeat=rep,makespan_s=time.perf_counter()-start,setup=setup,records=records))
            (args.out/'runs.json').write_text(json.dumps(runs,indent=1)+'\n')
            print(mode,rep,len(records),round(runs[-1]['makespan_s'],4),
                  'mismatched sessions',sum(not r['matches_baseline'] for r in records),flush=True)


if __name__=='__main__':main()
