# AIGC Query System Data Flow

## Purpose

本文件定义 `aigc/query` 的最小数据流真源，回答“问什么就先去哪一层取证”。

## Canonical Query Carriers

| truth role | canonical carriers | notes |
| --- | --- | --- |
| project governance | `governance-state.yaml`、`project_state.yaml`、`mandate.yaml`、`mission-brief.yaml`、`route-plan.yaml`、`preflight-verdict.yaml`、`validation-report.md`、`learning-record.md` | 项目治理链、断点与 lifecycle 证据 |
| planning | `projects/<项目名>/规划/` | 包括阶段产物与 `规划/validation-report.md` |
| directing | `projects/<项目名>/编导/第N集.json` | `2-组间` 与 `3-明细` 共用根文件 |
| subject | `projects/<项目名>/主体/` | 主体产物与阶段验收 |
| media | `projects/<项目名>/画面/`、`视频/`、`后期/` | 画面、视频、后期产物层 |
| governance system | `team.yaml`、`.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`、root `aigc/SKILL.md` | 路由、顾问团、制度问题 |

## Query Order

1. 先确认 `PROJECT_ROOT`
2. 再识别 truth role
3. 只读取该 truth role 的 canonical carrier
4. 若问题涉及“当前断点 / 下一入口 / 缺治理工件”，先读 `governance-state.yaml`
5. 若问题涉及“是否通过 / 是否完成”，补读对应 `validation-report.md`
6. 若问题涉及“为什么这么路由”，补读 registry / routes / root skill

## Fast Command Patterns

```bash
rg --files "$PROJECT_ROOT/规划"
rg --files "$PROJECT_ROOT/编导" | rg '第[0-9]+集\\.json$'
rg --files "$PROJECT_ROOT/主体"
rg --files "$PROJECT_ROOT/画面"
rg --files "$PROJECT_ROOT/视频"
sed -n '1,220p' "$PROJECT_ROOT/project_state.yaml"
sed -n '1,220p' "$PROJECT_ROOT/governance-state.yaml"
sed -n '1,220p' "$PROJECT_ROOT/validation-report.md"
```

## Conflict Rules

- `产物存在` 不等于 `验收通过`
- `技能合同存在` 不等于 `项目产物存在`
- `registry/routes` 优先回答制度问题
- `projects/<项目名>/` 优先回答项目事实问题
