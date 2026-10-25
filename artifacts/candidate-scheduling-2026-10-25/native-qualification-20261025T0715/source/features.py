"""Source-only ordering features; no outcome or timing inputs at inference."""
import math,re,runpy
from pathlib import Path
STRIP=runpy.run_path(str(Path(__file__).with_name('analyze.py')))['strip_comments']
TACTICS=['simp','simp_all','simpa','norm_num','omega','linarith','nlinarith','ring','ring_nf','decide','native_decide','interval_cases','aesop','exact','rw','have','by_cases','rcases','cases','induction','constructor','apply']
NAMES=['log_characters','log_lines','log_numeral_max','log_numerals','log_semicolon_chains']+['log_'+x for x in TACTICS]
def vector(code):
 text=STRIP(code)
 nums=re.findall(r'\b\d+\b',text)
 # log10 via digit length avoids constructing arbitrarily large integers.
 largest=max((len(s.lstrip('0'))for s in nums),default=0)
 base=[math.log1p(len(text)),math.log1p(text.count('\n')+1),math.log1p(largest),math.log1p(len(nums)),math.log1p(text.count('<;>'))]
 return base+[math.log1p(len(re.findall(r'(?<![\w])'+t+r'(?![\w])',text)))for t in TACTICS]
def score(code,model):
 x=[1.]+[(v-m)/s for v,m,s in zip(vector(code),model['means'],model['scales'])]
 logit=sum(a*b for a,b in zip(x,model['logistic_coefficients']))
 logprob=-math.log1p(math.exp(-logit))if logit>=0 else logit-math.log1p(math.exp(logit))
 logtime=sum(a*b for a,b in zip(x,model['logtime_coefficients']))
 return logprob-logtime
