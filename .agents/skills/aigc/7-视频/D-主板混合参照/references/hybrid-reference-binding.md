# Hybrid Reference Binding Contract

本文件定义故事板总参照与主体参照的查找、绑定和审查边界。

## Storyboard Total Reference

查找路径：

1. `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/images/<group_id>.*`
2. `projects/aigc/<项目名>/6-图像/B-分镜故事板/第N集/<group_id>.*`

允许扩展名：`png`、`jpg`、`jpeg`、`webp`。

绑定规则：

- 唯一命中时写入 `storyboard_total_reference`。
- 无命中时记录 `storyboard_missing_optional`，不保留空图片槽。
- 多个同优先级命中时阻断该组，要求用户选择或先清理上游。
- 故事板总参照只能作为整组总参照，不得挂到某个主体后。

## Subject References

主体来源：

- 组底 YAML 的 `角色`
- 组底 YAML 的 `场景`
- 组底 YAML 的 `道具`

设计图查找路径：

- `projects/aigc/<项目名>/5-设计/角色/3-生成/`
- `projects/aigc/<项目名>/5-设计/场景/3-生成/`
- `projects/aigc/<项目名>/5-设计/道具/3-生成/`

优先级：

1. 多视图图或 multiview 图。
2. 主图、单图、封面图。
3. 其他真实图片候选。

禁止：

- 只存在 JSON、Markdown 或 prompt 文件时，不得当作图片参照。
- 不得从正文泛词自动扩展主体列表。
- 不得用角色图替代道具图，或用场景图替代角色图。

## Manifest Shape

```json
{
  "group_id": "1-1-1",
  "storyboard_total_reference": {
    "path": "projects/aigc/<项目名>/6-图像/B-分镜故事板/第1集/images/1-1-1.png",
    "marker": "@图1",
    "role": "storyboard_total_reference"
  },
  "subject_references": [
    {
      "subject_type": "角色",
      "subject_name": "林夏",
      "path": "projects/aigc/<项目名>/5-设计/角色/3-生成/林夏/多视图.png",
      "marker": "@图2",
      "inline_text": "林夏 @图2",
      "selected_variant": "multi_view"
    }
  ],
  "missing": []
}
```

## Over Limit Strategy

若图片数量超过 LibTV 当前上限：

1. 必须记录 `reference_over_limit`。
2. 默认不静默裁剪。
3. 可选策略为 `block_for_user_choice`、`prioritize_storyboard_and_core_subjects`、`split_jobs`、`text_only_fallback`。
4. 最终策略必须写入 submit plan 和执行报告。
