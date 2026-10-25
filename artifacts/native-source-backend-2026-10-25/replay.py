"""Replay retained native CLI diagnostics through the actual built Rust classifier."""
from pathlib import Path
import datetime,gzip,json,os,subprocess,time
R=Path(__file__).resolve().parents[2]
A=Path(__file__).resolve().parent
OLD=R/'artifacts/lean-code-verification-2026-10-25/verina-full189-20261025T0725/native'
D=Path(os.environ.get('CARGO_TARGET_DIR','/tmp/gpu-smt-rust-engine-build-20261025/target'))
T=Path('/tmp/gpu-smt-native-cli-20261025');T.mkdir(exist_ok=True)
deps=D/'debug/deps'
library=lambda name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns)
command=['/usr/local/cargo/bin/rustc','--edition=2024',str(A/'replay-classifier.rs'),
    '--extern','gpu_smt_lean='+str(library('gpu_smt_lean')),
    '--extern','serde_json='+str(library('serde_json')),
    '-L','dependency='+str(deps),'-o',str(T/'replay-classifier')]
started=time.monotonic()
build=subprocess.run(command,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
    env=dict(os.environ,CARGO_HOME="/usr/local/cargo",RUSTUP_HOME="/usr/local/rustup"))
(A/'replay-build.log.gz').write_bytes(gzip.compress(build.stdout,mtime=0))
build.check_returncode()
rows=[json.loads(line)for line in gzip.decompress((OLD/'results.jsonl.gz').read_bytes()).decode().splitlines()]
inputs=[]
expected={'native_exit0_no_explicit_admission':'accepted','incomplete_reference':'incomplete','lean_error':'rejected'}
for row in rows:
 sid=row['source_id'];stream={}
 for channel in ['stdout','stderr']:
  stream[channel]=gzip.decompress((OLD/'logs'/(sid+'.'+channel+'.gz')).read_bytes()).decode()
 inputs.append(dict(source_id=sid,exit=row['exit'],**stream))
result=subprocess.run([str(T/'replay-classifier')],input=''.join(json.dumps(v)+'\n'for v in inputs),
    text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
(A/'replay-output.jsonl.gz').write_bytes(gzip.compress(result.stdout.encode(),mtime=0))
values=[json.loads(line)for line in result.stdout.splitlines()]
byid={x['source_id']:x for x in values};assert len(byid)==len(rows)==189
differences=[dict(source_id=row['source_id'],old=row['status'],classified=byid[row['source_id']])
 for row in rows if expected[row['status']]!=byid[row['source_id']]['status']]
from collections import Counter
receipt=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=command,
    rows=len(rows),classified=dict(Counter(v['status']for v in values)),differences=differences,
    whole_replay_seconds=time.monotonic()-started,new_native_executions=0,
    scope='Actual Rust classifier on archived original-filename native outputs; not new stdin/path or performance equivalence.')
(A/'replay-result.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
assert not differences
