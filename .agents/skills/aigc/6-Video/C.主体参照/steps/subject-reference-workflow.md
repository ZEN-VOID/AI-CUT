# Subject Reference Workflow

## Business Requirement Analysis

| slot | conclusion |
| --- | --- |
| `business_goal` | 把 `3-Detail` 中的组级视频事实和可见主体收束成一个可审计的视频主体参照包。 |
| `business_object` | `3-Detail/<episode>.json`、组级请求对象、主体索引、`Assets/` 主体图片引用、provider handoff 包。 |
| `constraint_profile` | LLM 主创 prompt/TXT；主体识别必须回链上游事实；引用只绑定真实 Assets；provider handoff 不伪造执行能力。 |
| `success_criteria` | 同一 episode 根下能看到全能参照蒸馏、主体识别/绑定、生成交接三段证据，且最终下一入口唯一。 |
| `non_goals` | 不改写 3-Detail，不生成图片，不重命名资产，不直接提交 provider。 |
| `topology_fit` | 串行主干 + mode 分支 + gate 汇流。 |

## Thinking-Action Nodes

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定 project、episode、subject scope、mode、输出根与全能参照配置消化结果 | 用户目标、父级路由、项目目录、旧 `全能参照` 合同与 `prompt-assembly-spec.md` | 判定 mode，定位 source/output，形成 `omni_reference_digest` | `mode_profile`、`subject_scope`、`output_root`、`omni_reference_digest` | `N2`、`N3`、`N4`、`N5` 或 blocked | mode、主体范围和全能参照消化结果明确 |
| `N2-DISTILL` | 生成全能参照请求对象和 TXT | `3-Detail/<episode>.json`、prompt 合同、模板 | LLM 主创 prompt/TXT，写 distill 三件套 | `distill_manifest` | `N3` 或 `N6` | JSON/TXT/manifest 齐备 |
| `N3-IDENTIFY` | 识别可作为视频参照锚点的主体 | detail root、distill request、主体绑定合同 | 提取角色/服装/道具/场景主体，写 subject index | `subject_index`、`subject_report` | `N4` 或 `N6` | 主体可回链且不臆造 |
| `N4-BIND` | 绑定 `Assets/` 主体图片引用 | subject index、distill 或兼容请求 JSON、`Assets/` | 生成候选、唯一匹配、重建引用字段 | `subject_match_report` | `N5` 或 blocked | 无猜测绑定 |
| `N5-HANDOFF` | 写 provider handoff 包 | 稳定请求对象、provider 偏好 | 判定 input_mode，写 plan/brief | `submit_plan`、`submit_brief` | `N6` 或 waiting | 下一入口唯一 |
| `N6-REVIEW` | 汇总 gate verdict | 三段 artifacts、review 合同 | 本地 review checklist 或 provider review | `verdict` | done 或 rework | `pass/pass_with_todo` |

### N1 Intake: 全能参照配置消化门

`N1-INTAKE` 不只是 route/mode 锁定。凡本轮可能进入 `distill_only`、`full_chain`，或从旧三段链迁入 `distill/` 产物，N1 必须先把 `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/` 的核心配置消化成 `omni_reference_digest`，再交给后续节点消费。

`omni_reference_digest` 必须至少包含：

- `source_contracts`: 已对照 `全能参照/SKILL.md`、同目录 `CONTEXT.md` 与 `prompt-assembly-spec.md`，并确认本融合包承接的是“分镜组 -> 1 条组级视频请求对象 + episode TXT/manifest”的组级蒸馏合同；旧脚本只作为投影、校验或兼容迁移辅助。
- `input_gate`: `3-Detail/<episode>.json` 是 canonical detail root；compat projection 后 `metadata.document_phase=ready`；目标组在 `final_output.main_content.分镜组列表` 中稳定命中；每组满足 `分镜组ID / 分镜切换 / 剧本正文 / 正文切分参考[] / 组间设计.全局风格 / 类型元素 / 导演意图 / 出场角色及穿搭 / 分镜明细[] / 正文回指.beat_refs / 时间段`，且 `len(分镜明细[]) == 分镜切换`。
- `prompt_assembly`: prompt 采用 `BC` 结构，不保留独立 A 段整组 `剧本正文`；组级设计块吸收 `全局风格 / 类型元素 / 导演意图 / 出场角色及穿搭 / 固定音频约束`；镜级行固定以 `xx秒-xx秒｜分镜<组内序号>：` 起笔；字段标题隐藏，完整四段式 `分镜ID` 只写入结构化回链。
- `txt_semantics`: `第N集.txt` 是人工审阅主稿，按“分镜组ID -> 全局风格/类型元素/导演意图 -> 分镜N，x-y秒 -> 剧本正文 -> 主体锚定 -> 分镜明细 -> 字数统计”组织；`剧本正文`、`主体锚定.场景/角色` 不得压缩，`主体锚定.道具` 只允许轻量收束。
- `compression_budget`: 继承 `G1/P0/P1/P2/P3` 与 `full / normal / tight / ultra` 预算语义；优先保住剧情桥段、动作/表演、景别、构图、运镜、速度、视角；字数压力先压 `P3`，再酌情收束 `P2`，不得先牺牲 `P0/P1`。
- `subject_evidence_bridge`: 从 `主体锚定.角色 / 场景 / 道具`、`组间设计.出场角色及穿搭`、镜级动作/可见物、`道具及状态` 与 `source_shot_ids` 提前形成主体候选证据，供 `N3-IDENTIFY` 写入 `subject-index.json`；不得在 `N3` 凭 prompt 印象重新发明主体。
- `artifact_shape`: `distill/` 段输出仍是 `第N集.json + 第N集.txt + _manifest.json` 三件套，并保留 `reference_images / image_markers` 的 provider-neutral 骨架；`_manifest.json` 至少记录 source detail root、episode、group scope、generated packets、source group ids、source shot ids、prompt char count 与 subject candidate extraction status。

`N1` 的证据必须写出 `omni_reference_digest.status`。若状态不是 `ready`，不得进入 `N2-DISTILL`；若本轮只走 `identify_subjects`、`bind_subject_references` 或 `handoff_provider`，也要记录跳过 distill 的原因，以及现有请求对象如何满足上述 artifact shape 与 subject evidence bridge。

## Branch Rules

- `distill_only`: `N1 -> N2 -> N6`
- `identify_subjects`: `N1 -> N3 -> N6`
- `bind_subject_references`: `N1 -> N3 -> N4 -> N6`
- `handoff_provider`: `N1 -> N5 -> N6`
- `full_chain`: `N1 -> N2 -> N3 -> N4 -> N5 -> N6`
- `compat_migration`: `N1 ->` 仅进入缺失或待投影节点，不补未执行段占位。

## Failure Routes

| failure | route |
| --- | --- |
| detail root 不稳定 | 停止并回 `3-Detail` |
| group scope 或 subject scope 多义 | 停止并回 `N1`，要求明确目标或修上游 |
| prompt/TXT 不满足 LLM 主创或字段覆盖 | 回 `N2` |
| 主体无法回链来源镜头或类别混淆 | 回 `N3` |
| 主体资产候选歧义 | 停止于 `N4`，输出歧义报告 |
| 引用状态 `unresolved` 却试图 handoff | 回 `N4` |
| provider 未明确且无法推荐主案 | 停在 `N5` 等待用户裁决 |
| review 发现阻断项 | 回对应节点 |
