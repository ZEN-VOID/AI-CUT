---
name: nano-banana-general
version: "v1.0"
governance_tier: lite
description: |
  nano-banana 通用生图入口。当用户要求"生张图"、"文本生图"、"参考图生图"但不涉及换脸、换装、多视图等特化场景时，使用本技能。支持单任务直调、结构化 JSON 承接、多任务自动并发。所有 API 契约（参数枚举、默认值、请求格式）继承父级 `nano-banana/SKILL.md`。
tools: [Read, Write, Edit, Bash]
---

# nano-banana 通用生图

## 1. 触发条件

用户意图属于以下任一场景，且不涉及换脸、换装、多视图等特化 prompt 需求：

- "帮我生张图" / "文本生图" / "T2I"
- "参考这张图再生一张" / "参考图生图" / "I2I"
- 上游流程输出了结构化生图请求但未指定特化子技能

意图模糊时默认走本技能。

## 2. API 契约继承

本技能不重复定义 API 参数、默认值、请求格式、并发调度与落盘规则——全部继承父级：

- 参数枚举与默认值：`../SKILL.md` §3
- 执行流程：`../SKILL.md` §5
- 输出约定：`../SKILL.md` §7
- 失败排查：`../SKILL.md` §10

如需查阅完整契约，先读父级 `../SKILL.md`。

## 3. 标准调用示例

脚本入口统一为：

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py [参数]
```

### 3.1 最小调用（只传 prompt）

未指定比例与清晰度时，父级契约自动补齐 `16:9 / 4K`。

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "一只坐在霓虹雨夜巷口的黑猫，电影剧照感"
```

### 3.2 显式指定比例与清晰度

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --project-name "赛博唐人街" \
  --task-kind project \
  --prompt "未来感竖版海报，银蓝霓虹，强透视" \
  --aspect-ratio 9:16 \
  --image-size 2K
```

### 3.3 参考图生图（I2I）

建议加 `--no-report` 减少冗余文件。

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --project-name "赛博唐人街" \
  --task-kind project \
  --prompt "保留人物身份，将场景改为旧上海街头，黄昏潮湿空气，胶片质感" \
  --image-url "https://example.com/ref-1.jpg" \
  --no-report
```

### 3.4 承接上游结构化请求

当上游流程已输出 JSON 文件时，用 `--input-json` 直接承接，无需手动拆字段。

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --input-json /tmp/nano_banana_request.json
```

JSON 结构示例：

```json
{
  "prompt": "东方奇幻山门，云雾缭绕，清晨金光",
  "project_name": "测试",
  "task_kind": "test",
  "aspect_ratio": "",
  "image_size": null,
  "images": [{"url": "https://example.com/ref.png"}],
  "request_id": "shot-001"
}
```

空字符串或 `null` 的参数会被父级默认值契约自动补齐。

### 3.5 多任务自动并发

当 `--input-json` 内容为对象数组或含 `tasks[]` 时，自动进入并发模式。

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --input-json /tmp/nano_banana_batch.json \
  --max-concurrent 100
```

默认最大并发 `100`，硬上限 `100`。详见父级 `../SKILL.md` §3.8。

## 4. 输出规范

继承父级 `../SKILL.md` §7，不做额外扩展。

- 默认输出目录：
  - T2I（无参考图）：`output/影片/[项目名]/5-API/image/nano-banana/general/`
  - I2I（有参考图）：与参考图同目录，命名 `<参考图文件名>-general.png`，递增防覆盖
- 产物：图片文件 + 可选 report JSON
- 下游交接：默认 `BASE64` 透传
- 若显式传 `--output-dir`，允许覆盖默认路径
- 永不覆盖原则：原始文件保持不变

## 5. 字段通过表（Lite Combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- |
| `FIELD-GEN-01` prompt 收束 | `prompt` 非空，参考图（若有）结构稳定 | `FAIL-GEN-INPUT` | 检查输入参数，回查父级 §3.1 |
| `FIELD-GEN-02` 参数合规 | 继承父级默认值契约：缺失时补齐 `16:9 / 4K`，显式值不被覆盖 | `FAIL-GEN-PARAMS` | 回查父级 §3 核心约束 |
| `FIELD-GEN-03` 输出落盘 | 图片文件可定位，report（若启用）字段完整，下游可追溯 | `FAIL-GEN-OUTPUT` | 回查父级 §7 输出约定 |

## 6. Root-Cause 执行契约

继承父级 `../SKILL.md` §9。通用生图场景下的补充排查优先级：

1. prompt 是否为空或被截断
2. 参数是否被父级默认值正确补齐
3. 参考图（若有）是否成功转为 `inline_data`
4. 上溯父级完整排查链路
