from pathlib import Path
import subprocess,json,datetime,time,shutil
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016')
sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux');src=p/'lean4-4.27.0/src'
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038'
clang=str(sdk/'bin/clang')
common=[clang,'-x','c++','-std=c++17','-O3','-fPIC','-stdlib=libc++','-nostdinc','-nostdinc++','-isystem',str(p/'libcxx-19.1.7.src/include'),'-isystem',str(sdk/'include/clang'),'-isystem','/usr/include/x86_64-linux-gnu','-isystem','/usr/include','-DLEAN_MULTI_THREAD','-DLEAN_USE_GMP','-DLEAN_EXPORTING','-I'+str(sdk/'include'),'-I'+str(src),'-I'+str(r/'bench/lean-native')]
commands=[
 ('branch-support-build',common+['-shared',str(r/'bench/lean-native/native-ref-branches.cpp'),'-L'+str(sdk/'lib'),'-Wl,-rpath,'+str(sdk/'lib'),'-Wl,-soname,libgpu_smt_ref_branches.so','-o',str(p/'libgpu_smt_ref_branches.so')]),
 ('runtime-io-build',common+['-c',str(src/'runtime/io.cpp'),'-o',str(p/'io.cpp.o')]),
 ('runtime-object-build',common+['-c',str(src/'runtime/object.cpp'),'-o',str(p/'object.cpp.o')])
]
for tag,cmd in commands:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
 with (e/(tag+'.stdout')).open('w') as out,(e/(tag+'.stderr')).open('w') as err:
  z=subprocess.run(cmd,cwd=p,stdout=out,stderr=err)
 rec={'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'cwd':str(p),'exit':z.returncode,'whole_seconds':time.monotonic()-tick,'scope':'native dependency/runtime setup only, not verifier or performance result'}
 (e/(tag+'.terminal.json')).write_text(json.dumps(rec,indent=2)+'\n')
 print(tag,z.returncode,(e/(tag+'.stderr')).read_text()[-2500:],flush=True)
 if z.returncode:break
