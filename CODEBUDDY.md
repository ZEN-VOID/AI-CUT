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
3. 根 `AGENTS.md`
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

- `SKILL.md` 是规范合同，负责入口、路由、授权模块、门禁、输出合同与学习回写；不得退化为目录导航或经验笔记。
- `CONTEXT.md` 是经验层，保存可复用 heuristic、失败模式和修复策略；不得重定义 `SKILL.md` 的规范合同。
- `MEMORY.md` 是项目记忆层，只保存当前项目跨阶段持续生效的偏好、禁区与长期要求；不得写入技能调试经验或一次性任务说明。
- 主技能拥有业务域或阶段链的总入口和真源裁决权；子技能经父级路由进入并回流局部 patch；卫星技能承担查询、恢复、复核、桥接等旁路职责，默认不并入主链聚合。
- 每次命中任意 skill 时，必须成对加载同目录 `SKILL.md + CONTEXT.md`；若绑定 `projects/story/<项目名>/` 或 `projects/aigc/<项目名>/`，还必须加载项目根 `MEMORY.md` 和相关 `CONTEXT/`。
- `references/`、`review/`、`types/`、`templates/`、`scripts/`、`guardrails/`、`assets/`、`steps/`、`knowledge-base/` 只有在当前 `SKILL.md` 显式授权时才参与执行。
- `CHANGELOG.md`、执行报告和迁移记录默认不预加载，仅在追溯变更、审计差异或查看过程证据时按需读取。
- 新经验优先写入最窄有效作用域的 `CONTEXT.md`；稳定、重复、高置信度的规则再晋升到对应 `SKILL.md`、runbook、validator 或根层规则。
- 用户对项目提出“记住”“以后都按这个来”或替换/撤销长期偏好时，必须同轮更新对应项目根 `MEMORY.md`。
- 用户对 `projects/aigc/<项目名>/` 或 `projects/story/<项目名>/` 发出清空、移除或等价删除指令时，必须同步检查并修正当前项目内相关状态、进度、manifest 或索引残留。

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

- 每份 `CONTEXT.md` 应包含 `Context Health`；默认阈值为 `soft_limit_chars: 20000`、`hard_limit_chars: 40000`。
- 达到 `warn` 时做定向压缩与结构整理；达到 `critical` 时，在继续大规模追加前必须归档或压缩旧内容。
- 压缩时保留高复用结论，长时间线和过程材料外置到 `reports/context-archive/`、`CHANGELOG.md` 或其他可追踪载体。
- 默认只处理当前技能上下文，不在未被要求时全仓重写。

### CONTEXT 知识库模式（强制）

- `CONTEXT.md` 默认是知识库，不是时间日志；优先维护 Type Map、Repair Playbook 与 Reusable Heuristics。
- 详细时间线、长日志、迁移流水、版本差异和里程碑证据应外置到 `CHANGELOG.md`、执行报告或 `reports/`。
- 禁止把进度叙述、低复用噪声、未经整理的迁移流水或一次性表面修改写入 `CONTEXT.md`。

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

### 源层工件放置原则（全局真源）

- 规范型元合同写入 `AGENTS.md` 或 meta-SKILL；技能运行合同写入对应 `SKILL.md`；经验写入 `CONTEXT.md`；项目长期偏好写入项目根 `MEMORY.md`；时间序变更写入 `CHANGELOG.md` 或 `reports/`。
- 多成员协作规则的总拓扑由父 `SKILL.md` 持有；`team.md` 持有 roster / handoff 共识；单个 agent doc 持有角色级边界与输出合同。
- 稳定规则可自下而上晋升，但不得把经验、日志或一次性案例直接倾倒进规范文档。
- 发生迁移、拆分、重命名或真源调整时，必须同步直接引用并运行可行验证。

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

- 根目录 `HARNESS.md` 是本仓库 HARNESS 工程的总览型派生文档，不是新的第一真源。
- `HARNESS.md` 的定位、维护合同、变更同步范围与更新要求，以 `HARNESS.md` 自身”更新维护合同”章节为准。
- 当 `AGENTS.md` 的 Harness 相关口径调整时，必须同步检查并更新 `HARNESS.md`；如无法同步，必须报告缺口、原因与临时护栏。
- AIGC 改造、`bootstrap_compat`、registry/routes/runbook/audit 等 Harness 细节以 `HARNESS.md` 及其声明真源为准，根文件不重复维护操作手册。
