from pathlib import Path
import subprocess,os,resource,json
R=Path("/workspaces/repository");D=R/"bench/lean-native/linarith-oracle/reproduction"
A=R/"docs/tmp/bootstrap/step-0010-20261014T133154+0000/portable-source-20261018"
U=Path("/tmp/gpu-smt-linarith-oracle-20261017/portable-source-build")
os.sched_setaffinity(0,{20,21,22,23});resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
env=dict(os.environ,PATH="/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux/bin:/usr/local/cargo/bin:"+os.environ["PATH"],CARGO_HOME="/usr/local/cargo",RUSTUP_HOME="/usr/local/rustup",CARGO_NET_OFFLINE="true")
env.pop("CARGO_TARGET_DIR",None)
cmd=["python3","-u",str(D/"build.py"),"--mathlib","/tmp/gpu-smt-goedel427-20261014/mathlib4","--out",str(U)]
p=subprocess.run(cmd,cwd=R,env=env)
(A/"native-build-terminal.json").write_text(json.dumps({"returncode":p.returncode,"argv":cmd})+"\n")
raise SystemExit(p.returncode)
