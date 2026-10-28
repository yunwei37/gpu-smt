import gzip,importlib.util,json
from pathlib import Path
a=Path(__file__).resolve().parent
r=next(p for p in a.parents if (p/'Cargo.toml').exists())
s=importlib.util.spec_from_file_location('cmp',r/'bench/lean-warm-resource/compare.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
old=m.read_point(a.parent/'warm-resource-qualification-20261028T044624Z')
cap=json.loads(gzip.decompress((a/'engine.stdout.gz').read_bytes()))
assert json.loads((a/'terminal.json').read_text())['state']=='timely-reply24-complete'
computed=m.compare({**old,'engine':cap,'engine_exit':json.loads((a/'engine-exit.json').read_text())})
saved=json.loads((a/'comparison.json').read_text())
assert all(saved[k]==v for k,v in computed.items())
print(json.dumps({'paired_fields_exact':True,'native_candidates_executed':0}))
