---
name: nano-banana-multiview-prop
version: "v1.0"
governance_tier: lite
description: |
  多视图布局-道具：基于参照图 + 道具描述，生成 PROP_DESIGN_SHEET 多视图道具设计页（16:9 三栏布局）。当用户要求"道具多视图"、"道具设计页"、"道具转身图"、"PROP_DESIGN_SHEET"时使用本技能。底层调用 nano-banana API（继承父级契约）。
tools: [Read, Write, Edit, Bash]
---

# 道具多视图布局（PROP_DESIGN_SHEET）

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 触发条件

用户提供一张或多张道具参照图 + 道具主体描述，要求生成多视图道具设计页。

## 必需输入

| 参数 | 必填 | 说明 |
|------|------|------|
| `<图片路径...>` | 是 | 一张或多张本地图片路径，空格分隔 |
| `--id` | 是 | 道具ID，如 `PRP-001` |
| `--name` | 是 | 道具名称 |
| `--desc` | 是 | 中文道具主体描述，400字以内；涵盖道具功能、造型骨架、材质工艺、磨损痕迹、尺度比例、光影表现 |
| `--output-dir` | 否 | 输出目录，默认与第一张输入图同目录 |
| `--filename` | 否 | 输出文件名（不含扩展名），默认 `<原文件名>-multiview` |
| `--dry-run` | 否 | 仅打印生成命令，不实际调用 API |

## 执行流程

### Step 1 / 参数解析

- 提取所有图片路径（支持相对路径，自动转绝对路径）
- 提取 `--id`、`--name`、`--desc` 参数
- 确定输出目录和文件名

### Step 2 / 构建提示词

使用固定模板，将用户参数注入。模板源自 `.agents/skills/aigc2026/3-设定/4-面板/道具面板/templates/道具面板-提示词.json`，保持字段级一致：

```text
### 道具ID: <prop_id>
保留图一画面风格和道具形象不变，根据以下要求调整为专业多视图道具设计页：

【设计主体】
<desc>。道具居中展示，干净背景，产品摄影式布光。画面中不出现任何人手、人物、人形剪影或生物。

【画布规格】
Create one professional PROP_DESIGN_SHEET on a 4096x2304 widescreen canvas (16:9). Use dark gray base (#1a1a1a) with subtle technical grid overlay (#2A2A2A). Keep a fixed three-column layout LEFT 15% | CENTER 50% | RIGHT 35%, maintain clean spacing, and preserve technical-sheet readability for production review.

【三栏布局】
LEFT COLUMN (15%):
- MATERIAL PALETTE (4x3): Show 12 swatches for core material families, roughness variation, and wear state references.
- COLOR PALETTE (2x3): Show primary/secondary/accent color chips with tonal hierarchy suitable for the same prop identity.

CENTER COLUMN (50%):
- MULTI-VIEW TURNAROUND (front/side/back): Render front, side, and back views of one identical prop, aligned to a shared baseline and stable scale.

RIGHT COLUMN (35%):
- DETAIL CLOSE-UPS (2x3): Render six close-up cells for craftsmanship joints, surface wear, and narrative marks.
- USAGE CONTEXT (2 frames): Render two context frames to show practical handling or usage cues while keeping identical prop morphology.

【强制约束】
- Output must remain a PROP_DESIGN_SHEET (3-column layout), not a single product poster or 3x3 nine-grid storyboard.
- All modules must depict the same prop identity with stable silhouette, scale, and material logic — no drift allowed.
- Must display one fixed top-left identity badge: <prop_id> + <prop_name>. Keep position and typography stable.
- Do not redesign narrative facts or core prop identity from the reference image.
- Empty-scene guardrail: no humans, creatures, silhouettes, or human-shaped shadows in any module.
- Column gutter: 20px. Module spacing: 15px.
```

替换规则：
- `<prop_id>` → `--id` 值
- `<prop_name>` → `--name` 值
- `<desc>` → `--desc` 值

### Step 3 / 调用 API

工具路径：`.agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py`

```bash
python3 .agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "<构建的完整提示词>" \
  --image-url "<图片路径1>" \
  --aspect-ratio "16:9" \
  --output-dir "<输出目录>" \
  --output-filename "<输出文件名>" \
  --no-report
```

关键说明：
- `--image-url` 每张图使用独立的 `--image-url` flag（`action="append"`），脚本内部自动读取并转为 BASE64 传入 API
- `--aspect-ratio` 固定为 `16:9`（PROP_DESIGN_SHEET 标准画幅）
- 第一张图为主参照图（"图一"），后续图为辅助参照
- `--no-report` 固定启用

### Step 4 / 输出

默认输出目录：与第一张输入图同目录；若显式传 `--output-dir`，允许覆盖。

命名规则：`<原文件名>-multiview.png`
- 若已存在同名文件，自动递增：`-multiview-1.png`、`-multiview-2.png`
- 永不覆盖原则：原始文件保持不变

## 错误处理

| 错误场景 | 处理 |
|----------|------|
| 图片文件不存在 | 报错并提示确认文件路径 |
| 描述为空或超400字 | 报错并提示精简描述 |
| API 调用失败 | 报错并建议检查网络/API 配置，或加 `--dry-run` 先检查提示词 |

## 调用示例

```bash
/image:multiview-prop 旧玉佩.png \
  --id PRP-001 --name 旧玉佩 \
  --desc "一枚椭圆形旧玉佩，长约5cm，玉质青白带杂色，边缘有细小磕碰与温润包浆；正面浅浮雕缠枝纹，线条因长年摩挲已圆润模糊；背面刻有模糊家纹，笔画几近磨平；系绳为褪色红绳打结，绳结处有磨损起毛；整体呈现长期贴身佩戴的温润光泽与岁月痕迹；产品摄影式布光，干净背景"
```

## 字段通过表（lite combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
|----------|----------|--------|----------|
| FIELD-MVP-01 输入完整 | 图片+id+name+desc 齐全 | FAIL-MVP-INPUT | Step 1 |
| FIELD-MVP-02 提示词构建 | 模板注入正确，三栏布局规格完整 | FAIL-MVP-PROMPT | Step 2 |
| FIELD-MVP-03 空场景护栏 | 无人手/人物/生物出现 | FAIL-MVP-EMPTY-SCENE | Step 2 |
| FIELD-MVP-04 输出落盘 | 16:9 图片存在+不覆盖 | FAIL-MVP-OUTPUT | Step 4 |

## 依赖

- `../scripts/nano_banana_generate.py`
- API 契约继承 `../SKILL.md`
