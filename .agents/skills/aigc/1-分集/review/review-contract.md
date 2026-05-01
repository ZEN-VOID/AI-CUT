# Review Contract

## Pass Criteria

- 输入路径明确，且用户显式路径优先于项目默认路径。
- 若源资料自带集数划分，输出严格尊重原边界。
- `第N章`、chapter、卷/章/节等 story 章节结构未被误判为原生 `第N集` 集标。
- 章节不等于集数；审查时必须确认没有把 story 一章默认落成 AIGC 一集。
- 若无自带集数划分，大多数集数落在 2500-3000 字附近，偏离有自然边界理由。
- `第N集.md` 编号连续、正文未改写、覆盖无遗漏。
- `执行报告.md` 可复查输入、边界、字数、coverage 与返工入口。

## Fail Codes

| fail_code | symptom | rework |
| --- | --- | --- |
| `FAIL-SPLIT-01` | 输入真源不明或误用 `CONTEXT/` | 回到 source lock |
| `FAIL-SPLIT-02` | 忽略原资料自带集标 | 改走 explicit episode split |
| `FAIL-SPLIT-02A` | 把 story 章节标记误当原生集标，机械执行一章一集 | 回到 episode mark scan，改走 P2/P3 边界裁决 |
| `FAIL-SPLIT-03` | 默认切分机械截断句子或对白 | 回到 boundary solve |
| `FAIL-SPLIT-04` | 输出路径或编号不符合合同 | 回到 writeback |
| `FAIL-SPLIT-05` | 执行报告缺少覆盖证据 | 补报告与返工入口 |
