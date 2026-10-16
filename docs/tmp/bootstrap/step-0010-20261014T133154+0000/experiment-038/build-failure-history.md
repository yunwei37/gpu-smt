# E038 build/setup failures retained, 2026-10-16

Actual source preparation and integration failures are not verifier failures or performance observations.

* Earlier helper C++ attempts (missing stddef/features/vendor config/assertion headers) and the first io.cpp conditional-include mistake have separate original log/terminal files here.
* During this continuation, the first generated-Main entry edit expected an initializer string without its actual builtin comment and failed an assertion. The private dependency source was then read and the exact generated call repaired.
* The first setup executable link exposed undefined helper C++ symbols because clang used as a C driver did not automatically link libc++. Root explicitly linked the existing SDK static C++ libraries into the helper, with local symbolic binding.
* Subsequent link attempts exposed inconsistent host glibc headers versus the old SDK sysroot, including __isoc23_strtol and pthread GLIBC_2.34 references. The experimental executable now consistently uses the owning Workspace host glibc. It is not a matched rebuild of the shipped reference.
* Removing the original SDK sysroot fragment also removed its unwind linkage. Explicit existing SDK libunwind fixes this build dependency.
* A complete shared-runtime compile first lacked generated githash.h. It is generated from the actual official Lean4.27 tag/installed SDK commit db93fe1608548721853390a10cd40580fe7d22ae; mimalloc comes from Lean4.27's declared upstream v2.2.3. Initial shared-runtime-compile.json preserves this failure; later single-file build is successful.
* setup1 on/off fail before preparation because libLake_shared.so cannot be located.
* setup2 on/off fail before preparation because findSysroot invokes the SDK CLI under the new incomplete shared-runtime shell exports (missing lean_main). LEAN_SYSROOT now points directly to the unchanged existing SDK for the finite setup; original setup1/2 stdout/stderr/terminal records remain.

Some early repeated linker/compiler command receipts reused the same filenames and were overwritten before archival. The descriptions above are reconstructed from contemporaneous tool outputs, not complete original raw logs; do not claim full raw preservation for those overwritten attempts. Successful pre-map and v1 build receipts were archived before later builds. Source v1 and actual setup3/4 observations remain separate from the forward scheduler cleanup fix and setup5. No commits were rewritten and no original baseline binary or active capture was changed.
