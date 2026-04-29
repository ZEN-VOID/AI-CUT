# Cinematography Workflow

本文件定义 `3-摄影` 的思行一体化执行节点。

## Business Requirement Analysis

| slot | answer |
| --- | --- |
| `business_goal` | 给 `2-编导` 逐集稿的每个画面句子注入可执行的大师级镜头语言 |
| `business_object` | Markdown 编导稿中的字段化画面句子 |
| `constraint_profile` | 保真、逐集落盘、LLM 主创、动态引用、下游可执行 |
| `success_criteria` | 每个命中句子下有按节拍生成的 `镜头语言：分镜N`，且专业、炫技、服务剧情 |
| `non_goals` | 不改剧情、不改对白、不生成图像提示词、不替代下游视频阶段 |
| `complexity_source` | 画面匹配覆盖率、节拍判断、画面节奏张弛、高潮分镜强化、技法选择、连续性和保真约束 |
| `topology_fit` | 串行主干 + 类型分流 + review 汇流 |

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、集号、输入真源和上下文 | 用户请求、`2-编导/第N集.md`、项目 `MEMORY.md` | 定位文件，读取相关上下文，确认不改原文 | source path、episode list | `N2-TYPE` | 输入可读且有画面性正文 |
| `N2-TYPE` | 判断画面句子类型与处理策略 | `types/visual-unit-type-map.md` | 建立 visual category 和审美策略 | type_profile | `N3-MATCH` | 类型能覆盖主要字段 |
| `N3-MATCH` | 执行 step1 画面匹配 | `references/visual-matching-contract.md`、正文行 | 找出所有 visual_unit，记录场景锚点和匹配理由 | visual_unit list | `N4-BEAT` | 命中行覆盖画面性字段 |
| `N4-BEAT` | 执行 step2 节拍分析 | visual_unit、`references/beat-analysis-contract.md` | 判断节拍点和分镜数量 | beat_map | `N5-RHYTHM` | 每个 visual_unit 至少 1 个节拍点 |
| `N5-RHYTHM` | 执行 step2.5 画面节奏分析 | visual_unit、beat_map、上下文密度、`references/visual-rhythm-analysis-contract.md` | 判断收敛/发散、描述密度、运动复杂度、转场强度 | rhythm_profile | `N5.5-PEAK-SHOT` | 当前画面有张弛策略 |
| `N5.5-PEAK-SHOT` | 执行 step2.6 高潮分镜强化判断 | visual_unit、beat_map、rhythm_profile、上游 `peak_visual_policy` 或高点证据、`references/peak-shot-language-contract.md` | 识别 `peak_visual_unit`，决定分镜密度、镜头运动、景别尺度、停顿/断裂和余波交接 | peak_shot_profile | `N6-CONTINUITY` | 高点强化可回指上游，不新增事实 |
| `N6-CONTINUITY` | 回看临近镜头语言并建立连续性策略 | rhythm_profile、peak_shot_profile、前 3 个 visual_unit、`references/shot-continuity-contract.md` | 建立轴线、运动方向、景别梯度、光色和注意力交接策略 | continuity_profile | `N7-INJECT` | 当前镜头有进入点和交出点 |
| `N7-INJECT` | 执行 step3 镜头语言注入 | beat_map、rhythm_profile、peak_shot_profile、continuity_profile、`references/dynamic-lens-language-contract.md`、`references/cinematic-technique-library.md` | LLM 直写 `镜头语言：` 与 `分镜N` | enriched episode draft | `N8-REVIEW` | 原文保留，注入块紧跟命中句子 |
| `N8-REVIEW` | 执行质量与机械门禁 | candidate enriched draft、`review/review-contract.md`、可选 validator | 检查覆盖、连续编号、节奏张弛、连续性、保真、专业性，定位 repair target | review result、repair targets | `N8R-DIRECT-REPAIR` 或 `N9-WRITE` | 无阻断项才可写回 |
| `N8R-DIRECT-REPAIR` | 阶段内直接修复阻断项 | repair targets、candidate enriched draft、上游编导稿 | 最小修复 `镜头语言`、`分镜N`、连续性、节奏张弛、峰值分镜、专业可执行或报告证据；不改上游原文 | repaired draft、repair actions | `N8R-REVIEW-AGAIN` | 修复范围不越权 |
| `N8R-REVIEW-AGAIN` | 复审修复稿 | repaired draft、repair actions、上游编导稿 | 复跑阻断 gate；通过则准入写回，失败则回最早责任节点 | re-review verdict | `N9-WRITE` 或 `N3/N4/N5/N5.5/N6/N7/N8R` | 复审通过或明确阻断 |
| `N9-WRITE` | 落盘与报告 | enriched draft、review result | 写入 `3-摄影/第N集.md`，更新报告 | output path、report path | done | 路径和命名符合 Output Contract |

## Branch Rules

- `N3-MATCH` 中标签命中和语义命中可以并行思考，但必须汇总为单一 visual_unit list。
- `N4-BEAT` 先给每个 visual_unit 独立判断，不允许跨句共用分镜编号。
- `N5-RHYTHM` 必须判断当前画面句子该收敛还是发散；不允许所有画面句子同等华丽。
- `N5.5-PEAK-SHOT` 只强化上游已有高点或明显 `micro_payoff`，不得把普通画面硬拔成高潮；强化必须体现为分镜密度、运镜速度、景别尺度、停顿、转场或余波交接的有动机变化。
- `N6-CONTINUITY` 必须回看临近至少前 3 个画面单位；不足 3 个时回看已有全部单位并建立本场景的初始轴线。
- `N7-INJECT` 的技法选择可同时参考构图、运镜、转场、光影、色彩，但最终输出必须凝成可执行、连贯、张弛得当的动态分镜句。
- 任一节点发现需要改写剧情或对白才能成立，必须回退：镜头语言应服务原句，而不是修补原句。
- 若 review 发现上游高点被压平，回到 `N5.5-PEAK-SHOT`；若发现高潮强化导致跳轴、跳色或风格断裂，继续回到 `N6-CONTINUITY`。
- 若 review 发现可由本阶段修复的覆盖、编号、节拍、张弛、连续性或专业性问题，先进入 `N8R-DIRECT-REPAIR` 并复审；不得跳过复审写回。

## Output Shape Per Visual Unit

```markdown
动作画面：林寂猛地睁开眼，身体在座位上僵住，视线从白光里落回现实。
镜头语言：
分镜1: ...
分镜2: ...
```

不同画面句子的 `分镜N` 均从 `分镜1` 重新编号。
