# HARNESS.md

本文件是仓库根层的 HARNESS 总览文档，用于把当前仓库的 Harness 工程化构思、已落地真源、运行方式、现状判断与发展方向收束为一份可快速阅读的初始化说明。

注意：`HARNESS.md` 是总览型派生文档，不是新的第一真源。规范性约束仍以下列真源为准：

1. 根 `AGENTS.md`
2. `.codex/templates/harness/office-governance-contract.md`
3. `.codex/agents/harness治理/`
4. `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml`
5. `.codex/runbooks/task-lifecycle.md`
6. `.codex/templates/harness/`
7. `scripts/aigc_harness_audit.py`

## 文档定位

- 作为根层 HARNESS 初始化说明，服务于仓库维护者、后续技能开发者与治理升级任务。
- 作为总览投影，帮助快速理解“仓库当前已经做到哪里、还缺什么、下一步往哪里走”。
- 作为变更同步目标：当 HARNESS 工程相关真源发生变化时，必须同步更新本文件。

## 当前工程化构思

当前仓库的 HARNESS 不是把 agent、skill、prompt 临时串起来的运行胶水，而是按“三省六部制 + 编排工程”收束为一套可治理、可审计、可扩展的工作底座：

- 宪章层由根 `AGENTS.md` 负责，定义优先级、硬门槛、根因上溯、真源治理与闭环格式。
- 三省治理层负责起草、复核、执行分权：
  - 中书省：负责目标收束、任务起草、路线规划。
  - 门下省：负责预审、否决、验收、上溯与学习闭环。
  - 尚书省：负责执行调度、状态落盘、运行时控制与证据回传。
- 六部能力层负责把治理意图落到能力域真源：
  - 吏部：能力注册与路由
  - 户部：上下文、状态、项目控制面
  - 礼部：模板、合同、移交载体
  - 兵部：运行、调度、生命周期
  - 刑部：审计、风险控制、反回归
  - 工部：脚本、评测、基础设施

这一构思的核心目标不是“先把业务技能补齐”，而是先把业务技能未来必须依附的治理骨架、工件真源、状态面与审计入口建立起来。

当前针对 `.agents/skills/aigc/` 的重大改造，仍处于显式 `bootstrap_compat` 模式：

- 不清空 HARNESS 真源，只把它收缩为兼容骨架。
- 保留 `projects/aigc/<项目名>/`、registry、runbook、template、audit、已启用卫星技能入口与高风险 preflight / validation gate。
- 暂时不把 `aigc` 当前阶段内部细节视为冻结真源，允许在后续改造中重写。

## 当前已实现真源

截至 `2026-04-23`，当前仓库已经完成 HARNESS 引导期的最小真源收束，并把 `aigc` 项目工作流、repo-local 漫画链路、团队能力类 skill 注册、provider API skill 注册、命令型 wrapper skills、项目内 runtime 控制面与最小审计入口纳入同一套治理骨架。

### 1. 宪章层

- 根 `AGENTS.md` 已明确：
  - 执行深度默认规则
  - 内容创作型任务的 `LLM-first creative authorship` 规则：核心创作必须由 LLM 直出，脚本仅可承担读取/组装/校验/落盘等机械辅助
  - 三省六部制编排治理基线
  - `HARNESS.md` 总览同步责任
  - `bootstrap_compat` 改造兼容模式
  - 批量技能调度默认规则
  - `subagents` 默认真实启动、命中默认 subagent skill 即视为显式许可、以及降级显式报告口径
  - Rollout 标准
  - 根因优先、根因学习回路、真源治理与复合型输出治理

### 2. 三省治理层

- `.codex/agents/harness治理/中书省.md`
- `.codex/agents/harness治理/门下省.md`
- `.codex/agents/harness治理/尚书省.md`

三省角色合同已经从“目录骨架”推进到“共享上位合同 + office 差异职责”的状态。

其中，门下省已进一步吸收 `code-reviewer` 式 findings discipline：对技能树、shared contract、runtime mapping 与审计脚本的 review，默认要求 `severity + dimension + evidence path + impact + recommended action + confidence`，不再满足于泛化结论。

### 3. 共享治理合同

- `.codex/templates/harness/office-governance-contract.md`

该文件已承担跨 office 的单一共享真源职责，覆盖：

- canonical priority
- canonical carriers
- shared entry gates
- shared workflow
- layered trace contract
- shared handoff contract
- closure contract
- anti-drift rules

### 4. 注册与路由真源

- `.codex/registry/skills.yaml`
- `.codex/registry/routes.yaml`

当前注册表与路由表已经稳定承载以下事实：

