# 漫画剧本改编质量门禁

本文件承载 `漫画剧本改编` 的结构校验、语义验收与 reviewer/provider 降级口径。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：审查 Skill 2.0 结构、动态引用、脚本边界、模板一致性，以及漫画剧本输出门禁是否可执行。
- 若上层策略阻断真实 subagent 或外部 reviewer 调度，降级为本地 review checklist，并在最终报告中说明阻断层级、原计划 provider、实际降级路径和未真实启动的 reviewer。

## Validation Commands

```bash
python3 .agents/skills/comic/1-漫画剧本改编/scripts/validate_grouped_manga_script.py <第N组.md>
python3 .agents/skills/comic/1-漫画剧本改编/scripts/validate_grouped_manga_script.py <stage-1-output-dir>
```

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可作为 `2-九刀流漫画提示词` 的直接上游真源 |
| `pass_with_followups` | 可交付，但有非阻断后续项 |
| `needs_rework` | 有阻断问题，必须回到指定节点返工 |
| `blocked` | 缺关键输入、路径、权限或事实边界 |

## Review Scope

| dimension | checks |
| --- | --- |
| `contract` | 是否完成来源归一、事实边界、类型包加载、分组合同与钩子合同 |
| `source_fidelity` | 是否保住来源材料的事实核、关系核、情绪核与卖点核 |
| `adaptation_power` | 是否从素材转成可连载冲突，而不是摘要复述 |
| `comic_readiness` | 是否场景化、可拆页、可画、可进入九刀流 |
| `hook_quality` | 每组是否有悬停点、危险逼近点或关系反转 |
| `grouping` | 分组是否遵守约 1000 字口径、尾组规则与自然边界 |
| `type_handoff` | `type_stack_active_packs` 与两段投影是否写入组文件并体现在语气、节奏、钩子里 |
| `truth_boundary` | 新闻/热搜/纪实来源是否区分事实与虚构 |
| `voice_readability` | 解说漫兼容时是否可朗读、不绕、不泄气 |
| `audio_visual_pairing` | 对白、旁白、内心独白、音效、系统提示是否有就近可画承托 |
| `field_purity` | 声音、画面、心理、规则文字是否各归其位，没有混写抽象判断 |
| `scene_anchor` | 每组是否有稳定空间、光线/时间、核心物件、角色站位和最贵一格 |
| `single_truth` | 是否只保留 `第N组.md` 集合为 canonical output |

## Scoring Matrix

| dimension | indicator | score |
| --- | --- | --- |
| 维度0: 契约遵循 | 来源归一、事实边界、分组合同、钩子合同、类型包加载 | __/10 |
| 维度1 | 来源要点保真度 | __/10 |
| 维度2 | 类型卖点与冲突发动机强度 | __/10 |
| 维度3 | 分组节奏与追更欲 | __/10 |
| 维度4 | 组末钩子有效性 | __/10 |
| 维度5 | 分组边界稳定性 | __/10 |
| 维度6 | 组文件命名与顺序规范性 | __/10 |
| 维度7 | 漫画下游可消费性 | __/10 |
| 维度8 | 氛围压力场与高冲击画面设计 | __/10 |
| 维度9 | 旁白沉浸感与朗读质感 | __/10 |
| 维度10 | 声画配对、字段纯度与场景锚点稳定性 | __/10 |

## Pass Table

| field_id | pass_standard | fail_code | rework_entry |
| --- | --- | --- | --- |
| `FIELD-COMIC-01` | `source_digest` 同时覆盖事实、画面、情绪、关系、未解点 | `FAIL-COMIC-01` | `N3` |
| `FIELD-COMIC-02` | 事实边界明确，现实事实不被伪造 | `FAIL-COMIC-02` | `N4` |
| `FIELD-COMIC-03` | 改编摘要能说明类型、卖点、冲突与代价 | `FAIL-COMIC-03` | `N5` |
| `FIELD-COMIC-04` | 分组遵守默认口径与尾组规则，不机械截断 scene / hook / payoff | `FAIL-COMIC-04` | `N6` |
| `FIELD-COMIC-05` | 组文件严格按 `第N组.md` 命名，标题与 frontmatter 组号一致且顺序连续 | `FAIL-COMIC-05` | `N6-N9` |
| `FIELD-COMIC-06` | 每组推进清楚、正文场景化、组末有钩子 | `FAIL-COMIC-06` | `N7-N8` |
| `FIELD-COMIC-07` | 冲击画面、氛围母题、分格和翻页点足够明确 | `FAIL-COMIC-07` | `N5-N8` |
| `FIELD-COMIC-08` | 解说漫兼容时正文可朗读且文字负载可控 | `FAIL-COMIC-08` | `N7` |
| `FIELD-COMIC-09` | 每个组文件都可被 2 号技能当作独立九页处理单元 | `FAIL-COMIC-09` | `N8-N9` |
| `FIELD-COMIC-10` | 最终交付只保留 `第N组.md` 真源集合，无并行主稿竞争 | `FAIL-COMIC-10` | `Output Contract` |
| `FIELD-COMIC-11` | 声音文本与画面承托就近配对，画面字段具像化，规则/系统信息可视化 | `FAIL-COMIC-11` | `N7-N8` |

## Finding Shape

```yaml
finding:
  severity: critical | high | medium | low
  dimension: contract | source_fidelity | adaptation_power | comic_readiness | grouping | type_handoff | truth_boundary | audio_visual_pairing | field_purity | scene_anchor | single_truth
  symptom: ""
  direct_cause: ""
  source_contract: ""
  rework_target: ""
```

## Gate Rule

不得在以下情况宣布完成：

- 未加载 `CONTEXT.md` 或命中的 `types/` 类型包。
- 输出缺少 `第N组.md` 连续组文件，或 `reply_only` 未按同结构分组。
- 组文件缺任一 required frontmatter 字段或 required section。
- 新闻/热搜来源没有 `truth_boundary` 和事实/虚构区分。
- 正文只有摘要，没有可画场景。
- 命中编导字段桥接时，声音字段没有就近画面承托，或画面字段停留在心理判断、主题解释、抽象概念。
- 系统提示、规则文字、道具信息没有可视化承托。
- 组末没有钩子，或钩子把缺口完全解释完。
- 输出存在并行主稿与 `第N组.md` 竞争真源。
