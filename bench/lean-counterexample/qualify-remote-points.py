"""Qualify a remote point backend on real goals; never execute Lean proofs."""
from pathlib import Path
import argparse,importlib.util,json,os,signal,socket,time
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
 p.add_argument('--out',type=Path,required=True);p.add_argument('--port',type=int,default=5001);args=p.parse_args()
 os.sched_setaffinity(0,{8,9,10,11});args.out.mkdir(exist_ok=False)
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
  response=rpc(args.host,dict(screen_batch=entries),args.port);received=time.perf_counter()
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
 summary=dict(backend=args.backend,device=ping.get('device'),returned=len(checked),
  exact_witnesses=sum(x['exact_counterexample']for x in checked),
  missing_reference_witnesses=sum(x['reference_has_witness']and not x['exact_counterexample']for x in checked),
  additional_exact_witnesses=sum(x['exact_counterexample']and not x['reference_has_witness']for x in checked),
  invalid_returned_points=sum(x['invalid_returned_point']for x in checked),
  provider_errors=sum(bool(x['provider_error'])for x in checked),
  batch_rpc_seconds=received-started,whole_qualification_seconds=time.perf_counter()-started,
  initial_provider=initial,memory_watchdog=guard.summary(),
  scope='Offline actual-goal RPC batch. Device execution only when backend=device; no online candidate overlap or proof speedup.')
 (args.out/'checked.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n'for x in checked))
 (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
 assert not guard.error and not summary['invalid_returned_points']and not summary['provider_errors']
if __name__=='__main__':main()
