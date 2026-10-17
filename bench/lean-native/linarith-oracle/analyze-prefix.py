"""Recompute source-associated native-prefix occurrence counts; no execution speed claim."""
from pathlib import Path
import collections, gzip, json, re
R=Path('/workspaces/repository')
A=R/'artifacts/linarith-oracle-2026-10-17/prefix-opportunity'
def account(sequences):
    trie={};occurrences=nodes=0;byte_occurrences=byte_nodes=0
    for seq in sequences:
        node=trie
        for edge in seq:
            occurrences+=1;byte_occurrences+=len(edge.encode())
            if edge not in node:
                node[edge]={};nodes+=1;byte_nodes+=len(edge.encode())
            node=node[edge]
    return {'occurrences':occurrences,'unique_nodes':nodes,'reusable':occurrences-nodes,
            'reusable_fraction':(occurrences-nodes)/occurrences if occurrences else 0,
            'bytes':byte_occurrences,'unique_bytes':byte_nodes}
def main():
    with gzip.open(A/'native-units.jsonl.gz','rt') as f:
        native={x['proposalId']:x for x in map(json.loads,f)}
    result={}
    for ds in ['minif2f','proofnet']:
        with gzip.open(A/(ds+'-input.jsonl.gz'),'rt') as f:rows=list(map(json.loads,f))
        groups=collections.defaultdict(lambda:{'exact':[],'unit':[]})
        fallback=collections.Counter();eligible=0
        for i,row in enumerate(rows):
            assert row['index']==i
            m=re.search(r':=\s*by\b',row['code'])
            if not m:fallback['no by delimiter']+=1;continue
            ans=native[ds+'-'+str(i)]
            if not ans['eligible']:fallback['native parse/syntax fallback']+=1;continue
            source=row['code'][m.end():].split('```',1)[0].encode()
            previous=0;edges=[]
            for unit in ans['units']:
                start=unit['startByte'];stop=unit['stopByte']
                assert source[start:stop].decode()==unit['text']
                edges.append(source[previous:stop].decode());previous=stop
            group=groups[(i//32,row['code'][:m.end()])]
            group['exact'].append(edges)
            group['unit'].append([u['text'] for u in ans['units']]);eligible+=1
        modes={}
        for mode in ['exact','unit']:
            sums=collections.Counter()
            for group in groups.values():
                a=account(group[mode])
                sums.update({k:v for k,v in a.items() if k!='reusable_fraction'})
            modes[mode]={**dict(sums),'reusable_fraction':sums['reusable']/sums['occurrences']}
        result[ds]={'population':len(rows),'eligible':eligible,'fallbacks':dict(fallback),
                    'statement_specific_groups':len(groups),'modes':modes}
    (A/'recomputed-counts.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
