"""Run the already prepared71inputs once, manually after isolated42has exited.
Uses the existing engine/watchdog/full-stderr backend; no polling or scheduler.
Native diagnostic streams stay on the spacious existing /tmp filesystem.
"""
from pathlib import Path
import datetime,gzip,json,os,resource,shutil,subprocess,sys,time
REPO=Path('/workspaces/repository')
INPUT=REPO/'artifacts/hotspot-mechanisms-2026-10-25/prepared71-20261026'
OLD=REPO/'artifacts/engine-resource-profile-2026-10-25/isolated42-20261026T101138Z'
CONTEXT=Path('/tmp/gpu-smt-isolated42-20261026/context.json')
CLI=Path('/tmp/gpu-smt-rust-engine-build-20261025/target/debug/gpu-smt')
MODULES=[Path('/tmp/gpu-smt-simp-cadence-20261026'),
 Path('/tmp/gpu-smt-interval-map-20261026'),
 Path('/tmp/gpu-smt-interval-continuation-20261025'),
 Path('/tmp/gpu-smt-failfast-native-20261026')]
CELLS=['existing-simp-controls14','failfast-controls6','native71','import71','experimental71']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def birth(pid):
 try:return int((Path('/proc')/str(pid)/'stat').read_text().rsplit(')',1)[1].split()[19])
 except (OSError,IndexError,ValueError):return None
def inputs():
 result={}
 for name in CELLS:
  batch=json.loads(gzip.decompress((INPUT/(name+'.json.gz')).read_bytes()))
  assert batch['mode']=='all'
  assert len(batch['candidates'])==({'existing-simp-controls14':14,'failfast-controls6':6}.get(name,71))
  assert len({c['id'] for c in batch['candidates']})==len(batch['candidates'])
  assert all(c['timeout_ms']==300000 and c['reuse'] is False for c in batch['candidates'])
  result[name]=batch
 assert [c['id'] for c in result['native71']['candidates']]==[c['id'] for c in result['experimental71']['candidates']]
 assert [c['id'] for c in result['native71']['candidates']]==[c['id'] for c in result['import71']['candidates']]
 return result
def archive_closed(path):
 dest=path.with_suffix(path.suffix+'.gz')
 with path.open('rb')as src,gzip.open(dest,'wb')as out:shutil.copyfileobj(src,out)
 with path.open('rb')as src,gzip.open(dest,'rb')as check:
  while True:
   a=src.read(1024*1024);b=check.read(1024*1024)
   assert a==b,('archive mismatch',str(path))
   if not a:break
 path.unlink()
def main():
 batches=inputs();ctx=json.loads(CONTEXT.read_text());m=ctx['previous_manifest']
 lean=Path(m['sysroot'])/'bin/lean'
 assert CLI.is_file() and lean.is_file()
 assert all((p/(name+'.olean')).is_file() for p,name in zip(
  MODULES,['SimpAllProfile','IntervalMap','IntervalContinuation','NativeFailFast']))
 assert resource.getrlimit(resource.RLIMIT_AS)==(-1,-1)
 if sys.argv[1:]==['--validate-only']:
  print(json.dumps({'UTC':now(),'input_counts':{n:len(v['candidates']) for n,v in batches.items()},
   'native_executions':0,'backend':'NativeLean stock --json --stdin;not old REPL timing',
   'resources':{'actual_RSS_bytes':48*1024**3,'cpus':[8,9,10,11],'cores_per_worker':1},
   'runtime_not_qualified':True}));return
 assert not sys.argv[1:]
 terminal=json.loads((OLD/'terminal.json').read_text())
 assert terminal['exit_code']==0,'retain actual42failure; inspect before manual next launch'
 launch=json.loads((OLD/'launch.json').read_text())
 assert birth(launch['pid'])!=launch['start_ticks'],'42CLI still owns native work'
 assert birth(launch['controller_pid'])!=launch['controller_start_ticks'],'42controller not retired'
 # Only pinned research executables: never inspect/kill other Workspace owners.
 pinned={str(lean),m['repl'],m['prepared_host']}
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:argv=(p/'cmdline').read_bytes().split(b'\0')[0].decode(errors='replace')
  except OSError:continue
  assert argv not in pinned,('existing pinned native owner',p.name)
 os.sched_setaffinity(0,{8,9,10,11})
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 out=Path('/tmp')/('gpu-smt-original71-native-'+stamp);out.mkdir()
 env=dict(os.environ,LEAN_SYSROOT=m['LEAN_SYSROOT'])
 env['LEAN_PATH']=os.pathsep.join(map(str,MODULES))+os.pathsep+m['LEAN_PATH']
 env['PATH']=str(Path(m['sysroot'])/'bin')+os.pathsep+env['PATH']
 manifest={'UTC':now(),'controller_pid':os.getpid(),'controller_start_ticks':birth(os.getpid()),
 'source':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
 'binary_bytes':CLI.stat().st_size,'binary_mtime':CLI.stat().st_mtime,'LEAN_PATH':env['LEAN_PATH'],
 'prior42terminal':terminal,'cells':CELLS,'scope':'controls then original/import/experimental;48interval and23simp interpreted separately'}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(str(out),flush=True)
 started=time.monotonic()
 for name in CELLS:
  cell=out/name;cell.mkdir();stderr=cell/'native-stderr';stderr.mkdir()
  cmd=[str(CLI),'check','--lean',str(lean),'--project',m['project'],
   '--environment','lean4.9-original71-stock-cli-48GiB-4x1core-20261026',
   '--cpus','8,9,10,11','--worker-cores','1','--memory-gib','48','--stderr-dir',str(stderr)]
  source=cell/'input.jsonl'
  source.write_text(json.dumps(batches[name])+'\n')
  t=time.monotonic()
  with source.open('rb')as inp,(cell/'results.jsonl').open('wb')as result,(cell/'resource-events.jsonl').open('wb')as events:
   p=subprocess.Popen(cmd,cwd=m['project'],env=env,stdin=inp,stdout=result,stderr=events,start_new_session=True)
   (cell/'launch.json').write_text(json.dumps({'UTC':now(),'pid':p.pid,'start_ticks':birth(p.pid),'command':cmd},indent=2)+'\n')
   code=p.wait()
  (cell/'terminal.json').write_text(json.dumps({'UTC':now(),'exit_code':code,'cell_seconds':time.monotonic()-t,
    'scope':'CLI startup through native retirement;archival separately timed'},indent=2)+'\n')
  # All native children have retired. Preserve full streams,including failed/censored attempts.
  a=time.monotonic()
  for path in list(stderr.glob('*.stderr'))+[source,cell/'results.jsonl',cell/'resource-events.jsonl']:
   archive_closed(path)
  (cell/'archival.json').write_text(json.dumps({'UTC':now(),'seconds':time.monotonic()-a,'raw_streams_losslessly_preserved':True})+'\n')
  if code:raise SystemExit(code)
 (out/'terminal.json').write_text(json.dumps({'UTC':now(),'exit_code':0,'controller_seconds':time.monotonic()-started,
  'scope':'includes cell startup,queue,verification,cleanup and lossless archival;no speedup conclusion'})+'\n')
if __name__=='__main__':main()
