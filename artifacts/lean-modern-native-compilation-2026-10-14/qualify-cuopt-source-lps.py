from pathlib import Path
import importlib.util,json,os,sys,time
D=Path(__file__).parent
os.sched_setaffinity(0,{4,5,6,7})
spec=importlib.util.spec_from_file_location('cuoptOracle',D/'cuopt-certificate-oracle.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
inputs=[json.loads(x) for x in (D/'native-oracle-source-lps.jsonl').read_text().splitlines()]
with (Path(os.environ.get('CUOPT_QUALIFICATION_OUT',str(D)))/'cuopt-source-lp-qualification.jsonl').open('x',buffering=1) as output:
 for name,method in [('default-concurrent',None),('gpu-pdlp',1),('cpu-dual-simplex',2)]:
  start=time.monotonic_ns()
  oracle=m.Oracle(os.environ['LIBCUOPT_LIBRARY_PATH'],method)
  try:
   for x in inputs:
    answer,meta=oracle.run(x['lp'])
    row={'method':name,'proof_id':x['proof_id'],'call':x['call'],'answer':answer,'meta':meta}
    output.write(json.dumps(row)+'\n')
    print(json.dumps({'method':name,'proof_id':x['proof_id'],'call':x['call'],'support_repaired':answer.get('support_repaired'),'seconds':meta['elapsed_ns']/1e9,'gpu_error':meta['gpu_error']}),flush=True)
  finally:oracle.close()
  print(json.dumps({'method':name,'whole_qualification_seconds':(time.monotonic_ns()-start)/1e9,'scope':'actual9LP setup control, biased sample, not wholeLean performance'}),flush=True)
