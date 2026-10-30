#!/usr/bin/env python3
"""Conditional DAG cost models and reproducible stratified targets; not measured build times."""
import argparse,collections,csv,gzip,heapq,json,math,pathlib,random,resource,time
from inventory import write_csv
def load(base):
    with gzip.open(base/'content/file-metrics.csv.gz','rt') as f:
        profiles={x['path']:{k:(int(v) if k not in ('path','project') else v) for k,v in x.items()} for x in csv.DictReader(f)}
    roots=json.loads((base/'content/summary.json').read_text())['import_graph']['source_roots']
    def module(p):
        root=max((q for q in roots if p.startswith(q+'/')),key=len)
        return pathlib.PurePosixPath(p).relative_to(root).with_suffix('').as_posix().replace('/','.')
    modules={module(p):p for p in profiles};deps={m:set() for m in modules};external=collections.defaultdict(set)
    with gzip.open(base/'content/imports.csv.gz','rt') as f:
        for x in csv.DictReader(f):
            if x['internal']=='True':deps[x['module']].add(x['imports'])
            else:external[x['module']].add(x['imports'])
    reverse=collections.defaultdict(list);indegree={m:len(ds) for m,ds in deps.items()}
    for m,ds in deps.items():
        for d in ds:reverse[d].append(m)
    ready=sorted(m for m,n in indegree.items() if n==0);heapq.heapify(ready);order=[];depth={}
    while ready:
        m=heapq.heappop(ready);order.append(m);depth[m]=1+max((depth[d] for d in deps[m]),default=0)
        for child in reverse[m]:
            indegree[child]-=1
            if not indegree[child]:heapq.heappush(ready,child)
    assert len(order)==len(modules)==163097
    return profiles,modules,deps,external,reverse,order,depth
def closure(seeds,deps):
    seen=set();todo=list(seeds)
    while todo:
        m=todo.pop()
        if m not in seen:seen.add(m);todo.extend(deps[m]-seen)
    return seen
