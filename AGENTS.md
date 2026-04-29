# AGENTS.md

行业通用的 AI 智能体指令文件。兼容 Claude Code、Cursor、Windsurf 及其他 AI 编码工具。

## 项目基线

### 项目概览

AIGC（AI Generated Content）视频·小说·漫画创作管理工作区。该仓库不是传统意义上承载多个独立软件子项目的代码仓，而是用于组织 AIGC 创作流的项目工作台：

- 以 `projects/aigc/<项目名>/` 作为单个创作项目的主要工作空间
- 在项目空间内逐步沉淀文本、图片、视频及其过程工件
- 以仓库根层的规则、模板、脚本与治理工件，为多个创作项目提供统一编排能力

### 常用命令

```bash
# Git
git status                    # 查看工作区状态
git diff                      # 查看未暂存改动
git log --oneline -20         # 查看最近提交

# Python
python3 <script>              # 运行 Python 脚本
python3 -m pytest tests/      # 运行测试
python3 -m pip install <pkg>  # 安装依赖包
```

### 编码风格与命名约定

- **语言**：以 Python 3.12+ 为主，Shell 脚本用于自动化。
- **风格**：遵循 Python 的 PEP 8，尽可能补充类型标注。
- **命名**：Python 使用 `snake_case`，文件名使用 `kebab-case`。
- **提交**：使用 Conventional Commits 规范（`type(scope): description`）。
- **文档**：公共函数使用 docstring，行内注释仅在必要时添加。
- **测试**：实现改动应尽量配套测试。
- 分镜 ID 使用四段式模式：`episode-scene-group-frame`，例如 `1-1-1-1`。
- 小说创作的章节单位层级默认使用：`部 -> 卷 -> 章`。
- 小说创作中默认 `10 章 = 1 卷`。
- 小说创作中默认 `6 卷 = 1 部`；若任务、项目设定或用户明确额外强调，则可按声明例外处理。
- 创作项目通常以 `projects/aigc/<项目名>/` 作为主工作目录，并在其中组织文本、图片、视频及阶段产物。
- 模板要求时，提示中的任务 ID 应保持 ASCII 安全字符。

### 重命名引用同步（强制）

- 当重命名文件或文件夹时，必须自动扫描整个仓库中对旧路径的引用，并同步更新到新路径。扫描范围包括脚本、配置、`SKILL.md`、`CONTEXT.md`、命令文档、模板以及其他 markdown / 代码文件。
- 扫描目标包括但不限于：`import` / `require` 语句、路径字符串、符号链接、JSON / YAML 配置项、markdown 链接以及 shell 命令参数。
- 如果某些引用无法自动更新，例如存在于二进制文件或外部系统中，必须显式向用户报告该遗留引用。

### 架构决策

- `projects/` 是项目总容器；对当前仓库的 AIGC 影视工作流，规范命名空间固定为 `projects/aigc/`，而不是把项目直接平铺在 `projects/` 根层。
- 对当前仓库，创作项目的 canonical runtime 统一落在 `projects/aigc/<项目名>/`；影片/小说等媒介归属应通过技能路由、项目元数据或命名约定表达，而不是再引入 `projects/影片/<项目名>/` / `projects/小说/<项目名>/` 作为第二层路径真源。
- 共享工具与配置统一放在 `scripts/` 和 `configs/` 中。
- `reports/` 用于保存开发或任务过程中的报告，允许按主题、日期或自动化流程归类。
- `PRPs/` 用于保存大型开发计划与阶段性实施方案。
- `docs/` 用于保存重要知识、制度说明与典藏文档。
- `templates/` 中的模板用于脚手架与标准化生成。
- 本仓库的治理基线采用 `三省六部制 + 编排工程` 架构，而不是临时拼接的提示词集合。
- 当前编排治理的引导期真源已收束为：根 `AGENTS.md` + `.codex/templates/harness/office-governance-contract.md` 共享合同，配合 `.codex/agents/harness治理/`、`.codex/registry/`、`.codex/runbooks/`、`projects/aigc/<项目名>/` / `.codex/state/tasks/`、`.codex/evals/`、`.codex/templates/harness/` 与 `scripts/aigc_harness_audit.py`。
- `AIGC-ZEN-VOID` 被视为本仓库下一代影视工作流的发源仓库，但其继承必须通过显式映射与复核进行，而不能直接整仓复制。

### 测试指引

- 当前仓库未配置专门的测试框架。优先采用脚本级检查、示例运行或局部验证（参见 `scripts/` 与相关技能目录）。
- 新增脚本时，应尽量附带最小可运行示例或 dry-run 模式。

### 提交与 Pull Request 指引

- 提交信息通常遵循两类模式之一：项目同步时间戳格式，例如 `项目同步更新 - YYYY-MM-DD HH:MM`；或 `feat(scope): description`。
- PR 应保持聚焦，描述中应包含简要变更说明、影响的阶段（例如 3.x 分镜阶段）以及涉及的生成资产或报告。
- 如新增或修改报告，请写入 `reports/`，并使用类似 `报告类型-YYYYMMDD.md` 的日期后缀。

### 安全与配置提示

- 严禁提交 `.env` 文件或 API 密钥。请使用 `.env.example` 作为模板。
- 如果遇到类似 `/Volumes/...: No such file or directory` 的工作区路径错误，请运行 `python3 scripts/workspace_doctor.py` 检查或挂载工作区后再重试。

### 智能体专用指令

- 默认交互语言为中文；仅当任务确实需要英文输出时才切换。

## SKILL2.0

### 内容创作型任务的 LLM 主创规则（强制）

- 对 `SKILL` 命中的内容创作型任务，核心创作环节必须由 LLM 直接完成，不得把脚本当作主创执行器。
- 这里的“核心创作环节”包括但不限于：故事/章节正文、剧本改编、角色设定、场景设定、道具设定、研究结论、设计描述、提示词蒸馏、分镜/面板创作决策、海报文案、创作型总结与其他需要审美判断、叙事判断、风格判断的正文生成。
- 脚本只允许承担非主创辅助职责，例如：读取、抽取、切分、组装、格式转换、模板投影、复制粘贴、路径归档、批量提交、去重、校验、审计、统计、diff、manifest 回写与其他机械性流程。
- 脚本不得直接生成上述核心创作正文，不得以规则拼接、模板灌字、启发式补句、字段压缩扩写等方式替代 LLM 创作；即便脚本生成结果“可读”，也不得将其视为 canonical creative truth。
- 若某个内容创作型 skill 当前仍以脚本生成创作正文、提示词、设计稿、研究稿、layout 决策或等价创作产物，必须判定为源层违规，并回收为：`LLM 直出 canonical creative truth -> 脚本仅做投影/校验/落盘/执行辅助`。
- 对现有工作流的兼容改造，允许暂时保留脚本型 carrier、validator、runner 与 provider bridge，但不得继续扩大脚本主创覆盖面；任何新增创作链路默认必须按 `LLM-first creative authorship` 设计。
- 审查此类问题时，必须沿链路上溯：`Symptom -> Direct Script Overreach -> Skill/Template/Runner Source -> AGENTS.md 本条规则`。

### 批量 SKILL 调度默认规则（强制）

- 对 `skills` 子技能包的同级调度，命名前缀本身即为默认调度语义，无需额外显式声明。
- 无序号子技能包：命中同级无序号子技能包组时，默认全选并行执行。
- 数字序号子技能包：形如 `1-`、`2-`、`3-` 的同级子技能包默认按数字升序顺序串行执行。
- 英文序号子技能包：形如 `A-`、`B-`、`C-` 或 `a-`、`b-`、`c-` 的同级子技能包默认作为互斥候选，按用户意图、父技能路由或任务类型单选执行。
- 上述命名前缀语义仅针对 `skills` 子技能包与技能层调度，不外推到 subagents；subagents 一般不以名称序号承载调度语义。
- 若用户显式指定不同调度方式，以用户显式指令优先；否则按本命名前缀语义执行。

### Subagents 默认权限与降级口径（强制）

- 对命中 `skill-subagents`、team reviewer runtime、`master-check*`、阶段末 `supervision/review`、或其他已声明 subagent 合同的任务，默认应真实启动 subagents，而不是先由主 agent 本地模拟顾问流程。
- 当阶段或技能合同已声明 `use_subagents_by_default == true`、`parallel-council`、`serial-refine`、`single-reviewer`、`reviewer -> subagent` 等显式分发语义时，真实 subagent dispatch 视为默认主路径，而不是可有可无的增强项。
- 当用户手动点名执行某个 skill，或当前任务被仓库路由自动命中到某个 skill，且该 skill / 阶段合同已显式声明“默认走 subagents / parallel workers / reviewer -> subagent”，则在仓库治理口径内，这次 skill 执行本身就视为用户已对该默认 subagent 路径给出显式许可；主 agent 不得再把“用户没有额外补一句允许并行”当作默认不启动的理由。
- 一个 reviewer skill 默认对应一个 subagent；主 agent 负责路由、汇流、裁决与最终 canonical 写回，不得把“主 agent 顺序扮演多个 reviewer”表述成正常的 subagent 执行。
- 仅在以下情况允许降级为本地顺序纪要、顺序读取 skill 合同、或其他非真实 subagent 路径：
  - 当前会话的更高优先级 system / developer / tool policy 明确阻断
  - 当前环境或工具权限无法真实启动 subagents
  - 用户显式要求不要启用 subagents
