# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `dreamina-cli` 技能的经验知识库，不是执行流水账。
- 每次调用本技能时，先加载本文件，用于选择更稳的登录、提交、查询与排障路径。
- 冲突优先级遵循：用户显式请求 > `AGENTS.md` / 元规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
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
