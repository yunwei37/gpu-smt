"""Plot cohort variation from the closed same-resource original Goedel pairs."""
from pathlib import Path
import collections,csv,gzip,json,math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
F=Path(__file__).resolve().parent
R=F.parents[2]
A=R/"artifacts/linarith-oracle-2026-10-17/kimina-full29750-budgeted-20261019"
reference=json.loads((A/"full-root-recomputation.json").read_text())
selected={x["proof_id"]for x in map(json.loads,(A.parent/"input-top1000.jsonl").open())}
assert len(selected)==1000
paired=collections.defaultdict(list)
with(A/"full-paired-sources.csv").open()as stream:
 for row in csv.DictReader(stream):paired[int(row["pair"])].append(row)
assert set(paired)=={1,2,3}
series=[]
for rep,rows in sorted(paired.items()):
 assert len(rows)==len({x["proof_id"]for x in rows})==29750
 assert selected<={x["proof_id"]for x in rows}
 for method in ["native","power"]:
  terminal=json.loads((A/"full"/f"rep{rep}-{method}"/"terminal.json").read_text())
  assert terminal["state"]=="complete"and terminal["expected"]==terminal["returned"]==29750
  assert not terminal["owned_live_descendants_after_shutdown"]and not terminal["memory_watchdog"]["error"]
  assert terminal["affinity"]==[8,9,10,11]and terminal["source_concurrency"]==2
  assert terminal["maximum_live_native_repls"]==2
  assert terminal["aggregate_memory_budget_bytes"]==48*1024**3
  assert terminal["per_native_repl_address_limit_bytes"]==24*1024**3
 ranked=sorted(rows,key=lambda x:float(x["native_HTTP_envelope_seconds"]),reverse=True)
 groups=[
  ("Selected 1,000",[x for x in rows if x["proof_id"]in selected],"strata","original_selected_1000"),
  ("Other 28,750",[x for x in rows if x["proof_id"]not in selected],"strata","remaining_28750"),
  ("Slowest 1% (298)",ranked[:math.ceil(len(rows)*.01)],"tails","0.01"),
  ("Timeouts (40)",[x for x in rows if x["native_outcome"]=="timeout"],"strata","all_timeout_sources"),
 ]
 for name,items,category,key in groups:
  n=sum(float(x["native_HTTP_envelope_seconds"])for x in items)
  p=sum(float(x["power_HTTP_envelope_seconds"])for x in items)
  known=reference["pairs"][str(rep)][category][key]
  assert len(items)==known["sources"]
  assert math.isclose(n,known["native_overlapping_HTTP_seconds"],rel_tol=1e-12,abs_tol=1e-7)
  assert math.isclose(p,known["power_overlapping_HTTP_seconds"],rel_tol=1e-12,abs_tol=1e-7)
  series.append(dict(pair=rep,cohort=name,sources=len(items),native_envelope_sum_seconds=n,
   CPU_oracle_envelope_sum_seconds=p,CPU_over_native=p/n))
plt.rcParams.update({
 "font.size":8,"axes.labelsize":8,"xtick.labelsize":7.5,"ytick.labelsize":7.5,
 "legend.fontsize":7.5,"font.family":"serif","lines.linewidth":1.2,
 "pdf.fonttype":42,"axes.grid":True,"grid.alpha":.22,
})
fig,ax=plt.subplots(figsize=(3.375,2.70))
labels=[x[0]for x in groups]
markers=["o","s","^"];offsets=[.12,0,-.12]
for item in series:
 center=3-labels.index(item["cohort"]);rep=item["pair"]-1
 ax.plot(item["CPU_over_native"],center+offsets[rep],marker=markers[rep],
  color="#D55E00",markeredgecolor="#222222",markeredgewidth=.4,markersize=4.5,linestyle="none")
ax.axvline(1,color="#666666",linestyle="--",linewidth=1.0,zorder=0)
ax.set_xlim(.45,1.05);ax.set_xticks([.50,.65,.80,.90,1.0])
ax.set_xticklabels(["0.50","0.65","0.80","0.90","1.00"])
ax.set_ylim(-.38,3.40);ax.set_yticks([3,2,1,0]);ax.set_yticklabels(labels)
ax.set_xlabel("CPU / native HTTP-envelope sum")
ax.grid(axis="y",visible=False)
handles=[Line2D([],[],color="#D55E00",marker=m,markeredgecolor="#222222",
 markersize=4.5,linestyle="none",label=f"Pair {i+1}")for i,m in enumerate(markers)]
ax.legend(handles=handles,loc="lower center",bbox_to_anchor=(.10,1.01),
 ncol=3,frameon=False,handletextpad=.25,columnspacing=.65)
fig.subplots_adjust(left=.405,right=.96,bottom=.20,top=.82)
stem=F/"full-goedel-cohort-costs"
fig.savefig(stem.with_suffix(".pdf"))
fig.savefig(stem.with_suffix(".png"),dpi=300)
plt.close(fig)
(stem.with_suffix(".source.json")).write_text(json.dumps(dict(
 input=str((A/"full-paired-sources.csv").relative_to(R)),selected_input=str((A.parent/"input-top1000.jsonl").relative_to(R)),
 checked_against=str((A/"full-root-recomputation.json").relative_to(R)),series=series,
 source_population_per_condition=29750,paired_repetitions=3,
 scope="Same six closed CPU-only cells. Cohorts can overlap. Each native-ranked tail is fixed within its pair before looking up CPU costs. All failures remain. The plotted sum ratio is not whole lifecycle, CPU work, an Amdahl bound or GPU performance.",
 canvas_inches=[3.375,2.70],minimum_text_points=7.5,points_show="Three raw paired observations, not confidence intervals.",
),indent=2)+"\n")
print(json.dumps(dict(pdf=str(stem.with_suffix(".pdf")),ratios=[{k:x[k]for k in ["pair","cohort","sources","CPU_over_native"]}for x in series]),indent=2))
