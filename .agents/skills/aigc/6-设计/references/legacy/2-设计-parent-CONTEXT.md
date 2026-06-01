# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/6-设计/2-设计` tranche parent 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/6-设计/2-设计/SKILL.md` 时，应自动预加载本文件。

## Context Health

- soft_limit_chars: 18000
- hard_limit_chars: 36000
- status: ok
- last_checked_at: 2026-04-15

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| `2-设计` 直接回读 `3-Detail`，绕过 `1-清单` | tranche input layer | 回到 `1-清单/*.json` 作为第一输入 | 在 `_shared/design-input-contract.md` 固化三层输入口径 | `2-设计` 不再重新猜对象池 |
| `0-Init` 与 `2-Global` 风格信号互相覆盖 | upstream responsibility layer | 按 `2-Global > north_star > init_handoff` 重排优先级 | 在共享输入合同中显式写死优先级 | Style Backbone 不再漂移 |
| `[角色名].md` 与 `character_design.json` 内容不一致 | output projection layer | 以结构化真源回写 Markdown 投影 | 在 leaf 合同中固定 machine-first canonical truth | 人读稿不再成为第二真源 |
| leaf 已回迁，但父层仍宣称 pending | stage coverage layer | 更新 tranche parent 与 `6-设计` 父层 coverage 状态 | 在阶段总线上同步 stage coverage status | source-layer 状态与实体一致 |
| 场景设计 leaf 直接复刻旧仓 `3-设定` 路径 | migration adapter layer | 把旧仓字段密度迁移到当前 `6-设计/场景/2-设计` runtime | 在 `场景/SKILL.md` 固化当前仓输入输出路径，父层只声明 active leaf 与 handoff | 输出路径不再指向旧 `output/影片/.../3-设定` |
| 设计文件已落盘但没有自动生图，或生图 prompt 缺全局风格前缀 | output fast-path layer | 从主体设计文件生成 `full_generation_prompt`，再调用内置 imagegen 输出同目录同名图片 | `_shared/design-output-contract.md` 与 `run_design_auto_image.py` 只负责内置 imagegen request sidecar；Codex 会话用 `GPT-IMAGE-2` 口径生成并复制回项目 | 每个主体文件旁边存在同 stem 图片，manifest 记录 `auto_image.provider_skill=imagegen` |
| 批量输出中只生成了部分同 stem 图片，但 manifest 仍把自动生图写成成功 | auto-image completion aggregation layer | 用 `ensure_design_auto_images.py` 逐 Markdown 检查同 stem 图片，缺图就补跑或标失败 | 批量完成判定统一为“每个设计 Markdown 都有同 stem 图片”，leaf runner 不再各自聚合成功状态 | `_manifest.json.auto_image.missing_design_files=[]` 且 `status=success` |
| `full_generation_prompt` 的全局风格前缀混入 YAML frontmatter、章节说明、类型元素或设计元素文本 | prefix extraction layer | 只提取 `2-Global/全局风格.md` 中 `- 全局风格：` 的字段值 | 用 `_shared/scripts/global_style_prefix.py` 作为共享提取器，并让 leaf runner / auto-image helper 复用它 | prompt 中 `全局风格前缀：` 后紧跟一段项目风格正文，不出现 `project_name:`、`# 类型元素` 或模板说明 |
| `全局风格.md` 写成裸行 `全局风格:`，导致 `6-设计/2-设计` 无法提取统一前缀 | upstream format drift layer | 将项目风格文件规范化为 `## JSON 直接提取字段` 下的 `- 全局风格：...` | 共享提取器在失败时检测非规范裸行并输出可执行修复提示；上游 `2-Global` 必须继续服从模板字段 | `global_style_prefix.py <全局风格.md>` 成功返回前缀 |
| 全局风格字段本身已带句号时下游拼接成双句号 | prompt assembly layer | 拼接前检查结尾标点，只在缺失时补句号 | 设计脚本将前缀字段视为完整句，不额外无条件追加标点 | prompt 中前缀段以单个句号结束 |
| 子技能 Markdown 模板偏离 AIGC-ZEN-VOID 原参照结构 | template source layer | 将三份原参照直接迁入当前 `templates/*.md`，仅在 `prompt整合` 内加入全局风格前缀槽位 | 子技能 `SKILL.md` 严格引用 `.md` 模板；脚本必须从模板渲染，不能手工拼第二结构 | `rg` 无 `.txt` 旧引用，Markdown 含原参照章节顺序 |
| 旧式输出模板 reference 形态像第二份落盘模板，容易和 `templates/*.structured.v2.md` 抢权 | template canonical source layer | 直接移除旧式输出模板 reference，不再保留替代说明载体 | `_shared/design-output-contract.md` 增加 `Markdown Template Registry`，`aigc_skill_audit.py --strict` 检查旧式输出模板 reference 不得回流 | 只有三份 `templates/*_masterprompt.structured.v2.md` 承载完整落盘结构 |
| `prompt整合` 被误解为局部主体 prompt 拼接或短 prompt 摘要 | prompt integration layer | 改为对同一模板上方全部内容做英文自然语言整合 | 共享输出合同与三类子技能模板绑定合同固定 `Global style prefix + Integrated prompt`，并要求 `Integrated prompt` 完全英文、1800-2200 UTF-8 bytes、覆盖 `解构` 信息 | `prompt整合` 为约 2000 bytes 的英文连贯段落，覆盖结构、材质、镜头/摄影与负面约束 |
| 单主体参照图混入人物、手部或场景背景，导致后续面板/图像阶段污染 | reference cleanliness layer | 按域固定参照图纯净模式：场景为空镜头、道具为纯道具图、角色为纯色背景 | `_shared/design-output-contract.md` 增加 Reference Image Cleanliness Contract；场景/角色 validator 检查英文锚句，场景/道具 builder 固定锚句 | prompt 含 `empty environmental shot / no characters`、`isolated pure prop view / no hands / no characters`、或 `solid color background / no scene background elements` |
| 参照图洁净只写在输出规则，思维·执行节点仍按剧情剧照思路装配 prompt | thinking-action contract layer | 将洁净判断前移到 leaf 的摄影/设计卡 synthesis 节点，并在 prompt 与 auto-image 节点复验 | `_shared/design-output-contract.md` 增加 Thinking-Action Placement Contract；父层与三 leaf Field/Pass/Node 表登记 `reference_cleanliness_note` | 节点证据能说明污染词已被转写，且自动生图前已复验锚句 |
| 单主体自动生图 provider 长时间无响应，导致 `2-设计` 父级 pipeline 卡死 | provider timeout layer | 中断当前远端等待，将本轮 manifest 标为 `auto_image.failed/timeout`，继续交付可追踪设计真源与后续 layout dry-run | `run_design_auto_image.py` 增加默认 `--timeout`，超时返回 124 并输出明确错误，避免批量链路无限挂起 | 真实生图失败时命令能在超时窗内退出，manifest 与 validation-report 明确记录 provider timeout |
| 多主体设计批量生图仍直调 API 或远端 provider，导致 `2-设计` pipeline 依赖 API key / 网络 | execution mode layer | 将缺图 Markdown 聚合成 `design_auto_image_batch.json`，默认交给内置 imagegen 执行 | 共享 `image-generation-execution-contract.md` 固定 `codex-builtin-imagegen`；`ensure_design_auto_images.py` 默认只写 request sidecar 与 `request_ready` 状态 | `_manifest.json.auto_image.status=request_ready` 且含 `provider_skill=imagegen`、`default_model=GPT-IMAGE-2`、`request_batch_path` |
| 设计输出写完后仍继续进入 `team.yaml` 驱动的监制 closeout | council closeout layer | 在父层 `S6` 固定写明 `roles.supervision` 已停用为 post-write owner | 用 `_shared/workflow-supervision-contract.md` 作为停用占位真源，而不是 closeout 执行器 | 当前轮输出完成后只回溯 `post_write_audit_note` |
| 把 `6-设计` 的 post-write audit、final-stage review gate 与 `source_skill_refs` 混成一条 reviewer 权限线 | council runtime layering | 先收回 closeout reviewer 语义，再把 `source_skill_refs` 降为领域提示 | shared contract、`6-设计/SKILL.md` 与 `2-设计` 父/leaf 合同统一采用“停用 closeout + 保留 slot bundle 审计语义” | reviewer roster 不再成为当前轮 closeout 前提 |
| post-write 问题只能说“某个文件有问题”，无法定位到模板槽位或 canonical slot | slot-level audit governance layer | 保留 `_shared/design-slot-review-contract.md`，把当前轮输出从文件级 bundle 细化到 slot bundle | 父层、leaf 与占位合同统一回指 slot bundle 真源，audit note 默认带 `bundle_id` | 后置问题仍可定位到 `SCENE/ROLE/PROP-BUNDLE-*` |
| slot-bundle 合同已经写进父层/leaf，但 audit 仍全绿，因为没有任何执行器真正消费它 | audit-execution parity layer | 新增 `_shared/scripts/resolve_design_slot_bundles.py` 作为最小执行载体，并让 `scripts/aigc_skill_audit.py --strict` 显式检查 resolver + contract + `slot_bundles/slot_bundle_findings` | 对新增 shared contract，必须同时落三处：规范文档、执行脚本、审计器；缺一都不能视为“已落地” | `aigc_skill_audit.py --strict` 能在 resolver 缺失或 contract 未被脚本消费时失败 |
| leaf 在 coverage 表中 active，但实际缺少 builder / runner | leaf runtime layer | 先补 leaf pipeline，再运行当前 tranche | 在 leaf `SKILL.md` 补 `Executable Entrypoints`，并把 help/dry-run/validator 作为最小 runtime 验收 | active coverage 与真实可执行状态一致 |

