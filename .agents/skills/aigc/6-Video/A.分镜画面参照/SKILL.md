---
name: aigc-video-frame-visual-reference
description: Use when the AIGC 6-Video workflow needs one fused frame visual reference package that distills first-frame request JSON, binds Assets references, and prepares provider handoff without removing the legacy three-step skills.
governance_tier: full
---

# aigc 6-Video / A.分镜画面参照

`A.分镜画面参照` 是 `6-Video` 阶段的帧级融合型 Skill 2.0 包。它把用户指定的旧链路三段能力收束到一个受治理入口内：

1. `1-提示词蒸馏/首帧参照`
2. `2-参照引用`
3. `3-视频生成`

原三个技能包保留不删除；本包只建立新的融合入口、分区真源、输出合同和回接路径。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或明确报告阻塞；不得在未检查经验层的情况下执行。
- 若当前任务绑定 `projects/aigc/<项目名>/`，还必须先加载项目根 `MEMORY.md`，再按需读取项目根 `CONTEXT/` 中与视频阶段相关的上下文。
- 冲突优先级：用户显式请求 > 根 `AGENTS.md` / meta 规则 > `.agents/skills/aigc/SKILL.md` > `.agents/skills/aigc/6-Video/SKILL.md` > 本 `SKILL.md` > `references/` / `steps/` / `types/` / `review/` / `templates/` > `agents/openai.yaml` > 项目记忆与项目上下文 > 本 `CONTEXT.md`。
- 新的稳定失败模式、成功模式和可复用策略先写回本 `CONTEXT.md`；若升级为强制合同，再晋升到本 `SKILL.md` 或对应分区。

## Input Contract

Accepted input:

- 需要把 `projects/aigc/<项目名>/3-Detail/第N集.json` 中的单一 `分镜ID` 或一组帧级目标，整理成可用于视频生成的首帧/分镜画面参照包。
- 需要在同一技能入口内完成“首帧 prompt/TXT 蒸馏 -> `Assets/` 参照图绑定 -> provider submit-plan/brief”三段串联。
- 需要保留旧三段技能的语义，但希望新任务优先进入一个帧级融合包。
- 需要修复、复核或续跑 `A.分镜画面参照` 的阶段产物。

Required input:

- `project_name`
- `episode_id`，例如 `第1集`
- canonical detail root：`projects/aigc/<项目名>/3-Detail/<episode_id>.json`
- 明确的执行目标：`distill_only`、`bind_references`、`handoff_provider`、`full_chain` 或 `compat_migration`

Optional input:

- `shot_id` / `分镜ID`；若未提供，可按 episode carrier 批量处理命中的帧级请求。
- provider 偏好，例如 `dreamina`、`vidu`、`veo`、`sora`、`seedance`、`kling`、`grok`
- 是否允许纯 prompt 路径：`prompt_only` / `no_reference`
- 已选定或待绑定的 `Assets/` 资产范围
- 既有旧链路产物路径，用作兼容迁移输入

Reject or reroute when:

- `3-Detail/<episode_id>.json` 尚未形成稳定 `meta + groups[].global/detail.分镜列表`。
- 当前任务是整组视频请求蒸馏，且用户明确要组级全能参照；此时回到父级 `6-Video` 路由。
- 用户要求生成、挑选或重命名图片资产本体；本技能只绑定已存在的 `Assets/`。
- 任务已经是 provider 运行时提交、轮询、下载或报错排查；应进入对应 provider 技能或外部工具。

## LLM-First Creative Authorship Contract

- 首帧/单镜视频 prompt、`第N集.txt` 主稿、provider handoff 简报中的创作性描述，必须由 LLM 直接完成。
- `scripts/` 只能承担读取、校验、投影、格式转换、路径审计、台账生成等机械辅助；不得用规则拼接替代提示词、分镜画面描述或审美压缩判断。
- 旧 `首帧参照/scripts/generate_episode_packets.py` 只作为 legacy helper 来源，不得被本包重新设为默认主创执行器。
- 若临时复用旧脚本，必须显式说明它是兼容迁移或校验辅助，且不得把脚本输出视为 canonical creative truth。

## Mode Selection

