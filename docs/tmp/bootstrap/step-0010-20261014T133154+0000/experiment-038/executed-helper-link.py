from pathlib import Path
import subprocess,json,datetime,time,shutil
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016')
sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux');src=p/'lean4-4.27.0/src'
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038'
clang=str(sdk/'bin/clang')
common=[clang,'-x','c++','-std=c++17','-O3','-fPIC','-stdlib=libc++','-nostdinc','-nostdinc++','-isystem',str(p/'libcxx-19.1.7.src/include'),'-isystem',str(sdk/'include/clang'),'-isystem','/usr/include/x86_64-linux-gnu','-isystem','/usr/include','-DLEAN_MULTI_THREAD','-DLEAN_USE_GMP','-DLEAN_EXPORTING','-I'+str(sdk/'include'),'-I'+str(src),'-I'+str(r/'bench/lean-native')]

cmd=common+['-shared',str(r/'bench/lean-native/native-ref-branches.cpp'),'-L'+str(sdk/'lib'),'-Wl,-Bsymbolic','-Wl,-Bstatic','-lc++','-lc++abi','-lunwind','-Wl,-Bdynamic','-lpthread','-Wl,-soname,libgpu_smt_ref_branches.so','-o',str(p/'libgpu_smt_ref_branches.so')]
with (e/'branch-support-linked-cxx.stdout').open('w') as out,(e/'branch-support-linked-cxx.stderr').open('w') as err:z=subprocess.run(cmd,stdout=out,stderr=err)
(e/'branch-support-linked-cxx.json').write_text(json.dumps({'command':cmd,'exit_code':z.returncode},indent=2)+'\n')
print(z.returncode,(e/'branch-support-linked-cxx.stderr').read_text()[-2500:])
