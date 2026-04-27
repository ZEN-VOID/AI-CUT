---
name: man-tui-grok-video
governance_tier: full
description: |
  调用漫涂（Man-Tui）Grok 异步视频生成接口，提交 `grok-imagine-video` 任务、轮询任务状态，并获取最终 MP4 内容。适用于用户提到 `man-tui`、`漫涂`、`grok 视频`、`grok-imagine-video`、异步视频生成、参考图驱动视频等场景。
tools: [Read, Write, Edit, Bash]
color: teal
version: "v1.0"
---

# 漫涂 Grok 异步视频技能

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

- 本技能用于通过漫涂 Grok 异步视频接口执行以下动作：
  - `POST /v1/videos`：提交视频生成任务
  - `GET /v1/videos/{task_id}`：查询任务状态
  - `GET /v1/videos/{task_id}/content`：获取生成后的视频内容
- 默认模型：`grok-imagine-video`
- 默认 API 根地址：优先读取根目录 `.env` 的 `MAN_TUI_GROK_API_BASE_URL`，再回退 `MAN_TUI_GROK_CONNECTION_JSON.url`、`MAN_TUI_API_BASE_URL`，最终回退 `https://api.man-tui.com`
- 默认认证：优先读取根目录 `.env` 的 `MAN_TUI_GROK_API_KEY`，再回退 `MAN_TUI_GROK_CONNECTION_JSON.key`、`MAN_TUI_API_KEY`
- 统一脚本入口：

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py [subcommand] [参数]
```

## 2. 必需输入

### 2.1 创建任务

- `prompt`
- API Key（优先读取 `.env` 中的 `MAN_TUI_GROK_API_KEY`，再回退 `MAN_TUI_GROK_CONNECTION_JSON.key`、`MAN_TUI_API_KEY`，也可显式传 `--api-key`）

可选输入：
- `model`，默认 `grok-imagine-video`
- `seconds`，允许值：`6 / 10 / 12 / 16 / 20`
- `size`，允许值：`1280x720 / 720x1280 / 1792x1024 / 1024x1792 / 1024x1024`
- `quality`，允许值：`standard / high`
- `input_reference`：单张本地参考图
- `image_reference`：远程参考图 URL 数组字符串，或通过重复 `--image-reference-url` 构造
- `project_name`
- `task_kind`：`project / test / temp`
- `output_dir`
- `report_json`
- `wait / poll_interval / wait_timeout`
- `download_on_complete`

### 2.2 查询状态 / 获取视频

- `task_id`
- API Key

## 3. 核心约束（Mandatory）

1. **认证单一事实源**
   - 优先从根目录 `.env` 读取 `MAN_TUI_GROK_API_KEY` 与 `MAN_TUI_GROK_API_BASE_URL`。
   - 若存在 `MAN_TUI_GROK_CONNECTION_JSON`，脚本应从中提取 `key / url` 作为 Grok 专用连接。
   - 若 Grok 专用键缺失，再回退 `MAN_TUI_API_KEY` 与 `MAN_TUI_API_BASE_URL`。
   - 无 API Key 时必须硬退出，不得伪造 dry-run 成功。
2. **提交接口必须使用 `multipart/form-data`**
   - `POST /v1/videos` 必须通过 multipart 字段提交。
   - 禁止将创建任务错误写成 JSON 请求体。
3. **参考图模式互斥**
   - `input_reference` 与 `image_reference` 同一请求中默认互斥。
   - 若两者同时出现，必须视为输入冲突并拒绝执行。
4. **远程参考图必须是 JSON 字符串数组**
   - 对外接口字段 `image_reference` 必须传字符串，内容是 JSON 数组，例如：
   - `["https://a.png","https://b.png"]`
   - 若调用方以重复 `--image-reference-url` 传入，脚本必须先转成 JSON 字符串再提交。
5. **时长 / 尺寸 / 清晰度必须严格枚举**
   - `seconds` 仅允许：`6 / 10 / 12 / 16 / 20`
   - `size` 仅允许：`1280x720 / 720x1280 / 1792x1024 / 1024x1792 / 1024x1024`
   - `quality` 仅允许：`standard / high`
6. **状态轮询必须基于 `task_id`**
   - 创建成功后，唯一可靠追踪键为 `task_id`
   - 不得依赖 prompt 或时间戳猜测任务身份
7. **内容获取必须兼容 `200` 与 `302`**
   - `GET /content` 既可能直接返回二进制流，也可能返回 `302` 跳转到 CDN
   - 下载逻辑必须允许重定向，并记录最终来源 URL
8. **默认输出必须项目化**
   - 默认输出目录：`output/影片/[项目名]/5-API/video/man-tui/grok/`
   - 若 `task_kind=test` 且未显式传 `project_name`，默认项目名为 `测试`
   - 若 `task_kind=temp` 且未显式传 `project_name`，默认项目名为 `临时`
   - 若显式传 `--output-dir`，允许覆盖默认目录
9. **日志与报告禁止泄露密钥**
   - 控制台日志、报告 JSON、异常文本不得写出 Bearer token、`sk-...` 或完整未脱敏 URL
10. **失败优先修源层**
   - 若出现 multipart 构造错误、轮询失稳、下载失败、输出路径漂移、密钥泄露等问题，优先修复：
     - `scripts/grok_video.py`
     - 本 `SKILL.md`
   - 禁止只在单次调用时手工绕过而不修技能源层。

## 4. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-MTG-01` | 输入解析结果：`prompt / reference_mode / input_reference / image_reference / task_id` | 创建任务必须有 `prompt`；参考图模式清晰；状态与下载必须有 `task_id` | 用户输入、CLI 参数、`.env` | Step 1 | 输入收束完整度 | `FAIL-MTG-INPUT` |
| `FIELD-MTG-02` | 参数解析结果：`model / seconds / size / quality / output_dir / wait_policy` | 参数只允许落在已发布枚举中；输出路径和轮询策略明确 | 用户输入、默认值、项目化路径规则 | Step 2 | 参数合规性 | `FAIL-MTG-PARAMS` |
| `FIELD-MTG-03` | 创建请求：`multipart form / headers / files` | 创建任务必须是合法 multipart；`image_reference` 为 JSON 字符串数组；本地文件按文件句柄上传 | OpenAPI、脚本构造结果 | Step 3 | 请求体合法性 | `FAIL-MTG-CREATE` |
| `FIELD-MTG-04` | 状态与等待结果：`task_id / status / progress / url` | 状态轮询必须稳定；等待结束必须给出终态或超时结论 | 状态接口响应、轮询日志 | Step 4 | 执行稳定性 | `FAIL-MTG-STATUS` |
| `FIELD-MTG-05` | 输出产物：`report json / downloaded mp4 / final_url` | 报告可追溯；视频可落盘；重定向与最终文件路径可复盘 | 内容接口响应、落盘文件、报告 JSON | Step 5 | 输出可追溯性 | `FAIL-MTG-OUTPUT` |

