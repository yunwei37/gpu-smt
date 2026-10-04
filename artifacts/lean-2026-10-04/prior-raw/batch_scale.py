import subprocess, glob, os, time, sys, resource
KERNEL = "_build/checkers/official/src/.lake/build/bin/kernel"
jobs = sorted(glob.glob("_build/tests/bugs/*.ndjson") + glob.glob("_build/tests/corner-cases/*.ndjson") + glob.glob("_build/tests/other/*.ndjson"))
cores = "0-23"
def run(workers):
    # serial-ish batches: pool of `workers` concurrent processes
    import concurrent.futures as cf
    t0=time.time()
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(lambda f: subprocess.run(["taskset","-c",cores,KERNEL,f], capture_output=True), jobs))
    return time.time()-t0
for w in [1,2,4,8,12,16,24]:
    dt=run(w)
    print(f"workers={w:3d} jobs={len(jobs)} wall={dt:7.3f}s  decl_rate_jobs/s={len(jobs)/dt:6.1f}")
