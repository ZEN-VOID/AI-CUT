# Episode Performance Layer Template

```md
---
项目名: <项目名>
集数: 第N集
stage: 2-编导
layer: performance
source_director_layer_path: projects/aigc/<项目名>/2-编导/第N集.md
output_path: projects/aigc/<项目名>/2-编导/第N集.md
performance_craft: required
dialogue_performance: required
long_dialogue_delivery: required
dialogue_lock: true
field_order_policy: preserve_upstream
review_verdict: pending
---

# 第N集 编导稿：表演层

【剧本正文】

> 保留 `2-编导` director layer 字段结构，在既有字段内部嵌入表演工艺；每段对白写清语气/情绪/状态，关键对白就近承托气口、断句、停顿、声线、重音、尾音或对手反应；若上游含 long_dialogue_beat_map，逐 beat 形成 long_dialogue_delivery_map，不改写、不重切原文节拍；不得输出本提示说明。
```
