# Controlled Enrichment Contract

## Purpose

`controlled_enrichment` 是 `2-编导` 的 B 路线：在不替换默认 `faithful_projection` 主线的前提下，允许为影视可拍性、表演可执行性和场景张力补充受控承托细节。

它不是自由改编，不授权新增剧情事实、对白、桥段、因果、规则、人物动机或事件结果。它只允许把上游已经存在的信息、压力、心理、关系、规则或高点补足为更可拍、更可演、更可分组的非剧情性细节。

## Route Position

| route | default | authority | canonical status |
| --- | --- | --- | --- |
| `A-faithful_projection` | 默认主线 | 忠实投影上游正文 | canonical |
| `B-controlled_enrichment` | 受控增强，可由用户要求或质量门触发 | 增加非剧情性承托细节，必须有上游锚点 | 可写入 canonical，但必须在报告中留 `controlled_enrichment_ledger` |
| `C-authorized_adaptation` | 非本合同范围 | 新对白、新桥段、新场景、新因果强化 | 只能作为候选稿，需用户另行授权 |

## Trigger

进入 B 路线的合法触发：

- 用户要求“更影视化”“更有戏”“适当新增可拍承托”“增强表演层次”，但没有授权新剧情。
- 用户要求环境更有氛围、景境更充分、用自然景物衬托心境或情绪，但没有授权新剧情。
- `N4.7-CRAFT` 发现上游存在心理、潜台词、权力关系、沉默反应或状态差，但直接投影后演员无事可做。
- `N4.5-PEAK` 发现高点存在，但缺少画面、声音、群像、道具或余波承托。
- review 判定“保真通过但戏剧承托不足”，且修复不需要新增剧情事实或对白。

不得把以下请求自动降级为 B 路线：

- 用户要求新增对白、新场景、新角色行动、新规则、新冲突、新反转、新结局。
- 用户要求重排事件、压缩剧情、强化因果、补完整桥段。
- 上游事实缺失导致无法判断承托细节是否安全。

这些必须进入阻断或另行请求 `C-authorized_adaptation` 授权。

## Allowed Enrichment

| enrichment type | allowed example | required anchor |
| --- | --- | --- |
| 环境氛围增强 | 飘雪压低庭院声、落叶贴住门槛、朝露挂在草尖、风沙擦过墙角、雨丝映出灯火 | 上游已有地点、时段、季节可能性、类型气质、情绪压力或心境需求；只写景境本身，不写人物动作、剧情结果或新阻碍 |
| 群体反应 | 笔尖停住、后排椅子缩回、全班迟半拍抬头 | 上游已有群体恐惧、沉默、震动或公告 |
| 表演外显 | 呼吸变浅、手指压纸、避开视线、停半拍 | 上游已有心理、潜台词、试探或判断 |
| 场面调度 | 道具停在两人之间、讲台压住学生、门口被占据 | 上游已有权力关系、空间位置或对抗关系 |
| 声音承托 | 纸张摩擦、灯管嗡鸣、鞋跟节奏、沉默后的呼吸 | 上游已有声音来源、紧张场景或动作触发 |
| 道具承托 | 关键物件未被收起、痕迹停在信息旁、规则显影物反光 | 上游已有道具、规则文字、系统提示、线索痕迹或归属压力 |
| 余波承托 | 高点后声音短暂抽空、群像迟半拍、角色身体状态改变 | 上游已有高点、认知翻转、爽点或关系变化 |

## Forbidden Enrichment

以下属于剧情性新增，禁止在 B 路线写入 canonical：

- 新增上游没有的对白、旁白观点、系统公告或规则文本。
- 新增上游没有的事件、桥段、人物动作结果、伤害、救援、逃脱、死亡、胜负。
- 新增角色动机、因果解释、人物关系结论或设定信息。
- 新增道具功能、规则能力、系统机制、线索含义。
- 为了制造戏剧性改变场景顺序、压缩事件、合并人物或提前透露信息。
- 用“更高级”“更电影化”为理由删除上游事实。

## Enrichment Ledger

每次启用 B 路线，执行报告必须记录 `controlled_enrichment_ledger`。逐集编导稿可在 frontmatter 中标记：

```yaml
enrichment_mode: controlled_supportive
```

执行报告最小结构：

```yaml
controlled_enrichment_ledger:
  mode: controlled_supportive
  items:
    - source_anchor: "上游第N段/原句摘要"
      source_signal: "上游已存在的心理、关系、规则、空间、声音或高点"
      added_detail: "新增的非剧情性承托细节"
      target_field: "对白画面 / 角色动作 / 环境描写(写景/景境/氛围承托) / 群像画面 / 音效画面 / 道具特写"
      purpose: "可拍性 / 可演性 / 声画承托 / 高点余波 / 下游可分组"
      risk_check: "no_new_dialogue / no_new_event / no_new_causality / no_new_rule"
```

若无法写出 `source_anchor` 或 `risk_check`，该新增项不得进入 canonical。

## Review Gate

B 路线通过条件：

- 每个新增承托细节都能回指上游已有信息或情绪压力。
- 新增内容只改变表现层，不改变剧情层。
- 没有新增对白、事件、规则、线索、因果或人物动机。
- `controlled_enrichment_ledger` 完整记录新增项和风险检查。
- 若 review 对某项新增是否越权存在疑问，默认删除该新增项，而不是冒险保留。
