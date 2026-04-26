# AIGC Resume Output Template

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 输出一次恢复裁决包，包含项目根、证据、模式、缺口、唯一下一入口和安全边界。 |
| Output format | Markdown 用户-facing 报告；必要时附 YAML/JSON patch 建议。 |
| Output path | 默认不落盘；若用户要求报告，写入 `projects/aigc/<项目名>/resume/resume-report-YYYYMMDD.md`。 |
| Naming convention | 恢复报告使用 `resume-report-YYYYMMDD.md`；模式使用 ASCII-safe mode id。 |
| Completion gate | 必须通过 `review/resume-review-gate.md` 的项目根、证据链、风险、gate 和唯一入口检查。 |

## Template

```markdown
**恢复结论**
项目根：`projects/aigc/<项目名>/`
恢复模式：`<resume_mode>`
风险等级：`<risk_level>`

证据：
- `<evidence item>`

缺口：
- `<blocker or required repair>`

唯一下一入口：
`<skill or runtime path>`

原因：
`<why this entry is safe>`

安全边界：
- 不执行 destructive Git 或资产删除动作。
- 不替阶段技能写 canonical 业务真稿。
```
