# Reference Slot Binding Contract

本文件定义 step3：检查角色、场景、道具生成目录，给分镜 prompt 的空槽位绑定本地图片参照。

## Search Roots

固定检查以下目录：

```text
projects/aigc/<项目名>/5-设计/角色/3-生成
projects/aigc/<项目名>/5-设计/场景/3-生成
projects/aigc/<项目名>/5-设计/道具/3-生成
```

## Image Priority

对每个主体名称：

1. 优先选择 `<主体名称>-多视图.png`、`.jpg`、`.jpeg`、`.webp`。
2. 若多视图图片不存在，选择 `<主体名称>-主图.png`、`.jpg`、`.jpeg`、`.webp`。
3. 若只有 JSON 而无真实图片文件，不视为可绑定图片。
4. 若多视图与主图都不存在，槽位保持空或从最终 prompt 块移除。

## Matching Policy

- 默认使用精确主体名匹配。
- 可使用项目内已确认的规范别名，但必须在 manifest 中记录 `matched_by: alias`。
- 不得对子串、泛词、类别词或推测名进行自动绑定。例如“学生”不能自动绑定到“学生群像”，除非源 YAML 或用户显式确认。
- 同名多候选时进入 `ambiguous`，不得选择第一个凑数。

## Slot Output

推荐在 Markdown 中写为：

```markdown
Characters:
- 林寂: projects/aigc/<项目名>/5-设计/角色/3-生成/林寂-多视图.png

Scene:
- 永夜私立中学二年级A班教室: projects/aigc/<项目名>/5-设计/场景/3-生成/永夜私立中学二年级A班教室-多视图.png

Props:
- 红苹果: projects/aigc/<项目名>/5-设计/道具/3-生成/红苹果-多视图.png
```

## Manifest Requirements

`reference-manifest.json` 至少包含：

- `shot_id`
- `characters`
- `scene`
- `props`
- `bound`
- `missing`
- `ambiguous`
- `binding_policy`

所有 `bound[].path` 必须是存在的本地图片路径。