## 5. 思维导引与执行流程（Mandatory）

### 5.1 固定步骤

1. **Step 1 / 输入收束**
   - 判断当前是 `create / status / content`
   - 收束 `prompt / task_id / input_reference / image_reference / output_dir / project_name / task_kind`
2. **Step 2 / 参数校验**
   - 校验 `seconds / size / quality`
   - 校验参考图模式是否互斥
   - 解析默认输出路径与等待策略
3. **Step 3 / 请求构造**
   - `create`：构造 multipart `data + files`
   - `status`：构造带认证的 GET
   - `content`：构造可跟随重定向的 GET
4. **Step 4 / 调用与轮询**
   - 创建成功后读取 `task_id`
   - 若启用 `--wait`，按 `poll_interval` 轮询直到终态或超时
   - 终态至少区分：`completed / failed / timeout / other terminal`
5. **Step 5 / 落盘与报告**
   - 创建/查询写任务报告 JSON
   - 获取内容时保存 MP4
   - 报告中记录 `request_summary / response / saved_file / final_url / error`

### 5.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-MTG-01` | 当前是创建、查询还是下载？输入最小闭环是否齐全？ | 收束命令类型与关键字段 | 缺 prompt、缺 task_id、参考图来源不清 |
| `Step 2` | `FIELD-MTG-02` | 参数是否落在接口枚举内？输出路径是否可落盘？ | 校验枚举与输出根 | seconds/size/quality 非法，路径漂移 |
| `Step 3` | `FIELD-MTG-03` | 创建请求是否真的是 multipart？远程参考图是否已 JSON 字符串化？ | 组装 headers/data/files | 错把请求做成 JSON，或 `image_reference` 形态错误 |
| `Step 4` | `FIELD-MTG-04` | 是否拿到了稳定 `task_id`？等待过程是否能明确结束？ | 发起请求、轮询状态 | 轮询无法结束、状态不透明 |
| `Step 5` | `FIELD-MTG-05` | 结果能否下载并复盘？ | 保存 MP4、写报告 | 视频未保存、报告缺字段、最终 URL 丢失 |

## 6. 标准调用

### 6.1 提交远程参考图任务

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py create \
  --prompt "动漫电影质感，双角色同框，夜晚都市江边，镜头缓慢推进，人物特征稳定，不要字幕，不要水印。" \
  --seconds 10 \
  --size 1792x1024 \
  --quality high \
  --image-reference-url "https://example.com/ref-a.png" \
  --image-reference-url "https://example.com/ref-b.png"
