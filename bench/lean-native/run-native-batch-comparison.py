"""E038 native batch comparison collector (stock / private / branch-off).

Reusable CLI over the frozen Kimina 4.27 GC/header-repaired native REPLs. One
prepared native worker per method/round replays the ORIGINAL source order in
affinity-width batches of BatchCommand {env:0,mode:"naive",cmds:[...],gc:true}
after the shared header command; every method sees one ordered native JSON
array plus double-newline frame. All costs (header preparation, worker
start/restart, native verification, fallback children, transport, parsing,
final stdin EOF and process exit) are inside the measured cell.

Provenance: derived from the root-executed one-off command
docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038/native-batch-integration/full-command.executed.py
(verified native lifecycle: byte-level Repl._read_response, feed_data stdout
tee so timeout/canceled partial reads stay gzip-captured, inherited RLIMIT_AS
repair after the stock Kimina 12GiB thread-create failure, psutil process-tree
PSS sampling, RUSAGE_CHILDREN accounting). This file adds CLI parameterization
and finite preflight/validation modes; it does not change the native protocol.

Disclosed policy deltas from stock Kimina defaults (same on ALL methods):
- repl.max_memory_bytes = resource.getrlimit(RLIMIT_AS)[0] (currently -1,
  i.e. workspace-unlimited address space) set BEFORE Repl.start, replacing the
  nominal settings.max_repl_mem 12GiB per-worker cap. Evidence for the repair:
  experiment-038/native-batch-integration/native-default-thread-failure-observation.json
  (all methods exit 134 'failed to create thread' at ~12.879GB mapped AS).
- stdout is teed at the StreamReader.feed_data boundary before the original
  parser sees it; the parser itself is the unmodified upstream one.

No new manifest, control plane, schema, scheduler, daemon, thread/worker/CPU
tuning, memory quota, or per-proof deadline is introduced. Timeouts are the
reused Kimina defaults: 60s header preparation, 300s batch-request boundary.
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import datetime
import gzip
import json
import os
import resource
import shutil
import sys
import time
from pathlib import Path

DEFAULT_KIMINA = Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d')
DEFAULT_FROZEN = Path('/tmp/gpu-smt-native-ref-branches-20261016/batch-frozen-v1')
DEFAULT_SDK = Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux')
DEFAULT_PROJECT = Path('/tmp/gpu-smt-goedel427-20261014/mathlib4')
DEFAULT_INPUT = Path('artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl')
DEFAULT_MANIFEST = Path('artifacts/lean-modern-native-compilation-2026-10-14/native-library.json')
HEADER = 'import Mathlib\nimport Aesop\n'
ORDERS = [['stock', 'private', 'off'], ['private', 'off', 'stock'], ['off', 'stock', 'private']]
METHODS = ('stock', 'private', 'off')


def utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def emit(stream, value) -> None:
    stream.write(json.dumps(value, ensure_ascii=False) + '\n')


def outcome(value) -> str:
    """Classify one parsed native response element (upstream message shapes)."""
    if not isinstance(value, dict):
        return 'operational'
    if 'error' in value or 'message' in value:
        return 'native_error'
    if any(x.get('severity') == 'error' for x in value.get('messages', [])):
        return 'rejected'
    if value.get('sorries'):
        return 'incomplete'
    return 'complete'


def rusage_pair():
    return resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)


class Runner:
    def __init__(self, args) -> None:
        self.args = args
        self.items = [json.loads(line) for line in args.input.open()]
        if args.limit:
            self.items = self.items[: args.limit]
        bad = [x.get('proof_id') for x in self.items if not x['code'].startswith(HEADER)]
        if bad:
            raise SystemExit(f'{len(bad)} input sources lack the exact common header, e.g. {bad[:3]}')
        self.config = json.loads(args.manifest.read_text())
        self.width = args.width or len(os.sched_getaffinity(0))
        self.inherited_as = resource.getrlimit(resource.RLIMIT_AS)
        self.orders = args.orders or ORDERS[: args.repetitions]

    # ---------------------------------------------------------------- launch
    def prepare_environment(self) -> None:
        sys.path.insert(0, str(self.args.kimina))
        os.environ['PATH'] = str(self.args.sdk / 'bin') + os.pathsep + os.environ['PATH']
        os.environ['LEAN_SYSROOT'] = str(self.args.sdk)
        os.environ['LEAN_SERVER_NATIVE_DYNLIB'] = self.config['load_manifest']
        from server.settings import settings  # noqa: PLC0415
        settings.project_dir = str(self.args.project)
        self.settings = settings

    def library_path(self, method: str) -> str:
        root = self.args.frozen
        own = root / ('plain' if method == 'stock' else 'private')
        sdk = self.args.sdk
        return os.pathsep.join([str(own), str(sdk / 'lib'), str(sdk / 'lib/lean')] + self.config['library_paths'])

    def repl_path(self, method: str) -> Path:
        return self.args.frozen / ('plain' if method == 'stock' else 'private') / 'repl'

    # ------------------------------------------------------------------ cell
    async def cell(self, rep: int, name: str, limit: int = 0, label: str | None = None):
        args = self.args
        items = self.items if not limit else self.items[:limit]
        cellname = label or ('rep%d-%s' % (rep, name))
        from server.repl import Repl  # noqa: PLC0415
        path = args.out / cellname
        path.mkdir(exist_ok=False)
        started = time.monotonic_ns(); ru0 = rusage_pair()
        counts = collections.Counter(); workers = 0; completed = 0
        peak_pss = 0; peak_rss = 0; sample_errors = 0
        events = gzip.open(path / 'events.jsonl.gz', 'wt', compresslevel=1)
        rows = gzip.open(path / 'responses.jsonl.gz', 'wt', compresslevel=1)
        samples = gzip.open(path / 'resources.jsonl.gz', 'wt', compresslevel=1)
        raw = gzip.open(path / 'stdout.gz', 'wb', compresslevel=1)
        repl = None; err_task = None; sampler = None

        def event(kind, **data):
            emit(events, {'event': kind, 'ns': time.monotonic_ns(), **data}); events.flush()

        async def stderr_drain(worker, number):
            with gzip.open(path / ('stderr-worker%d.gz' % number), 'wb', compresslevel=1) as stream:
                while data := await worker.proc.stderr.read(65536):
                    stream.write(data)
        import psutil  # noqa: PLC0415

        async def sampler_loop(worker, number):
            nonlocal peak_pss, peak_rss, sample_errors
            while True:
                errors = []; values = []
                try:
                    root = psutil.Process(os.getpid())
                    processes = [root] + root.children(recursive=True)
                except psutil.Error as exc:
                    processes = []; errors.append(repr(exc))
                for proc in processes:
                    try:
                        m = proc.memory_full_info(); c = proc.cpu_times()
                        values.append({'pid': proc.pid, 'created': proc.create_time(), 'rss': m.rss,
                                       'pss': m.pss, 'vms': m.vms, 'user': c.user, 'system': c.system,
                                       'threads': proc.num_threads()})
                    except psutil.Error as exc:
                        errors.append(repr(exc))
                pss = sum(x['pss'] for x in values); rss = sum(x['rss'] for x in values)
                peak_pss = max(peak_pss, pss); peak_rss = max(peak_rss, rss)
                sample_errors += len(errors)
                emit(samples, {'ns': time.monotonic_ns(), 'worker': number, 'collector_included': True,
                               'pss': pss, 'rss': rss, 'processes': values, 'errors': errors})
                samples.flush()
                if worker.proc.returncode is not None:
                    break
                await asyncio.sleep(args.sample_seconds)

        async def exchange(value, deadline):
            wire = (json.dumps(value, ensure_ascii=False) + '\n\n').encode()
            repl.proc.stdin.write(wire); await repl.proc.stdin.drain()
            response = await asyncio.wait_for(repl._read_response(), deadline)
            return json.loads(response)

        async def retire(normal):
            nonlocal repl, err_task, sampler
            if repl is None:
                return None
            worker = repl; error = None; native_eof = False
            try:
                async def drain_stdout():
                    while await worker.proc.stdout.read(65536):
                        pass
                tail = asyncio.create_task(drain_stdout())
                if normal:
                    worker.proc.stdin.close()
                    await asyncio.wait_for(worker.proc.wait(), args.finalize_timeout)
                    await asyncio.wait_for(tail, args.finalize_timeout)
                    native_eof = True
                else:
                    try:
                        await worker.close()
                    except ProcessLookupError:
                        await worker.proc.wait()
                    await asyncio.wait_for(tail, args.finalize_timeout)
            except Exception as exc:
                error = repr(exc)
                if worker.proc is not None and worker.proc.returncode is None:
                    await worker.close()
            finally:
                if err_task is not None:
                    await err_task
                if sampler is not None:
                    sampler.cancel(); await asyncio.gather(sampler, return_exceptions=True)
                for task in [worker._cpu_task, worker._mem_task]:
                    if task is not None:
                        task.cancel(); await asyncio.gather(task, return_exceptions=True)
                event('worker_terminal', worker=workers, pid=worker.proc.pid if worker.proc else None,
                      exit_code=worker.proc.returncode if worker.proc else None,
                      normal_eof=native_eof, error=error)
                worker.error_file.close(); repl = None; err_task = None; sampler = None
            if normal and (not native_eof or error or worker.proc.returncode != 0):
                return {'error': error, 'exit_code': worker.proc.returncode}
            return None

        async def start():
            nonlocal repl, workers, err_task, sampler
            self.settings.repl_path = str(self.repl_path(name))
            lib = self.library_path(name)
            os.environ['LD_LIBRARY_PATH'] = lib
            os.environ['GPU_SMT_FALLBACK_REPL'] = str(self.args.frozen / 'plain/repl')
            sdk = self.args.sdk
            os.environ['GPU_SMT_FALLBACK_LIBRARY_PATH'] = os.pathsep.join(
                [str(self.args.frozen / 'plain'), str(sdk / 'lib'), str(sdk / 'lib/lean')] + self.config['library_paths'])
            if name == 'off':
                os.environ['GPU_SMT_BRANCH_OFF'] = '1'
            else:
                os.environ.pop('GPU_SMT_BRANCH_OFF', None)
            repl = await Repl.create(header=HEADER, max_repl_uses=self.settings.max_repl_uses,
                                     max_repl_mem=self.settings.max_repl_mem)
            # Deliberate common repair: inherit the workspace AS limit (currently
            # unlimited) instead of the stock 12GiB Kimina per-worker RLIMIT_AS
            # cap, which failed 'failed to create thread' at batch width. Same
            # for every method; disclosed in launch.json, never a new quota.
            repl.max_memory_bytes = self.inherited_as[0]
            workers += 1; t = time.monotonic_ns()
            event('worker_start', worker=workers, executable=self.settings.repl_path,
                  library_path=lib, effective_RLIMIT_AS=self.inherited_as[0])
            await repl.start()
            # Tee at the native StreamReader feed boundary, before readline can
            # consume or discard bytes on timeout / line-limit errors. The
            # original upstream parser stays intact.
            reader = repl.proc.stdout
            initial = bytes(reader._buffer)
            if initial:
                raw.write(initial); raw.flush()
            original_feed = reader.feed_data
            def capture_feed(data):
                raw.write(data); raw.flush(); original_feed(data)
            reader.feed_data = capture_feed
            err_task = asyncio.create_task(stderr_drain(repl, workers))
            sampler = asyncio.create_task(sampler_loop(repl, workers))
            header = await exchange({'cmd': HEADER}, args.header_timeout)
            event('header', worker=workers, pid=repl.proc.pid,
                  elapsed_ns=time.monotonic_ns() - t, response=header)
            if header.get('env') != 0:
                raise RuntimeError('native header did not return env0')

        try:
            for offset in range(0, len(items), self.width):
                batch = items[offset:offset + self.width]
                t = time.monotonic_ns(); failure = None; response = None
                try:
                    if repl is None:
                        await start()
                    request = {'env': 0, 'mode': 'naive', 'gc': True,
                               'cmds': ['\n\n' + x['code'][len(HEADER):] for x in batch]}
                    event('request', worker=workers, offset=offset, count=len(batch),
                          ids=[x['proof_id'] for x in batch])
                    response = await exchange(request, args.batch_timeout)
                    if not isinstance(response, list) or len(response) != len(batch):
                        raise RuntimeError('native response is not a complete matching array')
                except Exception as exc:
                    chain = []; cause = exc; seen = set()
                    while cause is not None and id(cause) not in seen:
                        seen.add(id(cause)); chain.append(repr(cause)); cause = cause.__cause__ or cause.__context__
                    failure = ' <- '.join(chain)
                    event('batch_operational', worker=workers, offset=offset, error=failure, partial=response)
                    await retire(False)
                observed = time.monotonic_ns()
                for index, item in enumerate(batch):
                    value = None if failure else response[index]
                    state = 'operational' if failure else outcome(value)
                    counts[state] += 1
                    emit(rows, {'index': offset + index, 'proof_id': item['proof_id'], 'worker': workers,
                                'batch_offset': offset, 'admitted_ns': t, 'observed_ns': observed,
                                'batch_latency_ns': observed - t, 'outcome': state,
                                'operational_error': failure, 'response': value})
                completed += len(batch); rows.flush()
                event('batch_terminal', offset=offset, count=len(batch), completed=completed,
                      elapsed_ns=observed - t, operational=failure is not None)
                if failure and ('Separator is not found' in failure or 'longer than limit' in failure
                                or 'chunk exceed' in failure):
                    raise RuntimeError('native frame transport limit encountered: preserve partial run '
                                       'and repair equally before continuing')
            finalization = await retire(True)
            if finalization is not None:
                raise RuntimeError('normal EOF failure: ' + repr(finalization))
            status = 'complete'
        except BaseException:
            await retire(False); status = 'failed'
            raise
        finally:
            for stream in [events, rows, samples, raw]:
                stream.close()
            ru1 = rusage_pair(); cpu = {}
            for label, before, after in [('collector', ru0[0], ru1[0]), ('waited_children', ru0[1], ru1[1])]:
                cpu[label] = {'user': after.ru_utime - before.ru_utime, 'system': after.ru_stime - before.ru_stime}
            result = {'method': name, 'rep': rep, 'state': locals().get('status', 'failed'),
                      'expected': len(items), 'attempts': completed, 'counts': dict(counts),
                      'whole_ns': time.monotonic_ns() - started, 'cpu': cpu,
                      'sampled_peak_fleet_pss_with_collector': peak_pss,
                      'sampled_peak_fleet_rss_with_collector': peak_rss,
                      'sampling_read_errors': sample_errors, 'workers': workers,
                      'effective_RLIMIT_AS': self.inherited_as[0], 'width': self.width,
                      'normalization': 'none; preserve complete parsed native JSON values',
                      'scope': 'one original-order offline native-batch grouped-array observation; '
                               'corpus %d of %d candidates' % (len(items), len(self.items))}
            dump(path / 'terminal.json', result)
            print('CELL_TERMINAL', json.dumps(result), flush=True)
        return result


    async def run(self):
        results = []
        for rep, order in enumerate(self.orders, 1):
            for name in order:
                results.append(await self.cell(rep, name))
                dump(self.args.out / 'completed-cells.json', results)
        dump(self.args.out / 'terminal.json',
             {'state': 'complete', 'cells': len(results),
              'attempts': sum(x['attempts'] for x in results),
              'results': results, 'utc': utc()})
        return results

# ---------------------------------------------------------------- preflight
def cmd_preflight(runner: Runner, args) -> None:
    """Finite preflight: worker start, header env0, real batches, complete EOF."""
    runner.prepare_environment()
    pair = runner.orders[0]
    chosen = [name for name in pair if not args.method or name == args.method]
    if args.method and args.method not in pair:
        raise SystemExit('preflight only exercises a method in the first order: %r' % (pair,))
    rep = 1
    results = collections.OrderedDict()
    for name in chosen:
        terminal = asyncio.run(runner.cell(rep, name, limit=args.batch * runner.width,
                                           label='preflight-' + name))
        path = args.out / ('preflight-' + name)
        with gzip.open(path / 'responses.jsonl.gz', 'rt') as stream:
            values = [json.loads(line) for line in stream]
        if not values or len(values) != terminal['expected'] or any(
                x['response'] is None or x['operational_error'] is not None for x in values):
            raise RuntimeError('preflight did not produce complete native responses: ' + name)
        results[name] = values
    reference = next(iter(results.values()))
    for name, values in results.items():
        if [(x['index'], x['proof_id'], x['response']) for x in values] != [
                (x['index'], x['proof_id'], x['response']) for x in reference]:
            raise RuntimeError('preflight native response mismatch: ' + name)
    print('PREFLIGHT_TERMINAL', json.dumps({
        'acquisition': 'complete', 'cells': list(results),
        'native_response_comparison': 'equal' if len(results) > 1 else 'not tested (one method)'
    }), flush=True)

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--kimina', type=Path, default=DEFAULT_KIMINA,
                        help='kimina-server checkout providing server.repl/settings')
    parser.add_argument('--frozen', type=Path, default=DEFAULT_FROZEN,
                        help='frozen native root containing plain/ and private/ repls')
    parser.add_argument('--sdk', type=Path, default=DEFAULT_SDK, help='Lean 4.27 SDK root')
    parser.add_argument('--project', type=Path, default=DEFAULT_PROJECT,
                        help='mathlib4 project dir used as lake cwd')
    parser.add_argument('--input', type=Path, default=DEFAULT_INPUT,
                        help='original input.jsonl in preserved original order')
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST,
                        help='native-library.json describing load_manifest/library_paths')
    parser.add_argument('--out', type=Path, required=True, help='fresh output directory (not created)')
    parser.add_argument('--repetitions', type=int, default=3, choices=(1, 2, 3),
                        help='whole-corpus method rotation repetitions')
    parser.add_argument('--width', type=int, default=0,
                        help='batch width override; 0 = actual CPU affinity size')
    parser.add_argument('--limit', type=int, default=0,
                        help='truncate corpus to first N sources (preflight)')
    parser.add_argument('--header-timeout', type=float, default=60)
    parser.add_argument('--batch-timeout', type=float, default=300)
    parser.add_argument('--finalize-timeout', type=float, default=300)
    parser.add_argument('--sample-seconds', type=float, default=1)
    parser.add_argument('--orders', type=json.loads, default=None,
                        help='optional rotation orders as nested JSON list override')
    sub = parser.add_subparsers(dest='mode')
    pre = sub.add_parser('preflight', help='finite native preflight; no full matrix')
    pre.add_argument('--batch', type=int, default=1,
                     help='real batches per method/round in preflight')
    pre.add_argument('--method', default=None, help='run only this one method from the first order')
    return parser

def main(argv=None) -> None:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.out.exists():
        raise SystemExit('refusing to overwrite existing --out directory')
    args.out.mkdir(parents=True)
    if not args.input.is_absolute():
        args.input = Path(os.getcwd()) / args.input
        args.input = args.input.resolve() if not args.input.exists() else args.input
    if not args.manifest.is_absolute():
        manifest_candidate = args.input.parent / args.manifest.name
        if manifest_candidate.exists():
            args.manifest = manifest_candidate
    runner = Runner(args)
    if args.mode == 'preflight':
        cmd_preflight(runner, args)
    else:
        runner.prepare_environment()
        with gzip.open(args.out / 'original-input.jsonl.gz', 'wb', compresslevel=1) as archive:
            with args.input.open('rb') as source:
                shutil.copyfileobj(source, archive)
        dump(args.out / 'launch.json', {'utc': utc(), 'pid': os.getpid(), 'source': str(args.input),
             'sources': len(runner.items), 'width': runner.width,
             'affinity': sorted(os.sched_getaffinity(0)), 'inherited_RLIMIT_AS': runner.inherited_as,
             'nominal_Kimina_max_repl_mem_MiB': runner.settings.max_repl_mem,
             'effective_policy': 'inherit Workspace AS for every native worker/replay child; not default12GiB Kimina policy',
             'orders': runner.orders, 'header_timeout_seconds': args.header_timeout,
             'batch_and_normal_exit_timeout_seconds': args.batch_timeout,
             'sampling_seconds': args.sample_seconds, 'collector_source': str(Path(__file__))})
        dump(args.out / 'completed-cells.json', [])
        asyncio.run(runner.run())

if __name__ == '__main__':
    main()
