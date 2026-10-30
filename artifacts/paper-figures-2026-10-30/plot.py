"""Offline paper figure from fixed published data; starts no verifier or GUI."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

root = Path(__file__).resolve().parent
repository = root.parents[1]
review = (repository / "artifacts/engine-resource-profile-2026-10-25/gpu-smt-warm-engine-full7808-20261028T1220Z/result-review.md").read_text(encoding="utf-8-sig")
rss = json.loads((repository / "research/mechanisms-2026-10-30/retained-analysis/observed-memory-thresholds.json").read_text(encoding="utf-8-sig"))

def table_row(label):
    for line in review.splitlines():
        if line.startswith("|"):
            cells = [s.strip() for s in line.strip().strip("|").split("|")]
            if cells[0] == label:
                return [float(s.replace(",", "")) for s in cells[1:]]
    raise ValueError(label)

elapsed = table_row("External launch-to-exit seconds")
assert table_row("Original candidate IDs returned") == [7808, 7808]
assert table_row("Accepted") == [3014, 3014]
assert sum(table_row(name)[0] for name in ["Accepted", "Rejected", "Timeout", "Resource exhausted"]) == 7808
ratio = elapsed[0] / elapsed[1]
reduction = (1 - elapsed[1] / elapsed[0]) * 100
thresholds = [8, 16, 32, 48]
values = {}
for name in ["warm", "engine"]:
    trace = rss["trace_comparison"][name]
    cells = {row["total_budget_GiB"]: row for row in trace["cells"]}
    assert set(cells) == set(thresholds)
    for row in cells.values():
        assert abs(row["held_sample_seconds_above_threshold"] / trace["covered_span_seconds"] - row["fraction_of_observed_span_above"]) < 1e-12
    values[name] = [cells[b]["fraction_of_observed_span_above"] * 100 for b in thresholds]

colors = ["#0072B2", "#D55E00"]
with plt.rc_context({"font.size": 8.5, "axes.spines.top": False,
                     "axes.spines.right": False, "pdf.fonttype": 42,
                     "svg.fonttype": "none"}):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.55))
    ax = axes[0]
    bars = ax.bar([0, 1], elapsed, color=colors, width=0.58, zorder=3)
    ax.set_xticks([0, 1], ["Four-warm\nservice", "Prepared\nengine"])
    ax.set_ylabel("Launch-to-exit batch time (s)")
    ax.set_ylim(0, 31000)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.yaxis.grid(True, color="#dddddd", linewidth=0.65, zorder=0)
    ax.set_title("(a) Complete batch time", fontsize=9, pad=9)
    ax.text(0.5, 0.94, f"{ratio:.5f}×; {reduction:.2f}% less elapsed", transform=ax.transAxes, ha="center", fontsize=8)
    for bar, duration in zip(bars, elapsed):
        ax.annotate(f"{duration:,.2f}", (bar.get_x()+bar.get_width()/2, duration),
                    xytext=(0, 5), textcoords="offset points", ha="center", va="bottom", fontsize=8.0)

    ax = axes[1]
    ax.plot(thresholds, values["warm"], linestyle="none", marker="o", markersize=5.5,
            markerfacecolor="white", markeredgewidth=1.5, color=colors[0], label="Warm trace")
    ax.plot(thresholds, values["engine"], linestyle="none", marker="D", markersize=4.3,
            color=colors[1], label="Engine trace")
    ax.set_yscale("log")
    ax.set_ylim(0.1, 130)
    ax.set_xlim(4, 60)
    ax.set_xticks(thresholds)
    ax.set_yticks([0.1, 1, 10, 100], ["0.1", "1", "10", "100"])
    ax.set_xlabel("Offline RSS threshold (GiB)")
    ax.set_ylabel("Trace above threshold (%, log)")
    ax.set_title("(b) Fixed-trace RSS thresholds", fontsize=8.5, pad=9)
    ax.grid(axis="y", which="major", color="#dddddd", linewidth=0.65)
    ax.legend(loc="lower left", frameon=False, fontsize=8.0)
    for name, color, offset, align in [
        ("warm", colors[0], (-7, -13), "right"),
        ("engine", colors[1], (7, 10), "left")]:
        ax.annotate(f"{values[name][-1]:.3f}%", (48, values[name][-1]),
                    xytext=offset, textcoords="offset points", ha=align,
                    va="center", color=color, fontsize=8.0)
    fig.subplots_adjust(left=0.085, right=0.975, bottom=0.19, top=0.88, wspace=0.42)
    for suffix in ["pdf", "svg", "png"]:
        kwargs = {"dpi": 180} if suffix == "png" else {}
        fig.savefig(root / ("retained-resource-point." + suffix), bbox_inches="tight", **kwargs)
    plt.close(fig)

print(json.dumps({"matplotlib": matplotlib.__version__, "ratio": ratio,
                  "elapsed_reduction_percent": reduction,
                  "inputs": ["fixed public paper/result-review at 5916957", "fixed public RSS summary at e259a49"],
                  "new_native_runs": 0,
                  "outputs": [str(root / ("retained-resource-point." + s)) for s in ["pdf", "svg", "png"]]}, indent=2))