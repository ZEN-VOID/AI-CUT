# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-design-prop` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/4-Design/道具/SKILL.md` 时，必须同时加载本文件。
- 旧 `1-清单/道具`、`2-设计/道具`、`3-面板/道具` 的经验已归档到 `references/legacy/legacy-*-CONTEXT.md`，只在追溯旧行为时读取。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 20000
hard_limit_chars: 40000
status: ok
recommended_action: keep-domain-scoped
last_checked_at: 2026-04-24
```

## Type Map

| type_id | 触发症状 | 立即修复 | 验证点 |
| --- | --- | --- | --- |
| `PROP-TM-01` | 道具输出仍散落在 `道具/1-清单`、`道具/2-设计`、`道具/3-面板` | 收束到 `projects/aigc/<项目名>/4-Design/` 根，并保留旧 JSON 为兼容侧车 | 根目录存在 `道具清单.md`、`[道具名].md`、`[道具名].json` |
| `PROP-TM-02` | 状态句或使用动作被升格成道具名 | 回到 `object-normalization-contract.md` | 主体名是物件实体 |
| `PROP-TM-03` | 设计文档缺 Photography、Prop Design 或 `prompt整合` | 回到 `templates/prop_masterprompt.structured.v2.md` 重投影 | 文档结构稳定 |
| `PROP-TM-04` | 面板 JSON 把手、人物或使用者写进主体 | 回到 `[主体名].md` 的 pure prop guardrail | JSON prompt 保持 isolated pure prop view |

## Repair Playbook

1. 先判定故障属于路径漂移、道具抽取、设计模板、面板 JSON 或 imagegen handoff。
2. 道具主体漂移优先修清单阶段 LLM 判断，不在设计阶段硬改文件名。
3. 模板漂移只改 `templates/prop_masterprompt.structured.v2.md` 和 renderer。
4. 面板失败先确认 `[主体名].json` 是否与 `[主体名].md` 同 stem、同道具、同 prompt 来源。

## Reusable Heuristics

- 道具主体必须是可被单独拍摄的物件，而不是动作或状态。
- `prompt整合` 必须保留功能、材质、工艺、状态痕迹和无手无人约束。
- 面板提示词消费道具设计，不反向发明道具用途。
