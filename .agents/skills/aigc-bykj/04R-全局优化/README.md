# 04R-全局优化

BYKJ `04R-全局优化` 承接 `output/[项目名]/04-全局预设/` 的已有产物，处理用户个人自然语言驱动的全局视觉预设二次优化。

## Files

```text
04R-全局优化/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
└── agents/
    └── openai.yaml
```

## Canonical Input

- `output/[项目名]/04-全局预设/全局风格预设.json`
- `output/[项目名]/04-全局预设/视觉风格库.json`
- `output/[项目名]/04-全局预设/全局预设.md`
- `output/[项目名]/04-全局预设/执行报告.json`
- `output/[项目名]/04-全局预设/manifest.json`
- 用户粘贴的等价风格片段、局部字段、自然语言调优要求或下游反馈

## Canonical Output

```text
output/[项目名]/04R-全局优化/
├── 优化预设.json
├── 视觉风格补丁.json
├── 全局优化.md
├── 优化报告.json
├── manifest.json
└── 变更摘要.md
```

`视觉风格补丁.json` 和 `变更摘要.md` 是可选补丁/摘要，不默认覆盖 `04` 原始风格库。

## Core Modes

- `overall_preset_tuning`：整体优化全局视觉预设。
- `intent_style_matching`：解析用户自然语言意图并匹配现有风格字段。
- `local_field_tuning`：只改用户指定字段或片段。
- `keyword_tuning`：优化英文关键词、负面词和权重顺序。
- `scene_variation_tuning`：优化场景变体、组别风格和下游使用边界。
- `review_only`：只审查不改预设。
- `conflict_resolution`：用户目标与故事源、参考事实、版权边界或下游可用性冲突时，先输出冲突判别单。

## Natural Language Layer

用户个人自然语言先进入前置解释层：

- `high_energy_intent_map`：把“更高级”“不对味”“别太赛博”等口语需求归一为风格轴和目标字段。
- `clarification_options`：低信息或多解需求先给 2-3 个风格路线，不直接重塑全局。
- `style_taste_profile`：记录本轮临时风格偏好，不自动写入项目长期记忆。
- `style_matching_matrix`：比对用户意图、04 源稿、02 故事源、参考图事实和下游 05/06 消费。
- `edit_intensity`：限定 `light_touch`、`medium_rework`、`heavy_reframe`、`experimental_alt`。
- `version_comparison`：保留原预设摘要、修改意图、影响范围和可回退说明。

## Quick Check

调用本阶段前确认：

- 已加载 `SKILL.md + CONTEXT.md`。
- 已定位 `04-全局预设` 源稿或用户粘贴片段。
- 已把用户自然语言归一为风格轴，或已进入澄清门。
- 已明确整体、意图匹配、局部字段、关键词、场景变体或只审查模式。
- 已明确修改强度、临时风格偏好画像和目标字段。
- 用户目标若与故事源、参考图事实、版权边界或下游消费冲突，必须先等用户判别。