- `aigc` 仍是仓库级总入口技能，`contract_mode: bootstrap_compat`，并显式声明：
  - `projects/aigc/<项目名>/` 为 canonical project runtime
  - `STATE.json` 与 `governance-state.yaml` 为项目内控制面
  - `.codex/state/tasks/<task_id>/` 仅作治理镜像或非项目任务账本
- `aigc.stage_index` 当前已登记：
  - `0-Init`、`1-Planning`、`2-Global`、`3-Detail`、`4-Design`、`5-Image`、`6-Video` 为 `active`
  - `7-Cut` 为 `shelved`
  - `4-Design` 下的 `1-清单/{场景,角色,道具}`、`2-设计/{场景,角色,道具}`、`3-面板/{场景,角色,道具}` 已进入 leaf/tranche 注册，其中 `3-面板` tranche parent 为 `partial-active`
- `aigc.satellite_index` 当前已登记并启用：
  - `query`
  - `resume`
- `routes.yaml` 已显式声明：
  - `aigc-root-entry`
  - `aigc-project-runtime-canonical`
  - `aigc-bootstrap-compat-mode`
  - `aigc-query / resume` 卫星入口
  - `aigc-image-stage-entry`
  - `aigc-video-stage-entry`
  - `high-risk-review-gate`
  - `aigc-shelved-stages`
  - `api-anyfast-image-entry`
  - `api-anyfast-nano-banana-image-entry`
  - `api-anyfast-seedream-image-entry`
  - `api-anyfast-doubao-seed-2.0-pro-entry`
  - `story-doubao-entry`
  - `api-man-tui-nano-banana-image-entry`
  - `api-vidu-video-entry`
- `comic` 已作为 repo-local 漫画项目父级入口接入治理，固定项目根为 `projects/comic/[项目名]/`
- 漫画链路已拆成受注册子入口：
  - `comic-novel-adaptation`
  - `comic-nine-blade-prompts`
  - `comic-generation`
  - `comic-episode-poster`
- provider API 类 repo-local skill 已开始进入注册与路由：
  - `api-anyfast-image`
  - `api-anyfast-nano-banana-image`
  - `api-anyfast-seedream-image`
  - `api-anyfast-doubao-seed-2.0-pro`
  - `api-man-tui-grok-video`
  - `api-man-tui-sora`
  - `api-man-tui-nano-banana-image`
  - `api-vidu-video`
- 命令型 repo-local skills 已进入注册与路由，并直接以各自目录级 `SKILL.md` 作为唯一真源：
  - `command-github-issue`
  - `command-github-push`
  - `command-next`
  - `command-subagent-preview`
  - `command-subagent-review`
- story 侧已新增 repo-local 单技能润色入口：
  - `story-doubao`
  - 作为 `story` 主链旁路技能，负责中文小说文风诊断、整稿统修、去 AI 味与中文表达强化，不拥有 planning / validation / actualization 真源
- 团队能力类 repo-local skill 已进入注册与路由，当前覆盖：
  - 小说组
  - 演员组
  - 导演组
  - 摄影组
  - 武术组
  - 动漫组
- `AIGC-ZEN-VOID` 继续只作为 design source，通过 `legacy_mapping` 管理，而不是直接整仓继承。

### 5. 生命周期与任务工件真源

- `.codex/runbooks/task-lifecycle.md`
- `.codex/templates/harness/mandate.yaml`
- `.codex/templates/harness/mission-brief.yaml`
- `.codex/templates/harness/route-plan.yaml`
- `.codex/templates/harness/preflight-verdict.yaml`
- `.codex/templates/harness/validation-report.md`
- `.codex/templates/harness/learning-record.md`

当前已经明确标准任务生命周期：

`受命 -> 起草 -> 预审 -> 执行 -> 验收 -> 沉淀`

并且当前 runbook 已明确：

- 通用默认控制面：`.codex/state/tasks/<task_id>/`
- `aigc` 项目控制面：`projects/aigc/<项目名>/`
- 若工作流已声明项目内 canonical runtime，镜像状态面不得反向覆盖主真源

### 6. 审计与验证入口

- `scripts/aigc_harness_audit.py`
- `scripts/aigc_skill_audit.py`
- `.codex/evals/`
- `.codex/state/tasks/README.md`
- `.codex/evals/README.md`

当前审计能力至少已经能检查：

- HARNESS 引导期最小 carrier 是否存在
- 根 `AGENTS.md` 与 `HARNESS.md` 的关键合同锚点是否存在
- 三省 office 合同是否显式回指共享治理合同
- runbook、template、registry 是否保留 `bootstrap_compat` 与 canonical runtime 口径
- `aigc` 技能树的 tier / CONTEXT / 注册状态与阶段合同基线
- `bootstrap_compat` 下的 checked / skipped 审计覆盖度，不再把 parent-only 通过包装成整树全绿
- `6-Video` 等 active 链路的 shared runtime 映射是否仍残留旧叶子口径

