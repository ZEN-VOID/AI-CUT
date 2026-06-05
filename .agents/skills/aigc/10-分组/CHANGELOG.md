# CHANGELOG

## 2026-06-05 (14.5s Boundary Hard Cap)

- 将分镜组目标时长调整为约 14.5 秒；通常 10-14.5 秒可接受，14.5 秒为硬上限。
- 保留最终累计结束秒 `.5` 收束规则：自然累计不以 `.5` 结尾时只允许上调到不超过 14.5 秒；超过 14.5 秒必须重裁或回退 source owner。
- 同步 `SKILL.md`、boundary、review、CONTEXT、README、模板、入口元数据、类型映射、知识库、脚本说明、validator 和 test prompts。

## 2026-06-05 (Remove Character Hard Limit)

- 移除分镜组字数硬上限；字数高低只作为语义复核信号，不再作为 validator error 或正式 pass 阻断项。
- 保留约 1680 字参考线和低于 850 字复核提示，用于报告解释密度风险；不得为了压低字数切断 atomic unit、改写上游正文或覆盖分镜总时长判断。
- 同步 boundary、statistics、north-star projection、review、CONTEXT、knowledge-base 与 validator。

## 2026-06-05 (Remove Visual Style Header From Template)

- 从分镜组输出结构中移除独立 `画面风格：` 组头行。
- 当前组头结构收束为：场景标题行 -> `全局风格：` -> 单行全局风格内容 -> 第一个普通时间码分镜行。
- 同步 `SKILL.md`、templates、README、review、CONTEXT、入口元数据、脚本说明、validator 与 test prompts；不新增 `画面风格：` 的负向完成门。

## 2026-06-05 (Single-Line Global Style)

- 将每组 `全局风格：` 输出从三行结构收束为单行结构：只保留固定前置词 + 当前组 `Global Style Prompt` 整理句，300 字以内。
- 移除 `Visual Slogan / Design Principle` 与 `Visual Gene Profile / Negative Traits` 两个独立输出行；这些字段不再作为 `全局风格：` 完成门槛。
- 同步 `SKILL.md`、north-star projection、statistics、boundary、review、templates、CONTEXT、type map、入口元数据、脚本说明、validator 与 test prompts。
- validator 现在要求 `全局风格：` 字段只有 1 行内容。

## 2026-06-05 (13s Boundary And Half-Second Close)

- 将分镜组目标时长从约 15 秒调整为约 13 秒；常规可接受带从 12-18 秒调整为 10-16 秒，硬上限从 18 秒调整为 16 秒。
- 新增最终累计结束秒 `.5` 收束规则：每个分镜组最终结束秒必须以 `.5` 结尾；自然相加已为 `.5` 时保留，否则在组尾上调 0.5 秒；YAML `时长估算` 回指该最终结束秒。
- 同步 `SKILL.md`、`references/group-boundary-contract.md`、`references/statistics-yaml-contract.md`、`review/review-contract.md`、`types/grouping-type-map.md`、`CONTEXT.md`、README、模板、入口元数据、脚本说明与 validator。
- validator 现在将 `>16s`、最终结束秒未以 `.5` 结尾、YAML `时长估算` 未以 `.5` 结尾或未匹配最终结束秒视为 error。

## 2026-06-04 (Runtime Spine And Lighting Source Upgrade)

- 将 `10-分组` 升级为 Skill 2.0 runtime-spine 主合同：补齐 Business Requirement、Type Routing、Thinking-Action Node Map、Module Loading / Trigger、Convergence、Review Gate、Quantifiable Criteria、Attention、Checkpoint、Evaluation Prompt 与 Learning Writeback。
- 默认上游从旧分组/摄影路径收束为 `projects/aigc/<项目名>/9-光影/第N集.md` 光影稿；用户显式指定其他文稿时优先 source override，并在报告中声明 skipped light-specific checks。
- 删除 `steps/grouping-workflow.md`，节点真源回收到 `SKILL.md`；补充 `test-prompts.json` 作为回归评估资产。
- 同步模板、README、类型包、references、review、入口元数据、validator 和根路由/registry 中的旧 `5-分组` 引用到 `10-分组`。

## 2026-06-01 (Direct Screenplay Intake)

