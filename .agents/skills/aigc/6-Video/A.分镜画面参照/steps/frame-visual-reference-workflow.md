# Frame Visual Reference Workflow

## Business Requirement Analysis

| slot | conclusion |
| --- | --- |
| `business_goal` | 把 `3-Detail` 中的目标分镜事实收束成一个可审计的视频分镜画面参照包。 |
| `business_object` | `3-Detail/<episode>.json`、帧级请求对象、`Assets/` 图片引用、provider handoff 包。 |
| `constraint_profile` | LLM 主创 prompt/TXT；引用只绑定真实 Assets；provider handoff 不伪造执行能力。 |
| `success_criteria` | 同一 episode 根下能看到首帧蒸馏、绑定、生成交接三段证据，且最终下一入口唯一。 |
| `non_goals` | 不改写 3-Detail，不生成图片，不直接提交 provider。 |
| `topology_fit` | 串行主干 + mode 分支 + gate 汇流。 |

## Thinking-Action Nodes

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 锁定 project、episode、shot scope、mode、输出根与首帧语义消化结果 | 用户目标、父级路由、项目目录、旧 `首帧参照` 合同 | 判定 mode，定位 source/output，形成 `first_frame_digest` | `mode_profile`、`shot_scope`、`output_root`、`first_frame_digest` | `N2`、`N3`、`N4` 或 blocked | mode、帧级目标和首帧消化结果明确 |
| `N2-DISTILL` | 生成首帧请求对象和 TXT | `3-Detail/<episode>.json`、prompt 合同、模板 | LLM 主创 prompt/TXT，写 distill 三件套 | `distill_manifest` | `N3` 或 `N5` | JSON/TXT/manifest 齐备 |
| `N3-BIND` | 绑定 `Assets/` 图片引用 | distill 或兼容帧级请求 JSON、`Assets/` | 生成候选、唯一匹配、重建引用字段 | `match_report` | `N4` 或 blocked | 无猜测绑定 |
| `N4-HANDOFF` | 写 provider handoff 包 | 稳定请求对象、provider 偏好 | 判定 input_mode，写 plan/brief | `submit_plan`、`submit_brief` | `N5` 或 waiting | 下一入口唯一 |
| `N5-REVIEW` | 汇总 gate verdict | 三段 artifacts、review 合同 | 本地 review checklist 或 provider review | `verdict` | done 或 rework | `pass/pass_with_todo` |

### N1 Intake: 首帧参照消化门

`N1-INTAKE` 不只是 route/mode 锁定。凡本轮可能进入 `distill_only`、`full_chain` 或从旧三段链迁入 `distill/` 产物，N1 必须先把 `.agents/skills/aigc/6-Video/1-提示词蒸馏/首帧参照/` 的核心合同消化成 `first_frame_digest`，再交给后续节点消费。

`first_frame_digest` 必须至少包含：

- `source_contracts`: 已对照 `首帧参照/SKILL.md`、同目录 `CONTEXT.md` 与 `prompt-assembly-spec.md`，确认本融合包承接的是“单一 `分镜ID` 或 episode carrier 下的单镜多条请求”，不是组级全能参照。
- `input_gate`: `3-Detail/<episode>.json` 必须是 ready 的 canonical detail root；目标 `分镜ID` 唯一命中；所属组满足 `分镜切换 == len(分镜明细[])`；目标时间段使用当前分镜组内相对秒位。
- `bridge_semantics`: 通过 `正文切分参考[] -> 正文回指` 提取目标帧可见剧情桥段；边界模糊时保守压缩，不照搬整组剧本正文，也不虚构过渡。
- `prompt_semantics`: prompt 使用 `BC` 结构、镜级行以 `xx秒-xx秒｜分镜<组内序号>：` 起笔、除镜级标签外隐藏字段标题、完整四段式 `分镜ID` 只落在结构化回链。
- `txt_semantics`: `第N集.txt` 是一镜版同构主稿，固定保留 `分镜组ID / 全局风格 + 类型元素 + 导演意图 / 分镜N，x-y秒 / 剧本正文 / 主体锚定 / 分镜明细 / 字数统计`。
- `budget_semantics`: 继承 `G1/P0/P1/P2/P3` 保留与压缩顺序；非 `tight` 状态下，单镜预算余量优先补给当前分镜动作、空间、镜头控制与氛围细节。
- `artifact_shape`: `distill/` 段输出仍是 `第N集.json + 第N集.txt + _manifest.json` 三件套，保留 `reference_images / image_markers` 的 provider-neutral 骨架，脚本只可做投影、校验和兼容迁移辅助。

`N1` 的证据必须写出 `first_frame_digest.status`。若状态不是 `ready`，不得进入 `N2-DISTILL`；若本轮只走 `bind_references` 或 `handoff_provider`，也要记录跳过 distill 的原因和现有请求对象如何满足上述 artifact shape。

## Branch Rules

- `distill_only`: `N1 -> N2 -> N5`
- `bind_references`: `N1 -> N3 -> N5`
- `handoff_provider`: `N1 -> N4 -> N5`
- `full_chain`: `N1 -> N2 -> N3 -> N4 -> N5`
- `compat_migration`: `N1 ->` 仅进入缺失或待投影节点，不补未执行段占位。

## Failure Routes

| failure | route |
| --- | --- |
| detail root 不稳定 | 停止并回 `3-Detail` |
| 目标分镜不存在或多命中 | 停止并回 `N1/N2`，要求明确 `shot_id` 或修上游 |
| prompt/TXT 不满足 LLM 主创或字段覆盖 | 回 `N2` |
| 引用候选歧义 | 停止于 `N3`，输出歧义报告 |
| 引用状态 `unresolved` 却试图 handoff | 回 `N3` |
| provider 未明确且无法推荐主案 | 停在 `N4` 等待用户裁决 |
| review 发现阻断项 | 回对应节点 |
