"""Four fixed native measurement cells;existing CLI/lifecycle/archival only."""
from pathlib import Path
import datetime,gzip,importlib.util,json,os,resource,subprocess,sys,time,shutil,collections
R=Path('/workspaces/repository')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('closed_archival',R/'artifacts/hotspot-mechanisms-2026-10-25/prepared71-20261026/execute.py')
A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def raw_cores(project):
 return sorted([p for p in project.glob('core*') if p.is_file() and (p.name=='core' or (p.name.startswith('core.') and p.name[5:].isdigit()))],key=lambda p:p.stat().st_size)
def assert_no_native():
 for p in Path('/proc').iterdir():
  if not p.name.isdecimal():continue
  try:arg=(p/'cmdline').read_bytes().split(b'\0')[0].decode()
  except (OSError,UnicodeError):continue
  assert not (arg.endswith('/bin/repl') or arg.endswith('/prepared-host') or arg.endswith('/bin/lean')),('live native at cell boundary',p.name)
def assert_retired(capture):
 for v in capture['results']:
  for t in v['attempts']:
   for p in t['processes']:
    assert A.birth(p['pid'])!=p['start_ticks'],('recorded native still live',p)
def main():
 assert resource.getrlimit(resource.RLIMIT_AS)==(-1,-1)
 previous=Path(Path('/tmp/gpu-smt-active-task-memory32.txt').read_text())
 assert json.loads((previous/'terminal.json').read_text())['exit_code']==0
 for n in ['fifo','task-memory']:assert_retired(json.loads(gzip.decompress((previous/n/'capture.json.gz').read_bytes())))
 assert A.birth(486935)!=156110880
 oldcfg=json.loads(Path('/tmp/gpu-smt-resource-pair-repair-20261027T032050/full7808/manifest.json').read_text())
 project=Path(oldcfg['project'])
 assert not raw_cores(project),'finish existing closed-core archival before launching'
 for p in Path('/proc').iterdir():
  if not p.name.isdecimal():continue
  try:arg=(p/'cmdline').read_bytes().split(b'\0')[0].decode()
  except (OSError,UnicodeError):continue
  assert not (arg.endswith('/bin/repl') or arg.endswith('/prepared-host') or arg.endswith('/bin/lean')),('live previous native',p.name)
 os.sched_setaffinity(0,{8,9,10,11})
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 out=Path('/tmp')/('gpu-smt-prepared-policy7808-'+stamp);out.mkdir()
 Path('/tmp/gpu-smt-active-prepared-policy7808.txt').write_text(str(out))
 cli=out/'gpu-smt';shutil.copyfile(previous/'gpu-smt',cli);cli.chmod(0o755)
 assert cli.read_bytes()==(previous/'gpu-smt').read_bytes()
 host=out/'prepared-host';shutil.copyfile(oldcfg['prepared_host'],host);host.chmod(0o755)
 assert host.read_bytes()==Path(oldcfg['prepared_host']).read_bytes()
 env=dict(os.environ,LEAN_SYSROOT=oldcfg['sysroot'],LEAN_PATH=oldcfg['LEAN_PATH'],PATH=oldcfg['sysroot']+'/bin:'+os.environ['PATH'])
 original=R/'artifacts/engine-resource-pair-2026-10-25/full7808-20261027T032050Z'
 full=gzip.decompress((original/'input7808.json.gz').read_bytes())
 batch=json.loads(full);assert len(batch['candidates'])==7808 and batch['mode']=='all'
 assert all(c['timeout_ms']==300000 and c['reuse'] is False for c in batch['candidates'])
 (out/'original7808.json').write_bytes(full)
 small={'mode':'all','candidates':batch['candidates'][:24]}
 (out/'qualification24.json').write_text(json.dumps(small))
 expected=[v['outcome']['status'] for v in json.loads(gzip.decompress((original/'prepared/capture.json.gz').read_bytes()))['results'][:24]]
 assert collections.Counter(expected)=={'accepted':21,'rejected':3}
 del batch,full
 cells=[('qualification-fifo','fifo','qualification24.json'),('qualification-task-memory','task-memory','qualification24.json'),('block1-fifo','fifo','original7808.json'),('block1-task-memory','task-memory','original7808.json'),('block2-task-memory','task-memory','original7808.json'),('block2-fifo','fifo','original7808.json')]
 manifest={'utc':now(),'controller_pid':os.getpid(),'controller_start_ticks':A.birth(os.getpid()),'CLI_source':'8045cca release copied from completed32run','CLI_bytes':cli.stat().st_size,'prepared_host_source':oldcfg['prepared_host'],'prepared_host_bytes':host.stat().st_size,'repl':oldcfg['repl'],'project':oldcfg['project'],'sysroot':oldcfg['sysroot'],'LEAN_PATH':env['LEAN_PATH'],'cells':[{'name':n,'policy':p,'input':i}for n,p,i in cells],'resources':{'memory_bytes':48*2**30,'cpus':[8,9,10,11],'cores_per_worker':1,'fixed_process_AS_cap':False},'scope':'own load-feedback composition atop preparedMathlib;two opposite-order blocks;not competitor replication or unconditional novelty/strongestwarm claim'}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 allstart=time.monotonic()
 for name,policy,input_name in cells:
  cell=out/name;cell.mkdir()
  command=[str(cli),'measure','--repl',oldcfg['repl'],'--project',oldcfg['project'],'--environment','lean49rc1-Mathlib-prepared-policy-original7808','--prepared-host',str(host),'--sysroot',oldcfg['sysroot'],'--cpus','8,9,10,11','--worker-cores','1','--memory-gib','48','--policy',policy]
  begin=time.monotonic()
  with (out/input_name).open('rb')as src,(cell/'capture.json').open('wb')as dest,(cell/'resource-events.jsonl').open('wb')as logs:
   p=subprocess.Popen(command,cwd=project,env=env,stdin=src,stdout=dest,stderr=logs,start_new_session=True)
   (cell/'launch.json').write_text(json.dumps({'utc':now(),'pid':p.pid,'start_ticks':A.birth(p.pid),'command':command,'input':input_name},indent=2)+'\n')
   rc=p.wait()
  seconds=time.monotonic()-begin
  capture=json.loads((cell/'capture.json').read_text())
  count=24 if name.startswith('qualification') else 7808
  assert capture['policy']==policy and len(capture['results'])==count
  assert_retired(capture)
  assert_no_native()
  if count==24:
   assert [v['outcome']['status'] for v in capture['results']]==expected
   events=[e for v in capture['results'] for t in v['attempts'] for e in t['backend_events']]
   assert any(e['stage']=='prepared_ready' for e in events)
   assert not any(e['stage']=='fresh_fallback' for e in events)
  (cell/'terminal.json').write_text(json.dumps({'utc':now(),'exit_code':rc,'external_cell_seconds':seconds,'lifecycle_seconds':capture['lifecycle_seconds'],'returned':count,'retired_recorded_native_births':True,'scope':'CLI launch to complete output/exit includes preparation,recreation,queue,retry,fallback,serialization,retirement;archival separately charged'},indent=2)+'\n')
  del capture
  archive_start=time.monotonic();core_rows=[]
  # Reuse exactly the existing lossless closed-file archival after native retirement.
  # Dumps stay private on the owningPVC;publish metadata only.
  for core in raw_cores(project):
   st=core.stat();dest=core.with_suffix(core.suffix+'.gz');assert not dest.exists()
   A.archive_closed(core);os.utime(dest,ns=(st.st_atime_ns,st.st_mtime_ns))
   core_rows.append({'original':str(core),'archive':str(dest),'source_bytes':st.st_size,'stored_bytes':dest.stat().st_size,'original_mtime_ns':st.st_mtime_ns,'full_byte_comparison':True})
  (cell/'private-core-archives.json').write_text(json.dumps(core_rows,indent=2)+'\n')
  for f in [cell/'capture.json',cell/'resource-events.jsonl']:A.archive_closed(f)
  (cell/'archival.json').write_text(json.dumps({'utc':now(),'seconds':time.monotonic()-archive_start,'scope':'closedcapture/resourcegzip and privatecore retention,after CLI interval;charge additionally in completecost'},indent=2)+'\n')
  print(name,(cell/'terminal.json').read_text(),flush=True)
  assert rc==0
  if name in ['qualification-task-memory','block1-task-memory','block2-fifo']:
   prefix='qualification' if count==24 else name.split('-')[0]
   left='qualification-fifo' if count==24 else prefix+'-fifo'
   right='qualification-task-memory' if count==24 else prefix+'-task-memory'
   for n in [left,right]:(out/(n+'.json')).write_bytes(gzip.decompress((out/n/'capture.json.gz').read_bytes()))
   cmp=subprocess.run([str(cli),'compare',str(out/(left+'.json')),str(out/(right+'.json'))],capture_output=True)
   (out/(prefix+'-comparison.json')).write_bytes(cmp.stdout);(out/(prefix+'-compare.stderr')).write_bytes(cmp.stderr)
   assert cmp.returncode==0
   # These decompressed copies are derived,while original byte-compressed captures remain.
   for n in [left,right]:(out/(n+'.json')).unlink()
 (out/'terminal.json').write_text(json.dumps({'utc':now(),'exit_code':0,'controller_seconds':time.monotonic()-allstart,'scope':'both24qualificationcells,fourfullcells,allclosedarchival/privatecore retention andcompare;environment/binary preparation separately recorded'})+'\n')
if __name__=='__main__':main()
