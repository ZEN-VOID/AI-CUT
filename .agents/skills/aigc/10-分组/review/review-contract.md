# Review Contract

本文件定义 `10-分组` 的质量门禁。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `global_style_review` | 每次阶段 PASS 前 | 检查每个分镜组是否在场景标题行下方立即输出 `全局风格：`；字段内是否只有一行内容；该行是否以固定前置词开头并接 300 字以内当前组 `Global Style Prompt` 全局风格整理句；是否没有输出 `Visual Slogan`、`Design Principle`、`Visual Gene Profile` 或 `Negative Traits` 独立行；是否没有完整照抄全局母稿或新增无证据风格 |
| `first_storyboard_continuity_review` | 每次阶段 PASS 前 | 检查每组第一个时间码分镜行是否是普通 `分镜N（0-N秒）：` 或 `[0-N秒]` 分镜描述；首组是否自然整理本组开始画面，第二组起是否以回龙帧口径完整代入上一组结尾状态画面点内容，并只通过景别、机位、镜头角度、焦距、观看距离或焦点路径调整进入本组；若回龙到对白画面、独白画面、旁白画面或音效画面，是否同步代入对应声音内容；是否没有 `分镜画面：`、`增补首帧：`、`回龙帧：`、来源说明、规则说明、模板化尾句或新增剧情事实 |
| `mechanical_check` | 每次落盘前或修复后 | 运行 `scripts/validate_storyboard_groups.py`，检查分镜组标题、场景标题行、`全局风格：`、旧字段、字数统计、分镜总时长、组内时间码连续累加、YAML、连接件块；warning 进入语义复核，不直接等于 PASS |
| `boundary_review` | 每次阶段 PASS 前 | 检查每组是否先按上游每个分镜行最后时间段结束秒累计裁决边界，落盘后是否改写为当前分镜组基准下连续递增的 `[N-N秒]`，且后一个时间段起点等于前一个终点；组内分镜总时长是否接近 14.5 秒、通常是否落在约 10-14.5 秒、最终累计结束秒是否以 `.5` 结尾、且必须不超过 14.5 秒；atomic unit 与对白/画面承托必须完整，但不能作为超 14.5 秒放行理由 |
| `connector_removal_review` | 每次阶段 PASS 前 | 检查新产物是否不再输出 `## A~B` 连接件块，也不输出连接件字段；相邻组承接是否只由下一组第一个普通 `[0-N秒]` 分镜行承担 |
| `faithfulness_review` | 每次阶段 PASS 前 | 标准摄影路径 diff 或等价对照上游 `9-光影`，确认正文字段、对白、分镜行标题未被改写，且未新增 `分镜画面：` 替换原字段；`direct_screenplay` 路径对照剧本/编导稿，确认场景顺序、剧情事实、英文对白原文和声画承托未被改写，并记录时间码为本阶段 LLM 规划 |
| `statistics_evidence_review` | 每次阶段 PASS 前 | 抽查 YAML `角色`、`场景`、`道具` 是否能回指本组正文和第一个普通分镜行证据；道具项必须检查是否存在普通环境物过度列入、同物异名、状态差异、持有人差异、镜头差异或部件拆分造成的重复，并合并到稳定 canonical 道具名 |

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-GROUP-01` | 输入回指 | frontmatter 或报告记录 `source_lighting_path`、`visual_tone_path`，必要时记录 `north_star_path` 的项目禁区/不变量消费 |
| `GATE-GROUP-01D` | 剧本直入声明 | `direct_screenplay` 路径记录 `source_state=direct_screenplay`、剧本/编导稿源路径、时间码由本阶段 LLM 规划、`9-光影` 字段级 diff 不适用 |
| `GATE-GROUP-01S` | 初始化综合消费 | 项目存在初始化综合时，已形成 `init_team_synthesis_context`，并记录如何影响分组节奏、桥接策略或 north_star 投影；不得触发 team 身份、旧 stage profile 或伪顾问问答 |
| `GATE-GROUP-01A` | 场景标题行 | 每个分镜组标题后先写当前场景标题行，未切换场景的新分镜组也重复同一场景标题 |
| `GATE-GROUP-02` | `全局风格` 整理 | 每组在场景标题行下方立即输出 `全局风格：`；字段内只有一行纯内容；该行以固定前置词开头，后接当前组全局风格整理句；整理句依据 `画面基调.Global Style Prompt` 和当前证据抽取匹配部分，保持自然单段且 300 字以内；不得输出 `Visual Slogan`、`Design Principle`、`Visual Gene Profile` 或 `Negative Traits` 独立行 |
| `GATE-GROUP-05` | ID 真实 | 每组 ID 为 `x-y-z`，匹配真实集、场、场内序号 |
| `GATE-GROUP-06` | 组内时长 | 每组以分镜行总时长为主，裁决时按上游 `分镜N（起始秒-结束秒）：` 或兼容 `[起始秒-结束秒]` 行累计，落盘后改写为当前分镜组基准下连续递增的 `分镜N（N-N秒）：` 或 `[N-N秒]`；优先接近约 14.5 秒，通常约 10-14.5 秒可接受；最终累计结束秒必须以 `.5` 结尾，若自然相加不是 `.5` 结尾则在组尾上调 0.5 秒；低于约 10 秒必须有回填复核或短场景例外理由；超过 14.5 秒为硬失败 |
| `GATE-GROUP-06D` | 剧本直入 14.5 秒拆组 | `direct_screenplay` 路径按剧本声画 atomic unit 自动拆成约 14.5 秒/组，通常约 10-14.5 秒，硬上限 14.5 秒，最终累计结束秒以 `.5` 结尾；不得为追求 14.5 秒或制造 `.5` 结尾切断对白与对应画面承托 |
| `GATE-GROUP-07` | 字数、对白与密度风险 | 字数和对白数只作为辅助风险检查；高于约 1680 字或低于 850 字的组必须进入语义复核，但不得因此切断同一画面、对应对白承托或改写上游正文；字数不设硬上限 |
| `GATE-GROUP-08` | atomic unit | 分镜行及其连续时间段不跨组 |
| `GATE-GROUP-09` | 连接件禁用 | 不输出 `## <上一个分镜组ID>~<下一个分镜组ID>` 连接件块，也不输出 `连接类型：`、`连接方法：`、`变化过程：`、`主体运动：`、`运镜设计：`、`透视适应：`、`避免元素：` 等连接件字段 |
| `GATE-GROUP-10` | 非新增剧情与非尾钩 | 第一个普通 `[0-N秒]` 分镜行不新增关键事实、对白、人物或道具，不写成悬念尾钩、剧情解释、规则说明或下一剧情预告 |
| `GATE-GROUP-11` | YAML 统计 | 每组含 `字数统计`、`时长估算`、`角色`、`场景`、`道具`；`字数统计` 计入场景标题行和正文；不计入 `全局风格：` 和 YAML fenced block |
| `GATE-GROUP-13` | 位置细节禁用 | 不输出 `画面构图：` 或 `左侧：` / `中间：` / `右侧：` / `前景：` / `中景：` / `背景：` 等位置细节字段 |
| `GATE-GROUP-14` | 首帧衔接 / 回龙帧 | 每组第一个时间码分镜行是普通 `分镜N（0-N秒）：` 或 `[0-N秒]` 分镜描述；首组承接本组开始画面，第二组起完整代入上一组结尾状态画面点内容，并只调整景别和镜头视角；回龙到对白/独白/旁白/音效画面时同步带入对应声音内容；不写来源说明或规则说明 |
| `GATE-GROUP-15` | 禁用旧字段 | 新产物不得输出 `分镜画面：`、`增补首帧：`、`回龙帧：`、`入场镜头：`、`出场画面：`、`画面属性：`、旧版 `入场画面：`、`画面构图：` 或六类位置细节字段 |
| `GATE-GROUP-16` | 原文保真 | 标准摄影路径同步 `9-光影` 划定正文；`direct_screenplay` 路径保留剧本事实、场景顺序、英文对白原文和声画承托关系，未把 LLM 规划时间码伪称为 `9-光影` 真源 |
| `GATE-GROUP-17` | 输出路径 | 写入 `projects/aigc/<项目名>/10-分组/第N集.md` 和 `执行报告.md` |

