#!/usr/bin/env python3
"""Recompute AutoVerus direct-condition tail concentration from retained native receipts."""
import argparse, collections, csv, gzip, json, math, pathlib
def analyze(cells):
    groups=collections.defaultdict(list)
    for cell in cells:
        if cell['condition']=='direct':
            groups[cell['repetition']].append(cell)
    output=[]
    for repeat,rows in sorted(groups.items()):
        assert len(rows)==3566 and len({r['candidate'] for r in rows})==3566
        assert all(r['complete'] and r['external_wall_s']>=0 for r in rows)
        times=sorted((r['external_wall_s'] for r in rows),reverse=True)
        top=math.ceil(.016*len(rows));denominator=sum(times)
        rc=collections.Counter(r['returncode'] for r in rows)
        output.append(dict(dataset='AutoVerus',condition='direct',repeat=repeat,candidates=len(rows),
                           tail_fraction_requested=.016,tail_candidates=top,
                           sum_candidate_process_wall_s=denominator,tail_process_wall_s=sum(times[:top]),
                           tail_share=sum(times[:top])/denominator,timed_out=sum(bool(r['timed_out']) for r in rows),
                           exit_0=rc[0],exit_1=rc[1],exit_101=rc[101],
                           denominator='sum of separate native candidate process elapsed times; not batch wall or generation'))
    return output
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cells',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
    with gzip.open(a.cells,'rt') as f:rows=analyze(json.load(f))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
