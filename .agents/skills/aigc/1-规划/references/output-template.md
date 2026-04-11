# aigc 1-规划 / Output Template

本文件承载 `aigc 1-规划` 根技能的输出写位与跨阶段 handoff 规则。

## Artifact Roles

| artifact | 默认落点 | 角色 |
| --- | --- | --- |
| 故事源清单 | `projects/<项目名>/Init/story-source-manifest.yaml` | 故事主源类型、覆盖范围与预设保护模式真源 |
| 规划主稿 | `projects/<项目名>/规划/第N集.md` | 父级 `1-规划` 聚合后的唯一集级业务真源，必须是“格式化+分组完成后的最终文稿” |
| 阶段验收 | `projects/<项目名>/规划/validation-report.md` | 根技能级 route decision、source mode verdict、下一阶段入口 |
| 编导根文件目标 | `projects/<项目名>/编导/第N集.json` | 由 `2-组间` 首次创建的单一 episode 真源；规划阶段只登记目标路径与来源画像 |

## Default-Minimal Output Set

当用户进入父级 `1-规划` 全链模式时，默认只保留以下必要产物：

1. `projects/<项目名>/规划/第N集.md`
2. `projects/<项目名>/规划/validation-report.md`
3. `projects/<项目名>/规划/1-分集/第N集.md`
4. `projects/<项目名>/Init/story-source-manifest.yaml`
5. `projects/<项目名>/Init/episode-split-plan.json`

以下内容默认降为“非默认、仅在直达子技能 / 调试 / 复核时生成”的 sidecar：

- `projects/<项目名>/Init/episode-split-report.md`
- `projects/<项目名>/规划/2-格式/validation-report.md`
- `projects/<项目名>/规划/3-分组/group-plan.md`
- `projects/<项目名>/规划/3-分组/执行报告.md`
- `projects/<项目名>/规划/4-节奏/第N集.md`（仅在用户显式要求时）

## Parent Aggregation Inputs

父级 `1-规划` 走全链时，以下产物作为聚合输入，不应互相竞争主稿地位：

| child output | 默认路径 | 聚合角色 |
| --- | --- | --- |
| 分集规划表 | `projects/<项目名>/Init/episode-split-plan.json` | 提供集边界、来源范围、主事件与 bootstrap 输出路径 |
| 分集本地 sidecar | `projects/<项目名>/规划/1-分集/第N集.md` | 提供该子路径的可读集正文与边界摘要，供人工核读与父级引用；不与父级主稿竞争真源 |
| 格式化结果稿 | `projects/<项目名>/规划/2-格式/第N集.md` | 提供基于原文转写后的标准剧/解说剧格式化正文 |
| 分组结果 | `projects/<项目名>/规划/3-分组/第N集.md` 或内存态分组结果 | 提供分组计划表、组级容器与量化指标；父级据此给 `2-格式` 的 scene-first 正文加上 compact group summary，而不是原样复制 |
| 节奏 patch | `projects/<项目名>/规划/4-节奏/第N集.md` | 仅在用户显式要求时叠加节奏策略 |

硬规则：

1. `projects/<项目名>/规划/第N集.md` 必须引用以上实际执行过的子路径结果。
2. 未执行的子路径不得在父级主稿里补空白章节或伪造默认结论。
3. `4-节奏` 若未执行，父级主稿必须明确写为“默认跳过”，而不是假装没有这一层。

## Planning Master Template

- canonical template source: `references/output-template.md`（本文件）
- canonical output: `projects/<项目名>/规划/第N集.md`

父级主稿至少应包含：

1. 最终可读标题，例如 `# 第N集`
2. `## 来源画像`：至少显式写出 `source_type`、`preset_retention_mode`、`detail_expansion_mode`、`locked_preset_axes` 与当前集继承锚点
3. 已按所选变体转写好的正文场景块
4. 已写入 `G01 / G02 ...` 等组级边界
5. 每个组至少投影 `组目标 / 结构锚点 / 交接约束` 三项 compact summary，避免父级主稿退化成 `2-格式` 正文的简单复制
6. `场景号` 只按连续时空编号；若同一场景跨多个组延续，应写成 `场景X（续）`，并把 `镜号范围 / 锚点继承` 单独列出
7. 必要的极少量元信息，但不得让摘要、说明、验证段落压过正文
8. 若 `4-节奏` 未执行，可只在文末用一行说明默认跳过；不得把主稿写成验收报告

