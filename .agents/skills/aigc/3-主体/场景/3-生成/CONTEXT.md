# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `$aigc-scene-generation` 的经验层知识库，不是过程日志。
- 调用本目录 `SKILL.md` 时必须同时加载本文件。
- 本文件不改写 `SKILL.md` 的输入、输出和门禁；只沉淀可复用判断经验、失败模式和修复打法。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 22000
hard_limit_chars: 44000
status: ok
recommended_action: keep-generation-notes-target-scoped
last_checked_at: 2026-04-25
```

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 生成阶段重新设计场景 | 阶段边界层 | 回到上游设计文档，只抽取已有 `4. 解构` | `SKILL.md` 固定“不重新设计主体” | prompt JSON 可回指原设计稿 |
| 主图缺 JSON 记录 | 交付完整性层 | 补写同名 JSON，记录来源、prompt、mode、path | steps 将 JSON 落盘设为每次 libTV 后的 gate | 每张图片都有同名 JSON |
| 默认流程仍触发多视图 | 取消合同漂移层 | 停止 Step2，回到 `SKILL.md` 的 Multiview Cancellation Contract | Output Contract 和 review gate 固定主图-only | `-多视图` 不进入缺口、补齐目标或完成门 |
| 图片留在 provider 临时目录 | 项目持久化层 | 复制或移动最终图到项目 `3-生成` | 交付前执行 output persistence gate | 最终路径在 workspace 项目内 |
| 本地 canonical 已有但仍重复下载，或画布节点已有但项目 `场景/3-生成` 缺本地副本 | local canonical ensure 层 | 本地 canonical 已有时跳过下载/复制并记录 `already_present`；本地缺但画布已有时执行 `libtv download -p <canvas_uuid> -n <node> -o projects/aigc/<项目名>/3-主体/场景/3-生成/` | review gate 固化 `local_sync_action`、`local_sync_status`，并只在下载分支要求 `download_command` | 本地文件 stem 与 libTV 节点名一致，状态为 `already_present` / `synced` / `copied` |
| 批量任务混用提示词 | 批处理路由层 | 为每个设计文档建立独立 prompt record | 按设计文档一对一生成 `generation_profile` | 每个 JSON 的 source 不重复错配 |
| 未经许可覆盖旧资产 | 文件安全层 | 恢复或版本化输出，记录 variant | 输出合同默认版本化命名 | 同名冲突有明确用户许可或版本后缀 |
| other provider 被默认启用 | libTV 路由层 | 回到 libTV 画布 `image` 节点或询问用户 | 读取 `$libTV` 合同后再选模式 | 报告中记录 mode 与许可状态 |
| 2.0 包有目录但缺少可视化拓扑 | Skill 2.0 表达层 | 在 `SKILL.md` 和 `SKILL.md` runtime spine 补 Mermaid 主流程、状态图和失败回路 | 批量定制后检查 `Visual Maps` 与 SKILL.md Mermaid 是否存在 | `rg \"mermaid|Visual Maps\"` 能定位入口图和步骤图 |
| 多视图主图参照只记录路径未成为画布节点 | historical reference context layer | 不再修复多视图 reference；改为确认主图已进入 canonical 输出 | 多视图 reference gate 已取消 | 主图 JSON / 报告为 canonical 主图路径 |
| prompt JSON 看似完整但只是模板换名或视角词轮换 | 反模板伪差异层 | 废弃 JSON 候选，回到上游 `4. 解构` 和 LLM prompt 决策节点 | `SKILL.md` 固定 `FAIL-SCENE-GEN-PSEUDO-DIFF`，JSON schema 合规不得放行 | 主图 prompt 能回指场景专属结构、材质、光线或镜头裁决 |
| 旧 workflow 节点与 runtime-spine 节点并存 | Skill 2.0 主真源层 | 以 `SKILL.md` 末尾 `Skill 2.0 Runtime-Spine Upgrade` 中的节点表为执行主表，旧 workflow 只作兼容参考 | 升级时先补主入口必需控制块和 reference gate，不无限整包重写 | `rg "Thinking-Action Node Map|Module Trigger Matrix|Review Gate Binding" SKILL.md` 命中 |
| 跨集同主体同状态重复生成 | asset reuse layer | 扫描 `projects/aigc/<项目名>/3-主体`，复用或上传既有同名主体图 | 共享复用规则固定 `asset_reuse_decision` | `generation_skipped=true` 或 `canvas_action=uploaded_existing_image_to_canvas` |
| 同主体新状态仍用 Midjourney 重生 | state variant layer | 改用 `Lib Image`，以上一状态同主体图作为参考节点并添加状态后缀 | 状态变体 gate 固化 `generation_model_policy=lib_image_state_variant` | JSON 有 `variant_model_key`、`base_reference_node_name`、`state_variant_suffix` |

