# Canvas Control Contract

本文件定义 LibTV 画布控制的项目、上传、YAML 回刷和证据规范。

## Project Naming

1. 默认项目名为 `项目名-第N集`。
2. 用户提供版本号时使用 `项目名-第N集-版本号`。
3. 若 LibTV 中已有相同项目名或同项目同集画布，创建新画布时追加 `V2`、`V3`，不得覆盖旧画布。
4. `projectUuid` 是后续上传、节点、证据和 registry 的唯一远端 project truth。

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

## Evidence

必须生成或更新：

- `libtv-canvas-active-registry.json`
- `<group_id>-subject-reference-manifest.json`
- `<group_id>-libtv-submit-plan.json`
- `<group_id>-queue-record.json`
- `<group_id>-执行报告.md`

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 画布项目是否按默认命名创建，且没有覆盖同名旧项目？ | `GATE-LTVCTRL-PROJECT` | `FAIL-LTVCTRL-PROJECT-NAME` | `N1-PROJECT` | project list query, projectUuid |
| 参照图是否来自默认范围或用户显式 UUID，且无猜测替代？ | `GATE-LTVCTRL-UPLOAD` | `FAIL-LTVCTRL-REFERENCE-MATCH` | `N2-UPLOAD` | upload registry, skipped subjects |
| YAML 是否按 `图片N 主体名 UUID` 回刷，同 UUID 是否复用编号？ | `GATE-LTVCTRL-YAML` | `FAIL-LTVCTRL-YAML-BACKFILL` | `N3-YAML-BACKFILL` | YAML excerpt, manifest bindings |
