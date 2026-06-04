# Video Evidence Contract

## Real Video Understanding Gate

真实视频内容分析是 `$aigc-video-review` 的必须条件，不是可选增强。

- 在给出 verdict、finding、prompt 匹配、创作质量判断或上游修复前，必须先观察真实视频内容。
- 观察必须落成 `observed_content_summary`，说明实际出现的主体、场景空间、动作变化、镜头节奏、关键道具、音频事实和明显 AIGC 缺陷。
- `observed_content_summary` 必须能回指关键帧、联系表、场景切点或音频统计 / 听辨记录。
- 禁止只凭文件名、prompt、分镜组文本、manifest、queue、LibTV node query、远端 result URL、画布缩略图、用户预期或模型常识推断视频内容。
- 若目标来自 LibTV，必须先按 `references/libtv-intake-contract.md` 下载到本地可读视频，再执行本合同的真实视频理解门；远端 URL 或节点 JSON 只作为生成路线证据，不等于视频审片证据。
- 若视频证据无法支持真实内容分析，必须标记 `FAIL-REVIEW-EVIDENCE`，只能补采证据、阻断或要求澄清，不得写通过 / 不通过结论。

## Evidence Pack

每次审片至少收集：

- `video_path`
- `source_origin`：`local_file` 或 `libtv_download`
- `libtv_remote_query`：仅 LibTV 入口需要，指向保存的 node query
- `duration`
- `resolution`
- `fps`
- `has_audio`
- `audio_note`
- `keyframe_samples`
- `contact_sheet`
- `scene_cut_note`
- `observed_content_summary`

## Tool Boundary

脚本和工具只承担机械证据：

- `ffprobe` 获取元数据。
- `ffmpeg` 抽关键帧、联系表、音频统计和场景切点。
- `libtv` CLI 查询和下载 LibTV 远端视频节点。
- 图片查看工具用于观察实际画面。

核心判断必须由 LLM 完成：

- 实际视频内容里发生了什么。
- 画面是否匹配分镜组意图。
- 哪些偏差是生成瑕疵，哪些偏差来自上游文档。
- 是否写回 `10-分组` 或上升源层。

## Minimum Keyframes

单条 15 秒左右视频建议抽取：

- 起始帧：`0s`
- 1/4：约 `3s`
- 中点：约 `7s`
- 3/4：约 `11s`
- 结尾前：约 `14s`

若视频明显多切点，额外抽 scene change 附近帧。

## Audio Notes

音频审查只做事实记录和明显异常判断：

- 是否静音或接近静音。
- 是否含明显 BGM。
- 是否含对白、旁白、环境声或物理互动声。
- 是否与 `10-分组` 中“不生成BGM，仅生成物理互动音效与环境和氛围音效”冲突。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否在 verdict、finding、prompt 匹配、创作质量或上游修复前，先基于真实视频内容形成判断？ | `GATE-REVIEW-03` | `FAIL-REVIEW-EVIDENCE` | `SKILL.md#Thinking-Action Node Map (N3-EVIDENCE)` | `observed_content_summary`，并回指元数据、关键帧 / 联系表、场景切点或音频记录。 |
| `observed_content_summary` 是否覆盖主体、空间、动作变化、镜头节奏、关键道具、音频事实和明显 AIGC 缺陷？ | `GATE-REVIEW-03` | `FAIL-REVIEW-EVIDENCE` | `SKILL.md#Thinking-Action Node Map (N3-EVIDENCE)` | 审片报告中的 `observed_content_summary` 字段，逐项说明缺失项已补齐或不可用原因。 |
| 是否避免只凭文件名、prompt、分镜组文本、manifest、queue、用户预期或模型常识推断视频内容？ | `GATE-REVIEW-03` | `FAIL-REVIEW-EVIDENCE` | `references/video-evidence-contract.md#Real Video Understanding Gate` + `SKILL.md#Thinking-Action Node Map (N3-EVIDENCE)` | 报告中列明真实视频证据来源；若证据不足，verdict 必须为阻断 / 澄清 / 补采，不得写通过或不通过结论。 |
| LibTV 入口是否已先下载为本地可读视频，并把远端 node query 仅作为生成路线证据，而不是替代真实视频观察？ | `GATE-REVIEW-00` / `GATE-REVIEW-03` | `FAIL-REVIEW-LIBTV-INTAKE` / `FAIL-REVIEW-EVIDENCE` | `references/libtv-intake-contract.md` + `SKILL.md#Thinking-Action Node Map (N0-LIBTV-INTAKE)` | `libtv_input`、`remote_query_path`、`canonical_video_path`、ffprobe 元数据和关键帧 / 联系表。 |
| evidence pack 是否至少包含 `video_path`、`duration`、`resolution`、`fps`、`has_audio`、`audio_note`、`keyframe_samples`、`contact_sheet`、`scene_cut_note` 和 `observed_content_summary`？ | `GATE-REVIEW-03` | `FAIL-REVIEW-EVIDENCE` | `references/video-evidence-contract.md#Evidence Pack` + `SKILL.md#Thinking-Action Node Map (N3-EVIDENCE)` | 审片报告或证据包清单逐项列出字段；缺失字段必须说明原因和补采计划。 |
| 是否把脚本限制在 `ffprobe`、`ffmpeg`、抽帧、统计和查看等机械证据工作，而没有让脚本替代 LLM 的内容理解、匹配归因或落点判断？ | `GATE-REVIEW-03` | `FAIL-REVIEW-EVIDENCE` | `references/video-evidence-contract.md#Tool Boundary` + `SKILL.md#Thinking-Action Node Map (N4-METHOD-COMPARE)` | 报告区分机械证据与 LLM 判断：脚本输出只作为元数据 / 帧证据，核心 verdict 和 finding 有文字化分析依据。 |
| 15 秒左右视频是否至少覆盖起始、1/4、中点、3/4、结尾前关键帧，并在多切点时补 scene change 附近帧？ | `GATE-REVIEW-03` | `FAIL-REVIEW-EVIDENCE` | `references/video-evidence-contract.md#Minimum Keyframes` + `SKILL.md#Thinking-Action Node Map (N3-EVIDENCE)` | `keyframe_samples` 或 `contact_sheet` 记录时间点；多切点素材附 `scene_cut_note` 或说明未检测到明显切点。 |
| 有音轨时是否记录静音 / BGM / 对白旁白 / 环境声 / 物理互动声，并检查是否冲突于 `10-分组` 的音频约束？ | `GATE-REVIEW-03` | `FAIL-REVIEW-EVIDENCE` | `references/video-evidence-contract.md#Audio Notes` + `SKILL.md#Thinking-Action Node Map (N4-METHOD-COMPARE)` | `audio_note` 写明音频类型、明显异常和与分组音频约束的关系；无音轨时明确 `has_audio: false`。 |
