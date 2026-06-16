# Group Multi-Image Type Package

## Purpose

固定本技能的默认类型：按 `8-分组` 普通分镜组组织 `.agents/skills/cli/imagegen` 组级多图任务。

## Match Signals

- 用户给三段式 `group_id`。
- 用户给四段式 `shot_id`，需要回溯到所属 `group_id`。
- 用户提到 imagegen、多图、生成多张单独图片、不是故事板拼图。
- 用户要求保持角色和场景一致性。

## Type Profile

```yaml
type_id: group-multi-image
task_unit: group_id
output_unit: shot_id
source_truth: full_10_group_block
image_count_rule: image_count_equals_source_shot_count
non_collage_required: true
default_imagegen_max_concurrency: 10
```

## Fixed Context

- 一个普通 `group_id` 对应一个 group imagegen package。
- 组内普通 `分镜N` 源顺序映射为 `x-y-z-N`。
- 完整组稿必须进入 prompt 或可审计引用。
- YAML 对应主体图用于组级参照绑定。
- 输出是多张单独图片，不是单张故事板；实际生成由 `.agents/skills/cli/imagegen` 按 task spec 执行，批量默认 subagents 并发且最大并发 10。

## Replacement Gate

只有当父级 `9-图像` 新增其他叶子路线或用户明确要求单镜独立生成时，才考虑新增类型包；不得在本包内临时恢复旧逐镜串行拓扑。
