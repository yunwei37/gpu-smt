#!/usr/bin/env python3
"""Tiny standard-record adapter development controls; not an official kernel oracle."""
import ctypes as C
import importlib.util
import json
import tempfile
from pathlib import Path
import sys
spec=importlib.util.spec_from_file_location('closure_adapter',Path(__file__).with_name('closure-adapter.py'));a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
lib=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
rows=[{'meta':{'lean':{'version':'4.9.0-rc1','githash':'be6c4894e0a6c542d56a6f4bb1238087267d21a0'},'format':{'version':'3.1.0'},'exporter':{'name':'lean4export','version':'3.1.0'}}}]
names={};nodes=[]
def name(s):
 i=len(names)+1;names[s]=i;rows.append({'str':{'str':s,'pre':0},'in':i});return i
def n(k,d):
 i=len(nodes);nodes.append((k,d));rows.append({k:d,'ie':i});return i
u=name('u');natname=name('Nat');zeroname=name('Nat.zero');succname=name('Nat.succ');idname=name('identity');callname=name('identityNat');badname=name('invalidLet')
rows += [{'succ':0,'il':1},{'param':u,'il':2},{'succ':2,'il':3}]
sort1=n('sort',1);nat=n('const',{'name':natname,'us':[]});b0=n('bvar',0);b1=n('bvar',1);natpi=n('forallE',{'type':nat,'body':nat})
rows.append({'inductive':{'types':[{'name':natname,'levelParams':[],'type':sort1,'all':[natname],'ctors':[zeroname,succname],'isRec':True,'isReflexive':False,'numIndices':0,'numNested':0,'numParams':0,'isUnsafe':False}], 'ctors':[{'name':zeroname,'levelParams':[],'type':nat,'isUnsafe':False,'cidx':0,'numParams':0,'numFields':0,'induct':natname},{'name':succname,'levelParams':[],'type':natpi,'isUnsafe':False,'cidx':1,'numParams':0,'numFields':1,'induct':natname}], 'recs':[]}})
sortu=n('sort',3);inner=n('lam',{'type':b0,'body':b0});body=n('lam',{'type':sortu,'body':inner});innerpi=n('forallE',{'type':b0,'body':b1});typ=n('forallE',{'type':sortu,'body':innerpi})
rows.append({'def':{'name':idname,'levelParams':[u],'type':typ,'value':body,'safety':'safe','hints':'abbrev'}})
id0=n('const',{'name':idname,'us':[0]});toNat=n('app',{'fn':id0,'arg':nat});seven=n('natVal','7');applied=n('app',{'fn':toNat,'arg':seven})
rows.append({'def':{'name':callname,'levelParams':[],'type':nat,'value':applied,'safety':'safe','hints':'abbrev'}})
badlet=n('letE',{'type':sort1,'value':seven,'body':b0,'nondep':False})
rows.append({'def':{'name':badname,'levelParams':[],'type':nat,'value':badlet,'safety':'safe','hints':'abbrev'}})
# Split precisely at a declaration boundary to exercise retained prefix + overlay.
split=next(i for i,r in enumerate(rows) if 'ie' in r and r['ie']==sortu)
prefix=out/'control-prefix.ndjson';overlay=out/'control-overlay.ndjson'
prefix.write_text(''.join(json.dumps(r)+'\n' for r in rows[:split]));overlay.write_text(''.join(json.dumps(r)+'\n' for r in rows[split:]))
blobs,meta=a.load_graph([prefix,overlay],3)
_,prefix_meta,state=a.load_graph([prefix],0,return_state=True)
reused,reused_meta,overlay_state=a.load_graph([overlay],prefix_meta["nd"],base=state,return_state=True)
assert blobs==reused and meta==reused_meta
assert len(state["nodes"])==sortu and len(overlay_state["nodes"])==len(nodes)
answers=a.cpu_run(blobs,meta,lib)
assert [r['verified'] for r in answers]==[1,1,0],answers
assert answers[-1]['reason']!=0
# Dynamic operation returns materialized closure IDs in retained scratch.
inp,z,keep,work=a.prepare(blobs,meta);dll=C.CDLL(str(lib.resolve()));f=dll.closure_operation_cpu
f.argtypes=[a.Input,a.Scratch,C.c_uint32,C.c_uint32,C.c_uint32,C.c_uint32,C.POINTER(C.c_uint32)];f.restype=a.Answer
ret=C.c_uint32();res=f(inp,z,1,applied,0,2000000,C.byref(ret));assert not res.verified and res.reason==12
terms=C.cast(z.terms,C.POINTER(C.c_uint32));assert terms[ret.value*7]==8 and terms[ret.value*7+1]==7
# Structural recursor fields are serialized exactly from standard exporter keys.
# This metadata-only check is explicitly not validating the synthetic declaration.
name_rec=name('Nat.rec.control');rows.append({'inductive':{'types':[],'ctors':[],'recs':[{'name':name_rec,'levelParams':[u],'type':typ,'isUnsafe':False,'numParams':2,'numIndices':3,'numMotives':4,'numMinors':5,'rules':[{'ctor':succname,'nfields':1,'rhs':inner}], 'all':[natname],'k':True}]}})
metadata=out/'metadata-control.ndjson';metadata.write_text(''.join(json.dumps(r)+'\n' for r in rows));bb,mm=a.load_graph([metadata],3)
d=array_decl=C.cast(C.create_string_buffer(bb['decls']),C.POINTER(C.c_uint32));last=(mm['nd']-1)*16
assert [d[last+k] for k in (6,9,10,11,13,14)]==[2,3,4,5,1,8]
(out/'adapter-controls.json').write_text(json.dumps({'declarations':answers,'dynamic_whnf_literal':7,'standard_rec_metadata':'serialized fields checked; synthetic metadata not validated','scope':'development controls only; no official oracle or GPU execution'},indent=2)+'\n')
print('PASS standard NDJSON retained prefix+overlay, polymorphic dependent identity, instantiated application, invalid let, dynamic WHNF API and recursor metadata packing')
