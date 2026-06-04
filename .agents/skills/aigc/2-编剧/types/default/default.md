# Genre Narrative Type Package

本类型包为 `2-编剧` 的默认必载分型包，用于建立 `type_profile`。它不拥有输出路径、写回权限或 review gate。

## Match Signals

- 小说转剧本、剧本化改编、题材解析、叙事情节解析。
- 短剧节奏、爽点、反转、高潮、尾钩、声画同步、同画面连续性。
- 用户未指定题材，但 source 中存在明确题材信号。

## Genre Axes

| axis | values | decision_use |
| --- | --- | --- |
| `conflict_scale` | personal / family / workplace / public / supernatural | 决定场景空间、见证者和高潮落点 |
| `information_mode` | audience_knows_more / character_knows_more / shared_discovery / hidden_truth | 决定信息差、误会、证据露角 |
| `emotional_charge` | revenge / romance / fear / dignity / shame / protection / ambition | 决定对白、声音和动作承托 |
| `pace_density` | low / medium / high / burst | 决定单场长度、转场频率和信息密度 |
| `production_risk` | low / medium / high | 决定是否使用低成本奇观、少地点、少角色方案 |

## Narrative Patterns

| pattern | signal | preferred_rhythm |
| --- | --- | --- |
| `oppression-counterstrike` | 角色先被压制，随后出现反制条件 | `RHY-02`, `RHY-03`, `RHY-05`, `RHY-09` |
| `misread-intimacy` | 关系推进靠误会、保护、试探或未完成触碰 | `RHY-04`, `RHY-07`, `RHY-12` |
| `clue-pressure` | 真相靠线索逼近，角色必须隐藏或验证 | `RHY-01`, `RHY-03`, `RHY-06`, `RHY-10` |
| `public-proof` | 冲突需要见证者或制度场景确认 | `RHY-02`, `RHY-05`, `RHY-09` |
| `bridge-reveal` | 本集主要承接上集结果并铺下一集问题 | `RHY-03`, `RHY-10`, `RHY-11` |

## Fixed Context

- 分型结果必须进入 `genre_narrative_profile`。
- 不确定题材时优先依据 source 中的角色欲望、阻碍和信息释放方式判定，而不是依据表层人设。
- 同一集允许主/副题材并存，但节奏机制最多 2 主 1 辅，避免混乱。
