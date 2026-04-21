# Planning Slice Layout Contract

## Purpose

本文件把 `story/2-Planning` 的 canonical planning truth 从“单一大 root”收束为：

- 一个全局总索引根：`2-Planning/全息地图.json`
- 一组按十集切分的 episode slice：`2-Planning/十集分片/第001-010集.json` 等

它是 `2-Planning / 3-Drafting / 4-Validation / 5-Loopback / query` 共享的数据分层真源。任何 sibling skill 不得再各自定义第二套“root 放什么、slice 放什么”的平行规则。

## Layout Mode

- 默认新合同模式：`total-index-plus-deciles`
- 建议根文件声明：
  - `meta.layout_mode = "total-index-plus-deciles"`
  - `content.holomap.episode_slice_manifest`
- 兼容旧项目时，可继续保留 monolith，但一旦项目进入该模式，就必须按本合同读写与校验。

## Canonical Carriers

### 1. Global Index Root

- 路径：`2-Planning/全息地图.json`
- truth role：全局索引真源、路由锚点、全阶段默认入口

### 2. Episode Slice Files

- 路径模式：`2-Planning/十集分片/第001-010集.json`
- 每个 slice 固定覆盖 10 集；最后一个 slice 允许小于 10 集
- truth role：episode-local dense planning truth

### 3. Child Evidence Artifacts

- 路径模式：`2-Planning/pass-artifacts/1-题材选型.json` ... `7-伏笔设计.json`
- truth role：保留子技能领域分析、gate summary、`story_map_patch.global_patch` 与 `story_map_patch.slice_patches`

## Global Index Retained Slots

以下字段保留在 `2-Planning/全息地图.json.content.holomap`，不得拆到 slice 再把 root 留空：

| slot | retain_reason | downstream use |
| --- | --- | --- |
| `scope` | stage 级边界与真源说明 | 全阶段 |
| `story_promise` | 整书承诺与 type stack 根裁决 | `3-Drafting / 4-Validation` |
| `genre_corridor` | 叙事禁飞区与 type-pack 投影 | `3-Drafting / 4-Validation` |
| `story_spine` | 整书主问题、卷级推进、关键转折 | `3-Drafting / query` |
| `timeline_axis` | 全局时间轴 | `3-Drafting / 4-Validation` |
| `space_axis` | 全局空间轴 | `3-Drafting / 4-Validation` |
| `volume_boards` | 卷级容器与卷级 planning contract；不得退化成仅有卷名与摘要 | `3-Drafting / query` |
| `character_roster_projection` | 角色 planning projection | `3-Drafting / 4-Validation` |
| `relationship_graph_projection` | 关系 planning projection | `3-Drafting / 4-Validation` |
| `conflict_threads` | 冲突主线程定义 | `3-Drafting / 4-Validation / query` |
| `mission_threads` | 任务主线程定义 | `3-Drafting / 4-Validation / query` |
| `clue_threads` | 线索主线程定义 | `3-Drafting / 4-Validation / query` |
| `foreshadow_threads` | 伏笔主线程定义 | `3-Drafting / 4-Validation / query` |
| `lifecycle_lexicon` | 生命周期词典 | `query / loopback` |
| `cross_thread_indexes` | 跨线程导航索引 | `query / 4-Validation` |
| `state_transitions` | 全局状态转移语义 | `4-Validation / 5-Loopback` |
| `navigation_rules` | 导航与读法规则 | 全阶段 |
| `episode_sequence_axis` | episode -> slice -> chapter_board 的薄索引 | `3-Drafting / 4-Validation / query` |
| `episode_slice_manifest` | 十集分片清单与命名真源 | `3-Drafting / 4-Validation / 5-Loopback / validator` |
| `actualization` | 只保留 write policy、slice summary、episode status index | `5-Loopback / query` |

## Episode Slice Slots

以下字段必须下沉到 `2-Planning/十集分片/第XXX-YYY集.json.content.holomap_slice`，不得继续把完整 payload 塞回 root：

| slot | payload shape | owner |
| --- | --- | --- |
| `slice_scope` | `slice_id / episode_start / episode_end / episode_refs / file_ref` | 父层 |
| `slice_style_contract` | 当前十集 obey 的卷级规划镜像，至少含 `contract_ref / visual_climate / action_grammar / mystery_mode / emotional_temperature / taboo_writeups` | `2-章节规划` |
| `chapter_boards` | 当前十集的 board 全量密集载荷 | `2-章节规划` 起步，`3-7` 挂载 |
| `episode_sequence_axis` | 当前十集的轴明细，至少含 `episode_ref / chapter_board_ref / slice_ref` | `2-章节规划` |
| `thread_window_slice` | 当前十集的 conflict / mission / clue / foreshadow window | `4-7` |
| `foreshadow_silence_slice` | 当前十集的伏笔静默窗口 | `7-伏笔设计` |
| `actualization` | 当前十集 episode-local actualization 明细 | `5-Loopback` |

