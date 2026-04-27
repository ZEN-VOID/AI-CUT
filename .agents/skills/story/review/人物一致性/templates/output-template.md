# Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 人物一致性 `dimension_packet` 与 `dimension_report_ref`。 |
| Output format | Markdown 维度报告 + 结构化 packet。 |
| Output path | `projects/story/<项目名>/review/第V卷/人物一致性.md`。 |
| Naming convention | 文件名按父层 registry `report_filename`。 |
| Completion gate | packet 不写父层 gate 字段，人物问题可定位到返工 step。 |
