# Source provenance

The numerical engine derives from [Farkas](https://github.com/lucifer1004/farkas),
with upstream baseline commit
5a38a7e8502213cb644faa2e11a15429f0cf0f9a recorded by the experiment.
The original [Apache2 license](https://github.com/lucifer1004/farkas/blob/5a38a7e8502213cb644faa2e11a15429f0cf0f9a/LICENSE)
is included here. Upstream Farkas authors retain their attribution.

This is a modified research component. Local changes include the external
arithmetic AST, literal natural-power expansion, exact positive/negative
certificate portfolio, cancellable support workers and retained diagnostic
facilities. The Lean files include the local4.27 adaptation and reduced
diagnostic implementation. These are not claims of new LP primitives or
first external certificate checking.

Source bodies were copied from the actual retained E1080 implementation;
the only copy-time source addition is a provenance comment. Frozen historical
snapshots remain under artifacts/. Package compilation is performed separately
from every active capture, and successful packaging does not establish a new
performance result. Some legacy variable/log names say GPU even for a CPU
HiGHS support process; the configured provider determines actual device use.


## Scope of the local change

The [source-level comparison](../../../../docs/tmp/bootstrap/step-0010-20261014T133154+0000/literature-20261020T061754Z/report.md) distinguishes the inherited
numerical/proof mechanisms from this local composition. Direct reconstruction
is not the first external-certificate or deferred-proof design; direct Real/Rat
handling plus native fallback is not a strict coverage superset of the pinned
competitor. The measured4.27adaptation is distinct from unchanged upstream4.31.
The existing full population capture and native check path are not modified.
