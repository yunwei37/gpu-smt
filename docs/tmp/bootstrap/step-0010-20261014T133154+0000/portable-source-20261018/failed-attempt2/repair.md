The full source build links, but first real CLI verification fails before
the theorem with an undefined lp_mathlib linter symbol. Regenerating C without
Lean's package setup changed exported symbol identities relative to cached
OLeans. No proof success or timing is counted. Root inspected the pinned
Lean.ModuleSetup and Lake.Package.id? implementations, discovered original
package names through Lake's manifest, and qualified the actual expected
symbol using the serializer's package key. The builder now supplies proper
per-module setup for regenerated dependency C; host and proof algorithms
are unchanged. All failed logs/build metadata and first source remain.
