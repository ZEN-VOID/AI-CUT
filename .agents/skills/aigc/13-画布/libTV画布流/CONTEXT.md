# Context: libTV画布流

本文件是 `libTV画布流` 的经验层。它不重定义 `SKILL.md`、`references/` 或 LibTV CLI 命令真源。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 16000
hard_limit_chars: 32000
status: ok
```

## Type Map

| type_id | symptom | likely cause | immediate fix | verification |
| --- | --- | --- | --- | --- |
| `LTVCTRL-TM-01` | YAML 已有 UUID 但视频主体错绑 | 把 `{{Image N}}` 当作 YAML 顺序，而远端 `imageList` 顺序不同 | 本地先写 `图片N 主体名 UUID`，提交 prompt 时重排为 `图片N 主体名 {{Image N}} UUID`，再直接写 `imageList/mixedList` 为同顺序 | 查询节点 `data.params.imageList[]` |
| `LTVCTRL-TM-02` | 逐张 `--left-add` 后顺序仍不变 | LibTV 入边变更未重算 `params.imageList` | 连线后再次写入 `imageList/mixedList/imageListOrder/mixedListOrder` | final query 顺序等于 YAML |
| `LTVCTRL-TM-03` | 道具和场景复用同一图片 | 同一 UUID 出现在多条主体行 | 同组内相同 UUID 复用同一个 `图片N` | YAML 和 runtime map 都只占一个图位 |
| `LTVCTRL-TM-04` | 同一项目空间下画布重名 | 只按 `项目名-第N集` 查重，未区分 `projectSpaceId/folderId` 和画布名 | 先锁定 `projectSpaceId/folderId`，默认画布名用 `第N集`，冲突追加 `V2`、`V3`；无法锁定项目空间时才退回旧兼容命名 | project list 中 `uuid` 不重复，目标条目的 `projectSpaceId/folderId` 与报告一致 |
| `LTVCTRL-TM-05` | prompt 出现绑定表、命令或诊断 | handoff 文案进入视频 prompt | 重写 prompt，只保留分镜组正文 + fenced YAML | 远端 prompt hygiene pass |
| `LTVCTRL-TM-06` | 远端 prompt 看似不同但只替换 `group_id`、主体名或 `{{Image N}}` | scripted prompt projection | 标记 `FAIL-LTVCTRL-SCRIPTED-PROMPT`，恢复直接使用完整分镜组正文 + fenced YAML | final query prompt 可回指完整组正文，而不是模板句 |
| `LTVCTRL-TM-07` | 用户要求重生成已存在分镜组，执行器却跳过或覆盖旧节点 | 把分镜组 ID 当作视频节点唯一键 | 为同一 `source_group_id` 创建新的 `video_node_instance_id`，默认递增 `batch_no`；二修递增 `revision_no` 并记录父实例 | registry 中同一 source_group_id 有多个 instances，旧节点仍可查询 |
| `LTVCTRL-TM-08` | `libtv node --left-add` 对已经存在的入边长时间无返回 | 对同一视频节点重复追加同一 image edge | 不对已存在边重复执行 `--left-add`；创建时一次性带有序入边，随后直接重写 `imageList/mixedList` 并以 final query 为准 | final query 的 `data.params.imageList[]` 等于 YAML 顺序 |
| `LTVCTRL-TM-09` | 创建视频节点报 `图片最多 9 个` | 单组绑定图片超过 LibTV 当前视频节点输入上限 | 前置裁剪到 9 张：优先保留用户强指定的多维主角参照、所有关键角色和场景，再在容量内保留道具；被裁掉主体回写为未绑定文本并记录 skip reason | create 成功且 manifest/queue 记录被裁剪主体 |
| `LTVCTRL-TM-10` | 单组 YAML 修复后相邻分组标题消失或 prompt 夹带下一组正文 | 用局部 fragment 的 offset 回写全局 markdown，替换范围跨过 fence 边界 | 只用全局 regex span 或结构化 markdown block 边界替换；回写后立即校验 `^##` 分组数、每组 fenced YAML 可解析、目标 prompt 不含相邻 `group_id` | source group count 与原始计划一致，目标 final prompt 不含相邻分组标题 |
| `LTVCTRL-TM-11` | 视频规格时长是整数秒或非 `.5` 结尾 | 规格时长未做半秒尾帧缓冲 | 对视频规格中的非 `.5` 结尾 duration 额外 `+0.5s`；同步 queue record、submit plan 和 summary/report，远端存在同名节点时同步远端 settings.duration | 本地 queue duration 全部 `.5` 结尾，远端 final query duration 无剩余异常 |
| `LTVCTRL-TM-12` | 用户觉得画布节点数多于分组稿 | 目标画布执行前已有旧 video 节点，且本轮未获删除授权所以保留 | 预检时区分 `current_batch_video_nodes`、`legacy_video_nodes` 和 `reference_image_nodes`；最终汇报必须说明旧节点数量和名称前缀，避免误读为本轮多建 | remote node list 中本轮节点数等于分组数，legacy 节点单独列示 |