- 若上条“视为显式许可”的仓库口径与更高优先级 system / developer / tool policy 冲突，仍必须服从更高优先级约束；此时应报告“仓库层已视为许可，但上层策略仍阻断真实 dispatch”，不得把阻断原因误记为“用户未授权”。
- 若发生降级，必须显式报告：
  - 阻断来源属于 `system / developer / tool / user` 的哪一层
  - 原本应执行的 subagent 路径是什么
  - 实际采用的降级路径是什么
  - 哪些 reviewer / 角色 / 子任务没有真实启动
- 根 `AGENTS.md` 可以定义仓库内“默认应真实启动 subagents”的治理口径，但不得宣称能够覆盖更高优先级权限层；若与上层权限冲突，必须服从上层并按前条显式报告降级。

### 仓库 Rollout 标准（强制）

- 长期维护的 skill 默认按 Skill 2.0 包结构建设；旧技能包进入升级窗口时，应以 `skill-工作车间` 的目录合同为当前 canonical 参考，不得继续把长细则、步骤、类型策略和审查规则堆回单一 `SKILL.md`。
- Skill 2.0 标准目录结构如下；创建、修复或升级时若出现拼写变体，应归一到这些 canonical 名称：

  ```text
  skill-name/
  ├── references/
  ├── scripts/
  ├── templates/
  ├── review/
  ├── steps/
  ├── knowledge-base/
  ├── types/
  ├── agents/
  │   └── openai.yaml
  ├── CHANGELOG.md
  ├── SKILL.md
  ├── CONTEXT.md
  └── README.md
  ```

- 常见目录拼写变体必须归一：`reference` / `refs` -> `references/`，`script` / `tools` -> `scripts/`，`template` -> `templates/`，`reviews` / `audit` -> `review/`，`step` / `workflow` / `workflows` -> `steps/`，`knowledge_base` / `knowledgebase` / `kb` -> `knowledge-base/`，`type` / `type-map` / `typings` -> `types/`，`agent` / `agent-config` / `agent-configs` -> `agents/`；若 alias 与 canonical 同时存在，不得自动覆盖，必须先合并再删除 alias。
- Skill 2.0 分区可以以最小占位启动，但每个分区至少应包含一个说明文件，避免空目录在迁移、同步或版本控制中丢失。
- 父级导引 skill 是 Skill 2.0 的轻量 tier：当某个 `SKILL.md` 只负责路由、子技能/卫星技能边界、共享真源裁决、聚合门禁和回接关系，且不直接拥有业务执行细则、类型包、模板或质量评估细则时，必须在 frontmatter 中声明 `governance_tier: router`，其本级最小结构只要求同目录 `SKILL.md + CONTEXT.md`。
- `governance_tier: router` 只豁免本级完整分区、`README.md`、`CHANGELOG.md` 与 `agents/openai.yaml` 的强制要求，不豁免同目录 `CONTEXT.md`、Context Loading Contract、Root-Cause 合同、清晰输入/路由/输出或回接合同，也不降低子技能、卫星技能和真正执行型主技能的 Skill 2.0 要求。
- 父级导引 skill 可以按真实需要引用共享 `_shared/`、registry、routes 或既有父级细则文件；这些共享载体不等同于本级必须拥有完整 `references/`、`steps/`、`review/`、`types/`、`templates/`、`knowledge-base/`、`scripts/`、`agents/` 分区。若父级开始直接拥有执行细则、模板、类型策略、脚本或 review 真源，应取消 `governance_tier: router` 并升级为 `lite` 或 `full`。
- Skill 2.0 的核心 owner 边界：
  - `SKILL.md` 只保留入口、触发、路由、动态引用、关键门禁、Root-Cause 合同和输出合同。
  - `CONTEXT.md` 保存经验性 Type Map、Repair Playbook 与 Reusable Heuristics，不承载核心执行合同和流水日志。
  - `references/` 承载复杂规范、长细则、背景资料和专项规则展开，不拥有入口路由权。
  - `steps/` 承载思维与执行一体化节点、串并行、分支、汇流、回退和证据门，不替代类型矩阵。
  - `review/` 承载质量评估、审计规范、review provider 接入和交付门禁，不改写业务主真源。
  - `types/` 承载类型变量、类型映射矩阵和分型策略，不承载完整执行步骤。
  - `knowledge-base/` 承载人工添加的外部知识库、参考资料包和领域资料索引，不承载执行中沉淀的经验、heuristic 或强制合同。
  - `templates/` 承载输出模板、脚手架模板和报告模板，不承载运行状态。
  - `scripts/` 只承载机械创建、校验、格式转换、批量处理等自动化辅助，不替代 LLM 主创判断。
  - `agents/openai.yaml` 承载产品侧入口元数据，至少包含 `interface.display_name`、`interface.short_description` 与显式提到 `$skill-name` 的 `interface.default_prompt`。
  - `README.md` 承载目录树、快速说明和入口命令；`CHANGELOG.md` 承载版本更新与迁移摘要。
- Skill 2.0 的经验沉淀落点必须保持单一：执行中产生的新经验、稳定经验、失败模式、成功模式、修复打法与 reusable heuristic 均写入同目录 `CONTEXT.md`；`knowledge-base/` 只接收用户或维护者手动加入的外部知识材料，不作为自动学习、复盘或经验晋升的落点。
- 每个长期维护的 skill 都应包含：
  - 在 `SKILL.md` frontmatter 中声明 `governance_tier: full | lite | router`
  - 在 `SKILL.md` 中包含 `Context Loading Contract`：明确该技能每次被调用时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文
  - 在 `SKILL.md` 中包含 `Reference Loading Guide` 或等价动态引用表，声明何时加载 `references/`、`steps/`、`review/`、`types/` 与其他分区
  - 在 `SKILL.md` 中包含与本全局政策对齐的 Root-Cause 执行合同，并附带上溯到 meta 层合同的钩子
  - 在 `SKILL.md` 中根据 tier 提供字段中心映射（Tier-Full 使用三张表；Tier-Lite 使用合并表）
  - 在 `CONTEXT.md` 中包含知识库核心（Type Map、Repair Playbook 与/或 Reusable Heuristics）
  - `CONTEXT.md` 不再维护 `Case Log` / `Case Record` 专栏；里程碑经验也应折叠沉淀到知识库核心，详细过程外置到 `CHANGELOG.md` 或 `reports/`
  - 对 `full` / `lite` 技能，在 `agents/openai.yaml` 中提供产品侧入口元数据，不得把入口摘要偷渡成强于 `SKILL.md` 的隐藏执行规则；`router` 父级导引可不设本级 `agents/openai.yaml`，由上级或叶子入口承接产品发现
- 声明 `governance_tier: router` 的父级导引 skill 应改按轻量基线验收：
  - 同目录必须存在 `SKILL.md + CONTEXT.md`，且 `SKILL.md` frontmatter 必须包含 `governance_tier: router`
  - `SKILL.md` 必须包含 `Context Loading Contract`、输入边界、子技能/卫星技能索引或路由表、真源边界、Root-Cause 执行合同、Output / Handoff / Aggregation 合同
  - `CONTEXT.md` 必须包含经验性 `Type Map`、`Repair Playbook` 与/或 `Reusable Heuristics`
  - 本级不得虚设空分区来满足形式检查；若确有本级专属分区，必须说明其 owner 边界，且不得与子技能分区形成第二真源
- 上述基线适用于主技能、受治理子技能与长期维护的卫星技能；非执行型细则模块不单独视为独立 skill 基线对象。
- 由元技能生成的新技能，必须初始化完整 Skill 2.0 目录、根文件与 `agents/openai.yaml`，并满足上述基线；不得回退为“只有主合同 + 经验层”。
- 旧技能包升级到 Skill 2.0 时，必须先建立迁移矩阵，标注旧 `SKILL.md`、同目录资源与入口元数据中每个 section / 资源的 target owner、迁移动作、语义风险、引用更新与验证门禁；删除旧段落前必须能追到新 owner 或明确归档/丢弃理由。
- 重命名、拆分或迁移 skill 文件/目录后，必须同步扫描并更新 `SKILL.md`、`CONTEXT.md`、`README.md`、`CHANGELOG.md`、`agents/openai.yaml`、`scripts/`、`templates/`、markdown 链接、registry、routes、runbook 与项目内引用；无法自动更新的外部或二进制引用必须写入最终报告；若形成可复用经验，再沉淀到同目录 `CONTEXT.md`。
- 创建或升级 Skill 2.0 包后，应运行对应元技能提供的结构校验器或仓库内等价审计；脚手架类改动还应额外生成临时目标 skill 做端到端冒烟验证。
- 对 `story` 与 `aigc` 这类项目型创作工作流，初始化项目目录时还必须同步创建项目级 `MEMORY.md`：
  - `projects/story/<项目名>/MEMORY.md`
  - `projects/aigc/<项目名>/MEMORY.md`
- 对 `story` 与 `aigc` 这类项目型创作工作流，初始化项目目录时还必须同步创建项目级 `CONTEXT/`：
  - `projects/story/<项目名>/CONTEXT/`
  - `projects/aigc/<项目名>/CONTEXT/`
