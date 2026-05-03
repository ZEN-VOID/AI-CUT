# AIGC Query System Data Flow

本文件定义 `aigc/query` 的最小数据流真源：先判定 truth role，再读取有资格回答该问题的 carrier。

## Canonical Query Carriers

| truth role | canonical carriers | notes |
| --- | --- | --- |
| project governance | `projects/aigc/<项目名>/governance-state.yaml`；缺失时回读 `STATE.json`、`0-初始化/north_star.yaml`、`0-初始化/init_handoff.yaml`、`MEMORY.md`、`CONTEXT/` | `governance-state.yaml` 是结构化治理快照；`STATE.json` 是轻量入口 |
| initialization | `projects/aigc/<项目名>/0-初始化/`、项目根 `MEMORY.md`、项目根 `CONTEXT/` | 核心初始化工件优先于惰性治理工件 |
| episode split | `projects/aigc/<项目名>/1-分集/第N集.md`、`1-分集/执行报告.md` | 查询原文分集与分集执行状态 |
| directing | `projects/aigc/<项目名>/2-编导/第N集.md`、`2-编导/执行报告.md` | legacy `3-Detail/第N集.json` 只在旧项目或用户点名时兼容回读 |
| cinematography | `projects/aigc/<项目名>/3-摄影/第N集.md`、`3-摄影/执行报告.md` | 分镜明细与摄影稿事实 |
| grouping | `projects/aigc/<项目名>/4-分组/第N集.md`、`4-分组/执行报告.md` | 分镜组、组 ID、入场/出场画面、统计 YAML |
| subject assets | `projects/aigc/<项目名>/5-设计/场景/`、`5-设计/角色/`、`5-设计/道具/` | legacy `4-Design/` 只作兼容回读 |
| image assets | `projects/aigc/<项目名>/6-图像/A-分镜画面/`、`6-图像/B-分镜故事板/` | legacy `5-Image/` 只作兼容回读 |
| video assets | `projects/aigc/<项目名>/7-视频/A-分镜画面参照/`、`7-视频/B-分镜故事板参照/`、`7-视频/C-主体参照/`、`7-视频/D-主板混合参照/` | legacy `6-Video/` 只作兼容回读 |
| governance system | `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`、相关阶段 `SKILL.md` | 回答路由制度、技能状态、路径漂移 |

## Query Order

1. 确认 `PROJECT_ROOT`。
2. 判定 truth role。
3. 读取该 role 的 canonical carrier。
4. 若问题涉及“完成 / 通过 / 可交付”，补读同阶段 `validation-report.md` 或 `执行报告.md`。
5. 若问题涉及“为什么这么路由”，补读 registry/routes 与相关 `SKILL.md`。
6. 若 canonical carrier 缺失，再读取 legacy carrier，并明确标注 fallback。

## Fast Command Patterns

```bash
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
rg --files "$REPO_ROOT/projects/aigc"
rg --files "$PROJECT_ROOT/0-初始化"
rg --files "$PROJECT_ROOT/1-分集" | rg '第[0-9]+集\\.md$'
rg --files "$PROJECT_ROOT/2-编导" | rg '第[0-9]+集\\.md$'
rg --files "$PROJECT_ROOT/3-摄影" | rg '第[0-9]+集\\.md$'
rg --files "$PROJECT_ROOT/4-分组" | rg '第[0-9]+集\\.md$'
rg --files "$PROJECT_ROOT/5-设计"
rg --files "$PROJECT_ROOT/6-图像"
rg --files "$PROJECT_ROOT/7-视频"
test -f "$PROJECT_ROOT/governance-state.yaml" && sed -n '1,220p' "$PROJECT_ROOT/governance-state.yaml"
test -f "$PROJECT_ROOT/STATE.json" && sed -n '1,220p' "$PROJECT_ROOT/STATE.json"
```

## Conflict Rules

- `产物存在` 不等于 `验收通过`。
- `技能合同存在` 不等于 `项目产物存在`。
- `registry/routes` 优先回答制度问题；`projects/aigc/<项目名>/` 优先回答项目事实问题。
- 新链路中文阶段目录是 canonical；旧英文阶段目录必须标注为 legacy fallback。
