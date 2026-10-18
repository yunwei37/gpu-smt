$ErrorActionPreference='Stop'
$gpuPriorLifecycleWait64='ZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCmltcG9ydCBvcyxzZWxlY3QsanNvbix0aW1lCnA9UGF0aCgiL3Byb2MvMTM4MTM1IikKaWYgcC5leGlzdHMoKWFuZChwLyJzdGF0IikucmVhZF90ZXh0KCkuc3BsaXQoKVsyXSE9IloiOgogY21kPShwLyJjbWRsaW5lIikucmVhZF9ieXRlcygpLnJlcGxhY2UoYiJcMCIsYiIgIikuZGVjb2RlKCkKIGlmIndpZHRoOC1mdWxsMTAwMC1ncHUibm90IGluIGNtZDpyYWlzZSBSdW50aW1lRXJyb3IoIk9yaWdpbmFsIEdQVSBvd25lciBjaGFuZ2VkIikKIHRyeTpmZD1vcy5waWRmZF9vcGVuKDEzODEzNSkKIGV4Y2VwdCBQcm9jZXNzTG9va3VwRXJyb3I6ZmQ9Tm9uZQogaWYgZmQgaXMgbm90IE5vbmU6CiAgdHJ5OnNlbGVjdC5zZWxlY3QoW2ZkXSxbXSxbXSkKICBmaW5hbGx5Om9zLmNsb3NlKGZkKQpSPVBhdGgoIi93b3Jrc3BhY2VzL3JlcG9zaXRvcnkiKQpwPVIvImFydGlmYWN0cy9saW5hcml0aC1vcmFjbGUtMjAyNi0xMC0xNy9ncHUtc3RhZ2UvY3VvcHQtdGFyZ2V0L2FyaXRobWV0aWMtbGFyZ2UtbHAtcmFjZS1mdWxsMTAwMC1jbGVhbnVwLmpzb24iCndoaWxlIG5vdCBwLmV4aXN0cygpOnRpbWUuc2xlZXAoMSkKcj1qc29uLmxvYWRzKHAucmVhZF90ZXh0KCkpCmFzc2VydCByWyJkZWxldGVFeGl0Il09PTAgYW5kIHJbImxhYlJlYWR5Il09PSJUcnVlIiBhbmQgclsib3RoZXJXb3Jrc3BhY2VQaGFzZSJdPT0iUnVubmluZyIscgpVPVBhdGgoIi90bXAvZ3B1LXNtdC1saW5hcml0aC1vcmFjbGUtMjAyNjEwMTcvcmFjZS1vcmFjbGUtZnAtZmlyc3QiKQp0PWpzb24ubG9hZHMoKFUvInF1YWxpZmljYXRpb24yNC1jcHUvdGVybWluYWwuanNvbiIpLnJlYWRfdGV4dCgpKQphc3NlcnQgdFsic3RhdGUiXT09ImNvbXBsZXRlImFuZCBhbGwoeFsiY291bnRzIl09PXsiY29tcGxldGUiOjI0fWZvciB4IGluIHRbInJlc3VsdHMiXSkKYT1qc29uLmxvYWRzKChVLyJxdWFsaWZpY2F0aW9uMjQtY3B1L3BhaXJlZC1hbmFseXNpcy5qc29uIikucmVhZF90ZXh0KCkpWyJtZXRob2RzIl1bIm9yYWNsZS1oaW50Il0KYXNzZXJ0IG5vdCBhWyJvdXRjb21lX2RpZmZlcmVuY2VzIl1hbmQgbm90IGFbIm5vbl9tZXNzYWdlX2RpZmZlcmVuY2VzIl0KcHJpbnQoIk9yaWdpbmFsIEdQVSB0YXJnZXQgZnVsbHkgcmV0aXJlZDsgRlAtZmlyc3QgQ1BVIHF1YWxpZmljYXRpb24gcGFzc2VkLiBTdGFydCBmaW5pdGUgaGFyZHdhcmUgcXVhbGlmaWNhdGlvbi4iLGZsdXNoPVRydWUpCg=='
./scripts/kubectl-home.ps1 -n coder exec coder-81668d0b-bcba-4058-a2e6-473350357c52-9dc6df5ff-btpq6 -c dev '--' python3 -u -c 'import base64,sys;exec(base64.b64decode(sys.argv[1]))' $gpuPriorLifecycleWait64
if($LASTEXITCODE -ne 0){throw 'Prior GPU lifecycle/FP-first CPU qualification failed; no GPU target was created'}

