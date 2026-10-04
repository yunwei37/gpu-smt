import subprocess, glob, time, concurrent.futures as cf
K="_build/checkers/official/src/.lake/build/bin/kernel"
files=sorted(glob.glob("_build/tests/perf/*.ndjson"))
def run(w):
    t0=time.time()
    with cf.ThreadPoolExecutor(max_workers=w) as ex:
        rs=list(ex.map(lambda f: subprocess.run(["taskset","-c","0-23",K,f],capture_output=True), files))
    dt=time.time()-t0
    ok=sum(1 for r in rs if b"Accepted" in r.stdout)
    return dt, ok
# serial baseline = sum of individual IPv4 times
for w in [1,2,4,8,16,24]:
    dt,ok=run(w)
    print(f"perf-suite workers={w:3d} wall={dt:7.3f}s accepted={ok}/{len(files)}")
