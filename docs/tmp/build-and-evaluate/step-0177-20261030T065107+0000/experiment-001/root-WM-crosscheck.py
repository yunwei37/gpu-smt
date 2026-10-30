import csv,gzip,io,json,math,os,pathlib,resource,statistics,subprocess,time
os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
ROOT=pathlib.Path('/workspaces/repository')
STEP=pathlib.Path(pathlib.Path('/workspaces/.agent-state/gpu-smt-paper-WM-integration-step.txt').read_text().strip())
W='3c6546b';M='f387566'
started=time.monotonic()
def frozen(commit,path,binary=False):
    raw=subprocess.check_output(['git','-c','gc.auto=0','show',commit+':'+path],cwd=ROOT)
    return raw if binary else raw.decode()
def wjson(path): return json.loads(frozen(W,'workloads/candidates/'+path))
def mjson(path): return json.loads(frozen(M,'research/mechanisms-2026-10-30/'+path))
with gzip.open(ROOT/'artifacts/autoverus-native-2026-10-09/full/analysis/cells.json.gz','rt') as f:
    cells=json.load(f)
reported=list(csv.DictReader(io.StringIO(frozen(W,'workloads/candidates/autoverus-tail-direct.csv'))))
tail=[]
for rep in range(3):
    rows=[x for x in cells if x['condition']=='direct' and x['repetition']==rep]
    assert len(rows)==len({x['candidate'] for x in rows})==3566
    assert all(x['complete'] and not x['timed_out'] for x in rows)
    ordered=sorted(rows,key=lambda x:x['external_wall_s'],reverse=True)
    den=math.fsum(x['external_wall_s'] for x in ordered)
    n=math.ceil(len(rows)*.016)
    num=math.fsum(x['external_wall_s'] for x in ordered[:n])
    rc={str(k):sum(x['returncode']==k for x in rows) for k in [0,1,101]}
    assert rc=={'0':190,'1':3359,'101':17}
    published=next(x for x in reported if int(x['repeat'])==rep)
    for key,v in [('sum_candidate_process_wall_s',den),('tail_process_wall_s',num),('tail_share',num/den)]:
        assert math.isclose(float(published[key]),v,rel_tol=1e-12,abs_tol=1e-8),(key,v)
    tail.append({'repeat':rep,'rows':len(rows),'tail_rows':n,'process_wall_sum_s':den,
                 'tail_process_wall_s':num,'tail_share':num/den,'returncodes':rc})