## Repair Playbook

1. 先检查命中的 leaf 是否真的存在 source-layer 合同。
2. 再检查输入是否仍按 `1-清单 -> 0-Init -> 2-Global` 三层顺序锁定。
3. 若 human projection 与 structured truth 漂移，优先以 `character_design.json` 修正。
4. 设计文件稳定后，检查 `full_generation_prompt / prompt整合` 是否是完全英文、1800-2200 UTF-8 bytes 的 integrated prompt，而不是 `global_style_prefix + subject_design_prompt` 的机械拼接。
5. 检查 `global_style_prefix` 是否来自 `全局风格.md` 的 `- 全局风格：` 字段值；若字段被写成裸行 `全局风格:`，先把项目文件规范化到 `## JSON 直接提取字段` 下再重跑产物。
6. 检查参照洁净是否在节点证据中完成：场景已把人物动作转写为空间痕迹，角色已锁纯色背景，道具已把手持/触碰转写为器物自身证据。
7. 最后执行 `ensure_design_auto_images.py`，逐个 Markdown 补齐内置 imagegen request sidecar；Codex 会话再调用内置 `image_gen` 并复制同 stem 图片，回接 `3-面板` handoff，让面板批量链路可扫描同 stem 图片作 SMART 参照，而不是反向让面板兜底。
8. 若内置 `image_gen` 失败或输出无法复制回项目，立即按图片步骤失败处理，不得把 request sidecar 视为已产图成功；继续保留设计真源、request/dry-run 证据和验收缺口。
9. 默认自动生图先看 `execution_mode`：`codex-builtin-imagegen` + `request_ready` 只证明 request 已准备；需要消费真实图片时必须复核同 stem 图片。
10. 当前轮 canonical 输出与 projection 落盘后，就读取项目根 `team.yaml` 做 `S6`；但 `S6` 的职责已经改成写审计边界说明。
11. `S6` 先确认 `roles.supervision` 已不再承担当前轮 closeout，再决定是否需要把问题写入 audit note / acceptance handoff。
12. 若用户明确要求本轮做落盘后复核，当前也只按 audit 需求记录，不回退到旧的 顾问与复核流程 监制强化。
13. 当前轮若要写 audit note，先按 `_shared/design-slot-review-contract.md` 把目标文件解析成 slot bundles；若无法解析，优先修共享合同或 leaf mapping。
14. 对 slot-bundle 这类 shared audit contract，不能只看 `SKILL.md` 是否提到；必须同时检查 `_shared/scripts/resolve_design_slot_bundles.py` 和 `scripts/aigc_skill_audit.py` 是否消费了同一合同。