- 项目级 `MEMORY.md` 是当前项目的创作记忆载体，用于沉淀跨阶段持续生效的偏好、口味、习惯、特殊元素、禁区与长期要求。
- 项目级 `CONTEXT/` 不替代技能同目录 `CONTEXT.md`；它是项目运行时的附加上下文根，面向整个创作阶段共享。
- `scripts/skill_context_audit.py --strict` 用于全仓校验：每个纳入范围的 `SKILL.md` 是否存在同目录 `CONTEXT.md`，并是否声明 `Context Loading Contract` 与“必须同时加载同目录 `CONTEXT.md`”规则。
- `scripts/aigc_skill_audit.py --strict` 用于校验：tier 声明是否存在、对应 tier 所需表格是否齐全、`CONTEXT.md` 的基线章节是否存在；同时应对 `CONTEXT.md` 的日志化倾向、旧 `Case Log` 残留与超 soft-limit 状态给出软警告。缺项应被视为审计失败。
  - 对 `aigc` 技能树，还应校验阶段注册状态、搁浅阶段声明以及 `projects/aigc/<项目名>/` 项目根运行时合同是否已同步进入 registry / routes / audit。
- 对 `.agents/skills/team/` 技能树，凡成员配置出现新增、删除、重命名、迁移或适配场景显著变化，都必须在同一轮任务内同步更新 `.agents/skills/team/SKILL.md` 的 `Member And Scenario Index`；不得允许 team 子树与根索引脱节。

### 技能组成与语义

- 技能目录基线：
  - 长期维护的可执行 skill 默认采用 Skill 2.0 目录结构：`SKILL.md`、`CONTEXT.md`、`README.md`、`CHANGELOG.md`、`references/`、`steps/`、`review/`、`types/`、`knowledge-base/`、`templates/`、`scripts/`、`agents/openai.yaml`
  - 父级导引 skill 若声明 `governance_tier: router`，默认采用轻量结构：`SKILL.md`、`CONTEXT.md`；它通过父级合同路由到子技能、卫星技能、共享 `_shared/` 或真实脚本，不要求本级完整 Skill 2.0 分区
  - `SKILL.md`：必需，作为入口、路由、动态引用、关键门禁和输出合同
  - `CONTEXT.md`：必需，作为预加载运行上下文和经验性知识库
  - `references/`、`steps/`、`review/`、`types/`、`knowledge-base/`、`templates/`、`scripts/`、`agents/`：作为 Skill 2.0 功能分区，不得用拼写变体平行演化
  - `assets/` 仅在技能确有静态素材需要时作为业务资源目录使用，不属于 Skill 2.0 canonical 必备分区；若出现，应由 `SKILL.md` 或 `README.md` 说明所有权和加载方式
- `SKILL` 细分定位（仓库级规范）：
  - 主技能：拥有一段业务域或一条阶段链的总入口、总路由、共享载体边界与真源裁决权。形态通常为 `<skill-root>/SKILL.md + CONTEXT.md`，也可以是技能树中的阶段根，例如 `aigc/1-规划`。
  - 父级导引 skill：主技能或阶段根的一种轻量形态，只负责路由、边界、聚合、回接和门禁，不直接拥有子技能的执行细则、模板、类型包或 review 真源；必须在 frontmatter 中声明 `governance_tier: router`。
  - 子模块：主技能或子技能为了拆分长细则而挂出的非执行模块，可落在 `references/`、`steps/`、`review/`、`types/`、`templates/`、schema、spec、helper 或其他被合同显式声明的专项细则载体中；它们提供规则细则，但不拥有独立调度权、闭环权或经验层主权。
  - 子技能：受治理的可执行下钻单元；其路径、命名与载体形态必须由父级主技能显式声明，不再绑定固定目录包裹约定。它们由父级主技能路由进入，负责局部执行合同，不得擅自越权为新的总入口。
  - 卫星技能：与主技能同根同级放置的旁路可执行 skill，推荐形态为 `<skill-root>/<satellite-name>/SKILL.md + CONTEXT.md`；它们服务查询、恢复、复核、汇总、桥接等辅助职责，可被直接调用，但不默认冒充新的主链 stage 或新的父级总线。
- 结构判定规则：
  - 若某单元只提供长细则、模板、schema、思维链或策略表，而不独立受理任务，则它是子模块，不是子技能。
  - 若某单元必须经父级路由进入，且其结果默认回流到父级共享目标，则它优先视为子技能。
  - 若某单元与主技能同根同级存在，可直接被用户或上游命中，承担查询/恢复/审查承接等旁路职责，则它优先视为卫星技能。
  - 若某单元既想直达受理任务，又想长期维护独立 `CONTEXT.md`，则不得伪装成普通细则模块，必须显式定义为子技能或卫星技能之一。
- 现有结构判例：
  - `aigc/SKILL.md` 与各阶段根（如 `aigc/1-规划`、`aigc/3-Detail`）属于主技能层。
  - 跨项目仓 `story2026/query`、`story2026/resume` 属于卫星技能层；`story2026/review` 若被根技能声明为旁路承接而非主链真源拥有者，也应按卫星技能合同治理其边界。
- `卫星技能` 的角色：
  - 是主技能侧的旁路执行层，而不是普通细则模块，也不是默认加入主链阶段序列的子技能
  - 必须在主技能 `SKILL.md` 中显式声明其 `stage_position`、`truth ownership`、`not-owned truth` 与回接关系
  - 可共享主技能的 `scripts/`、`templates/` 与其他共享模块载体，但不得借共享载体偷渡新的总线规则
  - 默认只拥有辅助真源或辅助动作权，例如查询、恢复、审查承接、状态持久化、桥接；不得改写主技能或主链 stage 的 canonical truth 判定权
- `SKILL.md` 的角色（硬规则）：
  - 定义范围、触发条件、必需输入、Mode Selection、Reference Loading Guide、核心工作流、工具/脚本入口、输出合同与质量门槛
  - 必须明确、可执行、偏确定性；避免长篇叙述，也不要存放易过期的零散技巧
  - 对 Skill 2.0 包，`SKILL.md` 可以摘要并回链分区细则，但不得复制 `references/`、`steps/`、`review/`、`types/` 或外部 `knowledge-base/` 的完整正文；若 `references/`、`steps/`、`review/` 或 `types/` 改变主流程，必须同步回改 `SKILL.md` 的拓扑和引用表；`knowledge-base/` 不得直接改变主流程
- `agents/openai.yaml` 的角色（入口元数据层）：
  - 承载 `interface.display_name`、`interface.short_description`、`interface.default_prompt` 等 UI-facing 元数据
  - `interface.default_prompt` 应显式提到 `$skill-name` 或目标 skill 的标准唤起名
  - 负责 Codex 发现与进入技能时的入口摘要，但不得偷渡比主 `SKILL.md` 更强的执行规则
- `references/` 的角色（细则层）：
  - 保存复杂规范、详细规则、背景资料、专项合同和可独立回指的长细则
  - 不拥有入口路由权；若细则需要改变主流程，必须回改 `SKILL.md`
- `steps/` 的角色（思行网络层）：
  - 保存串行、并行、树、网、分支、汇流、回退、证据门与执行节点
  - 节点应同时表达判断、动作、证据、路由和 gate，不应退化为普通 checklist
- `review/` 的角色（质量门禁层）：
  - 保存质量评估、审计规范、评分模型、review provider 接入与验收 verdict
  - 不拥有业务主真源改写权；审查结论应通过主技能的聚合与回写规则生效
- `types/` 的角色（类型策略层）：
  - 保存类型变量、类型映射矩阵、分型策略和 `type_profile` 生成规则
  - 多类型任务应先判型，再让 `steps/` 消费类型画像进入对应分支
- `knowledge-base/` 的角色（外部知识库层）：
  - 保存用户或维护者手动添加的外部知识库、参考资料包、资料索引、摘录入口与领域背景材料
  - 不承载执行中沉淀的新经验、稳定经验、reusable heuristic、失败复盘或强制合同；这些经验一律写入同目录 `CONTEXT.md`，若稳定到必须执行，再晋升到 `SKILL.md` 或对应规范分区
- `templates/` 的角色（模板层）：
  - 保存输出模板、脚手架模板、报告模板与可复用结构样板
  - 不承载运行状态，也不作为任务唯一验收标准
- `scripts/` 的角色（自动化辅助层）：
  - 保存初始化、校验、格式转换、路径归一、批量处理等机械辅助脚本
  - 不得替代 LLM 对目标 skill 业务合同、审美判断、叙事判断或复杂策略的主创设计
- `CONTEXT.md` 的角色（经验层）：
  - 保存可复用的 heuristic：成功/失败案例、陷阱、调试线索、兼容性注记、提示技巧与战术捷径
  - 作为规划/执行时的预加载上下文，但不得重定义核心合同
  - `CONTEXT.md` 中的 Type Map 属于经验性映射与修复知识；同一技能的规范型类型化处理 / 多模式策略，应落在主合同显式回指的专项模块或共享 spec，而不是继续整合进 `CONTEXT.md`
