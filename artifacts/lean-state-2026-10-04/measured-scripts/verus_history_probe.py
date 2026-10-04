#!/usr/bin/env python3
"""Probe the two prefix-pool differences not reproduced by fresh scope alone.

Compare a target as the first request after prefix setup with its recorded
preceding request history. Query limits/options are unchanged; diagnostics
are observational get-info requests. No fidelity or speedup claim is made.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from analyze_smt_trace import split_commands, command_head, int_arg
from verus_session_replay import Session, decisions
from verus_scope_ablation import leading_options


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run-dir',type=Path,required=True);ap.add_argument('--replay-dir',type=Path,required=True)
    ap.add_argument('--ablation-dir',type=Path,required=True);ap.add_argument('--z3',required=True)
    ap.add_argument('--cores',default='8');ap.add_argument('--repeat',type=int,default=2)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    config=json.loads((args.replay_dir/'config.json').read_text())
    runs=json.loads((args.replay_dir/'runs.json').read_text())
    cold=next(r for r in runs if r['mode']=='cold' and r['repeat']==0)['records']
    pooled=next(r for r in runs if r['mode']=='prefix_pool' and r['repeat']==0)['records']
    scoped=next(r for r in json.loads((args.ablation_dir/'runs.json').read_text()) if r['mode']=='prefix_scope_fresh' and r['repeat']==0)['records']
    targets={r['trace'] for r in scoped if r['matches_baseline'] and not r['matches_reused_pool']}
    pool_status={r['trace']:r['statuses'] for r in pooled};jobs=[];prefixes={}
    for r in cold:
        path=args.run_dir/'traces'/r['task_id']/Path(r['trace']).name
        commands=split_commands(path.read_text());k=leading_options(commands)
        group=hashlib.sha256('\n'.join(commands[:k]).encode()).hexdigest()
        n=config['groups'][group]['prefix_commands'];prefix=commands[:n]
        if group in prefixes and prefixes[group]!=prefix:raise ValueError('prefix differs')
        prefixes[group]=prefix
        depth=sum(int_arg(c)*(1 if command_head(c)=='push' else -1) for c in commands if command_head(c) in ('push','pop'))
        jobs.append(dict(original=r,group=group,suffix=commands[n:],depth=depth))
    metadata=dict(targets=sorted(targets),z3_sha256=hashlib.sha256(Path(args.z3).read_bytes()).hexdigest(),settings={k:str(v) for k,v in vars(args).items()})
    (args.out/'config.json').write_text(json.dumps(metadata,indent=1)+'\n');records=[]
    for rep in range(args.repeat):
        for mode in ['isolated_prefix','recorded_history']:
            pool={}
            try:
                for j in jobs:
                    r=j['original'];target=r['trace'] in targets
                    if mode=='isolated_prefix' and not target:continue
                    g=j['group'];key=r['trace'] if mode=='isolated_prefix' else g
                    if key not in pool:
                        s=Session(args.z3,args.cores);pool[key]=s
                        out,err=s.call('\n'.join(prefixes[g]));decisions(out)
                        if err:raise RuntimeError(err)
                    suffix=[]
                    for c in j['suffix']:
                        suffix.append(c)
                        if target and command_head(c)=='check-sat':suffix.append('(get-info :reason-unknown)')
                    start=time.perf_counter()
                    out,err=pool[key].call('(push 1)\n'+'\n'.join(suffix)+f'\n(pop {j["depth"]+1})')
                    if err:raise RuntimeError(err)
                    statuses=decisions(out)
                    record=dict(mode=mode,repeat=rep,trace=r['trace'],task_id=r['task_id'],target=target,
                                seconds=time.perf_counter()-start,statuses=statuses,
                                cold_statuses=r['statuses'],original_pool_statuses=pool_status[r['trace']],
                                matches_cold=statuses==r['statuses'],matches_original_pool=statuses==pool_status[r['trace']])
                    if target:record['output']=out
                    records.append(record)
                    with (args.out/'sessions.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
                    if mode=='isolated_prefix':pool.pop(key).close()
            finally:
                for s in pool.values():s.close()
            print(mode,rep,[(r['task_id'],r['statuses']) for r in records if r['target'] and r['mode']==mode and r['repeat']==rep],flush=True)
    (args.out/'records.json').write_text(json.dumps(records,indent=1)+'\n')


if __name__=='__main__':main()
