# Review Contract: D-主板混合参照

本 review gate 只裁决 `D-主板混合参照` 的组级视频 prompt、混合参照、Dreamina 计划、队列和项目持久化，不改写 `4-分组` 主真源。

## Review Checklist

1. 运行 Skill 2.0 结构校验。
2. 检查 `第N集-hybrid-group-index.json` 是否可回指 `4-分组/第N集.md` 的 `## group_id`。
3. 检查 prompt 是否以固定总参照说明起笔。
4. 检查故事板参照是否来自 `6-图像/B-分镜故事板`，且只作为 `storyboard_total_reference`。
5. 检查主体参照是否只来自组底 YAML 与 `5-设计/*/3-生成` 的真实图片。
6. 检查每个已绑定主体是否在对应主体信息后出现 `@参照图`、`@图片路径` 或等价 Dreamina marker。
7. 检查缺图主体、缺故事板或图片超限是否写入 manifest、submit plan 和报告。
8. 检查 Dreamina command type：有任一参照图用 `multimodal2video`，无图用 `text2video`，默认不用 `image2video`。
9. 检查提交前是否有 `dreamina user_credit` 策略；执行生成时是否有 queue ledger 与 submit_id / blocked reason。
10. 检查输出路径是否全部位于 `projects/aigc/<项目名>/7-视频/D-主板混合参照/第N集/`。

## Verdict

| verdict | meaning |
| --- | --- |
| `pass` | 全部必需 gate 通过 |
| `pass_with_todo` | 非阻断缺图或待查询事项已记录 |
| `fail` | prompt、参照、命令、路径或队列任一硬门失败 |

## Failure Routing

| fail code | rework |
| --- | --- |
| `FAIL-VIDHYB-INPUT` | `types/type-map.md` |
| `FAIL-VIDHYB-GROUP` | `references/group-source-extraction.md` |
| `FAIL-VIDHYB-PROMPT` | `references/hybrid-prompt-assembly-contract.md` |
| `FAIL-VIDHYB-REF` | `references/hybrid-reference-binding.md` |
| `FAIL-VIDHYB-DREAMINA` | `references/dreamina-handoff.md` |
| `FAIL-VIDHYB-REPORT` | `templates/output-template.md` |