del cells
epfl=wjson('epfl-evaluation-0bbf3133/summary.json')
groups=list(csv.DictReader(io.StringIO(frozen(W,'workloads/candidates/epfl-evaluation-0bbf3133/verdicts.csv'))))
sums={key:sum(int(x[key]) for x in groups) for key in ['programs','valid','invalid','failed','wrong_declaration']}
assert len(groups)==6
assert sums==dict(programs=68932,valid=28145,invalid=40787,failed=39473,wrong_declaration=1314)
assert sums['programs']==sums['valid']+sums['invalid']
assert sums['invalid']==sums['failed']+sums['wrong_declaration']
assert epfl['lexical_failures']==2 and epfl['no_native_processes']
april=wjson('april-test-4e307527-script-v2/summary.json')
subsets=list(csv.DictReader(io.StringIO(frozen(W,'workloads/candidates/april-test-4e307527-script-v2/subsets.csv'))))
lnsym=wjson('lnsym-5c05220f.json')
# Validate M's completed native receipts and the exact declarations whose axioms were printed.
native='native/phobos-digits-certificate-v4/'
receipt=mjson(native+'receipt.json')
source=frozen(M,'research/mechanisms-2026-10-30/'+native+'source.lean')
stdout=frozen(M,'research/mechanisms-2026-10-30/'+native+'stdout.txt')
assert receipt['exit']==0 and receipt['retired'] and receipt['signals_sent']==0
assert receipt['sampled_peak_owned_rss_bytes']<16*2**30
assert "'MechanismCertificate.computed_count' does not depend on any axioms" in stdout
assert stdout.count('depends on axioms: [propext, Quot.sound, Classical.choice]')==2
assert 'sorryAx' not in stdout
recheck_ns=int(stdout.split('M_KERNEL_RECHECK_NS=')[1].splitlines()[0])
assert recheck_ns==8557221814
assert 'theorem computed_count : blockSum 100 = 100 := by decide' in source
assert 'S.card = 100' in source and 'digitsFuel_eq 4 n hn' in source
qualifying=[n for n in range(1000,10000) if n%5==0 and all(int(d)%2==0 for d in str(n))]
assert len(qualifying)==100 and sum(qualifying)==544000
versions=[{'version':i,'exit':mjson(f'native/phobos-digits-certificate-v{i}/receipt.json')['exit']} for i in range(1,5)]
assert [x['exit'] for x in versions]==[1,1,1,0]
# This is a check of the retained leader table, not a new scan of all raw RSS streams.
raw=frozen(M,'research/mechanisms-2026-10-30/retained-analysis/prepared-leader-observations.jsonl.gz',True)
leaders=[json.loads(x) for x in gzip.decompress(raw).decode().splitlines()]
ordinary=[x['leader_peak_bytes'] for x in leaders if x['status'] in ['accepted','rejected']]
ms=mjson('retained-analysis/parent-rss-scope.json')
assert len(leaders)==7808 and len(ordinary)==7682
assert statistics.median(ordinary)==ms['accepted_or_rejected_prepared_leader_peak_bytes']['median']==470599680
p99=sorted(ordinary)[int((len(ordinary)-1)*.99)]
assert p99==ms['accepted_or_rejected_prepared_leader_peak_bytes']['p99']==977809408
parent=ms['registered_parent_observed_peak_bytes']['maximum']
assert parent==3614543872
result={'W_commit':W,'M_commit':M,'native_executions_by_root':0,'independent_autoverus_receipt_recalculation':tail,
        'EPFL_six_group_conservation':sums,'EPFL_lexical_unavailable':2,
        'APRIL_test_rows':april['rows_read'],'APRIL_native_runs':april['native_runs'],
        'LNSym_source_files':lnsym['source_files'],'LNSym_direct_tokens':lnsym['lexical_occurrences'],
        'M_certificate':{'version_exits':versions,'wall_s':receipt['wall_s'],'cpu_s':receipt['native_cpu_seconds'],
         'leader_wait4_peak_bytes':receipt['native_kernel_peak_rss_bytes'],
         'sampled_own_tree_peak_bytes':receipt['sampled_peak_owned_rss_bytes'],
         'warm_extra_declaration_recheck_ns':recheck_ns,'root_independent_count':len(qualifying),
         'root_independent_sum':sum(qualifying),'numeric_check_is_not_a_proof':True,
         'full_cost_includes_extra_recheck':True,'ordinary_kernel_success':'native v4 retained output',
         'bridge_axioms':['propext','Quot.sound','Classical.choice'],
         'new_trust_axioms_observed':False},
        'M_leader_table_self_review':{'prepared_attempt_rows':len(leaders),'ordinary_rows':len(ordinary),
          'ordinary_median_leader_RSS_bytes':statistics.median(ordinary),'ordinary_p99_leader_RSS_bytes':p99,
          'separately_observed_parent_max_bytes':parent,'aggregate_memory_discount_inferred':False,
          'quantile_convention':'M floor((n-1)*.99), checked at n=7682; no small-n percentile claim'},
        'scope':['Derived-table consistency is self-review, not a second EPFL full raw scan.',
                 'AutoVerus uses each repeat own process-wall sum; not service wall or generation time.',
                 'Native certificate changes proof representation and is not engine throughput or original-candidate parity.',
                 'Leader RSS omits descendants/parent; separate maxima cannot establish a simultaneous aggregate frontier.'],
        'root_affinity':sorted(os.sched_getaffinity(0)),'elapsed_s':time.monotonic()-started,
        'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(STEP/'experiment-001/root-crosscheck.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
