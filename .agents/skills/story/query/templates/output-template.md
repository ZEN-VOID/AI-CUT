# $story-query Output Template

Use this template for evidence-backed story query responses. It mirrors `SKILL.md` `Output Contract`.

## Output Contract Alignment

| marker | binding |
| --- | --- |
| Required output | conclusion with truth role, confidence, evidence paths, gaps or conflicts, next entry |
| Output format | Markdown structured answer |
| Output path | chat by default; optional `projects/story/<项目名>/reports/query-report-YYYYMMDD.md` |
| Naming convention | saved reports use `query-report-YYYYMMDD.md` |
| Completion gate | project root and truth role are resolved, canonical carriers are checked, planned/current/validated_actual distinction is explicit |

## Standard Shape

```markdown
结论：<one or two sentences>
truth_role：<planned|current|history|validated_actual|quality|execution|manual_spec|conflict_diagnosis>
置信度：<high|medium|low>

证据：
- <path or command>: <what it proves>

边界/冲突：
- <none or specific gap>

下一入口：
- <specific stage | resume | review | 5-上下文回流 | no execution needed>
```

## Planned / Current / Actual Split

```markdown
原计划：
- <planning evidence>

当前态：
- <Cards.current_state / STATE / index evidence>

已验证实绩：
- <actualization + context-return + validation evidence, or explicit gap>
```

## Ambiguous Project Shape

```markdown
目前不能唯一定位 `projects/story/<项目名>/`。

候选项目：
- <path>

需要你补充项目名或项目根路径后，我才能继续读取规划、卡片、状态和实绩证据。
```
