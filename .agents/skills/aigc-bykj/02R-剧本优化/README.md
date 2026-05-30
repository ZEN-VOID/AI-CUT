# 02R-剧本优化

BYKJ `02R-剧本优化` 承接 `output/[项目名]/02-剧本处理/` 的已有产物，处理用户二次人工介入调优需求。

## Files

```text
02R-剧本优化/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── CHANGELOG.md
└── agents/
    └── openai.yaml
```

## Canonical Input

- `output/[项目名]/02-剧本处理/剧本处理稿.json`
- `output/[项目名]/02-剧本处理/执行报告.json`
- `output/[项目名]/02-剧本处理/manifest.json`
- 用户粘贴的等价局部片段或调优需求

## Canonical Output

```text
output/[项目名]/02R-剧本优化/
├── 优化稿.json
├── 优化报告.json
├── manifest.json
└── 变更摘要.md
```

`变更摘要.md` 是可选摘要，不替代 `优化稿.json`。

## Core Modes

- `overall_tuning`：整体调优，最大程度满足用户需求但不破坏基本叙事结构。
- `concept_requirements_tuning`：把一个概念或多条需求映射为可执行编辑点。
- `local_targeted_tuning`：只改用户指定选区。
- `conflict_resolution`：局部目标与前后剧情冲突时，先输出冲突判别单。
- `review_only`：只审查不改稿。
- `repair_previous_02R`：最小修复已有 02R 输出。

## Natural Language Layer

用户个人自然语言先进入前置解释层：

- `natural_language_intent_map`：把“更爽”“更高级”“不对味”等口语需求归一为可执行编辑变量。
- `clarification_options`：低信息或多解需求先给 2-3 个方向，不直接大改。
- `user_taste_profile`：记录本轮临时偏好，不自动写入项目长期记忆。
- `edit_intensity`：限定 `light_touch`、`medium_rework`、`heavy_rewrite`、`experimental_alt`。
- `version_comparison`：保留原段落摘要、修改意图、影响范围和可回退说明。

## Quick Check

调用本阶段前确认：

- 已加载 `SKILL.md + CONTEXT.md`。
- 已定位 `02-剧本处理` 源稿或用户粘贴片段。
- 已把用户自然语言归一为编辑变量，或已进入澄清门。
- 已明确整体、概念/多需求、局部或只审查模式。
- 已明确修改强度和临时偏好画像。
- 局部调优目标若与前后剧情冲突，必须先等用户判别。
