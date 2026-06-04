# AGENTS.md
<!-- last_synced: 2026-06-04 | version: 2026-06-04 -->

行业通用的 AI 智能体指令文件。兼容 Claude Code、Cursor、Windsurf 及其他 AI 编码工具。

## 项目基线

### 项目概览

AIGC（AI Generated Content）视频·小说·漫画创作管理工作区。该仓库不是传统意义上承载多个独立软件子项目的代码仓，而是用于组织 AIGC 创作流的项目工作台：

- 以 `projects/` 作为创作项目总容器，并按媒介进入对应 canonical runtime
- 影视 / 视频 / AIGC 短剧项目使用 `projects/aigc/<项目名>/`
- 小说 / 长篇故事项目使用 `projects/story/<项目名>/`
- 漫画项目在命中 comic 技能时使用 `projects/comic/<项目名>/`
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
- 影视类创作项目通常以 `projects/aigc/<项目名>/` 作为主工作目录；小说与漫画项目按项目概览中的媒介命名空间落位。
- 模板要求时，提示中的任务 ID 应保持 ASCII 安全字符。

### 重命名引用同步（强制）

- 当重命名文件或文件夹时，必须自动扫描整个仓库中对旧路径的引用，并同步更新到新路径。扫描范围包括脚本、配置、`SKILL.md`、`CONTEXT.md`、命令文档、模板以及其他 markdown / 代码文件。
- 扫描目标包括但不限于：`import` / `require` 语句、路径字符串、符号链接、JSON / YAML 配置项、markdown 链接以及 shell 命令参数。
- 如果某些引用无法自动更新，例如存在于二进制文件或外部系统中，必须显式向用户报告该遗留引用。

### 架构决策

- `projects/` 是项目总容器；对当前仓库的 AIGC 影视工作流，规范命名空间固定为 `projects/aigc/`，而不是把项目直接平铺在 `projects/` 根层。
- 对当前仓库，媒介归属通过技能路由、项目元数据和 canonical runtime namespace 表达：影视落到 `projects/aigc/<项目名>/`，小说落到 `projects/story/<项目名>/`，漫画落到 `projects/comic/<项目名>/`；不得再引入 `projects/影片/<项目名>/` / `projects/小说/<项目名>/` 作为第二层路径真源。
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
- 当用户使用英文提问时，应首先判断用户是否期望英文响应：
  - 若用户明确要求英文输出（如 "please respond in English"），则使用英文
  - 若用户仅使用英文措辞但未明确要求语言切换，默认保持中文响应
  - 若任务本身涉及英文技术文档、代码、API 或需要输出英文内容，以任务需求为准
- 多语言混合输入时，以用户的主要意图语言为准；若意图不清，优先使用中文响应

### Skill 路由失败兜底策略（强制）

当用户输入同时命中多个 skill、或命中 skill 但无法确定子技能路由时，按以下策略处理：

1. **多命中仲裁**：
   - 若同时命中的 skill 存在明确的父子关系，优先路由到子技能
   - 若命中的 skill 之间无父子关系，按以下优先级选择：主技能 > 卫星技能 > 子技能
   - 若仍无法裁决，以用户的第一个请求词或任务关键词为路由锚点

2. **无命中兜底**：
   - 若用户输入未命中任何已知 skill，以任务类型为锚点尝试最近似匹配
   - 若无近似匹配，进入自由任务模式，按 AGENTS.md 通用规则处理
   - 自由任务模式下的输出应明确说明"未命中特定 skill，按通用规则执行"

3. **部分命中处理**：
   - 若命中 skill 但缺少必要的输入字段，显式询问缺失字段
   - 不得在输入不完整时假设默认值或跳过必要校验

4. **路由失败报告**：
   - 若路由失败且无法自动兜底，必须显式报告：
     - 当前命中的 skill（若有）
     - 路由失败的原因
     - 已尝试的兜底策略
     - 需要用户确认的信息

## 规则优先级与分级

### 全局冲突优先级（强制）

当本文件内或跨文件的规则出现冲突时，按以下顺序裁决：

1. 用户显式指令
2. 安全与权限规则（`.env` 禁提交、路径安全等）
3. 根 `AGENTS.md` / 共享治理合同（`office-governance-contract.md`）
4. 主 `SKILL.md`（规范合同）
5. 子技能 / 卫星技能 `SKILL.md`（局部合同）
6. 当前 `SKILL.md` 通过 `Module Loading Matrix` 显式授权的模块（`references/`、`review/`、`types/`、`templates/`、`scripts/`、`guardrails/`、`assets/`、`steps/`、`knowledge-base/` 等）
7. 项目级 `MEMORY.md` > 项目级 `CONTEXT/` > 主 `CONTEXT.md` > 子/卫星 `CONTEXT.md`
8. 按需读取的 `CHANGELOG.md`

### 规则分级

本文件中的规则分为三级，执行时按级处理：

- **P0-硬门槛**：不可绕过、不可降级。违反时必须暂停执行并修复。典型规则：安全红线、真源治理、根因上溯、`bootstrap_compat` 退出条件、LLM-first 主创规则。
- **P1-默认规则**：默认遵守，用户可显式覆盖。违反时应报告偏离理由。典型规则：执行深度默认标准、批量调度默认语义、CONTEXT 健康阈值、Skill 2.0 runtime-spine 结构基线。
- **P2-最佳实践**：应遵守但不阻断执行。违反时记入经验层待后续改进。典型规则：命名约定、提交格式、CHANGELOG 维护建议、PR 叙述要求。

各规则章节中标注的"（强制）"对应 P0；未标注的默认为 P1；建议性表述默认为 P2。

### P0 规则冲突 Tie-Break 协议（强制）

当两条或以上 P0 规则在同一执行上下文中产生不可调和的冲突时，按以下顺序裁决：

1. **安全与权限规则优先**：涉及 `.env` 禁提交、路径安全、权限边界、API 密钥保护的规则 > 其他任何 P0 规则
2. **用户显式指令次之**：用户明确要求"必须"、"不得"、"禁止"的事项，覆盖任何 P0 规则
3. **真源收束规则优先**：涉及"单一真源"、"不得演化第二真相"的规则 > 具体执行规则
4. **根因上溯规则优先**：当诊断规则与修复规则冲突时，诊断规则优先（先定位，再行动）
5. **硬门槛兜底**：若仍无法裁决，取更宽泛的解释（给执行留有余地），并在输出中显式说明冲突点和临时护栏

> **注**：`bootstrap_compat` 模式下的临时降级不受此 tie-break 约束；降级期间以临时护栏声明为准。

### 调度前缀与角色类型的边界澄清（强制）

命名前缀的调度语义仅适用于 `skills` 子技能包的结构化分组，不得与角色类型（主技能、子技能、卫星技能）的语义混淆：

