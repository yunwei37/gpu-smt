from pathlib import Path
import os,json,subprocess,time,datetime,resource
point=Path(__file__).parent
definition=json.loads((point/'rebound-point-13d4606.json').read_text())
assert resource.getrlimit(resource.RLIMIT_AS)==(-1,-1)
os.sched_setaffinity(0,set(definition['resources']['cpu_ids']))
environment=dict(os.environ,**definition['native_environment_overrides'])
environment['PATH']=definition['PATH_prepend']+':'+environment['PATH']
for key in ['GPU_SMT_CEX_MODE','GPU_SMT_ORACLE_SOCKET','GPU_SMT_LINARITH_SOCKET']:
    environment.pop(key,None)
begin=time.monotonic()
with (point/'requests.jsonl').open('rb') as source,(point/'native.stdout').open('wb') as out,(point/'native.stderr').open('wb') as err:
    child=subprocess.Popen(definition['prospective_command'],cwd=definition['cwd'],env=environment,
      stdin=source,stdout=out,stderr=err,start_new_session=True)
    birth=int(Path('/proc',str(child.pid),'stat').read_text().rsplit(')',1)[1].split()[19])
    (point/'launch.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':child.pid,
      'start_ticks':birth,'command':definition['prospective_command'],'source_engine':definition['candidate_engine_source'],
      'resources':definition['resources'],'input':'requests.jsonl','scope':'Requested finite original42native resource run;not AI session/daemon/schedule'})+'\n')
    code=child.wait()
(point/'exit.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'exit':code,'external_seconds':time.monotonic()-begin,'scope':'Whole CLI launch,input/output/native checking and retirement;original42point,no exclusions'})+'\n')
rows=[]
try:
    for line in (point/'native.stdout').read_text().splitlines():
        rows.extend(json.loads(line)['results'])
    assert len(rows)==42 and {r['id']for r in rows}==set(definition['original_ids'])
    assert all(len(r['attempts'])==1 and r['attempts'][0]['exclusive']for r in rows)
    for row in rows:
        for process in row['attempts'][0]['processes']:
            try:
                st=Path('/proc',str(process['pid']),'stat').read_text().rsplit(')',1)[1].split()
                assert int(st[19])!=process['start_ticks']or st[0]=='Z'
            except FileNotFoundError:pass
    assert code==0
    statuses={r['outcome']['status']for r in rows}
    result={'state':'complete','returned':42,'status_counts':{s:sum(r['outcome']['status']==s for r in rows)for s in sorted(statuses)},
      'scope':'Own fixed42fresh native resource point;root review required,not a speedup or automatic successor'}
except Exception as error:
    result={'state':'incomplete','error':repr(error),'cli_exit':code,'partial_rows':len(rows),'scope':'Preserve failure;no automatic retry/next collection'}
result['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(point/'terminal.json').write_text(json.dumps(result)+'\n')
