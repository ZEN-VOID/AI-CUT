# Prompt Assembly Contract

本文件定义 step1 的 prompt 组装规则：直接使用现有分镜组内容作为生图提示词主体，并添加固定开头明确多格 storyboard 属性。

## Fixed Prefix

每条组级 prompt 必须逐字以下列文本开头：

```text
Create a multi-panel storyboard based on the following shot breakdown. Add the shot sequence number in the bottom-left corner of each panel (no other text). Auto-adapt the panel layout grid based on the total number of shots.
```

固定开头之后直接进入 `4-分组` 的组正文主体，不插入解释性说明、provider 参数、执行日志或额外任务指令。

## Prompt Body

- `prompt_body` 直接采用 `group_body` 的现有内容。
- 保留组内风格句、类型元素、画面风格、入场画面、出场画面、对白、动作画面、分镜明细和 `分镜N:` 顺序。
- 不翻译、不摘要、不改写剧情事实。
- 可在结构化侧车中记录 `shot_count`、`group_id` 和 YAML 主体，但不要把报告字段插入 prompt 正文。

## Layout Semantics

固定开头已声明：

- 多格 storyboard；
- 每格左下角放 shot sequence number；
- 除镜头序号外无其他文字；
- 根据总镜头数自动适配 panel grid。

执行者不得再额外硬编码格数，除非用户明确要求某种布局。

## Prompt Package Shape

Markdown prompt 包推荐：

```markdown
## 1-1-1

Create a multi-panel storyboard based on the following shot breakdown. Add the shot sequence number in the bottom-left corner of each panel (no other text). Auto-adapt the panel layout grid based on the total number of shots.

<4-分组中该组现有正文，不含底部 YAML>

### Reference Subjects

Characters:
- 林寂: projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png

Scene:
- 永夜私立中学二年级A班教室: projects/aigc/<项目名>/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png

Props:
- 厚黑窗帘: missing
```

## Integrity Gate

通过 prompt 组装必须满足：

1. prompt 以固定开头起笔。
2. `group_body` 直接来自 `4-分组`，没有上游剧情改写。
3. 所有 `分镜N:` 标签按原顺序保留。
4. YAML 不被混入 prompt 正文主体，但其主体列表进入 reference manifest。
5. 若由于 provider 限制必须压缩，必须先记录风险并得到用户确认；默认不压缩。

## Failure And Rework

| fail signal | rework |
| --- | --- |
| 固定开头分行、漏句或被翻译 | 重写 prompt header |
| 组正文被摘要 | 回到 `group-source-extraction.md` 重新提取 |
| 插入了说明文字或 provider 参数 | 删除非 prompt 内容，移到 plan/report |
| 分镜顺序乱序 | 按源正文顺序恢复 |
