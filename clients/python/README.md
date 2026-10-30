# Python client

From the repository root: `pip install ./clients/python` (Python3.10+, no runtime dependencies).
Start the service with the root Docker quick start, then run
`python examples/check_batch.py`.

```python
from proofserve import Client

response = Client("http://localhost:3000").check(
    [{"id": "one", "code": "import Mathlib\nexample : (2 : Nat) + 2 = 4 := by norm_num"},
     {"id": "two", "code": "example : False := by decide"}],
    timeout=180,
)
for result in response["results"]:
    print(result["id"], result["response"], result["error"])
```

The batch/snippets, timeout and reuse fields follow the core Kimina /check API.
Results keep caller order and raw Lean diagnostics. An operational error of
None does not certify acceptance; errors or sorries in response still matter.
Unsupported debug/infotree/session extensions are documented in ../../docs/api.md.
HTTP/network exceptions propagate. Use Client(..., request_timeout=600) for
a separate HTTP deadline; per-candidate Lean timeouts do not bound batch time.
