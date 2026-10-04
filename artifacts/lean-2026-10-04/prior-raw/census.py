import mmap,json,collections,sys
p='/tmp/lean-kernel-arena/_build/tests/mathlib.ndjson'
c=collections.Counter()
with open(p,'rb') as f:
    m=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
    n=0
    for line in iter(m.readline,b''):
        n+=1
        if line[:1]==b'{':
            try: k=next(iter(json.loads(line)))
            except Exception: k='?'
            if k in ('def','thm','inductive','opaque','axiom','quot'): c[k]+=1
print('mathlib lines',n,'decls',sum(c.values()),dict(c))
