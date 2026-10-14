from pathlib import Path
import json,statistics,math,zipfile,re,collections
d=Path(__file__).parent;run=d/'full1-proofnet'
pairs=[];missing=[]
for rep in range(3):
 names=[f'proofnet-rep{rep}-original-warm',f'proofnet-rep{rep}-closed-cache']
 files=[run/(n+'.analysis.json') for n in names]
 if not all(p.exists() for p in files):
  missing.extend(n for n,p in zip(names,files) if not p.exists());continue
 a,b=[json.loads(p.read_text()) for p in files]
 differences=[k for k in a['basic_rows'] if a['basic_rows'][k]!=b['basic_rows'].get(k)]
 pairs.append({'rep':rep,'original_s':a['whole_seconds'],'cached_s':b['whole_seconds'],
  'wall_reduction_percent':100*(1-b['whole_seconds']/a['whole_seconds']),
  'speedup':a['whole_seconds']/b['whole_seconds'],'basic_differences':differences,
  'valid_complete':a['valid_complete'] and b['valid_complete'] and not differences})
profiles={}
for name in ['original-warm','closed-cache']:
 p=run/f'proofnet-profile-{name}.analysis.json'
 if p.exists():
  j=json.loads(p.read_text());profiles[name]={'whole_s':j['whole_seconds'],'valid':j['valid_complete'],'resources':j['resources'],'outcomes':j['outcomes']}
 else:missing.append('profile-'+name)
report={'pairs':pairs,'profiles':profiles,'missing_cells':missing,'complete_planned_matrix':len(pairs)==3 and len(profiles)==2 and not missing,'scope':'8cells x5952original sources; three rotated complete pairs plus two separate resource profiles','limitations':['whole primaries include normal output persistence/cleanup, archival after clock','three repetitions only, observed variation is not a robust population confidence interval','profile clocks are instrumented, not additional primary replicates','native kernel unchanged; auxiliary proof value hash differences remain visible','version4.9/published corpus only; official current WHNF already caches all eligible modes; no current-release/novelty/OSDI claim']}
if len(pairs)==3:
 report['mean_wall_reduction_percent']=statistics.mean(p['wall_reduction_percent'] for p in pairs)
 report['observed_effect_range_percent']=[min(p['wall_reduction_percent'] for p in pairs),max(p['wall_reduction_percent'] for p in pairs)]
 report['total_wall_reduction_percent']=100*(1-sum(p['cached_s'] for p in pairs)/sum(p['original_s'] for p in pairs))
 logs=[math.log(p['speedup']) for p in pairs];mu=statistics.mean(logs);half=4.30265273*statistics.stdev(logs)/math.sqrt(3)
 report['paired_log_speedup_t_interval_assuming_iid_normal']=[math.exp(mu-half),math.exp(mu+half)]
 report['interval_limit']='illustrative95percent t interval on3log ratios; iid/normal assumptions unverified, not evidence of a stable speedup'
(d/'complete-matrix-analysis.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['profiles','limitations']}))
