# 2-编导 Review Contract

## Review Purpose

`2-编导` 的 review gate 验证逐集编导稿是否把 script layer、director layer、performance layer 的职责合成一个可拍、可听、可演的 canonical 主稿：忠实承接 `1-分集`，对白逐字冻结，导演判断和表演工艺内嵌到字段正文，最终表达全部落为画面化语言，并能以结构化 handoff 交给 `3-运动` 继续强化角色运动。

## Default Provider

- 默认辅助 provider：`code-reviewer`
- 用途：检查 Skill 2.0 包结构、脚本边界、输出合同、三层创作证据和画面化语言门禁。
- review 必须加载本文件、`../steps/directing-workflow.md`、本阶段实际命中的 `references/`、`types/`，以及 `../../_shared/concrete-visual-language-contract.md`。
- 若存在 `init_team_synthesis_context`，review 必须检查它是否只消费初始化冻结综合、服务当前节点判断，并且没有调用 team 成员身份、解析旧 stage profile、改写上游剧情事实或替代 LLM 主创。

## Stage-End Review-Repair Rule

- 除 `review_only` 外，review gate 是写回 `2-编导/第N集.md` 前的阻断门。
- `needs_rework` 必须回到 `steps/directing-workflow.md` 的 `N6R-BD-REPAIR`，由 `2-编导` 本阶段直接做最小修复并复审；复审未通过不得写入 canonical，也不得推进 `3-运动` 或 `4-摄影`。
- 允许直接修复的范围：字段投影、声画配对、slugline、对白画面、小说转译、信息释放、导演判断嵌入、视觉主轴、氛围/声音/尾钩、心理反应、台词交付、潜台词行为、场面调度、沉默余波、具像画面化语言、frontmatter、报告证据和格式。
- 禁止直接修复的范围：新增或删减剧情事实、改写对白、改变事件顺序、替上游 `1-分集` 修剧情、直接生成分镜编号/图像提示词/视频请求。
- `pass_with_followups` 只允许非阻断质量建议；保真、对白、输出路径、LLM-first、导演/表演缺层或抽象化语言不得降级为 followup。

## Blocking Gates

