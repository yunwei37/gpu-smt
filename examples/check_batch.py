"""Run after the Docker quick start and pip install ./clients/python."""
from proofserve import Client

response = Client().check(
    [
        {"id": "arithmetic", "code": "import Mathlib\nexample : (2 : Nat) + 2 = 4 := by norm_num"},
        {"id": "false", "code": "example : False := by decide"},
    ],
    timeout=30,
)
for result in response["results"]:
    print(result["id"], result["response"], result["error"])
