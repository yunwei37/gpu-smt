#!/usr/bin/env python3
"""Verify published Mathlib proofs and controlled mutations with REPL backtracking.

Parser-observed command spans retain the exact source prefix before each proof.
This is a real-library proof replay workload with artificial negative variants,
not a collected model-generated candidate stream.
"""
import argparse
import codecs
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import time


def classify(response):
    if response.get('error') or any(m['severity']=='error' for m in response.get('messages', [])):
        return 'rejected'
    if response.get('sorries') or any(re.search(r"declaration uses [`']sorry[`']", m.get('data','')) for m in response.get('messages', [])):
        return 'incomplete'
    if 'env' not in response:
        raise RuntimeError(f'unknown REPL response: {response}')
    return 'accepted'


class REPL:
    def __init__(self, args, env):
        self.proc = subprocess.Popen(['taskset','-c',args.cores,args.repl],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1,env=env)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.proc.stdout, selectors.EVENT_READ)
        self.buffer = ''
        self.decoder = codecs.getincrementaldecoder('utf-8')()

    def call(self, request):
        start = time.perf_counter()
        self.proc.stdin.write(json.dumps(request)+'\n\n'); self.proc.stdin.flush()
        while True:
            stripped = self.buffer.lstrip()
            try:
                response, consumed = json.JSONDecoder().raw_decode(stripped)
                self.buffer = stripped[consumed:]
                return response, time.perf_counter()-start
            except json.JSONDecodeError:
                pass
            # A finite protocol timeout catches a stuck backend, not a research deadline.
            if not self.selector.select(3600): raise TimeoutError('REPL response timeout')
            data = os.read(self.proc.stdout.fileno(),65536)
            if not data: raise RuntimeError('REPL exited: '+self.proc.stderr.read())
            self.buffer += self.decoder.decode(data)

    def close(self):
        self.proc.stdin.close(); self.proc.wait(timeout=60)
        self.selector.close()
        if self.proc.returncode: raise RuntimeError(self.proc.stderr.read())


def read_workload(source, spans):
    data = source.read_bytes()
    parsed = json.loads(spans.read_text())
    if parsed['errors']: raise ValueError('source trace contains errors')
    cases = []
    for index, span in enumerate(parsed['commands']):
        text = data[span['start']:span['stop']].decode()
        match = re.search(r'\b(?:theorem|lemma)\s+(\S+)', text)
        if not match: continue
        if ':=' not in text: raise ValueError('proof body delimiter absent')
        head = text.split(':=',1)[0] + ':= '
        cases.append(dict(command_index=index, name=match.group(1), start=span['start'],stop=span['stop'],
                          prefix=data[:span['start']].decode(), original=text,
                          rejected=head+'by exact (0 : Nat)', incomplete=head+'by sorry'))
    return data, parsed, cases


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True); ap.add_argument('--spans',type=Path,required=True)
    ap.add_argument('--repl',required=True); ap.add_argument('--lean',default='/root/.elan/bin/lean')
    ap.add_argument('--env-json',type=Path,required=True); ap.add_argument('--cores',default='0')
    ap.add_argument('--repeat',type=int,default=3); ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--modes',default='repl_prefix,cold_lean,repl_fresh')
    args = ap.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    env = {**os.environ,**json.loads(args.env_json.read_text())}
    data, spans, cases = read_workload(args.source,args.spans)
    (args.out/'source.lean').write_bytes(data)
    (args.out/'command-spans.json').write_text(json.dumps(spans,indent=1)+'\n')
    (args.out/'cases.json').write_text(json.dumps(cases,indent=1)+'\n')
    metadata=dict(source=str(args.source),source_sha256=hashlib.sha256(data).hexdigest(),
                  settings={k:str(v) for k,v in vars(args).items()},environment=env['LEAN_PATH'],
                  repl_sha256=hashlib.sha256(Path(args.repl).read_bytes()).hexdigest(),cases=len(cases))
    (args.out/'metadata.json').write_text(json.dumps(metadata,indent=1)+'\n')
    runs=[]
    variants=['rejected','incomplete','original']
    for rep in range(args.repeat):
        modes=args.modes.split(',')
        if any(m not in ('cold_lean','repl_fresh','repl_prefix') for m in modes):
            ap.error('unknown mode')
        if rep%2: modes.reverse()
        for mode in modes:
            start=time.perf_counter(); records=[]; setup=[]
            repl = REPL(args,env) if mode=='repl_prefix' else None
            if mode=='repl_prefix':
                first=cases[0]
                response, elapsed=repl.call({'cmd':first['prefix']})
                if classify(response)!='accepted': raise RuntimeError('initial prefix failed')
                base=response['env']; previous_stop=first['start']
                setup.append(dict(kind='initial_prefix',response=response,seconds=elapsed))
            try:
                for case in cases:
                    if mode=='repl_fresh':
                        # REPL deliberately retains every returned environment.
                        # Bound lifetime to a theorem's candidate group instead
                        # of accumulating fresh imports for the entire corpus.
                        repl = REPL(args,env)
                    # Include between-proof commands/comments in each branch.
                    # REPL rejects a comment-only request as unexpected EOF;
                    # attaching the gap to the declaration also preserves all
                    # intermediate aliases/scopes without guessing lexical trivia.
                    gap=data[previous_stop:case['start']].decode() if mode=='repl_prefix' else ''
                    for variant in variants:
                        command=case[variant]
                        if mode=='cold_lean':
                            path=args.out/'Cold.lean'
                            path.write_text(case['prefix']+command+'\nend Nat\n')
                            t=time.perf_counter()
                            proc=subprocess.run(['taskset','-c',args.cores,args.lean,
                                '+leanprover/lean4:v4.34.1',str(path.resolve())],env=env,capture_output=True,text=True)
                            elapsed=time.perf_counter()-t
                            status='rejected' if proc.returncode else ('incomplete' if re.search(r"declaration uses [`']sorry[`']",proc.stdout+proc.stderr) else 'accepted')
                            if proc.returncode not in (0,1): raise RuntimeError('Lean crashed')
                            response=dict(returncode=proc.returncode,stdout=proc.stdout,stderr=proc.stderr)
                        else:
                            request={'cmd':case['prefix']+command} if mode=='repl_fresh' else {'cmd':gap+command,'env':base}
                            response,elapsed=repl.call(request); status=classify(response)
                        record=dict(name=case['name'],variant=variant,decision=status,seconds=elapsed,response=response)
                        if repl:
                            status_text=Path(f'/proc/{repl.proc.pid}/status').read_text()
                            match=re.search(r'^VmRSS:\s+(\d+)',status_text,re.M)
                            record['repl_rss_kib']=int(match.group(1)) if match else None
                        records.append(record)
                        with (args.out/'jobs.jsonl').open('a') as log:
                            log.write(json.dumps(dict(mode=mode,repeat=rep,**record))+'\n')
                        expected='accepted' if variant=='original' else variant
                        if status!=expected: raise RuntimeError(f"{mode} {case['name']} {variant}: {status} != {expected}")
                        if mode=='repl_prefix' and variant=='original': base=response['env']
                    previous_stop=case['stop']
                    if mode=='repl_fresh':
                        repl.close(); repl=None
            finally:
                if repl: repl.close()
            run=dict(mode=mode,repeat=rep,makespan_s=time.perf_counter()-start,records=records,setup=setup)
            runs.append(run)
            (args.out/'runs.json').write_text(json.dumps(runs,indent=1)+'\n')
            print(mode,rep,len(records),round(run['makespan_s'],3),flush=True)


if __name__=='__main__': main()
