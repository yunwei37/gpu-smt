# Disposable RTX 5090 cuOpt oracle target
Date: 2026-10-17. State: admitted finite benchmark, not a retained service.

## Authority and question
User: “如果上限够得着 1.5×，就实现 GPU 批量 oracle：批量 LP 用 cuOpt batch/PDLP 或自写求解器，浮点解只用来找支持集，CPU 做精确修复，Lean 照旧检查证书，失败就回退强基线。”
User: “全部由本线程自己完成，不用子代理、OMP 或其他 agent，每完成一步就 commit/push。”

Question: can robust GPU support search remove exact LP fallback cost and improve the fixed 1000-candidate end-to-end pipeline, including packing, transfer, queueing, repair, Lean checking, fallback and retirement? Final rule remains best(CPU, GPU)>1.5x; CPU=1.34668x is an intermediate result.

## Runtime and boundary
All source changes, builds, test clients and Lean processes remain in yunwei356/gpu-smt-dev, /workspaces/repository, main. Existing prefix PID5256 is preserved.
That CPU standard-dev Pod has no NVIDIA devices or libcuda. In-place GPU resize is unsupported by Kubernetes; no template/Workspace mutation or restart is made.
One disposable upstream NVIDIA server Job in coder is a numeric system under test, not another development environment. It has no project checkout, source build, Agent, PVC, Secret, Service, Ingress, host port or scheduled controller.
Use existing native time-slicing and one of two shared RTX5090 resources; one slot was free. Other GPU Workspace remains running. This does not reserve half the physical GPU.
Finite work ends after interface/repair qualification and the requested paired fixed-cohort GPU trial or a material failure; delete this Job and its Pods on completion/failure, and record restoration. No recurring service is retained.

## Upstream defaults and deliberate differences
Image nvidia/cuopt:26.10.0-cu12, pinned OCI index sha256:ed854f295ebc2323beee947cd3ade3cbab1aae6c559694983666ce4369365734; amd64 manifest sha256:60bc4a5409bd1489d117a1b268dac9ef98dc94097f9fcbdd281786bbed010658.
Registry config: entrypoint /opt/cuopt/entrypoint.sh, cmd proxy; CUDA12.9, Python3.14. Default proxy starts gRPC5001 and HTTP5000.
Preserve upstream startup through a shell wrapper solely for user-required 48GiB RLIMIT_AS (50331648 KiB) and zero core dumps. No CPU/memory K8s caps/reservations, no custom time budget, no credential/network/security change. Single attempt restartNever/backoffLimit0 preserves launch failures rather than hiding retries.
Hardware selector fleet.yunwei37.com/gpu=rtx5090, one device-plugin resource. No hostname pin.
All matrix requests and replies are private Pod-IP numeric payloads. GPU method must explicitly be PDLP; concurrent default can finish on CPU and cannot establish GPU attribution. Crossover supports sparse exact repair; failures still require strong native fallback. CPU robust support control is required.

## Entry evidence and cleanup
2026-10-17T23:29Z: lab Ready, driver610.57.04; node FS available443944341504 bytes and image FS348584890368 bytes; 2 allocatable shared GPUs, 1 allocated running. Existing source Workspace and other GPU Workspace preserved.
48GiB address cap applies to every new capture; exceeding it is a resource failure, never silently relaxed.
Cleanup: scripts/kubectl-home.ps1 -n coder delete job gpu-smt-cuopt-20261017. Verify Job/Pods gone, one prior running GPU Workspace unchanged, owning Workspace/prefix alive, lab Ready and disk headroom. Outcome remains open until restoration.

## Official provenance
- https://docs.nvidia.com/cuopt/user-guide/latest/cuopt-server/quick-start.html
- https://docs.nvidia.com/cuopt/user-guide/latest/cuopt-server/advanced.html
- https://docs.nvidia.com/cuopt/user-guide/latest/convex-features.html
- https://hub.docker.com/r/nvidia/cuopt/tags
- https://v1-36.docs.kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/

Self-review: requested disposable benchmark authority under spark-manage AGENTS.md section8; not a persistent configuration delta. No independent audit.

## First launch and repair
The first Job omitted the existing NVIDIA runtimeClass and failed CUDA driver initialization before any numeric request. Driver/device allocation alone did not mount NVIDIA libraries. Other GPU Workspace verifies runtimeClassName=nvidia. Corrected the Job to that existing hardware execution path, retaining the same 48GiB cap, image, device allocation, and server defaults. Initial failure log is preserved. No result from this launch enters performance.
