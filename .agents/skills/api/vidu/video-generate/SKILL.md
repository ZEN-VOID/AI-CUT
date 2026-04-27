---
name: vidu-video-api
governance_tier: full
description: |
  repo-local Vidu 视频 API 技能。统一覆盖 Vidu 企业版视频创建接口（参考生、文生、图生、首尾帧、智能多帧、场景特效模板、模板成片）以及任务查询、任务列表、取消任务、积分查询与回调签名校验。适用于用户提到 `vidu`、`reference2video`、`text2video`、`img2video`、`start-end2video`、`multiframe`、`template-story`、Vidu 回调验签等场景。
tools: [Read, Write, Edit, Bash]
color: teal
version: "v1.0"
---

# Vidu 视频 API 技能

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

- 本技能用于统一驱动 Vidu 企业版视频 API：
  - `POST /ent/v2/reference2video`
  - `POST /ent/v2/text2video`
  - `POST /ent/v2/img2video`
  - `POST /ent/v2/start-end2video`
  - `POST /ent/v2/multiframe`
  - `POST /ent/v2/template`
  - `POST /ent/v2/template-story`
  - `GET /ent/v2/tasks/{id}/creations`
  - `GET /ent/v2/tasks`
  - `POST /ent/v2/tasks/{id}/cancel`
  - `GET /ent/v2/credits`
  - 回调签名生成与验签
- 默认 API 根地址：优先读取根目录 `.env` 的 `VIDU_API_BASE_URL`，回退 `https://api.vidu.cn`
- 默认认证：优先读取根目录 `.env` 的 `VIDU_API_KEY`
- Vidu 官方请求头规范：`Authorization: Token {your api key}`
- 统一脚本入口：

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py [subcommand] [参数]
```

## 2. 目录与模块约定

- 主合同：`SKILL.md`
- 经验层：`CONTEXT.md`
- 入口元数据：`agents/openai.yaml`
- 统一执行脚本：`scripts/vidu_video.py`
- 参考模块：
  - `references/overview.md`
  - `references/reference-to-video.md`
  - `references/text-to-video.md`
  - `references/image-to-video.md`
  - `references/start-end-to-video.md`
  - `references/multi-frame.md`
  - `references/template.md`
  - `references/template-story.md`
  - `references/task-management.md`
  - `references/callback-signature.md`

说明：
- 与其把每个 Vidu 能力拆成兄弟子技能，本技能默认采用“一个 provider skill + references 模块”的收束方式。
- 简单任务可直接走 CLI 参数。
- 全字段、复杂主体、关键帧、模板专属参数或文档后续新增字段，优先使用 `--input-json` 直传原始请求体，再由本技能负责认证、媒体归一、轮询、下载、报告与日志脱敏。

## 3. 必需输入

### 3.1 创建任务

- `mode`：`reference2video / text2video / img2video / start-end2video / multiframe / template / template-story`
- API Key（优先读取 `.env` 中的 `VIDU_API_KEY`，也可显式传 `--api-key`）
- 对应模式的最小请求体

推荐输入策略：
- 简单模式：直接用 CLI 传常用字段
- 复杂模式：使用 `--input-json <path>` 作为唯一业务请求体真源

### 3.2 任务管理

- `task_id`：查询生成物、取消任务时必需
- 列表查询参数：按需传入
- `show_detail`：查积分时可选，默认 `false`

### 3.3 回调签名

- `callback_url`
- `http_method`
- `Date`
- `X-HMAC-SIGNED-HEADERS` 对应的 header 顺序和值
- `secret_key`，默认可回退到 `VIDU_API_KEY`

## 4. 核心约束（Mandatory）

1. **认证单一事实源**
   - 优先从根目录 `.env` 读取 `VIDU_API_KEY` 与 `VIDU_API_BASE_URL`
   - 无 API Key 时必须硬退出，不得伪造 dry-run 成功
2. **请求头必须使用 Vidu 官方格式**
   - 所有 HTTP 请求默认使用：
   - `Authorization: Token <VIDU_API_KEY>`
   - `Content-Type: application/json`
3. **复杂字段优先走 `--input-json`**
   - `subjects`、`image_settings`、模板专属字段、后续新增字段不要强行塞进大量 CLI 开关
   - 这些字段的业务真源应优先落在 JSON 文件，再通过 `--input-json` 直传
4. **媒体输入允许 URL、data URL 或本地文件**
   - 脚本允许把本地图片/视频路径自动转成 data URL
   - 已是 `http(s)://` 或 `data:` 的值应原样透传