## Semantic Pass Gate

阶段 PASS 必须同时满足：

- `mechanical_check` 已运行且 error 为 0；warning 必须在语义 review 中处理。
- `boundary_review`、`global_style_review`、`first_storyboard_continuity_review`、`connector_removal_review`、`faithfulness_review`、`statistics_evidence_review` 均记录 LLM 或人工结论。
- 初始化综合存在时，`init_team_synthesis_context` 已记录消费来源和采纳点，且没有 creative-stage team persona dispatch。
- 语义结论只能为 `pass` 或 `pass_with_declared_exception`；任何 `fail` 都必须按 Failure Routing 返回源层修复。`>14.5s` 单组超时或最终累计结束秒未以 `.5` 结尾不得作为 `pass_with_declared_exception`。

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-GROUP-02` | `全局风格：` 缺失、位置错误、单行内容缺失、固定前置词缺失、整理句超过 300 字、完整照抄全局母稿、未匹配当前组证据、错误输出 `Visual Slogan` / `Design Principle` / `Visual Gene Profile` / `Negative Traits` 独立行，或 `Global Style Prompt` 缺失 | `references/north-star-projection-contract.md` |
| `FAIL-GROUP-INIT-SYNTHESIS` | 初始化综合存在但未形成 `init_team_synthesis_context`，或误触发 team 身份 / 旧 stage profile / 伪顾问问答 | `SKILL.md#N1-INTAKE` |
| `FAIL-GROUP-04` | ID 不匹配或不连续 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-05` | 组内分镜总时长明显偏离 14.5 秒且未复核、低于约 10 秒未回填、超过 14.5 秒、最终累计结束秒未以 `.5` 结尾、单个 atomic unit 超 14.5 秒但未回退 `9-光影` 修复，或字数/对白风险失控 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-DIRECT-SCREENPLAY` | 直接接手剧本时仍要求用户补 `9-光影`、未自动按约 14.5 秒/组拆组、最终累计结束秒未以 `.5` 结尾、未声明 direct screenplay 源路径与时间码来源、或把本阶段规划时间码伪称为 `9-光影` 真源 | `references/group-boundary-contract.md#direct-screenplay-intake-rule` |
| `FAIL-GROUP-06` | 同一分镜行、对应对白/画面承托或连续时间段被截断，或组内后续字段时间码从 0 重启 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-07` | 继续输出 `## A~B` 连接件块、旧 `组间连接件：` 区块，或继续输出连接件字段 | `SKILL.md#N7-ASSEMBLE-STATS` |
| `FAIL-GROUP-08` | YAML 缺字段、统计错误，或道具未做同物识别与归一合并导致重复/过细 | `references/statistics-yaml-contract.md` |
| `FAIL-GROUP-09` | 改写上游正文 | `SKILL.md` Output Contract 与本文件 `faithfulness_review` |
| `FAIL-GROUP-11` | 新产物仍输出 `画面构图：`、六类位置细节字段，或组头输出结构化 `角色：` / `场景：` / `道具：` 清单 | `SKILL.md#N7-ASSEMBLE-STATS` |
| `FAIL-GROUP-12` | 首帧衔接/回龙帧缺失、第一个时间码分镜行不是普通 `分镜N（0-N秒）：` 或 `[0-N秒]` 分镜描述、未完整代入上一组结尾状态画面点内容、回龙到对白/独白/旁白/音效画面却遗漏对应声音内容、输出 `分镜画面：` / `增补首帧：` / `回龙帧：`、写成来源/规则说明、出现模板化尾句，或新增剧情、改对白、改变人物状态 | `SKILL.md#N6-FIRST-LINE-CONTINUITY` |

## Review Output

执行报告至少记录：

- 输入文件、north_star 文件与输出文件。
- `direct_screenplay` 路径的触发原因、剧本/编导稿源路径、时间码来源声明和 `9-光影` 字段级 diff 不适用说明。
- 初始化综合消费来源、采纳点和 persona dispatch 禁用确认。
- 处理集号和场景数量。
- 分镜组数量与每场组号范围。
- 每组时长估算、字数、`全局风格：` 摘要、首帧衔接/回龙帧检查、结尾状态画面点完整代入检查、声音承托同步检查、YAML 角色/场景/道具短名单概览。
- 连接件禁用检查结果，包括是否存在 `## A~B` 连接件块、旧 `组间连接件：` 区块或连接件字段残留。
- 机械校验结果，包括 error / warning 数量。
- `boundary_review`、`global_style_review`、`first_storyboard_continuity_review`、`connector_removal_review`、`faithfulness_review`、`statistics_evidence_review` 的语义结论、抽查范围、时长偏离和例外理由。
- 需要返工的分镜组 ID 和失败码。
