from pathlib import Path
import argparse,importlib.util,json
R=Path('/workspaces/repository')
D=R/'bench/lean-native/linarith-oracle'
def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=load_module('batch_analysis',D/'analyze-batch.py')
def summarize(path,method,inputs):
 c=m.cell(path,method,inputs);t=c['terminal']
 events=[]
 for x in c['byidx'].values():events.extend([(x['start_ns'],1),(x['end_ns'],-1)])
 active=peak=0
 for _,delta in sorted(events):active+=delta;peak=max(peak,active)
 assert active==0
 return c,{'whole_seconds':t['whole_ns']/1e9,'counts':t['counts'],
 'peak_active_candidates':peak,'missing_spans':c['missing_candidate_spans'],
 'unmatched_spans':c['unmatched_candidate_spans'],'terminal':t}
def compare(ref,c,inputs):
 verdict=[];messages=[];other=[]
 for i,(x,y)in enumerate(zip(ref['responses'],c['responses'])):
  assert x['proof_id']==y['proof_id']==inputs[i]['proof_id']
  if x['outcome']!=y['outcome']:verdict.append(i)
  if x['response']!=y['response']:
   messages.append(i)
   strip=lambda z:{k:v for k,v in z.items()if k!='messages'}if isinstance(z,dict)else z
   if strip(x['response'])!=strip(y['response']):other.append(i)
 return {'outcome_differences':verdict,'JSON_differences':messages,'non_message_differences':other}
def main():
 p=argparse.ArgumentParser();p.add_argument('--static',type=Path,required=True);p.add_argument('--dynamic',type=Path,required=True);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 inputs=m.rows(a.input);ref,rs=summarize(a.static,'fast-hybrid',inputs);dyn,ds=summarize(a.dynamic,'fast-hybrid',inputs)
 out={'scope':'Matched native static versus dynamic scheduler, same private binary/source body, original input order and width8. Root self-review. Short preflight is not a paper performance result.',
 'count':len(inputs),'static':rs,'dynamic':ds,'native_static_over_dynamic':rs['whole_seconds']/ds['whole_seconds'],
 'fidelity':compare(ref,dyn,inputs)}
 out['functional_pass']=all(not out['fidelity'][k]for k in ['outcome_differences','non_message_differences'])and all(not x['missing_spans']and not x['unmatched_spans']and x['peak_active_candidates']<=8 for x in [rs,ds])
 out['preflight_benefit']=out['native_static_over_dynamic']>1
 a.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
