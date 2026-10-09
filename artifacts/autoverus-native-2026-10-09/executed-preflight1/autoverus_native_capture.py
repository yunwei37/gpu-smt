#!/usr/bin/env python3
"""Replay every retained saved AutoVerus source through pinned whole-file Verus.

Sorted saved-corpus order is deterministic; it is not historical agent order.
Native stdout/stderr are retained verbatim, including failing and censored cells.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

FOLDERS = ('gpt4o-clover-1.0', 'gpt4o-diffy-1.0', 'gpt4o-mbpp-1.0', 'gpt4o-misc-1.0')
ENV_KEYS = ('PATH', 'RUSTUP_HOME', 'CARGO_HOME', 'RUSTUP_TOOLCHAIN', 'LD_LIBRARY_PATH',
            'VERUS_Z3_PATH', 'GPU_SMT_REAL_Z3', 'GPU_SMT_TRACE_DIR')


def recorded_environment(env):
    return {key: env[key] for key in ENV_KEYS if key in env}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temp.replace(path)


def terminate(proc):
    if proc.poll() is None:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()
    # A exited leader may leave descendants: our session/group alone is owned.
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cohort-raw', required=True, type=Path)
    parser.add_argument('--verus', required=True, type=Path)
    parser.add_argument('--real-z3', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--repeat', type=int, default=3)
    parser.add_argument('--cores', default='8', help='comma-separated permitted CPU IDs')
    parser.add_argument('--indices', help='optional comma-separated saved-corpus indices for real preflight')
    parser.add_argument('--timeout', type=float, default=120)
    args = parser.parse_args()
    def interrupted(signum, frame):
        raise KeyboardInterrupt(f'interrupted by signal {signum}')
    signal.signal(signal.SIGTERM, interrupted)
    if args.repeat <= 0 or args.timeout <= 0:
        parser.error('repeat and timeout must be positive')
    raw = args.cohort_raw.resolve()
    verus = args.verus.resolve()
    z3 = args.real_z3.resolve()
    shim = Path(__file__).resolve().parents[1] / 'tools/z3_capture_full.py'
    root = raw / 'generated/autoverus/autoverus-generated'
    sources = sorted((p for folder in FOLDERS for p in (root / folder).rglob('*.rs')),
                     key=lambda p: p.relative_to(raw).as_posix())
    if len(sources) != 3566:
        parser.error(f'expected all 3566 retained sources, found {len(sources)}')
    allowed = os.sched_getaffinity(0)
    affinity = sorted({int(x) for x in args.cores.split(',')})
    if not affinity or not set(affinity).issubset(allowed):
        parser.error(f'requested CPU IDs unavailable: {affinity}')
    selected = set(range(len(sources))) if args.indices is None else {int(x) for x in args.indices.split(',')}
    if not selected or not selected.issubset(range(len(sources))):
        parser.error('indices outside saved corpus')
    args.out.mkdir(parents=True, exist_ok=False)
    out = args.out.resolve()
    inputs = out / 'inputs'
    inputs.mkdir()
    candidates = []
    for index, source in enumerate(sources):
        relative = source.relative_to(raw)
        local = inputs / f'candidate_{index:05d}.rs'
        data = source.read_bytes()
        local.write_bytes(data)
        inside = source.relative_to(root)
        intermediate = len(inside.parts) > 2
        context = inside.parts[1].removeprefix('intermediate-') if intermediate else source.stem
        context_path = root / inside.parts[0] / f'{context}.time'
        candidates.append(dict(index=index, source_relative_path=relative.as_posix(),
                               source_sha256=hashlib.sha256(data).hexdigest(), bytes=len(data),
                               input=str(local), role='intermediate' if intermediate else 'final',
                               context_key=f'{inside.parts[0]}/{context}',
                               context_log_path=str(context_path.relative_to(raw)),
                               context_log_sha256=digest(context_path),
                               context_log_bytes=context_path.stat().st_size))
    os.sched_setaffinity(0, affinity)
    metadata = dict(arguments={k: str(v) if isinstance(v, Path) else v for k,v in vars(args).items()},
                    ordering='lexicographic saved corpus paths; not historical agent order',
                    candidates=candidates, selected_indices=sorted(selected), affinity=affinity, uname=list(os.uname()),
                    load_average=os.getloadavg(), cpu_topology=Path('/proc/cpuinfo').read_text(),
                    verus=str(verus), verus_sha256=digest(verus), z3=str(z3), z3_sha256=digest(z3),
                    shim=str(shim), shim_sha256=digest(shim), runner_sha256=digest(__file__),
                    time_binary='/usr/bin/time', time_sha256=digest('/usr/bin/time'),
                    environment=recorded_environment(os.environ), started_unix=time.time(), complete=False)
    save(out / 'metadata.json', metadata)
    for repetition in range(args.repeat):
        conditions = ('direct', 'capture') if repetition % 2 == 0 else ('capture', 'direct')
        for condition in conditions:
            for candidate in candidates:
                if candidate['index'] not in selected:
                    continue
                cell = out / f'repeat-{repetition}' / condition / f"{candidate['index']:05d}"
                cell.mkdir(parents=True)
                env = dict(os.environ)
                env['VERUS_Z3_PATH'] = str(z3 if condition == 'direct' else shim)
                env['GPU_SMT_REAL_Z3'] = str(z3)
                env['GPU_SMT_TRACE_DIR'] = str(cell / 'traces')
                argv = [str(verus), candidate['input'], '--multiple-errors', '5', '--output-json',
                        '--error-format=json', '--num-threads', '1', '--time', '--time-expanded']
                wrapped = ['/usr/bin/time', '-v', '-o', str(cell / 'time.txt'), '--', *argv]
                receipt = dict(repetition=repetition, condition=condition, candidate=candidate['index'],
                               argv=argv, executed_argv=wrapped, environment=recorded_environment(env), affinity=affinity,
                               cwd=str(verus.parent), load_average=os.getloadavg(),
                               started_unix=time.time(), complete=False, timed_out=False)
                save(cell / 'receipt.json', receipt)
                start = time.perf_counter()
                proc = None
                try:
                    with (cell / 'stdout.bin').open('wb') as stdout, (cell / 'stderr.bin').open('wb') as stderr:
                        proc = subprocess.Popen(wrapped, cwd=verus.parent, env=env, stdin=subprocess.DEVNULL,
                                                stdout=stdout, stderr=stderr, start_new_session=True)
                        receipt['pid'] = proc.pid
                        save(cell / 'receipt.json', receipt)
                        try:
                            proc.wait(timeout=args.timeout)
                        except subprocess.TimeoutExpired:
                            receipt['timed_out'] = True
                            terminate(proc)
                        receipt['returncode'] = proc.returncode
                        receipt['complete'] = not receipt['timed_out']
                except OSError as exc:
                    receipt['exception'] = repr(exc)
                    if proc is not None:
                        terminate(proc)
                        receipt['returncode'] = proc.returncode
                except BaseException as exc:
                    receipt['exception'] = repr(exc)
                    if proc is not None:
                        terminate(proc)
                        receipt['returncode'] = proc.returncode
                    raise
                finally:
                    receipt['external_wall_s'] = time.perf_counter()-start
                    receipt['finished_unix'] = time.time()
                    save(cell / 'receipt.json', receipt)
                print(f"repeat={repetition} condition={condition} candidate={candidate['index']} exit={receipt.get('returncode')} timeout={receipt['timed_out']}", flush=True)
    metadata.update(complete=True, finished_unix=time.time())
    save(out / 'metadata.json', metadata)


if __name__ == '__main__':
    main()
