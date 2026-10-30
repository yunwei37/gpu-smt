/* Native-loader regression only; no verifier algorithm or persistent state. */
#include <stdio.h>
#include <stdlib.h>
__attribute__((constructor)) static void record_load(void) {
    const char *path = getenv("GPU_SMT_NATIVE_LOAD_MARKER");
    if (!path) abort();
    FILE *out = fopen(path, "a");
    if (!out) abort();
    if (fputs("loaded\n", out) < 0 || fclose(out)) abort();
}
