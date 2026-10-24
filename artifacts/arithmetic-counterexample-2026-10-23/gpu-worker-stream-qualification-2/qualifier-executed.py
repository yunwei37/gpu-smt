"""Qualify a remote point backend on real goals; never execute Lean proofs."""
from pathlib import Path
import argparse,concurrent.futures,copy,importlib.util,json,os,shutil,signal,socket,subprocess,time
from worker import Q,verify,provider_memory_sampler
R=Path('/workspaces/repository');A=R/'artifacts/arithmetic-counterexample-2026-10-23'
def rpc(host,request,port=5001):
 with socket.create_connection((host,port))as connection:
  with connection.makefile('rwb')as stream:
   stream.write((json.dumps(request,separators=(',',':'))+'\n').encode());stream.flush()
   return json.loads(stream.readline())
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--host',required=True);p.add_argument('--backend',choices=['device','cpu-reference'],required=True)
 p.add_argument('--out',type=Path,required=True);p.add_argument('--port',type=int,default=5001)
 p.add_argument('--worker-stream',action='store_true',help='Use two persistent actual worker subprocesses rather than one prepacked batch; no Lean proof run.')
 args=p.parse_args()
 os.sched_setaffinity(0,{8,9,10,11});args.out.mkdir(exist_ok=False)
 shutil.copy2(Path(__file__),args.out/'qualifier-executed.py')
 entries=[json.loads(line)for line in(A/'point-evaluator-qualification-input.jsonl').read_text().splitlines()]
 expected={(x['source_id'],x['entry_ns']):x['exact_counterexample']for x in map(json.loads,(A/'point-bytecode-cpu-qualification-v2/entries.jsonl').read_text().splitlines())}
 sampler=provider_memory_sampler(args.host,args.port,args.backend)
 initial=sampler();ping=rpc(args.host,{'ping':True},args.port)
 spec=importlib.util.spec_from_file_location('own_capture_memory',R/'bench/lean-native/linarith-oracle/memory_budget.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 guard=module.MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,'repl',args.out)
 launch=json.loads((A/'full-observe-start.json').read_text())
 if Path('/proc',str(launch['pid'])).exists():
  guard.include_owned_tree(launch['pid'],launch['start_ticks'],A/'full-observe/verification')
 guard.extra_memory=sampler;guard.on_error=lambda:os.kill(os.getpid(),signal.SIGTERM)
 guard.start();started=time.perf_counter()
 try:
  if args.worker_stream:
   source=args.out/'source';source.mkdir()
   worker=source/'worker.py';shutil.copy2(Path(__file__).with_name('worker.py'),worker)
   environment=dict(os.environ,GPU_SMT_CEX_GPU_HOST=args.host,GPU_SMT_CEX_GPU_PORT=str(args.port),
    GPU_SMT_CEX_LOG=str(args.out/'worker-goals.jsonl'))
   children=[subprocess.Popen(['/usr/bin/python3','-u',str(worker)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
    text=True,env=environment)for _ in range(2)]
   try:
    def sequence(lane):
     child=children[lane];answers=[]
     for index in range(lane,len(entries),2):
      entry=copy.deepcopy(entries[index]);entry['mode']='gpu'
      child.stdin.write(json.dumps(entry,separators=(',',':'))+'\n');child.stdin.flush()
      line=child.stdout.readline()
      if not line:raise RuntimeError('Online worker exited without a reply')
      answer=json.loads(line);witness=answer.get('witness')or{}
      answers.append((index,dict(source_id=entry['source_id'],entry_ns=entry['entry_ns'],
       candidate_point=witness.get('point'),point_index=witness.get('point_index'),
       backend=answer.get('provider_backend'),error=answer.get('fallback_error'),online_answer=answer)))
     return answers
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
     outputs=list(pool.map(sequence,range(2)))
    response=dict(backend=args.backend,results=[item for _,item in sorted(sum(outputs,[]))])
   finally:
    for child in children:
     if child.stdin:child.stdin.close()
    for child in children:
     if child.poll()is None:
      try:child.wait(timeout=5)
      except subprocess.TimeoutExpired:child.kill();child.wait()
    (args.out/'worker-exits.json').write_text(json.dumps([dict(pid=c.pid,exit=c.returncode)for c in children],indent=2)+'\n')
   if any(child.returncode!=0 for child in children):raise RuntimeError('Worker retirement failed')
  else:
   response=rpc(args.host,dict(screen_batch=entries),args.port)
  received=time.perf_counter()
  (args.out/'response.json').write_text(json.dumps(response,indent=2)+'\n')
  if response.get('backend')!=args.backend:raise RuntimeError('Wrong returned backend')
  ping=rpc(args.host,{'ping':True},args.port)
  if args.backend=='device'and'RTX 5090'not in(ping.get('device')or''):raise RuntimeError('Actual device initialization failed')
  results=response['results']
  if len(results)!=len(entries):raise RuntimeError('Missing point responses')
  seen=set();checked=[]
  for entry,result in zip(entries,results):
   key=(entry['source_id'],entry['entry_ns'])
   if key in seen or(result.get('source_id'),result.get('entry_ns'))!=key:raise RuntimeError('Source/entry mismatch')
   seen.add(key);point=result.get('candidate_point');exact=False
   if point is not None:exact=verify(entry['payload']['ast'],[Q(int(n),int(d))for n,d in point])
   checked.append(dict(source_id=key[0],entry_ns=key[1],candidate_received=point is not None,
    exact_counterexample=exact,invalid_returned_point=point is not None and not exact,
    reference_has_witness=expected[key],provider_error=result.get('error')))
 finally:guard.stop()
 summary=dict(backend=args.backend,device=ping.get('device'),worker_stream=args.worker_stream,returned=len(checked),
  cpu_closed_entries=sum(x.get('online_answer',{}).get('evaluation_backend')=='cpu_closed'for x in results),
  exact_witnesses=sum(x['exact_counterexample']for x in checked),
  missing_reference_witnesses=sum(x['reference_has_witness']and not x['exact_counterexample']for x in checked),
  additional_exact_witnesses=sum(x['exact_counterexample']and not x['reference_has_witness']for x in checked),
  invalid_returned_points=sum(x['invalid_returned_point']for x in checked),
  provider_errors=sum(bool(x['provider_error'])for x in checked),
  batch_rpc_seconds=received-started,whole_qualification_seconds=time.perf_counter()-started,
  initial_provider=initial,memory_watchdog=guard.summary(),
  scope=('Actual retained goals through two persistent native-facing worker streams; no Lean proof candidate run or speedup.'if args.worker_stream else'Offline actual-goal RPC batch. Device execution only when backend=device; no online candidate overlap or proof speedup.'))
 (args.out/'checked.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n'for x in checked))
 (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
 assert not guard.error and not summary['invalid_returned_points']and not summary['provider_errors']
if __name__=='__main__':main()