### 7. 架构初始化方案

- `docs/plans/2026-04-08-san-sheng-liu-bu-architecture.md`

该文档承担本轮改造升级的阶段性架构包角色，记录了现状诊断、映射关系、迁移阶段与防回归方案。

## 当前运行方式

当前仓库的 HARNESS 运行逻辑可概括为：

1. 用户请求或自动化触发进入治理链。
2. 中书省负责把复杂任务收束为 `mandate + mission-brief + route-plan`。
3. 高风险任务先由门下省给出 `preflight-verdict`。
4. 尚书省在已声明的 canonical runtime 中执行：
   - `aigc` 项目工作流：`projects/aigc/<项目名>/`
   - 通用非项目任务：`.codex/state/tasks/<task_id>/`
5. 门下省以 `validation-report` 完成验收。
6. 学习结果沉淀到 `learning-record` 与对应 `CONTEXT.md`。

当 `aigc` 处于 `bootstrap_compat` 改造窗口时，额外执行一条兼容约束：

- HARNESS 继续守住项目 runtime、治理工件 carriers、卫星技能入口与高风险预审。
- `scripts/aigc_skill_audit.py` 可降级深层阶段细节检查，不用旧叶子细节去卡住正在进行的结构重构；但仍需覆盖 active stage 父合同，防止父级路由、真源或本地引用断链被静默放行。

对当前仓库而言，最重要的运行约束是：

- 复杂任务不能跳过起草工件。
- 高风险任务不能跳过预审。
- 非平凡失败不能跳过分层上溯。
- 新 skill、新 route、新模板字段、新继承映射不能绕过 registry / runbook / audit。
- `projects/aigc/<项目名>/` 始终优先于 `.codex/state/tasks/<task_id>/`，后者仅为治理镜像或通用账本。
- `query / resume` 是 `aigc` 的卫星入口，而不是可随意绕开的旁注说明；高风险预审与验收则回根 `aigc` 处理。
- `comic` 项目链路已经是受 registry / routes 管理的 repo-local workflow，不再只是临时脚本集合。
- provider API skill 已开始按 registry / routes 管理，而不再只是散落脚本目录。
- 当用户手动执行或仓库自动路由命中某个已声明“默认走 subagents”的 skill 时，仓库治理层将其视为对该默认分发路径的显式许可；只有更高优先级 system / developer / tool policy 或用户反向要求，才会阻断真实 dispatch。
- 团队能力类 skill 的 canonical carrier 是其 skill 根目录与自包含研究载体，不默认创建项目 runtime。
- 命中 subagent 合同的任务默认应真实启动 subagents；若受当前会话上层策略、工具权限或用户显式边界阻断，必须显式报告降级来源与替代路径。
- `story / aigc` 项目初始化现在除 `CONTEXT/` 外，还默认创建项目根 `MEMORY.md`，用于保存项目级创作偏好、特殊元素与长期要求；它与技能 `CONTEXT.md` 的经验层职责分离。
- `CONTEXT.md` 必须保持知识库模式；详细时间线与迁移流水应外置到 `CHANGELOG.md` 或报告载体，而不是默认注入运行上下文。

## 现状判断

当前 HARNESS 的成熟度判断为：

`引导期已落地，当前位于 bootstrap-to-shadow 之间的工程化早期阶段；其中 aigc 主技能树仍运行在 bootstrap_compat 改造窗口，但 registry / route / runtime / template / audit 五条主骨架已稳定存在。`

已经完成的关键收束包括：

- 有宪章层，不再只靠零散 prompt 口头约束。
- 有三省角色合同，不再只有一个模糊 orchestrator。
- 有 registry / runbook / template / audit / runtime control plane，不再只是目录占位。
- 有 legacy mapping，不再默认从旧仓无治理复制。
- `aigc` 的主入口、卫星入口、项目内控制面与阶段状态已经纳入同一张注册表。
- `2-Global` 已开始对齐 `3-Detail` 的模板中心模式：默认围绕 `.agents/skills/aigc/2-Global/_shared/episode_root.json` 直接写 `episode_root.json`，旧 Markdown 下沉为兼容投影。
- `3-Detail` 阶段内合同已进一步收束为“单根技能 + references 模块 + `分镜构图` 先行”的固定主链，不再把 `1-水月 / 2-镜花` 视为当前主执行真源。
- `comic` 已成为独立受治理的 repo-local workflow，而不是根层手工串接。
- 团队能力类 skill 已不是“散落人物卡”，而是开始进入统一的注册、路由与真源口径。

