"""Grid interim analysis of completed captures only; all preparation on E cores."""
from pathlib import Path
import os,json,csv,re,collections,statistics,filecmp
os.sched_setaffinity(0,set(range(8,16)))
HERE=Path(__file__).resolve().parent
B=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
OUT=HERE/'grid-interim'
def write(name,rows):
    if not rows:return
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def summarize(rows,keys):
    result=[]
    for key in sorted({tuple(x[k] for k in keys) for x in rows}):
        rr=[x for x in rows if tuple(x[k] for k in keys)==key]
        vals=[x['value'] for x in rr if x['value'] is not None]
        result.append({**dict(zip(keys,key)),'n':len(vals),'median':statistics.median(vals) if vals else None,
          'min':min(vals) if vals else None,'max':max(vals) if vals else None})
    return result
def flat(rep):
    p=B/'grid-interim'/f'record-r{rep}-flat.txt'
    rows=[]
    for line in p.read_text().splitlines():
        c=[s.strip() for s in line.split(';')]
        if len(c)<6 or not c[0].endswith('%'):continue
        try:period=int(c[2]);samples=int(c[1])
        except ValueError:continue
        rows.append(dict(rep=rep,comm=c[3],dso=c[4],symbol=c[5],period=period,samples=samples))
    return rows
