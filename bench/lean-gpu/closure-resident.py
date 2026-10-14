#!/usr/bin/env python3
"""Resident CUDA Driver adapter for the frozen partial closure checker.

Matches sokonanoda_gpu_resident_service.rs Worker stdin/stdout protocol. Only
CPU/CUDA-matching positive declaration checks discharge; official checking owns
prefix, metadata, all remaining declarations and whole-source acceptance.
No native Meta integration. Import and static inspection do not load CUDA.
"""
import argparse
import ctypes as C
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import struct
import sys
import time
from array import array

KEYS=('nodes','levels','decls','rules','ulists','params')
SCALARS=('nn','nl','nd','nr','nat','string_','zero','succ','nu','np')
FIELDS=('verified','reason','steps','terms','frames','envs','levels')
FROZEN={
 'engine':'875dea76be6ba4a3acf16659653bead5e6330a8d3ef8241946285d1b2571ef09',
 'adapter':'f77d83a5c9c3ccadcd9ed822713b247f4cef0c28a8ccc4282591825970249eea',
 'cpu_library':'9cfe1f6bf9c71fbfe9e9c7454d6f02e237f48e0835dd844c429349ce3fcf2f53',
 'ptx':'4e4b7a78c8da2ae1b90b265b09e27038530e9b9cf8c379d7491fc039b30f6356'}
