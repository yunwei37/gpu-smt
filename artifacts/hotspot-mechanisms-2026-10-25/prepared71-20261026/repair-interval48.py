"""Manually rerun only the interval48cells affected by the missing import.
Preserve the valid71reference and23simp capture. This is diagnostic repair,
not a matched whole-cohort throughput pair or new rejection implementation.
"""
from pathlib import Path
import datetime,gzip,importlib.util,json,os,resource,subprocess,sys,time
sys.dont_write_bytecode=True
R=Path('/workspaces/repository')
SPEC=importlib.util.spec_from_file_location('existing_execution',R/'artifacts/hotspot-mechanisms-2026-10-25/prepared71-20261026/execute.py')
E=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(E)
BASE=R/'artifacts/hotspot-mechanisms-2026-10-25/interval-continuation/first-stage-map'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def batches():
 result={'interval-controls22':json.loads(gzip.decompress((BASE/'control-inputs.json.gz').read_bytes()))}
 inventory=json.loads((BASE/'original48-preparation/preparation.json').read_text())
 ids={v['id']for v in inventory['manifest']};assert len(ids)==48
 for src,name in [('import71','import48'),('experimental71','mapped48')]:
  b=json.loads(gzip.decompress((E.INPUT/(src+'.json.gz')).read_bytes()))
  b['candidates']=[c for c in b['candidates']if c['id']in ids]
  assert len(b['candidates'])==48
  result[name]=b
 for b in result.values():
  assert b['mode']=='all'
  assert all(c['reuse'] is False and c.get('timeout_ms',300000)==300000 for c in b['candidates'])
 assert len(result['interval-controls22']['candidates'])==22
 return result
def main():
 bs=batches()
 required=['SimpAllProfile','IntervalMap','IntervalContinuation','NativeFailFast']
 assert all((p/(n+'.olean')).is_file()for p,n in zip(E.MODULES,required))
 assert len(E.MODULES)==len(required)
 if sys.argv[1:]==['--validate-only']:
  print(json.dumps({'UTC':now(),'counts':{n:len(v['candidates'])for n,v in bs.items()},
   'compiled_modules':{n:str(p/(n+'.olean'))for p,n in zip(E.MODULES,required)},
   'native_executions':0,'whole_pair_speedup_not_defined':True}));return
 assert not sys.argv[1:]
 prior=json.loads(Path(Path('/tmp/gpu-smt-active-original71-context.txt').read_text()).read_text())
 out0=Path(prior['runtime_output']);terminal=json.loads((out0/'terminal.json').read_text());assert terminal['exit_code']==0
 assert E.birth(prior['controller_pid'])!=prior['controller_start_ticks']
 for f in out0.glob('*/launch.json'):
  q=json.loads(f.read_text());assert E.birth(q['pid'])!=q['start_ticks']
 m=json.loads(E.CONTEXT.read_text())['previous_manifest']
 for f in Path('/proc').iterdir():
  if not f.name.isdigit():continue
  try:exe=(f/'cmdline').read_bytes().split(b'\0')[0].decode(errors='replace')
  except OSError:continue
  assert exe not in [m['repl'],m['prepared_host'],str(Path(m['sysroot'])/'bin/lean')],('existingresearchnative',f.name)
 assert resource.getrlimit(resource.RLIMIT_AS)==(-1,-1)
 os.sched_setaffinity(0,{8,9,10,11})
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 out=Path('/tmp')/('gpu-smt-interval48-import-repair-'+stamp);out.mkdir();print(str(out),flush=True)
 env=dict(os.environ,LEAN_SYSROOT=m['LEAN_SYSROOT'],
  LEAN_PATH=os.pathsep.join(map(str,E.MODULES))+os.pathsep+m['LEAN_PATH'])
 env['PATH']=str(Path(m['sysroot'])/'bin')+os.pathsep+env['PATH']
 (out/'manifest.json').write_text(json.dumps({'UTC':now(),'controller_pid':os.getpid(),'controller_start_ticks':E.birth(os.getpid()),
  'prior71terminal':terminal,'LEAN_PATH':env['LEAN_PATH'],'cells':list(bs),'original_reference_preserved':str(out0/'native71'),
  'binary_bytes':E.CLI.stat().st_size,'binary_mtime':E.CLI.stat().st_mtime,
  'scope':'repair48missingimport only;22realcontrols before48;not matched71throughput;no23repeat'},indent=2)+'\n')
 start=time.monotonic()
 for name,b in bs.items():
  cell=out/name;cell.mkdir();logs=cell/'native-stderr';logs.mkdir()
  inp=cell/'input.jsonl';inp.write_text(json.dumps(b)+'\n')
  cmd=[str(E.CLI),'check','--lean',str(Path(m['sysroot'])/'bin/lean'),'--project',m['project'],
   '--environment','lean4.9-original48-import-repair-48GiB-4x1core-20261026',
   '--cpus','8,9,10,11','--worker-cores','1','--memory-gib','48','--stderr-dir',str(logs)]
  t=time.monotonic()
  with inp.open('rb')as source,(cell/'results.jsonl').open('wb')as result,(cell/'resource-events.jsonl').open('wb')as events:
   p=subprocess.Popen(cmd,cwd=m['project'],env=env,stdin=source,stdout=result,stderr=events,start_new_session=True)
   (cell/'launch.json').write_text(json.dumps({'UTC':now(),'pid':p.pid,'start_ticks':E.birth(p.pid),'command':cmd},indent=2)+'\n')
   code=p.wait()
  (cell/'terminal.json').write_text(json.dumps({'UTC':now(),'exit_code':code,'cell_seconds':time.monotonic()-t})+'\n')
  a=time.monotonic()
  for f in list(logs.glob('*.stderr'))+[inp,cell/'results.jsonl',cell/'resource-events.jsonl']:E.archive_closed(f)
  (cell/'archival.json').write_text(json.dumps({'UTC':now(),'seconds':time.monotonic()-a,'lossless':True})+'\n')
  if code:raise SystemExit(code)
 (out/'terminal.json').write_text(json.dumps({'UTC':now(),'exit_code':0,'controller_seconds':time.monotonic()-start})+'\n')
if __name__=='__main__':main()
