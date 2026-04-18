---
name: vidu
description: Use when the task must submit Vidu video generation jobs via `POST /v1/video/generations`, especially for prompt/image/first-last-frame driven creation with FineAPI-style fields and `.env`-managed `ANYFAST_VIDEO_API_KEY`.
governance_tier: full
---

# Vidu 生视频技能

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

- 本技能用于通过 Vidu 创建接口提交异步视频任务。
- 当前已确认真源：
  - 文档页：`https://docs.fineapi.cloud/403045611e0`
  - 创建接口：`POST /v1/video/generations`
  - 当前截图与文档可确认字段：
    - 请求头：`Accept / Content-Type / Authorization`
    - Body：`Model / SceneType / Prompt / NegativePrompt / EnhancePrompt / ImageUrl / ImageInfos / LastImageUrl / Duration / AdditionalParameters / Operator / StoreCosParam / ExtraParameters`
    - 响应：`id / task_id / model / status / created_at`
- 当前公开材料只稳定覆盖“创建任务”这一步；查询状态与下载结果端点在本轮材料中未锁定，因此本技能不得擅自虚构后续接口。
- 默认执行脚本：

```bash
python3 .agents/skills/api/video/vidu/scripts/vidu_video_generate.py submit ...
```

## 2. 必需输入

以下三者至少满足其一：

- `prompt`
- `image-url`
- `image-info / image-info-json`

API Key：

- 优先读取根目录 `.env` 中的 `ANYFAST_VIDEO_API_KEY`
- 回退 `VIDU_API_KEY`
- 再回退 `ANYFAST_API_KEY`
- 再回退 `FINEAPI_API_KEY`
- 也可显式传 `--api-key`

可选输入：

- `model`：默认模型治理统一回指父级 `../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族；脚本共享骨架使用 `../shared/default_model_policy.py`，Vidu 的 provider 特有差异是只允许 `Vidu-*` 通用模型作为默认值并排除 `mix` 变体；当前解析结果为 `Vidu-q3-pro`
- `scene-type`
- `negative-prompt`
- `enhance-prompt`
- `last-image-url`
- `duration`
- `additional-parameters`
- `operator`
- `cos-bucket-name / cos-bucket-region / cos-bucket-path`
- `resolution / aspect-ratio / logo-add / enable-audio / offpeak`
- `base-url`
  - 优先 `VIDU_API_BASE_URL`
  - 回退 `ANYFAST_API_BASE_URL`
  - 再回退 `FINEAPI_API_BASE_URL`
  - 再回退 `https://fw2afus.ent.acc.kurtisasia.com`
- `project-name`
- `output-dir`
- `filename-prefix`
- `report-json`
- `timeout`
- `dry-run`

## 3. 核心约束（Mandatory）

1. **当前只锁定创建接口**
   - 已证实的是 `POST /v1/video/generations`。
   - 在没有后续文档前，不得编造状态查询或下载端点。
2. **JSON 提交刚性**
   - 当前接口使用 `application/json`。
   - 不得误改为 multipart/form-data。
3. **输入门槛是“三选一”**
   - `Prompt / ImageUrl / ImageInfos` 至少填一项。
   - 不得把三项都空的请求静默发出。
4. **默认模型必须自动跟随当前已知最高通用 Vidu 型号**
   - 默认模型治理统一遵循父级 `../runbooks/default-model-policy.md` 的 `highest-available-general` 规则族。
   - 共享算法骨架由 `../shared/default_model_policy.py` 提供；`scripts/vidu_video_generate.py` 只补 Vidu 的本地过滤条件。
   - 当前解析结果为 `Vidu-q3-pro`；文档与 UI 元数据只能引用该裁决结果，不再各自写死旧型号。
5. **统一以 `.env` 的 `ANYFAST_VIDEO_API_KEY` 为主事实源**
   - 不在技能文件、脚本样例、报告中写明文 token。
6. **部分字段存在模型边界**
   - `ReferenceType` 截图标注“仅 GV 模型支持”。
   - `4:3 / 3:4` 截图标注“仅 q2 支持”。
   - `OffPeak` 截图标注“仅 Vidu 支持”。
   - 脚本应保留这些风险提示，而不是假装所有模型都完全支持。
7. **项目化输出路径**
   - 默认输出目录必须为 `output/影片/[项目名]/5-API/video/vidu/`。
   - 若未显式传 `project-name`，默认项目名使用 `测试`。
8. **失败优先修源层**
   - 若出现鉴权错误、字段大小写不匹配、模型边界误用、Base URL 漂移或把创建回执误认成成片，优先修：
     - `scripts/vidu_video_generate.py`
     - `references/api.md`
     - 本 `SKILL.md`

## 4. Visual Maps (Mermaid)

### 4.1 主流程

