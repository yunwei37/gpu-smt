#!/usr/bin/env python3
"""Run original bytes through release/source CLI and lazy/eager native frontend."""
import argparse
import hashlib
import json
import os
import signal
from pathlib import Path
import subprocess
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from analyze_smt_trace import split_commands, command_head


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def version(binary):
    proc = subprocess.run([str(binary.resolve()), '-version'], capture_output=True, text=True, start_new_session=True)
    return dict(stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('run_dir', type=Path)
    for name in ('release', 'source', 'driver', 'out'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--repeat', type=int, default=3)
    p.add_argument('--cores', default='8')
    p.add_argument('--index', type=int, help='Separate real preflight original index')
    a = p.parse_args()
    if a.repeat < 1: p.error('positive repetitions required')
    a.out = a.out.resolve()
    a.out.mkdir(parents=True, exist_ok=False)
    cores = set()
    for part in a.cores.split(','):
        limits = [int(v) for v in part.split('-')]
        cores.update(range(limits[0], limits[-1] + 1))
    inputs = a.out / 'inputs'
    inputs.mkdir()
    jobs = []
    for trace in sorted(a.run_dir.glob('*.original'), key=lambda t: int(t.stem)):
        jobs.append(dict(index=int(trace.stem), trace=str(trace.resolve())))
    if not jobs: raise ValueError('no original streams')
    if a.index is not None: jobs = [j for j in jobs if j['index'] == a.index]
    if not jobs: raise ValueError('requested original index absent')
    for job in jobs:
        source = Path(job['trace'])
        path = inputs / (str(job['index']) + '.smt2')
        path.write_bytes(source.read_bytes())
        commands = split_commands(source.read_text())
        job.update(input=str(path.relative_to(a.out)), sha256=sha(path),
                   checks=[i for i, c in enumerate(commands) if command_head(c) in ('check-sat', 'check-sat-assuming')],
                   requests=[dict(command_index=i, head=command_head(c), command=c) for i, c in enumerate(commands) if command_head(c).startswith('get-')], responses=[dict(command_index=i, head=command_head(c), command=c) for i,c in enumerate(commands) if command_head(c) in ('check-sat','check-sat-assuming') or command_head(c).startswith('get-')])
    (a.out / 'jobs.json').write_text(json.dumps(jobs, indent=2) + '\n')
    files = [a.release, a.source, a.driver, Path(__file__), Path(__file__).with_name('native_z3_frontend.cpp'), Path(__file__).resolve().parents[1] / 'tools/analyze_smt_trace.py', Path(__file__).resolve().parents[1] / 'tools/analyze_native_frontend_probe.py']
    (a.out / 'provenance.json').write_text(json.dumps(dict(argv=sys.argv, hashes={str(f.resolve()): sha(f) for f in files}, repetitions=a.repeat, modes=['release', 'source', 'lazy', 'eager'], indices=[j['index'] for j in jobs], requested_cores=a.cores, versions={name: version(binary) for name,binary in [('release',a.release),('source',a.source)]}, affinity=sorted(os.sched_getaffinity(0)), cpu_topology=subprocess.check_output(['lscpu'], text=True), load_before=Path('/proc/loadavg').read_text()), indent=2) + '\n')
    with (a.out / 'processes.jsonl').open('w') as rows:
        for repeat in range(a.repeat):
            modes = ['release', 'source', 'lazy', 'eager']
            if repeat % 2: modes.reverse()
            for mode in modes:
                folder = a.out / f'{mode}-{repeat}'
                folder.mkdir()
                print(f'repeat={repeat} mode={mode} streams={len(jobs)}', flush=True)
                for job in jobs:
                    n = str(job['index'])
                    command = ['taskset', '-c', a.cores]
                    command += [str(a.release.resolve() if mode == 'release' else a.source.resolve()), '-in', '-smt2'] if mode in ('release', 'source') else [str(a.driver.resolve()), mode]
                    begin = time.perf_counter()
                    with (a.out / job['input']).open('rb') as stdin, (folder / (n + '.stdout')).open('wb') as stdout, (folder / (n + '.stderr')).open('wb') as stderr:
                        proc = subprocess.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr, start_new_session=True, preexec_fn=lambda: os.sched_setaffinity(0, cores))
                        try:
                            actual_affinity = sorted(os.sched_getaffinity(proc.pid))
                        except ProcessLookupError:
                            actual_affinity = None
                        try:
                            proc.wait()
                        except BaseException:
                            try:
                                os.killpg(proc.pid, signal.SIGTERM)
                                proc.wait(timeout=5)
                            except subprocess.TimeoutExpired:
                                os.killpg(proc.pid, signal.SIGKILL)
                                proc.wait()
                            except ProcessLookupError:
                                proc.wait()
                            raise
                    rows.write(json.dumps(dict(repeat=repeat, mode=mode, index=job['index'], command=command, input=job['input'], stdout=str((folder / (n + '.stdout')).relative_to(a.out)), stderr=str((folder / (n + '.stderr')).relative_to(a.out)), actual_affinity=actual_affinity, terminal=True, returncode=proc.returncode, seconds=time.perf_counter()-begin)) + '\n')
                    rows.flush()

    (a.out / 'completion.json').write_text(json.dumps(dict(terminal=True, completed_processes=a.repeat * 4 * len(jobs), repetitions=a.repeat, load_after=Path('/proc/loadavg').read_text()), indent=2) + '\n')

if __name__ == '__main__': main()
