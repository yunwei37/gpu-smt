"""Build the measured oracle source with a caller's Lean4.27 Mathlib project."""
from pathlib import Path
import argparse,concurrent.futures,json,os,shutil,subprocess,sys,threading
ROOT=Path(__file__).resolve().parent
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--mathlib",type=Path,required=True,help="Existing Mathlib4.27 project with its ordinary OLean cache")
 parser.add_argument("--out",type=Path,required=True,help="Separate build output; choose a directory unused by running verifiers")
 args=parser.parse_args()
 project=args.mathlib.resolve();out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
 lake=shutil.which("lake");cargo=shutil.which("cargo")
 if lake is None or cargo is None:raise RuntimeError("lake and cargo must be on PATH")
 base=json.loads(subprocess.check_output([lake,"env",sys.executable,"-c",'import os,json;print(json.dumps({k:os.environ.get(k,"")for k in["LEAN_PATH","LEAN_SRC_PATH"]}))'],cwd=project,text=True))
 sdk=Path(subprocess.check_output([lake,"env","lean","--print-prefix"],cwd=project,text=True).strip()).resolve()
 lean=sdk/"bin/lean";leanc=sdk/"bin/leanc"
 version=subprocess.check_output([str(lean),"--version"],text=True).strip()
 if"version 4.27."not in version:raise RuntimeError("This reproduction component targets Lean4.27: "+version)
 lib=out/"lean";lib.mkdir(exist_ok=True)
 source_root=(ROOT/"lean").resolve()
 env=dict(os.environ)
 env.update(base);env["LEAN_PATH"]=str(lib)+os.pathsep+base["LEAN_PATH"]
 env["LEAN_SRC_PATH"]=str(source_root)+os.pathsep+base["LEAN_SRC_PATH"]
 roots=sorted({Path(x).resolve()for x in env["LEAN_SRC_PATH"].split(os.pathsep)if x},key=lambda p:-len(str(p)))
 order=[];visited=set();modules={}
 def visit(source):
  source=source.resolve()
  if source in visited:return
  visited.add(source)
  if source.is_relative_to(sdk):return
  root=next((r for r in roots if source.is_relative_to(r)),None)
  if root is None:raise RuntimeError("Source root not exposed by Lake: "+str(source))
  name=".".join(source.relative_to(root).with_suffix("").parts)
  deps=subprocess.check_output([str(lean),"--src-deps",str(source)],cwd=project,env=env,text=True)
  for line in deps.splitlines():
   if line.strip():visit(Path(line.strip()))
  modules[name]=(source,root);order.append(name)
 for source in sorted(source_root.rglob("*.lean")):visit(source)
 lock=threading.Lock();commands=[]
 log=(out/"build.log").open("w")
 def run(argv):
  p=subprocess.run([str(x)for x in argv],cwd=project,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  with lock:
   commands.append({"argv":[str(x)for x in argv],"returncode":p.returncode,"output":p.stdout})
   log.write("$ "+repr([str(x)for x in argv])+"\n"+p.stdout+"\n");log.flush()
  if p.returncode:raise RuntimeError("Build command failed: "+repr(argv)+"\n"+p.stdout[-3000:])
 run([cargo,"build","--release","--locked","--manifest-path",ROOT/"native/Cargo.toml","--target-dir",out/"native-target"])
 for name in["arithmetic-batchd","farkas-batchd","farkas-race-worker"]:shutil.copy2(out/"native-target/release"/name,out/name)
 cdir=out/"c";cdir.mkdir(exist_ok=True)
 custom=[];dependencies=[]
 for name in order:
  source,root=modules[name]
  if source.is_relative_to(source_root):
   olean=lib/Path(*name.split(".")).with_suffix(".olean");olean.parent.mkdir(parents=True,exist_ok=True)
   cfile=cdir/(name+".c")
   run([lean,"--root="+str(source_root),"-o",olean,"-c",cfile,source]);custom.append(cfile)
  else:dependencies.append(name)
 dep_dir=out/"imports";dep_dir.mkdir(exist_ok=True)
 def native_dependency(name):
  source,root=modules[name]
  # Use ordinary generated C when present; otherwise regenerate into our output.
  cached=None
  for path in base["LEAN_PATH"].split(os.pathsep):
   olean=Path(path)/Path(*name.split(".")).with_suffix(".olean")
   if olean.exists()and"/lib/lean/"in str(olean):
    candidate=Path(str(olean).replace("/lib/lean/","/ir/")).with_suffix(".c")
    if candidate.exists():cached=candidate
    break
  cfile=cached or(cdir/(name+".c"))
  if cached is None:
   argv=[lean,"--root="+str(root)]
   if name.startswith("Mathlib."):
    # These are the typechecking options of Mathlib4.27's public lakefile.
    argv+=["-DautoImplicit=false","-DmaxSynthPendingDepth=3","-Dpp.unicode.fun=true"]
   run(argv+["-c",cfile,source])
  so=dep_dir/(name+".so")
  run([leanc,"-O3","-DLEAN_EXPORTING","-shared","-fPIC",cfile,"-o",so])
  return so
 jobs=len(os.sched_getaffinity(0))
 with concurrent.futures.ThreadPoolExecutor(max_workers=jobs)as pool:
  built=dict(zip(dependencies,pool.map(native_dependency,dependencies)))
 plugin=out/"batch-oracle.so"
 run([leanc,"-O3","-DLEAN_EXPORTING","-shared","-fPIC",*custom,ROOT/"c/clock.c",ROOT/"c/cost-emit.c","-lz","-o",plugin])
 libraries=[str(built[name])for name in order if name in built]+[str(plugin)]
 (out/"native-load.txt").write_text("\n".join(libraries)+"\n")
 record={"lean_version":version,"sdk":str(sdk),"mathlib":str(project),"lean_path":env["LEAN_PATH"],"lean_src_path":env["LEAN_SRC_PATH"],"libraries":libraries,"library_paths":[str(dep_dir),str(out),str(sdk/"lib"),str(sdk/"lib/lean")],"modules":[{"name":n,"source":str(modules[n][0])}for n in order],"commands":commands}
 (out/"build.json").write_text(json.dumps(record,indent=2)+"\n");log.close()
 print(json.dumps({"state":"complete","output":str(out),"native_dependency_modules":len(dependencies),"local_modules":len(custom),"lean":version}),flush=True)
if __name__=="__main__":main()
