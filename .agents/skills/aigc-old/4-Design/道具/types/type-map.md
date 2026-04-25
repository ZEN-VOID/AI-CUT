# Prop Type Map

| type_profile | trigger | route |
| --- | --- | --- |
| `full_prop_chain` | 只有 `3-Detail/第N集.json` | `PROP-N1 -> PROP-N2 -> PROP-N3 -> PROP-N4 -> PROP-N5` |
| `design_from_list` | 已有道具清单或道具对象池 | `PROP-N1 -> PROP-N3 -> PROP-N4 -> PROP-N5` |
| `panel_from_design` | 已有 `[道具名].md` 或兼容 prompt JSON | `PROP-N1 -> PROP-N4 -> PROP-N5` |
| `repair_projection` | 输出路径、命名或模板漂移 | `PROP-N1 -> PROP-N5 -> failed owner` |
