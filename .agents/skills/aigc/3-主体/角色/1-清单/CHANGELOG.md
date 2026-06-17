# Changelog

## 2026-06-16

- 新增多状态 / 多服装 / 年龄阶段变体归并合同：常服、礼服、战斗态、战损态、受伤态、少年期、老年期等默认作为同一 base character 的 `variant_state`，不得拆成新角色行。
- 同步 `SKILL.md`、source/merge reference、review、模板、types、CONTEXT、knowledge-base、README、入口元数据、legacy workflow 和测试 prompt；新增 `FAIL-CHAR-LIST-VARIANT-SPLIT` / `FAIL-CHAR-LIST-VARIANT-OMISSION`。
- 升级为 runtime-spine Skill 2.0 口径，补齐业务分析、类型路由、思行节点、模块触发、汇流门、review gate、量化标准、注意力协议、检查点和测试 prompts。
- 将历史 workflow 文件迁移为 `references/legacy-character-list-workflow.md`，保留旧语义但不再作为第二执行主链。
- 强化 LLM-first 作者性门禁：角色归并、首次登场和关键词描述必须由 LLM 逐条裁决，脚本只能做读取、校验和风险提示。

## 2026-04-26

- 补齐 `SKILL.md` 的 topology contract、mermaid 主流程图、身份分型图和验收状态图。
- 强化历史 workflow（现迁移为 `references/legacy-character-list-workflow.md`）：增加业务需求分析、思行拓扑图、节点 `route_out` 与失败回路。
- 强化 `review/review-contract.md`：增加默认辅助 reviewer、review flow mermaid 和 finding shape。
- 在 `README.md` 增加快速视觉总览，便于批量定制后的人工核查。

## 2026-04-25

- 初始化 `角色/1-清单` Skill 2.0 包结构。
- 建立上游 `8-分组` 组底 YAML `角色` 字段到角色清单的业务合同。
- 固定 canonical 输出路径、三列表格字段、别名归并规则和 LLM-first 边界。
