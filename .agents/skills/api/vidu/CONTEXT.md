# Context: vidu-video-api

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
current_chars: auto
current_lines: auto
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-20T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `vidu-video-api` 技能的经验层，聚焦 Vidu 多模式视频创建、任务查询、24 小时下载链接、媒体 data URL 归一、项目化输出路径与回调签名验签。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-VDU-AUTH-HEADER` | 调用返回 401/403 | 认证层 | 确认请求头使用 `Authorization: Token <key>` | 在脚本中固定 `Token` 头格式，不让调用方自行拼接 | dry-run 摘要与真实请求头一致 |
| `TM-VDU-BASE-URL` | 路径命中错误环境或返回 404 | 环境配置层 | 检查 `.env` 中的 `VIDU_API_BASE_URL`，默认回退 `https://api.vidu.cn` | 把 base URL 解析集中到单一 helper | 报告中的 `base_url` 正确 |
| `TM-VDU-LOCAL-MEDIA` | 本地文件直接传给接口导致请求失败 | 媒体归一层 | 把本地图片/视频转成 data URL 后再提交 | 对已知媒体字段统一做“本地路径 -> data URL” 归一 | 报告中的媒体字段以 `data:` 或 `http` 开头 |
| `TM-VDU-SUBJECTS-DRIFT` | `reference2video` 的 `subjects` 结构复杂，CLI 参数不够表达 | 输入建模层 | 改用 `--input-json` 作为请求体真源 | 明确“复杂模式优先 JSON 文件，不继续膨胀 CLI 开关” | `subjects` 来自 JSON 文件且成功提交 |
| `TM-VDU-MULTIFRAME-MODE` | 智能多帧关键帧结构错误 | 模式合同层 | 用 `image_settings` JSON 明确每个关键帧 | 把多帧模式沉到 references 与 JSON 直传，不在终端里临时拼接 | `multiframe` 请求体含 `start_image + image_settings[]` |
| `TM-VDU-TASK-STATE` | 创建成功后被误判为最终成功 | 任务状态层 | 继续调用 `GET /tasks/{id}/creations` 查看 `state` | 固化“创建只拿 task_id，终态以查询接口为准” | 报告中存在查询结果与 `state` |
| `TM-VDU-CREATION-URL-EXPIRE` | 过期下载链接无法再取回生成物 | 生成物下载层 | 尽快查询并落盘生成物，必要时重新查询获取新 URL | 在技能中写明链接仅 24 小时有效，默认下载优先执行 | 本地已生成 MP4 |
| `TM-VDU-WATERMARK-CHOICE` | 错拿带水印或不带水印链接 | 下载策略层 | 明确 `url` 与 `watermarked_url` 的选择 | 把下载策略固定到 `--download-watermarked` 开关 | 下载报告里 `selected_url_kind` 正确 |
| `TM-VDU-OFFPEAK-CANCEL` | 错峰任务无人跟进或无法止损 | 编排层 | 用 `cancel` 子命令显式取消任务 | 把错峰任务的取消能力纳入主技能而不是手工记忆 | `cancel-<task_id>.json` 可复盘 |
| `TM-VDU-IMG2VIDEO-RESOLUTION` | `img2video + viduq3-pro-fast` 在创建时返回 `400 FieldInvalid: resolution` | 模式兼容层 | 对该模型先省略 `resolution`，让服务端回退默认值 | 把该差异沉淀到经验层，避免继续把“通用 resolution 参数”硬塞给所有图生模型 | 去掉 `resolution` 后任务能成功受理，并由服务端回填默认 `720p` |
| `TM-VDU-TEMPLATE-STORY-MIN-IMAGES` | `template-story` 的 `one_shot` 单图调用返回 `400`，要求至少 3 图 | 模板约束层 | 改为传入 3-10 张图 | 在参考模块显式写出 `one_shot` 的实测最小图片数 | 补足 3 图后任务成功 |
| `TM-VDU-MULTIFRAME-UPLOAD-SIZE` | `multiframe` 在发送阶段触发 `urllib/ssl` 异常 | 传输层 | 优先改用更小的 JPG 输入，压低 JSON body 体积 | 在经验层固定“多帧优先用小图/轻图”策略，并保留网络异常为可读错误 | 换小图后任务成功受理并完成 |
| `TM-VDU-REPORT-DATAURL-BLOAT` | 报告 JSON 被完整 base64 `data:` URL 撑爆，不利于复盘 | 报告治理层 | 在 `sanitize()` 中把 `data:` 缩写为长度摘要 | 固化“报告保留类型和大小，不保留整段 base64” | 新报告中 `request_body` 不再包含完整 data URL |
| `TM-VDU-CALLBACK-ORDER` | 回调验签总是失败 | 签名层 | 严格按 `X-HMAC-SIGNED-HEADERS` 顺序拼接 header 行，且签名字符串尾部保留换行 | 把签名生成逻辑沉到统一 helper，并在文档中固定顺序敏感性 | 计算签名与期望签名一致 |
| `TM-VDU-CALLBACK-SECRET` | 把 access key 当 secret key 使用，导致验签失败 | 签名密钥层 | 使用创建任务时的 token 作为 `secret_key` | 在参考模块中明确“`vidu` 是 access key，token 是 HMAC secret” | 验签成功或生成签名与官方示例一致 |
| `TM-VDU-REPORT-LEAK` | 报告里泄露 API Key 或下载签名 query | 安全日志层 | 对 token 与 URL query 做统一脱敏 | 把报告写入和异常输出都走同一套 sanitize 流程 | 报告中不存在原始 token 和 query 字符串 |
| `TM-VDU-OUTPUT-PATH` | 产物落到散乱目录，和项目 runtime 脱节 | 输出路由层 | 统一走 `output_dir > project_name/task_kind -> 默认项目化路径` | 把输出路径解析收口到单一 helper | 报告和 MP4 位于 `output/影片/[项目名]/5-API/video/vidu/` |

