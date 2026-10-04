#!/usr/bin/env python3
"""Build/run a CUDA loose-bvar metadata pass on a packed real Lean DAG.

--compile-only requires NVRTC but no GPU/driver. Execution uses the NVIDIA
driver supplied through the existing Kubernetes device-plugin/runtime path.
Every returned value is compared with an independent official Lean reference.
This executable does not accept or reject Lean proofs.
"""
import argparse
from array import array
import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import time


def compile_ptx(source, target, nvrtc_path):
    lib = C.CDLL(nvrtc_path)
    def check(result):
        if result: raise RuntimeError(f'NVRTC error {result}')
    program=C.c_void_p()
    lib.nvrtcCreateProgram.argtypes=[C.POINTER(C.c_void_p),C.c_char_p,C.c_char_p,C.c_int,C.c_void_p,C.c_void_p]
    check(lib.nvrtcCreateProgram(C.byref(program),source.read_bytes(),b'dag_bounds.cu',0,None,None))
    options=(C.c_char_p*2)(b'--gpu-architecture=compute_80',b'--std=c++17')
    lib.nvrtcCompileProgram.argtypes=[C.c_void_p,C.c_int,C.POINTER(C.c_char_p)]
    status=lib.nvrtcCompileProgram(program,2,options)
    size=C.c_size_t()
    lib.nvrtcGetProgramLogSize.argtypes=[C.c_void_p,C.POINTER(C.c_size_t)]
    lib.nvrtcGetProgramLog.argtypes=[C.c_void_p,C.c_void_p]
    lib.nvrtcGetProgramLogSize(program,C.byref(size)); log=C.create_string_buffer(size.value)
    lib.nvrtcGetProgramLog(program,log)
    target.with_suffix('.compile.log').write_bytes(log.value)
    check(status)
    lib.nvrtcGetPTXSize.argtypes=[C.c_void_p,C.POINTER(C.c_size_t)]
    lib.nvrtcGetPTX.argtypes=[C.c_void_p,C.c_void_p]
    check(lib.nvrtcGetPTXSize(program,C.byref(size)))
    ptx=C.create_string_buffer(size.value);check(lib.nvrtcGetPTX(program,ptx))
    target.write_bytes(ptx.raw)
    lib.nvrtcDestroyProgram.argtypes=[C.POINTER(C.c_void_p)]
    check(lib.nvrtcDestroyProgram(C.byref(program)))


