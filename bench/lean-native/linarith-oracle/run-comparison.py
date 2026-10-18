"""Native warm-batch arithmetic direct-certificate comparison using the existing Kimina collector."""
from pathlib import Path
import argparse, asyncio, importlib.util, os, json, resource, sys
R=Path('/workspaces/repository')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017')
T=Path('/tmp/gpu-smt-goedel427-20261014')
F=Path('/tmp/gpu-smt-farkas-fast427-20261014/farkas427')
A=R/'artifacts/linarith-oracle-2026-10-17'
P=R/'bench/lean-native/run-native-batch-comparison.py'
# Only change the common import/header on the reused source-native collector.
source=P.read_text().replace("header = await exchange({'cmd': HEADER}, args.header_timeout)",
  "header = await exchange({'cmd': HEADER + 'import GpuArithmetic.Stages\\nimport GpuArithmetic.Baseline\\nimport GpuArithmetic.Oracle\\n' + EXTRA_IMPORT}, args.header_timeout)")
ns={'__name__':'arithmetic_native_batch','__file__':str(P),'EXTRA_IMPORT':''}
source=source.replace("                    await retire(False)\n                observed = time.monotonic_ns()", '''                    await retire(False)
                    stderr_path = path / ('stderr-worker%d.gz' % workers)
                    if stderr_path.exists():
                        with gzip.open(stderr_path, 'rt', errors='replace') as f:
                            diagnostic_stderr = f.read()
                        if 'std::bad_alloc' in diagnostic_stderr or 'Cannot allocate memory' in diagnostic_stderr:
                            failure += ' [resource_failure: inherited 48 GiB address-space ceiling]'
                observed = time.monotonic_ns()''')
