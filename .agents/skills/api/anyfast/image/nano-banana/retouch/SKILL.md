---
name: nano-banana-retouch
version: "v1.0"
governance_tier: lite
description: |
  修图：保留主体身份、构图和叙事不变，对原图进行自然、写实的精修优化。当用户要求"修图"、"精修"、"去瑕疵"、"提高清晰度"、"优化曝光色彩"时使用本技能。底层调用 nano-banana API（继承父级 `nano-banana/SKILL.md` 契约）。
tools: [Read, Write, Edit, Bash]
---

# 修图（Retouch）

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

基于原图（图A）执行自然、写实、高保真的修图，不改变主体身份、构图关系与场景叙事。输入图通过 BASE64 方式直接传入，继承父级 nano-banana API 契约。

## 触发条件

用户提供一张图，要求保留原图内容主干，仅做画质、瑕疵、色彩、细节或局部问题修复。典型表述：

- "修图" / "精修" / "去瑕疵"
- "提高清晰度" / "优化曝光和颜色"
- "去掉小穿帮" / "让皮肤自然一点"
- "保留人物和构图，做电影感精修"

## 必需输入

| 参数 | 必填 | 说明 |
|------|------|------|
| `<原图路径>` | 是 | 图A：待修原图 |
| `--desc` | 否 | 补充修图目标（如"去掉脸上小瑕疵但保留皮肤纹理"、"提亮主体但不动背景"） |
| `--output-dir` | 否 | 输出目录，默认与原图同目录 |
| `--filename` | 否 | 输出文件名（不含扩展名），默认 `<原文件名>-retouch` |
| `--dry-run` | 否 | 仅打印生成命令，不实际调用 API |

## 执行流程

### Step 1 / 参数解析

- 第一个路径 → 图A（待修原图）
- 验证图片存在且可读
- 确定输出目录（`--output-dir` 或默认与原图同目录）和文件名（`--filename` 或 `<原文件名>-retouch`）

### Step 2 / 构建提示词

基础模板：

```text
在保持图一中主体身份、面部特征、发型发色、服装造型、构图布局、镜头视角和场景叙事完全不变的前提下，对图一执行自然、写实、高质量修图。修图目标：清理轻微瑕疵与噪点，优化曝光、白平衡、对比度和色彩纯净度，恢复高光与阴影细节，提升主体关键区域清晰度与材质层次，修正小范围穿帮或杂物。真实感锁定：必须保留皮肤纹理、面料纹理、环境细节和自然光影，严禁磨皮过度、塑料感、脸型漂移、背景重构或把人物改成另一张脸。
```

若有 `--desc`，追加到模板末尾：

```text
补充要求：<desc>
```

关键约束：

- 提示词必须强调"自然修图"而不是重绘式改造
- 身份锁定、构图锁定和真实感锁定描述必须保留
- 若用户仅说"修图"而未给更多约束，默认执行轻量精修而非风格化改造

### Step 3 / 比例适配

用 `sips -g pixelWidth -g pixelHeight` 获取原图尺寸，计算宽高比并映射到最近的合法值：

| 合法值 | 适用场景 |
|--------|----------|
| `16:9` | 横版宽屏 |
| `9:16` | 竖版人像 |
| `4:3` | 横版标准 |
| `3:4` | 竖版半身 |
| `1:1` | 方形构图 |

比例从原图动态适配，不做硬编码。

### Step 4 / 调用 API

```bash
python3 .agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "<完整提示词>" \
  --image-url "<原图路径>" \
  --aspect-ratio "<适配后的比例>" \
  --output-dir "<输出目录>" \
  --output-filename "<输出文件名>"
```

关键说明：

- 原图使用单个 `--image-url` 传入
- 脚本内部自动将本地文件转为 BASE64 编码传入 API
- 继承父级 nano-banana API 契约（默认值注入、原生格式、BASE64 交接等）

### Step 5 / 输出

- 默认输出目录：与原图同目录；若显式传 `--output-dir`，允许覆盖
- 命名规则：`<原文件名>-retouch.png`
- 若已存在同名文件，自动递增：`-retouch-1.png`、`-retouch-2.png`
- 永不覆盖原则：原始文件保持不变

## 错误处理

### 图片文件不存在

```text
错误：输入图片不存在
   路径: path/to/missing.png
   提示: 请确认文件路径正确
```

### API 调用失败

```text
错误：生图 API 调用失败
   错误: [API 错误信息]
   提示: 检查网络连接和 API 配置，或加 --dry-run 先检查提示词
```

## 调用示例

```bash
# 基础用法：自然精修
/image:retouch 原图.png

# 带补充描述
/image:retouch 人像.png \
  --desc "去掉轻微痘印和眼下阴影，保留皮肤毛孔与真实妆面质感"

# 指定输出
/image:retouch 海报原图.png \
  --output-dir output/影片/项目名/1-设定/1.2-角色/1.2.3-角色生成 \
  --filename 青青-精修版

# dry-run 预览
/image:retouch 原图.png --dry-run
```

## 字段通过表（lite combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
|----------|----------|--------|----------|
| `FIELD-RT-01` 单图输入 | 原图存在且路径有效 | `FAIL-RT-INPUT` | Step 1 |
| `FIELD-RT-02` 提示词构建 | 基础模板完整 + 真实感锁定与身份锁定描述在位 | `FAIL-RT-PROMPT` | Step 2 |
| `FIELD-RT-03` 比例适配 | 从原图正确读取尺寸并映射到合法枚举值 | `FAIL-RT-RATIO` | Step 3 |
| `FIELD-RT-04` 输出落盘 | 图片文件存在 + 不覆盖原文件 + 递增命名正确 | `FAIL-RT-OUTPUT` | Step 5 |

## 依赖

- 脚本入口：`../scripts/nano_banana_generate.py`
- API 契约：继承 `../SKILL.md`（默认值注入、原生格式、BASE64 交接、项目化输出路径等）
- 环境变量：API Token 由 `nano_banana_generate.py` 内部从 `.env` 读取
- 系统工具：`sips`（macOS 原生，用于读取图片尺寸）

## Root-Cause 执行契约

当修图失败或输出不符预期时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：真实感锁定不足、身份漂移、磨皮过度、局部瑕疵未修、比例适配错误、输出覆盖原文件
-> `规则源`：本 `SKILL.md` + `../scripts/nano_banana_generate.py`
-> `规则源的规则源`：`../SKILL.md`（父级 API 契约）
-> `Fix Landing Points`：优先修本技能提示词模板和参数传递逻辑，再修父级脚本

用户侧关闭语必须包含：根因位置 + 立即修复 + 系统性预防修复
