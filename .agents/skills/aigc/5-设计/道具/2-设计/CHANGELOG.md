# Changelog: aigc 道具 2-设计

## 2026-04-26

- 升级研究层合同：研究必须形成 `source cue -> confidence -> visual translation -> design lock -> prompt evidence token` 链路。
- 在 `references/`、`steps/`、`types/`、`review/` 与模板中补齐形制、材料、工艺、年代、使用痕迹、功能逻辑、风险/不确定性和 prompt evidence chain 的规则与验收。
- 强化 LLM-first 边界：脚本只能检查研究链字段和 prompt 字符数，不得判断研究置信度或代写创作正文。
- 保持纯色背景单道具 45 度近景约束，并将该约束写入 prompt evidence chain 与 review gate。

## 2026-04-25

- 初始化 Skill 2.0 包结构，补齐 canonical 分区与根文件。
- 建立 `SKILL.md + CONTEXT.md` 成对加载合同、LLM-first 创作边界和 subagent 默认执行合同。
- 定义上游 `道具/1-清单` 消费、`north_star.yaml` / `team.yaml` 监制上下文读取、单道具 Markdown 输出路径和 prompt 2000 字符门禁。
- 新增 references、steps、types、review、templates、knowledge-base、scripts、agents 元数据。
- 固定道具设计画面约束为纯色背景单道具近景特写、45 度视角，不置身剧情场景、桌面环境、室内陈设、街景或人物手持情境。
- 补齐工作车间要求的关键 Mermaid 图谱：根执行拓扑、来源汇入、LLM-first 边界、类型分流、审查汇流与 README 可视化入口。