source=source.replace("if header.get('env') != 0:", "if header.get('env') != 0 or any(m.get('severity') == 'error' for m in header.get('messages', [])):")
exec(compile(source,str(P),'exec'),ns)
Base=ns['Runner']
class Runner(Base):
    def library_path(self, method):
        return os.pathsep.join(([str(self.args.cost_root)] if self.args.cost_profile else [])+[str(U),str(self.args.sdk/'lib'),str(self.args.sdk/'lib/lean')]+self.config['library_paths'])
    def repl_path(self, method):
        return T/'repl-kimina-native-gc-header-repair/.lake/build/bin/repl'
    async def cell(self, rep, name, **kwargs):
        for key in ['GPU_ARITHMETIC_BASELINE','GPU_ARITHMETIC_ORACLE','FARKAS_EXTERNAL_CPU_HYBRID','GPU_ARITHMETIC_STRONG_PROFILE']:
            os.environ.pop(key,None)
        old=R/'artifacts/lean-modern-native-compilation-2026-10-14'
        os.environ['FARKAS_NATIVE_BIN']=str(old/'highs-certificate-oracle.py' if name=='fast-highs' else old/'farkas-external-support')
        if self.args.cost_profile:
            os.environ['FARKAS_NATIVE_BIN']=str(self.args.cost_root/'farkas-costd')
            os.environ['GPU_ARITHMETIC_STRONG_PROFILE']='1'
            cellname=kwargs.get('label') or ('rep%d-%s' % (rep,name))
            os.environ['FARKAS_COST_FILE']=str(self.args.out/cellname/'solver-costs.jsonl')
        else:
            os.environ.pop('FARKAS_COST_FILE',None)
        if name.startswith('fast-'):
            os.environ['GPU_ARITHMETIC_BASELINE']=name
            if name=='fast-hybrid':os.environ['FARKAS_EXTERNAL_CPU_HYBRID']='1'
        if name=='oracle':
            os.environ['GPU_ARITHMETIC_ORACLE']=str(self.args.cost_root/'arithmetic-costd') if self.args.cost_profile else str(U/'arithmetic-oracled-product-sign-fixed')
            os.environ['GPU_ARITHMETIC_BASELINE']='fast-hybrid'
            os.environ['FARKAS_EXTERNAL_CPU_HYBRID']='1'
        if name=='strong-profile':
            os.environ['GPU_ARITHMETIC_STRONG_PROFILE']='1'
            os.environ['FARKAS_EXTERNAL_CPU_HYBRID']='1'
        if name=='profile':
            os.environ['GPU_ARITHMETIC_PROFILE']='1'
            cellname=kwargs.get('label') or ('rep%d-%s' % (rep,name))
            os.environ['FARKAS_CORPUS_FILE']=str(self.args.out/cellname/'stages.jsonl')
        else:
            os.environ.pop('GPU_ARITHMETIC_PROFILE',None)
            os.environ.pop('FARKAS_CORPUS_FILE',None)
        if self.args.diagnostic:
            cellname=kwargs.get('label') or ('rep%d-%s' % (rep,name))
            os.environ['FARKAS_CORPUS_FILE']=str(self.args.out/cellname/'oracle.jsonl')
        if getattr(self.args,'numeric_replay_bin',None) is not None:
            replay=str(self.args.numeric_replay_bin.resolve())
            os.environ['FARKAS_NATIVE_BIN']=replay
            if name in ['oracle','oracle-hint']:
                os.environ['GPU_ARITHMETIC_ORACLE']=replay
            cellname=kwargs.get('label') or ('rep%d-%s' % (rep,name))
            os.environ['GPU_ARITHMETIC_REPLAY_LOG']=str(self.args.out/cellname/'replay-calls.jsonl')
        return await super().cell(rep,name,**kwargs)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--limit',type=int,default=0)
    p.add_argument('--input',type=Path,default=A/'input-top1000.jsonl')
    p.add_argument('--methods',nargs='+',choices=['native','profile','strong-profile','fast-hybrid','fast-highs','oracle'],default=['fast-hybrid','oracle'])
    p.add_argument('--affinity',type=int,nargs='+',default=[12,13,14,15])
    p.add_argument('--width',type=int,default=4)
    p.add_argument('--diagnostic',action='store_true')
    p.add_argument('--cost-root',type=Path,default=U,help='separate diagnostic build output; preserve an active capture')
    p.add_argument('--cost-profile',action='store_true',help='complete all-call Lean/Rust attribution; diagnostic, not a primary performance result')
    p.add_argument('--sample-seconds',type=float,default=1,help='nonpositive disables process-tree memory observer for overhead qualification')
    p.add_argument('--reuse-reference',type=Path,default=None)
    p.add_argument('--numeric-replay-bin',type=Path,help='Diagnostic fixed-certificate numerical omission control, not a deployable verifier')
    opts=p.parse_args()
    if opts.numeric_replay_bin is not None:
        if opts.cost_profile or any(m not in ['fast-hybrid','oracle','oracle-hint']for m in opts.methods):
            p.error('fixed-certificate diagnostic supports only native/CPU oracle, without phase instrumentation')
        if not os.environ.get('GPU_ARITHMETIC_REPLAY_DATA'):
            p.error('fixed-certificate diagnostic requires actual request/answer data')
    if opts.cost_profile and any(m not in ['fast-hybrid','oracle'] for m in opts.methods):
        p.error('--cost-profile supports only the matched fast-hybrid and oracle paths')
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    # User-required upstream SHRED memory ceiling for every new capture.
    resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
    os.sched_setaffinity(0,set(opts.affinity))
    ns['EXTRA_IMPORT']=''
    if 'strong-profile' in opts.methods:
        ns['EXTRA_IMPORT']='import GpuArithmetic.StrongProfile\n'
    if opts.cost_profile:
        ns['EXTRA_IMPORT']='import GpuArithmetic.CostOracle\n'
    c=json.loads((R/'artifacts/lean-modern-native-compilation-2026-10-14/native-library.json').read_text())
    manifest=U/('strong-profile-native-load.txt' if 'strong-profile' in opts.methods else 'comparison-native-load.txt')
    manifest.write_text(Path(c['load_manifest']).read_text()+''.join(str(U/f)+'\n' for f in (['comparison-strong-fallback.so','strong-profile.so'] if 'strong-profile' in opts.methods else ['comparison-strong-fallback.so'])))
    if opts.cost_profile:
        manifest=opts.cost_root/'cost-profile-native-load.txt'
        manifest.write_text(Path(c['load_manifest']).read_text()+str(U/'comparison-strong-fallback.so')+'\n'+str(opts.cost_root/'cost-profile.so')+'\n')
    c['load_manifest']=str(manifest)
    config=(opts.cost_root/'cost-profile-native-library.json') if opts.cost_profile else U/('strong-profile-native-library.json' if 'strong-profile' in opts.methods else 'comparison-native-library.json');config.write_text(json.dumps(c))
    paths=([str(opts.cost_root)] if opts.cost_profile else [])+[str(U),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]
    paths += [str(q/'.lake/build/lib/lean') for q in (T/'mathlib4/.lake/packages').iterdir() if q.is_dir()]
    os.environ['LEAN_PATH']=os.pathsep.join(paths)
    args=argparse.Namespace(input=opts.input,limit=opts.limit,
       manifest=config,kimina=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d'),
       sdk=T/'lean-4.27.0-linux',project=T/'mathlib4',frozen=U,width=opts.width,
       orders=[opts.methods],repetitions=1,out=opts.out,diagnostic=opts.diagnostic or opts.cost_profile,cost_profile=opts.cost_profile,cost_root=opts.cost_root,numeric_replay_bin=opts.numeric_replay_bin,
       header_timeout=60,batch_timeout=300,finalize_timeout=300,sample_seconds=opts.sample_seconds)
    args.out.mkdir(parents=True,exist_ok=False)
    if opts.reuse_reference is not None:
        os.symlink(opts.reuse_reference.resolve(),args.out/'rep1-fast-hybrid',target_is_directory=True)
    runner=Runner(args);runner.prepare_environment()
    (args.out/'launch.json').write_text(json.dumps({'argv':sys.argv,'pid':os.getpid(),
      'affinity':sorted(os.sched_getaffinity(0)),'methods':opts.methods,'input':str(args.input),
      'limit':opts.limit,'resource_observer_seconds':opts.sample_seconds,'header':'import Mathlib;import Aesop;import GpuArithmetic.Stages',
      'boundary':'existing native batch collector, same imports; original source bodies; stages use sequential thread CPU and invocation wall; whole includes start/preparation/queue/native/fallback/EOF',
      'numeric_replay_bin':str(opts.numeric_replay_bin) if opts.numeric_replay_bin else None,'numeric_replay_data':os.environ.get('GPU_ARITHMETIC_REPLAY_DATA') if opts.numeric_replay_bin else None,'effective_RLIMIT_AS':list(resource.getrlimit(resource.RLIMIT_AS)),'cost_profile':opts.cost_profile,'cost_root':str(opts.cost_root),'collector':str(P)},indent=2)+'\n')
    asyncio.run(runner.run())
if __name__=='__main__':main()
