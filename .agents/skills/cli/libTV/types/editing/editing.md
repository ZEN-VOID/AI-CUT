# Editing Type Package

Use when the user provides one or more local images/videos and wants LibTV to edit, animate, extend, restyle, replace, remove, or use them as references.

## Fixed Context

- Verify every local file exists before upload.
- Upload only image/video files.
- Treat uploaded OSS URLs as numbered references appended to the user's instruction.
- The user's wording remains the creative source of truth.

## Handoff Shape

```text
<original user instruction>
参照图1：<oss_url_1>
参照图2：<oss_url_2>
```

Use a more specific Chinese label such as `参考图` or `参考视频` when the file type is obvious.
