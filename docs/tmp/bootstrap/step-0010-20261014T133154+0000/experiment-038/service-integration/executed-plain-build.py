from pathlib import Path
import tarfile,subprocess,shutil,json,shlex
r=Path('/workspaces/repository');e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/service-integration'
p=Path('/tmp/gpu-smt-native-ref-branches-20261016');sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux');q=sdk.parent/'repl-producer-native'
d=p/'plain-runtime';d.mkdir(exist_ok=False);src=p/'lean4-4.27.0/src'
common=[str(sdk/'bin/clang'),'-x','c++','-std=c++17','-O3','-fPIC','-stdlib=libc++','-nostdinc','-nostdinc++','-isystem',str(p/'libcxx-19.1.7.src/include'),'-isystem',str(sdk/'include/clang'),'-isystem','/usr/include/x86_64-linux-gnu','-isystem','/usr/include','-DLEAN_MULTI_THREAD','-DLEAN_USE_GMP','-DLEAN_EXPORTING','-I'+str(sdk/'include'),'-I'+str(src),'-I'+str(r/'bench/lean-native')]
def run(tag,cmd):
 with (e/(tag+'.stdout')).open('w') as out,(e/(tag+'.stderr')).open('w') as err:z=subprocess.run(cmd,cwd=p,stdout=out,stderr=err)
 (e/(tag+'.json')).write_text(json.dumps({'command':cmd,'exit_code':z.returncode},indent=2)+'\n')
 print(tag,z.returncode, (e/(tag+'.stderr')).read_text()[-1500:] if z.returncode else '',flush=True)
 if z.returncode:raise SystemExit(z.returncode)
with tarfile.open(p/'lean4-v4.27.0.tar.gz') as tf:
 for name in ['io.cpp','object.cpp','process.cpp']:
  f=d/name;f.write_bytes(tf.extractfile('lean4-4.27.0/src/runtime/'+name).read())
  run('plain-static-'+name,common+['-c',str(f),'-o',str(d/(name+'.o'))])
  run('plain-shared-'+name,common+['-DNDEBUG','-ftls-model=initial-exec','-c',str(f),'-o',str(d/(name+'.shared.o'))])
shutil.copyfile(sdk/'lib/lean/libleanrt.a',d/'libleanrt.a')
run('plain-runtime-archive',[str(sdk/'bin/llvm-ar'),'rcs',str(d/'libleanrt.a')]+[str(d/(name+'.o')) for name in ['io.cpp','object.cpp','process.cpp']])
cmd=[str(sdk/'bin/clang'),'-shared','-fuse-ld=lld','-o',str(d/'libleanshared.so'),'-Wl,-soname,libleanshared.so','-Wl,-Bsymbolic','-Wl,--whole-archive']+[str(sdk/'lib/lean'/x) for x in ['libLean.a','libStd.a','libInit.a','libleancpp.a']]
for f in (p/'runtime-shared').glob('*.o'):
 cmd.append(str(d/(f.name.removesuffix('.o')+'.shared.o')) if f.name in ['io.cpp.o','object.cpp.o','process.cpp.o'] else str(f))
cmd+=['-Wl,--no-whole-archive','-L'+str(sdk/'lib'),'-Wl,-Bstatic','-lc++','-lc++abi','-lunwind','-lgmp','-luv','-Wl,-Bdynamic','-lpthread','-ldl','-lm','-lrt','-Wl,-rpath,'+str(d)]
run('plain-shared-runtime-link',cmd)
trace=json.loads((q/'.lake/build/bin/repl.trace').read_text())
cmd=shlex.split(trace['log'][0]['message'][3:]);cmd[cmd.index('-o')+1]=str(d/'repl')
first=cmd.index('--sysroot');last=cmd.index('-fuse-ld=lld');cmd[first:last]=['-L'+str(sdk/'lib')]
cmd.insert(cmd.index('-lc++abi')+1,'-lunwind');cmd[cmd.index('-lleanrt')]=str(d/'libleanrt.a');cmd+=['-Wl,-rpath,'+str(d),'-Wl,-rpath,'+str(sdk/'lib')]
run('plain-repl-link',cmd)