- **数字序号（如 `1-`、`2-`）**：表示串行执行顺序，但若该子技能同时被声明为卫星技能角色，则默认不参与主链聚合，应以角色类型合同为准
- **英文序号（如 `A-`、`B-`）**：表示互斥候选，但卫星技能即使以 `A-` 命名，也不应自动参与互斥选择；是否参与由父技能显式声明
- **卫星技能无论命名前缀为何**：其默认合同是不参与主链串行聚合，除非父技能明确将其输出声明为共享目标的必需 side input

若父技能需要对卫星技能进行串行调度，必须在 `SKILL.md` 中显式声明"该卫星技能参与聚合"及其调度位置，不得依赖命名前缀语义自动推断。

## SKILL 2.0 运行规则

### 内容创作型任务的 LLM 主创规则（强制）

- 对 `SKILL` 命中的内容创作型任务，核心创作环节必须由 LLM 直接完成，不得把脚本当作主创执行器。
- 这里的“核心创作环节”包括但不限于：故事/章节正文、剧本改编、角色设定、场景设定、道具设定、研究结论、设计描述、提示词蒸馏、分镜/面板创作决策、海报文案、创作型总结与其他需要审美判断、叙事判断、风格判断的正文生成。
- 脚本只允许承担非主创辅助职责，例如：读取、抽取、切分、组装、格式转换、模板投影、复制粘贴、路径归档、批量提交、去重、校验、审计、统计、diff、manifest 回写与其他机械性流程。
- 脚本不得直接生成上述核心创作正文，不得以规则拼接、模板灌字、启发式补句、字段压缩扩写等方式替代 LLM 创作；即便脚本生成结果“可读”，也不得将其视为 canonical creative truth。
- 若某个内容创作型 skill 当前仍以脚本生成创作正文、提示词、设计稿、研究稿、layout 决策或等价创作产物，必须判定为源层违规，并回收为：`LLM 直出 canonical creative truth -> 脚本仅做投影/校验/落盘/执行辅助`。
- 对现有工作流的兼容改造，允许暂时保留脚本型 carrier、validator、runner 与 provider bridge，但不得继续扩大脚本主创覆盖面；任何新增创作链路默认必须按 `LLM-first creative authorship` 设计。
- 审查此类问题时，必须沿链路上溯：`Symptom -> Direct Script Overreach -> Skill/Template/Runner Source -> AGENTS.md 本条规则`。

### AIGC 创作型 SKILL 执行报告证据标准（强制）

- 对 `projects/aigc/<项目名>/` 下正式写回 canonical 产物的内容创作型 skill，若该 skill 的 `Output Contract` 声明需要同步生成执行报告，则报告不是可选附属物，而是完成门禁的一部分。
- 执行报告必须记录“可公开、可审计的执行决策链”，不得输出自由散文式、不可验证的长篇思维链；这里的“思考过程”应落为结构化的 `Execution Decision Trace`，说明关键判断、适用规则、输入证据、取舍理由和输出落点。
- 执行报告必须记录 `Reference Execution Matrix`：对当前 `SKILL.md` 通过 `Module Loading Matrix` 和 `Module Trigger Matrix` 授权加载的 `references/` 细则，逐条说明 `reference`、`load_status`、`trigger_reason`、`applied_to`、`evidence_in_output`、`verdict` 与 `n/a_reason`。
- 执行报告必须采用“全量审计 / 选择性触发 / 必须说明未触发原因”模式：已授权且本轮相关的细则必须审计；不适用的细则必须写明 `N/A` 理由；不得用“已参考”“已综合考虑”等泛化表述替代证据。
- 执行报告必须包含 `Rule Evidence Map`：把关键 gate、字段合同、声画配对、节奏承托、高潮/尾钩、保真边界、下游 handoff 等规则映射到正文位置、source anchor 或报告证据。
- 执行报告必须包含 `N/A Justification` 与 `Repair Log`：规则未触发时说明原因；候选稿曾经违反 gate 时记录失败码、返工目标和修复结果。
- `Reference Execution Matrix`、`Execution Decision Trace`、`Rule Evidence Map`、`N/A Justification`、`Repair Log` 中任一必需证据缺失时，正式写回不得判定为 `pass`；应回到对应 `Review Gate Binding` 的返工目标补证或修复。
- 报告证据服务审计和下游交接，不得替代 canonical 创作正文，不得把完整创作过程稿、冗长推演或未筛选草稿灌入共享业务真源。

### 批量 SKILL 调度默认规则（强制）

- 对 `skills` 子技能包的同级调度，命名前缀本身即为默认调度语义，无需额外显式声明。
- 无序号子技能包：命中同级无序号子技能包组时，默认全选并行执行。
- 数字序号子技能包：形如 `1-`、`2-`、`3-` 的同级子技能包默认按数字升序顺序串行执行。
- 英文序号子技能包：形如 `A-`、`B-`、`C-` 或 `a-`、`b-`、`c-` 的同级子技能包默认作为互斥候选，按用户意图、父技能路由或任务类型单选执行。
- 上述命名前缀语义仅针对 `skills` 子技能包与技能层调度，不外推到协作成员、顾问或外部 provider；协作成员一般不以名称序号承载调度语义。
- 若用户显式指定不同调度方式，以用户显式指令优先；否则按本命名前缀语义执行。

### Skill 2.0 Runtime-Spine 基线（强制）

- 本仓库恢复 Skill 2.0 作为长期技能工程与项目级编排治理外壳，但采用 runtime-spine 版 Skill 2.0；不得恢复旧的“完整分区越多越合规”制度。
- 长期维护的可执行 skill 默认应采用 core layout：

  ```text
  skill-name/
  ├── agents/
  │   └── openai.yaml
  ├── CHANGELOG.md
  ├── SKILL.md
  ├── CONTEXT.md
  └── README.md
  ```
