# Review Contract

本文件定义 `6-分组` 的质量门禁。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 每次落盘前或修复后 | 运行 `scripts/validate_storyboard_groups.py`，检查分镜组标题、场景标题行、必填标题、计入场景标题行后的正文字数、显式时长累计、YAML、组间连接件结构；warning 进入语义复核，不直接等于 PASS |
| `boundary_review` | 每次阶段 PASS 前 | LLM 或人工检查每组显式 `分镜N（约X秒）` 累计是否接近 15 秒、通常是否落在约 12-18 秒、且必须不超过 18 秒；atomic unit 与对白/画面承托必须完整，但不能作为超 18 秒放行理由；单个 atomic unit 超 18 秒时必须回退 `5-摄影` 修复；字数和对白数只作为辅助风险检查 |
| `bridge_review` | 每次阶段 PASS 前 | LLM 或人工检查组间首尾帧连接件是否能从第 N 组原尾帧抵达第 N+1 组原首帧，是否以标题作为唯一连接件 ID，是否标题后先写场景标题行并在跨场景时使用 `场景标题A ➡️ 场景标题B`，是否在 `连接类型` 前写三项 north_star 风格行，是否为 3-4 秒连接件，是否区分同场景/跨场景，是否把内部方法论选择转换为具体画面连接办法，是否避免复述起点/目标端点，是否以变化过程、主体运动、运镜设计和透视适应描述连接过程，是否以 `避免元素` 承载负面约束，是否非新增剧情且非尾钩 |
| `faithfulness_review` | 每次阶段 PASS 前 | diff 或等价对照上游 `5-摄影`，确认正文字段、对白、原有分镜明细未被改写 |
| `statistics_evidence_review` | 每次阶段 PASS 前 | LLM 或人工抽查 YAML `角色`、`场景`、`道具` 是否能回指本组正文证据；高风险组和新增/异常统计项逐项复核 |

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-GROUP-01` | 输入回指 | frontmatter 或报告记录 `source_cinematography_path`、`north_star_path` |
| `GATE-GROUP-01A` | 场景标题行 | 每个分镜组标题后先写当前场景标题行，未切换场景的新分镜组也重复同一场景标题；每个连接件标题后先写场景标题行，同场景重复同一标题，跨场景使用 `场景标题A ➡️ 场景标题B` |
| `GATE-GROUP-02` | north_star 投影 | 每组组头含三行纯内容；第 1 行以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。需要生成现场物理互动音效、氛围感音效、环境声、自然现象声、动作声，不要生成任何字幕，不要生成背景音乐。` 开头，后接直引 `全局风格.全局风格提示词` 原词，第 2、3 行分别直引 `类型元素.类型元素提示词`、`细分风格.画面风格`；不显示 `[全局风格]`、`[类型元素]`、`[画面风格]` 标题字段 |
| `GATE-GROUP-05` | ID 真实 | 每组 ID 为 `x-y-z`，匹配真实集、场、场内序号 |
| `GATE-GROUP-06` | 组内时长 | 每组以 `分镜N（约X秒）` 累计为主，优先接近约 15 秒，通常约 12-18 秒可接受；低于约 10 秒必须有回填复核或短场景例外理由；超过 18 秒为硬失败，必须拆分、重组或回退 `5-摄影` 修复，不允许完整 atomic unit 例外放行 |
| `GATE-GROUP-07` | 字数、对白与密度风险 | 字数和对白数只作为辅助风险检查；长对白约 4 句、短对白约 6 句是风险提示；高于 1680 字或低于 850 字的组必须进入语义复核，但不得因此切断同一画面或对应对白承托 |
| `GATE-GROUP-08` | atomic unit | 画面字段及其 `分镜明细/分镜N` 不跨组 |
| `GATE-GROUP-09` | 组间连接件 | 每对相邻分镜组之间都有 `## <上一个分镜组ID>~<下一个分镜组ID>`，连接件物理夹在上下两个分镜组中间，标题作为唯一连接件 ID，标题后先写场景标题行，同场景重复同一标题，跨场景使用 `场景标题A ➡️ 场景标题B`；随后在 `连接类型` 前写三项 north_star 风格行，且第 1 行以固定全局风格前置词开头；字段包含连接类型、连接方法、时长、变化过程、主体运动、运镜设计、透视适应和避免元素；不得包含 `起点尾帧：` / `目标首帧：` / `分镜ID：` / `连接件提示：`；`连接方法` 必须是具体画面连接办法，不得只填抽象分类名；`避免元素` 不复述正向提示 |
| `GATE-GROUP-10` | 非新增剧情与非尾钩 | 连接件不新增关键事实、对白、人物或道具，不写成悬念尾钩、剧情解释或下一剧情预告 |
| `GATE-GROUP-11` | YAML 统计 | 每组含 `字数统计`、`时长估算`、`角色`、`场景`、`道具`；`字数统计` 必须计入分镜组标题后的场景标题行，`时长估算` 只回指组内 `分镜N（约X秒）` 累计，其他统计项能回指本组正文证据，或在执行报告中记录已修复/排除的异常项 |
| `GATE-GROUP-12` | 原文保真 | 划定正文同步原换行，未改写 `5-摄影` 字段、对白、原有分镜明细 |
| `GATE-GROUP-13` | 输出路径 | 写入 `projects/aigc/<项目名>/6-分组/第N集.md` 和 `执行报告.md` |

