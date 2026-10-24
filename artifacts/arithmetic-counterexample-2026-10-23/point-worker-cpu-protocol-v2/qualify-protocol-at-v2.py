"""Finite real-goal CPU-reference RPC check. Not GPU or Lean execution."""
from pathlib import Path
import json,os,signal,socket,subprocess,time
R=Path('/workspaces/repository');B=R/'bench/lean-counterexample';A=R/'artifacts/arithmetic-counterexample-2026-10-23'
os.sched_setaffinity(0,{8,9,10,11})
out=A/'point-worker-cpu-protocol-v2';out.mkdir(exist_ok=False)
for name in ['worker.py','point-provider.py','gpu_points.py','point_proposals.py']:(out/name).write_bytes((B/name).read_bytes())
entries=[json.loads(l)for l in(A/'first-witness-entries.jsonl').read_text().splitlines()]
control=json.loads((A/'point-evaluator-qualification-input.jsonl').read_text().splitlines()[0]);entries.append(control)
environment=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
command=['/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python','-u',str(B/'point-provider.py'),
 '--backend','cpu-reference','--port','0']
started=time.perf_counter();provider=subprocess.Popen(command,cwd=R,env=environment,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
worker=None;provider_log=[];worker_error=(out/'worker.stderr').open('w')
try:
 ready_line=provider.stdout.readline();provider_log.append(ready_line)
 ready=json.loads(ready_line);assert ready['event']=='ready'and ready['backend']=='cpu-reference'
 (out/'launch.json').write_text(json.dumps(dict(provider_pid=provider.pid,command=command,ready=ready),indent=2)+'\n')
 env=dict(environment,GPU_SMT_CEX_GPU_HOST='127.0.0.1',GPU_SMT_CEX_GPU_PORT=str(ready['port']),
  GPU_SMT_CEX_LOG=str(out/'worker-calls.jsonl'))
 worker=subprocess.Popen(['/usr/bin/python3','-u',str(B/'worker.py')],cwd=R,env=env,
  stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=worker_error,text=True)
 answers=[]
 for entry in entries:
  q=dict(entry,mode='gpu');worker.stdin.write(json.dumps(q)+'\n');worker.stdin.flush()
  result=json.loads(worker.stdout.readline());answers.append(dict(source_id=q['source_id'],entry_ns=q['entry_ns'],**result))
 (out/'answers.json').write_text(json.dumps(answers,indent=2)+'\n')
 worker.stdin.close();worker_exit=worker.wait();assert worker_exit==0
 with socket.create_connection(('127.0.0.1',ready['port']))as connection:
  connection.sendall(b'{"memory":true}\n')
  with connection.makefile('r')as f:memory=json.loads(f.readline())
 import sys
 sys.path.insert(0,str(B))
 from worker import provider_memory_sampler
 sampler=provider_memory_sampler('127.0.0.1',ready['port'],'cpu-reference')
 checked_memory=sampler()
 assert checked_memory['root_pid']==provider.pid and sampler()['root_start_ticks']==checked_memory['root_start_ticks']
 assert [x['exact_counterexample']for x in answers]==[True,True,False]
 assert all(x['provider_backend']=='cpu-reference'for x in answers)
 provider.send_signal(signal.SIGTERM);provider_log.append(provider.stdout.read());provider_exit=provider.wait()
 assert provider_exit==0
 # Actual closed-endpoint failure must produce ordinary native fallback.
 failed=subprocess.run(['/usr/bin/python3','-u',str(B/'worker.py')],cwd=R,
  env=dict(env,GPU_SMT_CEX_LOG=str(out/'closed-endpoint-calls.jsonl')),
  input=json.dumps(dict(entries[0],mode='gpu'))+'\n',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (out/'closed-endpoint-response.json').write_text(failed.stdout)
 fallback=json.loads(failed.stdout)
 assert failed.returncode==0 and not fallback['exact_counterexample']and'fallback_error'in fallback
 summary=dict(scope='CPU reference provider + actual worker sockets on retained goals; no GPU or Lean execution. Root self-review.',
  returned=len(answers),exact_witnesses=2,valid_goal_control_not_refuted=True,
  provider_exit=provider_exit,worker_exit=worker_exit,closed_endpoint_native_fallback=True,
  provider_memory=memory,owned_provider_sampler_qualified=True,whole_qualification_seconds=time.perf_counter()-started,
  owned_child_pids=[provider.pid,worker.pid],owned_children_reaped=True)
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
finally:
 if worker is not None and worker.poll()is None:worker.kill();worker.wait()
 if provider.poll()is None:provider.kill();provider.wait()
 worker_error.close();(out/'provider.log').write_text(''.join(provider_log))