5. **任务完成态以查询接口为准**
   - 创建接口成功只代表拿到 `task_id`
   - 任务最终状态、下载链接与消耗积分，必须以 `GET /ent/v2/tasks/{id}/creations` 为准
6. **下载优先级固定**
   - 默认下载不带水印生成物：`creations[*].url`
   - 若显式要求带水印，则改用 `creations[*].watermarked_url`
   - 下载链接只有 24 小时有效，应及时落盘
7. **错峰任务可取消**
   - `off_peak=true` 的任务仍需支持手动取消
   - 取消动作必须显式记录到报告，而不是只依赖终端滚屏
8. **报告与日志必须脱敏**
   - 报告 JSON、控制台异常与本地日志不得暴露原始 API Key
   - 带签名 query 的生成物 URL 只可保留无 query 主体
9. **默认输出必须项目化**
   - 默认输出目录：`output/影片/[项目名]/5-API/video/vidu/`
   - 若 `task_kind=test` 且未显式传 `project_name`，默认项目名为 `测试`
   - 若 `task_kind=temp` 且未显式传 `project_name`，默认项目名为 `临时`
10. **失败优先修源层**
   - 若出现认证头错误、媒体归一错误、轮询失稳、生成物下载漂移、回调验签顺序错误或输出路径漂移，优先修复：
   - `scripts/vidu_video.py`
   - 本 `SKILL.md`
   - 对应 `references/*.md`

## 5. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-VDU-01` | 输入解析：`command / mode / task_id / input_json` | 动作与最小输入闭环明确 | 用户输入、CLI 参数、JSON 文件 | Step 1 | 输入收束完整度 | `FAIL-VDU-INPUT` |
| `FIELD-VDU-02` | 认证与请求：`base_url / auth_header / endpoint / request_body` | API 根地址、认证头、端点与请求体一致 | `.env`、脚本构造结果、官方文档 | Step 2 | 请求正确性 | `FAIL-VDU-REQUEST` |
| `FIELD-VDU-03` | 媒体归一：`images / videos / start_image / key_image / subjects` | 本地路径、URL 与 data URL 归一稳定 | 本地文件、JSON 文件、CLI 参数 | Step 3 | 媒体输入稳定性 | `FAIL-VDU-MEDIA` |
| `FIELD-VDU-04` | 执行结果：`task_id / state / credits / creations` | 状态、积分、生成物与失败原因可追踪 | 创建响应、查询响应 | Step 4 | 执行稳定性 | `FAIL-VDU-TASK` |
| `FIELD-VDU-05` | 落盘与签名：`saved_file / report_json / callback_signature` | 生成物、报告、回调验签结果可复盘 | 本地文件、回调头、脚本输出 | Step 5 | 输出可追溯性 | `FAIL-VDU-OUTPUT` |

## 6. 思维导引与执行流程（Mandatory）

### 6.1 固定步骤

1. **Step 1 / 输入收束**
   - 判断当前是 `create / task / list / cancel / credits / verify-callback`
   - 创建任务时再锁定 `mode`
   - 收束 `input_json / project_name / output_dir / wait_policy`
2. **Step 2 / 请求构造**
   - 解析根 `.env`
   - 决定 API 根地址、认证头、目标端点和查询参数
   - 对复杂模式优先信任 `--input-json`
3. **Step 3 / 媒体归一**
   - 把本地图片/视频转为 data URL
   - 保持 `http(s)` 与已有 `data:` 原样透传
   - 仅对已知媒体字段做定点归一，避免意外改写业务 JSON
4. **Step 4 / 调用与轮询**
   - 创建成功后提取 `task_id`
   - 若启用 `--wait`，循环查询 `GET /ent/v2/tasks/{id}/creations`
   - 终态至少区分：`success / failed / timeout`
5. **Step 5 / 落盘与报告**
   - 查询成功后按 `creation_index` 选择生成物
   - 下载视频
   - 写报告 JSON
   - 回调验签场景输出签名字符串、计算值、校验结果

### 6.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-VDU-01` | 当前动作与模式是否明确？最小输入是否齐全？ | 收束命令与关键参数 | `mode` 缺失、`task_id` 缺失、JSON 文件不存在 |
| `Step 2` | `FIELD-VDU-02` | 请求是否对准官方端点？认证头是否是 `Token` 格式？ | 构造 headers / path / query | 401、404、把查询接口打成创建接口 |
| `Step 3` | `FIELD-VDU-03` | 输入媒体是 URL、data URL 还是本地文件？是否需要转码？ | 归一媒体字段 | 本地路径未转 data URL、主体视频字段残留无效路径 |
| `Step 4` | `FIELD-VDU-04` | 是否拿到稳定 `task_id`？终态与积分是否明确？ | 发请求、轮询、解析状态 | 只拿创建响应就宣称成功、漏掉 `failed`、误读 `creations` |
| `Step 5` | `FIELD-VDU-05` | 下载、报告与回调验签结果能否复盘？ | 落盘、脱敏、验签 | URL 泄露 query、无报告、签名顺序错乱 |

