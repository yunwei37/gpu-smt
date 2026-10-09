#!/usr/bin/env python3
"""Recompute native response identity and completeness from authoritative raw files."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from analyze_smt_trace import split_commands


def digest(data):
    return hashlib.sha256(data).hexdigest()


def raw_path(root, value):
    path = Path(value)
    if not path.is_absolute():
        return root / path
    # Older runs used absolute output paths; their last two components are native.
    relocated = root / path.parent.name / path.name
    return relocated if relocated.exists() else path


def observe(path, job):
    data = path.read_bytes()
    matches = list(re.finditer(rb'^<<DONE>>[ \t]*\r?\n|^<<DONE>>[ \t]*\r?$', data, re.M))
    frames = []
    start = 0
    for match in matches:
        frames.append((start, match.start(), data[start:match.start()]))
        start = match.end()
    responses = []
    for i, request in enumerate(job['responses']):
        present = i < len(frames)
        offset, end, block = frames[i] if present else (None, None, b'')
        text = block.decode('utf-8', errors='replace')
        parsed = split_commands(text)
        errors = [b for b in parsed if b.lstrip().startswith('(error')]
        # A complete single list/model response, not merely a nonempty frame.
        model = (present and len(parsed) == 1 and not errors and
                 text.strip() == parsed[0].strip() and
                 (parsed[0].strip() in ('()', '(model)') or
                  bool(re.match(r'^\(\s*(?:\(\s*define-fun(?:-rec)?\b|model(?:\s|\)))', parsed[0]))))
        responses.append(dict(request_index=i, command_index=request['command_index'], head=request['head'],
                              statistics=':all-statistics' in request['command'], present=present,
                              nonempty=present and bool(block.strip()),
                              check_decision=text.strip() if request['head'] in ('check-sat', 'check-sat-assuming') and text.strip() in ('sat', 'unsat', 'unknown') else None,
                              byte_start=offset, byte_end=end, sha256=digest(block) if present else None,
                              errors=errors, model_available=model if request['head']=='get-model' else None,
                              model_sha256=digest(block) if model and request['head']=='get-model' else None))
    text = data.decode('utf-8', errors='replace')
    return dict(stdout_sha256=digest(data), decisions=re.findall(r'^(sat|unsat|unknown)\s*$', text,re.M),
                errors=[b for b in split_commands(text) if b.lstrip().startswith('(error')],
                response_frames=responses, expected_frames=len(job['responses']), actual_frames=len(frames),
                complete_response_frames=len(frames)==len(job['responses']) and not data[start:].strip() and all(r['nonempty'] for r in responses),
                extra_frames=[dict(byte_start=s, byte_end=e, sha256=digest(b)) for s,e,b in frames[len(job['responses']):]],
                trailing_output=data[start:].decode('utf-8',errors='replace'),
                complete_checks=len(re.findall(r'^(sat|unsat|unknown)\s*$',text,re.M))==len(job['checks']) and all(r['check_decision'] is not None for r in responses if r['head'] in ('check-sat', 'check-sat-assuming')))


def compare(obs, ref):
    if ref is None:
        return dict(reference_missing=True)
    pairs=[]
    for f,r in zip(obs['response_frames'],ref['response_frames']):
        pairs.append(dict(command_index=f['command_index'], statistics=f['statistics'],
                          exact_equal=f['present'] and r['present'] and f['sha256']==r['sha256'],
                          model_availability_equal=f['model_available']==r['model_available']))
    return dict(reference_missing=False, decisions_equal=obs['decisions']==ref['decisions'],
                stdout_bytes_equal=obs['stdout_sha256']==ref['stdout_sha256'], response_comparison=pairs,
                nonstatistics_exact_equal=obs['complete_response_frames'] and ref['complete_response_frames'] and
                len(pairs)==len(obs['response_frames'])==len(ref['response_frames']) and
                all(p['exact_equal'] for p in pairs if not p['statistics']))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('out',type=Path)
    a=p.parse_args()
    root=a.out.resolve()
    job_list=json.loads((root/'jobs.json').read_text())
    jobs={j['index']:j for j in job_list}
    provenance=json.loads((root/'provenance.json').read_text())
    rows=[json.loads(s) for s in (root/'processes.jsonl').read_text().splitlines()]
    repetitions=provenance.get('repetitions')
    if repetitions is None:
        argv=provenance.get('argv',[])
        repetitions=int(argv[argv.index('--repeat')+1]) if '--repeat' in argv else 3
    expected={(r,m,i) for r in range(repetitions) for m in ('release','source','lazy','eager') for i in jobs}
    counts=Counter((r['repeat'],r['mode'],r['index']) for r in rows)
    observations=[]
    by_key={}
    for row in rows:
        key=(row['repeat'],row['mode'],row['index'])
        obs=dict(row)
        if 'input' in obs:
            input_path=Path(obs['input'])
            obs['input']=str(Path('inputs') / input_path.name) if input_path.is_absolute() else str(input_path)
        job=jobs.get(row['index'])
        try:
            if job is None: raise ValueError('unexpected original index')
            path=raw_path(root,row['stdout'])
            obs.update(observe(path,job))
            stderr=raw_path(root,row['stderr']).read_bytes()
            obs.update(stdout=str(path.relative_to(root)),stderr=str(raw_path(root,row['stderr']).relative_to(root)),stderr_text=stderr.decode('utf-8',errors='replace'),stderr_sha256=digest(stderr),check_command_indices=job['checks'])
        except (OSError,ValueError) as exc:
            obs['analysis_error']=str(exc)
        observations.append(obs)
        if counts[key]==1 and 'analysis_error' not in obs:
            by_key[key]=obs
    for obs in observations:
        if 'analysis_error' in obs: continue
        r,m,i=obs['repeat'],obs['mode'],obs['index']
        refs=['release','source'] + (['lazy'] if m=='eager' else [])
        obs['comparisons']={ref:compare(obs,by_key.get((r,ref,i))) for ref in refs}
    completion_path=root/'completion.json'
    completion=json.loads(completion_path.read_text()) if completion_path.exists() else None
    summary=dict(declared_repetitions=repetitions, expected_processes=len(expected),actual_processes=len(rows),
                 duplicate_jobs=[i for i,n in Counter(j['index'] for j in job_list).items() if n>1],
                 duplicate_cells=[list(k) for k,n in counts.items() if n>1],
                 missing_cells=[list(k) for k in sorted(expected-set(counts))],unexpected_cells=[list(k) for k in sorted(set(counts)-expected)],
                 completion=completion, incomplete_frames=[ [o['repeat'],o['mode'],o['index']] for o in observations if not o.get('complete_response_frames',False)],
                 nonzero_exits=[[o['repeat'],o['mode'],o['index'],o['returncode']] for o in observations if o['returncode']])
    summary['matrix_complete']=not any(summary[k] for k in ('duplicate_jobs','duplicate_cells','missing_cells','unexpected_cells')) and len(rows)==len(expected)
    summary['terminal_complete']=summary['matrix_complete'] and completion is not None and completion.get('terminal') is True and completion.get('completed_processes')==len(expected) and completion.get('repetitions')==repetitions
    (root/'analysis.json').write_text(json.dumps(observations,indent=2)+'\n')
    (root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
