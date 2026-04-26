# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `5-设计/场景` 的经验层知识库，不是执行日志。
- 调用本技能时，应在根 `aigc -> 3-Detail -> 1-清单/_shared` 之后加载本文件。
- 优先级固定为：用户显式请求 > `AGENTS.md` / meta 规则 > `SKILL.md` > `CONTEXT.md`。

## Context Health

- soft_limit_chars: 20000
- hard_limit_chars: 40000
- status: ok
- last_checked_at: 2026-04-14

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍按旧仓分镜 markdown 或 `场景及方位` 主链来解释当前仓输入 | 输入契约层 | 回到 `3-Detail/第N集.json`，只消费 `分镜组列表[]` 与 shot fields | 在 `SKILL.md` 与 shared consumption contract 固化 JSON-only 主链 | 不再依赖旧式 storyboard markdown |
| 把 `角色背景面` 整句直接升格成 canonical scene name | 对象归一层 | 先抽主场景实体，再把朝向/气氛/边界降到 `scene_variant` | 在 `references/detail-scene-normalization.md` 固化“主场景家族 > 变体/状态层”规则 | `scene_name` 不再是长背景句 |
| 旧仓 `scene_bible_card / bridge / quality` 迁移时三份文件互相抢事实 | 输出治理层 | 按 `清单/研究/bridge` 重新拆分字段边界 | 在 `_shared/list-output-contract.md` 与本地 `SKILL.md` 共同锁定三真源结构 | 默认输出三份业务 JSON |
| 用户要求场景链恢复三真源 | 输出治理层 | 将 `场景研究.json / scene_design_bridge.json` 恢复为业务真源成员 | 用字段边界防止三份文件互相复制：清单管对象池，研究管证据/结论，bridge 管设计直参 | 默认输出 `场景清单.json + 场景研究.json + scene_design_bridge.json` |
| 只抄 `角色背景面`，导致研究密度不够、下游还要回头看 `分镜表现 / 摄影美学` | 补证层 | 把 `分镜表现 / 摄影美学 / 时间段 / 导演意图` 一起纳入 `evidence_ledger` | 在 `FIELD-SCENE-03` 固化 evidence augmentation 门 | `design_context.evidence_ledger` 可回链多字段 |
| shared contract 已切到 branch-owned，但 extractor 仍把 `角色背景面` 当主锚 | schema handoff 层 | 先读 `氛围表现.层次`，再用 `分镜构图 / 摄影美学` 补 framing 与光感；`角色背景面` 只做 fallback | 在脚本与 `detail-scene-normalization.md` 同时固定 `branch-owned first, legacy fallback` | 场景抽取主路径不再锚在 compatibility projection |
| `scene_variant` 与 `fixed_anchor_layer` 混写，导致场景不稳定 | 分层建模层 | 把结构/材质/色光收到 `fixed_anchor_layer`，把门禁/朝向/时态收到 `variable_state_layer` | 在 `scene_blueprint` 固化双层输出 | 同场景多次出现时不会每镜都长出新主键 |
| `design_handoff` 只剩 prose，总结很好看但 `2-设计` 不可直读 | bridge 层 | 补 `fixed_anchor_bridge / variable_state_bridge / prompt_anchor / negative_constraints` | 在 `Pass Table` 固化 bridge 机读门 | 下游无需再次解析长文 |
| 质量门缺失，弱证据场景被静默放行 | 质量控制层 | 输出 `quality_profile / quality_overview / enrichment_actions` | 把平均具像化分、weak 场景与 top missing fields 固化进统计 | `statistics.quality_overview` 非空 |
| 短句如“静姐一侧仍靠着锦鲤池”“生怕木星那头比社区广场”被误抽为 `scene_name` | 脚本归一层 | 在 `extract_episode_scenes.py` 先命中强空间短语，再让人物动作/状态句只进入 `scene_variant` | 维护 `STRONG_SCENE_PHRASES` 与 `SENTENCE_NOISE_RE`，让可复用空间实体优先于整句 fallback | `scene_name` 收束为 `锦鲤池 / 木星工程背景 / 社区广场` 等实体名，面板 identity badge 不出现长句 |
| 都市恐怖项目中的“卫生间/吊顶/门板/洗手池”缺少场景词表支持，脚本回退到剧本动作句并把“她睡前擦干洗手池”抽成 `scene_name` | 脚本词表与 fallback 层 | 扩展 domestic-horror 空间词表，且 fallback 结果再次经过动作噪声过滤 | 场景抽取器必须覆盖当前题材的强空间实体；`剧本正文` 只能做解歧回退，不应让动作句越过 `角色背景面` 成为主键 | `scene_name` 不出现“睡前/擦干/报警/播放”等动作句，卫生间、吊顶、门板等空间实体可稳定抽出 |
| `剧本正文` 标题行与局部空间锚并存时，脚本把“动作画面/对白/人物动作句”升成 `scene_name` | heading-vs-local-anchor 层 | 先解析 `### 场景X：...` 标题作为场景家族，再让 `大厅/墙面/门板` 等局部锚降到 alias/variant | 在 `extract_episode_scenes.py` 增加 `SCRIPT_SCENE_HEADING_RE + is_untrustworthy_scene + MICRO_ANCHOR_HINTS`，让标题级空间优先于动作句和局部表面 | scene family 回到 `苏家酒店顶层宴会厅 / 消防通道与车内 / 深巷阁楼外间` 等稳定名 |