| mode | 触发信号 | 主动作 | 输出范围 |
| --- | --- | --- | --- |
| `distill_only` | 只需从 `3-Detail` 生成帧级视频请求对象和 TXT | 执行首帧 prompt/TXT 蒸馏，不绑定 Assets，不写 provider plan | `distill/` |
| `bind_references` | 已有稳定帧级请求对象，需要补 `reference_images / image_markers` | 执行资产匹配、歧义阻断、引用字段重建 | `reference-binding/` |
| `handoff_provider` | 请求对象和引用状态已稳定，需要提交前组织 | 写 provider 路由、`submit-plan.json`、`submit-brief.md` | `generation-handoff/` |
| `full_chain` | 用户要求一次完成分镜画面参照包 | 串行执行蒸馏、参照绑定、生成交接；任一 gate 失败即停机 | 三段全部落盘 |
| `compat_migration` | 从旧三段链路迁移或补全缺件 | 读取旧产物，按本包结构投影并标明来源 | 对应缺失分区 |

## Reference Loading Guide

| 场景 | 读取文件 |
| --- | --- |
| 追踪旧三段内容如何融合进新包 | `references/source-fusion-map.md` |
| 执行首帧 prompt/TXT 蒸馏 | `references/prompt-distillation-contract.md`、`references/shared-prompt-principles.md` |
| 执行 `Assets/` 参照图绑定 | `references/reference-binding-contract.md` |
| 组织 provider handoff | `references/provider-handoff-contract.md` |
| 判断 `distill_only / bind_references / handoff_provider / full_chain / compat_migration` | `types/type-map.md` |
| 执行串行主链与失败回路 | `steps/frame-visual-reference-workflow.md` |
| 交付前审查 | `review/review-contract.md` |
| 复用经验与避坑 | `knowledge-base/video-reference-heuristics.md` 与同目录 `CONTEXT.md` |
| 渲染输出 | `templates/output-template.md`、`templates/request-packet.template.json`、`templates/submit-plan.template.json` |
| 机械辅助 | `scripts/README.md` |
| 产品侧入口 | `agents/openai.yaml` |

## Visual Maps

```mermaid
flowchart TD
    A["3-Detail/<episode>.json + optional shot_id"] --> B{"Mode Selection"}
    B -->|"distill_only / full_chain"| C["N2 首帧参照蒸馏"]
    C --> D["distill/第N集.json + txt + manifest"]
    B -->|"bind_references / full_chain"| E["N3 参照引用绑定"]
    D --> E
    E --> F["reference-binding/第N集.json + manifest + match-report"]
    B -->|"handoff_provider / full_chain"| G["N4 Provider Handoff"]
    F --> G
    G --> H["generation-handoff/<provider>/submit-plan + brief"]
```

```mermaid
stateDiagram-v2
    [*] --> Intake
    Intake --> SourceGate
    SourceGate --> FrameDistilled
    FrameDistilled --> ReferenceBound
    ReferenceBound --> HandoffReady
    HandoffReady --> Reviewed
    Reviewed --> [*]
    SourceGate --> Blocked
    ReferenceBound --> Blocked
    HandoffReady --> WaitingForProviderChoice
```

## Execution Contract

1. 锁定项目根、集号、目标 `shot_id` 范围、执行模式与输出根，并完成旧 `首帧参照` 的入口消化，形成 `first_frame_digest`；不得只把旧技能路径当作来源占位。`first_frame_digest` 至少覆盖：
   - `1-提示词蒸馏/首帧参照/SKILL.md + CONTEXT.md + prompt-assembly-spec.md` 中的单镜边界：`单一 shot_id -> 1 条帧级请求对象`。
   - 首帧输入门：`document_phase=ready`、目标 `分镜ID` 唯一命中、所属组 `分镜切换 == len(分镜明细[])`、时间段为当前分镜组内相对秒位。
   - 桥段与 prompt 语义：`正文切分参考[] -> 正文回指 -> 剧情桥段`、`BC` 结构、`xx秒-xx秒｜分镜<组内序号>：`、字段标题隐藏、完整四段式 `分镜ID` 只留结构化回链。
   - TXT 与预算语义：一镜版固定 TXT block、`G1/P0/P1/P2/P3` 压缩优先级、非 `tight` 时把余量转为当前分镜细节密度。
   - handoff 形状：`第N集.json + 第N集.txt + _manifest.json` 三件套、`reference_images / image_markers` provider-neutral 骨架、脚本只做投影/校验。
