"""Plot all six completed HTTP-attempt populations; no source exclusion."""
from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = Path(__file__).resolve().parent
data = json.loads((A / "closed-cells/full-http-boundary-analysis.json").read_text())
assert set(data["conditions"]) == {f"rep{r}-{m}" for r in [1,2,3] for m in ["native","power"]}
records = []
plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "legend.fontsize": 7,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
fig, axes = plt.subplots(1, 3, figsize=(10, 2.65), sharey=True)
for rep, axis in zip([1,2,3], axes):
    for method, color, style, label in [
        ("native", "#222222", "--", "Default exact reference"),
        ("power", "#0072B2", "-", "Power")]:
        cell = data["conditions"][f"rep{rep}-{method}"]
        assert cell["source_count"] == cell["recorded_requests"] == cell["completed_HTTP_attempts"] == 438
        assert cell["exactly_one_recorded_request_per_source"] and cell["exactly_one_matching_final_attempt_per_source"]
        assert not cell["unanswered_recorded_requests"] and not cell["non_200_attempts"]
        statuses = {x["proof_id"]: x["status"] for x in cell["per_source"]}
        xs = sorted(x["HTTP_attempt_seconds"] for x in cell["completed_attempts"])
        assert len(xs) == 438 and xs[0] > 0
        axis.step(xs, [(i+1)/len(xs) for i in range(len(xs))],
                  where="post", color=color, linestyle=style, linewidth=1.4, label=label)
        for event in cell["completed_attempts"]:
            records.append({
                "rep": rep, "method": method, "proof_id": event["proof_id"],
                "status": statuses[event["proof_id"]],
                "HTTP_attempt_seconds": event["HTTP_attempt_seconds"],
                "native_body_seconds": event["reported_body_seconds"],
            })
    axis.set_xscale("log")
    axis.set_ylim(0, 1.01)
    axis.set_title(f"Pair {rep}")
    axis.set_xlabel("Completed HTTP attempt (s)")
    axis.grid(alpha=.25, which="major")
axes[0].set_ylabel("Fraction of original sources")
axes[-1].legend(loc="lower right", framealpha=.85)
fig.tight_layout(pad=.6, w_pad=1.2)
fig.savefig(A / "completed-http-cdf.pdf", bbox_inches="tight")
fig.savefig(A / "completed-http-cdf.png", dpi=180, bbox_inches="tight")
plt.close(fig)
assert len(records) == 2628
with (A / "completed-http-times.csv").open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
print("Plotted all2628source observations, including1050Lean-error observations.")
