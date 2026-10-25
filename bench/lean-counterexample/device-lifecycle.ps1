param(
 [Parameter(Mandatory)][string]$SourcePod,
 [Parameter(Mandatory)][string]$Out,
 [ValidateSet('points','lean24','lean-full')][string]$Phase='points',
 [switch]$WorkerStream,
 [string]$ReuseOff
)
# Invoke from the sole spark-manage checkout; application files stay in Workspace.
$ErrorActionPreference='Stop'
if($ReuseOff -and $Phase -ne 'lean-full'){throw 'ReuseOff applies only to complete GPU repair'}
if($WorkerStream -and $Phase -ne 'points'){throw 'WorkerStream belongs only to the finite point qualification'}
$gpuRoot='/workspaces/repository'
$gpuArc="$gpuRoot/artifacts/arithmetic-counterexample-2026-10-23"
$gpuBench="$gpuRoot/bench/lean-counterexample"
$gpuCheck='import pathlib,json,sys;p=pathlib.Path("/workspaces/repository/artifacts/arithmetic-counterexample-2026-10-23/full-observe/verification/terminal.json");assert sys.argv[2]=="points" or (p.exists() and json.loads(p.read_text())["state"]=="complete"),"Original full observation is still active";assert not pathlib.Path(sys.argv[1]).exists(),"Preserve existing output"'
./scripts/kubectl-home.ps1 -n coder exec $SourcePod -c dev '--' python3 -c $gpuCheck $Out $Phase
if($LASTEXITCODE -ne 0){throw 'Keep the current acquisition and existing outputs'}
$gpuSpecText=./scripts/kubectl-home.ps1 -n coder exec $SourcePod -c dev '--' cat "$gpuArc/point-job.json"
if($LASTEXITCODE -ne 0){throw 'Cannot read the owned finite benchmark specification'}
$gpuSpec=$gpuSpecText|ConvertFrom-Json
$gpuJob=$gpuSpec.metadata.name
$gpuExisting=./scripts/kubectl-home.ps1 -n coder get job $gpuJob --ignore-not-found -o name
if($LASTEXITCODE -ne 0){throw 'Cannot establish Job ownership'}
if($gpuExisting){throw 'Existing finite GPU target has an owner; do not replace it'}
$gpuSource=./scripts/kubectl-home.ps1 -n coder get pod $SourcePod -o json|ConvertFrom-Json
if($LASTEXITCODE -ne 0){throw 'Cannot establish the existing Workspace identity'}
$gpuSourceNode=$gpuSource.spec.nodeName
$gpuClock=[Diagnostics.Stopwatch]::StartNew()
$gpuUID=$null;$gpuPodName=$null;$gpuPodUID=$null;$gpuReady=$null;$gpuStartup=$null;$gpuClientSeconds=$null;$gpuClientExit=$null;$gpuProviderExit=$null
$gpuMayHaveClient=$false;$gpuClientTerminal=$false;$gpuLaunch=$null
$gpuCleanup=[Collections.Generic.List[string]]::new()
$gpuLog='';$gpuRemains=$null
try {
 $gpuSpecText|./scripts/kubectl-home.ps1 apply -f -
 if($LASTEXITCODE -ne 0){throw 'Finite Job creation failed'}
 $gpuIdentity=./scripts/kubectl-home.ps1 -n coder get job $gpuJob -o json|ConvertFrom-Json
 if($LASTEXITCODE -ne 0){throw 'Cannot read created Job identity'}
 $gpuUID=$gpuIdentity.metadata.uid
 do {
  $gpuPods=./scripts/kubectl-home.ps1 -n coder get pods -l "job-name=$gpuJob" -o json|ConvertFrom-Json
  if($LASTEXITCODE -ne 0){throw 'Cannot observe the same owned Job'}
  $gpuCandidates=@($gpuPods.items|Where-Object {$_.metadata.ownerReferences.uid -contains $gpuUID})
  if(!$gpuCandidates){Start-Sleep -Milliseconds 1000;continue}
  $gpuPod=$gpuCandidates[0];$gpuPodName=$gpuPod.metadata.name;$gpuPodUID=$gpuPod.metadata.uid
  if($gpuPod.status.phase -in @('Succeeded','Failed')){throw 'Provider exited before readiness'}
  $gpuReasons=@($gpuPod.status.containerStatuses|ForEach-Object {$_.state.waiting.reason})
  if($gpuReasons|Where-Object {$_ -in @('ErrImagePull','ImagePullBackOff','CreateContainerError','CrashLoopBackOff')}){throw 'Provider startup failed'}
  if($gpuPod.status.phase -eq 'Running'){
   $gpuLines=./scripts/kubectl-home.ps1 -n coder logs $gpuPodName -c points
   if($LASTEXITCODE -eq 0){
    foreach($gpuLine in $gpuLines){
     if($gpuLine -match '"event":"ready"'){$gpuReady=$gpuLine|ConvertFrom-Json;break}
    }
   }
  }
  if(!$gpuReady){Start-Sleep -Milliseconds 1000}
 } until($gpuReady)
 if($gpuReady.backend -ne 'device'){throw 'Provider did not establish the requested backend API'}
 if($gpuPod.spec.nodeName -ne $gpuSourceNode){throw 'GPU/Workspace are on different hosts; the same-CPU resource point is not established'}
 $gpuStartup=$gpuClock.Elapsed.TotalSeconds
 $gpuIP=$gpuPod.status.podIP
 $gpuScript=if($Phase -eq 'points'){'qualify-remote-points.py'}else{'qualify-screening.py'}
 $gpuArguments=@('--host',$gpuIP,'--backend','device','--out',$Out)
 if($Phase -eq 'lean-full'){$gpuArguments+='--full'}
 if($WorkerStream){$gpuArguments+='--worker-stream'}
 if($ReuseOff){$gpuArguments+=@('--reuse-off',$ReuseOff)}
 if($Phase -eq 'points'){
  ./scripts/kubectl-home.ps1 -n coder exec $SourcePod -c dev '--' /workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python -u "$gpuBench/$gpuScript" @gpuArguments
  $gpuClientExit=$LASTEXITCODE
 } else {
  # Only short idempotent launch/observation calls cross SSH. A lost observer
  # must neither replay the client nor stop its still-owned provider.
  $gpuLaunchCode=@"
import pathlib,subprocess,json,sys,time
out=pathlib.Path(sys.argv[3]);record=pathlib.Path(str(out)+'.launch.json')
if record.exists():
 r=json.loads(record.read_text());p=pathlib.Path('/proc')/str(r['pid'])/'stat'
 same=p.exists() and int(p.read_text().rsplit(')',1)[1].split()[19])==r['start_ticks']
 done=out/'client-exit.json'
 if not same and not done.exists():raise RuntimeError('Prior client stopped without a terminal receipt; preserve it')
 if done.exists():
  e=json.loads(done.read_text())
  if (e['pid'],e['start_ticks'])!=(r['pid'],r['start_ticks']):raise RuntimeError('Exit receipt belongs to another client')
 print(json.dumps(r));sys.exit(0)
if out.exists():raise RuntimeError('Existing output has no owned launch receipt; do not replay')
with record.open('x')as receipt:
 with pathlib.Path(str(out)+'.client.log').open('xb')as log:
  p=subprocess.Popen([sys.argv[1],'-u',sys.argv[2],*sys.argv[4:]],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 stat=pathlib.Path('/proc')/str(p.pid)/'stat'
 r=dict(pid=p.pid,start_ticks=int(stat.read_text().rsplit(')',1)[1].split()[19]),out=str(out),command=[sys.argv[1],sys.argv[2],*sys.argv[4:]])
 receipt.write(json.dumps(r)+chr(10));receipt.flush()
print(json.dumps(r))
"@
  $gpuMayHaveClient=$true
  $gpuLaunch64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($gpuLaunchCode))
  $gpuLaunchRaw=./scripts/kubectl-home.ps1 -n coder exec $SourcePod -c dev '--' python3 -c 'import base64,sys;source=base64.b64decode(sys.argv[1]);sys.argv=sys.argv[1:];exec(source)' $gpuLaunch64 /workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/.venv/bin/python "$gpuBench/$gpuScript" $Out @gpuArguments
  if($LASTEXITCODE -ne 0){throw 'Client launch outcome uncertain; preserve provider and inspect the existing launch receipt'}
  $gpuLaunch=$gpuLaunchRaw|ConvertFrom-Json
  $gpuPollCode=@"
import pathlib,json,sys,time
out=pathlib.Path(sys.argv[1]);pid=int(sys.argv[2]);birth=int(sys.argv[3]);until=time.monotonic()+50
while True:
 p=pathlib.Path('/proc')/str(pid)/'stat';same=False;state=None
 try:
  f=p.read_text().rsplit(')',1)[1].split();same=int(f[19])==birth;state=f[0]
 except FileNotFoundError:pass
 done=out/'client-exit.json'
 if (not same or state=='Z')and done.exists():
  e=json.loads(done.read_text())
  if (e['pid'],e['start_ticks'])!=(pid,birth):raise RuntimeError('Wrong client exit identity')
  print(json.dumps(dict(state='terminal',receipt=e)));break
 if not same or state=='Z':
  print(json.dumps(dict(state='lost',reason='Client stopped without durable exit; preserve raw/provider')));break
 if time.monotonic()>=until:
  print(json.dumps(dict(state='running',pid=pid,start_ticks=birth)));break
 time.sleep(1)
"@
  do {
   $gpuPoll64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($gpuPollCode))
   try {
   $gpuPollRaw=./scripts/kubectl-home.ps1 -n coder exec $SourcePod -c dev '--' python3 -c 'import base64,sys;source=base64.b64decode(sys.argv[1]);sys.argv=sys.argv[1:];exec(source)' $gpuPoll64 $Out $gpuLaunch.pid $gpuLaunch.start_ticks
   } catch {Start-Sleep -Seconds 1;continue}
   if($LASTEXITCODE -ne 0){Start-Sleep -Seconds 1;continue}
   $gpuPoll=$gpuPollRaw|ConvertFrom-Json
   if($gpuPoll.state -eq 'lost'){throw 'Actual client disappeared without exit receipt; preserve raw and owned provider for recovery'}
   if($gpuPoll.state -eq 'terminal'){
    $gpuClientTerminal=$true;$gpuClientExit=[int]$gpuPoll.receipt.exit
   }
  } until($gpuClientTerminal)
 }
 $gpuClientSeconds=$gpuClock.Elapsed.TotalSeconds-$gpuStartup
} finally {
 if($gpuMayHaveClient -and !$gpuClientTerminal){
  Write-Warning "Client termination is unverified. Preserve Job $gpuJob UID $gpuUID and output $Out; observation loss is not permission to stop its provider."
 } else {
 $gpuRetiring=$gpuClock.Elapsed.TotalSeconds
 try {
  if($gpuReady -and $gpuPodName){
   $gpuStop='import socket,json,sys;s=socket.create_connection((sys.argv[1],5001),timeout=1);s.sendall((json.dumps({"stop":True})+chr(10)).encode());print(s.makefile().readline());s.close()'
   ./scripts/kubectl-home.ps1 -n coder exec $SourcePod -c dev '--' python3 -c $gpuStop $gpuPod.status.podIP
   if($LASTEXITCODE -ne 0){throw 'Provider graceful-stop request failed'}
   do {
    $gpuStopping=./scripts/kubectl-home.ps1 -n coder get pod $gpuPodName --ignore-not-found -o json|ConvertFrom-Json
    if($LASTEXITCODE -ne 0 -or !$gpuStopping){throw 'Provider process exit is unverified'}
    $gpuTerminated=$gpuStopping.status.containerStatuses|Where-Object name -eq points|ForEach-Object {$_.state.terminated}
    if(!$gpuTerminated){Start-Sleep -Milliseconds 1000}
   } until($gpuTerminated)
   $gpuProviderExit=$gpuTerminated.exitCode
   if($gpuProviderExit -ne 0){$gpuCleanup.Add('Provider process exited unsuccessfully')}
  }
 } catch {$gpuCleanup.Add($_.Exception.Message)}
 try {
  if($gpuPodName){
   $gpuLog=(./scripts/kubectl-home.ps1 -n coder logs $gpuPodName -c points 2>&1|Out-String)
   if($LASTEXITCODE -ne 0){$gpuCleanup.Add('Provider log collection incomplete')}
  }
 } catch {$gpuCleanup.Add($_.Exception.Message)}
 try {
  $gpuCurrent=./scripts/kubectl-home.ps1 -n coder get job $gpuJob --ignore-not-found -o json|ConvertFrom-Json
  if($LASTEXITCODE -ne 0){throw 'Cannot verify Job identity for cleanup'}
  if($gpuCurrent -and $gpuUID -and $gpuCurrent.metadata.uid -eq $gpuUID){
   ./scripts/kubectl-home.ps1 -n coder delete job $gpuJob
   if($LASTEXITCODE -ne 0){throw 'Owned Job deletion failed'}
   if($gpuPodName){
    do {
     $gpuLeft=./scripts/kubectl-home.ps1 -n coder get pod $gpuPodName --ignore-not-found -o name
     if($LASTEXITCODE -ne 0){throw 'Pod retirement is unverified'}
     if($gpuLeft){Start-Sleep -Milliseconds 1000}
    } until(!$gpuLeft)
   }
  }
  $gpuLeftJob=./scripts/kubectl-home.ps1 -n coder get job $gpuJob --ignore-not-found -o name
  if($LASTEXITCODE -ne 0){throw 'Final Job absence is unverified'}
  $gpuRemains=[bool]$gpuLeftJob
 } catch {$gpuCleanup.Add($_.Exception.Message)}
 $gpuReceipt=@{utc=(Get-Date).ToUniversalTime().ToString('o');phase=$Phase;workerStream=[bool]$WorkerStream;reusedOff=$ReuseOff;clientLaunch=$gpuLaunch;clientTerminalVerified=$gpuClientTerminal;sourcePod=$SourcePod;sourcePodUID=$gpuSource.metadata.uid;sourceNode=$gpuSourceNode;jobUID=$gpuUID;pod=$gpuPodName;podUID=$gpuPodUID;providerReady=$gpuReady;startupToAPIReadySeconds=$gpuStartup;clientWrapperSeconds=$gpuClientSeconds;clientExit=$gpuClientExit;providerExit=$gpuProviderExit;retirementSeconds=$gpuClock.Elapsed.TotalSeconds-$gpuRetiring;completeColdLifecycleSeconds=$gpuClock.Elapsed.TotalSeconds;ownJobRemains=$gpuRemains;cleanupErrors=$gpuCleanup.ToArray();scope='Own finite point/native experiment; CUDA initializes on first monitored batch; performance requires complete pair analysis; joint48GiB contract'}
 $gpuPayload=@{receipt=$gpuReceipt;providerLog=$gpuLog;job=$gpuSpec}|ConvertTo-Json -Depth 18 -Compress
 $gpuWrite='import pathlib,json,gzip,sys;x=json.load(sys.stdin);p=pathlib.Path(sys.argv[1]);p.mkdir(parents=True,exist_ok=True);(p/"lifecycle.json").write_text(json.dumps(x["receipt"],indent=2)+chr(10));(p/"job.json").write_text(json.dumps(x["job"],indent=2)+chr(10));(p/"provider.log.gz").write_bytes(gzip.compress(x["providerLog"].encode(),mtime=0));print(json.dumps(x["receipt"]))'
 $gpuPayload|./scripts/kubectl-home.ps1 -n coder exec -i $SourcePod -c dev '--' python3 -c $gpuWrite $Out
 if($LASTEXITCODE -ne 0){throw 'Lifecycle evidence was not saved; retain the control-shell output'}
 }
}
if($gpuClientExit -ne 0 -or $gpuCleanup.Count -ne 0 -or $gpuRemains){throw 'Qualification or complete cleanup did not succeed; preserve all partial records'}
