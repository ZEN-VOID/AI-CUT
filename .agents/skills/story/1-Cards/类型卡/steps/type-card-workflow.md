# Type Card Workflow

```mermaid
flowchart TD
    A["Read current cards truth"] --> B["Lock story promise"]
    B --> C["Narrow genre corridor"]
    C --> D["Define forbidden zone and navigation"]
    D --> E["Assemble type-card payload"]
    E --> F["Parent writer and planning import gate"]
```

| step_id | action | evidence | gate |
| --- | --- | --- | --- |
| `T1` | 回读 init 与既有 cards | `input_trace` | cards truth 最新 |
| `T2` | 锁定读者承诺和平台承诺 | `promise_note` | 承诺可执行 |
| `T3` | 确定主副题材和禁飞区 | `corridor_note` | 题材不漂移 |
| `T4` | 生成 payload 与 planning import projection | `type_payload` | 只写类型卡 owned slots |
