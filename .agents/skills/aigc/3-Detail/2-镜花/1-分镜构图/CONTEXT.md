# CONTEXT.md

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~2200
current_lines: ~52
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-17T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Purpose & Loading Contract

- 本文件保存 `1-分镜构图` 的经验层。
- 命中本 skill 时必须和同目录 `SKILL.md` 一起加载。
- 经验层只沉淀失败类型、修复顺序与可复用 heuristic，不重写 `module-spec.yaml`、叶子 `module-spec.yaml` 或 `SKILL.md` 的规范字段。

## Type Map

| failure_or_outcome_type | immediate_fix | verification_point |
| --- | --- | --- |
| 有镜头感但没有骨架 | 回到 `watermoon_inheritance + shot_count_plan + shot_slot_map` 四件套，先重建组级脊柱，再进入叶子串行 | 后三支能直接承接，不再反向救骨架 |
| `构图形式` 先天发虚 | 回到主体/陪体/背景、空间锚点、轴线和 frame task，先让画面站住 | `composition_skeleton` 能解释“谁压谁、镜头怎么站住” |
| `景别景深` 漂成摄影参数 | 退回“观看距离 + 景深层级 + 心理距离”三件事，不写焦段、光圈或器材值 | `shot_size_rhythm_preview` 能解释情感距离而不是器材设置 |
| `镜头类型` 被写成器材或运镜 | 回到 POV、descriptor 与观看姿态，明确它是叶子上位类，内部统领 `镜头类型 / 镜头框架 / 镜头视角`，不是设备选择或运动路线 | `shot_descriptor_lock` 和 `focus_spatial_logic` 可被后续摄影、运镜直接消费 |
| slot 可读但画面不可拍 | 回到 `SHOT-N2-ANCHOR-SLOT` 与 `构图形式`，重查主陪背景、视线路径与空间锚点是否共用同一镜头任务 | `slot_id`、`构图骨架` 与 `视线组织` 能互相解释 |
| `thinking_process` 只剩审美口号 | 回到思行节点证据，逐条补齐输入依据、动作和 patch 对应关系 | branch review 能从 `thinking_process` 直接追到 `patch_payload` |

## Repair Playbook

1. 先查 shared root 的 `分镜切换`、`剧本正文` 与 `水月` 是否稳定，再判断是不是构图层问题。
2. 若本组锚点说不清，先补 `watermoon_inheritance + shot_slot_map`，不要直接改叶子输出。
3. 若画面站不住，优先回退 `构图形式`，不要直接用景别或镜头类型硬救。
4. 若景别景深变成摄影技术语言，立刻收回到观看距离与心理距离，不允许把摄影参数混进构图层。
5. 若镜头类型开始承担器材、光影或运镜说明，先切回 POV 与 descriptor 槽位，再继续汇流。
6. 若 review 难以判断 patch 是否成立，通常是 `thinking_process -> patch_payload` 的映射断了。

## Reusable Heuristics

- `分镜构图` 最稳的产物不是“漂亮描述”，而是“后三支拿到后不需要重判骨架”的 shot spine。
- 叶子顺序固定为 `构图形式 -> 景别景深 -> 镜头类型`；只要顺序倒过来，通常就会出现画面没站住却先谈距离或类型的漂移。
- `构图形式` 先回答“画面怎么站住”，`景别景深` 再回答“观众离多远”，`镜头类型` 最后回答“观众怎么被带着看”。
- `镜头类型` 是上位叶子名，不是单个 shot 字段；它内部应收束 `镜头类型 / 镜头框架 / 镜头视角` 等具体概念。
- `镜头类型` 不是器材，`景别景深` 不是光圈；一旦名词被误读，构图层就会越权到摄影层。
- `slot_id / 构图骨架 / 视线组织 / beat_refs` 是最小可交付集，缺任一项都说明构图骨架还没站住。
