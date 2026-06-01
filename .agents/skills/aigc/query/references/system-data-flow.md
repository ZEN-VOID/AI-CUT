# AIGC Query System Data Flow

本文件定义 `aigc/query` 的最小数据流真源：先判定 truth role，再读取有资格回答该问题的 carrier。

## Canonical Query Carriers

| truth role | canonical carriers | notes |
| --- | --- | --- |
| project governance | `projects/aigc/<项目名>/governance-state.yaml`；缺失时回读 `STATE.json`、`0-初始化/north_star.yaml`、`0-初始化/init_handoff.yaml`、`MEMORY.md`、`CONTEXT/` | `governance-state.yaml` 是结构化治理快照；`STATE.json` 是轻量入口 |
| initialization | `projects/aigc/<项目名>/0-初始化/`、项目根 `MEMORY.md`、项目根 `CONTEXT/` | 核心初始化工件优先于惰性治理工件 |
| episode split | `projects/aigc/<项目名>/1-分集/第N集.md`、`1-分集/执行报告.md` | 查询原文分集与分集执行状态 |
| directing | `projects/aigc/<项目名>/2-编导/第N集.md`、`2-编导/执行报告.md` | legacy `3-Detail/第N集.json` 只在旧项目或用户点名时兼容回读 |
| motion enrichment | `projects/aigc/<项目名>/3-运动/第N集.md`、`3-运动/执行报告.md` | 查询运动五要素强化与跨画面连续性 |
| cinematography | `projects/aigc/<项目名>/4-摄影/第N集.md`、`4-摄影/执行报告.md` | 分镜明细与摄影稿事实 |
| grouping | `projects/aigc/<项目名>/5-分组/第N集.md`、`5-分组/执行报告.md` | 分镜组、组 ID、组间连接件、统计 YAML |
| subject assets | `projects/aigc/<项目名>/6-设计/场景/`、`6-设计/角色/`、`6-设计/道具/` | legacy `4-Design/` 只作兼容回读 |
| image assets | `projects/aigc/<项目名>/7-图像/A-分镜画面/`、`7-图像/B-分镜故事板/` | legacy `5-Image/` 只作兼容回读 |
| video assets | `projects/aigc/<项目名>/8-视频/A-分镜画面参照/`、`8-视频/B-分镜故事板参照/`、`8-视频/C-主体参照/`、`8-视频/D-主板混合参照/` | legacy `6-Video/` 只作兼容回读 |
| footage review | `projects/aigc/<项目名>/9-审片/` | 查询审片报告、缺陷清单、修复路由与验收证据 |
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
rg --files "$PROJECT_ROOT/3-运动" | rg '第[0-9]+集\\.md$'
rg --files "$PROJECT_ROOT/4-摄影" | rg '第[0-9]+集\\.md$'
rg --files "$PROJECT_ROOT/5-分组" | rg '第[0-9]+集\\.md$'
rg --files "$PROJECT_ROOT/6-设计"
rg --files "$PROJECT_ROOT/7-图像"
rg --files "$PROJECT_ROOT/8-视频"
rg --files "$PROJECT_ROOT/9-审片"
test -f "$PROJECT_ROOT/governance-state.yaml" && sed -n '1,220p' "$PROJECT_ROOT/governance-state.yaml"
test -f "$PROJECT_ROOT/STATE.json" && sed -n '1,220p' "$PROJECT_ROOT/STATE.json"
```

## Conflict Rules

- `产物存在` 不等于 `验收通过`。
- `技能合同存在` 不等于 `项目产物存在`。
- `registry/routes` 优先回答制度问题；`projects/aigc/<项目名>/` 优先回答项目事实问题。
- 新链路中文阶段目录是 canonical；旧英文阶段目录必须标注为 legacy fallback。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 查询是否先锁定真实 `projects/aigc/<项目名>/`，再读取本表中的任何 carrier，而不是从仓库根、技能目录或 registry 目录直接推断项目事实？ | `GATE-QUERY-02` | `FAIL-QUERY-PROJECT-ROOT` | `N1-project-root` | 报告 `project_root_lock`、锁定依据，以及被排除的非项目根候选；无法唯一定位时输出 `needs_clarification`。 |
| 查询是否在读取文件前完成 truth role 判定，并让 `project_governance`、`stage_output`、`subject_asset`、`media_asset`、`governance_system` 或 `conflict_diagnosis` 决定 carrier 组？ | `GATE-QUERY-03` | `FAIL-QUERY-TRUTH-ROLE` | `N2-truth-role` | 报告选中的主 truth role、次要 role、用户问题信号和对应的 carrier 选择理由。 |
| 项目治理查询是否优先读取 `governance-state.yaml`，缺失时才按 `STATE.json`、`0-初始化/north_star.yaml`、`init_handoff.yaml`、`MEMORY.md`、`CONTEXT/` 顺序回读，并区分结构化治理快照与轻量入口？ | `GATE-QUERY-07` | `FAIL-QUERY-CARRIER` | `N3-carrier-read` | 列出 governance carrier 命中/缺失状态、fallback 原因，以及每个载体可回答的事实范围。 |
| 初始化查询是否以 `0-初始化/`、项目根 `MEMORY.md` 和项目根 `CONTEXT/` 为核心初始化证据，不把惰性治理工件缺失误判为初始化失败？ | `GATE-QUERY-07` | `FAIL-QUERY-CARRIER` | `N3-carrier-read` | 报告初始化核心工件路径、缺失项和是否属于 lazy governance 缺口。 |
| 分集、编导、运动、摄影、分组类阶段查询是否默认读取中文阶段 `1-分集`、`2-编导`、`3-运动`、`4-摄影`、`5-分组` 的 `第N集.md` 与 `执行报告.md`，而不是默认回到旧英文目录？ | `GATE-QUERY-07` | `FAIL-QUERY-CARRIER` | `N3-carrier-read` | 报告当前阶段 carrier 路径、集号匹配方式、执行报告路径和未命中的 canonical 路径。 |
| `2-编导` 查询若读取 legacy `3-Detail/第N集.json`，是否只作为旧项目或用户点名的 fallback，并在回答中明确标注当前 canonical 是 `2-编导/第N集.md`？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告 `2-编导` current carrier、`3-Detail` fallback 路径、fallback 触发原因和回答中的 legacy 标注。 |
| 角色、场景、道具等主体资产查询是否默认读取 `6-设计/{场景,角色,道具}/`，并把旧 `4-Design/` 仅作为兼容证据而非默认资产真源？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告命中的 `6-设计` 子目录、旧 `4-Design` 命中情况和 canonical/legacy 差异。 |
| 分镜画面、故事板、视频、参照视频与审片报告查询是否默认读取 `7-图像/A-B`、`8-视频/A-D` 与 `9-审片`，并把旧 `5-Image/6-Video/7-Cut` 明确降级为 legacy fallback？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前图像/视频/审片 carrier、旧路径 fallback、是否存在 provider 输出、阶段工件与审片结论差别。 |
| 用户问“完成 / 通过 / 可交付”时，是否在 carrier 命中后继续补读对应 `validation-report.md` 或 `执行报告.md`，并区分产物存在、报告存在和验收通过？ | `GATE-QUERY-05` | `FAIL-QUERY-VALIDATION` | `N4-validation-crosscheck` | 报告产物路径、执行报告或验收报告路径；缺报告时写明“未见验收证据”。 |
| 用户问“为什么这么路由 / 制度是否一致 / 技能是否 active”时，是否读取 `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml` 和相关阶段 `SKILL.md`，而不是只看项目目录？ | `GATE-QUERY-08` | `FAIL-QUERY-GOVERNANCE` | `N5-governance-crosscheck` | 报告 registry/routes 路径、相关阶段 `SKILL.md` 路径、制度层与项目层是否漂移。 |
| canonical carrier 缺失时，是否先报告缺口，再安全读取 legacy carrier，并在最终回答里同时说明 current canonical path 与 legacy fallback path？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告缺失的 canonical path、读取的 legacy path、fallback 触发条件和回答中的降级措辞。 |
| 最终回答是否把每个结论回接到实际读取的 carrier 或明确缺失的 canonical path，避免用“技能合同存在”替代“项目产物存在”？ | `GATE-QUERY-04` | `FAIL-QUERY-EVIDENCE` | `N6-answer` | 报告每条结论的证据路径、缺口路径和对应 truth role；技能合同证据只能用于制度类结论。 |
