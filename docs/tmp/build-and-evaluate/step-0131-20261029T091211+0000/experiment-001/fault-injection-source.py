import importlib.util,sys,json,traceback
from pathlib import Path
spec=importlib.util.spec_from_file_location("state_measure_test", "/workspaces/repository/bench/lean-failure-profile/state-reuse/run.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.BUDGET=128*1024**2
error=None
try:
    module.main()
except BaseException:
    error=traceback.format_exc()
    raise
finally:
    if module.RUN_OUTPUT:
        (module.RUN_OUTPUT/"injection.json").write_text(json.dumps(dict(
            test_local_budget_bytes=module.BUDGET,actual_collection_budget_bytes=48*1024**3,
            production_source_budget_changed=False,error=error))+"\n")
        (module.RUN_OUTPUT/"client-exit.json").write_text(json.dumps(dict(error=error))+"\n")
