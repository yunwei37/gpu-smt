#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build the experimental Lean 4.27 Linux native branches and stock comparator.

Inputs are an unmodified Lean source tree, its matching official binary SDK,
a built matching GC REPL, and the libc++/mimalloc source headers used by Lean.
This is a source build command, not a benchmark or persistent service.
"""
from pathlib import Path
import argparse
import datetime
import json
import os
import re
import resource
import shlex
import shutil
import subprocess
import sys
import sysconfig
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lean-source", type=Path, required=True,
                    help="unmodified Lean 4.27 source tree")
    ap.add_argument("--repl", type=Path, required=True,
                    help="matching GC REPL tree after lake build repl")
    ap.add_argument("--libcxx-headers", type=Path, required=True,
                    help="libc++ 19 include directory (SDK lacks these headers)")
    ap.add_argument("--mimalloc-source", type=Path, required=True,
                    help="Lean's mimalloc v2.2.3 source tree")
    ap.add_argument("--output", type=Path, required=True,
                    help="new build directory; existing builds are never overwritten")
    ap.add_argument("--sysroot", type=Path,
                    help="matching Lean binary SDK; otherwise discover with lean --print-prefix")
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    repl = args.repl.resolve()
    sdk = (args.sysroot.resolve() if args.sysroot else
           Path(subprocess.check_output(["lean", "--print-prefix"], cwd=repl, text=True).strip()))
    source = args.lean_source.resolve()
    libcxx = args.libcxx_headers.resolve()
    mimalloc = args.mimalloc_source.resolve()
    out = args.output.resolve()
    # The SDK's own generated headers remain authoritative for ABI/configuration.
    for path in [source / "src/runtime/CMakeLists.txt", sdk / "include/lean/lean.h",
                 libcxx / "__config", mimalloc / "src/static.c",
                 repl / ".lake/build/bin/repl.trace",
                 repl / ".lake/build/ir/REPL/Main.c"]:
        if not path.is_file():
            ap.error(f"missing build input: {path}")
    out.mkdir(parents=True, exist_ok=False)
    plain = out / "plain"
    private = out / "private"
    for directory in [plain, private, out / "logs", out / "implementation"]:
        directory.mkdir()
    for name in ["native-ref-branches.cpp", "native-ref-branches.h",
                 "native-ref-branches.patch", "NativeBranchBackend.lean"]:
        shutil.copyfile(here / name, out / "implementation" / name)
    patched = out / "lean-private"
    shutil.copytree(source / "src", patched / "src")
    env = dict(os.environ)
    env["LEAN_PATH"] = str(repl / ".lake/build/lib/lean")
    log = (out / "commands.jsonl").open("w")

    def run(tag, command, cwd=out):
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        tick = time.monotonic()
        utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        with (out / "logs" / (tag + ".stdout")).open("wb") as stdout:
            with (out / "logs" / (tag + ".stderr")).open("wb") as stderr:
                result = subprocess.run([str(v) for v in command], cwd=cwd, env=env,
                                        stdout=stdout, stderr=stderr)
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        log.write(json.dumps({"stage": tag, "command": [str(v) for v in command],
                              "cwd": str(cwd), "utc": utc,
                              "seconds": time.monotonic() - tick,
                              "compiler_cpu_seconds": after.ru_utime + after.ru_stime -
                              before.ru_utime - before.ru_stime,
                              "exit_code": result.returncode}) + "\n")
        log.flush()
        print(tag, result.returncode, flush=True)
        if result.returncode:
            raise RuntimeError(f"{tag} failed; see {out / 'logs' / (tag + '.stderr')}")

    try:
        run("runtime-patch", ["patch", "-p1", "--batch", "-i",
                             out / "implementation/native-ref-branches.patch"], patched)
        common = [sdk / "bin/clang", "-x", "c++", "-std=c++17", "-O3", "-fPIC",
                  "-ftls-model=initial-exec", "-nostdinc", "-nostdinc++",
                  "-isystem", libcxx, "-isystem", sdk / "include/clang",
                  "-isystem", Path("/usr/include") / sysconfig.get_config_var("MULTIARCH"),
                  "-isystem", "/usr/include", "-DLEAN_MULTI_THREAD", "-DLEAN_USE_GMP",
                  "-DLEAN_EXPORTING", "-DNDEBUG", "-I" + str(sdk / "include"),
                  "-I" + str(source / "src"), "-I" + str(out / "implementation"),
                  "-I" + str(mimalloc / "include")]
        static_cpp = ["-Wl,-Bstatic", "-lc++", "-lc++abi", "-lunwind", "-Wl,-Bdynamic"]
        run("helper", common + ["-shared", out / "implementation/native-ref-branches.cpp",
                                "-L" + str(sdk / "lib"), "-Wl,-Bsymbolic"] + static_cpp +
            ["-lpthread", "-Wl,-soname,libgpu_smt_ref_branches.so", "-o",
             private / "libgpu_smt_ref_branches.so"])
        text = (source / "src/runtime/CMakeLists.txt").read_text()
        sources = re.search(r"set\(RUNTIME_OBJS\s+(.*?)\)", text, re.S).group(1).split()
        for directory in [out / "plain-objects", out / "private-objects"]:
            directory.mkdir()
        plain_objects = []
        private_objects = []
        changed = {"io.cpp", "object.cpp", "process.cpp", "compact.cpp"}
        for name in sources:
            obj = out / "plain-objects" / (name + ".o")
            run("plain-" + name, common + ["-c", source / "src/runtime" / name, "-o", obj])
            plain_objects.append(obj)
            if name in changed:
                replacement = out / "private-objects" / (name + ".o")
                run("private-" + name, common + ["-I" + str(patched / "src"),
                                                "-c", patched / "src/runtime" / name,
                                                "-o", replacement])
                private_objects.append(replacement)
            else:
                private_objects.append(obj)
        mi = out / "plain-objects/static.c.o"
        run("mimalloc", common + ["-DMI_SHARED_LIB", "-DMI_SHARED_LIB_EXPORT",
                                  "-DMI_WIN_NOREDIRECT", "-c", mimalloc / "src/static.c",
                                  "-o", mi])
        plain_objects.append(mi)
        private_objects.append(mi)
        shell = out / "shell.cpp.o"
        run("shell", common + ["-c", source / "src/util/shell.cpp", "-o", shell])
        for target, objects in [(plain, plain_objects), (private, private_objects)]:
            run(target.name + "-archive",
                [sdk / "bin/llvm-ar", "rcs", target / "libleanrt.a"] + objects)
            command = [sdk / "bin/clang", "-shared", "-fuse-ld=lld", "-o",
                       target / "libleanshared.so", "-Wl,-soname,libleanshared.so",
                       "-Wl,-Bsymbolic", "-Wl,--whole-archive"]
            command += [sdk / "lib/lean" / name for name in
                        ["libLean.a", "libStd.a", "libInit.a", "libleancpp.a"]]
            command += objects + [shell, "-Wl,--no-whole-archive"]
            if target == private:
                command += ["-L" + str(private), "-lgpu_smt_ref_branches"]
            command += ["-L" + str(sdk / "lib"), "-Wl,-Bstatic", "-lc++", "-lc++abi",
                        "-lunwind", "-lgmp", "-luv", "-Wl,-Bdynamic", "-lpthread",
                        "-ldl", "-lm", "-lrt", "-Wl,-rpath," + str(target)]
            run(target.name + "-shared", command)
        backend = out / "implementation/NativeBranchBackend.lean"
        run("backend-lean", [sdk / "bin/lean", "-o", out / "NativeBranchBackend.olean",
                             "-c", out / "NativeBranchBackend.c", backend])
        run("backend-c", [sdk / "bin/leanc", "-c", "-O3", out / "NativeBranchBackend.c",
                          "-o", out / "NativeBranchBackend.o"])
        entry = (repl / ".lake/build/ir/REPL/Main.c").read_text()
        old_init = "res = initialize_REPL_REPL_Main(1 /* builtin */);"
        old_main = "res = _lean_main(in);"
        if entry.count(old_init) != 1 or entry.count(old_main) != 1:
            raise RuntimeError("unsupported GC REPL generated entry point")
        entry = entry.replace("char ** lean_setup_args(int argc, char ** argv);",
                              "extern lean_object* initialize_NativeBranchBackend(uint8_t builtin);\n"
                              "extern lean_object* gpu_smt_native_backend(lean_object*);\n"
                              "char ** lean_setup_args(int argc, char ** argv);")
        entry = entry.replace(old_init, "res = initialize_NativeBranchBackend(1 /* builtin */);")
        entry = entry.replace(old_main, "res = gpu_smt_native_backend(in);")
        (out / "Main.setup.c").write_text(entry)
        run("entry", [sdk / "bin/leanc", "-c", "-O3", out / "Main.setup.c",
                       "-o", out / "Main.setup.o"])
        trace = json.loads((repl / ".lake/build/bin/repl.trace").read_text())
        message = next(x["message"] for x in trace["log"] if x["message"].startswith("cc "))
        original = shlex.split(message[3:])
        for target in [plain, private]:
            command = list(original)
            command[command.index("-o") + 1] = str(target / "repl")
            command[command.index("-lleanrt")] = str(target / "libleanrt.a")
            if target == private:
                main_object = next(v for v in command if v.endswith("/REPL/Main.c.o.export"))
                command[command.index(main_object)] = str(out / "Main.setup.o")
                command.insert(command.index("-rdynamic"), str(out / "NativeBranchBackend.o"))
                command.insert(command.index("-L"), "-L" + str(private))
            first, last = command.index("--sysroot"), command.index("-fuse-ld=lld")
            command[first:last] = ["-L" + str(sdk / "lib")]
            command.insert(command.index("-lc++abi") + 1, "-lunwind")
            command += ["-Wl,-rpath," + str(target), "-Wl,-rpath," + str(sdk / "lib")]
            if target == private:
                command += ["-L" + str(private), "-lgpu_smt_ref_branches"]
            run(target.name + "-repl", command)
        print("Build complete:", out, flush=True)
        print("Set LD_LIBRARY_PATH to the chosen plain/private directory and SDK lib; "
              "use the existing native-library manifest for Mathlib native loading.")
    finally:
        log.close()


if __name__ == "__main__":
    main()
