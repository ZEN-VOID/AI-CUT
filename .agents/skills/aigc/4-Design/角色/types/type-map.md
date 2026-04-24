# Role Type Map

| type_profile | trigger | route |
| --- | --- | --- |
| `full_role_chain` | 只有 `3-Detail/第N集.json` | `ROLE-N1 -> ROLE-N2 -> ROLE-N3 -> ROLE-N4 -> ROLE-N5` |
| `design_from_list` | 已有角色清单或角色对象池 | `ROLE-N1 -> ROLE-N3 -> ROLE-N4 -> ROLE-N5` |
| `panel_from_design` | 已有 `[角色名].md` 或 `character_design.json` | `ROLE-N1 -> ROLE-N4 -> ROLE-N5` |
| `repair_projection` | 输出路径、命名或模板漂移 | `ROLE-N1 -> ROLE-N5 -> failed owner` |
