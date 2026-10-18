"""Reuse the six closed captures; source-span overlap and CDF are not CPU utilization."""
from pathlib import Path
import json,gzip,collections,math
A=Path(__file__).resolve().parent
Q=A.parent/"power-export"
def read(p):
 if not p.exists():p=p.with_name(p.name+".gz")
 with(gzip.open(p,"rt")if p.suffix==".gz"else p.open())as f:return[json.loads(x)for x in f if x.strip()]
def dist(xs):
 xs=sorted(xs);n=len(xs)
 return{"n":n,"sum_seconds":sum(xs),**{k:xs[math.ceil(q*n)-1]for k,q in[("p50",.5),("p90",.9),("p99",.99),("max",1)]}}
def analyze(cell):
 term=json.loads((cell/"terminal.json").read_text());assert term["state"]=="complete"and term["attempts"]==1000
 spans=read(cell/"candidate-times.jsonl");assert len(spans)==1000
 events=collections.Counter()
 values=[]
 for x in spans:
  a,b=x["start_ns"],x["end_ns"];assert b>=a
  events[a]+=1;events[b]-=1;values.append((b-a)/1e9)
 active=0;hist=collections.Counter();last=min(events)
 for t,d in sorted(events.items()):
  hist[active]+=(t-last)/1e9;active+=d;last=t
 assert active==0
 envelope=(max(events)-min(events))/1e9
 assert abs(sum(hist.values())-envelope)<1e-6
 assert abs(sum(n*t for n,t in hist.items())-sum(values))<1e-5
 charged=sum(v["user"]+v["system"]for v in term["cpu"].values())
 return{"source_service_seconds":{x["source"]:(x["end_ns"]-x["start_ns"])/1e9 for x in spans},"whole_seconds":term["whole_ns"]/1e9,"span_distribution_seconds":dist(values),"candidate_envelope_seconds":envelope,"wall_seconds_by_active_source_spans":dict(sorted(hist.items())),"single_active_seconds":hist[1],"zero_active_seconds":hist[0],"peak_active_source_spans":max(hist),"charged_self_waited_child_CPU_seconds":charged,"charged_CPU_scope":"collector plus waited children, not exhaustive descendant CPU or scheduler utilization","span_scope":"native source service intervals including waiting; envelope excludes earlier preparation/later retirement. Zero source spans need not mean idle CPU; overlap is not concurrentlyGPU-ready LPs."},values
def main():
 paths=[(1,Q/"full1000-raw/stock-native/rep1-fast-hybrid",Q/"full1000-raw/power/rep1-oracle-highs")]
 for n in[2,3]:paths.append((n,A/f"raw/rep{n}-native-control/rep1-fast-hybrid",A/f"raw/rep{n}-power/rep1-oracle-highs"))
 data={"scope":"secondary reuse of complete actual instrumented captures; not a new experiment, zero-instrumentation speedup, new GPU bound or independent audit","blocks":[]}
 plotted=[]
 for n,native,power in paths:
  a,av=analyze(native);b,bv=analyze(power)
  data["blocks"].append({"block":n,"native":a,"power":b,"whole_ratio":a["whole_seconds"]/b["whole_seconds"],"charged_CPU_ratio":a["charged_self_waited_child_CPU_seconds"]/b["charged_self_waited_child_CPU_seconds"],"source_service_span_sum_ratio":a["span_distribution_seconds"]["sum_seconds"]/b["span_distribution_seconds"]["sum_seconds"]})
  per_source={k:{"native":a["source_service_seconds"][k],"power":b["source_service_seconds"][k]}for k in a["source_service_seconds"]}
  assert len(per_source)==1000 and a["source_service_seconds"].keys()==b["source_service_seconds"].keys()
  data["blocks"][-1]["source_regression_counts"]={"power_slower":sum(x["power"]>x["native"]for x in per_source.values()),"power_faster":sum(x["power"]<x["native"]for x in per_source.values()),"meaning":"service-span observations with waiting and interference; not isolated per-source CPU or confidence"}
  plotted.append((n,av,bv))
 input_rows=read(A.parents[2]/"input-top1000.jsonl")
 header="import Mathlib\nimport Aesop\n"
 source_id={"\n\n"+x["code"][len(header):]:x["proof_id"]for x in input_rows}
 stable=[]
 for source,pid in source_id.items():
  observations=[{"native":x["native"]["source_service_seconds"][source],"power":x["power"]["source_service_seconds"][source]}for x in data["blocks"]]
  if all(x["power"]>x["native"]for x in observations):stable.append({"proof_id":pid,"observations":observations,"summed_service_delta_seconds":sum(x["power"]-x["native"]for x in observations)})
 data["same_source_slower_in_all_three_observations"]=sorted(stable,key=lambda x:-x["summed_service_delta_seconds"])
 for block in data["blocks"]:
  for mode in["native","power"]:del block[mode]["source_service_seconds"]
 (A/"service-span-analysis.json").write_text(json.dumps(data,indent=2)+"\n")
 import matplotlib
 matplotlib.use("Agg")
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,3,figsize=(8.4,2.65),sharex=True,sharey=True)
 for ax,(n,av,bv)in zip(axes,plotted):
  for values,label,color in[(av,"Compiled control","#2464a0"),(bv,"Direct natural powers","#c4671a")]:
   xs=sorted(values);ys=[(i+1)/len(xs)for i in range(len(xs))]
   ax.step(xs,ys,where="post",label=label,color=color,linewidth=1.2)
  ax.set_xscale("log");ax.set_ylim(0,1.01);ax.set_title("Block "+str(n),fontsize=9)
  ax.set_xlabel("Candidate service span (s)",fontsize=8)
  ax.grid(True,which="major",alpha=.2);ax.tick_params(labelsize=7)
 axes[0].set_ylabel("Empirical CDF",fontsize=8)
 axes[0].legend(loc="upper left",fontsize=6.5,frameon=False)
 fig.tight_layout(pad=.8)
 fig.savefig(A/"candidate-service-cdf.pdf",bbox_inches="tight")
 fig.savefig(A/"candidate-service-cdf.png",dpi=180,bbox_inches="tight")
 plt.close(fig)
 print(json.dumps({"blocks":[{"block":x["block"],"whole_ratio":x["whole_ratio"],"charged_CPU_ratio":x["charged_CPU_ratio"],"source_regression_counts":x["source_regression_counts"],"source_span_sum_ratio":x["source_service_span_sum_ratio"],"native_span_quantiles":x["native"]["span_distribution_seconds"],"power_span_quantiles":x["power"]["span_distribution_seconds"],"single_active_native_power":[x["native"]["single_active_seconds"],x["power"]["single_active_seconds"]],"peak_source_spans":[x["native"]["peak_active_source_spans"],x["power"]["peak_active_source_spans"]]}for x in data["blocks"]],"matplotlib":matplotlib.__version__},indent=2))
if __name__=="__main__":main()
