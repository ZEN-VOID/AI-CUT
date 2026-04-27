# Context: aigc 5-设计/角色/3-生成

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
| 主图重新设计角色 | 上游真源层 | 回到 `2-设计/<角色名>.md` 的 `提示词设计`，删除新增设定 | 主图 JSON 固定记录 source_design_path 与 source_prompt_section | prompt 可回指上游设计稿 |
| 多视图模板压过角色事实 | 模板边界层 | 将模板文字改回 layout-only，保留角色身份与服装来自上游 | `critical_requirements` 明确设计文档优先 | 多视图 prompt 没有替换身份、时代、服装事实 |
| 参照图缺失仍生成多视图 | Step 汇流层 | 先补主图或切换 prompt-only 阻断报告 | Step2 gate 必查 reference_image_path | 多视图 JSON 指向存在的主图路径 |
| imagegen 输出留在临时目录 | 项目持久化层 | 按 imagegen persistence 规则复制到本阶段输出目录 | 输出合同固定 canonical path | 报告路径位于 `projects/aigc/.../3-生成/` |
| JSON 与图片不同名 | 命名层 | 以图片 basename 重写 JSON basename 或反向修复 | 模板中固定 output_image_path 与 output_prompt_path | `<主体名称>-主图.*` 与 `<主体名称>-主图.json` 配对 |
| prompt-only 被误报为已生图 | 执行证据层 | 把 verdict 改为 blocked/prompt_only，清空不存在图片路径 | review gate 区分真实图片与 dry-run JSON | 图片路径存在性检查通过或明确阻断 |
| 批量角色互相串图 | 批量隔离层 | 每个角色单独读取设计稿、单独生成 JSON 和参照图 | worker 只处理一个角色主体 | 每份 JSON 的 subject_name 与 source_design_path 匹配 |
| 脚本拼接创作提示词 | LLM-first 层 | 删除脚本生成正文逻辑，仅保留校验/manifest | scripts 分区固定机械辅助边界 | 脚本不生成 prompt_text |
| 默认执行器漂移到 nano-banana/API 子技能 | 执行器路由层 | 删除非授权执行结果，恢复为 imagegen 或 prompt-only | `SKILL.md` 固定 Executor Lock，非 imagegen 需要用户本轮显式点名 | 报告中能看到默认 `.agents/skills/cli/imagegen` 或明确授权原文 |

## Repair Playbook

1. 先确认目标角色是否已有 `2-设计/<角色名>.md`，并定位 `提示词设计` 区块。
2. 若设计文档缺少 `提示词设计`，停止本阶段生成，回报需要上游 `2-设计` 修复。
3. 主图 prompt 只做必要的 imagegen 执行包装，不新增角色身份、服装、时代或气质。
4. 多视图 prompt 可以增加布局、视角、模块和一致性要求，但不得覆盖上游设计事实。
5. Step2 前必须确认 Step1 主图已经落到项目输出目录，不能使用临时预览路径作为长期参照。
6. 批量生成时逐角色闭环：主图 -> 主图 JSON -> 多视图 JSON -> 多视图图像 -> review，再进入下一个角色或并行汇流。
7. 若 imagegen 不可用，保留 prompt JSON 和阻断报告，不制造假图片路径。
8. 若需要重跑，先检查用户是否允许覆盖；未允许时使用版本化文件名或返回确认请求。
9. 除非用户本轮显式要求替代执行器，否则不要把“多视图/参考图/批量”理解为 nano-banana、AnyFast 或其他 API 子技能授权。

## Reusable Heuristics

- 角色生成阶段的创造性主要在“执行与组织画面”，不在“重新发明角色”。
- 本技能默认执行器只有 `.agents/skills/cli/imagegen`；执行器切换是用户授权事项，不是 agent 可自行优化的实现细节。
- 主图越忠实于 `提示词设计`，多视图参照越稳定；不要在主图阶段塞入复杂面板布局。
- 多视图模板应像制作部门的审阅板：强调同一身份、同一服装体系、同一材质逻辑和可验证背面/侧面。
- 角色多视图应先应用 `subject_invariant_lock`，再排 front / three-quarter / side / rear turnaround；表情、姿态和细节 callout 只能服务身份证明，不应挤占主 turnaround。
- 角色多视图生产板必须有顶左身份牌：图中优先显示短 ASCII 角色 ID，完整角色名进入 JSON；若模型文字不稳，应保留干净 badge plate 供后期叠字。
- 单主体图是 continuity anchor；即使多视图有更多模块，也应服从主图的脸、发型、体型和服装主轮廓。
- JSON prompt 是可复现证据，不是美术散文；路径、来源、模式和最终 prompt 必须清楚。
- 对角色名做安全文件名转换时，要在 JSON 中保留原名，避免后续资产回链断裂。
