# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `dreamina-cli` 技能的经验知识库，不是执行流水账。
- 每次调用本技能时，先加载本文件，用于选择更稳的登录、提交、查询与排障路径。
- 冲突优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok
- action_policy:
  - ok: 优先更新 Type Map / Repair Playbook / Reusable Heuristics
  - warn: 对当前技能上下文做定向压缩
  - critical: 先归档旧案例，再继续大规模追加

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `TM-DRM-PATH` | 安装与环境层 | 重新执行安装命令并确认 `dreamina --help` 可调用 | 把“先验 binary 可用性”固定为所有工作流第一步 | `dreamina --help` 成功输出 |
| `TM-DRM-AUTH-STALE` | 登录态层 | 重新运行 `dreamina login` / `dreamina relogin` / `dreamina import_login_response` | 固化“任何生成前必须跑 `dreamina user_credit`” | `dreamina user_credit` 返回 JSON |
| `TM-DRM-CALLBACK-STUCK` | 登录流程层 | 使用 `dreamina login --debug` 重试，必要时改走 manual import | 在技能中显式给出 browser / headless / debug / import 四分流 | 登录成功后 `user_credit` 正常 |
| `TM-DRM-POLL-TIMEOUT` | 异步任务层 | 保留 `submit_id`，改用 `dreamina query_result --submit_id=...` | 把 `--poll` 视为短等待，不把它当作“必定出结果”的承诺 | `query_result` 能返回结果或下载文件 |
| `TM-DRM-LOCAL-INPUT` | 本地输入层 | 先检查上传图片路径是否存在，再提交 `image2image` / `image2video` | 把“本地路径预检”固定为图像输入命令前置步骤 | `test -f <path>` 成功 |
| `TM-DRM-DIAG-ORDER` | 排障流程层 | 按 `config.toml -> credential.json -> tasks.db -> logs/` 顺序检查 | 在技能中固定本地文件排障顺序，避免随意翻找 | 能定位到配置、凭证或任务记录异常 |
| `TM-DRM-QUEUE-MISSING` | 任务编排层 | 立刻创建 queue ledger，并从 `submit_id`、`list_task`、`query_result` 回填活动行 | 把“pending job 必须入清单”提升为技能硬规则 | 活跃任务都有 queue row，且可继续跟进 |
| `TM-DRM-QUEUE-DRIFT` | 人工更新层 | 对照 `query_result` / `list_task` / `tasks.db` 校正 `remote_status`、`last_checked_at`、`next_action` | 不再把聊天记录或终端滚屏当作唯一状态来源 | queue ledger 与 CLI 查询结果一致 |
| `TM-DRM-OUTPUT-PATH-DRIFT` | 输出路径层 | 先判断当前调用是 standalone Dreamina 还是 AIGC2026 downstream，再把下载物和 queue ledger 挪回正确根目录 | 把“standalone 默认走 output/dreamina，而 AIGC2026 下游继承调用方 stage path”写成显式规则 | 下载物与 queue ledger 都命中当前合同路径 |
| `TM-DRM-MULTIMODAL-ROUTE` | 命令路由层 | 当任务需要多张参照图或 `@图N` 顺序绑定时，优先改走 `multimodal2video` 而不是 `image2video` | 在技能合同中显式纳入 `multimodal2video` / `multiframe2video`，并区分“多参照编辑”与“多帧叙事”两种场景 | 命令类型与任务的参照结构一致 |
| `TM-DRM-VIDEO-MODEL-MISMATCH` | 子命令能力层 | 先用 `dreamina <subcommand> -h` 确认当前子命令暴露的 `model_version`，再选命令；若用户指定 `3.5pro`，优先走 `image2video` | 在技能正文和官方摘录中固化“视频子命令 != 共享同一模型集合”的矩阵 | 所选子命令的 `-h` 输出包含目标 `model_version` |
| `TM-DRM-FRAMES2VIDEO-MIXED-UPLOAD` | 双图上传层 | 若 `frames2video` 在首尾帧混合上传时只失败其中一张，先做最小复现实验，再重试或对失败图做保守重编码 | 把“单图上传成功 != 双图上传必稳”记录进 Dreamina CLI 执行经验，遇到 mixed upload fail 时先区分单图问题与双图配对问题 | 同图双传成功、混合双传重试成功或经重编码后成功 |
| `TM-DRM-DOWNLOAD-TIMEOUT` | 下载层 | 若 `query_result --download_dir=...` 在远端已成功后超时，先判定为下载故障，删除半截本地文件后重试；如仍超时，再改用 `query_result` 暴露的媒体直链完成下载 | 把“生成成功”和“下载成功”拆成两个独立检查点，并把“半截文件必须清理后重试”写成固定动作 | 本地输出文件可被 `ffprobe` / 图片读取正常验证，且 queue ledger 标记为 `downloaded` |

