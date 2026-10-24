"""Package own point provider into the existing finite RTX5090 benchmark Job."""
from pathlib import Path
import base64,json,subprocess
R=Path('/workspaces/repository');B=R/'bench/lean-counterexample';A=R/'artifacts/arithmetic-counterexample-2026-10-23'
prior=json.loads((R/'artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023/job.json').read_text())
files={name:(B/name).read_text()for name in['point-provider.py','gpu_points.py','point_proposals.py','worker.py']}
files['points.ptx']=(A/'points.ptx').read_text()
payload=base64.b64encode(json.dumps(files).encode()).decode()
boot='import base64,json,pathlib,os,sys;d=json.loads(base64.b64decode('+repr(payload)+'));p=pathlib.Path("/tmp/gpu-smt-point-provider");p.mkdir();[(p/n).write_text(s)for n,s in d.items()];os.execv(sys.executable,[sys.executable,"-u",str(p/"point-provider.py"),"--ptx",str(p/"points.ptx")])'
pod=prior['spec']['template']['spec']
words='用 GPU 给失败的证明「找反例、提前判死」'
job=dict(apiVersion='batch/v1',kind='Job',
 metadata=dict(name=prior['metadata']['name'],namespace=prior['metadata']['namespace'],
 labels={'app.kubernetes.io/name':'gpu-smt-arithmetic-benchmark'},
 annotations={'admission.yunwei37.com/approval-ref':'gpu-smt/artifacts/arithmetic-counterexample-2026-10-23/plan.md','admission.yunwei37.com/user-words':words}),
 spec=dict(backoffLimit=prior['spec']['backoffLimit'],template=dict(spec=dict(
  restartPolicy=pod['restartPolicy'],nodeSelector=pod['nodeSelector'],runtimeClassName=pod['runtimeClassName'],
  containers=[dict(name='points',image=pod['containers'][0]['image'],command=['python3','-u','-c',boot],resources=pod['containers'][0]['resources'])]))))
(A/'point-job.json').write_text(json.dumps(job,indent=2,ensure_ascii=False)+'\n')
receipt=dict(base_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),
 working_source_status=subprocess.check_output(['git','status','--short','--',*[str(B/n)for n in files if n.endswith('.py')]],cwd=R,text=True).splitlines(),
 source_copies_embedded=True,files={n:len(s.encode())for n,s in files.items()},job_name=job['metadata']['name'],
 image=pod['containers'][0]['image'],scope='Existing finite Job name/path, own code only; no PVC/Secret/Service/schedule. Not applied by this packager.')
(A/'point-job-build.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