### Inline Canonical Skeleton

```markdown
---
project: <项目名>
episode: 第N集
planning_master_version: aigc-planning-episode-master/v2
format_variant: 标准剧|解说剧
source_type: novel_original|script_original|storyboard_script|hybrid_story_text
preset_retention_mode: standard|preserve_and_extend|preserve_only
detail_expansion_mode: free_expand|respect_storyboard_presets
locked_preset_axes: []
---

# 第N集

## 来源画像

- 故事主源：
- 预设保留：
- 明细扩写：
- 锁定轴：
- 当前集继承锚点：
- 场景编号规则：仅按连续时空编号；镜号、锚点、组号单独保留

## G01 组名

- 组目标：
- 结构锚点：
- 交接约束：

### 场景1：地点·时间

- 镜号范围：
- 锚点继承：

动作画面：

对白（角色）：“……”

对白画面：

## G02 组名

- 组目标：
- 结构锚点：
- 交接约束：

### 场景1（续）或 场景2：地点·时间

- 镜号范围：
- 锚点继承：
```

硬规则：

1. 根级 `1-规划` 不再另设平行 `templates/planned-episode.md`。
2. 若主稿骨架升级，统一只改本文件，再由父级执行流与项目产物继承。
3. 子技能可以提供自己的局部产物模板，但不得为父级 `规划/第N集.md` 再定义第二份平行主模板。
4. 父级聚合时，`2-格式/第N集.md` 必须保持 scene-first draft；父级主稿不得与其只差一层文件路径或一句节奏说明。

## Source Profile Handoff

若本轮规划已完成 `1-分集/3-分组`，则后续 `2-组间` 首次创建 `第N集.json` 时应带上：

```json
{
  "metadata": {
    "source_profile": {
      "source_type": "storyboard_script",
      "preset_retention_mode": "preserve_and_extend",
      "detail_expansion_mode": "respect_storyboard_presets",
      "locked_preset_axes": [
        "scene_boundary",
        "shot_order",
        "camera_motif"
      ],
      "preset_registry": [
        {
          "anchor_id": "A01",
          "source_span": "第1场 开场走廊调度",
          "lock_level": "soft_lock",
          "owned_axes": ["scene_boundary", "camera_motif"],
          "expandable_axes": ["shot_density", "composition", "micro_action"],
          "forbidden_changes": ["reverse_viewpoint"],
          "projected_group_ids": ["G01"],
          "projected_shot_mode": "single_anchor_multi_shot"
        }
      ]
    }
  }
}
```

## Output Checklist

1. `story-source-manifest.yaml` 是否明确当前主故事源类型。
2. `projects/<项目名>/规划/第N集.md` 是否已成为规划阶段唯一集级主稿，且内容是“格式化+分组后的最终文稿”而不是摘要说明。
3. `projects/<项目名>/规划/1-分集/第N集.md` 是否存在，且保留当前集正文与边界摘要，作为 `1-分集` 的本地可读 sidecar。
4. `projects/<项目名>/规划/2-格式/第N集.md` 是否存在，且能作为父级主稿的正文底稿。
5. 若是 `storyboard_script` 或 `hybrid_story_text`，主稿顶部是否显式写出 `preset_retention_mode`、`locked_preset_axes` 与当前集继承锚点，而不是只藏在 handoff 文件里。
6. 若存在外部分镜预设，是否已把可保留、可扩写、不可推翻的锚点写进 `preset_registry`。
7. `场景号` 是否按连续时空编号，而不是把 `镜号 / 组号` 直接转写成新场景号。
8. `validation-report.md` 是否写清 `source_mode verdict` 与冲突解消理由。
9. 若已进入 `2-组间` 且创建 `第N集.json`，是否已写入 `metadata.source_profile`。
10. 下游建议是否明确指出 `3-明细` 是“自由扩写”还是“顺着预设扩写”。
