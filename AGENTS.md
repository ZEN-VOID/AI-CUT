# AGENTS.md

行业通用的 AI 智能体指令文件。兼容 Claude Code、Cursor、Windsurf 及其他 AI 编码工具。

## 项目基线

### 项目概览

AIGC（AI Generated Content）故事创作与管理工作区。该仓库不是传统意义上承载多个独立软件子项目的代码仓，而是用于组织 AIGC 创作流的项目工作台：

- 以 `projects/<项目名>/` 作为单个创作项目的主要工作空间
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
- 分镜 ID 使用四段式模式：`episode-scene-group-frame`，例如 `1-1-10-1`。
- 创作项目通常以 `projects/<项目名>/` 作为主工作目录，并在其中组织文本、图片、视频及阶段产物。
- 模板要求时，提示中的任务 ID 应保持 ASCII 安全字符。

### 重命名引用同步（强制）

- 当重命名文件或文件夹时，必须自动扫描整个仓库中对旧路径的引用，并同步更新到新路径。扫描范围包括脚本、配置、`SKILL.md`、`CONTEXT.md`、命令文档、模板以及其他 markdown / 代码文件。
- 扫描目标包括但不限于：`import` / `require` 语句、路径字符串、符号链接、JSON / YAML 配置项、markdown 链接以及 shell 命令参数。
- 如果某些引用无法自动更新，例如存在于二进制文件或外部系统中，必须显式向用户报告该遗留引用。

### 架构决策

- `projects/` 表示 AIGC 创作项目空间，而不是传统软件工程中的独立子项目集合。
- 每个创作项目通常落在 `projects/<项目名>/`，并在其内部继续组织文本、图片、视频、阶段产物与过程状态。
- 共享工具与配置统一放在 `scripts/` 和 `configs/` 中。
- `reports/` 用于保存开发或任务过程中的报告，允许按主题、日期或自动化流程归类。
- `PRPs/` 用于保存大型开发计划与阶段性实施方案。
- `docs/` 用于保存重要知识、制度说明与典藏文档。
- `templates/` 中的模板用于脚手架与标准化生成。
- 本仓库的治理基线采用 `三省六部制 + 编排工程` 架构，而不是临时拼接的提示词集合。
- 当前编排治理的引导期真源已收束为：根 `AGENTS.md` + `.codex/templates/harness/office-governance-contract.md` 共享合同，配合 `.codex/agents/harness治理/`、`.codex/registry/`、`.codex/runbooks/`、`projects/<项目名>/` / `.codex/state/tasks/`、`.codex/evals/`、`.codex/templates/harness/` 与 `scripts/aigc_harness_audit.py`。
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
- 涉及 COS 上传时，优先使用 `assets-refresh` 技能，以保持本地文件、索引与 COS 存储同步。
- 如果遇到类似 `/Volumes/...: No such file or directory` 的工作区路径错误，请运行 `python3 scripts/workspace_doctor.py` 检查或挂载工作区后再重试。

## Harness 工程

### 智能体专用指令

- 默认交互语言为中文；仅当任务确实需要英文输出时才切换。

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
  - 运行时控制面：`projects/<项目名>/` 为 `aigc` 项目工作流唯一真源，`.codex/state/tasks/<task_id>/` 为通用任务状态面或治理镜像
  - 审计与评测入口：`scripts/aigc_harness_audit.py`、`.codex/evals/`
- 六部当前最小落点应与真源载体显式对应：
  - 吏部：`.codex/registry/skills.yaml` / `.codex/registry/routes.yaml`
  - 户部：`projects/<项目名>/` 与 `.codex/state/tasks/<task_id>/`
  - 礼部：`.codex/templates/harness/` 与 `office-governance-contract.md`
  - 兵部：`.codex/runbooks/task-lifecycle.md`
  - 刑部：`scripts/aigc_harness_audit.py`、`preflight-verdict.yaml`、`validation-report.md`
  - 工部：`scripts/`、`.codex/evals/`、`.codex/schemas/`
