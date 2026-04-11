# Context: grok

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: auto
current_lines: auto
current_cases: auto
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-03T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `grok` 技能的经验层，默认以知识库模式维护：优先沉淀 GROK 生视频的双接口提交合同、图片读取与编码策略、响应字段归一化，以及提交报告落盘的稳定套路。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-GROK-MODE-DRIFT` | 文本 PRP 与截图示例接口不一致，导致调用时纠结到底该走哪个端点 | 接口契约层 | 保持 `json` 与 `multipart` 双模式共存，并把 `auto` 默认收敛到 `json` | 在 `references/api.md` 中显式记录“文字版 vs 截图版”证据来源，避免后续误删一支 | `--dry-run` 输出里可见 `request_mode` 与 `endpoint` |
| `TM-GROK-IMAGE-READ` | 本地图、远程图、data URL 三种输入不能统一消费 | 输入标准化层 | 统一把所有图片读成 `bytes + mime_type`，再根据模式转 `data URL` 或 multipart 文件 | 脚本内固定保留 `_read_image_source()` 与 `_to_data_url()` 两段逻辑 | 三类输入都能通过 `--dry-run` |
| `TM-GROK-MULTIPART-SINGLE` | multipart 模式下传多图后请求失败或行为不可预测 | 接口边界层 | 显式拒绝多图 multipart | 在 `SKILL.md` 与脚本参数校验中双重硬卡 | `--request-mode multipart --image a --image b` 直接报错 |
| `TM-GROK-RESPONSE-DRIFT` | 有时返回 `task_id`，有时返回 `id`，导致上游拿不到任务号 | 响应解析层 | 使用 `task_id or id` 归一化 | 报告 JSON 固定输出 `normalized_submission.task_id` | 报告里始终可见 `task_id` |
| `TM-GROK-SUBMIT-ONLY` | 用户以为技能能下载最终视频，但 PRP 并未提供查询/下载端点 | 需求边界层 | 在技能合同中明确当前只保证提交回执，不承诺 MP4 下载 | 若未来补到查询接口，再升级技能而不是先在文档里虚构能力 | `SKILL.md` 未出现未证实的下载流程 |
| `TM-GROK-DRYRUN-AUTH` | `--dry-run` 时仍被 API Key 校验拦住，无法完成本地预检 | 脚本执行顺序层 | 把 API Key 校验后移到真实提交前 | 保持 dry-run 只验证输入、模式裁决与请求摘要，不依赖外部密钥 | 无 API Key 时 `--dry-run --print-payload` 仍返回 0 |
| `TM-GROK-UPSTREAM-HANDSHAKE` | 真实提交时出现 `SSL EOF`、`RemoteDisconnected` 或 `Empty reply from server`，请求尚未进入业务响应层 | 外部依赖/网关层 | 先用 `curl -Ivs https://api.ai666.net` 与 `curl -Ivs http://api.ai666.net` 复验连通性，确认是上游端点问题 | 在脚本里把 SSL/连接中断错误归一化成“上游端点不可用”提示，避免误修 payload | `curl` 与真实提交都在握手/首包阶段断开时，不再继续调整业务参数 |
| `TM-GROK-SECRET-HYGIENE` | API Key 被误写进技能文件或报告 | 安全层 | 所有技能文件只引用环境变量名，不写明文密钥 | 在脚本报告里默认不回写完整 Authorization 头 | 仓内 grep 不出现实际密钥 |

## Repair Playbook

1. **先判定模式**
   - 如果任务涉及多图或“读图即转 data URL”，先走 `json`
   - 只有用户强制要求 OpenAPI 文字版接口时才走 `multipart`
2. **先跑 Dry Run**
   - `python3 .agents/skills/api/video/grok/scripts/grok_video_generate.py --prompt "test" --dry-run --print-payload`
   - 确认 `request_mode / endpoint / image_inputs / request_summary`
3. **图片输入排查**
   - 本地图：检查路径是否存在
   - 远程图：检查 URL 是否可访问
   - data URL：检查是否以 `data:image/` 开头
4. **回执排查**
   - 若返回只有 `id` 没有 `task_id`，检查归一化逻辑
   - 若状态为 `failed`，保留原始响应，不做静默吞错
5. **输出排查**
   - 检查默认目录是否为 `output/影片/[项目名]/5-API/video/grok/`
   - 检查报告中是否包含 `normalized_submission`

## Reusable Heuristics

- 同一 PRP 同时存在“文字 OpenAPI”和“截图示例”时，不应强行二选一，而应把它们收敛成主路径与回退路径。
- 涉及“图片读取”的视频接口，最稳的抽象不是“URL 还是文件”，而是统一转成“字节 + MIME”，后面再适配 JSON 或 multipart。
- 当服务端响应字段有轻微漂移时，优先做归一化层，不要把漂移直接暴露给上游技能。
- 如果文档只给了提交接口，没有给查询/下载接口，就把技能边界锁在“提交回执”，这样最诚实也最不容易误导下游。
- 默认报告里只保留请求摘要，不落完整鉴权头，能显著降低技能文件和产物的泄密风险。
- 如果 `https` 与 `http` 都在握手或首包阶段断开，应优先判定为网关/上游不可用，而不是继续修改 prompt、比例、时长等业务参数。

