from pathlib import Path
import os,subprocess,resource,json,time
R=Path("/workspaces/repository")
D=R/"bench/lean-native/linarith-oracle/reproduction"
A=R/"docs/tmp/bootstrap/step-0010-20261014T133154+0000/portable-source-20261018"
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build")
os.sched_setaffinity(0,{20,21,22,23});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
env=dict(os.environ,PATH="/usr/local/cargo/bin:"+os.environ["PATH"],CARGO_HOME="/usr/local/cargo",RUSTUP_HOME="/usr/local/rustup",CARGO_NET_OFFLINE="true")
env.pop("CARGO_TARGET_DIR",None)
commands=[["cargo","build","--release","--locked","--manifest-path",str(D/"native/Cargo.toml"),"--target-dir",str(U/"native-target")],["cargo","test","--locked","--lib","--manifest-path",str(D/"native/Cargo.toml"),"--target-dir",str(U/"native-target")]]
records=[]
for cmd in commands:
 start=time.monotonic();p=subprocess.run(cmd,cwd=U,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 records.append({"argv":cmd,"returncode":p.returncode,"whole_seconds":time.monotonic()-start,"output":p.stdout})
 (A/"numeric-build-tests.json").write_text(json.dumps(records,indent=2)+"\n")
 print(p.returncode,p.stdout[-4000:],flush=True)
 if p.returncode:raise SystemExit(p.returncode)
