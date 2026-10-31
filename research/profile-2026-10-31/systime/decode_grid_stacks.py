"""Streaming on-CPU period attribution; raw perf.data remains the primary artifact."""
from pathlib import Path
import os,subprocess,re,csv,collections,json,argparse,gzip
B=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
HERE=Path(__file__).resolve().parent
def classify(frames,domain):
    names=[f[1].lower() for f in frames]
    s='\n'.join(names)
    if domain=='kernel':
        k='\n'.join(name for (ip,name,dso) in frames if 'kernel' in dso or ip>=0xffff800000000000).lower()
        if any(x in k for x in ['getrusage','task_cputime','thread_group_cputime']):return 'resource_accounting'
        if any(x in k for x in ['do_user_addr_fault','handle_mm_fault','do_anonymous_page','filemap_fault','filemap_map_pages']):return 'page_fault'
        if any(x in k for x in ['__x64_sys_mmap','__x64_sys_munmap','do_mmap','do_munmap','madvise']):return 'mapping_advice'
        if 'futex' in k:return 'futex_synchronization'
        if any(x in k for x in ['perf_event','x86_pmu','intel_pmu','native_write_msr']):return 'PMU_observer_path'
        if any(x in k for x in ['__schedule','finish_task_switch','pick_next_task','enqueue_task','dequeue_task','select_idle','update_rq','try_to_wake','ttwu','psi_group_change']):return 'scheduler_wakeup'
        return 'kernel_other'
    # Visible user operation, not an additive high-level phase allocation.
    if 'check_memory' in s:return 'native_memory_check'
    if any(x in s for x in ['mi_malloc','mi_heap_malloc','mi_free','_mi_','malloc','calloc','realloc','_int_free','operator new','operator delete','lean_alloc','lean_free']):return 'allocation_release'
    if any(x in s for x in ['lean_dec','lean_inc_ref','lean::inc(','lean::dec(']):return 'reference_count'
    if any(x in s for x in ['__hash_table','__hash_iterator']):return 'hash_table'
    if any(x in s for x in ['lean::type_checker','lean::kernel','l_lean_kernel']):return 'kernel_type_check_other'
    if names and 'lean::ir::interpreter' in names[0]:return 'IR_interpreter_leaf'
    # A generic task_manager::worker ancestor cannot label arbitrary import/computation as waiting.
    if any(x in s for x in ['task_manager::wait_for','task_manager::enqueue','task_manager::resolve','task_manager::add_dep','lean_task_get','lean_task_spawn','lean_task_bind','lean_task_map']):
        if any(x in s for x in ['pthread_cond','pthread_mutex','futex','condition_variable','task_manager::wait_for']):return 'task_pool_synchronization'
    if any(x in s for x in ['l_lean_elab_tactic','l_mathlib_tactic','l_lean_meta_simp','l_lean_meta_tactic']):return 'tactic_other'
    if any(x in s for x in ['l_lean_finalizeimport','l_lean_importmodules']):return 'import_other'
    if 'lean::ir::interpreter' in s:return 'interpreted_other'
    return 'unclassified'

