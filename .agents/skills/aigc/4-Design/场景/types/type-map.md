# Scene Type Map

| type_profile | trigger | route |
| --- | --- | --- |
| `full_scene_chain` | 只有 `3-Detail/第N集.json` | `SCENE-N1 -> SCENE-N2 -> SCENE-N3 -> SCENE-N4 -> SCENE-N5` |
| `design_from_list` | 已有场景清单或场景对象池 | `SCENE-N1 -> SCENE-N3 -> SCENE-N4 -> SCENE-N5` |
| `panel_from_design` | 已有 `[场景名].md` 或 `scene_design.json` | `SCENE-N1 -> SCENE-N4 -> SCENE-N5` |
| `repair_projection` | 输出路径、命名或模板漂移 | `SCENE-N1 -> SCENE-N5 -> failed owner` |
