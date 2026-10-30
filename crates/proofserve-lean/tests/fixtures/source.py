"""Source/argv transport fixture; no native theorem is checked."""
import json, os, sys, time
if "--stdin" in sys.argv[1:]:
    code = sys.stdin.read()
else:
    from pathlib import Path
    code = Path(sys.argv[-1]).read_bytes().decode("utf-8")
if code == "large-stderr":
    for row in range(1024):
        sys.stderr.write(json.dumps(dict(row=row, payload="α" * 64), ensure_ascii=False) + "\n")
background = None
if code in ("hold-stderr", "hold-stdout"):
    background = os.fork()
    if background == 0:
        os.close(1 if code == "hold-stderr" else 2)
        time.sleep(3)
        os._exit(0)
detail = dict(source=code, argv=sys.argv[1:], pid=os.getpid(), background=background)
print(json.dumps(dict(severity="information", data=json.dumps(detail))))