- `MEMORY.md` 的角色（项目记忆层）：
  - 保存当前项目跨阶段持续生效的创作偏好、审美口味、表达习惯、必须保留元素、明确禁区、长期协作要求与其他“以后继续按这个项目执行”的稳定约束
  - 只服务当前项目，不承载跨项目 heuristic、源层故障复盘、脚本调试经验或技能治理规则
  - 当用户明确要求“记住”、给出会影响后续多个阶段的长期偏好/限制，或对既有项目偏好作出替换/撤销时，必须在同轮同步更新对应项目根 `MEMORY.md`
  - 临时任务指令、一次性试验口味、局部实现细节与根因学习结论不得写入 `MEMORY.md`
- `SKILL` 调用上下文加载合同（硬规则）：
  - 每次调用任意 `SKILL.md` 时，必须同时加载该 `SKILL.md` 同目录 `CONTEXT.md` 作为预加载上下文，不得只读取 `SKILL.md` 而跳过同目录经验层。
  - 若同目录 `CONTEXT.md` 缺失，则视为该 skill 基线不完整；执行前应优先补齐，或在当前任务中显式报告该缺口与临时护栏。
  - 若当前任务已绑定具体项目根，且命中 `.agents/skills/story/` 或 `.agents/skills/aigc/` 任一技能树，则除技能同目录 `CONTEXT.md` 外，还必须先加载项目根 `MEMORY.md`，再加载项目根 `CONTEXT/` 中与当前任务相关的上下文文件。
  - 项目根 `MEMORY.md` 负责项目偏好、口味、长期要求与特殊元素；项目级 `CONTEXT/` 负责项目共享材料、项目补充事实、运行期附加上下文与非偏好型参考，不得互相替代。
  - 项目级 `MEMORY.md` 的标准落点仅限：
    - `projects/story/<项目名>/MEMORY.md`
    - `projects/aigc/<项目名>/MEMORY.md`
  - 项目级 `CONTEXT/` 的标准落点仅限：
    - `projects/story/<项目名>/CONTEXT/`
    - `projects/aigc/<项目名>/CONTEXT/`
- `CHANGELOG.md` 的角色（派生变更史）：
  - 承载时间序变更摘要、迁移过程、结构调整说明与长段审计/执行时间线
  - 默认不作为运行时上下文自动加载，也不拥有规范裁决权或经验裁决权
  - 仅用于帮助追溯“发生了什么变化”，不得替代 `CONTEXT.md` 的知识库职责
- 子技能自身 `SKILL.md` 的角色（子技能规范合同）：
  - 定义该子技能的局部合同、边界、加载顺序、命名规则与进入条件
- 子技能自身 `CONTEXT.md` 的角色（子技能经验层）：
  - 仅保存该子技能自身的局部 heuristic、陷阱、案例与修复模式
  - 不得吞并属于主技能根层 `CONTEXT.md` 的跨子技能或整技能经验
- `<satellite-name>/SKILL.md` 的角色（卫星技能规范合同）：
  - 定义该卫星技能的旁路职责、触发条件、共享载体依赖、可拥有真源与禁止越权范围
  - 必须写清它与主链或主技能的回接位置，避免卫星技能演化成隐式第二总入口
- `<satellite-name>/CONTEXT.md` 的角色（卫星技能经验层）：
  - 仅保存该卫星技能自身的局部 heuristic、运行陷阱、恢复/查询/承接策略
  - 不得吞并属于主技能根层 `CONTEXT.md` 的跨卫星、跨主链或整技能经验
- 运行时加载顺序与优先级：
  1. 每次命中任意 skill 时，先成对定位当前命中的 `SKILL.md` 与其同目录 `CONTEXT.md`；二者共同构成该 skill 的默认预加载入口。
  2. 先解析当前命中的 `SKILL.md`，锁定强制约束、总路由与真源边界。
  3. 立即加载该 `SKILL.md` 同目录 `CONTEXT.md`，用于选择策略并避开该技能已知经验性失败模式。
  4. 若当前任务已绑定 `projects/story/<项目名>/` 或 `projects/aigc/<项目名>/`，则在进入具体阶段执行前，先加载该项目根 `MEMORY.md`，再加载项目根 `CONTEXT/` 目录中与本轮任务相关的上下文文件；前者是项目创作记忆，后者是项目共享附加上下文。
  5. 若进入某个受治理子技能，按同样规则加载该子技能在父级合同中声明的局部 `SKILL.md + CONTEXT.md`；若进入某个卫星技能，按同样规则加载 `<satellite-name>/SKILL.md + CONTEXT.md`，锁定其局部合同与局部经验层。
  6. 若当前主技能、子技能或卫星技能采用 Skill 2.0 动态引用模式，则按 `Reference Loading Guide` 动态加载分区：复杂规则读 `references/`，执行拓扑读 `steps/`，质量门禁读 `review/`，分型任务先读 `types/` 形成 `type_profile` 后再进入 steps 分支；模板、schema、spec 与其他模块按任务需要读取。
  7. `CHANGELOG.md`、执行报告、迁移记录与其他时间序载体默认不预加载；仅在需要追溯详细变更过程时按需读取。
  8. 冲突优先级：用户显式请求 > `AGENTS.md` / meta 规则 > 主 `SKILL.md` > 当前命中的子技能或卫星技能 `SKILL.md` > 已声明的 `references/` / `steps/` / `review/` / `types/` / 模板 / spec > `agents/openai.yaml` > 项目级 `MEMORY.md` > 项目级 `CONTEXT/` > 主 `CONTEXT.md` > 当前命中的子技能或卫星技能 `CONTEXT.md` > 按需读取的 `CHANGELOG.md`
- 维护规则：
  - 新的或尚不稳定的经验先写入 `CONTEXT.md`
  - 稳定、可重复、高置信度的实践再从 `CONTEXT.md` 晋升到 `SKILL.md`
  - 每个显著失败都应在 `CONTEXT.md` 中记录：症状、根因、修复与预防检查
  - 每个经用户确认的显著成功都应在 `CONTEXT.md` 中记录：结果、设计决策、提炼 heuristic 与可复制范围
  - 当前项目内一旦出现新的稳定偏好、禁区、长期要求、特殊元素或用户明确要求“以后都按这个来”的口径，应优先写入项目根 `MEMORY.md`
  - 若 `MEMORY.md` 中已有记录被用户替换、撤销或纠偏，必须同轮更新或删除旧条目，不得让项目记忆保留失效偏好
  - 每次用户主动针对 `projects/aigc/<项目名>/` 或 `projects/story/<项目名>/` 下相关项目发出清空、移除或等价删除指令时，必须顺带自动检查当前 `aigc` 或 `story` 项目状态记录、运行态控制面与治理镜像是否需要同步更新；若存在状态残留、路径残留或索引残留，应在同轮同步修正或明确报告无法自动处理的遗留项。
  - 跨项目可复用的失败模式、修复策略、调试结论与治理规则，仍应写回技能 `CONTEXT.md` 或上升到 `SKILL.md` / `AGENTS.md`，不得写进单项目 `MEMORY.md`
  - 同一技能的类型化/多模式处理若已上升为执行前必须遵守的专项细则，应沉到主合同显式声明的规范模块；`CONTEXT.md` 只保留执行后沉淀出的经验性 Type Map、Playbook 与 Heuristics
  - 详细变更时间线、迁移流水、执行长日志应优先写入 `CHANGELOG.md` 或 `reports/`，而不是把 `CONTEXT.md` 写成时间序备忘录
  - 保持 `SKILL.md` 简洁且规范；保持 `CONTEXT.md` 可积累且经验化
  - 当主技能、子技能与卫星技能的 `CONTEXT.md` 同时存在时，新经验应优先写入最窄且有效的作用域；仅当模式跨子技能、跨卫星或已经成为整技能级政策时，才向上晋升

### 复合型技能输出治理合同（强制）

- 当一个主 `SKILL` 负责调度多个子技能、子模块或受治理执行单元，并最终要把结果继续落盘到共享目标时，默认采用“子单元受理输出 + 主技能按规则聚合落盘”的复合型输出机制。
- 共享目标（例如统一根文件、统一主稿、共享结构化对象）必须是唯一业务真相，只承载累计后的最终事实，不承载每个子单元的完整过程稿。
- 主技能必须拥有以下职责：
  - 路由裁决：决定本轮命中哪些子单元。
  - 选择性调度：只调度命中的子单元，而不是默认全量运行。
  - 聚合校验：只聚合已调度子单元返回的有效 patch / delta / section update。
  - 最终落盘：把通过校验的聚合结果继续写回共享目标。
- 选择性调度是默认规则：
  - 未被调度的子单元不参与本轮聚合。
  - 未被调度的子单元不得因为“结构完整性”被补空字段、补占位块或补默认思维链。
  - 最终共享目标只反映已经实际发生的有效 patch，不反映“理论上还存在但本轮未执行的子单元”。
- 卫星技能的默认合同：
  - 卫星技能默认不并入主技能的主链串行聚合。
  - 只有当主技能显式声明某个卫星技能的输出是共享目标必需 side input 时，该卫星技能才参与聚合。
  - 查询、恢复、审查承接等卫星技能的默认落点应是辅助工件、状态回接或治理证据层，而不是直接篡改主链业务真源。
- 子单元的标准输出应优先是局部变更，而不是平行总稿：
  - 优先返回 `field patch`、`section patch`、`module delta`、`slot fill` 或等价的局部落盘结果。
  - 除非用户显式要求，否则不应让每个子单元先各自写一份完整主稿，再由主技能二次汇总。
