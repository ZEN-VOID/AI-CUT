# Episode Director Layer Template

```md
---
项目名: <项目名>
集数: 第N集
stage: 2-编导
layer: director
source_script_layer_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/2-编导/第N集.md
directorial_authorship: required
dialogue_lock: true
field_order_policy: preserve_upstream
controlled_enrichment: none | controlled_supportive
review_verdict: pending
---

# 第N集 编导稿：导演层

【剧本正文】

> 保留 `2-编导` script layer 字段结构，在既有字段内部嵌入导演判断；不得输出本提示说明。
```
