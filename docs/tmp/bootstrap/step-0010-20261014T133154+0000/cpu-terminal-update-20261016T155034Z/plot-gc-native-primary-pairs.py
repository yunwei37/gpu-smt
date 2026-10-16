from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent
old=json.loads((O/'reused-primary-evidence.json').read_text())['gc_prior_primary_pairs']
new=json.loads((O/'gc-third-primary-pair.json').read_text())
points=[{'reference_seconds':p['reference_seconds'],'candidate_seconds':p['candidate_seconds'],'pair':p.get('rep',i)+1} for i,p in enumerate(old)]
points.append({'reference_seconds':new['reference_whole_seconds'],'candidate_seconds':new['candidate_whole_seconds'],'pair':3})
assert len(points)==3
# Match the existing paper result style and its measured 243bp column width.
plt.rcParams.update({'font.size':8,'axes.labelsize':8,'xtick.labelsize':7.5,'ytick.labelsize':7.5,'legend.fontsize':7.5,'font.family':'serif','lines.linewidth':1.2,'pdf.fonttype':42,'axes.grid':True,'grid.alpha':.22})
fig,ax=plt.subplots(figsize=(3.375,2.55))
x=list(range(3));w=.34
ax.bar([i-w/2 for i in x],[p['reference_seconds']/3600 for p in points],width=w,color='#9E9E9E',edgecolor='#333333',linewidth=.6,hatch='//',label='Original library loading')
ax.bar([i+w/2 for i in x],[p['candidate_seconds']/3600 for p in points],width=w,color='#0072B2',edgecolor='#333333',linewidth=.6,label='Native library loading')
ax.set_ylim(0,12);ax.set_yticks([0,3,6,9,12]);ax.set_ylabel('Corpus elapsed time (h)')
ax.set_xticks(x);ax.set_xticklabels(['Pair 1','Pair 2','Pair 3']);ax.set_xlabel('Alternating full-corpus observations')
ax.grid(axis='x',visible=False);ax.set_axisbelow(True)
ax.legend(loc='lower center',bbox_to_anchor=(.5,1.01),frameon=False,borderpad=.3)
fig.subplots_adjust(left=.17,right=.98,bottom=.21,top=.78)
fig.savefig(O/'gc-native-primary-pairs.pdf')
fig.savefig(O/'gc-native-primary-pairs.png',dpi=300)
plt.close(fig)
(O/'gc-native-primary-pairs.source.json').write_text(json.dumps({'population_per_condition':29750,'pairs':points,'baseline':'same GC REPL with original library loading','candidate':'native shared-library loading; ordinary compilation, not system novelty','profiles':'excluded, two incomplete resource conditions are not extra primary repetitions','qualification':'Every actual primary pair is shown. Shared background, failures, service shutdown/EOF and capture costs remain charged. Observed differences/range are not confidence intervals, isolated causality or GPU benefit. Native outcomes are not asserted identical.','intended_print_width_bp':243,'canvas_width_inches':3.375,'minimum_font_pt':7.5},indent=2)+'\n')
print('FIGURE_COMPLETE',str(O/'gc-native-primary-pairs.pdf'))