```mermaid
flowchart TD
    A["收束 Prompt / ImageUrl / ImageInfos"] --> B{"三选一至少一项存在?"}
    B -- 否 --> X["停止：补 prompt 或图像输入"]
    B -- 是 --> C["读取 ANYFAST_VIDEO_API_KEY 与 Base URL"]
    C --> D["裁决 Model / Duration / ExtraParameters"]
    D --> E{"dry-run?"}
    E -- 是 --> F["输出 payload 与 validation notes"]
    E -- 否 --> G["POST /v1/video/generations"]
    G --> H["保存 submit report"]
    H --> I["返回 task receipt: id / task_id / status"]
```

### 4.2 模型边界

```mermaid
flowchart TD
    A["扩展参数"] --> B{"aspect_ratio 为 4:3 / 3:4 ?"}
    B -- 是 --> C{"model 属于 Vidu-q2 系列?"}
    C -- 否 --> D["写 validation note：4:3 / 3:4 仅 q2 支持"]
    C -- 是 --> E["允许提交"]
    B -- 否 --> F["继续"]
    F --> G{"ImageInfos 带 ReferenceType?"}
    G -- 是 --> H["写 validation note：ReferenceType 截图标注仅 GV 支持"]
    G -- 否 --> I["继续"]
```

## 5. 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| `FIELD-VIDU-01` | 输入解析结果：`Prompt / ImageUrl / ImageInfos / project_name` | 三者至少一项有效；`ImageInfos` 结构合法 | 文档截图、CLI 参数 | Step 1 | 输入收束完整度 | `FAIL-VIDU-INPUT` |
| `FIELD-VIDU-02` | 参数裁决结果：`Model / Duration / Base URL / ExtraParameters` | 默认模型固定；枚举字段合法；模型边界被显式提示 | 文档页、截图、脚本默认值 | Step 2 | 参数与环境一致性 | `FAIL-VIDU-PARAMS` |
| `FIELD-VIDU-03` | 创建请求：`POST /v1/video/generations` JSON 请求体 | Header 与 Body 字段名准确；可选嵌套对象结构正确 | 文档页、截图、脚本构造结果 | Step 3 | 请求体合法性 | `FAIL-VIDU-CREATE` |
| `FIELD-VIDU-04` | 创建回执：`id / task_id / model / status / created_at` | 报告完整保留任务回执，不把其误判为成片结果 | 文档截图响应、API 响应 | Step 4 | 回执闭环完整性 | `FAIL-VIDU-RECEIPT` |

## 6. 思维导引与执行流程（Mandatory）

### 6.1 固定步骤

1. **Step 1 / 输入收束**
   - 读取 `prompt`、`image_url`、`image_infos`
   - 校验三者至少一项存在
   - 若传 `image_infos`，统一归一成 `[{ImageUrl, ReferenceType?}]`
2. **Step 2 / 参数与环境裁决**
   - 读取 `.env` 中的 `ANYFAST_VIDEO_API_KEY`
   - 读取 `VIDU_API_BASE_URL / ANYFAST_API_BASE_URL / FINEAPI_API_BASE_URL`
   - 校验 `resolution / aspect_ratio / logo_add`
   - 对 `ReferenceType / 4:3 / 3:4 / OffPeak` 写入模型边界提示
3. **Step 3 / 创建任务**
   - 组装 JSON：`Model / SceneType / Prompt / NegativePrompt / EnhancePrompt / ImageUrl / ImageInfos / LastImageUrl / Duration / AdditionalParameters / Operator / StoreCosParam / ExtraParameters`
   - 提交到 `/v1/video/generations`
4. **Step 4 / 回执落盘**
   - 保存任务回执 JSON
   - 输出 `id / task_id / model / status / created_at`
   - 明确声明“当前闭环停在 create receipt，不含状态轮询与下载”

### 6.2 思维导引表

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `Step 1` | `FIELD-VIDU-01` | 是否至少收束了 prompt、单图或多图参考之一？ | 校验三选一与 `ImageInfos` 结构 | 三项全空、`ImageInfos` 非法、空字符串输入 |
| `Step 2` | `FIELD-VIDU-02` | API Key、Base URL 与扩展参数是否明确？ | 裁决环境变量并生成 validation notes | Base URL 缺失、模型边界被吞掉、枚举越界 |
| `Step 3` | `FIELD-VIDU-03` | 请求体是否严格贴合字段大小写与嵌套对象？ | 构造 JSON 并提交 | 字段拼成小写、嵌套对象结构错、布尔型误传字符串 |
| `Step 4` | `FIELD-VIDU-04` | 是否把创建回执正确落盘并解释为 task receipt？ | 保存 submit report 并规范化回执 | 把 `queued/processing` 说成已出片 |

## 7. 标准调用

### 7.1 文生视频

```bash
python3 .agents/skills/api/video/vidu/scripts/vidu_video_generate.py submit \
  --prompt "一只猫在草地上奔跑，阳光明媚" \
  --project-name "测试"
```

### 7.2 图生视频

```bash
python3 .agents/skills/api/video/vidu/scripts/vidu_video_generate.py submit \
  --image-url "https://example.com/reference.jpg" \
  --prompt "保持角色主体，镜头缓慢推进，电影级自然光" \
  --project-name "测试"
```