```

### 6.2 提交本地参考图任务

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py create \
  --prompt "电影级夜景双人角色视频，动作克制自然，强调五官稳定。" \
  --seconds 10 \
  --size 1792x1024 \
  --quality high \
  --input-reference /abs/path/ref.png
```

### 6.3 创建后等待并自动下载

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py create \
  --prompt "赛博都市角色视频，浅景深，高级构图。" \
  --seconds 10 \
  --size 1792x1024 \
  --quality high \
  --wait \
  --download-on-complete
```

### 6.4 查询状态

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py status \
  task_xxx \
  --wait
```

### 6.5 下载视频

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py content \
  task_xxx \
  --output output/影片/测试/5-API/video/man-tui/grok/task_xxx.mp4
```

## 7. 输出约定

- 默认输出目录：`output/影片/[项目名]/5-API/video/man-tui/grok/`
- 默认项目名映射：
  - `task_kind=project`：必须显式给 `project_name`，否则回退 `未命名项目`
  - `task_kind=test`：默认 `测试`
  - `task_kind=temp`：默认 `临时`
- 默认产物：
  - `man_tui_grok_create_report_YYYYmmdd_HHMMSS.json`
  - `man_tui_grok_status_report_YYYYmmdd_HHMMSS.json`
  - `task_<task_id>.mp4`
- 报告文件必须至少包含：
  - `ok`
  - `command`
  - `request_summary`
  - `response`
  - `saved_file`
  - `final_url`
  - `error`

## 8. 参考资料

- 接口摘要：`.agents/skills/api/man-tui/video/grok/references/api.md`
- 环境变量源：根目录 `.env`
- Grok 专用推荐块：

```dotenv
MAN_TUI_GROK_CONNECTION_JSON='{"_type":"newapi_channel_conn","key":"<grok-key>","url":"https://api.man-tui.com"}'
MAN_TUI_GROK_API_KEY=<grok-key>
MAN_TUI_GROK_API_BASE_URL=https://api.man-tui.com
```

## 9. Root-Cause 执行契约（Mandatory）

当调用失败、轮询异常或视频无法下载时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：API Key 缺失、multipart 构造错误、参考图模式冲突、`image_reference` 不是 JSON 字符串、状态轮询超时、内容下载未跟随重定向、输出路径漂移
-> `规则源`：`.agents/skills/api/man-tui/video/grok/SKILL.md` 与 `scripts/grok_video.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Context Loading / Registry Governance 契约
-> `Fix Landing Points`：优先修脚本请求构造、轮询逻辑、下载逻辑、报告脱敏与技能说明，再修局部调用样例

用户侧关闭语必须至少包含：
- 根因位置
- 立即修复
- 系统性预防修复

## 10. 失败排查

1. 检查根目录 `.env` 是否存在：
   - `MAN_TUI_GROK_API_KEY`
   - `MAN_TUI_GROK_API_BASE_URL`
   - 或 `MAN_TUI_GROK_CONNECTION_JSON`
2. 使用 dry-run 验证创建参数：

```bash
python3 .agents/skills/api/man-tui/video/grok/scripts/grok_video.py create \
  --prompt "test" \
  --dry-run --print-request
```

3. 若创建报 4xx：
   - 先检查 `image_reference` 是否是 JSON 字符串数组
   - 再检查 `seconds / size / quality` 是否落在发布枚举中
4. 若本地参考图报错：
   - 检查 `--input-reference` 路径是否存在且可读
5. 若等待一直无结果：
   - 先单独执行 `status task_xxx`
   - 再检查 `wait_timeout` 是否过短
6. 若下载失败：
   - 检查 `/content` 是否发生 `302`
   - 检查是否允许自动跟随重定向
7. 若报告中出现密钥：
   - 必须回到脚本脱敏层修复，不得接受“只是测试日志”

## 11. 字段通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| `FIELD-MTG-01` | 输入收束完整度 | 创建有 `prompt`；查询/下载有 `task_id`；参考图模式清晰 | `FAIL-MTG-INPUT` | 回到 `Step 1` |
| `FIELD-MTG-02` | 参数合规性 | `seconds / size / quality` 合法；输出目录可解析 | `FAIL-MTG-PARAMS` | 回到 `Step 2` |
| `FIELD-MTG-03` | 请求体合法性 | 创建请求确为 multipart；远程参考图为 JSON 字符串数组 | `FAIL-MTG-CREATE` | 回到 `Step 3` |
| `FIELD-MTG-04` | 执行稳定性 | 能稳定得到 `task_id`；等待能给出终态或超时说明 | `FAIL-MTG-STATUS` | 回到 `Step 4` |
| `FIELD-MTG-05` | 输出可追溯性 | 报告可读；MP4 可落盘；最终 URL 或内容来源可复盘 | `FAIL-MTG-OUTPUT` | 回到 `Step 5` |
