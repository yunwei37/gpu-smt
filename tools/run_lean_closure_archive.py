#!/usr/bin/env python3
"""Run a changed CUDA checker on every retained independently checked real graph.

Development/error analysis only: source frontend outcomes come from the original
whole acquisition. This cannot measure complete candidate verification speed.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import zipfile


def main():
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--tool', type=Path, required=True)
    p.add_argument('--cpu-library', type=Path, required=True)
    p.add_argument('--ptx', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    counts = Counter()
    expected = 0
    process = None
    prefix_hash = None
    worker_count = 0
    command = None
    status = {'start_utc': datetime.now(timezone.utc).isoformat(),
              'archive': str(a.archive), 'actual_gpu_results_inferred': False,
              'scope': 'complete retained qualified graphs only; no source frontend/native acceptance or complete-verification performance measured',
              'sources': {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in (a.archive, a.tool, a.cpu_library, a.ptx)}}
    (a.out/'execution.json').write_text(json.dumps(status,indent=2)+'\n')
    (a.out/'executed-runner.py').write_bytes(Path(__file__).read_bytes())
    records_stream = (a.out/'returned.jsonl').open('x')
    stderr_stream = (a.out/'worker-stderr.bin').open('xb')

    def read():
        line = process.stdout.readline()
        if not line:
            raise RuntimeError('resident worker EOF before complete response')
        row = json.loads(line)
        records_stream.write(json.dumps(row)+'\n');records_stream.flush()
        return row

    def close_worker():
        nonlocal process
        if process is None:
            return
        process.stdin.close()
        terminal = read()
        remaining = process.stdout.read()
        if remaining:
            (a.out/f'worker-{worker_count}-trailing.bin').write_bytes(remaining)
        process.stdout.close()
        code = process.wait()
        if code != 0 or terminal.get('event') != 'worker_finished' or terminal.get('error') or terminal.get('candidate_errors') or terminal.get('device_error'):
            raise RuntimeError(f'resident worker failed at final EOF: {code}')
        process = None

    try:
        with zipfile.ZipFile(a.archive) as archive:
            label = a.archive.stem
            receipt = json.loads(archive.read(label+'/receipt.json'))
            rows = [json.loads(line) for line in archive.read(label+'/results.jsonl').splitlines()]
            if len(rows) != receipt['expected_inputs'] or receipt.get('signals'):
                raise RuntimeError('source acquisition incomplete or paused')
            prepared = {}
            for line in archive.read(label+'/events.jsonl').splitlines():
                row = json.loads(line)
                prefix = row.get('record',{}).get('backend_preparation')
                if prefix and prefix.get('prefix_verified'):
                    prepared[row['worker']] = prefix['declarations']
            for row in rows:
                counts['original_sources'] += 1
                counts['original_'+row['outcome']] += 1
                if row['outcome'] != 'complete':
                    continue
                if row.get('cached'):
                    counts['success_cache_hits'] += 1
                    continue
                value = row['record']['result']
                checked = (value.get('backend') or {}).get('checked') or {}
                if value.get('native_fallback') or checked.get('code') != 0:
                    counts['no_independently_checked_overlay'] += 1
                    continue
                expected += 1
                path = Path(checked['overlay'])
                relative = path.parts[path.parts.index(label)+1:]
                member = label+'/'+'/'.join(relative)+'.gz'
                prefix_member = str(Path(member).parent/'prefix.ndjson.gz')
                prefix_bytes = archive.read(prefix_member)
                digest = hashlib.sha256(prefix_bytes).hexdigest()
                if digest != prefix_hash:
                    close_worker()
                    prefix = a.out/f'prefix-{worker_count}.ndjson.gz'
                    prefix.write_bytes(prefix_bytes)
                    command = ['python3',str(a.tool), '--prefix',str(prefix),
                               '--first-declaration',str(prepared[row['worker']]),
                               '--cpu-library',str(a.cpu_library),'--ptx',str(a.ptx),
                               '--out',str(a.out/f'worker-{worker_count}')]
                    (a.out/f'worker-{worker_count}.command.json').write_text(json.dumps(command,indent=2)+'\n')
                    process = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                                               stderr=stderr_stream,text=True,bufsize=1)
                    worker_count += 1
                    ready = read()
                    if ready.get('event') != 'worker_ready' or ready.get('actual_gpu') is not True or not ready.get('ready'):
                        raise RuntimeError('resident worker did not become ready')
                    prefix_hash = digest
                overlay = a.out/f'source-{row["source_index"]}.ndjson.gz'
                overlay.write_bytes(archive.read(member))
                process.stdin.write(str(overlay.resolve())+'\n');process.stdin.flush()
                answer = read()
                if answer.get('actual_gpu') is not True:
                    raise RuntimeError('no actual CUDA result for retained source graph')
                if answer.get('error') or answer.get('cpu_cuda_bytes_equal') is not True:
                    raise RuntimeError('device execution/control failure; no qualified graph result')
                counts['actual_returned_graphs'] += 1
                counts['actual_verified_declarations'] += answer['verified_declarations']
                print(json.dumps({'source_index':row['source_index'],'actual_verified_declarations':answer['verified_declarations']}),flush=True)
            close_worker()
            if counts['actual_returned_graphs'] != expected:
                raise RuntimeError('actual graph population incomplete')
        status.update(finish_utc=datetime.now(timezone.utc).isoformat(),expected_graphs=expected,
                      counts=counts,normal_worker_eof=True,exit=0)
    except BaseException as error:
        status.update(finish_utc=datetime.now(timezone.utc).isoformat(),expected_graphs_so_far=expected,
                      counts=counts,error=repr(error),exit=1)
        if process is not None:
            process.stdin.close()
            remaining = process.stdout.read()
            (a.out/'failed-worker-trailing.bin').write_text(remaining)
            process.stdout.close()
            status['failed_worker_exit'] = process.wait()
        raise
    finally:
        records_stream.close();stderr_stream.close()
        (a.out/'terminal.json').write_text(json.dumps(status,indent=2)+'\n')


if __name__ == '__main__':
    main()
