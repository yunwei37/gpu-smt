"""Whole native prefix execution vs native warm in-process command batches.
SHRED exact-edge accounting is compared with native unit-text keys (trivia ablation).
"""
from pathlib import Path
import argparse, collections, dataclasses, gzip, importlib.util, json, os, re, resource
import subprocess, sys, time
R=Path('/workspaces/repository')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix')
A=R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity'
SDK=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
MATH=SDK.parent/'mathlib4'
NATIVE=Path('/tmp/gpu-smt-native-mathlib-20261014')
UPSTREAM=Path('/tmp/gpu-smt-primary-opportunities-20261017/shred')
def load_client():
    p=UPSTREAM/'src/lean_prefix/repl.py'
    spec=importlib.util.spec_from_file_location('shred_native_repl',p)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    return module
def classify(x):
    if not isinstance(x,dict) or x.get('message') or x.get('error'):return 'operational'
    if any(m.get('severity')=='error' for m in x.get('messages',[])):return 'rejected'
    if x.get('sorries') or any('sorry' in m.get('data','') for m in x.get('messages',[]) if m.get('severity')=='warning'):return 'incomplete'
    return 'complete'
def blank_header(x):
    h=x['header']
    if not x['code'].startswith(h):return None
    return ''.join(c if c in '\r\n' else ' ' for c in h)+x['code'][len(h):]
def rusage():
    return [resource.getrusage(x) for x in [resource.RUSAGE_SELF,resource.RUSAGE_CHILDREN]]
