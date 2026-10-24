import socket,time,json,sys
from pathlib import Path
host=sys.argv[1];begin=time.monotonic();last=None
while time.monotonic()-begin<60:
 try:
  with socket.create_connection((host,5001),timeout=1)as s:
   s.sendall(b'{"memory":true}\n')
   with s.makefile("rb")as f:answer=json.loads(f.readline())
  assert answer["ready"]and answer["affinity"]==[8,9,10,11]
  Path(__file__).with_name("provider-ready.json").write_text(json.dumps(dict(readiness_seconds=time.monotonic()-begin,memory=answer),indent=2)+"\n")
  print(json.dumps(answer));break
 except (OSError,ValueError)as e:last=repr(e);time.sleep(.1)
else:raise RuntimeError("Existing finite provider did not become API-ready: "+str(last))
