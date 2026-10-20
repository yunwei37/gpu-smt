"""Source-level work counts in the closed E1074 four-condition ablation."""
from pathlib import Path
import collections,csv,gzip,json
A=Path(__file__).resolve().parent
def rows(path):
 if not path.exists():path=path.with_name(path.name+".gz")
 with(gzip.open(path,"rt")if path.suffix==".gz"else path.open())as stream:
  return [json.loads(line)for line in stream if line.strip()]
inputs=rows(A.parents[2]/"input-top1000.jsonl")
header="import Mathlib\nimport Aesop\n"
assert all(x["code"].startswith(header)for x in inputs)
source_id={"\n\n"+x["code"][len(header):]:x["proof_id"]for x in inputs}
assert len(source_id)==len(inputs)==1000
selected={x["proof_id"]for x in rows(A/"input-affected111.jsonl")}
assert len(selected)==111 and selected<=set(source_id.values())
previous=json.loads((A/"full1000-result.json").read_text())
assert previous["state"]=="complete"
data={}
for method in ["native-dual","direct","power"]:
 cell=A/"full1000-raw"/method/"rep1-oracle-highs"
 races=rows(cell/"lp-races.jsonl")
 per={x["proof_id"]:dict(races=0,winners=collections.Counter(),race_wall_seconds=0,
  child_CPU_seconds=0,cancelled_child_CPU_seconds=0,reaped_children=0,rows_sum=0,columns_sum=0)
  for x in inputs}
 children=set()
 for x in races:
  ident=source_id[x["source"]];entry=per[ident]
  entry["races"]+=1;entry["winners"][x["winner"]]+=1
  entry["race_wall_seconds"]+=x["whole_ns"]/1e9
  entry["rows_sum"]+=x["rows"];entry["columns_sum"]+=x["cols"]
  for role in ["cpu","gpu","strong_cpu"]:
   child=x.get(role+"_exit")
   if not isinstance(child,dict):continue
   assert child["pid"]not in children and not child.get("wait_error")and not child.get("kill_error")
   children.add(child["pid"]);entry["reaped_children"]+=1
   cpu=(child["wait4_user_cpu_ns"]+child["wait4_system_cpu_ns"])/1e9
   entry["child_CPU_seconds"]+=cpu
   if child["signal"]is not None:entry["cancelled_child_CPU_seconds"]+=cpu
 assert all(x["rows"]>=11 for x in races)
 assert len(races)==sum(x["races"]for x in per.values())==previous["methods"][method]["numeric_races_observed"]
 data[method]=per
groups={"previously_identified_fallback111":selected,"remaining889":set(source_id.values())-selected}
result=dict(scope="Closed E1074 source-attributed work counts. Previous111selection, all1000retained; root self-review. Not all-call LP/CPU coverage or a causal wall/GPU bound.",groups={},whole_seconds={m:v["whole_seconds"]for m,v in previous["methods"].items()})
for name,ids in groups.items():
 out=dict(sources=len(ids),methods={})
 for method,per in data.items():
  winners=collections.Counter()
  for ident in ids:winners.update(per[ident]["winners"])
  sums={k:sum(per[i][k]for i in ids)for k in["races","race_wall_seconds","child_CPU_seconds","cancelled_child_CPU_seconds","reaped_children","rows_sum","columns_sum"]}
  sums.update(source_IDs_with_recorded_race=sum(per[i]["races"]>0 for i in ids),winners_legacy=dict(winners))
  out["methods"][method]=sums
 out["direct_to_power_count_change"]={k:out["methods"]["power"][k]-out["methods"]["direct"][k]for k in["races","reaped_children","rows_sum","columns_sum"]}
 out["source_count_with_lower_direct_to_power_races"]=sum(data["power"][i]["races"]<data["direct"][i]["races"]for i in ids)
 out["source_count_with_higher_direct_to_power_races"]=sum(data["power"][i]["races"]>data["direct"][i]["races"]for i in ids)
 out["same_ID_overlapping_service_seconds"]={m:sum(previous["methods"][m]["source_service_seconds"][i]for i in ids)for m in previous["methods"]}
 out["source_count_with_longer_Power_service_than_direct"]=sum(previous["methods"]["power"]["source_service_seconds"][i]>previous["methods"]["direct"]["source_service_seconds"][i]for i in ids)
 result["groups"][name]=out
result["source_IDs_with_changed_recorded_race_count"]=[i["proof_id"]for i in inputs if data["power"][i["proof_id"]]["races"]!=data["direct"][i["proof_id"]]["races"]]
result["changed_count_IDs_outside_previous111"]=[i for i in result["source_IDs_with_changed_recorded_race_count"]if i not in selected]
result["recording_boundary"]="race_eligible selects rows>=11; smaller problems use cpu_or_decline, and spawn failure may bypass the recorded race. Reductions can include routing below the threshold, not eliminated all-call LP work."
result["total_recorded_races"]={m:sum(x["races"]for x in per.values())for m,per in data.items()}
result["recorded_race_reduction_percent"]=100*(1-result["total_recorded_races"]["power"]/result["total_recorded_races"]["direct"])
result["total_sources_with_fewer_recorded_races"]=sum(data["power"][x["proof_id"]]["races"]<data["direct"][x["proof_id"]]["races"]for x in inputs)
result["total_sources_with_more_recorded_races"]=sum(data["power"][x["proof_id"]]["races"]>data["direct"][x["proof_id"]]["races"]for x in inputs)
result["reduced_race_IDs_with_longer_Power_service"]=sum(previous["methods"]["power"]["source_service_seconds"][i]>previous["methods"]["direct"]["source_service_seconds"][i]for i in result["source_IDs_with_changed_recorded_race_count"])
with(A/"source-mechanism.csv").open("w",newline="")as stream:
 fields=["proof_id","previous_fallback111"]
 for method in data:
  fields.extend(method+"_"+k for k in["races","external_infeasible","cpu_no_certificate","child_CPU_seconds","reaped_children","rows_sum","columns_sum"])
 fields.extend(m+"_service_seconds"for m in previous["methods"])
 writer=csv.DictWriter(stream,fieldnames=fields,lineterminator="\n");writer.writeheader()
 for item in inputs:
  ident=item["proof_id"];row=dict(proof_id=ident,previous_fallback111=int(ident in selected))
  for method,per in data.items():
   entry=per[ident]
   for key in["races","child_CPU_seconds","reaped_children","rows_sum","columns_sum"]:row[method+"_"+key]=entry[key]
   row[method+"_external_infeasible"]=entry["winners"]["external-infeasible"]
   row[method+"_cpu_no_certificate"]=entry["winners"]["cpu-no-certificate"]
  for method in previous["methods"]:row[method+"_service_seconds"]=previous["methods"][method]["source_service_seconds"][ident]
  writer.writerow(row)
(A/"source-mechanism.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items()if k not in["source_IDs_with_changed_recorded_race_count","changed_count_IDs_outside_previous111"]},indent=2))