## Repair Playbook

1. 先确认 CLI 可用：运行 `dreamina --help`。
2. 再确认登录态：运行 `dreamina user_credit`。
3. 如果登录失败：
   - 优先选对登录路径：browser / headless / debug / import
   - 再检查 `~/.dreamina_cli/config.toml`
   - 再检查 `~/.dreamina_cli/credential.json`
4. 如果提交任务后没拿到最终结果：
   - 检查是否设置了 `--poll`
   - 保留 `submit_id`
   - 用 `dreamina query_result --submit_id=...`
   - 如果仍在排队或处理中，马上写入 / 更新 queue ledger
   - 立刻确认下载目标根目录：standalone 用 `output/dreamina/<项目名>/<模型名称>/`，AIGC2026 下游调用则继承该技能自己的 stage path
   - 如果是 `frames2video`，且只在首尾帧其中一张上传时报错，补做“同图双传”最小复现实验，确认是不是 mixed upload 特有故障
   - 如果远端已 `success` 但 `--download_dir` 超时，先删掉半截文件再重试下载；连续超时再切媒体直链下载
5. 如果是图像输入型命令失败：
   - 先验证本地图片路径
   - 再核对命令必填参数
   - 如果 `image2image` 能上传、但 `frames2video` 的混合双图上传失败，优先重试一次；必要时对失败图做保守重编码（普通 RGB PNG）再提交
6. 如果问题仍未收敛：
   - 查 `~/.dreamina_cli/tasks.db`
   - 查 `~/.dreamina_cli/logs/`

## Reusable Heuristics

- `dreamina user_credit` 是最便宜也最可靠的登录自检，不要直接用生成命令代替它。
- `--poll` 适合“先短等一下”，不适合被当成完整任务编排；真正稳定的异步闭环仍然是 `submit_id + query_result`。
- 只要任务会跨过当前会话，`submit_id` 就应该立刻进入 queue ledger；否则最容易发生“任务还在排队，但人已经忘了”的漂移。
- `list_task` 和 `tasks.db` 适合做证据校对，不适合代替人工清单；当前批次真正可操作的仍应是一份手动动态更新的 ledger。
- standalone Dreamina 的默认根目录应该稳定收束到 `output/dreamina/<项目名>/`，不要把队列文件散落到 `reports/` 或下载结果散落到 `./downloads/`。
- 如果 Dreamina 只是 `aigc2026` 链路里的生成运输层，输出路径所有权仍属于调用它的 stage skill，Dreamina 不应强行改写到自己的 standalone 路径。
- 需要多张参考图同时约束同一条视频时，优先选 `multimodal2video`；`image2video` 只适合单首帧驱动。
- `multiframe2video` 适合“多帧故事过渡”，不是“多参考图锁定身份/场景”的通用替代品。
- 视频子命令的模型面不是共享的：`text2video` 和 `multimodal2video` 当前只暴露 `seedance2.0 / seedance2.0fast`，`3.5pro` 这类模型要走 `image2video`。
- 判断旧模型是否还能用时，不要凭历史印象；先看当前 `dreamina <subcommand> -h`，因为同一 CLI build 下不同视频子命令的 `model_version` 集合并不相同。
- `frames2video` 的 mixed upload 失败要和“图片本身不可上传”分开看：单图上传成功、同图双传成功，通常说明问题更接近双图配对上传的偶发故障，而不是路径或文件彻底坏掉。
- `query_result` 里远端 `success` 不等于本地下载也完成；下载超时后留下的半截 MP4/PNG 必须先删，再重试，否则最容易把截断文件误判成正式产物。
- 登录路径应该四分流：浏览器正常就 `login`，远程/agent 环境优先 `--headless`，卡回调用 `--debug`，跨机登录则走 `import_login_response`。
- Dreamina 的本地状态文件足够关键，排障时不要跳过 `config.toml` 和 `credential.json`。
- 对于 `image2image` 和 `image2video`，最常见的低级失败不是 API，而是本地路径写错。

