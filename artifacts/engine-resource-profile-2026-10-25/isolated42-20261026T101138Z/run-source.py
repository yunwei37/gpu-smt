from pathlib import Path
import os,json,datetime,time,subprocess,resource
tmp=Path('/tmp/gpu-smt-isolated42-20261026')
ctx=json.loads((tmp/'context.json').read_text());out=Path(ctx['out'])
repo=Path('/workspaces/repository');m=ctx['previous_manifest']
os.sched_setaffinity(0,{8,9,10,11})
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def birth(pid):return int((Path('/proc')/str(pid)/'stat').read_text().rsplit(')',1)[1].split()[19])
assert resource.getrlimit(resource.RLIMIT_AS)==(-1,-1)
for proc in Path('/proc').iterdir():
 if not proc.name.isdigit():continue
 try:
  first=(proc/'cmdline').read_bytes().split(b'\0')[0].decode(errors='replace')
  assert first not in [m['repl'],m['prepared_host']],('Old native owner still running',proc.name)
 except OSError:pass
assert __import__('shutil').disk_usage('/workspaces').free>0
env=dict(os.environ,PATH='/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup',CARGO_TARGET_DIR='/tmp/gpu-smt-rust-engine-build-20261025/target')
build=['/usr/local/cargo/bin/cargo','build','--locked','-p','gpu-smt-server','--bin','gpu-smt']
with (out/'build.log').open('wb')as f:
 code=subprocess.call(build,cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT)
(out/'build.json').write_text(json.dumps({'UTC':now(),'command':build,'exit_code':code,'source':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()},indent=2)+'\n')
if code:raise SystemExit(code)
env.update(LEAN_PATH=m['LEAN_PATH'],LEAN_SYSROOT=m['LEAN_SYSROOT'])
env['PATH']=str(Path(m['sysroot'])/'bin')+os.pathsep+env['PATH']
cli='/tmp/gpu-smt-rust-engine-build-20261025/target/debug/gpu-smt'
cmd=[cli,'check','--repl',m['repl'],'--project',m['project'],'--environment','lean4.9-original42-exclusive48GiB-4core-20261026','--cpus','8,9,10,11','--worker-cores','4','--memory-gib','48']
start=time.monotonic()
with (tmp/'requests.jsonl').open('rb')as source,(out/'results.jsonl').open('wb')as result,(out/'resource-events.jsonl').open('wb')as events:
 p=subprocess.Popen(cmd,cwd=m['project'],env=env,stdin=source,stdout=result,stderr=events,start_new_session=True)
 launch={'UTC':now(),'controller_pid':os.getpid(),'controller_start_ticks':birth(os.getpid()),'pid':p.pid,'start_ticks':birth(p.pid),'command':cmd,'cwd':m['project'],'source':ctx['source'],'original_ids':ctx['expected_ids'],'resources':{'actual_aggregate_budget_bytes':48*1024**3,'cpu_ids':[8,9,10,11],'cores_per_worker':4,'fixed_AS_limit':False},'LEAN_PATH':m['LEAN_PATH'],'LEAN_SYSROOT':m['LEAN_SYSROOT'],'binary_size':Path(cli).stat().st_size,'binary_mtime':Path(cli).stat().st_mtime,'one_native_group':True,'workspace_free_bytes_at_launch':__import__('shutil').disk_usage('/workspaces').free}
 (out/'launch.json').write_text(json.dumps(launch,indent=2)+'\n')
 (tmp/'active.json').write_text(json.dumps(launch,indent=2)+'\n')
 code=p.wait()
terminal={'UTC':now(),'exit_code':code,'controller_seconds':time.monotonic()-start,'scope':'native CLI startup through all42consumer records and complete retirement;no post-run analysis or observer delay','stdout_bytes':(out/'results.jsonl').stat().st_size,'stderr_bytes':(out/'resource-events.jsonl').stat().st_size,'workspace_free_bytes':__import__('shutil').disk_usage('/workspaces').free}
(out/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
print(json.dumps(terminal),flush=True)
