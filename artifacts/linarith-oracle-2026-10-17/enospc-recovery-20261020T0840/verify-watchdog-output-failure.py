"""Real /dev/full regression of watchdog-output failure; not Lean performance evidence."""
from pathlib import Path
import contextlib,json,os,subprocess,sys,tempfile,time,types
ROOT=Path(__file__).resolve().parents[3]
source=ROOT/"bench/lean-native/linarith-oracle/memory_budget.py"
old=subprocess.check_output(["git","show","17f75ba1aba9cbb468bf59d63a8dcfb21fea91b0:bench/lean-native/linarith-oracle/memory_budget.py"],cwd=ROOT,text=True)
rows=[]
for version,body in [("published_before_fix",old),("fixed",source.read_text())]:
 module=types.ModuleType("watchdog_regression_"+version);exec(compile(body,str(source),"exec"),module.__dict__)
 for both_outputs_full in [False,True]:
  with tempfile.TemporaryDirectory(prefix="gpu-smt-watchdog-io-",dir="/tmp")as directory:
   out=Path(directory)
   (out/"memory-rss.jsonl").symlink_to("/dev/full")
   if both_outputs_full:(out/"memory-watchdog-error.txt").symlink_to("/dev/full")
   child=subprocess.Popen([sys.executable,"-c","import signal;signal.pause()"])
   callback=[]
   guard=module.MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,"/no-test-native-repl",out)
   def terminate():
    callback.append(True);child.terminate()
   guard.on_error=terminate
   escaped=None
   try:
    guard.run()
   except OSError as exc:escaped=str(exc)
   finally:
    # The old broken control must not leave its test child running.
    stopped_by_callback=bool(callback)
    if child.poll()is None and not stopped_by_callback:child.terminate()
    exitcode=child.wait(timeout=10)
   rows.append(dict(version=version,both_sample_and_error_record_ENOSPC=both_outputs_full,
    real_errno28_in_original_error="No space left on device"in(guard.error or""),
    stop_callback_executed=stopped_by_callback,real_child_exitcode=exitcode,
    escaped_error=escaped))
assert rows[0]["stop_callback_executed"]
assert not rows[1]["stop_callback_executed"] and rows[1]["escaped_error"]
assert all(x["stop_callback_executed"]and x["real_errno28_in_original_error"]and x["escaped_error"]is None for x in rows[2:])
assert all(x["real_child_exitcode"]==-15 for x in rows)
print(json.dumps({"scope":"Actual /dev/full flush/error-record failures plus real owned child termination; not Lean workload qualification or performance.", "observations":rows},indent=2))
