#!/usr/bin/env python3
"""Isolated actual native WHNF replacement/provider executable. Build only."""
import argparse,hashlib,json,os,pathlib,subprocess
repo=pathlib.Path(__file__).resolve().parents[2]
sdk=pathlib.Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
base=repo/'artifacts/lean-service-lifecycle-2026-10-13/build1'
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=pathlib.Path,default=repo/'artifacts/lean-gpu-checking-2026-10-13/closure-development-20261013/native-bridge2');out=parser.parse_args().out.resolve()
out.mkdir(parents=True,exist_ok=True)
if (out/'Lean49ClosureNativeV2').exists() or (out/'Lean49ClosureNativeV2-final').exists():raise FileExistsError('integrated executable already exists; preserve identity')
old=json.loads((base/'build.terminal.json').read_text());original=sdk/'src/lean/Lean/Meta/WHNF.lean';text=original.read_text()
marker='@[export lean_whnf]\npartial def whnfImp'
header='''-- Isolated dynamic beta/zeta provider. Value layout matches the native C ABI.
private structure ClosureProviderResult where
  value : Option Expr
  reason : UInt32
  reductionSteps : UInt64
  quotationNodes : UInt64
  environments : UInt64
  deriving Inhabited
@[extern "closure_native_provider_enabled"]
private opaque closureProviderEnabled (e : @& Expr) : Bool
@[extern "closure_native_provider_reduce"]
private opaque closureProviderReduce (e : @& Expr) (steps cap : UInt64) : IO ClosureProviderResult
private def closureHeadRedex (e : Expr) : Bool :=
  match e.consumeMData with
  | .letE .. => true
  | .app f .. =>
    match f.getAppFn.consumeMData with
    | .lam .. | .letE .. => true
    | _ => false
  | _ => false
private def closureProviderTry (e : Expr) : MetaM (Option Expr) := do
  if !closureProviderEnabled e || !closureHeadRedex e || e.hasLooseBVars then return none
  if (← read).canUnfold?.isSome then return none
  if (← isTracingEnabledFor `Meta.whnf) then return none
  checkSystem "whnf"
  let r ← closureProviderReduce e 2000000 65536
  checkSystem "whnf"
  return r.value

'''
assert text.count(marker)==1;text=text.replace(marker,header+marker)
start=text.index('      withTraceNode `Meta.whnf',text.index(marker));end=text.index('\n/-- If `e` is a projection',start)
body=text[start:end].rstrip()
# Original entire miss computation is preserved literally except indentation;
# None runs it directly, NEVER calls lean_whnf again on the same original input.
text=text[:start]+'''      do
        let bridgeResult ← closureProviderTry e
        if let some r := bridgeResult then
          return (← cache useCache e r)
'''+ '\n'.join('  '+line for line in body.splitlines())+'\n'+text[end:]
source=out/'Lean/Meta/WHNF.lean';source.parent.mkdir(parents=True,exist_ok=True);source.write_text(text)
host=(base/'lean49_prepared_parent.c').read_text()
insert='''extern void closure_native_provider_enable(void);
extern void closure_native_provider_close(void);
extern void closure_native_provider_disable(void);
extern void closure_native_provider_checkpoint(uint64_t,const char*);
static void closure_native_exit(int code) { closure_native_provider_close(); _exit(code); }
#define _exit closure_native_exit
'''
point='static int snapshot_mode = 0;';assert host.count(point)==1;host=host.replace(point,insert+'\n'+point)
# Existing native checkpoint is the actual frontend boundary. Never enable in
# the immutable prepared parent or before native import preparation finishes.
point='    /* Both methods prepare imports/cache synchronously.'
assert host.count(point)==1
host=host.replace(point,'''    if (!strcmp(lean_string_cstr(stage), "frontend_begin") && (snapshot_mode || in_candidate_child)) closure_native_provider_enable();
    if (!strcmp(lean_string_cstr(stage), "frontend_complete")) { closure_native_provider_disable(); closure_native_provider_checkpoint(index, "frontend_complete"); }
'''+point)
# Main return/normal EOF owns cleanup, including snapshot stream lifetime.
host=host.replace('int main(int argc, char **argv) {','static int closure_original_main(int argc, char **argv) {')
host+='''\nint main(int argc,char **argv) { int result=closure_original_main(argc,argv); closure_native_provider_close(); return result; }\n'''
hostpath=out/'lean49_closure_parent.c';hostpath.write_text(host)
inc=base/'lean49_prepared_worker_pool.c.inc';(out/inc.name).write_bytes(inc.read_bytes())
helper=repo/'bench/lean-gpu/closure_native_provider_helpers/ClosureProviderHelpers.lean'
commands=[
 [str(sdk/'bin/lean'),'-R',str(out),'-c',str(out/'WHNF.c'),str(source)],
 [str(sdk/'bin/leanc'),'-O3','-c',str(out/'WHNF.c'),'-o',str(out/'WHNF.o')],
 [str(sdk/'bin/lean'),'-R',str(helper.parent),'-c',str(out/'ClosureProviderHelpers.c'),str(helper)],
 ['gcc','-O3','-I'+str(sdk/'include'),'-c',str(out/'ClosureProviderHelpers.c'),'-o',str(out/'ClosureProviderHelpers.o')],
 ['g++','-std=c++17','-O3','-Wall','-Wextra','-I'+str(sdk/'include'),'-c',str(repo/'bench/lean-gpu/closure-native-bridge-v2.cpp'),'-o',str(out/'closure-native-bridge-v2.o')],
 ['g++','-std=c++17','-O3','-Wall','-Wextra','-I'+str(sdk/'include'),'-c',str(repo/'bench/lean-gpu/closure-native-provider-v2.cpp'),'-o',str(out/'closure-native-provider-v2.o')],
 ['gcc','-std=gnu11','-O3','-Wall','-Wextra','-I'+str(sdk/'include'),'-c',str(hostpath),'-o',str(out/'parent.o')],
 ['/workspaces/.agent-state/gpu-smt-deps/cuda-12.8-minimal/sdk/bin/nvcc','-std=c++17','-O2','-ptx','-arch=compute_120',str(repo/'bench/lean-gpu/closure-native-packed-v2.cu'),'-o',str(out/'closure-native-packed-v2.ptx')]]
