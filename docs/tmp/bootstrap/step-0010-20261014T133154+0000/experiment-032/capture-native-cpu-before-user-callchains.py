#!/usr/bin/env python3
# Finite native CPU sample capture for the admitted complete-source profile.
from pathlib import Path
import argparse,collections,datetime,gzip,importlib.util,json,os,resource,signal,subprocess,threading,time
ROOT=Path('/workspaces/repository')
D=ROOT/'artifacts/lean-modern-native-compilation-2026-10-14'
E=ROOT/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-032'
P=Path('/tmp/gpu-smt-native-cpu-perf-20261015')
NATIVE=P/'native-repl'
RAW=Path('/workspaces/.agent-state/gpu-smt-deps/native-cpu-perf-20261015')
PERF=P/'runtime/usr/bin/perf'
ENV=dict(os.environ)
ENV['LD_LIBRARY_PATH']=str(P/'runtime/usr/lib/x86_64-linux-gnu')+(':'+ENV['LD_LIBRARY_PATH'] if ENV.get('LD_LIBRARY_PATH') else '')
spec=importlib.util.spec_from_file_location('native_capture',D/'native-cpu-sampling-capture.py')
cap=importlib.util.module_from_spec(spec);spec.loader.exec_module(cap)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(path,value):path.write_text(json.dumps(value,indent=2)+chr(10))
class Sampler:
    def __init__(self,label,out):
        self.label=label;self.out=out;self.raw=RAW/label;self.raw.mkdir()
        self.stopped=threading.Event();self.thread=threading.Thread(target=self.loop)
        self.running={};self.records=[];self.seen=set();self.errors=[]
    def discover(self):
        found={}
        for entry in Path('/proc').iterdir():
            if not entry.name.isdecimal():continue
            try:
                if entry.joinpath('exe').resolve()!=NATIVE:continue
                fields=(entry/'stat').read_text().rsplit(')',1)[1].split()
                found[int(entry.name)]=int(fields[19])
            except (OSError,ValueError,IndexError):continue
        return found
    def start(self):self.thread.start()
    def start_one(self,pid,ticks):
        path=self.raw/f'native-{pid}-{ticks}.data'
        log=self.out/f'perf-native-{pid}-{ticks}.log'
        handle=log.open('wb')
        cmd=[str(PERF),'record','-e','cpu-clock:u','-F','99','--call-graph','dwarf','-z','-p',str(pid),'-o',str(path)]
        began=time.monotonic_ns()
        proc=subprocess.Popen(cmd,env=ENV,stdout=handle,stderr=subprocess.STDOUT,start_new_session=True)
        rec=dict(native_pid=pid,native_start_ticks=ticks,discovered_monotonic_ns=began,recorder_pid=proc.pid,
            command=cmd,raw_profile=str(path),tool_log=str(log),started_utc=now())
        self.running[(pid,ticks)]=(proc,handle,rec);self.seen.add((pid,ticks))
    def stop_one(self,key,reason):
        proc,handle,rec=self.running.pop(key)
        if proc.poll() is None:proc.send_signal(signal.SIGINT)
        code=proc.wait();handle.close()
        rec.update(recorder_returncode=code,stop_reason=reason,stopped_monotonic_ns=time.monotonic_ns(),
            stopped_utc=now(),raw_bytes=Path(rec['raw_profile']).stat().st_size if Path(rec['raw_profile']).exists() else 0)
        self.records.append(rec)
        save(self.out/'sampler-progress.json',dict(terminal=False,records=self.records,active=len(self.running),errors=self.errors))
    def loop(self):
        try:
            while not self.stopped.is_set():
                found=self.discover()
                for pid,ticks in found.items():
                    if (pid,ticks) not in self.seen:self.start_one(pid,ticks)
                for key,(proc,handle,rec) in list(self.running.items()):
                    if key[0] not in found or found[key[0]]!=key[1]:self.stop_one(key,'observed native exit/PID identity change')
                    elif proc.poll() is not None:self.stop_one(key,'recorder exited while native remained')
                self.stopped.wait(.1)
        except BaseException as exc:self.errors.append(dict(type=type(exc).__name__,error=str(exc)))
    def stop(self):
        self.stopped.set();self.thread.join()
        for key in list(self.running):self.stop_one(key,'capture finished; flush owned recorder')
        save(self.out/'sampler-receipt.json',dict(terminal=True,utc=now(),records=self.records,errors=self.errors,
          scope='Only this private native executable; user-mode CPU samples; attach gaps and failed/unknown data retained. Raw stack memory stays outside Git.'))
def report_profiles(sampler,out):
    reports=[]
    for rec in sampler.records:
        data=Path(rec['raw_profile'])
        if not data.exists() or not data.stat().st_size:
            reports.append(dict(native_pid=rec['native_pid'],report_returncode=None,error='empty/missing raw profile'));continue
        report=out/f"perf-native-{rec['native_pid']}-{rec['native_start_ticks']}-flat.txt.gz"
        cmd=[str(PERF),'report','--stdio','--no-children','--percent-limit','0','--sort','dso,symbol','-i',str(data)]
        proc=subprocess.Popen(cmd,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        with gzip.open(report,'wb') as dst:
            for chunk in iter(lambda:proc.stdout.read(65536),b''):dst.write(chunk)
        err=proc.stderr.read();code=proc.wait()
        error_path=report.with_suffix('.stderr.txt');error_path.write_bytes(err)
        reports.append(dict(native_pid=rec['native_pid'],raw_profile=str(data),raw_bytes=data.stat().st_size,
          report_command=cmd,report_returncode=code,flat_report=str(report),stderr_path=str(error_path)))
    save(out/'profile-reports.json',reports)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['preflight','full']);args=parser.parse_args()
    resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.sched_setaffinity(0,{12,13,14,15})
    out=D/('native-cpu-sampling-preflight1' if args.action=='preflight' else 'native-cpu-sampling-full1')
    out.mkdir()
    save(out/'capture-scope.json',dict(utc=now(),action=args.action,native_executable=str(NATIVE),
      source_capture=str(D/'native-cpu-sampling-capture.py'),raw_profiles=str(RAW),affinity=sorted(os.sched_getaffinity(0)),
      event='cpu-clock:u',sample_frequency_hz=99,callgraph='dwarf default8192byte stack',compression='perf default zstd1',
      note='Instrumented observation, not primary acceleration timing; native setup/import may be sampled; raw memory is runtime-private.'))
    if args.action=='preflight':
        cap.capture(out,'unprofiled-controls','preflight','compiled',False)
        label='profiled-controls';ds='preflight'
    else:label='goedel427-compiled-profile';ds='goedel427'
    sampler_out=out/(label+'-sampling');sampler_out.mkdir()
    sampler=Sampler(label,sampler_out);sampler.start();failure=None
    try:cap.capture(out,label,ds,'compiled',True)
    except BaseException as exc:
        failure=dict(type=type(exc).__name__,error=str(exc));raise
    finally:sampler.stop()
    report_profiles(sampler,sampler_out)
    save(out/'native-cpu-profile-terminal.json',dict(utc=now(),source_capture_terminal=str(out/(label+'.terminal.json')),
      sampler_terminal=str(sampler_out/'sampler-receipt.json'),failure=failure,recorders=len(sampler.records),
      note='Complete capture is not a result review or GPU/CPU acceleration claim.'))
    print('PROFILE_CAPTURE_TERMINAL',args.action,len(sampler.records),flush=True)
if __name__=='__main__':main()
