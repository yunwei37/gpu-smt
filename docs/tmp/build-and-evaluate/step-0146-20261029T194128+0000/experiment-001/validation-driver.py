import pathlib,subprocess,os,sys,time,json,signal,psutil,datetime
r=pathlib.Path('/workspaces/repository')
base=pathlib.Path('/workspaces/.agent-state/gpu-smt-rust-development')
step=pathlib.Path(pathlib.Path('/workspaces/.agent-state/gpu-smt-step0146-path.txt').read_text().strip())
toolchain=pathlib.Path('/usr/local/rustup/toolchains/1.98.1-x86_64-unknown-linux-gnu/bin')
env=os.environ.copy()
env.update(PATH=str(toolchain)+':'+env.get('PATH',''),
 CARGO_HOME=str(base/'cargo-home'),CARGO_TARGET_DIR=str(base/'target'),
 CARGO_BUILD_JOBS='1',CARGO_INCREMENTAL='0',CARGO_PROFILE_DEV_DEBUG='0',
 CARGO_PROFILE_TEST_DEBUG='0',RUST_TEST_THREADS='1',RUSTDOCFLAGS='-D warnings')
label=sys.argv[1];command=sys.argv[2:]
logpath=step/'experiment-001'/(label+'.log')
stat=os.statvfs('/workspaces');free_before=stat.f_bavail*stat.f_frsize
started=time.monotonic()
with logpath.open('w') as log:
 child=subprocess.Popen(['taskset','-c','6,7']+command,cwd=r,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 peak=0;abort=False
 while child.poll() is None:
  me=psutil.Process()
  processes=[me,psutil.Process(os.getppid())]+me.children(recursive=True)
  seen=set();total=0
  for p in processes:
   try:
    if p.pid not in seen:total+=p.memory_info().rss;seen.add(p.pid)
   except psutil.NoSuchProcess:pass
  peak=max(peak,total)
  if total>48<<30:
   abort=True;os.killpg(child.pid,signal.SIGKILL);break
  time.sleep(1)
 code=child.wait()
stat=os.statvfs('/workspaces')
record=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 command=command,exit_code=code,seconds=time.monotonic()-started,
 sampled_owned_rss_bytes=peak,budget_abort=abort,pvc_free_before=free_before,
 pvc_free_after=stat.f_bavail*stat.f_frsize,cpu_ids=[6,7],
 build_settings={k:env[k] for k in ['CARGO_HOME','CARGO_TARGET_DIR','CARGO_BUILD_JOBS','CARGO_INCREMENTAL','CARGO_PROFILE_DEV_DEBUG','CARGO_PROFILE_TEST_DEBUG','RUST_TEST_THREADS']},
 scope='G10 development validation,no native collection or performance point')
(step/'experiment-001'/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record));print(logpath.read_text()[-10000:])
sys.exit(code if code>=0 else 1)