- `SKILL.md` 是单次任务执行主脊柱，必须能独立跑通最小合格任务路径；不得退化为目录导航、入口摘要或引用索引。
- runtime-spine `SKILL.md` 应至少表达：`Context Loading Contract`、`Runtime Spine Contract`、`Input Contract`、`Type Routing Matrix`、`Thinking-Action Node Map`、`Module Loading Matrix`、`Convergence Contract`、`Multi-Subskill Continuous Workflow`、`Review Gate Binding`、`Root-Cause Execution Contract`、`Field Mapping`、`Output Contract` 与 `Learning / Context Writeback`。
- `references/`、`review/`、`types/`、`templates/`、`scripts/`、`guardrails/`、`assets/`、`steps/`、`knowledge-base/` 是受支持的可选模块；只有在技能自身 `SKILL.md` 的 `Module Loading Matrix` 显式声明触发条件、权限边界、禁止越权和回接 gate 时才参与执行。
- 可选模块不得作为第二规则源：模块可以展开、校验、投影或提供资料，但不得改写 `SKILL.md` 的入口、节点、路由、gate、输出合同或学习回写规则。
- `steps/` 不再是默认执行主链；思行节点主表必须在 `SKILL.md`。若启用 `steps/`，它只能展开 `SKILL.md` 已声明节点，不能维护第二节点网络。
- `Type Routing Matrix.module_load` 应写成可解析的已授权模块或模块内真实文件路径；不得只写“按需加载”“按失败码加载”等依赖模型自行猜测的自然语言。
- `Convergence Contract` 必须定义关键汇流点的通过条件、失败条件、证据和返工目标；最终完成不得只靠自我声明。
- `knowledge-base/` 只承载用户或维护者手动加入的外部资料、参考包和资料索引；执行中产生的经验、失败模式、成功模式、修复打法与 reusable heuristic 写入同目录 `CONTEXT.md`。
- `templates/` 只承载输出模板、脚手架模板和报告模板；它必须映射 `SKILL.md` 的 Output Contract，不得另立输出路径、命名规范或完成门禁。
- `scripts/` 只承载机械创建、校验、格式转换、批量处理、diff、manifest 回写等辅助动作；内容创作、审美判断、叙事判断和复杂策略判断仍由 LLM 完成。
- 创建、升级、修复或审计 Skill 2.0 包时，以 `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-2.0` 为当前 canonical meta skill；不得继续引用已废弃的旧元技能路径。
- 旧技能升级到 Skill 2.0 时，必须先建立迁移矩阵，标注旧 `SKILL.md`、同目录资源和入口元数据中每个 section / 资源的 `SKILL.md` 落点或授权模块落点、迁移动作、语义风险、引用更新与验证门禁。

### 项目级记忆与上下文规则（强制）

- 对 `story` 与 `aigc` 这类项目型创作工作流，初始化项目目录时还必须同步创建项目级 `MEMORY.md`：

  - `projects/story/<项目名>/MEMORY.md`
  - `projects/aigc/<项目名>/MEMORY.md`
- 对 `story` 与 `aigc` 这类项目型创作工作流，初始化项目目录时还必须同步创建项目级 `CONTEXT/`：

  - `projects/story/<项目名>/CONTEXT/`
  - `projects/aigc/<项目名>/CONTEXT/`
- 项目级 `MEMORY.md` 是当前项目的创作记忆载体，用于沉淀跨阶段持续生效的偏好、口味、习惯、特殊元素、禁区与长期要求。
- 项目级 `CONTEXT/` 不替代技能同目录 `CONTEXT.md`；它是项目运行时的附加上下文根，面向整个创作阶段共享。

### 团队技能索引同步（强制）

- 对 `.agents/skills/team/` 技能树，凡成员配置出现新增、删除、重命名、迁移或适配场景显著变化，都必须在同一轮任务内同步更新 `.agents/skills/team/SKILL.md` 的 `Member And Scenario Index`；不得允许 team 子树与根索引脱节。

### 技能组成与语义

- 技能载体基线：
  - 长期维护的可执行 skill 默认采用 Skill 2.0 runtime-spine 基线：core layout 由 `SKILL.md`、`CONTEXT.md`、`README.md`、`CHANGELOG.md`、`agents/openai.yaml` 构成。
  - `SKILL.md` 是执行主合同，负责入口、输入、类型路由、思行节点、模块授权、关键门禁、输出合同和学习回写。
  - `CONTEXT.md` 是经验层，作为预加载运行上下文和可复用知识库。
  - `references/`、`review/`、`types/`、`templates/`、`scripts/`、`guardrails/`、`assets/`、`steps/`、`knowledge-base/` 只有在当前技能 `SKILL.md` 显式授权时才参与执行；它们是模块展开层，不是根层强制完整分区。
- `SKILL` 细分定位（仓库级规范）：
  - 主技能：拥有一段业务域或一条阶段链的总入口、总路由、共享载体边界与真源裁决权。形态通常为 `<skill-root>/SKILL.md + CONTEXT.md`，也可以是技能树中的阶段根，例如 `aigc/1-规划`。
  - 父级导引 skill：主技能或阶段根的一种轻量形态，只负责路由、边界、聚合、回接和门禁，不直接吞并子技能的局部执行合同或业务真源。
  - 子模块：主技能或子技能为了拆分长细则而挂出的非执行模块；它们提供规则细则，但不拥有独立调度权、闭环权或经验层主权。
  - 子技能：受治理的可执行下钻单元；其路径、命名与载体形态由父级主技能显式声明，不再绑定固定目录包裹约定。它们由父级主技能路由进入，负责局部执行合同，避免擅自越权为新的总入口。
  - 卫星技能：与主技能同根同级放置的旁路可执行 skill，推荐形态为 `<skill-root>/<satellite-name>/SKILL.md + CONTEXT.md`；它们服务查询、恢复、复核、汇总、桥接等辅助职责，可被直接调用，但不默认冒充新的主链 stage 或新的父级总线。
- 结构判定规则：
  - 若某单元只提供长细则、样例、schema、思维链或策略表，而不独立受理任务，则它是子模块，不是子技能。
  - 若某单元需要经父级路由进入，且其结果默认回流到父级共享目标，则它优先视为子技能。
  - 若某单元与主技能同根同级存在，可直接被用户或上游命中，承担查询/恢复/审查承接等旁路职责，则它优先视为卫星技能。
  - 若某单元既想直达受理任务，又想长期维护独立 `CONTEXT.md`，则不应伪装成普通说明文件，应显式定义为子技能或卫星技能之一。
- 现有结构判例：
  - `aigc/SKILL.md` 与各阶段根（如 `aigc/1-规划`、`aigc/3-Detail`）属于主技能层。
  - 跨项目仓 `story2026/query`、`story2026/resume` 属于卫星技能层；`story2026/review` 若被根技能声明为旁路承接而非主链真源拥有者，也应按卫星技能合同治理其边界。
- `卫星技能` 的角色：
  - 是主技能侧的旁路执行层，而不是普通说明文件，也不是默认加入主链阶段序列的子技能
  - 应在主技能 `SKILL.md` 中显式声明其 `stage_position`、`truth ownership`、`not-owned truth` 与回接关系
  - 可使用主技能允许的共享载体，但不应借共享载体偷渡新的总线规则
  - 默认只拥有辅助真源或辅助动作权，例如查询、恢复、审查承接、状态持久化、桥接；不应改写主技能或主链 stage 的 canonical truth 判定权
- `SKILL.md` 的角色（硬规则）：
  - 定义范围、触发条件、必需输入、Mode Selection、Type Routing Matrix、Thinking-Action Node Map、Module Loading Matrix、Convergence Contract、核心工作流、工具/脚本入口、输出合同与质量门槛
  - 应明确、可执行、偏确定性；避免长篇叙述，也不要存放易过期的零散技巧
  - 对 Skill 2.0 包，`SKILL.md` 不得只是 `Reference Loading Guide` 或目录导航；它必须包含能独立跑通单次任务的 runtime spine。
