"""Source/argv transport fixture; no native theorem is checked."""
import json, os, sys
if "--stdin" in sys.argv[1:]:
    code = sys.stdin.read()
else:
    from pathlib import Path
    code = Path(sys.argv[-1]).read_bytes().decode("utf-8")
if code == "large-stderr":
    for row in range(1024):
        sys.stderr.write(json.dumps(dict(row=row, payload="α" * 64), ensure_ascii=False) + "\n")
detail = dict(source=code, argv=sys.argv[1:], pid=os.getpid())
print(json.dumps(dict(severity="information", data=json.dumps(detail))))
