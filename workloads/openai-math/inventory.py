#!/usr/bin/env python3
"""Static inventory of pinned public OpenAI math sources. No Lean build."""
import argparse, collections, concurrent.futures, csv, gzip, json, os, pathlib, statistics, time, urllib.request

REPO = "openai/math"
def get(url):
    headers = {"User-Agent": "proofserve-workload-characterization"}
    if url.startswith("https://api.github.com") and os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=90) as response:
        return response.read()
def api(path):
    return json.loads(get("https://api.github.com/repos/" + REPO + "/" + path))
def project(path):
    parts = pathlib.PurePosixPath(path).parts
    if len(parts) >= 4 and parts[1] == "OAI":
        return "/".join(parts[1:4]).removesuffix(".lean")
    return "/".join(parts[1:-1]) or "lean-root"
def tree(sha, prefix, receipts):
    data = api("git/trees/" + sha + "?recursive=1")
    receipts.append({"prefix": prefix, "tree": sha, "truncated": data.get("truncated"), "entries": len(data["tree"])})
    if not data.get("truncated"):
        return [{"path": prefix + "/" + x["path"], "size": x.get("size"), "sha": x["sha"], "type": x["type"]}
                for x in data["tree"] if x["type"] == "blob"]
    # A truncated recursive response is never treated as a complete inventory.
    direct = api("git/trees/" + sha)
    if direct.get("truncated"):
        raise ValueError("Even non-recursive tree truncated: " + prefix)
    result = []
    for x in direct["tree"]:
        if x["type"] == "tree":
            result.extend(tree(x["sha"], prefix + "/" + x["path"], receipts))
        elif x["type"] == "blob":
            result.append({"path": prefix + "/" + x["path"], "size": x.get("size"), "sha": x["sha"], "type": "blob"})
    return result
def write_csv(path, rows):
    with (gzip.open(path, "wt", newline="") if path.suffix == ".gz" else path.open("w", newline="")) as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pin", required=True)
    parser.add_argument("--out", type=pathlib.Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    commit = api("commits/" + args.pin)
    if commit["sha"] != args.pin:
        raise ValueError("Use an immutable full commit")
    root = api("git/trees/" + commit["commit"]["tree"]["sha"])
    lean = next(x for x in root["tree"] if x["path"] == "lean")
    direct = api("git/trees/" + lean["sha"])
    receipts = []
    rows = []
    subtrees = [x for x in direct["tree"] if x["type"] == "tree"]
    def one(item):
        trace = []
        value = tree(item["sha"], "lean/" + item["path"], trace)
        return value, trace
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for value, trace in pool.map(one, subtrees):
            rows.extend(value); receipts.extend(trace)
    rows.extend({"path": "lean/" + x["path"], "size": x.get("size"), "sha": x["sha"], "type": "blob"}
                for x in direct["tree"] if x["type"] == "blob")
    rows.sort(key=lambda x:x["path"])
    if len({r["path"] for r in rows}) != len(rows):
        raise ValueError("Duplicate tree path")
    sources = [r for r in rows if r["path"].endswith(".lean")]
    for r in sources:
        r["project"] = project(r["path"])
    groups = collections.defaultdict(list)
    for r in sources:
        groups[r["project"]].append(r)
    projects = []
    for key, values in sorted(groups.items()):
        sizes = sorted(v["size"] for v in values)
        projects.append({"project": key, "lean_files": len(values), "source_bytes": sum(sizes),
                         "median_file_bytes": statistics.median(sizes), "max_file_bytes": max(sizes)})
    write_csv(args.out/"files.csv.gz", sources)
    write_csv(args.out/"projects.csv", projects)
    support = {}
    for name in ["README.md", "LICENSE", "lean/README.md", "lean/lean-toolchain", "lean/lake-manifest.json", "lean/lakefile.lean", "lean/ComparatorChallenges/README.md"]:
        text = get("https://raw.githubusercontent.com/" + REPO + "/" + args.pin + "/" + name).decode()
        support[name] = text
    (args.out/"upstream-metadata.json").write_text(json.dumps(support, indent=2)+"\n")
    manifest = json.loads(support["lean/lake-manifest.json"])
    package_rows = [{"name": x.get("name"), "url": x.get("url"), "revision": x.get("rev"),
                     "input_revision": x.get("inputRev"), "type": x.get("type")}
                    for x in manifest["packages"]]
    write_csv(args.out/"dependencies.csv", package_rows)
    github = next((x for x in root["tree"] if x["path"] == ".github"), None)
    workflows = tree(github["sha"], ".github", receipts) if github else []
    summary = {"repository": REPO, "commit": args.pin, "upstream_commit_time": commit["commit"]["committer"]["date"],
               "lean_files": len(sources), "lean_source_bytes": sum(x["size"] for x in sources), "projects": len(projects),
               "all_lean_tree_blobs":len(rows), "toolchain":support["lean/lean-toolchain"].strip(),
               "repository_license":"Apache-2.0 (root and lean LICENSE); dependencies keep their licenses",
               "recursive_responses_truncated":sum(x["truncated"] for x in receipts), "tree_receipts":receipts,
               "workflow_files":workflows, "elapsed_s":time.monotonic()-start,
               "scope":"Complete Git tree inventory; declarations/import contents not yet scanned; no Lean compilation or timing."}
    (args.out/"inventory.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