2. 读取 `.agents/skills/aigc/SKILL.md + CONTEXT.md`、父级 `6-Video/SKILL.md + CONTEXT.md`、本 `SKILL.md + CONTEXT.md`，再按 `Reference Loading Guide` 加载分区。
3. 对 `3-Detail/<episode>.json` 做输入门检查：只消费稳定 canonical detail root，不把 compat projection 当第一真源。
4. 进入 `distill_only` 或 `full_chain` 时，由 LLM 主创生成首帧 prompt/TXT；脚本只可做投影与校验。
5. 进入 `bind_references` 或 `full_chain` 时，优先按 `shot_id -> Assets/分镜画板/分镜帧/` 绑定真实文件；无匹配可保守跳过，歧义候选必须阻断。
6. 进入 `handoff_provider` 或 `full_chain` 时，先判定引用状态是 `reference_driven`、`prompt_only` 还是 `unresolved`；`unresolved` 必须回 `reference-binding`。
7. 每段产物都写入 `projects/aigc/<项目名>/6-Video/A.分镜画面参照/<episode_id>/` 下的声明子目录。
8. 最终只给一个下一入口：provider skill、人工提交、回 `reference-binding`、回 `3-Detail` 或等待 provider 裁决。

## Field Mapping

### Field Master

| field_id | 输出位置/字段 | 内容要求 | 默认责任节点 | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- |
| `FIELD-FVISREF-ROOT-01` | `mode / source_root / output_root / shot_scope / first_frame_digest` | 锁定项目、集号、帧级目标、模式、唯一输出根，并消化旧 `首帧参照` 的输入门、桥段、prompt/TXT、预算与三件套形状 | `N1` | 路由清晰度与源语义吸收度 | `FAIL-FVISREF-ROOT-01` |
| `FIELD-FVISREF-DISTILL-02` | `distill/<episode>.json + txt + _manifest.json` | 首帧 prompt/TXT 由 LLM 主创，覆盖目标分镜所属组与当前分镜事实，不虚构引用 | `N2` | 蒸馏完整度 | `FAIL-FVISREF-DISTILL-02` |
| `FIELD-FVISREF-BIND-03` | `reference-binding/<episode>.json + match-report.md` | `reference_images / image_markers` 只绑定真实 `Assets/` 路径，帧级画板优先，顺序稳定 | `N3` | 引用可信度 | `FAIL-FVISREF-BIND-03` |
| `FIELD-FVISREF-HANDOFF-04` | `generation-handoff/<provider>/submit-plan.json + submit-brief.md` | 明确 provider、`input_mode`、引用解析策略与唯一下一入口 | `N4` | 交接可执行性 | `FAIL-FVISREF-HANDOFF-04` |
| `FIELD-FVISREF-REVIEW-05` | `review verdict / final response` | 三段证据、失败回路、残余风险和降级路径齐备 | `N5` | 结案可复核性 | `FAIL-FVISREF-REVIEW-05` |

### Thought Pass Map

| node_id | 聚焦字段 | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| `N1` | `FIELD-FVISREF-ROOT-01` | 当前任务是否应进入帧级融合包，以及走哪种 mode | 锁定 project/episode/shot_scope/mode/source/output，并输出 `first_frame_digest` | 多入口并列、输出根不清、旧首帧语义未消化 |
| `N2` | `FIELD-FVISREF-DISTILL-02` | 目标分镜能否稳定转为首帧视频请求对象 | LLM 生成 prompt/TXT，写三件套与追溯 manifest | 脚本主创、漏镜、字段标题泄露 |
| `N3` | `FIELD-FVISREF-BIND-03` | 哪些图片引用能安全绑定到该帧 | 扫描 `Assets/`、唯一匹配、重建 marker | 猜测性绑定、外部路径、占位残留 |
| `N4` | `FIELD-FVISREF-HANDOFF-04` | 当前请求如何交给 provider | 写 submit plan/brief 与 provider-specific 解析策略 | 直接下命令、provider 槽位冒充能力 |
| `N5` | `FIELD-FVISREF-REVIEW-05` | 三段是否能作为一个交付包结案 | 按 review gate 汇总 verdict、风险和下一入口 | 只有路径清单，没有失败回路 |

### Pass Table

