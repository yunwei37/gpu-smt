"""Rebuild small Grid stack summaries from qualified decoded samples."""
from pathlib import Path
import os,json,csv,gzip,statistics
HERE=Path(__file__).resolve().parent
B=Path('/workspaces/.agent-state/gpu-smt-captures/profile-2026-10-31/systime')
OUT=HERE/'grid-interim'
def write(name,rows):
    with (OUT/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    os.sched_setaffinity(0,set(range(8,16)))
    ops=[];origins=[];quality=[];examples={}
    for rep in [1,2,3]:
        meta=json.loads((OUT/f'Grid-baseline-record-r{rep}-decode.json').read_text())
        assert meta['method'].startswith('v2:') and meta['all_native_period_and_sample_totals_equal_independent_flat_report']
        for x in csv.DictReader((OUT/f'Grid-baseline-record-r{rep}-operations.csv').open()):
            ops.append(dict(rep=rep,domain=x['domain'],operation=x['operation'],value=float(x['within_domain_fraction'])))
        orig=meta['accounting_origin_periods'];total=sum(orig.values());resolved=total-orig.get('guard_caller_unresolved',0)
        origins.append(dict(rep=rep,accounting_period=total,resolved_guard_period=resolved,
          resolved_application_origin_fraction=resolved/total,
          kernel_checker_fraction_among_resolved=orig.get('guard_from_kernel_type_checker',0)/resolved if resolved else None,
          interpreter_fraction_among_resolved=orig.get('guard_from_IR_interpreter',0)/resolved if resolved else None,
          unresolved_is_not_zero_cost=True))
        seen={}
        with gzip.open(B/f'grid-interim/Grid-baseline-record-r{rep}-callchains-v2.jsonl.gz','rt') as f:
            for line in f:
                x=json.loads(line)
                if x['domain']!='kernel':continue
                frames=x['frames'];mem=next((i for i,(_,name,_) in enumerate(frames) if 'check_memory' in name),None)
                if mem is None:continue
                after=[name for _,name,_ in frames[mem+1:] if 'lean::check_system' not in name]
                if not after:continue
                kind='kernel_checker' if 'lean::type_checker' in after[0] else 'IR_interpreter' if 'lean::ir::interpreter' in after[0] else 'other'
                if kind not in seen:seen[kind]=dict(period=x['period'],functions=[name for _,name,_ in frames[:min(mem+8,len(frames))]])
                if 'kernel_checker' in seen and 'IR_interpreter' in seen:break
        examples[str(rep)]=seen
        quality.append(dict(rep=rep,native_samples=meta['native_samples'],flat_periods_and_samples_identical=True,
          application_guard_caller_resolved_fraction=resolved/total,frame_limit=48,inline_expansion=False,
          raw_perf_path=str(B/'runs'/f'Grid-baseline-record-r{rep}'/'perf.data')))
    summaries=[]
    for domain,operation in sorted({(x['domain'],x['operation']) for x in ops}):
        vals=[next((r['value'] for r in ops if r['rep']==rep and r['domain']==domain and r['operation']==operation),0.) for rep in [1,2,3]]
        summaries.append(dict(domain=domain,operation=operation,n=3,median=statistics.median(vals),min=min(vals),max=max(vals),
          scope='within-domain sampled cycles, visible-operation priority; not seconds or source-phase fractions'))
    write('operations-per-repeat.csv',ops);write('operations-summary.csv',summaries)
    write('accounting-origin-per-repeat.csv',origins);write('stack-quality.csv',quality)
    (OUT/'guard-origin-examples.json').write_text(json.dumps(examples,indent=2)+'\n')
if __name__=='__main__':main()
