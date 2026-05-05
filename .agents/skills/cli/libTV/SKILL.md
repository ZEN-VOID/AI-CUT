---
name: libtv-skill
description: agent-im 会话技能 - 通过 liblib.tv 的 AI 能力生成和编辑图片/视频。覆盖场景包括：生成（文生图、文生视频、图生视频、做动画、画一个xxx、来段xxx）、编辑修改（把xxx换成yyy、去掉xxx、加上xxx、改成xxx、调整xxx、局部修改、改镜头）、风格转换（风格迁移、转绘、换风格）、视频续写延长、复刻视频/TVC/宣传片、短剧/短漫剧生成、音乐MV生成、产品广告/展示片制作、分镜/故事板设计、教育视频/短视频制作。当用户提到 liblib、libtv、上传参考图/视频、查看生成进度时也应触发。关键判断：只要用户的请求涉及 AI 图片或视频的创作、生成、编辑、修改，无论措辞如何（如"画只猫"、"做个海报"、"把纸船换成爱心"、"这个视频帮我改一下"、"帮我复刻这段视频"、"用这首歌做个MV"、"一句话生成短剧"），都必须触发此技能。
governance_tier: full
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "requires":
          {
            "bins": ["python3"],
            "env": ["LIBTV_ACCESS_KEY"]
          },
        "primaryEnv": "LIBTV_ACCESS_KEY"
      }
  }
---

# agent-im 会话（生图 / 生视频）

通过 agent-im 的 OpenAPI 创建会话、发送消息（生图、生视频、编辑视频等）、上传图片/视频文件，并查询会话消息进展。

LibTV 是 LiblibAI 推出的 AI 视频创作平台，同时为人类创作者和 Agent 设计。Agent 通过 Skill 入口理解任务、调用模型并自动编排工作流。

**平台核心能力：**
- **生成**：文生图、文生视频、图生视频、视频续写
- **编辑**：局部修改、元素替换、镜头调整、风格迁移
- **复杂创作**：一句话生成完整短剧（剧本→分镜→成片）、复刻已有视频风格做 TVC/宣传片、用音乐生成 MV、产品展示片制作
- **模型**：Seedance 2.0、Kling 3.0/O3、Wan 2.6、NanoBanana、Midjourney、Seedream 5.0 等顶级模型

用户的所有创作和编辑需求都通过发送自然语言消息来完成，Agent 会自主编排工作流。复杂任务（短剧、MV）耗时较长，需耐心轮询。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- 每次调用本技能时，必须同时识别并加载同目录 `types/` 中选中的类型包（单选或多选）。若 `types/` 当前缺失，视为 Skill 2.0 结构缺口，本轮临时使用 `CONTEXT.md` 的 Type Map 进行降级判型，并在交付中报告该缺口。
- 先读取本 `SKILL.md`，锁定输入边界、调用路径、画布默认工作区规则、输出合同和禁止事项；再加载同目录 `CONTEXT.md`，用于选择策略并避开已知失败模式。
- 若当前任务绑定具体 AIGC 项目根，还必须按仓库规则加载项目根 `MEMORY.md` 与项目根 `CONTEXT/` 中和本轮 LibTV 任务相关的上下文文件。
- 当前目录只保留本技能入口合同、经验层与机械脚本；脚本只能上传、创建会话、查询、切换项目和下载，不得替代 LLM 或 LibTV 后端 Agent 做创作决策。
- 冲突优先级：用户显式请求 > 仓库 `AGENTS.md` > 本 `SKILL.md` > `references/`、`types/`、`steps/`、`review/`、`templates/`、`knowledge-base/` > 同目录 `CONTEXT.md` > `scripts/` 的机械行为。

## Reference Loading Guide

