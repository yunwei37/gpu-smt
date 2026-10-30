from pathlib import Path
import os,sys,json,subprocess,collections,struct,re,math,time,resource,datetime
os.sched_setaffinity(0,{0,1});sys.dont_write_bytecode=True;t0=time.monotonic()
root=Path('/workspaces/repository');m=root/'research/mechanisms-2026-10-30'
source=subprocess.check_output(['git','show','363851c:research/mechanisms-2026-10-30/analyze_pc_samples.py'],cwd=root,text=True)
ns={'__name__':'root_source_reanalysis','__file__':str(m/'analyze_pc_samples.py')};exec(compile(source,str(m/'analyze_pc_samples.py'),'exec'),ns)
def independent_phase_counts(path):
 with path.open('rb') as f:
  n,cap,interval,version=struct.unpack('<QQQQ',f.read(32));assert version==1 and n<=cap
  phases=collections.Counter();threads=set()
  for _ in range(n):
   pc,phase,thread=struct.unpack('<QQQ',f.read(24));phases[phase]+=1;threads.add(thread)
 return {'count':n,'interval_us':interval,'phases':dict(phases),'threads':sorted(threads)}
def row_capture(prefix,expected):
 raw=Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/captures')
 cells={}
 for mode in ['stock','library-off','sampler-on']:
  p=raw/(prefix+'-'+mode);rec=json.loads((p/'receipt.json').read_text())
  assert rec['exit']==0 and rec['retired']
  stat=Path('/proc')/str(rec['pid'])/'stat'
  if stat.exists():assert stat.read_text().split(') ',1)[1].split()[19]!=str(rec['start_ticks'])
  text=(p/'stdout.txt').read_text()
  rows=[json.loads(l[6:]) for l in text.splitlines() if l.startswith('M_DAG ')]
  if expected:assert len(rows)==expected
  cells[mode]={'rows':rows,'stdout':text,'source':(p/'source.lean').read_text(),'receipt':rec,'path':str(p)}
 return cells
reps=row_capture('pc-native-representatives',31);differences=[]
for mode in ['library-off','sampler-on']:
 for a,b in zip(reps['stock']['rows'],reps[mode]['rows']):
  assert a['id']==b['id']
  for field in ['hasErrors','errors','infos','allocatedHeartbeatDelta']:
   if a[field]!=b[field]:differences.append({'id':a['id'],'comparator':mode,'field':field,'stock':a[field] if field=='allocatedHeartbeatDelta' else None,'observed':b[field] if field=='allocatedHeartbeatDelta' else None})
assert differences==[{'id':'minif2f-6684-pc-repeat-0','comparator':'library-off','field':'allocatedHeartbeatDelta','stock':964276,'observed':964274}]
reps_p=Path(reps['sampler-on']['path'])/'samples.bin'
reps_ind=independent_phase_counts(reps_p);reps_res=ns['analyze'](reps_p)
assert reps_ind['count']==reps_res['samples_retained']==16649 and reps_res['overflow']==0
assert reps_ind['phases']==reps_res['phase_counts']
kernel=row_capture('pc-digits-pure-timing',0)
base=(m/'DigitsCertificate.lean').read_text()
def math_part(s):return s[s.index('namespace MechanismCertificate\n'):s.index('\nopen Lean Elab Command in')]
mathematical_source_equal=all(math_part(x['source'])==math_part(base) for x in kernel.values());assert mathematical_source_equal
canonical=[];kernel_cells=[]
for mode,x in kernel.items():
 s=x['source'];assert s.index('let stop ← IO.monoNanosNow',s.index('let result := env.addDeclCore'))<s.index('mPCStop',s.index('let result := env.addDeclCore'))
 nsvalue=int(re.search(r'M_KERNEL_RECHECK_NS=(\d+)',x['stdout'])[1]);hb=int(re.search(r'M_KERNEL_RECHECK_HB=(\d+)',x['stdout'])[1])
 stdout=[l for l in x['stdout'].splitlines() if 'M_KERNEL_RECHECK_' not in l]
 canonical.append(stdout)
 assert any("'MechanismCertificate.computed_count' does not depend on any axioms" in l for l in stdout)
 assert hb==57844573
 kernel_cells.append({'mode':mode,'warm_recheck_interval_s':nsvalue/1e9,'raw_HB':hb,'whole_process_wall_s':x['receipt']['wall_s'],'receipt':x['receipt']})
assert canonical[0]==canonical[1]==canonical[2]
kernel_p=Path(kernel['sampler-on']['path'])/'samples.bin'
kernel_ind=independent_phase_counts(kernel_p);kernel_res=ns['analyze'](kernel_p)
assert kernel_ind['count']==kernel_res['samples_retained']==4258 and kernel_ind['phases']=={4:4258} and kernel_res['overflow']==0
def phase_table(decoded,phases):
 cats=collections.Counter({(x['phase'],x['category']):x['samples'] for x in decoded['category_samples']})
 out=[]
 for phase in phases:
  n=decoded['phase_counts'][phase]
  out.append({'phase':phase,'n':n,'IR':cats[(phase,'IR_interpreter_residence')],
    'RC':cats[(phase,'out_of_line_reference_count_lower_bound')],
    'alloc_free':cats[(phase,'allocation_or_deallocation_lower_bound')],
    'tables':cats[(phase,'named_hash_or_table_lower_bound')],
    'unresolved':cats[(phase,'unresolved')]})
 return out
table=phase_table(reps_res,[0,1,2,3,4]);kernel_table=phase_table(kernel_res,[4])
assert kernel_table[0]=={'phase':4,'n':4258,'IR':0,'RC':699,'alloc_free':462,'tables':777,'unresolved':124},kernel_table
initial=json.loads((m/'pc-digits-result.json').read_text())
assert all(c['recheck_raw_HB']==57844572 for c in initial['cells'])
matrix=json.loads(Path('/workspaces/.agent-state/gpu-smt-captures/mechanisms-2026-10-30/native-cohort-matrix/terminal.json').read_text())
matrix_wall=math.fsum(c['wall_s'] for c in matrix['cells'])
d={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_invocations':0,'decoder_commit':'363851c',
 'representative_returns':93,'representative_sources':31,'representative_differences':differences,
 'representative_PC_binary':reps_ind,'representative_PC_table':table,
 'representative_body_totals':{mode:{'cpu_s':math.fsum(x['cpuNanoseconds']/1e9 for x in c['rows']),'wall_s':math.fsum(x['wallNanoseconds']/1e9 for x in c['rows'])} for mode,c in reps.items()},
 'representative_whole_process_wall_s':{mode:c['receipt']['wall_s'] for mode,c in reps.items()},
 'kernel_cells':kernel_cells,'math_source_equal':mathematical_source_equal,'same_non_timing_stdout':True,
 'printed_axioms':canonical[0],'corrected_kernel_PC_binary':kernel_ind,'corrected_kernel_PC_table':kernel_table,
 'initial_recheck_raw_HB':57844572,'corrected_recheck_raw_HB':57844573,
 'whole_matrix_native_wall_sum_s':matrix_wall,'M_reported_group_limit_s':1800,'matrix_exceeds_reported_group_limit':matrix_wall>1800,
 'root_elapsed_s':time.monotonic()-t0,'root_maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(sys.argv[1]).write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({k:v for k,v in d.items() if k not in ['kernel_cells','printed_axioms']},indent=2))
print('KERNEL_TIMES',[{k:v for k,v in c.items() if k!='receipt'} for c in kernel_cells])
