# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-design-scene` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/4-Design/场景/SKILL.md` 时，必须同时加载本文件。
- 旧 `1-清单/场景`、`2-设计/场景`、`3-面板/场景` 的经验已归档到 `references/legacy/legacy-*-CONTEXT.md`，只在追溯旧行为时读取。

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
| `SCENE-TM-01` | 场景输出仍散落在 `场景/1-清单`、`场景/2-设计`、`场景/3-面板` | 收束到 `projects/aigc/<项目名>/4-Design/` 根，并保留旧 JSON 为兼容侧车 | 根目录存在 `场景清单.md`、`[场景名].md`、`[场景名].json` |
| `SCENE-TM-02` | 场景名从角色动作句或背景整句中膨胀出来 | 回到 `object-normalization-contract.md` 和 `detail-scene-normalization.md` | 场景主体名是空间实体，不是动作描述 |
| `SCENE-TM-03` | 设计文档缺 `Scene Design / Cinematography / prompt整合` | 回到 `templates/scene_masterprompt.structured.v2.md` 重投影 | validator 通过 |
| `SCENE-TM-04` | 面板 JSON 重新设计场景事实 | 回到 `[主体名].md` 的 `prompt整合`，面板只做 layout/prompt handoff | JSON prompt 回链同 stem Markdown |

## Repair Playbook

1. 先判定故障属于路径漂移、对象抽取、设计模板、面板 JSON 或 imagegen handoff。
2. 路径漂移优先修 `SKILL.md` Output Contract 与 `references/processing-order.md`。
3. 对象抽取错误优先修清单阶段 LLM 判断，不把脚本 heuristics 升为主创真源。
4. 模板漂移只改 `templates/scene_masterprompt.structured.v2.md` 和 renderer/validator，不在业务文档里开第三套结构。
5. 面板失败先确认 `[主体名].json` 是否与 `[主体名].md` 同 stem、同主体、同 prompt 来源。

## Reusable Heuristics

- 场景清单的关键不是列尽背景句，而是收束可复用空间主体。
- 场景设计文档必须先能作为单主体环境设计卡阅读，再作为图像 prompt 被消费。
- 面板提示词不应补写新世界观；它只把当前场景设计转成 16:9 面板请求。