| 场景 | 必须加载 |
| --- | --- |
| 任意 LibTV 生成、编辑、查询或下载任务 | `SKILL.md` + 同目录 `CONTEXT.md` |
| 新建图片/视频生成任务 | 本文件的“典型工作流”“核心原则”“注意事项”与 `CONTEXT.md` 的生成类经验 |
| 本地图片/视频作为参考或编辑源 | 本文件的上传流程与 `CONTEXT.md` 的参考文件交接经验 |
| 查询进度、下载结果或追加已有会话 | 本文件的查询/下载/已有会话流程与 `CONTEXT.md` 的 session 操作经验 |
| 脚本命令细节 | `scripts/create_session.py`、`scripts/query_session.py`、`scripts/upload_file.py`、`scripts/download_results.py`、`scripts/change_project.py` |
| 后续恢复完整 Skill 2.0 分区后 | `references/`、`types/type-map.md`、`steps/`、`review/`、`templates/`、`knowledge-base/` 中和任务相关的文件 |

若后续恢复 `types/`、`steps/`、`review/`、`templates/` 等 Skill 2.0 分区，必须同步更新本表，避免 `SKILL.md` 与分区真源脱节。

## Input Contract

- 接受输入：文生图、文生视频、图生视频、视频续写、图片/视频编辑、风格迁移、短剧/MV/广告/分镜生成、上传参考文件、查询会话进度、下载结果、切换项目或向已有会话追加消息。
- 必需输入：实时调用必须有 `LIBTV_ACCESS_KEY`；新建创作任务必须有用户原始自然语言需求；参考/编辑任务必须有可访问的本地图片或视频路径；查询或下载任务必须有 `sessionId`。
- 可选输入：`OPENAPI_IM_BASE`、`IM_BASE_URL`、已有 `sessionId`、`projectUuid`、输出目录、文件名前缀、显式视频时长、声音要求或静音要求。
- 需要先澄清：用户给出多个参考文件但角色不清、输出目录可能覆盖既有结果、用户要求本地 Agent 改写创意内容但没有说明改写目标。
- 必须停止：缺少凭证、文件不存在、文件不是图片/视频、上传失败、API 未返回可用会话或结果、用户要求脚本或本地 Agent 代替后端做创作主判断。

## Multi-Subskill Continuous Workflow

- 本技能当前没有同级子技能包；整体调用时按本文件的步骤连续完成已选路径，不在上传、创建会话、轮询、下载等内部节点之间反复询问。
- 若未来恢复或新增数字序号子技能包，默认按数字升序串行；若恢复无序号同级子技能包，默认全选并行；若恢复英文序号路线，默认按用户意图或任务类型单选。
- 连续执行不得越过阻断门：缺凭证、缺文件、路径角色不清、会覆盖用户文件、或会把错误 prompt 发给 LibTV 时必须先停下。
- 子技能、卫星技能或 reviewer 若在未来重新接入，仍必须加载自身 `SKILL.md + CONTEXT.md`，其结果回流到本技能的唯一交付口。

## 功能

1. **创建会话 / 发消息** - 创建新会话或向已有会话发送一条消息（如「生一个动漫视频」「把纸船换成爱心」）
2. **查询会话进展** - 根据 sessionId 拉取该会话的消息列表，用于轮询生图/生视频结果
3. **切换项目** - 将当前 accessKey 绑定的项目切换到新项目，后续 create_session 将使用新 projectUuid
4. **上传文件** - 上传图片或视频文件到 OSS，返回可访问的 OSS 地址（编辑已有视频/图片时需要先上传）
5. **下载结果** - 将会话中生成的图片/视频批量下载到本地，自动提取 URL 并命名

## 前置要求

```bash
export LIBTV_ACCESS_KEY="your-access-key"
```

可选：`OPENAPI_IM_BASE` 或 `IM_BASE_URL`，默认 `https://im.liblib.tv`。

无需安装额外依赖，仅使用 Python 标准库。

## 使用方法

### 1. 创建会话 / 发送消息

```bash
# 创建新会话并发送「生一个动漫视频」
python3 {baseDir}/scripts/create_session.py "生一个动漫视频"

# 向已有会话发送消息
python3 {baseDir}/scripts/create_session.py "再生成一张风景图" --session-id SESSION_ID

# 只创建/绑定会话，不发消息
python3 {baseDir}/scripts/create_session.py
```

### 2. 查询会话进展

