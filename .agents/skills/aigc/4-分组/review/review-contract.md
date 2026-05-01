# Review Contract

本文件定义 `4-分组` 的质量门禁。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 落盘前或修复时 | 检查分镜组 ID、必填标题、分镜级站位位移首次锁定、禁止输出 `空间锚点：` 字段、字数、YAML、组间桥接一致性 |
| `boundary_review` | 分组边界争议时 | 检查对白数、1980 字上限、atomic unit 完整性 |
| `spatial_review` | 空间连续性风险高时 | 检查 `站位和位移：` 中的空间参照是否为真实位置参照点，首次锁定及发生变化的 `分镜N:` 是否有对应 `站位和位移：`，并以明确角色名说明方位、运动方向和多角色顺位关系；逐条核对位移是否由当前分镜证据、上一分镜状态或入场/出场补位支持；连续无变化分镜不要求重复输出；不得输出独立 `空间锚点：` 字段 |
| `bridge_review` | 组间衔接风险高时 | 检查入场/出场画面是否同画面、短镜头、非新增剧情 |
| `faithfulness_review` | 有改写风险时 | diff 上游 `3-摄影`，确认正文字段、对白、原有镜头语言未被改写；`站位和位移：` 仅作为新增分镜明细辅助行存在 |

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-GROUP-01` | 输入回指 | frontmatter 或报告记录 `source_cinematography_path`、`north_star_path` |
| `GATE-GROUP-02` | north_star 投影 | 每组组头含三行纯内容；第 1 行以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。` 开头，后接直引 `全局风格.全局风格提示词` 原词，第 2、3 行分别直引 `类型元素.类型元素提示词`、`细分风格.画面风格`；不显示 `[全局风格]`、`[类型元素]`、`[画面风格]` 标题字段 |
| `GATE-GROUP-03` | 空间参照 | 不输出独立 `空间锚点：` 字段；空间参照只内化到首次锁定及变化分镜的 `站位和位移：` 中 |
| `GATE-GROUP-04` | 站位位移 | 首次锁定及发生变化的 `分镜N:` 明细下方含非空 `站位和位移：` 辅助行，以明确角色名或上游已命名的稳定群体称谓为主语，不使用 `画面主体`、`主体`、`人物`、`角色`、`主角`、`他/她/他们/她们` 等含混指代，并说明空间参照、方位和运动方向；涉及多角色时必须明确前后、左右、内外、近远或动作先后的顺位关系；有移动时必须能回指当前分镜原文、上一分镜状态或入场/出场补位画面，无移动证据且连续状态不变时只保留首次锁定，不在每个分镜重复输出 |
| `GATE-GROUP-05` | ID 真实 | 每组 ID 为 `x-y-z`，匹配真实集、场、场内序号 |
| `GATE-GROUP-06` | 字数 | 每组完整构成 <= 1980 字，不含 YAML，包含必要的站位位移首次锁定和变化声明 |
| `GATE-GROUP-07` | 对白与密度 | 长对白约 4 句、短对白约 6 句；低于约 1000 字的组完成回填复核，低于 850 字通常不保留 |
| `GATE-GROUP-08` | atomic unit | 画面字段及其 `镜头语言/分镜N` 不跨组 |
| `GATE-GROUP-09` | 桥接 | 每集首组不输出入场画面段；相邻组出场/入场同画面且自然承接；下一组首条 `站位和位移：` 能从本组入场画面接到第一个原始分镜，不造成角色瞬移、左右倒置或内外倒置 |
| `GATE-GROUP-10` | 非新增剧情 | 补位画面不新增关键事实、对白、人物或道具 |
| `GATE-GROUP-11` | YAML 统计 | 每组含 `字数统计`、`角色`、`场景`、`道具` |
| `GATE-GROUP-12` | 原文保真 | 划定正文同步原换行，未改写 `3-摄影` 字段、对白、原有镜头语言；只允许在首次锁定或发生变化的对应 `分镜N:` 下方新增 `站位和位移：` 辅助行 |
| `GATE-GROUP-13` | 输出路径 | 写入 `projects/aigc/<项目名>/4-分组/第N集.md` 和 `执行报告.md` |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-GROUP-02` | north_star 三项缺失、被改写，或全局风格固定前置词缺失/未置于最前 | `references/north-star-projection-contract.md` |
| `FAIL-GROUP-03` | 输出独立空间锚点字段、空间参照抽象化、缺少首次站位锁定、变化分镜缺站位位移、站位位移使用模糊主语、涉及多角色却未写明顺位关系，或位移无法由剧情动作/上一分镜/组间补位连续推导 | `references/spatial-consistency-contract.md` |
| `FAIL-GROUP-04` | ID 不匹配或不连续 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-05` | 组超字数或对白过载 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-06` | 同一画面句子或镜头语言被截断 | `references/group-boundary-contract.md` |
| `FAIL-GROUP-07` | 入场/出场不一致或新增剧情 | `references/bridge-shot-contract.md` |
| `FAIL-GROUP-08` | YAML 缺字段或统计错误 | `references/statistics-yaml-contract.md` |
| `FAIL-GROUP-09` | 改写上游正文 | `SKILL.md` Output Contract 与本文件 `faithfulness_review` |

## Review Output

执行报告至少记录：

- 输入文件、north_star 文件与输出文件。
- 处理集号和场景数量。
- 分镜组数量与每场组号范围。
- 每组字数、对白数、站位位移首次锁定和变化声明、角色、场景、道具概览。
- 组间桥接检查结果。
- 空间连续性人工/LLM review 结果，至少说明是否发现无证据移动、角色瞬移、左右/内外倒置、镜头运动误写成角色位移。
- 机械校验结果或人工 review 结果。
- 需要返工的分镜组 ID 和失败码。
