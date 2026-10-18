import Farkas.Telemetry
namespace GpuArithmetic.CostTelemetry
@[extern "gpu_smt_cost_emit"] opaque emit (s : String) : IO Unit
end GpuArithmetic.CostTelemetry
