"""Wrap the official Farkas/DeepSeek proof corpus for the existing HTTP comparison.
Original proof payloads remain outside the repository; retain the official
replay_live.py source used for its strip_imports operation.
"""
import argparse
import collections
import json
from pathlib import Path
import runpy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--official-replayer", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source-paths", type=Path, required=True)
    args = parser.parse_args()
    strip_imports = runpy.run_path(str(args.official_replayer))["strip_imports"]
    files = sorted(args.source_root.glob("*/*.lean"))
    if len(files) != 438:
        raise ValueError(f"Published reference has438files; observed{len(files)}. Record source drift.")
    rows, paths, imports = [], [], collections.Counter()
    for source in files:
        text = source.read_text()
        declarations = [line for line in text.splitlines() if line.startswith("import ")]
        if not set(declarations) <= {"import Mathlib", "import Aesop"}:
            raise ValueError(f"Common-header protocol does not retain imports from{source}")
        imports.update(declarations)
        ident = str(source.relative_to(args.source_root))
        rows.append({"proof_id": ident, "code": "import Mathlib\nimport Aesop\n" + strip_imports(text)})
        paths.append({"proof_id": ident, "source_bytes": source.stat().st_size, "imports": declarations})
    # Refuse accidental replacement of an active experiment's inputs.
    with args.out.open("x") as stream:
        stream.write("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))
    with args.source_paths.open("x") as stream:
        stream.write(json.dumps(paths, indent=2) + "\n")
    print(json.dumps({"sources": len(rows), "producer_imports": dict(imports)}))


if __name__ == "__main__":
    main()
