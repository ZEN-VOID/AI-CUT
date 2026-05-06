# Video Prompt Assembly Contract

本文件定义 step1 之后的组级视频 prompt 组装规则。目标是把 `4-分组` 的现有组正文保真转换为 LibTV 可提交文本，而不是重新创作分镜。

## Prompt Shape

每个分镜组生成一个独立 prompt：

```text
横屏真人实拍感视频，保持平行当代校园规则怪谈质感，低饱和冷白灯光，黑白红警告层与金色真相层分离。请根据以下完整分镜组内容生成一条连续视频，保留镜头顺序、角色动作、对白、音效、分镜明细与氛围约束；默认忽略相邻组间连接件。

主体参照说明：
角色：林寂 @projects/aigc/诡校-测试版/5-设计/角色/3-生成/林寂-多视图.png，多视图角色参考；生成时保持身份、服装与体态一致。
场景：永夜私立中学二年级A班教室 @projects/aigc/诡校-测试版/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png，多视图场景参考；生成时保持空间布局和光线一致。

分镜组原文：
<直接粘贴 group_body>
```

本地审核用 prompt 可以保留 `@projects/...` 本地路径，便于 review gate 回查 reference manifest。发送给 LibTV 的 `*-libtv-submission.txt` 必须改写为远端可理解的提交形态，使用下列固定开头。

## Prompt Fidelity Modes

默认提交口径是 `strict_original + transport_only`：

| mode | default | allowed | forbidden |
| --- | --- | --- | --- |
| `strict_original` | yes | 将 `【主体参照说明】` 的主体名/参照图绑定关系与 `source-group-body.md` / `group_body` 原文共同作为 Seedance `create_generation_task.params.prompt` 完整体；其中 `【分镜组源文本】` 必须逐字保留 | 改写、摘要、重排、压缩、合并镜头、补镜头、把源文本改成优化版提示词、只保留裸图片 token |
| `transport_only` | yes | 替换本地路径为 uploaded URL，裁剪超过 provider 上限的参照图，补齐 `mixed2video / mixedList / duration / ratio / resolution / enableSound` 等技术参数 | 改动分镜内容、角色动作、对白、镜头顺序、音效、氛围事实 |
| `libtv_optimize` | no | 在用户显式 opt-in 后，允许 LibTV 重新组织提示词、压缩、合并镜头或做工作流规划 | 未显式 opt-in 时不得启用 |

字段约束：

- `prompt_fidelity_mode` 默认值为 `strict_original`。
- `allow_libtv_prompt_optimization` 默认值为 `false`。
- 只有用户明确选择 `libtv_optimize` 或明确声明 `allow_libtv_prompt_optimization: true` 时，远端才允许执行提示词优化或创作型编排。
- `strict_original` 下，`【分镜组源文本】` 必须逐字来自当前组源文本；`【主体参照说明】` 必须保留主体名、参照图编号与 uploaded URL 的绑定关系，并与源文本共同组成生成 prompt 完整体。技术投影只能发生在远端调用锁定、主体 URL 和 provider 参数区，不得把主体名绑定裁掉。
- 若远端返回内容显示其在 `create_generation_task` 前自行生成“优化版提示词 / 重新编排脚本 / 镜头计划 / 摘要版分镜”，且本地未 opt-in，必须判定为 `prompt_fidelity_violation`。

## LibTV Remote Opening

`*-libtv-submission.txt` 必须以此固定开头开始，且必须位于任何 `分镜组原文`、`分镜明细` 或长正文之前：

