#!/usr/bin/env python3
"""Link v3 retained-host-arena provider against frozen v2 hook/algorithm. Build only."""
import argparse,hashlib,json,pathlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[2]
base=repo/'artifacts/lean-gpu-checking-2026-10-13/closure-development-20261013/native-bridge2'
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=pathlib.Path,default=base.parent/'native-bridge3');out=p.parse_args().out.resolve()
out.mkdir(parents=True,exist_ok=False)
old=json.loads((base/'final-link-receipt.json').read_text());sdk=pathlib.Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
provider=repo/'bench/lean-gpu/closure-native-provider-v3.cpp';obj=out/'closure-native-provider-v3.o';binary=out/'Lean49ClosureNativeV3'
compile_cmd=['g++','-std=c++17','-O3','-Wall','-Wextra','-I'+str(sdk/'include'),'-c',str(provider),'-o',str(obj)]
link=[str(obj) if x.endswith('/closure-native-provider-v2-final.o') else x for x in old['final_link_command']]
link[link.index('-o')+1]=str(binary)
paths=[base/'final-link-receipt.json',base/'closure-native-packed-v2.ptx',provider,pathlib.Path(__file__).resolve()]
paths += [pathlib.Path(x) for x in link if x.endswith(('.o','.a')) and pathlib.Path(x)!=obj]
identity={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
receipt=dict(commands=[compile_cmd,link],inherited_link=str(base/'final-link-receipt.json'),inherited_sha256=identity,role='causal control arena-lifetime fairness repair; build only; same frozen semantics/PTX; no executions')
(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (out/'build.log').open('x') as log:
 for i,cmd in enumerate([compile_cmd,link]):
  log.write(json.dumps(cmd)+'\n');log.flush();r=subprocess.run(cmd,cwd=repo,stdout=log,stderr=log)
  receipt.update(last_command=i,last_returncode=r.returncode);(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
  if r.returncode:raise SystemExit(r.returncode)
for x in paths:assert hashlib.sha256(x.read_bytes()).hexdigest()==identity[str(x)]
receipt.update(build_complete=True,executable_bytes=binary.stat().st_size,sha256={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [provider,obj,binary,pathlib.Path(__file__).resolve()]},gpu_launches=0,queries=0,fixtures=0)
(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'executable':str(binary),'bytes':receipt['executable_bytes'],'sha256':receipt['sha256'][str(binary)],'GPU_launches':0}))
