---
name: aigc-video-stage
description: "Use when routing AIGC video-stage work into LibTV video plans and CLI execution handoff."
governance_tier: router
metadata:
  short-description: AIGC video stage router
---

# aigc 8-视频

`8-视频` 是 AIGC 项目的视频阶段父级入口。它只负责视频阶段路由、项目 runtime 边界、计划层汇流和下游执行交接；不直接生成视频，不直接操作 LibTV 画布节点，不直接改写 `5-分组`、`6-设计` 或 `7-图像` 的 canonical truth。

当前 active 默认叶子为 `.agents/skills/aigc/8-视频/libTV画布流/SKILL.md`。该叶子定位为 LibTV 视频生成计划层：读取 `5-分组` 和主体资产，形成 submit plan、manifest、queue record、CLI handoff plan 和审查证据；真正的项目、分组、节点、上传、下载与运行执行，必须交给最新版 `.agents/skills/cli/libTV`。

旧 A/B/C/D 叶子位于 `.agents/skills/aigc/backup/`，仅用于兼容回读、修复旧产物或用户明确点名旧路线时旁路承接。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 若任务绑定 `projects/aigc/<项目名>/`，必须先加载项目根 `MEMORY.md`，再加载项目根 `CONTEXT/` 中与视频阶段、风格、角色、场景、主体资产或生成限制相关的上下文。
- 父级只做路由、计划边界和汇流判断；视频 prompt 组织、主体绑定、CLI handoff plan、queue / manifest / report 由命中的叶子技能负责。
- 调用 LibTV 前，命中叶子必须加载 `.agents/skills/cli/libTV/SKILL.md` 以及任务相关命令文档。官方 1.0.1 包当前没有同目录 `CONTEXT.md`，应记录为上游包结构缺口，不得伪造经验层。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `.agents/skills/aigc/SKILL.md` > 本 `SKILL.md` > 目标叶子 `SKILL.md` > 目标叶子分区规范 > `.agents/skills/cli/libTV/SKILL.md` 与命令文档 > `agents/openai.yaml` > 项目 `MEMORY.md` > 项目 `CONTEXT/` > 本 `CONTEXT.md` > 目标叶子 `CONTEXT.md`。

## Multi-Subskill Continuous Workflow

当本主技能包被整体调用时，视为用户已授权按本级声明的同级子技能包自动完成整个技能组任务；在满足必要输入、显式选择和安全门后，不再为“是否继续下一步”额外确认。

- 无序号同级子技能包默认全选并发执行，由本父级汇总、裁决和写回唯一 canonical 输出。
- 数字序号子技能包或节点默认按数字升序串行执行，前一节点产物自动作为后一节点输入。
- 英文序号子技能包或路线默认按用户意图、父级路由或输入类型单选分流；只有用户明确要求对比、并跑或批量多路线时才多选。
- 卫星技能、查询/恢复/审查类旁路入口不默认纳入主链；只有用户请求、阶段门禁或叶子合同显式需要时才回接。
- 连续调度不得绕过阻断门：缺少项目根、上游分镜组、目标叶子、LibTV 登录状态或 CLI handoff 证据会造成错误写回时，必须先阻断并说明最小修复项。
- 每个被调度的叶子包仍必须加载自身 `SKILL.md + CONTEXT.md`；脚本只能承担机械辅助，不得替代 LLM 对计划、绑定、路线选择或交付裁决的判断。

## Input Contract

Accepted input:

- 用户命中 `8-视频`、视频阶段、生视频、LibTV、LibTV 画布流、主体参照、分镜组视频或批量视频计划。
- 来自 `projects/aigc/<项目名>/5-分组/` 的分镜组稿，需要转为 LibTV 视频计划和 CLI 执行交接。
- 已有 `projects/aigc/<项目名>/8-视频/*/` 的 manifest、submit plan、queue、CLI handoff、画布节点或生成结果需要 query / download / repair / review / rerun。

Required input:

- 项目名或项目根。
- 可读的上游分镜组稿，或可定位的既有 `8-视频` 阶段工件。
- 能够判断目标路线；未显式指定旧路线时默认进入 `libTV画布流`。

Reject or clarify when:

- 用户要求父级直接生成视频、直接操作 LibTV 节点、直接运行 `libtv node --run`，或跨过叶子技能改写业务真源。
- 用户要生成分镜画面图或故事板图本体，应转入 `7-图像` 对应叶子技能。
- 用户要求修改剧情、镜头顺序、角色事实或分组边界，应转回 `5-分组` 或明确声明这是上游修复。
- 旧 A/B/C/D 路线无法唯一判断，且自动选择会造成参照资产错用或重复提交。

## Mode Selection