- `CONTEXT.md` 的角色（经验层）：
  - 保存可复用的 heuristic：成功/失败案例、陷阱、调试线索、兼容性注记、提示技巧与战术捷径
  - 作为规划/执行时的预加载上下文，但不得重定义核心合同
  - `CONTEXT.md` 中的 Type Map 属于经验性映射与修复知识，不得替代 `SKILL.md` 的执行主合同
- `MEMORY.md` 的角色（项目记忆层）：
  - 保存当前项目跨阶段持续生效的创作偏好、审美口味、表达习惯、长期保留元素、明确禁区、长期协作要求与其他“以后继续按这个项目执行”的稳定约束
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
  - 应写清它与主链或主技能的回接位置，避免卫星技能演化成隐式第二总入口
- `<satellite-name>/CONTEXT.md` 的角色（卫星技能经验层）：
  - 仅保存该卫星技能自身的局部 heuristic、运行陷阱、恢复/查询/承接策略
  - 不得吞并属于主技能根层 `CONTEXT.md` 的跨卫星、跨主链或整技能经验
- 运行时加载顺序与优先级：
  1. 每次命中任意 skill 时，先成对定位当前命中的 `SKILL.md` 与其同目录 `CONTEXT.md`；二者共同构成该 skill 的默认预加载入口。
  2. 先解析当前命中的 `SKILL.md`，锁定强制约束、总路由与真源边界。
  3. 立即加载该 `SKILL.md` 同目录 `CONTEXT.md`，用于选择策略并避开该技能已知经验性失败模式。
  4. 若当前任务已绑定 `projects/story/<项目名>/` 或 `projects/aigc/<项目名>/`，则在进入具体阶段执行前，先加载该项目根 `MEMORY.md`，再加载项目根 `CONTEXT/` 目录中与本轮任务相关的上下文文件；前者是项目创作记忆，后者是项目共享附加上下文。
  5. 若进入某个受治理子技能，按同样规则加载该子技能在父级合同中声明的局部 `SKILL.md + CONTEXT.md`；若进入某个卫星技能，按同样规则加载 `<satellite-name>/SKILL.md + CONTEXT.md`，锁定其局部合同与局部经验层。
  6. 若当前 `SKILL.md` 包含 `Module Loading Matrix`，只按其触发条件加载被授权模块；未授权模块不得作为默认上下文或阻断真源。
  7. `CHANGELOG.md`、执行报告、迁移记录与其他时间序载体默认不预加载；仅在需要追溯详细变更过程时按需读取。
  8. 冲突优先级：用户显式请求 > `AGENTS.md` / meta 规则 > 主 `SKILL.md` > 当前命中的子技能或卫星技能 `SKILL.md` > 当前 `SKILL.md` 授权模块 > 项目级 `MEMORY.md` > 项目级 `CONTEXT/` > 主 `CONTEXT.md` > 当前命中的子技能或卫星技能 `CONTEXT.md` > 按需读取的 `CHANGELOG.md`
- 维护规则：
  - 新的或尚不稳定的经验先写入 `CONTEXT.md`
  - 稳定、可重复、高置信度的实践再从 `CONTEXT.md` 晋升到 `SKILL.md`
  - 每个显著失败都应在 `CONTEXT.md` 中记录：症状、根因、修复与预防检查
  - 每个经用户确认的显著成功都应在 `CONTEXT.md` 中记录：结果、设计决策、提炼 heuristic 与可复制范围
  - 当前项目内一旦出现新的稳定偏好、禁区、长期要求、特殊元素或用户明确要求“以后都按这个来”的口径，应优先写入项目根 `MEMORY.md`
  - 若 `MEMORY.md` 中已有记录被用户替换、撤销或纠偏，必须同轮更新或删除旧条目，不得让项目记忆保留失效偏好
  - 每次用户主动针对 `projects/aigc/<项目名>/` 或 `projects/story/<项目名>/` 下相关项目发出清空、移除或等价删除指令时，必须顺带自动检查当前项目内展示其创作记录、阶段状态与进度的载体是否需要同步更新，例如项目根或阶段目录中的 `STATE.json`、进度索引、章节/分镜清单、manifest 或其他项目内状态文件；若存在已删除产物对应的状态残留、进度残留或索引残留，应在同轮同步修正或明确报告无法自动处理的遗留项。该规则不要求围绕 Git 追踪状态、跨项目治理镜像或外部控制面做泛化检查，除非当前项目合同另有显式声明。
  - 跨项目可复用的失败模式、修复策略、调试结论与治理规则，仍应写回技能 `CONTEXT.md` 或上升到 `SKILL.md` / `AGENTS.md`，不得写进单项目 `MEMORY.md`
  - 详细变更时间线、迁移流水、执行长日志应优先写入 `CHANGELOG.md` 或 `reports/`，而不是把 `CONTEXT.md` 写成时间序备忘录
  - 保持 `SKILL.md` 简洁且规范；保持 `CONTEXT.md` 可积累且经验化
  - 当主技能、子技能与卫星技能的 `CONTEXT.md` 同时存在时，新经验应优先写入最窄且有效的作用域；仅当模式跨子技能、跨卫星或已经成为整技能级政策时，才向上晋升

### 复合型技能输出治理合同（强制）

- 当一个主 `SKILL` 负责调度多个子技能、子模块或受治理执行单元，并最终要把结果继续落盘到共享目标时，默认采用“子单元受理输出 + 主技能按规则聚合落盘”的复合型输出机制。
- 共享目标（例如统一根文件、统一主稿、共享结构化对象）是唯一业务真相，只承载累计后的最终事实，不承载每个子单元的完整过程稿。
- 主技能拥有以下职责：
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
  - 子单元应显式回指父级真源。
  - 子单元不得再额外定义第二份平行输出模板。
  - 子单元自己的局部文件、样例或 sidecar 规则，只应承载局部写位、执行流程、路由策略或本地约束，不得重写父级输出真源。
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
- 压缩时应保持证据完整性：
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

- 执行任务时，默认按“成熟版 engine”标准推进，避免因为习惯性谨慎而总是停在“最小补丁”或“最小闭环”。
- 判断应做到哪一层时，以”用户需求自然要求的完成层级”为准，而不是以”当前最小可改动量”为准。
- 对技能、工作流、规则、编排系统、模板体系、验证链路这类任务，默认目标应接近”成熟版 grouping engine”口径：
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

### “成熟版 engine”的量化特征定义

以下特征用于判断当前工作是否已达到”成熟版”标准：

| 特征维度 | 量化指标 | 说明 |
| -------- | -------- | ---- |
| **运行时完整性** | `SKILL.md` 包含完整的 `Runtime Spine Contract`（入口 → 类型路由 → 思行节点 → 输出合同 → 回写） | 可独立跑通最小合格任务路径 |
| **下游调用覆盖** | 至少覆盖 2 个下游调用节点（如子技能调度、外部脚本、验证器调用） | 非单点线性处理 |
| **类型路由存在** | `Type Routing Matrix` 包含至少 3 种有效路由分支 | 非单一路径死路 |
| **真源收束** | 输入/输出合同在 `SKILL.md` 中显式声明，不依赖隐式推断 | 可追溯、可验证 |
| **防回归机制** | 包含 validator、dry-run、smoke test 或等效校验链路之一 | 可自检、可回归 |

