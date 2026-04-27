# 漫画剧本改编输出模板

## Output Contract Alignment

- Required output: `第1组.md`、`第2组.md`、`第3组.md` 等分组漫剧剧本；`reply_only` 时在回复中按同构结构输出。
- Output format: Markdown；每组包含 frontmatter、`# 第N组`、`【本组跨度】`、`【边界判定】`、`【漫剧正文】`、`【组末钩子】`。
- Output path: 默认 `projects/comic/<项目名>/1-漫画剧本改编/`；用户显式指定时按指定目录。
- Naming convention: `第N组.md`，从 `第1组.md` 连续递增，不混用“第N集”。
- Completion gate: 文件级或目录级 `validate_grouped_manga_script.py` 通过，语义 review verdict 为 `pass` 或 `pass_with_followups`。

## Final Output

```markdown
---
项目名: <项目名>
组号: 第<N>组
分组口径: 约1000字一组
估算原文字数: <positive integer>
尾组决议: <single_group|normal|merged_into_previous|standalone_tail>
source_type: <text|image|video|news_event|hot_search|mixed>
truth_boundary: <faithful|inspired_by|free_reimagining>
adaptation_posture: <faithful-core|comic-first|spectacle-first>
type_stack_summary: <<base> / <primary> / <secondary...>>
type_stack_active_packs: <_base|经典漫画叙事|...>
type_pack_projection_script_adaptation: <script adaptation stage projection summary>
type_pack_projection_nine_blade: <nine blade prompting stage projection summary>
scene_anchor: <space/time-light/core-prop/relationship-position/most-expensive-panel>
---

# 第<N>组

【本组跨度】
<一句话说明本组覆盖的剧情推进、冲突跨度或起止状态>

【边界判定】
<说明为什么这一组在这里起止；若是尾组，必须写明决议与理由>

【漫剧正文】
<本组可直接被 2 号技能消费的场景化漫剧正文>

【声画字段提示】
<可选。命中编导字段桥接时填写：本组对白/旁白/音效/系统提示如何就近配对画面承托；哪些规则、道具或心理压力需要转成可见格。>

【组末钩子】
<下一组或下一轮九刀必须承接的悬停点、危险逼近点或关系反转点>
```

## Evidence

- `source_type / truth_boundary / adaptation_posture / output_mode`
- 命中的类型包路径
- 命中编导字段桥接时的 `scene_anchor` 与声画字段检查结论
- 分组数量、尾组决议与目录级 validator 结果

## Review Result

- verdict: `pass | pass_with_followups | needs_rework | blocked`
- findings: 按 `review/review-contract.md` 的 finding shape 汇总