- 新增 `source_state=direct_screenplay` 源层规则：当用户要求 `10-分组` 直接接手剧本/编导稿，或项目缺少 `9-光影` 但存在可读剧本源时，不再阻断到 `9-光影`。
- 明确 direct screenplay 路径由 LLM 按剧本声画 atomic unit 自动规划约 15 秒/组，补写连续 `[N-N秒]` 时间码、组级 `画面风格：`、首帧衔接和 YAML 统计；脚本仍只做机械校验。
- 要求 frontmatter 与执行报告声明剧本源路径、`source_state=direct_screenplay`、时间码由本阶段规划，以及 `9-光影` 字段级 diff 不适用。
- 同步 `SKILL.md`、`types/grouping-type-map.md`、`references/group-boundary-contract.md`、`steps/grouping-workflow.md`、`review/review-contract.md`、`CONTEXT.md` 与 `README.md`。

## 2026-06-01 (Hulong Frame Terminology)

- 将“回龙帧”定义为首帧衔接的内部执行口径：下一分镜组第一个普通 `[0-N秒]` 分镜行完整代入上一组结尾状态画面点内容，再通过景别和镜头视角调整进入本组开始画面。
- 明确回龙帧不是输出字段、独立连接件、上一组完整画面块复制或完整原画面性字段复制；新产物不得输出 `回龙帧：`、来源说明或规则说明。
- 补充声音承托规则：若回龙锚点来自对白画面、独白画面、旁白画面或音效画面，必须同步带入对应声音内容，避免声画承托断裂。
- 同步 `SKILL.md`、boundary、workflow、review、模板、README、入口元数据、经验层、类型包、脚本说明与 validator。

## 2026-06-01 (Inherited Visual Field Titles)

- 将 `10-分组` 的正文继承口径同步为直接保留 `9-光影` 的原画面性字段标题，不再把画面字段替换或包裹为 `分镜画面：`。
- 强化组内时间码规则：每个分镜组内部从 `[0-N秒]` 开始后连续累加，后续原画面性字段下的时间段不得各自从 0 重启。
- 同步 `SKILL.md`、boundary / visual-tone / statistics / north-star references、workflow、review、模板、README、入口元数据、经验层、类型包、脚本说明与 validator。

## 2026-06-01 (First Storyboard Line Continuity Schema)

- 移除 `增补首帧：` 作为输出字段的规则；首帧衔接只作为内部裁决，落盘时直接内化为每组第一个普通 `[0-N秒]` 分镜行。
- 第二组起仍回看上一组最后分镜的主体、动作、道具、空间关系、光线和已成立状态，但输出不写特殊字段、来源说明或规则说明。
- validator 将 `增补首帧：` 作为禁用旧字段检查；YAML `字数统计` 改为计入场景标题行、`画面风格：` 和普通分镜正文。
- 同步 `SKILL.md`、workflow、review、模板、references、README、入口元数据、经验层、类型包、脚本说明与 validator。

## 2026-06-01 (Global Style And Supplemental First Frame Schema)

- 移除新产物中的 `入场镜头：` 与 `出场画面：` 字段机制，旧字段只作为禁用项保留在 validator / review 里。
- 移除独立 `## A~B` 组间连接件设计；相邻组承接先改由下一组补帧承担，随后在同日新 schema 中收束为第一个普通 `[0-N秒]` 分镜行。
- 将 north_star 投影改为显式字段 `全局风格：`，固定放在每组的场景标题行下方；字段内三行分别为固定前置词 + 300 字以内当前证据风格整理句、类型元素提示词、细分画面风格。
- 将 `画面属性：` 改为 `画面风格：`，并固定移动到第一个 `分镜画面：` 上方。
- 移除新产物中的 `画面构图：` 与左/中/右/前景/中景/背景位置细节字段；validator / review 将其作为禁用残留检查。
- 新增组内累计时间码规则：分组后原分散 `分镜画面：` 的 `[起始秒-结束秒]` 必须改写为当前分镜组基准下连续递增的 `[N-N秒]`，YAML `时长估算` 取最后结束秒。
- 当时新增过独立线头帧规则；该规则已在同日后续 schema 中改为首帧衔接内化，不再作为输出字段。
- 同步 `SKILL.md`、north-star / visual-tone / statistics / boundary references、workflow、review、模板、README、入口元数据、经验层、类型包、脚本说明与 validator。

