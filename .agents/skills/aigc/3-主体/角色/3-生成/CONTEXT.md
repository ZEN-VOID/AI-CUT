# Context: aigc 3-主体/角色/3-生成

本文件是 `角色/3-生成` 的经验层知识库，不是过程日志。它用于沉淀从角色设计文档到主图生图执行中的可复用经验、失败修复和边界提醒。

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
| 默认流程仍触发多视图 | 取消合同漂移层 | 停止 Step2，回到 `SKILL.md` 的 Multiview Cancellation Contract | Output Contract 和 review gate 固定主图-only | `-多视图` 不进入缺口、补齐目标或完成门 |
| 参照图缺失仍生成多视图 | Step 汇流层 | 取消该分支，只补主图或主图 JSON | Step2 作为 cancelled legacy node | 多视图缺失不构成失败 |
| libTV 输出留在临时目录 | 项目持久化层 | 按 libTV persistence 规则复制到本阶段输出目录 | 输出合同固定 canonical path | 报告路径位于 `projects/aigc/.../3-生成/` |
| 本地 canonical 已有但仍重复下载，或画布节点已有但项目 `角色/3-生成` 缺本地副本 | local canonical ensure 层 | 本地 canonical 已有时跳过下载/复制并记录 `already_present`；本地缺但画布已有时执行 `libtv download -p <canvas_uuid> -n <node> -o projects/aigc/<项目名>/3-主体/角色/3-生成/` | review gate 固化 `local_sync_action`、`local_sync_status`，并只在下载分支要求 `download_command` | 本地文件 stem 与 libTV 节点名一致，状态为 `already_present` / `synced` / `copied` |
| JSON 与图片不同名 | 命名层 | 以图片 basename 重写 JSON basename 或反向修复 | 模板中固定 output_image_path 与 output_prompt_path | `<主体ID>-<主体名称>-主图.*` 与 `<主体ID>-<主体名称>-主图.json` 配对 |
| prompt-only 被误报为已生图 | 执行证据层 | 把 verdict 改为 blocked/prompt_only，清空不存在图片路径 | review gate 区分真实图片与 dry-run JSON | 图片路径存在性检查通过或明确阻断 |
| 批量角色互相串图 | 批量隔离层 | 每个角色单独读取设计稿、单独生成 JSON 和参照图 | worker 只处理一个角色主体 | 每份 JSON 的 subject_name 与 source_design_path 匹配 |
| 脚本拼接创作提示词 | LLM-first 层 | 删除脚本生成正文逻辑，仅保留校验/manifest | scripts 分区固定机械辅助边界 | 脚本不生成 prompt_text |
| 默认执行器漂移到 nano-banana/API 子技能 | 执行器路由层 | 删除非授权执行结果，恢复为 libTV 或 prompt-only | `SKILL.md` 固定 Executor Lock，非 libTV 需要用户本轮显式点名 | 报告中能看到默认 `.agents/skills/cli/libTV` 或明确授权原文 |
| 多视图主图参照只记录路径未成为画布节点 | historical reference context layer | 不再修复多视图 reference；改为确认主图已进入 canonical 输出 | 多视图 reference gate 已取消 | 主图 JSON / 报告为 canonical 主图路径 |
| 跨集同主体同状态重复生成 | asset reuse layer | 扫描 `projects/aigc/<项目名>/3-主体`，复用或上传既有同名主体图 | 共享复用规则固定 `asset_reuse_decision` | `generation_skipped=true` 或 `canvas_action=uploaded_existing_image_to_canvas` |
| 同主体新状态仍用 Midjourney 重生 | state variant layer | 改用 `Lib Image`，以上一状态同主体图作为参考节点并添加状态后缀 | 状态变体 gate 固化 `generation_model_policy=lib_image_state_variant` | JSON 有 `variant_model_key`、`base_reference_node_name`、`state_variant_suffix` |
| prompt JSON 看似完整但只是模板换名或视角词轮换 | 反模板伪差异层 | 废弃 JSON 候选，回到上游 `4. 解构` 和 LLM prompt 决策节点 | `SKILL.md` 固定 `FAIL-CHAR-GEN-PSEUDO-DIFF`，JSON schema 合规不得放行 | 主图 prompt 能回指角色专属身份、服装、姿态或摄影裁决 |
| 生成包需要 Skill 2.0 升级但旧正文较长 | runtime-spine 追加层 | 保留旧正文，在末尾追加 `Skill 2.0 Runtime-Spine Upgrade` 小节和必需控制块 | README/CHANGELOG/test-prompts 同步；legacy workflow 作为 reference | 控制块可被 validator 发现，旧执行器锁和 同画布主图节点 规则不丢失 |