## Repair Playbook

1. 先确认目标场景对应哪一份 `2-设计` 文档，避免从清单或记忆中临时拼接主体。
2. 主图 prompt 优先使用设计文档 `## 4. 解构` 内容；不得回退读取 `## 5. 提示词设计` 的英文整合 prompt。
3. 多视图已取消；不要为 layout 或 reference 需求恢复 Step2。
4. 每次生成后立刻落同名 JSON，避免图片与 prompt 分离。
5. 当前画布缺同名主图节点时才上传本地主图；不要为历史多视图 reference 新增上传动作。
6. 批量任务按“设计文档 -> 既有主体图扫描 -> 主图节点/上传/生成 -> 主图 JSON -> review”闭环处理，失败项单独记录，不阻塞已完成项的路径回写。
7. 任一集画布节点生成、复用或上传后，先确认 `projects/aigc/<项目名>/3-主体/场景/3-生成/` 是否已有同 stem 资产；本地 canonical 已有则记录 `already_present` 并跳过下载/复制，本地缺失时才用 `libtv download` 或复制补齐。
8. 若顾问与复核流程不可用，至少执行本地 review checklist：来源、命名、JSON、参照、持久化、本地同步、边界七项。
9. 批量生成的 Skill 2.0 包若只有表格没有图，优先补 `SKILL.md` 的总览图，再补 `SKILL.md` runtime spine 的执行拓扑图；不要把完整细则倒灌回 `SKILL.md`。
10. 若主图 prompt 只是替换场景名、视角标签或同义形容词，不修几个 token；废弃该 JSON 候选并重新由 LLM 基于 `4. 解构` 裁决生成重点。

## Reusable Heuristics

- 场景生成阶段的价值是把上游设计稳定投影成可检查资产，不是重新做美术设定。
- 多视图经验仅作为历史资料保留，不参与默认生成；场景生成默认主图-only。
- 场景图默认不加人物、动物、剪影或人形阴影，除非上游设计文档明确要求。
- 主图是后续连续性的锚点；它帮助锁定场景身份，但不能覆盖设计文档的提示词真源。
- 主图作为本地参照时按需 `同画布主图节点` 可见化；否则只是路径证据，不是已传入视觉参照。
- 画布节点不是项目持久化终点；每次真实生成、复用或上传后，都要确认项目 `场景/3-生成` 目录已有同名本地资产。本地 canonical 已有就是通过条件，不应重复下载。
- 场景多视图生产板规则已停用；如未来单独恢复，需要先更新 `SKILL.md` 的取消合同。
- JSON prompt record 是复现、审查和后续视频阶段的证据，重要性不低于图片本身。
- Mermaid 图在本类技能中不是装饰，而是防止 Step1/Step2、repair、review_only 和批量汇流被批量模板抹平的路由证据。
- 场景生成 skill 升级时优先守住 source deconstruction、主图 JSON、项目持久化 gate 和多视图取消合同；旧正文可以保留，但执行主链必须回到 `SKILL.md`。
- 跨集生成时，把“同主体同状态已存在”当作通过条件而不是缺口；只有昼夜、季节、战后废墟、修复后等状态变体才生成新图，且必须使用 `Lib Image`。
