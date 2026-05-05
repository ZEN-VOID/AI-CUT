# Editing Type Package

Use when the user provides one or more local images/videos and wants LibTV to edit, animate, extend, restyle, replace, remove, or use them as references.

## Fixed Context

- Verify every local file exists before upload.
- Upload only image/video files.
- Upload references before session submission through the same LibTV access/project context that will receive the prompt.
- Treat returned OSS URLs as the only submitted reference payload; local filesystem paths are upload inputs only and must not appear in the prompt.
- Treat uploaded OSS URLs as numbered references appended outside the preserved `【创作请求原文】` block.
- The user's wording remains the creative source of truth.
- Add a separate start-of-task notice to 龙虾: `把全部工作流和结果都放在画布上。`
- For video requests, add a separate hard default video spec before the preserved request unless the user explicitly overrides it: 15-second video, not 10 seconds, set canvas/video duration to 15 seconds before generation, sound/audio enabled, 16:9, 720P.
- Do not automatically poll or download after session creation. The project canvas is the default progress/result surface; query/download only when the user explicitly asks.

## Handoff Shape

```text
【视频默认规格】
硬性生成参数：这是 15 秒视频，不是 10 秒。生成前必须把画布/视频时长设置为 15 秒；不要使用默认 10 秒模板；不要缩短。声音/音频开启，保留物理互动音效、环境声或用户请求中的声音元素。横屏 16:9，720P。

【创作请求原文】
<original user instruction>

【参照资源】
参照图1：<oss_url_1>
参照图2：<oss_url_2>

【给龙虾的工作流管理要求】
把全部工作流和结果都放在画布上。
```

Use a more specific Chinese label such as `参考图` or `参考视频` when the file type is obvious.
If any reference upload does not return an OSS URL, stop before `create_session.py`; do not replace the missing URL with a local path or filename.