## Repair Playbook

1. 先跑 dry-run 看请求摘要：

```bash
python3 .agents/skills/api/vidu/scripts/vidu_video.py create \
  --mode text2video \
  --model viduq3-turbo \
  --prompt "test" \
  --dry-run --print-request
```

2. 检查 `.env`：
   - `VIDU_API_KEY`
   - `VIDU_API_BASE_URL`
3. 如果是复杂模式：
   - 优先检查 `--input-json`
   - 再看本地图片/视频路径是否能转成 data URL
4. 如果创建后迟迟没结果：
   - 用 `task` 子命令查询 `state`
   - 再决定是否 `--wait`
5. 如果下载失败：
   - 先确认 `state=success`
   - 再确认 `creations[*].url` 或 `watermarked_url` 是否存在
   - 再确认链接是否已过期
6. 如果回调验签失败：
   - 确认 `Date`
   - 确认 `X-HMAC-SIGNED-HEADERS` 的顺序
   - 确认签名字符串末尾仍有换行
   - 确认使用的 secret 是 token，而不是 `"vidu"`

## Reusable Heuristics

- 对 Vidu 来说，创建接口解决的是“受理”，查询接口解决的是“完成与生成物”；这两层不要混成一个成功概念。
- 官方允许图片和视频传 URL 或 Base64，repo-local 最稳的做法是把本地文件在脚本层自动转成 data URL，而不是要求用户手工编码。
- `reference2video` 与 `multiframe` 的结构天然复杂，最稳定的输入方式是 JSON 真源，不要把它们退化成零碎终端参数拼装。
- `img2video` 不能假设所有模型都接受统一的 `resolution` 参数；这次实测里 `viduq3-pro-fast` 传 `resolution=540p` 会被直接拒绝，省略后服务端自动回填 `720p`。
- `template-story` 的 `one_shot` 在当前实测里不是单图模板，至少要 3 张图。
- `multiframe` 比普通图生更容易在上传阶段碰到连接层问题，优先选更小的 JPG 输入，而不是高分辨率 PNG。
- 生成物链接只有 24 小时有效，适合“查到即下”，不适合只把 URL 记在聊天里。
- 回调签名最容易错的不是 HMAC 算法本身，而是 header 顺序、尾部换行和把 token/vidu 搞反。
- 模板类接口的参数面可能扩展得比文生/图生快；当文档新增字段时，优先让 JSON passthrough 吸收变化，再考虑是否升格为 CLI sugar。