- 若子单元需要保留完整创作过程、思维链、推导说明或工作草案，应落到本地 sidecar，而不是灌入共享目标：
  - sidecar 可采用三段式 `MD` 或其他约定格式。
  - sidecar 是工作侧车，不是业务真源。
  - 共享目标中若保留 `thinking_chain`、`reasoning_summary`、`decision_log` 等字段，默认只允许承载父级精简摘要、patch provenance、验收结论或最小可追踪信息，不得重复堆叠子单元完整思维链。
- 当父级已经定义统一输出模板、共享 schema、统一根文件合同或聚合规则时：
  - 子单元必须显式回指父级真源。
  - 子单元不得再额外定义第二份平行输出模板。
  - 子单元自己的局部模块、模板或 sidecar 规则，只应承载局部写位、执行流程、路由策略或本地约束，不得重写父级输出真源。
- 若共享目标当前无法直接承接局部 patch，必须显式报告：
  - 阻塞原因
  - 临时聚合适配层
  - 临时同步护栏
  - 为什么当前还不能完全收敛为单一真源

### CONTEXT 健康监控（强制）

- 每份 `CONTEXT.md` 都应包含自动维护的 `Context Health` 章节。
- 该要求同时适用于主技能根层 `CONTEXT.md` 与子技能 `CONTEXT.md`。
- 默认健康阈值如下：
  - `soft_limit_chars: 20000`，`hard_limit_chars: 40000`
- 动作策略：
  - `ok`：保持面向目标的知识更新，优先更新 Type Map / Playbook / Reusable Heuristics
  - `warn`：对该技能的上下文做定向压缩与整理
  - `warn` 且文档很长但知识密度失衡：优先做人为结构整理（章节合并/拆分/抽取），而不是继续追加
  - `critical`：在继续大规模追加前，必须先压缩并归档旧内容
- 压缩时必须保持证据完整性：
  - 将仍有高复用价值的结论保留在 `CONTEXT.md`
  - 将较长时间线、旧证据和过程性材料外置到 `reports/context-archive/`、`CHANGELOG.md` 或其他可追踪载体
- 默认操作应针对单个技能上下文，而不是在未被要求时全仓重写。

### CONTEXT 知识库模式（强制）

- `CONTEXT.md` 的默认模式是知识库，而不是按时间顺序记录的日志。
- 该规则同时适用于主技能根层 `CONTEXT.md` 与子技能 `CONTEXT.md`。
- 优先维护以下内容：
  - Type Map：失败类型 -> 根因层级 -> 立即修复 -> 系统预防 -> 验证方式
  - Repair Playbook：稳定的排障顺序与 fallback 策略
  - Reusable Heuristics：简洁且高价值的可复用经验
  - `Type Map` 在此特指经验性映射与排障知识，不等于同一技能的规范型类型策略工作台；后者应放在主合同显式指定的规范模块
- 详细时间线、长日志、迁移流水、版本差异说明应外置到 `CHANGELOG.md`、执行报告或 `reports/`；不要把这些内容直接堆进 `CONTEXT.md`
- 里程碑事件处理：
  - 不再单设 `Case Log`；负向或正向里程碑也应优先回写为 Type Map / Playbook / Reusable Heuristics 中的结论化条目
  - 若某次里程碑需要保留独立证据链，`CONTEXT.md` 仅保留摘要与回指，详细过程应外置到 `CHANGELOG.md` 或 `reports/`
- 禁止记录低价值内容：
  - 进度叙述、长段执行日志、迁移流水原文、仅做表面润色的修改、无法提供复用防护或复制价值的一次性噪声笔记

## 源层治理

### 执行深度默认规则（强制）

- 执行任务时，默认按“成熟版 engine”标准推进，不得因为习惯性谨慎而总是停在“最小补丁”或“最小闭环”。
- 判断应做到哪一层时，以“用户需求自然要求的完成层级”为准，而不是以“当前最小可改动量”为准。
- 对技能、工作流、规则、编排系统、模板体系、验证链路这类任务，默认目标应接近“成熟版 grouping engine”口径：
  - 不只修局部文案或单点症状。
  - 应优先补齐对应的真源载体、路由细则、模板、校验/脚本、上下游回指与防回归机制。
- 只有在以下情况成立时，才主动收敛到最小补丁：
  - 用户明确要求只做最小修复、临时补丁或探索性试改；
  - 外部依赖、权限、时间窗或兼容性风险阻止继续深挖；
  - 再往下推进会明显越过用户目标边界。
- 若因阻塞无法做到成熟版落点，必须明确报告：
  - 当前已完成到哪一层；
  - 为什么没有继续做到更完整层；
  - 下一步应补的真源或机制载体是什么。

### 根因优先（强制）

- 当用户反馈项目问题或任务执行故障时，必须先调查源层原因，再决定是否修补本地产物。
- 源层诊断应优先检查规则工件与执行入口，通常包括 `SKILL.md`、已声明的 Skill 2.0 分区（`references/`、`steps/`、`review/`、`types/`）、`CONTEXT.md`、命令 runbook、阶段模板与相关脚本；仅当主合同显式引用外部资料时，才按需联查 `knowledge-base/`。
- 对采用或正在升级为 Skill 2.0 的技能，源层修复/优化必须先做 owner 分区定位：判断问题应落在 `SKILL.md`、`CONTEXT.md`、`references/`、`steps/`、`review/`、`types/`、`templates/`、`scripts/`、`agents/openai.yaml`、`README.md` 或 `CHANGELOG.md` 中的哪一个真源载体；不得把所有修复继续堆回 `SKILL.md` 或 `CONTEXT.md`。只有当问题涉及用户或维护者手动导入的外部知识材料、索引或摘录入口时，才允许把 `knowledge-base/` 作为修复 owner。
- Skill 2.0 结构问题本身也属于源层问题：缺失 canonical 目录、存在拼写 alias、`agents/openai.yaml` 缺入口元数据、`CONTEXT.md` 缺知识库核心、分区没有说明文件、长细则未拆出、经验错写到 `knowledge-base/`、执行步骤错写到 `CONTEXT.md` 等，都应先按结构 owner 修复，再继续业务产物修复。
- 源层诊断不仅要看“写了什么规则”，还要看“规则要求如何思考与如何执行”：凡 `SKILL.md`、`references/` 或 `steps/` 中存在思维·执行节点、思维链细则、执行流程节点、判断分叉、tie-break、字段思考顺序、聚合/回写顺序等设计，均应视为可追因、可优化的源层合同。
- 源层追踪必须分层进行：不得停在第一个局部原因，必须继续上溯直到识别治理该行为的规则源。
- 非平凡问题的强制追因链为：
  - `Symptom/Failure` -> `Runtime Artifact` -> `Direct Technical Cause` -> `Owner Partition`（Skill 2.0 owner / runbook / template / script gate）-> `Rule Source`（skill / module / runbook / template / script gate）-> `Meta Rule Source`（meta-AGENT / meta-SKILL / global policy）-> `Fix Landing Points` -> `Reference Sync` -> `Audit/Smoke`
- `Rule Source` 通常包括：任务级 `SKILL.md`、Skill 2.0 分区、专项细则模块、`types/` 类型化模块、`steps/` 思维·执行节点设计、命令 runbook、阶段模板、验证脚本与执行入口。
- `Meta Rule Source` 通常包括：仓库 `AGENTS.md`、`.codex/skills/meta/*/SKILL.md` 以及其他跨技能治理合同。
- 如果诊断无法上溯到 meta 层工件，必须明确说明为什么没有更高层治理合同。
- 对每个问题，都应给出简洁修复建议，包括：根因位置、owner 分区、立即修复、系统预防修复、引用同步范围与验证门禁。
- 在使用 `SKILL` 执行、dry-run、工作流排练或 `pytest` 回归测试期间，迭代相关源层工件（`SKILL.md`、Skill 2.0 分区、`CONTEXT.md`、runbook、脚本、模板、验证器）应被视为合法且优先的并行目标，而不是事后补文档。
- 如果执行被阻塞，必须立即暂停下游动作，先完成分层追因与源层修复/增强，再恢复任务。
- 优先修复产生该错误模式的规则或脚本，使同类问题在后续运行中不再重复。
- 每一个非平凡修复都应视为一次源层增强机会：不仅要修症状，也要补强源层合同，降低类似问题再次发生的概率。
- 如果在工作中发现更优的执行路径或工作流，且源层重构风险可控，则允许在继续下游工作前优先完成源层优化。
- 如果优化的安全性、范围或预期收益不够明确，应先按 `PRPs/README.md` 记录为 `PRP`，再沿当前最安全路径继续工作，等待人工确认。
- 推荐的增强方向可从以下一项或多项中选择：显式 gate / 诊断（明确错误状态、非零退出码、可执行提示）、对不稳定依赖的 fallback / retry、将重复逻辑收敛到单一真源（配置 / 入口 / 共享 helper）、补齐 Skill 2.0 结构与分区说明、在 `types/` 中补强类型化模块与决策表、在 `steps/` 中重写失效的思维·执行节点、在 `review/` 中补交付门禁、在 `templates/` 中修正输出样板、在 `scripts/` 中加机械校验，或在 `SKILL.md` / `references/` 中修正入口拓扑与合同说明。
- 只有满足以下条件，才算“增强闭环完成”：问题已修复 + 已定位并修复最高杠杆 owner 分区 + 至少一个可复用的源层预防机制已落地 + 相关文档/合同已同步更新 + 引用同步范围已扫描或说明 + 已运行相应审计 / dry-run / smoke 验证，或明确报告验证阻塞。
- 如果增强被权限、外部依赖或范围限制阻塞，必须显式报告阻塞项与临时防护措施。