def main():
    OUT.mkdir(exist_ok=True)
    native=[];counters=[];facts={};traces=[];quality=[]
    baseline=B/'runs/Grid-baseline-plain-r1'
    for rep in [1,2,3]:
      d=B/'runs'/f'Grid-baseline-stat-r{rep}'
      if not (d/'result.json').exists():continue
      rr=json.loads((d/'result.json').read_text());assert rr['returncode']==0 and rr['retired']
      ev={}
      for line in (d/'perf-stat.csv').read_text().splitlines():
        c=line.split(';')
        if len(c)<5 or line.startswith('#'):continue
        try:value=float(c[0])
        except ValueError:value=None
        event=c[2];ev[event]=value
        counters.append(dict(rep=rep,metric=event,value=value,running_percent=float(c[4]) if c[4] else None,
          scope='process-scoped inherited helper+Lean; hybrid cpu_core PMU scaled counts'))
      for mode in ['u','k']:
        inst=ev[f'cpu_core/instructions/{mode}'];cycles=ev[f'cpu_core/cycles/{mode}']
        counters.append(dict(rep=rep,metric=f'IPC/{mode}',value=inst/cycles,running_percent=None,
          scope='per-repeat ratio of scaled instructions/cycles; no pooling with plain native CPU'))
    write('stat-per-repeat.csv',counters);write('stat-summary.csv',summarize(counters,['metric']))
    for mode in ['plain','stat','record','trace']:
      for rep in [1,2,3]:
        d=B/'runs'/f'Grid-baseline-{mode}-r{rep}'
        if not (d/'result.json').exists():continue
        rr=json.loads((d/'result.json').read_text())
        source=Path(*json.loads((B/'inputs.json').read_text())['modules']['Grid']['module'].split('.')).with_suffix('.olean')
        equal=filecmp.cmp(d/'artifact'/source,baseline/'artifact'/source,shallow=False) if rr['olean_exists'] else False
        diag=filecmp.cmp(d/'native.log',baseline/'native.log',shallow=False)
        assert rr['returncode']==0 and rr['retired'] and equal and diag
        for metric in ['wall_s','user_s','system_s','peak_rss_kib','minor_faults','major_faults','voluntary_switches','involuntary_switches']:
          native.append(dict(mode=mode,rep=rep,metric=metric,value=rr[metric]))
        native.append(dict(mode=mode,rep=rep,metric='system_cpu_share',value=rr['system_s']/(rr['system_s']+rr['user_s'])))
        native.append(dict(mode=mode,rep=rep,metric='effective_cores',value=(rr['system_s']+rr['user_s'])/rr['wall_s']))
        if mode=='trace':
          text=(d/'perf-trace.txt').read_text()
          comm='';tid='';parts=[]
          for line in text.splitlines():
            h=re.match(r'\s*(.*?)\s+\((\d+)\),\s+\d+\s+events',line)
            if h:comm,tid=h.groups()
            hit=re.match(r'\s+(\w+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)',line)
            if hit:
              name,n,err,total,low,avg,high=hit.groups()
              parts.append(dict(comm=comm,tid=tid,syscall=name,calls=int(n),errors=int(err),elapsed_ms=float(total)))
          sums=collections.defaultdict(lambda:dict(calls=0,errors=0,elapsed_ms=0.))
          for row in parts:
            if row['comm']!='lean':continue
            for key in ['calls','errors','elapsed_ms']:sums[row['syscall']][key]+=row[key]
          lost=sum(map(int,re.findall(r'LOST (\d+) events',text)))
          quality.append(dict(rep=rep,lost_events=lost,lean_thread_summaries=len({x['tid'] for x in parts if x['comm']=='lean'}),
            all_thread_summaries=len({(x['comm'],x['tid']) for x in parts}),
            exact_call_counts=False,scope='observed entry/exit summaries; missing/lost/unpaired events not zeros'))
          for name in ['futex','getrusage','mmap','munmap','madvise','brk','read','clone3','statx']:
            a=sums.get(name)
            for metric in ['calls','errors','elapsed_ms']:
              traces.append(dict(rep=rep,syscall=name,metric=metric,value=a[metric] if a else None,
                scope='Lean-comm summaries only; elapsed may overlap across threads and includes sleep/preemption; event loss retained'))
    write('native-per-repeat.csv',native);ns=summarize(native,['mode','metric']);write('native-summary.csv',ns)
    write('syscalls-per-repeat.csv',traces);write('syscalls-summary.csv',summarize(traces,['syscall','metric']))
    write('trace-quality.csv',quality)
    overhead=[]
    for metric in ['wall_s','user_s','system_s']:
      plain=next(x for x in ns if x['mode']=='plain' and x['metric']==metric)
      for mode in ['stat','record','trace']:
        s=next((x for x in ns if x['mode']==mode and x['metric']==metric),None)
        if s:overhead.append(dict(mode=mode,metric=metric,plain_n=plain['n'],profile_n=s['n'],
          ratio_of_medians=s['median']/plain['median'],scope='descriptive ordered-triplet comparison; no randomized paired CI'))
    write('overhead.csv',overhead)
    hot=[];flat_facts=[];all_flat=[]
    for rep in [1,2,3]:
      p=B/'grid-interim'/f'record-r{rep}-flat.txt'
      if not p.exists() or not (B/'runs'/f'Grid-baseline-record-r{rep}'/'result.json').exists():continue
      allrows=flat(rep);rr=[x for x in allrows if x['comm']=='lean'];all_flat.extend(rr);tp=sum(x['period'] for x in rr)
      for domain in ['kernel','user']:
        dd=[x for x in rr if x['symbol'].startswith('[k]')==(domain=='kernel')]
        total=sum(x['period'] for x in dd)
        top=sorted(dd,key=lambda x:-x['period'])[:20]
        hot.extend({**x,'domain':domain,'within_domain_fraction':x['period']/total,'of_native_fraction':x['period']/tp} for x in top)
        rusage=sum(x['period'] for x in dd if any(n in x['symbol'] for n in ['getrusage','task_cputime','thread_group_cputime']))
        flat_facts.append(dict(rep=rep,domain=domain,total_period=total,of_native_fraction=total/tp,
          rusage_three_leaf_fraction=rusage/total if total else None,scope='flat native leaf symbols; caller proof handled separately'))
    write('top20-per-repeat.csv',hot);write('sampled-domain-periods.csv',flat_facts)
    aggregate=[]
    reps=sorted({x['rep'] for x in all_flat})
    for domain in ['user','kernel']:
      native=[x for x in all_flat if x['symbol'].startswith('[k]')==(domain=='kernel')]
      den={rep:sum(x['period'] for x in native if x['rep']==rep) for rep in reps}
      candidates=[]
      for symbol,dso in {(x['symbol'],x['dso']) for x in native}:
        vals=[sum(x['period'] for x in native if x['rep']==rep and x['symbol']==symbol and x['dso']==dso)/den[rep] for rep in reps]
        candidates.append(dict(domain=domain,symbol=symbol,dso=dso,n=len(reps),median=statistics.median(vals),min=min(vals),max=max(vals)))
      aggregate.extend(dict(rank=rank,**row) for rank,row in enumerate(sorted(candidates,key=lambda x:-x['median'])[:20],1))
    write('top20-summary.csv',aggregate)
    facts={'stat_repeats':len({x['rep'] for x in counters}),'trace_repeats':len(quality),
      'record_flat_repeats':len(flat_facts)//2,'all_completed_native_acceptance_and_exact_diagnostics_olean_equal':True,
      'raw_root':str(B),'scope':'completed captures only; trace losses prevent exact syscall census; native plain and instrumentation kept separate'}
    (OUT/'scope.json').write_text(json.dumps(facts,indent=2)+'\n')
    print(json.dumps(facts,indent=2))
if __name__=='__main__':main()