**判断规则**：

- 满足全部 5 项 → 达到成熟版标准
- 满足 3-4 项 → 接近成熟版，存在可改进空间
- 满足 1-2 项 → 处于早期阶段，需要补充
- 满足 0 项 → 视为脚手架或探索性原型，不计入成熟版统计

**注**：此特征清单是经验性参考，不是硬性合规门槛。特殊场景（如一次性任务、快速原型）允许跳过部分特征，但应在输出中显式说明当前处于”原型/实验”状态。

### 源层自动迭代触发协议（强制）

- `源层治理`、`源层同步` 与 `源层优化` 是任务执行中的自动行为，不是只有用户再次点名才执行的事后文档整理。
- 当用户已经明确指出某条规则、技能、工作流、模板、脚本、验证链路或治理合同“没有自动触发、没有同步、没有自发升级、反复失效、执行时漏掉”时，必须把该反馈本身视为负向触发，并在同一轮任务中优先修复对应源层合同。
- 每轮任务结束前必须执行一次 `Source Sync Check`，即使最终不展开说明也要完成判断：
  1. 用户本轮是否反馈了规则、技能、工作流、模板、脚本、验证链路或治理合同的问题？
  2. 本轮是否出现了可复用的负向失败模式或正向成功模式？
  3. 本轮是否修改了规则、模板、脚本、registry、route、runbook、agent doc 或其他会影响后续执行的源层工件？
- 任一问题答案为“是”，必须执行最小源层闭环：
  1. 定位最高杠杆源层工件。
  2. 修复该工件，并同步直接受影响的引用或派生文档。
  3. 做一次可行验证；无法验证时说明阻塞和临时护栏。
  4. 在最终回复中给出 `源层触发 -> 已同步内容 -> 验证结果`。
- 若问题涉及 skill、工作流、模板、脚本或验证链路，源层闭环必须优先按 Skill 2.0 runtime-spine 模型追因：
  1. 先检查目标 `SKILL.md` 是否能独立跑通任务路径。
  2. 再检查 `Type Routing Matrix.required_nodes`、`Type Routing Matrix.module_load` 与 `Module Loading Matrix` 是否能互相解析。
  3. 再检查 `Convergence Contract` 是否给出可验收的汇流/返工门。
  4. 再检查授权模块、模板、脚本、README、registry、route、runbook、AGENTS/HARNESS 是否与 `SKILL.md` 同步。
  5. 最后运行对应 validator、smoke test、dry-run 或审计脚本。
- 若问题来自文档与脚本、模板与 validator、父技能与子技能、registry 与 routes、agent doc 与父层 topology 漂移，必须同步受影响关联面，而不是只修当前文件。
- 若问题已表现为跨技能、跨阶段或跨项目复发，必须把预防机制向上晋升到 `AGENTS.md`、meta-SKILL 或共享治理合同。
- 自动迭代的默认顺序为：`触发识别 -> 源层追因 -> 源层修复/优化 -> 引用同步 -> 审计或 smoke 验证 -> 经验沉淀或规范晋升 -> 继续原任务`。
- 对 Skill 2.0 相关源层优化，默认顺序细化为：`症状 -> SKILL.md runtime spine -> Type Routing / Module Loading / Convergence -> 授权模块 -> 模板/脚本/validator/smoke -> 根 AGENTS/HARNESS -> 验证 -> CONTEXT 经验沉淀`。
- 除非用户明确要求只解释、不改文件，或者更高优先级权限/安全规则阻断，否则不得把“是否进行源层升级”作为追问项；应直接实施可控范围内的源层修复，并在最终输出中说明已完成的升级点和剩余阻塞。
- 如果当前任务不是修复源层本身，但执行过程中发现了低风险、高复用的源层改进机会，应在不破坏用户主目标的前提下并行完成；若改动风险较高或范围会明显扩大，必须记录为 `PRP` 或未决项，并继续当前最安全路径。
- 自动迭代不能只停在 `CONTEXT.md` 经验记录：已确认会影响后续执行的稳定规则、触发条件、路由、输出合同、验证门禁或同步范围，必须晋升到对应规范真源。

### 根因优先（强制）

- 当用户反馈项目问题或任务执行故障时，必须先调查源层原因，再决定是否修补本地产物。
- 源层诊断应优先检查规则工件与执行入口，通常包括 `AGENTS.md`、目标 `SKILL.md`、`CONTEXT.md`、命令 runbook、阶段模板、registry、route、agent doc 与相关脚本。
- 源层修复/优化应先判断最高杠杆源层工件，避免把所有修复继续堆回 `SKILL.md` 或 `CONTEXT.md`。
- 源层诊断不仅要看“写了什么规则”，还要看“规则要求如何思考与如何执行”：凡规则工件中存在执行流程、判断分叉、tie-break、字段思考顺序、聚合/回写顺序等设计，均应视为可追因、可优化的源层合同。
- 源层追踪必须分层进行：不得停在第一个局部原因，必须继续上溯直到识别治理该行为的规则源。
- 非平凡问题的强制追因链为：
  - `Symptom/Failure` -> `Runtime Artifact` -> `Direct Technical Cause` -> `Rule Source` -> `Meta Rule Source` -> `Fix Landing Points` -> `Reference Sync` -> `Audit/Smoke`
- `Rule Source` 通常包括：任务级 `SKILL.md`、命令 runbook、阶段模板、验证脚本与执行入口。
- `Meta Rule Source` 通常包括：仓库 `AGENTS.md`、`.codex/skills/meta/*/SKILL.md` 以及其他跨技能治理合同。
- 如果诊断无法上溯到 meta 层工件，必须明确说明为什么没有更高层治理合同。
- 对每个问题，都应给出简洁修复建议，包括：根因位置、立即修复、系统预防修复、引用同步范围与验证门禁。
- 在使用 `SKILL` 执行、dry-run、工作流排练或 `pytest` 回归测试期间，迭代相关源层工件（`SKILL.md`、`CONTEXT.md`、runbook、脚本、模板、验证器）应被视为合法且优先的并行目标，而不是事后补文档。
- 如果执行被阻塞，必须立即暂停下游动作，先完成分层追因与源层修复/增强，再恢复任务。
- 优先修复产生该错误模式的规则或脚本，使同类问题在后续运行中不再重复。
- 每一个非平凡修复都应视为一次源层增强机会：不仅要修症状，也要补强源层合同，降低类似问题再次发生的概率。
- 如果在工作中发现更优的执行路径或工作流，且源层重构风险可控，则允许在继续下游工作前优先完成源层优化。
- 如果优化的安全性、范围或预期收益不够明确，应先按 `PRPs/README.md` 记录为 `PRP`，再沿当前最安全路径继续工作，等待人工确认。
- 推荐的增强方向可从以下一项或多项中选择：显式 gate / 诊断（明确错误状态、非零退出码、可执行提示）、对不稳定依赖的 fallback / retry、将重复逻辑收敛到单一真源（配置 / 入口 / 共享 helper）、在模板中修正输出样板、在脚本中加机械校验，或在 `SKILL.md` 中修正入口拓扑与合同说明。
- 只有满足以下条件，才算“增强闭环完成”：问题已修复 + 已定位并修复最高杠杆源层工件 + 至少一个可复用的源层预防机制已落地 + 相关文档/合同已同步更新 + 引用同步范围已扫描或说明 + 已运行相应审计 / dry-run / smoke 验证，或明确报告验证阻塞。
- 如果增强被权限、外部依赖或范围限制阻塞，必须显式报告阻塞项与临时防护措施。

