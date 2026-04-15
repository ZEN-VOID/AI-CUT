# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/4-Design/2-设计` tranche parent 的经验层知识库，不是过程日志。
- 调用 `.agents/skills/aigc/4-Design/2-设计/SKILL.md` 时，应自动预加载本文件。

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
| leaf 已回迁，但父层仍宣称 pending | stage coverage layer | 更新 tranche parent 与 `4-Design` 父层 coverage 状态 | 在阶段总线上同步 stage coverage status | source-layer 状态与实体一致 |
| 场景设计 leaf 直接复刻旧仓 `3-设定` 路径 | migration adapter layer | 把旧仓字段密度迁移到当前 `4-Design/场景/2-设计` runtime | 在 `场景/SKILL.md` 固化当前仓输入输出路径，父层只声明 active leaf 与 handoff | 输出路径不再指向旧 `output/影片/.../3-设定` |
| 设计文件已落盘但没有自动生图，或生图 prompt 缺全局风格前缀 | output fast-path layer | 从主体设计文件生成 `full_generation_prompt`，再调用 nano-banana general 输出同目录同名图片 | 新增 `_shared/design-output-contract.md` 与 `run_design_auto_image.py`，把全局风格前缀和图片快路径沉为共享真源 | 每个主体文件旁边存在同 stem 图片，manifest 记录 `auto_image` |
| 批量输出中只生成了部分同 stem 图片，但 manifest 仍把自动生图写成成功 | auto-image completion aggregation layer | 用 `ensure_design_auto_images.py` 逐 Markdown 检查同 stem 图片，缺图就补跑或标失败 | 批量完成判定统一为“每个设计 Markdown 都有同 stem 图片”，leaf runner 不再各自聚合成功状态 | `_manifest.json.auto_image.missing_design_files=[]` 且 `status=success` |
| `full_generation_prompt` 的全局风格前缀混入 YAML frontmatter、章节说明、类型元素或设计元素文本 | prefix extraction layer | 只提取 `2-Global/全局风格.md` 中 `- 全局风格：` 的字段值 | 用 `_shared/scripts/global_style_prefix.py` 作为共享提取器，并让 leaf runner / auto-image helper 复用它 | prompt 中 `全局风格前缀：` 后紧跟一段项目风格正文，不出现 `project_name:`、`# 类型元素` 或模板说明 |
| `全局风格.md` 写成裸行 `全局风格:`，导致 `4-Design/2-设计` 无法提取统一前缀 | upstream format drift layer | 将项目风格文件规范化为 `## JSON 直接提取字段` 下的 `- 全局风格：...` | 共享提取器在失败时检测非规范裸行并输出可执行修复提示；上游 `2-Global` 必须继续服从模板字段 | `global_style_prefix.py <全局风格.md>` 成功返回前缀 |
| 全局风格字段本身已带句号时下游拼接成双句号 | prompt assembly layer | 拼接前检查结尾标点，只在缺失时补句号 | 设计脚本将前缀字段视为完整句，不额外无条件追加标点 | prompt 中前缀段以单个句号结束 |
| 子技能 Markdown 模板偏离 AIGC-ZEN-VOID 原参照结构 | template source layer | 将三份原参照直接迁入当前 `templates/*.md`，仅在 `prompt整合` 内加入全局风格前缀槽位 | 子技能 `SKILL.md` 严格引用 `.md` 模板；脚本必须从模板渲染，不能手工拼第二结构 | `rg` 无 `.txt` 旧引用，Markdown 含原参照章节顺序 |
| 旧式输出模板 reference 形态像第二份落盘模板，容易和 `templates/*.structured.v2.md` 抢权 | template canonical source layer | 直接移除旧式输出模板 reference，不再保留替代说明载体 | `_shared/design-output-contract.md` 增加 `Markdown Template Registry`，`aigc_skill_audit.py --strict` 检查旧式输出模板 reference 不得回流 | 只有三份 `templates/*_masterprompt.structured.v2.md` 承载完整落盘结构 |
| `prompt整合` 被误解为局部主体 prompt 拼接或短 prompt 摘要 | prompt integration layer | 改为对同一模板上方全部内容做英文自然语言整合 | 共享输出合同与三类子技能模板绑定合同固定 `Global style prefix + Integrated prompt`，并要求 `Integrated prompt` 完全英文、1800-2200 UTF-8 bytes、覆盖 `解构` 信息 | `prompt整合` 为约 2000 bytes 的英文连贯段落，覆盖结构、材质、镜头/摄影与负面约束 |
| 单主体参照图混入人物、手部或场景背景，导致后续面板/图像阶段污染 | reference cleanliness layer | 按域固定参照图纯净模式：场景为空镜头、道具为纯道具图、角色为纯色背景 | `_shared/design-output-contract.md` 增加 Reference Image Cleanliness Contract；场景/角色 validator 检查英文锚句，场景/道具 builder 固定锚句 | prompt 含 `empty environmental shot / no characters`、`isolated pure prop view / no hands / no characters`、或 `solid color background / no scene background elements` |
| 参照图洁净只写在输出规则，思维·执行节点仍按剧情剧照思路装配 prompt | thinking-action contract layer | 将洁净判断前移到 leaf 的摄影/设计卡 synthesis 节点，并在 prompt 与 auto-image 节点复验 | `_shared/design-output-contract.md` 增加 Thinking-Action Placement Contract；父层与三 leaf Field/Pass/Node 表登记 `reference_cleanliness_note` | 节点证据能说明污染词已被转写，且自动生图前已复验锚句 |
| 单主体自动生图 provider 长时间无响应，导致 `2-设计` 父级 pipeline 卡死 | provider timeout layer | 中断当前远端等待，将本轮 manifest 标为 `auto_image.failed/timeout`，继续交付可追踪设计真源与后续 layout dry-run | `run_design_auto_image.py` 增加默认 `--timeout`，超时返回 124 并输出明确错误，避免批量链路无限挂起 | 真实生图失败时命令能在超时窗内退出，manifest 与 validation-report 明确记录 provider timeout |
| 多主体设计批量生图仍逐个前台等待，拖慢或阻塞 `2-设计` pipeline | execution mode layer | 将缺图 Markdown 聚合成 `design_auto_image_batch.json`，默认后台提交 | 新增共享 `image-generation-execution-contract.md`，`ensure_design_auto_images.py` 默认 `background-batch-concurrent + max_concurrent=100`，只在 `--foreground` 时等待 | `_manifest.json.auto_image.status=background_submitted` 且含 `request_batch_path/background_pid/background_log` |