## 7. 标准调用

### 7.1 文生视频

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py create \
  --mode text2video \
  --model viduq3-turbo \
  --prompt "赛博雨夜中的角色缓慢回头，霓虹倒影，电影级镜头运动" \
  --duration 5 \
  --aspect-ratio 16:9 \
  --resolution 720p
```

### 7.2 图生视频

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py create \
  --mode img2video \
  --model viduq3-pro-fast \
  --image ./first-frame.png \
  --prompt "角色抬头望向镜头，风吹动头发，城市灯光闪烁" \
  --duration 5
```

### 7.3 首尾帧生视频

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py create \
  --mode start-end2video \
  --model viduq3-pro \
  --image ./start.png \
  --image ./end.png \
  --prompt "从安静站立过渡到转身离开"
```

### 7.4 复杂模式走 JSON 真源

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py create \
  --mode reference2video \
  --input-json /abs/path/reference2video.json \
  --wait \
  --download-on-complete
```

### 7.5 查询任务并下载生成物

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py task \
  --task-id your_task_id \
  --download-on-complete
```

### 7.6 查询任务列表

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py list \
  --state success \
  --pagesz 20
```

### 7.7 取消任务

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py cancel \
  --task-id your_task_id
```

### 7.8 查询积分

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py credits \
  --show-detail
```

### 7.9 校验回调签名

```bash
python3 .agents/skills/api/vidu/video-generate/scripts/vidu_video.py verify-callback \
  --callback-url "https://example.com/vidu/callback?scene=demo" \
  --http-method POST \
  --date "Tue, 06 May 2025 12:09:42 GMT" \
  --header "Date=Tue, 06 May 2025 12:09:42 GMT" \
  --header "x-request-nonce=123e4567-e89b-12d3-a456-426614174000" \
  --signed-header Date \
  --signed-header x-request-nonce
```

## 8. 输出与产物合同

- 默认输出目录：`output/影片/[项目名]/5-API/video/vidu/`
- 统一报告：
  - 创建：`create-<mode>-<task_id>.json`
  - 查询：`task-<task_id>.json`
  - 列表：`list-<timestamp>.json`
  - 取消：`cancel-<task_id>.json`
  - 积分：`credits-<timestamp>.json`
  - 回调验签：`callback-signature-<timestamp>.json`
- 默认下载文件名：
  - `<task_id>-<creation_id>.mp4`

## 9. 参考模块

- 总览：`.agents/skills/api/vidu/video-generate/references/overview.md`
- 参考生：`.agents/skills/api/vidu/video-generate/references/reference-to-video.md`
- 文生视频：`.agents/skills/api/vidu/video-generate/references/text-to-video.md`
- 图生视频：`.agents/skills/api/vidu/video-generate/references/image-to-video.md`
- 首尾帧：`.agents/skills/api/vidu/video-generate/references/start-end-to-video.md`
- 智能多帧：`.agents/skills/api/vidu/video-generate/references/multi-frame.md`
- 场景特效模板：`.agents/skills/api/vidu/video-generate/references/template.md`
- 模板成片：`.agents/skills/api/vidu/video-generate/references/template-story.md`
- 任务管理：`.agents/skills/api/vidu/video-generate/references/task-management.md`
- 回调签名：`.agents/skills/api/vidu/video-generate/references/callback-signature.md`

## 10. Root-Cause Trace

当 Vidu 调用失败时，按以下链路追因：

`Symptom / Failure`
-> `Direct Technical Cause`
-> `Rule Source`: `.agents/skills/api/vidu/video-generate/SKILL.md`、`scripts/vidu_video.py`、对应 `references/*.md`
-> `Meta Rule Source`: 根 `AGENTS.md`
-> `Fix Landing Points`

典型落点：
- 认证或请求体问题：`scripts/vidu_video.py`
- 接口字段和模式合同问题：`references/*.md` 与本 `SKILL.md`
- 输出路径或报告脱敏漂移：`scripts/vidu_video.py` 与 `CONTEXT.md`
