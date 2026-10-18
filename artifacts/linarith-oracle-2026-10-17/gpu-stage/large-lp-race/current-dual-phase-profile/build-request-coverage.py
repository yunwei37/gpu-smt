from pathlib import Path
import os,resource,subprocess,shutil,json,datetime
R=Path('/workspaces/repository');A=R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/current-dual-phase-profile'
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/current-dual-phase-profile')
C=Path('/tmp/gpu-smt-linarith-oracle-20261017/pooled-wall-cost');B=Path('/tmp/gpu-smt-linarith-oracle-20261017/two-sided-oracle')
T=Path('/tmp/gpu-smt-goedel427-20261014')
os.sched_setaffinity(0,{4,5,6,7});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
env=dict(os.environ,PATH=str(T/'lean-4.27.0-linux/bin')+':/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
env['LEAN_PATH']=':'.join([str(U),str(U.parent),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]+[str(p/'.lake/build/lib/lean')for p in (T/'mathlib4/.lake/packages').iterdir()if p.is_dir()])
records=[]
def run(cmd,cwd=R):
 p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 records.append({'cmd':cmd,'cwd':str(cwd),'exit':p.returncode,'output':p.stdout})
 (A/'request-build-receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':records},indent=2)+'\n')
 print(p.stdout[-1600:],flush=True)
 if p.returncode:raise SystemExit(p.returncode)
names=['CostNative','CostFast','CostBaseline','CostOracle']
for name in names:
 out=U/'GpuArithmetic'/(name+'.olean')
 if out.is_symlink():out.unlink()
 run(['lean','-o',str(out),'-c',str(U/(name+'.c')),str(U/'GpuArithmetic'/(name+'.lean'))],U)
all_names=['CostTelemetry','CostStages','CostProducts','CostNative','CostFast','CostBaseline','CostOracle']
sources=[str((U if n in names else C)/(n+'.c'))for n in all_names]
run(['leanc','-O3','-DLEAN_EXPORTING','-shared','-fPIC',*sources,str(A/'cost-emit.c'),'-L/usr/lib/x86_64-linux-gnu','-lz','-o',str(U/'batch-oracle.so')])
core=U/'numeric-source'
shutil.copytree(B/'native',core,ignore=shutil.ignore_patterns('target','.git'))
p=core/'src/bin/arithmetic-batchd.rs';s=p.read_text()
needle=' Ok(json!({"cert":cert,"linear_ns":linear_ns,"products_ns":products_ns,"lp_ns":lp_ns,"facts":all.len(),"atoms":ids.len()-1}))'
replacement=r''' let exact_nnz:usize=hyps.iter().map(|h|h.coeffs.iter().filter(|(_,c)|!c.is_zero()).count()+usize::from(h.ineq==Ineq::Lt)).sum();
 let product_columns:Vec<bool>=origins.iter().map(|(origin,_)|origin[0]=="mul").collect();
 Ok(json!({"cert":cert,"linear_ns":linear_ns,"products_ns":products_ns,"lp_ns":lp_ns,"facts":all.len(),"atoms":ids.len()-1,
  "exact_certificate_shape":{"rows":ids.len()+1,"cols":hyps.len(),"nnz":exact_nnz},
  "generated_products":all.len()-pool.len()-1,"product_columns":product_columns}))'''
assert s.count(needle)==1;s=s.replace(needle,replacement);p.write_text(s)
(A/'request-source/arithmetic-batchd.rs').write_text(s)
run(['cargo','build','--release','--offline','--locked','--bin','arithmetic-batchd'],core)
p=U/'arithmetic-batchd';p.unlink();shutil.copy2(core/'target/release/arithmetic-batchd',p)
print('REQUEST_BUILD_COMPLETE',flush=True)
