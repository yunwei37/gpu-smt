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
    # POSIX APIs need full platform headers, absent from the minimal SDK sysroot.
    # Upstream supports LEAN_CC and removes bundled sysroot flags for that mode.
    env.setdefault("LEAN_CC","cc")
    receipt={"cwd":str(project),"sysroot":str(sysroot),"LEAN_CC":env["LEAN_CC"],"commands":[]}
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
        runtime=sysroot/"lib/lean/libleanrt.a"
        symbols=subprocess.run(["nm","-g","--defined-only",str(runtime)],
            text=True,capture_output=True,check=True)
        defer_uv=any(line.split() and line.split()[-1]=="initialize_libuv" for line in symbols.stdout.splitlines())
        receipt["libuv_initializer_present"]=defer_uv
        (out/"build.json").write_text(json.dumps(receipt,indent=2)+"\n")
        compile_flags=["-DGPU_SMT_DEFER_LIBUV=1"] if defer_uv else []
        link_flags=["-Wl,--wrap=initialize_libuv"] if defer_uv else []
        commands=[
            ["lake","env","lean","-R",str(source),"-c",str(out/"GpuSmtPrepared.c"),str(source/"GpuSmtPrepared.lean")],
            ["lake","env","leanc","-O3","-c",str(out/"GpuSmtPrepared.c"),"-o",str(out/"GpuSmtPrepared.o")],
            ["lake","env","leanc","-std=gnu11","-O2","-Wall","-Wextra","-Werror"]+compile_flags+[
                "-c",str(source/"prepared_host.c"),"-o",str(out/"prepared_host.o")],
            ["lake","env","leanc","-O3","-rdynamic","-L"+str(sysroot/"lib"),"-o",str(out/"prepared-host"),
                str(out/"prepared_host.o"),str(out/"GpuSmtPrepared.o"),str(embedded)]+link_flags]
        for command in commands:
            run(command)
    finally:
        for name in ["GpuSmtPrepared.lean","prepared_host.c","build.py"]:
            (out/("source-"+name)).write_bytes((source/name).read_bytes())
if __name__=="__main__":
    main()
