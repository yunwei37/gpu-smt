from pathlib import Path
import concurrent.futures,json,subprocess,os,time,resource,signal,sys
b=Path('/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle')
out=b/'direct-feasibility-numeric';out.mkdir(exist_ok=False)
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{0,1,2,3})
py='/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python'
host=sys.argv[1];sock=out/'cuopt.sock'
sys.path.insert(0,str(b/'cuopt-grpc'))
import grpc
channel=grpc.insecure_channel(host+':5001')
grpc.channel_ready_future(channel).result();channel.close()
log=(out/'proxy.log').open('w')
proxy=subprocess.Popen([py,'/workspaces/repository/bench/lean-native/linarith-oracle/support-proxy.py','--backend','cuopt','--socket',str(sock),'--log',str(out/'support-calls.jsonl'),'--host',host,'--proto-root',str(b/'cuopt-grpc')],stdout=log,stderr=subprocess.STDOUT)
try:
 while not sock.exists():
  if proxy.poll()is not None:raise RuntimeError('proxy startup failed')
  time.sleep(.01)
 rows=json.loads((b/'qualification-inputs.json').read_text())
 def run(pair):
  i,x=pair;env=dict(os.environ);env['GPU_ARITHMETIC_SUPPORT_SOCKET']=str(sock);env['FARKAS_EXTERNAL_CPU_HYBRID']='1'
  start=time.monotonic_ns();cmd=b/('arithmetic-batchd'if x['kind']=='direct'else'farkas-batchd')
  child=subprocess.Popen([str(cmd)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env=env,start_new_session=True)
  timed_out=False
  try:stdout,stderr=child.communicate(json.dumps(x['request'])+'\n',timeout=300)
  except subprocess.TimeoutExpired:
   timed_out=True;os.killpg(child.pid,signal.SIGKILL);stdout,stderr=child.communicate()
  try:answer=json.loads(stdout)
  except Exception:answer=None
  record={'index':i,'kind':x['kind'],'seconds':(time.monotonic_ns()-start)/1e9,'answer':answer,'original_cert_nonnull':x['answer'].get('cert')is not None,'returncode':child.returncode,'resource_or_operational_timeout':timed_out,'stdout':stdout,'stderr':stderr}
  print(json.dumps({k:v for k,v in record.items()if k not in ['answer','stdout','stderr']}),flush=True)
  return record
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:results=list(pool.map(run,enumerate(rows)))
 (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print('QUALIFICATION_DONE',len(results),flush=True)
finally:
 proxy.terminate();proxy.wait();log.close()
