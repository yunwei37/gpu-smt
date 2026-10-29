from pathlib import Path
import json,os,subprocess,sys
d=json.loads(Path("/tmp/gpu-smt-solo42-native-library-20261028/rebound-point-13d4606.json").read_text())
env=dict(os.environ,**d["native_environment_overrides"])
env["PATH"]=d["PATH_prepend"]+":"+env["PATH"]
for k in list(env):
    if k.startswith("GPU_ARITHMETIC_")or k in ["GPU_SMT_CEX_MODE","GPU_SMT_ORACLE_SOCKET","GPU_SMT_LINARITH_SOCKET","GPU_SMT_CANDIDATE_TIMING"]:
        env.pop(k,None)
cmd=list(d["prospective_command"])
cmd[cmd.index("--environment")+1]="lean49-native-four-qualification-20261029"
with Path("/tmp/gpu-smt-state-reuse-20261029/native-repl-four-input.jsonl").open("rb")as source:
    q=subprocess.run(cmd,cwd=d["cwd"],env=env,stdin=source)
raise SystemExit(q.returncode)
