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