```bash
# 查询会话消息列表
python3 {baseDir}/scripts/query_session.py SESSION_ID

# 增量拉取（只返回 seq 大于 N 的消息）
python3 {baseDir}/scripts/query_session.py SESSION_ID --after-seq 5

# 附带项目地址（传入 create_session 返回的 projectUuid，结果中带 projectUrl）
python3 {baseDir}/scripts/query_session.py SESSION_ID --project-id PROJECT_UUID
```

### 3. 切换项目

```bash
# 切换当前 accessKey 绑定的项目（后续创建会话将使用新项目）
python3 {baseDir}/scripts/change_project.py
```

### 4. 上传文件

当用户提供了参考的文件地址时，进行上传，仅支持图片、视频，文件大小必须在200M以下。

```bash
# 上传图片
python3 {baseDir}/scripts/upload_file.py /path/to/image.png

# 上传视频
python3 {baseDir}/scripts/upload_file.py /path/to/video.mp4
```

### 5. 下载结果

生成完成后，可以将会话中的所有图片/视频批量下载到本地。

```bash
# 从会话自动提取并下载所有结果
python3 {baseDir}/scripts/download_results.py SESSION_ID

# 指定输出目录
python3 {baseDir}/scripts/download_results.py SESSION_ID --output-dir ~/Desktop/my_project

# 指定文件名前缀（如 storyboard_01.png, storyboard_02.png ...）
python3 {baseDir}/scripts/download_results.py SESSION_ID --prefix "storyboard"

# 直接下载指定 URL 列表（不需要 session_id）
python3 {baseDir}/scripts/download_results.py --urls URL1 URL2 URL3 --output-dir ./output
```

## 典型工作流

理解这些工作流，才能正确组合上面的脚本完成用户需求。

### 场景 1：用户要求生成图片/视频（最常见）

```
1. create_session.py "把全部工作流和结果都放在画布上。用户的描述"  →  拿到 sessionId + projectUuid
2. 每隔 8 秒调用 query_session.py SESSION_ID --after-seq 0 轮询
3. 检查 messages：当出现 assistant 角色的消息且包含图片/视频 URL → 任务完成
4. 自动下载：download_results.py SESSION_ID --output-dir ~/Downloads/项目名 --prefix 有意义的前缀
5. 向用户展示：本地文件列表 + projectUrl（画布链接）
```

生成完成后**自动执行下载**，不需要用户额外请求。下载目录和前缀根据任务语义自动命名（如分镜用 `storyboard`，角色设定用 `character` 等）。

新建生成或编辑任务时，默认把完整生成工作流和结果放在 LibTV 项目画布上。提交给 LibTV 的消息必须包含独立的操作性指令：`把全部工作流和结果都放在画布上。` 这不是创作扩写，不得替代、改写或稀释用户原始描述。

### 场景 2：用户提供图片/视频要求编辑修改（如"把纸船换成爱心"）

```
1. upload_file.py /path/to/video.mp4  →  拿到 OSS URL
2. create_session.py "把全部工作流和结果都放在画布上。把四周的纸船都换成白色的纸爱心 参考视频：{oss_url}"
3. 后续同场景 1 的步骤 2-5
```

用户给了文件路径 + 编辑指令 = 先上传文件，再把编辑指令和 OSS URL 一起发送。

### 场景 3：用户提供参考图/视频要求生成新内容

```
1. upload_file.py /path/to/ref.png  →  拿到 OSS URL
2. create_session.py "根据参考图生成xxx，参考图：{oss_url}"
3. 后续同场景 1 的步骤 2-5
```

### 场景 4：在已有会话中追加新需求

```
1. create_session.py "新的描述" --session-id SESSION_ID
2. 后续同场景 1 的步骤 2-5
```

### 轮询策略

- **间隔**：每 8 秒查询一次
- **增量拉取**：首次用 `--after-seq 0`，后续用上次拿到的最大 seq 值
- **完成判断**：messages 中出现 assistant 消息且 content 包含结果 URL（图片/视频地址）
- **超时**：连续轮询 3 分钟仍无结果，告知用户"生成时间较长，可稍后通过项目画布链接查看"，不再继续轮询
- **错误重试**：单次查询失败可重试 1 次，连续 3 次失败则停止并告知用户