### 多子智能体技能的源层联动（强制）

- 当目标技能由 `skill-subagents` 创建、升格或长期治理时，源层诊断不得只停在父 `SKILL.md`。
- 对这类多子智能体 skill，分层上溯除父 `SKILL.md` / `CONTEXT.md` 外，还必须按需联查：
  - 父 skill 显式回链的 `team.md`
  - 相关 agent rule docs（例如 `.codex/agents/<skill-slug>/**/*.md`）
  - 受治理子路径或子技能的局部 `SKILL.md` / `CONTEXT.md`
  - 与该 roster 绑定的 handoff schema、shared template、runbook、validator、route 配置
- 源层同步/修复遵循“只联动受影响关联面”原则：
  - 父 skill 总合同变更时，同步检查其引用的 `team.md`、agent docs、子路径合同是否仍一致
  - 某 subagent / team 合同变更时，同步检查父 skill 的 topology / handoff / synthesis / audit 描述是否仍准确
  - 不得因为某个子角色局部变更而无差别重写整个 roster；也不得只修局部 agent doc 而放任父层合同失真
- 真源边界默认如下：
  - 父 `SKILL.md` 持有 topology、dispatch、handoff、synthesis、audit 与 canonical writeback 的总合同
  - `team.md` 持有 team 级 roster、默认调用关系与 team 内共享 handoff 约定
  - 单个 agent rule doc 持有该角色的局部任务边界、I/O、veto、证据与越权约束
  - 子路径本地 `SKILL.md` / `CONTEXT.md` 持有局部执行合同与局部经验层
- 若关联 subagent 的合同未同步修复，则不得宣称源层闭环完成；如暂无法同步，必须报告缺口、影响面与临时护栏。

### 根因学习回路自动化（强制）

该学习回路有两个方向，负向与正向都必须执行。

**负向触发**：当出现以下任一情况时自动触发：用户报告问题、运行失败、任务实践/测试阻塞（包括 `SKILL` 执行、dry-run 与 `pytest` 回归）、失败后返工、或用户明确要求修正。

- 无需额外等待用户提示，必须自动执行以下流程：
  1. 源层诊断（分层上溯）：从症状追到运行产物、直接原因、`Owner Partition` 与 `Rule Source`，必要时继续追到 `Meta Rule Source`（`AGENTS.md` / meta-SKILL）；诊断时必须按需联查 `references/`、`steps/`、`review/`、`types/` 与 `SKILL.md` 中的动态引用和主流程，并检查目标 skill 是否存在 Skill 2.0 结构错位。
  2. 立即修复 + 增强：优先修补最高杠杆的源层 owner 分区（规则 / 脚本 / runbook / Skill 2.0 分区 / meta-rule），增加至少一项可复用的加固机制，然后再恢复下游执行；如仍有必要，再补本地产物。
  3. 上下文沉淀：更新受影响技能的 `CONTEXT.md`（若缺失则创建）；优先把结论化经验写入 Type Map / Playbook / Reusable Heuristics，若需保留里程碑细节，则外置到 `CHANGELOG.md` 或 `reports/`。
  4. 引用同步与验证：若发生重命名、拆分、迁移或 owner 分区调整，必须扫描并同步 `SKILL.md`、`CONTEXT.md`、`README.md`、`CHANGELOG.md`、`agents/openai.yaml`、`scripts/`、`templates/`、registry、routes、runbook、markdown 链接和项目内引用；随后运行对应结构审计、脚本 dry-run 或 smoke 验证。
  5. 预防晋升（自下而上）：将已验证的修复从本地产物 -> `CONTEXT.md` -> `SKILL.md` / Skill 2.0 分区 / runbook -> `AGENTS.md` 或 meta-SKILL 逐级晋升；若已观察到跨技能复发，则必须继续向上晋升。
  6. 面向用户的闭环输出：必须返回 `root cause location + owner partition + immediate fix + systemic prevention fix + validation`，并附上分层追踪路径 `symptom -> owner partition -> rule source -> meta rule source`。

**正向触发**：当出现以下任一情况时自动触发：用户明确认可某输出（例如“这个很好”“以后按这个来”）、某设计决策在跨项目场景中被复用且无需重新推导、或输出质量明显超过预期基线。

- 无需额外等待用户提示，必须自动执行以下流程：
  1. 模式识别：定位产出正向结果的设计决策，例如 prompt 结构、参数选择、工作流顺序、字段映射或架构安排。
  2. 抽象：将该决策提炼为 1-3 句可复用 heuristic，且要限定适用范围（skill、阶段、领域、主题），避免过度泛化。
  3. 上下文沉淀：将 heuristic 写入对应技能的 `CONTEXT.md` 中的 Reusable Heuristics；若需要保留里程碑级证据，只保留结论摘要在知识库章节中，长材料外置到 `CHANGELOG.md` 或 `reports/`。
  4. 晋升（自下而上）：当同一正向模式在 >= 2 次独立执行中得到确认时，将其从 `CONTEXT.md` 晋升到 `SKILL.md` 或对应 Skill 2.0 owner 分区；若已成为跨技能治理模式，再晋升到 `AGENTS.md` 或 meta-SKILL。
  5. 面向用户的闭环输出：返回三元组：成功模式位置 + 提炼出的 heuristic + 晋升范围。
- 若需要保留里程碑级证据，`CONTEXT.md` 仅保留结论化沉淀；详细字段、时间线与长证据材料应写入 `CHANGELOG.md`、执行报告或 `reports/`。
- 如果只是修复了本地产物或确认了结果，却没有同步更新 `CONTEXT.md`，则视为 `Root-Cause Learning Loop` 尚未完成；若因阻塞无法更新，必须显式报告阻塞原因。

### AGENT、SKILL、专项模块、CONTEXT 与入口元数据放置矩阵（全局真源）

- 以下内容应写入 `AGENTS.md` / meta-SKILL（规范型元合同）：

  - 跨技能的根因上溯顺序（`Rule Source -> Meta Rule Source`）
  - 从本地修复晋升到全局规则的条件
  - 仓库级硬门槛、闭环格式与防回归要求
  - 仓库级多因素决策方法，包括层级角色、覆盖规则与回退原则
  - 字段中心 thought-pass 系统的规范标识符与必填表头
- 以下内容应写入共享 `templates/` / schema / spec / shared helper（规范型复用载体）：

  - 跨模式、跨模块共用的章节骨架、输出结构、schema 真源、复用清单与路由模板，不应在兄弟工件中各自重复定义
  - 这类载体负责稳定复用结构；各兄弟模块应继承或局部特化，而不是静默拷贝一份再演化
  - 当共享 template / spec 成为真源后，下游 `SKILL.md` / `module-spec.md` / runbook 必须显式回指该真源
- 以下内容应写入具体 agent 规则文档（例如 `.codex/agents/**/*.md`）作为源层规范合同：

  - agent 的人格边界、任务范围、输出 schema、路径约定、字段落点、审查合同与面向用户的硬门槛
  - 对多子智能体 skill，`team.md` 承载 team 级 roster / topology / handoff 共识，具体 agent doc 承载角色级合同；二者不得与父 `SKILL.md` 形成平行第二真相
  - 如果某 agent 没有独立 `CONTEXT.md`，则稳定的规范增强可以直接写进 agent 规则文档本身
  - 这种 agent 级直接优化仅限于规范内容：规则、schema、优先级、失败闭环、路由与输出合同
  - 经验性内容不得直接倾倒进 agent 规则文档，例如单次案例、噪声实验、临时 heuristic 与里程碑证据，应保留在 `reports/`、技能 `CONTEXT.md` 或其他经验层载体中，待验证后再晋升
  - 晋升规则：重复、多轮、高置信度的 agent heuristic，可在足够稳定后从经验层载体晋升回 agent 规则文档
- 以下内容应写入 `SKILL.md`（规范合同）：

  - frontmatter、触发条件、适用/不适用场景、Mode Selection、Reference Loading Guide、强制工作流、硬门槛与完成标准
  - 源层诊断顺序与修复顺序（包括上溯到 meta 合同的钩子）
  - 面向用户的标准闭环格式（根因位置 + 立即修复 + 系统预防修复）
  - 从经验到规范的晋升规则（何时可将重复模式提升为规范）
  - 当技能存在复杂选择逻辑时，定义领域专属的一层/二层/三层决策信号、tie-break 规则与显式覆盖条件
  - skill 自己的 `field_id` 主定义，以及 `step_id -> field_id` 和 `field_id -> quality_dimension -> fail_code -> rework_entry` 映射
- 以下内容应写入卫星技能 `SKILL.md`（同根旁路执行合同）：

  - 卫星职责、触发条件、与主链/主技能的 `stage_position`
  - `owned truth`、`not-owned truth`、共享载体依赖与回接路径
  - 是否参与 tracked workflow、是否允许直接调用、以及完成后回到哪个主技能或阶段
  - 不得把卫星技能写成主技能缩略版，也不得把它伪装成普通细则模块
