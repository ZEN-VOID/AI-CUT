# SMART Image Handoff Contract

本文件是 `4-Design/3-面板` 到内置 `$imagegen` / `image_gen` 的共享 handoff 真源。

## Canonical Rule

`3-面板` leaf 必须先写 layout JSON，再构造内置 imagegen 标准 request sidecar。默认按 `.agents/skills/aigc/_shared/image-generation-execution-contract.md` 由 Codex 会话调用内置 `image_gen` 生图，默认模型口径为 `GPT-IMAGE-2`；显式 `--layout-only`、`--json-only` 或 `--request-only` 时只交付 layout JSON、request sidecar 与 bridge report。

## SMART Mode

| mode | 触发 | references policy | imagegen route |
| --- | --- | --- | --- |
| `continuous-batch` | 由 `4-Design` 系列批量调度，或只给 `--project + --episode` 批量处理设计目录 | 自动扫描 layout 中声明的 `continuity_source_roots`、设计目录同级图片与 `projects/aigc/<项目名>/Assets/<域>/` 中匹配主体的已有图片 | 有图则 I2I，无图则 T2I |
| `single-doc-t2i` | 显式 `--prompt-file` 指向单文件、目录、单个 JSON/Markdown，或 direct-request 上下文 | 默认不隐式扫描 continuity refs；只使用用户显式给出的参考图 | 默认 T2I |
| `natural-language-t2i` | 显式 `--prompt-text` 或会话自然语言要求生图 | 默认不隐式扫描 continuity refs；只使用用户显式给出的参考图 | 默认 T2I |

## Request JSON Shape

```json
{
  "tasks": [
    {
      "prompt": "panel-ready prompt text",
      "images": [{"url": "/abs/path/or/https-url"}],
      "project_name": "<项目名>",
      "task_kind": "project",
      "provider_skill": "imagegen",
      "provider_mode": "built-in image_gen",
      "default_model": "GPT-IMAGE-2",
      "aspect_ratio": "16:9",
      "image_size": "4K",
      "request_id": "ROLE-001-角色名-baseline-CharacterPanel",
      "output_dir": "projects/aigc/<项目名>/4-Design/角色/3-面板/第1集/generated/ROLE-001",
      "output_filename": "ROLE-001-角色名-baseline-CharacterPanel.png",
      "prompt_reference": {
        "smart_mode_requested": "auto",
        "smart_mode_resolved": "continuous-batch",
        "prompt_field": "prompt_payload.prompt_text",
        "source_layout_json": "projects/aigc/<项目名>/4-Design/角色/3-面板/第1集/ROLE-001-角色名-baseline-CharacterPanel-layout.json"
      }
    }
  ]
}
```

## Hard Gates

1. `prompt` 必须来自 leaf layout JSON 中的稳定 prompt 字段。
2. `images[]` 只能来自 SMART 规则或用户显式参考图；不得在 single/natural 模式下隐式扫描 continuity refs。
3. `prompt_reference.source_layout_json` 必须回链到实际存在的 layout JSON。
4. request sidecar 默认落到 `projects/aigc/<项目名>/4-Design/<域>/3-面板/第N集/generated/requests/panel_auto_generate_batch.json`。
5. `--layout-only / --json-only` 必须仍通过共享 bridge 写 request sidecar 与 bridge report，但以 `request-sidecar-only` 停点退出，不调用内置 `image_gen`。
6. active leaf 不得私造第二套 API payload、Assets 扫描或 SMART mode 解析；统一调用 `_shared/panel_auto_generate.py`。
7. 默认请求准备态必须写 `status=request_ready`、`execution_mode=codex-builtin-imagegen`、`provider_skill=imagegen`、`provider_mode=built-in image_gen` 与 `default_model=GPT-IMAGE-2`；只有真实图片文件复制回项目后才允许把本轮结果写成完成。
