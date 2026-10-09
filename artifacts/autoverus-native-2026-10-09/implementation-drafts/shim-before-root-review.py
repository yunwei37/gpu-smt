#!/usr/bin/env python3
"""Byte-preserving streaming instrumentation for the pinned native Z3."""
import hashlib
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
                real_z3_sha256=hashlib.sha256(Path(real).read_bytes()).hexdigest(),
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
    meta['child_pid'] = proc.pid
    save()
    def pump(name, src, dst, close_dst=False):
        count = 0
        forwarded = True
        eof = False
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
                            write_all(dst, chunk)
                        except BrokenPipeError:
                            forwarded = False
        except BaseException as exc:
            meta['errors'].append(f'{name}: {exc!r}')
        finally:
            if close_dst:
                try:
                    os.close(dst)
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
    meta['invocation_kind'] = ('version' if '--version' in sys.argv[1:] else 'solver')
    save()
    if rc < 0:
        signal.signal(-rc, signal.SIG_DFL)
        os.kill(os.getpid(), -rc)
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