```text
【LibTV 调用锁定】
prompt_fidelity_mode: strict_original
allow_libtv_prompt_optimization: false
禁止提示词优化、禁止重新编排、禁止摘要、禁止改写、禁止补镜头。
禁止把【分镜组源文本】转换成优化版提示词、工作流说明或镜头计划。
必须将【主体参照说明】中相关主体名、参照图编号、主体参照 URL 绑定关系 + 【分镜组源文本】原文共同作为 Seedance create_generation_task.params.prompt 的完整主体。
禁止在生成 prompt 中只保留裸图片 token、裸图片编号或裸 URL；每个图片 token/图片编号必须邻近对应主体名称。
只允许执行 transport_only 投影：上传 URL、mixedList、duration、ratio、resolution、enableSound。
禁止调用 ask_user。
禁止向用户确认、展示“请稍候”、等待下一条消息。
用户已授权立即生成。
如果需要模型参数，直接使用下方固定参数，不要查询后停顿。
无法创建生成节点时，直接返回 ERROR_NO_GENERATION_NODE。
provider: seedance2.0
taskType: video
工具调用字段名必须使用 taskType，不得使用 task_type。
create_generation_task 的 params 必须作为顶层字段传入，内部包含 modeType、prompt、mixedList、duration、ratio、resolution、enableSound。
modeType: mixed2video
mixedList: [{"url": "<uploaded_url_1>", "type": "image"}, {"url": "<uploaded_url_2>", "type": "image"}, ...]
duration: 15
ratio: 16:9
resolution: 720p
enableSound: on

【视频默认规格】
硬性生成参数：这是 15 秒视频，不是 10 秒。生成前必须把画布/视频时长设置为 15 秒；不要使用默认 10 秒模板；不要缩短。声音/音频开启，保留物理互动音效、环境声、对白声音和旁白声音；不生成 BGM。横屏 16:9，720P。

【给龙虾的工作流管理要求】
把全部工作流和结果都放在画布上。不要把这句话转化为确认问题或等待消息；它是执行要求。

【已上传主体参照 URL】
<主体名>：参照图<序号> <uploaded_url>

【主体参照说明】
角色：<主体名>，参照图<序号>；生成时保持身份、外观、服装、材料、体态和表演连续性。
场景：<主体名>，参照图<序号>；生成时保持空间布局、光影、材料、湿度和镜头透视连续性。
道具：<主体名>，参照图<序号>；生成时保持形制、旧化、材质、尺寸和动作关系连续性。

【直接生成请求】
请基于【主体参照说明】（包含主体名、主体类别、参照图编号和主体参照 URL）和下方【分镜组源文本】，按 `mixed2video + mixedList` 生成一条连续视频。请直接把【主体参照说明】中与本组相关的主体名/参照图绑定关系 + 【分镜组源文本】原文作为生成 prompt 完整体。禁止重新组织、压缩、合并或摘要【分镜组源文本】；禁止把主体参照简化为裸图片 token、裸图片编号或裸 URL。

【分镜组源文本】
<直接粘贴 group_body>
```

远端提交口径要求：

- 默认必须声明 `prompt_fidelity_mode: strict_original` 和 `allow_libtv_prompt_optimization: false`；不得把 LibTV 的提示词优化当作默认增强项。
- 默认必须显式禁止提示词优化、重新编排、摘要、改写和补镜头；只有用户 opt-in `libtv_optimize` 时才可移除该禁止项，并需在 submit plan / report 中记录。
- `*-libtv-submission.txt` 不得包含 `@projects/...`、绝对本地路径或其他本地文件路径；远端只接收 `参照图<序号> <uploaded_url>`。
- `mixedList` 内必须直接填入上传返回的真实 URL，并使用严格 JSON 对象写法；不得写 `参照图N URL`、`<uploaded_url>` 或其他占位符后再期待远端二次解析。
- 远端最终 `create_generation_task.params.prompt` 必须同时包含主体名称和对应图片 token/编号，例如 `任盈盈 参照图1`、`令狐冲 参照图2`、`真鹤竹屋 参照图4`；不得生成只有 `{{Image 1}} {{Image 2}} ...`、`图片1 图片2 ...` 或裸 URL 列表开头的 prompt。
- 远端工具调用必须使用 `taskType` 字段名，不得改写成 `task_type`；`params` 必须作为 `create_generation_task` 顶层参数传入，不得把 provider 参数散落在自然语言或错误 envelope 中。
- 固定开头必须显式禁止 `ask_user`、确认、等待下一条消息和“请稍候”状态式回复；远端若不能创建生成节点，应返回 `ERROR_NO_GENERATION_NODE`，不得进入用户确认循环。
- `分镜组源文本` 是连续视频约束文本，不是图片生成任务列表；固定开头必须显式防止远端代理把它改路由为分镜图流程。
- 若某主体缺图，只能在 `主体参照说明` 中写“无独立参照图，按源文本作为群像/环境/随场景保留”，不得生成空 `参照图` 槽位。
- `【直接生成请求】` 必须出现在 `【分镜组源文本】` 前，避免远端先读到 `分镜明细` 后自动规划图片工作流。

## Provider Instruction Boundary

