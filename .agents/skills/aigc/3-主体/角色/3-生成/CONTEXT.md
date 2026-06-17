# Context: aigc 3-主体/角色/3-生成

本文件是 `角色/3-生成` 的经验层知识库，不是过程日志。它用于沉淀从角色设计文档到主图、多视图生图执行中的可复用经验、失败修复和边界提醒。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 24000
hard_limit_chars: 48000
status: ok
recommended_action: keep-generation-scoped
last_checked_at: 2026-04-25
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 主图重新设计角色 | 上游真源层 | 回到 `2-设计/<角色名>.md` 的 `4. 解构`，删除新增设定 | 主图 JSON 固定记录 source_design_path 与 source_deconstruction_section | prompt 可回指上游设计稿 |
| 多视图模板压过角色事实 | 模板边界层 | 将模板文字改回 layout-only，保留角色身份与服装来自上游 | `critical_requirements` 明确设计文档优先 | 多视图 prompt 没有替换身份、时代、服装事实 |
| 参照图缺失仍生成多视图 | Step 汇流层 | 先补主图或切换 prompt-only 不可用说明 | Step2 gate 必查 reference_image_path | 多视图 JSON 指向存在的主图路径 |
| libTV 输出留在临时目录 | 项目持久化层 | 按 libTV persistence 规则复制到本阶段输出目录 | 输出合同固定 canonical path | 报告路径位于 `projects/aigc/.../3-生成/` |
| 本地 canonical 已有但仍重复下载，或画布节点已有但项目 `角色/3-生成` 缺本地副本 | local canonical ensure 层 | 本地 canonical 已有时跳过下载/复制并记录 `already_present`；本地缺但画布已有时执行 `libtv download -p <canvas_uuid> -n <node> -o projects/aigc/<项目名>/3-主体/角色/3-生成/` | review gate 固化 `local_sync_action`、`local_sync_status`，并只在下载分支要求 `download_command` | 本地文件 stem 与 libTV 节点名一致，状态为 `already_present` / `synced` / `copied` |
| JSON 与图片不同名 | 命名层 | 以图片 basename 重写 JSON basename 或反向修复 | 模板中固定 output_image_path 与 output_prompt_path | `<主体ID>-<主体名称>-主图.*` 与 `<主体ID>-<主体名称>-主图.json` 配对 |
| prompt-only 被误报为已生图 | 执行证据层 | 把 verdict 改为 blocked/prompt_only，清空不存在图片路径 | review gate 区分真实图片与 dry-run JSON | 图片路径存在性检查通过或明确阻断 |
| 批量角色互相串图 | 批量隔离层 | 每个角色单独读取设计稿、单独生成 JSON 和参照图 | worker 只处理一个角色主体 | 每份 JSON 的 subject_name 与 source_design_path 匹配 |
| 脚本拼接创作提示词 | LLM-first 层 | 删除脚本生成正文逻辑，仅保留校验/manifest | scripts 分区固定机械辅助边界 | 脚本不生成 prompt_text |
| 默认执行器漂移到 nano-banana/API 子技能 | 执行器路由层 | 删除非授权执行结果，恢复为 libTV 或 prompt-only | `SKILL.md` 固定 Executor Lock，非 libTV 需要用户本轮显式点名 | 报告中能看到默认 `.agents/skills/cli/libTV` 或明确授权原文 |
| 多视图主图参照只记录路径未成为画布节点 | reference context layer | 生成 Step2 前确保主图已是同一 libTV 画布图片节点；本地路径先 `libtv upload` | Step2 gate 固化 `reference_node_name` 与 `reference_context_status` | 多视图 JSON / 报告为 `linked_in_libtv_canvas` |
| 跨集同主体同状态重复生成 | asset reuse layer | 扫描 `projects/aigc/<项目名>/3-主体`，复用或上传既有同名主体图 | 共享复用规则固定 `asset_reuse_decision` | `generation_skipped=true` 或 `canvas_action=uploaded_existing_image_to_canvas` |
| 同主体新状态仍用 Midjourney 重生 | state variant layer | 改用 `Lib Image`，以上一状态同主体图作为参考节点并添加状态后缀 | 状态变体 gate 固化 `generation_model_policy=lib_image_state_variant` | JSON 有 `variant_model_key`、`base_reference_node_name`、`state_variant_suffix` |
| prompt JSON 看似完整但只是模板换名或视角词轮换 | 反模板伪差异层 | 废弃 JSON 候选，回到上游 `4. 解构` 和 LLM prompt 决策节点 | `SKILL.md` 固定 `FAIL-CHAR-GEN-PSEUDO-DIFF`，JSON schema 合规不得放行 | 主图/多视图 prompt 能回指角色专属身份、服装、姿态或摄影裁决 |
| 生成包需要 Skill 2.0 升级但旧正文较长 | runtime-spine 追加层 | 保留旧正文，在末尾追加 `Skill 2.0 Runtime-Spine Upgrade` 小节和必需控制块 | README/CHANGELOG/test-prompts 同步；legacy workflow 作为 reference | 控制块可被 validator 发现，旧执行器锁和 同画布主图节点 规则不丢失 |

