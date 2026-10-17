"""Compare completed formal prefix captures by original source index.
Operational outcomes and partial acquisition never establish semantic agreement.
"""
from pathlib import Path
import argparse,gzip,json
def cell(path):
    receipt=path/'terminal.json'
    if not receipt.exists():return None
    t=json.loads(receipt.read_text())
    with gzip.open(path/'results.jsonl.gz','rt') as f:rows=[json.loads(x) for x in f]
    by={x['index']:x for x in rows}
    return {'terminal':t,'rows':by,
      'complete':t['state']=='complete' and len(rows)==len(by)==t['expected']}
def analyze(root):
    cells={m:cell(root/m) for m in ['batch','exact','unit']}
    out={'root':str(root),'comparisons':[]}
    for method in ['exact','unit']:
        b=cells['batch'];c=cells[method]
        if not b or not c:
            out['comparisons'].append({'method':method,'state':'pending'});continue
        full=b['complete'] and c['complete'] and b['rows'].keys()==c['rows'].keys()
        ops={m:[i for i,x in v['rows'].items() if x['outcome']=='operational']
             for m,v in [('batch',b),(method,c)]}
        diffs=[i for i in b['rows'].keys() & c['rows'].keys()
               if b['rows'][i]['outcome']!=c['rows'][i]['outcome']]
        unchecked=[i for i,x in c['rows'].items() if x['outcome']=='complete'
                   and 'proofState' in x['response'] and x['response'].get('kernelChecked') is not True]
        valid=full and not any(ops.values()) and not diffs and not unchecked
        bt=b['terminal'];ct=c['terminal']
        out['comparisons'].append({'method':method,
          'state':'pending' if not full else ('valid' if valid else 'operational_or_verdict_mismatch'),
          'sources':len(b['rows'].keys() & c['rows'].keys()),
          'operational_indices':ops,'verdict_differences':sorted(diffs),
          'closed_prefix_without_native_kernel_receipt':unchecked,
          'batch_whole_seconds':bt['whole_seconds'],'prefix_whole_seconds':ct['whole_seconds'],
          'observed_batch_over_prefix_ratio':bt['whole_seconds']/ct['whole_seconds'] if full else None,
          'validated_whole_ratio':bt['whole_seconds']/ct['whole_seconds'] if valid else None,
          'cpu_accounting_complete':bt.get('cpu_accounting_complete',bt.get('normal_native_exit',False)) and ct.get('cpu_accounting_complete',ct.get('normal_native_exit',False)),
          'native_parser_included_seconds':ct['native_parse_seconds'],
          'fallbacks':ct['fallbacks'],'cached_lookups':ct['cached_lookups'],
          'executed_prefix_nodes':ct['executed_prefix_nodes']})
    out['scope']='One offline capture/order of original task candidates, native in-process batch4 versus SHRED-parser-based prefix executor. Includes parse/preparation/IPC/fallback/kernel/retirement. Not an upstream whole-service SHRED benchmark, repeated-trial result, or GPU speedup. Forced-retirement CPU is censored; operational results remain unresolved.'
    return out
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run',type=Path);a=p.parse_args()
    out=analyze(a.run);(a.run/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
