# Existing heartbeat update

The app tool confirms updating gpu-smt-osdi in place, retaining ACTIVE, the same thread and hourly interval. No new schedule or model. Notification policy is unchanged. The saved prompt is:

持续推进 yunwei37/gpu-smt 的 Lean 优先完整研究、真实标准工作负载实验和 docs/paper/ 论文，目标为 OSDI 水平的系统贡献。复用 yunwei356/gpu-smt-dev 的 /workspaces/repository，GPU 仅用 RTX 5090；沿用 main 和已有 Workspace，不创建替代 checkout、Workspace 或调度。

用户最新明确要求所有工作由本聊天线程的本机 Codex 自己完成：实现、实验、分析、文档、论文、复核和审计都在本线程执行，禁止 OMP、其他 Agent、Codex subagent 和原生研究会话启动或恢复。所有原会话状态和已有复核记录保留；不切 zai，不再使用 OMP。自己执行的复核明确标为自审，不冒充独立审计。

从最新 Markdown step report 和 route-closure-20261017T0127 关闭记录恢复，使用 auto-research-orchestrator 及配套技能。CPU 原生分支运行时 E038 路线已由用户要求关闭：d5665ff 的24源两序诊断没有稳定优于 stock；旧 eager-v1 全量采集已按用户要求停止，完整和部分原始数据保留为已知慢版本的部分结果。不得恢复该矩阵，不得启动新的全量矩阵，除非真实匹配预检先显示收益并有完整成本依据；不继续开不出收益的小变体、缓冲区/缓存/线程网格或窄 GPU kernel。

下一主线是判断真实 Lean 验证流程还有没有能超过现有服务、缓存和快照工作的重大系统机会。先使用已有真实数据和官方实现找出可消除的昂贵工作、与最强 warm/native 基线的差异以及可证伪机制；不能证明机会就如实保留负结论，不以普通 CPU 编译优化或更多报告代替新贡献。新机制的真实端到端预检必须包括准备、打包、传输、fallback、排队和清理成本。四个原 RQ、Lean/SMT 和论文目标保留，不因为测试成功声称 OSDI 接受。

GPU 现有结论要保留分母：defeq 的1.067–1.090×是跨采集假设下条件敏感性计算，不是实测加速或严格端到端上限；声明桥接14.53%、完整官方 Init4.84%、融合解析6.27%、回收后13.72%是相应观测/固定参考的 body-thread CPU 覆盖，未替代原生检查。回收构造耗时约1052秒且已关闭，不再移植 GPU。5090 当前是候选加速资源，尚无已证明的完整验证收益。

保留原始、失败、部分结果和现有作者文件。已停止 OMP 的故障输出无损归档清理，状态目录保留。后台有效的其他原始 CPU 采集只在实际终止时一次收结果，不用 goal 轮次轮询。按用户已完成部分即时入库要求提交并推送已验证的完整边界。复核和审计由本线程按证据完成，明确局限；不派生其他执行者。通知只在新研究结论、关键进展、完成、故障或需要用户处理时发送，无可行动变化保持安静。
