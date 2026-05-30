# CHANGELOG

## 2026-05-27

- 初始化 `aigc-workflow-sword6` Skill 2.0 包。
- 固定 `2-编剧 -> 3-导演 -> 4-表演 -> 5-摄影 -> 6-分组` 串行阶段链。
- 固定每阶段一集一个后台隔离 subagent，主窗口只做派发、追踪、汇流和下一阶段触发。
- 新增 subagent dispatch、stage handoff、steps、review、types、templates、guardrails 与入口元数据。