## 2026-06-01 (Storyboard Block Duration Parsing)

- 将 `时长估算` 解析从所有 `[起始秒-结束秒]` 差值相加，修正为每个 `分镜画面：` 块取最后一个时间段的结束秒作为该画面总时长，组内连续画面块相加。
- 更新 validator 只统计 `分镜画面：` 块内时间码，避免入场镜头、出场画面、说明字段或其他文本中的时间示例污染组时长；legacy `分镜N（约X秒）` 仍作为旧式时长错误处理。
- 同步 boundary、statistics、review、workflow、types、template、README、经验层与入口元数据的时长口径。

## 2026-06-01 (Time Range Duration Alignment)

- 将分组边界与 YAML `时长估算` 的主口径从旧 `分镜N（约X秒）` 累计同步为 `分镜画面：` 下 `[起始秒-结束秒]` 时间段。
- 同步入口合同、boundary/statistics/entry/exit/north-star/review/workflow/type/template/validator 口径；legacy 旧式时长不再计入 canonical 分组时长，validator 会要求回到 `9-光影` 迁移。

## 2026-06-01 (Init-Only Team Synthesis)

- 接入冻结初始化综合消费：读取 `team.yaml.init_synthesis.stage_seed_summary."10-分组"`、`init_handoff.grouping_seed` 与 `north_star.yaml.创作阶段不变量.分组`，形成 `init_team_synthesis_context`。
- 明确分组阶段不调用 team 身份、不解析旧 stage profile、不补造创作阶段顾问问答；初始化综合只影响分组节奏、桥接策略和 north star 投影提示。
- 同步 SKILL、workflow、review、模板、README 和 `agents/openai.yaml`。

## 2026-06-01

- 恢复组内 `出场画面：` 尾钩字段：每组原正文之后、YAML 之前必须记录本组最后一个原始分镜/末帧/尾帧的主体末态、空间关系、动作余势、镜头/观看位置和承接锚点。
- 同步新版 `入场镜头：` 规则：第二组及之后优先承接上一组 `出场画面：`，并结合上一组尾帧、连接件抵达首态和本组首帧校正，避免把入场镜头写成静态定场或无证据重置。
- 调整组间连接件边界：连接件消费上一组 `出场画面：` 与下一组 `入场镜头：`，但块内不重复输出组内 `出场画面：` 字段；旧 `入场画面：` 仍禁用。
- 同步 `SKILL.md`、entry/exit/bridge/statistics/boundary references、workflow、review、模板、入口元数据、经验层、类型包、脚本说明与 validator；`出场画面：` 计入 `字数统计` 和正文风险口径，但不计入 `时长估算`。

## 2026-05-30

- 将分镜组开头字段从 `定场镜头：` 同步调整为 `入场镜头：`，并更新主合同、reference、workflow、review、模板、入口元数据、经验层、脚本说明和 validator 的字段口径。
- 将 `入场镜头：` 从字段名升级为“进入方式账本”：必须说明入口源、入场触发、镜头/观看位置、主体入画状态和动态关系变化；场景/环境信息只作为入场路径上下文，不再沿用旧式静态场景说明。
- 将入场镜头 reference 迁移为 `group-entry-shot-contract.md`，同步 `entry_shot_review`、`N5A-ENTRY-SHOT`、validator 命名和报告口径。
- 强化构图分区规则：位置关系不得写成静态站位清单，必须体现动作相位、距离变化、遮挡变化、视线转移、朝向变化或上一组尾帧延续到本组首态的动态关系。
- 强化 north_star 场景化投影规则：新增 `Style Signature Retention Rule`，要求第 1 行全局风格整理句在不完整照抄母稿的前提下保留作品级风格签名、当前组场景适配锚点、材质/摄影锚点和必要边界锚点，避免被压缩成局部物件或普通光影描述。
- 同步 `SKILL.md`、`references/north-star-projection-contract.md`、`review/review-contract.md` 与 `CONTEXT.md`，将“全局风格强度不足”纳入 `FAIL-GROUP-02` 的源层修复范围。