link=list(old['commands'][-1]);link[link.index('-o')+1]=str(out/'Lean49ClosureNativeV2')
link=[str(out/'parent.o') if p==str(base/'parent.o') else p for p in link]
link[link.index('-o')+2:link.index('-o')+2]=[str(out/k) for k in ('WHNF.o','ClosureProviderHelpers.o','closure-native-bridge-v2.o','closure-native-provider-v2.o')]
libstdcpp=subprocess.check_output(['g++','-print-file-name=libstdc++.so'],text=True).strip()
link += [libstdcpp,'-ldl','-pthread'];commands.append(link)
receipt=dict(commands=commands,inherited_build=str(base/'build.terminal.json'),source_boundary=str(original),source_whnf_miss_body_sha256=hashlib.sha256(body.encode()).hexdigest(),role='isolated dependency/integration build only; zero runtime/fixture/GPU/candidate execution')
(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
env=dict(os.environ)
with (out/'build.log').open('x') as log:
 for i,cmd in enumerate(commands):
  log.write(json.dumps(cmd)+'\n');log.flush();p=subprocess.run(cmd,cwd=repo,env=env,stdout=log,stderr=log)
  receipt['last_command']=i;receipt['last_returncode']=p.returncode;(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
  if p.returncode:raise SystemExit(p.returncode)
paths=[original,source,hostpath,inc,helper,pathlib.Path(__file__),out/'Lean49ClosureNativeV2',out/'closure-native-packed-v2.ptx']
paths += [pathlib.Path(p) for p in link if p.endswith(('.o','.a'))]
paths += list((repo/'bench/lean-gpu').glob('closure-native-*-v2.*'))
receipt.update(build_complete=True,sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
(out/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
