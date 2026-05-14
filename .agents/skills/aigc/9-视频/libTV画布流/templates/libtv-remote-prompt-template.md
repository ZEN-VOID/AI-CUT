# LibTV Remote Prompt Template

本模板区分两层内容：

- `handoff_message`：发给 LibTV Agent IM 的外层执行指令，可包含模式、参数、参考图绑定和禁止优化要求。
- `create_generation_task.params.prompt`：视频节点真正使用的创作提示词，只能是干净创作正文。

不得把 `handoff_message` 中的执行锁、生成参数、参考图清单、主体绑定诊断、missing/excluded 原因、文件路径或审计说明复制进 `create_generation_task.params.prompt`。

## Handoff Message

外层消息用于指挥 LibTV Agent IM 创建视频任务。花括号字段由执行者投影，不得保留占位文本发送。

```text
把全部工作流和结果都放在画布上。
创建一个“全能参考 / 多图主体参考生成视频”任务，modeType=mixed2video，duration={duration}，resolution={resolution}，ratio={ratio}，download=false，allow_libtv_prompt_optimization=false。
禁止优化、改写、扩写、压缩、总结、重排、翻译或补全 create_generation_task.params.prompt；不要新增镜头，不要合并分镜。
create_generation_task.params.prompt 必须严格等于下方【VIDEO_PROMPT】内的内容；不要把本段执行指令、生成参数、主体绑定表、缺失/排除原因或文件路径复制进 params.prompt。
参考图必须按 yaml_name/category/node_key/URL 绑定；不要按上传图片顺序、Image N、imageList 顺序或缩略图顺序匹配主体。
REFERENCE_BINDINGS_FOR_TOOL_PARAMS_ONLY 是唯一参照真源：每个主体的 `@` 资产引用、source_node_keys、source_node_url_mapping 和 imageList/mixedList 都必须由 yaml_name 查表得到对应 node_key/URL 后生成。数组顺序、图1/图2、Portrait 1/2、上传先后顺序没有任何主体语义权重。
imageList/mixedList、source_node_keys 和 source_node_url_mapping 的传入顺序必须按 YAML 主体展示顺序排序：先 `角色` 原顺序，再 `场景` 原顺序，再 `道具` 原顺序；若超过 9 张，先按预算规则筛选，再保持剩余主体的 YAML 相对顺序。不得使用上传顺序、画布创建时间或本地文件扫描顺序。

【REFERENCE_BINDINGS_FOR_TOOL_PARAMS_ONLY】
{selected_reference_bindings_yaml}

【VIDEO_PROMPT】
{clean_video_prompt}
```

## Assembly Rules

- `clean_video_prompt` 由两部分组成：`## x-y-z` 下的分镜组正文 + 底部完整 fenced YAML 内容。
- `clean_video_prompt` 不包含执行锁、生成参数、`YAML主体清单`、`主体绑定表`、参考图清单、missing/excluded 诊断、manifest 路径或 submit plan 字段。
- 底部 YAML 必须完整保留原字段和值，包括 `字数统计`、`时长估算`、`角色`、`场景`、`道具` 等；不得只摘要成主体清单。
- 每个已绑定 YAML 主体在分镜组正文第一次出现时，必须在主体名后插入 LibTV 画布 `@` 资产引用 / node mention（标准名称待官方确认）。
- 底部 YAML 中对应已绑定主体名后也必须插入同一个 `@` 资产引用 / node mention，确保 YAML 主体和画布素材一一对应。
- `@` 引用必须是 LibTV/Agent-IM 可识别的画布资产引用或 node mention；不得伪造成普通文本解释、URL 注释、`〔主体参照: ...〕`、手写图片编号或 `{{Portrait N}}` 占位文本。
- `@` 引用只能绑定 `selected_reference_bindings_yaml` 中已有的 `canvas_node_name / node_key / URL` 对应素材；不得按上传顺序、图片编号或自然语言猜测生成。
- 构造 `source_node_keys`、`source_node_url_mapping` 和 `imageList/mixedList` 时，必须先以 `yaml_name + category` 查 `selected_reference_bindings_yaml`，再取该行的 `node_key/URL`；不得先生成数组再按数组下标回填主体。
- 构造数组前必须先生成 `canonical_reference_order`：`YAML.角色[] -> YAML.场景[] -> YAML.道具[]`，保留各列表内原顺序；`subject_bindings`、`selected_reference_bindings_yaml`、`source_node_keys`、`source_node_url_mapping`、`imageList/mixedList` 都按这个顺序的选中子集排列。
- 如果 `imageList` 顺序与主体出现顺序不同，仍以 `source_node_url_mapping` 和绑定表为准；不得把第 N 张图默认绑定给第 N 个主体。
- 当前 CLI `create_session.py` 只发送纯文本消息，不能单独证明 UI 级 `@` 引用已插入；必须通过 LibTV 查询结果、后端工具参数或画布节点引用回显验证，否则只能记录为 `at_asset_mention_unverified`。
- 插入 `@` 引用属于 transport-only 参照绑定，不得改变原文措辞、句序、镜头顺序、台词、动作结果或风格描述。
- 同一 YAML 主体默认只提交一张主体参照图；除非用户显式要求多视图或多版本对比，不得为同一主体在同一视频任务中重复提交两张同义主体图。
- 参照图超过 9 张时，预算裁决只影响 `imageList/mixedList` 和 evidence artifacts；被排除主体仍保留在底部 YAML 原文中，但不得在 prompt 中写入缺图原因或排除原因。
- 不得追加 `StyleBible`、`StyleBible_Summary` 或 `其中，...` 尾部复述。
- 不得出现 `本轮不提交任何参考图 URL`、`参考图审核失败`、`改为纯文生视频`、`角色与道具按原文生成` 等执行诊断或泛化主体替代句。
