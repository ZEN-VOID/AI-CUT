# Cinematography Style Analysis Contract

`摄影风格解析.md` 是 `shot-by-shot` 输出给 `3-摄影` 的摄影语法 side context。它可以讨论景别、视角、焦点、运镜、构图、光影和节奏，但不得改写 `2-编导` 正文，也不得固定照抄参考片镜头数量或顺序。

## Required Fields

| field | requirement |
| --- | --- |
| `visual_unit_function` | 该类画面在目标项目中的观看任务 |
| `beat_map_seed` | 注意力、动作相位、信息揭示、情绪转折或空间关系的换镜理由 |
| `rhythm_profile_seed` | 收敛、标准展开、发散强化或断裂停顿的节奏建议 |
| `continuity_seed` | 轴线、运动方向、光影母题、景别梯度和交出点 |
| `camera_grammar_plan_seed` | 景别、视角、景深、焦点、镜头类型、构图、光影、运镜的迁移策略 |
| `functional_projection_payload` | 主体、动作、运镜、构图锚点、光影、空间接口、交出点 |
| `shot_detail_style_seed` | 可转成自然中文 `分镜明细：` 的写法参考 |
| `do_not_import` | 不得导入参考片具体构图、镜头顺序、标志性画面或专属视觉符号 |

## Markdown Shape

`摄影风格解析.md` 至少包含：

1. `## 使用边界`
2. `## 摄影语法摘要`
3. `## 摄影风格 Seeds`
4. `## 分镜明细写法参考`
5. `## AIGC 可执行性`
6. `## Do Not Import`
