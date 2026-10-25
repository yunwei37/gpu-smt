# Daily open-source organization and progress reflection

The root is now a Rust workspace with four crates. Source/data experiments stay
in their established directories. README gains actual build/usage/layer/status
links; architecture/API/contribution/license/CI/examples/benchmark are explicit.
The formerly491-line implementation frontier is archived byte-for-byte and
replaced with a current concise implementation/resource/test status. Foreign
dirty files and raw results are preserved.

怎样才能取得实质进展：当前卡点不在更多文献或窄GPU内核，而在原生验证工作
如何在48GiB/4核下调度、回收、复用且保持每个候选语义。先把这些行为做成
可复用、可测的Rust接口，避免实验脚本各自改资源语义。下一步最有希望的是
在已有采集结束后，用同一引擎做42条资源失败的无24GiB上限独占重跑与真实
native差分，再实现安全的单次Mathlib准备/COW；失败检测继续针对已测
interval_cases/simp热点寻找充分证据，不能用预测或短超时冒充判死。
先用真实差分/内存日志确认行为，再在相同48GiB/4核上做完整吞吐配对。
普通缓存、预热和COW只是资源层基础，不当novelty；当前接口与测试不等于
已实现COW或研究成功。四方向持续，无关口/截止/收尾，CPUoracle保持冻结。


## Following the reflection: exact duplicates measured

The reusable Rust engine and measurement API now exist, rather than remaining
an architecture document. Existing-data analysis finds only 17 redundant literal
None failures (0.03093% of cumulative HTTP spans), so exact caching cannot carry
the miniF2F performance story. Main uncertainty remains whole-population
throughput/decision differences under dynamic 48GiB admission, and then safe
native preparation plus workload-aware gains. Next real native work is 42 isolated
resource reruns after the healthy old group retires, followed by a matched engine
qualification/full pair. Continue source-level failure and code-workload work
without an additional simultaneous collection or CPU oracle changes.

## Following the reflection: native prepared import boundary

可选 Lean+C 导入父进程已完成实际 Lean4.18 差分和生命周期 CI，Rust 核心/接口
检查也通过。默认仍为 fresh backend；此前构建、初始化和继承 FD 故障全部保留。
这一步把接口变成了真实可运行组件，但还没有 Mathlib/48GiB 吞吐数据。
剩余主线仍是旧全量结束后一次收结果、42条独占重跑、同资源全量配对；不能把
固定 Init 控制当作全体验证加速。今日核心文档45个相对链接存在；真实原生测试
命令已按 fresh/optional prepared 拆开，避免缺少可选环境时失败。
