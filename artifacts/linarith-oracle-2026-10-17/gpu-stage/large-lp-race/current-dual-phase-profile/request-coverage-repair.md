# Qualification exposes missing request metadata

First real64qualification passes source fidelity, all stage engagement and gzip
integrity: native53.140828s, strongCPUprofile30.283087s versus normal28.765037s,
5.277%diagnostic overhead. Raw firstcapture/source remain retained. Its reused
roundtrip emitters contain answer/source/callID but omit request body. Add that
body to both native and direct roundtrip records, with no verifier change.

The direct numeric response now also reports exact certificate-space shape and
product-column provenance from data already constructed by the unchanged solver:
rows, columns, nonzeros, generated product count and per-column origin flags.
These are EXACT UNSCALED certificate matrices; actual successful floating models
remain separately recorded by HiGHS proxy. No second numerical solve or matrix
reconstruction is inserted. Metadata-scan/serialization overhead stays charged
to the diagnostic whole clock. Pure cancelled child CPU remains unmeasured.

Compile private copies only; unlink old read-only source/output symlinks before
writing so the retained profiler/primary trees remain unchanged. Requalify the
same64sources before admitting full1000, preserving both attempts. This repairs
measurement completeness, not a performance optimization or source reselection.
