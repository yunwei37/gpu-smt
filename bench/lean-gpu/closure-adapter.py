#!/usr/bin/env python3
"""Thin standard lean4export prefix+overlay converter and CPU development adapter.

This is a partial kernel checker, never whole-source acceptance. Trust the
inductives/prefix only after the official independent checker validates them.
No CUDA runtime entry point exists in this development tool.
"""
import argparse
import ctypes as C
import gzip
import json
from array import array
from pathlib import Path
from collections import ChainMap
from collections.abc import Sequence
from itertools import chain
from types import MappingProxyType

NONE = 0xffffffff

class Input(C.Structure):
    _fields_ = [(k, C.c_void_p) for k in ('nodes','levels','decls','rules','ulists','params')] + [(k,C.c_uint32) for k in ('nn','nl','nd','nr','nat','string_','zero','succ','nu','np')]
class Scratch(C.Structure):
    _fields_ = [(k,C.c_void_p) for k in ('terms','envs','levels','frames')] + [('cap',C.c_uint32),('fcap',C.c_uint32)]
class Answer(C.Structure):
    _fields_ = [(k,C.c_uint32) for k in ('verified','reason','steps','terms','frames','envs','levels')]

class PrefixTail(Sequence):
    """Read-only retained prefix with separately writable appended rows."""
    def __init__(self, base): self.base=base; self.tail=[]; self.boundary=len(base)
    def __len__(self): return self.boundary+len(self.tail)
    def __getitem__(self, i):
        if isinstance(i,slice): return [self[k] for k in range(*i.indices(len(self)))]
        if i<0:i+=len(self)
        return self.base[i] if i<self.boundary else self.tail[i-self.boundary]
    def __setitem__(self,i,v):
        if i<self.boundary:raise ValueError('overlay attempts to mutate retained prefix')
        self.tail[i-self.boundary]=v
    def __iter__(self): return chain(self.base,self.tail)
    def append(self,v): self.tail.append(v)
    def extend(self,vs): self.tail.extend(vs)

