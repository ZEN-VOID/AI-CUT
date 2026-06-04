# LibTV Intake Contract

本合同定义 `9-审片` 如何从 LibTV 画布入口取得真实视频素材。凡用户输入包含 LibTV 链接、画布项目 UUID、画布名称或视频节点名时，审片必须先通过 `.agents/skills/cli/libTV` 官方 CLI 查询和下载真实视频，再进入 `N3-EVIDENCE`。

## Accepted LibTV Targets

| input shape | required fields | resolution route |
| --- | --- | --- |
| `libTV链接 + 视频名` | `https://www.liblib.tv/canvas?projectId=<uuid>`；视频名可省略，省略时用 `group_id` | 从 URL query 参数提取 `projectId`，用 `libtv node <video_name> -p <projectId>` 查询，再用 `libtv download -p <projectId> -n <video_name>` 下载。 |
| `projectUuid + 视频名` | LibTV project UUID；视频名可省略，省略时用 `group_id` | 直接使用显式 `-p <projectUuid>` 查询节点和下载。 |
| `libTV画布名 + 视频名` | 画布名称或名称片段；视频名可省略，省略时用 `group_id` | 用 `libtv project list --name "<canvas_name>"` 查询，必须唯一命中后再查询节点。多命中时阻断并要求最小澄清。 |
| `.libtv/project.json + 视频名` | 当前目录已绑定 projectUuid；视频名可省略，省略时用 `group_id` | 可读取目录默认项目，但报告必须记录实际 `projectUuid`。 |

`视频名` 默认等于分镜组 ID，例如 `1-1-1`。如果用户只给了画布入口而没有给 `group_id` 或视频名，不能凭画面猜测，必须要求最小澄清。

## Required CLI Sequence

所有 LibTV 操作必须通过 `.agents/skills/cli/libTV` 的 `libtv` CLI 完成，不得手写 HTTP 请求、绕网页端或读取凭据文件。

1. `libtv account info`
   - 仅验证账号摘要，不输出 token、cookie 或 credentials 内容。
2. Resolve project:
   - URL / UUID 输入：记录 `projectUuid`。
   - 画布名输入：运行 `libtv project list --name "<canvas_name>"`，唯一命中后记录 `projectUuid` 与项目名。
3. Resolve node:
   - 运行 `libtv node <video_name> -p <projectUuid>`。
   - `<video_name>` 解析必须精确；多节点同名或节点不存在时阻断。
   - 节点类型必须是 `video`，或报告中明确为什么按非视频素材处理。
4. Persist remote evidence:
   - 将节点查询 stdout 保存到 `projects/aigc/<项目名>/9-审片/第N集/evidence/<group_id>/<group_id>-libtv-node-query.ndjson`。
   - 记录 `nodeKey`、`data.url[]`、`taskInfo`、`params.prompt`、`params.imageList/mixedList`、`settings`、`model`、`modeType`。
5. Download real media:
   - 运行 `libtv download -p <projectUuid> -n <video_name> -o projects/aigc/<项目名>/8-视频`。
   - 下载后的 canonical 视频文件应为 `projects/aigc/<项目名>/8-视频/<group_id>[-variant].mp4`。
   - 如果 CLI 输出文件名不规范，允许整理为 canonical 文件名，但必须在审片报告中记录原始下载路径和命名整理动作。
6. Only after download:
   - 对本地视频执行 `ffprobe`、`ffmpeg` 抽帧、联系表、音频统计和 scene cut 检测。
   - 不得只看 LibTV 节点 JSON、远端 URL、prompt 或画布缩略图给出审片结论。

## Evidence Fields

LibTV 入口审片报告必须增加：

```yaml
libtv_input:
  input_shape: "canvas_url | project_uuid | canvas_name | bound_project"
  canvas_url: ""
  canvas_name: ""
  projectUuid: ""
  video_node_name: ""
  video_node_key: ""
  remote_result_url: ""
  remote_task_id: ""
  remote_query_path: ""
  download_output_path: ""
  canonical_video_path: ""
  prompt_source: "libtv_node_params | local_8_video_prompt | user_prompt | missing"
```

