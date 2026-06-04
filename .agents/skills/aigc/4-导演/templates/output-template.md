# 4-导演 Output Template

本模板只投影 `SKILL.md#Output Contract`，不得新增输出路径或完成门。

## Output Contract Alignment

| field | template landing |
| --- | --- |
| Required output | Annotated Episode + Execution Report |
| Output format | 原剧本结构 + `（导演批注：XXX）` 内联注入 + 结构化报告 |
| Output path | `projects/aigc/<项目名>/4-导演/` 下的 `第N集.md` and `执行报告.md` |
| Naming convention | 单集文件沿用 `第N集.md`；批量逐集输出 |
| Completion gate | `GATE-DIR-01..18` 阻断项为 0 |

## Annotated Episode

```markdown
# 第N集

<!-- 保留 2-编剧 原 frontmatter 和正文结构 -->

【剧本正文】

### 场景1：内景/外景 地点 - 日/夜 - 天气

环境描写：
原剧本文字。
（导演批注：围绕当前画面点写导演理解、观看重点、表演/节奏/空间/声音调度；关键心理和对白要给出视线、呼吸、停顿、手部、距离、声线等演员可执行种子，不改原文。）
```

## Execution Report

```markdown
# 4-导演 执行报告

## Source Manifest

## Visual Tone Context Map

## Director Style Source Matrix

## Episode Director Intent Plan

## Episode Visual Spine

## Director Substance Plan

## Information Asymmetry Map

## Scene Rhythm Profile

## Anticlimax Strategy Map

## Performance Handoff Map

## Episode Directing Profile

## Visual Point Coverage

## Annotation Binding Map

## Review Verdict

## Repair Log

## N/A Justification
```
