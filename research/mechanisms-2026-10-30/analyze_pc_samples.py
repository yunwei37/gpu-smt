"""Resolve process-local PC samples with ELF load segments, no PMU or ptrace."""
import argparse, bisect, collections, json, struct, subprocess
from pathlib import Path

def loads(path):
    with path.open("rb") as f:
        head=f.read(64)
        if head[:6]!=bytes([127,69,76,70,2,1]):
            raise ValueError("Expected little-endian ELF64")
        phoff=struct.unpack_from("<Q",head,32)[0]
        phentsize,phnum=struct.unpack_from("<HH",head,54)
        rows=[]
        for i in range(phnum):
            f.seek(phoff+i*phentsize);p=f.read(phentsize)
            typ,flags,offset,vaddr,_,filesz,memsz,align=struct.unpack_from("<IIQQQQQQ",p)
            if typ==1:rows.append((offset,vaddr,filesz,memsz,flags))
        return rows

def symbols(path):
    rows=[]
    # SDK binaries retain local symbols; system libraries may only expose dynsym.
    for dynamic in [False,True]:
        args=["nm","-S","-n","-C","--defined-only"]
        if dynamic:args.append("-D")
        proc=subprocess.Popen(args+[str(path)],stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL,text=True)
        for line in proc.stdout:
            fields=line.rstrip().split(None,3)
            if len(fields)==4 and fields[2] in ("t","T","w","W"):
                try:a,size=int(fields[0],16),int(fields[1],16)
                except ValueError:continue
                if size:rows.append((a,a+size,fields[3]))
        proc.wait()
        if rows:break
    return sorted(rows)

def classify(symbol,module):
    # Disjoint top-level residence categories; inlined operations remain in caller.
    if "lean::ir::interpreter" in symbol or "lean::interpreter" in symbol:
        return "IR_interpreter_residence"
    if any(s in symbol for s in ["lean_dec_ref_cold","lean_inc_ref_cold","lean_inc_ref_n_cold"]):
        return "out_of_line_reference_count_lower_bound"
    if symbol.split("@")[0] in ("free","__libc_free","cfree") or any(s in symbol for s in ["lean_alloc_","lean_free_","lean::lean_alloc","lean::dealloc","lean::allocator::","malloc","calloc","realloc","free("]):
        return "allocation_or_deallocation_lower_bound"
    if any(s in symbol for s in ["hash_table","hash_map","HashMap","HashSet"]):
        return "named_hash_or_table_lower_bound"
    if any(s in symbol for s in ["lean::type_checker::","lean::whnf","lean::kernel","lean_kernel_"]):
        return "named_kernel_residence"
    if "libMathlib" in module:return "Mathlib_native_library_residence"
    if symbol:return "other_named_native_residence"
    return "unresolved"

def analyze(raw):
    maps=[]
    for line in Path(str(raw)+".maps").read_text().splitlines():
        x=line.split(None,5)
        if len(x)<6 or not x[5].startswith("/"):continue
        a,b=(int(z,16) for z in x[0].split("-"))
        maps.append((a,b,int(x[2],16),Path(x[5].removesuffix(" (deleted)"))))
    with raw.open("rb") as f:
        count,capacity,interval,version=struct.unpack("<QQQQ",f.read(32))
        data=[struct.unpack("<QQQ",f.read(24)) for _ in range(min(count,capacity))]
    if version!=1:raise ValueError("Unsupported sampler schema")
    cache={};counts=collections.Counter();cats=collections.Counter();phases=collections.Counter()
    for pc,phase,tid in data:
        phases[phase]+=1
        module="<unmapped>";symbol="";relative=None
        for a,b,offset,path in maps:
            if a<=pc<b:
                module=str(path)
                if path not in cache:
                    try:
                        syms=symbols(path);cache[path]=(loads(path),syms,[s[0] for s in syms])
                    except (OSError,ValueError):cache[path]=([],[],[])
                segs,syms,starts=cache[path]
                filepc=pc-a+offset
                for off,va,fs,ms,flags in segs:
                    if off<=filepc<off+fs:
                        relative=filepc-off+va;break
                if relative is not None:
                    k=bisect.bisect_right(starts,relative)-1
                    for j in range(k,max(-1,k-20),-1):
                        if syms[j][0]<=relative<syms[j][1]:
                            symbol=syms[j][2];break
                break
        counts[(phase,module,symbol)]+=1
        cats[(phase,classify(symbol,module))]+=1
    return {"file":str(raw),"samples_written":count,"samples_retained":len(data),
            "overflow":max(0,count-capacity),"interval_cpu_us":interval,
            "threads":sorted({tid for _,_,tid in data}),
            "phase_counts":dict(phases),
            "category_samples":[{"phase":p,"category":c,"samples":n}for (p,c),n in cats.most_common()],
            "top_symbols":[{"phase":p,"module":m,"symbol":s,"samples":n}for (p,m,s),n in counts.most_common(60)],
            "limits":["CPU timer samples are instruction residence, not PMU cycles/IPC/cache/TLB counts.",
                      "Out-of-line RC/allocation/table categories are lower bounds; inlined work stays in caller.",
                      "No precompilation speedup follows directly from interpreter residence.",
                      "Runtime mappings are start-time snapshot; later loads may be unresolved.",
                      "Sampling must pass native decision/diagnostic/heartbeat differential before interpretation."]}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("raw",type=Path);p.add_argument("--out",type=Path,required=True)
    a=p.parse_args();d=analyze(a.raw);a.out.write_text(json.dumps(d,indent=2)+chr(10))
    print(json.dumps({k:v for k,v in d.items() if k!="top_symbols"},indent=2))