### 多成员协作技能的源层联动（强制）

- 当目标技能由多成员、团队顾问、外部 provider 或协作角色创建、升格或长期治理时，源层诊断不得只停在父 `SKILL.md`。
- 对这类多成员协作 skill，分层上溯除父 `SKILL.md` / `CONTEXT.md` 外，还必须按需联查：
  - 父 skill 显式回链的 `team.md`
  - 相关 agent rule docs（例如 `.codex/agents/<skill-slug>/**/*.md`）
  - 受治理子路径或子技能的局部 `SKILL.md` / `CONTEXT.md`
  - 与该 roster 绑定的 handoff schema、shared template、runbook、validator、route 配置
- 源层同步/修复遵循“只联动受影响关联面”原则：
  - 父 skill 总合同变更时，同步检查其引用的 `team.md`、agent docs、子路径合同是否仍一致
  - 某协作成员 / team 合同变更时，同步检查父 skill 的 topology / handoff / synthesis / audit 描述是否仍准确
  - 不得因为某个子角色局部变更而无差别重写整个 roster；也不得只修局部 agent doc 而放任父层合同失真
- 真源边界默认如下：
  - 父 `SKILL.md` 持有 topology、dispatch、handoff、synthesis、audit 与 canonical writeback 的总合同
  - `team.md` 持有 team 级 roster、默认调用关系与 team 内共享 handoff 约定
  - 单个 agent rule doc 持有该角色的局部任务边界、I/O、veto、证据与越权约束
  - 子路径本地 `SKILL.md` / `CONTEXT.md` 持有局部执行合同与局部经验层
- 若关联协作成员或子路径合同未同步修复，则不得宣称源层闭环完成；如暂无法同步，必须报告缺口、影响面与临时护栏。

### 根因学习回路自动化（强制）

该学习回路有两个方向，负向与正向都必须执行。

**负向触发**：当出现以下任一情况时自动触发：用户报告问题、用户指出源层治理/同步/优化未自动发生、运行失败、任务实践/测试阻塞（包括 `SKILL` 执行、dry-run 与 `pytest` 回归）、失败后返工、或用户明确要求修正。

- 无需额外等待用户提示，必须自动执行以下流程：
  1. 源层诊断（分层上溯）：从症状追到运行产物、直接原因、`Rule Source` 与 `Meta Rule Source`（`AGENTS.md` / meta-SKILL），同时检查当前任务实际读取或执行的规则、模板、runbook、registry、routes、agent doc 与脚本是否存在合同错位。
  2. 立即修复 + 增强：优先修补最高杠杆的源层工件（规则 / 脚本 / runbook / validator / registry / routes / agent doc / meta-rule），增加至少一项可复用的加固机制，然后再恢复下游执行；如仍有必要，再补本地产物。
  3. 上下文沉淀：更新受影响技能的 `CONTEXT.md`（若缺失则创建）；优先把结论化经验写入 Type Map / Playbook / Reusable Heuristics，若需保留里程碑细节，则外置到 `CHANGELOG.md` 或 `reports/`。
  4. 引用同步与验证：若发生重命名、拆分、迁移或真源落点调整，必须扫描并同步直接引用该工件的 `SKILL.md`、`CONTEXT.md`、`README.md`、`CHANGELOG.md`、脚本、模板、registry、routes、runbook、markdown 链接和项目内引用；随后运行对应审计、脚本 dry-run 或 smoke 验证。
  5. 预防晋升（自下而上）：将已验证的修复从本地产物 -> `CONTEXT.md` -> `SKILL.md` / runbook / validator -> `AGENTS.md` 或 meta-SKILL 逐级晋升；若已观察到跨技能复发，则必须继续向上晋升。
  6. 面向用户的闭环输出：必须返回 `root cause location + immediate fix + systemic prevention fix + validation`，并附上分层追踪路径 `symptom -> rule source -> meta rule source -> synced artifacts`。

**正向触发**：当出现以下任一情况时自动触发：用户明确认可某输出（例如“这个很好”“以后按这个来”）、某设计决策在跨项目场景中被复用且无需重新推导、或输出质量明显超过预期基线。

- 无需额外等待用户提示，必须自动执行以下流程：
  1. 模式识别：定位产出正向结果的设计决策，例如 prompt 结构、参数选择、工作流顺序、字段映射或架构安排。
  2. 抽象：将该决策提炼为 1-3 句可复用 heuristic，且要限定适用范围（skill、阶段、领域、主题），避免过度泛化。
  3. 上下文沉淀：将 heuristic 写入对应技能的 `CONTEXT.md` 中的 Reusable Heuristics；若需要保留里程碑级证据，只保留结论摘要在知识库章节中，长材料外置到 `CHANGELOG.md` 或 `reports/`。
  4. 晋升（自下而上）：当同一正向模式在 >= 2 次独立执行中得到确认时，将其从 `CONTEXT.md` 晋升到对应 `SKILL.md`、runbook、validator 或其他已存在的规范真源；若已成为跨技能治理模式，再晋升到 `AGENTS.md` 或 meta-SKILL。
  5. 面向用户的闭环输出：返回三元组：成功模式位置 + 提炼出的 heuristic + 晋升范围。
- 若需要保留里程碑级证据，`CONTEXT.md` 仅保留结论化沉淀；详细字段、时间线与长证据材料应写入 `CHANGELOG.md`、执行报告或 `reports/`。
- 如果只是修复了本地产物或确认了结果，却没有同步更新 `CONTEXT.md`，则视为 `Root-Cause Learning Loop` 尚未完成；若因阻塞无法更新，必须显式报告阻塞原因。

### 源层工件放置矩阵（全局真源）

- 以下内容应写入 `AGENTS.md` / meta-SKILL（规范型元合同）：

  - 跨技能的根因上溯顺序（`Rule Source -> Meta Rule Source`）
  - 从本地修复晋升到全局规则的条件
  - 仓库级硬门槛、闭环格式与防回归要求
  - 仓库级多因素决策方法，包括层级角色、覆盖规则与回退原则
  - 字段中心 thought-pass 系统的规范标识符与必填表头