- 标准引导期合同：
  - 中书省负责将复杂任务先写成 `mandate + mission-brief + route-plan`
  - 门下省负责 `preflight-verdict + validation-report + upward trace`
  - 尚书省负责将执行状态与产物落到已声明的 canonical runtime；对 `aigc` 项目型工作流，canonical runtime 为 `projects/<项目名>/`
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
  - 运行状态必须优先落到已声明的 canonical control plane 中；对 `aigc` 项目工作流，以 `projects/<项目名>/` 为准，`.codex/state/tasks/` 仅作为跨项目治理镜像或非项目任务账本
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

### 批量 SKILL 调度默认规则（强制）

- 当批量或成组调度多个技能执行任务时，默认执行模式应由技能名称决定。
- 如果技能名称中包含数字序列标记，则将该数字视为执行顺序信号，默认按数字升序串行执行。
- 如果技能名称中不包含数字序列标记，则默认以多线程并行执行。
- 更高优先级约束可覆盖上述默认规则，包括：用户显式指令、上游/下游硬依赖，以及相关 `SKILL.md` 中定义的安全限制。

### 仓库 Rollout 标准（强制）

- 每个长期维护的 skill 都应包含：
  - 在 `SKILL.md` frontmatter 中声明 `governance_tier: full | lite`
  - 在 `SKILL.md` 中包含与本全局政策对齐的 Root-Cause 执行合同，并附带上溯到 meta 层合同的钩子
  - 在 `SKILL.md` 中根据 tier 提供字段中心映射（Tier-Full 使用三张表；Tier-Lite 使用合并表）
  - 在 `CONTEXT.md` 中包含知识库核心（Type Map 与/或 Playbook 与/或 Reusable Heuristics）
  - 在 `CONTEXT.md` 中包含符合 `meta/skill-context` 结构的 Case Log（仅里程碑级）
- 由元技能生成的新技能，必须至少初始化 `SKILL.md` 与 `CONTEXT.md`，并满足上述基线；若对应元技能已将 `references/` 或 `agents/openai.yaml` 定义为默认层，则也必须同步初始化，不得回退为“只有主合同 + 经验层”。
- `scripts/aigc_skill_audit.py --strict` 用于校验：tier 声明是否存在、对应 tier 所需表格是否齐全、`CONTEXT.md` 的基线章节是否存在。缺项应被视为审计失败。
  - 对 `aigc` 技能树，还应校验阶段注册状态、搁浅阶段声明以及 `projects/<项目名>/` 项目根运行时合同是否已同步进入 registry / routes / audit。

### 技能组成与语义

- 技能目录基线：
  - `SKILL.md`：必需，作为规范执行合同
  - `CONTEXT.md`：推荐，作为预加载运行上下文
  - `references/`：按技能合同决定；可作为普通参考资料层，也可被上游元技能或主 `SKILL.md` 声明为默认生成、默认加载、默认维护的核心细则模块层
  - 可选：`scripts/`、`templates/`、`subtypes/`、`assets/`
- `references/` 的角色：
  - 默认语义由技能合同决定；若未被声明为模块层，可作为普通参考文件、示例、支持材料
  - 一旦被主 `SKILL.md` 或上游元技能声明为 canonical module layer，即承担被拆出的专项细则，而不是“可有可无的参考区”
  - 可承载思维链细则、执行流程细则、类型化处理 / 模式化策略、输出模板等可独立升级的专项模块
  - `references/` 与主 `SKILL.md` 的关系是“主合同 + 模块细则”，不是双真源竞争；不得替代主合同，也不得退化为无结构随笔堆放区
- `subtypes/` 的角色：
  - 受治理的可执行子技能
  - 推荐形态为 `subtypes/<subskill-name>/SKILL.md + CONTEXT.md`
- `SKILL.md` 的角色（硬规则）：
  - 定义范围、触发条件、必需输入、严格工作流、工具/脚本入口、输出合同与质量门槛
  - 必须明确、可执行、偏确定性；避免长篇叙述，也不要存放易过期的零散技巧
- `agents/openai.yaml` 的角色（入口元数据层）：
  - 承载 `display_name`、`short_description`、`default_prompt` 等 UI-facing 元数据
  - 负责 Codex 发现与进入技能时的入口摘要，但不得偷渡比主 `SKILL.md` 更强的执行规则
