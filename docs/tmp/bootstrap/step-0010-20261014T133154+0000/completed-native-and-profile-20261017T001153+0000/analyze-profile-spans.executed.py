from pathlib import Path
import json,gzip,zipfile,statistics
r=Path('/workspaces/repository');out=Path(__file__).resolve().parent
info=json.loads((out/'profile-reconstruction.json').read_text())
for x,directory in zip(info,['full-gc2','farkas-fast427-full1']):
 label=x['label'];spans=[]
 with zipfile.ZipFile(r/'artifacts/lean-modern-native-compilation-2026-10-14'/directory/(label+'.zip')) as z:
  with gzip.GzipFile(fileobj=z.open(label+'/resources.jsonl.gz')) as f:
   for line in f:
    row=json.loads(line);spans.append((row['observation_end_ns']-row['monotonic_ns'])/1e9)
 x['observed_scan_wall_span_seconds']={'median':statistics.median(spans),'sum':sum(spans),'max':max(spans),'scope':'Actual monotonic before/after non-atomic sample; wall scheduling/read span, not observer CPU or isolated slowdown.'}
(out/'profile-reconstruction.json').write_text(json.dumps(info,indent=2)+'\n')
p=Path('/tmp/gpu-smt-e038-full-native-batch-20261016T150428Z/original-input.jsonl.gz')
with gzip.open(p,'rb') as f:assert f.read()==(r/'artifacts/lean-modern-native-compilation-2026-10-14/input.jsonl').read_bytes()
print('Profile wall sample spans and exact native input archive equality reconstructed.')
