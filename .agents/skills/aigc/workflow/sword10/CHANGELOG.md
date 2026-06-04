# CHANGELOG

## 2026-06-04

- 将 workflow 包从 `sword6` 调整为 `sword10`，目录、技能 ID、入口元数据和输出路径同步改为 `sword10`。
- 将执行节点更新为 `2-编剧 -> 3-美学 -> 4-导演 -> 5-表演 -> 6-氛围 -> 7-分镜 -> 8-摄影 -> 9-光影 -> 10-分组`。
- 同步 stage handoff、resume matrix、dispatch packet、run ledger、output template、review gate、registry route 和 workflow carrier。
- 按 Skill 2.0 最新 runtime-spine 规范补齐 B1-B14 控制块：业务需求、量化标准、注意力协议、checkpoint 和评估 prompt 合同。
- 删除 `steps/` 第二节点真源，把执行拓扑与失败回路收回 `SKILL.md#Thinking-Action Node Map`。
- 新增 `test-prompts.json`，覆盖 bounded、batch、retry、blocked preflight 四类回归场景。

## 2026-05-31

- 将串行阶段链更新为 `2-编导 -> 3-运动 -> 4-摄影 -> 10-分组`。
- 同步 stage handoff、resume matrix、dispatch packet、run ledger、openai 入口元数据和经验层，确保 `4-摄影` 默认消费 `3-运动` 输出。

## 2026-05-27

- 初始化 `aigc-workflow-sword10` Skill 2.0 包。
- 固定 `2-编导 -> 3-运动 -> 4-摄影 -> 10-分组` 串行阶段链；旧 `3-导演` / `4-表演` 已并入 `2-编导`。
- 固定每阶段一集一个后台隔离 subagent，主窗口只做派发、追踪、汇流和下一阶段触发。
- 新增 subagent dispatch、stage handoff、steps、review、types、templates、guardrails 与入口元数据。
