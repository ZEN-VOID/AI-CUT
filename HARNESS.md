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

当前针对 `.agents/skills/aigc/` 的重大改造，还额外启用了显式 `bootstrap_compat` 模式：

- 不清空 HARNESS 真源，只把它收缩为兼容骨架。
- 保留 `projects/aigc/<项目名>/`、registry、runbook、template、audit、卫星技能入口与 review gate。
- 暂时不把 `aigc` 当前阶段内部细节视为冻结真源，允许在后续改造中重写。

## 当前已实现真源

截至 `2026-04-15`，当前仓库已经完成了 HARNESS 引导期的最小真源收束，并开始把 `aigc` 根级卫星技能、`4-Design` 局部 active leaf、项目治理状态快照、根级 benchmark suite、repo-local 漫画链路与团队能力 skill 纳入受治理注册：

### 1. 宪章层

- 根 `AGENTS.md` 已明确：
  - 执行深度默认规则
  - 三省六部制编排治理基线
  - 批量技能调度默认规则
  - Rollout 标准
  - 根因优先、根因学习回路、真源治理、复合型输出治理等全局合同

### 2. 三省治理层

- `.codex/agents/harness治理/中书省.md`
- `.codex/agents/harness治理/门下省.md`
- `.codex/agents/harness治理/尚书省.md`

三省角色合同已经从“目录骨架”推进到“有共享上位合同、各自写差异职责”的状态。

### 3. 共享治理合同

- `.codex/templates/harness/office-governance-contract.md`

该文件已经承担跨 office 的单一共享真源职责，覆盖：

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

当前已显式声明：

- `aigc` 为仓库级总入口技能
- `aigc` 根下的 `query / resume / review` 已作为卫星技能登记到 `active_skills[id=aigc].satellite_index`
- `4-Design` 已在 `active_skills[id=aigc].stage_index[id=aigc-4-subject].leaf_index` 登记 `1-清单/{场景,角色,道具}`、`2-设计/{场景,角色,道具}` 与 `3-面板/{场景,角色,道具}` 的 active leaf；`3-面板` tranche parent 处于 `partial-active`，仍处于 `bootstrap_compat` 局部迁移窗口
- `comic` 已登记为 repo-local 漫画项目父级总入口，固定 canonical runtime 为 `projects/comic/[项目名]/`
- `comic-novel-adaptation` 已登记为 repo-local 改编技能，负责把文本、图片、视频、新闻事件与网络热搜改编为后续漫画生成可消费的小说底稿
- `comic-nine-blade-prompts` 已登记为 repo-local 提示词蒸馏技能，负责把小说或漫画小说桥接包输出为 `nine_blade_comic_prompts.v1` JSON
- `comic-generation` 已登记为 repo-local 执行技能，负责校验九刀流 JSON 并通过 Seedream 单次连续多图请求生成 9 张竖版漫画页
- `team-screenwriter-dazai-osamu` 已登记为编剧组 repo-local 人物叙事视角 skill，固定 skill 根为 `.agents/skills/team/编剧组/太宰治/`，其自包含调研载体为 `references/research/`
- `team-actor-leslie-cheung` 已登记为演员组 repo-local 人物表演视角 skill，固定 skill 根为 `.agents/skills/team/演员组/张国荣/`，其自包含调研载体为 `references/research/`
- `team-actor-anita-mui` 已登记为演员组 repo-local 人物表演视角 skill，固定 skill 根为 `.agents/skills/team/演员组/梅艳芳/`，其自包含调研载体为 `references/research/`
- `team-actor-leung-ka-fai` 已登记为演员组 repo-local 人物表演视角 skill，固定 skill 根为 `.agents/skills/team/演员组/梁家辉/`，其自包含调研载体为 `references/research/`
- `team-actor-maggie-cheung` 已登记为演员组 repo-local 人物表演视角 skill，固定 skill 根为 `.agents/skills/team/演员组/张曼玉/`，其自包含调研载体为 `references/research/`
- `team-actor-brigitte-lin` 已登记为演员组 repo-local 人物表演视角 skill，固定 skill 根为 `.agents/skills/team/演员组/林青霞/`，其自包含调研载体为 `references/research/`
- `team-director-park-chan-wook` 已登记为导演组 repo-local 人物导演视角 skill，固定 skill 根为 `.agents/skills/team/导演组/朴赞郁/`，其自包含调研载体为 `references/research/`
- `team-director-ang-lee` 已登记为导演组 repo-local 人物导演视角 skill，固定 skill 根为 `.agents/skills/team/导演组/李安/`，其自包含调研载体为 `references/research/`
- `team-director-hou-hsiao-hsien` 已登记为导演组 repo-local 人物导演视角 skill，固定 skill 根为 `.agents/skills/team/导演组/侯孝贤/`，其自包含调研载体为 `references/research/`
- `team-director-jiang-wen` 已登记为导演组 repo-local 人物导演视角 skill，固定 skill 根为 `.agents/skills/team/导演组/姜文/`，其自包含调研载体为 `references/research/`
- `team-director-bong-joon-ho` 已登记为导演组 repo-local 人物导演视角 skill，固定 skill 根为 `.agents/skills/team/导演组/奉俊昊/`，其自包含调研载体为 `references/research/`
- `team-cinematography-christopher-doyle` 已登记为摄影组 repo-local 人物摄影视角 skill，固定 skill 根为 `.agents/skills/team/摄影组/杜可风/`，其自包含调研载体为 `references/research/`
- `team-cinematography-wing-shya` 已登记为摄影组 repo-local 人物摄影视角 skill，固定 skill 根为 `.agents/skills/team/摄影组/夏永康/`，其自包含调研载体为 `references/research/`
- `team-cinematography-hiroshi-sugimoto` 已登记为摄影组 repo-local 人物摄影视角 skill，固定 skill 根为 `.agents/skills/team/摄影组/杉本博司/`，其自包含调研载体为 `references/research/`
- `team-action-ching-siu-tung` 已登记为武术组 repo-local 人物动作设计视角 skill，固定 skill 根为 `.agents/skills/team/武术组/程小东/`，其自包含调研载体为 `references/research/`
- `projects/aigc/<项目名>/` 是 `aigc` 项目工作流的 canonical runtime
- `projects/aigc/<项目名>/governance-state.yaml` 已被定位为结构化治理快照与断点真源
- `.codex/state/tasks/<task_id>/` 只作为治理镜像或通用账本
- `5-Image` 已升级为真实阶段父合同，当前统一收口 `1-提示词蒸馏 / 2-参照引用 / 3-图像生成`
- `6-Video` 已升级为部分可执行阶段，当前 `1-提示词蒸馏/全能参照 / 首帧参照` 可路由
- `7-Cut` 仍处于 `shelved` 状态
- `AIGC-ZEN-VOID` 作为 design source 通过 mapping 管理，而不是直接整仓继承

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