## 输出格式

**create_session** 返回：
```json
{
  "projectUuid": "aa3ba04c5044477cb7a00a9e5bf3b4d0",
  "sessionId": "90f05e0c-...",
  "projectUrl": "https://www.liblib.tv/canvas?projectId=aa3ba04c5044477cb7a00a9e5bf3b4d0"
}
```

**query_session** 返回：
```json
{
  "messages": [
    {"id": "msg-xxx", "role": "user", "content": "生一个动漫视频"},
    {"id": "msg-yyy", "role": "assistant", "content": "..."}
  ],
  "projectUrl": "https://www.liblib.tv/canvas?projectId=..."
}
```
（`projectUrl` 仅在传入 `--project-id` 时存在）

**change_project** 返回：
```json
{
  "projectUuid": "新项目UUID",
  "projectUrl": "https://www.liblib.tv/canvas?projectId=新项目UUID"
}
```

**upload_file** 返回：
```json
{
  "url": "https://libtv-res.liblib.art/claw/{projectUuid}/{uuid}.png"
}
```

**download_results** 返回：
```json
{
  "output_dir": "/Users/xxx/Downloads/libtv_results",
  "downloaded": ["/Users/xxx/Downloads/libtv_results/01.png", "..."],
  "total": 9
}
```

## 最终向用户展示时（OpenClaw）

- **视频地址**：来自 `query_session` 返回的 `messages` 中 assistant 消息的 content 或结果里的视频/图片 URL，即「返回的结果」。
- **项目地址**：使用 `create_session` 返回的 `projectUrl`，或自行拼接 `https://www.liblib.tv/canvas?projectId=` + `projectUuid`。查询进展时若传入 `--project-id PROJECT_UUID`，`query_session` 会直接返回 `projectUrl`，便于一并展示。

在任务完成时，同时给出：**视频/图片结果链接** + **项目画布链接（projectUrl）**。
过程中，不要给出 **项目画布链接（projectUrl）**。

## 核心原则：用户侧不做创作，只做传话

你（用户侧 Agent）的职责是**搬运工**，不是创作者。后端有专门的 Agent 负责理解需求、拆解分镜、编排工作流、选模型、写 prompt。你要做的只有三件事：

1. **上传**：用户给了本地文件 → `upload_file.py` 拿到 OSS URL
2. **传话**：把用户的原始描述 + OSS URL 原封不动发给 `create_session.py`
3. **取件**：轮询结果 → 下载到本地 → 展示给用户

**绝对不要做的事：**
- 不要替用户扩写、润色、翻译 prompt（用户说"帮我推演分镜"，就直接传"帮我推演分镜"，不要自己先写个分镜表再逐条发）
- 不要自行拆解任务步骤（如把"生成9张分镜图"拆成9次独立请求）
- 不要自行编排镜头描述、剧情推演、风格分析
- 不要在消息中添加自己编的 prompt（如"超写实风格，电影级光影，8K分辨率"之类的描述词）

后端 Agent 对模型能力、参数配置、prompt 工程远比用户侧更专业。用户侧越俎代庖只会降低生成质量，换个弱模型更是灾难。

**正确示例：**
```
用户说：「帮我推演后续的故事，来个分镜大爆炸，帮我出一个16:9的九宫格的图。新建一个任务。」
用户给了参考图：/path/to/ref.png

→ upload_file.py /path/to/ref.png  →  拿到 oss_url
→ create_session.py "把全部工作流和结果都放在画布上。帮我推演后续的故事，来个分镜大爆炸，帮我出一个16:9的九宫格的图。参考图：{oss_url}"
→ 轮询 → 下载 → 展示
```

**错误示例：**
```
❌ 用户侧自己先写了个九宫格分镜表（对峙、交锋、危机...）
❌ 然后把自己编的描述发给后端
❌ 或者拆成9次 create_session 分别发送
```

## 注意事项

