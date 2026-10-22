/- gpu-smt reproduction snapshot; local Lean4.27 adaptation/reduced diagnostic implementation. See ../../PROVENANCE.md. -/
import Farkas.Telemetry
namespace GpuArithmetic.CostTelemetry
@[extern "gpu_smt_cost_emit"] opaque emit (s : String) : IO Unit
@[extern "gpu_smt_stage_emit"] opaque emitStage (s : String) : IO Unit
end GpuArithmetic.CostTelemetry
