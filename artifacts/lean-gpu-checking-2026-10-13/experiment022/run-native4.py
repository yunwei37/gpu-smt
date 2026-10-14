#!/usr/bin/env python3
"""Finite E022 whole original native warm/snapshot/CPU/GPU acquisition.

Plan/admission/review remain ordinary owner Markdown, not this CLI. Preflight
does not promote or launch full work. Mini scheduling belongs to the owner.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import time
import zipfile

from analyze import analyze_cell

BASE = Path(__file__).resolve().parent
ROOT = Path('/workspaces/repository')
SOURCE = BASE / 'source1'
SDK = Path('/workspaces/.agent-state/gpu-smt-deps/lean-4.9-capture/lean-4.9.0-rc1-linux')
WORK = SDK.parent / 'mathlib4'
STOCK = ROOT / 'artifacts/lean-service-lifecycle-2026-10-13/build1/Lean49PreparedBranches'
BRIDGE = BASE.parent / 'closure-development-20261013/native-bridge4/Lean49ClosureNativeV4'
PTX = BASE.parent / 'closure-development-20261013/native-bridge2/closure-native-packed-v2.ptx'
PRIMARY = [('warm', 'snapshot-cache', 'cpu', 'gpu'),
           ('snapshot-cache', 'cpu', 'gpu', 'warm'),
           ('cpu', 'gpu', 'warm', 'snapshot-cache')]
PROFILE = ('gpu', 'cpu', 'snapshot-cache', 'warm')


def identity(path):
    with path.open('rb') as stream:
        return {'path': str(path), 'bytes': path.stat().st_size,
                'sha256': hashlib.file_digest(stream, 'sha256').hexdigest()}


def native_environment(method):
    env = dict(os.environ)
    for name in list(env):
        if name.startswith(('LEAN_GPU_', 'LEAN_NATIVE_CLOSURE_', 'FARKAS_')) or name in (
            'LEAN_NUM_THREADS', 'GPU_SMT_PARENT_PREPARATION', 'GPU_SMT_CHECKPOINT_INDEX',
            'GPU_SMT_CHECKPOINT_STAGE', 'GPU_SMT_WORKER_RETIRE_AFTER',
            'GPU_SMT_PARENT_SEED_FIRST_HEADER', 'GPU_SMT_NATIVE_PROFILER'):
            env.pop(name, None)
    if method in ('cpu', 'gpu'):
        env['LEAN_NATIVE_CLOSURE_MODE'] = method
        if method == 'gpu':
            env['LEAN_NATIVE_CLOSURE_PTX'] = str(PTX)
    return env


def lean_path():
    receipt = ROOT / 'artifacts/lean-native-boundary-2026-10-11/experiment012/preflight2/branch-minif2f-first32/receipt.json'
    return json.loads(receipt.read_text())['environment']['LEAN_PATH']


def inputs(dataset, preflight):
    return (BASE.parent / 'experiment021/inputs/preflight3' / dataset if preflight else
            ROOT / 'artifacts/lean-parallel-verification-2026-10-12/experiment014/inputs' / dataset)


def archive_cell(out, label):
    directory, target = out / label, out / (label + '.zip')
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as zipped:
        for file in directory.rglob('*'):
            if file.is_file():
                zipped.write(file, file.relative_to(out))
    with zipfile.ZipFile(target) as zipped:
        if zipped.testzip() is not None:
            raise OSError('completed raw ZIP member failed CRC')
        members = {str(p.relative_to(out)) for p in directory.rglob('*') if p.is_file()}
        if set(zipped.namelist()) != members:
            raise OSError('completed raw ZIP member population differs')
    # Ordinary after-clock verified lossless archival of this terminal own cell.
    # Failed/partial captures and unique original source are never removed.
    if directory.parent.resolve() != out.resolve() or not directory.resolve().is_relative_to(BASE):
        raise ValueError('archive reclaim outside own E022 capture')
    shutil.rmtree(directory)
    (out / (label + '.archive.json')).write_text(json.dumps({
        'archive': str(target), 'bytes': target.stat().st_size,
        'scope': 'all complete own raw members, CRC/member population verified after measured whole clock',
        'reproduction': 'python3 -m zipfile -e ARCHIVE OS_TEMP_DIRECTORY'}, indent=2) + '\n')


def capture(out, label, dataset, method, width, profile=False, preflight=False):
    original = inputs(dataset, preflight)
    source = original / 'input.jsonl'
    population = [json.loads(line) for line in source.read_bytes().splitlines() if line.strip()]
    folder = out / label
    if folder.exists() or any((out / (label + suffix)).exists() for suffix in
                             ('.command.json', '.runner.log', '.terminal.json', '.zip', '.analysis.json')):
        raise FileExistsError('retain prior complete/failed/partial cell; select a fresh output: ' + label)
    binary = BRIDGE if method in ('cpu', 'gpu') else STOCK
    common = ['--workspace', str(WORK), '--sysroot', str(SDK), '--lean-path', lean_path(),
              '--jobs', str(width), '--out', str(folder)]
    if method == 'snapshot-cache':
        # Exact existing native branch: external native/backend fields satisfy
        # its original parser but are never invoked for --method native.
        command = ['python3', str(SOURCE / 'lean_capture_formal_backend.py'),
                   '--method', 'native', '--input', str(source), '--tasks', str(original / 'tasks.json'),
                   '--native', str(STOCK), '--reference', str(STOCK), '--backend', str(STOCK)] + common
    else:
        command = ['python3', str(SOURCE / 'lean_capture_prepared.py'),
                   '--input', str(source), '--native', str(binary), '--lake', str(SDK / 'bin/lake'),
                   '--parent-preparation', 'header-cache', '--native-runtime-default',
                   '--warm-pool', '--retire-after', str(len(population)), '--parent-seed-first-header'] + common
    if profile:
        command.append('--resources')
    command = ['/usr/bin/time', '-v', '-o', str(out / (label + '.process-time.txt'))] + command
    env = native_environment(method)
    receipt = {'label': label, 'dataset': dataset, 'method': method, 'command': command,
               'input': str(source), 'input_identity': identity(source), 'binary': identity(binary),
               'ptx': identity(PTX) if method == 'gpu' else None,
               'expected_attempts': len(population), 'cpu_set': sorted(os.sched_getaffinity(0)),
               'worker_width': width, 'profile': profile, 'preflight': preflight,
               'environment': {k: v for k, v in env.items() if k.startswith(('LEAN_', 'GPU_SMT_'))},
               'runtime': 'native default threads, unset LEAN_NUM_THREADS, original per-source 300s timeout, core0',
               'whole_boundary': 'caller/native launch, preparation, original input/failed/cache rows, frontend/final kernel, native provider/setup/transfer/fallback, output persistence, EOF/replacement; archive after clock',
               'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'begin_ns': time.monotonic_ns(), 'host_load_begin': os.getloadavg()}
    (out / (label + '.command.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    with (out / (label + '.runner.log')).open('xb') as log:
        result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    receipt.update(returncode=result.returncode, end_ns=time.monotonic_ns(), host_load_end=os.getloadavg())
    receipt['complete_wall_seconds'] = (receipt['end_ns'] - receipt['begin_ns']) / 1e9
    (out / (label + '.terminal.json')).write_text(json.dumps(receipt, indent=2) + '\n')
    report = analyze_cell(out, label)
    (out / (label + '.analysis.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'label': label, 'returncode': result.returncode, 'whole_seconds': receipt['complete_wall_seconds'],
                      'outcomes': report['outcomes'], 'returned': report['returned'],
                      'provider': report['provider']['cumulative_per_pid_maxima_sum']}), flush=True)
    if report['valid_complete']:
        archive_cell(out, label)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('preflight-cpu', 'preflight-gpu', 'full-proofnet', 'full-minif2f'))
    parser.add_argument('attempt', type=int, nargs='?', default=1)
    parser.add_argument('--out', type=Path, help='fresh own E022 output directory; no implicit recovery/timing stitching')
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    os.sched_setaffinity(0, {17, 18, 19, 20})
    preflight = args.action.startswith('preflight')
    out = args.out or (BASE / (f'preflight{args.attempt}' if preflight else 'full2-' + args.action[5:]))
    if not out.resolve().is_relative_to(BASE):
        raise ValueError('E022 capture output must remain inside its owning artifact directory')
    if preflight:
        out.mkdir(parents=True, exist_ok=True)  # disjoint CPU/GPU legs share one attempt
        for dataset in ('proofnet', 'minif2f'):
            for method in (('gpu',) if args.action == 'preflight-gpu' else ('warm', 'snapshot-cache', 'cpu')):
                status = capture(out, dataset + '-' + method, dataset, method, 1, profile=True, preflight=True)
                if status:
                    return status
    else:
        out.mkdir(parents=True, exist_ok=False)
        dataset = args.action[5:]
        width = 4 if dataset == 'proofnet' else 1
        for repetition, order in enumerate(PRIMARY):
            for method in order:
                status = capture(out, f'{dataset}-rep{repetition}-{method}', dataset, method, width)
                if status:
                    return status
        for method in PROFILE:
            status = capture(out, dataset + '-profile-' + method, dataset, method, width, profile=True)
            if status:
                return status
        (out / 'acquisition-completed.txt').write_text(datetime.datetime.now(datetime.timezone.utc).isoformat() + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
