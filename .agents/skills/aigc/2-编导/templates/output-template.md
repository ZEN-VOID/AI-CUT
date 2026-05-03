# Output Template

## Output Contract Alignment

### Required output

- `OUTPUT-DIRECTING-EPISODE`: `projects/aigc/<项目名>/2-编导/第N集.md`
- `OUTPUT-DIRECTING-REPORT`: `projects/aigc/<项目名>/2-编导/执行报告.md`

### Output format

- 逐集编导稿：Markdown，含 YAML frontmatter、`【剧本正文】`、场景标题和字段化剧本正文。
- 执行报告：Markdown，记录输入、目标集、review verdict、直接修复项、复审结果、`director_substance_evidence`、`advisor_consultation_packet` 节点锚点、遗留风险和下游 handoff。

### Output path

```text
projects/aigc/<项目名>/2-编导/
├── 第1集.md
├── 第2集.md
└── 执行报告.md
```

### Naming convention

- 逐集编导稿：`第N集.md`
- 报告：`执行报告.md`

### Completion gate

- 上游 `1-分集/第N集.md` 已回指。
- 事实、顺序和对白保真。
- 声画配对、字段纯度和 slugline 稳定通过 review。
- 上游存在高潮/爽点/高光成分时，已按 `peak_visual_pass` 落入既有可拍字段，没有新增事实或对白。
- 关键场景已按 `director_substance_pass` 提炼戏剧问题、人物压力、观众位置、信息释放和可拍执行策略；执行报告含 `director_substance_evidence`，正文中能看到对应动作、声音、空间、道具、表演或沉默余波。
- 关键场景已按 `scene_turn_pass` 落实状态差；心理、潜台词、权力关系和沉默反应已转成可执行表演任务、场面调度或反应余波。
- `场面调度` 未写机位、景别、镜头运动、分镜编号或 `分镜明细预设`。
- `表演提示`、`场面调度` 没有在场景或分镜组末尾总结式列出；相关细节已内嵌到对白画面、角色动作、环境、道具、群像、声音和反应字段。
- 若启用 `controlled_enrichment`，执行报告含 `controlled_enrichment_ledger`，每个新增承托细节都有上游锚点、目标字段、用途和风险检查。
- 若启用 subagents，执行报告含 `advisor_consultation_packet` 摘要，至少记录顾问 roster、`node_ref/pass_ref/gate_ref/role_lens`、采纳指导、风险提示、`routeback_targets` 或降级路径。
- 若 review 发现阻断项，已在 `2-编导` 阶段内直接最小修复并复审通过；若无法修复，已记录阻断来源且不得推进下游。
- 执行报告记录 review verdict、repair actions、re-review verdict、残余风险和是否允许进入 `3-摄影`。

## Report Evidence Blocks

执行报告必须包含或等价覆盖：

```yaml
advisor_consultation_packet:
  status: not_applicable | completed | blocked
  roster: []
  node_anchors: []
  routeback_targets: []
  execution_brief: ""
  downgrade:
    blocked_by: none
    planned_path: ""
    actual_path: ""
    skipped_members: []
director_substance_evidence:
  - scene_id: ""
    source_anchor: ""
    dramatic_question: ""
    audience_position: ""
    character_pressure: ""
    scene_turn: ""
    directorial_strategy: ""
    embedded_in_fields: []
    risk_check:
      fact_drift: false
      new_dialogue: false
      over_explaining: false
      cinematography_overreach: false
```

## Episode File Skeleton

See `templates/episode-script.template.md`.
