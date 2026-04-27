# Context: Comic 漫画总入口

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 4272
current_lines: 61
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-27T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件沉淀 `comic` 导引式父级入口的路由、项目根、类型包和四段链交接经验。根层不拥有子技能执行细则。

## Type Map

| type_id | 症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-COMIC-ROOT-01` | 1/2/3/4 阶段产物散落在当前目录或 `output/comic` | 项目根合同层 | 统一迁回 `projects/comic/[项目名]/<阶段>/` | 父级 SKILL 与 registry 固定项目根 | 路径全在 `projects/comic/` |
| `TM-COMIC-ROOT-02` | 直接调用 3 号但没有合格 JSON | 交接门缺失 | 先运行 2 号 validator 或回到 2 号生成 JSON | 父级路由要求 handoff gate | 3 号输入为单个 group 级 `nine_blade_comic_prompts.v1` |
| `TM-COMIC-ROOT-03` | 2 号从小说直接写图，跳过 group JSON | 上下游边界混淆 | 明确 2 号只产 JSON，不调用生图 | 子技能边界表固化 | JSON 和图片落点分离 |
| `TM-COMIC-ROOT-04` | 生成结果是九宫格或九变体 | 下游 prompt/JSON 源层 | 回到 2 号 hard constraints 与 story_beat_map | 3 号只执行，不临场改剧情 | master prompt 含禁拼图/禁变体 |
| `TM-COMIC-ROOT-05` | 用户说“做漫画”但系统只输出小说 | 路由判定过窄 | 默认识别为 full_pipeline，除非用户限定只做某段 | 父级默认执行策略固化 | 任务意图能映射到 1/2/3/4 |
| `TM-COMIC-ROOT-06` | 剧集海报用了本集未出场角色，或像通用角色海报 | 4 号技能交接层 | 回到 4 号技能的 `subject_lock / representative_scene` | 父级明确 4 号只接当前集真实 artifact | 4 号 JSON 只引用本集事实 |
| `TM-COMIC-ROOT-07` | 2 号输出多个 page-group JSON 后，下游仍按旧整集单文件路径读取 | 父子技能 handoff 合同层 | 同步把 3 号、4 号与父级路由改成按 `page-group-*.json` 或 `第N集-page-group-*.json` 读取 | 父级 SKILL 与下游技能路径合同同步更新 | 当前 episode 的 group JSON 能被 3/4 号技能稳定命中 |
| `TM-COMIC-ROOT-08` | 根技能仍保留旧 `4-动画生成 / 5-剧集海报` 口径 | 父级阶段编排层 | 把根技能统一改成 `1-2-3-4`，第 4 段为剧集海报 | 父级 SKILL 持有唯一阶段索引，不允许兄弟技能平行演化阶段编号 | 根技能树、阶段表和 4 号技能编号一致 |
| `TM-COMIC-ROOT-09` | 3 号仍默认走 Seedream、Dreamina 或散装 provider | 3 号 runtime policy 层 | 回到 3 号 CLI imagegen 合同，默认生成 dry-run plan / JSONL jobs / page prompts | 父级明确 3 号默认 provider 为 `.agents/skills/cli/imagegen` | 3 号 report 记录 `provider=cli-imagegen` |
| `TM-COMIC-ROOT-10` | 1 号锁了类型包，2/3/4 段却丢失类型语义，导致作品中途变风格 | type-pack handoff 层 | 把 `type_stack_ref / type_pack_context` 设为跨阶段必带字段 | 根技能与 2/3/4 的 schema/validator/script 同步透传 | 任一阶段 artifact 都能回指 active packs |
| `TM-COMIC-ROOT-12` | 海报 JSON 后续生图仍走旧 API、Seedream 或散装脚本 | imagegen handoff 层 | 固定 4 号 `imagegen_handoff.tool_skill_path = .agents/skills/cli/imagegen` | 父级、4 号 schema/template/review 同步 imagegen 交接合同 | 海报生图能回指 `.agents/skills/cli/imagegen` |
| `TM-COMIC-ROOT-11` | 只新增了题材目录，没有写 resolver/child schema/加载合同，类型包系统形同虚设 | 系统真源层 | 先补 `comic_type_pack_resolver.py + child schema/validator + loading contract` | 把 type-pack 当跨阶段系统，而不是单点参考目录 | type-pack 既可被解析，也可被下游读取 |
| `TM-COMIC-ROOT-13` | 漫画题材包已迁到 2 号 `types/漫画/`，根层仍引用旧 `comic/type-packs/漫画/` | type-pack 真源迁移层 | 更新根 SKILL、shared contract、resolver、模板和项目产物路径 | 题材知识真源固定为 `2-九刀流漫画提示词/types/漫画/`，`type-packs/runtime.yaml` 只保留跨阶段默认栈 | 全仓无旧 `type-packs/漫画` 引用 |

## Repair Playbook

1. 先确认项目名与项目根：`projects/comic/[项目名]/`。
2. 再确认当前任务阶段：素材改编、九刀 JSON、漫画页生图、还是剧集海报。
3. 若下游缺输入，不得硬凑；返回上一段补 artifact。
4. 若输出路径漂移，优先修父级路径合同和脚本默认值。
5. 若内容质量问题来自故事切分、角色锁或漫画语法，回到 2 号；若来自 CLI imagegen job、文件命名或执行环境，回到 3 号。
6. 若海报脱离当前集角色或剧情，回到 4 号，不要在父级路由层硬补文案。
7. 若类型包只在某一段生效，优先排查 `type_stack_ref / type_pack_context` 是否在 handoff 中丢失。

## Reusable Heuristics

- `comic` 根层已经收束为导引式 router；它的价值在项目根、路由和交接真源，不在于复写子技能细则。
- 四段链完整交付时，最稳的节奏是：先把 `第N组.md` 分组漫剧剧本落盘，再把九刀流 group JSON 落盘，再让 3 号 CLI imagegen 生成 plan/jobs/pages/report，最后由 4 号技能收束成单集海报设计 JSON。
- 当 2 号技能进入多组口径后，父级最稳路由是：stage 1 先落 `第N组.md`，stage 2 再逐组产出 group JSON，stage 3 再按 `group_index` 逐组消费，而不是试图把多组 JSON 二次拼回一个超长 prompt。
- 当需要海报时，最稳的节奏是：先锁 1/2 号真源，3 号图片只做可选参考，再由 4 号生成单集 poster JSON。
- 当需要海报生图时，最稳的节奏是：4 号 JSON 先通过 validator，再把 `prompt_package.positive_prompt` 交给 `.agents/skills/cli/imagegen`，不要临场绕到旧 provider。
- `projects/comic/[项目名]/` 是漫画项目的业务真源；`output/` 只适合临时实验，不适合作为正式 comic 项目交付根。
- 正向验证：`滴滴滴` 从 AIGC 故事源到 9 页漫画图像一次跑通，说明父级 full_pipeline 路由、阶段落点、JSON validator、3 号生成链路可作为默认执行路径复用。
- 质量提升的下一优先级不是改父级路由，而是回到 2 号技能强化 `style_bible` 与 `pages[].layout`，以及 4 号技能强化 `representative_scene + hook_title + text_system`。
- comic 类型包系统最稳的落点不是“多一组题材标签”，而是让 1/2/3/4 段都消费同一份 `type_pack_context.stage_projection`。
- 漫画题材包当前 canonical root 是 `2-九刀流漫画提示词/types/漫画/`；根层和 1/3/4 段只通过 resolver 与 handoff 消费，不另建第二题材真源。
