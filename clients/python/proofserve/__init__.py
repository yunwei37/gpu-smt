"""Dependency-free client for the core Kimina /check contract."""
import json
from urllib.request import Request, urlopen


class Client:
    """Submit source batches and receive original Lean responses.

    timeout in check() is the server's per-candidate timeout.
    request_timeout separately controls the HTTP connection; None waits for the
    complete batch. Network and HTTP errors propagate rather than becoming
    Lean rejections.
    """

    def __init__(self, api_url="http://localhost:3000", *, request_timeout=None):
        self.api_url = api_url.rstrip("/")
        self.request_timeout = request_timeout

    def check(self, snippets, *, timeout=300.0, reuse=True):
        """Accept a string or a batch of strings / {'id', 'code'} mappings.

        Returns the server dictionary with ordered results. Each result retains
        its id, time, raw response and operational error. A missing operational
        error alone does not mean the proof is accepted: inspect Lean messages
        and sorries too.
        """
        if isinstance(snippets, str):
            snippets = [snippets]
        normalized = []
        for index, item in enumerate(snippets):
            if isinstance(item, str):
                normalized.append({"id": str(index), "code": item})
            else:
                normalized.append({"id": str(item.get("id", index)), "code": item["code"]})
        request = Request(
            self.api_url + "/check",
            data=json.dumps({"snippets": normalized, "timeout": timeout, "reuse": reuse}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=self.request_timeout) as response:
            return json.load(response)
