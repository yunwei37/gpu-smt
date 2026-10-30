#!/usr/bin/env python3
"""Cross-tabulate native JSON verdict flags and actual process exits in retained direct receipts."""
import argparse,collections,csv,gzip,json,pathlib
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cells',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
    with gzip.open(a.cells,'rt')as f:allrows=json.load(f)
    out=[]
    for repeat in range(3):
        rows=[x for x in allrows if x['condition']=='direct'and x['repetition']==repeat]
        assert len(rows)==3566 and len({x['candidate']for x in rows})==3566
        total=sum(x['external_wall_s']for x in rows);by=collections.defaultdict(lambda:[0,0.])
        for x in rows:
            v=x.get('native_json',{}).get('verification-results')or{}
            key=(x['returncode'],str(v.get('success','missing')),str(v.get('encountered-vir-error','missing')))
            by[key][0]+=1;by[key][1]+=x['external_wall_s']
        for (rc,success,vir),(count,seconds)in sorted(by.items()):
            out.append({'repetition':repeat,'returncode':rc,'native_json_success':success,'native_json_encountered_vir_error':vir,'candidates':count,'process_wall_s':seconds,'share_of_repetition_process_wall':seconds/total,'denominator_process_wall_s':total,'accepted_interpretation':'do not infer whole acceptance from partial JSON alone'})
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('w',newline='')as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
