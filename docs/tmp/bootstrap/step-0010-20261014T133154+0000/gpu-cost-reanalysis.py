from pathlib import Path
import importlib.util,json,datetime
R=Path('/workspaces/repository')
E=R/'artifacts/lean-gpu-checking-2026-10-13/experiment022'
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('e022',E/'analyze.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=[]
for rep in range(3):
 label=f'proofnet-rep{rep}-gpu'
 raw=m.Raw(E/'full4-proofnet',label)
 try:p=m.provider(raw)
 finally:raw.close()
 previous=json.loads((E/'full4-proofnet'/f'{label}.analysis.json').read_text())
 assert p==previous['provider']
 totals=p['cumulative_per_pid_maxima_sum']
 warm=json.loads((E/'full4-proofnet'/f'proofnet-rep{rep}-warm.terminal.json').read_text())['complete_wall_seconds']
 gpu=json.loads((E/'full4-proofnet'/f'{label}.terminal.json').read_text())['complete_wall_seconds']
 extra={}
 raw=m.Raw(E/'full4-proofnet',label)
 try:
  for name in raw.names():
   if name!='stderr.bin' and not name.endswith('/stderr.bin'):continue
   for line in raw.read(name).splitlines():
    try:event=json.loads(line)
    except (ValueError,UnicodeDecodeError):continue
    if not str(event.get('event','')).startswith('closure_native_'):continue
    group=extra.setdefault(event.get('pid'),{})
    for key in ['host_declined','prepacking_declined','head_admission_ns']:
     group[key]=max(group.get(key,0),int(event.get(key,0)))
 finally:raw.close()
 extra_totals={key:sum(v.get(key,0) for v in extra.values()) for key in ['host_declined','prepacking_declined','head_admission_ns']}
 rows.append(dict(rep=rep,warm_seconds=warm,gpu_seconds=gpu,slowdown_percent=100*(gpu/warm-1),
  supported_call_percent=100*totals['supported']/totals['calls'],
  counters=totals,additional_counters=extra_totals,censored_processes=p['censored_processes'],
  actual_rtx5090_ready=p['actual_rtx5090_ready'],driver_errors=p['driver_errors']))
out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),rows=rows,
 scope='Existing three complete native6 ProofNet primary GPU cells. Observed per-PID maxima; failed worker lacks final counters. Counts are not cost-weighted coverage; parallel summed provider wall is not makespan attribution. No new benchmark or contention estimate.')
(D/'gpu-cost-reanalysis.json').write_text(json.dumps(out,indent=2)+'\n')
table=['| Rep | Warm s | GPU s | Slower | Supported / calls | Observed support | Provider summed wall s | Init s | Allocation/upload s | Launch/sync s |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for x in rows:
 t=x['counters'];table.append(f"|{x['rep']}|{x['warm_seconds']:.3f}|{x['gpu_seconds']:.3f}|{x['slowdown_percent']:.2f}%|{t['supported']} / {t['calls']}|{x['supported_call_percent']:.4f}%|{t['whole_provider_ns']/1e9:.4f}|{t['initialization_ns']/1e9:.4f}|{t['allocation_upload_ns']/1e9:.4f}|{t['launch_sync_ns']/1e9:.4f}|")
report='''# Native6 GPU cost and coverage: all three complete ProofNet primary repetitions

Supporting RQ4 analysis of existing complete source-native captures, not another experiment or complete RQ answer. Recompute with python3 gpu-cost-reanalysis.py in this directory. The script reads the original three ZIPs through the established E022 raw analyzer and retains per-PID cumulative maxima, never summing repeated checkpoints. It reproduces all stored provider aggregates exactly.

'''+ '\n'.join(table)+'''

## What the existing mechanism actually does

bench/lean-gpu/closure-native-provider-v5.cpp issues cuLaunchKernel with grid=(1,1,1) and block=(1,1,1), followed by cuCtxSynchronize. It offloads one narrow beta/zeta reduction synchronously, not a batch of independent reductions or the complete Lean kernel. One active CUDA thread cannot use this GPU's broad parallel arithmetic capacity. Host classification, packet preparation, allocation/upload, synchronization, readback and quotation accompany useful work; ordinary native fallback and final kernel checking remain.

Observed successful support is approximately 0.0925% of provider calls in each repetition. Unsupported native heads are largely rejected before packet construction by the existing conservative native Expr walk. This is a call-count result, not a measured fraction of checking time: expensive and cheap calls differ, and the failed native worker lacks terminal counters. Each GPU repetition contains one censored worker; the basic cohort remains complete because normal replacement returns every original input.

## What can and cannot explain the negative whole result

The mechanism engages RTX5090 and returns 2201 supported native results, but most provider calls still need the ordinary CPU path. Device initialization plus serialized tiny operations add measured costs rather than displacing most work. Upload and launch/sync observed sums rise substantially across repetitions. These timers measure steady-clock duration and include waits; they are not isolated CUDA kernel execution time.

The complete warm-vs-GPU slowdown is 1.74%, 3.64%, 1.58%, superseding the reader-facing old native4 ~33% number for the current native6 implementation. This does not establish a causal improvement across versions. Nor can provider sums be subtracted from whole makespan: workers overlap and uninstrumented wrapper/native costs remain. Shared-GPU contention is a possible contributor to variable waits, but no matched concurrent-owner trace or controlled comparison establishes it as the cause.

## Research disposition

These data reject the current single-operation provider as an acceleration result on this cohort. Merely shortening already-small transfers or another metadata-only speedup cannot establish complete Lean acceleration. Any next GPU mechanism must reach expensive native work and expose parallel independent work, then beat the strongest measured CPU path on the full formal cohorts with transfers/fallback/final checking included. The current complete stock-service acquisition continues unchanged; no speculative parallel GPU run is launched on top of it. Wider CPU/GPU/concurrency and miniF2F evidence, all four RQs and the full paper objective remain open.

This report is root analysis/self-review under the human no-delegation instruction; it is not independent audit.
'''
(D/'gpu-cost-reanalysis.md').write_text(report)
print(json.dumps(out,indent=2))
