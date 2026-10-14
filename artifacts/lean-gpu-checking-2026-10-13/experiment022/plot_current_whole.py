#!/usr/bin/env python3
"""Stage full matched native/GPU blocks from the actual E022 analyzer output."""
import argparse
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

METHODS = ('warm', 'snapshot-cache', 'cpu', 'gpu')
LABELS = ('Native warm', 'Native snapshot/cache', 'CPU algorithm control', 'GPU + native fallback')
COLORS = ('#333333', '#777777', '#E69F00', '#0072B2')
HATCHES = ('', '///', '..', 'xx')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--analysis', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    report = json.loads(args.analysis.read_text())
    by_label = {x['label']: x for x in report['cells']}
    pairs = [x for x in report['paired_whole_effects']
             if x['dataset'] == 'proofnet' and x['role'] == 'primary whole repetition']
    if not pairs or not all(x['valid_basic_resource_matched_block'] and x['actual_device_operation_and_readback'] for x in pairs):
        raise ValueError('no valid complete native/device block')
    for pair in pairs:
        if not all(by_label[f'proofnet-{pair["block"]}-{method}']['valid_complete'] for method in METHODS):
            raise ValueError('incomplete whole source cell')
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'source-analysis.json').write_bytes(args.analysis.read_bytes())
    (args.out / 'executed-plot.py').write_bytes(Path(__file__).read_bytes())
    plt.rcParams.update({'font.family': 'serif', 'font.size': 8, 'axes.labelsize': 8,
                         'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 8,
                         'pdf.fonttype': 42, 'grid.alpha': .2})
    fig, ax = plt.subplots(figsize=(3.375, 2.75))
    rows = []
    width = .18
    for j, method in enumerate(METHODS):
        series = [by_label[f'proofnet-{pair["block"]}-{method}'] for pair in pairs]
        ax.bar([i + (j - 1.5) * width for i in range(len(pairs))],
               [x['whole_seconds'] for x in series], width=width,
               label=LABELS[j], color=COLORS[j], hatch=HATCHES[j], edgecolor='black', linewidth=.5)
        rows.extend({'block': pair['block'], 'method': method, 'whole_seconds': x['whole_seconds'],
                     'valid_complete': x['valid_complete'], 'source_outcomes': json.dumps(x['outcomes'], sort_keys=True)}
                    for pair, x in zip(pairs, series))
    ax.set_xticks(range(len(pairs)), [x['block'].replace('rep', 'Run ') for x in pairs])
    ax.set_ylabel('Complete verification time (s)')
    ax.set_ylim(bottom=0)
    ax.grid(axis='y'); ax.set_axisbelow(True)
    ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.01), frameon=False, ncol=1)
    fig.tight_layout(pad=.5)
    fig.savefig(args.out / 'whole-time.pdf')
    fig.savefig(args.out / 'whole-time.png', dpi=300)
    plt.close(fig)
    with (args.out / 'whole-observations.csv').open('x', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0]); writer.writeheader(); writer.writerows(rows)
    (args.out / 'README.md').write_text(
        '# Complete-block native/GPU verification observations\n\n'
        f'{len(pairs)} complete matched primary ProofNet blocks, each method verifies all5952 original candidate sources. '
        'All basic decisions and CPU masks/worker width agree; actual GPU operations/native Expr readback engage and CPU algorithm calls are zero in GPU cells. '
        'The whole boundary retains frontend/preparation/cache/device setup/representation/upload/launch/readback/native fallback/final kernel and EOF; archive costs remain after-clock as declared. '
        'Both native warm and native snapshot/cache are main competitors. Same-algorithm CPU is a control, not a substitute strong baseline. '
        'The shown GPU method is slower than the faster native competitor in every shown block.\n\n'
        'Bars are individual whole runs, not an average/CI; no significance or universal GPU impossibility is inferred. '
        f'This saved analysis has {report["terminal_full_cells"]} terminal cells of the original {report["planned_full_cells"]}; complete_full_matrix={report["complete_full_matrix"]}. '
        'Normal shared5090/host competition is explicit, with no isolation/half-card assumption. '
        'Native3 invalid aborted timings are excluded and preserved separately; no runtime clocks are stitched.\n\n'
        'Vector PDF3.375in/font8pt, distinguishable gray/color/hatches, zero-based seconds axis; executed source and exact analyzer input retained. '
        'Reproduce plot_current_whole.py --analysis SOURCE --out ABSENT_DIRECTORY in retained matplotlib environment. '
        'Staged artifact only; complete planned scope and fresh review precede paper insertion.\n')


if __name__ == '__main__':
    main()
