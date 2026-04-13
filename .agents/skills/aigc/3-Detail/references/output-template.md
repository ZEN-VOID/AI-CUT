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
- quantizer verdict
- validator verdict
- 通过 / 阻塞 verdict
- review 结论
- audit 结论
- 返工入口
- 默认下一入口

## `acceptance_notes` 最小合同

至少覆盖以下四类中的两类：

- preset / lock-axis 是否被遵守
- 哪些字段族在本轮被更新
- 哪些字段族被刻意保留为空或保持原样
- 下游 `4-Design` 消费时的注意事项

若本轮命中组已形成有效 `分镜明细[]`，则还应优先说明：

- `组间设计.出场角色及穿搭` 是否已回填
- 若未回填，阻塞点是什么

## 写回顺序

1. 更新 `metadata`
2. patch `final_output.main_content.分镜组列表`
3. 更新 `acceptance_notes`
4. 写 `validation-report.md`
5. 仅当 `第N集.json` 与 `validation-report.md` 都已真实存在时，才允许同步 `projects/<项目名>/project_state.yaml` 为 `detail_complete_validated` 并推荐进入 `4-Design`

## Stage Closure Sync

- `project_state.yaml` 只能在以下条件同时满足后，才允许宣称本阶段完成：
  - `projects/<项目名>/3-Detail/第N集.json` 已写回
  - `projects/<项目名>/3-Detail/validation-report.md` 已写回
  - `scripts/validate_detail_output.py` 已返回 `PASS`
- 如果 `project_state.yaml` 已声称完成，但上述任一产物缺失，应视为 runtime drift，先重建 artifact，再改状态。

## authoritative 量化校验

- `validation-report.md` 应显式记录：
  - `scripts/detail_density_quantizer.py` 的格式档位、节奏档位与镜数分布
  - `scripts/validate_detail_output.py` 的 pass / fail 结论
- 若 quantizer 与 episode JSON 不一致，不得宣布阶段完成。
- 若 validator 检测到同一组内 shot-level 业务字段存在过量逐镜原句复制，也不得宣布阶段完成。
- 若 validator 检测到 `组间设计.出场角色及穿搭` 缺失或格式不满足 `角色名-服装简述` 的组级摘要要求，也不得宣布阶段完成。

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
