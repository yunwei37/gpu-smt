from pathlib import Path
import subprocess,json,datetime,time,shutil
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016')
sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux');src=p/'lean4-4.27.0/src'
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/service-integration'
clang=str(sdk/'bin/clang')
common=[clang,'-x','c++','-std=c++17','-O3','-fPIC','-stdlib=libc++','-nostdinc','-nostdinc++','-isystem',str(p/'libcxx-19.1.7.src/include'),'-isystem',str(sdk/'include/clang'),'-isystem','/usr/include/x86_64-linux-gnu','-isystem','/usr/include','-DLEAN_MULTI_THREAD','-DLEAN_USE_GMP','-DLEAN_EXPORTING','-I'+str(sdk/'include'),'-I'+str(src),'-I'+str(r/'bench/lean-native')]

for name in ['io.cpp','object.cpp','process.cpp']:
 cmd=common+['-c',str(src/'runtime'/name),'-o',str(p/(name+'.o'))]
 with (e/('static-'+name+'.stdout')).open('w') as out,(e/('static-'+name+'.stderr')).open('w') as err:z=subprocess.run(cmd,stdout=out,stderr=err)
 (e/('static-'+name+'.json')).write_text(json.dumps({'command':cmd,'exit_code':z.returncode},indent=2)+'\n')
 print(name,z.returncode,(e/('static-'+name+'.stderr')).read_text()[-1500:])
 if z.returncode:raise SystemExit(z.returncode)
