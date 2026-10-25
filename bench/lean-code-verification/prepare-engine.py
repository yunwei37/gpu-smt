"""Preserve original Verina reference source bytes in the Rust Batch input."""
import argparse,gzip,json
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    with gzip.open(args.input,'rt',encoding='utf8') as stream:
        rows=[json.loads(line)for line in stream]
    sources=sorted((row for row in rows if row['path'].startswith('datasets/verina/')
        and row['path'].endswith('/task.lean')),key=lambda row:row['path'])
    assert len(sources)==189
    assert {row['repository']for row in sources}=={'sunblaze-ucb/verina'}
    assert {row['commit']for row in sources}=={'66b3ce5014edafb20cb26b87c681e7f31847249f'}
    candidates=[dict(id=Path(row['path']).parent.name,task_id=None,code=row['text'],
        timeout_ms=120000,reuse=False)for row in sources]
    assert len({row['id']for row in candidates})==189
    args.out.mkdir(exist_ok=False)
    with gzip.open(args.out/'all.json.gz','xt',encoding='utf8') as stream:
        json.dump(dict(mode='all',candidates=candidates),stream,ensure_ascii=False)
        stream.write('\n')
    manifest=[{key:row[key]for key in ['repository','commit','path']}for row in sources]
    (args.out/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (args.out/'README.md').write_text("""# Original Verina engine inputs

All189official reference task.lean files at66b3ce5014edafb20cb26b87c681e7f31847249f.
Source text/order,ID and repository-relative filename mapping retained; no
sorry/admit/error removal. Batch all-mode,120s original synchronous timeout,
reuse=false. No task competition, cached zero-time proof or filename rewrite
inside the source. No native verifier/model/solver runs during preparation.

Use the NativeLean backend with exact4.18.0/Mathlibaa936c36 context. Stdin source
has a different diagnostic filename than original-path CLI; path-dependent code
requires explicit same-context differential qualification before full pairing.
The source manifest retains original filenames; it does not make stdin path
semantics identical.139admitted stubs and4API errors stay in the population.
Old results remain historical; do not mix old24GiB/2worker clocks with new
dynamic48GiB/four eligible cores. Do not start another native acquisition while
the existing sole original7808group is alive. Preparation is not a performance
result, proof completeness claim or reproduction of another prover system.
""")
    print(json.dumps(dict(candidates=len(candidates),source_bytes=sum(len(c['code'].encode())
        for c in candidates),source_changed=False,new_native_executions=0)))

if __name__=='__main__':
    main()