MEMORY_SCOPE='explicit cuMemAlloc allocations only; excludes context/module/JIT/default stack/driver allocations and other owners'

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def write_json(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def emit(value):print(json.dumps(value),flush=True)
def error_text(exc):return f'{type(exc).__name__}: {exc}'

def load_adapter(path):
    spec=importlib.util.spec_from_file_location('frozen_closure_adapter',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    if C.sizeof(module.Input)!=88 or C.sizeof(module.Answer)!=28:raise RuntimeError('frozen ABI size mismatch')
    expected=[0,8,16,24,32,40,48,52,56,60,64,68,72,76,80,84]
    if [getattr(module.Input,k).offset for k,_ in module.Input._fields_]!=expected:raise RuntimeError('frozen Input layout mismatch')
    if sys.byteorder!='little' or C.sizeof(C.c_void_p)!=8:raise RuntimeError('requires little-endian 64-bit host ABI')
    return module

class Device:
    """One ordinary context, shared immutable prefix and reusable query arenas."""
    def __init__(self,ptx,prefix,out):
        self.api=C.CDLL('libcuda.so.1');self.prefix=prefix;self.buffers={};self.allocations={}
        self.ctx=C.c_void_p();self.module=C.c_void_p();self.fn=C.c_void_p();self.name=None
        self.events=(out/'driver-events.jsonl').open('a');self.peak=0;self.calls=0;self.htod=0;self.dtoh=0
        self.init_seconds=0;self.prefix_seconds=0;self.last_stats={};self.close_errors=[]
        p=C.c_void_p;u=C.c_uint32;ptr=C.c_uint64
        self.alloc=self.bind('cuMemAlloc_v2',[C.POINTER(ptr),C.c_size_t])
        self.free=self.bind('cuMemFree_v2',[ptr])
        self.upload=self.bind('cuMemcpyHtoD_v2',[ptr,p,C.c_size_t])
        self.download=self.bind('cuMemcpyDtoH_v2',[p,ptr,C.c_size_t])
        self.sync=self.bind('cuCtxSynchronize',[])
        self.launch=self.bind('cuLaunchKernel',[p,u,u,u,u,u,u,u,p,p,p])
        start=time.perf_counter();init_start=start;phase='driver_initialization'
        try:
            self.bind('cuInit',[u])(0);dev=C.c_int()
            self.bind('cuDeviceGet',[C.POINTER(C.c_int),C.c_int])(C.byref(dev),0)
            name=C.create_string_buffer(256)
            self.bind('cuDeviceGetName',[p,C.c_int,C.c_int])(name,256,dev)
            self.name=name.value.decode()
            if not re.search(r'\bRTX\s*5090\b',self.name,re.IGNORECASE):raise RuntimeError(f'only RTX5090 authorized; actual device {self.name}')
            self.bind('cuCtxCreate_v2',[C.POINTER(p),u,C.c_int])(C.byref(self.ctx),0,dev)
            # No cuCtxSetLimit: frozen engine uses explicit continuations.
            source=C.create_string_buffer(Path(ptx).read_bytes())
            self.bind('cuModuleLoadData',[C.POINTER(p),p])(C.byref(self.module),source)
            self.bind('cuModuleGetFunction',[C.POINTER(p),p,C.c_char_p])(C.byref(self.fn),self.module,b'closure_check_device')
            self.init_seconds=time.perf_counter()-start;start=time.perf_counter();phase='prefix_allocation_upload'
            for key in KEYS:
                ptr,_=self.buffer(key,len(prefix[key]))
                self.put(ptr,prefix[key])
            self.sync();self.prefix_seconds=time.perf_counter()-start
            write_json(out/'device-initialization.json',dict(success=True,device=self.name,device_init_jit_seconds=self.init_seconds,prefix_upload_seconds=self.prefix_seconds,allocation_calls=self.calls,uploaded_bytes=self.htod,explicit_allocation_bytes=self.owned_bytes(),explicit_peak_bytes=self.peak,memory_scope=MEMORY_SCOPE,context_stack_limit_override=False,whole_seconds=time.perf_counter()-init_start))
        except Exception as exc:
            if phase=='driver_initialization':self.init_seconds=time.perf_counter()-start
            else:self.prefix_seconds=time.perf_counter()-start
            failure=dict(success=False,error=error_text(exc),phase=phase,device=self.name,device_init_jit_seconds=self.init_seconds,prefix_upload_partial_seconds=self.prefix_seconds,allocation_calls=self.calls,uploaded_bytes=self.htod,explicit_allocation_bytes=self.owned_bytes(),explicit_peak_bytes=self.peak,memory_scope=MEMORY_SCOPE,context_stack_limit_override=False,whole_seconds=time.perf_counter()-init_start)
            try:failure['close']=self.close()
            except Exception as close_exc:failure['close_error']=error_text(close_exc)
            write_json(out/'device-initialization.json',failure);raise

    def log(self,event):
        self.events.write(json.dumps(dict(time_ns=time.time_ns(),**event))+'\n');self.events.flush()

    def bind(self,name,types):
        fn=getattr(self.api,name);fn.argtypes=types;fn.restype=C.c_int
        def call(*args):
            start=time.perf_counter();code=fn(*args)
            self.log(dict(api=name,code=code,seconds=time.perf_counter()-start))
            if code:raise RuntimeError(f'{name}: CUDA driver code {code}')
        return call

    def owned_bytes(self):return sum(self.allocations.values())

    def buffer(self,key,size):
        size=max(4,size);old=self.buffers.get(key)
        if old and old[1]>=size:return old[0],False
        mem=C.c_uint64();self.alloc(C.byref(mem),size)
        self.calls+=1;self.allocations[mem.value]=size;self.peak=max(self.peak,self.owned_bytes())
        self.log(dict(event='allocated',buffer=key,bytes=size,explicit_current=self.owned_bytes(),explicit_peak=self.peak))
        # Allocate first: an allocation failure leaves the previous prefix intact.
        if old:
            self.free(old[0]);del self.allocations[old[0].value]
        self.buffers[key]=(mem,size)
        return mem,True

    def put(self,ptr,data,offset=0):
        if data:
            self.upload(C.c_uint64(ptr.value+offset),C.c_char_p(data),len(data));self.htod+=len(data)

    def run(self,adapter,tail,meta,capacity,frames,steps):
        nq=len(meta['queries']);before_upload=self.htod;before_download=self.dtoh;before_alloc=self.calls
        stats=self.last_stats=dict(device=self.name,actual_launch=False,nq=nq,memory_scope=MEMORY_SCOPE,
                                  context_stack_limit_override=False)
        if not nq:
            stats.update(no_declarations=True,owned_allocation_bytes=self.owned_bytes(),owned_allocation_peak_bytes=self.peak)
            return b'',stats
        start=time.perf_counter();device_inputs=[]
        for key in KEYS:
            prefix=self.prefix[key];appended=tail[key]
            mem,grown=self.buffer(key,len(prefix)+len(appended))
            if grown:self.put(mem,prefix)
            self.put(mem,appended,len(prefix));device_inputs.append(C.c_void_p(mem.value))
        query_data=array('I',meta['queries']).tobytes();queries,_=self.buffer('queries',len(query_data));self.put(queries,query_data)
        terms,_=self.buffer('terms',nq*capacity*28);envs,_=self.buffer('envs',nq*capacity*12)
        levels,_=self.buffer('runtime_levels',nq*capacity*12);continuations,_=self.buffer('frames',nq*frames*52)
        output,_=self.buffer('answers',nq*28)
        # Each engine execute() creates zero counters, so old arena bytes are
        # unreachable. Each thread uses its own q*capacity/q*frames region.
        self.sync()
        stats.update(allocation_and_overlay_upload_seconds=time.perf_counter()-start,
                     uploaded_bytes=self.htod-before_upload,allocation_calls=self.calls-before_alloc,
                     owned_allocation_bytes=self.owned_bytes(),owned_allocation_peak_bytes=self.peak,
                     scratch_reserved_bytes=nq*(capacity*52+frames*52),
                     fresh_candidate_state='engine counters reset; caller arenas retained')
        inp=adapter.Input(*device_inputs,*[meta[k] for k in SCALARS])
        args=[inp,terms,envs,levels,continuations,C.c_uint32(capacity),C.c_uint32(frames),queries,
              C.c_uint32(nq),output,C.c_uint32(steps)]
        params=(C.c_void_p*len(args))(*[C.cast(C.pointer(x),C.c_void_p) for x in args])
        start=time.perf_counter();self.launch(self.fn,(nq+31)//32,1,1,32,1,1,0,None,params,None)
        stats['actual_launch']=True;self.sync();stats['launch_sync_seconds']=time.perf_counter()-start
        raw=C.create_string_buffer(nq*28);start=time.perf_counter()
        self.download(raw,output,len(raw));self.dtoh+=len(raw);self.sync()
        stats.update(download_seconds=time.perf_counter()-start,downloaded_bytes=self.dtoh-before_download)
        return raw.raw,stats

    def close(self):
        start=time.perf_counter();errors=[]
        for address in list(self.allocations):
            try:self.free(C.c_uint64(address));del self.allocations[address]
            except Exception as exc:errors.append(error_text(exc))
        if self.module.value:
            try:self.bind('cuModuleUnload',[C.c_void_p])(self.module)
            except Exception as exc:errors.append(error_text(exc))
            self.module=C.c_void_p()
        if self.ctx.value:
            try:self.bind('cuCtxDestroy_v2',[C.c_void_p])(self.ctx)
            except Exception as exc:errors.append(error_text(exc))
            self.ctx=C.c_void_p()
        self.buffers.clear();self.close_errors.extend(errors)
        report=dict(close_seconds=time.perf_counter()-start,errors=errors,
                    explicit_bytes_at_close=self.owned_bytes(),explicit_peak_bytes=self.peak,memory_scope=MEMORY_SCOPE)
        self.log(dict(event='device_closed',**report));self.events.close()
        return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix',type=Path,required=True);parser.add_argument('--first-declaration',type=int,required=True)
    parser.add_argument('--cpu-library',type=Path,required=True);parser.add_argument('--ptx',type=Path)
    parser.add_argument('--out',type=Path,required=True);parser.add_argument('--capacity',type=int,default=65536)
    parser.add_argument('--frames',type=int,default=8192);parser.add_argument('--steps',type=int,default=2000000)
    parser.add_argument('--adapter',type=Path,default=Path(__file__).with_name('closure-adapter.py'))
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=False);begin=time.perf_counter()
    device=None;count=0;candidate_errors=0;device_error=None;ready=False;terminal_error=None;close_report=None
    try:
        if min(args.capacity,args.frames,args.steps)<=0 or max(args.capacity,args.frames,args.steps)>0xffffffff:raise ValueError('arena/step counts require positive uint32')
        hashes=dict(worker=digest(__file__),adapter=digest(args.adapter),cpu_library=digest(args.cpu_library))
        engine_path=Path(__file__).with_name('closure-checker.cu')
        if engine_path.is_file():
            hashes['engine']=digest(engine_path)
            if hashes['engine']!=FROZEN['engine']:raise RuntimeError('frozen engine source identity differs')
        if args.ptx:hashes['ptx']=digest(args.ptx)
        for key in ('adapter','cpu_library','ptx'):
            if key in hashes and hashes[key]!=FROZEN[key]:raise RuntimeError(f'frozen {key} identity differs')
        adapter=load_adapter(args.adapter);convert=time.perf_counter()
        blobs,meta,base=adapter.load_graph([args.prefix],args.first_declaration,return_state=True)
        if meta['nd']!=args.first_declaration:raise ValueError('prefix declaration boundary differs')
        prefix_conversion=time.perf_counter()-convert;prefix_hash=digest(args.prefix)
        if args.ptx:
            device_attempt_start=time.perf_counter()
            try:device=Device(args.ptx,blobs,args.out)
            except Exception as exc:
                device_error=error_text(exc)
                if not (args.out/'device-initialization.json').is_file():
                    write_json(args.out/'device-initialization.json',dict(success=False,error=device_error,phase='driver_library_or_binding',whole_seconds=time.perf_counter()-device_attempt_start,memory_scope=MEMORY_SCOPE,context_stack_limit_override=False))
        prefix_report=dict(event='worker_ready',ready=bool(device),prefix_declarations=meta['nd'],prefix_sha256=prefix_hash,
                           prefix_conversion_seconds=prefix_conversion,source_hashes=hashes,engine_expected_sha256=FROZEN['engine'],
                           device=device.name if device else None,device_error=device_error,
                           device_init_jit_seconds=device.init_seconds if device else None,
                           prefix_upload_seconds=device.prefix_seconds if device else None,
                           explicit_allocation_bytes=device.owned_bytes() if device else None,memory_scope=MEMORY_SCOPE,
                           capacity=args.capacity,frames=args.frames,steps=args.steps,
                           whole_seconds=time.perf_counter()-begin,actual_gpu=device is not None,
                           initialization=json.loads((args.out/'device-initialization.json').read_text()) if (args.out/'device-initialization.json').is_file() else None,
                           scope='partial declaration worker; readiness is actual initialization, not semantic/performance evidence')
        write_json(args.out/'prefix.json',prefix_report);emit(prefix_report);ready=True
        for line in sys.stdin:
            if not line.strip():continue
            source=Path(line.strip());folder=args.out/f'candidate-{count}';folder.mkdir();start=time.perf_counter()
            info=None;rows=[];cpu_rows=[];cpu=b'';actual=None;stats=None;err=None;matched=False;conversion=None;cpu_seconds=None;overlay_hash=None
            try:
                overlay_hash=digest(source);convert=time.perf_counter()
                full,info,overlay=adapter.load_graph([source],args.first_declaration,base=base,return_state=True)
                conversion=time.perf_counter()-convert;cpu_start=time.perf_counter()
                cpu_rows=adapter.cpu_run(full,info,args.cpu_library,args.capacity,args.frames,args.steps)
                cpu_seconds=time.perf_counter()-cpu_start
                cpu=b''.join(struct.pack('<7I',*[r[k] for k in FIELDS]) for r in cpu_rows)
                (folder/'cpu-answers.bin').write_bytes(cpu)
                if device:
                    try:actual,stats=device.run(adapter,overlay['blob_tails'],info,args.capacity,args.frames,args.steps)
                    except Exception as exc:
                        stats=device.last_stats;device_error=error_text(exc);close_report=device.close();device=None
                        raise RuntimeError(device_error) from exc
                    (folder/'answers.bin').write_bytes(actual)
                    matched=actual==cpu
                    rows=[dict(d,**dict(zip(FIELDS,answer)),serialized_name=overlay['decls'][d['index']][1])
                          for d,answer in zip(info['declarations'],struct.iter_unpack('<7I',actual))]
                    if not matched:raise RuntimeError('CPU/CUDA answer bytes differ; zero declaration discharge')
                else:err=device_error or 'PTX omitted; no GPU declaration discharge'
            except Exception as exc:err=error_text(exc)
            if err:candidate_errors+=1
            verified=[r['serialized_name'] for r in rows if r['verified']] if matched and not err else []
            report=dict(event='candidate',ordinal=count,overlay=str(source),prefix_sha256=prefix_hash,
                        overlay_sha256=overlay_hash,source_hashes=hashes,engine_expected_sha256=FROZEN['engine'],
                        conversion_seconds=conversion,cpu_control_seconds=cpu_seconds,
                        cpu_control_scope='same frozen algorithm control; online CPU replay cost included',
                        gpu=stats,error=err,cpu_cuda_bytes_equal=matched,
                        cpu_answers_sha256=hashlib.sha256(cpu).hexdigest() if cpu else None,
                        answers_sha256=hashlib.sha256(actual).hexdigest() if actual is not None else None,
                        declarations=rows,cpu_control_declarations=cpu_rows,total_declarations=len(info['queries']) if info else None,
                        verified_declarations=len(verified),verified_names=verified,
                        actual_gpu=bool(stats and stats.get('actual_launch')),whole_candidate_seconds=time.perf_counter()-start,
                        scope='partial candidate declaration checks; official prefix/metadata/undecided checks required')
            write_json(folder/'result.json',report)
            emit(dict(event='candidate',ordinal=count,verified_names=verified,verified_declarations=len(verified),actual_gpu=report['actual_gpu'],error=err,cpu_cuda_bytes_equal=matched))
            count+=1
    except Exception as exc:
        terminal_error=error_text(exc)
        if not ready:
            record=dict(event='worker_error',error=terminal_error,actual_gpu=False,verified_names=[])
            write_json(args.out/'startup-error.json',record);emit(record)
    finally:
        if device:
            try:close_report=device.close()
            except Exception as exc:
                close_report=dict(error=error_text(exc));terminal_error=terminal_error or error_text(exc)
        terminal=dict(event='worker_finished',candidates=count,candidate_errors=candidate_errors,
                      error=terminal_error,device_error=device_error,device_close=close_report,
                      whole_seconds=time.perf_counter()-begin,normal_eof=ready and terminal_error is None)
        write_json(args.out/'terminal.json',terminal);emit(terminal)
    return 1 if terminal_error else 0

if __name__=='__main__':raise SystemExit(main())
