"""Summarize disjoint arithmetic stage CPU; never divide overlapping wall sums by whole wall."""
from pathlib import Path
import argparse,gzip,json,collections,importlib.util
def rows(path):
    if path.suffix=='.gz':
        with gzip.open(path,'rt') as f:return [json.loads(l) for l in f]
    return [json.loads(l) for l in path.read_text().splitlines()]
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('cell',type=Path);a=p.parse_args()
    t=json.loads((a.cell/'terminal.json').read_text())
    path=next((a.cell/x for x in ['oracle.jsonl','oracle.jsonl.gz','stages.jsonl','stages.jsonl.gz'] if (a.cell/x).exists()),None)
    raw=rows(path);matched=[x for x in raw if x.get('ty')=='strong-arithmetic-stages']
    sums=collections.defaultdict(lambda:[0,0])
    for x in matched:
        for k,v in x['stages'].items():
            for i in [0,1]:sums[k][i]+=v[i]/1e9
    cpu=sum(v['user']+v['system'] for v in t['cpu'].values())
    spec=importlib.util.spec_from_file_location('arithmetic_matrix_analysis',Path(__file__).with_name('analyze-matrix.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    tree=module.sampled_tree_cpu(a.cell,t)
    phases={'preprocess_and_linearize':['preprocess','linearize'],'nonlinear_products':['products'],'lp_caller':['lp'],'certificate':['certificate']}
    out={'receipt':t,'arithmetic_invocations':len(matched),'observed_pipeline_cpu_seconds':cpu,
         'process_tree_cpu':tree,
         'arithmetic_thread_cpu_seconds':sum(x['cpu_ns'] for x in matched)/1e9,'phases':{}}
    for label,keys in phases.items():
        c=sum(sums[k][0] for k in keys);w=sum(sums[k][1] for k in keys)
        out['phases'][label]={'thread_cpu_seconds':c,'fraction_observed_pipeline_cpu':c/cpu,
                              'summed_invocation_wall_seconds':w,
                              'ratio_to_known_cpu_lower_bound':c/tree['known_pipeline_cpu_seconds_lower_bound'] if tree.get('available') else None}
    out['unattributed_pipeline_cpu_seconds']=cpu-sum(v['thread_cpu_seconds'] for v in out['phases'].values())
    out['scope']='Diagnostic build of Fast/hybrid and product reuse; source-associated native verdict comparison required. Thread CPU stage counters exclude external LP-child CPU; pipeline denominator includes observed collector and waited-child CPU, not exhaustive external descendants. Ratios to known CPU lower bounds remain descriptive counter ratios, not exact complete-verification phase fractions. LP round-trip wall includes queue, IPC and external solve but overlaps concurrent source work, so these wall sums are not whole-wall fractions or an end-to-end speedup upper bound. Preprocessing includes numeric parse/type reasoning and restricted native linearization, not a separate ring/defeq/typeclass partition. Failed pre-probe/setup/control and work outside arithmetic remain unattributed.'
    (a.cell/'stage-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='receipt'},indent=2))
if __name__=='__main__':main()
