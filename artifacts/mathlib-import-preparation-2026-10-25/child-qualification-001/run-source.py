"""Native Mathlib prepared-child development qualification (not throughput).

Root-owned sequential fresh comparisons and two simultaneous isolated children.
Uses psutil in the existing Workspace environment. The retained full acquisition
is observed by identity but never signalled or reconfigured.
"""
import argparse, concurrent.futures, gzip, json, os, resource, signal, socket
import subprocess, tempfile, threading, time
from pathlib import Path
import psutil

def classify(v):
    if v.get('error')or v.get('message')or any(
        m.get('severity')=='error'for m in v.get('messages',[])):
        return 'rejected'
    if v.get('sorries')or any("declaration uses 'sorry'"in m.get('data','')
                           for m in v.get('messages',[])):
        return 'incomplete'
    return 'accepted'if isinstance(v.get('env'),int)else'backend_error'

def main():
    a=argparse.ArgumentParser(description=__doc__)
    for n in ['sdk','project','host','repl','out']:a.add_argument('--'+n,type=Path,required=True)
    a.add_argument('--existing-owner',type=int,required=True)
    a.add_argument('--existing-birth',type=float,required=True)
    args=a.parse_args();args.out.mkdir(exist_ok=False)
    os.sched_setaffinity(0,{10,11})
    assert resource.getrlimit(resource.RLIMIT_AS)[0]==resource.RLIM_INFINITY
    old=psutil.Process(args.existing_owner)
    assert abs(old.create_time()-args.existing_birth)<.01
    reference=next(q for q in old.children(recursive=True)if q.name()=='repl')
    env=dict(os.environ,PATH=str(args.sdk/'bin')+os.pathsep+os.environ['PATH'],
             LEAN_SYSROOT=str(args.sdk))
    context=reference.environ()
    for key in ['LEAN_PATH','LEAN_SRC_PATH']:
        if key in context:env[key]=context[key]
    fixtures=[
        ('arithmetic','example (n : Nat) : n + 0 = n := by omega','accepted'),
        ('ring','example (x y : Int) : (x+y)^2 = x^2+2*x*y+y^2 := by ring','accepted'),
        ('failed','example : (1 : Nat) = 2 := by rfl','rejected'),
        ('admitted','example : False := by sorry','incomplete'),
        ('private-definition','def gpuSmtPrivateChild : Nat := 7\nexample : gpuSmtPrivateChild = 7 := by rfl','accepted'),
        ('no-sibling-leak','#check gpuSmtPrivateChild','rejected')]
    header='import Mathlib\n\n'
    rows=[dict(id=i,code=header+c+'\n',expected=s)for i,c,s in fixtures]
    (args.out/'inputs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    root=psutil.Process();stop=threading.Event();samples=[];pressure=[];errors=[]
    parent=None;parent_identity=None;start=time.monotonic()
    def watch():
        while not stop.is_set():
            try:
                owned={};new=[]
                for owner in [root,old]:
                    try:
                        for q in [owner]+owner.children(recursive=True):
                            try:
                                owned[(q.pid,q.create_time())]=q.memory_info().rss
                                if owner==root and q.pid!=root.pid:new.append(q)
                            except psutil.NoSuchProcess:pass
                    except psutil.NoSuchProcess:pass
                total=sum(owned.values())
                samples.append(dict(seconds=time.monotonic()-start,rss_bytes=total,
                    processes=[dict(pid=k[0],birth=k[1],rss_bytes=v)for k,v in owned.items()]))
                if total>48*1024**3:
                    candidates=[q for q in new if parent is None or q.pid!=parent.pid]
                    if not candidates:candidates=new
                    if candidates:
                        victim=max(candidates,key=lambda q:q.memory_info().rss)
                        identity=(victim.pid,victim.create_time())
                        pressure.append(dict(pid=identity[0],birth=identity[1],rss_bytes=total))
                        if psutil.Process(identity[0]).create_time()==identity[1]:
                            os.killpg(victim.pid,signal.SIGKILL)
                    return
            except BaseException as e:
                errors.append(repr(e));return
            stop.wait(1)
    thread=threading.Thread(target=watch,daemon=True)
    directory=Path(tempfile.mkdtemp(prefix='smt-cow-qual-',dir='/tmp'));channel=directory/'s'
    results=[];receipt=dict(sdk=str(args.sdk),project=str(args.project),
        host=str(args.host),repl=str(args.repl),context_reference=dict(
        pid=reference.pid,birth=reference.create_time()),
        resource_contract=dict(aggregate_rss_bytes=48*1024**3,AS_limit=None,
        cpu=[10,11],sample_seconds=1),development_controls_only=True,
        full_population_executions=0,performance_claim=False)
    def branch(row,cpu):
        begin=time.monotonic()
        with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)as s:
            s.connect(str(channel))
            f=s.makefile('rwb')
            started=json.loads(f.readline())
            identity=psutil.Process(started['started'])
            birth=identity.create_time()
            f.write((str(cpu)+'\n'+json.dumps(row['code'])+'\n').encode());f.flush()
            native=json.loads(f.readline())
            retired=json.loads(f.readline())
            f.close()
        status=classify(native.get('native',{}))
        item=dict(id=row['id'],kind='prepared',status=status,expected=row['expected'],
            started=started,birth=birth,retired=retired,
            absent_after_retirement=not psutil.pid_exists(started['started']),
            seconds=time.monotonic()-begin,response=native)
        (args.out/(row['id']+'-prepared.json')).write_text(json.dumps(item,indent=2)+'\n')
        return item
    try:
        with(args.out/'parent-stderr.log').open('wb')as err:
            parent=subprocess.Popen([str(args.host),str(channel),str(args.sdk)],
                cwd=args.project,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                stderr=err,text=True,start_new_session=True)
            parent_identity=psutil.Process(parent.pid).create_time()
            thread.start()
            parent.stdin.write(json.dumps(header)+'\n');parent.stdin.flush()
            ready=json.loads(parent.stdout.readline());receipt['ready']=ready
            assert ready['prepared_context']['header_errors']is False
            assert ready['prepared_context']['imported_modules']>0
            assert ready['parent_threads']==1
            for row in rows:
                begin=time.monotonic()
                cmd=[str(args.repl)]
                fresh=subprocess.run(cmd,cwd=args.project,env=env,input=
                    json.dumps(dict(cmd=row['code']))+'\n\n',text=True,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
                (args.out/(row['id']+'-fresh.stdout')).write_text(fresh.stdout)
                (args.out/(row['id']+'-fresh.stderr')).write_text(fresh.stderr)
                value=json.loads(fresh.stdout)
                results.append(dict(id=row['id'],kind='fresh',status=classify(value),
                    expected=row['expected'],exit=fresh.returncode,command=cmd,
                    seconds=time.monotonic()-begin,response=value))
                results.append(branch(row,11))
                print(json.dumps({k:v for k,v in results[-1].items()if k!='response'}),flush=True)
                if pressure or errors:raise RuntimeError('development qualification interrupted')
            # Both connections are established before either proof is submitted.
            sockets=[socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)for _ in range(2)]
            files=[];starts=[]
            for s in sockets:
                s.connect(str(channel));f=s.makefile('rwb');files.append(f)
                starts.append(json.loads(f.readline()))
            receipt['simultaneous_children']=starts
            assert len(psutil.Process(parent.pid).children())==2
            for f,row,cpu in zip(files,rows[:2],[10,11]):
                f.write((str(cpu)+'\n'+json.dumps(row['code'])+'\n').encode());f.flush()
            concurrent=[]
            for f,s,identity,row in zip(files,sockets,starts,rows[:2]):
                native=json.loads(f.readline());done=json.loads(f.readline())
                f.close();s.close()
                concurrent.append(dict(id=row['id'],started=identity,native=native,
                    retired=done,absent=not psutil.pid_exists(identity['started'])))
            receipt['concurrent_results']=concurrent
            parent.stdin.close();receipt['parent_exit']=parent.wait()
            receipt['parent_absent']=not psutil.pid_exists(parent.pid)
    finally:
        if parent and parent.poll()is None:
            os.killpg(parent.pid,signal.SIGTERM);parent.wait()
        stop.set()
        if thread.ident:thread.join()
        if channel.exists():channel.unlink()
        directory.rmdir()
        receipt.update(seconds=time.monotonic()-start,results=results,
            mismatches=[x['id']+'-'+x['kind']for x in results if x['status']!=x['expected']],
            peak_combined_rss_bytes=max((x['rss_bytes']for x in samples),default=0),
            pressure=pressure,monitor_errors=errors)
        (args.out/'terminal.json').write_text(json.dumps(receipt,indent=2)+'\n')
        (args.out/'memory.jsonl.gz').write_bytes(gzip.compress(
            ''.join(json.dumps(x)+'\n'for x in samples).encode(),mtime=0))
        (args.out/'run-source.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps({k:v for k,v in receipt.items()if k not in ['results','concurrent_results']}),flush=True)

if __name__=='__main__':main()
