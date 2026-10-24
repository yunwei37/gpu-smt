"""Finite benchmark point provider; no persistent Service or model Agent."""
from pathlib import Path
import argparse,contextlib,json,os,queue,signal,socketserver,threading,time
from gpu_points import pack,reference_masks,exact_results,Device

def owned_memory():
 root=os.getpid();entries={}
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:
   s=(p/'stat').read_text();tail=s[s.rfind(')')+2:].split()
   entries[int(p.name)]=dict(pid=int(p.name),ppid=int(tail[1]),start_ticks=int(tail[19]),
    rss_bytes=int(tail[21])*os.sysconf('SC_PAGE_SIZE'))
  except FileNotFoundError:pass
 keep={root}
 while True:
  more={pid for pid,x in entries.items()if x['ppid']in keep}
  if more<=keep:break
  keep|=more
 selected=[x for pid,x in entries.items()if pid in keep]
 return dict(ready=True,root_pid=root,root_start_ticks=entries[root]['start_ticks'],
  rss_bytes=sum(x['rss_bytes']for x in selected),processes=selected,
  time_ns=time.monotonic_ns(),affinity=sorted(os.sched_getaffinity(0)))

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--ptx',type=Path);p.add_argument('--port',type=int,default=5001)
 p.add_argument('--backend',choices=['device','cpu-reference'],default='device')
 p.add_argument('--affinity',type=int,nargs='+',default=[8,9,10,11])
 args=p.parse_args();os.sched_setaffinity(0,set(args.affinity))
 if args.backend=='device'and not args.ptx:p.error('device backend requires PTX')
 pending=queue.Queue();stopping=threading.Event();log_lock=threading.Lock();registration_lock=threading.Lock()
 def log(item):
  with log_lock:print(json.dumps(item,separators=(',',':')),flush=True)
 class Handler(socketserver.StreamRequestHandler):
  def handle(self):
   try:
    request=json.loads(self.rfile.readline())
    if request.get('memory'):reply=owned_memory()
    elif request.get('ping'):reply=dict(ready=True,backend=args.backend,pid=os.getpid())
    else:
     entry=request['screen']
     ticket=dict(entry=entry,received_ns=time.monotonic_ns(),done=queue.Queue())
     with registration_lock:
      if stopping.is_set():raise RuntimeError('provider stopping')
      pending.put(ticket)
     reply=ticket['done'].get()
    self.wfile.write((json.dumps(reply,separators=(',',':'))+'\n').encode());self.wfile.flush()
   except (BrokenPipeError,ConnectionResetError):pass
   except Exception as ex:
    try:self.wfile.write((json.dumps(dict(error=repr(ex)))+'\n').encode());self.wfile.flush()
    except OSError:pass
 class Server(socketserver.ThreadingTCPServer):
  allow_reuse_address=True;daemon_threads=False
 def stop(*_):stopping.set()
 signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
 manager=Device(args.ptx)if args.backend=='device'else contextlib.nullcontext(None)
 with manager as device:
  server=Server(('0.0.0.0',args.port),Handler)
  thread=threading.Thread(target=server.serve_forever,daemon=False);thread.start()
  log(dict(event='ready',backend=args.backend,pid=os.getpid(),port=server.server_address[1],
   device=device.name if device else None,owned_memory=owned_memory()))
  try:
   while not stopping.is_set():
    try:first=pending.get(timeout=.1)
    except queue.Empty:continue
    tickets=[first]
    while True:
     try:tickets.append(pending.get_nowait())
     except queue.Empty:break
    entries=[t['entry']for t in tickets];began=time.monotonic_ns()
    try:
     batch=pack(entries);packed=time.monotonic_ns()
     if device:timing=device.evaluate(batch);masks=batch['hits']
     else:timing=dict(backend='CPU_REFERENCE_NOT_GPU');masks=reference_masks(batch)
     evaluated=time.monotonic_ns()
     verified=exact_results(batch,masks);checked=time.monotonic_ns()
     for ticket,result in zip(tickets,verified):
      ticket['done'].put(dict(source_id=result['source_id'],entry_ns=result['entry_ns'],
       candidate_point=result['witness']['point']if result['witness']else None,
       point_index=result['witness']['point_index']if result['witness']else None,
       backend=args.backend,timing=dict(queue_ns=began-ticket['received_ns'],
        shared_batch_pack_ns=packed-began,shared_batch_exact_check_ns=checked-evaluated,
        batch_size=len(tickets),**timing)))
     log(dict(event='batch_retired',backend=args.backend,batch_size=len(tickets),
      entries=[dict(source_id=e['source_id'],entry_ns=e['entry_ns'])for e in entries],
      distinct_sources=len({e['source_id']for e in entries}),pack_ns=packed-began,
      exact_check_ns=checked-evaluated,whole_batch_ns=checked-began,device=timing))
    except Exception as ex:
     for ticket in tickets:
      e=ticket['entry'];ticket['done'].put(dict(source_id=e['source_id'],entry_ns=e['entry_ns'],
       backend=args.backend,error=repr(ex)))
     log(dict(event='batch_error',error=repr(ex),backend=args.backend))
  finally:
   with registration_lock:stopping.set()
   server.shutdown();thread.join()
   while True:
    try:
     ticket=pending.get_nowait();e=ticket['entry']
     ticket['done'].put(dict(source_id=e['source_id'],entry_ns=e['entry_ns'],
      backend=args.backend,error='provider stopped before dispatch'))
    except queue.Empty:break
   server.server_close()
  log(dict(event='provider_retired',backend=args.backend,owned_memory=owned_memory()))
if __name__=='__main__':main()