def execute(args):
    start=time.perf_counter()
    packed=args.input.read_bytes(); reference=args.reference.read_bytes()
    magic,n,waves,roots,reserved=struct.unpack_from('<8sIIII',packed)
    if magic!=b'LBVDAG1\0' or len(reference)!=4*n or reserved:
        raise ValueError('bad input/reference header')
    expected_size=24+20*n+4*n+4*(waves+1)+4*roots
    if len(packed)!=expected_size: raise ValueError('bad input size')
    nodes=packed[24:24+20*n];order=packed[24+20*n:24+24*n]
    offsets=struct.unpack_from(f'<{waves+1}I',packed,24+24*n)
    host_read_s=time.perf_counter()-start
    api=C.CDLL('libcuda.so.1')
    def bind(name,types):
        f=getattr(api,name);f.argtypes=types;f.restype=C.c_int
        def call(*values):
            r=f(*values)
            if r: raise RuntimeError(f'{name}: CUDA driver result {r}')
        return call
    init=bind('cuInit',[C.c_uint]);dev_get=bind('cuDeviceGet',[C.POINTER(C.c_int),C.c_int])
    ctx_create=bind('cuCtxCreate_v2',[C.POINTER(C.c_void_p),C.c_uint,C.c_int])
    alloc=bind('cuMemAlloc_v2',[C.POINTER(C.c_uint64),C.c_size_t])
    free=bind('cuMemFree_v2',[C.c_uint64])
    htod=bind('cuMemcpyHtoD_v2',[C.c_uint64,C.c_void_p,C.c_size_t])
    dtoh=bind('cuMemcpyDtoH_v2',[C.c_void_p,C.c_uint64,C.c_size_t])
    load=bind('cuModuleLoadData',[C.POINTER(C.c_void_p),C.c_void_p])
    getfn=bind('cuModuleGetFunction',[C.POINTER(C.c_void_p),C.c_void_p,C.c_char_p])
    launch=bind('cuLaunchKernel',[C.c_void_p,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_uint,C.c_void_p,C.c_void_p,C.c_void_p])
    sync=bind('cuCtxSynchronize',[])
    context=C.c_void_p();device=C.c_int();module=C.c_void_p();fn=C.c_void_p()
    init_start=time.perf_counter();init(0);dev_get(C.byref(device),0)
    ctx_create(C.byref(context),0,device)
    ptx_bytes=args.ptx.read_bytes()
    ptx=C.create_string_buffer(ptx_bytes);load(C.byref(module),ptx)
    getfn(C.byref(fn),module,b'dag_bounds')
    initialize_s=time.perf_counter()-init_start
    name=C.create_string_buffer(256)
    bind('cuDeviceGetName',[C.c_void_p,C.c_int,C.c_int])(name,256,device)
    driver=C.c_int();bind('cuDriverGetVersion',[C.POINTER(C.c_int)])(C.byref(driver))
    ptrs=[]
    try:
        allocation_start=time.perf_counter()
        for size in [len(nodes),len(order),len(reference)]:
            p=C.c_uint64();alloc(C.byref(p),size);ptrs.append(p)
        allocation_s=time.perf_counter()-allocation_start
        upload_start=time.perf_counter()
        htod(ptrs[0],C.c_char_p(nodes),len(nodes));htod(ptrs[1],C.c_char_p(order),len(order));sync()
        upload_s=time.perf_counter()-upload_start
        create_event=bind('cuEventCreate',[C.POINTER(C.c_void_p),C.c_uint])
        record_event=bind('cuEventRecord',[C.c_void_p,C.c_void_p])
        elapsed_event=bind('cuEventElapsedTime',[C.POINTER(C.c_float),C.c_void_p,C.c_void_p])
        destroy_event=bind('cuEventDestroy_v2',[C.c_void_p])
        e0=C.c_void_p();e1=C.c_void_p();create_event(C.byref(e0),0);create_event(C.byref(e1),0)
        begin=C.c_uint();end=C.c_uint()
        cells=ptrs+[begin,end]
        params=(C.c_void_p*5)(*[C.cast(C.pointer(v),C.c_void_p) for v in cells])
        records=[]
        for rep in range(args.repeat):
            t=time.perf_counter();record_event(e0,None)
            for l in range(waves):
                begin.value=offsets[l];end.value=offsets[l+1]
                if end.value>begin.value:
                    launch(fn,(end.value-begin.value+255)//256,1,1,256,1,1,0,None,params,None)
            record_event(e1,None);sync();wall=time.perf_counter()-t
            ms=C.c_float();elapsed_event(C.byref(ms),e0,e1)
            output=C.create_string_buffer(len(reference)); t=time.perf_counter()
            dtoh(output,ptrs[2],len(reference));sync();download=time.perf_counter()-t
            matches=output.raw==reference
            records.append(dict(repeat=rep,resident_wall_s=wall,cuda_event_ms=ms.value,
                                download_s=download,matches_official_lean=matches))
            if not matches: raise RuntimeError('GPU metadata differs from official Lean')
        destroy_event(e0);destroy_event(e1)
        payload=dict(device=name.value.decode(),driver_version=driver.value,expressions=n,waves=waves,
            input_sha256=hashlib.sha256(packed).hexdigest(),reference_sha256=hashlib.sha256(reference).hexdigest(),
            ptx_sha256=hashlib.sha256(ptx_bytes).hexdigest(),host_read_s=host_read_s,
            initialize_and_jit_s=initialize_s,allocation_s=allocation_s,upload_s=upload_s,
            device_bytes=sum([len(nodes),len(order),len(reference)]),runs=records)
        args.json.write_text(json.dumps(payload,indent=1)+'\n');print(json.dumps(payload))
    finally:
        for p in ptrs: free(p)
        bind('cuCtxDestroy_v2',[C.c_void_p])(context)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--compile-only',action='store_true')
    ap.add_argument('--source',type=Path,default=Path(__file__).parent/'lean-dag/dag_bounds.cu')
    ap.add_argument('--nvrtc',default='/tmp/gpu-smt-cuda-toolkit/nvidia/cuda_nvrtc/lib/libnvrtc.so.12')
    ap.add_argument('--ptx',type=Path,required=True)
    ap.add_argument('--input',type=Path);ap.add_argument('--reference',type=Path)
    ap.add_argument('--repeat',type=int,default=7);ap.add_argument('--json',type=Path)
    args=ap.parse_args()
    if args.compile_only: compile_ptx(args.source,args.ptx,args.nvrtc)
    else:
        if not all([args.input,args.reference,args.json]) or args.repeat<1:
            ap.error('execution requires input, reference, json and positive repeat')
        execute(args)
