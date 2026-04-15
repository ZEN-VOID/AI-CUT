# Context: Comic 漫画总入口

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~2200
current_lines: ~45
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-15T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件沉淀 `comic` 父级总入口的路由、项目根和三段链交接经验。

## Type Map

| type_id | 症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-COMIC-ROOT-01` | 1/2/3 阶段产物散落在当前目录或 `output/comic` | 项目根合同层 | 统一迁回 `projects/comic/[项目名]/<阶段>/` | 父级 SKILL 与 registry 固定项目根 | 路径全在 `projects/comic/` |
| `TM-COMIC-ROOT-02` | 直接调用 3 号但没有合格 JSON | 交接门缺失 | 先运行 2 号 validator 或回到 2 号生成 JSON | 父级路由要求 `N3-HANDOFF` | 3 号输入为 `nine_blade_comic_prompts.v1` |
| `TM-COMIC-ROOT-03` | 2 号从小说直接写图，跳过桥接信息 | 上下游边界混淆 | 明确 2 号只产 JSON，不调用生图 | 子技能边界表固化 | JSON 和图片落点分离 |
| `TM-COMIC-ROOT-04` | 生成结果是九宫格或九变体 | 下游 prompt/JSON 源层 | 回到 2 号 hard constraints 与 story_beat_map | 3 号只执行，不临场改剧情 | master prompt 含禁拼图/禁变体 |
| `TM-COMIC-ROOT-05` | 用户说“做漫画”但系统只输出小说 | 路由判定过窄 | 默认识别为 full_pipeline，除非用户限定只做某段 | 父级默认执行策略固化 | 任务意图能映射到 1/2/3 |

## Repair Playbook

1. 先确认项目名与项目根：`projects/comic/[项目名]/`。
2. 再确认当前任务阶段：素材改编、提示词 JSON、还是生图执行。
3. 若下游缺输入，不得硬凑；返回上一段补 artifact。
4. 若输出路径漂移，优先修父级路径合同和脚本默认值。
5. 若内容质量问题来自故事切分、角色锁或漫画语法，回到 2 号；若来自 API/流式解析，回到 3 号或 seedream。

## Reusable Heuristics

- `comic` 根层的价值在于项目根和交接真源，不在于复写子技能细则。
- 三段链最稳的交付节奏是：先把小说母稿和桥接包落盘，再把九刀流 JSON 落盘，最后让生图报告引用 JSON 和图片。
- `projects/comic/[项目名]/` 是漫画项目的业务真源；`output/` 只适合临时实验，不适合作为正式 comic 项目交付根。
- 正向验证：`滴滴滴` 从 AIGC 故事源到 9 页 Seedream 漫画图像一次跑通，说明父级 full_pipeline 路由、阶段落点、JSON validator、3 号单请求生成链路可作为默认执行路径复用。
- 质量提升的下一优先级不是改父级路由，而是回到 2 号技能强化 `style_bible` 与 `pages[].layout`：全局漫画风格词越犀利、版式轮换越经典，生成页越不容易退成平整电影分镜。
