$ErrorActionPreference='Stop'
$gpuJobName='gpu-smt-cuopt-20261017'
$gpuSourcePod='coder-81668d0b-bcba-4058-a2e6-473350357c52-9dc6df5ff-wzmfb'
$gpuResult='/workspaces/repository/artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023'
$gpuNode=./scripts/kubectl-home.ps1 get node lab -o json | ConvertFrom-Json
if(($gpuNode.status.conditions|Where-Object type -eq Ready).status -ne 'True'){throw 'lab not Ready'}
$gpuOld=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName --ignore-not-found -o name
if($gpuOld){throw 'Existing finite GPU target has an owner; do not replace it'}
$gpuSource=./scripts/kubectl-home.ps1 -n coder get pod $gpuSourcePod -o json|ConvertFrom-Json
if($gpuSource.spec.nodeName -ne 'lab'){throw 'Four-CPU comparison requires the same lab host'}
$gpuSpec=./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' cat "$gpuResult/job.json"
if($LASTEXITCODE -ne 0){throw 'Cannot read owned benchmark spec'}
$gpuClock=[Diagnostics.Stopwatch]::StartNew()
$gpuUID=$null;$gpuPodName=$null;$gpuClientExit=$null;$gpuStartup=$null;$gpuClientSeconds=$null;$gpuProbe=$null
try {
 $gpuSpec|./scripts/kubectl-home.ps1 apply -f -
 if($LASTEXITCODE -ne 0){throw 'Finite target creation failed'}
 $gpuIdentity=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName -o json|ConvertFrom-Json
 $gpuUID=$gpuIdentity.metadata.uid
 $gpuPods=./scripts/kubectl-home.ps1 -n coder get pods -l "job-name=$gpuJobName" -o json|ConvertFrom-Json
 if(!$gpuPods.items){throw 'Created Job has no Pod yet; retain lifecycle failure'}
 $gpuPodName=$gpuPods.items[0].metadata.name
 ./scripts/kubectl-home.ps1 -n coder wait --for=condition=Ready "pod/$gpuPodName"
 if($LASTEXITCODE -ne 0){throw 'GPU provider Pod did not become Ready'}
 $gpuPod=./scripts/kubectl-home.ps1 -n coder get pod $gpuPodName -o json|ConvertFrom-Json
 $gpuStartup=$gpuClock.Elapsed.TotalSeconds
 $gpuIP=$gpuPod.status.podIP
 ./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' python3 "$gpuResult/await-provider.py" $gpuIP
 if($LASTEXITCODE -ne 0){throw 'GPU provider API did not become ready'}
 ./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' /workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python -u "$gpuResult/run-preflight.py" $gpuIP
 $gpuClientExit=$LASTEXITCODE
 $gpuClientSeconds=$gpuClock.Elapsed.TotalSeconds-$gpuStartup
 $gpuProbe=(./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' python3 -c 'import socket,json,sys;s=socket.create_connection((sys.argv[1],5001),timeout=1);s.sendall(b"{\"ping\":true}\n");print(s.makefile().readline());s.close()' $gpuIP|Out-String).Trim()
} finally {
 $gpuRetire=$gpuClock.Elapsed.TotalSeconds
 $gpuLog=''
 if($gpuPodName){$gpuLog=(./scripts/kubectl-home.ps1 -n coder logs $gpuPodName -c cuopt 2>&1|Out-String)}
 $gpuCurrent=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName --ignore-not-found -o json|ConvertFrom-Json
 if($gpuCurrent -and $gpuCurrent.metadata.uid -eq $gpuUID){
  ./scripts/kubectl-home.ps1 -n coder delete job $gpuJobName
  if($gpuPodName){./scripts/kubectl-home.ps1 -n coder wait --for=delete "pod/$gpuPodName"}
 }
 $gpuLeft=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName --ignore-not-found -o name
 $gpuLab=./scripts/kubectl-home.ps1 get node lab -o json|ConvertFrom-Json
 $gpuReceipt=@{utc=(Get-Date).ToUniversalTime().ToString('o');jobUID=$gpuUID;pod=$gpuPodName;clientExit=$gpuClientExit;startupToPodReadySeconds=$gpuStartup;clientWrapperSeconds=$gpuClientSeconds;retirementSeconds=$gpuClock.Elapsed.TotalSeconds-$gpuRetire;completeColdLifecycleSeconds=$gpuClock.Elapsed.TotalSeconds;ownJobRemains=[bool]$gpuLeft;labReady=($gpuLab.status.conditions|Where-Object type -eq Ready).status;providerProbe=$gpuProbe;scope='Same four CPUs8-11; source2/live2/24GiB each; single48GiB parent sums native tree and exact-owned provider RSS every second; retain native+HiGHS; only added GPU row38 eligibility; full cancellation and retirement charged'}
 $gpuPayload=@{receipt=$gpuReceipt;log=$gpuLog}|ConvertTo-Json -Depth 8 -Compress
 $gpuPayload|./scripts/kubectl-home.ps1 -n coder exec -i $gpuSourcePod -c dev '--' python3 -c 'import sys,json,gzip,pathlib;x=json.load(sys.stdin);p=pathlib.Path("/workspaces/repository/artifacts/linarith-oracle-2026-10-17/current-budget-gpu-20261023");(p/"gpu-lifecycle.json").write_text(json.dumps(x["receipt"],indent=2)+"\n");(p/"gpu-provider.log.gz").write_bytes(gzip.compress(x["log"].encode(),mtime=0));print(json.dumps(x["receipt"]))'
}
if($gpuClientExit -ne 0){throw "GPU qualifier exit $gpuClientExit"}
