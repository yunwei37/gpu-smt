from pathlib import Path
import gzip,json,datetime,sys,importlib.util,resource
sys.dont_write_bytecode=True
r=Path('/workspaces/repository')
s=Path(Path('/tmp/gpu-smt-step0092-path.txt').read_text().strip())
q=Path(Path('/tmp/gpu-smt-active-warm-resource-qualification.txt').read_text().strip())
m=json.loads((q/'manifest.json').read_text())
previous=json.loads((Path(m['retained_fifo_root'])/'manifest.json').read_text())
input_source=r/'artifacts/engine-resource-profile-2026-10-25/isolated42/requests.jsonl.gz'
raw=gzip.decompress(input_source.read_bytes())
requests=[json.loads(line)for line in raw.decode().splitlines()]
assert len(requests)==42
ids=[batch['candidates'][0]['id']for batch in requests]
assert len(set(ids))==42
with gzip.open(r/'artifacts/arithmetic-counterexample-2026-10-23/native-gpu-full-20261024T0913/off/results.jsonl.gz','rt')as f:
    baseline=[json.loads(line)for line in f]
expected=[row['proof_id']for row in baseline if row['status']=='resource_failure']
assert ids==expected
with gzip.open(r/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z/input7808.json.gz','rt')as f:
    canonical=json.load(f)
original={row['id']:row for row in canonical['candidates']}
for batch in requests:
    assert batch['mode']=='all'and len(batch['candidates'])==1
    row=batch['candidates'][0]
    assert row['timeout_ms']==300000 and row['reuse']is False
    assert all(row[k]==original[row['id']][k]for k in ['id','code','timeout_ms','reuse'])
spec=importlib.util.spec_from_file_location('warm_resource_context',r/'bench/lean-warm-resource/run.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
library_environment=module.native_library_environment(previous)
assert library_environment['LEAN_SERVER_NATIVE_DYNLIB']==m['native_library']
stage=Path('/tmp/gpu-smt-solo42-native-library-20261028')
stage.mkdir(exist_ok=False)
(stage/'requests.jsonl').write_bytes(raw)
assert(stage/'requests.jsonl').read_bytes()==raw
command=[str(q/'gpu-smt'),'check','--repl',m['warm_repl'],'--project',previous['project'],
 '--environment','lean49-native-mathlib-solo42-48GiB-20261028',
 '--cpus','8,9,10,11','--worker-cores','4','--memory-gib','48']
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'state':'prepared-not-executed','launched':False,'native_candidate_executions':0,
 'stage':str(stage),'input_source':str(input_source),'stdin':str(stage/'requests.jsonl'),
 'input_decompressed_bytes':len(raw),'exact_decompressed_bytes_verified':True,
 'original_ids':ids,'historical_off_resource_failure_ids_order_equal':True,
 'canonical7808_id_code_timeout_reuse_fields_equal':True,
 'task_metadata_scope':'Original solo NDJSON has no task_id;all-modeFIFO only,no task policy or first-success.',
 'prospective_command':command,'cwd':previous['project'],
 'environment_overrides':dict(library_environment,LEAN_SYSROOT=previous['sysroot'],LEAN_PATH=previous['LEAN_PATH']),
 'PATH_prepend':str(Path(previous['sysroot'])/'bin'),
 'current_pending_point_manifest':str(q/'manifest.json'),
 'candidate_engine_source':m['engine_source'],
 'candidate_engine_build_receipt':m['engine_build_receipt'],
 'candidate_qualification_definition_source':m['qualification_definition_source'],
 'candidate_point_still_requires_actual_qualification_review':True,
 'resources':{'aggregate_RSS_bytes':48*1024**3,'cpu_ids':[8,9,10,11],'cores_per_worker':4,
              'maximum_simultaneous_native_candidates':1,'fixed_process_AS_limit':False,
              'COW_import_parent':False,'lease_size_is_not_observed_CPU_use':True},
 'preparation_RLIMIT_AS':list(resource.getrlimit(resource.RLIMIT_AS)),
 'execution_order':'Only after the currentFIFO exits and the corrected4warm/engine point is reviewed/repaired. No automatic launch/controller is installed. Rebind to any further repaired release before actual execution.',
 'analysis_contract':'Retain every actual status including accepted/rejected/incomplete/operational outcomes,not failure-only assertions from the historical42analyzer. Keep allpartial/rawresults and actualexternalclock;do not pool timings across nativecode/concurrency/ASpoints.',
 'historical_context':'Old42launcher used stockREPL/debugCLI and did not explicitly configure the nativeMathlib library. Per-sourcemodulemaps were not retained;41budgetfailures/1timeout are historical,not correctedpoint results.'}
(stage/'prepared-point.json').write_text(json.dumps(record,indent=2)+'\n')
(s/'experiment-001/prepared-solo42-point.json').write_text(json.dumps(record,indent=2)+'\n')
(s/'experiment-001/preparation-source.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(record,indent=2))