- `CONTEXT.md` 的角色（经验层）：
  - 保存可复用的 heuristic：成功/失败案例、陷阱、调试线索、兼容性注记、提示技巧与战术捷径
  - 作为规划/执行时的预加载上下文，但不得重定义核心合同
  - `CONTEXT.md` 中的 Type Map 属于经验性映射与修复知识；同一技能的规范型类型化处理 / 多模式策略，默认应落在 `references/type-strategies.md` 或等价模块，而不是继续整合进 `CONTEXT.md`
- `subtypes/<subskill-name>/SKILL.md` 的角色（子技能规范合同）：
  - 定义该子技能的局部合同、边界、加载顺序、命名规则与进入条件
- `subtypes/<subskill-name>/CONTEXT.md` 的角色（子技能经验层）：
  - 仅保存该子技能自身的局部 heuristic、陷阱、案例与修复模式
  - 不得吞并属于主技能根层 `CONTEXT.md` 的跨子技能或整技能经验
- 运行时加载顺序与优先级：
  1. 先解析 `SKILL.md`，锁定强制约束
  2. 若进入某个受治理子技能，先加载 `subtypes/<subskill-name>/SKILL.md`，锁定局部合同
  3. 若当前技能或子技能声明 `references/` 为核心细则模块层，则按任务需要加载相关模块；涉及同一技能的类型化处理 / 多模式策略时，默认优先读取 `references/type-strategies.md` 或等价模块
  4. 加载主技能根层 `CONTEXT.md`，用于选择策略并避开整技能级已知失败模式
  5. 子技能 `CONTEXT.md` 仅用于该子技能自身的局部经验与陷阱
  6. 冲突优先级：用户显式请求 > `AGENTS.md` / meta 规则 > 主 `SKILL.md` > 子 `SKILL.md` > `agents/openai.yaml` > 已声明的 `references/` 模块 > 主 `CONTEXT.md` > 子 `CONTEXT.md`
- 维护规则：
  - 新的或尚不稳定的经验先写入 `CONTEXT.md`
  - 稳定、可重复、高置信度的实践再从 `CONTEXT.md` 晋升到 `SKILL.md`
  - 每个显著失败都应在 `CONTEXT.md` 中记录：症状、根因、修复与预防检查
  - 每个经用户确认的显著成功都应在 `CONTEXT.md` 中记录：结果、设计决策、提炼 heuristic 与可复制范围
  - 同一技能的类型化/多模式处理若已上升为执行前必须遵守的专项细则，应沉到 `references/type-strategies.md` 或等价模块；`CONTEXT.md` 只保留执行后沉淀出的经验性 Type Map、Playbook 与 Heuristics
  - 保持 `SKILL.md` 简洁且规范；保持 `CONTEXT.md` 可积累且经验化
  - 当主技能与子技能的 `CONTEXT.md` 同时存在时，新经验应优先写入最窄且有效的作用域；仅当模式跨子技能边界或已经成为整技能级政策时，才向上晋升

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
  - 子单元自己的 `references/` 应只承载局部写位、sidecar 规则、执行流程、路由策略或本地约束，不得重写父级输出真源。
- 若共享目标当前无法直接承接局部 patch，必须显式报告：
  - 阻塞原因
  - 临时聚合适配层
  - 临时同步护栏
  - 为什么当前还不能完全收敛为单一真源

## 源层治理

### 根因优先（强制）

- 当用户反馈项目问题或任务执行故障时，必须先调查源层原因，再决定是否修补本地产物。
- 源层诊断应优先检查规则工件与执行入口，通常包括 `SKILL.md`、已声明为核心细则模块层的 `references/`、`CONTEXT.md`、命令 runbook、阶段模板与相关脚本。
- 源层追踪必须分层进行：不得停在第一个局部原因，必须继续上溯直到识别治理该行为的规则源。
- 非平凡问题的强制追因链为：
  - `Symptom/Failure` -> `Direct Technical Cause` -> `Rule Source`（skill / runbook / template / script gate）-> `Meta Rule Source`（meta-AGENT / meta-SKILL / global policy）-> `Fix Landing Points`
