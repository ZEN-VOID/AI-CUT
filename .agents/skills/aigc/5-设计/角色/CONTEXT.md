# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc-design-role` 的经验层知识库，不是执行日志。
- 调用 `.agents/skills/aigc/5-设计/角色/SKILL.md` 时，必须同时加载本文件。
- 旧 `1-清单/角色`、`2-设计/角色`、`3-面板/角色` 的经验已归档到 `references/legacy/legacy-*-CONTEXT.md`，只在追溯旧行为时读取。

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
| `ROLE-TM-01` | 角色输出仍散落在 `角色/1-清单`、`角色/2-设计`、`角色/3-面板` | 收束到 `projects/aigc/<项目名>/4-设计/` 根，并保留旧 JSON 为兼容侧车 | 根目录存在 `角色清单.md`、`[角色名].md`、`[角色名].json` |
| `ROLE-TM-02` | 动作、环境或服装残片被升格成角色名 | 回到 `object-normalization-contract.md` 和 `detail-role-normalization.md` | `角色清单.md` 的主体身份稳定 |
| `ROLE-TM-03` | 设计文档缺 Personality、Costume、Cinematography 或 `prompt整合` | 回到 `templates/character_masterprompt.structured.v2.md` 重投影 | validator 通过 |
| `ROLE-TM-04` | 面板 JSON 在角色设计后重新发明服装或身份 | 回到 `[主体名].md` 的 `prompt整合`，面板只做 layout/prompt handoff | JSON prompt 回链同 stem Markdown |

## Repair Playbook

1. 先判定故障属于路径漂移、角色抽取、设计模板、面板 JSON 或 imagegen handoff。
2. 身份漂移优先修清单阶段 LLM 判断和 role alias 合并，不靠面板阶段补救。
3. 模板漂移只改 `templates/character_masterprompt.structured.v2.md` 和 renderer/validator。
4. 面板失败先确认 `[主体名].json` 是否与 `[主体名].md` 同 stem、同角色、同 prompt 来源。

## Reusable Heuristics

- 角色清单必须保留身份、服装状态、镜头证据与别名归并。
- 角色设计文档要让面部、发型、体态、服装和镜头可读性一起成立。
- 面板提示词消费角色设计，不应在面板阶段新造人物关系。
