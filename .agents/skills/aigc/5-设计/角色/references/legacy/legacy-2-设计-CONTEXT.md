# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-设计/角色` 的经验层知识库，不是过程日志。
- 调用本技能时，应在 `SKILL.md` 之后预加载本文件。

## Context Health

- soft_limit_chars: 22000
- hard_limit_chars: 44000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍把 `1-清单` 角色输出当成旧式单文件 prompt 输入 | input contract layer | 回到 `角色清单.json / role_design_bridge.json / 角色研究.json` | 在 `SKILL.md` 固化 bridge-first 输入层 | `2-设计` 不再重猜对象池 |
| `north_star` 与 `全局风格` 互相争夺风格主导权 | style governance layer | 以 `全局风格.md` 锁 `Style Backbone`，`north_star` 只负责故事与 anti-goals | 在共享输入合同中固定责任边界 | style 不再混写 |
| `character_design.json` 缺失而只剩 Markdown | output governance layer | 补回 machine-first structured truth | 固化 `character_design.json` 为 canonical truth | 下游 `3-面板` 可直读 JSON |
| `[角色名].md` 与 `character_design.json` 不一致 | projection layer | 由 JSON 反写 Markdown | 将模板绑定写入 SKILL 与模板真源 | Markdown 不再成为第二真源 |
| 文化原型角色被泛化成“东方奇幻” | archetype guardrail layer | 进入保守模式，缺证据打 `manual_review_required` | 在 references 中固定 cultural archetype trigger | archetype 角色不再漂移 |
| `prompt整合` 只剩字段 dump，没有身份钩子和叙事张力 | prompt assembly layer | 回到 `story pivot + style backbone + differentiation axes` 三段式收束 | 在 `FIELD-CHAR-02/03/07` 固化故事与风格驱动 | 最终 prompt 不再扁平 |
| 角色设计文件存在但没有同名图片或图片 prompt 缺全局风格前缀 | auto image layer | 以 `[角色名].md` 的 `prompt整合` 加 `2-Global/全局风格` 生成 `full_generation_prompt` | 在 `SKILL.md` 回指共享输出合同并新增 `FIELD-CHAR-11` | `[角色名].<ext>` 与 `[角色名].md` 同目录同 stem |
| 角色模板缺失原参照中的 Personality 字段或被重排 | template drift layer | 用 `.md` 直接承接 AIGC-ZEN-VOID `character_masterprompt.structured.v2` 结构 | `SKILL.md` 固定引用 `templates/character_masterprompt.structured.v2.md`，只允许在 `prompt整合` 加全局前缀 | Markdown 含 Personality 的 Constellation / Blood Type 等原槽位 |
| `prompt整合` 只拼接全局前缀和局部角色 prompt，或 Integrated prompt 过短 | prompt integration layer | 改为约 2000 bytes 英文自然语言整合同模板上方全部内容 | Template Binding Contract 固定覆盖身份、叙事压力、服装、姿态、材质、表演状态与镜头，并用校验器卡住非 ASCII 与 1800-2200 bytes | `prompt整合` 英文段落含角色设计与表演设计信息 |
| 角色参照图混入场景背景，导致后续角色引用带背景污染 | reference cleanliness layer | 将角色 prompt 固定为纯色背景角色图 | `SKILL.md / references / validate_character_design_projection.py` 固定 `solid color background` 与 `no scene background elements` | role prompt 不要求建筑、街道、房间、道具环境、叙事场景或其他人物 |
| 角色摄影节点仍按剧情剧照组织，后续只在 prompt 末尾禁止背景 | thinking-action node layer | 在 `N6-CAMERA` 先锁单角色定妆参照视角，再由 `N7/N10` 注入并复验纯色背景锚句 | `Thinking-Action Node Contract` 登记 `character_reference_note / reference_cleanliness_note` | camera block 不要求场景深度，prompt 含 `solid color background / no scene background elements` |
| Markdown 只有 `物语/解构/prompt整合` 摘要而缺少 structured v2 模板块 | projection validation layer | 运行 `scripts/validate_character_design_projection.py --output-dir <第N集>` 定位缺失块 | 在 `SKILL.md` 完成门中强制校验器通过，manifest 记录 `template_validation` | 缺 `Detailed Character Design / Detailed Costume Design / Cinematography` 时非零退出 |
| `character_design.json` 的 `structured_fields` 只有 `face_body/hair/costume/camera/performance` 粗字段 | structured truth layer | 回到角色装配环节补齐 face/hair/body/costume/camera 组级字段 | 校验器检查 `structured_fields` 组级覆盖和 prompt 厚度 | `structured_fields` 不再靠单行泛词通过 |
| Integrated prompt 先填充后按句截断，导致长度重新跌破 1800 bytes 下限 | prompt length gate layer | 截断后再次执行长度复检与短填充 | 生成器必须把 `trim -> guardrail injection -> min/max byte check` 作为最终门，而不是只在截断前补长 | `validate_character_design_projection.py` 不再报 prompt too short |
| 角色输出写完后仍继续进入 `team.yaml` 驱动的监制 closeout | council closeout layer | 在 `S11/N11` 固定读取项目根 `team.yaml`，但只写明当前轮 closeout 已不再由 `监制` 执行 | 用 `_shared/subagent-supervision-contract.md` 固定停用边界 | 当前轮角色输出完成后可回溯 `post_write_audit_note` |
| 角色 post-write 问题只能笼统说“角色稿薄”或“角色图不对”，无法指出具体槽组 | slot-level audit governance layer | 先把当前轮目标解析成 `ROLE-BUNDLE-01~04`，再写 audit note | `_shared/design-slot-review-contract.md` 固定 bundle 命名、carrier 边界与记录顺序 | audit 结论能区分是身份压力、视觉系统、摄影可读性还是 prompt/background bundle 失真 |
| leaf 已标 active，但缺少实际 builder / runner | executable runtime layer | 补齐 `build_character_design_packets.py + run_character_design_pipeline.py`，让角色 leaf 与场景/道具同级可执行 | 在 `SKILL.md` 固化 `Executable Entrypoints`，并以 validator + dry-run 作为最小验收 | `2-设计/角色` 可直接运行，不再只剩模板和校验器 |

