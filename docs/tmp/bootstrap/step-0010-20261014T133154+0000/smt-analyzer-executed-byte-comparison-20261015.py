#!/usr/bin/env python3
"""Recompute complete-source native observations; never execute a verifier."""
import argparse
import base64
from collections import Counter
import gzip
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import zipfile
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'native-prefix-4125-development'))
from service_common import commands

METHODS = ('stock','branch','logical')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decoded(name,data):
    return gzip.decompress(data) if name.endswith('.gz') else data


def quantiles(values):
    if not values:
        return None
    values = sorted(values)
    def q(p):
        x = (len(values)-1)*p
        i = int(x)
        return values[i]+(values[min(i+1,len(values)-1)]-values[i])*(x-i)
    return dict(observed=len(values),sum=sum(values),mean=statistics.mean(values),
                p50=q(.5),p95=q(.95),p99=q(.99),p999=q(.999),max=max(values))


def semantic(native):
    """Original Verus basic result and per-function identities, not timings."""
    if not isinstance(native,dict):
        return None
    result = native.get('verification-results')
    functions = []
    for m in native.get('times-ms',{}).get('smt',{}).get('smt-run-module-times',[]):
        functions.extend((m.get('module'),f.get('function'),f.get('success'))
                         for f in m.get('function-breakdown',[]))
    return dict(verification_results=result,functions=sorted(functions,key=str))


def time_fields(data):
    result = {}
    for name,key in [('User time (seconds)','user_cpu_s'),('System time (seconds)','system_cpu_s'),
                     ('Maximum resident set size (kbytes)','maxrss_kib')]:
        m = re.search(r'^\s*'+re.escape(name)+r':\s*([0-9.]+)',data.decode(errors='replace'),re.M)
        if m:
            result[key] = float(m.group(1))
    return result


def requested_artifacts(stdin,stdout):
    """Use Verus's original echo barriers, not an invented SMT interpretation.

    Statistics/version reply groups stay raw, but cannot make a model appear
    changed merely because a timing counter elsewhere changed.
    """
    if stdin is None:
        return None
    groups, requested = [],[]
    for begin,end,head in commands(stdin):
        command = stdin[begin:end]
        if head in ('get-model','get-proof','get-unsat-core','get-value'):
            requested.append(head)
        if head=='echo' and re.fullmatch(rb'\(echo\s+"<<DONE>>"\s*\)',command):
            groups.append(requested)
            requested = []
    replies = re.split(rb'(?m)^<<DONE>>\r?\n',stdout)
    if len(replies)-1!=len(groups):
        return dict(framing_equal=False,input_barriers=len(groups),output_barriers=len(replies)-1)
    return dict(framing_equal=True,replies=[dict(barrier=i,requests=heads,
                response_bytes_b64=base64.b64encode(replies[i]).decode('ascii'),bytes=len(replies[i]))
                for i,heads in enumerate(groups) if heads])