- 以下内容应写入 `agents/openai.yaml`（入口元数据层）：

  - `interface.display_name`、`interface.short_description`、`interface.default_prompt` 等 UI-facing 入口元数据
  - `interface.default_prompt` 必须显式提到 `$skill-name` 或目标 skill 的标准唤起名
  - 与主 `SKILL.md` 同步的发现入口摘要
  - 不得承载独立于主合同之外的隐藏执行规则
- 以下内容应写入 Skill 2.0 分区或共享模块文件 / spec / schema（专项细则层）：

  - `references/`：可独立升级、但仍受主合同约束的复杂规范、长细则、背景资料与专项合同
  - `steps/`：思维·执行节点设计、执行流程细则、判断分叉、串并行、汇流、回退和证据门
  - `review/`：质量评估、审计流程、评分模型、review provider 接入与交付 verdict
  - `types/`：类型变量、类型映射矩阵、分型处理策略与 `type_profile` 生成规则
  - `knowledge-base/`：人工添加的外部知识库、参考资料包、资料索引与领域背景材料；不得作为执行经验、稳定 heuristic 或复盘结论的沉淀落点
  - `templates/`：输出模板、脚手架模板和报告模板；不得承载运行状态
  - `scripts/`：机械创建、校验、格式转换、路径归一与批量处理；不得替代 LLM 主创判断
  - 同一技能的多类型化 / 多模式化若属于执行前必须遵守的工作台，应优先落到主合同显式指定的规范模块，而不是放进 `CONTEXT.md`
  - 若某项问题根因来自错误的思考顺序、判断节点、聚合节点、回写节点、review gate 或类型路由，应优先在对应 `references/`、`steps/`、`review/`、`types/`、spec、schema 或 module 中修复，而不是只在局部产物层面兜底
  - 一旦某模块已成为 canonical module，主 `SKILL.md` 与其他文档应回链该模块，而不是平行复制同一套长说明
- 以下内容应写入 `CONTEXT.md`（经验层）：

  - Type Map（失败模式 -> 修复策略 -> 验证点）、Repair Playbook 与 Reusable Heuristics
  - 运行陷阱、兼容性问题、成功恢复策略
  - 多因素选择任务中的经验性 tie-break heuristic、收窄 heuristic 与观察到的失败模式
  - 对类型化处理的经验性复盘、失败模式、修复策略与验证点；但不承载同一技能的规范型多模式策略主表
  - 尚未稳定到足以晋升为 `SKILL.md` 的候选经验
  - 若某次里程碑事件需要保留额外证据，`CONTEXT.md` 仅保留结论化摘要，长材料外置到 `CHANGELOG.md` 或 `reports/`
- 以下内容应写入项目级 `MEMORY.md`（项目记忆层）：

  - 用户明确要求长期保留的创作偏好、风格口味、叙事习惯、角色关系偏好、视觉/声音/氛围倾向
  - 当前项目必须保留的特殊元素、固定母题、反复强调的钩子、明确禁区与长期执行要求
  - 会影响后续多个阶段判断的项目级协作约定，例如“这个项目不要鸡汤式收束”“感情线始终克制表达”“视觉上固定保留雨夜霓虹”之类的长期口径
  - 对既有项目记忆的更新、替换与撤销结论
  - 不得写入技能调试经验、源层故障复盘、跨项目 heuristic、一次性任务说明或迁移时间线
- 以下内容应写入 `CHANGELOG.md`（派生变更史）：

  - 按时间顺序组织的变更摘要、迁移记录、结构重排说明、长段执行时间线与版本差异
  - `CHANGELOG.md` 是派生说明载体，不是规范真源，也不是经验真源；不得与 `AGENTS.md` / `SKILL.md` / `CONTEXT.md` 并列竞争事实裁决权
  - `CHANGELOG.md` 默认不参与技能运行时预加载；只有在追溯迁移、审计差异、发布说明或需要查看详细过程时才按需读取
  - 若某条经验需要保留较长过程材料，`CONTEXT.md` 只保留结论化沉淀，并链接指向 `CHANGELOG.md` 或 `reports/`
- `CONTEXT.md` 支持多级放置。
- 当前规范特指主技能、子技能与卫星技能之间的多级放置：

  - 主技能根层 `CONTEXT.md`：整个技能族的默认经验层，承接跨子技能、跨模式、跨工作流的经验
  - 项目级 `MEMORY.md`：项目运行时的创作记忆真源，面向当前项目整个创作阶段；当前仅允许以下 canonical 形态：

    ```text
    projects/story/<项目名>/MEMORY.md
    projects/aigc/<项目名>/MEMORY.md
    ```

    项目级 `MEMORY.md` 中存放的是该项目已经确认、后续阶段应持续遵守的偏好、口味、特殊元素与长期要求；它不替代技能 `CONTEXT.md`，也不替代项目级 `CONTEXT/`
  - 项目级 `CONTEXT/`：项目运行时共享附加上下文根，面向当前项目整个创作阶段；当前仅允许以下 canonical 形态：

    ```text
    projects/story/<项目名>/CONTEXT/
    projects/aigc/<项目名>/CONTEXT/
    ```

    项目级 `CONTEXT/` 中存放的是任务执行时必须额外加载的项目共享上下文文件；它作用于整个项目创作阶段，但不替代主技能、子技能或卫星技能自身的 `CONTEXT.md`
  - 子技能 `CONTEXT.md`：用于受治理子技能的局部经验层，路径由父级合同显式声明，通常采用如下形态：

    ```text
    <skill-root>/
      ...
      <child-skill-path>/
        SKILL.md
        CONTEXT.md
    ```

    子技能 `CONTEXT.md` 仅保存该子技能自己的局部 heuristic、陷阱、案例与修复模式，不得替代主技能根层 `CONTEXT.md`
- 卫星技能 `CONTEXT.md`：用于同根旁路 skill 的局部经验层，通常采用如下形态：

  ```text
  <skill-root>/
    SKILL.md
    CONTEXT.md
    <satellite-name>/
      SKILL.md
      CONTEXT.md
  ```

  卫星技能 `CONTEXT.md` 仅保存该卫星技能自己的局部 heuristic、旁路恢复/查询/承接策略与陷阱，不得替代主技能根层 `CONTEXT.md`
- 子技能与卫星技能 `CONTEXT.md` 的升级规则：

  - 一旦某个技能采用受治理子技能结构，则范围内长期维护的子技能应在父级合同声明的子技能路径上显式暴露 `SKILL.md + CONTEXT.md`
  - 一旦某个技能出现长期维护、可直接调用、且拥有独立旁路职责的 sibling skill，则应显式表现为 `<skill-root>/<satellite-name>/SKILL.md + CONTEXT.md`
  - 跨子技能、跨卫星或跨技能的 heuristic，仍必须回晋升到主技能根层 `CONTEXT.md` 或 `SKILL.md`
- 冲突优先级如下：用户显式请求 > `AGENTS.md` / meta-SKILL > 主 `SKILL.md` > 当前命中的子技能或卫星技能 `SKILL.md` > 已声明的 `references/` / `steps/` / `review/` / `types/` / 模板 / spec > `agents/openai.yaml` > 项目级 `MEMORY.md` > 项目级 `CONTEXT/` > 主 `CONTEXT.md` > 当前命中的子技能或卫星技能 `CONTEXT.md` > 按需读取的 `CHANGELOG.md`

### Agent 源层优化合同（强制）

- Agent 规则文档是第一类源层工件，而不只是人格包装。
- 对多子智能体 skill，agent 源层优化至少联查三处回指：父 skill 的 topology / handoff / synthesis 说明、`team.md` 的 team 级调用规则、agent doc 的局部边界与输出合同。
- 若 agent 或父 skill 还显式依赖 `references/`、`steps/`、`review/`、`types/`、decision table 或 handoff node spec，源层优化必须把这些载体纳入联查与修复范围，不得只停留在 agent 主文档正文。
- 如果某个问题受 agent 自身合同约束，且该 agent 没有专用 `CONTEXT.md`，则应直接在 agent 规则文档中修复稳定规则，而不是等待外部经验层。
- 若某次修复触及父 skill、`team.md` 或单个 agent doc 中任一层，必须同步核对其余受影响层；未联查或未同步说明，视为源层闭环不完整。
- 直接修改 agent 规则文档时，应优先覆盖以下内容：
  - 范围澄清
  - 输出 schema 修复
  - 路径/落点约定
  - 优先级与路由修复
  - 失败闭环与防回归表述
- 直接修改 agent 规则文档时，应避免写入以下内容：
  - 进度日志
  - 单轮轶事
  - 噪声案例叙述
  - 大段未经整理的 heuristic 堆积
- 当相关内容仍处于探索期、存在争议、出现频率低、或证据负担较重时，应先留在经验层载体，待验证后再晋升。
- 简言之：agent 文档可以吸收**稳定政策**，但不应伪装成原始经验日记。

### 真源治理合同（强制）

