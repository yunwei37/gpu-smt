class Runner(Runner):
    async def cell(self, rep, name, **kwargs):
        os.environ.pop('GPU_ARITHMETIC_STRONG_CPU_SOCKET',None)
        if name!='oracle-gpu':
            return await super().cell(rep,name,**kwargs)
        import subprocess,time
        cellname=kwargs.get('label')or('rep%d-%s'%(rep,name))
        out=self.args.out/(cellname+'-strong-cpu-backend')
        out.mkdir(parents=True,exist_ok=False)
        sock=BATCH/('strong-cpu-%d-%d.sock'%(os.getpid(),rep))
        if sock.exists():raise RuntimeError('existing strong CPU proxy owner')
        argv=['/workspaces/.agent-state/gpu-smt-deps/highs-1.15.1/bin/python',
              '/workspaces/repository/bench/lean-native/linarith-oracle/support-proxy.py',
              '--backend','highs','--negative-certificates','--socket',str(sock),
              '--log',str(out/'support-calls.jsonl')]
        start=time.monotonic_ns()
        log=(out/'support-proxy.log').open('w')
        proc=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT)
        try:
            while not sock.exists():
                if proc.poll()is not None:raise RuntimeError('strong CPU proxy startup failed')
                await asyncio.sleep(.01)
            ready=time.monotonic_ns()
            os.environ['GPU_ARITHMETIC_STRONG_CPU_SOCKET']=str(sock)
            result=await super().cell(rep,name,**kwargs)
        finally:
            cleanup=time.monotonic_ns()
            proc.terminate();proc.wait();log.close();sock.unlink(missing_ok=True)
            os.environ.pop('GPU_ARITHMETIC_STRONG_CPU_SOCKET',None)
            retired=time.monotonic_ns()
        extra=ready-start+retired-cleanup
        result['retained_strong_cpu_proxy_setup_cleanup_ns']=extra
        result['whole_ns']+=extra
        result['portfolio_boundary']='Keep native hybrid and CPU HiGHS contenders, add CUDA; exact repair and parent recheck, cancellation/wait and BOTH host proxy lifecycles charged. Four CPUs and same source concurrency. GPU context cold lifecycle separate.'
        (self.args.out/cellname/'terminal.json').write_text(json.dumps(result,indent=2)+'\n')
        return result
