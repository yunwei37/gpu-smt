#!/usr/bin/env python3
"""Pack a real lean4export DAG for a scoped loose-bound-variable metadata pass.

No type inference, reduction or proof acceptance occurs here. Dense expression
indices and backward references are required by this experimental format.
"""
import argparse
from array import array
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys
import time

MAGIC = b"LBVDAG1\0"


def pack(source: Path, output: Path):
    if sys.byteorder != "little":
        raise RuntimeError("experimental format requires little endian host")
    start = time.perf_counter()
    nodes, levels, bounds, roots = array('I'), array('I'), array('I'), array('I')
    kinds = collections.Counter()
    digest = hashlib.sha256()
    with source.open('rb') as f:
        for line in f:
            digest.update(line)
            r = json.loads(line)
            if 'ie' in r:
                i = r['ie']
                if i != len(levels):
                    raise ValueError(f"expected dense fresh expression index {len(levels)}, got {i}")
                tag = next(k for k in r if k != 'ie')
                kinds[tag] += 1
                data = r[tag]
                children = []
                kind, a, b, c, imm = 0, 0, 0, 0, 0
                if tag == 'bvar':
                    kind, imm = 1, int(data)
                    if not 0 <= imm < (1 << 20)-1:
                        raise ValueError('bvar index outside validated Lean metadata range')
                elif tag == 'app':
                    kind, a, b = 2, data['fn'], data['arg']; children = [a, b]
                elif tag in ('lam', 'forallE'):
                    kind, a, b = 3, data['type'], data['body']; children = [a, b]
                elif tag == 'letE':
                    kind, a, b, c = 4, data['type'], data['value'], data['body']; children = [a, b, c]
                elif tag in ('proj', 'mdata'):
                    kind, a = 5, data['struct' if tag == 'proj' else 'expr']; children = [a]
                elif tag not in ('sort', 'const', 'natVal', 'strVal'):
                    raise ValueError(f'unsupported expression {tag}')
                if any(not isinstance(j, int) or j < 0 or j >= i for j in children):
                    raise ValueError('invalid or forward expression reference')
                level = max((levels[j]+1 for j in children), default=0)
                value = {0: lambda: 0, 1: lambda: imm+1,
                         2: lambda: max(bounds[a], bounds[b]),
                         3: lambda: max(bounds[a], max(0, bounds[b]-1)),
                         4: lambda: max(bounds[a], bounds[b], max(0, bounds[c]-1)),
                         5: lambda: bounds[a]}[kind]()
                nodes.extend([kind, a, b, c, imm]); levels.append(level); bounds.append(value)
            else:
                for tag in ('def', 'thm', 'opaque', 'axiom', 'quot'):
                    if tag in r:
                        roots.extend(r[tag][k] for k in ('type', 'value') if k in r[tag])
                if 'inductive' in r:
                    for tag in ('types', 'ctors', 'recs'):
                        for entry in r['inductive'][tag]:
                            roots.append(entry['type'])
    parsed = time.perf_counter()
    n = len(levels)
    if not n:
        raise ValueError('no expressions')
    widths = collections.Counter(levels)
    offsets = array('I', [0])
    for l in range(max(levels)+1): offsets.append(offsets[-1]+widths[l])
    cursors = array('I', offsets[:-1]); order = array('I', [0])*n
    for i, l in enumerate(levels):
        order[cursors[l]] = i; cursors[l] += 1
    with output.open('wb') as f:
        f.write(struct.pack('<8sIIII', MAGIC, n, len(offsets)-1, len(roots), 0))
        for a in (nodes, order, offsets, roots): a.tofile(f)
    with output.with_suffix('.python-reference.bin').open('wb') as f:
        bounds.tofile(f)
    record = dict(input=str(source.resolve()), input_sha256=digest.hexdigest(),
                  input_bytes=source.stat().st_size, expressions=n, expression_kinds=dict(kinds),
                  levels=len(offsets)-1, level_widths=[widths[l] for l in range(len(offsets)-1)],
                  roots=len(roots), closed_roots=sum(bounds[r]==0 for r in roots),
                  max_bound=max(bounds), parse_and_pack_values_s=parsed-start,
                  schedule_and_write_s=time.perf_counter()-parsed,
                  packed_bytes=output.stat().st_size,
                  packed_sha256=hashlib.sha256(output.read_bytes()).hexdigest())
    output.with_suffix('.json').write_text(json.dumps(record,indent=1)+'\n')
    return record


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path); ap.add_argument('output', type=Path)
    args = ap.parse_args()
    print(json.dumps(pack(args.input, args.output)))
