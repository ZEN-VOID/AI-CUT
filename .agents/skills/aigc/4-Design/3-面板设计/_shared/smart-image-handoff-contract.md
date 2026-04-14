# SMART Image Handoff Contract

## Purpose

本合同是 `.agents/skills/aigc/4-Design/3-面板设计` 各域叶子技能把 panel packet 桥接到 `.agents/skills/api/image/nano-banana/general` 的唯一共享真源。

目标：

1. 统一 `3-面板 -> nano-banana/general` 的 prompt / reference / output 路径合同
2. 明确 `SMART` 模式下何时自动转为参考图生图
3. 保持 panel packet 仍是 canonical business truth，PNG 与 request JSON 只是派生 sidecar

## SMART Mode

`SMART = Stage-aware Material Auto-Reference Transfer`

### 模式枚举

| mode | 适用场景 | 默认行为 |
| --- | --- | --- |
| `auto` | 未显式指定模式时 | `panel-stage` 上下文解析为 `continuous-batch`；直接对单个文档 / JSON 发起生图解析为 `single-doc-t2i` |
| `continuous-batch` | `1-主体清单 -> 2-主体设计 -> 3-面板设计` 的连续批量任务 | 自动把对应主体在 `2-主体设计` 目录里的图像资产并入 `images[]`，优先走 I2I |
| `single-doc-t2i` | 用户单独指定某个文档 / JSON / layout packet 发起生图 | 不做隐式 continuity ref 扫描；除非用户显式给参考图，否则按 T2I 处理 |
| `off` | 只产出 packet，不执行自动生图 | 不写 request sidecar，不调用 `nano-banana` |

## Packet Extension

各域 `3-面板` 输出的 layout packet 应统一补充 `image_generation` 段：

```json
{
  "image_generation": {
    "target_skill_id": "nano-banana-general",
    "smart_mode_default": "continuous-batch",
    "prompt_field": "prompt",
    "prompt_text": "...",
    "prompt_reference_sections": [
      "prompt",
      "prompt_segments.identity_prompt",
      "prompt_segments.layout_prompt"
    ],
    "reference_images": [],
    "explicit_references": [],
    "continuity_source_roots": [],
    "output_filename": "subject-panel.png",
    "request_id": "panel-subject-id"
  }
}
```

硬规则：

1. `prompt_text` 必须直接回链到 panel packet 已稳定写出的 prompt 真源，不得在桥接阶段临时二次改写。
2. `prompt_reference_sections` 必须显式列出 prompt 的引用来源，便于人工审阅与故障追因。
3. `reference_images` 记录 packet 已知参考图；`continuity_source_roots` 记录 SMART 扫描 `2-主体设计` 图像的根目录。
4. `output_filename` 只声明派生 PNG 名，不改变 layout packet 的 canonical 身份。

## Request Sidecar Contract

自动生图桥接层必须先写 request JSON sidecar，再调用 `nano-banana/general`。

推荐落点：

- request root: `projects/aigc/<项目名>/4-Design/<领域>/3-面板/第N集/generated/requests/`
- image output root: `projects/aigc/<项目名>/4-Design/<领域>/3-面板/第N集/generated/<packet_stem>/`

request JSON 必须至少包含：

```json
{
  "prompt": "...",
  "images": [{"url": "/abs/path/to/ref.png"}],
  "project_name": "项目名",
  "task_kind": "project",
  "request_id": "panel-subject-id",
  "output_dir": ".../generated/<packet_stem>",
  "output_filename": "subject-panel.png",
  "prompt_reference": {
    "smart_mode_requested": "auto",
    "smart_mode_resolved": "continuous-batch",
    "prompt_field": "image_generation.prompt_text",
    "prompt_reference_sections": ["..."],
    "source_layout_json": ".../layout.json",
    "packet_reference_images": [],
    "continuity_reference_images": [],
    "explicit_references": []
  }
}
```

说明：

- `prompt_reference` 是桥接审计元数据，供人读与追因；`nano_banana_generate.py` 只消费其标准输入字段。
- 若 resolved mode 为 `single-doc-t2i`，则 `continuity_reference_images` 必须为空。
- 若最终 `images[]` 为空，则视为 T2I；非空则视为 I2I。

## Canonical Governance

1. panel packet 是 `3-面板` 唯一业务真相。
2. request JSON、批量 request、PNG、nano 报告、bridge report 都是派生 sidecar。
3. 若不同域都需要自动生图，必须复用本合同与共享桥接脚本，不得在四个 leaf 中平行复制 SMART 规则。
