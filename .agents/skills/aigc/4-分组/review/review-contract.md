# Review Contract

本文件定义 `4-分组` 的质量门禁。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 每次落盘前或修复后 | 运行 `scripts/validate_storyboard_groups.py`，检查分镜组标题、必填标题、纯正文字数、YAML、组间连接件结构；warning 进入语义复核，不直接等于 PASS |
| `boundary_review` | 每次阶段 PASS 前 | LLM 或人工检查对白数、纯正文 1680 字目标上限、1980 字硬上限、atomic unit 完整性、过长组拆分复核和短组例外理由 |
| `bridge_review` | 每次阶段 PASS 前 | LLM 或人工检查组间首尾帧连接件是否能从第 N 组原尾帧抵达第 N+1 组原首帧，是否以标题作为唯一连接件 ID，是否标题后、`连接类型` 前先写三项 north_star 风格行，是否为 3-4 秒连接件，是否区分同场景/跨场景，是否把内部方法论选择转换为具体画面连接办法，是否避免复述起点/目标端点，是否以变化过程、主体运动、运镜设计和透视适应描述连接过程，是否以 `避免元素` 承载负面约束，是否非新增剧情且非尾钩 |
| `faithfulness_review` | 每次阶段 PASS 前 | diff 或等价对照上游 `3-摄影`，确认正文字段、对白、原有分镜明细未被改写 |
| `statistics_evidence_review` | 每次阶段 PASS 前 | LLM 或人工抽查 YAML `角色`、`场景`、`道具` 是否能回指本组正文证据；高风险组和新增/异常统计项逐项复核 |

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-GROUP-01` | 输入回指 | frontmatter 或报告记录 `source_cinematography_path`、`north_star_path` |
| `GATE-GROUP-02` | north_star 投影 | 每组组头含三行纯内容；第 1 行以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。` 开头，后接直引 `全局风格.全局风格提示词` 原词，第 2、3 行分别直引 `类型元素.类型元素提示词`、`细分风格.画面风格`；不显示 `[全局风格]`、`[类型元素]`、`[画面风格]` 标题字段 |
| `GATE-GROUP-05` | ID 真实 | 每组 ID 为 `x-y-z`，匹配真实集、场、场内序号 |
| `GATE-GROUP-06` | 字数 | 每组纯分镜剧本正文常规目标 <= 1680 字；1681-1980 字必须有拆分复核后的例外理由；任何组纯正文不得超过 1980 字；不含分镜组标题、north_star、YAML 和组间连接件 |
| `GATE-GROUP-07` | 对白与密度 | 长对白约 4 句、短对白约 6 句；高于 1680 字的组完成拆分复核；低于约 1000 字的组完成回填复核；低于 850 字只允许在上游单场景/单事件极短且无法合并时保留，并在执行报告写明例外理由 |
| `GATE-GROUP-08` | atomic unit | 画面字段及其 `分镜明细/分镜N` 不跨组 |
| `GATE-GROUP-09` | 组间连接件 | 每对相邻分镜组之间都有 `## <上一个分镜组ID>~<下一个分镜组ID>`，连接件物理夹在上下两个分镜组中间，标题作为唯一连接件 ID，标题后、`连接类型` 前有三项 north_star 风格行，且第 1 行以固定全局风格前置词开头；字段包含连接类型、连接方法、时长、变化过程、主体运动、运镜设计、透视适应和避免元素；不得包含 `起点尾帧：` / `目标首帧：` / `分镜ID：` / `连接件提示：`；`连接方法` 必须是具体画面连接办法，不得只填抽象分类名；`避免元素` 不复述正向提示 |
| `GATE-GROUP-10` | 非新增剧情与非尾钩 | 连接件不新增关键事实、对白、人物或道具，不写成悬念尾钩、剧情解释或下一剧情预告 |
| `GATE-GROUP-11` | YAML 统计 | 每组含 `字数统计`、`角色`、`场景`、`道具`；统计项能回指本组正文证据，或在执行报告中记录已修复/排除的异常项 |
| `GATE-GROUP-12` | 原文保真 | 划定正文同步原换行，未改写 `3-摄影` 字段、对白、原有分镜明细 |
| `GATE-GROUP-13` | 输出路径 | 写入 `projects/aigc/<项目名>/4-分组/第N集.md` 和 `执行报告.md` |

## Semantic Pass Gate

阶段 PASS 必须同时满足：

- `mechanical_check` 已运行且 error 为 0；warning 必须在语义 review 中处理。
- `boundary_review`、`bridge_review`、`faithfulness_review`、`statistics_evidence_review` 均记录 LLM 或人工结论。
- 语义结论只能为 `pass` 或 `pass_with_declared_exception`；任何 `fail` 都必须按 Failure Routing 返回源层修复。

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-GROUP-02` | north_star 三项缺失、被改写，或全局风格固定前置词缺失/未置于最前 | `references/north-star-projection-contract.md` |
| `FAIL-GROUP-04` | ID 不匹配或不连续 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-05` | 纯正文超 1680 字未复核、纯正文超 1980 字硬上限或对白过载 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-06` | 同一画面句子或分镜明细被截断 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-07` | 连接件缺失、字段不完整、三项风格行缺失或全局风格前置词错误、标题 ID 不是 `上一个分镜组ID~下一个分镜组ID`、块内重复输出 `分镜ID：`、连接方法缺失或只填抽象分类名、变化过程/主体运动/运镜设计/透视适应缺失、复述起点/目标端点、未夹在上下分镜组中间、无法从尾帧抵达首帧、继续使用旧入场/出场、继续输出 `连接件提示：` 或新增剧情 | `references/bridge-shot-contract.md` |
| `FAIL-GROUP-08` | YAML 缺字段或统计错误 | `references/statistics-yaml-contract.md` |
| `FAIL-GROUP-09` | 改写上游正文 | `SKILL.md` Output Contract 与本文件 `faithfulness_review` |

## Review Output

执行报告至少记录：

- 输入文件、north_star 文件与输出文件。
- 处理集号和场景数量。
- 分镜组数量与每场组号范围。
- 每组字数、对白数、角色、场景、道具概览。
- 组间连接件检查结果，包括相邻组 ID、三项风格行、连接类型、连接方法、变化过程、主体运动、运镜设计、透视适应、避免元素和 3-4 秒连接件语义结论。
- 机械校验结果，包括 error / warning 数量。
- `boundary_review`、`bridge_review`、`faithfulness_review`、`statistics_evidence_review` 的语义结论、抽查范围和例外理由。
- 需要返工的分镜组 ID 和失败码。
