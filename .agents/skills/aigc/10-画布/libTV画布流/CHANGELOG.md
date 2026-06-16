# Changelog

## 2026-06-16

- 增加 `Thought Pass Map` 审计兼容别名，明确 N1-N9、R1、R2 仍以 `Thinking-Action Node Map` 为可执行真源，避免全局 Skill 2.0 审计把新版节点表误判为缺少思考 pass。
- 按最新版 `skill-2.0` runtime-spine 规范升级 `libTV画布流` 主入口：补齐 `Runtime Spine Contract`、业务分析、类型路由、思行节点、量化口径、注意力协议、检查点、评估 prompts、模块授权、模块触发、收敛合同和 review gate。
- 将旧 `steps/canvas-control-workflow.md` 的 N1-N9 节点迁回 `SKILL.md#Thinking-Action Node Map` 和 Mermaid 图，移除 `steps/` 第二节点真源。
- 新增 `test-prompts.json`，覆盖完整画布控制、只回刷、只重建、顺序修复和多分镜参照模式。
- 同步 README、type map、scripts 边界和输出模板，明确脚本不得批量生成、批量插入、正则套句或映射投影 LibTV prompt / 视频节点正文，并补结构化执行报告证据要求。

## 2026-06-09

- 同步新版 LibTV 项目空间 / 画布分层口径：`projectSpaceId` / `folderId` 作为上层项目空间线索，`projectUuid` 作为具体画布 UUID。
- 调整默认命名：优先以 `项目名` 定位项目空间、以 `第N集` 命名具体画布；无法唯一定位项目空间时才退回旧兼容命名 `项目名-第N集`。
- 更新主合同、canvas control reference、workflow、type 包、review gate、输出模板和入口元数据，使证据同时记录 `projectSpaceId/folderId` 与 `projectUuid`。
- 明确 AIGC 本地层级映射：`projects/aigc/<项目名>` 对应 LibTV 项目空间名，`projects/aigc/<项目名>/第N集` 对应该项目空间下的画布语义范围；输入文件和证据目录继续使用阶段内标准路径。

## 2026-06-05

- 调整 LibTV 提交 prompt 的 YAML 主体行顺序：由 `图片N 主体名 UUID {{Image N}}` 改为 `图片N 主体名 {{Image N}} UUID`，并保留本地回刷 `图片N 主体名 UUID` 作为 UUID 匹配和顺序锁定格式。
- 完善同一画布内同一分镜组多批次与二次修改的视频节点命名规范：分离 `source_group_id` 与 `video_node_instance_id`，节点唯一名统一为 `vid__<source_group_id>__bNNN__rNN__vNNN`。
- 更新执行合同、审查门禁、输出模板和 registry 结构，要求重生成已存在分镜组时默认新增实例，不得覆盖旧节点，也不得因 `source_group_id` 已存在而跳过。

## 2026-06-01

- 新建 `libTV画布流` Skill 2.0 包。
- 固化当前上下文验证出的最佳实践：本地 YAML 先显式 `图片N 主体名 UUID`，视频节点按该顺序逐张 `--left-add`，并同步写入 `imageList/mixedList/imageListOrder/mixedListOrder`。
- 默认视频规格调整为 `16:9 / 720p / star-video2 / mixed2video`，用户显式指定时覆盖对应默认值。
