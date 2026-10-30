"""Research-only literal arithmetic routing; no production acceptance/cache change."""
from pathlib import Path
import re,json,argparse
from analyze_generalization import literal_params,detect
from run_candidate_recovery import mask_comments
def transform(source):
    if not detect(source):return source,0
    masked=mask_comments(source)
    spans=list(re.finditer(r"\brfl\b",masked))
    result=source
    for match in reversed(spans):
        result=result[:match.start()]+"m_closed_nat_rfl"+result[match.end():]
    return "import ClosedNatMethods\n"+result,len(spans)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path);p.add_argument("output",type=Path)
    a=p.parse_args();s=a.source.read_text();out,n=transform(s)
    with a.output.open("x") as f:f.write(out)
    print(json.dumps({"rfl_sites":n,"literals":literal_params(s),
      "acceptance":"entire output must pass original kernel; otherwise keep original result"}))
