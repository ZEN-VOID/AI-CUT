# Episode Final Image Type Map

## Purpose

本类型包负责在 `2-编导` 中为每集终结画面做类型化匹配。它不直接写尾钩正文，只输出 `final_image_type_profile`，供 `references/episode-final-image-contract.md` 和 `steps/directing-workflow.md` 消费。

## Type Profile Variables

| variable | values | detection cue | strategy |
| --- | --- | --- | --- |
| `next_episode_context_status` | `next_episode_readable` / `episode_local_only` | `projects/aigc/<项目名>/1-分集/第N+1集.md` 是否可读 | 可读时只取关联方向；不可读时只做本集局部推断，不硬造下一集事实 |
| `final_anchor_surface` | `environment` / `prop` / `emotion` / `peak_aftershock` / `mixed` | 本集最后段落主要落在空间氛围、道具状态、人物情绪还是高点余波 | 决定优先手法，必要时只选一个主手法、一个辅助手法 |
| `hook_promise_type` | `suspense` / `danger` / `relationship_unfinished` / `information_gap` / `theme_stamp` / `emotional_aftertaste` / `state_reversal` | 本集末尾留下的追更理由 | 决定尾钩表层吸引力，避免写成剧情总结 |
| `spoiler_risk_level` | `low` / `medium` / `high` | 是否需要借下一集具体事件、台词、新角色、规则答案或结果才能成立 | `high` 时必须退回本集局部推断或更换手法 |
| `continuity_mode` | `smooth_extension` / `callback_variation` / `aftershock_hold` / `unresolved_action` | 尾钩如何从本集自然顺延 | 选择环境延展、母题呼应、高点余波或未完成动作 |
| `preferred_method` | `environmental_tag` / `prop_closeup_tag` / `emotional_brew_tag` / `climax_tail_tag` | 由 anchor、promise 和 spoiler 风险综合决定 | 输出给 `episode_final_image_plan.final_image_method` |

## Method Selection Matrix

| condition | preferred_method | notes |
| --- | --- | --- |
| `final_anchor_surface=environment` 且下一集压力可由空间、天气、声音或远处状态暗示 | `environmental_tag` | 最适合非剧透地把下一集压力提前变成氛围方向 |
| `final_anchor_surface=prop` 且本集已有物件可承接未解问题 | `prop_closeup_tag` | 只写道具可见状态、归属、异常或未完成动作，不新增功能 |
| `final_anchor_surface=emotion` 或 `hook_promise_type=relationship_unfinished/emotional_aftertaste` | `emotional_brew_tag` | 通过沉默、停顿、手部、距离、群像或声音余波制造追更欲 |
| `final_anchor_surface=peak_aftershock` 且本集高点刚兑现 | `climax_tail_tag` | 消费 `peak_visual_plan.cost_or_aftershock`，不改高点结果 |
| `spoiler_risk_level=high` | 降级为 `environmental_tag` 或 `emotional_brew_tag` | 避开下一集具体事件、台词、答案和结果 |
| `next_episode_context_status=episode_local_only` | 只允许 `episode-local inference` | 不声明下一集事实，只承接本集未解决压力和项目类型承诺 |

## Output Shape

```yaml
final_image_type_profile:
  next_episode_context_status: next_episode_readable | episode_local_only
  final_anchor_surface: environment | prop | emotion | peak_aftershock | mixed
  hook_promise_type: suspense | danger | relationship_unfinished | information_gap | theme_stamp | emotional_aftertaste | state_reversal
  spoiler_risk_level: low | medium | high
  continuity_mode: smooth_extension | callback_variation | aftershock_hold | unresolved_action
  preferred_method: environmental_tag | prop_closeup_tag | emotional_brew_tag | climax_tail_tag
```

`final_image_type_profile` 只决定终结画面的手法匹配，不授权新增剧情事实、对白、线索、规则或下一集剧透。
