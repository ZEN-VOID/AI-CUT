# Canonical Output Contract

## 主产物

- `projects/<项目名>/3-Detail/第N集.json`

必须满足：

1. 继续服从 `.agents/skills/aigc/_shared/director_episode_output.schema.json`
2. 只做 patch-in-place，不整稿覆盖未命中切片
3. `metadata.document_phase` 保持在 `detail_in_progress` 或 `ready`

## 验收产物

- `projects/<项目名>/3-Detail/validation-report.md`

至少包含：

- 本轮 scope
- 通过 / 阻塞 verdict
- review 结论
- audit 结论
- 返工入口
- 默认下一入口

## `thinking_chain` 最小合同

- `thinking_goal`
  - 说明本轮 detail 的目标切片与为什么进入该链路
- `key_steps`
  - 只记录父 skill 的关键收束判断，不记录每条能力链的原始长推理
- `conclusion`
  - 说明本轮为什么允许写回或为什么阻塞

## `acceptance_notes` 最小合同

至少覆盖以下四类中的两类：

- preset / lock-axis 是否被遵守
- 哪些字段族在本轮被更新
- 哪些字段族被刻意保留为空或保持原样
- 下游 `4-Design` 消费时的注意事项

## 写回顺序

1. 更新 `metadata`
2. 更新 `thinking_chain`
3. patch `final_output.main_content.分镜组列表`
4. 更新 `acceptance_notes`
5. 写 `validation-report.md`

## 可选镜头描述子槽

若当前项目、下游模块或用户显式要求结构化镜头标签，可在每个 `shot_detail` 里额外补以下可选字段：

- `景别`
- `镜头属性`
- `镜头框架`
- `镜头类型`
- `镜头视角`

约束：

- 这五个字段都属于 `FIELD-DETAIL-05 / structural_staging_engine`，不是 `运镜手法` 或 `摄影美学` 的替身。
- `镜头框架` 应优先承接“主体·陪体·背景关系 + 构图布局/方式”的压缩结果。
- 若只写 `分镜表现` 不写这五个字段，旧数据仍视为有效。
- 若写这五个字段，则必须与 `分镜表现` 同步，不得互相矛盾。

## 下游 handoff

- 默认下一入口：`4-Design`
- `4-Design / 5-Image / 6-Video / query / review` 均应读取这份 `第N集.json`
- 不再允许依赖平行 sidecar 或已删除的外置制作组文档