## Case Log

### [CASE-20260403-GROK-INIT] 基于空目录初始化 GROK 生视频技能

- milestone_type: new_success_class
- outcome: 从空目录创建完成 `grok` 技能包，补齐 `SKILL.md`、`CONTEXT.md`、`references/api.md`、`scripts/grok_video_generate.py`、`requirements.txt` 与 `agents/openai.yaml`。
- root_cause_or_design_decision: 目标目录仅存在空壳，`quick_validate` 基线直接报 `SKILL.md not found`；同时 `PRPs/grok.md` 的文字接口与截图接口存在分歧，必须在技能层统一合同。
- final_fix_or_heuristic: 采用“`auto` 默认走 JSON，多图/图片读取友好；保留 multipart 为显式回退”的双接口策略，并在脚本中统一图片读取和响应字段归一化。
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 包含完整三表与 Root-Cause 契约
  - [x] `CONTEXT.md` 建立 Type Map / Playbook / Heuristics 基线
  - [x] 脚本支持本地图 / 远程图 / data URL
  - [x] 报告 JSON 固定输出 `normalized_submission.task_id`
  - [x] 技能文件不写入明文 API Key
- evidence_paths:
  - `.agents/skills/api/video/grok/SKILL.md`
  - `.agents/skills/api/video/grok/CONTEXT.md`
  - `.agents/skills/api/video/grok/references/api.md`
  - `.agents/skills/api/video/grok/scripts/grok_video_generate.py`
  - `.agents/skills/api/video/grok/agents/openai.yaml`
- user_feedback_or_constraint: 基于 `PRPs/grok.md`，包含图片读取能力，把 `.agents/skills/api/video/grok` 完善为 GROK 生视频技能包。

### [CASE-20260403-GROK-DRYRUN] dry-run 预检被错误地要求 API Key

- milestone_type: source_contract_change
- outcome: 修复了 `--dry-run` 仍前置要求 API Key 的脚本顺序错误，本地验证可在无密钥条件下完成。
- root_cause_or_design_decision: API Key 校验发生在 dry-run 分支之前，导致本该只验证请求构造的本地预检也依赖外部密钥。
- final_fix_or_heuristic: 把 API Key 校验后移到真实提交前；dry-run 只负责输入校验、模式裁决、图片读取与请求摘要生成。
- prevention_or_replication_checklist:
  - [x] 无 API Key 时 `--dry-run --print-payload` 仍可执行
  - [x] 非 dry-run 仍保持严格的密钥校验
  - [x] Type Map 新增 `TM-GROK-DRYRUN-AUTH`
- evidence_paths:
  - `.agents/skills/api/video/grok/scripts/grok_video_generate.py`
  - `.agents/skills/api/video/grok/CONTEXT.md`
- user_feedback_or_constraint: 本轮验证需优先支持本地 dry-run，不额外消耗或依赖真实 API 调用。

### [CASE-20260403-GROK-UPSTREAM] 真实随机提交被上游端点在握手阶段断开

- milestone_type: new_failure_class
- outcome: 完成一次真实随机视频提交测试，但 `https://api.ai666.net` 在 TLS 握手阶段 `SSL EOF`，`http://api.ai666.net` 也返回空回复，未进入业务响应层。
- root_cause_or_design_decision: 直接技术原因是上游端点/网关不可用或配置异常；规则源层风险在于脚本此前只原样抛异常，容易让执行者误以为是 payload 或参数问题。
- final_fix_or_heuristic: 在脚本中增加 SSL/连接中断错误归一化提示，并在 `SKILL.md` 与 Type Map 中明确“先做端点连通性复验，再决定是否调整业务参数”的排障顺序。
- prevention_or_replication_checklist:
  - [x] 真实提交失败时报告中写出端点级错误解释
  - [x] Type Map 新增 `TM-GROK-UPSTREAM-HANDSHAKE`
  - [x] `SKILL.md` 失败排查新增 `SSL EOF / Empty reply` 分支
- evidence_paths:
  - `.agents/skills/api/video/grok/scripts/grok_video_generate.py`
  - `.agents/skills/api/video/grok/SKILL.md`
  - `.agents/skills/api/video/grok/CONTEXT.md`
  - `output/影片/随机测试/5-API/video/grok/grok_video_20260403_013053.json`
  - `output/影片/随机测试/5-API/video/grok/grok_video_20260403_013107.json`
- user_feedback_or_constraint: 用户要求“API KEY 添加到 .env 中并引用，随机视频生成测试”，因此需要真实提交而不是仅 dry-run。
