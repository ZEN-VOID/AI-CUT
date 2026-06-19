# 道具生成执行报告

project: `projects/aigc/<项目名>`
output_dir: `projects/aigc/<项目名>/3-主体/道具/3-生成`

## 生成资产

| 主体ID | 主体 | 上游设计文档 | 主图 | 主图 JSON | asset_reuse_decision | canvas_action | local_sync_status | multiview_status | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<主体ID>` | `<主体名称>` | `3-主体/道具/2-设计/<主体名称>.md` | `<主体ID>-<主体名称>-主图.png` | `<主体ID>-<主体名称>-主图.json` | `generate_new_subject` | `create_new_node` | `synced` | `disabled_by_contract` | `pending` |

## LibTV Canvas Notes

```yaml
libtv_canvas_mode: libtv_canvas_generate
libtv_canvas_uuid: ""
model_policy: new_subject_midjourney_default | state_variant_lib_image
model_display_name: Midjourney V8.1 | Lib Image
state_variant_suffix: ""
base_reference_node_name: ""
local_sync_action: confirm_local_canonical_present | download_generated_canvas_node | download_existing_canvas_node | copy_existing_local_to_canonical | prompt_only_pending
local_sync_status: already_present | synced | copied | pending | blocked
local_asset_path: projects/aigc/<项目名>/3-主体/道具/3-生成/<主体ID>-<主体名称>-主图.<ext>
download_command: libtv download -p <canvas_uuid> -n <node_id_or_node_name> -o projects/aigc/<项目名>/3-主体/道具/3-生成 | not_applicable
```

## 顾问与复核流程 Status

```yaml
worker: Worker-道具生成
reviewer: ""
review_status: external_reviewer | local_checklist | not_requested
local_checklist:
  findings: []
  repair_actions: []
```

## Review Verdict

```yaml
verdict: pass | pass_with_followups | needs_rework | blocked
checked_at: ""
findings: []
next_action: ""
```

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 每个主体一张单主体图、一个单主体 JSON；多视图默认取消。 |
| Output format | 图像资产为 PNG/JPEG/WebP；提示词为 JSON；执行报告为 Markdown。 |
| Output path | canonical path 为 `projects/aigc/<项目名>/3-主体/道具/3-生成/`。 |
| Naming convention | 单体图 `主体ID-主体名称-主图`；JSON 与对应图像同 stem。 |
| Completion gate | 每组资产回指上游 `2-设计` 文档，主图引用 `4. 解构`，已完成既有主体图扫描；同主体同状态复用或上传；画布节点已下载或确认保存到项目 `道具/3-生成/`；状态变体使用 `Lib Image` 和参考节点；多视图未被生成、补齐或验收；已完成 review verdict。 |
