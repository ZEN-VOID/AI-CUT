# Review Contract

## Pass Criteria

- 输入路径明确，且用户显式路径优先于项目默认路径。
- 若源资料自带集数划分，输出严格尊重原边界。
- `第N章`、`第N回`、chapter、卷/章/节等章节/回目结构未被误判为 P1 原生集标，但在无 P1 时默认映射为一章/一回一集。
- 若无 P1 且有章节/回目结构，审查时必须确认已默认一章/一回一集；偏离必须有用户重组指令或源结构异常证据。
- 若连续正文缺少章节/回目结构，或用户要求重组，大多数集数落在 2500-3000 字附近，偏离有自然边界理由。
- `第N集.md` 编号连续、正文未改写、覆盖无遗漏。
- `执行报告.md` 可复查输入、边界、字数、coverage 与返工入口。

## Review Gates

| gate_id | review_question | fail_code | rework_target | required_evidence |
| --- | --- | --- | --- | --- |
| `GATE-SPLIT-01-SOURCE-LOCK` | 是否锁定唯一小说原文真源，并按用户显式路径优先、项目 `源/` 次之、旧路径 fallback 仅用户明确要求的顺序执行？ | `FAIL-SPLIT-01` | `SKILL.md#T2-SOURCE-LOCK`；`SKILL.md#Input Contract`；`references/input-output-contract.md#Source Priority` | 输入路径、fallback 说明、文件清单、被排除的非正文资料 |
| `GATE-SPLIT-01A-SOURCE-ORDER` | 多文件或多章节来源是否可读，并已建立可复查的确定性顺序？ | `FAIL-SPLIT-01A` | `SKILL.md#T3-SOURCE-ORDER`；`references/input-output-contract.md#Valid Source Material` | 可读性判断、排序依据、输入文件顺序表 |
| `GATE-SPLIT-02-P1-EPISODE-MARK` | 原资料存在真实 P1 集标时，是否按原集标进入 `explicit_episode_split`，没有按字数重切？ | `FAIL-SPLIT-02` | `SKILL.md#T4-MARK-SCAN`；`SKILL.md#T5-BOUNDARY-SOLVE`；`references/input-output-contract.md#Episode Boundary Policy` | 集标列表、原始边界、切分模式 |
| `GATE-SPLIT-02A-CHAPTER-AS-EPISODE` | 章节、回目、卷、节、chapter 或 story 文件名是否在无 P1 集标时默认映射为一章/一回一集？ | `FAIL-SPLIT-02A` | `SKILL.md#T4-MARK-SCAN`；`SKILL.md#T5-BOUNDARY-SOLVE`；`references/input-output-contract.md#Episode Boundary Policy` | 章节/回目边界列表、默认映射说明、偏离原因 |
| `GATE-SPLIT-03-BOUNDARY-SOLVE` | 连续正文缺少章节/回目结构，或用户要求重组时，边界是否结合自然结构、戏剧断点和 2500-3000 字目标窗，且没有切断句子、对白或关键动作？ | `FAIL-SPLIT-03` | `SKILL.md#T5-BOUNDARY-SOLVE`；`references/input-output-contract.md#Episode Boundary Policy` | 每集字数、起止段落、边界理由、偏离说明 |
| `GATE-SPLIT-04-EPISODE-WRITEBACK` | 逐集文件是否写入 canonical 目录、编号连续、正文保真，且未混入改写、剧本化、分镜化或设定说明？ | `FAIL-SPLIT-04` | `SKILL.md#T6-WRITEBACK`；`SKILL.md#Output Contract`；`references/input-output-contract.md#Episode File Requirements` | 输出文件清单、编号检查、正文保真抽查或 diff 说明 |
| `GATE-SPLIT-05-REPORT-COVERAGE` | `执行报告.md` 是否足以复查输入、边界、字数、覆盖状态、跳过原因和具体返工入口？ | `FAIL-SPLIT-05` | `SKILL.md#T7-REVIEW`；`SKILL.md#Output Contract`；`references/input-output-contract.md#Execution Report Requirements` | 边界表、coverage 表、跳过原因、返工入口 |

## Fail Codes

| fail_code | symptom | rework |
| --- | --- | --- |
| `FAIL-SPLIT-01` | 输入真源不明或误用 `CONTEXT/` | 回到 source lock |
| `FAIL-SPLIT-01A` | 多文件来源不可读、未排序或排序依据不可复查 | 回到 source order |
| `FAIL-SPLIT-02` | 忽略原资料自带集标 | 改走 explicit episode split |
| `FAIL-SPLIT-02A` | 有章节/回目结构却没有默认一章/一回一集，或偏离该默认规则但缺少证据 | 回到 episode mark scan，按章节/回目默认映射或补足偏离证据 |
| `FAIL-SPLIT-03` | 默认切分机械截断句子或对白 | 回到 boundary solve |
| `FAIL-SPLIT-04` | 输出路径、编号或正文保真不符合合同 | 回到 writeback |
| `FAIL-SPLIT-05` | 执行报告缺少覆盖证据 | 补报告与返工入口 |
