# Video Evidence Contract

## Real Video Understanding Gate

真实视频内容分析是 `$aigc-video-review` 的必须条件，不是可选增强。

- 在给出 verdict、finding、prompt 匹配、创作质量判断或上游修复前，必须先观察真实视频内容。
- 观察必须落成 `observed_content_summary`，说明实际出现的主体、场景空间、动作变化、镜头节奏、关键道具、音频事实和明显 AIGC 缺陷。
- `observed_content_summary` 必须能回指关键帧、联系表、场景切点或音频统计 / 听辨记录。
- 禁止只凭文件名、prompt、分镜组文本、manifest、queue、用户预期或模型常识推断视频内容。
- 若视频证据无法支持真实内容分析，必须标记 `FAIL-REVIEW-EVIDENCE`，只能补采证据、阻断或要求澄清，不得写通过 / 不通过结论。

## Evidence Pack

每次审片至少收集：

- `video_path`
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
- 图片查看工具用于观察实际画面。

核心判断必须由 LLM 完成：

- 实际视频内容里发生了什么。
- 画面是否匹配分镜组意图。
- 哪些偏差是生成瑕疵，哪些偏差来自上游文档。
- 是否写回 `4-分组` 或上升源层。

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
- 是否与 `4-分组` 中“不生成BGM，仅生成物理互动音效与环境和氛围音效”冲突。
