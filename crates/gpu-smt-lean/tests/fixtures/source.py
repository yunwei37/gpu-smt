"""Source/argv transport fixture; no native theorem is checked."""
import json, os, sys
code = sys.stdin.read()
detail = dict(source=code, argv=sys.argv[1:], pid=os.getpid())
print(json.dumps(dict(severity="information", data=json.dumps(detail))))
