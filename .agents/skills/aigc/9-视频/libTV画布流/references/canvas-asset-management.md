# Canvas Asset Management

本文件定义 AIGC 画布流的资产节点计划规则。真实上传、节点查询、节点更新和分组归档由最新版 `.agents/skills/cli/libTV` 执行，本技能只生成可审查的 CLI handoff plan 和证据要求。

## Official Source

执行层真源：

- `.agents/skills/cli/libTV/SKILL.md`
- `.agents/skills/cli/libTV/commands/upload.md`
- `.agents/skills/cli/libTV/commands/node.md`
- `.agents/skills/cli/libTV/commands/group.md`

本技能不得自建上传脚本、HTTP provider bridge 或凭据读取逻辑。需要真实执行时，handoff plan 必须声明 `executor_skill=.agents/skills/cli/libTV`，并给出 `libtv upload`、`libtv node`、`libtv group` 的命令参数。

## Asset Node Contract

当用户要求上传角色图、场景图、道具图、参考图或其他项目资产到 LibTV 画布时，计划层必须产生两类输出：

1. `cli_handoff.asset_uploads[]`：每张本地图片对应一个 `libtv upload "<nodeName>" -p <projectUuid> -g <group> -f <path>` 计划。
2. `asset_node_evidence[]`：执行后必须回填的 `source_path -> canvas_node_name -> node_key -> url` 映射。

执行门禁：

- 本地路径只允许作为 `libtv upload -f` 的参数，不得写入视频 prompt 正文。
- 上传结果必须能形成画布可见资源节点，不能只记录远端 URL。
- 每张资产必须取得 `node_key`；若 CLI 输出提供 URL，也必须记录 URL。
- 若执行器只返回节点而不返回 URL，后续必须通过 `libtv node` 查询补齐或标记 `url_unavailable`。
- 所有资产节点必须进入 active registry，供后续分镜组复用。

推荐 handoff 片段：

```yaml
cli_handoff:
  executor_skill: ".agents/skills/cli/libTV"
  auth_check:
    command: "libtv account info"
  asset_uploads:
    - command: "libtv upload"
      args:
        projectUuid: "<projectUuid>"
        group: "主体参照图"
        nodeName: "CHAR-005-令狐冲.png"
        file: "projects/aigc/<项目名>/7-设计/角色/3-生成/CHAR-005-令狐冲.png"
      expected_evidence:
        - node_key
        - url
        - canvas_node_name
```

## Node Naming Repair

若执行后节点显示名不是 AIGC 规范名，计划层必须生成节点命名修复计划，由 CLI skill 执行 `libtv node <node> --name <name>` 或当前 CLI 文档支持的等价节点更新命令。

命名修复必须满足：

- 顶层显示名等于原文件名或 AIGC 规范名。
- URL、节点类型和资源内容不改变。
- 不新建重复素材节点。
- 若当前 CLI 不支持该更新能力，记录 `node_rename_unsupported`，不得声称已修复。

## Naming Contract

AIGC 主体参照图应使用规范文件名：

```text
CHAR-005-令狐冲.png
S030-海雾村山道-2.png
PROP-001-旧银匣.png
```

主体绑定表中 `canvas_node_name` 应与画布节点显示名一致；`yaml_name` 应与 `6-分组` 组底 YAML 主体名一致。

## Binding Rule

LibTV 画布 UI、节点框体和生成工具可能重排图片顺序。主体身份不得由以下任何一项单独决定：

- `Image 1/2/3`
- `imageList` 顺序
- 节点框体内图片展示顺序
- 上传先后顺序
- UI 缩略图随机排列

主体身份必须由 `主体绑定表` 的 `yaml_name + category + node_key + URL + image_index` 决定。`Image 1/2/3` 只有在执行层已按 canonical order 用 `--left/--left-add` 连接图片节点，并查询确认左侧输入顺序后，才具备 prompt 引用语义。

## Active Registry Handoff

画布节点创建、命名修复和主体绑定必须回写或更新项目级 active registry：

```text
projects/aigc/<项目名>/9-视频/libTV画布流/libtv-canvas-active-registry.json
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
source_path: projects/aigc/<项目名>/7-设计/角色/3-生成/CHAR-005-令狐冲.png
last_verified_at: ""
executor_skill: ".agents/skills/cli/libTV"
```

`registry_key` 使用 `projectUuid::category::yaml_name`，不得使用 UI 图片顺序或上传顺序作为主键。

## Completion Gate

- 所有进入 LibTV 生成任务的主体图都有 `node_key` 和 URL，或明确记录 URL 不可取的原因。
- 画布节点显示名可回指原文件名或规范名。
- active registry 已登记或更新每个可复用主体图。
- submit plan 的 `主体绑定表` 说明图序冲突时以绑定表为准。
- submit plan 的 `left_input_edges[]` 和 `image_placeholder_map[]` 能说明每个 `{{Image N}}` 对应哪个 `node_key`。
- 真实执行证据来自 `.agents/skills/cli/libTV` 的命令输出或查询结果。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 资产图是否通过最新版 CLI handoff 上传为当前 LibTV 项目画布上的可见资源节点？ | `REV-LIBTVCANVAS-19` | `FAIL-CANVAS-ASSET-DETAIL` | `N3 Subject Binding` / `N5 CLI Handoff` | `cli_handoff.asset_uploads[]`、CLI 输出、对应数量的 `node_key` |
| 每张资产是否建立 `原文件名/AIGC规范名 -> URL -> node_key` 映射，且本地路径没有进入视频 prompt 正文？ | `REV-LIBTVCANVAS-17` | `FAIL-MANIFEST` | `N3b Evidence Artifacts` | manifest 中的 source_path、url、node_key、canvas_node_name 映射与 prompt hygiene check |
| 画布节点若显示名异常，是否生成 CLI 节点命名修复计划或明确记录当前 CLI 不支持？ | `REV-LIBTVCANVAS-19` | `FAIL-CANVAS-ASSET-DETAIL` | `N3 Subject Binding` / `N5 CLI Handoff` | 节点详情查询、命名修复命令计划、修复前后 `name` 对照或 `node_rename_unsupported` |
| 主体绑定是否只依赖已验证左侧连线顺序下的 `{{Image N}}`，不依赖上传顺序、UI 缩略图或 `imageList` 下标？ | `REV-LIBTVCANVAS-04` | `FAIL-ORDER-SAFETY` | `N3 Subject Binding` / `N3e Prompt Assembly` | `主体绑定表`、`left_input_edges[]`、`image_placeholder_map[]`、queried left input order |
| active registry 是否以 `projectUuid::category::yaml_name` 为主键，且同一主体只有一条 active 记录？ | `REV-LIBTVCANVAS-16` | `FAIL-ACTIVE-REGISTRY` | `N3 Subject Binding` | `libtv-canvas-active-registry.json` 记录、替换时旧记录 `active=false/status=replaced` 证据 |
| 进入生成任务的每个主体图是否同时具备 `yaml_name / category / canvas_node_name / node_key / URL`，并能回指 YAML 主体名？ | `REV-LIBTVCANVAS-03` | `FAIL-BINDING` | `N3 Subject Binding` | `主体绑定表`、manifest `subject_bindings`、submit plan 参考图清单 |
