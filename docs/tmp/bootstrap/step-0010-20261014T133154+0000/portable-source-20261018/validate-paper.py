from pathlib import Path
import subprocess,resource,os,json
R=Path("/workspaces/repository")
A=R/"docs/tmp/bootstrap/step-0010-20261014T133154+0000/portable-source-20261018"
os.sched_setaffinity(0,{16,17,18,19})
resource.setrlimit(resource.RLIMIT_AS,(51539607552,51539607552))
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
cmd=["/workspaces/.agent-state/gpu-smt-deps/tectonic-0.17.0/tectonic","--keep-logs","main.tex"]
p=subprocess.run(cmd,cwd=R/"docs/paper")
(A/"paper-terminal.json").write_text(json.dumps({"returncode":p.returncode,"command":cmd})+"\n")
