# Episode Batch Chain

适用于多个分集的批处理。

## Fixed Context

- 每阶段按目标分集并发启动 subagents。
- 阶段汇流时允许把通过集和失败集分开记录；是否让通过集进入下一阶段，应由用户输入或批处理策略明确。
- completion report 必须包含 batch summary：total、passed、failed、skipped、current frontier。

## Gate Bias

默认不让失败集进入下游。若用户允许部分推进，通过集可以继续，但失败集必须保留 retry route。
