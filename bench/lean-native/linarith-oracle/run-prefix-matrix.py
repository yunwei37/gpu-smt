"""Continue the two original formal prefix populations after real timeout qualification."""
from pathlib import Path
import json, os, select, subprocess, sys
R=Path('/workspaces/repository')
U=Path('/tmp/gpu-smt-linarith-oracle-20261017/prefix')
def main():
    pid=int(sys.argv[1])
    path=U/'timeout-repair-real-preflight/batch/terminal.json'
    if not path.exists():
        fd=os.pidfd_open(pid)
        try:select.select([fd],[],[])
        finally:os.close(fd)
    t=json.loads(path.read_text())
    if t['state']!='complete' or t['returned']!=8:
        raise RuntimeError('real timeout/successor qualification incomplete; preserve raw outputs')
    for ds in ['minif2f','proofnet']:
        cmd=['python3',str(R/'bench/lean-native/linarith-oracle/run-prefix.py'),
             '--out',str(U/('full-recovered-'+ds)),'--dataset',ds]
        with (U/(ds+'-full-recovered.log')).open('wb') as log:
            subprocess.run(cmd,cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
    print('Original populations complete; native verdict/timing result review required.',flush=True)
if __name__=='__main__':main()
