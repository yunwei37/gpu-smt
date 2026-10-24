"""Qualify our point-evaluator packing on retained real tactic-entry queries."""
from pathlib import Path
import argparse,json,time
import numpy as np
from point_proposals import eval_array
from gpu_points import pack,reference_masks,exact_results,Device,compile_ptx

def direct_masks(batch):
 output=[]
 for item,m in zip(batch['retained'],batch['meta']):
  ast=item['entry']['payload']['ast'];_,_,ds,n,offset,count,_=map(int,m)
  points=batch['points'][offset:offset+count*n].reshape(count,n)
  mask=np.all(np.isfinite(points),axis=1)
  with np.errstate(all='ignore'):
   for j,d in enumerate(batch['domains'][ds:ds+n]):
    if d:mask&=points[:,j]==np.floor(points[:,j])
    if d==2:mask&=points[:,j]>=0
   for h in ast['hypotheses']:mask&=eval_array(h,points)
   mask&=np.logical_not(eval_array(ast['goal'],points))
  output.append(np.asarray(mask,dtype=np.uint8))
 return np.concatenate(output)

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 p.add_argument('--backend',choices=['cpu','device'],default='cpu')
 p.add_argument('--ptx',type=Path);p.add_argument('--nvrtc',type=Path)
 args=p.parse_args();args.out.mkdir(exist_ok=False)
 entries=[json.loads(line)for line in args.input.read_text().splitlines()if line.strip()]
 start=time.perf_counter();batch=pack(entries);packed=time.perf_counter()
 reference=direct_masks(batch);nested=time.perf_counter()
 lifecycle={};device=None
 if args.backend=='device':
  if not args.ptx:raise ValueError('device qualification requires a PTX output path')
  if args.nvrtc:
   began=time.perf_counter();compile_ptx(args.ptx,str(args.nvrtc));lifecycle['compile_seconds']=time.perf_counter()-began
  began=time.perf_counter()
  with Device(args.ptx)as gpu:
   device=gpu.name;lifecycle['context_and_load_seconds']=time.perf_counter()-began
   timing=gpu.evaluate(batch);observed=batch['hits'].copy()
   began=time.perf_counter()
  lifecycle.update(timing,context_destroy_seconds=time.perf_counter()-began)
 else:observed=reference_masks(batch)
 evaluated=time.perf_counter();observed_exact=exact_results(batch,observed)
 exact_done=time.perf_counter();reference_exact=exact_results(batch,reference)
 by_entry=[dict(source_id=a['source_id'],entry_ns=a['entry_ns'],
  same_exact_witness_presence=a['exact_counterexample']==b['exact_counterexample'],
  reference_exact_counterexample=b['exact_counterexample'],**a)
  for a,b in zip(observed_exact,reference_exact)]
 masks=(observed!=reference).reshape(len(entries),batch['count'])
 summary=dict(backend=args.backend,device=device,entries=len(entries),points_per_entry=batch['count'],
  sources=len({x['source_id']for x in entries}),
  maximum_stack_depth=max(x['stack_depth']for x in batch['retained']),
  maximum_instructions=max(int(m[1]-m[0])for m in batch['meta']),
  proposal_mask_differences=int(np.count_nonzero(masks)),
  entries_with_proposal_mask_differences=int(np.count_nonzero(np.any(masks,axis=1))),
  exact_witness_entries=sum(x['exact_counterexample']for x in by_entry),
  exact_witness_presence_differences=sum(not x['same_exact_witness_presence']for x in by_entry),
  packing_seconds=packed-start,nested_reference_seconds=nested-packed,
  exact_check_seconds=exact_done-evaluated,lifecycle=lifecycle,
  whole_qualification_seconds=time.perf_counter()-start,
  scope='Retained actual-goal functional qualification. Offline batching is not online candidate concurrency or end-to-end speed. CPU backend is not GPU execution. Root self-review.')
 (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (args.out/'entries.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n'for x in by_entry))
 print(json.dumps(summary,indent=2))
 assert summary['exact_witness_presence_differences']==0
if __name__=='__main__':main()