## Reusable Heuristics

- `2-设计` 最容易坏的不是字段缺一项，而是“谁负责对象、谁负责风格、谁负责故事边界”三层责任被混写。
- 一旦 `1-清单` 已经输出稳定对象池，`2-设计` 就不该再重猜角色主键。
- `0-Init` 负责世界与情绪的北极星，`2-Global` 负责视觉与类型总线；两者都不该替代角色 bridge 本身。
- 场景设计迁回时，旧仓 `场景设计` 的价值在字段、质量门和三段式输出，不在旧 runtime 路径；当前仓必须以 `场景清单.json + 场景研究.json + scene_design_bridge.json` 为上游设计源。
- 自动生图不要让每个 leaf 各写一套 prompt 拼接规则；统一从共享输出合同取得 `global_style_prefix -> full_generation_prompt -> built-in imagegen -> same-dir same-stem image` 的单一路径。
- 自动生图完整性不要按“至少有一张图片”聚合；批量 design 目录必须逐 Markdown 对齐同 stem 图片，缺任一主体都只能是 `failed` 或 `dry_run`。
- `全局风格.md` 是富文档，不能整文压缩进 prompt；provider-ready 前缀只认 `## JSON 直接提取字段` 下的 `- 全局风格：` 值。
- 当全局风格字段已包含结束标点时，设计脚本不得再额外追加句号；前缀字段应被视作完整句子。
- 当前 `2-设计` 的三类 Markdown projection 模板应直接继承 AIGC-ZEN-VOID 原参照结构；当前仓只在 `prompt整合` 内补充英文 `Global style prefix` 与英文 `Integrated prompt`，其他章节不应为局部便利重排。
- 模板真源判断不要只看文件名；凡非 `templates/*.structured.v2.md` 文件包含完整 `物语 / 解构 / prompt整合` 样例，就会被执行者误用为第二模板，应直接移除或由 audit 阻断。
- `prompt整合` 是同模板上文的英文整合层，不是字段拼接层或短摘要层；执行时要先看 `物语 / 解构 / Photography / Prop Design / Cinematography` 等已落位内容，再写一段可直接给图像模型的约 2000 bytes 英文自然语句。
- 当用户确认当前 `6-设计` 提示词效果稳定时，自动生图修复应只补齐调用、状态聚合和 manifest 闭环，不要顺手重写 `full_generation_prompt / prompt整合` 的生成策略。
- `2-设计` 的同名自动图首先是后续参照资产，不是叙事剧照；场景要空、道具要纯、角色要纯色背景，否则后续一致性引用会把人物、手或背景一起带走。
- 凡会影响参照污染的规则，不能只写在 prompt 末尾；它必须进入思维·执行节点：先在摄影/设计卡 synthesis 中改写污染源，再在 prompt 节点注入锚句，最后在 auto-image 前复验。
- `2-设计` 的单主体图片只服务主体概念锁定和 panel continuity reference；不替代 `3-面板` 的 layout 图。
- 外部 API provider 是显式 fallback，不再是默认依赖；默认链路应通过内置 imagegen 避开 API key / 网络 provider 失败。
- AIGC 图像生成默认应以 request sidecar 为提交真源，内置 imagegen 逐资产执行；`request_ready` 是可追踪准备态，不是最终产图成功态。
- `2-设计` 当前轮 closeout 已不再看 `roles.supervision.members`；它们只影响前置 advisory。
- `source_skill_refs` 适合做领域提示，不适合当 `6-设计` 当前轮 closeout 的授权字段。
- 当 `2-设计` 已经有稳定模板真源和 canonical truth 时，post-write 问题仍应用“文件 + slot bundle”双层粒度记录，但不再以 `监制强化` 的形式执行。
- 对 shared closeout contract 的审计，最容易出现的假阳性是“文档全提到了，但 runner 一个都没有”；防这种漂移最稳的方式是给 contract 配一个最小 resolver，并让 audit 直接检查它。
- `2-设计` 父层不能只看 leaf 目录和 validator 就宣布 active；真正的 active 至少要满足 builder 可运行、projection 可校验、auto-image 可受控降级三件事。