def main(folder):
    os.sched_setaffinity(0,set(range(8,16)))
    folder=Path(folder);tag=folder.name;out=HERE/'grid-interim';out.mkdir(exist_ok=True)
    assert (folder/'result.json').exists(),'never decode a live record'
    cmd=['perf','script','--no-inline','--ns','--max-stack','48','-i',str(folder/'perf.data'),'-F','comm,pid,tid,time,event,period,ip,sym,dso']
    raw=B/'grid-interim';raw.mkdir(exist_ok=True)
    categories=collections.Counter();totals=collections.Counter();hot=collections.Counter()
    samples=0;ignored=0;unparsed=[];examples={};maxdepth=collections.Counter();helperperiod=0;origins=collections.Counter();kernel_user_caller=0
    cache=gzip.open(raw/(tag+'-callchains-v2.jsonl.gz'),'xt')
    def block(lines):
        nonlocal samples,ignored,helperperiod,kernel_user_caller
        if not lines:return
        header=lines[0]
        match=re.search(r'\s(\d+)\s+(?:cpu_core/)?cycles[^:]*:',header)
        if not match:
            unparsed.append(header[:300]);return
        period=int(match[1])
        if not header.lstrip().startswith('lean '):
            ignored+=1;helperperiod+=period;return
        frames=[]
        for line in lines[1:]:
            if ' (' not in line or not line.endswith(')'):continue
            left,dso=line.rsplit(' (',1)
            pair=left.split(None,1)
            if len(pair)!=2 or not re.fullmatch('[0-9a-fA-F]+',pair[0]):continue
            frames.append((int(pair[0],16),pair[1],dso[:-1]))
        if not frames:
            unparsed.append(header[:300]);return
        leaf=frames[0];domain='kernel' if ('kernel' in leaf[2] or leaf[0]>=0xffff800000000000) else 'user'
        operation=classify(frames,domain)
        cache.write(json.dumps({'header':header,'period':period,'domain':domain,'frames':frames})+'\n')
        if domain=='kernel' and any(ip<0xffff800000000000 for ip,_,_ in frames):kernel_user_caller+=period
        if domain=='kernel' and operation=='resource_accounting':
            idx=next((i for i,(_,name,_) in enumerate(frames) if 'check_memory' in name),None)
            origin='guard_caller_unresolved'
            if idx is not None:
                after=[name for _,name,_ in frames[idx+1:] if 'lean::check_system' not in name]
                if after and 'lean::ir::interpreter' in after[0]:origin='guard_from_IR_interpreter'
                elif after and 'lean::type_checker' in after[0]:origin='guard_from_kernel_type_checker'
                else:origin='guard_from_native_other'
            origins[origin]+=period
        samples+=1;totals[domain]+=period;categories[(domain,operation)]+=period
        hot[(domain,leaf[1],leaf[2])]+=period;maxdepth[len(frames)]+=1
        key=domain+'/'+operation
        if key not in examples:examples[key]=[header]+[f'{a:x} {s} ({d})' for a,s,d in frames[:24]]
    with (raw/(tag+'-script.stderr')).open('w') as err:
        p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True)
        lines=[]
        for line in p.stdout:
            line=line.rstrip('\n')
            if line:lines.append(line)
            else:block(lines);lines=[]
        block(lines);code=p.wait()
    cache.close()
    if code:raise RuntimeError(f'perf script failed {code}')
    (raw/(tag+'-decode-examples.json')).write_text(json.dumps(examples,indent=2)+'\n')
    if unparsed:
        (raw/(tag+'-unparsed.json')).write_text(json.dumps(unparsed[:100],indent=2)+'\n')
        raise RuntimeError(f'{len(unparsed)}unparsed sample blocks; keep output unpublished')
    # Independently check all native period/sample totals against perf report flat output.
    flat=B/'grid-interim'/('record-r'+str(json.loads((folder/'result.json').read_text())['rep'])+'-flat.txt')
    expectedperiod=0;expectedsamples=0
    for line in flat.read_text().splitlines():
        c=[x.strip() for x in line.split(';')]
        if len(c)>=6 and c[0].endswith('%') and c[3]=='lean':
            expectedperiod+=int(c[2]);expectedsamples+=int(c[1])
    assert sum(totals.values())==expectedperiod and samples==expectedsamples,(totals,expectedperiod,samples,expectedsamples)
    def write(name,rr):
        with (out/(tag+'-'+name+'.csv')).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
    write('operations',[dict(domain=d,operation=k,period=v,within_domain_fraction=v/totals[d],
        of_native_fraction=v/sum(totals.values())) for (d,k),v in sorted(categories.items())])
    rr=[]
    for domain in ['user','kernel']:
        rr.extend(dict(domain=d,symbol=s,dso=l,period=v,within_domain_fraction=v/totals[d])
            for (d,s,l),v in sorted(((k,v) for k,v in hot.items() if k[0]==domain),key=lambda x:-x[1])[:20])
    write('top20',rr)
    accounting=sum(origins.values())
    write('accounting-origin',[dict(origin=k,period=v,within_accounting_fraction=v/accounting,within_kernel_fraction=v/totals['kernel']) for k,v in origins.items()])
    meta={'native_samples':samples,'ignored_helper_samples':ignored,'helper_period':helperperiod,
      'periods':dict(totals),'kernel_period_with_any_user_caller':kernel_user_caller,'accounting_origin_periods':dict(origins),'sample_stack_depth_counts':dict(maxdepth),'all_native_period_and_sample_totals_equal_independent_flat_report':True,
      'method':'v2: kernel OS-callchain categories; user visible-operation priorities, no generic-worker attribution; non-expanded48-frame callchains',
      'limits':'inlined RC unresolved; dropped/truncated callers retained unclassified; sampling period !=seconds or off-CPU time',
      'argv':cmd}
    (out/(tag+'-decode.json')).write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps({'folder':tag,'samples':samples,'periods':dict(totals),'kernel_period_with_any_user_caller':kernel_user_caller,'accounting_origin_periods':dict(origins),'categories':{str(k):v for k,v in categories.items()}},indent=2),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('capture');main(p.parse_args().capture)
