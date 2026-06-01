# Storyboard Reference Flow

分镜参照流当前为空白占位，待补充。

## Placeholder Scope

未来应定义：

- 基本输入对象：故事板图、分镜图或 `7-图像/B-分镜故事板` 工件。
- 图像参照绑定表：故事板图与分镜组 ID 的关系。
- LibTV Agent IM 提交文本和 source_node 映射。
- 时长、分辨率、比例、画布沉淀和下载策略。
- review gate 与输出目录。

## Current Behavior

若用户显式选择本流，必须返回 `not_implemented_placeholder`，不得提交生成任务。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 用户未显式指定“分镜参照流 / storyboard reference flow”时，是否没有进入本占位路线？ | `REV-LIBTVCANVAS-01` | `FAIL-ROUTE` | `N1 Intake` | route note、selected flow、用户原始指令摘录 |
| 用户显式选择分镜参照流时，是否返回 `not_implemented_placeholder`，而不是伪造提交计划或生成任务？ | `REV-LIBTVCANVAS-01` | `FAIL-ROUTE` | `N1 Intake` | `PLACEHOLDER` verdict、blocked queue/report、未调用 create_session 的命令证据 |
| 占位响应是否说明未来最小输入对象：故事板图、分镜图或 `7-图像/B-分镜故事板` 工件？ | `REV-LIBTVCANVAS-01` | `FAIL-ROUTE` | `references/storyboard-reference-flow.md` | placeholder report 中的 missing input list |
| 占位响应是否没有借主体参照流规则临时推断 storyboard 图像绑定、source_node 映射或远端 prompt？ | `REV-LIBTVCANVAS-09` | `FAIL-SOURCE-FIDELITY` | `N1 Intake` / `references/storyboard-reference-flow.md` | 无 manifest/submit plan 伪生成证据、报告中的 not-owned truth 声明 |
| 分镜参照流是否没有调用 LibTV 远端生成、上传、下载或写入正式 queue record 成功状态？ | `REV-LIBTVCANVAS-07` | `FAIL-OFFICIAL-HANDOFF` | `N5 LibTV Handoff` | command log 为空或 blocked、queue/report 状态为 `not_implemented_placeholder` |
| 后续实现本流前，是否把 review gate、输出目录、source_node 映射和证据链作为待补 owner，而不是在本文件中声明已完成？ | `REV-LIBTVCANVAS-18` | `FAIL-QUEUE-EVIDENCE` | `references/storyboard-reference-flow.md` / `review/review-contract.md` | placeholder owner list、未实现项清单、无 PASS verdict |