def load_graph(paths, first=0, base=None, return_state=False):
    if base is None:
        names={0:''}; levels=[(0,0,0)]; nodes=[]; decls=[]; rules=[]; ulists=[]; params=[]
        by_name={};strings={};metadata=[];maxdep=[];seen_meta=False
    else:
        names=ChainMap({},base['names']);by_name=ChainMap({},base['by_name']);strings=ChainMap({},base['strings'])
        levels,nodes,decls,rules,ulists,params,metadata,maxdep=[PrefixTail(base[k]) for k in ('levels','nodes','decls','rules','ulists','params','metadata','maxdep')]
        seen_meta=base['seen_meta']
    pending=[]
    starts={k:len(v) if base is not None else 0 for k,v in [('levels',levels),('nodes',nodes),('decls',decls),('rules',rules)]}
    def put(seq,i,row,empty):
        while len(seq)<=i: seq.append(empty)
        if seq[i]!=empty: raise ValueError(f'duplicate index {i}')
        seq[i]=row
    def add(d,kind):
        if d['name'] in by_name: raise ValueError('duplicate declaration')
        idx=len(decls); by_name[d['name']]=idx
        po=len(params); params.extend(d['levelParams'])
        ro=len(rules)
        for r in d.get('rules',[]): rules.append([r['ctor'],r['nfields'],r['rhs']])
        flags=int(d.get('isUnsafe',False) or d.get('safety','safe')!='safe')
        flags |= int(d.get('isRec',False))*2 | int(d.get('isReflexive',False))*4 | int(d.get('k',False))*8
        ctors=d.get('ctors',[])
        decls.append([kind,d['name'],d['type'],d.get('value',NONE),po,len(d['levelParams']),d.get('numParams',0),d.get('numFields',0),d.get('induct',NONE),d.get('numIndices',0),d.get('numMotives',0),d.get('numMinors',0),ro,len(d.get('rules',[])),flags,ctors[0] if len(ctors)==1 else NONE])
        metadata.append({'index':idx,'name':names[d['name']],'kind':kind,'universe_parameters':len(d['levelParams'])})
    for path in map(Path,paths):
        with (gzip.open if path.suffix=='.gz' else open)(path,'rt') as f:
            for line in f:
                o=json.loads(line)
                if 'meta' in o:
                    seen_meta=True
                    if o['meta']['lean'] != {'version':'4.9.0-rc1','githash':'be6c4894e0a6c542d56a6f4bb1238087267d21a0'}: raise ValueError('kernel semantics pinned to Lean 4.9.0-rc1 be6c4894e0a6c542d56a6f4bb1238087267d21a0')
                    if o['meta']['format']['version'].split('.')[:2] != ['3','1']: raise ValueError('requires standard lean4export 3.1')
                    continue
                if 'in' in o:
                    if o['in'] in names:raise ValueError('duplicate/overwritten name index')
                    k='str' if 'str' in o else 'num';d=o[k];pre=names[d['pre']];names[o['in']]=(pre+'.' if pre else '')+str(d[k] if k=='str' else d['i']);continue
                if 'il' in o:
                    k=next(k for k in o if k!='il');d=o[k]
                    row={'succ':lambda:(1,d,0),'max':lambda:(2,*d),'imax':lambda:(3,*d),'param':lambda:(4,d,0)}[k]()
                    put(levels,o['il'],row,None);continue
                if 'ie' in o:
                    k=next(k for k in o if k!='ie');d=o[k];row=(0,0,0,0,0)
                    if k=='bvar':row=(1,d,0,0,0)
                    elif k=='sort':row=(2,d,0,0,0)
                    elif k=='const':
                        off=len(ulists);ulists.extend(d['us']);row=(3,d['name'],off,len(d['us']),0);pending.append(o['ie'])
                    elif k=='app':row=(4,d['fn'],d['arg'],0,0)
                    elif k in ('lam','forallE'):row=(5 if k=='lam' else 6,d['type'],d['body'],0,0)
                    elif k=='letE':row=(7,d['type'],d['value'],d['body'],int(d.get('nondep',False)))
                    elif k=='natVal':
                        val=int(d);row=(8,val,0,0,0) if 0<=val<NONE else (0,0,0,0,0)
                    elif k=='strVal':row=(9,strings.setdefault(d,len(strings)),0,0,0)
                    elif k=='proj':row=(10,d['typeName'],d['idx'],d['struct'],0)
                    elif k=='mdata':row=(11,d['expr'],0,0,0)
                    put(nodes,o['ie'],row,None);continue
                if 'inductive' in o:
                    for key,kind in [('types',4),('ctors',5),('recs',6)]:
                        for d in o['inductive'][key]:add(d,kind)
                else:
                    for key,kind in [('def',1),('thm',2),('opaque',3),('axiom',7),('quot',8)]:
                        if key in o:add(o[key],kind);break
                    else:raise ValueError(f'unknown export record: {list(o)}')
    for i in pending:
        n=list(nodes[i]);n[1]=by_name.get(n[1],NONE);nodes[i]=tuple(n)
    if not seen_meta:raise ValueError('missing exact-version export metadata')
    for i in range(starts['nodes'],len(nodes)):
        n=nodes[i]
        if n is None:raise ValueError(f'missing expression index {i}')
        if n[0]==10:n=list(n);n[1]=by_name.get(n[1],NONE);nodes[i]=tuple(n)
    for d in (decls[i] for i in range(starts['decls'],len(decls))):
        d[8]=by_name.get(d[8],NONE);d[15]=by_name.get(d[15],NONE)
    for r in (rules[i] for i in range(starts['rules'],len(rules))):r[0]=by_name.get(r[0],NONE)
    if any(levels[i] is None for i in range(starts['levels'],len(levels))):raise ValueError('missing universe index')
    if not 0<=first<=len(decls):raise ValueError('invalid retained prefix boundary')
    # Enforce acyclic AST/level tables. Definitions may only use prior declared
    # constants; same-block inductive metadata is trusted only via CPU validation.
    for i in range(starts['nodes'],len(nodes)):
        n=nodes[i]
        tag,a,b,c,_=n
        children={4:(a,b),5:(a,b),6:(a,b),7:(a,b,c),10:(c,),11:(a,)}.get(tag,())
        if any(ch>=i for ch in children):raise ValueError('non-topological expression table')
        if tag==2 and a>=len(levels):raise ValueError('bad sort universe')
        if tag==3 and (a==NONE or any(l>=len(levels) for l in ulists[b:b+c])):raise ValueError('unresolved constant or universe')
    for i in range(starts['levels'],len(levels)):
        l=levels[i]
        if l[0] in (1,2,3) and (l[1]>=i or (l[0]!=1 and l[2]>=i)):raise ValueError('non-topological universe table')
    # Check dependency order on declaration type/body, without recursively walking
    # Python stacks or scanning unrelated prefix graphs per declaration.
    for n in (nodes[i] for i in range(starts['nodes'],len(nodes))):
        tag,a,b,c,_=n;children={4:(a,b),5:(a,b),6:(a,b),7:(a,b,c),10:(c,),11:(a,)}.get(tag,())
        maxdep.append(max(([a] if tag==3 else [])+[maxdep[ch] for ch in children],default=-1))
    for i in range(starts['decls'],len(decls)):
        d=decls[i]
        if d[2]>=len(nodes) or (d[0] in (1,2,3) and d[3]>=len(nodes)):raise ValueError('bad declaration term reference')
        if d[0]==5 and (d[8]>=len(decls) or decls[d[8]][0]!=4):raise ValueError('bad constructor inductive metadata')
        if d[15]!=NONE and (d[15]>=len(decls) or decls[d[15]][0]!=5):raise ValueError('bad single-constructor metadata')
        if any(d[k]>65535 for k in (6,7,9,10,11,13)):raise ValueError('unsupported oversized inductive metadata')
        if d[0] in (1,2,3,7,8):
            for t in [d[2]]+([d[3]] if d[0] in (1,2,3) else []):
                if t>=len(nodes) or maxdep[t]>=i:raise ValueError('forward/self declaration reference')
        if len(set(params[d[4]:d[4]+d[5]]))!=d[5]:raise ValueError('duplicate universe parameter')
    for r in (rules[i] for i in range(starts['rules'],len(rules))):
        if r[0]>=len(decls) or decls[r[0]][0]!=5 or r[2]>=len(nodes) or r[1]>65535:raise ValueError('bad recursor rule metadata')
    by_text={names[n]:i for n,i in (by_name.items() if base is None else by_name.maps[0].items())}
    if base is not None:by_text=ChainMap(by_text,base['by_text'])
    rows={'nodes':nodes,'levels':levels,'decls':decls,'rules':rules,'ulists':ulists,'params':params}
    tails={k:array('I',(v for row in (rows[k].tail if base is not None else rows[k]) for v in row)).tobytes() if k not in ('ulists','params') else array('I',rows[k].tail if base is not None else rows[k]).tobytes() for k in rows}
    blobs={k:(base['blobs'][k]+tails[k] if base is not None else tails[k]) for k in rows}
    meta=dict(nn=len(nodes),nl=len(levels),nd=len(decls),nr=len(rules),nu=len(ulists),np=len(params),nat=by_text.get('Nat',NONE),string_=by_text.get('String',NONE),zero=by_text.get('Nat.zero',NONE),succ=by_text.get('Nat.succ',NONE),declarations=metadata[first:],queries=list(range(first,len(decls))))
    if return_state:
        state=dict(rows,names=names,by_name=by_name,strings=strings,metadata=metadata,maxdep=maxdep,by_text=by_text,blobs=blobs,blob_tails=tails,seen_meta=seen_meta)
        for k in ('nodes','levels','decls','rules','ulists','params','metadata','maxdep'):
            v=state[k]
            if base is None:state[k]=tuple(tuple(r) if isinstance(r,list) else r for r in v)
            else:v.tail=tuple(tuple(r) if isinstance(r,list) else r for r in v.tail)
        for k in ('names','by_name','strings','by_text'):
            v=state[k]
            state[k]=MappingProxyType(v) if base is None else ChainMap(MappingProxyType(v.maps[0]),base[k])
        return blobs,meta,state
    return blobs,meta