def simulate(workers,weights,deps,reverse,order):
    downstream={}
    for m in reversed(order):downstream[m]=weights[m]+max((downstream[c] for c in reverse[m]),default=0)
    remaining={m:len(ds) for m,ds in deps.items()}
    ready=[(-downstream[m],m) for m,n in remaining.items() if not n];heapq.heapify(ready)
    running=[];now=0.;peak=0
    while ready or running:
        while ready and len(running)<workers:
            _,m=heapq.heappop(ready);heapq.heappush(running,(now+weights[m],m));peak=max(peak,len(running))
        now=running[0][0];done=[]
        while running and running[0][0]<=now+1e-9:done.append(heapq.heappop(running)[1])
        for m in done:
            for child in reverse[m]:
                remaining[child]-=1
                if not remaining[child]:heapq.heappush(ready,(-downstream[child],child))
    return now,peak
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--inventory',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();profiles,modules,deps,external,reverse,order,depth=load(a.inventory)
    model_rows=[];cp_rows=[]
    models={'constant_1s':lambda p:1.,'constant_10s':lambda p:10.,'constant_60s':lambda p:60.,'startup1s_plus_64KiB_per_s':lambda p:1.+p['bytes']/65536.}
    for model,fn in models.items():
        weights={m:fn(profiles[p]) for m,p in modules.items()};finish={};parent={}
        for m in order:
            best=max(deps[m],key=lambda d:finish[d],default=None)
            finish[m]=weights[m]+(finish[best] if best else 0)
            if best:parent[m]=best
        endpoint=max(order,key=lambda m:finish[m]);critical=finish[endpoint];chain=[];node=endpoint
        while True:
            chain.append(node)
            if node not in parent:break
            node=parent[node]
        chain.reverse()
        for i,m in enumerate(chain):cp_rows.append({'model':model,'position':i+1,'module':m,'path':modules[m],'assumed_cpu_s':weights[m]})
        total=sum(weights.values())
        for workers in [8,24]:
            wall,peak=simulate(workers,weights,deps,reverse,order)
            model_rows.append({'model':model,'workers':workers,'cpu_hours':total/3600,'critical_path_s':critical,'critical_path_modules':len(chain),'work_span_wall_lower_s':max(total/workers,critical),'list_scheduled_wall_s':wall,'list_scheduled_wall_hours':wall/3600,'simulated_peak_workers':peak,'empirically_calibrated':False})
    write_csv(a.out/'conditional-build-time.csv',model_rows);write_csv(a.out/'model-critical-paths.csv',cp_rows)
    groups=collections.defaultdict(list)
    sizes=sorted(p['bytes'] for p in profiles.values());cuts=[sizes[int((len(sizes)-1)*q)] for q in [.5,.9,.99]]
    for m,path in modules.items():
        row=profiles[path];b=row['bytes'];sizebin='0-50' if b<=cuts[0] else '50-90' if b<=cuts[1] else '90-99' if b<=cuts[2] else '99-100'
        depthbin='1-10' if depth[m]<=10 else '11-100' if depth[m]<=100 else '101+'
        groups[(sizebin,depthbin,int(row['decide_plus_kernel']>0))].append(m)
    rng=random.Random(20261030);samples=[];strata=[]
    for key,pop in sorted(groups.items()):
        pop.sort();chosen=rng.sample(pop,min(2,len(pop)))
        strata.append({'size_percentile_bin':key[0],'import_depth_bin':key[1],'has_decide_kernel':key[2],'population_modules':len(pop),'sample_modules':len(chosen),'inclusion_probability':len(chosen)/len(pop)})
        for m in chosen:samples.append((m,'probability_sample',';'.join(map(str,key)),len(chosen)/len(pop)))
    projects=['OAI/Analysis/MutuallyUnbiased','OAI/Combinatorics/Ramsey','OAI/Analysis/PlanarPacking','OAI/MathematicalPhysics/Transonic','OAI/GameTheory/SnakyTwentyOne','OAI/LinearAlgebra/MatrixFields','OAI/Algorithms/SubexponentialSAT','OAI/Combinatorics/Progressions']
    project_rows=[]
    for project in projects:
        pop=[m for m,path in modules.items() if profiles[path]['project']==project]
        ordered=sorted(pop,key=lambda m:(profiles[modules[m]]['bytes'],m));chosen=ordered[len(ordered)//2]
        samples.append((chosen,'purposeful_project_median',project,0));complete=closure(pop,deps)
        project_rows.append({'project':project,'own_modules':len(pop),'own_source_bytes':sum(profiles[modules[m]]['bytes'] for m in pop),'own_decide_kernel':sum(profiles[modules[m]]['decide_plus_kernel'] for m in pop),'closure_modules':len(complete),'closure_source_bytes':sum(profiles[modules[m]]['bytes'] for m in complete),'closure_decide_kernel':sum(profiles[modules[m]]['decide_plus_kernel'] for m in complete),'external_modules':len(set().union(*(external[m] for m in complete))),'max_depth':max(depth[m] for m in pop),'median_target':chosen})
    for m,reason in [(max(modules,key=lambda m:depth[m]),'longest_import_depth'),(max(modules,key=lambda m:profiles[modules[m]]['bytes']),'largest_source'),(max(modules,key=lambda m:profiles[modules[m]]['decide_plus_kernel']),'most_decide_kernel')]:
        samples.append((m,'purposeful_stress',reason,0))
    sample_rows=[];union=set();external_union=set()
    for m,role,stratum,prob in samples:
        closed=closure([m],deps);union.update(closed);ext=set().union(*(external[q] for q in closed));external_union.update(ext);row=profiles[modules[m]]
        sample_rows.append({'module':m,'path':modules[m],'project':row['project'],'role':role,'stratum':stratum,'inclusion_probability':prob,'source_bytes':row['bytes'],'import_depth':depth[m],'decide_kernel_occurrences':row['decide_plus_kernel'],'closure_modules':len(closed),'closure_source_bytes':sum(profiles[modules[q]]['bytes'] for q in closed),'external_import_modules':len(ext),'native_fit_16GiB':'unknown until pilot'})
    write_csv(a.out/'strata.csv',strata);write_csv(a.out/'sample-targets.csv',sample_rows);write_csv(a.out/'project-closures.csv',project_rows)
    write_csv(a.out/'sample-closure-union.csv.gz',[{'module':m,'path':modules[m],'bytes':profiles[modules[m]]['bytes'],'project':profiles[modules[m]]['project']} for m in sorted(union)])
    write_csv(a.out/'external-imports.csv',[{'module':m,'included_in_internal_DAG':False}for m in sorted(external_union)])
    memory=[]
    for workers in [8,24]:
        for rss in [.5,1,2,4,8]:
            memory.append({'requested_workers':workers,'assumed_peak_RSS_per_job_GiB':rss,'assumed_jobs_peak_GiB':workers*rss,'workers_under_16GiB_before_controller':min(workers,math.floor(16/rss)),'model':'constant per-job peak; imports/kernel scratch unknown; excludes controller'})
    write_csv(a.out/'conditional-memory.csv',memory);disk=[]
    for scope,source in [('all_sources',sum(x['bytes']for x in profiles.values())),('sample_internal_closure',sum(profiles[modules[m]]['bytes']for m in union))]:
        for factor in [2,10,40]:
            disk.append({'scope':scope,'source_bytes':source,'assumed_artifact_source_ratio':factor,'source_plus_artifact_GiB':source*(1+factor)/2**30,'external_packages_cache_GiB':'unknown; additional','calibrated':False})
    write_csv(a.out/'conditional-disk.csv',disk)
    summary={'modules':len(modules),'source_bytes':sum(x['bytes']for x in profiles.values()),'unit_critical_path':max(depth.values()),'strata':len(strata),'probability_targets':sum(x['sample_modules']for x in strata),'purposeful_targets':len(samples)-sum(x['sample_modules']for x in strata),'unique_target_modules':len({x[0]for x in samples}),'sample_closure_modules':len(union),'sample_closure_source_bytes':sum(profiles[modules[m]]['bytes']for m in union),'external_import_modules':len(external_union),'size_cuts':cuts,'seed':20261030,'native_runs':0,'elapsed_s':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'limitations':['All time/RSS/artifact expansion assumptions uncalibrated.','External dependency DAG/build/cache costs excluded.','No hard bound on kernel reduction cost from source bytes.','Probability weights apply only to target costs, not closure modules or purposeful stresses.','No sample is certified to fit16GiB before native pilot.']}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