def source(directory,index):
    result = dict(candidate=index,issues=[],native_sessions=[])
    archive = directory/f'source-{index:05d}.zip'
    try:
        with zipfile.ZipFile(archive) as z:
            files = {name:decoded(name,z.read(name)) for name in z.namelist()}
        receipt = json.loads(files['receipt.json'])
        result['receipt'] = receipt
        result.update({key:receipt.get(key) for key in ('returncode','terminal','timed_out',
                                                       'external_wall_s','exception','source_sha256')})
        raw = files['stdout.bin.gz']
        result['stdout_sha256'] = sha(raw)
        result['stderr_sha256'] = sha(files['stderr.bin.gz'])
        result.update(time_fields(files.get('time.txt',b'')))
        try:
            native = json.loads(raw)
            result['basic'] = semantic(native)
            result['native_json'] = native
        except (ValueError,UnicodeError):
            result['basic'] = None
        for label in ('stdout','stderr'):
            r = receipt.get('streams',{}).get(label,{})
            data = files[label+'.bin.gz']
            if r.get('eof') is not True or r.get('bytes')!=len(data):
                result['issues'].append('original enclosing stream incomplete or identity differs: '+label)
        # Native streams are independent of enclosing Verus stdout: Verus
        # consumes them. Preserve every original output/model/error, then derive
        # only plain status sequence; alternative artifacts need interpretation.
        stdout_names = sorted(n for n in files if n.startswith('native/') and
                              (n.endswith('stdout.bin.gz') or n.endswith('stdout.bin')))
        for name in stdout_names:
            stem = name.removesuffix('.gz').removesuffix('stdout.bin')
            stdout = files[name]
            stdin = files.get(stem+'stdin.bin.gz',files.get(stem+'stdin.bin'))
            stderr = files.get(stem+'stderr.bin.gz',files.get(stem+'stderr.bin'))
            row = dict(path=name,stdout_sha256=sha(stdout),stdout_bytes=len(stdout),
                       statuses=[s.decode() for s in re.findall(rb'(?m)^\s*(sat|unsat|unknown)\s*$',stdout)],
                       stdin_sha256=sha(stdin) if stdin is not None else None,
                       stdin_bytes_b64=base64.b64encode(stdin).decode('ascii') if stdin is not None else None,
                       stderr_sha256=sha(stderr) if stderr is not None else None,
                       original_artifact_requests=bool(stdin is not None and
                         re.search(rb'\(\s*(get-model|get-proof|get-unsat-core|get-value)\b',stdin)))
            try:
                row['artifact_responses'] = requested_artifacts(stdin,stdout)
            except ValueError as e:
                row['artifact_responses'] = dict(framing_error=repr(e))
            if stdin is None or stderr is None:
                result['issues'].append('native stream counterpart missing: '+name)
            result['native_sessions'].append(row)
        for name,data in files.items():
            if name.startswith('native/') and name.endswith('.json'):
                try:
                    meta = json.loads(data)
                    result.setdefault('native_receipts',[]).append(dict(path=name,value=meta))
                    result.setdefault('native_exit_codes',[]).append(meta.get('native_exit_code'))
                    streams = meta.get('streams',{})
                    for label in ('stdin','stdout','stderr'):
                        stream = streams.get(label,{})
                        original_path = str(stream.get('path',''))
                        archived_name = (Path(name).parent/Path(original_path).name).as_posix()
                        actual = files.get(archived_name)
                        if actual is None or stream.get('eof') is not True or stream.get('closed') is not True or stream.get('bytes')!=len(actual):
                            result['issues'].append('native original stream missing/incomplete/different: '+name+' '+label)
                    if meta.get('errors') or meta.get('input_errors') or meta.get('output_errors'):
                        result['issues'].append('native transport error: '+name)
                except ValueError as e:
                    result['issues'].append('native receipt parse: '+str(e))
    except (OSError,ValueError,KeyError,zipfile.BadZipFile,EOFError) as e:
        result['issues'].append(repr(e))
    return result


def compare(stock,other):
    issues = []
    for r in (stock,other):
        if r.get('issues') or not r.get('terminal') or r.get('timed_out'):
            issues.append('source outcome missing/incomplete/censored')
    if stock.get('returncode')!=other.get('returncode'):
        issues.append('enclosing native exit differs')
    for key in ('candidate','source_file','argv','affinity'):
        if stock.get('receipt',{}).get(key)!=other.get('receipt',{}).get(key):
            issues.append('original source/command/resource identity differs: '+key)
    a,b = stock.get('basic'),other.get('basic')
    if a!=b:
        issues.append('enclosing native basic result differs')
    # Both invalid syntax sources can have no JSON; keep the original exit and
    # raw diagnostics instead of demanding string formatting equality.
    if a is None and stock.get('returncode')==0:
        issues.append('successful native JSON missing')
    aa,bb = stock.get('native_sessions',[]),other.get('native_sessions',[])
    if len(aa)!=len(bb):
        issues.append('native session count differs')
    if stock.get('native_exit_codes',[])!=other.get('native_exit_codes',[]):
        issues.append('native session exit differs')
    artifacts = []
    for x,y in zip(aa,bb):
        if x['stdin_bytes_b64']!=y['stdin_bytes_b64']:
            issues.append('original native command stream differs')
        if x['statuses']!=y['statuses']:
            issues.append('native decision sequence differs')
        if x['original_artifact_requests'] and x.get('artifact_responses')!=y.get('artifact_responses'):
            artifacts.append(dict(stock=x['path'],method=y['path'],reason='requested artifact raw differs; semantic review required'))
        elif x['original_artifact_requests'] and (not x.get('artifact_responses') or x['artifact_responses'].get('framing_equal') is not True):
            artifacts.append(dict(stock=x['path'],method=y['path'],reason='requested artifact framing unresolved'))
    return dict(basic_equal=not issues,issues=sorted(set(issues)),
                artifact_review_required=artifacts,performance_valid=not issues and not artifacts)


