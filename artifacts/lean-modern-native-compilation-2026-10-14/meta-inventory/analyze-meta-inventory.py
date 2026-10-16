#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,json,struct,collections
MAGIC=0x47534d5444455131
FLAGS=['expression_metavariable','universe_metavariable','free_variable','loose_bound_variable','level_parameter','pointer_identical']
def analyze(folder):
    totals={n:[0]*64 for n in ['all_entered','all_completed','outer_entered','outer_completed','outer_cpu_ns']}
    files=[];errors=[]
    for p in sorted(folder.glob('*.bin')):
        data=p.read_bytes()
        if len(data)!=2624:
            errors.append(dict(path=str(p),error='size',bytes=len(data)));continue
        v=struct.unpack('<328Q',data)
        if v[0]!=MAGIC or v[1]!=1:
            errors.append(dict(path=str(p),error='header',magic=v[0],version=v[1]));continue
        row=dict(path=str(p),pid=v[2],tid=v[3],open_wrapped_depth=v[4],max_wrapped_depth=v[5],clock_errors=v[6],created_monotonic_ns=v[7])
        proc=Path('/proc')/str(v[2])
        try:row['same_observed_native_alive']=(proc/'exe').resolve()==Path('/tmp/gpu-smt-meta-inventory-20261016/repl-meta-inventory')
        except OSError:row['same_observed_native_alive']=False
        arrays={}
        for j,k in enumerate(totals):
            a=list(v[8+64*j:8+64*(j+1)]);arrays[k]=a
            totals[k]=[x+y for x,y in zip(totals[k],a)]
        row['all_entered']=sum(arrays['all_entered']);row['all_completed']=sum(arrays['all_completed'])
        row['outer_entered']=sum(arrays['outer_entered']);row['outer_completed']=sum(arrays['outer_completed'])
        row['outer_cpu_ns']=sum(arrays['outer_cpu_ns'])
        row['counts_consistent']=all(arrays['all_completed'][i]<=arrays['all_entered'][i] and arrays['outer_completed'][i]<=arrays['outer_entered'][i] and arrays['outer_entered'][i]<=arrays['all_entered'][i] for i in range(64))
        files.append(row)
    categories=[]
    for i in range(64):
        categories.append(dict(category=i,flags={k:bool(i&(1<<j))for j,k in enumerate(FLAGS)},**{k:a[i]for k,a in totals.items()}))
    return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),folder=str(folder),files=files,errors=errors,
        totals={k:sum(a)for k,a in totals.items()},categories=categories,
        scope='Aggregate observation of wrapped export calls only; private/same-object calls may bypass wrapping. Only outermost completed wrapped calls carry per-thread instrumented CPUtime, including nested observation overhead. Header/import and body work coexist. Live files are non-atomic snapshots; killed/in-progress/failed-init/clock-error work is incomplete. No whole/nativeCPU fraction, cache hit, parallel readiness, GPU eligibility, uninstrumented cost, Amdahl bound or speedup.')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);args=ap.parse_args()
    x=analyze(args.folder)
    path=args.folder.parent/(args.folder.name+'-analysis.json')
    path.write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps(dict(output=str(path),files=len(x['files']),errors=x['errors'],totals=x['totals'],
        live=sum(r['same_observed_native_alive']for r in x['files']),clock_errors=sum(r['clock_errors']for r in x['files']),
        open_depth=sum(r['open_wrapped_depth']for r in x['files'])),indent=2))
if __name__=='__main__':main()
