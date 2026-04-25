# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `4-Design/场景` 的经验层知识库，不是执行日志。
- 调用本技能时，应在父级 `4-Design/2-设计`、共享输入合同、`1-清单/场景` 之后加载本文件。
- 优先级固定为：用户显式请求 > `AGENTS.md` / meta 规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 直接把旧仓 `3-设定/2-设计/场景设计` 路径复制进当前仓 | runtime 迁移层 | 改为 `projects/aigc/<项目名>/4-Design/场景/2-设计/第N集/` | 在 `SKILL.md` 的 Parent Positioning 与 Output Contract 固化当前仓 runtime | 输出不再指向 `output/影片/.../3-设定` |
| 只读 `场景清单.json`，丢失旧仓 research / bridge 密度 | 输入装配层 | 以清单为对象根，同时强建议读取 `场景研究.json + scene_design_bridge.json` | 在 `Total Input Contract` 与 reference 装配规则中固定三真源消费顺序 | `source_trace` 能显示 catalog/research/bridge 状态 |
| `场景研究.json` 或 `scene_design_bridge.json` 缺失时静默继续 | 降级治理层 | 在 `quality_flags` 和 `_manifest.json.notes` 写入 `research_degraded / bridge_degraded` | Pass Table 固定 `manifest` 审计门 | 下游能看出本轮是否保守降级 |
| Scene Style 复述全局风格，没有完成场景领域适配 | 风格转译层 | 以 `2-Global/全局风格` 为基调，重写为空间纵深、材质、体积光、天气时态和环境叙事 | `FIELD-SCN-DES-03` 固定 Style Backbone 与 Scene Style 分工 | `scene_style` 不是抽象风格词 |
| 场景类型被恢复成 `室内/室外/野外` 多技能拆分 | 技能边界层 | 收回单一 `场景` leaf，把类型降为 `scene_type` 字段 | `Completion Criteria` 与 `Detailed Assembly Rules` 禁止多技能分裂 | source-layer 只有一个 `2-设计/场景` leaf |
| 强文化原型场景只靠氛围词生成 | 查证与保守模式层 | 命中寺庙、祠堂、祭坛、阴司桥渡等原型时，先查制式、仪轨组件、材料与禁忌 | `references/scene-design-assembly.md` 固定外部查证触发条件 | `source_trace.external_verification` 或保守说明非空 |
| Markdown 与 `scene_design.json` 互相漂移 | 输出投影层 | 以 `scene_design.json` 回投 Markdown；prompt 只从结构化字段汇流 | Template Binding Contract 固定 Markdown 是 projection | `design_prompt == prompt` 且 Markdown 三段齐全 |
| 场景设计文件存在但没有同名图片或图片 prompt 缺全局风格前缀 | 自动生图层 | 以 `[场景名].md` 的 `prompt整合` 加 `2-Global/全局风格` 生成 `full_generation_prompt` | 在 `SKILL.md` 回指共享输出合同并新增 `FIELD-SCN-DES-12` | `[场景名].<ext>` 与 `[场景名].md` 同目录同 stem |
| 场景模板被当前仓重排为非原参照字段 | template drift layer | 用 `.md` 直接承接 AIGC-ZEN-VOID `scene_masterprompt.structured.v2` 结构 | `SKILL.md` 固定引用 `templates/scene_masterprompt.structured.v2.md`，只允许在 `prompt整合` 加全局前缀 | Markdown 章节顺序为 `物语 -> 解构 -> Scene Design -> Cinematography -> prompt整合` |
| `prompt整合` 只拼接全局前缀和局部场景 prompt，或 Integrated prompt 过短 | prompt integration layer | 改为约 2000 bytes 英文自然语言整合同模板上方全部内容 | Template Binding Contract 固定覆盖 `解构 / Scene Design / Cinematography`，并用校验器卡住非 ASCII 与 1800-2200 bytes | `prompt整合` 英文段落含空间结构、材质、氛围、构图和镜头 |
| 场景参照图混入角色或人群，导致后续背景引用带人物污染 | reference cleanliness layer | 将场景 prompt 固定为空镜头环境图 | `SKILL.md / references / validate_scene_design_projection.py / build_scene_design_packets.py` 固定 `empty environmental shot` 与 `no characters` | scene prompt 不要求人物、角色、人群、手部或表演动作入画 |
| 空镜规则只在 prompt 末尾禁止人物，`N6-CAMERA` 仍把剧情动作当成画面主体 | thinking-action node layer | 在 `N6-CAMERA` 先把人物动作转写为空间痕迹、动线、环境状态或物体尺度线索 | `Thinking-Action Node Contract` 登记 `scene_empty_shot_note`，`N7/N10` 复验 `reference_cleanliness_note` | prompt 中没有正向人物动作，且含 `empty environmental shot / no characters` |
| 场景 Markdown 批量输出绕过 `scene_masterprompt.structured.v2.md`，只生成简化 bullet 卡 | executable gate layer | 增加 `scripts/build_scene_design_packets.py` 从模板填槽，并用 `scripts/validate_scene_design_projection.py` 检查关键章节 | `SKILL.md` 将渲染器和校验器升为显式入口；`_manifest.json.template_validation.status` 必须为 `success` | 11 个第1集场景 Markdown 均含 `Reasoning Pivot / ## Scene Design ## / ## Cinematography ## / **prompt整合**` |
| 场景设计脚本遇到新项目场景名时把中文透传进 `prompt整合` | prompt localization layer | 为 `build_scene_design_packets.py` 增加项目感知场景名/风格兜底、非 ASCII 过滤与恐怖出租屋 period-region 判型 | `prompt整合` 的生成链必须先转写为英文 ASCII，再进入模板和 `full_generation_prompt` | `validate_scene_design_projection.py` 不再报 Chinese/non-ASCII prompt |
| 场景输出写完后仍继续进入 `team.yaml` 驱动的监制 closeout | council closeout layer | 在 `S11/N11` 固定读取项目根 `team.yaml`，但只写明当前轮 closeout 已不再由 `监制` 执行 | 用 `_shared/subagent-supervision-contract.md` 固定停用边界 | 当前轮场景输出完成后可回溯 `post_write_audit_note` |
| 场景 post-write 问题无法定位具体失真槽位 | slot-level audit governance layer | 先把当前轮目标解析成 `SCENE-BUNDLE-01~04`，再写 audit note | `_shared/design-slot-review-contract.md` 固定 bundle 命名、carrier 边界与记录顺序 | audit 结论能区分是 `story-world`、`design-structure`、`cinematography` 还是 `prompt-cleanliness` bundle 失真 |

