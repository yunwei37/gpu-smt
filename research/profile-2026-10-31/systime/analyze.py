"""Small native/perf result tables; no raw perf payloads are copied into Git."""
from pathlib import Path
import json,csv,statistics,filecmp,argparse,subprocess,re,collections
BASE=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
HERE=Path(__file__).resolve().parent
def write(path,rows):
    if not rows:return
    keys=list(dict.fromkeys(k for x in rows for k in x))
    with path.open('w') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def counters(folder):
    result=[];p=folder/'perf-stat.csv'
    if not p.exists():return result
    for line in p.read_text().splitlines():
        if not line or line.startswith('#'):continue
        cells=line.split(';')
        if len(cells)<5:continue
        try:value=float(cells[0].replace(',',''))
        except ValueError:value=None
        result.append(dict(event=cells[2],value=value,running_percent=cells[4],
          raw_folder=str(folder),available=value is not None))
    return result
def main():
    rows=[];events=[]
    inp=json.loads((BASE/'inputs.json').read_text())
    for folder in sorted((BASE/'runs').glob('*')):
        f=folder/'result.json'
        if not f.exists():continue
        x=json.loads(f.read_text());log=(folder/'native.log').read_text(errors='replace')
        x={k:v for k,v in x.items() if not isinstance(v,(list,dict))}
        x['sorry_warning']="declaration uses 'sorry'" in log
        x['native_error']=bool(re.search(r'\berror:',log)) or 'INTERNAL PANIC' in log
        x['accepted']=x.get('returncode')==0 and not x['sorry_warning'] and not x['native_error'] and x['olean_exists']
        x['system_cpu_share']=x['system_s']/(x['system_s']+x['user_s']) if x.get('system_s',0)+x.get('user_s',0)>0 else None
        module=inp['modules'][x['module']]['module']
        ref=BASE/'runs'/f"{x['module']}-baseline-plain-r1"/'artifact'/Path(*module.split('.')).with_suffix('.olean')
        own=folder/'artifact'/Path(*module.split('.')).with_suffix('.olean')
        x['olean_equal_baseline']=filecmp.cmp(own,ref,shallow=False) if own.exists() and ref.exists() else None
        native_ref=BASE/'runs'/f"{x['module']}-baseline-plain-r1"/'native.log'
        x['diagnostic_equal_baseline']=filecmp.cmp(folder/'native.log',native_ref,shallow=False) if native_ref.exists() else None
        rows.append(x)
        events.extend({**q,'module':x['module'],'config':x['config'],'mode':x['mode'],'rep':x['rep']} for q in counters(folder))
    summaries=[]
    for key in sorted({(x['module'],x['config'],x['mode']) for x in rows}):
        rr=[x for x in rows if (x['module'],x['config'],x['mode'])==key]
        s=dict(zip(['module','config','mode'],key));s.update(n=len(rr),accepted=sum(x['accepted'] for x in rr),
          byte_equal=sum(x['olean_equal_baseline'] is True for x in rr),byte_comparisons=sum(x['olean_equal_baseline'] is not None for x in rr))
        for metric in ['wall_s','user_s','system_s','peak_rss_kib','sampled_tree_peak_bytes','voluntary_switches','involuntary_switches','minor_faults','major_faults','system_cpu_share']:
            vals=[x[metric] for x in rr if x.get(metric) is not None]
            if vals:
                for agg,fn in [('median',statistics.median),('min',min),('max',max)]:s[metric+'_'+agg]=fn(vals)
        summaries.append(s)
    write(HERE/'native.csv',rows);write(HERE/'summary.csv',summaries);write(HERE/'counters.csv',events)
    overhead=[]
    for s in summaries:
        ref=next((r for r in summaries if r['module']==s['module'] and r['config']==s['config'] and r['mode']=='plain'),None)
        if s['mode']=='plain' or ref is None:continue
        overhead.append(dict(module=s['module'],config=s['config'],mode=s['mode'],plain_n=ref['n'],profile_n=s['n'],
            qualified_triplets=ref['n']>=3 and s['n']>=3 and ref['accepted']==ref['n'] and s['accepted']==s['n'],
            native_wall_median_ratio=s['wall_s_median']/ref['wall_s_median'],
            scope='separate native process medians; no pooling with unprofiled observations'))
    write(HERE/'profiler-overhead.csv',overhead)
    print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()
