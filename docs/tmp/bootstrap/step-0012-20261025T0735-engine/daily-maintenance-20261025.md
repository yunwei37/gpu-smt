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