### 6. 审计与验证入口

- `scripts/aigc_harness_audit.py`
- `.codex/evals/`

当前审计能力已经能检查引导期最小 HARNESS 载体是否存在，以及关键合同锚点是否缺失。
同时，`scripts/aigc_skill_audit.py --strict` 已开始校验 `aigc` 的根级卫星技能是否完成目录、registry 与 route policy 对齐，并对 `CONTEXT.md` 的超 soft-limit、Case 失衡与日志化回流给出软警告；在 `bootstrap_compat` 下，至少仍会检查 active stage 父合同，避免父级 `SKILL.md` 的断链回指被误判为全绿。
同时，AIGC 项目运行时已经开始把 `project_state.yaml + governance-state.yaml` 视为“人类摘要 + 结构化控制面”的双状态组合。
同时，根级 `.agents/skills/aigc/benchmark-suite.yaml` 已落盘，作为后续动态评测的最小基线入口。

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

- harness 继续守住项目 runtime、治理工件 carriers、卫星技能入口与高风险预审。
- `scripts/aigc_skill_audit.py` 可降级深层阶段细节检查，不用旧叶子细节去卡住正在进行的结构重构；但仍需覆盖 active stage 父 `SKILL.md`，防止父级路由、真源或本地引用断链被静默放行。

对当前仓库而言，最重要的运行约束是：

