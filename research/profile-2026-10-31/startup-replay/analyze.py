#!/usr/bin/env python3
"""Reduce retained native records to small, explicitly scoped CSVs."""
import csv,json,statistics,sys
from pathlib import Path
raw=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
rows=[json.loads(x) for x in (raw/'results.jsonl').read_text().splitlines()]
def write(name,data):
    if not data:return
    keys=list(data[0])
    with (out/name).open('w',newline='')as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(data)
def flatten(r):
    z={k:r.get(k,'') for k in ['key','mode','module','rep','returncode','stop','wall_s','user_s','system_s','peak_rss_kib','minor_faults','major_faults','voluntary_switches','involuntary_switches','historical_build_s']}
    for k,v in r['sampled_tree_peaks_kib'].items():z['sampled_'+k.lower()+'_peak_kib']=v
    samples=json.loads((raw/(r['key']+'.smaps.json')).read_text())
    peak=max(samples,key=lambda s:s.get('Rss',0),default={})
    for k in ['Pss_File','Pss_Anon','Rss','Pss','Shared_Clean','Shared_Dirty','Private_Clean','Private_Dirty']:
        z['at_sampled_rss_peak_'+k.lower()+'_kib']=peak.get(k,0)
    return z
write('measurements.csv',[flatten(r) for r in rows if r['mode']!='preflight'])
groups={}
for r in rows:
    if r['mode'] in ['build','imports'] and r['returncode']==0 and not r['stop']:
        groups.setdefault(r['module'],{}).setdefault(r['mode'],[]).append(r)
paired=[]
for module,d in groups.items():
    if not all(m in d for m in ['build','imports']):continue
    med=lambda mode,k:statistics.median(r[k] for r in d[mode])
    b=med('build','wall_s');imp=med('imports','wall_s')
    paired.append(dict(module=module,build_n=len(d['build']),import_n=len(d['imports']),build_median_s=b,import_median_s=imp,import_over_build=imp/b,build_minus_import_s=b-imp,
      import_user_median_s=med('imports','user_s'),import_system_median_s=med('imports','system_s'),import_peak_rss_median_kib=med('imports','peak_rss_kib'),
      replay_cli_s=next((r['wall_s']for r in rows if r['mode']=='replay'and r['module']==module and r['returncode']==0),''),
      extrapolated_163000_import_serial_hours=imp*163000/3600))
write('startup-paired.csv',paired)
replays=[]
for r in rows:
    if r['mode']!='replay':continue
    b=next((p['build_median_s'] for p in paired if p['module']==r['module']),None)
    replays.append(dict(module=r['module'],returncode=r['returncode'],stop=r['stop'],replay_total_wall_s=r['wall_s'],replay_user_s=r['user_s'],replay_system_s=r['system_s'],replay_peak_rss_kib=r['peak_rss_kib'],
      historical_build_s=r['historical_build_s'],ratio_to_historical_build=r['wall_s']/r['historical_build_s'] if r['returncode']==0 else '',
      current_build_median_s=b if b is not None else '',ratio_to_current_build=r['wall_s']/b if b and r['returncode']==0 else '',
      scope='target-module CLI; imported declarations trusted; unsafe/partial skipped'))
write('kernel-replay.csv',replays)
summary={'rows':len(rows),'by_mode':{m:{'n':sum(r['mode']==m for r in rows),'success':sum(r['mode']==m and r['returncode']==0 for r in rows)}for m in sorted(set(r['mode']for r in rows))}}
if paired:
    times=[r['import_median_s']for r in paired]
    summary['startup']={'modules':len(paired),'min_s':min(times),'median_s':statistics.median(times),'max_s':max(times),
      'median_import_over_build':statistics.median(p['import_over_build']for p in paired),
      'import_wall_sum_over_build_wall_sum':sum(p['import_median_s']for p in paired)/sum(p['build_median_s']for p in paired),
      '163000_extrapolation_hours_min_median_max':[x*163000/3600 for x in [min(times),statistics.median(times),max(times)]]}
(raw/'analysis-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
