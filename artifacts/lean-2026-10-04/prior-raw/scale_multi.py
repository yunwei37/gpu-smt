import subprocess, glob, time, concurrent.futures as cf
K="_build/checkers/official/src/.lake/build/bin/kernel"
tut=sorted(glob.glob("_build/tests/tutorial/*/*.ndjson"))
small=sorted(glob.glob("_build/tests/other/*.ndjson")+glob.glob("_build/tests/bugs/*.ndjson")+glob.glob("_build/tests/corner-cases/*.ndjson"))
def run(files,w,cores):
    t0=time.time()
    with cf.ThreadPoolExecutor(max_workers=w) as ex:
        rs=list(ex.map(lambda f: subprocess.run(["taskset","-c",cores,K,f],capture_output=True), files))
    return time.time()-t0, sum(1 for r in rs if b"Accepted" in r.stdout)
print("== tutorial 141 subtests (parse+check each; kernel startup dominates) ==")
for w in [1,4,8,16,24]:
    dt,ok=run(tut,w,"0-23"); print(f"  workers={w:3d} wall={dt:8.3f}s accepted={ok}")
print("== small correctness 46 files: repeated 10x ==")
batch=small*10
for w in [1,4,8,16,24]:
    dt,ok=run(batch,w,"0-23"); print(f"  workers={w:3d} wall={dt:8.3f}s accepted={ok}")