## Repair Playbook

1. 先检查 `角色清单.json` 是否锁定了 `role_id / role_tier / costume_state`。
2. 再检查 `role_design_bridge.json` 是否存在并足够支撑主要视觉字段。
3. Style 漂移时，先回 `2-Global/全局风格`，不要直接改 prompt。
4. Markdown 与 JSON 漂移时，优先回到 `character_design.json`，再投影 Markdown。
5. archetype 角色拿不准时，保守降级优先于臆造。
6. 角色文件落盘后，用 `run_design_auto_image.py --design-file <角色名>.md` 验证同目录同名图片快路径。
7. 自动生图前检查 `reference_cleanliness_note`：缺 `solid color background / no scene background elements` 或出现正向建筑、房间、街道、道具环境、叙事场景、其他人物时，回到 `N6/N7`。
8. 在宣布 `角色/2-设计` 完成前，先跑 `scripts/validate_character_design_projection.py --output-dir <角色2-设计/第N集>`；失败时先修投影/JSON，不要让 `3-面板` 消费薄 prompt。
9. 当前轮角色 canonical 输出与 projection 落盘后，再读取项目根 `team.yaml` 做 `N11-POST-WRITE-AUDIT-NOTE`；图片状态只作证据。
10. `N11` 先确认 post-write closeout 已不再由 `监制` 执行，再决定是否补写 audit note / acceptance handoff。
11. 进入 `N11` 前，先按 `_shared/design-slot-review-contract.md` 将目标文件解析成 `ROLE-BUNDLE-*`；若无法解析，先修 mapping，不直接写泛化审计意见。

## Reusable Heuristics

- `1-清单` 负责“是谁”，`2-设计` 负责“这个角色应如何被稳定看见”。
- 角色设计最稳的顺序不是先写五官，而是先写 `Identity Hook + Narrative Tension + Style Backbone`。
- 如果 `character_design.json` 不存在，后续 `3-面板` 与图像阶段都会重新猜字段，这比单个角色文案差很多。
- 人读稿应该服务校审与浏览；结构化 JSON 才应该服务下游程序化消费。
- cultural archetype 角色最怕的是“看起来有文化感，但其实没有制式感”；宁可显式 `manual_review_required`，也不要伪装成稳定结论。
- 角色自动图是单角色概念图，不是定妆多视图；多视图仍应交给 `3-面板/角色` 或 `nano-banana/multiview-character`。
- 角色 Markdown 模板必须保留原参照结构中的身份压力、视觉驱动、角色细节、服装细节、摄影与 prompt 段；缺证据时填 `TBD`，不要删槽位。
- 角色 `prompt整合` 应是一段约 2000 bytes 的英文 casting/design prompt：既要保住身份钩子，也要把 `解构` 中的服装、身体、脸、发型、姿态、表演压力和镜头要求并入自然语句；背景固定为 `solid color background`，不得加入场景背景元素。
- 角色背景洁净要在摄影节点先确立为“单角色定妆参照”，不要等 Integrated prompt 末尾才否定场景；否则服装、姿态和表演压力很容易把剧情环境带回来。
- 如果下游角色面板只能读到 `Global style prefix + Integrated prompt` 两行，通常说明 `2-设计` 人读投影已经被压扁；先回 `character_design.json + Markdown template validation`，不要在 `3-面板` 里补救角色本体信息。
- 角色 prompt 生成器如果需要按句截断，必须在截断之后重新检查 1800-2200 bytes 与 `solid color background / no scene background elements`，因为保留句子边界可能删掉原本用于达标的填充段。
- 角色输出后的 post-write 问题不再看 `roles.supervision.members`；这些成员只作用于前置 advisory。
- 对角色这种多槽位高耦合输出，后置审计粒度过粗会直接把问题误判成“prompt 不够好”；更稳的顺序是先看 `ROLE-BUNDLE-01/02/03`，最后才看 `ROLE-BUNDLE-04`。
- `2-设计/角色` 的 active coverage 只有在 builder、validator、auto-image guard 三者都可跑时才算真 active；单有模板和 validator 不算运行时闭环。
