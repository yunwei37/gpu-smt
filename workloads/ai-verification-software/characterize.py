#!/usr/bin/env python3
"""Static public verification software; no generation, build or timing."""
import argparse,collections,csv,gzip,json,re,statistics,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'openai-math'))
from scan import masks,IMPORT
WORDS=('decide','native_decide','bv_decide','ofReduceBool','omega','simp','simp_all','grind','norm_num','aesop','rfl','mvcgen','linarith','nlinarith','sorry','axiom','unsafe','assert','proof','requires','ensures','invariant','decreases','reveal','assume')
C_TOKEN=re.compile(r'/\*|//|"(?:\\.|[^"\\])*"',re.S)
def mask_c(text):
 out=[];pos=0
 while True:
  found=C_TOKEN.search(text,pos)
  if not found:out.append(text[pos:]);break
  out.append(text[pos:found.start()])
  if found.group().startswith('"'):end=found.end()
  elif found.group()=='//':
   end=text.find('\n',found.end())
   if end<0:end=len(text)
  else:
   end=found.end();depth=1
   while depth:
    n=re.search(r'/\*|\*/',text[end:])
    if not n:raise ValueError('unterminated block comment')
    end+=n.end();depth+=1 if n.group()=='/*'else -1
  out.append(re.sub(r'[^\n]',' ',text[found.start():end]));pos=end
 return ''.join(out)
def write(path,rows):
 if not rows:return
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
def scope(key,rel):
 p=rel.parts
 if key=='vero':
  if p[0]=='benchmarks':return 'vero_active_scaffolds',p[1],Path(*p[:2])
  if p[:2]==('archive','benchmarks'):return 'vero_archived_scaffolds',p[2],Path(*p[:3])
  if p[:2]==('reference','BankLedger'):return 'vero_reference_exemplar',p[1],Path(*p[:2])
  if p[:2]==('reference','BankLedger-solution-old'):return 'vero_legacy_solution_provenance_unknown',p[1],Path(*p[:2])
 if key=='vericoding'and p[0]in ['vericoded','specs','inspection']:
  return 'vericoding_'+p[0],rel.stem,rel.parent
 if key=='algoveri'and p[0]=='algoveri_data':return ('algoveri_alternative_specifications' if rel.name=='lean_spec_new.lean' else 'algoveri_specifications'),p[1],Path(*p[:2])
 if key=='lkv'and p[0]=='lean':return 'lkv_checker_sources','KV',Path('lean')