| gate_id | check | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| `GATE-BD-01` | 输出路径为 `projects/aigc/<项目名>/2-编导/第N集.md`，不创建 script/director/performance 并列新主稿 | `FAIL-BD-PATH` | `N7-BD-WRITEBACK` | `output_path_check` |
| `GATE-BD-02` | frontmatter 含 `source_episode_path` 且可回指 `1-分集/第N集.md` | `FAIL-BD-SOURCE` | `N1-BD-INTAKE` | `source_episode_path` |
| `GATE-BD-03` | 上游事实、信息量、事件顺序完整承接 | `FAIL-BD-FAITHFULNESS` | `N2-BD-SCRIPT` | `faithfulness_evidence` |
| `GATE-BD-04` | 对白逐字保真，引号内不加入动作或解释 | `FAIL-BD-DIALOGUE` | `N2-BD-SCRIPT` | `dialogue_lock_evidence` |
| `GATE-BD-05` | 场景标题、字段分流、声画配对和字段纯度成立 | `FAIL-BD-FIELD-PURITY` | `N2-BD-SCRIPT` | `script_layer_evidence` |
| `GATE-BD-06` | 小说作者评论、心理内视、抽象概括、因果解释、关系结论已二次画面化 | `FAIL-BD-NOVEL-TO-SCREEN` | `N2-BD-SCRIPT` | `novel_expression_transform_evidence` |
| `GATE-BD-07` | 关键场景有观众知识状态、信息差、悬念保留与节奏画像 | `FAIL-BD-AUDIENCE-RHYTHM` | `N2-BD-SCRIPT` | `audience_psychology_map` / `scene_rhythm_profile` |
| `GATE-BD-08` | 导演判断不是抽象评语，已落为戏剧问题、人物压力、视觉主轴、高潮/反高潮、声音与终结画面 | `FAIL-BD-DIRECTOR-SUBSTANCE` | `N3-BD-DIRECTOR` | `director_layer_evidence` |
| `GATE-BD-09` | 导演增强没有新增剧情事实、对白、因果或未授权桥段 | `FAIL-BD-CONTROLLED-ENRICHMENT` | `N3-BD-DIRECTOR` | `controlled_enrichment_ledger` |
| `GATE-BD-10` | 表演层有心理反应、演员五层控制、台词交付、潜台词行为、场面调度和沉默余波 | `FAIL-BD-PERFORMANCE` | `N4-BD-PERFORMANCE` | `performance_layer_evidence` |
| `GATE-BD-11` | 长对白保留原文片段，并有气口、停顿、重音、声线、身体联动和对手反应 | `FAIL-BD-LONG-DIALOGUE` | `N4-BD-PERFORMANCE` | `long_dialogue_delivery_map` |
| `GATE-BD-12` | 群戏和角色弧线有主次、空间占位、注意力焦点和状态差 | `FAIL-BD-ENSEMBLE-ARC` | `N4-BD-PERFORMANCE` | `ensemble_performance_evidence` / `character_arc_performance_evidence` |
| `GATE-BD-13` | 全稿通过具像画面语言检查；不得用情绪标签、审美口号、心理论文、表演意图总结代替可见可听可演锚点 | `FAIL-BD-VISUAL-LANGUAGE` | `N5-BD-VISUAL-LANGUAGE` | `concrete_visual_language_evidence` |
| `GATE-BD-14` | 没有机位、景别、镜头运动、分镜编号或视频提示词越权 | `FAIL-BD-STAGE-OVERREACH` | `N5-BD-VISUAL-LANGUAGE` | `stage_boundary_check` |
| `GATE-BD-15` | 脚本没有替代 LLM 生成核心创作正文 | `FAIL-BD-LLM-FIRST` | `N6R-BD-REPAIR` | `llm_first_authorship_check` |
| `GATE-BD-16` | 执行报告含 `thinking_action_node_ledger`、三层证据、`scene_field_evidence_index`、review verdict、repair actions 和 re-review verdict；关键判断可回到来源、目标字段和正文嵌入句 | `FAIL-BD-EVIDENCE` | `N7-BD-WRITEBACK` | `report_evidence_check` |
| `GATE-BD-17` | 初始化团队综合若存在，已被裁决为节点上下文，不改写上游真源，不触发 team 身份技能或旧 stage profile | `FAIL-BD-ADVISOR-BOUNDARY` | `N6R-BD-REPAIR` | `init_team_synthesis_context` |
| `GATE-BD-18` | `motion_enrichment_handoff.visual_unit_candidate_map` 齐全，每项含 `source_anchor`、`target_field`、`visual_unit_text`、`why_visual` 和 `non_camera_boundary`；不得含机位、景别、镜头运动、分镜编号或 prompt | `FAIL-BD-HANDOFF` | `N7-BD-WRITEBACK` | `motion_enrichment_handoff` |

## Recommended Mechanical Check

```bash
python3 .agents/skills/aigc/2-编导/scripts/validate_script_projection.py projects/aigc/<项目名>/2-编导/第N集.md
```

该脚本只检查结构、字段和基础风险，不能证明剧情事实完整承接、导演判断成立或表演工艺有效；这些必须由 LLM/人工 review 对读上游和本合同。

## Verdict Model

| verdict | meaning |
| --- | --- |
| `pass` | 可交付给 `3-运动`，再由 `3-运动` 交付给 `4-摄影` |
| `pass_with_followups` | 可交付，但存在非阻断质量优化 |
| `needs_rework` | 存在保真、对白、导演、表演、画面化语言、输出路径或证据阻断项 |
| `blocked` | 上游缺失、路径不可读、权限或策略阻断 |

## Report Shape

```yaml
review:
  verdict: pass | pass_with_followups | needs_rework | blocked
  source_episode_path: projects/aigc/<项目名>/1-分集/第N集.md
  output_path: projects/aigc/<项目名>/2-编导/第N集.md
  checks:
    source_lock: pass
    faithfulness: pass
    dialogue_lock: pass
    script_layer: pass
    director_layer: pass
    performance_layer: pass
    concrete_visual_language: pass
    stage_boundary: pass
    llm_first: pass
    report_evidence: pass
    handoff_to_cinematography: pass
  repair_actions: []
  re_review_verdict: pass
  thinking_action_node_ledger: []
  scene_field_evidence_index: []
  script_layer_evidence: {}
  director_layer_evidence: {}
  performance_layer_evidence: {}
  concrete_visual_language_evidence: {}
  motion_enrichment_handoff:
    next_stage: 3-运动
    ready: true
    visual_unit_candidate_map: []
    forbidden_payload: ["shot_number", "camera_angle", "lens", "camera_movement", "image_prompt", "video_prompt"]
  init_team_synthesis_context:
    status: not_applicable | completed | blocked
    execution_brief: ""
  findings: []
```