## Repair Playbook

1. 先检查 `3-Detail/第N集.json` 是否具备 `分镜组列表[]` 与 `分镜明细[]`。
2. 再按“`氛围表现.层次` -> `分镜构图 / 摄影美学` -> `角色背景面 / 分镜表现 / 时间段 / 导演意图` -> `剧本正文回退`”的顺序补证。
3. 归一场景前，先判断哪些词属于主场景实体，哪些只属于方位、门禁、边界或气氛。
4. 折叠 research 时，先保证 `evidence_ledger / detail_profile / scene_blueprint` 成立，再写 `scene_bible_card / compendium / design_handoff`。
5. 结束前必须检查 `quality_overview` 是否已指出 weak scene、missing fields 与 enrichment actions。

## Reusable Heuristics

- 场景链最容易漂的不是“研究写得不够美”，而是主场景实体没有先锁住。
- `角色背景面` 只负责告诉你“人站在什么空间面前”，不等于它整句都该成为场景主键。
- `氛围表现.层次` 才是新结构下的主场景锚；`角色背景面` 现在更像兼容投影与补证线索，而不是第一真相。
- 当前仓迁移旧仓场景链时，若用户要求三真源，最稳的做法是恢复三份业务 JSON，但用字段边界约束它们，而不是把三份都写成完整总稿。
- `分镜表现 / 摄影美学 / 时间段` 对场景链的价值不是重建事实真相，而是补足可设计的材质、色光、节奏和状态层。
- 如果某个场景的 design handoff 不能被 `2-设计` 直接读成固定锚点、状态差分和负面约束，它就还没有真正完成清单阶段。
- 对近未来社区类项目，先抓 `中央全息广场 / 全息锦鲤池 / 社区广场 / 木星通讯画面` 这类强空间短语；人物名、情绪、动作、状态词只允许成为证据和变体，不应污染主键。
- 对都市恐怖/出租屋类项目，先抓 `出租屋卫生间 / 卧室床头 / 卫生间门板 / 洗手池 / 吊顶 / 楼道` 这类强空间短语；“睡前擦干、报警、播放录音”等动作句只能作为证据，不应成为 `scene_name`。
- 当 `剧本正文` 已经给出 `### 场景X：...` 标题时，它通常比 shot 里的局部表面词更适合作为 scene family；`冷白墙面 / 门板 / 大厅亮点` 这类局部锚更适合留在 alias 或 variant，不应抢 canonical 主键。
