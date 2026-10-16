#!/usr/bin/env python3
"""Error analysis of retained complete formal witnesses with the frozen CPU clone.

This reuses an independently checked whole acquisition. It does not generate
candidates, call CUDA, measure GPU performance, or accept any new proof.
"""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import struct
import sys
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'bench'))
from lean_gpu_check import load_graph, cpu_run


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--cpu-library', type=Path, required=True)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--closure-adapter', type=Path, help='isolated changed closure implementation; no CUDA execution')
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    (a.out / 'executed-analysis.py').write_bytes(Path(__file__).read_bytes())
    graph_loader, runner = load_graph, cpu_run
    if a.closure_adapter:
        spec = importlib.util.spec_from_file_location('closure_adapter', a.closure_adapter)
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        graph_loader, runner = adapter.load_graph, adapter.cpu_run
        (a.out / 'executed-adapter.py').write_bytes(a.closure_adapter.read_bytes())
    (a.out / 'executed-checker.cu').write_bytes(a.source.read_bytes())
    counters = Counter()
    reasons = Counter()
    prefix_digest = None
    state = None
    rows = a.out / 'declarations.jsonl'
    with zipfile.ZipFile(a.archive) as archive, rows.open('x') as output:
        label = a.archive.stem
        receipt = json.loads(archive.read(label + '/receipt.json'))
        records = [json.loads(line) for line in archive.read(label + '/results.jsonl').splitlines()]
        if len(records) != receipt['expected_inputs'] or receipt.get('signals'):
            raise RuntimeError('whole acquisition is not complete and unpaused')
        prepared = {}
        for line in archive.read(label + '/events.jsonl').splitlines():
            event = json.loads(line)
            prefix = event.get('record', {}).get('backend_preparation')
            if prefix and prefix.get('prefix_verified'):
                prepared[event['worker']] = prefix['declarations']
        for record in records:
            counters['original_sources'] += 1
            counters['original_' + record['outcome']] += 1
            if record['outcome'] != 'complete':
                continue
            if record.get('cached'):
                counters['success_cache_hits'] += 1
                continue
            value = record['record']['result']
            checked = (value.get('backend') or {}).get('checked') or {}
            if value.get('native_fallback') or checked.get('code') != 0:
                counters['no_independent_overlay'] += 1
                continue
            overlay_path = Path(checked['overlay'])
            relative = overlay_path.parts[overlay_path.parts.index(label)+1:]
            member = label + '/' + '/'.join(relative) + '.gz'
            prefix_member = str(Path(member).parent / 'prefix.ndjson.gz')
            compressed = archive.read(prefix_member)
            digest = sha(compressed)
            first = prepared[record['worker']]
            if digest != prefix_digest:
                stage = a.out / 'retained-prefix-copy.ndjson.gz'
                stage.write_bytes(compressed)
                _, meta, state = graph_loader([stage], 0 if a.closure_adapter else first, return_state=True)
                if meta['nd'] != first:
                    raise RuntimeError('import prefix boundary differs')
                stage.unlink()  # unchanged unique source remains in original ZIP
                prefix_digest = digest
                counters['prefix_conversions'] += 1
            overlay = archive.read(member)
            stage = a.out / 'retained-overlay-copy.ndjson.gz'
            stage.write_bytes(overlay)
            graph, meta = graph_loader([stage], first, base=state)
            if a.closure_adapter:
                answer_rows = runner(graph, meta, a.cpu_library)
            else:
                answer, _ = runner(graph, meta, 65536, a.cpu_library)
                answer_rows = [dict(declaration, verified=bool(result[0]), reason=result[1],
                                    steps=result[2], terms=result[3])
                               for declaration, result in zip(meta['declarations'], struct.iter_unpack('<IIII', answer))]
            stage.unlink()  # original ZIP remains the unique retained evidence
            declarations = []
            for result in answer_rows:
                declaration = {key:value for key,value in result.items() if key in ('index','serialized_name','name','kind','universe_parameters')}
                verified, reason, steps, nodes = result['verified'], result['reason'], result['steps'], result['terms']
                row = dict(declaration, source_index=record['source_index'],
                           verified=bool(verified), fallback_reason=reason,
                           steps=steps, working_nodes=nodes,
                           original_overlay_member=member,
                           compressed_overlay_sha256=sha(overlay),
                           compressed_prefix_sha256=digest)
                output.write(json.dumps(row) + '\n')
                declarations.append(bool(verified))
                counters['declarations'] += 1
                counters['cpu_clone_verified_declarations'] += bool(verified)
                reasons[str(reason)] += 1
            counters['independently_checked_source_graphs'] += 1
            counters['all_declarations_cpu_clone_verified_sources'] += bool(declarations) and all(declarations)
            counters['some_declarations_cpu_clone_verified_sources'] += any(declarations)
            output.flush()
            print(json.dumps({'source_index': record['source_index'], 'declarations': len(declarations),
                              'verified': sum(declarations)}), flush=True)
    result = dict(counters=counters, fallback_reasons=reasons,
                  original_archive=str(a.archive), original_archive_sha256=sha(a.archive.read_bytes()),
                  cpu_library=str(a.cpu_library), cpu_library_sha256=sha(a.cpu_library.read_bytes()),
                  checker_source=str(a.source), checker_source_sha256=sha(a.source.read_bytes()),
                  closure_adapter=str(a.closure_adapter) if a.closure_adapter else None,
                  closure_adapter_sha256=sha(a.closure_adapter.read_bytes()) if a.closure_adapter else None,
                  capacity=65536, actual_gpu_execution=False,
                  scope='full retained accepted ProofNet source graphs; fixed CPU clone algorithm coverage only, not GPU coverage/speedup or complete original benchmark performance',
                  limitations='Rejected/incomplete sources produce no witness. Success cache hits reuse original results. Numeric fallback codes may mask earlier errors. CUDA resource/stack feasibility is not measured.')
    (a.out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