## Repair Playbook

1. 先确认本轮是 `full_canvas_control`、`backfill_only`、`node_rebuild_only` 还是 `repair_order`。
2. 对已有视频节点错序，优先删除重建；若不能删除，则清边、逐张连线、再直接重写 `imageList/mixedList`。
3. 所有 `{{Image N}}` 都必须来自本地 YAML `图片N` 和 final remote query 的双重一致性，不来自上传顺序、画布布局或 CLI 参数顺序。
4. 缺图主体跳过回刷，不写负面占位，不把相邻主体图拿来代替。
5. 每次执行后更新 `queue-record.json`，状态必须区分 `created_not_run`、`run_executed`、`blocked`。
6. prompt hygiene 不只查污染词，也要查伪差异；如果多节点 prompt 的差异主要来自锚点替换，不能进入生成。
7. 同一分镜组重新生成时先查询 active registry 和远端节点名，生成下一个 `vid__<source_group_id>__bNNN__rNN__vNNN`；不得因为同组已有实例而跳过。
8. 如果 create 命令已经把图片节点连入 video 节点，后续不要再次对同一入边执行 `--left-add`；重复追加既有边可能卡住 CLI。需要修正顺序时直接重写 `imageList/mixedList/imageListOrder/mixedListOrder`，再 final query。
9. 单个 video 节点当前按 9 张图片输入上限处理；计划阶段若 `ordered_subjects` 超过 9，必须先裁剪并记录被裁剪主体，不要等远端 create 失败后才发现。
10. 任何单组 YAML 边界修复后，必须先本地验证 `^##` 分组数量、所有 fenced YAML 可解析、目标 prompt 不含前后相邻 `group_id`，再写远端节点；不得用未验证的 prompt 覆盖 LibTV 节点。
11. 视频规格时长归一时，所有非 `.5` 结尾的 duration 直接加 `0.5` 秒，而不是四舍五入；例如 `13.0 -> 13.5`、`3.0 -> 3.5`。同步本地证据后必须重新扫描所有 queue record。
12. 复用已有画布时，执行前后都要按名称前缀统计远端 video 节点：本轮 `vid__<episode>-*`、历史遗留、图片参照分别报告。没有用户明确删除授权时，旧 video 节点必须保留，但最终汇报不能只报总节点数。

## Reusable Heuristics

- 最稳顺序锁定是四件套：`图片N` YAML、逐张 `--left-add`、`params.imageList/mixedList` 直接写入、final query 验证。
- 本地分组稿里 `图片N` 是给人和脚本看的既定顺序；远端 prompt 里 `{{Image N}}` 是 LibTV 模型实际消费的编号。两者必须在最终查询时一致。
- 在正确项目空间下创建新画布比在旧污染画布上修复节点更稳；旧节点可保留证据但不应继续作为新生成真源。
- `projectUuid` 是具体画布 UUID；`projectSpaceId/folderId` 是上层项目空间线索。执行 `libtv upload/node/group` 时只传画布 UUID。
- 本地 `projects/aigc/<项目名>/第N集` 是 AIGC 项目到 LibTV 画布的语义映射，不是输入文件路径；输入文件看 `10-分组/第N集.md`，证据目录看 `13-画布/libTV画布流/第N集/`。
- 默认视频规格使用 `star-video2 / mixed2video / 16:9 / 720p`；用户显式指定模型、模式、画幅或分辨率时覆盖对应默认值。
- LibTV prompt 的稳定做法是“完整组稿直入 + YAML 主体行重排为 `图片N 主体名 {{Image N}} UUID`”；脚本只负责把 `{{Image N}}` 对齐，不负责把组稿改写成新正文。
- 节点身份要两层存储：`source_group_id` 用于追溯上游分镜组，`video_node_instance_id` 用于远端节点名、证据文件名和 queue record 唯一键。
- 当用户要求主角多图参照且同组还有多名角色、场景和道具时，先计算图片槽位预算。若超过 9 张，角色和场景优先于道具；任何被裁掉的已知道具必须保留原 YAML 文本并在 manifest/queue/report 中说明是 `libtv_video_max_9`，不得静默丢失。
