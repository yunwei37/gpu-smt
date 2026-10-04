import os,subprocess,time,json,sys
BASE="/tmp/lean-kernel-arena"
K=BASE+"/_build/checkers/official/src/.lake/build/bin/kernel"
SRC=BASE+"/_build/tests/init.ndjson"
OUT="/tmp/prefix"; os.makedirs(OUT,exist_ok=True)
DECL=b'{"inductive"'; KEYS=(b'{"inductive"',b'{"def"',b'{"thm"',b'{"opaque"',b'{"axiom"',b'{"quot"')
# 1. collect byte offsets of decl lines
offs=[]; pos=0
with open(SRC,'rb') as f:
    for line in f:
        if line.startswith(KEYS): offs.append(pos+len(line))
        pos+=len(line)
total=pos
print("decls",len(offs),"bytes",total,flush=True)
N=12
cuts=[offs[min(len(offs)-1, (i+1)*len(offs)//N -1)] for i in range(N)]
cuts[-1]=total
# 2. write prefix files
with open(SRC,'rb') as f:
    data=f.read()
for i,c in enumerate(cuts):
    open(f"{OUT}/p{i:02d}.ndjson","wb").write(data[:c])
# 3. time each prefix (isolated cores 8-15)
rows=[]
import re
for i,c in enumerate(cuts):
    f=f"{OUT}/p{i:02d}.ndjson"
    n_decl=sum(1 for o in offs if o<=c)
    t0=time.time()
    r=subprocess.run(["taskset","-c","8-15","/usr/bin/time","-f","%e %U %M",K,f],capture_output=True,text=True)
    wall=time.time()-t0
    m=re.search(r"([\d.]+) ([\d.]+) (\d+)\s*$", r.stderr.strip())
    rows.append(dict(i=i,decls=n_decl,wall=float(m.group(1)),user=float(m.group(2)),rss_mb=int(m.group(3))/1024,ok=r.returncode==0))
    print(json.dumps(rows[-1]),flush=True)
json.dump(rows,open("/tmp/prefix_split.json","w"),indent=1)
print("DONE")
