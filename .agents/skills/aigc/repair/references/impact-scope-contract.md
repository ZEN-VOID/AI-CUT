# Impact Scope Contract

本文件定义 `aigc-repair` 在局部或整体调整前必须锁定的影响范围。通用矩阵属于技能规则层真源，项目特例只能进入项目 `CONTEXT/`、`MEMORY.md` 或本次 repair report。

## Impact Surface

| surface | required question | canonical examples |
| --- | --- | --- |
| project memory | 该改动是否属于长期偏好、禁区或稳定口味 | `projects/aigc/<项目名>/MEMORY.md` |
| project context | 项目共享事实、参考片解析、风格资料是否要同步 | `projects/aigc/<项目名>/CONTEXT/` |
| init source | north_star、team、全局风格、题材元素是否是错误源 | `0-初始化/north_star.yaml`、`team.yaml` |
| episode source | 原文切集是否错位、漏段或误归集 | `1-分集/第N集.md` |
| script source | 剧情事实、对白、slugline、声画配对是否错误 | `2-编剧/第N集.md` |
| director source | 戏剧问题、视觉主轴、氛围和高潮处理是否需要修 | `3-导演/第N集.md` |
| performance source | 表演动作、心理可见化、场面调度是否需要修 | `4-表演/第N集.md` |
| cinematography source | 景别、运镜、焦点、时长、连续性锚点是否需要修 | `5-摄影/第N集.md` |
| grouping source | 分镜组边界、入场/出场、统计、组间桥接是否需要修 | `6-分组/第N集.md` |
| design assets | 场景、角色、道具清单/设计/生成是否要同步 | `7-设计/**` |
| image outputs | 图像 prompt、reference manifest、成图和报告是否要失效或重做 | `8-图像/**` |
| video outputs | 视频任务、首帧/参照、MP4、生成报告是否要失效或重做 | `9-视频/**` |
| review and state | 审片、review gate、STATE、governance state 是否要重验 | `10-审片/**`、`review/**`、`STATE.json`、`governance-state.yaml` |

## Universal Type Matrix

| 当修改对象是 | 必查上游 | 必查同层/当前 | 必查下游/未来 | 必查验收 |
| --- | --- | --- | --- | --- |
| 剧情事实 / 对白 / 顺序 | `1-分集`、`2-编剧` | 当前集、相邻场景、字段纯度 | `3-导演` 到 `10-审片` 已产物和后续生成约束 | 事实保真、对白不漂移、顺序一致 |
| 导演意图 / 氛围 / 视觉主轴 | `3-导演`、north_star 风格 | 当前场景、高潮画面、五感意境 | `4-表演`、`5-摄影`、`6-分组`、图像/视频 prompt | 意图可见、非空泛口号、下游可执行 |
| 表演动作 / 心理可见化 | `4-表演`、`3-导演` | 当前画面句、角色状态、场面调度 | `5-摄影` 镜头、`6-分组` 组内动作、视频表现 | 表演具体、动机连续、不改剧情事实 |
| 镜头语言 / 时长 / 连续性 | `5-摄影`、`4-表演` | 当前分镜明细、相邻镜头 | `6-分组`、`8-图像`、`9-视频` | 景别运镜可执行、时长合理、连续性成立 |
| 分镜组 / 组间桥接 | `6-分组`、`5-摄影` | 组 ID、入场/出场、统计 YAML | storyboard、视频任务、审片 finding | 组边界、桥接、统计和生成消费一致 |
| 场景 / 角色 / 道具资产 | `7-设计`、`6-分组`、项目 CONTEXT | 清单、设计稿、参照图、alias | 图像 prompt、视频 reference、后续分镜组 | 资产身份、造型、用途和引用路径一致 |
| 图像 / storyboard | `8-图像` leaf、`6-分组`、`7-设计` | prompt、reference manifest、结果报告 | `9-视频` 首帧/参照、`10-审片` | 成图是否消费正确源，不用文字修补图像缺陷 |
| 视频 / MP4 | `9-视频` leaf、`8-图像`、`6-分组` | 任务 JSON、素材、生成报告、实际视频 | `10-审片` 和 repair route | 缺陷定位到生成、图像、分组或摄影 owner |
| 中文表达 / 友好润色 | owning stage 文本合同、项目 MEMORY | 当前段落、相邻语气、字段格式 | 后续 prompt、provider messages、review | 只润表达，不改事实、编号、字段和引用 |
| 创意激发 / 候选增强 | north_star、阶段源合同、用户禁区 | 候选点与原目标的映射 | 需要用户选择或 owning stage 吸收 | 创意可执行、有边界、不自动成为真源 |

## Minimum Impact Map

```yaml
impact_map:
  upstream_truth:
    - path: ""
      status: affected | unaffected | unknown
      reason: ""
  same_layer_neighbors:
    - path: ""
      reason: ""
  current_locality:
    path: ""
    repair_intent: ""
  downstream_existing:
    - path: ""
      action: inspect | rewrite | invalidate | regenerate | unchanged
  generated_assets:
    - path: ""
      action: preserve | invalidate | regenerate | review_only
  future_constraints:
    - path: ""
      action: update | preserve | add_guardrail
  review_state:
    - path: ""
      gate_action: rerun | invalidate | preserve | update
```

## Scope Rules

1. 旧口径在上游源层命中时，默认先修上游，除非用户明确要求只做实验性局部草稿。
2. 旧口径只在某个生成 handoff 中命中时，优先修 owning leaf 的 prompt / manifest / task，而不是反向改上游事实。
3. 已生成图像或视频不直接文本编辑；repair 只能保留、失效、重建任务或进入 review route。
4. 中文润色默认不改变编号、字段名、YAML、分镜 ID、路径、对白文本和结构化引用。
5. 创意激发输出默认是候选建议，只有用户授权或 owning stage 吸收后才成为 canonical truth。