仍然明显未完成的部分包括：

- `aigc` 虽已完成主骨架注册，但阶段内部合同仍在重构，尚未 fully cut over 到稳定影子态。
- 其中 `3-Detail` 已完成一轮根包收束，但与更老 runtime sidecar、旧 child 包与部分兼容校验之间仍存在历史兼容面，需要继续逐步去枝。
- `6-Video` 已升级为 active stage，但内部子路径和 provider 级执行面仍需继续收束。
- `7-Cut` 仍是注册层已声明、执行层未落地的搁浅阶段。
- 门下省的 `review` 已作为统一入口存在，但更细的专项 reviewer 席位仍未系统展开。
- 兵部侧 `resume` 已是受治理入口，但自动化 hook、批量恢复和更细粒度调度能力仍待补齐。
- 更大范围的 cross-skill eval、hook、auto-remediation 仍主要停留在骨架期。

## 可期发展方向

后续 HARNESS 工程建议按以下方向推进：

### 1. 从 bootstrap 走向 shadow

- 继续把 `aigc` 各阶段父合同从“已注册可路由”推进到“可稳定执行且审计可覆盖”。
- 让更多真实项目任务以 `projects/aigc/<项目名>/` 为主控制面闭环，而不是停留在根层治理准备态。
- 把阶段状态、局部可执行声明、项目控制面与审计覆盖进一步联动。

### 2. 从通用治理走向专项治理

- 在根 `aigc` 的高风险 preflight / validation gate 之上继续拆出故事审计、角色一致性、镜头语法、交付质量等专项 reviewer 席位。
- 为中书省补足更细粒度的任务起草、路线裁决与阶段切换策略。
- 为尚书省补足 `query / resume` 的深层产物索引、失败恢复与长流程执行策略。

### 3. 从人工驱动走向半自动化治理

- 将更多校验沉到 `scripts/`、`.codex/evals/` 与未来 hooks。
- 让 registry / route / template / audit 之间具备更强的一致性校验，包括主链阶段、卫星技能与 repo-local workflow 的协同审计。
- 为 HARNESS 关键变更建立更明确的同步检查与升级路径。

### 4. 从设计源继承走向制度化继承

- 继续以 `mapping -> review -> landing` 吸收 `AIGC-ZEN-VOID` 的高价值结构。
- 严禁未登记、未复核、未声明 canonical 落点的直接复制。
- 优先迁移制度资产、审计逻辑、路由经验和 suite 架构，而不是运行时内容产物。

### 5. 从单点规则走向系统防漂移

- 让新增或调整的 HARNESS 规则优先回收到单一真源。
- 减少在兄弟 agent 文档、技能文档、runbook 中平行复制相同合同。
- 将 `HARNESS.md` 维护成“总览投影”，而不是让它与真源竞争。

## 更新维护合同

`HARNESS.md` 的维护原则如下：

### 1. 真源优先

- 本文件是总览投影，不替代 `AGENTS.md`、registry、runbook、模板、agent 合同或审计脚本。
- 若本文件与真源冲突，以真源为准，并应尽快把本文件同步修正。

### 2. 变更即同步

当以下任一内容发生变化时，必须在同一轮任务内同步检查并更新 `HARNESS.md`：

- 根 `AGENTS.md` 中的 HARNESS 宪章、治理层级、硬门槛、闭环格式
- `.codex/templates/harness/office-governance-contract.md`
- `.codex/agents/harness治理/` 下任何 office 合同
- `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`
- `.codex/runbooks/task-lifecycle.md`
- `.codex/templates/harness/` 下任务工件结构或字段
- `scripts/aigc_harness_audit.py` 的审计口径
- `projects/aigc/<项目名>/` 与 `.codex/state/tasks/<task_id>/` 的 canonical / mirror 关系
- HARNESS 阶段成熟度、搁浅阶段、suite 规划、继承策略、自动化策略
- 多子智能体 skill 的父层总合同、`team.md` / agent docs 关系、以及相关 review / audit / route 路径的 canonical 绑定关系

### 3. 更新要求

每次更新本文件时，至少应检查以下四类内容是否仍然准确：

- 当前工程化构思是否变化
- 当前已实现真源与运行方式是否变化
- 现状判断与成熟度是否变化
- 可期发展方向与待补机制是否变化

### 4. 阻塞处理

- 如果某次 HARNESS 真源变更因为范围、权限或时机原因无法同步更新本文件，必须在任务结尾显式报告遗漏点与临时护栏。
- 不允许默默让 `HARNESS.md` 过期漂移。