- 以下内容应写入具体 agent 规则文档（例如 `.codex/agents/**/*.md`）作为源层规范合同：

  - agent 的人格边界、任务范围、输出 schema、路径约定、字段落点、审查合同与面向用户的硬门槛
  - 对多成员协作 skill，`team.md` 承载 team 级 roster / topology / handoff 共识，具体 agent doc 承载角色级合同；二者不得与父 `SKILL.md` 形成平行第二真相
  - 如果某 agent 没有独立 `CONTEXT.md`，则稳定的规范增强可以直接写进 agent 规则文档本身
  - 这种 agent 级直接优化仅限于规范内容：规则、schema、优先级、失败闭环、路由与输出合同
  - 经验性内容不得直接倾倒进 agent 规则文档，例如单次案例、噪声实验、临时 heuristic 与里程碑证据，应保留在 `reports/`、技能 `CONTEXT.md` 或其他经验层载体中，待验证后再晋升
  - 晋升规则：重复、多轮、高置信度的 agent heuristic，可在足够稳定后从经验层载体晋升回 agent 规则文档
- 以下内容应写入 `SKILL.md`（规范合同）：

  - frontmatter、触发条件、适用/不适用场景、Mode Selection、强制工作流、硬门槛与完成标准
  - 源层诊断顺序与修复顺序（包括上溯到 meta 合同的钩子）
  - 面向用户的标准闭环格式（根因位置 + 立即修复 + 系统预防修复）
  - 从经验到规范的晋升规则（何时可将重复模式提升为规范）
  - 当技能存在复杂选择逻辑时，定义领域专属的一层/二层/三层决策信号、tie-break 规则与显式覆盖条件
  - skill 自己的 `field_id` 主定义，以及 `step_id -> field_id` 和 `field_id -> quality_dimension -> fail_code -> rework_entry` 映射
- 以下内容应写入卫星技能 `SKILL.md`（同根旁路执行合同）：

  - 卫星职责、触发条件、与主链/主技能的 `stage_position`
  - `owned truth`、`not-owned truth`、共享载体依赖与回接路径
  - 是否参与 tracked workflow、是否允许直接调用、以及完成后回到哪个主技能或阶段
  - 不得把卫星技能写成主技能缩略版，也不得把它伪装成普通说明文件
- 以下内容应写入 `CONTEXT.md`（经验层）：

  - Type Map（失败模式 -> 修复策略 -> 验证点）、Repair Playbook 与 Reusable Heuristics
  - 运行陷阱、兼容性问题、成功恢复策略
  - 多因素选择任务中的经验性 tie-break heuristic、收窄 heuristic 与观察到的失败模式
  - 对类型化处理的经验性复盘、失败模式、修复策略与验证点；但不承载同一技能的规范型多模式策略主表
  - 尚未稳定到足以晋升为 `SKILL.md` 的候选经验
  - 若某次里程碑事件需要保留额外证据，`CONTEXT.md` 仅保留结论化摘要，长材料外置到 `CHANGELOG.md` 或 `reports/`
- 以下内容应写入项目级 `MEMORY.md`（项目记忆层）：

  - 用户明确要求长期保留的创作偏好、风格口味、叙事习惯、角色关系偏好、视觉/声音/氛围倾向
  - 当前项目需长期保留的特殊元素、固定母题、反复强调的钩子、明确禁区与长期执行要求
  - 会影响后续多个阶段判断的项目级协作约定，例如“这个项目不要鸡汤式收束”“感情线始终克制表达”“视觉上固定保留雨夜霓虹”之类的长期口径
  - 对既有项目记忆的更新、替换与撤销结论
  - 不得写入技能调试经验、源层故障复盘、跨项目 heuristic、一次性任务说明或迁移时间线
- 以下内容应写入 `CHANGELOG.md`（派生变更史）：

  - 按时间顺序组织的变更摘要、迁移记录、结构重排说明、长段执行时间线与版本差异
  - `CHANGELOG.md` 是派生说明载体，不是规范真源，也不是经验真源；不得与 `AGENTS.md` / `SKILL.md` / `CONTEXT.md` 并列竞争事实裁决权
  - `CHANGELOG.md` 默认不参与技能运行时预加载；只有在追溯迁移、审计差异、发布说明或需要查看详细过程时才按需读取
  - 若某条经验需要保留较长过程材料，`CONTEXT.md` 只保留结论化沉淀，并链接指向 `CHANGELOG.md` 或 `reports/`
- `CONTEXT.md` 支持主技能、子技能与卫星技能多级放置；角色定义、canonical 路径与加载顺序以“技能组成与语义”及“`SKILL` 调用上下文加载合同”两节为准，本矩阵不再重复展开。
- 子技能或卫星技能一旦长期维护并拥有局部职责，应在父级合同声明的路径上显式暴露 `SKILL.md + CONTEXT.md`；跨子技能、跨卫星或跨技能的 heuristic，再回晋升到主技能根层 `CONTEXT.md` 或 `SKILL.md`。
- 冲突优先级沿用上文“运行时加载顺序与优先级”第 8 条；后续章节只声明增量，不再平行重写完整优先级链。

### Agent 源层优化合同（强制）

- Agent 规则文档是第一类源层工件，而不只是人格包装。
- 对多成员协作 skill，agent 源层优化至少联查三处回指：父 skill 的 topology / handoff / synthesis 说明、`team.md` 的 team 级调用规则、agent doc 的局部边界与输出合同。
- 若 agent 或父 skill 的当前执行依赖 decision table、handoff node spec、validator、registry、routes、runbook 或其他具体源层工件，源层优化必须把实际依赖载体纳入联查与修复范围，不得只停留在 agent 主文档正文。
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
- 真源设计应回答以下问题：
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
- 最小已落地真源载体（详细运行方式与现状判断见 `HARNESS.md`）：
  - 共享治理合同：`.codex/templates/harness/office-governance-contract.md`
  - 三省角色合同：`.codex/agents/harness治理/中书省.md`、`.codex/agents/harness治理/门下省.md`、`.codex/agents/harness治理/尚书省.md`
  - 注册与路由真源：`.codex/registry/skills.yaml`、`.codex/registry/routes.yaml`
  - 生命周期真源：`.codex/runbooks/task-lifecycle.md`
  - 任务工件真源：`.codex/templates/harness/{mandate, mission-brief, route-plan, preflight-verdict, validation-report, learning-record}`
  - 运行时控制面：`projects/aigc/<项目名>/` 为 `aigc` 项目工作流唯一真源，`.codex/state/tasks/<task_id>/` 为通用任务状态面或治理镜像
  - 审计与评测入口：`scripts/aigc_harness_audit.py`、`scripts/aigc_skill_audit.py`、`.codex/evals/`
