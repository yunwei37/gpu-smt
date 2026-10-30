#!/usr/bin/env python3
"""Retain umbrella stress as deferred; compute executable-pilot closure and default-root scenarios."""
import argparse,csv,json,pathlib,re
from inventory import write_csv
from plan_build import load,closure,simulate
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--inventory',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
    profiles,modules,deps,external,reverse,order,depth=load(a.inventory)
    lake=json.loads((a.inventory/'upstream-metadata.json').read_text())['lean/lakefile.lean']
    root=re.search(r'@\[default_target\]\s*lean_lib\s+([\w.]+)',lake)[1]
    original=list(csv.DictReader((a.out/'sample-targets.csv').open()));phase=[];deferred=[]
    for row in original:
        (deferred if row['module']==root else phase).append(row)
    m=max((m for m in modules if m!=root),key=lambda m:depth[m]);closed=closure([m],deps);x=profiles[modules[m]]
    phase.append({'module':m,'path':modules[m],'project':x['project'],'role':'purposeful_stress','stratum':'longest_non_default_root','inclusion_probability':0,'source_bytes':x['bytes'],'import_depth':depth[m],'decide_kernel_occurrences':x['decide_plus_kernel'],'closure_modules':len(closed),'closure_source_bytes':sum(profiles[modules[q]]['bytes']for q in closed),'external_import_modules':len(set().union(*(external[q]for q in closed))),'native_fit_16GiB':'unknown until pilot'})
    union=closure([x['module']for x in phase],deps);ext=set().union(*(external[m]for m in union))
    write_csv(a.out/'phaseA-targets.csv',phase);write_csv(a.out/'deferred-umbrella.csv',deferred)
    write_csv(a.out/'phaseA-closure.csv.gz',[{'module':m,'path':modules[m],'source_bytes':profiles[modules[m]]['bytes'],'project':profiles[modules[m]]['project']}for m in sorted(union)])
    write_csv(a.out/'phaseA-external-imports.csv',[{'module':m}for m in sorted(ext)])
    rootset=closure([root],deps);rootorder=[m for m in order if m in rootset]
    rootdeps={m:deps[m] for m in rootset};rootrev={m:[x for x in reverse[m]if x in rootset]for m in rootset};models=[]
    for model,fn in [('constant_1s',lambda p:1.),('constant_10s',lambda p:10.),('constant_60s',lambda p:60.),('startup1s_plus_64KiB_per_s',lambda p:1.+p['bytes']/65536.)]:
        weights={m:fn(profiles[modules[m]])for m in rootset};span={}
        for m in rootorder:span[m]=weights[m]+max((span[d]for d in rootdeps[m]),default=0)
        for workers in [8,24]:
            wall,peak=simulate(workers,weights,rootdeps,rootrev,rootorder)
            models.append({'scope':'default_root_source_closure','model':model,'workers':workers,'modules':len(rootset),'cpu_hours':sum(weights.values())/3600,'critical_path_s':max(span.values()),'list_scheduled_wall_hours':wall/3600,'empirically_calibrated':False})
    write_csv(a.out/'default-root-build-time.csv',models)
    info={'default_target':root,'default_target_closure_modules':len(rootset),'default_target_source_bytes':sum(profiles[modules[m]]['bytes']for m in rootset),'phaseA_targets':len(phase),'phaseA_probability_targets':sum(x['role']=='probability_sample'for x in phase),'phaseA_closure_modules':len(union),'phaseA_closure_source_bytes':sum(profiles[modules[m]]['bytes']for m in union),'phaseA_closure_decide_kernel':sum(profiles[modules[m]]['decide_plus_kernel']for m in union),'external_import_modules':len(ext),'deepest_nonroot':phase[-1]['module'],'deepest_nonroot_depth':phase[-1]['import_depth'],'native_RSS_unknown':True,'compiler_environment_ready':False,'execution_contract':'One Lean process at a time in W;16GiB aggregate,8cores,heartbeats,natural exit,under30min.24/8 job schedule is hypothetical full-build projection,not a native W launch.'}
    (a.out/'phaseA-summary.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__':main()
