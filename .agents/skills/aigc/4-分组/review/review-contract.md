# Review Contract

本文件定义 `4-分组` 的质量门禁。

## Review Modes

| mode | trigger | action |
| --- | --- | --- |
| `mechanical_check` | 落盘前或修复时 | 检查分镜组 ID、必填标题、字数、YAML、组间桥接一致性 |
| `boundary_review` | 分组边界争议时 | 检查对白数、1980 字上限、atomic unit 完整性 |
| `bridge_review` | 组间衔接风险高时 | 检查入场/出场画面是否同画面、短镜头、非新增剧情 |
| `faithfulness_review` | 有改写风险时 | diff 上游 `3-摄影`，确认正文字段、对白、原有镜头语言未被改写 |

## Acceptance Checklist

| gate_id | check | pass criteria |
| --- | --- | --- |
| `GATE-GROUP-01` | 输入回指 | frontmatter 或报告记录 `source_cinematography_path`、`north_star_path` |
| `GATE-GROUP-02` | north_star 投影 | 每组组头含三行纯内容；第 1 行以固定前置词 `视频生成的画面风格，光影和氛围与场景参照图保持一致。不生成文字字幕和BGM，仅生成物理互动音效与环境和氛围音效。` 开头，后接直引 `全局风格.全局风格提示词` 原词，第 2、3 行分别直引 `类型元素.类型元素提示词`、`细分风格.画面风格`；不显示 `[全局风格]`、`[类型元素]`、`[画面风格]` 标题字段 |
| `GATE-GROUP-05` | ID 真实 | 每组 ID 为 `x-y-z`，匹配真实集、场、场内序号 |
| `GATE-GROUP-06` | 字数 | 每组完整构成 <= 1980 字，不含 YAML |
| `GATE-GROUP-07` | 对白与密度 | 长对白约 4 句、短对白约 6 句；低于约 1000 字的组完成回填复核，低于 850 字通常不保留 |
| `GATE-GROUP-08` | atomic unit | 画面字段及其 `镜头语言/分镜N` 不跨组 |
| `GATE-GROUP-09` | 桥接 | 每集首组不输出入场画面段；相邻组出场/入场同画面且自然承接 |
| `GATE-GROUP-10` | 非新增剧情 | 补位画面不新增关键事实、对白、人物或道具 |
| `GATE-GROUP-11` | YAML 统计 | 每组含 `字数统计`、`角色`、`场景`、`道具` |
| `GATE-GROUP-12` | 原文保真 | 划定正文同步原换行，未改写 `3-摄影` 字段、对白、原有镜头语言 |
| `GATE-GROUP-13` | 输出路径 | 写入 `projects/aigc/<项目名>/4-分组/第N集.md` 和 `执行报告.md` |

## Failure Routing

| fail_code | symptom | rework target |
| --- | --- | --- |
| `FAIL-GROUP-02` | north_star 三项缺失、被改写，或全局风格固定前置词缺失/未置于最前 | `references/north-star-projection-contract.md` |
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
- 每组字数、对白数、角色、场景、道具概览。
- 组间桥接检查结果。
- 机械校验结果或人工 review 结果。
- 需要返工的分镜组 ID 和失败码。
