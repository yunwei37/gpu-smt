"""Task-held-out lexical success/time model using the completed native capture."""
from pathlib import Path
import argparse,collections,gzip,json,math,runpy,time
import numpy as np
ROOT=Path('/workspaces/repository');HERE=Path(__file__).parent
F=runpy.run_path(str(HERE/'features.py'))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(exist_ok=False)
 with gzip.open(ROOT/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity/minif2f-input.jsonl.gz','rt')as f:source=[json.loads(l)for l in f]
 reference=json.loads((ROOT/'artifacts/candidate-scheduling-2026-10-25/offline-v2/source-features.json').read_text())
 assert len(source)==len(reference)==7808
 x=np.array([F['vector'](s['code'])for s in source],dtype=float)
 y=np.array([r['valid']for r in reference],dtype=float);t=np.log([r['http_seconds']for r in reference])
 groups=np.arange(len(source))//32;folds=groups%5;scores=np.zeros(len(source));models=[]
 for fold in range(5):
  train=folds!=fold;test=~train
  mean=x[train].mean(axis=0);scale=x[train].std(axis=0);scale[scale==0]=1.
  a=np.column_stack([np.ones(train.sum()),(x[train]-mean)/scale]);yt=y[train]
  penalty=np.eye(a.shape[1]);penalty[0,0]=0.
  beta=np.zeros(a.shape[1]);converged=False
  for iteration in range(100):
   z=np.clip(a@beta,-40,40);prob=1/(1+np.exp(-z));gradient=a.T@(prob-yt)+penalty@beta
   hessian=a.T@((prob*(1-prob))[:,None]*a)+penalty
   step=np.linalg.solve(hessian,gradient);beta-=step
   if np.max(np.abs(step))<1e-7:converged=True;break
  gamma=np.linalg.solve(a.T@a+penalty,a.T@t[train])
  b=np.column_stack([np.ones(test.sum()),(x[test]-mean)/scale])
  z=b@beta;logprob=-np.logaddexp(0,-z);scores[test]=logprob-b@gamma
  models.append(dict(fold=fold,means=mean.tolist(),scales=scale.tolist(),logistic_coefficients=beta.tolist(),logtime_coefficients=gamma.tolist(),
   train_sources=int(train.sum()),held_out_sources=int(test.sum()),training_task_ids=sorted(set(groups[train].tolist())),held_out_task_ids=sorted(set(groups[test].tolist())),optimizer_converged=converged,optimizer_iterations=iteration+1))
 assert all(m['optimizer_converged']for m in models)
 predictions=[];ordered=[];curves=collections.Counter()
 for task in range(244):
  ids=list(range(task*32,(task+1)*32));ranked=sorted(ids,key=lambda i:(-scores[i],i));ordered+=ranked
  for k in [1,2,4,8,16,32]:curves[k]+=any(reference[i]['valid']for i in ranked[:k])
  for rank,i in enumerate(ranked):
   runtime=F['score'](source[i]['code'],models[task%5])
   assert abs(runtime-scores[i])<1e-8
   predictions.append(dict(source_id=reference[i]['source_id'],task_id=task,fold=task%5,rank=rank+1,score=runtime))
 model=dict(feature_names=F['NAMES'],fold_assignment='producer_task_index modulo5, all32siblings together',models=models,
  scope='Cross-fitted ordering only. No candidate is rejected by prediction. Every scored task is held out of its own model, but this is retrospective inspected data, not fresh unseen-benchmark validation. DefaultL2penalty1, unpenalizedintercept; no hyperparameter search.')
 (args.out/'models.json').write_text(json.dumps(model,indent=2)+'\n')
 (args.out/'predictions.json').write_text(json.dumps(predictions,indent=2)+'\n')
 base={r['source_id']:r for r in reference};analysis=runpy.run_path(str(HERE/'analyze.py'))
 replay=analysis['simulate'](base,[reference[i]['source_id']for i in ordered],2,True)
 # Match the interleaved model used by the actual one-active-candidate/task policy.
 taskorders=[sorted(range(task*32,(task+1)*32),key=lambda i:(-scores[i],i))for task in range(244)]
 interleaved=[reference[taskorders[task][rank]]['source_id']for rank in range(32)for task in range(244)]
 interleaved_replay=analysis['simulate'](base,interleaved,2,True)
 result=dict(held_out_first_k_solved_task_counts=dict(curves),task_count=244,source_count=7808,solved_tasks=142,
  contiguous_task_replay=replay,interleaved_task_replay=interleaved_replay,scope=model['scope'])
 (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 for name in ['features.py','train-order.py']:(args.out/name).write_bytes((HERE/name).read_bytes())
 print(json.dumps(dict(first_k=dict(curves),model_interleaved_seconds=interleaved_replay['model_makespan_seconds'],model_span_seconds=interleaved_replay['model_consumed_span_seconds'],actual_measurement=False),indent=2))
if __name__=='__main__':main()