## Repair Playbook

1. 先检查 `场景清单.json` 是否存在并含 `scenes[]`。
2. 再检查 `场景研究.json / scene_design_bridge.json` 是否存在；缺失时只允许保守降级并留痕。
3. 锁定 `scene_id / scene_name / scene_type` 后，再读取 `0-Init / 2-Global` 装配故事支点和 Style Backbone。
4. 进入设计前先写或至少形成 thinking sidecar 的三层收敛：原型与风格骨架 -> 结构材料动线 -> 氛围构图镜头。
5. 结束前复核 `scene_design.json`、Markdown、`_manifest.json` 三者路径、数量和 prompt alias 是否一致。
6. 运行 `scripts/validate_scene_design_projection.py --output-dir <场景设计输出目录>`；只有 `_manifest.json.template_validation.status == success` 才能进入面板或自动生图。
7. 自动生图前检查 `reference_cleanliness_note`：缺 `empty environmental shot / no characters` 或出现正向人物、人群、手部、表演动作时，回到 `N6/N7`。
8. 最后用 `run_design_auto_image.py --design-file <场景名>.md` 检查同目录同名图片是否能由完整 prompt 生成。
9. 当前轮场景 canonical 输出与 projection 落盘后，再读取项目根 `team.yaml` 做 `N11-POST-WRITE-AUDIT-NOTE`；图片状态只作证据。
10. `N11` 先确认 post-write closeout 已不再由 `监制` 执行，再决定是否补写 audit note / acceptance handoff。
11. 进入 `N11` 前，先按 `_shared/design-slot-review-contract.md` 将目标文件解析成 `SCENE-BUNDLE-*`；若无法解析，先修 mapping，不直接写泛化审计意见。

## Reusable Heuristics

- 场景设计迁移最稳的做法不是复刻旧仓路径，而是复刻旧仓字段密度与质量门，再把输入输出接到当前仓 `4-Design` runtime。
- `场景清单.json` 负责告诉本阶段“设计哪个场景”，`场景研究.json` 负责“凭什么这样设计”，`scene_design_bridge.json` 负责“如何直达设计”；三者缺一时都要显式降级。
- `Scene Style` 是全局风格的场景专业偏转，不是全局风格原文摘要。
- 场景 prompt 的质量通常由“原型锁定 -> 参照转译 -> 结构材料动线 -> 镜头参数”决定；先写氛围词最容易导致泛化。
- 对历史、宗教、民俗、神话空间，宁可保守写制式和禁忌，也不要用现代建筑大师或空泛东方感兜底。
- 场景自动图不是面板图；它只验证单一场景主体概念是否可生成，默认不处理 3x3 layout 或多镜头排版。
- 场景 Markdown 模板不要为当前项目临时增加新的结构性小节；如需补充字段，优先映射到原参照模板现有槽位。
- 场景 `prompt整合` 应像导演给图像模型的一段约 2000 bytes 英文场景 brief：从 `物语` 和 `解构` 整合空间事实、镜头事实和风格事实，不要把中文字段逐条粘贴，也不要加入人物/角色/人群。
- 批量脚本的英文 prompt 兜底必须面向“项目类型”而不只是面向上一轮样本；遇到未登记中文场景名时，应降级为英文 generic 场景锚，而不是把中文原文透传进 `Integrated prompt`。
- 场景自动图是环境参照资产，默认必须是 `empty environmental shot`；即使上游剧情含角色动作，也只能转写为空间痕迹、动线或环境状态。
- 空镜不是 prompt 末端的否定词，而是摄影节点的取景前提；先决定“没有角色主体的空间怎么仍然可读”，再写 Integrated prompt。
- 场景 leaf 只写“模板必须绑定”还不够；凡模板是质量门，必须同时有渲染器和 validator，否则批量任务会自然滑向临时 Markdown 拼接。
- 场景输出后的 post-write 问题不再看 `roles.supervision.members`；这些成员只作用于前置 advisory。
- 对场景这种 machine-first truth + Markdown projection 双载体输出，最稳的后置审计粒度不是“评哪个文件”，而是“记哪个 slot bundle”；文件只负责承载 bundle，不负责定义 bundle。
