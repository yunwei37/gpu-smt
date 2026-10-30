"""HTTP contract tests; no native process or external service."""
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError
from proofserve import Client


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.requests = []
        requests = self.requests

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                requests.append((self.path, body))
                if body["timeout"] == -1:
                    self.send_response(400)
                    self.end_headers()
                    return
                data = json.dumps({"results": [
                    {"id": s["id"], "response": {"messages": [{"severity": "error"}]},
                     "error": None, "time": 0.01}
                    for s in body["snippets"]
                ]}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *args):
                pass

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.client = Client(f"http://127.0.0.1:{self.server.server_port}/")

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def test_batch_preserves_ids_unicode_and_native_error(self):
        result = self.client.check([{"id": "α", "code": "example : False := by decide"}, "example : True := by trivial"],
                                   timeout=5, reuse=False)
        self.assertEqual([r["id"] for r in result["results"]], ["α", "1"])
        self.assertEqual(result["results"][0]["response"]["messages"][0]["severity"], "error")
        self.assertEqual(self.requests[0][0], "/check")
        self.assertFalse(self.requests[0][1]["reuse"])
        self.assertEqual(self.requests[0][1]["timeout"], 5)

    def test_single_string_is_one_candidate(self):
        self.client.check("example : True := by trivial")
        self.assertEqual(len(self.requests[0][1]["snippets"]), 1)

    def test_http_failure_is_not_native_rejection(self):
        with self.assertRaises(HTTPError):
            self.client.check("example : True := by trivial", timeout=-1)


if __name__ == "__main__":
    unittest.main()
