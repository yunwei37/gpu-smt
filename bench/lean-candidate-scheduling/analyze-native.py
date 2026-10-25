"""Audit actual scheduling consumer results, clocks and task acceptance."""
from pathlib import Path
import argparse,collections,gzip,json
def analyze(root):
 selected=json.loads((root/'selected.json').read_text())['ids'];wanted=set(selected)
 cells={};baseline=None
 for mode in ['all','first-original','first-short']:
  out=root/mode;t=json.loads((out/'terminal.json').read_text())
  with gzip.open(out/'consumer-results.jsonl.gz','rt')as f:rows=[json.loads(l)for l in f]
  by={x['proof_id']:x for x in rows}
  assert len(rows)==len(by)==len(wanted)and set(by)==wanted
  assert t['state']=='complete'and t['returned']==len(wanted)
  assert not t['owned_live_descendants_after_shutdown']
  assert not t['memory_watchdog']['error']and t['memory_watchdog']['peak_sampled_native_repl_count']<=2
  assert t['memory_watchdog']['peak_sampled_owned_rss_bytes']<=48*1024**3
  task=lambda pid:int(pid.split('-')[1])//32
  valid={pid for pid,x in by.items()if x['status']=='valid'}
  solved={task(pid)for pid in valid}
  cancelled=[x for x in rows if x['status']=='cancelled_after_success']
  for x in cancelled:
   assert x['native_response_returned']is False and x['result']['time']is None
   assert x['winner']in valid and task(x['proof_id'])==task(x['winner'])
  if baseline is None:baseline=by;baseline_solved=solved
  actual=[x for x in rows if x['native_response_returned']]
  changes=[dict(source_id=x['proof_id'],all_status=baseline[x['proof_id']]['status'],consumer_status=x['status'])
   for x in actual if baseline[x['proof_id']]['status']!=x['status']]
  cells[mode]=dict(counts=dict(collections.Counter(x['status']for x in rows)),solved_task_ids=sorted(solved),
   solved_task_set_matches_all=solved==baseline_solved,actual_response_count=len(actual),
   source_status_changes_on_executed=changes,queued_cancellations=len(cancelled),
   whole_native_lifecycle_seconds=t['whole_lifecycle_seconds'],
   consumer_complete_lifecycle_seconds=t['consumer_complete_lifecycle_seconds'],memory=t['memory_watchdog'])
 assert json.loads((root/'client-exit.json').read_text())['exit']==0
 return dict(selection_count=len(selected),task_count=len({int(x.split('-')[1])//32 for x in selected}),cells=cells,
  scope='Measured complete native and consumer lifecycles; task acceptance differs from per-candidate labels. All cancellations verified against an actually checked same-task winner. Self-review.')
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',type=Path,required=True);a=p.parse_args()
 result=analyze(a.run);(a.run/'paired-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
