#!/usr/bin/env python3
"""Plot real native LP count and search-CPU distributions from a closed trace."""
import argparse,collections,csv,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from plot_lean_current_performance import STYLE, BLUE, GREY, ORANGE

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--threshold",type=int,default=11)
    args=parser.parse_args()
    bins=collections.defaultdict(lambda:{"calls":0,"cpu_seconds":0.})
    with (gzip.open(args.input,"rt")if args.input.suffix==".gz"else args.input.open())as stream:
        for line in stream:
            rec=json.loads(line)
            if rec.get("kind")not in ["direct","fallback"]or rec["request"].get("hello"):continue
            shape=next(e for e in rec["events"]if e["stage"]=="shape"and e["kind"]=="fp-scaled")
            row=bins[shape["rows"]];row["calls"]+=1
            row["cpu_seconds"]+=sum(e["cpu_ns"]/1e9 for e in rec["events"]if e["stage"]in ["fp_solve","exact_lp"])
    count=sum(x["calls"]for x in bins.values())
    cpu=sum(x["cpu_seconds"]for x in bins.values())
    if not count or not cpu:raise ValueError("closed LP trace with nonzero search CPU required")
    args.out.mkdir(parents=True,exist_ok=True)
    x=[1.5];yc=[0.];yt=[0.];records=[];nc=0;nt=0.
    for rows,b in sorted(bins.items()):
        nc+=b["calls"];nt+=b["cpu_seconds"]
        x.append(rows);yc.append(100*nc/count);yt.append(100*nt/cpu)
        records.append({"LP_rows":rows,"calls":b["calls"],"LP_search_CPU_seconds":b["cpu_seconds"],
                        "cumulative_call_percent":yc[-1],"cumulative_LP_CPU_percent":yt[-1]})
    with(args.out/"lp-size-cost.csv").open("w",newline="")as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0]),lineterminator="\n");writer.writeheader();writer.writerows(records)
    small_calls=sum(v["calls"]for r,v in bins.items()if r<args.threshold)
    small_cpu=sum(v["cpu_seconds"]for r,v in bins.items()if r<args.threshold)
    summary={"input":str(args.input),"calls":count,"LP_search_CPU_seconds":cpu,
             "threshold_rows":args.threshold,"small_calls":small_calls,"small_LP_CPU_seconds":small_cpu,
             "small_call_fraction":small_calls/count,"small_LP_CPU_fraction":small_cpu/cpu,
             "scope":"One complete original1000-source native diagnostic. CPU means FP+exact numeric LP search, not whole verification wall. CDF shows this capture's observed distribution, not replicated statistical uncertainty."}
    (args.out/"lp-size-cost-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    plt.rcParams.update(STYLE)
    fig,ax=plt.subplots(figsize=(3.375,2.4))
    fig.subplots_adjust(left=.18,right=.98,bottom=.20,top=.80)
    ax.step(x,yc,where="post",color=BLUE,linestyle="-",label="LP calls")
    ax.step(x,yt,where="post",color=ORANGE,linestyle="--",label="LP search CPU")
    ax.axvline(args.threshold,color=GREY,linestyle=":",linewidth=1.1)
    ax.text(args.threshold*1.15,6,"≥ "+str(args.threshold)+" rows",fontsize=8)
    ax.set_xscale("log");ax.set_xlim(1.5,1500);ax.set_ylim(0,102)
    ax.set_xticks([2,10,100,1000],["2","10","100","1,000"]);ax.minorticks_off()
    ax.set_yticks([0,25,50,75,100])
    ax.set_xlabel("LP rows");ax.set_ylabel("Cumulative share (%)")
    ax.grid(axis="y",alpha=.2)
    ax.legend(ncol=2,loc="lower center",bbox_to_anchor=(.5,1.02),frameon=False)
    fig.savefig(args.out/"lp-size-cost.pdf")
    fig.savefig(args.out/"lp-size-cost.png",dpi=300)
    plt.close(fig)
    print(json.dumps(summary))
if __name__=="__main__":main()
