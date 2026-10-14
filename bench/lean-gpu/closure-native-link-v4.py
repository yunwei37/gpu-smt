#!/usr/bin/env python3
"""Repair native provider C++ exception ABI using exact SDK libc++ headers/runtime."""
import hashlib,json,pathlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[2]
root=repo/'artifacts/lean-gpu-checking-2026-10-13/closure-development-20261013'
out=root/'native-bridge4';out.mkdir(exist_ok=True)
sdk=pathlib.Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
owned=pathlib.Path('/workspaces/.agent-state/gpu-smt-deps/lean49-owned-runtime')
old=json.loads((root/'native-bridge3/build-receipt.json').read_text())
commands=[]; replacements={}
for name in ['closure-native-bridge-v2','closure-native-provider-v3']:
 src=repo/'bench/lean-gpu'/f'{name}.cpp';obj=out/f'{name}-libcxx.o'
 commands.append([str(sdk/'bin/clang'),'-O3','-std=c++17','-nostdinc++','-isystem',str(owned/'libcxx-15.0.1.src/include'),'-isystem','/usr/lib/gcc/x86_64-linux-gnu/14/include','-I'+str(owned/'build4'),'-I'+str(owned/'lean4-be6c4894e0a6/src'),'-pthread','-fPIC','-U__OPTIMIZE__','-DLEAN_MULTI_THREAD','-DLEAN_EXPORTING','-I'+str(sdk/'include'),'-c',str(src),'-o',str(obj)])
 replacements[name]=str(obj)
link=[]
for arg in old['commands'][-1]:
 if arg=='/usr/lib/gcc/x86_64-linux-gnu/14/libstdc++.so':continue
 if arg.endswith('/closure-native-bridge-v2.o'):arg=replacements['closure-native-bridge-v2']
 if arg.endswith('/closure-native-provider-v3.o'):arg=replacements['closure-native-provider-v3']
 link.append(arg)
binary=out/'Lean49ClosureNativeV4';link[link.index('-o')+1]=str(binary);commands.append(link)
inputs=[pathlib.Path(x) for x in old['commands'][-1] if x.endswith(('.o','.a'))]
inputs += [repo/'bench/lean-gpu/closure-native-bridge-v2.cpp',repo/'bench/lean-gpu/closure-native-provider-v3.cpp',root/'native-bridge2/closure-native-packed-v2.ptx']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
receipt=dict(commands=commands,frozen_inputs_sha256=hashes,repair='SDK libc++ ABI throughout; remove dynamically mixed GNU C++ exception runtime; algorithm and PTX unchanged',affinity=[0],gpu_launches=0)
with (out/'build.log').open('x') as log:
 for i,cmd in enumerate(commands):
  log.write(json.dumps(cmd)+'\n');log.flush();r=subprocess.run(cmd,cwd=repo,stdout=log,stderr=log)
  receipt.update(last_command=i,last_returncode=r.returncode);(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
  if r.returncode:raise SystemExit(r.returncode)
for p in inputs:assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[str(p)]
receipt.update(build_complete=True,executable_bytes=binary.stat().st_size,sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [binary,pathlib.Path(__file__).resolve()]+[pathlib.Path(x) for x in replacements.values()]})
(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt['sha256']))
