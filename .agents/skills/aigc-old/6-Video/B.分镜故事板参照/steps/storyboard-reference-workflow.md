# Storyboard Reference Workflow

本文件定义 `B.分镜故事板参照` 的思行一体化节点网络。

## Node Network

| node_id | objective | action | evidence | route_out | fail_code |
| --- | --- | --- | --- | --- | --- |
| `N1-INTAKE` | 判断任务是否属于组级故事板融合包，并为后续蒸馏建立 `全能参照` 配置画像 | 锁定 project、episode、group_scope、mode、output_root；在涉及蒸馏或旧产物判源时读取并摘要 `全能参照` 入口、经验层、`prompt-assembly-spec.md` 与共享图生视频原则 | `3-Detail/<episode>.json` 路径、用户 mode、目标 group_id、`omni_config_profile` | `N2`、`N3`、`N4` | `FAIL-SBREF-ROOT-01` |
| `N2-DISTILL` | 生成组级全能参照 request packet | LLM 主创 prompt/TXT，脚本仅投影/校验，写 `distill/` 三件套 | `distill/<episode>.json`、TXT、manifest | `N3` 或 `N5` | `FAIL-SBREF-DISTILL-02` |
| `N3-BIND` | 将故事板/漫画/主体资产绑定到请求对象 | 扫描 `Assets/`，唯一匹配，重建 `reference_images / image_markers` | `reference-binding/<episode>.json`、match-report、manifest | `N4` 或 `N5` | `FAIL-SBREF-BIND-03` |
| `N4-HANDOFF` | 形成 provider 提交前 handoff 包 | 判定 `reference_driven / prompt_only / unresolved`，写 submit plan/brief | `generation-handoff/<provider>/submit-plan.json`、brief | `N5` 或 `Blocked` | `FAIL-SBREF-HANDOFF-04` |
| `N5-REVIEW` | 汇总三段 gate 与下一入口 | 按 review contract 给 verdict、风险、TODO、next_entry | review verdict、最终回复 | `Done` | `FAIL-SBREF-REVIEW-05` |

## Branch Rules

- `distill_only`：执行 `N1 -> N2 -> N5`。
- `bind_references`：执行 `N1 -> N3 -> N5`，若缺少稳定 source request，则回 `N2` 或兼容旧 `全能参照` 产物。
- `handoff_provider`：执行 `N1 -> N4 -> N5`，若引用状态 `unresolved`，回 `N3`。
- `full_chain`：执行 `N1 -> N2 -> N3 -> N4 -> N5`，任一硬 gate 失败立即停止。
- `compat_migration`：执行 `N1` 后只投影缺失段，不补未执行段占位。

## N1 Omni Config Digestion Gate

`N1-INTAKE` 不只是路由锁定；只要本轮可能触达 `N2-DISTILL`，或需要判断旧 `全能参照` 产物是否能作为稳定来源，就必须先生成 `omni_config_profile`。该 profile 只服务本包执行与审查，不建立新的第二真源。

### Required Source Set

- `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/SKILL.md`
- `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/CONTEXT.md`
- `.agents/skills/aigc/6-Video/1-提示词蒸馏/全能参照/prompt-assembly-spec.md`
- `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md`
- `.agents/skills/aigc/6-Video/B.分镜故事板参照/references/prompt-distillation-contract.md`
- `.agents/skills/aigc/6-Video/B.分镜故事板参照/references/shared-prompt-principles.md`

### Profile Fields

| profile_field | must absorb | N2 consumption |
| --- | --- | --- |
| `canonical_source` | `projects/aigc/<项目名>/3-Detail/第N集.json` 的 `meta + groups[].global/detail.分镜列表` 是唯一业务真源；compat projection 只作派生视图 | 拒绝用旧 helper 视图反向覆盖 canonical detail root |
| `input_integrity_gates` | `document_phase=ready`、目标分镜组非空、组内镜头顺序稳定、镜头数与 `分镜切换` 对齐 | N2 开始前先给 `ready / blocked` verdict |
| `prompt_structure` | 最终 prompt 固定为 `BC`：组级设计块 + 每镜融写行，不保留独立 A 段整组剧本正文 | LLM 写 prompt 时按 BC 结构组织 |
| `txt_render_contract` | `第N集.txt` 按“分镜组ID -> 全局风格/类型元素/导演意图 -> 分镜N，x-y秒 -> 剧本正文 -> 主体锚定 -> 分镜明细 -> 字数统计”渲染 | TXT 是人工审阅主稿，JSON 才是 completeness carrier |
| `group_design_block` | 吸收 `全局风格 / 类型元素 / 导演意图 / 出场角色及穿搭`，并保留固定音频约束 | prompt 顶部形成稳定组级锚点 |
| `shot_opening_template` | 每镜以 `xx秒-xx秒｜分镜<组内序号>：` 开头；完整四段式 ID 只进结构化回链 | prompt 正文不泄露完整分镜 ID |
| `field_priority` | `P0` 剧情桥段、`P1` 主体动作/表演与镜头控制、`P2` 环境摄影、`P3` 视觉组织与兼容补充 | 超限时按优先级压缩，不牺牲剧情桥段和镜头控制 |
| `compression_levels` | `full / normal / tight / ultra` 与 1600-1900 字窗口；预算未紧张时默认自然句 | 避免过早短语化或硬裁字段 |
| `dialogue_clause_rule` | 有 `对话戏` 或说话信号时补“谁在说 / 话头落点 / 稳定短引号词” | 对白存在感不得被镜头动作吞没 |
| `hidden_field_title_rule` | 除组/镜序号外不暴露字段标题，也不得隐性按字段顺序串联 | N2 审查标题泄露和字段顺排痕迹 |
| `shared_i2v_principles` | 主体锚点、场景/风格、镜头起势、可见动作、运动速度、光感道具、构图重心与镜间衔接的图生视频顺序 | prompt 更像视频模型指令，而不是字段转述 |
| `branch_owned_first_and_legacy_fallback` | 优先消费 branch-owned canonical 字段；legacy 字段只作 fallback | 防止旧字段重新升格为主真源 |
| `reference_skeleton` | `reference_images: []` 与 `image_markers` 顺序承接骨架保留，但不虚构图片引用 | N3 再绑定真实 `Assets/` 路径 |
| `script_authorship_boundary` | 旧 `generate_episode_packets.py` 只可做兼容投影、校验、统计、manifest，不可主创 prompt/TXT | 防止脚本主创回流 |

### Evidence And Failure

- `N1` 输出必须能在工作记录、manifest 或 review 摘要中回放 `omni_config_profile` 的来源文件与关键取舍。
- 若缺少 `prompt-assembly-spec.md`、共享图生视频原则或 `全能参照/CONTEXT.md` 任一关键来源，`N1` 必须标记 `blocked` 或显式降级为 `compat_migration`，不得直接进入 N2。
- 若用户只要求 `bind_references` 或 `handoff_provider`，且已有稳定 request JSON，`N1` 可把 `omni_config_profile` 标为 `not_required_by_mode`；但一旦要判定旧请求是否稳定，仍需至少读取 `全能参照/SKILL.md + CONTEXT.md` 与 request template 相关约束。

## Evidence Gates

- 每个执行段都必须写明 source path、output path、verdict。
- 未执行段必须标记 `skipped_by_mode`，不得伪造空产物。
- 阻断时必须给出 rework entry，而不是继续猜测下游。
