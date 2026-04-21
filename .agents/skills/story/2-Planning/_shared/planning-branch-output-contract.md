# Story Planning Branch Output Contract

## Purpose

本文件定义 `story/2-Planning` 在“父 skill + 7 个子技能包 + shared story_map”重构后的输出真源。

目标不是只把 `references/*/module-spec.md` 换个目录，而是把 planning 真正改成：

- 7 个子技能包各自负责本领域的 planning evidence artifact
- 每个子技能同时声明并产出自己的 `story_map_patch`
- 父层先从 `1-Cards/2-角色卡` 导入 `character_roster_projection / relationship_graph_projection`
- 父层只做 `route lock / serial dispatch / review gate / progressive commit / normalize / validate`
- `2-Planning/全息地图.json` 是唯一 global index truth
- `2-Planning/十集分片/*.json` 是唯一 episode-local dense planning truth

global/slice 的字段边界、命名规则与防漂移要求以 `planning-slice-layout-contract.md` 为第一真源；本文件只定义 branch patch 如何落到这两层。

## Canonical Carriers

### 1. Child evidence artifact

- 路径模式：
  - `2-Planning/pass-artifacts/1-题材选型.json`
  - `2-Planning/pass-artifacts/2-章节规划.json`
  - `2-Planning/pass-artifacts/3-故事大纲.json`
  - `2-Planning/pass-artifacts/4-冲突设计.json`
  - `2-Planning/pass-artifacts/5-任务设计.json`
  - `2-Planning/pass-artifacts/6-线索设计.json`
  - `2-Planning/pass-artifacts/7-伏笔设计.json`
- 用途：
  - 保留对应子技能的领域分析结论
  - 保留 `story_map_patch`
  - 保留 gate summary 与返工入口

### 2. Shared global root

- 路径模式：
  - `2-Planning/全息地图.json`
- 用途：
  - 作为唯一 global index planning truth
  - 接收 1-7 子技能的 global patch progressive commit
  - 为 `3-Drafting / query / resume / 5-Loopback` 提供 holomap-first 默认入口

### 3. Shared episode slices

- 路径模式：
  - `2-Planning/十集分片/第001-010集.json`
  - `2-Planning/十集分片/第011-020集.json`
- 用途：
  - 接收 2-7 子技能的 episode-local dense patch progressive commit
  - 承载 `chapter_boards / thread_window_slice / foreshadow_silence_slice / actualization`

## Hard Rules

1. 子技能必须写自己的 evidence artifact，不得只把 prose 结论交给父层。
2. evidence artifact 必须包含 `story_map_patch`，不得只输出本地分析而不声明写入槽位。
3. 父层只允许 deterministic writeback，不允许重新创作或改写子技能领域结论。
4. `1 -> 7` 固定串行；后一子技能开始前，必须重新读取当前 `2-Planning/全息地图.json` 与受影响 slice。
5. 若当前 story_map root 不存在，父层必须先用 `.agents/skills/story/_shared/story_map_bootstrap.template.json` 建立 bootstrap root。
6. 若两个子技能命中同一路径，由父层 gate 直接阻塞，不允许“折中改写”。
7. 父层负责 normalize 与收束，不得越权重写 1-7 已稳定的领域判断，只能补三轴、chapter board、cross-thread index 与导航层。
8. `2-Planning/全息地图.json` 的运行时兼容入口仍是 `content.holomap`；slice 的运行时兼容入口固定为 `content.holomap_slice`。
9. `character_roster_projection / relationship_graph_projection` 由父层导入并维护；任何 child 都只能读不能改。
10. `2-章节规划 / 4-冲突设计 / 5-任务设计` 只能写角色/关系 refs 与 hook，不得复制完整角色卡正文或图谱 Markdown。
11. 当项目已启用显式 `type-pack` 时，planning child 应消费 `story_promise.type_stack_ref + genre_corridor.type_pack_projection`，并把本轮采用的 pack bias 摘要写入 evidence artifact，而不是在局部重新猜题材偏好。

## Parent-Owned Import Slots

