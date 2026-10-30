"""Root cross-check of W's committed derived tables; no source scan/native run."""
import argparse, collections, csv, gzip, io, json, math, resource, subprocess, time
from pathlib import Path

REV = "daffefc"
BASE = "workloads/openai-math/static-4eaee875/content/"

def audit(root, out):
    start = time.monotonic()
    def blob(name):
        return subprocess.check_output(["git", "show", REV + ":" + BASE + name], cwd=root)
    def rows(name):
        return csv.DictReader(io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(blob(name)))))
    summary = json.loads(blob("summary.json"))
    source_roots = sorted(summary["import_graph"]["source_roots"], key=len, reverse=True)
    files, byte_sizes, count_tokens, modules, paths = 0, [], collections.Counter(), {}, set()
    tactic_files = collections.Counter()
    fields = list(summary["token_occurrences"])
    for row in rows("file-metrics.csv.gz"):
        path = row["path"]
        assert path not in paths
        paths.add(path)
        source_root = next(q for q in source_roots if path.startswith(q + "/"))
        module = path[len(source_root)+1:-5].replace("/", ".")
        assert module not in modules
        modules[module] = files
        files += 1
        byte_sizes.append(int(row["bytes"]))
        for key in fields:
            value = int(row[key])
            count_tokens[key] += value
            tactic_files[key] += value > 0
    assert files == summary["files_scanned"] == summary["files_expected"] == 163097
    assert sum(byte_sizes) == summary["source_bytes_scanned"] == 1785499363
    assert dict(count_tokens) == summary["token_occurrences"]
    del paths
    deps = [set() for _ in range(files)]
    reverse = [[] for _ in range(files)]
    external = collections.Counter()
    for row in rows("imports.csv.gz"):
        source = modules[row["module"]]
        target = modules.get(row["imports"])
        assert (target is not None) == (row["internal"] == "True")
        if target is None:
            external[row["imports"].split(".")[0]] += 1
        else:
            deps[source].add(target)
    edges = sum(map(len, deps))
    for child, parents in enumerate(deps):
        for parent in parents:
            reverse[parent].append(child)
    indegree = [len(d) for d in deps]
    depth = [1] * files
    ready = collections.deque(i for i,d in enumerate(indegree) if d == 0)
    visited, waves = 0, collections.Counter()
    while ready:
        i = ready.popleft()
        visited += 1
        waves[depth[i]] += 1
        for child in reverse[i]:
            depth[child] = max(depth[child], depth[i]+1)
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    reachable, frontier = set(), [modules["OAI"]]
    while frontier:
        i = frontier.pop()
        if i in reachable:
            continue
        reachable.add(i)
        frontier.extend(deps[i] - reachable)
    graph = dict(modules=files, internal_edges=edges, topologically_ordered=visited,
                 unit_weight_longest_import_chain=max(depth), max_import_depth_wave_width=max(waves.values()),
                 OAI_root_reachable_modules=len(reachable),
                 OAI_root_reachable_source_bytes=sum(byte_sizes[i] for i in reachable))
    for key, value in graph.items():
        assert summary["import_graph"][key] == value, (key,value)
    assert visited == files and edges == 370864
    assert graph["unit_weight_longest_import_chain"] == 451
    assert graph["max_import_depth_wave_width"] == 9225
    assert dict(external) == summary["import_graph"]["external_root_occurrences"]
    largest = math.ceil(.016 * files)
    byte_share = sum(sorted(byte_sizes, reverse=True)[:largest]) / sum(byte_sizes)
    result = dict(source_W_commit=REV, dataset_pin=summary["commit"],
                  files=files, source_bytes=sum(byte_sizes), token_occurrences=dict(count_tokens),
                  files_with_tokens=dict(tactic_files), graph=graph,
                  largest_1p6percent_file_count=largest, largest_file_byte_share=byte_share,
                  elapsed_crosscheck_s=time.monotonic()-start,
                  process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  native_executions=0,
                  interpretation=[
                      "Independent computation from W-derived CSVs is an internal-consistency self-review, not a second full source scan.",
                      "Token counts are lexical; graph depth/width are unit-weight structure, not native time or safe parallelism.",
                      "No native acceptance, transitive axiom closure, cache-hit rate or speedup is established.",
                  ])
    out.mkdir(parents=True, exist_ok=False)
    (out/"result.json").write_text(json.dumps(result, indent=2)+"\n")
    return result

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(audit(a.root,a.out),indent=2))
