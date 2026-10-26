# Synchronize the canonical draft PDF with already accepted source changes

Root-only targeted writing/self-review,2026-10-26. This is artifact delivery,
not a new experiment or a research result. docs/paper/main.pdf was last updated
at502a4d3(505618bytes),while later committed source already contains completed
first-success scheduling,Mathlib4.9development controls,hotspot prototype
limits and the memory sensitivity check. The old PDF still labels the completed
consumer matrix pending. previous-source-diff.patch.gz records exactly that drift.

The actual pinnedTectonic compile already exists in
../lean-failure-profile-2026-10-25/body-memory-association-20261026/paper-compile/ .
Currentmain.tex matches sourcecdaae00byte-for-byte;no paper source has changed
since that compile. Copy its509096-byte PDF into the canonical path and verify
byte equality. Preserve oldbinary/source through normalGit history. No new
compilation,candidate proof,number,claim,RQ or narrative is authored.

Read-only PDFinspection uses the bundleddesktopruntime26.1020.11618:
pypdf text comparison confirms both drafts have34pages and the sensitivity
paragraph appears onp14. Poppler renders all34pages at45dpi for two inspected
overview sheets andp13–15at110dpi for detailed review. No new clipping,overlap,
blank page or unreadable glyph defect is observed in that scope. The local
review directory/commands/scope are recorded in receipt.json. PNGs are temporary
derived views;the sourcePDF and exact compile/log remain committed and can
reproduce them. An initialcp1252printing error is corrected with Python-Xutf8,
without altering PDF bytes.

Whole-paper semantic review,full-resolution inspection of all34pages and
submission readiness are not claimed. Existing result placeholders,layout
warnings,openRQs and self-review limits remain. The authoritative manuscript
source staysdocs/paper/main.tex. Resource-layer controls and ordinary scheduling
remain prior techniques;no newnovelty or OSDIacceptance is implied.

The current sole fullpair is not restarted or joined by a second native group.
This edit only repairs the published draft pointer's content;it adds no new
file-format,workflow,runner,entity or source configuration.
