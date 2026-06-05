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
| `LTVCTRL-TM-04` | 画布项目重名 | 项目名和集数重复执行 | 默认追加 `V2`、`V3` | project list 无重名覆盖 |
| `LTVCTRL-TM-05` | prompt 出现绑定表、命令或诊断 | handoff 文案进入视频 prompt | 重写 prompt，只保留分镜组正文 + fenced YAML | 远端 prompt hygiene pass |
| `LTVCTRL-TM-06` | 远端 prompt 看似不同但只替换 `group_id`、主体名或 `{{Image N}}` | scripted prompt projection | 标记 `FAIL-LTVCTRL-SCRIPTED-PROMPT`，恢复直接使用完整分镜组正文 + fenced YAML | final query prompt 可回指完整组正文，而不是模板句 |
| `LTVCTRL-TM-07` | 用户要求重生成已存在分镜组，执行器却跳过或覆盖旧节点 | 把分镜组 ID 当作视频节点唯一键 | 为同一 `source_group_id` 创建新的 `video_node_instance_id`，默认递增 `batch_no`；二修递增 `revision_no` 并记录父实例 | registry 中同一 source_group_id 有多个 instances，旧节点仍可查询 |

## Repair Playbook

1. 先确认本轮是 `full_canvas_control`、`backfill_only`、`node_rebuild_only` 还是 `repair_order`。
2. 对已有视频节点错序，优先删除重建；若不能删除，则清边、逐张连线、再直接重写 `imageList/mixedList`。
3. 所有 `{{Image N}}` 都必须来自本地 YAML `图片N` 和 final remote query 的双重一致性，不来自上传顺序、画布布局或 CLI 参数顺序。
4. 缺图主体跳过回刷，不写负面占位，不把相邻主体图拿来代替。
5. 每次执行后更新 `queue-record.json`，状态必须区分 `created_not_run`、`run_executed`、`blocked`。
6. prompt hygiene 不只查污染词，也要查伪差异；如果多节点 prompt 的差异主要来自锚点替换，不能进入生成。
7. 同一分镜组重新生成时先查询 active registry 和远端节点名，生成下一个 `vid__<source_group_id>__bNNN__rNN__vNNN`；不得因为同组已有实例而跳过。

## Reusable Heuristics

- 最稳顺序锁定是四件套：`图片N` YAML、逐张 `--left-add`、`params.imageList/mixedList` 直接写入、final query 验证。
- 本地分组稿里 `图片N` 是给人和脚本看的既定顺序；远端 prompt 里 `{{Image N}}` 是 LibTV 模型实际消费的编号。两者必须在最终查询时一致。
- 创建新画布项目比在旧污染画布上修复节点更稳；旧节点可保留证据但不应继续作为新生成真源。
- 默认视频规格使用 `star-video2 / mixed2video / 16:9 / 720p`；用户显式指定模型、模式、画幅或分辨率时覆盖对应默认值。
- LibTV prompt 的稳定做法是“完整组稿直入 + YAML 主体行重排为 `图片N 主体名 {{Image N}} UUID`”；脚本只负责把 `{{Image N}}` 对齐，不负责把组稿改写成新正文。
- 节点身份要两层存储：`source_group_id` 用于追溯上游分镜组，`video_node_instance_id` 用于远端节点名、证据文件名和 queue record 唯一键。
