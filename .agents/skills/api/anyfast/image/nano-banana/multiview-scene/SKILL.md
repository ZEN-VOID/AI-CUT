---
name: nano-banana-multiview-scene
version: "v1.0"
governance_tier: lite
description: |
  多视图布局-场景：基于参照图 + 场景描述，生成 3x3 九宫格多视图场景设计页（16:9）。当用户要求"场景多视图"、"场景设计页"、"场景九宫格"、"SCENE_DESIGN_SHEET"时使用本技能。底层调用 nano-banana API（继承父级契约）。
tools: [Read, Write, Edit, Bash]
---

# 多视图布局-场景（Multiview Scene Design Sheet）

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

基于一张或多张参照图，结合场景主体描述，生成 16:9 九宫格布局的场景设计页。参照图默认通过 BASE64 方式直接传入，无需上传 COS。

## 触发条件

用户提供一张或多张场景参照图 + 场景主体描述，要求生成多视图场景设计页。
关键词匹配：场景多视图、场景设计页、场景九宫格、SCENE_DESIGN_SHEET。

## 必需输入

| 参数 | 必填 | 说明 |
|------|------|------|
| `<图片路径...>` | 是 | 一张或多张本地图片路径，空格分隔 |
| `--id` | 是 | 场景ID，如 `SCN-001` |
| `--name` | 是 | 场景名称 |
| `--desc` | 是 | 中文场景主体描述，400字以内；涵盖建筑形制、空间尺度、材质肌理、光影氛围、色彩基调 |
| `--output-dir` | 否 | 输出目录，默认与第一张输入图同目录 |
| `--filename` | 否 | 输出文件名（不含扩展名），默认 `<原文件名>-multiview` |
| `--dry-run` | 否 | 仅打印生成命令，不实际调用 API |

## 执行流程

### Step 1 / 参数解析

- 提取所有图片路径（支持相对路径，自动转绝对路径）
- 提取 `--id`、`--name`、`--desc` 参数
- 确定输出目录和文件名

### Step 2 / 构建提示词

使用固定模板，将用户参数注入：

```text
### 场景ID: <scene_id>
保留图一画面风格和场景形象不变，根据以下要求调整为多视图构图展示：
设计主体：<desc>
空镜头护栏：画面中不出现任何人物、人形剪影、生物或人影。
布局规格：SCENE_DESIGN_SHEET模板，16:9画幅，4K分辨率（4096x2304），深色中性背景（#1a1a1a），严格3x3九宫格，均匀间距与面板比例，干净分割线，无装饰性边框噪声。
布局模块（9个面板各自拍摄要求）：
  P1 氛围全景：平视广角全景，建立完整空间包络与主光源逻辑，展示场景全貌与纵深关系；
  P2 氛围中景：中景展示功能分区与叙事中心，保留建筑主体与周边环境的空间关系；
  P3 氛围特写：近距离建筑/材质细节特写，保持与全景相同的年代与建造语法；
  P4 东向视图：场景东侧方向性正交视图，保持比例与透视纪律；
  P5 西向视图：场景西侧方向性正交视图，与P4形成对称参照；
  P6 低角度仰拍：低机位向上仰拍，展示建筑高度、檐角轮廓与天空关系；
  P7 南向视图：场景南侧方向性正交视图，保持与P4/P5一致的比例纪律；
  P8 北向视图：场景北侧方向性正交视图，完成四方位空间验证；
  P9 高角度俯拍：高机位向下俯瞰，展示场景平面布局、屋顶形制与空间层次。
一致性约束：
  光照连续性：所有面板共享相同主光源方向与强度，保持物理一致；
  材质连续性：材质家族与纹理老化状态跨面板保持稳定，不可漂移；
  构图纪律：面板尺寸均等、分割线干净、无重叠、无装饰性边框噪声；
  锚点道具身份锁定：场景中的标志性元素在所有面板中保持数量、轮廓、比例、材质一致。
身份标识：左上角固定身份标识徽章 <scene_id> <scene_name>，位置与字体跨输出保持稳定。
```

替换规则：
- `<scene_id>` → `--id` 值
- `<scene_name>` → `--name` 值
- `<desc>` → `--desc` 值

### Step 3 / 调用 API

工具路径：`.agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py`

```bash
python3 .agents/skills/api/anyfast/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "<完整提示词>" \
  --image-url "<图片路径1>" \
  --aspect-ratio "16:9" \
  --output-dir "<输出目录>" \
  --output-filename "<输出文件名>" \
  --no-report
```

关键说明：
- `--image-url` 每张图使用独立的 `--image-url` flag（`action="append"`），脚本内部自动读取并转为 BASE64 传入 API
- `--aspect-ratio` 固定为 `16:9`（九宫格标准画幅）
- `--no-report` 不输出 report JSON 文件，仅输出图片
- 第一张图为主参照图（"图一"），后续图为辅助参照

### Step 4 / 输出

默认输出目录：与第一张输入图同目录；若显式传 `--output-dir`，允许覆盖。

命名规则：`<原文件名>-multiview.png`
- 若已存在同名文件，自动递增：`-multiview-1.png`、`-multiview-2.png`
- 永不覆盖原则：原始文件保持不变

## 错误处理

| 错误场景 | 提示信息 | 处理方式 |
|----------|----------|----------|
| 图片文件不存在 | 输入图片不存在，请确认文件路径正确 | 中止执行 |
| 描述为空或超400字 | 场景描述不符合要求，请精简至400字以内 | 中止执行 |
| API 调用失败 | 生图 API 调用失败，检查网络连接和 API 配置 | 可加 `--dry-run` 先检查提示词 |

## 调用示例

```bash
# 单张参照图
/image:multiview-scene 通天塔外观.png \
  --id SCN-001 --name 通天塔外观 \
  --desc "赛博朋克风格的巨型建筑外观..."

# 多张参照图 + 指定输出
/image:multiview-scene ref1.png ref2.png \
  --id SCN-002 --name 地下酒吧 \
  --output-dir output/影片/东方三侠2026/1-设定/1.3-场景/1.3.3-场景生成 \
  --desc "..."
```

## 字段通过表（lite combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
|----------|----------|--------|----------|
| FIELD-MVS-01 输入完整 | 图片+id+name+desc 齐全 | FAIL-MVS-INPUT | Step 1 |
| FIELD-MVS-02 提示词构建 | 模板注入正确，九宫格规格完整 | FAIL-MVS-PROMPT | Step 2 |
| FIELD-MVS-03 空镜头护栏 | 无人物/人影出现 | FAIL-MVS-EMPTY-SCENE | Step 2 |
| FIELD-MVS-04 输出落盘 | 16:9 图片存在+不覆盖 | FAIL-MVS-OUTPUT | Step 4 |

## 依赖

- `../scripts/nano_banana_generate.py`
- API 契约继承 `../SKILL.md`
- 环境变量：API Token（由 nano_banana_generate.py 内部管理）

## 相关技能

- `multiview-character`：角色多视图布局
- `multiview-prop`：道具多视图布局
