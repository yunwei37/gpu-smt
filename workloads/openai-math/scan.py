#!/usr/bin/env python3
"""Stream a pinned public archive into static source metrics, without extracting/building."""
import argparse, collections, csv, gzip, hashlib, heapq, json, pathlib, re, resource, tarfile, time, urllib.request
from inventory import project, write_csv
TOKENS = ("decide", "native_decide", "bv_decide", "ofReduceBool", "simp", "simp_all",
          "norm_num", "omega", "grind", "linarith", "nlinarith", "interval_cases", "aesop", "rfl")
SPECIAL = re.compile(r'/\-|--|"(?:\\.|[^"\\])*"', re.S)
IMPORT = re.compile(r'(?m)^[ \t]*(?:(?:public|private|meta)[ \t]+)*import[ \t]+([^\n;]+)')
COMMAND = re.compile(r"(?m)^(?P<indent>[ \t]*)(?:(?:private|protected|noncomputable|unsafe|partial|local|scoped)\s+)*(?P<kind>theorem|lemma|def|abbrev|instance|opaque|axiom|example|namespace|section|end|attribute|set_option|inductive|structure|class|variable|variables|open|export)\b")
DECL = re.compile(r"\s*([\w'.«»]+)")
def masks(text):
    """Erase nested comments, preserving strings; separately erase string literals."""
    pieces=[]; code=[]; pos=0
    def spaces(s): return re.sub(r'[^\n]', ' ', s)
    for_search=0
    while True:
        m=SPECIAL.search(text, for_search)
        if not m:
            pieces.append(text[pos:]); code.append(text[pos:]); break
        pieces.append(text[pos:m.start()]); code.append(text[pos:m.start()])
        token=m.group()
        if token.startswith('"'):
            pieces.append(token); code.append(spaces(token)); end=m.end()
        elif token=='--':
            end=text.find('\n',m.end())
            if end<0:end=len(text)
            blank=spaces(text[m.start():end]);pieces.append(blank);code.append(blank)
        else:
            end=m.end(); depth=1
            while depth:
                n=re.search(r'/\-|\-/',text[end:])
                if not n: raise ValueError("unterminated block comment")
                end += n.end();depth += 1 if n.group()=='/-' else -1
            blank=spaces(text[m.start():end]);pieces.append(blank);code.append(blank)
        pos=end;for_search=end
    return ''.join(pieces), ''.join(code)
def metrics(path, text):
    clean, code=masks(text)
    counts={key:len(re.findall(r'(?<![\w\'])'+key+r'(?![\w\'])',code)) for key in TOKENS}
    counts["decide_plus_kernel"]=len(re.findall(r'\bdecide\s*\+\s*kernel\b',code))
    imports=[]
    for m in IMPORT.finditer(code):
        imports.extend(x for x in re.findall(r"[A-Za-z_][\w'.]*",m.group(1)) if x not in ("all", "in"))
    commands=list(COMMAND.finditer(code));declarations=[]
    for index,m in enumerate(commands):
        if m["kind"] not in ("lemma","theorem"):continue
        name=DECL.match(code,m.end())
        if not name:continue
        indent=len(m["indent"].expandtabs(8))
        end=next((n.start() for n in commands[index+1:] if len(n["indent"].expandtabs(8))<=indent),len(text))
        block=clean[m.start():end].strip()
        # Comments become whitespace; exact remaining bytes, not alpha/semantic equivalence.
        declarations.append({"name":name[1],"kind":m["kind"],"offset":m.start(),
                             "fingerprint":hashlib.blake2b(block.encode(),digest_size=32).hexdigest(),
                             "bytes":len(block.encode()),"direct_ofReduceBool_reference":bool(re.search(r'\bofReduceBool\b',code[m.start():end])),
                             "native_decide_occurrences":len(re.findall(r'\bnative_decide\b',code[m.start():end]))})
    return counts,list(dict.fromkeys(imports)),declarations
class CountReader:
    def __init__(self,stream):self.stream=stream;self.count=0
    def read(self,n=-1):
        data=self.stream.read(n);self.count+=len(data);return data
