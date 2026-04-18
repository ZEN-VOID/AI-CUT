# Story Planning Branch Output Contract

## Purpose

本文件定义 `story/2-Planning` 在“父 skill + 7 个子技能包 + shared story_map”重构后的输出真源。

目标不是只把 `references/*/module-spec.md` 换个目录，而是把 planning 真正改成：

- 7 个子技能包各自负责本领域的 planning evidence artifact
- 每个子技能同时声明并产出自己的 `story_map_patch`
- 父层只做 `route lock / serial dispatch / review gate / progressive commit / normalize / validate`
- `Planning/全息地图.json` 继续是唯一 canonical planning truth，但它现在被显式视为 story_map carrier

## Canonical Carriers

### 1. Child evidence artifact

- 路径模式：
  - `Planning/全息地图.json`
  - `Planning/全息地图.json`
  - `Planning/全息地图.json`
  - `Planning/全息地图.json`
  - `Planning/全息地图.json`
  - `Planning/全息地图.json`
  - `Planning/全息地图.json`
- 用途：
  - 保留对应子技能的领域分析结论
  - 保留 `story_map_patch`
  - 保留 gate summary 与返工入口

### 2. Shared story_map root

- 路径模式：
  - `Planning/全息地图.json`
- 用途：
  - 作为唯一 canonical planning truth
  - 接收 1-7 子技能的 progressive commit
  - 为 `3-Drafting / query / resume / 5-Loopback` 提供 holomap-first 默认入口

## Hard Rules

1. 子技能必须写自己的 evidence artifact，不得只把 prose 结论交给父层。
2. evidence artifact 必须包含 `story_map_patch`，不得只输出本地分析而不声明写入槽位。
3. 父层只允许 deterministic writeback，不允许重新创作或改写子技能领域结论。
4. `1 -> 7` 固定串行；后一子技能开始前，必须重新读取当前 `Planning/全息地图.json`。
5. 若当前 story_map root 不存在，父层必须先用 `.agents/skills/story/_shared/story_map_bootstrap.template.json` 建立 bootstrap root。
6. 若两个子技能命中同一路径，由父层 gate 直接阻塞，不允许“折中改写”。
7. 父层负责 normalize 与收束，不得越权重写 1-7 已稳定的领域判断，只能补三轴、chapter board、cross-thread index 与导航层。
8. `Planning/全息地图.json` 的运行时兼容入口仍是 `content.holomap`；story_map 是语义名称，不额外制造第二份平行 JSON 真源。

## Default Child Ownership Map

| child skill | evidence artifact | owned story_map slots |
| --- | --- | --- |
| `1-题材选型` | `Planning/全息地图.json` | `content.holomap.story_promise`、`content.holomap.genre_corridor`、`content.holomap.navigation_rules[]` 的题材门 |
| `2-章节规划` | `Planning/全息地图.json` | `content.holomap.volume_boards`、`chapter_boards` skeleton、`episode_sequence_axis` |
| `3-故事大纲` | `Planning/全息地图.json` | `content.holomap.story_spine`、`chapter_boards[].bundled_elements.events` 的主干挂载 |
| `4-冲突设计` | `Planning/全息地图.json` | `content.holomap.conflict_threads`、`chapter_boards[].bundled_elements.conflicts` |
| `5-任务设计` | `Planning/全息地图.json` | `content.holomap.mission_threads`、`chapter_boards[].bundled_elements.missions` |
| `6-线索设计` | `Planning/全息地图.json` | `content.holomap.clue_threads`、`chapter_boards[].bundled_elements.clues` |
| `7-伏笔设计` | `Planning/全息地图.json` | `content.holomap.foreshadow_threads`、`chapter_boards[].bundled_elements.foreshadows` |

## Progressive Commit Rules

1. `1-题材选型` 之后，story_map 至少要有 `story_promise + genre_corridor`。
2. `2-章节规划` 之后，story_map 必须出现稳定 `volume_boards + chapter_boards skeleton`。
3. `3-故事大纲` 之后，chapter board 必须能看见主干事件挂载。
4. `4-7` 每步都只补自己拥有的 thread 与 bundled_elements 槽位。
5. 父层在 1-7 完成后，负责补齐 three-axis、cross-thread indexes、lifecycle、actualization 与 navigation rules。
6. `Planning/全息地图.json` 不是独立 child 的产物，而是 1-7 progressive commit 自然长出来的 shared root。

## Validation Hooks

- stage validator:
  - `.agents/skills/story/2-Planning/scripts/validate_story_map_output.py`
