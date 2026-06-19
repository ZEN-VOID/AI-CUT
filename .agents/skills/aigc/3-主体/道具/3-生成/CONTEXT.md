# Context: aigc 道具 3-生成

本文件是 `$aigc-prop-generation` 的经验层知识库，不是过程日志。它沉淀道具生成阶段消费上游设计文档、调用 libTV、保存主图资产时的可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: initial
recommended_action: keep-generation-heuristics-target-scoped
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 系统预防修复 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-PROP-GEN-01` | 生成阶段开始补写研究、物语或解构 | 阶段越界 | 回到只消费 `2-设计` 的 `4. 解构` | 在 `SKILL.md` 和 `references/` 固定非目标 | 无 `2-设计` 文件改动 |
| `TM-PROP-GEN-02` | 默认流程仍触发多视图 | 取消合同漂移层 | 停止 Step2，回到 `SKILL.md` 的 Multiview Cancellation Contract | Output Contract 和 review gate 固定主图-only | `-多视图` 不进入缺口、补齐目标或完成门 |
| `TM-PROP-GEN-03` | JSON 提示词无法追溯来源 | 证据字段缺失 | 补 `source_design_doc`、`source_deconstruction_section`、`output_image` | 模板固定追溯字段 | JSON 能回指上游 Markdown 和输出图 |
| `TM-PROP-GEN-04` | 普通生成任务误用非 `.agents/skills/cli/libTV` 执行器，例如直接调用 nano-banana / Dreamina / AnyFast 子技能 | 执行入口漂移 | 删除或撤回非默认执行器产物，回到 `.agents/skills/cli/libTV` 唯一默认入口 | 每次读取 libTV 合同，并在 `type_profile` 中显式保持 `allow_external_provider: false` | 无未经用户显式要求的外部 provider 产物 |
| `TM-PROP-GEN-05` | 文件名丢失 `-主图` | 命名门禁缺失 | 按 Output Contract 重命名并同步 JSON | review gate 检查命名后缀 | 图像与 JSON 同 stem |
| `TM-PROP-GEN-06` | 输出只停在 provider 临时目录 | 持久化缺口 | 复制最终资产到项目 canonical 输出目录 | 把项目路径写入 prompt/result 记录 | 报告路径在 workspace 内 |
| `TM-PROP-GEN-06A` | 本地 canonical 已有但仍重复下载，或画布节点已有但项目 `道具/3-生成` 缺本地副本 | local canonical ensure 层 | 本地 canonical 已有时跳过下载/复制并记录 `already_present`；本地缺但画布已有时执行 `libtv download -p <canvas_uuid> -n <node> -o projects/aigc/<项目名>/3-主体/道具/3-生成/` | review gate 固化 `local_sync_action`、`local_sync_status`，并只在下载分支要求 `download_command` | 本地文件 stem 与 libTV 节点名一致，状态为 `already_present` / `synced` / `copied` |
| `TM-PROP-GEN-07` | Skill 2.0 文件齐全但执行者仍看不出分支与汇流 | 拓扑表达不足 | 在 `SKILL.md`、`SKILL.md` runtime spine、`types/` 或 `review/` 补 Mermaid 图和节点交接表 | 结构校验之外增加语义 review gate | 可从图表追踪 single/batch/prompt-only/repair/review 路径 |
| `TM-PROP-GEN-08` | 多视图主图参照只记录路径未成为画布节点 | historical reference context layer | 不再修复多视图 reference；改为确认主图已进入 canonical 输出 | 多视图 reference gate 已取消 | 主图 JSON / 报告为 canonical 主图路径 |
| `TM-PROP-GEN-09` | prompt JSON 看似完整但只是模板换名、换材质或视角词轮换 | 反模板伪差异层 | 废弃 JSON 候选，回到上游 `4. 解构` 和 LLM prompt 决策节点 | `SKILL.md` 固定 `FAIL-PROP-GEN-PSEUDO-DIFF`，JSON schema 合规不得放行 | 主图 prompt 能回指道具专属形制、材质、功能或工艺裁决 |
| `TM-PROP-GEN-10` | `SKILL.md` runtime spine 的流程图与 `SKILL.md` 节点表不一致 | runtime spine 漂移层 | 以 `SKILL.md` 的 Thinking-Action Node Map 和 Visual Maps 为准；`SKILL.md` runtime spine 只作 legacy read-only reference | Module Loading Matrix 固定 `SKILL.md` runtime spine 禁止第二执行链 | main prompt -> main image -> review 可在 `SKILL.md` 跟踪 |
| `TM-PROP-GEN-11` | 缺 `test-prompts.json` 导致 prompt-only / repair 回归不可复现 | 评估资产层 | 新增测试 prompts 覆盖 single generation、prompt-only、reference repair、reject-template | 标准变更同步 prompts | JSON schema 可解析且至少 3 条 |
| `TM-PROP-GEN-12` | 跨集同主体同状态重复生成 | asset reuse layer | 扫描 `projects/aigc/<项目名>/3-主体`，复用或上传既有同名主体图 | 共享复用规则固定 `asset_reuse_decision` | `generation_skipped=true` 或 `canvas_action=uploaded_existing_image_to_canvas` |
| `TM-PROP-GEN-13` | 同主体新状态仍用 Midjourney 重生 | state variant layer | 改用 `Lib Image`，以上一状态同主体图作为参考节点并添加状态后缀 | 状态变体 gate 固化 `generation_model_policy=lib_image_state_variant` | JSON 有 `variant_model_key`、`base_reference_node_name`、`state_variant_suffix` |

## Repair Playbook

1. 先确认问题属于输入设计文档、主图生成、JSON 追溯、输出命名、路径持久化、多视图取消合同还是 libTV 路由。
2. 若缺上游设计文档，回到 `道具/2-设计`；不要在生成阶段临时创作主体设计。
3. 若设计文档缺 `4. 解构`，暂停生图并要求修复上游设计文档。
4. 若执行链恢复多视图，优先回到取消合同并停止 Step2，而不是强化参照图。
5. 当前画布缺同名主图节点时才上传本地主图；不要为历史多视图 reference 新增上传动作。
6. 若图像已生成但未落盘到项目目录，按 `$libTV` 的 persistence gate 把选定最终资产复制到 `3-生成`。
7. 任一集画布节点生成、复用或上传后，先确认 `projects/aigc/<项目名>/3-主体/道具/3-生成/` 是否已有同 stem 资产；本地 canonical 已有则记录 `already_present` 并跳过下载/复制，本地缺失时才用 `libtv download` 或复制补齐。
8. 若不使用外部顾问与复核流程 或 reviewer，按 `SKILL.md` 的顾问与复核流程 Execution Contract 直接执行本地 checklist。
9. 若校验器通过但用户指出“批量定制不细”，优先检查 Visual Maps、Node Network、Failure Routing、Provider Degradation 和 Output Contract Alignment 是否足够具体。
10. 若主图 prompt 只是替换道具名、材质、视角标签或同义形容词，不修几个 token；废弃该 JSON 候选并重新由 LLM 基于 `4. 解构` 裁决生成重点。
11. 维护生成 Skill 2.0 合同时，先保证默认 libTV 边界、`4. 解构` 真源、主图持久化、多视图取消合同和反模板 gate 在 `SKILL.md` 可定位，再同步 templates/review/scripts。

## Reusable Heuristics

- 生成阶段的创造力在于“忠实执行设计”，不是重新发现主体。
- 主图是后续连续性的视觉锚点；多视图模板经验仅作为历史资料保留，不参与默认生成。
- 主图作为本地参照时按需 `同画布主图节点` 可见化；否则只是路径证据，不是已传入视觉参照。
- 画布节点不是项目持久化终点；每次真实生成、复用或上传后，都要确认项目 `道具/3-生成` 目录已有同名本地资产。本地 canonical 已有就是通过条件，不应重复下载。
- 道具多视图生产板规则已停用；如未来单独恢复，需要先更新 `SKILL.md` 的取消合同。
- JSON 提示词是可复跑证据，应保存输入来源、最终 prompt、参考图和输出图路径。
- 对道具生成，最容易漂移的是尺度、材质老化和功能部件；这些应从上游 prompt 中原样保留。
- 普通项目生图默认且唯一执行入口是 `.agents/skills/cli/libTV`；不得直接调用 nano-banana、Dreamina 或 AnyFast 子技能，除非用户显式点名该 provider / API / model。
- Mermaid 图不是装饰项；它承担把分型、分支、汇流和失败回路从文字清单中显形的职责。
- 生成叶子的最小可执行 spine 是“设计文档 scope + 主图 prompt + 主图资产 + review”；任何 prompt 批量化捷径都应回到该链路。
- 跨集生成时，把“同主体同状态已存在”当作通过条件而不是缺口；只有开合、破损、修复、激活等状态变体才生成新图，且必须使用 `Lib Image`。
