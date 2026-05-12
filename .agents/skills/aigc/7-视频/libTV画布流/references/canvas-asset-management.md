# Canvas Asset Management

本文件以 `.agents/skills/cli/libTV/references/canvas-asset-management.md` 为 canonical 官方细则，并补充 AIGC 画布流的主体绑定要求。执行画布资产上传、节点创建、节点命名修正或视频结果命名时，必须同时遵守官方文件；本文件只追加项目级约束，不削弱官方步骤。

## Asset Node Contract

当用户要求上传资产图、参考图、角色图、道具图、场景图或其他项目资产图片到 LibTV 画布时，必须完成两个层面的交付：

1. 使用官方 `upload_file.py` 将本地图片上传到 LibTV OSS，取得可访问 URL。
2. 通过 LibTV Agent IM 要求后端使用 `resource_generator` 把每个 OSS URL 创建为当前项目画布上的可见图片素材节点。

执行门禁：

- 本地路径只用于上传，不直接发送给 LibTV 会话。
- 会话消息必须包含 `把全部工作流和结果都放在画布上。`
- 每张资产图都必须有 `原文件名 -> OSS URL -> node_key` 映射。
- 完成后必须查询会话，确认工具结果中包含对应数量的 `type=image` 和 `node_key`。
- 图片素材节点必须是画布可见节点，不只是远端 URL。

推荐素材节点创建语义：

```text
把全部工作流和结果都放在画布上。
请逐项调用 resource_generator，把下面每个 URL 创建为当前项目画布上的可见图片素材节点。
节点标题/显示名必须使用原文件名；不要重新生成，不要只保存链接。
文件名.png: https://...
```

若一次提交较长或返回 `会话正在进行中`，按批次提交并等待上一批完成后再提交下一批。批次大小建议 5-8 张。

## Node Naming Repair

`resource_generator` 可能把图片素材节点的顶层 `name` 或 `data.name` 写成默认 `素材图片`。创建图片节点后必须核验和修正：

1. 查询会话消息，提取每个工具结果中的 `node_key` 与 URL。
2. 使用本地映射还原 `node_key -> 原文件名`。
3. 请求后端查询画布节点详情，确认节点顶层 `name` 和 `data.name` 是否仍为 `素材图片`。
4. 若仍为默认名，要求后端调用 `nodes_connections_batch` 或等价节点更新能力，按 `node_key -> 原文件名` 批量更新节点。

命名修复必须满足：

- 顶层 `name` 等于原文件名或 AIGC 规范名。
- `data.name` 等于原文件名或 AIGC 规范名。
- URL 和 `action=image_resource` 不得改变。
- 不得新建重复节点。

推荐修复语义：

```text
把全部工作流和结果都放在画布上。
修复命名：刚才创建的图片节点在画布里显示为“素材图片”。
请调用可更新画布节点的工具，按下面 node_key 精确把每个图片节点的显示名/标题/name 改成对应文件名。
不要重新生成图片，不要新建重复节点。
node_key: 文件名.png
```

完成门禁：

- 会话返回 `nodes_connections_batch` 或等价节点更新调用。
- 后端确认已按对应关系重命名。
- 若当前后端工具不支持重命名，必须明确报告 `不支持节点重命名`，不得声称已完成。

## Naming Contract

AIGC 主体参照图应使用规范文件名：

```text
CHAR-005-令狐冲.png
S030-海雾村山道-2.png
PROP-001-旧银匣.png
```

主体绑定表中 `canvas_node_name` 应与画布节点显示名一致；`yaml_name` 应与 `4-分组` 组底 YAML 主体名一致。

## Binding Rule

LibTV 画布 UI、节点框体和生成工具可能重排图片顺序。主体身份不得由以下任何一项单独决定：

- `Image 1/2/3`
- `imageList` 顺序
- 节点框体内图片展示顺序
- 上传先后顺序
- UI 缩略图随机排列

主体身份必须由 `主体绑定表` 的 `yaml_name + node_key + URL` 决定。

## Active Registry Handoff

画布节点创建、命名修复和主体绑定必须回写或更新项目级 active registry：

```text
projects/aigc/<项目名>/7-视频/libTV画布流/libtv-canvas-active-registry.json
```

每条 active 记录至少包含：

```yaml
registry_key: "<projectUuid>::角色::令狐冲"
yaml_name: 令狐冲
category: 角色
canvas_node_name: CHAR-005-令狐冲.png
node_key: 5a9b2d1e-eb41-4ae9-a93d-9d0d5a67355c
url: https://libtv-res.liblib.art/claw/.../CHAR.png
active: true
status: active
source_type: uploaded_main
source_path: projects/aigc/<项目名>/5-设计/角色/3-生成/CHAR-005-令狐冲.png
last_verified_at: ""
```

`registry_key` 使用 `projectUuid::category::yaml_name`，不得使用 UI 图片顺序或上传顺序作为主键。

## Completion Gate

- 所有进入 LibTV 生成任务的主体图都有 `node_key` 和 URL。
- 画布节点显示名可回指原文件名或规范名。
- active registry 已登记或更新每个可复用主体图。
- 远端提交文本包含 `主体绑定表`，并说明图序冲突时以绑定表为准。
