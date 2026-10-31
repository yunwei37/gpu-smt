"""perf trace -s aggregate elapsed syscall time; not exclusive kernel CPU."""
from pathlib import Path
import os,re,csv,argparse,collections
HERE=Path(__file__).resolve().parent
def main(raw):
    os.sched_setaffinity(0,set(range(8,24)))
    p=Path(raw);comm='unknown';pid='unknown';rows=[]
    for line in p.read_text(errors='replace').splitlines():
        head=re.match(r'\s*(.*?)\s+\((\d+)\),\s+\d+\s+events',line)
        if head:comm,pid=head.groups()
        hit=re.match(r'\s+(\w+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)',line)
        if hit:
            name,calls,errors,total,low,avg,high=hit.groups()
            rows.append(dict(comm=comm,pid=pid,syscall=name,calls=int(calls),errors=int(errors),elapsed_ms=float(total),
              min_ms=float(low),avg_ms=float(avg),max_ms=float(high)))
    if not rows:raise ValueError('no native syscall summary; retain raw capture and inspect, do not invent zeros')
    out=HERE/'syscalls';out.mkdir(exist_ok=True)
    label=p.parent.name
    for name,items in [('threads',rows),('aggregate',[])]:
        if name=='aggregate':
            totals=collections.defaultdict(lambda:dict(calls=0,errors=0,elapsed_ms=0.))
            for r in rows:
                for field in ['calls','errors','elapsed_ms']:totals[r['syscall']][field]+=r[field]
            items=[dict(syscall=k,**v,scope='elapsed across threads may overlap; not kernelCPU') for k,v in sorted(totals.items(),key=lambda kv:-kv[1]['elapsed_ms'])]
        with (out/(label+'-'+name+'.csv')).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
    print('parsed',len(rows),'summaries from',str(p))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('raw');main(p.parse_args().raw)