def resources(path):
    rows,issues = [],[]
    try:
        with gzip.open(path,'rt') as f:
            for line in f:
                row = json.loads(line)
                rows.append(row)
    except (OSError,ValueError,EOFError) as e:
        issues.append(repr(e))
    sums = {key:[sum(p[key] for p in row['processes'] if key in p) for row in rows]
            for key in ('pss_kib','private_kib','rss_kib')}
    return dict(samples=len(rows),incomplete=sum(r.get('incomplete_processes',0)>0 for r in rows),
                issues=issues,peak_observed={key:max(value,default=None) for key,value in sums.items()},
                limits='One-second non-atomic tree; short-lived processes and unsampled peaks can be missed. Observer CPU separate.')


def engagement(directory,method,sources):
    """Describe existing native acknowledgements/events, never invent counters."""
    receipts = [r['value'] for s in sources for r in s.get('native_receipts',[])]
    routes, fallback = Counter(),Counter()
    accepted, complete, prefix_bytes, prefix_hashes = [],[],[],set()
    for r in receipts:
        route = r.get('route')
        name = route.get('route') if isinstance(route,dict) else route
        routes[str(name)] += 1
        if name=='stock':
            fallback[str(route.get('reason','unrecorded'))] += 1
        if name=='branch' and r.get('method')==method:
            accepted.append(r)
            prefix_bytes.append(route.get('prefix_bytes'))
            if route.get('prefix_sha256'):
                prefix_hashes.add(route['prefix_sha256'])
            terminal = r.get('terminal') or {}
            if terminal.get('native_terminal_kind')==2 and r.get('native_exit_code') is not None:
                complete.append(r)
    event_path = directory/'service/service.jsonl'
    events, errors = [],[]
    if method!='stock':
        try:
            with event_path.open() as f:
                for line in f:
                    events.append(json.loads(line))
        except (OSError,ValueError) as e:
            errors.append(repr(e))
    preparations = [e for e in events if e.get('kind')=='parent-preparation']
    lookups = [e for e in events if e.get('kind')=='online-lookup']
    earlier_sources = {e.get('sequence'):e.get('source_sha256') for e in lookups}
    prior = [e for e in lookups if isinstance(e.get('earlier_witness'),int) and
             isinstance(e.get('sequence'),int) and e['earlier_witness']<e['sequence'] and
             isinstance(e.get('prefix_bytes'),int) and e['prefix_bytes']>0 and
             isinstance(e.get('source_sha256'),str) and
             isinstance(earlier_sources.get(e['earlier_witness']),str) and
             earlier_sources[e['earlier_witness']]!=e['source_sha256']]
    active = [e for e in preparations if e.get('supported') is True]
    def sum_observed(rows,key):
        values = [e[key] for e in rows if isinstance(e.get(key),(int,float))]
        return dict(observed=len(values),missing=len(rows)-len(values),sum=sum(values))
    return dict(method=method,native_receipts=len(receipts),routes=dict(routes),fallback_reasons=dict(fallback),
        acknowledged_reuse_sessions=len(accepted),terminal_reuse_sessions=len(complete),
        observed_prefix_bytes=quantiles([x for x in prefix_bytes if isinstance(x,(int,float))]),
        unique_observed_prefix_hashes=len(prefix_hashes),service_event_counts=dict(Counter(e.get('kind') for e in events)),
        service_lookup_routes=dict(Counter(str(e.get('route')) for e in lookups)),
        parent_misses=sum(e.get('parent_miss') is True for e in lookups),
        parent_hits=sum(e.get('parent_miss') is False for e in lookups),
        earlier_source_prefix_witnesses=len(prior),supported_parent_preparations=len(active),
        native_parent_preparation_wall_s=sum_observed(preparations,'native_wall_s'),
        native_parent_preparation_cpu_s=sum_observed(preparations,'native_cpu_s'),
        native_terminal_suffix_wall_s=sum_observed([r.get('terminal') or {} for r in complete],'native_wall_s'),
        native_terminal_suffix_cpu_s=sum_observed([r.get('terminal') or {} for r in complete],'native_cpu_s'),
        intended_mechanism_engaged=(bool(complete) and bool(active) and bool(prior) and not errors) if method!='stock' else bool(receipts),
        actual_fork_call_counter=None,actual_solver_translate_call_counter=None,
        exact_counter_limit='Current receipts acknowledge branch/logical sessions and terminal work; no independent fork/translate-call counter is emitted. Logical service route is named branch in the shared transport protocol.',
        raw_service_events=str(event_path) if method!='stock' else None,errors=errors)


