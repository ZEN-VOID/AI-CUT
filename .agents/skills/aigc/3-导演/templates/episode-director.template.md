# Episode Director Template

```md
---
项目名: <项目名>
集数: 第N集
stage: 3-导演
source_screenplay_path: projects/aigc/<项目名>/2-编剧/第N集.md
output_path: projects/aigc/<项目名>/3-导演/第N集.md
directorial_authorship: required
dialogue_lock: true
field_order_policy: preserve_upstream
controlled_enrichment: none | controlled_supportive
review_verdict: pending
---

# 第N集 导演稿

【剧本正文】

> 保留上游字段结构，在既有字段内部嵌入导演判断；不得输出本提示说明。
```
