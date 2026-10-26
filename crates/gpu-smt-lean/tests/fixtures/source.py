"""Source/argv transport fixture; no native theorem is checked."""
import json, os, sys
if "--stdin" in sys.argv[1:]:
    code = sys.stdin.read()
else:
    from pathlib import Path
    code = Path(sys.argv[-1]).read_bytes().decode("utf-8")
detail = dict(source=code, argv=sys.argv[1:], pid=os.getpid())
print(json.dumps(dict(severity="information", data=json.dumps(detail))))
