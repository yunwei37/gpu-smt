from pathlib import Path
import os,json,signal,time,datetime
n=Path(__file__).resolve().parent
before=json.loads((n/'before-stop.json').read_text())
expected={x['pid']:x for x in before['processes']}
actions=[]
def live(pid):
 try:
  x=(Path('/proc')/str(pid)/'stat').read_text().split(') ',1)[1].split()
  return x[0]!='Z' and x[19]==expected[pid]['start_ticks']
 except FileNotFoundError:return False
def send(pid,sig):
 if live(pid):
  os.kill(pid,sig);actions.append({'pid':pid,'signal':sig.name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
# These are only the recorded project OMP trees and the requested E038 collector.
for pid,x in expected.items():
 if pid not in [2043473,2109370,2109397]:send(pid,signal.SIGTERM)
send(2043473,signal.SIGINT)
until=time.monotonic()+10
while any(live(p) for p in expected) and time.monotonic()<until:time.sleep(.25)
for p in expected:send(p,signal.SIGTERM)
until=time.monotonic()+5
while any(live(p) for p in expected) and time.monotonic()<until:time.sleep(.25)
for p in expected:send(p,signal.SIGKILL)
time.sleep(.25)
result={'operator_requested_stop':True,'actions':actions,'still_running':[p for p in expected if live(p)],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'project OMP coordinator/OSS/experiments/paper/CLI and known-slow eager-v1 native capture only; unrelated CPU acquisitions untouched'}
(n/'stop-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert not result['still_running']
