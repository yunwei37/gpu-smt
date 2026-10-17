"""Build official pinned cuOpt protobuf client in the owning Workspace."""
from pathlib import Path
import urllib.request,subprocess,json,resource,os
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/batch-oracle/cuopt-grpc');U.mkdir(parents=True,exist_ok=True)
resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3));resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{0,1,2,3})
SHA='02bfe53163c3e8eba25827f548623a8ab8071f88'
paths=['cpp/src/grpc/cuopt_remote.proto','cpp/src/grpc/cuopt_remote_service.proto','cpp/src/grpc/codegen/generated/cuopt_remote_data.proto','cpp/src/grpc/routing/cuopt_routing.proto','cpp/src/grpc/routing/cuopt_routing_solution.proto']
for path in paths:
 (U/Path(path).name).write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/NVIDIA/cuopt/'+SHA+'/'+path).read())
py='/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python'
pip='/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/pip'
commands=[[pip,'--python',py,'install','grpcio-tools==1.78.0','grpcio==1.84.0','protobuf==6.33.6'],[py,'-m','grpc_tools.protoc','-I'+str(U),'--python_out='+str(U),'--grpc_python_out='+str(U),*[str(U/Path(p).name)for p in paths]]]
with (U/'build-client.log').open('w')as log:
 for cmd in commands:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
(U/'provenance.json').write_text(json.dumps({'upstream':'https://github.com/NVIDIA/cuopt','commit':SHA,'paths':paths,'license':'Apache-2.0; upstream notices retained','commands':commands,'scope':'CPU-side generated wire client, no cuOpt GPU library installed in source Workspace'},indent=2)+'\n')
