#!/usr/bin/env python3
"""Build the experimental Meta batch REPL without changing a live Lean install.

The provider is optional: an unlinked build is native fallback, not GPU evidence.
The upstream REPL must already be built with the same SDK as --defeq-c.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shlex
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("sdk", "repl", "defeq-c", "out"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--provider-object", type=Path, action="append", default=[])
    args = parser.parse_args()
    sdk, repl, original_c, out = (
        p.resolve() for p in (args.sdk, args.repl, args.defeq_c, args.out)
    )
    src = Path(__file__).resolve().parent
    trace = repl / ".lake/build/bin/repl.trace"
    messages = json.loads(trace.read_text())["log"]
    links = [
        shlex.split(row["message"][3:]) for row in messages
        if row.get("message", "").startswith(".> ")
        and " -o " in row["message"]
        and str(repl / ".lake/build/bin/repl") in row["message"]
    ]
    if len(links) != 1:
        raise ValueError("expected one native REPL link command in Lake trace")
    link = links[0]
    if Path(link[0]).resolve() != (sdk / "bin/clang").resolve():
        raise ValueError("REPL trace compiler and selected SDK differ")
    main_object = str(repl / ".lake/build/ir/REPL/Main.c.o.export")
    if link.count(main_object) != 1:
        raise ValueError("expected one original REPL Main object")
    original, replacements = re.subn(
        r"(LEAN_EXPORT lean_object\* )lean_is_expr_def_eq(\(lean_object\* x_1,)",
        r"\1gpu_meta_batch_original_defeq\2", original_c.read_text(),
    )
    if replacements != 1:
        raise ValueError("expected one exported equality definition in generated C")
    main_source = (repl / "REPL/Main.lean").read_text()
    imports = [i for i, line in enumerate(main_source.splitlines())
               if line.startswith("import ")]
    if not imports:
        raise ValueError("REPL Main has no module import boundary")
    lines = main_source.splitlines(keepends=True)
    lines.insert(imports[-1] + 1, "import NativeMetaBatch\n")
    out.mkdir(parents=True, exist_ok=False)
    (out / "src/REPL").mkdir(parents=True)
    (out / "lib/REPL").mkdir(parents=True)
    (out / "src/REPL/Main.lean").write_text("".join(lines))
    (out / "ExprDefEq-original.c").write_text(original)
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(
        (str(out), str(repl / ".lake/build/lib/lean"))
    ))
    records = []

    def run(name, command):
        log_path = out / (name + ".log")
        with log_path.open("w") as log:
            result = subprocess.run([str(x) for x in command], cwd=repl,
                                    env=env, stdout=log, stderr=log)
        records.append(dict(name=name, command=[str(x) for x in command],
                            returncode=result.returncode, log=str(log_path)))
        (out / "build-commands.json").write_text(json.dumps(records, indent=2) + "\n")
        result.check_returncode()

    lean, leanc = sdk / "bin/lean", sdk / "bin/leanc"
    run("module", [lean, "--root=" + str(src), "-c", out / "NativeMetaBatch.c",
                   "-o", out / "NativeMetaBatch.olean", src / "NativeMetaBatch.lean"])
    for name in ("NativeMetaBatch", "ExprDefEq-original"):
        run(name, [leanc, "-O3", "-DNDEBUG", "-fPIC", "-c", out / (name + ".c"),
                   "-o", out / (name + ".o")])
    run("hook", ["cc", "-O3", "-DNDEBUG", "-std=c11", "-fPIC",
                 "-Wall", "-Wextra", "-Werror", "-I", sdk / "include",
                 "-c", src / "meta-batch-native.c", "-o", out / "meta-batch-native.o"])
    run("main", [lean, "--root=" + str(out / "src"), "-c", out / "Main.c",
                 "-o", out / "lib/REPL/Main.olean", out / "src/REPL/Main.lean"])
    run("main-c", [leanc, "-O3", "-DNDEBUG", "-fPIC", "-c", out / "Main.c",
                   "-o", out / "Main.o"])
    link[link.index("-o") + 1] = str(out / "repl-meta-batch")
    link[link.index(main_object)] = str(out / "Main.o")
    link[3:3] = [str(out / (n + ".o")) for n in
                 ("NativeMetaBatch", "meta-batch-native", "ExprDefEq-original")]
    link[3:3] = [str(p.resolve()) for p in args.provider_object]
    run("link", link)
    print(json.dumps(dict(binary=str(out / "repl-meta-batch"),
                          provider_objects=[str(p.resolve()) for p in args.provider_object],
                          scope="build only; device engagement and performance unmeasured")))


if __name__ == "__main__":
    main()