def error_class(row):
 if row.get('success')is True:return 'publisher_success'
 text=str(row.get('error_message')or'').lower()
 if not text:return 'publisher_failure_no_diagnostic'
 for name,words in [
 ('reported_resource',['bad_alloc','out of memory','memory limit','memory_exception','excessive memory']),
 ('reported_budget',['timeout','timed out','time limit','heartbeats','maximum recursion']),
 ('reported_infrastructure',['command not found','no such file','connection refused','traceback']),
 ('reported_syntax',['syntax error','parse error','unexpected token','unexpected end']),
 ('reported_name_or_type',['unknown identifier','cannot find','unresolved','type mismatch','unknown constant']),
 ('reported_verification',['postcondition','assertion','verification failed','could not prove'])]:
  if any(x in text for x in words):return name
 return 'other_reported_failure'
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ['assets','evidence','out']:p.add_argument('--'+name,type=Path,required=True)
 a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);sources=[];records=[];graphs=collections.defaultdict(list)
 def add(sc,lang,identity,text,project,module,unit):
  data=dict(scope=sc,language=lang,identity=identity,project=project,unit=unit,bytes=len(text.encode()),scan_status='complete')
  try:
   code=masks(text)[1]if lang=='lean'else mask_c(text)
   data.update({w:len(re.findall(r"(?<![\w'])"+w+r"(?![\w'])",code))for w in WORDS})
   data['decide_plus_kernel']=len(re.findall(r'\bdecide\s*\+\s*kernel\b',code))
   data['raw_native_decide']=len(re.findall(r'\bnative_decide\b',text))
   imports=[]
   if lang=='lean':
    for m in IMPORT.finditer(code):imports.extend(x for x in re.findall(r"[A-Za-z_][\w'.]*",m[1])if x not in ['all','in'])
   data['imports']=sorted(set(imports))
  except ValueError as e:data['scan_status']=str(e);data['imports']=[]
  records.append(data)
  if lang=='lean'and unit=='source_file':graphs[(sc,project)].append((module,data))
 for key in ['vero','vericoding','algoveri','lkv']:
  m=json.loads((a.evidence/key/'inventory.json').read_text());root=a.assets/(key+'-'+m['revision'][:8])
  sources.append(dict(dataset=key,repository=m['repository'],revision=m['revision'],git_blob_files=m['files'],git_blob_bytes=m['bytes'],tree_truncated=m['tree_truncated'],root_license=m['license']['spdx_id'],native_workload_run=False))
  for file in sorted(root.rglob('*')):
   lang={'.lean':'lean','.rs':'verus','.dfy':'dafny'}.get(file.suffix)
   if not file.is_file()or not lang:continue
   rel=file.relative_to(root);scoped=scope(key,rel)
   if not scoped:continue
   sc,project,project_root=scoped;module=file.relative_to(root/project_root).with_suffix('').as_posix().replace('/','.')
   add(sc,lang,str(rel),file.read_text(errors='replace'),project,module,'source_file')
 pin=json.loads((a.evidence/'vericoding-scripts/commit.json').read_text())['sha'];secondary=a.assets/('vericoding-scripts-'+pin[:8]);tables=[];errors=collections.Counter()
 secondary_meta=json.loads((a.evidence/'vericoding-scripts/repository.json').read_text());secondary_tree=json.loads((a.evidence/'vericoding-scripts/tree.json').read_text())
 blobs=[x for x in secondary_tree['tree']if x['type']=='blob']
 sources.append(dict(dataset='vericoding-scripts',repository='Beneficial-AI-Foundation/vericoding',revision=pin,git_blob_files=len(blobs),git_blob_bytes=sum(x.get('size',0)for x in blobs),tree_truncated=secondary_tree.get('truncated'),root_license=secondary_meta['license']['spdx_id'],native_workload_run=False))
 for file in sorted((secondary/'vericoded').rglob('*')):
  lang={'.lean':'lean','.rs':'verus','.dfy':'dafny'}.get(file.suffix)
  if file.is_file()and lang:add('vericoding_scripts_snapshots',lang,str(file.relative_to(secondary)),file.read_text(errors='replace'),str(file.relative_to(secondary)),file.stem,'source_file')

 for file in sorted((secondary/'experiments').rglob('detailed_results.table.json')):
  raw=json.loads(file.read_text());rows=[dict(zip(raw['columns'],row))for row in raw['data']];rel=file.relative_to(secondary);lang=rel.parts[2];run=rel.parts[-2]
  nonempty=sum(isinstance(x.get('final_output'),str)and bool(x['final_output'].strip())for x in rows)
  tables.append(dict(path=str(rel),language=lang,run_id=run,rows=len(rows),publisher_success=sum(x.get('success')is True for x in rows),publisher_failure=sum(x.get('success')is False for x in rows),nonempty_final_candidates=nonempty,missing_candidates=len(rows)-nonempty,bypass_flags=sum(x.get('has_bypass')is True for x in rows),full_agent_trace_public=False))
  for i,row in enumerate(rows):
   errors[(lang,error_class(row),bool(row.get('final_output')))]+=1
   if isinstance(row.get('final_output'),str)and row['final_output'].strip():add('vericoding_table_final_outputs',lang,str(rel)+'#'+str(i),row['final_output'],run,'','final_output_row')
 projects=[]
 for (sc,project),group in graphs.items():
  modules=dict(group);done={};visiting=set()
  def visit(m):
   if m in done:return done[m]
   if m in visiting:raise ValueError('cycle')
   visiting.add(m);ds=[x for x in modules[m]['imports']if x in modules]
   result=1+max((visit(x)for x in ds),default=0);visiting.remove(m);done[m]=result;return result
  for m,data in group:
   try:data['internal_import_depth']=visit(m);data['internal_import_edges']=sum(x in modules for x in data['imports'])
   except ValueError:data['internal_import_depth']='unknown_cycle';data['internal_import_edges']=0
  depths=[x['internal_import_depth']for _,x in group if isinstance(x['internal_import_depth'],int)]
  if sc.startswith('vero_')or sc=='lkv_checker_sources':projects.append(dict(scope=sc,project=project,lean_files=len(group),source_bytes=sum(x['bytes']for _,x in group),max_internal_import_depth=max(depths,default='unknown'),internal_import_edges=sum(x['internal_import_edges']for _,x in group),lexical_scan_errors=sum(x['scan_status']!='complete'for _,x in group)))
 groups=collections.defaultdict(list)
 for x in records:groups[(x['scope'],x['language'],x['unit'])].append(x)
 summary=[];identifiers=[]
 for (sc,lang,unit),group in sorted(groups.items()):
  sizes=sorted(x['bytes']for x in group);valid=[x for x in group if x['scan_status']=='complete'];depths=[x['internal_import_depth']for x in group if isinstance(x.get('internal_import_depth'),int)]
  summary.append(dict(scope=sc,language=lang,unit=unit,observations=len(group),source_bytes=sum(sizes),median_bytes=statistics.median(sizes),p90_bytes=sizes[int((len(sizes)-1)*.9)],max_bytes=max(sizes),completed_lexical_scans=len(valid),lexical_scan_errors=len(group)-len(valid),max_internal_import_depth=max(depths,default='not_applicable'),external_dependency_depth='unmeasured'))
  for word in WORDS+('decide_plus_kernel','raw_native_decide'):identifiers.append(dict(scope=sc,language=lang,unit=unit,identifier=word,occurrences=sum(x[word]for x in valid),observations_with_identifier=sum(x[word]>0 for x in valid),observations_scanned=len(valid),total_observations=len(group),meaning='lexical identifier; not executed call, cost or acceptance'))
 write(a.out/'sources.csv',sources);write(a.out/'scope-summary.csv',summary);write(a.out/'identifiers.csv',identifiers);write(a.out/'multi-module-projects.csv',sorted(projects,key=lambda x:(x['scope'],x['project'])));write(a.out/'public-output-tables.csv',tables)
 write(a.out/'reported-error-classes.csv',[dict(language=k[0],reported_class=k[1],output_present=k[2],rows=v,scope='publisher final rows; heuristic first-match label, no native timing')for k,v in sorted(errors.items())])
 with gzip.open(a.evidence/'static-observations.jsonl.gz','wt')as f:
  for x in records:f.write(json.dumps(x)+'\n')
 state=dict(static_observations=len(records),public_final_tables=len(tables),final_rows=sum(x['rows']for x in tables),nonempty_final_candidates=sum(x['nonempty_final_candidates']for x in tables),native_workload_run=False)
 (a.evidence/'static-summary.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(state));print(json.dumps(summary))
if __name__=='__main__':main()
