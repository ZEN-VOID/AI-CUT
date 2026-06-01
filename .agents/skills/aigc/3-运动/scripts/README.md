# Scripts

本目录只承载 `3-运动` 的机械辅助脚本，不承担运动描写、状态推导或正文扩写主创工作。

## Available Checks

```bash
python3 scripts/validate_motion_enrichment.py projects/aigc/<项目名>/3-运动/第N集.md
```

该脚本只检查：

- frontmatter 或正文是否标记 `stage: 3-运动`
- 是否误新增独立 `运动强化：` 或对照标签字段
- 是否存在 `motion_state_ledger` 或执行报告证据
- 是否存在 `group_reference_profile`、`Scene / Segment Reference Profile` 或场景/动作段参照系证据
- 是否出现明显下游越权词，如 `分镜N`、`机位`、`景别`、`运镜`

脚本结果不能替代 `review/review-contract.md` 的语义验收。
