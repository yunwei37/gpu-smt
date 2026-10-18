$ErrorActionPreference='Stop'
$gpuJobName='gpu-smt-cuopt-20261017'
$gpuSourcePod='coder-81668d0b-bcba-4058-a2e6-473350357c52-9dc6df5ff-btpq6'
$gpuEntryLab=./scripts/kubectl-home.ps1 get node lab -o json | ConvertFrom-Json
if(($gpuEntryLab.status.conditions | Where-Object type -eq 'Ready').status -ne 'True'){throw 'Managed target node not ready; preserve work and recover before mutation'}
$gpuEntryOther=./scripts/kubectl-home.ps1 -n coder get pod coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns -o json | ConvertFrom-Json
$gpuProviderProbe=$null
./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' python3 -c 'import json;x=json.load(open("/tmp/gpu-smt-linarith-oracle-20261017/strong-cpu-gpu-portfolio/qualification64-cpu/terminal.json"));assert x["state"]=="complete" and x["attempts"]==64;print("same-CPU reference terminal verified")'
if($LASTEXITCODE -ne 0){throw 'Actual equal-CPU reference must finish before GPU qualification'}
$gpuOldJob=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName --ignore-not-found -o name
if($gpuOldJob){throw 'Existing target owner must be inspected before reuse'}
$gpuSpec=./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' cat /workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target/../large-lp-race/strong-cpu-gpu-portfolio/job.json
if($LASTEXITCODE -ne 0){throw 'Cannot read recorded benchmark target'}
$gpuProbeStart=(Get-Date).ToUniversalTime().ToString('o')
$gpuStartClock=[Diagnostics.Stopwatch]::StartNew()
$gpuSpec | ./scripts/kubectl-home.ps1 apply -f -
if($LASTEXITCODE -ne 0){throw 'Target creation failed'}
$gpuIdentity=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName -o json | ConvertFrom-Json
$gpuUID=$gpuIdentity.metadata.uid
$gpuPodName=$null
$gpuQualExit=$null
$gpuReadySeconds=$null
$gpuClientSeconds=$null
try {
 do {
  $gpuPods=./scripts/kubectl-home.ps1 -n coder get pods -l job-name=$gpuJobName -o json | ConvertFrom-Json
  if(!$gpuPods.items){continue}
  $gpuPodName=$gpuPods.items[0].metadata.name
  ./scripts/kubectl-home.ps1 -n coder wait --for=condition=Ready pod/$gpuPodName
  $gpuPod=./scripts/kubectl-home.ps1 -n coder get pod $gpuPodName -o json | ConvertFrom-Json
  if($gpuPod.status.phase -in @('Failed','Succeeded')){throw 'Target terminated before API preflight'}
 } until (($gpuPod.status.conditions | Where-Object type -eq 'Ready').status -eq 'True')
 $gpuReadySeconds=$gpuStartClock.Elapsed.TotalSeconds
 $gpuIP=$gpuPod.status.podIP
 ./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' env GPU_SMT_CUDA_BATCH_HOST=$gpuIP GPU_SMT_CUOPT_HOST=$gpuIP GPU_ARITHMETIC_RACE_ROOT=/tmp/gpu-smt-linarith-oracle-20261017/strong-cpu-gpu-portfolio GPU_ARITHMETIC_RACE_MIN_ROWS=11 GPU_ARITHMETIC_GPU_MIN_READY=2 GPU_ARITHMETIC_NEGATIVE_CERTIFICATES=1 /workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python /workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-cpu-gpu-portfolio/run-qualification.py --out /tmp/gpu-smt-linarith-oracle-20261017/strong-cpu-gpu-portfolio/qualification64-gpu --input /workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/candidate-capacity32/input-first64.jsonl --limit 64 --methods oracle-gpu --width 32 --affinity 8 9 10 11 --native-buckets --repl /tmp/gpu-smt-goedel427-20261014/repl-bucket-candidate-timing/.lake/build/bin/repl --reuse-reference /tmp/gpu-smt-linarith-oracle-20261017/strong-cpu-gpu-portfolio/qualification64-cpu/rep1-fast-hybrid
 $gpuQualExit=$LASTEXITCODE
 $gpuClientSeconds=$gpuStartClock.Elapsed.TotalSeconds-$gpuReadySeconds
 $gpuProviderProbe=(./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' python3 -c 'import socket,json,sys;s=socket.create_connection((sys.argv[1],5001));s.sendall(b"{\"ping\":true}\n");print(s.makefile().readline());s.close()' $gpuIP | Out-String).Trim()
 if($LASTEXITCODE -ne 0){throw 'Provider retirement probe failed'}

} finally {
 $gpuRetireStart=$gpuStartClock.Elapsed.TotalSeconds
 $gpuLogText=''
 $gpuAffinity=''
 if($gpuPodName){
  $gpuLogText=(./scripts/kubectl-home.ps1 -n coder logs $gpuPodName -c cuopt 2>&1 | Out-String)
  $gpuAffinity=(./scripts/kubectl-home.ps1 -n coder exec $gpuPodName -c cuopt '--' python3 -c 'import pathlib,json;rows=[];[(rows.append({"pid":p.name,"cmd":(p/"comm").read_text().strip(),"allowed":[l for l in (p/"status").read_text().splitlines() if l.startswith("Cpus_allowed_list")]})) for p in pathlib.Path("/proc").iterdir() if p.name.isdigit() and (p/"status").exists()];print(json.dumps(rows))' 2>&1 | Out-String)
 }
 $gpuCurrent=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName --ignore-not-found -o json | ConvertFrom-Json
 $gpuDeleteExit=$null
 if($gpuCurrent -and $gpuCurrent.metadata.uid -eq $gpuUID){
  ./scripts/kubectl-home.ps1 -n coder delete job $gpuJobName
  $gpuDeleteExit=$LASTEXITCODE
  if($gpuPodName){./scripts/kubectl-home.ps1 -n coder wait --for=delete pod/$gpuPodName}
 }
 $gpuOther=./scripts/kubectl-home.ps1 -n coder get pod coder-eb48d962-76f4-4ff7-bac5-7bc62ec2ada3-5c8bb655f6-khnns -o json | ConvertFrom-Json
 $gpuLab=./scripts/kubectl-home.ps1 get node lab -o json | ConvertFrom-Json
 $gpuReceipt=@{start=$gpuProbeStart;end=(Get-Date).ToUniversalTime().ToString('o');jobUID=$gpuUID;pod=$gpuPodName;qualifierExit=$gpuQualExit;deleteExit=$gpuDeleteExit;otherWorkspacePhase=$gpuOther.status.phase;labReady=($gpuLab.status.conditions | Where-Object type -eq 'Ready').status;startupToPodReadySeconds=$gpuReadySeconds;clientWrapperSeconds=$gpuClientSeconds;retirementAndRestorationSeconds=$gpuStartClock.Elapsed.TotalSeconds-$gpuRetireStart;totalLifecycleSeconds=$gpuStartClock.Elapsed.TotalSeconds;scope='Finite original-prefix64-source capacity32 qualification,actual CUDA batched phase-I simplex,unchanged request-sized CUDA VMM/independent groups, retain native hybrid AND CPU HiGHS, add exact-repaired GPU contender,per-model cancellation,row11,minimum-ready2,one persistent batched GPU provider,same max32candidates and32contiguousnativequeues,all server/clientCPUs8--11,48GiB,no numeric warmup; actual launch groups and per-model retirement recorded; no independence audit; unchanged reversed CPU replication onCPUs0--3 and prefix preserved'} | ConvertTo-Json -Depth 8 -Compress
 $gpuPayload=@{receipt=$gpuReceipt;log=$gpuLogText;affinity=$gpuAffinity;providerProbe=$gpuProviderProbe} | ConvertTo-Json -Compress -Depth 6
 # Large logs travel through existing kubectl stdin, never a Windows commandargument.
 $gpuPayload | ./scripts/kubectl-home.ps1 -n coder exec -i $gpuSourcePod -c dev '--' python3 -c 'import sys,json,gzip,pathlib;x=json.load(sys.stdin);p=pathlib.Path("/workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/strong-cpu-gpu-portfolio");(p/"provider-probe.json").write_text(json.dumps(x.get("providerProbe"))+"\n");(p/"arithmetic-device-strong-cpu64-cleanup.json").write_text(x["receipt"]+"\n");(p/"arithmetic-device-strong-cpu64-backend.log.gz").write_bytes(gzip.compress(x["log"].encode(),mtime=0));(p/"arithmetic-device-strong-cpu64-affinity.txt").write_text(x["affinity"]);print(x["receipt"])'
 if($LASTEXITCODE -ne 0){throw 'Native results retained but GPU lifecycle archive failed'}
}
if($gpuQualExit -ne 0){throw "Native qualification failed exit=$gpuQualExit"}