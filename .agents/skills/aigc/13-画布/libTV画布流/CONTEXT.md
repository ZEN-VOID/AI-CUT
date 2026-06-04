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
| `LTVCTRL-TM-01` | YAML 已有 UUID 但视频主体错绑 | 把 `{{Image N}}` 当作 YAML 顺序，而远端 `imageList` 顺序不同 | 本地先写 `图片N 主体名 UUID`，再直接写 `imageList/mixedList` 为同顺序 | 查询节点 `data.params.imageList[]` |
| `LTVCTRL-TM-02` | 逐张 `--left-add` 后顺序仍不变 | LibTV 入边变更未重算 `params.imageList` | 连线后再次写入 `imageList/mixedList/imageListOrder/mixedListOrder` | final query 顺序等于 YAML |
| `LTVCTRL-TM-03` | 道具和场景复用同一图片 | 同一 UUID 出现在多条主体行 | 同组内相同 UUID 复用同一个 `图片N` | YAML 和 runtime map 都只占一个图位 |
| `LTVCTRL-TM-04` | 画布项目重名 | 项目名和集数重复执行 | 默认追加 `V2`、`V3` | project list 无重名覆盖 |
| `LTVCTRL-TM-05` | prompt 出现绑定表、命令或诊断 | handoff 文案进入视频 prompt | 重写 prompt，只保留分镜组正文 + fenced YAML | 远端 prompt hygiene pass |

## Repair Playbook

1. 先确认本轮是 `full_canvas_control`、`backfill_only`、`node_rebuild_only` 还是 `repair_order`。
2. 对已有视频节点错序，优先删除重建；若不能删除，则清边、逐张连线、再直接重写 `imageList/mixedList`。
3. 所有 `{{Image N}}` 都必须来自本地 YAML `图片N` 和 final remote query 的双重一致性，不来自上传顺序、画布布局或 CLI 参数顺序。
4. 缺图主体跳过回刷，不写负面占位，不把相邻主体图拿来代替。
5. 每次执行后更新 `queue-record.json`，状态必须区分 `created_not_run`、`run_executed`、`blocked`。

## Reusable Heuristics

- 最稳顺序锁定是四件套：`图片N` YAML、逐张 `--left-add`、`params.imageList/mixedList` 直接写入、final query 验证。
- 本地分组稿里 `图片N` 是给人和脚本看的既定顺序；远端 prompt 里 `{{Image N}}` 是 LibTV 模型实际消费的编号。两者必须在最终查询时一致。
- 创建新画布项目比在旧污染画布上修复节点更稳；旧节点可保留证据但不应继续作为新生成真源。
- 默认视频规格使用 `star-video2 / mixed2video / 16:9 / 720p`；用户显式指定模型、模式、画幅或分辨率时覆盖对应默认值。
