# Official input path and existing ephemeral filesystem

Root reads pinned315f24d4 lka.py and actual tests/init.yaml and init-prelude.yaml. Full Init is an official leanfile test (tests/init_module.lean), accepted outcome, compare-perf true; skip-on-ci true. The official small tarball independently excludes inputs larger than10MB. It is not necessary to replace the official workload with toy obligations.

The official entrypoint is lka.py build-test init. For leanfile tests it creates an ordinary Test module using the Arena root toolchain, builds lean4export for that toolchain, builds Test, then exports it. The helper's lean4export fetch follows master; any local reconstruction must retain the resolved exporter commit/toolchain/header rather than claim it automatically matches an older published snapshot.

The existing owning Workspace /tmp has about317GBfree on its overlay, separate from /workspaces Longhorn. Regenerable official input and dependency builds can live there; durable source/result provenance remains in the project. No new mount, volume, project checkout or external development environment is needed. Private temporary dependency source is not a second gpu-smt checkout.

This is a source/filesystem qualification only. No new full-input build, GPU call, full Init preflight, corpus matrix or experimental finding is claimed. The current eager bridge/interpreter still lacks an adequate paid-cost case. Any admitted actual full-input comparison must retain its exact generated producer identity and the existing complete-cost boundary.
