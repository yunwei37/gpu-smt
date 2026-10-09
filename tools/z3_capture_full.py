#!/usr/bin/env python3
"""Byte-preserving streaming instrumentation for the pinned native Z3."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time


def write_all(fd, data):
    view = memoryview(data)
    while view:
        n = os.write(fd, view)
        if n <= 0:
            raise OSError('write made no progress')
        view = view[n:]


def main():
    real = str(Path(os.environ['GPU_SMT_REAL_Z3']).resolve())
    directory = Path(os.environ['GPU_SMT_TRACE_DIR'])
    directory.mkdir(parents=True, exist_ok=True)
    stem = f'z3-{time.time_ns()}-{os.getpid()}'
    meta_path = directory / f'{stem}.meta.json'
    meta = dict(argv=[real, *sys.argv[1:]], shim_pid=os.getpid(),
                complete=False, streams={}, errors=[])
    def save():
        temp = meta_path.with_suffix('.tmp')
        temp.write_text(json.dumps(meta, indent=2) + '\n')
        temp.replace(meta_path)
    save()
    start = time.perf_counter()
    try:
        proc = subprocess.Popen(meta['argv'], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
    except OSError as exc:
        meta['errors'].append(repr(exc))
        meta['elapsed_s'] = time.perf_counter() - start
        save()
        return 127
    launch_completed = time.perf_counter()
    meta['child_pid'] = proc.pid
    save()
    # The native caller waits synchronously for DONE before sending its next
    # command. Hold this lock until the input write and byte accounting agree.
    input_lock = threading.Lock()
    live = dict(stdin_forwarded_bytes=0, first_stdin_monotonic_s=None)
    meta['child_launch_monotonic_s'] = start
    meta['child_launch_completed_monotonic_s'] = launch_completed
    meta['clock_ticks_per_second'] = os.sysconf('SC_CLK_TCK')
    marker = b'<<DONE>>\n'

    def sample_first_done(stdout_marker_end, observed_at):
        sampling_start = time.perf_counter()
        snapshot = directory / f'{stem}.first-done'
        snapshot.mkdir()
        observation = dict(observed_monotonic_s=observed_at,
                           stdout_marker_end_bytes=stdout_marker_end,
                           sampling_started_monotonic_s=sampling_start,
                           clock_ticks_per_second=meta['clock_ticks_per_second'],
                           files={}, errors=[])
        with input_lock:
            observation.update(live)
        observation['launch_to_done_observed_s'] = observed_at - start
        if observation['first_stdin_monotonic_s'] is not None:
            observation['first_stdin_to_done_observed_s'] = (
                observed_at - observation['first_stdin_monotonic_s'])
        base = Path('/proc') / str(proc.pid)
        paths = [('stat', base / 'stat'), ('status', base / 'status'),
                 ('smaps_rollup', base / 'smaps_rollup')]
        try:
            paths.extend((f'task-{p.name}-schedstat', p / 'schedstat')
                         for p in sorted((base / 'task').iterdir()))
        except OSError as exc:
            observation['errors'].append(f'task enumeration: {exc!r}')
        for label, path in paths:
            before = time.perf_counter()
            try:
                data = path.read_bytes()
                target = snapshot / f'{label}.bin'
                target.write_bytes(data)
                observation['files'][label] = dict(path=str(target.name),
                    read_started_monotonic_s=before,
                    read_finished_monotonic_s=time.perf_counter(), bytes=len(data))
            except OSError as exc:
                observation['errors'].append(f'{label}: {exc!r}')
        observation['sampling_finished_monotonic_s'] = time.perf_counter()
        observation['sampling_duration_s'] = (
            observation['sampling_finished_monotonic_s'] - sampling_start)
        observation['scope'] = ('Original first native DONE line; caller blocked during sampling. '
            'Live task schedstat omits departed tasks; no general quiescence claim. '
            'Exact prefix is first stdin_forwarded_bytes of raw stdin.bin.')
        meta['first_done'] = observation
        save()

    def pump(name, src, dst, close_dst=False):
        count = 0
        forwarded = True
        eof = False
        tail = b''
        done_observed = False
        try:
            with (directory / f'{stem}.{name}.bin').open('wb') as trace:
                while True:
                    chunk = os.read(src, 65536)
                    if not chunk:
                        eof = True
                        break
                    trace.write(chunk)
                    trace.flush()
                    count += len(chunk)
                    if forwarded:
                        try:
                            if name == 'stdin':
                                with input_lock:
                                    if live['first_stdin_monotonic_s'] is None:
                                        live['first_stdin_monotonic_s'] = time.perf_counter()
                                    write_all(dst, chunk)
                                    live['stdin_forwarded_bytes'] += len(chunk)
                            else:
                                if name == 'stdout' and not done_observed:
                                    combined = tail + chunk
                                    offset = 0
                                    while True:
                                        found = combined.find(marker, offset)
                                        if found < 0:
                                            break
                                        absolute_start = count - len(chunk) - len(tail) + found
                                        if ((found > 0 and combined[found-1:found] == b'\n')
                                                or absolute_start == 0):
                                            observed_at = time.perf_counter()
                                            try:
                                                sample_first_done(absolute_start + len(marker), observed_at)
                                            except Exception as exc:
                                                meta['errors'].append(f'first DONE sample: {exc!r}')
                                            done_observed = True
                                            break
                                        offset = found + 1
                                    tail = combined[-(len(marker) + 1):]
                                write_all(dst, chunk)
                        except BrokenPipeError:
                            forwarded = False
        except BaseException as exc:
            meta['errors'].append(f'{name}: {exc!r}')
        finally:
            if close_dst:
                try:
                    proc.stdin.close()
                except OSError:
                    pass
            meta['streams'][name] = dict(bytes=count, eof=eof, forwarded_all=forwarded)
    threads = [threading.Thread(target=pump, args=args, daemon=True) for args in
               [('stdin', 0, proc.stdin.fileno(), True),
                ('stdout', proc.stdout.fileno(), 1), ('stderr', proc.stderr.fileno(), 2)]]
    for thread in threads:
        thread.start()
    _, status, usage = os.wait4(proc.pid, 0)
    rc = os.waitstatus_to_exitcode(status)
    proc.returncode = rc
    # Output EOF is guaranteed after child exit; stdin may remain open at parent.
    for thread in threads[1:]:
        thread.join()
    threads[0].join(timeout=0.1)
    meta.update(returncode=rc, elapsed_s=time.perf_counter()-start,
                user_cpu_s=usage.ru_utime, system_cpu_s=usage.ru_stime,
                maxrss_kib=usage.ru_maxrss,
                complete=all(not t.is_alive() for t in threads) and not meta['errors'])
    meta.update(live)
    meta['invocation_kind'] = ('version' if any(x in sys.argv[1:] for x in ('-version', '--version')) else 'solver')
    save()
    if rc < 0:
        signal.signal(-rc, signal.SIG_DFL)
        os.kill(os.getpid(), -rc)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
