# Directing Workflow

## Business Requirement Analysis

| slot | value |
| --- | --- |
| `business_goal` | 将逐集小说原文投影为忠实、可拍、可分组的编导稿 |
| `business_object` | `projects/aigc/<项目名>/1-分集/第N集.md` |
| `constraint_profile` | 原文信息量保真、对白冻结、声画配对、slugline 稳定、LLM-first |
| `success_criteria` | 输出能完整承接上游，并可被下游分组/摄影/设计消费 |
| `non_goals` | 不做分镜组切分、不生成图像提示词、不重写剧情 |
| `complexity_source` | 场景解析、字段分流、声画配对、高潮画面识别、保真与质量的优先级协调 |
| `topology_fit` | 串行主干 + 类型分支 + review 回路 |

## Thinking-Action Nodes

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定项目、集号、上游正文真源 | 用户请求、项目根、`1-分集/` | 定位目标集，读取 `SKILL.md + CONTEXT.md`、项目记忆和相关预设 | `source_episode_path`、目标输出路径 | `N2-TYPE` | 上游文件可读 |
| `N2-TYPE` | 形成 `type_profile` | 上游正文结构 | 读取 `types/source-to-script-type-map.md`，判断显式场景/纯小说/系统密集/对白密集等类型 | `type_profile` | `N3-SCENE` | 改编策略不违背保真 |
| `N3-SCENE` | 解析并稳定场景 slugline | 上游段落、type_profile | 按真实地点/空间范围和日夜建立场景表；同 slugline 去重 | `scene_slugline_table` | `N4-FIELD` | 每个场景标题符合 slugline 规则 |
| `N4-FIELD` | 字段分流与声画配对 | 上游段落、场景表 | 逐段投影为声音字段、画面字段、动作、心理、系统、规则、道具、群像等 | `field_projection_map` | `N4.5-PEAK` | 字段纯度和顺序成立 |
| `N4.5-PEAK` | 高潮画面识别与强化计划 | `field_projection_map`、上游段落、质量规范 | 识别 1-3 个上游高点或最强 `micro_payoff`，锁 `source_evidence / audience_desire / promise_source / character_anchor / payoff_mode / build_up / delivery_action / satisfaction_delta / visual_payload / audio_payload / aftershock` | `peak_visual_plan` | `N5-DRAFT` | 高点可回指上游，强化不新增事实或对白 |
| `N5-DRAFT` | LLM 直出逐集编导稿 | 场景表、字段映射、高潮画面计划、质量规范 | 写入 frontmatter、`【剧本正文】`、场景标题和字段化正文 | `第N集.md` 草稿 | `N6-REVIEW` | 未使用脚本主创 |
| `N6-REVIEW` | 保真、对白、声画、slugline 与质量门禁 | candidate 草稿、上游正文、`review/review-contract.md` | 运行机械校验或人工 review；定位阻断项和 source owner | 校验结果、问题清单、repair targets | `N6R-DIRECT-REPAIR` 或 `N7-WRITEBACK` | 无阻断项才可写回 |
| `N6R-DIRECT-REPAIR` | 阶段内直接修复阻断项 | `repair targets`、candidate 草稿、上游正文 | 最小修复字段投影、声画配对、slugline、具像化、声音本体、高点承托或格式证据；不改上游事实和对白 | repaired draft、repair actions | `N6R-REVIEW-AGAIN` | 修复范围不越权 |
| `N6R-REVIEW-AGAIN` | 复审修复稿 | repaired draft、上游正文、repair actions | 复跑阻断 gate；通过则准入写回，失败则回最早责任节点 | re-review verdict | `N7-WRITEBACK` 或 `N3/N4/N4.5/N5/N6R` | 复审通过或明确阻断 |
| `N7-WRITEBACK` | 落盘与报告 | 最终编导稿、校验证据 | 写入 `2-编导/第N集.md` 和 `执行报告.md` | 文件路径、verdict | done | 输出路径和报告完整 |

## Branch Rules

- 若 `type_profile.dialogue_dense == true`，先建立对白原文清单，再写声画配对。
- 若 `type_profile.system_rule_dense == true`，优先使用 `系统画面`、`规则显影`、`旁白（系统提示）` 和 `道具特写`。
- 若 `type_profile.inner_pressure_dense == true`，优先使用 `独白`、`内心独白`、`心理反应` 与 `表演提示`，不得把内视塞入 `动作画面`。
- 若 `type_profile.single_location_multi_beat == true`，必须先建立 slugline 去重表，避免 beat 变化导致重复场景标题。
- 若上游出现行动结果、认知翻转、关系暖点、规则显影、奇观、怪异落点或高超对决，必须进入 `N4.5-PEAK`；强化落入既有字段，不新增 `高潮画面` 字段作为第二解析体系。

## Failure Loops

| symptom | route_back |
| --- | --- |
| 上游事实缺失或顺序漂移 | `N4-FIELD` |
| 对白不保真 | `N5-DRAFT` |
| 声画未配对或混写 | `N4-FIELD` |
| 上游高点被压平成普通叙述，或强化时新增事实 | `N4.5-PEAK` |
| slugline 重复编号 | `N3-SCENE` |
| 质量不足但保真通过 | `N5-DRAFT` |
| review 阻断项可在本阶段修复 | `N6R-DIRECT-REPAIR` |
| 修复后复审仍失败 | 回到最早责任节点：`N3-SCENE` / `N4-FIELD` / `N4.5-PEAK` / `N5-DRAFT` |

## Mermaid

```mermaid
flowchart TD
    A["N1 Intake"] --> B["N2 Type Profile"]
    B --> C["N3 Scene Slugline Table"]
    C --> D["N4 Field Projection"]
    D --> H["N4.5 Peak Visual Pass"]
    H --> E["N5 LLM Draft"]
    E --> F{"N6 Review Gate"}
    F -->|"pass"| G["N7 Writeback"]
    F -->|"needs_rework"| R["N6R Direct Repair"]
    R --> RR{"N6R Review Again"}
    RR -->|"pass"| G
    RR -->|"fail"| D
    F -->|"fact drift"| D
    F -->|"peak flattening"| H
    F -->|"slugline drift"| C
    F -->|"quality rework"| E
```