def graph(profiles, edges, out, source_roots=("lean",)):
    def module(path):
        root=max((q for q in source_roots if path.startswith(q+"/")),key=len)
        return pathlib.PurePosixPath(path).relative_to(root).with_suffix('').as_posix().replace('/','.')
    modules={module(p):p for p in profiles}
    if len(modules)!=len(profiles):raise ValueError("Ambiguous source-root module identity")
    rename={pathlib.PurePosixPath(p).relative_to('lean').with_suffix('').as_posix().replace('/','.'):module(p) for p in profiles}
    edges={rename.get(m,m):v for m,v in edges.items()}
    deps={m:set() for m in modules};rev=collections.defaultdict(list);external=collections.Counter()
    for module,imports in edges.items():
        for dep in imports:
            if dep in modules:deps[module].add(dep)
            else:external[dep.split('.')[0]]+=1
    return modules,deps,external,edges
def analyze_graph(profiles, edges, out, source_roots=("lean",)):
    modules,deps,external,edges=graph(profiles,edges,out,source_roots)
    reverse=collections.defaultdict(list)
    for m,ds in deps.items():
        for d in ds:reverse[d].append(m)
    degree={m:len(d) for m,d in deps.items()}
    ready=collections.deque(sorted(m for m,n in degree.items() if n==0))
    depth={m:1 for m in ready};parent={};ordered=[]
    while ready:
        m=ready.popleft();ordered.append(m)
        for child in reverse[m]:
            if depth.get(child,1)<depth[m]+1:depth[child]=depth[m]+1;parent[child]=m
            degree[child]-=1
            if degree[child]==0:ready.append(child)
    cyclic=[m for m,n in degree.items() if n]
    waves=collections.Counter(depth[m] for m in ordered)
    path=[]
    if ordered:
        m=max(ordered,key=lambda x:depth[x])
        while True:
            path.append(m)
            if m not in parent:break
            m=parent[m]
        path.reverse()
    reachable=set();front=['OAI'] if 'OAI' in modules else []
    while front:
        m=front.pop()
        if m in reachable:continue
        reachable.add(m);front.extend(deps[m]-reachable)
    write_csv(out/'import-levels.csv',[{"level":k,"modules":v} for k,v in sorted(waves.items())])
    write_csv(out/'critical-import-path.csv',[{"position":i+1,"module":m,"path":modules[m]} for i,m in enumerate(path)])
    with gzip.open(out/'imports.csv.gz','wt',newline='') as f:
        w=csv.writer(f);w.writerow(['module','imports','internal'])
        for m,values in edges.items():
            for dep in values:w.writerow([m,dep,dep in modules])
    return {"source_roots":list(source_roots),"modules":len(modules),"internal_edges":sum(map(len,deps.values())),"external_root_occurrences":dict(external),
            "topologically_ordered":len(ordered),"cyclic_or_cycle_dependent_modules":len(cyclic),
            "unit_weight_longest_import_chain":len(path),"max_import_depth_wave_width":max(waves.values(),default=0),
            "OAI_root_reachable_modules":len(reachable),
            "OAI_root_reachable_source_bytes":sum(profiles[modules[m]]["bytes"] for m in reachable),
            "scope":"Source-import structural graph only; depth/width are not measured time or safe runtime parallelism. External dependency graph is excluded."}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--inventory',type=pathlib.Path,required=True)
    ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    info=json.loads((a.inventory/'inventory.json').read_text());pin=info["commit"]
    with gzip.open(a.inventory/'files.csv.gz','rt') as f:expected={x["path"]:x for x in csv.DictReader(f)}
    start=time.monotonic();profiles={};edges={};groups=collections.defaultdict(collections.Counter);dups=collections.defaultdict(list)
    decode_errors=[];parse_errors=[];state={"complete":False,"native_processes":0}
    url='https://codeload.github.com/openai/math/tar.gz/'+pin
    reader=None
    journal_buffer=[]
    journal_index=0
    def checkpoint():
        nonlocal journal_index
        if not journal_buffer:return
        folder=a.out/'journal';folder.mkdir(exist_ok=True)
        with gzip.open(folder/f'chunk-{journal_index:05d}.jsonl.gz','wt') as f:
            for item in journal_buffer:f.write(json.dumps(item)+'\n')
        journal_index+=1;journal_buffer.clear()
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"proofserve-static-audit"}),timeout=180) as response:
            reader=CountReader(response)
            with tarfile.open(fileobj=reader,mode='r|gz') as archive:
                for member in archive:
                    if not member.isfile():continue
                    path=member.name.partition('/')[2]
                    if path not in expected:continue
                    data=archive.extractfile(member).read()
                    if len(data)!=int(expected[path]["size"]):raise ValueError("source size mismatch: "+path)
                    try:text=data.decode('utf-8')
                    except UnicodeDecodeError:
                        decode_errors.append(path);continue
                    try:counts,imports,decls=metrics(path,text)
                    except ValueError as e:
                        parse_errors.append({"path":path,"error":str(e)});continue
                    group=expected[path]["project"];row={"path":path,"project":group,"bytes":len(data),**counts,"lemma_theorem_declarations":len(decls),"imports":len(imports)}
                    profiles[path]=row;edges[pathlib.PurePosixPath(path).relative_to('lean').with_suffix('').as_posix().replace('/','.')]=imports
                    journal_buffer.append({"profile":row,"imports":imports,"declarations":decls})
                    if len(journal_buffer)>=1000:checkpoint()
                    groups[group].update({**counts,"files":1,"source_bytes":len(data),"lemma_theorem_declarations":len(decls)})
                    for d in decls:dups[(d["fingerprint"],d["bytes"])].append({"path":path,"project":group,**d})
                    if len(profiles)%2000==0:
                        print(json.dumps({"files_scanned":len(profiles),"download_bytes":reader.count,"elapsed_s":time.monotonic()-start,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}),flush=True)
                        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>4_500_000:raise MemoryError("W approaches allocated 5GiB ceiling")
                    if len(profiles)==len(expected):break
        state["complete"]=not decode_errors and not parse_errors and len(profiles)==len(expected)
    finally:
        checkpoint()
        if profiles:write_csv(a.out/'file-metrics.csv.gz',list(profiles.values()))
        if groups:write_csv(a.out/'project-tactics.csv',[{"project":g,**dict(c)} for g,c in sorted(groups.items())])
        duplicate_rows=[]
        for (fingerprint,size),values in dups.items():
            if len({x["project"] for x in values})<2:continue
            for x in values:duplicate_rows.append(x)
        if duplicate_rows:write_csv(a.out/'cross-project-declaration-candidates.csv.gz',duplicate_rows)
        state.update({"commit":pin,"files_expected":len(expected),"files_scanned":len(profiles),"source_bytes_scanned":sum(x["bytes"] for x in profiles.values()),
                      "token_occurrences":dict(sum(groups.values(),collections.Counter())),"decode_errors":decode_errors,"lexical_errors":parse_errors,
                      "cross_project_exact_comment_masked_declaration_fingerprint_groups":len({x["fingerprint"] for x in duplicate_rows}),
                      "cross_project_declaration_occurrences":len(duplicate_rows),"elapsed_s":time.monotonic()-start,
                      "archive_transfer_bytes":reader.count if reader else None,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "ofReduceBool_axiom_dependency_theorem_count":None,
                      "limitations":["Lexical token occurrences outside comments/strings are not tactic executions.",
                                     "Declaration boundaries are source candidates, not elaborated identity or safe reuse.",
                                     "ofReduceBool transitive kernel-axiom dependence requires compiled #print axioms; not inferred from source names.",
                                     "No source/compiler wall times, timeout reasons or 1.6%/73% tail claim established."]})
        if state["complete"]:
            lake=json.loads((a.inventory/'upstream-metadata.json').read_text())['lean/lakefile.lean']
            roots=["lean"]+["lean/"+q for q in re.findall(r'srcDir\s*:=\s*"([^"]+)"',lake)]
            state["import_graph"]=analyze_graph(profiles,edges,a.out,roots)
        (a.out/'content-summary.json').write_text(json.dumps(state,indent=2)+'\n')
        print(json.dumps(state,indent=2),flush=True)
    if not state["complete"]:raise ValueError("Incomplete source scan; retained partial outputs are not whole-corpus results")
if __name__=='__main__':main()