| owner | slots | source |
| --- | --- | --- |
| `2-Planning` 父层 | `content.holomap.character_roster_projection` | `1-Cards/2-角色卡/**/*.json` |
| `2-Planning` 父层 | `content.holomap.relationship_graph_projection` | `1-Cards/2-角色卡/角色关系图谱.md` + `relationship_edges` |

## Default Child Ownership Map

| child skill | evidence artifact | owned story_map slots |
| --- | --- | --- |
| `1-题材选型` | `2-Planning/pass-artifacts/1-题材选型.json` | global: `content.holomap.story_promise`、`content.holomap.genre_corridor`、`content.holomap.navigation_rules[]` 的题材门 |
| `2-章节规划` | `2-Planning/pass-artifacts/2-章节规划.json` | global: `content.holomap.volume_boards`、`content.holomap.episode_slice_manifest`、薄 `content.holomap.episode_sequence_axis`；slice: `content.holomap_slice.slice_style_contract`、`content.holomap_slice.chapter_boards`、`content.holomap_slice.episode_sequence_axis` |
| `3-故事大纲` | `2-Planning/pass-artifacts/3-故事大纲.json` | global: `content.holomap.story_spine`；slice: `content.holomap_slice.chapter_boards[].bundled_elements.events` |
| `4-冲突设计` | `2-Planning/pass-artifacts/4-冲突设计.json` | global: `content.holomap.conflict_threads`（含 `character_refs / relationship_edge_refs`）；slice: `content.holomap_slice.thread_window_slice.conflicts`、`content.holomap_slice.chapter_boards[].bundled_elements.conflicts` |
| `5-任务设计` | `2-Planning/pass-artifacts/5-任务设计.json` | global: `content.holomap.mission_threads`（含 `owners / counterparts / relationship_edge_refs`）；slice: `content.holomap_slice.thread_window_slice.missions`、`content.holomap_slice.chapter_boards[].bundled_elements.missions` |
| `6-线索设计` | `2-Planning/pass-artifacts/6-线索设计.json` | global: `content.holomap.clue_threads`；slice: `content.holomap_slice.thread_window_slice.clues`、`content.holomap_slice.chapter_boards[].bundled_elements.clues` |
| `7-伏笔设计` | `2-Planning/pass-artifacts/7-伏笔设计.json` | global: `content.holomap.foreshadow_threads`；slice: `content.holomap_slice.thread_window_slice.foreshadows`、`content.holomap_slice.foreshadow_silence_slice`、`content.holomap_slice.chapter_boards[].bundled_elements.foreshadows` |

## Progressive Commit Rules

1. `1-题材选型` 之后，story_map 至少要有 `story_promise + genre_corridor`。
2. `2-章节规划` 之后，global root 必须出现稳定 `volume_boards + episode_slice_manifest + thin episode_sequence_axis`，且 `volume_boards` 已达到卷级 planning contract 密度；对应 slice 必须出现 `slice_style_contract + chapter_boards skeleton`。
3. `3-故事大纲` 之后，slice 内 `chapter_board` 必须能看见主干事件挂载。
4. `4-7` 每步都只补自己拥有的 thread master 与 slice bundled_elements 槽位。
5. 父层在 1-7 完成后，负责补齐 three-axis、cross-thread indexes、lifecycle、global actualization summary/index 与 navigation rules。
6. `2-Planning/全息地图.json` 不是独立 child 的产物，而是 1-7 progressive commit 自然长出来的 shared global root；十集分片同理是 episode-local shared slices。
7. 角色/关系 projection 在 Step 2 前就必须已经导入 root，后续 child 只消费 id / hook。
8. 若项目已启用 `type-pack`，各 child 的 evidence artifact 至少应记录本轮采用的 `type_pack_projection_summary`，便于后续 drafting / validation / review 回溯。

## Validation Hooks

- stage validator:
  - `.agents/skills/story/2-Planning/scripts/validate_story_map_output.py`
  - 启用 `total-index-plus-deciles` 后，validator 必须同时检查 root 与 manifest 命中的 slices