| field_id | Pass Standard | Fail Code | Rework Entry |
| --- | --- | --- | --- |
| `FIELD-FVISREF-ROOT-01` | 项目、集号、shot scope、mode、source root、output root 与 `first_frame_digest` 均明确 | `FAIL-FVISREF-ROOT-01` | `N1` |
| `FIELD-FVISREF-DISTILL-02` | prompt/TXT 完成目标分镜桥段、组级空气层与镜级事实覆盖，`prompt_char_count` 可复核，JSON/TXT/manifest 齐备 | `FAIL-FVISREF-DISTILL-02` | `N2` |
| `FIELD-FVISREF-BIND-03` | 引用字段只含真实 `Assets/` 路径或明确空绑定；歧义阻断有报告 | `FAIL-FVISREF-BIND-03` | `N3` |
| `FIELD-FVISREF-HANDOFF-04` | `submit-plan.json` 和 `submit-brief.md` 都能支持唯一下一入口 | `FAIL-FVISREF-HANDOFF-04` | `N4` |
| `FIELD-FVISREF-REVIEW-05` | review verdict 为 `pass` 或 `pass_with_todo`，且 TODO 不阻断交付 | `FAIL-FVISREF-REVIEW-05` | `N5` |

## Root-Cause Execution Contract (Mandatory)

当出现失败时，必须沿以下链路上溯：

`Symptom -> Direct Technical Cause -> Section Owner -> Source Contract -> Meta Rule Source`

优先检查：

1. Step 1 只锁定路径/模式，没有形成 `first_frame_digest`：回本 `Execution Contract` Step 1、`references/source-fusion-map.md` 与 `steps/frame-visual-reference-workflow.md#N1`。
2. prompt/TXT 由脚本主创、漏字段或不自然：回 `references/prompt-distillation-contract.md` 与 `steps/frame-visual-reference-workflow.md#N2`。
3. 引用绑定出现猜测、外部路径或占位残留：回 `references/reference-binding-contract.md` 与 `steps/frame-visual-reference-workflow.md#N3`。
4. 已有请求却直接跳 provider 命令：回 `references/provider-handoff-contract.md` 与 `steps/frame-visual-reference-workflow.md#N4`。
5. 三段旧包迁入后语义丢失：回 `references/source-fusion-map.md`。
6. 质量门没有阻断：回 `review/review-contract.md`。
7. 同类经验可复用：写入本 `CONTEXT.md` 或 `knowledge-base/video-reference-heuristics.md`。

Meta rule source:

- 根 `AGENTS.md`
- `.agents/skills/aigc/SKILL.md`
- `.agents/skills/aigc/6-Video/SKILL.md`
- `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/SKILL.md`

## Output Contract

Required output:

- 一个融合型分镜画面参照包，至少包含当前 mode 对应的 canonical artifacts，并保留 `首帧参照 + 2-参照引用 + 3-视频生成` 三段旧链路的来源映射。

Output format:

- Markdown 合同与报告、JSON 请求对象、JSON manifest、provider `submit-plan.json`、Markdown `submit-brief.md` 与最终用户闭环摘要。

Output path:

- 技能包：`.agents/skills/aigc/6-Video/A.分镜画面参照/`
- 项目运行时：`projects/aigc/<项目名>/6-Video/A.分镜画面参照/<episode_id>/`
- 蒸馏段：`distill/<episode_id>.json`、`distill/<episode_id>.txt`、`distill/_manifest.json`
- 参照绑定段：`reference-binding/<episode_id>.json`、`reference-binding/_manifest.json`、`reference-binding/match-report.md`
- 生成交接段：`generation-handoff/<provider>/submit-plan.json`、`generation-handoff/<provider>/submit-brief.md`

Naming convention:

- skill frontmatter 使用 `aigc-video-frame-visual-reference`。
- 技能目录保留用户指定名 `A.分镜画面参照`。
- 运行时 episode 目录使用原始 `第N集` 命名；provider 目录使用小写 provider id。
- 不修改、移动或删除旧目录 `1-提示词蒸馏/首帧参照`、`2-参照引用`、`3-视频生成`。

Completion gate:

- `scripts/skill_context_audit.py --strict` 不因本包新增文件失败。
- `/Users/vincentlee/.codex/skills/meta/构建/技能/skill-工作车间/scripts/validate_skill_2_0.py .agents/skills/aigc/6-Video/A.分镜画面参照` 通过。
- 若注册为 AIGC governed leaf，`python3 scripts/aigc_skill_audit.py --strict` 至少不因本包结构、上下文、root-cause、Field Master、Thought Pass Map 或 Pass Table 失败。
- 若上层策略阻断默认 reviewer/subagent，必须报告降级来源与本地 review checklist 结果。
