"""Recover only uniquely invertible two-writer JSON-line splices; retain raw log."""
from pathlib import Path
import argparse,json,re,gzip
p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('output',type=Path);p.add_argument('receipt',type=Path);a=p.parse_args()
decoder=json.JSONDecoder();pending=None;ledger=[];count=0
with(gzip.open(a.input,'rt')if a.input.suffix=='.gz'else a.input.open())as src,a.output.open('w')as out:
 for no,line in enumerate(src,1):
  try:json.loads(line)
  except json.JSONDecodeError:pass
  else:
   if pending is not None:raise ValueError('unpaired corruption before valid record')
   out.write(line);count+=1;continue
  if pending is None:pending=(no,line);continue
  prior,first=pending
  if no!=prior+1:raise ValueError('nonadjacent corruption')
  matches=[]
  for m in re.finditer(r'\{"',first):
   start=m.start()
   try:
    foreign,size=decoder.raw_decode(first[start:])
    if not isinstance(foreign,dict)or'ty'not in foreign:continue
    tail=first[start+size:].removesuffix('\n')
    rebuilt=first[:start]+tail+line
    parent=json.loads(rebuilt)
    if not isinstance(parent,dict)or'ty'not in parent:continue
    inserted=first[start:start+size]
    # Reconstruct the exact original two physical lines from the derived records.
    inverse=rebuilt[:start]+inserted+rebuilt[start:start+len(tail)]+'\n'+rebuilt[start+len(tail):]
    if inverse!=first+line:continue
    matches.append((start,size,tail,inserted,rebuilt,parent,foreign))
   except json.JSONDecodeError:continue
  if len(matches)!=1:raise ValueError('splice not uniquely invertible at '+str(prior))
  start,size,tail,inserted,rebuilt,parent,foreign=matches[0]
  derived=inserted+'\n'+rebuilt
  assert len(derived.encode())==len((first+line).encode())
  out.write(derived);count+=2
  ledger.append({'physical_lines':[prior,no],'inserted_character_offset':start,'inserted_character_length':size,'first_line_parent_suffix_characters':len(tail),'parent_type':parent['ty'],'inserted_type':foreign['ty'],'inverse_equals_original':True,'UTF8_byte_length_preserved':True})
  pending=None
 if pending:raise ValueError('unfinished corrupt pair')
a.receipt.write_text(json.dumps({'input':str(a.input),'output':str(a.output),'records':count,'recovered_pairs':ledger,'raw_untouched':True,'scope':'Only unique two-record writer interleavings recovered. Every splice is exactly invertible to original bytes; no numeric value/source/timing synthesized. Derived record order is inserted-record completion then parent completion.'},indent=2)+'\n')
print('RECOVERED',len(ledger),'pairs;',count,'records')