- `Rule Source` 通常包括：任务级 `SKILL.md`、`references/` 模块细则、命令 runbook、阶段模板、验证脚本与执行入口。
- `Meta Rule Source` 通常包括：仓库 `AGENTS.md`、`.codex/skills/meta/*/SKILL.md` 以及其他跨技能治理合同。
- 如果诊断无法上溯到 meta 层工件，必须明确说明为什么没有更高层治理合同。
- 对每个问题，都应给出简洁修复建议，包括：根因位置、立即修复、系统预防修复。
- 在使用 `SKILL` 执行、dry-run、工作流排练或 `pytest` 回归测试期间，迭代相关源层工件（`SKILL.md`、`references/`、`CONTEXT.md`、runbook、脚本、模板、验证器）应被视为合法且优先的并行目标，而不是事后补文档。
- 如果执行被阻塞，必须立即暂停下游动作，先完成分层追因与源层修复/增强，再恢复任务。
- 优先修复产生该错误模式的规则或脚本，使同类问题在后续运行中不再重复。
- 每一个非平凡修复都应视为一次源层增强机会：不仅要修症状，也要补强源层合同，降低类似问题再次发生的概率。
- 如果在工作中发现更优的执行路径或工作流，且源层重构风险可控，则允许在继续下游工作前优先完成源层优化。
- 如果优化的安全性、范围或预期收益不够明确，应先按 `PRPs/README.md` 记录为 `PRP`，再沿当前最安全路径继续工作，等待人工确认。
- 推荐的增强方向可从以下一项或多项中选择：显式 gate / 诊断（明确错误状态、非零退出码、可执行提示）、对不稳定依赖的 fallback / retry、将重复逻辑收敛到单一真源（配置 / 入口 / 共享 helper）、或在 `SKILL.md` / runbook 中补强合同说明。
- 只有满足以下条件，才算“增强闭环完成”：问题已修复 + 至少一个可复用的源层预防机制已落地 + 相关文档/合同已同步更新。
- 如果增强被权限、外部依赖或范围限制阻塞，必须显式报告阻塞项与临时防护措施。

### 根因学习回路自动化（强制）

该学习回路有两个方向，负向与正向都必须执行。

**负向触发**：当出现以下任一情况时自动触发：用户报告问题、运行失败、任务实践/测试阻塞（包括 `SKILL` 执行、dry-run 与 `pytest` 回归）、失败后返工、或用户明确要求修正。

- 无需额外等待用户提示，必须自动执行以下流程：
  1. 源层诊断（分层上溯）：从症状追到直接原因，再追到 `Rule Source`，必要时继续追到 `Meta Rule Source`（`AGENTS.md` / meta-SKILL）。
  2. 立即修复 + 增强：优先修补最高杠杆的源层工件（规则 / 脚本 / runbook / meta-rule），增加至少一项可复用的加固机制，然后再恢复下游执行；如仍有必要，再补本地产物。
  3. 上下文沉淀：使用 `meta/skill-context` 结构更新受影响技能的 `CONTEXT.md`（若缺失则创建）；优先更新 Type Map / Playbook / Reusable Heuristics，仅在达到里程碑级别时新增 Case Record。
  4. 预防晋升（自下而上）：将已验证的修复从本地产物 -> `CONTEXT.md` -> `SKILL.md` / runbook -> `AGENTS.md` 或 meta-SKILL 逐级晋升；若已观察到跨技能复发，则必须继续向上晋升。
  5. 面向用户的闭环输出：必须返回三元组 `root cause location + immediate fix + systemic prevention fix`，并附上分层追踪路径 `symptom -> rule source -> meta rule source`。

**正向触发**：当出现以下任一情况时自动触发：用户明确认可某输出（例如“这个很好”“以后按这个来”）、某设计决策在跨项目场景中被复用且无需重新推导、或输出质量明显超过预期基线。