### 7.3 多图参考

```bash
python3 .agents/skills/api/video/vidu/scripts/vidu_video_generate.py submit \
  --prompt "让角色延续参考图中的服装与质感，形成平稳推镜" \
  --image-info "https://example.com/ref-a.jpg|style" \
  --image-info "https://example.com/ref-b.jpg|asset"
```

### 7.4 首尾帧

```bash
python3 .agents/skills/api/video/vidu/scripts/vidu_video_generate.py submit \
  --image-url "https://example.com/start.jpg" \
  --last-image-url "https://example.com/end.jpg" \
  --prompt "从首帧自然过渡到尾帧，动作连续"
```

### 7.5 Dry Run 检查请求体

```bash
python3 .agents/skills/api/video/vidu/scripts/vidu_video_generate.py submit \
  --prompt "测试请求" \
  --resolution 720P \
  --aspect-ratio 16:9 \
  --dry-run \
  --print-payload
```

## 8. 参数约定

| CLI 参数 | 创建字段 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--model` | `Model` | 自动裁决（当前 `Vidu-q3-pro`） | 默认模型 |
| `--scene-type` | `SceneType` | 不发送 | 场景类型字符串 |
| `--prompt` | `Prompt` | 无 | 可选，但与图像输入三选一 |
| `--negative-prompt` | `NegativePrompt` | 不发送 | 负向提示词 |
| `--enhance-prompt` | `EnhancePrompt` | 不发送 | 显式传 `true/false` 时才写入 |
| `--image-url` | `ImageUrl` | 不发送 | 单图参考 |
| `--image-info` | `ImageInfos[]` | 可重复 | 格式：`URL|style` 或 `URL|asset` |
| `--image-info-json` | `ImageInfos[]` | 可重复 | 直接传单个 JSON 对象 |
| `--last-image-url` | `LastImageUrl` | 不发送 | 尾帧图 |
| `--duration` | `Duration` | 不发送 | 秒数，文档截图示例为 `5` |
| `--additional-parameters` | `AdditionalParameters` | 不发送 | 原样字符串 |
| `--operator` | `Operator` | 不发送 | 操作者标识 |
| `--resolution` | `ExtraParameters.Resolution` | 不发送 | `720P / 768P / 1080P` |
| `--aspect-ratio` | `ExtraParameters.AspectRatio` | 不发送 | `16:9 / 9:16 / 1:1 / 4:3 / 3:4` |
| `--logo-add` | `ExtraParameters.LogoAdd` | 不发送 | `0 / 1` |
| `--enable-audio` | `ExtraParameters.EnableAudio` | 不发送 | 显式传 `true/false` |
| `--offpeak` | `ExtraParameters.OffPeak` | 不发送 | 截图标注仅 Vidu 支持 |
| `--base-url` | API Base URL | `.env` 回退链 | 优先 `VIDU_API_BASE_URL`，回退 `ANYFAST_API_BASE_URL` |

完整字段说明见：`references/api.md`

## 9. 输出约定

- 默认输出目录：`output/影片/[项目名]/5-API/video/vidu/`
- 默认产物：
  - `vidu_submit_report_YYYYmmdd_HHMMSS.json`
- 报告至少包含：
  - `ok`
  - `command`
  - `request_summary`
  - `normalized_submit`
  - `validation_notes`
  - `diagnostic_hint`
  - `raw_response`
  - `error`

## 10. Root-Cause 执行契约（Mandatory）

当创建失败、字段大小写不对、三选一输入缺失、模型边界误用、Base URL 漂移或调用方误以为任务已出片时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：API Key 缺失、Base URL 未配置、`Prompt/ImageUrl/ImageInfos` 同时为空、`ReferenceType` 用在非 GV 模型、`4:3/3:4` 用在非 q2、把 task receipt 误读为成片
-> `规则源`：`.agents/skills/api/video/vidu/SKILL.md`、`references/api.md`、`scripts/vidu_video_generate.py`
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的 Root-Cause First / Context Loading / Canonical Source / Composite Output 治理契约
-> `Fix Landing Points`：优先修脚本的环境变量回退、字段映射、validation notes 和回执解释，再修样例

用户侧关闭语必须至少包含：
- 根因位置
- 立即修复
- 系统性预防修复

## 11. 失败排查

1. 检查 `.env` 是否存在 `ANYFAST_VIDEO_API_KEY`
2. 检查 `.env` 或命令行是否已提供 `VIDU_API_BASE_URL / ANYFAST_API_BASE_URL / --base-url`
3. 使用 `submit --dry-run --print-payload` 确认 JSON 请求体
4. 若 `Prompt / ImageUrl / ImageInfos` 三项都空，先补至少一项再提交
5. 若使用 `ReferenceType` 且模型不是 `GV-*`，先去掉该字段再试
6. 若使用 `4:3 / 3:4` 但模型不是 `Vidu-q2*`，先改回 `16:9 / 9:16 / 1:1`
7. 若响应只有 `id / task_id / status / created_at`，说明只是创建成功，不是下载完成
