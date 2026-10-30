from pathlib import Path
import os,time,resource,json,subprocess,collections,shutil
os.sched_setaffinity(0,{0,1});resource.setrlimit(resource.RLIMIT_AS,(3*1024**3,3*1024**3));start=time.monotonic()
r=Path('/workspaces/repository');e=Path(__file__).parent
b=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30')
inp=json.loads((b/'pc-timeout-prefix-input.json').read_text());assert len(inp)==10
assert len({x['code']for x in inp})==1 and all(x['phase']==3 for x in inp)
assert all(x['id']==f'minif2f-4997-genuine-timeout-prefix-{i}'for i,x in enumerate(inp))
assert inp[0]['code'].startswith('set_option maxHeartbeats 3000')
outrows={};receipts=[];peak=0;collector_sources=[]
for cell in ['stock','library-off','sampler-on']:
 p=b/'captures'/('pc-native-timeout-prefix-'+cell)
 rec=json.loads((p/'receipt.json').read_text());assert rec['exit']==0 and rec['retired'] and rec['signals_sent']==0
 proc=Path('/proc')/str(rec['pid'])/'stat'
 if proc.exists():assert proc.read_text().split(') ')[1].split()[19]!=rec['start_ticks']
 receipts.append(rec);collector_sources.append((p/'source.lean').read_bytes())
 rows=[json.loads(l[6:])for l in (p/'stdout.txt').open()if l.startswith('M_DAG ')]
 assert len(rows)==10 and [x['id']for x in rows]==[x['id']for x in inp]
 assert all(x['hasErrors']for x in rows)
 outrows[cell]=rows
 for l in (p/'memory.jsonl').open():peak=max(peak,json.loads(l)['owned_rss_bytes'])
assert len(set(collector_sources))==1
for cell in ['library-off','sampler-on']:
 for x,y in zip(outrows['stock'],outrows[cell]):
  assert all(x[k]==y[k]for k in ['hasErrors','errors','infos','allocatedHeartbeatDelta'])
decoder=subprocess.check_output(['git','show','9b67361:research/mechanisms-2026-10-30/analyze_pc_samples.py'],cwd=r,text=True)
ns={'__name__':'root_readonly_pc_decoder'};exec(compile(decoder,'pinned9b67361-analyze_pc_samples.py','exec'),ns)
raw=b/'captures/pc-native-timeout-prefix-sampler-on/samples.bin';pc=ns['analyze'](raw)
assert pc['samples_written']==pc['samples_retained']==2977 and pc['overflow']==0
phase={int(k):v for k,v in pc['phase_counts'].items()};assert phase=={3:1751,0:1226}
cats={x['category']:x['samples']for x in pc['category_samples']if x['phase']==3}
assert cats['IR_interpreter_residence']==149 and cats['out_of_line_reference_count_lower_bound']==185 and cats['allocation_or_deallocation_lower_bound']==156 and cats['named_hash_or_table_lower_bound']==167 and cats['unresolved']==24
wrappers=[x for x in pc['top_symbols']if x['phase']==3 and x['symbol']in ['lean_inc','lean_dec']]
assert {x['symbol']for x in wrappers}=={'lean_inc','lean_dec'}
wrapper=sum(x['samples']for x in wrappers);assert wrapper==57
w=b/'captures/auxiliary-bound-witness';wr=json.loads((w/'receipt.json').read_text());assert wr['exit']==0 and wr['retired'] and wr['signals_sent']==0
proc=Path('/proc')/str(wr['pid'])/'stat'
if proc.exists():assert proc.read_text().split(') ')[1].split()[19]!=wr['start_ticks']
assert (w/'stdout.txt').read_text().strip()=="'auxiliary_bound_counterexample' does not depend on any axioms"
assert 667!=3 and 3!=1 and 1!=667 and 667*3*1==2001 and not667<=40 and 667+3+1==671
# Small source/receipt snapshots owned by root; original owner paths untouched.
(e/'collector-source.lean').write_bytes(collector_sources[0])
shutil.copyfile(w/'source.lean',e/'auxiliary-witness-source.lean')
shutil.copyfile(w/'receipt.json',e/'auxiliary-witness-receipt.json')
shutil.copyfile(w/'stdout.txt',e/'auxiliary-witness-stdout.txt')
(e/'inputs.json').write_text(json.dumps(inp,indent=2)+'\n')
result={'decoder_source':'9b67361','owner_result_state_at_read':'M source/result working tree not yet committed; root claims below independently reconstructed from retained raw captures using published decoder.','original_candidates':1,'repeated_units_per_cell':10,'cells':3,'native_returns':30,'all_native_retired':True,'all_flags_diagnostics_InfoTrees_rawHB_equal':True,'body_CPU_s':{k:sum(x['cpuNanoseconds']/1e9 for x in v)for k,v in outrows.items()},'body_wall_s':{k:sum(x['wallNanoseconds']/1e9 for x in v)for k,v in outrows.items()},'process_wall_s':[x['wall_s']for x in receipts],'sampled_owned_tree_peak_bytes':peak,'phase_counts':phase,'phase3_categories':cats,'additional_named_inc_dec_samples':wrapper,'RC_exact_named_subset_total':185+wrapper,'prefix_IR_fraction':149/1751,'IR_only_zero_cost_conditional_ratio':1/(1-149/1751),'witness':{'native_exit':wr['exit'],'native_retired':True,'whole_wall_s':wr['wall_s'],'native_wait4_peak_RSS_bytes':wr['native_kernel_peak_rss_bytes'],'one_sample_peak_RSS_bytes':wr['sampled_peak_owned_rss_bytes'],'axioms':[],'statement_role':'Counterexample to i<=40 under actual integer-product/distinctness hypotheses; final sum bound remains true at this point.'},'limits':['One original historically timed-out candidate repeated10times,not10 distinct candidates.','Explicit maxHeartbeats3000 samples a curtailed prefix,not original300s execution.','Named PC residence is not hardware cycles,total inlined operation counts or a full-timeout distribution.','No actual precompilation acceleration,early-abort method,failure accuracy or global Amdahl bound.','Counterexample to a local assertion does not refute final theorem or qualify whole-request rejection with backtracking/recovery.','One ordered stock/off/on pass; no causal overhead or IID confidence estimate.','Short-witness1s sampling misses native high-water peak; report wait4 separately.','No production engine method or closed GPU route enabled.']}
result.update(root_elapsed_s=time.monotonic()-start,root_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(e/'reanalysis.json').write_text(json.dumps(result,indent=2)+'\n');(e/'decoded-PC-summary.json').write_text(json.dumps({k:v for k,v in pc.items()if k!='top_symbols'},indent=2)+'\n');print(json.dumps(result,indent=2))