## 2026-05-26

- 将构图分区从“至少两个有内容”升级为硬门槛：必须按固定顺序完整输出 `左侧：`、`中间：`、`右侧：`、`前景：`、`中景：`、`背景：` 六字段，且每字段必须展示具体可见主体、环境锚点、遮挡、光影材质或空场压力，不得使用泛化占位句。
- 同步 `group-entry-shot-contract.md`、`SKILL.md`、workflow、review、模板、入口元数据、经验层、脚本说明与 validator；validator 现在机械检查六字段完整性、固定顺序和明显泛化内容。
- 将 `north_star` 风格投影升级为当前组风格整理：第 1 行不再完整照抄 `全局风格.全局风格提示词`，而是以全局风格母稿为总体，根据当前分镜组或连接件的场景类型、光影、色彩、材质、动作和摄影证据抽取匹配部分，整理为 300 字以内自然语句。
- 同步当时的 projection / bridge / workflow / review / 模板、入口元数据、经验层、类型包、脚本说明与 validator；validator 现在机械检查固定前置词后全局风格整理句不超过 300 字。
- 进一步升级 `入场镜头：` 为构图分区主体账本：必须在场景/环境身份中包含氛围、光影、色彩，并新增 `画面构图：` 与左/中/右、前景/中景/背景等分区，把主体准确布置在画面结构中。
- 在 workflow 中新增 `N5E-SUBJECT-EVIDENCE` 取证节点，从 `9-光影` 的画面、角色动作、镜头设计、分镜明细、对白主体和道具特写建立主体/空间/镜头证据表，再进入入场落盘。
- 明确 `画面构图：` 是主体站位账本，区别于后续 `画面属性：` 的摄影风格提炼；构图分区不得凭空创造上游没有的位置。
- 强化字数统计口径：场景标题行、入场镜头、画面构图、构图分区和画面属性计入 `字数统计`；组底 YAML fenced block 本身不计入 `字数统计`、`时长估算`、1680 目标上限或 1980 硬上限。
- 升级 `入场镜头：` 的主体信息承载口径：角色、群体、关键道具和场景锚点不再在组头另列 `角色：` / `场景：` / `道具：` 清单，而是自然融入入场镜头、画面构图和构图分区本身。
- 明确主体描述必须带必要形容属性、状态属性、站位属性、空间方位、朝向和注意力落点；复杂群像可按主位、左右对立位、阵营和关键道具焦点组织位置关系。
- 保留组底 YAML 作为 canonical 短名单统计和校验索引，不让 YAML 替代组头主体传达。
- 更新 validator 以兼容多行 `入场镜头：` 自然段，并机械检查 `画面构图：`、六个构图分区、尾帧锚点、字数和 YAML。

## 2026-05-24

- 升级 `入场镜头：` 组间连续性口径：第二组起不再要求固定句式 `承接上一组结束状态`，改为以上一组尾帧还原入场作为入口源，再承接完整站位关系。
- 明确尾帧还原入场必须具体复现上一组末帧可见状态，包括主体位置、姿态、朝向、视线、身体接触、道具关系、光线、烟雾、水纹、碎片、衣袍或发丝等仍在延续的状态。
- 明确跨组连续分镜序列感只能通过入场镜头和画面属性说明“同一尾帧状态换景别/机位/焦点/构图/观看距离进入”，不得改写 `9-光影` 原正文或原有 `分镜明细`。
- 同步 `SKILL.md`、入场镜头合同、workflow、review、模板、入口元数据、经验层、脚本说明与 validator；validator 现在检查第二组起是否含 `上一组末帧` / `上一组尾帧` / `上一组最后一帧` 等尾帧还原入场锚点。

## 2026-05-22

