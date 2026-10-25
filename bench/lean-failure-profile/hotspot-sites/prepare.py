"""Prepare exact-source simp_all diagnostics from retained native Syntax spans.

No candidate execution. Original, added-import control and profiling variant
remain separate; no interval program is rewritten and no failure rule is used.
"""
import argparse, collections, gzip, json
from pathlib import Path

def write_json_gz(path, value):
    path.write_bytes(gzip.compress((json.dumps(value,ensure_ascii=False)+'\n').encode(),mtime=0))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inputs',type=Path,required=True)
    p.add_argument('--sites',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    original=json.loads(gzip.decompress(args.inputs.read_bytes()))
    parsed=json.loads(args.sites.read_text())
    codes={row['id']:row for row in original}
    assert len(codes)==len(original)==len(parsed)
    assert {row['id']for row in parsed}==set(codes)
    args.out.mkdir(exist_ok=False)
    counts=collections.defaultdict(collections.Counter)
    batches={name:[]for name in ['original','import-control','profile']}
    manifest=[];unsupported=[]
    header_addition=b'\nimport SimpAllProfile\n\n'
    prefix=b'profile_simp_all '
    for row in parsed:
        source=codes[row['id']]
        group=source['hotspot_group']
        counts[group]['sources']+=1
        counts[group]['parse_errors']+=bool(row['parse_errors'])
        assert row['candidate_elaborated']is False
        raw=source['code'].encode()
        for site in row['sites']:
            begin,end=site['start_byte'],site['end_byte']
            assert 0<=begin<=end<=len(raw)
            assert raw[begin:end]==site['text'].encode()
            counts[group][site['kind']]+=1
        if group!='simp_all':continue
        if row['parse_errors']:
            unsupported.append(dict(id=row['id'],reason='native parse error',
                                    messages=row['messages']))
            continue
        positions=sorted({s['start_byte']for s in row['sites']
                         if s['kind']=='Lean.Parser.Tactic.simpAll'})
        assert positions and len(positions)==sum(
            s['kind']=='Lean.Parser.Tactic.simpAll'for s in row['sites'])
        header=row['header_end_byte']
        assert 0<=header<=min(positions)
        control=raw[:header]+header_addition+raw[header:]
        modified=control
        for position in reversed(positions):
            assert raw[position:position+8]==b'simp_all'
            offset=position+len(header_addition)
            modified=modified[:offset]+prefix+modified[offset:]
        # An inverse-by-recorded-edits check establishes byte preservation,
        # not semantic equivalence of the instrumentation.
        restored=modified
        mapping=[]
        for rank,position in reversed(list(enumerate(positions))):
            offset=position+len(header_addition)+rank*len(prefix)
            assert restored[offset:offset+len(prefix)]==prefix
            mapping.append(dict(original_byte=position,
                instrumented_keyword_byte=offset+len(prefix),
                instrumented_wrapper_byte=offset))
            restored=restored[:offset]+restored[offset+len(prefix):]
        assert restored==control
        assert control[:header]+control[header+len(header_addition):]==raw
        for name,body in [('original',raw),('import-control',control),('profile',modified)]:
            batches[name].append(dict(id=source['id'],task_id=source.get('task_id'),
                                      code=body.decode(),reuse=False))
        manifest.append(dict(id=source['id'],group=group,
            original_bytes=len(raw),original_sites=len(positions),
            native_prefix_commands=row['native_prefix_commands'],
            unelaborated_command_kinds=[k for k in row['command_kinds']
                if k!='Lean.Parser.Command.open'],
            inserted_import_at_original_byte=header,
            inserted_import=header_addition.decode(),
            inserted_tactic_prefix=prefix.decode(),
            sites=sorted(mapping,key=lambda m:m['original_byte'])))
    for name,candidates in batches.items():
        write_json_gz(args.out/(name+'.json.gz'),dict(mode='all',candidates=candidates))
    report=dict(original_timeout_sources=71,
        groups={k:dict(v)for k,v in counts.items()},prepared_simp_sources=len(manifest),
        prepared_simp_sites=sum(x['original_sites']for x in manifest),
        unsupported=unsupported,manifest=manifest,native_verification_runs=0,
        semantic_equivalence_claim=False,scope='native syntax and exact byte edits only')
    (args.out/'preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (args.out/'run-source.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps({k:v for k,v in report.items()if k not in ['manifest','groups']}))

if __name__=='__main__':main()
