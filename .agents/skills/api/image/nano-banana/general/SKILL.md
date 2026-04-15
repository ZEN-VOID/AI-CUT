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
- `.agents/skills/aigc/4-Design/2-设计` 已完成单一主体设计文件，希望直接自动生图，且当前目标只是通用概念图而非多视图版式
- `.agents/skills/aigc/4-Design/3-面板` 已输出 panel packet / SMART request sidecar，需要承接稳定的 `prompt + images[]`

意图模糊时默认走本技能。

## 2. API 契约继承

本技能不重复定义 API 参数、默认值、请求格式、并发调度与落盘规则——全部继承父级：

- 参数枚举与默认值：`../SKILL.md` §3
- 执行流程：`../SKILL.md` §5
- 输出约定：`../SKILL.md` §7
- 失败排查：`../SKILL.md` §10

如需查阅完整契约，先读父级 `../SKILL.md`。

## 3. 设计阶段 Prompt 引用（Mandatory）

当本技能被 `.agents/skills/aigc/4-Design/2-设计/SKILL.md` 以 `auto-image-fast-path` 调用时，prompt 必须直接读取上游已稳定 design carrier，并遵守 `.agents/skills/aigc/4-Design/2-设计/_shared/design-output-contract.md`。

关键约束：

1. 入参 `prompt` 必须是 `full_generation_prompt`。
2. `full_generation_prompt` 必须包含统一 `global_style_prefix`。
3. 图片必须写回主体设计文件同目录，文件 stem 与设计文件一致。
4. 本技能不得在通用层重新润色、改写或替换上游 prompt。

### 3.1 上游 prompt 真源表

| design 域 | 第一引用 | 允许回退 | 输出路径规则 |
| --- | --- | --- | --- |
| `场景` | `scene_design.json.scenes[].full_generation_prompt` | `global_style_prefix + scene_design.json.scenes[].design_prompt` 或 `[场景名].md / prompt整合` | `[场景名].md` 同目录同 stem |
| `角色` | `character_design.json.roles[].full_generation_prompt` | `global_style_prefix + character_design.json.roles[].prompt_integration` 或 `[角色名].md / prompt整合` | `[角色名].md` 同目录同 stem |
| `道具` | `<prop_id>-<canonical_name>.md / full_generation_prompt` | `global_style_prefix + Markdown **prompt整合**` | `<prop_id>-<canonical_name>.md` 同目录同 stem |
| `服装` | reserved | reserved | reserved |

### 3.2 硬规则

1. 若上游 `full_generation_prompt` 为空、缺失或不含全局风格前缀，必须阻塞并回到对应 design skill 修源层，不得在本技能里临时造 prompt。
2. 可把上游 `negative_constraints / reverse_taboos / render_hints` 合并为补充约束，但不得覆盖主 prompt 的真源位置。
3. 若上游已经绑定稳定参照图，可按 I2I 调用；否则按 T2I 调用。
4. 设计阶段快路径产物是 derived asset，不会反向改写上游 design master。
5. 如果调用方显式传入 `--output-dir` 与 `--output-filename`，必须尊重调用方的同目录同名策略。

### 3.3 `2-设计` 单主体快路径示例

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --project-name "<项目名>" \
  --task-kind project \
  --prompt "<full_generation_prompt>" \
  --output-dir "projects/aigc/<项目名>/4-Design/场景/2-设计/第1集" \
  --output-filename "<场景名>.png" \
  --no-report
```

推荐由共享 helper 调用：

```bash
python3 .agents/skills/aigc/4-Design/2-设计/_shared/scripts/run_design_auto_image.py \
  --design-file "projects/aigc/<项目名>/4-Design/场景/2-设计/第1集/<场景名>.md"
```

### 3.4 `3-面板` SMART request sidecar

当上游来自 `.agents/skills/aigc/4-Design/3-面板/_shared/smart-image-handoff-contract.md` 时，推荐直接承接 request JSON sidecar：

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --input-json projects/aigc/<项目名>/4-Design/角色/3-面板/第1集/generated/requests/panel_auto_generate_batch.json
```

推荐任务字段：

```json
{
  "prompt": "已经由 panel packet 收束好的最终提示词",
  "images": [{"url": "/abs/path/to/reference.png"}],
  "project_name": "项目名",
  "task_kind": "project",
  "request_id": "panel-role-001",
  "output_dir": "projects/aigc/<项目名>/4-Design/角色/3-面板/第1集/generated/role-001",
  "output_filename": "role-001-CharacterPanel.png",
  "prompt_reference": {
    "smart_mode_requested": "auto",
    "smart_mode_resolved": "continuous-batch",
    "prompt_field": "image_generation.prompt_text",
    "prompt_reference_sections": [
      "prompt_payload.prompt_text",
      "prompt_payload.prompt_segments.identity_prompt",
      "prompt_payload.prompt_segments.layout_prompt"
    ],
    "source_layout_json": "projects/aigc/<项目名>/4-Design/角色/3-面板/第1集/role-001-CharacterPanel-layout.json"
  }
}
```

