import subprocess, glob, time, concurrent.futures as cf
K="_build/checkers/official/src/.lake/build/bin/kernel"
CORES="8-23"   # avoid cores 0-7 used by the isolated stage-split run
tut=sorted(glob.glob("_build/tests/tutorial/*/*.ndjson"))
small=sorted(glob.glob("_build/tests/other/*.ndjson")+glob.glob("_build/tests/bugs/*.ndjson")+glob.glob("_build/tests/corner-cases/*.ndjson"))
perf=sorted(glob.glob("_build/tests/perf/*.ndjson"))
def run(files,w):
    t0=time.time()
    with cf.ThreadPoolExecutor(max_workers=w) as ex:
        rs=list(ex.map(lambda f: subprocess.run(["taskset","-c",CORES,K,f],capture_output=True), files))
    return time.time()-t0, sum(1 for r in rs if b"Accepted" in r.stdout)
batch=small*10
for name,files in [("tutorial141",tut),("small460",batch),("perf28",perf)]:
    print("==",name,"n=%d"%len(files),"==")
    for w in [1,4,8,16]:
        dt,ok=run(files,w); print(f"  workers={w:3d} wall={dt:7.3f}s accepted={ok}")
