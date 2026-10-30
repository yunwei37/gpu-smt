"""Third family route: proved sharp bounds plus128point stock-kernel checker."""
import re
from run_candidate_recovery import mask_comments
def transform(source):
    masked=mask_comments(source)
    theorem=re.search(r"\btheorem\s+\S+",masked)
    if not theorem:return source,{"route":None,"edits":[]}
    end=masked.find(":=",theorem.end())
    header=masked[theorem.start():end]
    if not (re.search(r"\^\s*3\b",header) and re.search(r"\^\s*4\b",header) and re.search(r"4096\s*≤",header)):
        return source,{"route":None,"edits":[]}
    positions=list(re.finditer(r"\binterval_cases\b",masked))
    if not positions:return source,{"route":"power","edits":[]}
    changed=source
    for m in reversed(positions):changed=changed[:m.start()]+"m_power_cases"+changed[m.end():]
    edits=[{"line":source[:m.start()].count("\n"),"original":"interval_cases","replacement":"m_power_cases"} for m in positions]
    changed="import PowerMethods\n"+changed
    return changed,{"route":"power","edits":edits}
