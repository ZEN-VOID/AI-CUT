# Context: wjs-uploading-video

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2811
current_lines: 66
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-uploading-video` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

- `oauth_bootstrap_blocked`
  - 症状：找不到 credentials/token，或 Google consent 返回 `access_denied 403`。
  - 根因层：机器级 OAuth 前置条件缺失，不是视频文件问题。
  - 立即修复：按凭据文档补 `~/.config/youtube/credentials.json`，把账号加入 OAuth Test users，重新生成 token。
  - 系统预防：上传前先检查 credentials、token、账号授权状态和依赖。
  - 验证点：后续运行能静默复用 `token.json`，无需重复浏览器授权。
- `proxy_resumable_upload_failure`
  - 症状：stock API client 卡住、`No route to host`、`socket.timeout`、长时间没有进度行。
  - 根因层：本地代理与 `google-api-python-client`/`httplib2` 的 resumable PUT 不兼容。
  - 立即修复：使用本技能脚本的 `requests` resumable uploader，检查 upload endpoint 代理连通性，必要时降低 `--chunk-mb`。
  - 系统预防：不要替换回 stock `MediaFileUpload`；代理环境下以 8 MB chunk + retry 为默认。
  - 验证点：上传过程中持续出现 chunk progress，失败可按 results file 续跑。
- `metadata_pairing_failure`
  - 症状：目录中 MP4 没有对应 meta block，或标题/描述/标签错绑到别的视频。
  - 根因层：`UPLOAD_META.md` heading 文件名与 `final/` 实际文件不一致。
  - 立即修复：先跑 `--dry-run`，修正 `## NN · filename.mp4`，必要时显式使用 `--allow-missing-meta`。
  - 系统预防：把 meta 文件视为批量上传的内容真源，不从文件名猜完整发布文案。
  - 验证点：dry-run 列出的 file、title、description、tags 与用户预期一致。
- `youtube_limit_misdiagnosis`
  - 症状：`quotaExceeded` 或 `429 rateLimitExceeded Video Uploads per day` 被误判成代理或认证问题。
  - 根因层：YouTube API quota 与每日视频上传数是两套限制。
  - 立即修复：`quotaExceeded` 走配额策略；`429 Video Uploads per day` 等太平洋时间午夜重置或改用 Studio 网页上传。
  - 系统预防：错误分类先看 API 响应码和 message，不先调代理。
  - 验证点：重跑前确认结果文件保留已成功项，避免重复上传。
- `privacy_expectation_mismatch`
  - 症状：用户以为可先审核，实际默认 public 已公开。
  - 根因层：技能默认值与发布意图未确认。
  - 立即修复：需要缓冲时用 `--privacy unlisted/private`；定时发布必须配合 private 和 `--publish-at`。
  - 系统预防：批量上传前明确 privacy、playlist、schedule 和 made-for-kids。
  - 验证点：结果表中列出 URL、privacy 和是否加入 playlist。

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认任务是上传到 YouTube，而不是微信视频号、抖音、小红书、B 站或 Shorts 重构。
2. 上传前检查 OAuth credentials/token、Python 依赖、代理连通性和用户选择的 privacy/playlist/schedule。
3. 批量目录优先读取 `UPLOAD_META.md` 并 dry-run；文件名、标题、描述、tags 全部确认后再触网。
4. 运行上传脚本时保留默认 results file，失败后重跑依赖它跳过已成功项。
5. 出错先按类型分流：OAuth、代理、quota、daily upload count、metadata、playlist。
6. 完成后用 markdown 表回传每个视频的文件、标题、URL 和剩余注意事项。

## Reusable Heuristics

- 默认 `public` 是立即发布；除非用户明确要直接上线，批量上传前应再次确认是否需要 `unlisted`。
- `UPLOAD_META.md` 的描述和 hashtag 是发布文案真源；不要把短标题自动扩写成另一个标题。
- 频道 CTA 和描述 footer 使用“王建硕”；嘉宾姓名只放在内容描述里。
- results file 是幂等上传的本地真源；删除它等于允许重复上传。
- `429 Video Uploads per day` 与 API quota 不同，不能靠换 chunk、重登 token 或重启代理解决。
- 若用户给的是横屏源但要求 Shorts，应先路由到 `wjs-reframing-video` 产出 9:16，再上传。

## Promotion Backlog

- 增加 upload preflight：检查 OAuth、proxy endpoint、metadata pairing、privacy 和 quota 风险。
- 增加 dry-run 报告模板，把 title、description 摘要、tags、privacy、playlist 一次列清。
- 在脚本错误输出中显式区分 API quota 与每日视频上传数限制。
- 增加 playlist 辅助流程：已有 playlist ID 时批量加入，缺失时提示用户提供或创建。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
