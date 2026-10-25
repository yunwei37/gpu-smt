#!/usr/bin/env python3
"""Build engine-owned native glue against an existing pinned Lean/REPL project."""
from pathlib import Path
import argparse, json, os, subprocess

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project",type=Path,required=True)
    parser.add_argument("--sysroot",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    project=args.project.resolve(strict=True)
    sysroot=args.sysroot.resolve(strict=True)
    source=Path(__file__).resolve().parent
    args.out.mkdir(parents=True,exist_ok=False)
    out=args.out.resolve()
    archives=[project/".lake/build/lib/lean/libREPL.a",project/".lake/build/lib/libREPL.a"]
    archive=next((p for p in archives if p.is_file()),None)
    if archive is None:
        raise FileNotFoundError("build the pinned REPL project with lake build first")
    env=dict(os.environ,PATH=str(sysroot/"bin")+os.pathsep+os.environ["PATH"],
        LEAN_SYSROOT=str(sysroot))
    commands=[
        ["lake","env","lean","-R",str(source),"-c",str(out/"GpuSmtPrepared.c"),str(source/"GpuSmtPrepared.lean")],
        ["lake","env","leanc","-O3","-c",str(out/"GpuSmtPrepared.c"),"-o",str(out/"GpuSmtPrepared.o")],
        ["gcc","-std=gnu11","-O2","-Wall","-Wextra","-Werror","-I"+str(sysroot/"include"),
            "-c",str(source/"prepared_host.c"),"-o",str(out/"prepared_host.o")],
        ["lake","env","leanc","-O3","-rdynamic","-o",str(out/"prepared-host"),
            str(out/"prepared_host.o"),str(out/"GpuSmtPrepared.o"),str(archive)]]
    receipt={"cwd":str(project),"sysroot":str(sysroot),"commands":[]}
    try:
        for command in commands:
            result=subprocess.run(command,cwd=project,env=env,text=True,capture_output=True)
            receipt["commands"].append({"command":command,"exit":result.returncode,
                "stdout":result.stdout,"stderr":result.stderr})
            (out/"build.json").write_text(json.dumps(receipt,indent=2)+"\n")
            print(result.stdout,result.stderr,flush=True)
            result.check_returncode()
    finally:
        for name in ["GpuSmtPrepared.lean","prepared_host.c","build.py"]:
            (out/("source-"+name)).write_bytes((source/name).read_bytes())
if __name__=="__main__":
    main()