## Repair Playbook

1. 先确认目标角色是否已有 `2-设计/<角色名>.md`，并定位 `4. 解构` 区块。
2. 若设计文档缺少 `4. 解构`，停止本阶段生成，回报需要上游 `2-设计` 修复。
3. 主图 prompt 只做必要的 libTV 执行包装，不新增角色身份、服装、时代或气质。
4. 多视图已取消；不要为布局、视角、模块或一致性要求恢复 Step2。
5. 交付前必须确认 Step1 主图已经落到项目输出目录，不能使用临时预览路径作为长期证据。
6. 当前画布缺同名主图节点时才上传本地主图；不要为历史多视图 reference 新增上传动作。
7. 任一集画布节点生成、复用或上传后，先确认 `projects/aigc/<项目名>/3-主体/角色/3-生成/` 是否已有同 stem 资产；本地 canonical 已有则记录 `already_present` 并跳过下载/复制，本地缺失时才用 `libtv download` 或复制补齐。
8. 批量生成时逐角色闭环：既有主体图扫描 -> 主图节点/上传/生成 -> 主图 JSON -> 本地同步 -> review，再进入下一个角色或并行汇流。
9. 若 libTV 不可用，保留 prompt JSON 和不可用说明，不制造假图片路径。
10. 若需要重跑，先检查用户是否允许覆盖；未允许时使用版本化文件名或返回确认请求。
11. 除非用户本轮显式要求替代执行器，否则不要把“参考图/批量”理解为 nano-banana、AnyFast 或其他 API 子技能授权。
12. 若主图 prompt 只是替换角色名、视角标签或同义形容词，不修几个 token；废弃该 JSON 候选并重新由 LLM 基于 `4. 解构` 裁决生成重点。

## Reusable Heuristics

- 角色生成阶段的创造性主要在“执行与组织画面”，不在“重新发明角色”。
- 本技能默认执行器只有 `.agents/skills/cli/libTV`；执行器切换是用户授权事项，不是 agent 可自行优化的实现细节。
- 主图必须忠实于 `4. 解构`；不要在主图阶段塞入复杂面板布局，也不要回退使用旧英文整合 prompt。
- 多视图模板和生产板经验仅作为历史资料保留，不参与默认生成。
- 单主体图是 continuity anchor；后续阶段若需要参考主体，应优先使用主图。
- 单主体图作为本地参照时按需 `同画布主图节点` 可见化；否则只是路径证据，不是已传入视觉参照。
- 画布节点不是项目持久化终点；每次真实生成、复用或上传后，都要确认项目 `角色/3-生成` 目录已有同名本地资产。本地 canonical 已有就是通过条件，不应重复下载。
- JSON prompt 是可复现证据，不是美术散文；路径、来源、模式和最终 prompt 必须清楚。
- 对角色名做安全文件名转换时，要在 JSON 中保留原名，避免后续资产回链断裂。
- 当生成技能包需要快速升级时，优先保持 Executor Lock、prompt_only、同画布主图节点 和 anti-pseudo-diff 四个门不变，再补 runtime-spine 表格。
- 跨集生成时，把“同主体同状态已存在”当作通过条件而不是缺口；只有服装、年龄、受伤、战斗前后等状态变体才生成新图，且必须使用 `Lib Image`。