## Repair Playbook

1. 先确认目标角色是否已有 `2-设计/<角色名>.md`，并定位 `4. 解构` 区块。
2. 若设计文档缺少 `4. 解构`，停止本阶段生成，回报需要上游 `2-设计` 修复。
3. 主图 prompt 只做必要的 libTV 执行包装，不新增角色身份、服装、时代或气质。
4. 多视图 prompt 可以增加布局、视角、模块和一致性要求，但不得覆盖上游设计事实。
5. Step2 前必须确认 Step1 主图已经落到项目输出目录，不能使用临时预览路径作为长期参照。
6. Step2 调用 libTV 画布 `image` 节点前必须确认主图已是同一画布节点；只有路径存在还不够，当前画布缺同名节点时才上传本地图。
7. 任一集画布节点生成、复用或上传后，先确认 `projects/aigc/<项目名>/3-主体/角色/3-生成/` 是否已有同 stem 资产；本地 canonical 已有则记录 `already_present` 并跳过下载/复制，本地缺失时才用 `libtv download` 或复制补齐。
8. 批量生成时逐角色闭环：既有主体图扫描 -> 主图节点/上传/生成 -> 主图 JSON -> 本地同步 -> 多视图 JSON -> 多视图图像 -> 本地同步 -> review，再进入下一个角色或并行汇流。
9. 若 libTV 不可用，保留 prompt JSON 和不可用说明，不制造假图片路径。
10. 若需要重跑，先检查用户是否允许覆盖；未允许时使用版本化文件名或返回确认请求。
11. 除非用户本轮显式要求替代执行器，否则不要把“多视图/参考图/批量”理解为 nano-banana、AnyFast 或其他 API 子技能授权。
12. 若主图/多视图 prompt 只是替换角色名、视角标签或同义形容词，不修几个 token；废弃该 JSON 候选并重新由 LLM 基于 `4. 解构` 裁决生成重点。

## Reusable Heuristics

- 角色生成阶段的创造性主要在“执行与组织画面”，不在“重新发明角色”。
- 本技能默认执行器只有 `.agents/skills/cli/libTV`；执行器切换是用户授权事项，不是 agent 可自行优化的实现细节。
- 主图越忠实于 `4. 解构`，多视图参照越稳定；不要在主图阶段塞入复杂面板布局，也不要回退使用旧英文整合 prompt。
- 多视图模板应像制作部门的审阅板：强调同一身份、同一服装体系、同一材质逻辑和可验证背面/侧面。
- 角色多视图应先应用 `subject_invariant_lock`，再排 front / three-quarter / side / rear turnaround；表情、姿态和细节 callout 只能服务身份证明，不应挤占主 turnaround。
- 角色多视图生产板必须有顶左身份牌：图中优先显示短 ASCII 角色 ID，完整角色名进入 JSON；若模型文字不稳，应保留干净 badge plate 供后期叠字。
- 单主体图是 continuity anchor；即使多视图有更多模块，也应服从主图的脸、发型、体型和服装主轮廓。
- 单主体图作为本地参照时必须先 `同画布主图节点` 可见化；否则只是路径证据，不是已传入视觉参照。
- 画布节点不是项目持久化终点；每次真实生成、复用或上传后，都要确认项目 `角色/3-生成` 目录已有同名本地资产。本地 canonical 已有就是通过条件，不应重复下载。
- JSON prompt 是可复现证据，不是美术散文；路径、来源、模式和最终 prompt 必须清楚。
- 对角色名做安全文件名转换时，要在 JSON 中保留原名，避免后续资产回链断裂。
- 当生成技能包需要快速升级时，优先保持 Executor Lock、prompt_only、同画布主图节点 和 anti-pseudo-diff 四个门不变，再补 runtime-spine 表格。
- 跨集生成时，把“同主体同状态已存在”当作通过条件而不是缺口；只有服装、年龄、受伤、战斗前后等状态变体才生成新图，且必须使用 `Lib Image`。