- 只要某条规则、结构、schema、模板、路由合同或清单被多个同级模块、模式、工作流或文档共享，源层优化就必须包含**真源治理**。
- 真源治理意味着：先确定哪个工件是单一权威真源，再强制其他载体退化为派生投影、适配层或局部补充，而不是并列的第二真相。
- 触发条件：如果同一规范结构需要在 2 个以上同级位置同时编辑，或经常出现漂移/忘记同步，应将“缺少单一真源”视为根因，而非仅仅认为是重复劳动。
- 可作为真源的载体包括但不限于：
  - 根 `SKILL.md` / 根 `AGENTS.md`
  - 共享 `templates/`
  - 共享 schema / spec 文件
  - 共享 runbook / validator
  - 共享 helper / config entrypoint
- 真源设计必须回答以下问题：
  - 哪个工件是权威真源
  - 哪些工件只是派生投影
  - 允许哪些本地变体
  - 下游工件应如何引用/继承，而不是静默重述
- 下游工件不得演化为隐藏的第二真相：
  - 如果共享模板已存在，兄弟模块只允许添加模式特有增量
  - 生成或适配后的文件不得悄悄重定义上游合同
  - 过时的旧真源必须被移除、降级为迁移 stub，或显式标记为非规范
- 只有满足以下条件，真源治理才算完成：
  - 已识别或创建权威真源
  - 共享规则在需要时已被迁移到该真源
  - 依赖工件已改为引用/继承该真源
  - 陈旧重复真相已被删除或显式降级
  - 同步/验证路径已更新，使未来漂移可以被检测到
- 如果由于兼容性、范围或时机限制，无法一次性完成真源合并，必须显式报告：
  - 阻塞项
  - 临时同步护栏
  - 仍保持非规范状态的部分及其原因
- 简言之：不要停在“把所有副本都改了”；只要问题横跨多个同级模块且经常漂移，就应优先恢复或创建那个单一真源。

## Harness 工程

### 三省六部制编排治理基线（强制）

- 本仓库按编排系统治理，层次如下：
  - 宪章层：根 `AGENTS.md`
  - 三省治理层：中书省起草、门下省复核、尚书省执行
  - 六部能力层：吏部注册、户部上下文、礼部合同、兵部调度、刑部审计、工部基础设施
- 当前引导期已不是“只有目录骨架”的口径，最小已落地真源载体如下：
  - 共享治理合同：`.codex/templates/harness/office-governance-contract.md`
  - 三省角色合同：`.codex/agents/harness治理/中书省.md`、`.codex/agents/harness治理/门下省.md`、`.codex/agents/harness治理/尚书省.md`
  - 注册与路由真源：`.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`
  - 生命周期真源：`.codex/runbooks/task-lifecycle.md`
  - 任务工件真源：`.codex/templates/harness/{mandate, mission-brief, route-plan, preflight-verdict, validation-report, learning-record}`
  - 运行时控制面：`projects/aigc/<项目名>/` 为 `aigc` 项目工作流唯一真源，`.codex/state/tasks/<task_id>/` 为通用任务状态面或治理镜像
  - 审计与评测入口：`scripts/aigc_harness_audit.py`、`.codex/evals/`
- 六部当前最小落点应与真源载体显式对应：
  - 吏部：`.codex/registry/skills.yaml` / `.codex/registry/routes.yaml`
  - 户部：`projects/aigc/<项目名>/` 与 `.codex/state/tasks/<task_id>/`
  - 礼部：`.codex/templates/harness/` 与 `office-governance-contract.md`
  - 兵部：`.codex/runbooks/task-lifecycle.md`
  - 刑部：`scripts/aigc_harness_audit.py`、`preflight-verdict.yaml`、`validation-report.md`
  - 工部：`scripts/`、`.codex/evals/`、`.codex/schemas/`
- 标准引导期合同：
  - 中书省负责将复杂任务先写成 `mandate + mission-brief + route-plan`
  - 门下省负责 `preflight-verdict + validation-report + upward trace`
  - 尚书省负责将执行状态与产物落到已声明的 canonical runtime；对 `aigc` 项目型工作流，canonical runtime 为 `projects/aigc/<项目名>/`
  - 三省共享总则、移交、闭环与防漂移要求统一以 `.codex/templates/harness/office-governance-contract.md` 为准，office-specific agent 文档只写各自差异
- 默认任务生命周期：
  1. `受命`
  2. `起草`
  3. `预审`
  4. `执行`
  5. `验收`
  6. `沉淀`
- 硬门槛：
  - 复杂任务不得跳过 `mission-brief` 与 `route-plan`
  - 高风险任务不得跳过 `preflight-verdict`
  - 任何任务不得在没有 `validation-report` 的情况下宣布完成
  - 任何非平凡失败不得在没有 `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source` 的情况下结案
- 防漂移规则：
  - 三省共享总则、移交流程、分层上溯链与闭环格式，必须优先回收到 `office-governance-contract.md`，不得在兄弟 agent 文档中平行复制演化
  - 新增仓库内本地技能时，必须先注册到 `.codex/registry/skills.yaml`
  - 新增工作流路由或旧仓继承映射时，必须先登记到 `.codex/registry/routes.yaml`
  - 新增或调整三省任务工件字段时，必须同步更新 `.codex/templates/harness/` 对应模板与 `scripts/aigc_harness_audit.py`
  - 共享结构必须沉到模板、schema、runbook 或 registry 等真源载体中，不得在多个同级工件中静默重复定义
  - 运行状态必须优先落到已声明的 canonical control plane 中；对 `aigc` 项目工作流，以 `projects/aigc/<项目名>/` 为准，`.codex/state/tasks/` 仅作为跨项目治理镜像或非项目任务账本
- `AIGC-ZEN-VOID` 继承规则：
  - `/Volumes/AIGC/AIGC-ZEN-VOID` 仅作为设计源，而不是自动规范真源
  - 来自发源仓库的复用必须遵循 `mapping -> review -> landing`，不得以批量复制 `output/`、运行时状态或未治理的技能树作为起点
- 引导期审计：
  - `python3 scripts/aigc_harness_audit.py --strict` 是当前最小编排治理审计入口
  - 未来的总控技能、阶段技能与推广落地工作应扩展这套审计，而不是绕开它

### HARNESS.md 总览与同步（强制）

- 根目录 `HARNESS.md` 是本仓库 HARNESS 工程的总览型派生文档，用于汇总：
  - 当前工程化构思
  - 已落地真源
  - 当前运行方式
  - 现状成熟度判断
  - 可期发展方向
- `HARNESS.md` 不是新的第一真源，不得与以下规范真源并行竞争：
  - 根 `AGENTS.md`
  - `.codex/templates/harness/office-governance-contract.md`
  - `.codex/agents/harness治理/`
  - `.codex/registry/skills.yaml`
  - `.codex/registry/routes.yaml`
  - `.codex/runbooks/task-lifecycle.md`
  - `.codex/templates/harness/`
  - `scripts/aigc_harness_audit.py`
- 当以下任一 HARNESS 相关真源发生变动时，必须在同一轮任务内同步检查并更新根目录 `HARNESS.md`，不得延后到“以后再补”：
  - HARNESS 宪章、治理层级、硬门槛、闭环格式发生调整
  - 三省 office 合同发生调整
  - registry / route / runtime canonical 关系发生调整
  - task lifecycle、模板字段、审计口径发生调整
  - active / planned / shelved 阶段状态与 suite 规划发生调整
  - legacy mapping、自动化策略、治理镜像策略发生调整
- 更新 `HARNESS.md` 时，至少要同步核对：
  - 当前工程化构思
  - 当前已实现真源
  - 当前运行方式
  - 现状判断
  - 可期发展方向
- 如果某次 HARNESS 变更因权限、范围或时机原因无法同步更新 `HARNESS.md`，必须在任务结尾显式报告缺口、原因与临时同步护栏。

### AIGC 改造兼容模式（强制）

- 当 `.agents/skills/aigc/` 进入重大结构改造窗口时，不得把 HARNESS 真源整体清空回“空白初始化态”。
- 此时应进入显式 `bootstrap_compat` 模式：保留 registry、runbook、template、audit、canonical runtime 与 review gate 这些骨架真源，只收缩其对 `aigc` 阶段内部细节的绑定强度。
- `bootstrap_compat` 模式下必须继续保留：
  - `projects/aigc/<项目名>/` 作为 canonical runtime
  - `.codex/registry/skills.yaml` / `.codex/registry/routes.yaml` 的根注册与路由入口
  - `.codex/runbooks/task-lifecycle.md` 的任务生命周期硬门槛
  - `.codex/templates/harness/` 的治理工件槽位
  - `scripts/aigc_harness_audit.py` 与 `scripts/aigc_skill_audit.py` 的审计入口
  - `query / resume / review` 等根级卫星技能入口与高风险 `preflight` gate
- `bootstrap_compat` 模式下允许放松的对象是：阶段内部结构、子路径细节、局部执行合同与深层 runtime 细节审计；这些内容可为 `aigc` 重构让路，不应继续被旧合同硬绑。
- 若需要放松约束，优先在 registry、routes、runbook、audit 中增加显式模式开关或降级逻辑，而不是删除现有真源载体。
- 等 `aigc` 新结构稳定后，再将稳定规则从 `aigc` 回填到 harness 真源、审计脚本与 `HARNESS.md`，结束 `bootstrap_compat` 模式。