## Case Log

### Case-20260401-dreamina-cli-init

- milestone_type: new_success_class
- outcome: 从零创建仓库内 Dreamina CLI 技能，补齐安装、登录、自检、提交、异步查询与排障合同
- root_cause_or_design_decision: 仓库内原本没有 Dreamina CLI 技能，未来 agent 容易只记住安装/登录，而遗漏 `user_credit` 自检、`submit_id` 异步闭环和本地状态文件排障顺序
- final_fix_or_extracted_heuristic: 把高频执行顺序收束进 `SKILL.md`，把长文档和 FAQ 下沉到 `references/official-doc.md`，把排障顺序与可复用经验沉淀到 `CONTEXT.md`
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 明确要求生成前执行 `dreamina user_credit`
  - [x] `SKILL.md` 明确 `--poll` 与 `query_result` 的分工
  - [x] `SKILL.md` 包含 browser / headless / debug / import 登录分流
  - [x] `CONTEXT.md` 建立 Type Map / Repair Playbook / Heuristics 基线
  - [x] `references/official-doc.md` 保存官方资料浓缩稿，避免主技能过长
- evidence_paths:
  - `.agents/skills/cli/dreamina-cli/SKILL.md`
  - `.agents/skills/cli/dreamina-cli/CONTEXT.md`
  - `.agents/skills/cli/dreamina-cli/references/official-doc.md`
- user_feedback_or_constraint: 以官方 Dreamina CLI 文档为主，保存到 `.agents/skills/cli/dreamina-cli`，便于后续 agent 快速调用

### Case-20260401-dreamina-cli-queue-ledger

- milestone_type: source_contract_change
- outcome: 为 Dreamina CLI 技能补齐排队管理合同，把 pending 视频/图片任务从“submit_id 记忆点”提升为“手动动态更新的清单对象”
- root_cause_or_design_decision: 原技能已经覆盖提交、轮询、查询与排障，但缺少“跨会话、跨批次管理 pending 任务”的显式机制，容易在视频生成场景里出现队列漂移和人工漏跟
- final_fix_or_extracted_heuristic: 在 `SKILL.md` 新增 queue workflow、最小 queue record、手动动态更新规则和对应 fail code；新增 `templates/task-queue.template.md` 作为实际清单载体；在 `CONTEXT.md` 补充 queue missing / queue drift 两类经验模式
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 把 queue ledger 升级为异步/批量任务硬步骤
  - [x] `SKILL.md` 补充 `FIELD-DRM-07/08`
  - [x] 新增可直接复用的 markdown queue template
  - [x] `CONTEXT.md` 沉淀 queue missing / drift 的 type map 和 heuristics
- evidence_paths:
  - `.agents/skills/cli/dreamina-cli/SKILL.md`
  - `.agents/skills/cli/dreamina-cli/CONTEXT.md`
  - `.agents/skills/cli/dreamina-cli/templates/task-queue.template.md`
- user_feedback_or_constraint: 用户明确要求考虑排队管理，并支持“专门记录排队中的视频或其他、清单式、手动动态更新”

