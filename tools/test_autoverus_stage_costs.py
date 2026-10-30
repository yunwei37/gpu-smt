"""Timer regressions: nested fields, absent diagnostics, incompatible clocks."""
import importlib.util
from pathlib import Path
import unittest
p = Path(__file__).with_name("analyze_autoverus_stage_costs.py")
s = importlib.util.spec_from_file_location("stage_costs", p)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)

class StageCostTests(unittest.TestCase):
    def cell(self):
        return {"external_wall_s": .15, "native_json": {"times-ms": {
            "num-threads": 1, "total": 130, "rust": {"total": 29},
            "verification": {"total": 99, "vir": {"total": 67, "hir": 2, "import": 28}},
            "air": {"total": 14}, "smt": {"smt-init": 3, "smt-run": 2, "total": 5}}}}
    def test_nested_children_not_added(self):
        x=m.partition(self.cell())
        self.assertAlmostEqual(x["residual_s"], .015)
        self.assertAlmostEqual(sum(x[k] for k in ("rust_s","vir_s","air_excluding_smt_s","smt_init_s","smt_run_s","residual_s")), .13)
    def test_absent_json_is_unknown(self):
        self.assertIsNone(m.partition({"external_wall_s": .01})["native_s"])
    def test_absent_smt_stays_unknown(self):
        c=self.cell(); del c["native_json"]["times-ms"]["smt"]
        x=m.partition(c)
        self.assertIsNone(x["smt_run_s"])
        self.assertAlmostEqual(x["residual_s"], .020)
    def test_parallel_point_rejected(self):
        c=self.cell();c["native_json"]["times-ms"]["num-threads"]=2
        with self.assertRaises(ValueError):m.partition(c)
    def test_overlap_rejected(self):
        c=self.cell();c["native_json"]["times-ms"]["total"]=10
        with self.assertRaises(ValueError):m.partition(c)

if __name__ == "__main__":unittest.main()