def prepare(blobs,meta,capacity=65536,frames=8192):
    buffers=[C.create_string_buffer(blobs[k] or b'\0'*4) for k in ('nodes','levels','decls','rules','ulists','params')]
    inp=Input(*[C.cast(b,C.c_void_p) for b in buffers],*[meta[k] for k in ('nn','nl','nd','nr','nat','string_','zero','succ','nu','np')])
    scratch_buffers=[C.create_string_buffer(capacity*28),C.create_string_buffer(capacity*12),C.create_string_buffer(capacity*12),C.create_string_buffer(frames*52)]
    scratch=Scratch(*[C.cast(b,C.c_void_p) for b in scratch_buffers],capacity,frames)
    return inp,scratch,buffers,scratch_buffers

def cpu_run(blobs,meta,library,capacity=65536,frames=8192,steps=2000000):
    inp,scratch,buffers,work=prepare(blobs,meta,capacity,frames)
    queries=(C.c_uint32*len(meta['queries']))(*meta['queries']);answers=(Answer*len(queries))()
    lib=C.CDLL(str(Path(library).resolve()));f=lib.closure_check_cpu
    f.argtypes=[Input,Scratch,C.POINTER(C.c_uint32),C.c_uint32,C.POINTER(Answer),C.c_uint32];f.restype=None
    f(inp,scratch,queries,len(queries),answers,steps)
    return [dict(info,**{k:getattr(a,k) for k,_ in Answer._fields_}) for info,a in zip(meta['declarations'],answers)]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inputs',type=Path,nargs='+',required=True);p.add_argument('--first-declaration',type=int,required=True);p.add_argument('--cpu-library',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--capacity',type=int,default=65536);p.add_argument('--frames',type=int,default=8192)
    a=p.parse_args();blobs,meta=load_graph(a.inputs,a.first_declaration);rows=cpu_run(blobs,meta,a.cpu_library,a.capacity,a.frames)
    a.out.mkdir(parents=True,exist_ok=False);(a.out/'answers.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps({'checked':len(rows),'verified':sum(r['verified'] for r in rows),'scope':'partial kernel declarations; all failures and trusted metadata require official CPU'}))
if __name__=='__main__':main()
