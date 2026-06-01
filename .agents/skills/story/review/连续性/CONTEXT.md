# CONTEXT.md

## Purpose & Loading Contract

- 本文件是 `连续性` 子技能包的局部经验层，只服务连续性验收维度。
- 加载顺序固定为：先读同目录 `SKILL.md`，再按需读取本文件。
- 跨维度的 route 经验仍优先回写到父层 `CONTEXT.md`。

## Context Health

- soft_limit_chars: 40000
- hard_limit_chars: 80000
- soft_limit_cases: 80
- hard_limit_cases: 140
- status: ok

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| 卷内某章开篇像重启，不像承接 | carryover bridge | 先回卷级 continuity matrix 抓 entry state，必要时再参考前序章终稿 | 把卷级 continuity matrix 固定成硬输入，前序章终稿降为增强输入 | 连续性报告能具体说出“从哪里接上” |
| 场景在切，但 reader debt 没跟着走 | thread continuity | 记录断掉的是哪条关系/任务/悬念线 | 在维度指标里固定 `thread_drop_count` | issue 不再只写“衔接一般” |
| 连续性问题被混成节奏评价，没有明确返工入口 | rework routing | 强制标 `1-起盘` 或 `Step 2 / 2-节奏优化` | 子技能输出固定带 `rework_target_step` | drafting 能精确返工 |
| Markdown frontmatter 被当成开篇正文，导致承接信号被截断误判 | intro window extraction | 连续性 intro 检查前先剥离 frontmatter/title 元数据 | 所有开篇窗口类 validator 都先看正文主体，不把 YAML 头算进 intro | 带 frontmatter 的章节也能稳定识别上一章承接锚 |
| 转场不断事实但手法生硬，只靠“与此同时 / 几天后 / 回到某处”移动镜头 | transition craft gap | 补查声音、物件、光影、人物动作、对白牵引、任务压力或因果过渡是否存在 | `transition_quality_issues` 固定进入维度 packet；转场质量问题默认回 `Step 2 / 2-节奏优化` | 报告能说明转场缺哪类牵引，而不是只写“突兀” |

## Repair Playbook

1. 先读卷级 continuity matrix；若已有前序章终稿，再补读最后一个真正改变局面的点。
2. 再看本章开篇是否回应了那个点，而不是只换了场景或天气。
3. 检查关键转场是否有感知触发物、人物动作、对白承接、光影/声音变化、任务压力或因果过渡；纯时间/地点标记只能作辅助，不能独自承担转场。
4. 最后检查本章内部各条活跃线是否在推进时保持可追踪。
5. 若正文是 Markdown 根稿，先剥掉 frontmatter 再判断开篇承接，不要让元数据吃掉 intro 窗口。

## Reusable Heuristics

- 连续性不是“人物名字和地点没写错”，而是读者上一章记着的压力，这一章有没有真的接住。
- 若问题只能被描述成“读着有点断”，通常说明还没把断在哪条线上找出来。
- 好转场不是把时间地点说明白就够；它通常由一个可感知触发物、一个动作余波、一个对白钩子或一个任务压力把镜头推到下一处。