## Read Layer Matrix

| consumer | 先读哪层 | 再读哪层 | 只从哪层取关键 payload |
| --- | --- | --- | --- |
| `2-Planning` 父层 | global index root | 本轮命中的 slice | dense `chapter_boards / actualization` 只从 slice 取 |
| `3-Drafting` | global index root | 当前集命中的 slice | `chapter_board / thread_window_slice / foreshadow_silence_slice` |
| `4-Validation` | global index root | 当前集命中的 slice | `chapter_board / planning debt / foreshadow_silence_slice` |
| `5-Loopback` | global index root | 当前集命中的 slice | `actualization` 细节只写 slice，root 只刷 summary/index |
| `query` | global index root | 仅在问题涉及 episode-local board 或 actualization detail 时再读 slice | local board / actualization detail |

## Writeback Boundary Matrix

| writer | 允许写 global root | 允许写 slice | 禁止 |
| --- | --- | --- | --- |
| `1-题材选型` | `story_promise / genre_corridor / navigation_rules` | 否 | episode-local board payload |
| `2-章节规划` | `volume_boards / episode_slice_manifest / 薄 episode_sequence_axis` | `slice_style_contract / chapter_boards / slice episode_sequence_axis` | 冲突/任务/线索/伏笔内容 |
| `3-故事大纲` | `story_spine` | `chapter_boards[].bundled_elements.events` | 直接改四条长线 master 定义 |
| `4-冲突设计` | `conflict_threads` | `thread_window_slice.conflicts`、`chapter_boards[].bundled_elements.conflicts` | 覆盖 story spine |
| `5-任务设计` | `mission_threads` | `thread_window_slice.missions`、`chapter_boards[].bundled_elements.missions` | 覆盖 conflict/clue/foreshadow master |
| `6-线索设计` | `clue_threads` | `thread_window_slice.clues`、`chapter_boards[].bundled_elements.clues` | 覆盖 global actualization |
| `7-伏笔设计` | `foreshadow_threads` | `thread_window_slice.foreshadows`、`foreshadow_silence_slice`、`chapter_boards[].bundled_elements.foreshadows` | 覆盖上一层 global planning master |
| `5-Loopback` | `actualization.write_policy / slice_status_index / episode_status_index` | `actualization` 明细 | 覆盖任何 `planned_*` 与 `chapter_boards` |

## Naming Rules

1. slice 目录固定：`2-Planning/十集分片/`
2. 文件名固定：`第%03d-%03d集.json`
3. `slice_id` 固定：`slice-%03d-%03d`
4. `episode_slice_manifest[].file_ref` 必须与文件名完全一致。
5. `episode_sequence_axis[].slice_ref` 必须回指 manifest 中已有 `slice_id`。
6. 每个 episode 只能落在一个 slice；禁止 overlap，禁止 hole。
7. 若最后一个 slice 不满 10 集，文件名仍按真实结束集号命名，例如 `第211-220集.json` 或 `第221-224集.json`。

## Anti-Drift Validation

启用 `total-index-plus-deciles` 后，validator 至少要检查：

1. global root 存在 `episode_slice_manifest`
2. root 的 `chapter_boards` 不得再承载 full dense payload
3. root 的 `actualization` 不得再承载 episode-local 明细
4. 每个 manifest entry 的 `file_ref` 命名合法
5. 所有 slice 的 episode coverage 连续、无重叠、无漏集
6. `episode_sequence_axis[].slice_ref` 能命中 manifest
7. slice 内 `chapter_boards[].episode_ref` 必须全部落在本 slice 范围内
8. `5-Loopback` 写回后，root 只更新 summary/index，slice 才更新 actualization 明细

## Compatibility Rule

- monolith 老项目可继续只用 `全息地图.json`
- 一旦项目显式切换到 `meta.layout_mode = total-index-plus-deciles`，所有新写回与校验必须服从本合同
- 不允许 root 和 slice 同时各自保留一份完整 `chapter_boards` 或完整 `actualization`，这会构成隐藏双真源
