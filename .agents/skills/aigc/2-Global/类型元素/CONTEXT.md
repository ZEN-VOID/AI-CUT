# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `aigc/2-Global/类型元素` 的经验层知识库，不是过程日志。
- 调用本技能时，应自动预加载本文件。
- 优先级遵循：用户显式请求 > `AGENTS.md` / meta 规则 > 本 `SKILL.md` > 本 `CONTEXT.md`。

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: ~2600
current_lines: ~55
current_cases: 0
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-13T18:30:00Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 仍只维护单文件 `类型元素.md`，双文件真源缺失 | 真源治理层 | 新增 `全集设计.md + 分组设计.md`，把旧文件降级为兼容投影 | 在 `SKILL.md` 固化 authoritative vs derived contract | 输出目录下出现双文件真源 |
| `0-Init` 题材 corridor 没有进来，导致组级判断失去项目统一性 | 输入合同层 | 把 `north_star.yaml` 的题材 corridor、观众合同、anti-goals 提升为必读上下文 | 在 `Context Preload` 与 `N2-INIT-CORRIDOR` 固化读取顺序 | `全集设计.md` 明确出现主副类型与禁区 |
| 只看 `north_star` 不看 `3-分组`，导致类型设计漂浮 | 主输入优先级层 | 把 `3-分组` 固定为第一主输入根 | 在 `SKILL.md` 与模板中强调所有组级设计必须附 `evidence` | 每组都能回指 `【组ID】` |
| inspiration 只有作品名，没有“借鉴哪种逻辑” | inspiration 抽取层 | 为每个 inspiration 补“参考桥段 + 借鉴逻辑 + 禁止复制项” | 在模板与引用矩阵中固定这三类槽位 | 不再只剩片名列表 |
| 全集设计写成单组放大稿，污染项目级总则 | 项目级/组级边界层 | 把单组波动移回 `分组设计.md` | 在 `全集设计` 合同中固定只写项目级稳定结论 | `全集设计.md` 不含单组小情绪 |
| 分组设计没有回答“整体一致、局部差异” | 组级判型层 | 为每组补 `与全集总则的对齐点` 与 `局部差异设计` | 在组卡字段中将二者列为必填 | 每组同时有共性与差异说明 |
| 兼容投影 `类型元素.md` 自行改写句义 | 兼容同步层 | 改为只从双文件真源汇编，不新写判断句 | 在 `N8-COMPAT-PROJECT` 固化“不得净新增真相” | `类型元素.md` 可追溯回双文件 |
| 输出只剩抽象口号，下游无法继承 | 下游桥接层 | 为每组补 `对 3-Detail 的直接执行导向`、`wrong_genre_negatives` 与 `fallback_floor` | 在分组模板中固定桥接槽位 | 下游能读出执行导向 |

## Repair Playbook

1. 先查是否真正读取了 `1-Planning/3-分组/第N集.md` 作为主输入。
2. 再查 `north_star.yaml` 的题材 corridor、受众合同、anti-goals 是否进入 `全集设计.md`。
3. 再查 inspiration 是否具体到“桥段逻辑”，而不是只报片名。
4. 再查每组是否同时写了 `对齐点` 和 `局部差异设计`。
5. 最后查 `类型元素.md` 是否只是由双文件汇编而来。

## Reusable Heuristics

- `类型元素` 最稳的写法，不是直接从项目梗概概括出一串类型词，而是先锁 `0-Init` 的题材 corridor，再让 `3-分组` 决定每组的局部差异如何成立。
- inspiration 真正有用的不是“像哪部片”，而是“借哪类类型片的哪种运作逻辑”，例如轻喜剧的关系错位、豪门情感的秩序压迫、近未来日常的科技反差。
- `全集设计.md` 负责稳定，`分组设计.md` 负责变化；只要这两层混写，下游就会一半过硬、一半过空。
- 每个组的 `类型元素` 短句都应该像“可直接继承的导演信号”，而不是摘要全文。
- 兼容文件 `类型元素.md` 只适合做过渡层，不适合继续承载新增真相；新增真相必须先回到双文件真源。
