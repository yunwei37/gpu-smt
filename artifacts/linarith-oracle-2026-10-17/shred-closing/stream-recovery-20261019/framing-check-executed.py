import sys,asyncio,json
from types import SimpleNamespace
sys.path[:0]=["/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d","/workspaces/.agent-state/gpu-smt-deps/kimina-server-fb2393d/client"]
from server.repl import Repl
async def main():
    reader=asyncio.StreamReader()
    payload=json.dumps({"messages":[{"severity":"error","data":"x"*200000}]}).encode()
    reader.feed_data(payload+b"\n\n"+b'{"env":0}\r\n \t\r\n'+b'{"env":1}')
    reader.feed_eof()
    repl=Repl.__new__(Repl);repl.proc=SimpleNamespace(stdout=reader);repl._stdout_pending=b""
    first=await repl._read_response();second=await repl._read_response();third=await repl._read_response();fourth=await repl._read_response()
    assert first==payload+b"\n"
    assert second==b'{"env":0}\r\n'
    assert third==b'{"env":1}'
    assert fourth==b""
    print(json.dumps(dict(default_stream_limit=reader._limit,long_response_bytes=len(first),coalesced_frames=3,exact_bytes_preserved=True,EOF_preserved=True)))
asyncio.run(main())
