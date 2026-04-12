# Type Strategies

## Design Completeness Strategy

| design_state | 判定信号 | 面板策略 | 说明 |
| --- | --- | --- | --- |
| `ready` | 具备 `final_scene_prompt + panel_handoff + scene_key` | 正常生成 panel carrier | 默认状态 |
| `prompt-only` | 只有 `final_scene_prompt`，缺 `panel_handoff` | 允许生成，但在 `场景面板.json.panels[]` 保留空 `panel_handoff` 并依赖模板布局合同 | 低风险降级 |
| `incomplete` | 缺 `final_scene_prompt` 或缺 `scene_key` | 失败退出 | 禁止编造 |

## Output Mode Strategy

| mode | 产物 | 用途 |
| --- | --- | --- |
| `episode-batch` | `场景面板.json + 多个 <scene_key>-layout.json` | 默认整集面板整理 |
| `single-scene` | 单个 `<scene_key>-layout.json` + 更新后的 `场景面板.json` | 局部返工或增补 |
| `dry-run` | 仅打印将生成的文件清单 | 验证命名和命中范围 |

## Negative Prompt Strategy

1. 优先使用 `reverse_taboos[]`。
2. 若 `reverse_taboos[]` 为空，则读取模板默认 negative prompt。
3. 额外追加固定门禁：`no humans, no creatures, no text clutter, no panel overlap`。
4. 不得把 `2-设计` 的大段 reasoning 文本直接塞进 negative prompt。

## Conflict Tie-Break

1. `场景设计.json` 的字段高于逐场景 Markdown 卡片。
2. `panel_handoff` 高于脚本自行猜测的布局解释。
3. 若 `final_scene_prompt` 与 `panel_handoff` 冲突，优先保留 `final_scene_prompt` 的空间事实，`panel_handoff` 只补布局视角。
4. 若模板与技能合同冲突，以本技能 `SKILL.md` 和输出契约为准。