- 吸收“身份先于动作”的早期分组入场口径；该口径已在 2026-05-30 升级为入口源、入场触发、镜头/观看位置、主体入画和动态关系优先。
- 新增每组开头 `入场镜头：` 合同：每个分镜组在场景标题行后重新交代场景、全部角色站位、姿态、空间方位和朝向关系，同场景连续组也必须重复。
- 强化组间连续性：当时要求每集第二组起回顾上一组结束状态；该口径已在 2026-05-24 升级为具体尾帧还原入场，不再使用固定套话。
- 强化动作链牵引：`入场镜头：` 必须先承接人物姿态、身体接触、未完成动作、朝向和注意力落点，再写环境锚点；不得把示例中的场景、道具或动作硬编码为固定模板。
- 明确 `入场镜头：` 只服务空间起始状态，不添加无互动道具氛围镜头或道具互动事实，避免道具镜头打断人物动作衔接。
- 同步 `SKILL.md`、workflow、review、模板、统计口径、入口元数据、经验层与 validator；`入场镜头：` 计入 YAML `字数统计`，不计入 `时长估算`。

## 2026-05-13

- 新增分镜组与连接件开头场景标题行合同：每个分镜组标题后必须重复当前场景标题；连接件同场景重复同一标题，跨场景使用 `场景标题A ➡️ 场景标题B`。
- 明确计数口径：分镜组标题后的场景标题行计入 YAML `字数统计`，但不计入 `时长估算`；连接件自身场景标题行不反向计入任何分镜组统计。
- 同步 `SKILL.md`、bridge/statistics/boundary/projection/review/workflow、模板、入口元数据、经验层与 validator。

## 2026-05-07

- 将单个分镜组显式时长累计 `>18s` 从语义 warning / 可声明完整性例外，升级为硬性 error；`10-分组` 不再允许用同画面完整、对白承托、动作完成或场景完整性放行超 18 秒组。
- 若单个 atomic unit 自身超过 18 秒，新增回退口径：必须返回 `9-光影` 拆分画面单位、压缩镜头时值或重裁分镜数量后再重新分组。
- 同步更新 `SKILL.md`、`references/group-boundary-contract.md`、`review/review-contract.md`、`steps/grouping-workflow.md`、`CONTEXT.md`、模板、脚本说明与 validator；validator 现在对超 18 秒组直接报 error。

## 2026-05-06

- 将 15 秒/组的边界裁决从字数中心切换为显式时长累计中心：优先累计 `9-光影` 的 `分镜N（约X秒）` 接近 15 秒，允许约 12-18 秒弹性，不为精确卡点拆断同一画面。
- 字数与对白句数降级为辅助风险复核；新增 YAML `时长估算` 和 validator 显式时长累计检查，要求短组/长组进入语义复核并说明完整性例外。
- 调整全局风格固定前置词：要求生成现场物理互动音效、氛围感音效、环境声、自然现象声和动作声，同时明确禁止任何字幕与背景音乐；同步主合同、projection / bridge / review / workflow、模板、入口元数据、经验层与 validator。

## 2026-05-04

- 将组间连续性源层从旧版 `入场画面：` / `出场画面：` 尾钩机制升级为独立 `## 上一个分镜组ID~下一个分镜组ID`，默认 3-4 秒，基于第 N 组原尾帧与第 N+1 组原首帧生成同场景或跨场景缝纫补丁，并强制物理夹放在上下两个分镜组中间。
- 调整字数统计口径：1680 常规目标和 1980 硬上限只约束从 `9-光影` 划定的纯分镜剧本正文；组标题、north_star、YAML 与组间连接件均不计入。
- 同步 validator、模板、review、workflow、入口元数据和经验层：禁止旧入场/出场字段，新增连接件结构检查，并保留连接件创意与非尾钩判断为 LLM/人工语义 review。

## 2026-05-03

- 收紧分组字数源层：常规目标上限调整为约 1680 字，1980 字保留为硬上限；超过 1680 字必须做拆分复核并说明例外，避免下游视频生成依赖 0.85 倍速才显得自然。
- 修复分组验收口径：`scripts/validate_storyboard_groups.py` 改为必跑机械校验但不替代语义 PASS，执行报告必须记录 boundary / bridge / faithfulness / statistics evidence 四类语义 review。
- 统一分镜组 ID 输出为 `## x-y-z` 标题，移除 `[分镜组ID]` 文案造成的双真源。
- 将低于 850 字的短组从 validator error 调整为 warning，要求语义 review 判断短场景例外或回到完整 atomic unit 重组。
- 强化 YAML 统计证据复核：角色、场景、道具字段形状通过不等于统计准确，需能回指本组正文证据。