- 可以添加最小 provider 指令，例如横屏、连续视频、保持镜头顺序、参照图路径绑定。
- 不得重写 `group_body` 中的剧情事实、镜头顺序或角色动作。
- 不得把 YAML 主体清单写成剧情正文；只可写成主体参照说明，并在每个有图主体信息后追加 `@<图片路径>`。
- 本地审核 prompt 使用 `@<图片路径>`；LibTV 远端提交 prompt 必须使用上传后的 URL 编号和主体名，不得把本地路径发送给远端。
- 远端生成 prompt 完整体必须包含 `【主体参照说明】 + 【分镜组源文本】`；不得只把 `【分镜组源文本】` 投给 `params.prompt`，也不得只把主体参照作为 `mixedList` 的匿名图片数组。
- LibTV 远端提交 prompt 必须明确锁定 `modeType=mixed2video` 和 `mixedList`；不得只用自然语言描述“全能参照”。
- 不得承诺 LibTV 不支持的参数或能力；模型、时长、分辨率以 `.agents/skills/cli/libTV` 当前约束为准。

## Reference Path Suffix Rule

- 当使用 `libtv_session_with_uploaded_references` 时，prompt 必须在对应主体信息后追加 `@<图片路径>`，例如 `角色：林寂 @projects/.../林寂-多视图.png`。
- 每个路径后缀必须说明主体名称、类别、图片变体，例如 `多视图角色参考`、`主图道具参考`。
- 缺图主体不得添加 `@` 后缀，也不得写 `@空`、`@null` 或空路径。
- `@<图片路径>` 的顺序必须与 submit plan 的 `images[]` 顺序一致；prompt 内不使用抽象占位符替代图片路径。
- 对 `*-libtv-submission.txt`，路径后缀规则投影为 `mixedList` 真实 URL 项和 `主体名：参照图<upload_index> <uploaded_url>` 列表；`upload_index` 必须与 submit plan 的 `images[]` 顺序一致。
- 对远端 `create_generation_task.params.prompt`，图片 token / 图片编号必须与主体名同段绑定，例如 `任盈盈：参照图1`、`{{Image 1}} 任盈盈` 或 `任盈盈 {{Image 1}}`。只有 `{{Image 1}} {{Image 2}}` 或 `图片1 图片2` 的裸 token 序列视为主体名绑定丢失。

## Length Handling

- 默认保留完整 `group_body`。
- 若 LibTV prompt 长度或人工策略要求压缩，必须先获得用户对 `libtv_optimize` 或等价压缩策略的显式 opt-in，并在 submit plan 中记录：
  - `source_group_body_preserved: true`
  - `prompt_compression: none / reviewed_summary`
  - `source_group_body_path`
  - `compression_reason`
- 压缩只能保留事实，不得添加新剧情。

## Gate

通过 prompt gate 必须满足：

1. prompt 能回指 `source_file` 与 `group_id`。
2. `group_body` 是主要内容，且没有被剧情改写。
3. 若存在参考图，对应主体信息后有 `@<图片路径>`，且顺序与 `images[]` 一致。
4. 若没有参考图，prompt 不包含空 `@` 后缀。
5. `*-libtv-submission.txt` 以 `【LibTV 调用锁定】` 开头；有主体参照图时包含 `modeType: mixed2video` 和 `mixedList`，无图时包含 `modeType: text2video`。
6. `*-libtv-submission.txt` 不包含本地图片路径，只包含已上传 URL 和参照图编号。
7. `*-libtv-submission.txt` 在 provider 参数前包含 no-ask 约束：禁止 `ask_user`、禁止确认、禁止等待下一条消息、用户已授权立即生成。
8. 默认提交包含 `prompt_fidelity_mode: strict_original`、`allow_libtv_prompt_optimization: false` 和禁止优化/重排/摘要/改写/补镜头约束。
9. 若 submit plan 未记录用户 opt-in，远端 query 中不得出现 LibTV 自行生成的优化版提示词、重新编排脚本、镜头计划或摘要版分镜。
10. 远端 `create_generation_task` 工具调用不得出现 `task_type`；若 tool 返回 `params is required`，状态必须记录为 `generation_tool_error`，不得标记为正常 pending。
11. 远端 `create_generation_task.params.prompt` 必须包含主体名与图片 token/编号绑定；若只出现裸 `{{Image N}}`、裸 `图片N` 或裸 URL 序列，状态必须记录为 `subject_reference_name_stripped`。
