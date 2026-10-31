"""On-CPU cycle-period attribution. Sleeping syscall durations are separate."""
from pathlib import Path
import os,subprocess,re,csv,collections,json,argparse
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
HERE=Path(__file__).resolve().parent
def category(frames,kernel):
    s='\n'.join(frames).lower()
    # Prefer a visible originating user operation over a generic futex label.
    if any(v in s for v in ['check_memory','get_peak_rss','get_current_rss']):return 'native_memory_check'
    if 'getrusage' in s:return 'unattributed_resource_accounting_syscall'
    if any(v in s for v in ['mi_malloc','mi_heap_malloc','mi_free','_mi_','malloc','calloc','realloc','_int_free','operator new','operator delete','lean_alloc','lean_free']):return 'allocation_release'
    if any(v in s for v in ['lean_inc_ref','lean_dec_ref','lean_inc_heartbeat','lean::inc(','lean::dec(']):
        return 'heartbeat' if 'heartbeat' in s else 'reference_count'
    if any(v in s for v in ['task_manager','lean_task_get','lean_task_spawn','lean_task_bind','lean_task_map']):return 'task_pool'
    if any(v in s for v in ['do_user_addr_fault','handle_mm_fault','do_anonymous_page','filemap_fault']):return 'page_fault'
    if any(v in s for v in ['__x64_sys_mmap','__x64_sys_munmap','do_mmap','do_munmap','madvise']):return 'mapping_advice'
    if any(v in s for v in ['lean::type_checker','lean::kernel','lean::check(','l_lean_kernel']):return 'kernel_type_check'
    if any(v in s for v in ['l_lean_elab_tactic','l_mathlib_tactic','l_lean_meta_simp','l_lean_meta_tactic']):return 'tactic'
    if kernel and any(v in s for v in ['futex','schedule','finish_task_switch']):return 'unattributed_synchronization'
    return 'unclassified'
def main(folder):
    os.sched_setaffinity(0,set(range(8,24)))
    folder=Path(folder);data=folder/'perf.data';script=folder/'perf-script.txt'
    with script.open('x') as f:
        q=subprocess.run(['perf','script','--ns','-i',str(data),'-F','comm,pid,tid,time,event,period,ip,sym,dso'],stdout=f,stderr=subprocess.PIPE,text=True)
    (folder/'perf-script.stderr').write_text(q.stderr)
    q.check_returncode()
    hot=collections.Counter();cats=collections.Counter();totals=collections.Counter();samples=0;unknown_period=0
    # Header emitted by explicit fields has "<event>: <period> <ip> ..." ordering;
    # archive a short excerpt for parser review instead of silently accepting a format mismatch.
    blocks=script.read_text(errors='replace').strip().split('\n\n')
    (folder/'script-format-excerpt.txt').write_text('\n\n'.join(blocks[:2])+'\n')
    for b in blocks:
        lines=b.splitlines()
        if not lines:continue
        header=lines[0]
        match=re.search(r'\s(\d+)\s+(?:cpu_core/)?cycles[^:]*:',header)
        if not match:
            match=re.search(r'cycles[^:]*:\s+(\d+)\s',header)
        if not match:unknown_period+=1;continue
        period=int(match[1]);frames=[]
        for line in lines[1:]:
            f=re.match(r'\s*[0-9a-fA-F]+\s+(.*?)\s+\((.*?)\)\s*$',line)
            if f:frames.append((f[1],f[2]))
        if not frames:unknown_period+=1;continue
        leaf,dso=frames[0]
        kernel='kernel' in dso or dso.startswith('[') and dso not in ['[unknown]','[vdso]']
        domain='kernel' if kernel else 'user'
        hot[(domain,dso,leaf)]+=period;totals[domain]+=period
        cats[(domain,category([f'{a} ({d})' for a,d in frames],kernel))]+=period;samples+=1
    if unknown_period:raise RuntimeError(f'{unknown_period} unparsed sample blocks; inspect archived excerpt before publishing any stack fractions')
    dest=HERE/'stacks';dest.mkdir(exist_ok=True)
    tag=folder.name
    def write(name,fields,rows):
        with (dest/(tag+'-'+name+'.csv')).open('w') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    rows=[]
    for domain in ['kernel','user']:
        rr=sorted(((k,v) for k,v in hot.items() if k[0]==domain),key=lambda x:-x[1])[:20]
        rows.extend(dict(domain=k[0],dso=k[1],symbol=k[2],period=v,within_domain_fraction=v/totals[domain]) for k,v in rr)
    write('top20',['domain','dso','symbol','period','within_domain_fraction'],rows)
    write('categories',['domain','operation','period','within_domain_fraction'],[
      dict(domain=k[0],operation=k[1],period=v,within_domain_fraction=v/totals[k[0]]) for k,v in cats.items()])
    (dest/(tag+'-scope.json')).write_text(json.dumps({'parsed_samples':samples,'cycles_period':dict(totals),
      'counter_scope':'period-weighted on-CPU samples, not sleeping time or exclusive source-level phase accounting',
      'classification':'visible stack substring attribution; missing callers remain unattributed; inline RC may be invisible',
      'raw':str(folder)},indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('capture');main(p.parse_args().capture)
