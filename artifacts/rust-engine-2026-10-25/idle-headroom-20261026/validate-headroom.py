from pathlib import Path
import subprocess,os,json,time,datetime,gzip
R=Path('/workspaces/repository');A=R/'artifacts/rust-engine-2026-10-25'/datetime.datetime.now(datetime.timezone.utc).strftime('validation-%Y%m%dT%H%M%S');A.mkdir();D=Path('/tmp/gpu-smt-rust-engine-build-20261025')
env=dict(os.environ,PATH='/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup',CARGO_TARGET_DIR=str(D/'target'))
steps=[['test','-p','gpu-smt-engine','--test','engine','--locked','-j','2','idle_native_state_cannot_strand_a_large_forecast','--','--exact','--nocapture']]
receipts=[]
for i,args in enumerate(steps):
 start=time.monotonic();command=['/usr/local/cargo/bin/cargo']+args;log=D/('headroom-repro-'+str(i)+'.log')
 with log.open('wb')as f:p=subprocess.run(command,cwd=R,env=dict(env,RUSTDOCFLAGS='-D warnings'),stdout=f,stderr=subprocess.STDOUT)
 receipts.append(dict(command=command,exit=p.returncode,seconds=time.monotonic()-start))
 (A/'validation.json').write_text(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=receipts,native_differential='Native tests compiled but not executed by ordinary checks; full7808resourcepair remains sole active native acquisition. Headroom regression uses fixture bytes/backend, not native performance evidence.'),indent=2)+'\n')
 (A/('validation-'+str(i)+'.log.gz')).write_bytes(gzip.compress(log.read_bytes(),mtime=0))
 if p.returncode:break

raise SystemExit(next((receipt["exit"] for receipt in receipts if receipt["exit"]), 0))