### Case-20260401-dreamina-cli-output-path-governance

- milestone_type: source_contract_change
- outcome: 为 Dreamina CLI 技能补齐 standalone 与 AIGC2026 downstream 两套输出路径归属规则，避免下载物和排队文件乱落目录
- root_cause_or_design_decision: 先前 queue 增强只定义了“要有清单”，但默认路径仍偏泛化，容易把 standalone 任务和 AIGC2026 下游任务混写到不同根目录
- final_fix_or_extracted_heuristic: 在 `SKILL.md` 明确 standalone 默认用 `output/dreamina/<项目名>/` 与 `output/dreamina/<项目名>/<模型名称>/`，同时新增 AIGC2026 downstream override；在模板示例和经验库中同步这套路径所有权规则
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 补充默认下载路径与 queue 路径
  - [x] `SKILL.md` 补充 `FIELD-DRM-09`
  - [x] queue template 示例路径改为 `output/dreamina/...`
  - [x] `CONTEXT.md` 补充 `TM-DRM-OUTPUT-PATH-DRIFT`
- evidence_paths:
  - `.agents/skills/cli/dreamina-cli/SKILL.md`
  - `.agents/skills/cli/dreamina-cli/CONTEXT.md`
  - `.agents/skills/cli/dreamina-cli/templates/task-queue.template.md`
- user_feedback_or_constraint: 用户要求素材下载默认输出到 `output/dreamina/[项目名]/[模型名称]/`，排队相关文件落到 `output/dreamina/[项目名]/`，且作为 `aigc2026` 下游调用时遵循 AIGC2026 输出规则

### Case-20260401-dreamina-cli-frames2video-mixed-upload

- milestone_type: new_failure_class
- outcome: `frames2video` 在双图混合上传时，首帧图报 `upload phase, no file upload`，但同一张图单独跑 `image2image` 可上传、同图双传的 `frames2video` 也可提交
- root_cause_or_design_decision: 故障不符合“路径不存在/图片彻底损坏”的模式，更像 `frames2video` 的 mixed upload 配对上传链路存在偶发不稳定；仅看首条报错容易误判成文件本身坏掉
- final_fix_or_extracted_heuristic: 把 mixed upload 与 single upload 分开诊断，先做最小复现实验；若单图上传和同图双传都正常，再优先重试或对失败图保守重编码，而不是马上改 prompt 或放弃整批任务
- prevention_or_replication_checklist:
  - [x] `CONTEXT.md` 新增 `TM-DRM-FRAMES2VIDEO-MIXED-UPLOAD`
  - [x] `Repair Playbook` 补充同图双传最小复现实验
  - [x] `Reusable Heuristics` 记录 mixed upload 与文件损坏的区分法
- evidence_paths:
  - `output/dreamina/榆仙特别版/20260401-35pro-首尾帧测试-dreamina-queue.md`
  - `output/dreamina/榆仙特别版/3.5pro/22f14c550203f4bb_last_frame.png`
  - `~/.dreamina_cli/logs/2026-04-01/21.log`
- user_feedback_or_constraint: 用户要求以上一段尾帧作为下一段首帧继续链式测试

### Case-20260401-dreamina-cli-download-timeout-after-success

- milestone_type: source_contract_change
- outcome: `frames2video` 任务远端已成功，但 `dreamina query_result --download_dir=...` 在下载 MP4 时客户端读超时，并在本地留下半截视频文件
- root_cause_or_design_decision: 现有技能已覆盖“生成超时后改查 `query_result`”，但未显式区分“生成成功”与“下载成功”两层状态，也未要求在下载超时后清理 partial file 再重试
- final_fix_or_extracted_heuristic: 在 `SKILL.md` 增加 download-timeout 处置规则和 `FIELD-DRM-10`，在 `CONTEXT.md` 补充 `TM-DRM-DOWNLOAD-TIMEOUT`，固定成“删半截文件 -> 重试 `query_result --download_dir` -> 必要时切媒体直链”的处理链
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 明确 `--download_dir` 超时属于下载层，不等于生成失败
  - [x] `SKILL.md` 明确 partial file 必须删除后再重试
  - [x] `SKILL.md` 新增 `FIELD-DRM-10`
  - [x] `CONTEXT.md` 新增 `TM-DRM-DOWNLOAD-TIMEOUT`
