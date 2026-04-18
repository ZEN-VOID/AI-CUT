# `.webnovel/preferences.json` Schema

`preferences.json` 是**可选偏好覆盖层**，不是 canonical truth。

用途：

- 给 `ContextManager` 提供写法偏好
- 给 `3-Drafting` 提供风格偏置
- 补充用户长期偏好，但不推翻 `0-Init / 1-Cards / 2-Planning` 的真源裁决

## 推荐结构

```json
{
  "tone": "热血克制",
  "pacing": {
    "target_words_per_chapter": 2400,
    "chapter_end_hook_bias": "strong",
    "transition_chapter_allowance": 1
  },
  "style": {
    "dialogue_ratio_target": 0.38,
    "narration_density": "medium",
    "voice_preferences": [
      "对白要有攻防",
      "避免说明书式自白"
    ]
  },
  "focus": [
    "主角成长压强",
    "关系推进",
    "章末期待锚点"
  ],
  "avoid": [
    "过度旁白",
    "AI模板腔",
    "重复打脸句式"
  ],
  "hard_preferences": {
    "allow_explicit_violence": false,
    "romance_heat_level": "medium",
    "worldbuilding_exposition_limit": "light"
  }
}
```

## 字段说明

| 字段 | 说明 |
|---|---|
| `tone` | 全局情绪与叙述基调 |
| `pacing` | 字数、钩子强度、过渡章容忍度等节奏偏好 |
| `style` | 对白占比、叙述密度、声口偏好 |
| `focus` | 希望持续强化的方向 |
| `avoid` | 希望系统持续规避的写法 |
| `hard_preferences` | 平台或用户长期边界 |

## 约束

- `preferences.json` 只影响“怎么写”，不改“必须发生什么”。
- 与 `0-Init` 的商业承诺、`Cards` 的对象规则、`MAP` 的章节编排冲突时，以真源为准。
