# Project Runtime Layout Reference

本文件为 `$aigc-resume` 固定新版 `aigc` 项目 runtime 的读取口径。它服务恢复判定，不拥有项目初始化权。

## Canonical Project Root

```text
projects/aigc/<项目名>/
```

项目根必须优先通过以下顺序锁定：

1. 用户给出完整 `projects/aigc/<项目名>/` 路径。
2. 当前工作目录位于某个 `projects/aigc/<项目名>/` 内。
3. 用户给出项目名，且 `projects/aigc/<项目名>/` 存在。
4. `projects/aigc/` 下只有一个候选项目。
5. 多项目且无项目名时停止，询问项目名。

## Current Chinese Runtime

新版 `aigc` 默认 runtime 使用中文阶段目录：

```text
projects/aigc/<项目名>/
├── 0-初始化/
├── 1-分集/
├── 2-编导/
├── 3-摄影/
├── 4-分组/
├── 5-设计/
│   ├── 场景/
│   │   ├── 1-清单/
│   │   ├── 2-设计/
│   │   └── 3-生成/
│   ├── 道具/
│   │   ├── 1-清单/
│   │   ├── 2-设计/
│   │   └── 3-生成/
│   └── 角色/
│       ├── 1-清单/
│       ├── 2-设计/
│       └── 3-生成/
├── 6-图像/
├── 7-视频/
├── 源/
├── CONTEXT/
├── CONTEXT/
├── MEMORY.md
├── CHANGELOG.md
├── STATE.json
└── team.yaml
```

## Governance Carriers

项目根治理载体：

- `STATE.json`
- `governance-state.yaml`
- `mandate.yaml`
- `mission-brief.yaml`
- `route-plan.yaml`
- `preflight-verdict.yaml`
- `validation-report.md`
- `learning-record.md`

`STATE.json` 是轻量 live route truth；`governance-state.yaml` 是复杂恢复与 review bridge 的结构化断点真源；`CHANGELOG.md` 是时间序记录，不是 live route truth。

## Project Context Carriers

- `MEMORY.md` 保存项目长期偏好、禁区、口味和持续要求。
- `CONTEXT/` 是项目级共享附加上下文根；恢复时只读取与当前断点、阶段、治理缺口或用户问题相关的文件。
- `CONTEXT/` 保存当前中文 runtime 的项目预设包和补充参考材料；它不替代 `MEMORY.md` 或 `CONTEXT/`。

## Stage Evidence Hints

阶段产物必须是真实文件，不是空目录：

| stage | evidence examples |
| --- | --- |
| `0-初始化` | `north_star.yaml`, `init_handoff.yaml`, `story-source-manifest.yaml` |
| `1-分集` | `第N集.md`, `执行报告.md` |
| `2-编导` | `第N集.md`, `validation-report.md` |
| `3-摄影` | `第N集.md`, `validation-report.md` |
| `4-分组` | `第N集.md`, 分组统计或 validation report |
| `5-设计` | `场景/角色/道具` 下的清单、设计稿、生成记录 |
| `6-图像` | `A-分镜画面`, `B-分镜故事板` 或 provider handoff |
| `7-视频` | 分镜画面参照、故事板参照、主体参照或生成任务记录 |

## Legacy Compatibility Inputs

旧 `aigc-old` 包使用过以下英文 runtime 口径：

- `0-Init`
- `1-Planning`
- `2-Global`
- `3-Detail`
- `4-Design`
- `5-Image`
- `6-Video`
- `7-Cut`
- transition `4-设计`

这些路径只允许作为历史项目或迁移输入读取；新版恢复输出不得把它们当作默认下一入口。若检测到旧路径与中文路径并存，优先报告 `root_reroute` 或 `governance_rebuild`，由根 `aigc` 决定迁移策略。

`7-Cut` 是旧后期/剪辑搁浅阶段。恢复时只能返回 `root_reroute` 或 `blocked_safety_stop`，不得把它当成可直接续跑阶段。