- evidence_paths:
  - `.agents/skills/cli/dreamina-cli/SKILL.md`
  - `.agents/skills/cli/dreamina-cli/CONTEXT.md`
  - `output/dreamina/榆仙特别版/3.5pro/cd6089f26a52c617_video_1.mp4`
  - `output/dreamina/榆仙特别版/20260401-35pro-首尾帧测试-dreamina-queue.md`
- user_feedback_or_constraint: 用户要求沿上一段首尾帧视频继续下一组，执行链不能因为下载层偶发超时而中断

### Case-20260402-dreamina-cli-multimodal-route

- milestone_type: source_contract_change
- outcome: 将 `multimodal2video` 与 `multiframe2video` 正式补入 Dreamina CLI 技能合同，用于承接 `5-视频/视频生成/seedance2.0` 的多参照图视频生成
- root_cause_or_design_decision: 本机 Dreamina CLI 已支持 `multimodal2video` / `multiframe2video`，但技能正文还停留在 `text2video / image2video / frames2video`，导致下游需要 `@图N` 多参照绑定时没有正式 transport 规则可依
- final_fix_or_extracted_heuristic: 在 `SKILL.md` 的 command map、submission patterns 与 non-obvious constraints 中补齐两条命令；在经验层明确区分“多参照编辑”与“多帧叙事过渡”是两类不同任务
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 已纳入 `multimodal2video`
  - [x] `SKILL.md` 已纳入 `multiframe2video`
  - [x] `CONTEXT.md` 新增路由类型映射
  - [x] 对 `@图N` 多参照任务给出优先命令选择
- evidence_paths:
  - `.agents/skills/cli/dreamina-cli/SKILL.md`
  - `.agents/skills/cli/dreamina-cli/CONTEXT.md`
- user_feedback_or_constraint: 用户要求下游视频生成阶段能消费 `seedance2.0 / 分镜参照` 文件里的参照图，并以 Dreamina 的 Seedance 2.0 系列正式生成视频

### Case-20260403-dreamina-cli-video-model-matrix

- milestone_type: source_contract_change
- outcome: 把当前官方 CLI 的视频子命令 `model_version` 暴露范围补成显式矩阵，并同步修正技能正文里容易引起混淆的旧口径
- root_cause_or_design_decision: 本机官方 CLI 已清楚表现出“不同视频子命令支持的模型集合不同”，但技能正文和参考摘录此前没有把差异显式矩阵化，容易让后续执行误以为 `3.5pro`、`seedance2.0`、旧 Seedance 模型在所有视频命令上都通用
- final_fix_or_extracted_heuristic: 在 `SKILL.md` 新增 `Current Video Model Matrix`，在 `official-doc.md` 增加视频模型速查表，并在经验层固定“先看当前子命令 `-h`，再选 transport”的路由规则
- prevention_or_replication_checklist:
  - [x] `SKILL.md` 新增视频模型矩阵
  - [x] `SKILL.md` 去掉旧的 `frames2video` 口径
  - [x] `references/official-doc.md` 新增视频模型速查表
  - [x] `CONTEXT.md` 新增 `TM-DRM-VIDEO-MODEL-MISMATCH`
- evidence_paths:
  - `.agents/skills/cli/dreamina-cli/SKILL.md`
  - `.agents/skills/cli/dreamina-cli/references/official-doc.md`
  - `.agents/skills/cli/dreamina-cli/CONTEXT.md`
- user_feedback_or_constraint: 用户明确要求把当前官方 CLI 显示的 `text2video / multimodal2video / image2video / multiframe2video` 模型支持情况整合到 `dreamina-cli` 技能目录中