$gpuJobName='gpu-smt-cuopt-20261017'
$gpuSourcePod='coder-81668d0b-bcba-4058-a2e6-473350357c52-9dc6df5ff-btpq6'
$gpuOldJob=./scripts/kubectl-home.ps1 -n coder get job $gpuJobName --ignore-not-found -o name
if($gpuOldJob){throw 'Existing target owner must be inspected before reuse'}
$gpuSpec=./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' cat /workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target/job-fp-first-race-gpu24.json
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
 ./scripts/kubectl-home.ps1 -n coder exec $gpuSourcePod -c dev '--' /workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python -u /workspaces/repository/bench/lean-native/linarith-oracle/run-race-gpu-preflight.py $gpuIP --root /tmp/gpu-smt-linarith-oracle-20261017/race-oracle-fp-first --affinity 8 9 10 11 --min-rows 11 --label fp-first-large-lp-race-gpu24 --out /tmp/gpu-smt-linarith-oracle-20261017/race-oracle-fp-first/qualification24-gpu --reference /tmp/gpu-smt-linarith-oracle-20261017/race-oracle-fp-first/qualification24-cpu/rep1-fast-hybrid
 $gpuQualExit=$LASTEXITCODE
 $gpuClientSeconds=$gpuStartClock.Elapsed.TotalSeconds-$gpuReadySeconds
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
 $gpuReceipt=@{start=$gpuProbeStart;end=(Get-Date).ToUniversalTime().ToString('o');jobUID=$gpuUID;pod=$gpuPodName;qualifierExit=$gpuQualExit;deleteExit=$gpuDeleteExit;otherWorkspacePhase=$gpuOther.status.phase;labReady=($gpuLab.status.conditions | Where-Object type -eq 'Ready').status;startupToPodReadySeconds=$gpuReadySeconds;clientWrapperSeconds=$gpuClientSeconds;retirementAndRestorationSeconds=$gpuStartClock.Elapsed.TotalSeconds-$gpuRetireStart;totalLifecycleSeconds=$gpuStartClock.Elapsed.TotalSeconds;scope='Finite FP-first exact-fallback large-LP CPU/GPU race original24 qualification, width8, minimum2-live-LP GPU batch; all server/client CPUs8--11,48GiB, no numeric warmup; pooled wall profile CPUs0--3 and prefix preserved'} | ConvertTo-Json -Depth 8 -Compress
 $gpuPayload=@{receipt=$gpuReceipt;log=$gpuLogText;affinity=$gpuAffinity} | ConvertTo-Json -Compress -Depth 6
 # Large logs travel through existing kubectl stdin, never a Windows commandargument.
 $gpuPayload | ./scripts/kubectl-home.ps1 -n coder exec -i $gpuSourcePod -c dev '--' python3 -c 'import sys,json,gzip,pathlib;x=json.load(sys.stdin);p=pathlib.Path("/workspaces/repository/artifacts/linarith-oracle-2026-10-17/gpu-stage/cuopt-target");(p/"arithmetic-fp-first-large-lp-race-gpu24-cleanup.json").write_text(x["receipt"]+"\n");(p/"arithmetic-fp-first-large-lp-race-gpu24-backend.log.gz").write_bytes(gzip.compress(x["log"].encode(),mtime=0));(p/"arithmetic-fp-first-large-lp-race-gpu24-affinity.txt").write_text(x["affinity"]);print(x["receipt"])'
 if($LASTEXITCODE -ne 0){throw 'Native results retained but GPU lifecycle archive failed'}
}
if($gpuQualExit -ne 0){throw "Native qualification failed exit=$gpuQualExit"}