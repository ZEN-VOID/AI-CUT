# Action Choreography Contract

## Purpose

本细则用于武侠、动作、玄幻、战争、格斗、追逐、兵器、术法对抗和其他打戏题材。它补足 `5-表演` 在动作戏中的编排职责：动作表现不能只停在演技、情绪或“打得激烈”，必须把动作戏本身设计成可执行、可拍、可接续的动作链。

本文件不授权新增胜负结果、伤势结果、招式设定、剧情因果、人物能力设定、镜头语言、分镜编号、prompt 或视频参数。所有动作设计必须回指上游画面点、导演批注、角色目标、场景压力或 `3-美学` 约束。

## Trigger Scope

出现以下任一信号时必须加载本细则：

- 题材或用户要求出现：武侠、动作、玄幻、仙侠、格斗、搏斗、追逐、逃杀、战争、兵器、剑、刀、枪、拳脚、术法、法阵、灵力、内力、妖兽、对决、打戏、动作戏。
- 字段出现 `动作画面`、`角色动作`、`群像画面`、`音效画面`、`心理反应` 等，并且当前 beat 涉及追、打、挡、避、摔、撞、压制、反击、冲刺、飞身、跃起、坠落、兵器交接或术法碰撞。
- 审查发现动作只有结果，没有过程、路径、方式、力度、伴随反应或身体代价。

## Action Choreography Map

命中打戏时，内部必须形成 `action_choreography_map`：

```yaml
action_choreography_map:
  beat_id: ""
  source_anchor: ""
  participants: []
  combat_intent:
    actor: ""
    opponent: ""
    objective: ""            # 压制、脱身、试探、保护、夺物、阻挡、拖延等
    constraint: ""           # 空间、伤势、距离、规则、身份、道具或时间限制
  spatial_path:
    start_position: ""
    route: ""                # 直进、斜切、绕后、后撤、贴地、跃上、跌退等
    end_position: ""
    distance_change: ""
  action_chain:
    initiation: ""           # 起手或触发
    attack_or_motion: ""
    defense_or_evasion: ""
    counter_or_adjustment: ""
    landing_or_interruption: ""
  force_profile:
    speed: ""
    weight: ""
    range: ""
    rhythm: ""
  contact_and_impact:
    contact_point: ""
    transfer: ""
    miss_or_glance: ""
    body_cost: ""
  accompaniment:
    sound: ""
    prop_or_costume: ""
    environment_response: ""
    magic_or_energy_anchor: ""
  preservation_check:
    no_new_outcome: true
    no_new_ability_lore: true
    field_embedding: []
```

## Writing Rules

- 动作链必须有起点、过程和落点。不能只写“二人交手”“剑光一闪”“他被打退”，要写清谁先动、朝哪里动、用什么方式动、对手如何接、力量如何传递、人物最后停在哪里。
- 路径必须能在空间里成立。写清方位、距离、方向、障碍、上/下/前/后/侧向变化，避免人物瞬移或兵器凭空触达。
- 力度和速度必须可感知。用骤发、压住、拖慢、短促、沉重、擦过、收住、被震偏、踉跄半步等身体化词，不用“非常激烈”“气势很强”代替。
- 攻防方式必须具体。至少区分起手、攻击/移动、防守/闪避、反制/变招、落点/中断中的关键两到三项；高密度打戏可写完整链条。
- 伴随反应必须服务动作，不做孤立装饰。衣摆、尘土、水汽、火光、碎石、兵器声、术法光、墙面震动等，只能从动作接触、速度、材质或环境锚点自然产生。
- 玄幻或术法动作必须有物理锚点。灵力、剑气、法阵、火焰、冰霜等不能只写概念爆发，必须落到手势、步法、兵器轨迹、身体承压、空气/地面/衣物/光声反应和对手接招方式。
- 打戏中的表演不能消失。动作后必须保留体力、疼痛、呼吸、重心、手部、眼神、犹豫或压制等演员可演残留，让下一 beat 能接上。
- 动作设计不得改变上游结果。若上游只说“逼退”，不能写成重伤；若上游没有明确招式名、门派设定或能力机制，不能新增世界观设定。

## Field Embedding

| source_field | choreography_projection |
| --- | --- |
| `动作画面` / `角色动作` | 承载动作链主体：起手、路径、攻防、变招、落点、力度速度、身体残留 |
| `群像画面` | 承载多人打戏焦点：行动者、反应者、背景压迫、阵形变化和避让路径 |
| `音效画面` | 承载兵器交接、拳脚撞击、落地、擦过、破风、术法碰撞和环境余响 |
| `心理反应` / `表演提示` | 承载动作中的目标、犹豫、判断、疼痛压制或呼吸残留，但必须外显 |
| `对白画面` | 承载打斗中说话的气口、断句、动作中断、压低声线或动作后的尾音 |

## Review Checks

| check | fail_code | repair |
| --- | --- | --- |
| 动作只有结果，没有起手、过程或落点 | `FAIL-PERF-ACTION-CHOREOGRAPHY` | 回到 `action_chain` 补 initiation、attack/evasion、landing |
| 动作没有空间路径或距离变化 | `FAIL-PERF-ACTION-PATH` | 补 start_position、route、end_position、distance_change |
| 动作没有方式、力度、速度或身体承重 | `FAIL-PERF-ACTION-FORCE` | 补 force_profile、contact_and_impact |
| 伴随声画与动作无因果关系 | `FAIL-PERF-ACTION-ACCOMPANIMENT` | 删除孤立装饰，或改为动作接触、速度、材质自然引发 |
| 玄幻术法只有概念，没有物理锚点 | `FAIL-PERF-ACTION-MAGIC-ANCHOR` | 补手势、步法、兵器轨迹、身体承压和环境反应 |
| 动作设计新增胜负、伤势、招式设定或剧情因果 | `FAIL-PERF-ACTION-FAITHFULNESS` | 删除新增结果，回到上游锚点与保真边界 |
