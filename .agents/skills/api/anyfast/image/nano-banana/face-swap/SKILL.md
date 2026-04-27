---
name: nano-banana-face-swap
version: "v1.0"
governance_tier: lite
description: |
  角色换脸：保留服装造型姿态不变，将角色形象替换为参照图中的角色面貌。当用户要求"换脸"、"把A的脸换成B"、"保留服装换角色"、"角色替换"时使用本技能。底层调用 nano-banana API（继承父级 `nano-banana/SKILL.md` 契约）。
tools: [Read, Write, Edit, Bash]
---

# nano-banana-face-swap 角色换脸

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 触发条件

用户提供两张图（原图 + 角色形象参照图），要求保留原图服装/姿态/构图，仅替换角色面貌。

典型触发语：
- "换脸"
- "把A的脸换成B"
- "保留服装换角色"
- "角色替换"
- "用这张定妆照替换那张图里的人"

## 必需输入

| 参数 | 必填 | 说明 |
|------|------|------|
| 图A（原图路径） | 是 | 保留其服装/姿态/构图 |
| 图B（角色形象图路径） | 是 | 提供角色面貌（如定妆照、角色面板） |
| `--desc` | 否 | 补充描述（如"保持战斗姿态"、"年龄调整为少年期"） |
| `--output-dir` | 否 | 输出目录，默认与原图（图A）同目录 |
| `--filename` | 否 | 输出文件名（不含扩展名），默认 `<原文件名>-face-swap` |
| `--dry-run` | 否 | 仅打印生成命令，不实际调用 API |

## 执行流程

### Step 1 / 参数解析

- 第一个路径 → 图A（保留服装/姿态的原图）
- 第二个路径 → 图B（提供角色形象的参照图）
- 验证两个文件均存在且可读
- 确定输出目录（`--output-dir` 或默认与原图同目录）和文件名（`--filename` 或 `<原文件名>-face-swap`）

### Step 2 / 构建提示词

基础模板：

```text
保留图一中的服装造型、姿态动作、构图布局和背景环境完全不变，仅将图一中角色的面部五官、发型发色、肤色、体态比例替换为图二中角色的形象特征。形象替换要求：完整还原图二角色的面部轮廓、五官比例、发型发色、肤色质感和体态气质；替换后的角色需自然融入图一的服装和姿态，保持衣物穿着的物理合理性。服装锁定：图一中的服装剪裁、面料质感、色彩配色、装饰细节和层次结构严禁改变。
```

若有 `--desc`，追加到模板末尾：

```text
补充要求：<desc>
```

### Step 3 / 比例适配

调用前用 `sips -g pixelWidth -g pixelHeight` 获取原图尺寸，将宽高比映射到最近的合法值：

| 合法比例 | 数值 |
|----------|------|
| 16:9 | 1.778 |
| 9:16 | 0.5625 |
| 4:3 | 1.333 |
| 3:4 | 0.75 |
| 1:1 | 1.0 |

取与实际宽高比距离最小的合法值。

### Step 4 / 调用 API

```bash
python3 .agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "<完整提示词>" \
  --image-url "<原图路径>" \
  --image-url "<角色形象图路径>" \
  --aspect-ratio "<适配后的比例>" \
  --output-dir "<输出目录>" \
  --output-filename "<输出文件名>"
```

关键约束：
- `--image-url` 每张图使用独立的 flag（`action="append"`）
- 第一个 = 图一（锁定服装/姿态），第二个 = 图二（提供面貌）
- 提示词中"图一""图二"与 `--image-url` 传入顺序严格对应
- 脚本内部自动 BASE64 编码，无需手动转换

### Step 5 / 输出

- 默认输出目录：与原图（图A）同目录；若显式传 `--output-dir`，允许覆盖
- 命名：`<原文件名>-face-swap.png`
- 若已存在同名文件，自动递增：`-face-swap-1.png`、`-face-swap-2.png`
- 永不覆盖原则：原始文件保持不变

## 错误处理

### 图片文件不存在

```text
错误: 输入图片不存在
  路径: path/to/missing.png
  提示: 请确认文件路径正确
```

### 只提供了一张图

```text
错误: 缺少角色形象参照图
  提示: face-swap 需要两张图：第一张为保留服装的原图，第二张为提供角色形象的参照图
```

### API 调用失败

```text
错误: 生图 API 调用失败
  错误: [API 错误信息]
  提示: 检查网络连接和 API 配置，或加 --dry-run 先检查提示词
```

## 调用示例

```bash
# 基础用法
/image:face-swap 原图.png 角色参照.png

# 带补充描述
/image:face-swap 场景截图.png 角色定妆照.png --desc "保持原图的奔跑姿态和运动模糊效果"

# 指定输出目录和文件名
/image:face-swap 原图.png 角色参照.png \
  --output-dir output/影片/项目名/1-设定/1.2-角色/1.2.3-角色生成 \
  --filename 青青-战斗装版
```

## 字段通过表（lite combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
|----------|----------|--------|----------|
| `FIELD-FS-01` 双图输入 | 两张图均存在且可读 | `FAIL-FS-INPUT` | Step 1 |
| `FIELD-FS-02` 提示词构建 | 模板完整 + 图序正确（图一=服装源，图二=面貌源） | `FAIL-FS-PROMPT` | Step 2 |
| `FIELD-FS-03` 比例适配 | 从原图尺寸正确映射到最近合法比例 | `FAIL-FS-RATIO` | Step 3 |
| `FIELD-FS-04` 输出落盘 | 图片存在 + 不覆盖原文件 | `FAIL-FS-OUTPUT` | Step 5 |

## 依赖

- 脚本入口：`../scripts/nano_banana_generate.py`
- API 契约继承：`../SKILL.md`（nano-banana 父级契约层）
- 环境变量：API Token 由 `nano_banana_generate.py` 内部管理（读取 `.env`）

## Root-Cause 执行契约

当换脸失败或输出不符预期时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：图序颠倒、提示词模板残缺、比例适配错误、输出覆盖原文件
-> `规则源`：本 `SKILL.md` + `../scripts/nano_banana_generate.py`
-> `规则源的规则源`：`../SKILL.md`（父级 API 契约）
-> `Fix Landing Points`：优先修本技能提示词模板和参数传递逻辑，再修父级脚本

用户侧关闭语必须包含：根因位置 + 立即修复 + 系统性预防修复