## Review Gate Mapping

No independent gate: 本文件是旧 `2-设计` tranche parent 的经验归档，不再作为 active 设计执行上下文或阻断真源；其中经验只能作为排障线索，必须回接当前 `6-设计` 父级 gate 与域级 `2-设计` leaf 合同。

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否把本 legacy CONTEXT 当作当前预加载经验层，而跳过 `场景 / 角色 / 道具` 域级 `2-设计` 的 `SKILL.md + CONTEXT.md`？ | `GATE-DESIGN-LEGACY-01` | `FAIL-DESIGN-LEGACY-ACTIVE-ENTRY` | `D-N4-DISPATCH`；对应域级 `2-设计` leaf `SKILL.md + CONTEXT.md` | 已加载上下文列表、legacy 只读归档声明、active leaf 位置 |
| `2-设计` 直接回读 `3-Detail`、重猜对象主键、混写 `1-清单 / 0-Init / 2-Global` 三层责任的问题，是否已回到当前域级合同复核？ | `GATE-DESIGN-LEGACY-02` | `FAIL-DESIGN-LEGACY-UNVALIDATED-RULE` | 对应域级 `2-设计` leaf；当前 `1-清单 -> 2-设计` 输入合同 | 问题症状、active input contract、采用/废弃的 legacy heuristic |
| 关于模板、`full_generation_prompt`、内置 imagegen、参照图洁净、slot bundle 的经验，是否被直接复制成当前规则而未通过 active shared contract / leaf review？ | `GATE-DESIGN-LEGACY-02` | `FAIL-DESIGN-LEGACY-UNVALIDATED-RULE` | 对应域级 `2-设计` leaf `review/review-contract.md`；active shared contract | 被复用经验、当前模板/共享合同位置、复核 verdict |
| 旧路径、旧 provider、旧 closeout reviewer 或旧 `team.yaml.roles.supervision` 语义是否仍冒充当前 canonical runtime？ | `GATE-DESIGN-LEGACY-03` | `FAIL-DESIGN-LEGACY-PATH-DRIFT` | `D-N2-DOMAIN -> registry/routes/shared runtime 修复`；`references/阶段路由矩阵.md` | `rg` 搜索结果、更新引用清单、无法自动更新的遗留引用 |
| 设计产物缺图、request sidecar 被误写为成功、或 provider timeout 等经验是否被当作父级可直接修复业务正文的理由？ | `GATE-DESIGN-CLOSEOUT-02` | `FAIL-DESIGN-CLOSEOUT-REPAIR-ROUTE` | `D-N5R-DOMAIN-REPAIR`；对应域级 `2-设计` / `3-生成` leaf repair + re-review | finding owner、repair route、leaf re-review verdict、父级未补写业务正文说明 |