## Repair Playbook

1. 先检查命中的 leaf 是否真的存在 source-layer 合同。
2. 再检查输入是否仍按 `1-清单 -> 0-Init -> 2-Global` 三层顺序锁定。
3. 若 human projection 与 structured truth 漂移，优先以 `character_design.json` 修正。
4. 设计文件稳定后，检查 `full_generation_prompt / prompt整合` 是否是完全英文、1800-2200 UTF-8 bytes 的 integrated prompt，而不是 `global_style_prefix + subject_design_prompt` 的机械拼接。
5. 检查 `global_style_prefix` 是否来自 `全局风格.md` 的 `- 全局风格：` 字段值；若字段被写成裸行 `全局风格:`，先把项目文件规范化到 `## JSON 直接提取字段` 下再重跑产物。
6. 检查参照洁净是否在节点证据中完成：场景已把人物动作转写为空间痕迹，角色已锁纯色背景，道具已把手持/触碰转写为器物自身证据。
7. 最后执行 `ensure_design_auto_images.py`，逐个 Markdown 补齐同 stem 图片并回接 `3-面板` handoff，让面板批量链路可扫描同 stem 图片作 SMART 参照，而不是反向让面板兜底。
8. 若 provider 超过 `run_design_auto_image.py --timeout` 仍未返回，立即按图片步骤失败处理，不得让父级 pipeline 无限等待；继续保留设计真源、request/dry-run 证据和验收缺口。
9. 默认自动生图先看 `execution_mode`：后台批量并发提交只证明 request 已交付；需要消费真实图片时再复核同 stem 图片或用 `--foreground` 重跑。

## Reusable Heuristics

- `2-设计` 最容易坏的不是字段缺一项，而是“谁负责对象、谁负责风格、谁负责故事边界”三层责任被混写。
- 一旦 `1-清单` 已经输出稳定对象池，`2-设计` 就不该再重猜角色主键。
- `0-Init` 负责世界与情绪的北极星，`2-Global` 负责视觉与类型总线；两者都不该替代角色 bridge 本身。
- 场景设计迁回时，旧仓 `场景设计` 的价值在字段、质量门和三段式输出，不在旧 runtime 路径；当前仓必须以 `场景清单.json + 场景研究.json + scene_design_bridge.json` 为上游设计源。
- 自动生图不要让每个 leaf 各写一套 prompt 拼接规则；统一从共享输出合同取得 `global_style_prefix -> full_generation_prompt -> same-dir same-stem image` 的单一路径。
- 自动生图完整性不要按“至少有一张图片”聚合；批量 design 目录必须逐 Markdown 对齐同 stem 图片，缺任一主体都只能是 `failed` 或 `dry_run`。
- `全局风格.md` 是富文档，不能整文压缩进 prompt；provider-ready 前缀只认 `## JSON 直接提取字段` 下的 `- 全局风格：` 值。
- 当全局风格字段已包含结束标点时，设计脚本不得再额外追加句号；前缀字段应被视作完整句子。
- 当前 `2-设计` 的三类 Markdown projection 模板应直接继承 AIGC-ZEN-VOID 原参照结构；当前仓只在 `prompt整合` 内补充英文 `Global style prefix` 与英文 `Integrated prompt`，其他章节不应为局部便利重排。
- 模板真源判断不要只看文件名；凡非 `templates/*.structured.v2.md` 文件包含完整 `物语 / 解构 / prompt整合` 样例，就会被执行者误用为第二模板，应直接移除或由 audit 阻断。
- `prompt整合` 是同模板上文的英文整合层，不是字段拼接层或短摘要层；执行时要先看 `物语 / 解构 / Photography / Prop Design / Cinematography` 等已落位内容，再写一段可直接给图像模型的约 2000 bytes 英文自然语句。
- 当用户确认当前 `4-Design` 提示词效果稳定时，自动生图修复应只补齐调用、状态聚合和 manifest 闭环，不要顺手重写 `full_generation_prompt / prompt整合` 的生成策略。
- `2-设计` 的同名自动图首先是后续参照资产，不是叙事剧照；场景要空、道具要纯、角色要纯色背景，否则后续一致性引用会把人物、手或背景一起带走。
- 凡会影响参照污染的规则，不能只写在 prompt 末尾；它必须进入思维·执行节点：先在摄影/设计卡 synthesis 中改写污染源，再在 prompt 节点注入锚句，最后在 auto-image 前复验。
- `2-设计` 的单主体图片只服务主体概念锁定和 panel continuity reference；不替代 `3-面板` 的 layout 图。
- 外部 provider 是不稳定依赖，批量设计链路必须有超时边界；超时后可以继续生成结构化设计和面板 layout，但不得把图片步骤宣布为成功。
- AIGC 图像生成默认应以 request sidecar 为提交真源，后台批量并发执行；`background_submitted` 是可追踪提交态，不是最终产图成功态。
