
from pathlib import Path
import subprocess,gzip,json
r=Path('/workspaces/repository');p=r/'crates/gpu-smt-engine/src/lib.rs'
s=r/Path('/tmp/gpu-smt-step0094-path.txt').read_text().strip()/'experiment-001'
fixed=p.read_bytes();old=Path('/tmp/gpu-smt-retry-tail-original.rs').read_bytes()
(s/'old-engine-source.rs.gz').write_bytes(gzip.compress(old,mtime=0))
try:
 p.write_bytes(old)
 result=subprocess.run(['cargo','test','-p','gpu-smt-engine','--test','engine','resource_retry_waits_behind_normal_work_without_blocking_free_slots','--locked','--','--nocapture'],cwd=r,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (s/'old-behavior-output.txt').write_text(result.stdout)
 print(result.stdout)
 assert result.returncode!=0 and 'retry waiter blocked normal work'in result.stdout,'control failed for an unrelated reason'
 print('OBSERVED_EXPECTED_OLD_BEHAVIOR_FAILURE')
finally:
 p.write_bytes(fixed)
 assert p.read_bytes()==fixed
 (s/'old-control-restoration.json').write_text(json.dumps({'fixed_source_byte_restored':True,'old_source_byte_preserved':True})+'\n')