硬规则：

1. `prompt_reference` 是桥接审计元数据；本技能只消费标准输入字段，不在通用层二次改 prompt。
2. `smart_mode_resolved=continuous-batch` 且 `images[]` 非空时按 I2I 执行。
3. 用户单独指定某个文档或 JSON 发起生图，且 sidecar 未显式给参考图时，默认按 T2I 执行。

## 4. 标准调用示例

脚本入口统一为：

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py [参数]
```

### 4.1 最小调用（只传 prompt）

未指定比例与清晰度时，父级契约自动补齐 `16:9 / 4K`。

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --prompt "一只坐在霓虹雨夜巷口的黑猫，电影剧照感"
```

### 4.2 显式指定比例与清晰度

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --project-name "赛博唐人街" \
  --task-kind project \
  --prompt "未来感竖版海报，银蓝霓虹，强透视" \
  --aspect-ratio 9:16 \
  --image-size 2K
```

### 4.3 参考图生图（I2I）

建议加 `--no-report` 减少冗余文件。

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --project-name "赛博唐人街" \
  --task-kind project \
  --prompt "保留人物身份，将场景改为旧上海街头，黄昏潮湿空气，胶片质感" \
  --image-url "https://example.com/ref-1.jpg" \
  --no-report
```

### 4.4 承接上游结构化请求

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
  "caller_skill": ".agents/skills/aigc/4-Design/2-设计/角色",
  "episode_id": "第1集",
  "aspect_ratio": "",
  "image_size": null,
  "images": [{"url": "https://example.com/ref.png"}],
  "request_id": "shot-001",
  "output_dir": "projects/aigc/<项目名>/4-Design/角色/2-设计/第1集/",
  "output_filename": "角色名.png"
}
```

空字符串或 `null` 的参数会被父级默认值契约自动补齐。若未显式传 `output_dir`，脚本会优先按 `caller_skill + episode_id` 推导默认输出路径。

### 4.5 多任务自动并发

当 `--input-json` 内容为对象数组或含 `tasks[]` 时，自动进入并发模式。

```bash
python3 .agents/skills/api/image/nano-banana/scripts/nano_banana_generate.py \
  --input-json /tmp/nano_banana_batch.json \
  --max-concurrent 100
```

默认最大并发 `100`，硬上限 `100`。详见父级 `../SKILL.md` §3.8。

## 5. 输出规范

继承父级 `../SKILL.md` §7，不做额外扩展。

- 默认输出目录：
  - 直调 `general` 且未声明调用方 skill：`output/影片/[项目名]/5-API/image/nano-banana/general/`
  - 若上游传入 `caller_skill`：优先跟随该技能包的默认输出路径
  - I2I（有参考图）且调用方是输入图驱动子技能时：与第一张本地参考图同目录
- 产物：图片文件 + 可选 report JSON
- 下游交接：默认 `BASE64` 透传
- 若显式传 `--output-dir`，允许覆盖默认路径
- 永不覆盖原则：原始文件保持不变
- 若上游显式把 `output_dir` 指到 `projects/aigc/<项目名>/4-Design/.../2-设计/第N集/` 并指定 `output_filename`，则应保留该同目录同名策略，不回退到默认目录

## 6. 字段通过表（Lite Combined）

| field_id | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- |
| `FIELD-GEN-01` prompt 收束 | `prompt` 非空，参考图（若有）结构稳定 | `FAIL-GEN-INPUT` | 检查输入参数，回查父级 §3.1 |
| `FIELD-GEN-02` 参数合规 | 继承父级默认值契约：缺失时补齐 `16:9 / 4K`，显式值不被覆盖 | `FAIL-GEN-PARAMS` | 回查父级 §3 核心约束 |
| `FIELD-GEN-03` 输出落盘 | 图片文件可定位，report（若启用）字段完整，下游可追溯 | `FAIL-GEN-OUTPUT` | 回查父级 §7 输出约定 |

## 7. Root-Cause 执行契约

继承父级 `../SKILL.md` §9。通用生图场景下的补充排查优先级：

1. prompt 是否为空或被截断
2. 若来自 `4-Design/2-设计`，prompt 是否按三域真源表读取且包含 `global_style_prefix`，而不是临时改写
3. 参数是否被父级默认值正确补齐
4. 参考图（若有）是否成功转为 `inline_data`
5. 若来自 `4-Design/3-面板`，先确认 `prompt_reference.prompt_field` 是否能回链到 panel packet 真源字段
6. 若是单文档 / 单 JSON 请求，确认是否被错误塞入 continuity refs
7. 上溯父级完整排查链路
