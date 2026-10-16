from pathlib import Path
import subprocess,os,json,time,urllib.request,tarfile,concurrent.futures,re
r=Path('/workspaces/repository');p=Path('/tmp/gpu-smt-native-ref-branches-20261016');sdk=Path('/tmp/gpu-smt-goedel427-20261014/lean-4.27.0-linux')
e=r/'docs/tmp/bootstrap/step-0010-20261014T133154+0000/experiment-038';src=p/'lean4-4.27.0/src'
url='https://codeload.github.com/microsoft/mimalloc/tar.gz/refs/tags/v2.2.3'
archive=p/'mimalloc-v2.2.3.tar.gz'
if not archive.exists():urllib.request.urlretrieve(url,archive)
if not (p/'mimalloc-2.2.3').exists():
 with tarfile.open(archive) as tf:tf.extractall(p,filter='data')
(e/'mimalloc-source.json').write_text(json.dumps({'url':url,'bytes':archive.stat().st_size,'upstream_binding':'Lean4.27 CMakeLists.txt ExternalProject mimalloc GIT_TAG v2.2.3'},indent=2)+'\n')
common=[str(sdk/'bin/clang'),'-x','c++','-std=c++17','-O3','-fPIC','-ftls-model=initial-exec','-nostdinc','-nostdinc++','-isystem',str(p/'libcxx-19.1.7.src/include'),'-isystem',str(sdk/'include/clang'),'-isystem','/usr/include/x86_64-linux-gnu','-isystem','/usr/include','-DLEAN_MULTI_THREAD','-DLEAN_USE_GMP','-DLEAN_EXPORTING','-DNDEBUG','-I'+str(sdk/'include'),'-I'+str(src),'-I'+str(r/'bench/lean-native'),'-I'+str(p/'mimalloc-2.2.3/include')]
t=(src/'runtime/CMakeLists.txt').read_text().split(')')[0].split('set(RUNTIME_OBJS',1)[1]
sources=[src/'runtime'/f for f in t.split()]+[p/'mimalloc-2.2.3/src/static.c']
outdir=p/'runtime-shared';outdir.mkdir(exist_ok=True)
def compile(f):
 tag=f.name+'.o';cmd=common+(['-DMI_SHARED_LIB','-DMI_SHARED_LIB_EXPORT','-DMI_WIN_NOREDIRECT'] if f.name=='static.c' else [])+['-c',str(f),'-o',str(outdir/tag)]
 with (e/('shared-'+tag+'.stdout')).open('w') as out,(e/('shared-'+tag+'.stderr')).open('w') as err:z=subprocess.run(cmd,stdout=out,stderr=err)
 (e/('shared-'+tag+'.json')).write_text(json.dumps({'command':cmd,'exit_code':z.returncode},indent=2)+'\n')
 return {'source':str(f),'exit_code':z.returncode,'stderr_tail':(e/('shared-'+tag+'.stderr')).read_text()[-1200:] if z.returncode else ''}
with concurrent.futures.ThreadPoolExecutor() as pool:rows=list(pool.map(compile,sources))
(e/'shared-runtime-compile.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([x for x in rows if x['exit_code']],indent=2),flush=True)
if any(x['exit_code'] for x in rows):raise SystemExit(1)
cmd=[str(sdk/'bin/clang'),'-shared','-fuse-ld=lld','-o',str(p/'libleanshared.so'),'-Wl,-soname,libleanshared.so','-Wl,-Bsymbolic','-Wl,--whole-archive']+[str(sdk/'lib/lean'/x) for x in ['libLean.a','libStd.a','libInit.a','libleancpp.a']]+[str(x) for x in outdir.glob('*.o')]+['-Wl,--no-whole-archive','-L'+str(p),'-lgpu_smt_ref_branches','-L'+str(sdk/'lib'),'-Wl,-Bstatic','-lc++','-lc++abi','-lunwind','-lgmp','-luv','-Wl,-Bdynamic','-lpthread','-ldl','-lm','-lrt','-Wl,-rpath,'+str(p)]
with (e/'shared-runtime-link.stdout').open('w') as out,(e/'shared-runtime-link.stderr').open('w') as err:z=subprocess.run(cmd,stdout=out,stderr=err)
(e/'shared-runtime-link.json').write_text(json.dumps({'command':cmd,'exit_code':z.returncode},indent=2)+'\n')
print('link',z.returncode,(e/'shared-runtime-link.stderr').read_text()[-4000:])
