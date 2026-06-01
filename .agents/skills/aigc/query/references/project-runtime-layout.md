# AIGC Project Runtime Layout

本文件是 `aigc/query` 内置的项目运行时布局参考，用于替代当前新 `aigc` 树尚未提供的根 `_shared/project-runtime-layout.md`。

## Canonical Runtime Root

```text
projects/aigc/<项目名>/
├── MEMORY.md
├── CONTEXT/
├── STATE.json
├── governance-state.yaml
├── 0-初始化/
├── 1-分集/
├── 2-编导/
├── 4-摄影/
├── 5-分组/
├── 6-设计/
│   ├── 场景/
│   ├── 角色/
│   └── 道具/
├── 7-图像/
│   ├── A-分镜画面/
│   └── B-分镜故事板/
├── 8-视频/
│   ├── A-分镜画面参照/
│   ├── B-分镜故事板参照/
│   ├── C-主体参照/
│   └── D-主板混合参照/
└── reports/
```

## Stage Mapping

| current stage | project carrier | legacy carrier | query note |
| --- | --- | --- | --- |
| `0-初始化` | `0-初始化/` | `0-Init/` | 新项目默认中文目录 |
| `1-分集` | `1-分集/第N集.md` | `1-Planning/` | 旧 `1-Planning` 不再是新链路默认分集目录 |
| `2-编导` | `2-编导/第N集.md` | `3-Detail/第N集.json` | 查询旧 JSON 时必须标注 legacy |
| `4-摄影` | `4-摄影/第N集.md` | none | 当前新链路新增的摄影主阶段 |
| `5-分组` | `5-分组/第N集.md` | none | 当前新链路分镜组主阶段 |
| `6-设计` | `6-设计/{场景,角色,道具}/` | `4-Design/` | 旧设计路径只作兼容 |
| `7-图像` | `7-图像/` | `5-Image/` | 旧图像路径只作兼容 |
| `8-视频` | `8-视频/` | `6-Video/`、`7-Cut/` | `7-Cut` 当前不作为默认可执行阶段 |

## Evidence Priority

1. 用户显式提供的项目路径。
2. 当前工作目录最近的 `projects/aigc/<项目名>/` 祖先。
3. `projects/aigc/<项目名>/STATE.json`、`MEMORY.md`、`0-初始化/` 共同指向的项目。
4. 只有一个候选项目时可谨慎推断。
5. 多候选或证据冲突时必须追问项目名。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 查询是否把 `projects/aigc/<项目名>/` 识别为唯一 canonical runtime root，而不是把仓库根、技能目录或旧英文阶段根当作项目根？ | `GATE-QUERY-02` | `FAIL-QUERY-PROJECT-ROOT` | `N1-project-root` | 报告锁定的项目根路径，以及用于确认的 `STATE.json`、`MEMORY.md`、`0-初始化/` 或阶段目录证据。 |
| 项目根回答是否区分 `MEMORY.md`、`CONTEXT/`、`STATE.json`、`governance-state.yaml` 和阶段目录的不同职责，避免把任一载体说成全量替代品？ | `GATE-QUERY-04` | `FAIL-QUERY-EVIDENCE` | `N3-carrier-read` | 列出实际读取或缺失的 runtime carrier，并说明每个 carrier 能回答的事实范围。 |
| `1-分集` 查询是否默认落到 `1-分集/第N集.md`，而不是旧 `1-Planning/`；旧路径被使用时是否明确标注 compatibility？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前 `1-分集` 路径、旧 `1-Planning` fallback 路径和 fallback 原因。 |
| `2-编导` 查询是否默认落到 `2-编导/第N集.md`，旧 `3-Detail/第N集.json` 只作为 legacy fallback？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 输出当前编导文件路径、legacy JSON 路径及二者状态差异。 |
| `4-摄影` 与 `5-分组` 是否被视为当前新链路主阶段，并且不被旧英文阶段名覆盖或跳过？ | `GATE-QUERY-04` | `FAIL-QUERY-EVIDENCE` | `N3-carrier-read` | 报告 `4-摄影/第N集.md` 或 `5-分组/第N集.md` 的存在、缺失或验收证据状态。 |
| 角色、场景、道具类查询是否默认读取 `6-设计/{场景,角色,道具}/`，旧 `4-Design/` 只作为兼容证据？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前设计子目录证据，并在使用旧 `4-Design` 时显式标注 legacy。 |
| 图像资产查询是否默认读取 `7-图像/A-分镜画面` 或 `7-图像/B-分镜故事板`，旧 `5-Image/` 不作为默认答案？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前图像 carrier、旧图像 fallback 与二者命中情况。 |
| 视频资产查询是否默认读取 `8-视频/A/B/C/D-*` 子链路，旧 `6-Video/` 与 `7-Cut/` 只作为 legacy fallback，且 `7-Cut` 不被说成默认可执行阶段？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前视频 carrier、旧视频/剪辑 fallback、以及回答中的 canonical/legacy 标注。 |
| Evidence Priority 是否先尊重用户显式项目路径，再使用 cwd 祖先和项目核心载体，只有单候选时才谨慎推断？ | `GATE-QUERY-02` | `FAIL-QUERY-PROJECT-ROOT` | `N1-project-root` | 报告项目根推断来源；多候选或冲突时输出 `needs_clarification` 而不是混答。 |
| 当用户问“完成/通过/可交付”时，runtime layout 命中的文件或目录是否只作为产物存在证据，并继续补读执行报告或 validation report？ | `GATE-QUERY-05` | `FAIL-QUERY-VALIDATION` | `N4-validation-crosscheck` | 报告产物路径、执行报告或验收报告路径；缺报告时写明“未见验收证据”。 |
