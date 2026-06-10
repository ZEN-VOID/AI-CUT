# Canvas Control Contract

本文件定义 LibTV 画布控制的项目空间、具体画布、上传、YAML 回刷和证据规范。

## Project Space And Canvas Naming

1. `local_project_root=projects/aigc/<项目名>` 对应 LibTV `project_space_name=<项目名>`。
2. `local_episode=第N集` 对应 LibTV `canvas_name=第N集`；`local_episode_scope=projects/aigc/<项目名>/第N集` 只表达跨系统语义范围。
3. 单集输入真源通常是 `projects/aigc/<项目名>/10-分组/第N集.md`；画布证据目录是 `projects/aigc/<项目名>/13-画布/libTV画布流/第N集/`，不得把 `local_episode_scope` 当成这两个物理路径。
4. 默认项目空间名为 `项目名`；若 `libtv project list` 返回的画布条目中已有可唯一对应的 `projectSpaceId` / `folderId`，后续新画布应优先落入该项目空间。
5. 默认画布名为 `第N集`；用户提供版本号时使用 `第N集-版本号`。
6. 若无法唯一定位项目空间，允许退回旧兼容命名 `项目名-第N集`；用户提供版本号时使用 `项目名-第N集-版本号`，并在报告记录 `project_space_resolution=unresolved_legacy_canvas_name`。
7. 若目标项目空间下已有同名或同项目同集画布，创建新画布时追加 `V2`、`V3`，不得覆盖旧画布。
8. `projectUuid` 是后续上传、节点、证据和 registry 的唯一远端 canvas truth；`projectSpaceId` / `folderId` 是上层项目空间 truth，不能传给 `-p/--project`。

## Video Node Identity

视频节点身份必须分为两层：

1. `source_group_id`：上游分镜组 ID，例如 `1-1-1`。它只用于追溯来源，不是远端节点唯一名。
2. `video_node_instance_id`：本次画布视频节点实例 ID，格式为 `vid__<source_group_id>__b<batch_no>__r<revision_no>__v<variant_no>`，例如 `vid__1-1-1__b002__r00__v001`。

编号规则：

- `batch_no` 使用三位数字，首批为 `b001`；用户要求对已生成过的分镜组“重新生成一组”时默认创建新批次并递增为 `b002`、`b003`。
- `revision_no` 使用两位数字，初稿为 `r00`；基于某个已生成节点做二次修改时递增为 `r01`、`r02`，并在 queue record 记录 `parent_video_node_instance_id`。
- `variant_no` 使用三位数字，同一批次同一修订轮内并行备选从 `v001` 递增。
- 若 active registry 与远端画布查询结果冲突，以远端已存在节点名为防覆盖边界，选择下一个未占用实例 ID，并在报告记录冲突来源。
- 不得因 `source_group_id` 已经存在而跳过本轮新建；只有完全相同的 `video_node_instance_id` 已存在时，才视为实例名冲突并重新分配或阻断。
- 删除或覆盖旧实例必须有用户显式授权；默认保留旧实例和旧证据。

## Reference Discovery

默认本地查找范围：

| category | path |
| --- | --- |
| 角色 | `projects/aigc/<项目名>/11-主体/角色/3-生成/` |
| 场景 | `projects/aigc/<项目名>/11-主体/场景/3-生成/` |
| 道具 | `projects/aigc/<项目名>/11-主体/道具/3-生成/` |

匹配规则：

1. 优先使用用户给出的 UUID 或 active registry。
2. 其次按本地文件名和 YAML 主体名精确匹配；上传后的画布节点名默认保持本地图片文件名。
3. 不匹配时跳过该主体，不猜测、不替代。
4. 同一文件只上传一次；同一 UUID 可服务多个 YAML 主体名。

## YAML Backfill

分组稿 fenced YAML 中的主体行统一回刷为：

```yaml
角色:
  - 图片1 艾娃·沃斯 7baf0914-3d12-4bac-9fbb-366d5d1bb2b5
场景:
  - 图片2 沃斯庄园书房 37515350-d9ff-4951-9d7c-97b7cc449f4d
道具:
  - 图片2 橡木书桌 37515350-d9ff-4951-9d7c-97b7cc449f4d
```

编号规则：

- 每个非连接件分镜组单独从 `图片1` 开始编号。
- 遍历顺序为 YAML 中的 `角色` 原顺序 -> `场景` 原顺序 -> `道具` 原顺序。
- 同一组内相同 UUID 复用第一次出现的 `图片N`。
- 无 UUID 或无法匹配的主体保持原主体行，不写 `图片N`。
- 回刷不得改写分镜组正文或连接件正文。
- 提交 LibTV prompt 时，主体行按 `references/image-order-contract.md` 重排为 `图片N 主体名 {{Image N}} UUID`；本地回刷格式不直接等同于远端 prompt 主体行格式。

## Evidence

必须生成或更新：

- `libtv-canvas-active-registry.json`
- `<video_node_instance_id>-subject-reference-manifest.json`
- `<video_node_instance_id>-libtv-submit-plan.json`
- `<video_node_instance_id>-queue-record.json`
- `<video_node_instance_id>-执行报告.md`

`libtv-canvas-active-registry.json` 必须记录本地 / 远端层级映射：`local_project_root`、`local_episode`、`local_episode_scope`、`source_file`、`evidence_dir`、`project_space_name`、`projectSpaceId`、`folderId`、`canvas_name` 和 `projectUuid`。

`libtv-canvas-active-registry.json` 还必须按 `source_group_id` 维护多实例索引，至少记录 `instances[]`、`active_instance_id`、每个实例的 `video_node_instance_id`、远端节点 key、状态、创建时间和父实例关系。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否锁定正确 AIGC 项目 / 集数到 LibTV 项目空间 / 画布的映射，并在其下创建或选择目标画布且没有覆盖同名旧画布？ | `GATE-LTVCTRL-PROJECT` | `FAIL-LTVCTRL-CANVAS-SCOPE` | `N1-CANVAS-SCOPE` | local mapping, project list query, `projectSpaceId` / `folderId`, projectUuid |
| 视频节点是否使用实例 ID，且重生成未覆盖或跳过旧实例？ | `GATE-LTVCTRL-NODE-IDENTITY` | `FAIL-LTVCTRL-NODE-IDENTITY` | `N5-NODE-CREATE` | remote node query, active registry, queue record |
| 参照图是否来自默认范围或用户显式 UUID，且无猜测替代？ | `GATE-LTVCTRL-UPLOAD` | `FAIL-LTVCTRL-REFERENCE-MATCH` | `N2-UPLOAD` | upload registry, skipped subjects |
| YAML 是否按 `图片N 主体名 UUID` 回刷，同 UUID 是否复用编号？ | `GATE-LTVCTRL-YAML` | `FAIL-LTVCTRL-YAML-BACKFILL` | `N3-YAML-BACKFILL` | YAML excerpt, manifest bindings |
