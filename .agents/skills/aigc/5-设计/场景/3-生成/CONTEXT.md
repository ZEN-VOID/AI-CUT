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
| 生成阶段重新设计场景 | 阶段边界层 | 回到上游设计文档，只抽取已有 `提示词设计` | `SKILL.md` 固定“不重新设计主体” | prompt JSON 可回指原设计稿 |
| 主图缺 JSON 记录 | 交付完整性层 | 补写同名 JSON，记录来源、prompt、mode、path | steps 将 JSON 落盘设为每次 imagegen 后的 gate | 每张图片都有同名 JSON |
| 多视图没有引用主图 | 参照连续性层 | 重新执行 Step2，显式标注主图为 reference image | 模板字段固定 `reference_main_image` | 多视图 JSON 有主图路径 |
| 图片留在 `$CODEX_HOME` | 项目持久化层 | 复制或移动最终图到项目 `3-生成` | 交付前执行 output persistence gate | 最终路径在 workspace 项目内 |
| 批量任务混用提示词 | 批处理路由层 | 为每个设计文档建立独立 prompt record | 按设计文档一对一生成 `generation_profile` | 每个 JSON 的 source 不重复错配 |
| 未经许可覆盖旧资产 | 文件安全层 | 恢复或版本化输出，记录 variant | 输出合同默认版本化命名 | 同名冲突有明确用户许可或版本后缀 |
| CLI fallback 被默认启用 | imagegen 路由层 | 回到内建 `image_gen` 或询问用户 | 读取 `$imagegen` 合同后再选模式 | 报告中记录 mode 与许可状态 |
| 2.0 包有目录但缺少可视化拓扑 | Skill 2.0 表达层 | 在 `SKILL.md` 和 `steps/` 补 Mermaid 主流程、状态图和失败回路 | 批量定制后检查 `Visual Maps` 与 steps Mermaid 是否存在 | `rg \"mermaid|Visual Maps\"` 能定位入口图和步骤图 |

## Repair Playbook

1. 先确认目标场景对应哪一份 `2-设计` 文档，避免从清单或记忆中临时拼接主体。
2. 主图 prompt 优先使用设计文档 `## 5. 提示词设计` 中 fenced text block；若有多个英文 prompt，选择明确标为生图提示词的版本并记录抽取说明。
3. 多视图 prompt 不重写场景设定，只把上游提示词嵌入模板的 `critical_requirements` 和 `source_prompt`。
4. 每次生成后立刻落同名 JSON，避免图片与 prompt 分离。
5. 使用主图作为多视图参照时，明确角色是 continuity reference，不把主图中的偶然构图当成新设定。
6. 批量任务按“设计文档 -> 主图 -> 主图 JSON -> 多视图 -> 多视图 JSON”闭环处理，失败项单独记录，不阻塞已完成项的路径回写。
7. 若 subagents 不可用，至少执行本地 review checklist：来源、命名、JSON、参照、持久化、边界六项。
8. 批量生成的 Skill 2.0 包若只有表格没有图，优先补 `SKILL.md` 的总览图，再补 `steps/` 的执行拓扑图；不要把完整细则倒灌回 `SKILL.md`。

## Reusable Heuristics

- 场景生成阶段的价值是把上游设计稳定投影成可检查资产，不是重新做美术设定。
- 多视图图最容易漂成九个不同场景；模板必须反复强调同一空间、同一时代、同一材质逻辑、同一光源方向。
- 场景图默认不加人物、动物、剪影或人形阴影，除非上游设计文档明确要求。
- 主图是多视图的连续性锚点；它帮助锁定场景身份，但不能覆盖设计文档的提示词真源。
- 场景多视图应先形成 `subject_invariant_lock`，再展开九宫格；每个 panel 都要证明同一空间的方向、阈限、结构、光源、材质和动线，而不是生成九个好看的镜头。
- 场景多视图生产板必须具备可追踪身份：顶左身份牌优先显示短 ASCII 场景 ID，完整主体名进入 JSON；每个 panel 左下角应有短视角标签，用于审阅时快速区分 wide、medium、detail、threshold、structure、low-angle、path、material 和 top-down。
- JSON prompt record 是复现、审查和后续视频阶段的证据，重要性不低于图片本身。
- Mermaid 图在本类技能中不是装饰，而是防止 Step1/Step2、repair、review_only 和批量汇流被批量模板抹平的路由证据。
