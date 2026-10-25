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
    env=dict(os.environ,PATH=str(sysroot/"bin")+os.pathsep+os.environ["PATH"],
        LEAN_SYSROOT=str(sysroot))
    receipt={"cwd":str(project),"sysroot":str(sysroot),"commands":[]}
    def run(command):
        result=subprocess.run(command,cwd=project,env=env,text=True,capture_output=True)
        receipt["commands"].append({"command":command,"exit":result.returncode,
            "stdout":result.stdout,"stderr":result.stderr})
        (out/"build.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print(result.stdout,result.stderr,flush=True)
        result.check_returncode()
    try:
        # The default executable build does not necessarily produce the archive
        # needed for embedding. Ask the dependency's own static-library facet.
        run(["lake","build","REPL:static"])
        archives=list((project/".lake/build").rglob("libREPL.a"))
        if len(archives)!=1:
            raise FileNotFoundError(f"expected one built REPL static archive, found {archives}")
        # The upstream Main module exports an executable main as well as the
        # REPL library API. Rename only that entry symbol in a private archive;
        # never edit the dependency source or hide other duplicate definitions.
        embedded=out/"libREPL-embedded.a"
        run(["objcopy","--redefine-sym","main=gpu_smt_dependency_main",str(archives[0]),str(embedded)])
        commands=[
            ["lake","env","lean","-R",str(source),"-c",str(out/"GpuSmtPrepared.c"),str(source/"GpuSmtPrepared.lean")],
            ["lake","env","leanc","-O3","-c",str(out/"GpuSmtPrepared.c"),"-o",str(out/"GpuSmtPrepared.o")],
            ["gcc","-std=gnu11","-O2","-Wall","-Wextra","-Werror","-I"+str(sysroot/"include"),
                "-c",str(source/"prepared_host.c"),"-o",str(out/"prepared_host.o")],
            ["lake","env","leanc","-O3","-rdynamic","-o",str(out/"prepared-host"),
                str(out/"prepared_host.o"),str(out/"GpuSmtPrepared.o"),str(embedded)]]
        for command in commands:
            run(command)
    finally:
        for name in ["GpuSmtPrepared.lean","prepared_host.c","build.py"]:
            (out/("source-"+name)).write_bytes((source/name).read_bytes())
if __name__=="__main__":
    main()