## Semantic Pass Gate

阶段 PASS 必须同时满足：

- `mechanical_check` 已运行且 error 为 0；warning 必须在语义 review 中处理。
- `boundary_review`、`bridge_review`、`faithfulness_review`、`statistics_evidence_review` 均记录 LLM 或人工结论。
- 语义结论只能为 `pass` 或 `pass_with_declared_exception`；任何 `fail` 都必须按 Failure Routing 返回源层修复。`>18s` 单组超时不得作为 `pass_with_declared_exception`。

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-GROUP-02` | north_star 三项缺失、被改写，或全局风格固定前置词缺失/未置于最前 | `references/north-star-projection-contract.md` |
| `FAIL-GROUP-04` | ID 不匹配或不连续 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-05` | 组内显式时长累计明显偏离 15 秒且未复核、低于约 10 秒未回填、超过 18 秒、单个 atomic unit 超 18 秒但未回退 `5-摄影` 修复，或字数/对白风险失控 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-06` | 同一画面句子、对应对白/画面承托或分镜明细被截断 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-07` | 连接件缺失、字段不完整、场景标题行缺失或跨场景未用 `场景标题A ➡️ 场景标题B`、三项风格行缺失或全局风格前置词错误、标题 ID 不是 `上一个分镜组ID~下一个分镜组ID`、块内重复输出 `分镜ID：`、连接方法缺失或只填抽象分类名、变化过程/主体运动/运镜设计/透视适应缺失、复述起点/目标端点、未夹在上下分镜组中间、无法从尾帧抵达首帧、继续使用旧入场/出场、继续输出 `连接件提示：` 或新增剧情 | `references/bridge-shot-contract.md` |
| `FAIL-GROUP-08` | YAML 缺字段或统计错误 | `references/statistics-yaml-contract.md` |
| `FAIL-GROUP-09` | 改写上游正文 | `SKILL.md` Output Contract 与本文件 `faithfulness_review` |

## Review Output

执行报告至少记录：

- 输入文件、north_star 文件与输出文件。
- 处理集号和场景数量。
- 分镜组数量与每场组号范围。
- 每组时长估算、字数、对白数、角色、场景、道具概览。
- 组间连接件检查结果，包括相邻组 ID、场景标题行、三项风格行、连接类型、连接方法、变化过程、主体运动、运镜设计、透视适应、避免元素和 3-4 秒连接件语义结论。
- 机械校验结果，包括 error / warning 数量。
- `boundary_review`、`bridge_review`、`faithfulness_review`、`statistics_evidence_review` 的语义结论、抽查范围、时长偏离和例外理由。
- 需要返工的分镜组 ID 和失败码。
