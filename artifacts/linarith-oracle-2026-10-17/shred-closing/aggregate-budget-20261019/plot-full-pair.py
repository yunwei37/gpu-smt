from pathlib import Path
import csv,json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parent
with(O/"full-pair-source-latencies.csv").open()as stream:rows=list(csv.DictReader(stream))
fig,axes=plt.subplots(1,2,figsize=(9,3.3))
ranked=sorted(rows,key=lambda x:-float(x["native_HTTP_seconds"]))[:781]
for ax,subset,title in[(axes[0],rows,"All 7,808 candidates"),(axes[1],ranked,"Same native-ranked slowest 10% (781 IDs)")]:
 for method,label,color in[("native","Native","#2463a0"),("shred","SHRED integration","#d35f2a")]:
  values=sorted(float(x[method+"_HTTP_seconds"])for x in subset)
  ax.step(values,[(i+1)/len(values)for i in range(len(values))],where="post",label=label,color=color,linewidth=1.5)
 ax.set_xscale("log");ax.set_xlabel("Completed HTTP attempt (s, log scale)")
 ax.set_ylabel("Fraction of candidates");ax.set_ylim(0,1.02);ax.set_title(title,fontsize=10)
 ax.grid(True,alpha=.25);ax.legend(fontsize=8,loc="lower right")
fig.suptitle("miniF2F: full-input latency including errors, timeouts and resource failures",fontsize=11)
fig.text(.5,.01,"2 live REPLs x 24 GiB; 48 GiB total RSS budget. One fixed-order shared-host pair.",ha="center",fontsize=8)
fig.tight_layout(rect=[0,.04,1,.92])
fig.savefig(O/"full-pair-http-cdf.pdf",bbox_inches="tight")
fig.savefig(O/"full-pair-http-cdf.png",bbox_inches="tight",dpi=150)
