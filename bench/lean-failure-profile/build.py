"""Relink existing native verification objects with one diagnostic runtime wrapper."""
from pathlib import Path
import json,os,resource,shlex,subprocess,sys
R=Path('/workspaces/repository');B=R/'bench/lean-failure-profile';A=R/'artifacts/lean-failure-profile-2026-10-25'
sdk=Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
original=Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix/repl-kernel')
out=Path('/tmp/gpu-smt-failure-profiler-20261025');out.mkdir(exist_ok=True)
os.sched_setaffinity(0,{8,9,10,11});resource.setrlimit(resource.RLIMIT_AS,(24*1024**3,24*1024**3))
text=json.loads((original/'.lake/build/bin/repl.log.json').read_text())['log'][0]['message']
link=shlex.split(text.removeprefix('.> '));link[link.index('-o')+1]=str(out/'repl')
compile=['g++','-std=c++17','-O2','-fPIC','-I'+str(sdk/'include'),'-c',str(B/'profileit.cpp'),'-o',str(out/'profileit.o')]
link.extend([str(out/'profileit.o'),'-Wl,--wrap=lean_profileit',subprocess.check_output(['g++','-print-file-name=libstdc++.so'],text=True).strip(),'-lz','-pthread'])
commands=[compile,link];logs=[]
for cmd in commands:
 result=subprocess.run(cmd,cwd=original,text=True,capture_output=True)
 logs.append(dict(command=cmd,exit=result.returncode,stdout=result.stdout,stderr=result.stderr))
 (A/'build.json').write_text(json.dumps(dict(original=str(original/'.lake/build/bin/repl'),binary=str(out/'repl'),source=str(B/'profileit.cpp'),commands=logs,scope='Existing native objects relinked; runtime diagnostic wrapper only.'),indent=2)+'\n')
 if result.returncode:print(result.stderr);raise SystemExit(result.returncode)
print(out/'repl')
