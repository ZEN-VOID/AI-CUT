---
name: nano-banana-background-swap
version: "v1.0"
governance_tier: lite
description: |
  背景替换：保留主体身份、服装、姿态与镜头关系不变，将背景环境替换为参照图中的场景。当用户要求"换背景"、"背景替换"、"抠图换景"、"保留人物换环境"时使用本技能。底层调用 nano-banana API（继承父级 `nano-banana/SKILL.md` 契约）。
tools: [Read, Write, Edit, Bash]
---

# 背景替换（Background Swap）

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

基于主体原图（图A）和背景参照图（图B），保留主体身份、服装、姿态、镜头视角与前景关系，仅替换背景环境。参照图通过 BASE64 方式直接传入，继承父级 nano-banana API 契约。

## 触发条件

用户提供两张图（主体原图 + 背景参照图），要求保留主体，仅替换背景。典型表述：

- "背景替换" / "换背景" / "抠图换景"
- "保留这个人，把背景换成那张图里的环境"
- "主体不动，换成雪山/城市/摄影棚背景"
- "保留构图和动作，只改环境"

## 必需输入

| 参数 | 必填 | 说明 |
|------|------|------|
| `<主体图路径>` | 是 | 图A：主体原图，保留其身份/服装/姿态/构图 |
| `<背景图路径>` | 是 | 图B：背景参照图，提供环境空间与氛围 |
| `--desc` | 否 | 补充描述（如"保留夜景霓虹反光"、"改成清晨薄雾版本"） |
| `--output-dir` | 否 | 输出目录，默认与主体原图（图A）同目录 |
| `--filename` | 否 | 输出文件名（不含扩展名），默认 `<原文件名>-background-swap` |
| `--dry-run` | 否 | 仅打印生成命令，不实际调用 API |

## 执行流程

### Step 1 / 参数解析

- 第一个路径 → 图A（主体原图）
- 第二个路径 → 图B（背景参照图）
- 验证两张图片均存在且可读
- 确定输出目录（`--output-dir` 或默认与主体原图同目录）和文件名（`--filename` 或 `<原文件名>-background-swap`）

### Step 2 / 构建提示词

基础模板：

```text
保留图一中主体人物或主体物体的身份特征、服装造型、姿态动作、镜头视角、主体尺度和前景关系完全不变，仅将原有背景环境替换为图二中展示的场景空间与氛围。背景替换要求：完整吸收图二的空间结构、透视关系、主要环境元素、色彩氛围和光线方向；移除图一原背景中的无关建筑、地面、天空和室内陈设；主体边缘过渡自然，接地阴影、景深关系和空气透视合理。主体锁定：面部、发型、服装、肢体姿态、道具持握关系和主体构图位置严禁漂移。
```

若有 `--desc`，追加到模板末尾：

```text
补充要求：<desc>
```

关键约束：

- 提示词中"图一""图二"与 `--image-url` 传入顺序严格对应
- 主体锁定描述必须保留，不可省略或弱化
- 必须显式要求清除旧背景残留，避免前后景混杂

### Step 3 / 比例适配

用 `sips -g pixelWidth -g pixelHeight` 获取主体原图尺寸，计算宽高比并映射到最近的合法值：

| 合法值 | 适用场景 |
|--------|----------|
| `16:9` | 横版宽屏 |
| `9:16` | 竖版全身 |
| `4:3` | 横版标准 |
| `3:4` | 竖版半身 |
| `1:1` | 方形构图 |

比例从主体原图（图A）适配，而非背景参照图。

### Step 4 / 调用 API

```bash
python3 .agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "<完整提示词>" \
  --image-url "<主体图路径>" \
  --image-url "<背景图路径>" \
  --aspect-ratio "<适配后的比例>" \
  --output-dir "<输出目录>" \
  --output-filename "<输出文件名>"
```

关键说明：

- `--image-url` 每张图使用独立的 flag（`action="append"`），第一个为主体原图（图一），第二个为背景参照图（图二）
- 脚本内部自动将本地文件转为 BASE64 编码传入 API
- 继承父级 nano-banana API 契约（默认值注入、原生格式、BASE64 交接等）

### Step 5 / 输出

- 默认输出目录：与主体原图（图A）同目录；若显式传 `--output-dir`，允许覆盖
- 命名规则：`<原文件名>-background-swap.png`
- 若已存在同名文件，自动递增：`-background-swap-1.png`、`-background-swap-2.png`
- 永不覆盖原则：原始文件保持不变

## 错误处理

### 图片文件不存在

```text
错误：输入图片不存在
   主体图: path/to/missing.png
   提示: 请确认文件路径正确
```

### 只提供了一张图

```text
错误：缺少背景参照图
   提示: background-swap 需要两张图：第一张为主体原图，第二张为背景参照图
```

### API 调用失败

```text
错误：生图 API 调用失败
   错误: [API 错误信息]
   提示: 检查网络连接和 API 配置，或加 --dry-run 先检查提示词
```

## 调用示例

```bash
# 基础用法：主体图 + 背景图
/image:background-swap 角色A.png 雪山背景.png

# 带补充描述
/image:background-swap 角色.png 摄影棚背景.png \
  --desc "保留人物边缘发丝细节，并让地面反光与霓虹色温一致"

# 指定输出
/image:background-swap 角色.png 城市夜景.png \
  --output-dir output/影片/项目名/1-设定/1.2-角色/1.2.3-角色生成 \
  --filename 青青-夜景换景版

# dry-run 预览
/image:background-swap 角色.png 背景.png --dry-run
```

## 字段通过表（lite combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
|----------|----------|--------|----------|
| `FIELD-BGS-01` 双图输入 | 两张图均存在且路径有效 | `FAIL-BGS-INPUT` | Step 1 |
| `FIELD-BGS-02` 提示词构建 | 基础模板完整 + 图序正确 + 主体锁定描述在位 | `FAIL-BGS-PROMPT` | Step 2 |
| `FIELD-BGS-03` 比例适配 | 从主体原图正确读取尺寸并映射到合法枚举值 | `FAIL-BGS-RATIO` | Step 3 |
| `FIELD-BGS-04` 输出落盘 | 图片文件存在 + 不覆盖原文件 + 递增命名正确 | `FAIL-BGS-OUTPUT` | Step 5 |

## 依赖

- 脚本入口：`../scripts/nano_banana_generate.py`
- API 契约：继承 `../SKILL.md`（默认值注入、原生格式、BASE64 交接、项目化输出路径等）
- 环境变量：API Token 由 `nano_banana_generate.py` 内部从 `.env` 读取
- 系统工具：`sips`（macOS 原生，用于读取图片尺寸）

## Root-Cause 执行契约

当背景替换失败或输出不符预期时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：图序颠倒、主体锁定描述不足、旧背景残留、比例适配错误、输出覆盖原文件
-> `规则源`：本 `SKILL.md` + `../scripts/nano_banana_generate.py`
-> `规则源的规则源`：`../SKILL.md`（父级 API 契约）
-> `Fix Landing Points`：优先修本技能提示词模板和参数传递逻辑，再修父级脚本

用户侧关闭语必须包含：根因位置 + 立即修复 + 系统性预防修复
