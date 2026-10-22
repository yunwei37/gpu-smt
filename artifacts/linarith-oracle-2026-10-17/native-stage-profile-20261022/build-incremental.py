from pathlib import Path
import os,sys,json,subprocess,resource,importlib.util,datetime
R=Path('/workspaces/repository');O=R/'artifacts/linarith-oracle-2026-10-17/native-stage-profile-20261022'
B=R/'bench/lean-native/linarith-oracle/reproduction'
F=R/'artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019'
original=json.loads((F/'executed-build.json').read_text())
attempt=int(sys.argv[1]) if len(sys.argv)>1 else 1
suffix='' if attempt==1 else '-v'+str(attempt)
out=Path('/tmp/gpu-smt-native-stage-profile-20261022'+suffix);out.mkdir(exist_ok=False)
(out/'lean').mkdir(exist_ok=True);(out/'c').mkdir(exist_ok=True)
os.sched_setaffinity(0,{8,9,10,11})
resource.setrlimit(resource.RLIMIT_AS,(24*1024**3,24*1024**3))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
spec=importlib.util.spec_from_file_location('budget',R/'bench/lean-native/linarith-oracle/memory_budget.py')
budget=importlib.util.module_from_spec(spec);spec.loader.exec_module(budget)
repl=Path('/tmp/gpu-smt-goedel427-20261014/repl-kimina-native-gc-header-repair/.lake/build/bin/repl')
(O/('build'+suffix)).mkdir(exist_ok=False)
guard=budget.MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,repl,O/('build'+suffix))
def stop():
    for proc in guard.owned():
        if proc.pid!=os.getpid():
            try:proc.kill()
            except Exception:pass
guard.on_error=stop
guard.start()
env=dict(os.environ)
env.update(LEAN_PATH=str(out/'lean')+os.pathsep+original['lean_path'],
           LEAN_SRC_PATH=str(B/'lean')+os.pathsep+original['lean_src_path'])
commands=[];custom=[];objects=[]
def run(argv):
    z=subprocess.run(list(map(str,argv)),env=env,cwd=original['mathlib'],capture_output=True,text=True)
    row=dict(argv=list(map(str,argv)),returncode=z.returncode,output=z.stdout+z.stderr)
    commands.append(row)
    (O/('build-commands'+suffix+'.json')).write_text(json.dumps(commands,indent=2)+'\n')
    print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':len(commands),'returncode':z.returncode,'name':Path(str(argv[-1])).name}),flush=True)
    if guard.error:raise RuntimeError(guard.error)
    if z.returncode:raise RuntimeError((z.stdout+z.stderr)[-5000:])
try:
    for entry in original['commands']:
        argv=entry['argv']
        if '-o' in argv and '-c' in argv and argv[-1].endswith('.lean') and str(B/'lean') in argv[-1]:
            name=Path(argv[argv.index('-c')+1]).stem
            src=Path(argv[-1])
            ol=out/'lean'/src.relative_to(B/'lean').with_suffix('.olean');ol.parent.mkdir(parents=True,exist_ok=True)
            c=out/'c'/(name+'.c')
            run([Path(original['sdk'])/'bin/lean','--root='+str(B/'lean'),'-o',ol,'-c',c,src]);custom.append(c)
    for c in sorted((B/'c').glob('*.c')):
        obj=out/'c'/(c.stem+'.o')
        run(['/usr/bin/cc','-O3','-fPIC','-I'+str(Path(original['sdk'])/'include'),'-c',c,'-o',obj]);objects.append(obj)
    plugin=out/'batch-oracle.so'
    run([Path(original['sdk'])/'bin/leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*custom,*objects,'-lz','-o',plugin])
    build=dict(original,lean_path=env['LEAN_PATH'],lean_src_path=env['LEAN_SRC_PATH'],
               libraries=original['libraries'][:-1]+[str(plugin)],
               library_paths=[str(out)]+original['library_paths'],commands=commands,
               diagnostic_scope='Opt-in native-stage profiling; original dependency DSOs borrowed unchanged.')
    (out/'native-load.txt').write_text('\n'.join(build['libraries'])+'\n')
    (out/'build.json').write_text(json.dumps(build,indent=2)+'\n')
    (O/('executed-build'+suffix+'.json')).write_text(json.dumps(build,indent=2)+'\n')
    print(json.dumps({'state':'complete','modules':len(custom),'output':str(out)}),flush=True)
finally:
    guard.stop()
    (O/('build-memory-summary'+suffix+'.json')).write_text(json.dumps(guard.summary(),indent=2)+'\n')
