# Project Runtime Layout Reference

本文件为 `$aigc-resume` 固定当前 `aigc` 项目 runtime 的读取口径。它服务恢复判定，不拥有项目初始化权。

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

当前 `aigc` 默认 runtime 使用中文阶段目录：

```text
projects/aigc/<项目名>/
├── 0-初始化/
├── 1-分集/
├── 4-编剧/
├── 2-美学/
├── 5-导演/
├── 6-分镜/
├── 7-摄影/
├── 8-分组/
├── 3-主体/
│   ├── 场景/
│   ├── 道具/
│   └── 角色/
├── 9-图像/
├── 10-画布/
├── CONTEXT/
├── MEMORY.md
├── STATE.json
└── governance-state.yaml
```

`governance-state.yaml`、`STATE.json`、根治理载体和旧初始化 carrier 都不是 scaffold-plus-memory 初始化的必出项。恢复时只能把旧 carrier 作为历史存在性证据，不得把缺失直接判为初始化失败，也不得把旧 carrier 当作当前上下文真源。

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
- `CONTEXT/` 不替代 `MEMORY.md` 或技能同目录 `CONTEXT.md`。

## Stage Evidence Hints

阶段产物必须是真实文件，不是空目录：

| stage | evidence examples |
| --- | --- |
| `0-初始化` | `MEMORY.md`, `CONTEXT/README.md`, scaffold directory existence |
| `1-分集` | `第N集.md`, `执行报告.md` |
| `4-编剧` | `第N集.md`, `validation-report.md`, `执行报告.md` |
| `2-美学` | 画面基调/角色风格/场景风格/道具风格/分镜风格/摄影风格协议 |
| `5-导演` | `第N集.md`, `validation-report.md` |
| `6-分镜` | `第N集.md`, `validation-report.md` |
| `7-摄影` | `第N集.md`, `validation-report.md` |
| `8-分组` | `第N集.md`, 分组统计或 validation report |
| `3-主体` | `场景/角色/道具` 下的清单、设计稿、生成记录 |
| `9-图像` | `A-分镜画面`, `B-分镜故事板` 或 provider handoff |
| `10-画布` | `libTV画布流` 或生成任务记录 |

## Legacy Compatibility Inputs

这些路径只允许作为历史项目或迁移输入读取；新版恢复输出不得把它们当作默认下一入口：

- `0-Init`
- `1-Planning`
- `2-Global`
- `3-Detail`
- `4-Design`
- `5-Image`
- `6-Video`
- `7-Cut`
- old Chinese `2-编导`
- old Chinese `3-运动`
- old Chinese `4-摄影`
- transition `4-设计`

旧 `2-编导` 可按意图映射到当前 `4-编剧 / 5-导演`，或显式 archived `backup/5-表演`；旧 `3-运动` 可映射到 `6-分镜 / 7-摄影`，或显式 archived `backup/9-光影`；旧 `4-摄影` 可映射到 `7-摄影`。映射必须在恢复报告中标注 legacy source、current owner 与 archived 状态。

`7-Cut` 是旧后期/剪辑搁浅阶段。恢复时只能返回 `root_reroute` 或 `blocked_safety_stop`，不得把它当成可直接续跑阶段。

## Forbidden Resume Assumptions

- `projects/` 根层不是 AIGC 项目根。
- `projects/aigc/<项目名>/CONTEXT/` 是项目级共享上下文根；恢复时按需读取相关文件，不得整目录灌入上下文。
- 空阶段目录不是完成证据。
- 缺旧初始化 carrier 不等于初始化失败。
- provider 生成缓存、临时下载、外部二进制不能单独决定恢复模式。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 项目根是否按完整路径、cwd 内项目、项目名存在性、单候选、最小追问的顺序唯一锁定，且未把仓库根或 `projects/` 当项目根？ | `GATE-RESUME-PROJECT-ROOT` | `FAIL-RESUME-PROJECT-ROOT` | `N1-INTAKE` | 报告列出 root lock method、候选项目列表、最终 `PROJECT_ROOT` 或最小追问。 |
| 新版恢复输出是否以 `projects/aigc/<项目名>/` 和当前中文阶段目录为默认 runtime，而不是旧英文路径、旧中文阶段或 transition 路径？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` | 报告列出当前 runtime profile、命中的中文阶段路径和被降级的 legacy path。 |
| `STATE.json`、`governance-state.yaml`、`mission-brief.yaml`、`route-plan.yaml`、`preflight-verdict.yaml` 等治理载体的职责是否被区分，未把时间序 `CHANGELOG.md` 当 live route truth？ | `GATE-RESUME-GOVERNANCE-GATE` | `FAIL-RESUME-GOVERNANCE-GATE` | `N5-GATE` | 报告记录存在/缺失的治理载体、各自 truth role 和是否触发 gate reentry。 |
| 项目 `MEMORY.md` 与项目 `CONTEXT/` 是否按偏好记忆和共享附加上下文分层读取，没有互相替代或整目录灌入？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` | 报告列出读取的项目 context 文件、读取原因和未读取整目录的说明。 |
| 阶段证据是否来自真实文件，如 `第N集.md`、validation report、设计稿或生成记录，而不是空 skeleton 目录？ | `GATE-RESUME-EVIDENCE-CHAIN` | `FAIL-RESUME-EVIDENCE` | `N2-TRUTH-LOCK` | 报告列出每个阶段证据文件路径、文件存在性和空目录排除结果。 |
| legacy 路径与当前中文路径并存时，是否优先报告 `root_reroute` 或 `governance_rebuild`，由根 `aigc` 决定迁移策略？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N3-TYPE` | 报告列出并存路径、漂移风险、选择的 resume mode 和 reroute owner。 |
| 旧 `7-Cut` 是否被识别为搁浅/blocked 阶段，只返回 `root_reroute` 或 `blocked_safety_stop`？ | `GATE-RESUME-LEGACY-SHELVED` | `FAIL-RESUME-LEGACY-STAGE` | `N4-PLAN` | 报告记录 `7-Cut` 证据、阻断理由和唯一回接入口。 |
| transition `4-设计` 与当前 `3-主体` 是否被区分；若 `3-主体` 存在，是否默认以 `3-主体` 作为设计阶段恢复真源？ | `GATE-RESUME-RUNTIME-PROFILE` | `FAIL-RESUME-RUNTIME` | `N2-TRUTH-LOCK` | 报告列出 `4-设计`/`3-主体` 存在性、采用的设计真源和漂移说明。 |
| provider 缓存、临时下载、外部二进制或最近修改文件是否只作辅助证据，未单独决定恢复模式？ | `GATE-RESUME-EVIDENCE-CHAIN` | `FAIL-RESUME-EVIDENCE` | `N2-TRUTH-LOCK` | 报告列出辅助证据类型、为何不足以单独裁决，以及主证据链。 |
| runtime layout 细则是否只服务恢复判定，不拥有初始化、迁移执行或阶段业务真稿生成权？ | `GATE-RESUME-TRUTH-BOUNDARY` | `FAIL-RESUME-TRUTH-BOUNDARY` | `N4-PLAN` | 报告说明本 reference 被用于路径/证据判定，未直接写业务产物或改变阶段真源。 |
