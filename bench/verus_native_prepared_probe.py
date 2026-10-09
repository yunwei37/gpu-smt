#!/usr/bin/env python3
"""Replay retained native SMT input bytes across prepared-context boundaries."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from analyze_smt_trace import split_commands, command_head

MODES = ['source', 'fresh', 'split', 'branch', 'reverse', 'cancel']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('retained', type=Path)
    for name in ('source', 'driver', 'out'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--repeat', type=int, default=3)
    p.add_argument('--cores', default='8')
    p.add_argument('--index', type=int, help='Single original real stream for preflight')
    a = p.parse_args()
    if a.repeat < 1:
        p.error('positive repetitions required')
    a.out = a.out.resolve()
    a.out.mkdir(parents=True, exist_ok=False)
    cores = set()
    for part in a.cores.split(','):
        limits = [int(v) for v in part.split('-')]
        cores.update(range(limits[0], limits[-1] + 1))
    retained = a.retained.resolve()
    old = [json.loads(s) for s in (retained / 'decisions.jsonl').read_text().splitlines()]
    old = [r for r in old if r['mode'] == 'branch' and r['repeat'] == 0]
    inputs = a.out / 'inputs'
    inputs.mkdir()
    jobs = []
    for row in sorted(old, key=lambda r: r['index']):
        i = row['index']
        group = Path(row['output']).parent.name
        original = retained / 'inputs' / f'{i}.original'
        commands = split_commands(original.read_text())  # observation only
        job = dict(index=i, group=group, checks=[n for n, c in enumerate(commands)
                   if command_head(c) in ('check-sat', 'check-sat-assuming')],
                   responses=[dict(command_index=n, head=command_head(c), command=c)
                   for n, c in enumerate(commands) if command_head(c) in
                   ('check-sat', 'check-sat-assuming') or command_head(c).startswith('get-')])
        for kind in ('original', 'full', 'suffix'):
            source = retained / 'inputs' / f'{i}.{kind}'
            job[kind] = f'inputs/{i}.{kind}'
            job[kind + '_sha256'] = sha(source)
            job[kind + '_bytes'] = source.stat().st_size
        prefix = retained / 'inputs' / f'{group}.prefix'
        if prefix.read_bytes() + (retained / 'inputs' / f'{i}.suffix').read_bytes() != (retained / 'inputs' / f'{i}.full').read_bytes():
            raise ValueError(f'retained concatenation differs at {i}')
        jobs.append(job)
    groups = sorted({j['group'] for j in jobs})
    # Select without consulting solver outputs: most checks, then largest
    # suffix, then lowest original index. Selection uses the complete corpus.
    cancel_jobs = {g: max((j for j in jobs if j['group'] == g),
                         key=lambda j: (len(j['checks']), j['suffix_bytes'], -j['index'])) for g in groups}
    if a.index is not None:
        jobs = [j for j in jobs if j['index'] == a.index]
    if not jobs:
        raise ValueError('no selected original streams')
    groups = sorted({j['group'] for j in jobs})
    for job in jobs + [cancel_jobs[g] for g in groups]:
        for kind in ('original', 'full', 'suffix'):
            shutil.copyfile(retained / job[kind], a.out / job[kind])
    for group in groups:
        shutil.copyfile(retained / 'inputs' / f'{group}.prefix', inputs / f'{group}.prefix')
    (a.out / 'jobs.json').write_text(json.dumps(jobs, indent=2) + '\n')
    files = [a.source, a.driver, Path(__file__), Path(__file__).with_name('native_z3_prepared.cpp'),
             Path(__file__).resolve().parents[1] / 'tools/analyze_native_prepared_probe.py',
             Path(__file__).resolve().parents[1] / 'tools/analyze_native_frontend_probe.py',
             Path(__file__).resolve().parents[1] / 'tools/analyze_smt_trace.py']
    version = subprocess.run([str(a.source.resolve()), '-version'], capture_output=True, text=True)
    provenance = dict(argv=sys.argv, hashes={str(f.resolve()): sha(f) for f in files},
                      repetitions=a.repeat, modes=MODES, indices=[j['index'] for j in jobs],
                      cancel_selection={g: cancel_jobs[g] for g in groups},
                      requested_cores=a.cores, affinity_before=sorted(os.sched_getaffinity(0)),
                      cpu_topology=subprocess.check_output(['lscpu'], text=True),
                      version=dict(stdout=version.stdout, stderr=version.stderr, returncode=version.returncode),
                      prefix_hashes={g: sha(inputs / f'{g}.prefix') for g in groups},
                      load_before=Path('/proc/loadavg').read_text())
    (a.out / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    launch_count = 0
    with (a.out / 'launches.jsonl').open('w') as launches, (a.out / 'processes.jsonl').open('w') as cells, (a.out / 'cancellations.jsonl').open('w') as cancellations:
        def launch(command, directory, stdin_path=None):
            nonlocal launch_count
            directory.mkdir(parents=True, exist_ok=False)
            begin = time.perf_counter()
            with (stdin_path.open('rb') if stdin_path else open(os.devnull, 'rb')) as stdin, (directory / 'launcher.stdout').open('wb') as stdout, (directory / 'launcher.stderr').open('wb') as stderr:
                proc = subprocess.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr,
                                        start_new_session=True, preexec_fn=lambda: os.sched_setaffinity(0, cores))
                try:
                    actual = sorted(os.sched_getaffinity(proc.pid))
                except ProcessLookupError:
                    actual = None
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
            row = dict(command=command, directory=str(directory.relative_to(a.out)), returncode=proc.returncode,
                       actual_affinity=actual, seconds=time.perf_counter() - begin, terminal=True)
            launches.write(json.dumps(row) + '\n'); launches.flush()
            launch_count += 1
            return row

        def emit(job, mode, repeat, directory, name, launch_row, prefix=False):
            costs = {}
            if (directory / 'cost.tsv').exists():
                with (directory / 'cost.tsv').open() as stream:
                    costs = {r['name']: r for r in csv.DictReader(stream, delimiter='\t')}
            cost = costs.get(mode if mode in ('fresh', 'split') else name)
            stdout = directory / (name + '.stdout')
            stderr = directory / (name + '.stderr')
            if mode == 'source':
                stdout, stderr = directory / 'launcher.stdout', directory / 'launcher.stderr'
            elif prefix and stdout.exists() and stderr.exists():
                combined_out = directory / (name + '.combined.stdout')
                combined_err = directory / (name + '.combined.stderr')
                combined_out.write_bytes((directory / 'prefix.stdout').read_bytes() + stdout.read_bytes())
                combined_err.write_bytes((directory / 'prefix.stderr').read_bytes() + stderr.read_bytes())
                stdout, stderr = combined_out, combined_err
            rc = launch_row['returncode'] if mode == 'source' else (int(cost['exit_code']) if cost and int(cost['signal']) == 0 else -int(cost['signal']) if cost else None)
            cells.write(json.dumps(dict(repeat=repeat, mode=mode, index=job['index'], group=job['group'],
                        stdout=str(stdout.relative_to(a.out)), stderr=str(stderr.relative_to(a.out)),
                        returncode=rc, terminal=mode == 'source' or cost is not None, cost=cost,
                        launch=launch_row['directory'], launcher_returncode=launch_row['returncode'])) + '\n')
            cells.flush()

        for repeat in range(a.repeat):
            modes = MODES if repeat % 2 == 0 else list(reversed(MODES))
            for mode in modes:
                print(f'repeat={repeat} mode={mode} streams={len(jobs)}', flush=True)
                folder = a.out / f'{mode}-{repeat}'
                if mode in ('source', 'fresh', 'split'):
                    for job in jobs:
                        directory = folder / str(job['index'])
                        if mode == 'source':
                            cmd = [str(a.source.resolve()), '-in', '-smt2']
                        elif mode == 'fresh':
                            cmd = [str(a.driver.resolve()), 'fresh', str(a.out / job['full']), str(directory)]
                        else:
                            cmd = [str(a.driver.resolve()), 'split', str(inputs / (job['group'] + '.prefix')), str(a.out / job['suffix']), str(directory)]
                        row = launch(cmd, directory, a.out / job['original'] if mode == 'source' else None)
                        emit(job, mode, repeat, directory, '0' if mode in ('fresh', 'split') else 'source', row)
                else:
                    for group in groups:
                        members = [j for j in jobs if j['group'] == group]
                        if mode == 'reverse':
                            members.reverse()
                        directory = folder / group
                        cmd = [str(a.driver.resolve()), {'branch':'branch','reverse':'branch-reverse','cancel':'branch-cancel'}[mode], str(inputs / (group + '.prefix')), str(directory)]
                        if mode == 'cancel':
                            cmd.append(str(a.out / cancel_jobs[group]['suffix']))
                        cmd += [str(a.out / j['suffix']) for j in members]
                        row = launch(cmd, directory)
                        for position, job in enumerate(members):
                            emit(job, mode, repeat, directory, str(position), row, prefix=True)
                        if mode == 'cancel':
                            cost = None
                            if (directory / 'cost.tsv').exists():
                                with (directory / 'cost.tsv').open() as stream:
                                    cost = next((r for r in csv.DictReader(stream, delimiter='\t') if r['name']=='cancel'), None)
                            cancellations.write(json.dumps(dict(repeat=repeat, group=group, index=cancel_jobs[group]['index'],
                                                directory=str(directory.relative_to(a.out)), cost=cost,
                                                launcher_returncode=row['returncode'])) + '\n'); cancellations.flush()
    (a.out / 'completion.json').write_text(json.dumps(dict(terminal=True, repetitions=a.repeat,
        completed_cells=a.repeat * len(MODES) * len(jobs), completed_launches=launch_count,
        load_after=Path('/proc/loadavg').read_text()), indent=2) + '\n')


if __name__ == '__main__':
    main()
