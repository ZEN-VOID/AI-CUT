# Episode Visual Spine Contract

## Purpose

本细则定义 `3-导演` 的整集视觉主轴。它位于单场 `visual_aesthetic_pass` 之前，负责回答“这一集被观众记住的视觉链条是什么”，避免每场各自好看但整集没有统一审美记忆。

它不是摄影方案，不写机位、景别、镜头运动、分镜编号或图像提示词；它也不是统一滤镜或统一色调，不要求每场都塞入同一个母题。

## Episode Visual Spine Pass

每集进入单场美学前，必须建立 `episode_visual_spine`：

| axis | question | output evidence |
| --- | --- | --- |
| `visual_question` | 本集画面在追问什么，例如秘密如何流转、权力如何压迫、离别如何逼近？ | `visual_question` |
| `motif_chain` | 哪 3-5 个视觉母题贯穿本集，并如何变化？ | `motif_chain` |
| `material_and_color_arc` | 纸、布、血、雾、火、金属、木、石等材质/色彩如何递进？ | `material_and_color_arc` |
| `rhythm_curve` | 本集画面节奏从密到疏、从静到动、从压迫到释放，还是反向？ | `rhythm_curve` |
| `callback_targets` | 哪些画面需要前后呼应，而不是只出现一次？ | `callback_targets` |
| `episode_restraint_rule` | 哪些场景只需冷静呈现，不应堆砌美学细节？ | `episode_restraint_rule` |

## Construction Rules

- 视觉主轴必须从上游已有信息、项目记忆、类型气质和安全的 B 路线景境承托中提取。
- 母题链优先选择可见物件、材质、自然景物、空间状态、群体姿态或动作节奏。
- 母题要变化，不要机械重复；同一物件或自然景物在不同场景里应承担不同压力、距离、归属或情绪温度。
- `material_and_color_arc` 只组织画面记忆，不要求所有场景同色同调。
- `rhythm_curve` 服务叙事体验：可以让画面从密集到留白、从静默到爆发、从松弛到逼近。
- `episode_restraint_rule` 必须写清哪里不该用力，防止每个字段都堆美学细节。

## Boundary

允许：

- 让核心物件、空间、自然景物、群体反应和动作节奏形成可感知的变化链。
- 让单场 `visual_aesthetic_pass` 消费整集主轴，在本场选择是否呼应、变奏或克制。
- 在不改变剧情条件的前提下，把安全的环境氛围项纳入视觉链。

禁止：

- 为了统一视觉主轴而新增线索、道具、伤势、天气灾害、行动障碍、规则条件或事件结果。
- 强迫每场都出现同一个母题。
- 把整集主轴写成抽象审美词，例如“高级感”“宿命感”“电影感”。
- 用主轴替代上游保真、对白冻结或单场戏剧功能。

## Example

若一集围绕“秘密在海雾中流转”，可以形成：

```yaml
episode_visual_spine:
  visual_question: "秘密如何从权力中心、衣料残卷和海雾中一路流向港口？"
  motif_chain:
    - "纸面密报"
    - "衣料秘文"
    - "残页缺口"
    - "油绢入袖"
    - "海雾港城"
  material_and_color_arc: "木案暗色和纸面开场，转入火光、残页朱线、油绢殷红，最后被海雾和残金日光压低。"
  rhythm_curve: "前半密集交代权力与秘术，中段追夺加速，末段短暂松弛后由港城轮廓收紧。"
  callback_targets:
    - "纸面信息反复变形为密报、残页、线报和油绢"
    - "海雾从孤船延伸到港口"
  episode_restraint_rule: "不把灾祸奇观化，优先用纸、布、雾、光和停顿承托逼近感。"
```

## Review Checklist

- 整集是否有清晰的 `visual_question`，而不是只列好看的物件？
- `motif_chain` 是否来自上游或安全承托，并且有变化？
- 材质、色彩和节奏是否形成弧线，而不是一组散点？
- 呼应目标是否能在终稿字段中找到落点？
- 克制规则是否防止了细节堆砌？
- 主轴是否没有新增剧情事实、线索、规则、障碍或结果？

## Cross-Episode Spine Continuity

当处理第 N 集且第 N-1 集编导稿已完成时，可读取前集 `执行报告.md` 中的 `visual_aesthetic_evidence.episode_visual_spine` 作为延续参考。

参考内容：

- 前集 `motif_chain`：若其中有可在本集延续的视觉母题，纳入本集 `motif_chain` 候选，但必须变化——同一物件/材质/自然景物在不同集应承担不同压力、距离、归属或情绪温度。
- 前集 `material_and_color_arc`：若前集的材质/色彩弧有延续空间，本集可选择呼应或反转。
- 前集 `rhythm_curve`：本集开场节奏可参考前集结尾的节奏密度，避免突兀跳变。
- 前集 `callback_targets`：若前集的呼应目标中有尚未闭合的母题链，本集可承接。

规则：

- 跨集延续只做参考，不做强制约束。若前集母题与本集剧情无关，不得强行延续。
- 不得为延续跨集母题新增本集没有的剧情事实、对白、事件、规则或线索。
- 前集信息不是本集的上游真源；本集的上游真源始终是 `1-分集/第N集.md`。
- 跨集延续的证据记入 `cross_episode_continuity_profile`，由 `N1-DIR-INTAKE` 加载、`N7-DIR-AESTHETIC` 消费。
- 若前集编导稿不存在，标注 `episode-local continuity`，不做跨集延续。
