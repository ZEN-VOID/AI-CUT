# 角色 3-生成执行报告

project: `projects/aigc/<项目名>/`
output_root: `projects/aigc/<项目名>/3-主体/角色/3-生成/`

## Targets

| 主体ID | 主体名称 | source_design_path | mode | verdict |
| --- | --- | --- | --- | --- |
| {{主体ID}} | {{主体名称}} | {{source_design_path}} | {{real_generation_or_prompt_only}} | {{verdict}} |

## Deliverables

| 主体ID | 主体名称 | 主图 | 主图 JSON | asset_reuse_decision | canvas_action | local_sync_status |
| --- | --- | --- | --- | --- | --- | --- |
| {{主体ID}} | {{主体名称}} | {{main_image_path}} | {{main_prompt_json_path}} | {{asset_reuse_decision}} | {{canvas_action}} | {{local_sync_status}} |

## LibTV Canvas Notes

- libtv canvas mode: {{libtv_canvas_mode}}
- canvas uuid: {{libtv_canvas_uuid}}
- model policy: {{model_policy}}
- model display name: {{model_display_name}}
- node name: {{libtv_node_name}}
- local sync action: {{confirm_local_canonical_present | download_generated_canvas_node | download_existing_canvas_node | copy_existing_local_to_canonical | prompt_only_pending}}
- local sync status: {{already_present | synced | copied | pending | blocked}}
- local asset path: {{local_asset_path}}
- download command: {{download_command_or_not_applicable}}
- multiview status: disabled_by_contract
- state variant suffix, if any: {{state_variant_suffix}}
- base reference node, if any: {{base_reference_node_name}}
- blocked reason, if any: {{blocked_reason}}

## Review Verdict

```yaml
verdict: pending
findings: []
review_status: ""
notes: ""
```

## LLM-First Authorship Evidence

- prompt_author: LLM runtime node
- forbidden_mechanical_generation: script concatenation, batch insertion, regex phrasing, synonym rotation, mapping projection
- evidence_required: each JSON prompt can point to upstream `4. 解构` and a role-specific LLM decision; JSON schema validity alone is not enough.

## Output Contract Alignment

| Output Contract field | Template alignment |
| --- | --- |
| Required output | 本模板汇总每个角色的一张主图和一份同名 JSON prompt 文件；多视图默认取消。 |
| Output format | 图片产物由 libTV 生成；JSON prompt 使用 `character-main-image-prompt-template.json`；报告为 Markdown。 |
| Output path | Canonical 路径为 `projects/aigc/<项目名>/3-主体/角色/3-生成/`。 |
| Naming convention | 主图为 `<主体ID>-<主体名称>-主图`，JSON 同名。 |
| Completion gate | source design 可回链；已完成既有主体图扫描；同主体同状态复用或上传；画布节点已下载或确认保存到项目 `角色/3-生成/`；状态变体使用 `Lib Image` 和参考节点；真实生成模式下图片节点存在；多视图未被生成、补齐或验收；prompt-only 模式阻断原因清楚。 |
