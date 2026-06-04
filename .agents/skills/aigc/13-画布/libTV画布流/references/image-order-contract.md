# Image Order Contract

本文件定义视频节点图片顺序、逐图连线和 `{{Image N}}` 稳定绑定规则。

## Core Rule

`图片N` 是本地分组稿 YAML 中的既定主体顺序；`{{Image N}}` 是 LibTV 远端视频节点实际消费的图片槽位。交付前必须证明二者一致。

## Standard Procedure

1. 从分组稿 fenced YAML 读取 `图片N 主体名 UUID`。
2. 按 `图片N` 升序形成 `ordered_subjects[]`。
3. 新建视频节点时写入：
   - `modeType=mixed2video`
   - `ratio=16:9` unless the user explicitly overrides it
   - `imageList=[{nodeId,url}, ...]`
   - `mixedList=[{nodeId,url,mediaType:"image"}, ...]`
   - `imageListOrder=[nodeId, ...]`
   - `mixedListOrder=[nodeId, ...]`
4. 按 `图片N` 顺序逐张执行 `libtv node <group_id> --left-add <node_key>`。
5. 连线后再次写入 `imageList/mixedList/imageListOrder/mixedListOrder`，因为单靠 `--left-add` 不保证远端 `params.imageList` 重新排序。
6. 最后查询 `libtv node <group_id>`，以返回的 `data.params.imageList[] + data.params.prompt` 为唯一完成真源。

## Prompt Rule

远端 prompt 由两部分组成：

1. 原分镜组正文，保持不改写。
2. 底部完整 fenced YAML；只在已有 `图片N 主体名 UUID` 行末追加 `{{Image N}}`。

示例：

```yaml
角色:
  - 图片1 罗曼·沃斯 4222b19c-b712-478e-ad33-9ce68b8fb61a {{Image 1}}
  - 图片2 艾娃·沃斯 7baf0914-3d12-4bac-9fbb-366d5d1bb2b5 {{Image 2}}
场景:
  - 图片3 沃斯庄园书房 37515350-d9ff-4951-9d7c-97b7cc449f4d {{Image 3}}
```

不得在正文中插入 `{{Image N}}`，不得使用旧 `{{Portrait N}}`。

## Anti-Patterns

- 按上传顺序解释 `{{Image N}}`。
- 按一次性 `--left A --left B` 参数顺序解释 `{{Image N}}`。
- 只查 `planned_left_input_edges[]`，不查远端 `data.params.imageList[]`。
- 只写 `imageListOrder`，不写 `imageList/mixedList`。
- 用视觉排列、画布节点位置或 UI 缩略图顺序推断主体。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 每组 YAML 是否先有稳定的 `图片N 主体名 UUID` 顺序？ | `GATE-LTVCTRL-ORDER` | `FAIL-LTVCTRL-MISSING-IMAGE-N` | `N3-YAML-BACKFILL` | YAML excerpt |
| 视频节点 `imageList/mixedList` 是否与 YAML `图片N` 顺序完全一致？ | `GATE-LTVCTRL-ORDER` | `FAIL-LTVCTRL-IMAGELIST-MISMATCH` | `N6-ORDER-LOCK` | final node query |
| prompt 是否只在 YAML 主体行后使用 `{{Image N}}`，且没有 `{{Portrait N}}`？ | `GATE-LTVCTRL-PROMPT` | `FAIL-LTVCTRL-PROMPT-POLLUTION` | `N7-PROMPT-HYGIENE` | final prompt query |
