# Plan — root implementation node

Implement NativeLean using the existing backend trait and Linux lifecycle helpers.
Selectable with --lean instead of --repl; prepared host remains REPL-specific.
Use installed Lean's documented --json --stdin, source bytes unchanged.
Reuse existing aggregate monitor/admission rather than add another runner.
Run format,Clippy,ordinary tests,docs and actual native CI; no local fullcapture.
Original source path-dependent imports need their original project environment;
stdin's diagnostic filename is not an original reference filename.
