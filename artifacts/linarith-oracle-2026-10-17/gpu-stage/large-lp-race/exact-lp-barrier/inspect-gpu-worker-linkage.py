import pathlib,json,subprocess,os
out=[]
for p in pathlib.Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  comm=(p/'comm').read_text().strip()
  if comm not in ['cuopt_grpc_serv','exe']:continue
  env=(p/'environ').read_bytes().split(bytes([0]))
  maps=(p/'maps').read_text()
  row={'pid':p.name,'comm':comm,'preload':[x.decode(errors='replace')for x in env if x.startswith(b'LD_PRELOAD=')],'shim_mapped':'gpu-smt-cuda-async-fallback.so'in maps,'vm':[x for x in(p/'status').read_text().splitlines()if x.startswith(('VmSize:','VmRSS:'))]}
  for tool in [['ldd',str(p/'exe')],['nm','-D',str(p/'exe')]]:
   try:
    r=subprocess.run(tool,text=True,capture_output=True)
    row[tool[0]]=[l for l in r.stdout.splitlines()if any(x in l for x in ['cuda','cuopt','cuMemAlloc','cuGetProc','MallocAsync'])][:30]
   except FileNotFoundError:row[tool[0]]='unavailable'
  out.append(row)
 except FileNotFoundError:pass
print(json.dumps(out),flush=True)