def capture(ds,method,limit,out,start_index=0):
    started=time.monotonic_ns();ru0=rusage()
    out.mkdir(parents=True,exist_ok=False)
    with gzip.open(A/(ds+'-input.jsonl.gz'),'rt') as f:items=[json.loads(l) for l in f]
    if start_index:items=items[start_index:]
    if limit:items=items[:limit]
    log=gzip.open(out/'requests-responses.jsonl.gz','wt',compresslevel=1)
    rows=gzip.open(out/'results.jsonl.gz','wt',compresslevel=1)
    mapped={};extract_seconds=0.0
    if method!='batch':
        requests=[]
        for x in items:
            m=re.search(r':=\s*by\b',x['code'])
            if m:
                mapped[x['index']]={'statement':x['code'][:m.end()],'proof':x['code'][m.end():]}
                requests.append(json.dumps({'proposalId':str(x['index']),'proof':mapped[x['index']]['proof']},ensure_ascii=False))
        t=time.monotonic()
        parser=subprocess.run(['lake','env','lean','--run',str(UPSTREAM/'lean/LeanPrefix/Extract.lean')],
          cwd=MATH,input='\n'.join(requests)+'\n',capture_output=True,text=True,check=True)
        extract_seconds=time.monotonic()-t
        (out/'extract.stderr').write_text(parser.stderr)
        with gzip.open(out/'native-parser.jsonl.gz','wt') as f:f.write(parser.stdout)
        for line in parser.stdout.splitlines():
            ans=json.loads(line);i=int(ans['proposalId'])
            mapped[i].update(ans)
    module=load_client()
    client=module.LeanRepl(MATH,executable=U/'repl-kernel/.lake/build/bin/repl',
      timeout_seconds=300,memory_limit_bytes=None)
    headers={};counts=collections.Counter();fallbacks=0;hits=0;nodes=0;forced_retirements=0
    def request(data):
        nonlocal forced_retirements
        if client._process is None:client.start()
        t=time.monotonic_ns()
        log.write(json.dumps({'event':'request','request':data,'start_ns':t},ensure_ascii=False)+'\n');log.flush()
        try:
            res=client.request(data)
        except module.ReplError as error:
            stderr=getattr(error,'stderr','')
            if not stderr and client._stderr is not None:
                stderr=os.pread(client._stderr.fileno(),os.fstat(client._stderr.fileno()).st_size,0).decode(errors='replace')
            log.write(json.dumps({'event':'request_failure','request':data,'wall_ns':time.monotonic_ns()-t,
               'error':str(error),'kind':type(error).__name__,'stderr':stderr},ensure_ascii=False)+'\n');log.flush()
            client.close();headers.clear();forced_retirements+=1
            raise
        log.write(json.dumps({'event':'response','request':data,'wall_ns':time.monotonic_ns()-t,
           'native_wall_seconds':res.wall_seconds,'native_cpu_seconds':res.cpu_seconds,
           'response':res.response,'stderr':res.stderr},ensure_ascii=False)+'\n');log.flush()
        return res.response
    def env_for(h):
        if h not in headers:
            ans=request({'cmd':h,'allTactics':False,'ast':False,'tactics':False,'premises':False})
            if classify(ans)!='complete' or not isinstance(ans.get('env'),int):raise RuntimeError('header preparation failed')
            headers[h]=ans['env']
        return headers[h]
    def independent(xs):
        answers={}
        byheader=collections.defaultdict(list)
        for x in xs:byheader[x['header']].append(x)
        for h,group in byheader.items():
            for start in range(0,len(group),4):
                chunk=group[start:start+4]
                if any(blank_header(x) is None for x in chunk):
                    for x in chunk:
                        try:answers[x['index']]=request({'cmd':x['code'],'allTactics':False,'ast':False,'tactics':False,'premises':False})
                        except module.ReplError as error:
                            answers[x['index']]={'message':str(error),'transport_failure':type(error).__name__}
                else:
                    try:
                        env=env_for(h)
                        ans=request({'env':env,'cmds':[blank_header(x) for x in chunk],
                           'allTactics':False,'ast':False,'tactics':False,'premises':False})
                        values=ans.get('results')
                        if not isinstance(values,list) or len(values)!=len(chunk):raise RuntimeError('native batch frame failed')
                        answers.update((x['index'],v) for x,v in zip(chunk,values))
                    except module.ReplError as error:
                        answers.update((x['index'],{'message':str(error),'transport_failure':type(error).__name__}) for x in chunk)
        return answers
    try:
        client.start()
        for start in range(0,len(items),32):
            group=items[start:start+32]
            answers={};cache={};roots={};plans={};needs=[]
            try:
                if method=='batch':answers=independent(group)
                else:
                    for x in group:
                        i=x['index'];info=mapped.get(i);h=x['header']
                        if not info or not info.get('eligible') or '```' in info['proof'] or not info['statement'].startswith(h):
                            needs.append(x);continue
                        statement=info['statement'];rootkey=(h,statement)
                        if rootkey not in roots:
                            body=''.join(c if c in '\r\n' else ' ' for c in h)+statement[len(h):]+'\n  sorry'
                            ans=request({'cmd':body,'env':env_for(h),'allTactics':False,'ast':False,'tactics':False,'premises':False})
                            sorries=ans.get('sorries',[])
                            roots[rootkey]=sorries[0].get('proofState') if len(sorries)==1 and not any(m.get('severity')=='error' for m in ans.get('messages',[])) else None
                        state=roots[rootkey]
                        if not isinstance(state,int):needs.append(x);continue
                        previous=0;edges=[];source=info['proof'].split('```',1)[0].encode()
                        for unit in info['units']:
                            stop=unit['stopByte']
                            edge=source[previous:stop].decode() if method=='exact' else unit['text']
                            edges.append(edge);previous=stop
                        plans[i]={'item':x,'root':rootkey,'state':state,'edges':edges,'bad':False,'last':None}
                    for depth in range(max((len(x['edges']) for x in plans.values()),default=0)):
                        pending={}
                        for i,p in plans.items():
                            if p['bad'] or depth>=len(p['edges']):continue
                            key=(p['root'],tuple(p['edges'][:depth+1]))
                            if key in cache or key in pending:hits+=1
                            if key not in cache:pending.setdefault(key,{'proofState':p['state'],'tactic':p['edges'][depth]})
                        work=list(pending.items())
                        for offset in range(0,len(work),4):
                            chunk=work[offset:offset+4]
                            result=request({'proofSteps':[v for _,v in chunk]})
                            result=result.get('results')
                            if not isinstance(result,list) or len(result)!=len(chunk):raise RuntimeError('native proof batch failed')
                            for (key,_),v in zip(chunk,result):cache[key]=v;nodes+=1
                        for p in plans.values():
                            if p['bad'] or depth>=len(p['edges']):continue
                            key=(p['root'],tuple(p['edges'][:depth+1]));ans=cache[key];p['last']=ans
                            if classify(ans)!='complete' or not isinstance(ans.get('proofState'),int):p['bad']=True
                            else:p['state']=ans['proofState']
                    for i,p in plans.items():
                        last=p['last']
                        if p['bad'] or not last or last.get('goals') or last.get('kernelChecked') is not True:
                            needs.append(p['item'])
                        else:answers[i]=last
                    fallbacks+=len(needs)
                    if needs:answers.update(independent(needs))
                    request({'clearProofSnapshots':True})
            except module.ReplError:
                # Any process replacement invalidates all saved proof-state ids
                # in this task group. Fall back all32 through unchanged commands.
                fallbacks+=len(group)
                answers=independent(group)
            for x in group:
                ans=answers[x['index']];status=classify(ans);counts[status]+=1
                rows.write(json.dumps({'index':x['index'],'outcome':status,'response':ans},ensure_ascii=False)+'\n')
            rows.flush()
    finally:
        normal_exit=False
        if client._process is not None and client._process.poll() is None:
            try:
                bye=request({'quit':True})
                code=client._process.wait(timeout=300)
                normal_exit=bye.get('bye') is True and code==0
            except module.ReplError:
                pass  # request already captured failure and retired the worker
            except subprocess.TimeoutExpired:
                client.close();forced_retirements+=1
        if client._stderr is not None:
            client._stderr.flush()
            (out/'repl.stderr').write_bytes(os.pread(client._stderr.fileno(),os.fstat(client._stderr.fileno()).st_size,0))
        client.close();log.close();rows.close()
        ru1=rusage()
        cpu=sum((b.ru_utime+b.ru_stime)-(a.ru_utime+a.ru_stime) for a,b in zip(ru0,ru1))
        result={'state':'complete' if sum(counts.values())==len(items) else 'failed','dataset':ds,'method':method,'expected':len(items),'returned':sum(counts.values()),'counts':dict(counts),
           'whole_seconds':(time.monotonic_ns()-started)/1e9,'cpu_seconds':cpu,'normal_native_exit':normal_exit,'forced_native_retirements':forced_retirements,'cpu_accounting_complete':forced_retirements==0,
           'native_parse_seconds':extract_seconds,'fallbacks':fallbacks,'executed_prefix_nodes':nodes,'cached_lookups':hits,
           'affinity':sorted(os.sched_getaffinity(0)),
           'scope':'offline native batch width4 versus native prefix waves width4; all parse/preparation/IPC/kernel/fallback/cleanup included; source verdict comparison pending'}
        (out/'terminal.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result),flush=True)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--dataset',choices=['minif2f','proofnet'],required=True)
    p.add_argument('--methods',nargs='+',choices=['batch','exact','unit'],default=['batch','exact','unit'])
    p.add_argument('--limit',type=int,default=0)
    p.add_argument('--start',type=int,default=0,help='source-order slice for real failure qualification')
    a=p.parse_args()
    os.sched_setaffinity(0,{20,21,22,23});resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    os.environ['PATH']=str(SDK/'bin')+':'+os.environ['PATH']
    os.environ['LEAN_SERVER_NATIVE_DYNLIB']=str(NATIVE/'.lake/build/lib/libMathlib-Tactic-Linarith-1.so')
    os.environ['LD_LIBRARY_PATH']=':'.join([str(NATIVE/'.lake/build/lib')]+[str(x/'.lake/build/lib') for x in (NATIVE/'.lake/packages').iterdir() if x.is_dir()])
    for method in a.methods:capture(a.dataset,method,a.limit,a.out/method,a.start)
if __name__=='__main__':main()