- 硬门槛（P0）：
  - 复杂任务不得跳过 `mission-brief` 与 `route-plan`
  - 高风险任务不得跳过 `preflight-verdict`
  - tracked harness 任务、复杂任务与高风险任务应产出 `validation-report` 后再宣布完成
  - 普通问答、状态查询、窄范围审查或小修复可使用面向用户的 inline validation 摘要，不强制创建 harness 报告
  - 非平凡失败应提供 `Symptom -> Direct Cause -> Rule Source -> Meta Rule Source` 后再结案
- 防漂移规则（P0）：
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

- 根目录 `HARNESS.md` 是本仓库 HARNESS 工程的总览型派生文档，不是新的第一真源。
- `HARNESS.md` 的定位、维护合同、变更同步范围与更新要求，以 `HARNESS.md` 自身”更新维护合同”章节为准。
- 当 AGENTS.md 本节（Harness 工程）的内容发生调整时，必须在同一轮任务内同步检查并更新 `HARNESS.md`。
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
- `bootstrap_compat` 模式的退出必须满足以下全部量化条件，缺一不可：
  - 所有 `active` stage 的父合同已通过当前启用的审计入口或人工复核，不存在未说明的降级项
  - `6-Video` 内部子路径已收束且 provider 级执行面已注册到 `skills.yaml` 与 `routes.yaml`
  - `7-Cut` 已明确激活并完成当前阶段合同基线，或已显式归档并在 registry/routes 中标记为 `shelved + archived`
  - 整树审计或复核不存在仅父合同通过却伪装整树全绿的情况
  - 三省 agent doc 中引用的 `aigc` 路径、阶段名与 registry 条目全部与 `skills.yaml` / `routes.yaml` 一致
  - `HARNESS.md` 已同步更新为退出后状态，不再引用 `bootstrap_compat` 兼容口径
- 退出 `bootstrap_compat` 模式时，必须在 `HARNESS.md` 的"现状判断"中显式记录退出日期、满足的条件清单与残留风险。

---

## 术语表（Glossary）

本文档中使用的核心术语快速索引。详细定义请参阅对应章节。

### 核心概念

| 术语 | 定义 | 详细位置 |
| ---- | ---- | -------- |
| **真源（Canonical Source）** | 单一权威的事实来源；任何共享规则、结构、schema、模板或路由合同只允许有一个真源，其他载体为派生投影 | "真源治理合同"章节 |
| **运行时脊柱（Runtime-Spine）** | SKILL.md 作为单次任务执行主脊柱，必须包含入口、类型路由、思行节点、模块授权、输出合同与回写的完整链路 | "Skill 2.0 Runtime-Spine 基线"章节 |
| **bootstrap_compat** | 重大结构改造期间的兼容模式；保留 harness 真源骨架，放松对阶段内部细节的绑定强度 | "AIGC 改造兼容模式"章节 |
| **根因上溯（Root-Cause Tracing）** | 从症状逐层向上追查到治理该行为的最高层规则源 | "根因优先"章节 |
| **经验晋升（Experience Graduation）** | 将经验层（CONTEXT.md）中的稳定模式逐级晋升到规范层（SKILL.md / AGENTS.md） | "根因学习回路自动化"章节 |

### 技能层级

| 术语 | 定义 | 详细位置 |
| ---- | ---- | -------- |
| **主技能（Main Skill）** | 拥有业务域或阶段链的总入口、总路由、共享载体边界与真源裁决权 | "技能组成与语义"章节 |
| **子技能（Sub-Skill）** | 受治理的可执行下钻单元，经父级路由进入，负责局部执行合同 | "技能组成与语义"章节 |
| **卫星技能（Satellite Skill）** | 与主技能同根同级的旁路可执行技能；服务查询、恢复、复核等辅助职责 | "技能组成与语义"章节 |
| **父级导引技能（Parent Guide Skill）** | 只负责路由、边界、聚合、回接和门禁的轻量形态，不吞并子技能的业务真源 | "技能组成与语义"章节 |

### 合同类型

| 术语 | 定义 | 详细位置 |
| ---- | ---- | -------- |
| **规范合同（Normative Contract）** | 写在 SKILL.md / AGENTS.md 中的强制执行规则，不可绕过 | "规则分级"章节 |
| **经验层（Experience Layer）** | 写在 CONTEXT.md 中的可复用知识库，包括 Type Map、Repair Playbook、Reusable Heuristics | "CONTEXT 知识库模式"章节 |
| **项目记忆层（Project Memory）** | 写在项目根 MEMORY.md 中的跨阶段持续生效的偏好、口味与长期要求 | "项目级记忆与上下文规则"章节 |

### 治理工件

| 术语 | 定义 | 详细位置 |
| ---- | ---- | -------- |
| **三省六部制** | 本仓库的编排治理架构：宪章层（AGENTS.md）+ 三省治理层（中书/门下/尚书）+ 六部能力层（吏户礼兵刑工） | "三省六部制编排治理基线"章节 |
| **Harness** | 任务编排与治理的运行时控制面，包括共享治理合同、工件模板、审计入口 | "Harness 工程"章节 |
| **Mission Brief** | 复杂任务的标准化任务简报，包含背景、目标、约束与验收标准 | "三省六部制编排治理基线"章节 |
| **Route Plan** | 任务路由计划，定义技能调度顺序与回接策略 | "三省六部制编排治理基线"章节 |
| **Preflight Verdict** | 高风险任务执行前的预检裁决 | "三省六部制编排治理基线"章节 |
| **Validation Report** | 任务完成后的验证报告，确认输出符合预期 | "三省六部制编排治理基线"章节 |

### 规则分级（Glossary）

| 术语 | 定义 | 详细位置 |
| ---- | ---- | -------- |
| **P0-硬门槛** | 不可绕过、不可降级的强制规则；违反时必须暂停执行并修复 | "规则分级"章节 |
| **P1-默认规则** | 默认遵守，用户可显式覆盖的规则；违反时应报告偏离理由 | "规则分级"章节 |
| **P2-最佳实践** | 应遵守但不阻断执行的建议性规则 | "规则分级"章节 |
| **P0 Tie-Break** | 当两条 P0 规则冲突时的裁决协议，按安全 > 用户指令 > 真源 > 根因 > 兜底的顺序裁决 | "P0 规则冲突 Tie-Break 协议"章节 |

### 缩写对照

| 缩写 | 全称 |
| ---- | ---- |
| LLM-first | 以 LLM 作为核心创作环节的第一执行者 |
| runtime-spine | 运行时脊柱（SKILL.md 的核心执行链路） |
| Type Routing Matrix | 类型路由矩阵（定义输入类型到执行路径的映射） |
| Module Loading Matrix | 模块加载矩阵（定义哪些可选模块被授权参与执行） |
| sidecar | 辅助工件（承载过程稿、思维链等非业务真源内容） |
| canonical truth / canonical creative truth | 权威事实真相（单一真源的业务结论） |
| dry-run | 空运行（不产生实际副作用的演练） |
| smoke test | 冒烟测试（快速验证基本功能可用） |
