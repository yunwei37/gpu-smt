from pathlib import Path
import argparse,importlib.util,json
R=Path('/workspaces/repository')
def main():
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--reference',type=Path,required=True);a=p.parse_args()
 spec=importlib.util.spec_from_file_location('batch_analysis',R/'bench/lean-native/linarith-oracle/analyze-batch.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 inputs=m.rows(R/'artifacts/linarith-oracle-2026-10-17/gpu-stage/large-lp-race/candidate-capacity32/input-first64.jsonl')
 ref=m.cell(a.reference,'fast-hybrid',inputs);cpu=m.cell(a.reference,'oracle-highs',inputs);gpu=m.cell(a.root/'qualification64-gpu','oracle-gpu',inputs)
 out={'scope':'Original first64, capacity32, fourCPU8--11,48GiB. Same native sources/checker. Sequential acquisitions, GPU server cold lifecycle separate, not full1000/whole-population threshold evidence. Root self-review.','count':len(inputs),'methods':{}}
 for name,c in [('native',ref),('CPU_oracle',cpu),('GPU_oracle',gpu)]:
  verdict=[];changes=[];other=[]
  for i,(x,y)in enumerate(zip(ref['responses'],c['responses'])):
   assert x['proof_id']==y['proof_id']==inputs[i]['proof_id']
   if x['outcome']!=y['outcome']:verdict.append(i)
   if x['response']!=y['response']:
    changes.append(i)
    strip=lambda z:{k:v for k,v in z.items()if k!='messages'}if isinstance(z,dict)else z
    if strip(x['response'])!=strip(y['response']):other.append(i)
  out['methods'][name]={'whole_seconds':c['terminal']['whole_ns']/1e9,'outcome_differences':verdict,'JSON_differences':changes,'non_message_differences':other,'missing_spans':c['missing_candidate_spans'],'unmatched_spans':c['unmatched_candidate_spans'],'terminal':c['terminal']}
 n=out['methods']['native']['whole_seconds'];c=out['methods']['CPU_oracle']['whole_seconds'];g=out['methods']['GPU_oracle']['whole_seconds']
 out.update(native_over_CPU=n/c,native_over_GPU_warm=n/g,GPU_over_CPU=g/c)
 (a.root/'matched-qualification-analysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