def measured_cpu(receipt):
    keys = ('waited_tree_user_cpu_s','waited_tree_system_cpu_s','acquisition_observer_cpu_s')
    values = [receipt.get(k) for k in keys]
    return sum(values) if all(isinstance(v,(int,float)) for v in values) else None


def paired_comparison(name,baseline,method,expected,role):
    rows = [dict(candidate=a['candidate'],**compare(a,b))
            for a,b in zip(baseline.get('sources',[]),method.get('sources',[]))]
    ar,br = baseline.get('receipt',{}),method.get('receipt',{})
    identity_errors = []
    for key in ('affinity','source_order','candidates','repetition','profile'):
        if ar.get(key)!=br.get(key):
            identity_errors.append('paired complete-block identity differs: '+key)
    if ar.get('source_order')!=expected or br.get('source_order')!=expected:
        identity_errors.append('complete-block original source order unavailable/different')
    if not ar.get('affinity') or not br.get('affinity'):
        identity_errors.append('actual paired CPU affinity unavailable')
    a,b = ar.get('whole_wall_s'),br.get('whole_wall_s')
    if not all(isinstance(v,(int,float)) and math.isfinite(v) and v>0 for v in (a,b)):
        identity_errors.append('complete original whole clocks unavailable')
    numerical_valid = (baseline['complete'] and method['complete'] and len(rows)==len(expected)
                       and all(r['performance_valid'] for r in rows) and not identity_errors)
    engagement_missing = [c['name'] for c in (baseline,method)
       if not c['name'].endswith('-stock') and not c.get('engagement',{}).get('intended_mechanism_engaged')]
    valid = numerical_valid and not engagement_missing
    cpu_a,cpu_b = measured_cpu(ar),measured_cpu(br)
    peak_deltas = {}
    if ar.get('profile'):
        for key in ('pss_kib','private_kib','rss_kib'):
            ra = (baseline.get('resources') or {}).get('peak_observed',{}).get(key)
            rb = (method.get('resources') or {}).get('peak_observed',{}).get(key)
            peak_deltas[key] = dict(baseline_observed_peak=ra,method_observed_peak=rb,
                observed_reduction_percent=100*(ra-rb)/ra if valid and ra and rb is not None else None)
    return dict(name=name,baseline=baseline['name'],method=method['name'],comparison_role=role,
        valid_basic=len(rows)==len(expected) and all(r['basic_equal'] for r in rows),
        identity_errors=identity_errors,source_comparisons=rows,complete_cost_observation_valid=numerical_valid,
        intended_mechanism_missing=engagement_missing,performance_valid=valid,
        whole_baseline_s=a,whole_method_s=b,whole_reduction_percent=100*(a-b)/a if valid else None,
        measured_total_owned_cpu_baseline_s=cpu_a,measured_total_owned_cpu_method_s=cpu_b,
        measured_total_owned_cpu_reduction_percent=100*(cpu_a-cpu_b)/cpu_a if valid and cpu_a and cpu_b is not None else None,
        source_latency_baseline=baseline.get('elapsed_distribution'),source_latency_method=method.get('elapsed_distribution'),
        resources_baseline=baseline.get('resources'),resources_method=method.get('resources'),
        separate_profile_observed_memory_differences=peak_deltas if ar.get('profile') else None,
        resource_comparison_scope='One separate instrumented pair; sampled observed KiB peaks, incomplete/non-atomic sampling retained. Not primary replicated memory or an exact peak.' if ar.get('profile') else None)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args = p.parse_args()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    meta = json.loads((args.run/'metadata.json').read_text())
    expected = [c['index'] for c in meta['candidates']]
    conditions, by_name = [],{}
    preflight = meta['arguments'].get('preflight',False)
    names = [f'rep{rep}-{m}' for rep in range(1 if preflight else 3) for m in METHODS]
    if not preflight:
        names += ['profile-'+m for m in METHODS]
    for name in names:
        directory = args.run/name
        condition = dict(name=name,expected_sources=len(expected),issues=[])
        try:
            condition['receipt'] = json.loads((directory/'receipt.json').read_text())
        except (OSError,ValueError) as e:
            condition['issues'].append(repr(e))
        if 'receipt' in condition:
            condition['sources'] = [source(directory,index) for index in expected]
            condition['source_issues'] = sum(bool(row['issues']) for row in condition['sources'])
            condition['terminal_sources'] = sum(bool(row.get('terminal')) for row in condition['sources'])
            condition['elapsed_distribution'] = quantiles([row['external_wall_s'] for row in condition['sources']
                                                   if isinstance(row.get('external_wall_s'),(int,float))])
            condition['observed_exits'] = dict(Counter(str(row.get('returncode')) for row in condition['sources']))
            condition['observed_solver_sessions'] = sum(len(row['native_sessions']) for row in condition['sources'])
            condition['engagement'] = engagement(directory,name.rsplit('-',1)[1],condition['sources'])
            condition['complete'] = bool(condition['receipt'].get('terminal')) and condition['terminal_sources']==len(expected) and condition['source_issues']==0
            if name.startswith('profile-'):
                condition['resources'] = resources(directory/'resources.jsonl.gz')
                if condition['resources']['issues'] or not condition['resources']['samples']:
                    condition['issues'].append('resource profile missing/truncated; preserve native outcomes separately')
                    condition['complete'] = False
        else:
            condition['complete'] = False
        conditions.append(condition)
        by_name[name] = condition
    comparisons = []
    for name,other in by_name.items():
        if name.endswith('-stock'):
            continue
        stock = by_name[name.rsplit('-',1)[0]+'-stock']
        comparisons.append(paired_comparison(name,stock,other,expected,'Stock native behavior/current-practice reference; alone insufficient for superiority over reuse'))
    for group in [f'rep{i}' for i in range(1 if preflight else 3)]+([] if preflight else ['profile']):
        direct = paired_comparison(group+'-branch-vs-logical',by_name[group+'-logical'],
            by_name[group+'-branch'],expected,'Primary mechanism comparison against actual complete logical-copy/translation reuse')
        references = [c for c in comparisons if c['name'] in (group+'-branch', group+'-logical')]
        stock_fidelity = len(references)==2 and all(c['complete_cost_observation_valid'] for c in references)
        direct['both_methods_pass_complete_stock_reference'] = stock_fidelity
        direct['stock_reference_comparisons'] = [c['name'] for c in references]
        if not stock_fidelity:
            direct['performance_valid'] = False
            direct['whole_reduction_percent'] = None
            direct['measured_total_owned_cpu_reduction_percent'] = None
            for memory in (direct['separate_profile_observed_memory_differences'] or {}).values():
                memory['observed_reduction_percent'] = None
        comparisons.append(direct)
    # Authoritative outputs remain source ZIPs. Keep reproducible per-source
    # recomputation compressed instead of duplicating huge raw JSON in summary.
    source_analysis = args.out.with_name(args.out.stem+'-sources.jsonl.gz')
    with gzip.open(source_analysis,'wt',compresslevel=6) as f:
        for condition in conditions:
            for row in condition.get('sources',[]):
                f.write(json.dumps(dict(condition=condition['name'],**row))+'\n')
    for condition in conditions:
        condition.pop('sources',None)
    for comparison in comparisons:
        rows = comparison.pop('source_comparisons')
        comparison['compared_sources'] = len(rows)
        comparison['basic_equal_sources'] = sum(row['basic_equal'] for row in rows)
        comparison['differences_or_artifact_review'] = [row for row in rows if not row['performance_valid']]
    report = dict(metadata=meta,conditions=conditions,comparisons=comparisons,
                  complete_source_recomputation=str(source_analysis),
                  expected_conditions=len(names),complete_conditions=sum(c['complete'] for c in conditions),
                  complete=all(c['complete'] for c in conditions),
                  primary_boundary='Whole method startup/all originals/native transport/cleanup plus same raw archival; profiles separate',
                  note='Basic/raw comparison is necessary evidence, not a result review, RQ answer or acceptance claim.')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
