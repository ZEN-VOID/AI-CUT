---
name: nano-banana-multiview-character
version: "v1.0"
governance_tier: lite
description: |
  多视图布局-角色：基于参照图 + 角色描述，生成 CHARACTER_DESIGN_SHEET 多视图角色设计页（16:9 三栏布局）。当用户要求"角色多视图"、"角色设计页"、"角色转身图"、"CHARACTER_DESIGN_SHEET"时使用本技能。底层调用 nano-banana API（继承父级契约）。
tools: [Read, Write, Edit, Bash]
---

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 触发条件

用户提供一张或多张角色参照图 + 角色全身描述，要求生成多视图角色设计页。

## 必需输入

| 参数 | 说明 | 必需 |
|------|------|------|
| 图片路径 | 一张或多张角色参照图 | 是 |
| `--id` | 角色ID（如 CHR-001） | 是 |
| `--name` | 角色名称 | 是 |
| `--desc` | 中文角色全身描述（400字以内，涵盖面部特征、发型发色、体态身形、服饰细节、姿态气质） | 是 |
| `--output-dir` | 输出目录，默认与第一张输入图同目录 | 否 |
| `--filename` | 输出文件名 | 否 |
| `--dry-run` | 仅输出提示词不调用 API | 否 |

## 执行流程

### Step 1 / 参数解析

- 提取图片路径（支持相对路径，自动转绝对路径）
- 提取 `--id`、`--name`、`--desc`
- 确定输出目录和文件名
- 校验：图片文件存在、desc 非空且 ≤400 字

### Step 2 / 构建提示词

使用固定模板（源自 `.agents/skills/aigc2026/3-设定/4-面板/角色面板/templates/角色面板-提示词.json`）：

```text
### 角色ID: <character_id>
保留图一画面风格和角色形象不变，根据以下要求调整为专业多视图角色设计页：

【设计主体】
<desc>。全身站立像，双脚可见，中性简洁背景，角色概念设计图风格。

【画布规格】
Create one professional CHARACTER_DESIGN_SHEET on a 4096x2304 landscape canvas (16:9). Use dark gray base (#1a1a1a) with subtle grid overlay (#2A2A2A). Keep character zones transparent/pure flat color and do not render environment scene. Rendering style should be inherited from the reference image.

【三栏布局】
LEFT COLUMN (15%):
- COLOR PALETTE: 4x3 swatch grid. Row1: skin/eye/blush. Row2-4: costume colors from main to deep tones.
- HAIR STYLE: Hair structure/length/texture plus hair color details and value hints.

CENTER COLUMN (50%):
- FULL BODY VIEWS: Front view, side 3/4 view, back view. Feet must be bottom-aligned. 15-20px gap between views.

RIGHT COLUMN (35%):
- OUTFIT LAYERING: 2x3 flat-lay outfit layering from inner to outer. No mannequin model. Keep consistent with main outfit.
- ACCESSORIES: Only outfit-related wearables (hair/waist/wrist/shoe accents). No props/weapons/personal items.
- ACTION POSES: 3 dynamic pose slots showing character-appropriate movements.
- FACIAL EXPRESSIONS: 2x3 expression slots. Makeup continuity must be shown in this module only.

【强制约束】
- Output must be CHARACTER_DESIGN_SHEET (3-column layout), not 3x3 nine-grid storyboard.
- Keep one coherent style language across all modules; avoid mixed-style artifacts.
- Character identity lock: same face, hair, skin tone, body proportion across ALL views and modules — no drift allowed.
- No scene/environment/background narrative.
- No props/weapons/hand-held objects in any module.
- Layout reference image controls layout grammar only; never copy its character identity/gender/costume subject.
- Must display one fixed top-left identity badge: <character_id> + <character_name>. Keep position and typography stable.
- Makeup must be merged into FACIAL EXPRESSIONS slots; no standalone makeup panel.
- Column gutter: 20px. Module spacing: 15px.
```

替换规则：
- `<character_id>` → `--id` 值
- `<character_name>` → `--name` 值
- `<desc>` → `--desc` 值

### Step 3 / 调用 API

```bash
python3 .agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "<完整提示词>" \
  --image-url "<图片路径1>" \
  --image-url "<图片路径2>" \
  --aspect-ratio "16:9" \
  --output-dir "<输出目录>" \
  --output-filename "<输出文件名>" \
  --no-report
```

- `--aspect-ratio` 固定 `16:9`（CHARACTER_DESIGN_SHEET 标准画幅）
- `--no-report` 不输出 report JSON
- 多张图片时每张各用一个 `--image-url` 参数

### Step 4 / 输出

- 默认输出目录：与第一张输入图同目录；若显式传 `--output-dir`，允许覆盖
- 命名：`<原文件名>-multiview.png`，递增防覆盖
- 永不覆盖原则：原始文件保持不变

## 错误处理

| 错误场景 | 处理 |
|----------|------|
| 图片路径不存在 | 报错退出，提示检查路径 |
| `--desc` 为空 | 报错退出，提示提供角色描述 |
| `--desc` 超 400 字 | 警告并截断，或提示精简 |
| API 调用失败 | 返回 `FAIL-NANO-BANANA-GENERATION`，参照父级契约重试策略 |

## 调用示例

```bash
/image:multiview-character 角色定妆照.png \
  --id CHR-001 --name 青青 \
  --desc "25岁女性，身材纤细但有力量感..."
```

## 字段通过表（lite combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
|----------|----------|--------|----------|
| FIELD-MVC-01 输入完整 | 图片+id+name+desc 齐全 | FAIL-MVC-INPUT | Step 1 |
| FIELD-MVC-02 提示词构建 | 模板注入正确，三栏布局规格完整 | FAIL-MVC-PROMPT | Step 2 |
| FIELD-MVC-03 输出落盘 | 16:9 图片存在+不覆盖 | FAIL-MVC-OUTPUT | Step 4 |

## 依赖

- `../scripts/nano_banana_generate.py`
- API 契约继承 `../SKILL.md`