## 2026-05-01

- 收束分组阶段输出合同：移除旧的空间辅助输出链路和对应 validator 检查，分组阶段只保留边界裁决、north_star 投影、入场/出场补位、原文保真、YAML 统计与机械结构校验。
- 扩展全局风格固定前置词：加入“视频生成的画面风格，光影和氛围与场景参照图保持一致。”，并同步模板、projection contract、workflow、review gate、入口元数据、经验层与 validator。

## 2026-04-28

- 调整全局风格固定音频/字幕约束：从行尾追加改为第 1 行最前前置，并同步模板、review gate、workflow、入口元数据与 validator。
- 调整 `站位和位移：` 输出密度：连续多个分镜站位、位移、朝向和多角色顺位完全不变时，仅需首次固定；发生变化时再在对应分镜补入，避免每个分镜头重复。
- 强化多角色空间关系：`站位和位移：` 涉及多角色时必须明确前后、左右、内外、近远或动作先后的顺位关系。
- 收紧 `站位和位移：` 的空间逻辑合同：新增不输出的空间连续性账本，要求从本组入场状态、上一分镜状态、当前分镜证据、允许变化和本组出场状态连续推导，禁止为了造句新增无证据移动。
- 强化组间空间连续性：第 2 组起首条站位位移必须从本组入场画面接到首个原始分镜，防止角色瞬移、左右/内外倒置或镜头运动误写成角色位移，并同步 workflow、review、模板、入口元数据和经验层。
- 强化思维·执行节点图表化：在 `SKILL.md` 增补 PASS 级 Mermaid 判断图，在 `steps/grouping-workflow.md` 增补节点网络图、思维到执行产物图和失败返工回路图。
- 更新 north_star 投影合同：每组第 1 行全局风格必须包含固定音频/字幕约束，并同步模板、review gate、workflow、入口元数据与 validator 检查。
- 新增空间一致性合同：空间锚点作为内部参照系使用，不作为分镜组组头字段输出；在首次锁定及变化 `分镜N:` 补入 `站位和位移：` 辅助行，并同步模板、review gate、workflow、入口元数据与 validator 检查。
- 收紧 `站位和位移：` 归属层级：由分镜明细容器级改为分镜明细级，validator 检查分镜级首次锁定和非空辅助行。
- 收敛空间锚点输出：`空间锚点` 改为 `站位和位移：` 的内部参照系，不再作为分镜组组头字段或提示词独立段落输出；validator 改为禁止输出 `空间锚点：`。
- 收紧 `站位和位移：` 主语规则：必须使用明确角色名或上游已命名的稳定群体称谓，禁止 `画面主体`、`主体`、`人物`、`角色`、`主角` 和代词等模糊指代，并加入 validator 检查。

## 2026-04-25

- 初始化 `aigc/10-分组` Skill 2.0 包。
- 建立 `SKILL.md + CONTEXT.md`、动态引用分区、输出模板、产品入口元数据和机械 validator。
- 固化分组核心合同：`x-y-z` 分镜组 ID、north_star 三项直引、对白 4-6 句弹性上限、完整组构成 <= 1980 字、画面句子多分镜不可截断、入场/出场补位画面成对一致、组底 YAML 统计不计入字数。
- 根据 code-reviewer 顾问/审查者审计补强 validator：校验组正文真实场景号、禁止跨多场景、校验 YAML 字段类型和 `字数统计` 与非 YAML 估算字数的一致性。
- 修复 north_star 投影源层：三项来源改为 `全局风格.全局风格提示词 / 类型元素.类型元素提示词 / 细分风格.画面风格`，组头输出改为隐藏标题字段的三行纯内容，并让 validator 禁止旧 `[全局风格]` 等可见标题和中文括号。
- 修复首组入场空段源层：每集第 1 组直接省略 `入场画面：` 段，不再输出 `无`；第 2 组起继续要求入场画面等于上一组出场画面。
- 修复边界原则：取消“按情绪/话题/危险信息转折切组”的划组口径，改为字数密度、对白密度、atomic unit 完整性和桥接可行性共同裁决；validator 增加 850 字硬性复核地板。
