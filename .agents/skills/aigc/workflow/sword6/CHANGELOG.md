# CHANGELOG

## 2026-05-31

- 将串行阶段链更新为 `2-编导 -> 3-运动 -> 4-摄影 -> 5-分组`。
- 同步 stage handoff、resume matrix、dispatch packet、run ledger、openai 入口元数据和经验层，确保 `4-摄影` 默认消费 `3-运动` 输出。

## 2026-05-27

- 初始化 `aigc-workflow-sword6` Skill 2.0 包。
- 固定 `2-编导 -> 3-运动 -> 4-摄影 -> 5-分组` 串行阶段链；旧 `3-导演` / `4-表演` 已并入 `2-编导`。
- 固定每阶段一集一个后台隔离 subagent，主窗口只做派发、追踪、汇流和下一阶段触发。
- 新增 subagent dispatch、stage handoff、steps、review、types、templates、guardrails 与入口元数据。
