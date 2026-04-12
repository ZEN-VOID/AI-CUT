# AIGC Query System Data Flow

## Purpose

本文件定义 `aigc/query` 的最小数据流真源，回答“问什么就先去哪一层取证”。

## Canonical Query Carriers

| truth role | canonical carriers | notes |
| --- | --- | --- |
| project governance | `project_state.yaml`；若已生成，再补 `governance-state.yaml`、`mandate.yaml`、`mission-brief.yaml`、`route-plan.yaml`、`preflight-verdict.yaml`、`validation-report.md`、`learning-record.md` | 核心项目状态入口 + 惰性治理链 |
| planning | `projects/<项目名>/1-Planning/` | 包括阶段产物与 `1-Planning/validation-report.md` |
| directing | `projects/<项目名>/3-Detail/第N集.json` | `2-Global` 产出导演前置 Markdown，`3-Detail` 负责生成并维护 episode 根文件 |
| subject | `projects/<项目名>/4-Design/` | design-source 产物与阶段验收 |
| media | `projects/<项目名>/5-Image/`、`6-Video/`、`7-Cut/` | 画面、视频、后期产物层 |
| governance system | `team.yaml`、`.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`、root `aigc/SKILL.md` | 路由、顾问团、制度问题 |

## Query Order

1. 先确认 `PROJECT_ROOT`
2. 再识别 truth role
3. 只读取该 truth role 的 canonical carrier
4. 若问题涉及“当前断点 / 下一入口 / 缺治理工件”，先读 `project_state.yaml`；若 `governance-state.yaml` 存在，再把它视为更高优先级的结构化快照
5. 若问题涉及“是否通过 / 是否完成”，补读对应 `validation-report.md`
6. 若问题涉及“为什么这么路由”，补读 registry / routes / root skill

## Fast Command Patterns

```bash
rg --files "$PROJECT_ROOT/1-Planning"
rg --files "$PROJECT_ROOT/3-Detail" | rg '第[0-9]+集\\.json$'
rg --files "$PROJECT_ROOT/4-Design"
rg --files "$PROJECT_ROOT/5-Image"
rg --files "$PROJECT_ROOT/6-Video"
rg --files "$PROJECT_ROOT/7-Cut"
sed -n '1,220p' "$PROJECT_ROOT/project_state.yaml"
test -f "$PROJECT_ROOT/governance-state.yaml" && sed -n '1,220p' "$PROJECT_ROOT/governance-state.yaml"
sed -n '1,220p' "$PROJECT_ROOT/validation-report.md"
```

## Conflict Rules

- `产物存在` 不等于 `验收通过`
- `技能合同存在` 不等于 `项目产物存在`
- `registry/routes` 优先回答制度问题
- `projects/<项目名>/` 优先回答项目事实问题
