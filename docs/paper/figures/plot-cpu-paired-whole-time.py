from pathlib import Path
import collections
import json
import zipfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

F = Path(__file__).resolve().parent
R = F.parents[2]
D = R / "artifacts/lean-modern-native-compilation-2026-10-14"

def command(base, label):
    folder = base / label
    if folder.is_dir():
        return json.loads((folder / "command.json").read_text())
    with zipfile.ZipFile(base / (label + ".zip")) as z:
        return json.loads(z.read(label + "/command.json"))

specs = [
    ("Product reuse\n(vs Fast/hybrid)", "product-application-complete-cells-analysis.json",
     "product-application-full1", "fast", "fast-products", "#0072B2"),
    ("Native exact oracle\n(vs compiled Mathlib)", "native-oracle-complete-cells-analysis.json",
     "native-oracle-full1", "aot", "native", "#D55E00"),
]
series = []
for label, filename, rawdir, reference, candidate, color in specs:
    data = json.loads((D / filename).read_text())
    assert data["all_planned_complete"]
    assert len(data["primary_pairs"]) == 3
    observations = []
    for pair in sorted(data["primary_pairs"], key=lambda x: x["rep"]):
        rep = pair["rep"]
        a = f"goedel427-rep{rep}-{reference}"
        b = f"goedel427-rep{rep}-{candidate}"
        ca, cb = command(D / rawdir, a), command(D / rawdir, b)
        assert ca["affinity"] == cb["affinity"]
        for name in (a, b):
            cell = data["cells"][name]
            assert cell["valid_complete"] and cell["returned"] == cell["expected"] == 29750
        observations.append({
            "rep": rep, "reference_label": a, "candidate_label": b,
            "reference_seconds": pair["reference_seconds"],
            "candidate_seconds": pair["candidate_seconds"],
            "normalized_whole_time": pair["candidate_seconds"] / pair["reference_seconds"],
            "affinity": ca["affinity"],
        })
    series.append({"label": label, "source": str((D / filename).relative_to(R)),
                   "color": color, "observations": observations})

# Match the current paper's serif/colorblind-safe result-plot style.
# The 3.375-inch canvas matches the measured 243.0-bp printed column.
plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
    "font.family": "serif", "lines.linewidth": 1.2,
    "pdf.fonttype": 42, "axes.grid": True, "grid.alpha": .22,
})
fig, ax = plt.subplots(figsize=(3.375, 2.30))
markers = ["o", "s", "^"]
offsets = [.13, 0, -.13]
for row, item in enumerate(series):
    center = 1 - row
    for obs, marker, offset in zip(item["observations"], markers, offsets):
        ax.plot(obs["normalized_whole_time"], center + offset, marker=marker,
                color=item["color"], markeredgecolor="#222222",
                markeredgewidth=.4, markersize=4.5, linestyle="none")
ax.axvline(1.0, color="#666666", linestyle="--", linewidth=1.0, zorder=0)
# Scatter positions zoom around parity to show all six paired observations.
# No bar length or hidden zero is used; the caption explains this axis range.
ax.set_xlim(.75, 1.10)
ax.set_xticks([.75, .85, .95, 1.0, 1.10])
ax.set_xticklabels(["0.75", "0.85", "0.95", "1.00", "1.10"])
ax.set_ylim(-.36, 1.40)
ax.set_yticks([1, 0])
ax.set_yticklabels([x["label"] for x in series])
ax.set_xlabel("Whole-time ratio to paired reference")
ax.grid(axis="y", visible=False)
handles = [Line2D([], [], color="#222222", marker=m, linestyle="none",
                  markersize=4.5, label=f"Pair {i+1}")
           for i, m in enumerate(markers)]
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(.34, 1.01),
          ncol=3, frameon=False, handletextpad=.25, columnspacing=.75)
fig.subplots_adjust(left=.405, right=.95, bottom=.25, top=.83)
stem = F / "cpu-paired-whole-time"
fig.savefig(stem.with_suffix(".pdf"))
fig.savefig(stem.with_suffix(".png"), dpi=300)
plt.close(fig)
(stem.with_suffix(".source.json")).write_text(json.dumps({
    "series": series,
    "population_per_condition": 29750,
    "primary_pairs_per_series": 3,
    "excluded": "Two separate resource profiles per experiment; no partial cells or other comparisons.",
    "scope": "Within-pair whole-time ratios only. The two rows have different references and CPU eligibility and cannot rank methods across rows. All failures remain charged. Six observations show between-pair variation, not confidence intervals or isolated causal effects.",
}, indent=2) + "\n")
print(json.dumps({"pdf": str(stem.with_suffix(".pdf")),
                  "series": [[o["normalized_whole_time"] for o in x["observations"]]
                             for x in series]}))
