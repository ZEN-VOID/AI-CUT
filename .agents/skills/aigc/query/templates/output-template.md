# $aigc-query Output Template

Use this template for evidence-backed query responses. It mirrors `SKILL.md` `Output Contract`.

## Output Contract Alignment

| marker | binding |
| --- | --- |
| Required output | conclusion with confidence and drift status, evidence paths, gaps or conflicts, next entry |
| Output format | Markdown structured answer |
| Output path | chat by default; optional `projects/aigc/<项目名>/reports/query-report-YYYYMMDD.md` |
| Naming convention | saved reports use `query-report-YYYYMMDD.md` |
| Completion gate | project root and truth role are resolved, canonical carriers are checked, validation distinction is explicit |

## Standard Shape

```markdown
结论：<one or two sentences>
置信度：<high|medium|low>；漂移状态：<none|path-drift|registry-drift|validation-gap|unknown>

证据：
- <path>: <what it proves>

缺口/冲突：
- <none or specific gap>

下一入口：
- <root aigc | specific stage | resume | review | no execution needed>
```

## Ambiguous Project Shape

```markdown
目前不能唯一定位 `projects/aigc/<项目名>/`。

候选项目：
- <path>

需要你补充项目名或项目根路径后，我才能继续读取阶段产物和治理证据。
```
