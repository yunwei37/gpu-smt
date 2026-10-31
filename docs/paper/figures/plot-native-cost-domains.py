"""Rebuild the two-denominator native-cost figure from retained evidence.

Run from any directory:
  python3 docs/paper/figures/plot-native-cost-domains.py
Then compile native-cost-domains.tex with Tectonic (or pdflatex).
This is an offline rendering step: it starts no verifier or measurement.
"""
from pathlib import Path
import collections
import csv
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EVIDENCE = ROOT / "docs/tmp/build-and-evaluate/step-0217-20261031T061359+0000/experiment-001"

def read(name):
    with (EVIDENCE / name).open() as source:
        return list(csv.DictReader(source))

families = collections.defaultdict(dict)
for row in read("W4f89614-caller-families.csv"):
    families[row["module"]][row["nearest_recognized_caller"]] = int(row["period"])
baseline = {
    row["module"]: row
    for row in read("W4f89614-native-system-costs.csv")
    if row["mode"] == "baseline_before"
}
names = list(families)
assert len(names) == 5 and set(names) == set(baseline)
columns = {key: [] for key in ["user", "system", "checker", "meta", "import", "other", "unresolved"]}
data = []
for index, name in enumerate(names):
    values = families[name]
    total = sum(values.values())
    checker = values.get("cpp_type_checker_routines", 0)
    meta = values.get("lean_meta", 0)
    imports = values.get("module_import", 0)
    unresolved = values.get("unresolved_or_other", 0) + values.get("runtime_leaf_without_phase_anchor", 0)
    other = total - checker - meta - imports - unresolved
    assert other >= 0
    row = baseline[name]
    user = float(row["native_user_cpu_s"])
    system = float(row["native_system_cpu_s"])
    plotted = {
        "user": user / (user + system) * 100,
        "system": system / (user + system) * 100,
        "checker": checker / total * 100,
        "meta": meta / total * 100,
        "import": imports / total * 100,
        "other": other / total * 100,
        "unresolved": unresolved / total * 100,
    }
    assert abs(plotted["user"] + plotted["system"] - 100) < 1e-9
    assert abs(sum(plotted[key] for key in ["checker", "meta", "import", "other", "unresolved"]) - 100) < 1e-9
    for key, value in plotted.items():
        columns[key].append((value, index))
    data.append({"module": name, **plotted})
def points(key):
    return " ".join(f"({value:.9f},{index})" for value, index in columns[key])
def plot(key, style):
    return "\\addplot+[" + style + "] coordinates {" + points(key) + "};\n"
tex = r"""\documentclass[tikz,border=3pt]{standalone}
\usepackage{pgfplots}
\usepgfplotslibrary{groupplots}
\pgfplotsset{compat=1.18}
\definecolor{cpuuser}{RGB}{127,144,163}
\definecolor{cpusystem}{RGB}{213,94,0}
\definecolor{checker}{RGB}{0,114,178}
\definecolor{metacolor}{RGB}{230,159,0}
\definecolor{importcolor}{RGB}{86,180,233}
\definecolor{othercolor}{RGB}{0,158,115}
\definecolor{unresolvedcolor}{RGB}{190,190,190}
\begin{document}
\begin{tikzpicture}
\begin{groupplot}[
group style={group size=2 by 1,horizontal sep=0.65cm},
width=7.0cm,height=5.3cm,
xbar stacked,/pgf/bar width=10pt,xmin=0,xmax=100,
ymin=-0.6,ymax=4.6,y dir=reverse,
ytick={0,1,2,3,4},
xtick={0,25,50,75,100},
tick label style={font=\scriptsize},
title style={font=\small,align=center},
label style={font=\scriptsize},
legend style={font=\scriptsize,draw=none,at={(0.5,-0.19)},anchor=north},
legend columns=2,
axis x line*=bottom,axis y line*=left,
xmajorgrids=true,grid style={gray!20},
every axis plot/.append style={draw=white,line width=0.3pt},
]
\nextgroupplot[
title={A: Native CPU accounting\\Unprofiled before baseline},
yticklabels={InteriorH1Derivative,ReindexSingle,UMoments9,BarrierData41,EnvelopePsiB},
xlabel={Share of native user + system CPU (\%)},
]
"""
tex += plot("user", "fill=cpuuser") + plot("system", "fill=cpusystem")
tex += r"""\legend{User CPU,System CPU}
\nextgroupplot[
title={B: Native user-cycle sampling\\Separate perf-record execution},
yticklabels={,,,,},
xlabel={Share of decoded native user-cycle periods (\%)},
]
"""
for key, color in [("checker","checker"),("meta","metacolor"),("import","importcolor"),("other","othercolor"),("unresolved","unresolvedcolor")]:
    tex += plot(key, "fill=" + color)
tex += r"""\legend{C++ checker family,Lean Meta,Import,Other,Unresolved}
\end{groupplot}
\end{tikzpicture}
\end{document}
"""
(HERE / "native-cost-domains.tex").write_text(tex)
print(json.dumps({
    "data": data,
    "evidence": str(EVIDENCE.relative_to(ROOT)),
    "source_commit": "4f89614",
    "CPU_denominator": "each before-baseline native user+system CPU",
    "sample_denominator": "each separate native PID user-cycle period total",
    "cross_run_denominators_multiplied": False,
    "native_verifier_runs": 0,
}, indent=2))
