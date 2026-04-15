---
name: nano-banana-costume-swap
version: "v1.0"
governance_tier: lite
description: |
  角色换装：保留角色形象不变，将服装替换为参照图中的服装样式。当用户要求"换装"、"换衣服"、"保留角色换服装"、"服装替换"时使用本技能。底层调用 nano-banana API（继承父级 `nano-banana/SKILL.md` 契约）。
tools: [Read, Write, Edit, Bash]
---

# 角色换装（Costume Swap）

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

基于角色原图（图A）和服装参照图（图B），保留角色的面部、发型、体态等身份特征不变，仅将服装替换为图B中的服装样式。参照图通过 BASE64 方式直接传入，继承父级 nano-banana API 契约。

## 触发条件

用户提供两张图（角色原图 + 服装参照图），要求保留角色身份特征，仅替换服装。典型表述：
- "换装" / "换衣服" / "保留角色换服装" / "服装替换"
- "把 A 的衣服换成 B 的"
- "保留角色形象，穿上这套服装"

## 必需输入

| 参数 | 必填 | 说明 |
|------|------|------|
| `<角色图路径>` | 是 | 图A：角色原图，保留其面部/发型/体态 |
| `<服装图路径>` | 是 | 图B：服装参照图（单品图、穿着图、设计稿均可） |

可选参数：

| 参数 | 说明 |
|------|------|
| `--desc` | 补充描述服装细节（如"改为冬季厚重版本"、"保留原色但换为丝绸材质"） |
| `--keep-pose` | 保持原图姿态不变（默认开启） |
| `--output-dir` | 输出目录，默认与角色原图（图A）同目录 |
| `--filename` | 输出文件名（不含扩展名），默认 `<原文件名>-costume-swap` |
| `--dry-run` | 仅打印生成命令，不实际调用 API |

## 执行流程

### Step 1 / 参数解析

- 第一个路径 → 图A（角色原图）
- 第二个路径 → 图B（服装参照图）
- 验证两个文件均存在；任一缺失立即报错退出
- 确定输出目录（`--output-dir` 或默认与角色原图同目录）和文件名

### Step 2 / 构建提示词

基础模板：

```text
保留图一中角色的面部特征、发型发色、肤色、体态比例和姿态完全不变，仅将角色身上的服装整体替换为图二中展示的服装样式。服装替换要求：完整还原图二服装的剪裁版型、面料质感、色彩配色、装饰细节（纽扣/刺绣/腰带/配饰等）和层次结构；服装需自然贴合图一角色的体型，保持衣物褶皱和垂坠的物理合理性。身份锁定：面部五官、发型、肤色、体态比例严禁漂移。
```

若用户提供了 `--desc`，追加到模板末尾：

```text
补充要求：<desc>
```

关键约束：
- 提示词中"图一""图二"与 `--image-url` 的传入顺序严格对应
- 身份锁定描述必须保留，不可省略或弱化

### Step 3 / 比例适配

用 `sips -g pixelWidth -g pixelHeight` 获取角色原图尺寸，计算宽高比并映射到最近的合法值：

| 合法值 | 适用场景 |
|--------|----------|
| `16:9` | 横版宽屏 |
| `9:16` | 竖版全身 |
| `4:3` | 横版标准 |
| `3:4` | 竖版半身 |
| `1:1` | 方形头像 |

比例从角色原图（图A）适配，而非服装参照图。

### Step 4 / 调用 API

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "<完整提示词>" \
  --image-url "<角色图路径>" \
  --image-url "<服装图路径>" \
  --aspect-ratio "<适配后的比例>" \
  --output-dir "<输出目录>" \
  --output-filename "<输出文件名>"
```

关键说明：
- `--image-url` 每张图使用独立的 flag（`action="append"`），第一个为角色原图（图一），第二个为服装参照图（图二）
- 脚本内部自动将本地文件转为 BASE64 编码传入 API
- 继承父级 nano-banana API 契约（默认值注入、原生格式、BASE64 交接等）

### Step 5 / 输出

- 默认输出目录：与角色原图（图A）同目录；若显式传 `--output-dir`，允许覆盖
- 命名规则：`<原文件名>-costume-swap.png`
- 若已存在同名文件，自动递增：`-costume-swap-1.png`、`-costume-swap-2.png`
- 永不覆盖原则：原始文件保持不变

## 错误处理

### 图片文件不存在

```text
错误：输入图片不存在
   角色图: path/to/missing.png
   提示: 请确认文件路径正确
```

### 只提供了一张图

```text
错误：缺少服装参照图
   提示: costume-swap 需要两张图：第一张为角色原图，第二张为服装参照图
```

### API 调用失败

```text
错误：生图 API 调用失败
   错误: [API 错误信息]
   提示: 检查网络连接和 API 配置，或加 --dry-run 先检查提示词
```

## 调用示例

```bash
# 基础用法：角色图 + 服装图
/image:costume-swap 角色A.png 服装参照.png

# 带补充描述
/image:costume-swap 角色.png 服装.png \
  --desc "保留图B服装的整体剪裁与配色，但将面料质感改为做旧棉麻"

# 指定输出
/image:costume-swap 角色.png 服装.png \
  --output-dir output/影片/项目名/1-设定/1.2-角色/1.2.3-角色生成 \
  --filename 青青-换装版

# dry-run 预览
/image:costume-swap 角色.png 服装.png --dry-run
```

## 字段通过表（lite combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
|----------|----------|--------|----------|
| `FIELD-CS-01` 双图输入 | 两张图均存在且路径有效 | `FAIL-CS-INPUT` | Step 1 |
| `FIELD-CS-02` 提示词构建 | 基础模板完整 + 图序正确 + 身份锁定描述在位 | `FAIL-CS-PROMPT` | Step 2 |
| `FIELD-CS-03` 比例适配 | 从角色原图正确读取尺寸并映射到合法枚举值 | `FAIL-CS-RATIO` | Step 3 |
| `FIELD-CS-04` 输出落盘 | 图片文件存在 + 不覆盖原文件 + 递增命名正确 | `FAIL-CS-OUTPUT` | Step 5 |

## 依赖

- 脚本入口：`../scripts/nano_banana_generate.py`
- API 契约：继承 `../SKILL.md`（默认值注入、原生格式、BASE64 交接、项目化输出路径等）
- 环境变量：API Token 由 `nano_banana_generate.py` 内部从 `.env` 读取
- 系统工具：`sips`（macOS 原生，用于读取图片尺寸）
