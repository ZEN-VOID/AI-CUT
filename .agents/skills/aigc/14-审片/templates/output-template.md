# Output Template

## Output Contract Alignment

- Required output: 审片 verdict、入口摘要、真实视频内容分析、证据摘要、方法选择、prompt 匹配、创作质量、示例校准、finding list、operation 设计、顾问摘要、落盘动作、Execution Decision Trace、验证结果和残留风险。
- Output format: 面向用户的简短结论，加项目内 `14-审片/第N集/<group_id>[-variant]-审片.md` 报告；授权时附 `10-分组`、LibTV rerun 或源层 patch。
- Output path: `projects/aigc/<项目名>/14-审片/第N集/<group_id>[-variant]-审片.md`，证据目录为 `projects/aigc/<项目名>/14-审片/第N集/evidence/<group_id>/`。
- Naming convention: 报告使用 `<group_id>[-variant]-审片.md`；视频使用 `<group_id>[-variant].mp4`；task id、node key、result URL 只进入报告或 queue 证据。
- Completion gate: 真实视频可读、真实内容摘要可回指证据、分镜组真源可回指、方法选择和 finding 完整、operation 可执行、授权 patch 范围正确、final verdict 唯一。
- Module trigger evidence: 报告列出命中的 `Module Trigger Matrix` 行；未触发的模块写明 `none`。
- Business analysis evidence: 报告说明 business goal、object、constraint、success criteria 和 topology fit 是否满足。
- Quant criteria evidence: 报告说明 action scope、evidence count、pass threshold、retry limit 和 fallback evidence。
- Attention evidence: 报告说明注意力锚点、漂移信号和再集中入口；无漂移时写 `none observed`。
- Checkpoint evidence: 报告说明 CHK-SCOPE、CHK-SEMANTIC、CHK-VALIDATION、CHK-DARWIN 状态。
- Prompt eval evidence: 结构升级或回归评估时列出 `test-prompts.json` ids 与 `eval_mode`；普通审片写 `not run`。

## Final Output

写入用户可读结论、报告路径、授权改动、验证结果和残留风险。

## Evidence

列出视频元数据、关键帧或联系表、音频说明、source anchor、prompt evidence、example evidence 和 LibTV query evidence。

## Review Result

列出 gate result、fail code 返工记录、Execution Decision Trace 和 final verdict。
