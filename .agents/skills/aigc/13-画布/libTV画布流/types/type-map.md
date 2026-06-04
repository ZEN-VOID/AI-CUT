# Type Map

## Package Index

| type | trigger | load | route |
| --- | --- | --- | --- |
| `full_canvas_control` | 创建新画布项目、上传主体参照、回刷 YAML、创建视频节点 | `types/full-canvas-control.md` | `steps/canvas-control-workflow.md` |
| `backfill_only` | 只要求上传图片或回刷 UUID 到分组稿 | `types/backfill-only.md` | `N1` 到 `N4` |
| `node_rebuild_only` | YAML 已有 `图片N 主体名 UUID`，只重建视频节点 | `types/node-rebuild-only.md` | `N5` 到 `N8` |
| `repair_order` | 已有节点出现 `{{Image N}}` 错绑或顺序漂移 | `types/node-rebuild-only.md` + `references/image-order-contract.md` | `N7` 到 `N9` |

## Default Package Rule

Default: `full_canvas_control`.

## Loading Flow

1. 读取用户请求和项目路径。
2. 未显式指定时加载 `full_canvas_control`。
3. 只回刷 UUID 时加载 `backfill_only`。
4. YAML 已有 `图片N` 且只重建节点时加载 `node_rebuild_only`。
5. 修复错序时加载 `repair_order`，并强制读取 `references/image-order-contract.md`。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否选择了唯一模式，且没有把上传、回刷、建节点范围混在未知状态中？ | `GATE-LTVCTRL-ROUTE` | `FAIL-LTVCTRL-ROUTE` | `SKILL.md#Mode Selection` | route note |
