"""Native warm-batch arithmetic measurement using the existing Kimina collector."""
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
  "header = await exchange({'cmd': HEADER + 'import GpuArithmetic.Stages\\n'}, args.header_timeout)")
ns={'__name__':'arithmetic_native_batch','__file__':str(P)}
exec(compile(source,str(P),'exec'),ns)
Base=ns['Runner']
class Runner(Base):
    def library_path(self, method):
        return os.pathsep.join([str(U),str(self.args.sdk/'lib'),str(self.args.sdk/'lib/lean')]+self.config['library_paths'])
    def repl_path(self, method):
        return T/'repl-kimina-native-gc-header-repair/.lake/build/bin/repl'
    async def cell(self, rep, name, **kwargs):
        if name=='profile':
            os.environ['GPU_ARITHMETIC_PROFILE']='1'
            cellname=kwargs.get('label') or ('rep%d-%s' % (rep,name))
            os.environ['FARKAS_CORPUS_FILE']=str(self.args.out/cellname/'stages.jsonl')
        else:
            os.environ.pop('GPU_ARITHMETIC_PROFILE',None)
            os.environ.pop('FARKAS_CORPUS_FILE',None)
        return await super().cell(rep,name,**kwargs)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--limit',type=int,default=0)
    p.add_argument('--methods',nargs='+',choices=['native','profile'],default=['native','profile'])
    p.add_argument('--width',type=int,default=4)
    opts=p.parse_args()
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_AS,(48*1024**3,48*1024**3))
    os.sched_setaffinity(0,{12,13,14,15})
    c=json.loads((R/'artifacts/lean-modern-native-compilation-2026-10-14/native-library.json').read_text())
    manifest=U/'native-load-with-arithmetic.txt'
    manifest.write_text(Path(c['load_manifest']).read_text()+str(U/'comparison-strong-fallback.so')+'\n')
    c['load_manifest']=str(manifest)
    config=U/'native-library.json';config.write_text(json.dumps(c))
    paths=[str(U),str(F/'.lake/build/lib/lean'),str(T/'mathlib4/.lake/build/lib/lean')]
    paths += [str(q/'.lake/build/lib/lean') for q in (T/'mathlib4/.lake/packages').iterdir() if q.is_dir()]
    os.environ['LEAN_PATH']=os.pathsep.join(paths)
    args=argparse.Namespace(input=A/'input-top1000.jsonl',limit=opts.limit,
       manifest=config,kimina=Path('/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d'),
       sdk=T/'lean-4.27.0-linux',project=T/'mathlib4',frozen=U,width=opts.width,
       orders=[opts.methods],repetitions=1,out=opts.out,
       header_timeout=60,batch_timeout=300,finalize_timeout=300,sample_seconds=1)
    args.out.mkdir(parents=True,exist_ok=False)
    runner=Runner(args);runner.prepare_environment()
    (args.out/'launch.json').write_text(json.dumps({'argv':sys.argv,'pid':os.getpid(),
      'affinity':sorted(os.sched_getaffinity(0)),'methods':opts.methods,'input':str(args.input),
      'limit':opts.limit,'header':'import Mathlib;import Aesop;import GpuArithmetic.Stages',
      'boundary':'existing native batch collector, same imports; original source bodies; stages use sequential thread CPU and invocation wall; whole includes start/preparation/queue/native/fallback/EOF',
      'collector':str(P)},indent=2)+'\n')
    asyncio.run(runner.run())
if __name__=='__main__':main()
