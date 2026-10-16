"""Plot all existing complete E023 primary repetitions; no benchmark execution."""
from pathlib import Path
import json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
R=HERE.parents[2]
data=json.loads((R/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/service-replay-summary.json').read_text())
cells=[c for c in data['cells'] if c['primary']]
assert len(cells)==27 and all(c['returned']==5952 for c in cells)
rates=sorted({c['rate']for c in cells})
plt.rcParams.update({'font.family':'serif','font.size':8,'axes.labelsize':8,
 'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,'lines.linewidth':1.2,
 'pdf.fonttype':42,'axes.grid':True,'grid.alpha':.22})
fig,ax=plt.subplots(figsize=(3.375,2.7))
for method,label,color,style,marker in [
 ('branch','Independent branches','#0072B2','-','o'),
 ('prepared','Warm pool','#D55E00','--','s'),
 ('snapshot','Snapshot/cache','#333333',':','^')]:
 means=[]
 for rate in rates:
  vals=[c['metrics']['scheduled_arrival_to_terminal_ns']['p95_s']for c in cells if c['method']==method and c['rate']==rate]
  assert len(vals)==3
  ax.scatter([rate]*3,vals,marker=marker,s=22,color=color,alpha=.8,zorder=3)
  means.append(statistics.mean(vals))
 ax.plot(rates,means,label=label,color=color,linestyle=style)
ax.set_xlabel('Scheduled arrival rate (attempts/s)')
ax.set_ylabel('95th-percentile arrival latency (s)')
ax.set_xticks(rates,[f'{r:.2f}'for r in rates])
ax.set_yticks([0,60,120,180,240,300])
ax.set_ylim(0,300)
ax.legend(loc='upper left',frameon=False,handlelength=2)
fig.tight_layout(pad=.5)
fig.savefig(HERE/'proofnet-offered-arrival-p95.pdf',bbox_inches='tight',pad_inches=.02)
fig.savefig(HERE/'proofnet-offered-arrival-p95.png',bbox_inches='tight',pad_inches=.02,dpi=300)
print('matplotlib',matplotlib.__version__,'primary_cells',len(cells),'rates',rates)
