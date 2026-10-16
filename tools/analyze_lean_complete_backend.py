"""Recompute complete-cell coverage and paired complete-source CPU comparisons."""
import argparse,collections,json,pathlib,statistics

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=pathlib.Path,required=True)
    p.add_argument('--out',type=pathlib.Path,required=True)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
    execution=json.loads((a.root/'execution.json').read_text())
    ncontexts=len(execution['contexts']);args=execution['arguments']
    modes=['native-full','external-prefix'];cells={};incomplete=[]
    conditions=[(f'rep{r}',m) for r in range(args['repetitions']) for m in modes]
    if args['profiles']:conditions += [('profile',m) for m in modes]
    for repeat,mode in conditions:
        for c in range(ncontexts):
            folder=a.root/f'{repeat}-ctx{c:02d}-{mode}'
            if not (folder/'terminal.json').exists() or not (folder/'analysis.json').exists():
                incomplete.append(folder.name);continue
            terminal=json.loads((folder/'terminal.json').read_text());analysis=json.loads((folder/'analysis.json').read_text())
            rows=[json.loads(x) for x in (folder/'inputs.jsonl').read_text().splitlines()]
            records=[json.loads(x) for x in (folder/'stdout.jsonl').read_text().splitlines()]
            jobs=[x for x in records if 'index' in x]
            if terminal['returncode']!=0 or [x['index'] for x in jobs]!=[x['index'] for x in rows] or records[-1].get('finished')!=len(rows):
                incomplete.append(folder.name);continue
            counters=collections.Counter();projected=[]
            archive=sum(int(x.get('preparation_archive_ns',0)) for x in records)
            durations=[];fallbacks=0;cache_hits=0
            by_index={x['index']:x for x in rows}
            for job in jobs:
                r=job['result'];code=r['backend_code']
                outcome=('operational' if code==3 else 'accepted' if r['accepted'] else
                    'rejected' if r['has_errors'] or code==1 else 'incomplete' if r['has_sorry'] else 'unknown')
                counters[outcome]+=1;fallbacks+=bool(r['fallback']);cache_hits+=bool(job['cached'])
                projected.append({'index':job['index'],'outcome':outcome,'source_sha256':by_index[job['index']]['source_sha256']})
                if not job['cached']:archive+=int(r.get('archive_ns',0))
                durations.append(int(job['elapsed_ns'])/1e9)
            if projected!=analysis['candidate_rows']:raise RuntimeError('derived projection differs from raw: '+folder.name)
            info={'cell':folder.name,'base':terminal['base'],'repeat':repeat,'method':mode,
                  'seconds':terminal['whole_seconds'],'attempts':len(rows),'outcomes':dict(counters),
                  'archive_seconds':archive/1e9,'cache_hits':cache_hits,'fallbacks':fallbacks,
                  'serial_candidate_elapsed_seconds':durations,'candidate_rows':projected}
            if (folder/'resources-summary.json').exists():info['resources']=json.loads((folder/'resources-summary.json').read_text())
            cells[(repeat,mode,c)]=info
    complete_conditions=[];pairs=[]
    for repeat,mode in conditions:
        selected=[cells.get((repeat,mode,c)) for c in range(ncontexts)]
        if any(x is None for x in selected):continue
        seconds=sum(x['seconds'] for x in selected);attempts=sum(x['attempts'] for x in selected)
        if attempts!=execution['attempts_per_condition']:raise RuntimeError('complete population count differs')
        complete_conditions.append({'repeat':repeat,'method':mode,'context_process_seconds':seconds,
            'attempts':attempts,'attempts_per_second':attempts/seconds,
            'archive_seconds':sum(x['archive_seconds'] for x in selected),
            'scope':'sum of all sequential context-process start-to-exit elapsed; driver preprocessing/inter-cell analysis excluded'})
    for r in range(args['repetitions']):
        repeat=f'rep{r}'
        if not all((repeat,m,c) in cells for m in modes for c in range(ncontexts)):continue
        mismatches=[]
        for c in range(ncontexts):
            left=cells[(repeat,modes[0],c)]['candidate_rows'];right=cells[(repeat,modes[1],c)]['candidate_rows']
            if len(left)!=len(right):raise RuntimeError('paired population differs')
            mismatches.extend({'base':execution['contexts'][c],'native':l,'external':r} for l,r in zip(left,right) if l!=r)
        native=sum(cells[(repeat,modes[0],c)]['seconds'] for c in range(ncontexts))
        external=sum(cells[(repeat,modes[1],c)]['seconds'] for c in range(ncontexts))
        archive=sum(cells[(repeat,modes[1],c)]['archive_seconds'] for c in range(ncontexts))
        pairs.append({'repeat':repeat,'native_seconds':native,'external_seconds':external,
            'external_over_native':external/native,'basic_mismatches':mismatches,
            'external_archive_seconds':archive,
            'optimistic_archive_removed_external_seconds':external-archive,
            'optimistic_bound_scope':'explicitly timed synchronous collection pauses removed; not observed production speed'})
    summary={'expected_context_cells':len(conditions)*ncontexts,'complete_context_cells':len(cells),
        'incomplete_or_missing_cells':incomplete,'complete_whole_conditions':complete_conditions,'complete_primary_pairs':pairs,
        'full_declared_scope_complete':not incomplete,
        'limitations':['basic outcomes do not prove mathematical equivalence','partial cells do not yield whole throughput',
                      'archive-inclusive observed costs are not automatically production cost','three pairs describe variation, not general statistical significance',
                      'CPU comparison contains no device execution/GPU conclusion']}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (a.out/'complete-cell-data.json').write_text(json.dumps(list(cells.values()),indent=2)+'\n')
    print(json.dumps({'complete_context_cells':len(cells),'expected_context_cells':len(conditions)*ncontexts,'complete_whole_pairs':len(pairs)}))

if __name__=='__main__':main()