`4-设计` 是设计阶段 transition 输入：若旧项目只存在 `4-设计`，resume 应报告路径漂移并回根确认迁移；若 `5-设计` 存在，默认以 `5-设计` 作为设计阶段恢复真源。

## Forbidden Resume Assumptions

- `projects/` 根层不是 AIGC 项目根。
- `projects/aigc/<项目名>/CONTEXT/` 是项目级共享上下文根；恢复时按需读取相关文件，不得整目录灌入上下文。
- 空阶段目录不是完成证据。
- provider 生成缓存、临时下载、外部二进制不能单独决定恢复模式。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 项目根是否按完整路径、cwd 内项目、项目名存在性、单候选、最小追问的顺序唯一锁定，且未把仓库根或 `projects/` 当项目根？ | `GATE-RESUME-PROJECT-ROOT` | `FAIL-RESUME-PROJECT-ROOT` | `N1-INTAKE` | 报告列出 root lock method、候选项目列表、最终 `PROJECT_ROOT` 或最小追问。 |
| 新版恢复输出是否以 `projects/aigc/<项目名>/` 和中文阶段目录为默认 runtime，而不是旧英文路径或 transition 路径？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` | 报告列出当前 runtime profile、命中的中文阶段路径和被降级的 legacy path。 |
| `STATE.json`、`governance-state.yaml`、`mission-brief.yaml`、`route-plan.yaml`、`preflight-verdict.yaml` 等治理载体的职责是否被区分，未把时间序 `CHANGELOG.md` 当 live route truth？ | `GATE-RESUME-GOVERNANCE-GATE` | `FAIL-RESUME-GOVERNANCE-GATE` | `N5-GATE` | 报告记录存在/缺失的治理载体、各自 truth role 和是否触发 gate reentry。 |
| 项目 `MEMORY.md` 与项目 `CONTEXT/` 是否按偏好记忆和共享附加上下文分层读取，没有互相替代或整目录灌入？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` | 报告列出读取的项目 context 文件、读取原因和未读取整目录的说明。 |
| 阶段证据是否来自真实文件，如 `第N集.md`、validation report、设计稿或生成记录，而不是空 skeleton 目录？ | `GATE-RESUME-EVIDENCE-CHAIN` | `FAIL-RESUME-EVIDENCE` | `N2-TRUTH-LOCK` | 报告列出每个阶段证据文件路径、文件存在性和空目录排除结果。 |
| legacy 英文路径与中文路径并存时，是否优先报告 `root_reroute` 或 `governance_rebuild`，由根 `aigc` 决定迁移策略？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N3-TYPE` | 报告列出并存路径、漂移风险、选择的 resume mode 和 reroute owner。 |
| 旧 `7-Cut` 是否被识别为搁浅/blocked 阶段，只返回 `root_reroute` 或 `blocked_safety_stop`？ | `GATE-RESUME-LEGACY-SHELVED` | `FAIL-RESUME-LEGACY-STAGE` | `N4-PLAN` | 报告记录 `7-Cut` 证据、阻断理由和唯一回接入口。 |
| transition `4-设计` 与当前 `5-设计` 是否被区分；若 `5-设计` 存在，是否默认以 `5-设计` 作为设计阶段恢复真源？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` | 报告列出 `4-设计`/`5-设计` 存在性、采用的设计真源和漂移说明。 |
| provider 缓存、临时下载、外部二进制或最近修改文件是否只作辅助证据，未单独决定恢复模式？ | `GATE-RESUME-EVIDENCE-CHAIN` | `FAIL-RESUME-EVIDENCE` | `N2-TRUTH-LOCK` | 报告列出辅助证据类型、为何不足以单独裁决，以及主证据链。 |
| runtime layout 细则是否只服务恢复判定，不拥有初始化、迁移执行或阶段业务真稿生成权？ | `GATE-RESUME-TRUTH-BOUNDARY` | `FAIL-RESUME-TRUTH-BOUNDARY` | `N4-PLAN` | 报告说明本 reference 被用于路径/证据判定，未直接写业务产物或改变阶段真源。 |
