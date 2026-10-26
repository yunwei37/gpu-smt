from pathlib import Path
import subprocess,os,json,time,datetime,gzip
R=Path('/workspaces/repository');A=R/'artifacts/rust-engine-2026-10-25'/datetime.datetime.now(datetime.timezone.utc).strftime('validation-%Y%m%dT%H%M%S');A.mkdir();D=Path('/tmp/gpu-smt-rust-engine-build-20261025')
env=dict(os.environ,PATH='/usr/local/cargo/bin:'+os.environ['PATH'],CARGO_HOME='/usr/local/cargo',RUSTUP_HOME='/usr/local/rustup',CARGO_TARGET_DIR=str(D/'target'))
steps=[['fmt','--all'],['fmt','--all','--','--check'],['clippy','--workspace','--all-targets','--locked','-j','2','--','-D','warnings'],['test','--workspace','--all-targets','--locked','-j','2'],['doc','--workspace','--no-deps','--locked','-j','2'],['run','-p','gpu-smt-server','--bin','gpu-smt','--','--help']]
receipts=[]
for i,args in enumerate(steps):
 start=time.monotonic();command=['/usr/local/cargo/bin/cargo']+args;log=D/('final-'+str(i)+'.log')
 with log.open('wb')as f:p=subprocess.run(command,cwd=R,env=dict(env,RUSTDOCFLAGS='-D warnings'),stdout=f,stderr=subprocess.STDOUT)
 receipts.append(dict(command=command,exit=p.returncode,seconds=time.monotonic()-start))
 (A/'validation.json').write_text(json.dumps(dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),steps=receipts,native_differential='Native tests compiled but not executed by ordinary checks; full7808resourcepair remains sole active native acquisition. File/argv/complete-stderr fixtures are not Lean proofs.'),indent=2)+'\n')
 (A/('validation-'+str(i)+'.log.gz')).write_bytes(gzip.compress(log.read_bytes(),mtime=0))
 if p.returncode:break