## Failure Handling

| failure | handling |
| --- | --- |
| CLI 未安装或不可执行 | 按 `.agents/skills/cli/libTV/scripts/install.md` 安装或报告 `FAIL-REVIEW-LIBTV-INTAKE`。 |
| 未登录或账号空间不对 | 只用 `libtv account info/list/use` 处理账号摘要；不读取凭据文件。 |
| 画布名多命中 | 阻断，列出候选摘要，要求用户指定 URL 或 project UUID。 |
| 节点名不唯一或不存在 | 阻断，要求视频节点名或 node key；不得凭画面猜。 |
| 节点未生成视频 URL | 报告 `remote_video_not_ready`，可提示先生成或 rerun；不得虚构下载结果。 |
| 下载失败 | 保存节点查询证据，报告失败命令与 stderr 摘要；不得进入最终审片 verdict。 |
| 下载成功但本地视频不可读 | 报告 `FAIL-REVIEW-EVIDENCE`，回到下载或素材修复。 |

## Prompt And Rerun Coupling

审片发现 prompt 错配或远端 prompt 污染时：

- 必须先保存修复前节点查询证据。
- 修复 prompt 后，用 `libtv node <video_name> -p <projectUuid> --prompt <clean_prompt> ...` 覆盖远端节点。
- 运行前必须查询确认 prompt hygiene：无 `{{Portrait N}}`、无诊断文本、无路径、无绑定表污染；保留合法 `{{Image N}}`。
- 用户本轮明确要求重新提交或 rerun 时，才运行 `libtv node <video_name> -p <projectUuid> --run`。
- rerun 输出和最终查询必须写回 `8-视频/libTV画布流/第N集/<group_id>-queue-record.json` 或审片报告中的等价证据。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| LibTV 链接、project UUID、画布名或目录绑定是否被解析成唯一 `projectUuid`？ | `GATE-REVIEW-00` | `FAIL-REVIEW-LIBTV-INTAKE` | `steps/video-review-workflow.md#N0 LibTV Intake` | `libtv_input.projectUuid`、`canvas_url/canvas_name`、project list 或 URL 解析证据。 |
| 视频名是否解析成唯一视频节点，且默认视频名只在 `group_id` 明确时使用？ | `GATE-REVIEW-00` | `FAIL-REVIEW-LIBTV-INTAKE` | `steps/video-review-workflow.md#N0 LibTV Intake` | `video_node_name`、`video_node_key`、节点查询文件；多命中或缺失时的阻断说明。 |
| 是否通过官方 `libtv node` 与 `libtv download` 取得真实视频，而不是只看远端 URL、prompt 或画布缩略图？ | `GATE-REVIEW-00` / `GATE-REVIEW-03` | `FAIL-REVIEW-LIBTV-INTAKE` / `FAIL-REVIEW-EVIDENCE` | `references/libtv-intake-contract.md#Required CLI Sequence` + `references/video-evidence-contract.md` | `remote_query_path`、`download_output_path`、`canonical_video_path`、ffprobe/关键帧证据。 |
| LibTV prompt、imageList、taskInfo、result URL 是否作为生成路线证据保存，并与本地 `8-视频` prompt/queue 对齐？ | `GATE-REVIEW-14` | `FAIL-REVIEW-LIBTV-EVIDENCE` | `steps/video-review-workflow.md#N2 Source Lock` + `references/libtv-intake-contract.md#Evidence Fields` | 审片报告的 `libtv_input`、节点查询 NDJSON、queue record 或 submit plan 路径。 |
| 发现远端 prompt 污染并重新提交时，是否先修 prompt hygiene、再查询验证、再在用户授权下 `--run`？ | `GATE-REVIEW-15` | `FAIL-REVIEW-LIBTV-RERUN` | `references/libtv-intake-contract.md#Prompt And Rerun Coupling` + `steps/video-review-workflow.md#N5 Landing And Operation Design` | 修复前/后节点查询、clean prompt、rerun task id、最终 query、queue record。 |
