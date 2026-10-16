from pathlib import Path
import json,zipfile,collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
D=Path(__file__).parent
label='goedel427-rep0-aot'
with zipfile.ZipFile(D/'native-oracle-full1'/(label+'.zip')) as z:
 rows=[json.loads(s) for s in z.read(label+'/results.jsonl').decode().splitlines()]
# main.log records textwidth505.89pt; configured columnsep0.25in=18.0675pt.
# (505.89-18.0675)/(2*72.27)=3.375in. Near printed column size.
plt.rcParams.update({'font.size':8,'axes.labelsize':8,'xtick.labelsize':7,
 'ytick.labelsize':7,'legend.fontsize':7,'font.family':'serif',
 'lines.linewidth':1.2,'pdf.fonttype':42,'axes.grid':True,'grid.alpha':0.22})
fig,ax=plt.subplots(figsize=(3.375,2.7))
series=[('All outcomes',rows,'#222222','-'),
 ('Complete proofs',[x for x in rows if x['basic']=='complete'],'#0072B2','--'),
 ('Rejected sources',[x for x in rows if x['basic']=='rejected'],'#D55E00','-.'),
 ('Operational failures',[x for x in rows if x['basic']=='operational'],'#CC79A7',':')]
for label,data,color,style in series:
 values=np.sort([x['elapsed_seconds'] for x in data])
 sf=(len(values)-np.arange(len(values)))/len(values)
 ax.step(values,sf,where='post',label=label,color=color,linestyle=style)
ax.set_xscale('log');ax.set_yscale('log')
ax.set_xlabel('Closed-loop request latency (s)')
ax.set_ylabel('Fraction at or above latency')
ax.set_ylim(1/len(rows),1.1)
ax.set_xticks([.01,.1,1,10,100]);ax.set_xticklabels(['0.01','0.1','1','10','100'])
ax.set_yticks([1,.1,.01,.001,.0001]);ax.set_yticklabels(['1','0.1','0.01','0.001','0.0001'])
ax.minorticks_off()
ax.legend(loc='upper center',bbox_to_anchor=(.5,1.37),frameon=False,ncol=2,
 handlelength=2.1,columnspacing=1.1)
fig.subplots_adjust(left=.19,right=.98,bottom=.18,top=.79)
out=D/'native-aot-reference-latency'
fig.savefig(str(out)+'.pdf',bbox_inches='tight',pad_inches=.03)
fig.savefig(str(out)+'.png',bbox_inches='tight',pad_inches=.03,dpi=300)
plt.close(fig)
caption=('Closed-loop request latency for one complete native-compilation reference acquisition '
 'of all29,750 released GoedelWorkbook source files, with four outstanding requests '
 'on shared CPU0–3. Each curve is the fraction of its indicated outcome population '
 'whose request duration is at least the horizontal-axis value. Both axes are logarithmic '
 'to expose the tail. Alloutcomes include27319complete,2376rejected and55operational results; '
 'one acquisition provides no between-run uncertainty. Slow successful work and operational '
 'failures form distinct latency tails. These overlapping request durations are neither '
 'kernel-only CPUtime nor a decomposition of whole walltime, and the figure makes no '
 'speedup or offered-load queueing claim.')
(D/'native-aot-reference-latency-caption.md').write_text(caption+'\n')
print(json.dumps({'sources':len(rows),'outputs':[str(out)+'.pdf',str(out)+'.png'],
 'counts':dict(collections.Counter(x['basic'] for x in rows))}))