- 无需额外等待用户提示，必须自动执行以下流程：
  1. 模式识别：定位产出正向结果的设计决策，例如 prompt 结构、参数选择、工作流顺序、字段映射或架构安排。
  2. 抽象：将该决策提炼为 1-3 句可复用 heuristic，且要限定适用范围（skill、阶段、领域、主题），避免过度泛化。
  3. 上下文沉淀：将 heuristic 写入对应技能的 `CONTEXT.md` 中的 Reusable Heuristics；仅当该模式足够新颖或具有跨技能复用价值时，再追加里程碑案例。
  4. 晋升（自下而上）：当同一正向模式在 >= 2 次独立执行中得到确认时，将其从 `CONTEXT.md` 晋升到 `SKILL.md`，必要时再晋升到 `AGENTS.md` 或 meta-SKILL。
  5. 面向用户的闭环输出：返回三元组：成功模式位置 + 提炼出的 heuristic + 晋升范围。
- **Case Record 里程碑类型**（创建/更新案例时必须提供 `milestone_type`）：
  - 负向里程碑：`new_failure_class`、`source_contract_change`、`repeated_pattern_promotion`
  - 正向里程碑：`new_success_class`、`cross_skill_heuristic`、`positive_promotion_evidence`
- Case Record 的最小必填字段包括：`milestone_type`、症状或结果、根因或设计决策、最终修复或提炼 heuristic、预防/复现检查清单、证据路径、用户反馈/约束。
- 如果只是修复了本地产物或确认了结果，却没有同步更新 `CONTEXT.md`，则视为 `Root-Cause Learning Loop` 尚未完成；若因阻塞无法更新，必须显式报告阻塞原因。

### AGENT、SKILL、REFERENCES、CONTEXT 与入口元数据放置矩阵（全局真源）

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
  - 如果某 agent 没有独立 `CONTEXT.md`，则稳定的规范增强可以直接写进 agent 规则文档本身
  - 这种 agent 级直接优化仅限于规范内容：规则、schema、优先级、失败闭环、路由与输出合同
  - 经验性内容不得直接倾倒进 agent 规则文档，例如单次案例、噪声实验、临时 heuristic 与里程碑证据，应保留在 `reports/`、技能 `CONTEXT.md` 或其他经验层载体中，待验证后再晋升
  - 晋升规则：重复、多轮、高置信度的 agent heuristic，可在足够稳定后从经验层载体晋升回 agent 规则文档
- 以下内容应写入 `SKILL.md`（规范合同）：
  - 触发条件、强制工作流、硬门槛与完成标准
  - 源层诊断顺序与修复顺序（包括上溯到 meta 合同的钩子）
  - 面向用户的标准闭环格式（根因位置 + 立即修复 + 系统预防修复）
  - 从经验到规范的晋升规则（何时可将重复模式提升为规范）
  - 当技能存在复杂选择逻辑时，定义领域专属的一层/二层/三层决策信号、tie-break 规则与显式覆盖条件
  - skill 自己的 `field_id` 主定义，以及 `step_id -> field_id` 和 `field_id -> quality_dimension -> fail_code -> rework_entry` 映射
- 以下内容应写入 `agents/openai.yaml`（入口元数据层）：
  - `display_name`、`short_description`、`default_prompt` 等 UI-facing 入口元数据
  - 与主 `SKILL.md` 同步的发现入口摘要
  - 不得承载独立于主合同之外的隐藏执行规则
- 以下内容应写入 `references/`（核心细则模块层）：
  - 可独立升级、但仍受主合同约束的专项细则模块
  - 思维链细则、执行流程细则、类型化处理 / 模式化策略、输出模板等长细则
  - 同一技能的多类型化 / 多模式化若属于执行前必须遵守的工作台，应优先落到 `references/type-strategies.md` 或同类模块，而不是放进 `CONTEXT.md`
  - 一旦某模块已成为 canonical module，主 `SKILL.md` 与其他文档应回链该模块，而不是平行复制同一套长说明
- 以下内容应写入 `CONTEXT.md`（经验层）：
  - Type Map（失败模式 -> 修复策略 -> 验证点）、Repair Playbook 与 Reusable Heuristics
  - 基于真实执行形成的 Case Record（里程碑级、低频、高价值；避免进度流水账）
  - 运行陷阱、兼容性问题、成功恢复策略
  - 多因素选择任务中的经验性 tie-break heuristic、收窄 heuristic 与观察到的失败模式
  - 对类型化处理的经验性复盘、失败模式、修复策略与验证点；但不承载同一技能的规范型多模式策略主表
  - 尚未稳定到足以晋升为 `SKILL.md` 的候选经验
