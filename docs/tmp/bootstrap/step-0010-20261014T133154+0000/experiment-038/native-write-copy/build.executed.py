from pathlib import Path
import json,subprocess,time,datetime,resource,shutil
r=Path("/workspaces/repository")
n=r/"docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-write-copy"
previous=n.parent/"native-command-protocol/build.launch.json"
cmd=json.loads(previous.read_text())["command"]
out=Path("/tmp/gpu-smt-native-write-copy-20261016/build")
cmd[cmd.index("--output")+1]=str(out)
before=resource.getrusage(resource.RUSAGE_CHILDREN)
tick=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
(n/"build.launch.json").write_text(json.dumps({"command":cmd,"utc":utc},indent=2)+"\n")
with (n/"build.stdout").open("wb") as stdout,(n/"build.stderr").open("wb") as stderr:
 result=subprocess.run(cmd,stdout=stdout,stderr=stderr,cwd=r)
after=resource.getrusage(resource.RUSAGE_CHILDREN)
receipt={"command":cmd,"start_utc":utc,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"wall_seconds":time.monotonic()-tick,"waited_children_cpu_seconds":after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime,"exit_code":result.returncode,"overlap":"finite development build; original frozen-v1 native capture unchanged"}
(n/"build.terminal.json").write_text(json.dumps(receipt,indent=2)+"\n")
if out.exists():
 for src,name in [(out/"commands.jsonl","build.commands.jsonl"),(out/"logs","build-logs"),(out/"implementation","built-source")]:
  if src.is_dir():shutil.copytree(src,n/name)
  elif src.is_file():shutil.copyfile(src,n/name)
print(json.dumps(receipt))
raise SystemExit(result.returncode)