- 复杂任务不能跳过起草工件。
- 高风险任务不能跳过预审。
- 非平凡失败不能跳过分层上溯。
- 新 skill、新 route、新模板字段、新继承映射不能绕过 registry / runbook / audit。
- 团队能力类 skill 不默认创建项目 runtime；其 canonical carrier 是对应 `.agents/skills/team/<组名>/<技能名>/` 根目录和自包含 `references/` 材料。
- 对由 `skill-subagents` 治理的多子智能体 skill，父 skill、`team.md`、agent docs、子路径合同与相关 review / audit / route 工件必须保持联动同步，不能只改其中一层就宣称源层收束。
- `CONTEXT.md` 必须保持知识库模式；详细时间线与迁移流水应外置到 `CHANGELOG.md` 或报告载体，而不是默认注入运行上下文。

## 现状判断

当前 HARNESS 的成熟度判断为：`引导期已落地，但仍处于 bootstrap-to-shadow 之间的工程化早期阶段；其中 aigc 主技能树当前运行在 bootstrap_compat 改造窗口。`

已经完成的不是“概念宣言”，而是以下几类关键收束：

- 有宪章层，不再只靠零散 prompt 口头约束。
- 有三省角色合同，不再只有一个模糊 orchestrator。
- 有 registry / runbook / template / audit / runtime control plane，不再只是目录占位。
- 有 legacy mapping，不再默认从旧仓无治理复制。
- 已出现多类受 registry 管理的 repo-local 非 `aigc` 技能，包括漫画项目链路、编剧组人物叙事视角、演员组人物表演视角、导演组人物导演视角、摄影组人物摄影视角与武术组人物动作设计视角；编剧组已纳入太宰治等自包含人物叙事视角，演员组当前已有张国荣、梅艳芳、梁家辉、张曼玉、林青霞五个自包含人物表演视角，导演组已继续纳入朴赞郁、李安、侯孝贤、姜文、奉俊昊等自包含人物导演视角，摄影组已纳入杜可风、夏永康与杉本博司三个自包含人物摄影视角，武术组已纳入程小东动作设计视角，用来验证“非项目型/团队能力型技能也能走受治理注册与路由”。

仍然明显未完成的部分也很清楚：

- 业务级 suite skill 还没有 fully cut over 到本地 HARNESS 真源。
- 门下省已经有 `review` 卫星技能作为项目级 preflight / validation / learning bridge 入口，且其下已开始拆分 `preflight-review / acceptance-review / learning-bridge` 三个受治理子技能；更细分的内容专项 reviewer 仍未系统展开。
- 兵部侧已有 `resume` 卫星技能作为续跑与安全回接入口，但自动化 hook、批量恢复与更细粒度调度能力仍在待接入阶段。
- `6-Video` 已从纯预留升级为部分可执行阶段，但其余视频子路径仍待补齐。
- `7-Cut` 仍然是架构上预留、执行上搁浅的阶段。
- 面向真实项目任务的项目内工件落盘与审计闭环，还需要持续在 `projects/aigc/<项目名>/` 实战固化；当前已不再停留在纯 `validation-report` 单点闭环，首个项目已补入 `preflight-verdict.yaml` 与 `learning-record.md`。

## 可期发展方向

后续 HARNESS 工程建议按以下方向推进：

### 1. 从 bootstrap 走向 shadow

- 在 `comic` 父级总入口与 `comic-novel-adaptation / comic-nine-blade-prompts / comic-generation` 三段链基础上，继续补齐项目状态、续跑、验收与批量任务能力。
- 继续把 `aigc` 根级卫星技能从“已注册”推进到“可稳定复用的标准治理入口”。
- 继续把 `governance-state.yaml` 从 AIGC 项目内的专项控制面推广为更稳定的复用治理模式。
- 让更多真实任务以 `projects/aigc/<项目名>/` 为主控制面闭环，而不是停留在根层治理准备态。
- 把阶段状态、局部可执行声明、项目控制面与审计覆盖进一步联动。

### 2. 从通用治理走向专项治理

- 在现有 `review` 卫星技能之下继续拆出故事审计、角色一致性、镜头语法、交付质量等专项 reviewer 席位。
- 为中书省补足更细粒度的任务起草、路线裁决与阶段切换策略。
- 为尚书省补足 `query / resume` 的深层产物索引、失败恢复与长流程执行策略。

### 3. 从人工驱动走向半自动化治理

- 将更多校验沉到 `scripts/`、`.codex/evals/` 与未来 hooks。
- 让 registry / route / template / audit 之间具备更强的一致性校验，包括根级卫星技能与主阶段链的协同审计。
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