- 鉴权方式为请求头 `Authorization: Bearer <LIBTV_ACCESS_KEY>`
- 创建会话时若不传 `message`，仅创建/绑定会话，不会调用 SendMessage
- 查询会话时可用 `--after-seq` 做增量拉取，便于轮询新消息（含 assistant 回复与生图/生视频结果）
- 项目画布地址固定为：`https://www.liblib.tv/canvas?projectId=` + projectUuid
- 切换项目后，Redis 缓存会更新，下次 create_session 将使用新的 projectUuid
- 上传文件仅支持图片（image/*）和视频（video/*）类型，其他类型会被拒绝，文件大小须在 200MB 以下
- 上传返回的 OSS 地址格式为 `https://libtv-res.liblib.art/claw/{projectUuid}/{uuid}{ext}`
- 生成过程中只告知用户"正在生成中"，不要提前给出 projectUrl；任务完成后再同时给出：**结果链接（图片/视频 URL）** + **项目画布链接（projectUrl）**

## Root-Cause Execution Contract

遇到失败时按以下链路追溯：

`Symptom -> Direct Cause -> Section Owner -> Source Contract -> Meta Rule Source`

| 症状 | 直接归因 | 修复路径 |
| --- | --- | --- |
| 调用技能时未加载 `CONTEXT.md` | 入口加载机制缺失 | 回到 `Context Loading Contract`，先补同目录 `CONTEXT.md`，再执行任务 |
| 没有把工作流和结果放到画布 | 新建会话消息缺少操作性指令 | 在首次提交或已有会话追加一次 `把全部工作流和结果都放在画布上。` |
| 用户 prompt 被本地扩写、润色或拆分 | 本地 Agent 越权主创 | 恢复用户原文，只追加必要的 OSS URL 和画布操作性指令 |
| 参考文件路径被直接发给 LibTV | 上传交接错误 | 先用 `upload_file.py` 获取 OSS URL，再把 OSS URL 附到用户原始描述后 |
| API 调用失败 | 凭证、网络或脚本层问题 | 检查 `LIBTV_ACCESS_KEY`、`OPENAPI_IM_BASE` / `IM_BASE_URL` 与对应脚本输出 |
| 完成后没有画布链接 | projectUuid/projectUrl 丢失 | 使用 `create_session` 返回的 `projectUrl`，或由 `projectUuid` 拼接固定画布地址 |

## Field Mapping

| field_id | owner | must contain | fail code |
| --- | --- | --- | --- |
| `FIELD-LIBTV-01` | `SKILL.md` | 触发范围、Context Loading Contract、输入合同、工作流、Root-Cause、输出合同 | `FAIL-ENTRY` |
| `FIELD-LIBTV-02` | `CONTEXT.md` | Type Map、Repair Playbook、Reusable Heuristics | `FAIL-CONTEXT` |
| `FIELD-LIBTV-03` | `scripts/` | 上传、创建会话、查询、下载、切换项目的机械执行桥 | `FAIL-SCRIPT` |
| `FIELD-LIBTV-04` | `projectUrl` / `projectUuid` | 画布地址和结果查看入口 | `FAIL-CANVAS` |

## Output Contract

- Required output：任务完成时给出本地下载文件列表、结果链接和项目画布链接；若任务仍在生成，说明仍在生成中，不提前泄露 projectUrl。
- Output format：简洁列出 `sessionId`、`projectUuid`、结果 URL、本地文件路径、`projectUrl` 与残余问题；不要整段粘贴原始 JSON，除非用户要求。
- Output path：下载结果默认进入语义化本地目录，例如 `~/Downloads/项目名` 或用户指定目录；技能文件固定在 `.agents/skills/cli/libTV/`。
- Naming convention：下载文件前缀按任务语义命名，如 `storyboard`、`character`、`video`、`libtv` 或用户指定前缀。
- Completion gate：已加载 `SKILL.md + CONTEXT.md`；需要上传的参考文件已转为 OSS URL；消息包含画布操作性指令；没有本地创作越权；完成时已展示结果链接和项目画布链接。
