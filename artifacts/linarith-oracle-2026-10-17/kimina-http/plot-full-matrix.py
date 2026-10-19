"""Plot every original source in the completed strong-native/Power HTTP pairs."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
A=Path(__file__).resolve().parent
data=list(csv.DictReader((A/"full-matrix-source-latencies.csv").open()))
assert len(data)==9000
plt.rcParams.update({"font.size":8,"axes.labelsize":8,"legend.fontsize":7,"pdf.fonttype":42,"ps.fonttype":42})
fig,axes=plt.subplots(1,3,figsize=(10,2.65),sharey=True)
for rep,axis in zip([1,2,3],axes):
    for method,color,style,label in[
        ("native","#222222","--","Compiled hybrid + omega"),
        ("power","#0072B2","-","Direct natural powers")]:
        points=[x for x in data if int(x["rep"])==rep and x["method"]==method]
        assert len(points)==1000 and len({x["proof_id"]for x in points})==1000
        assert sum(x["status"]=="lean_error"for x in points)==8
        xs=sorted(float(x["HTTP_attempt_seconds"])for x in points)
        assert xs[0]>0
        axis.step(xs,[(i+1)/len(xs)for i in range(len(xs))],where="post",
            color=color,linestyle=style,linewidth=1.4,label=label)
    axis.set_xscale("log");axis.set_ylim(0,1.01)
    axis.set_title("Pair "+str(rep)+(" (mixed restart epochs)"if rep==3 else""))
    axis.set_xlabel("Completed HTTP attempt (s)")
    axis.grid(alpha=.25,which="major")
axes[0].set_ylabel("Fraction of original sources")
axes[-1].legend(loc="lower right",framealpha=.85)
fig.tight_layout(pad=.6,w_pad=1.2)
fig.savefig(A/"full-http-cdf.pdf",bbox_inches="tight")
fig.savefig(A/"full-http-cdf.png",dpi=180,bbox_inches="tight")
plt.close(fig)
print("Plotted6000original-source observations, including48Lean-error observations. All9000remain in CSV.")