| mode | trigger | route |
| --- | --- | --- |
| `libtv_canvas_plan` | 默认；用户只说进入视频阶段、生视频、LibTV、主体参照或按 `5-分组` 组级出视频 | `libTV画布流/SKILL.md` |
| `legacy_frame_visual_reference` | 用户明确点名旧 A 路线、修复旧 A 路线产物，或已有路径位于 `8-视频/A-分镜画面参照/` | `.agents/skills/aigc/backup/A-分镜画面参照/SKILL.md` |
| `legacy_storyboard_reference` | 用户明确点名旧 B 路线、修复旧 B 路线产物，或已有路径位于 `8-视频/B-分镜故事板参照/` | `.agents/skills/aigc/backup/B-分镜故事板参照/SKILL.md` |
| `legacy_subject_reference` | 用户明确点名旧 C 路线、修复旧 C 路线产物，或已有路径位于 `8-视频/C-主体参照/` | `.agents/skills/aigc/backup/C-主体参照/SKILL.md` |
| `legacy_hybrid_reference` | 用户明确点名旧 D 路线、修复旧 D 路线产物，或已有路径位于 `8-视频/D-主板混合参照/` | `.agents/skills/aigc/backup/D-主板混合参照/SKILL.md` |
| `query_or_download` | 已有 LibTV projectUuid、node id、group id、queue record、视频结果查询或下载 | 先定位所属叶子，再由叶子交给 `.agents/skills/cli/libTV` |
| `repair_or_review` | submit plan、manifest、CLI handoff、queue、结果漂移或只审查 | 先定位原产物所属叶子，再执行对应 review / repair |
| `footage_review_handoff` | 用户要求审片、分析已下载视频、对照实际素材、把审片问题改回分镜组 | 转入 `.agents/skills/aigc/9-审片/SKILL.md` |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 默认 LibTV 视频计划流 | `libTV画布流/SKILL.md` + `libTV画布流/CONTEXT.md` |
| 旧 A/B/C/D 路线回读、修复或明确点名 | `.agents/skills/aigc/backup/<路线>/SKILL.md` + 同目录 `CONTEXT.md` |
| LibTV 项目、分组、节点、上传、下载、运行或登录 | `.agents/skills/cli/libTV/SKILL.md` + 对应 `commands/*.md`、`node-types/*.md` |
| 上游事实边界核对 | `.agents/skills/aigc/5-分组/SKILL.md + CONTEXT.md`，必要时读取 `6-设计` 或 `7-图像` 对应入口 |

## Execution Contract

1. 读取本 `SKILL.md + CONTEXT.md`，锁定项目根、用户目标、上游可用资产和是否已有视频阶段工件。
2. 选择唯一叶子技能；默认进入 `libTV画布流`，只有用户明确点名旧路线或既有产物位于旧 A/B/C/D 目录时才进入 backup 对应叶子。
3. 加载目标叶子的 `SKILL.md + CONTEXT.md`，把本轮输入、项目根、集号/分镜组范围、LibTV project / group / node 线索传入叶子合同。
4. 父级不得直接写视频 prompt、主体 manifest、LibTV CLI 命令、queue 或结果报告；这些业务产物必须由目标叶子定义。
5. 若目标叶子需要远端执行，叶子必须生成 CLI handoff plan，再由 `.agents/skills/cli/libTV` 执行 `libtv project/group/node/upload/download/model` 等命令；父级不得绕过 CLI skill 直接调用 HTTP 或旧会话接口。
6. 查询、下载、修复或审查任务必须先定位原产物所属叶子，未定位前不得创建新的平行视频真源。
7. 若目标叶子缺失、不可读或与用户目标不匹配，报告阻断原因和建议入口，不临时伪造叶子合同。

## Root-Cause Execution Contract

失败链路：

`Symptom -> Direct Cause -> Parent Route Owner -> Leaf Skill Contract -> .agents/skills/cli/libTV -> AGENTS.md / skill-工作车间`

优先修复：

1. 路由误判或旧路线混用：回到本文件 `Mode Selection` 与 `CONTEXT.md` 的 Type Map。
2. 叶子加载缺失：补齐目标叶子的 `SKILL.md + CONTEXT.md` 或报告配置缺口。
3. 父级越权生成 prompt / CLI / queue：回收为叶子计划层执行，父级只保留路由说明。
4. 仍引用旧会话接口或旧 access-key 凭据模式：回到 `libTV画布流/references/official-libtv-cli-handoff.md` 和新版 `.agents/skills/cli/libTV` 文档。
5. 新版 CLI 登录或项目绑定失败：交给 `.agents/skills/cli/libTV` 的 `login/account/project` 命令排障。

## Output Contract

- Required output: 唯一叶子路由、项目级 LibTV 计划/执行交接状态，或明确的多路线用户授权，或阻断原因。
- Output format: 面向用户的简短路由说明；实际视频阶段计划和执行证据由叶子技能输出。
- Output path: 父级不直接落业务产物；当前 active 叶子写入 `projects/aigc/<项目名>/8-视频/libTV画布流/`，旧 A/B/C/D 兼容叶子仍回写其既有项目目录。
- Naming convention: canonical 视频命名固定为 `<分镜组ID>.mp4`；同组变体固定为 `<分镜组ID>-a.mp4`、`<分镜组ID>-b.mp4`。叶子技能可自定 prompt、manifest、queue 和 report 名称，但视频文件名必须遵守本规则以便 `9-审片` 反向定位 `5-分组`。
- Completion gate: 目标叶子明确且已加载；若涉及 LibTV 远端执行，已生成 CLI handoff plan 并交给 `.agents/skills/cli/libTV`，或已说明阻断原因。
