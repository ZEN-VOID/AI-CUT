# Object Normalization Contract

## Purpose

本合同是 `4-Design/1-清单` 四个 sibling leaf 的共享类型化抽取真源。

它解决的不是“每条句子怎么写得更完整”，而是“怎样把 `3-Detail` 的导演句子稳定收束成可复用对象池主键”。

## Cross-Leaf Hard Rules

1. 对象主键优先于整句描述。
2. 整句导演句只能降为 `evidence / state / variant / raw_text`，不能直接升格成 canonical identity。
3. 若无法稳定提取对象主键，应保守输出 `unknown` 或空 mention，不得用整句残片硬造对象。
4. 默认输出路径必须从 `projects/aigc/<项目名>` 项目根推断，不能从输入文件父目录随意外推。
5. 允许相对路径输入的 runner，项目根解析必须基于 `Path.parts` 或等价结构判断，不得依赖带前导斜杠的字符串命中。

## Type Priority Matrix

| object_type | 一级锚点 | 二级锚点 | 允许降级位置 | 禁止行为 |
| --- | --- | --- | --- | --- |
| `role` | 组级 `出场角色及穿搭` roster | 镜头 `角色站位走位` 中对 roster 的真实命中 | `group_role_map[].role_text`、`costume_mentions` | 把动作残片、环境词、姿态描述直接当角色名 |
| `scene` | 主场景家族 / 空间实体 | 朝向、边界、气氛描述 | `scene_variant`、`raw_examples` | 把每条 `角色背景面` 整句直接升格成新场景主键 |
| `prop` | canonical noun / 道具实体词 | clause 中的状态子句 | `state_variants`、`raw_mentions` | 把“被切成”“作为背景”“仍在运行”之类状态整句当道具名 |
| `costume` | `角色清单.json` 的 `role_id + canonical_name` | `costume_state` 与镜头 continuity evidence | `continuity_notes`、`group_costume_map[].costume_mentions` | 反向从导演句子残片发明新角色或新服装主键 |

## Role Extraction Rule

1. 先用组级 `出场角色及穿搭` 锁当前组 roster。
2. 再只认镜头 `角色站位走位` 中真实出现的 roster 名称或其稳定别名。
3. 群像仅在文本里明确命中 `群像 / 众人 / 路人 / 大妈群像` 等词时才进入对象池。
4. 自由切词只能作为 fallback，且必须经过对象合法性过滤。

## Scene Extraction Rule

1. 先找主场景家族或空间实体，例如 `社区中央广场 / 全息锦鲤池 / 木星深空通讯画面`。
2. 方位、边界、气氛、状态句默认写入 `scene_variant`。
3. 只有在完全找不到可复用空间实体时，才允许整句保守回退为 `scene_name`。

## Prop Extraction Rule

1. 先命中 canonical noun 或稳定器物名。
2. clause 里的动作、状态、明暗、功能效果只进入 `state` 或 `raw_mentions`。
3. 不允许使用“整句 fallback 成 prop_name”的宽松策略。

## Costume Extraction Rule

1. 角色身份真源只认 `角色清单.json.roles[]`。
2. `3-Detail` 只补 continuity、状态与镜头证据，不反向发明新角色。
3. `costume_id` 固定围绕 `role_id + costume_state`。

## Failure Closure

若出现以下症状，优先回到本合同再检查 sibling leaf：

- 对象数量暴涨到接近镜头数
- canonical name 出现大量句子残片
- 相对路径与绝对路径输入落到不同输出根
- 下游 `2-设计` 读取对象池时需要重新猜主键
