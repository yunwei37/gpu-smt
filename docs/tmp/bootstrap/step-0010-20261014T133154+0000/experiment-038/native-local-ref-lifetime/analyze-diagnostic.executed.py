from pathlib import Path
import json,statistics
n=Path(__file__).resolve().parent
rows=json.loads((n/'diagnostic-summary.json').read_text())
assert len(rows)==6
assert [(x['block'],x['method']) for x in rows]==[(1,'stock'),(1,'locked'),(1,'atomic'),(2,'atomic'),(2,'locked'),(2,'stock')]
assert all(x.get('complete_array') and x.get('normal_eof') and x.get('exit_code')==0 for x in rows)
assert all(x['responses']==rows[0]['responses'] for x in rows)
brief=[]
for block in [1,2]:
 d={x['method']:x for x in rows if x['block']==block}
 for method in ['stock','locked','atomic']:
  x=d[method]
  brief.append({'block':block,'method':method,'whole_seconds':x['whole_ns']/1e9,'batch_seconds':x['batch_ns']/1e9,'waited_child_cpu_user_seconds':x['waited_tree_cpu_user'],'waited_child_cpu_system_seconds':x['waited_tree_cpu_system'],'collector_cpu_seconds':x['collector_cpu_seconds'],'sampled_peak_pss_bytes':x['sampled_peak_pss']})
 print('BLOCK',block,'atomic_over_locked_whole',d['atomic']['whole_ns']/d['locked']['whole_ns'],'atomic_over_stock_whole',d['atomic']['whole_ns']/d['stock']['whole_ns'])
result={'cells':brief,'all_native_responses_equal':True,'all_native_normal_eof_exit0':True,'source_count_per_cell':rows[0]['width'],'orders':[['stock','locked','atomic'],['atomic','locked','stock']],'scope':'finite overlapped original24source development diagnostic; neither isolated nor full-corpus paper result'}
(n/'diagnostic-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
