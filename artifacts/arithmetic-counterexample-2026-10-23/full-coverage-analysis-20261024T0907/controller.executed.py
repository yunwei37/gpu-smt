import importlib.util,os,subprocess,json
from pathlib import Path
R=Path('/workspaces/repository');out=Path('/workspaces/repository/artifacts/arithmetic-counterexample-2026-10-23/full-coverage-analysis-20261024T0907')
spec=importlib.util.spec_from_file_location('budget',R/'bench/lean-native/linarith-oracle/memory_budget.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
guard=m.MemoryWatchdog(os.getpid(),48*1024**3,48*1024**3,2,'repl',out)
guard.start()
try:
 result=subprocess.run(['/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python','-u',str(R/'bench/lean-counterexample/analyze-goals.py'),'--output-dir',str(out)],cwd=R)
finally:guard.stop()
(out/'analysis-memory.json').write_text(json.dumps(guard.summary(),indent=2)+'\n')
(out/'analysis-exit.json').write_text(json.dumps({'exit_code':result.returncode,'watchdog_error':guard.error})+'\n')