- `CONTEXT.md` 支持多级放置。
- 当前规范特指主 `SKILL` 与子 `SKILL` 之间的多级放置：
  - 主技能根层 `CONTEXT.md`：整个技能族的默认经验层，承接跨子技能、跨模式、跨工作流的经验
  - 子技能 `CONTEXT.md`：用于受治理子技能的局部经验层，通常采用如下形态：

    ```text
    subtypes/
      <subskill-name>/
        SKILL.md
        CONTEXT.md
    ```

    子技能 `CONTEXT.md` 仅保存该子技能自己的局部 heuristic、陷阱、案例与修复模式，不得替代主技能根层 `CONTEXT.md`
- 子技能 `CONTEXT.md` 的升级规则：
  - 一旦某个技能采用受治理子技能结构，则范围内长期维护的子技能应显式表现为 `subtypes/<subskill-name>/SKILL.md + CONTEXT.md`
  - `references/` 默认不承担受治理子技能语义，但可由主技能或子技能合同声明为专项细则模块层；该情形下应视为可加载的规范细则承载层，而不是普通附录
  - 跨子技能或跨技能的 heuristic，仍必须回晋升到主技能根层 `CONTEXT.md` 或 `SKILL.md`
- 冲突优先级如下：用户显式请求 > `AGENTS.md` / meta-SKILL > 主 `SKILL.md` > 子 `SKILL.md` > `agents/openai.yaml` > 已声明的 `references/` 模块 > 主 `CONTEXT.md` > 子 `CONTEXT.md`

### Agent 源层优化合同（强制）

- Agent 规则文档是第一类源层工件，而不只是人格包装。
- 如果某个问题受 agent 自身合同约束，且该 agent 没有专用 `CONTEXT.md`，则应直接在 agent 规则文档中修复稳定规则，而不是等待外部经验层。
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

### CONTEXT 健康监控（强制）

- 每份 `CONTEXT.md` 都应包含自动维护的 `Context Health` 章节。
- 该要求同时适用于主技能根层 `CONTEXT.md` 与子技能 `CONTEXT.md`。
- 默认健康阈值如下：
  - `soft_limit_chars: 40000`，`hard_limit_chars: 80000`
  - `soft_limit_cases: 80`，`hard_limit_cases: 140`
- 动作策略：
  - `ok`：保持面向目标的知识更新，优先更新 Type Map / Playbook；仅在达到里程碑标准时追加案例
  - `warn`：对该技能的上下文做定向压缩与整理
  - `warn` 且文档很长但案例较少：优先做人为结构整理（章节合并/拆分/抽取），而不是只做案例压缩
  - `critical`：在继续大规模追加前，必须先压缩并归档旧内容
- 压缩时必须保持证据完整性：
  - 将近期活跃案例保留在 `CONTEXT.md`
  - 将较早案例归档到 `reports/context-archive/`，并保留可追踪索引
- 默认操作应针对单个技能上下文，而不是在未被要求时全仓重写。

### CONTEXT 知识库模式（强制）

- `CONTEXT.md` 的默认模式是知识库，而不是按时间顺序记录的日志。
- 该规则同时适用于主技能根层 `CONTEXT.md` 与子技能 `CONTEXT.md`。
- 优先维护以下内容：
  - Type Map：失败类型 -> 根因层级 -> 立即修复 -> 系统预防 -> 验证方式
  - Repair Playbook：稳定的排障顺序与 fallback 策略
  - Reusable Heuristics：简洁且高价值的可复用经验
  - `Type Map` 在此特指经验性映射与排障知识，不等于同一技能的规范型类型策略工作台；后者应放在 `references/type-strategies.md` 或等价模块
- Case Log 频率控制：
  - 仅在里程碑事件发生时新增/追加案例。负向里程碑包括：新错误类别、源规则变更、重复模式晋升；正向里程碑包括：新成功类别、跨技能可复用 heuristic、正向晋升证据
  - 对于非里程碑迭代，应优先更新已有 Type Map / Playbook / Heuristics，而不是新建案例
- 禁止记录低价值内容：
  - 进度叙述、仅做表面润色的修改、无法提供复用防护或复制价值的一次性噪声笔记
