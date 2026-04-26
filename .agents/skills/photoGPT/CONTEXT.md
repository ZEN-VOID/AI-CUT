# Context: photoGPT

本文件是 `photoGPT` 的经验层知识库。它不改写 `SKILL.md` 的执行合同，只保存围绕五大类十四子类的图像编辑类型识别、提示词强化和 imagegen handoff 可复用经验。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 30000
hard_limit_chars: 60000
status: ok
recommended_action: keep-type-and-template-heuristics-only
last_checked_at: 2026-04-25
```

## Type Map

| type_id | 触发症状 | 根因层 | 立即修复 | 验证点 |
| --- | --- | --- | --- | --- |
| `TM-PGPT-01` | 用户说“换一下”但没有说明换什么 | intent ambiguity | 追问或在 prompt plan 标为 `blocked_missing_edit_target` | 编辑目标与保留项均明确 |
| `TM-PGPT-02` | 元素替换后主体和参考对象混在一起 | image role order | 明确图一为待编辑图、图二为替换来源，并在 prompt 中反复锁定 | `image_roles` 与 `元素替换/<子类>` 模板图序一致 |
| `TM-PGPT-03` | 修图变成重绘，人物脸型漂移 | 修图 overreach | 使用 `修图/高清` 或 `修图/美颜美体`，强调真实感、构图和身份锁定 | prompt 含“严禁脸型漂移/背景重构” |
| `TM-PGPT-04` | 多视图输出成海报、普通九宫格或错对象 sheet | layout grammar missing | 使用 `多视图/<场景|道具|服装|角色>`，固定画幅、栏位/面板和身份徽章 | prompt 明确 sheet 类型和 layout |
| `TM-PGPT-05` | 用户要求 API/CLI 参数但 imagegen 合同未确认 | provider mismatch | 先加载 imagegen 合同；需 CLI fallback 时确认用户显式许可 | `imagegen_mode` 可追溯 |
| `TM-PGPT-06` | prompt 很美但缺少可执行约束 | prompt decorative drift | 补 `change scope / preserve scope / image roles / negative constraints / output target` | prompt plan 字段齐全 |
| `TM-PGPT-07` | 多图融合输出像拼贴或平均混合所有参考图 | fusion role collapse | 先区分 `电商广告` 与 `分镜构图`，逐张图标注职责 | 每张参考图都有 role，主次和融合边界清楚 |
| `TM-PGPT-08` | 风格化改变了人物身份或场景事实 | style overreach | 区分 `风格迁移` 与 `滤镜`，把风格限定为视觉语言 | preserve_scope 明确身份、构图和叙事事实 |

## Repair Playbook

1. 先读取 `types/type-map.md`，不要凭关键词直接进入模板。
2. 对所有输入图先标注角色，再写 prompt；多图任务没有图序标注不得执行。
3. 强化提示词时保留用户原始意图，不擅自新增剧情事实或改写上游设计真源。
4. 对 `元素替换` 四个子类必须同时写“替换来源”和“严禁改变项”。
5. 对 `修图` 默认保真；`高清` 强调画质与纹理，`美颜美体` 强调身份、比例和自然克制。
6. 对 `多视图` 先判断对象是场景、道具、服装还是角色，再保证 layout grammar、身份一致性和对应空场景/无人物/无强角色护栏。
7. 对 `多图融合` 先判断是电商广告还是分镜构图；每张图只承担被声明的职责。
8. 对 `风格化` 先判断是风格迁移还是滤镜；风格迁移可吸收视觉语言，滤镜只改色彩影调。
9. 调用 imagegen 前加载 `.agents/skills/cli/imagegen/SKILL.md + CONTEXT.md`，不要在 photoGPT 内自建 provider 规则。
10. 生成失败时先定位是判型错误、模板缺口、prompt 锁定不足，还是 imagegen 执行环境问题。

## Reusable Heuristics

- `photoGPT` 的价值不在“把提示词写长”，而在“把编辑类型、图片角色和不可漂移项写准”。
- `photoGPT` 子类模板以 JSON 为执行真源；不要再新增 Markdown 执行模板。字段化模板更利于 LLM 补齐 `required_fields`、`input_roles`、`preserve_scope`、`change_scope`、`negative_constraints`、`prompt_assembly` 和 `review_focus`。
- `元素替换` 模板最重要的是图序：图一通常是保留构图/主体的源图，图二是替换来源。
- `修图` prompt 应避免“重新设计”“重绘”“换风格”等词，除非用户明确要求。
- `多视图` sheet prompt 必须把对象类型、画幅、布局、身份徽章和禁止项写成结构化硬约束。
- `多视图` 身份徽章使用短 ASCII ID 作为图中可视化文本，完整主体名称进入 prompt plan / JSON 记录；若图像文字不稳，保留干净 badge plate 供后期叠字。
- `多视图/场景` 额外要求每个 panel 左下角具备短视角标签或叠字预留条，避免九宫格审阅时无法区分 wide、medium、detail、threshold、structure、low-angle、path、material 和 top-down。
- `多图融合` 的质量取决于角色分工，不取决于参考图数量；没有 role schema 的多图融合应阻塞。
- `风格化/滤镜` 是后期调色语义，不应偷换成 `风格化/风格迁移` 的强重绘语义。
- 若用户只给审美方向，最终 prompt 需要补齐镜头、光线、材质、构图、主体锁定和反向约束。
