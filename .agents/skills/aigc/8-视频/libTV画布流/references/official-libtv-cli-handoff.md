# Official LibTV CLI Handoff

本文件定义 `libTV画布流` 与最新版 `.agents/skills/cli/libTV` 的执行边界。它替代旧版会话接口脚本口径。

## Official Source

- Skill: `.agents/skills/cli/libTV/SKILL.md`
- CLI binary: `libtv`（本机常见路径：`/Users/vincentlee/.libtv/libtv`）
- Commands:
  - `.agents/skills/cli/libTV/commands/login.md`
  - `.agents/skills/cli/libTV/commands/account.md`
  - `.agents/skills/cli/libTV/commands/project.md`
  - `.agents/skills/cli/libTV/commands/group.md`
  - `.agents/skills/cli/libTV/commands/node.md`
  - `.agents/skills/cli/libTV/commands/upload.md`
  - `.agents/skills/cli/libTV/commands/model.md`
  - `libtv download --help`（官方 1.0.1 skill 包含命令但未随包提供 `commands/download.md`）
  - `.agents/skills/cli/libTV/node-types/`
  - `.agents/skills/cli/libTV/model-schema/schema.md`

官方 1.0.1 CLI skill 包当前没有同目录 `CONTEXT.md`。执行前若按仓库 SKILL 加载合同发现缺失，应记录为官方包结构缺口；不得把旧会话接口经验层复制回新版 CLI skill。

## Required Authentication

新版 CLI 使用本机凭据：

```bash
libtv login web --open
libtv account info
```

凭据默认保存到：

```text
~/.libtv/credentials.json
```

旧版 access-key 环境变量、会话脚本、项目切换脚本、文件上传脚本、下载脚本和本地凭据包装器属于旧 skill 口径，本技能不得继续依赖。

## Handoff Plan Shape

每个分镜组的 submit plan 必须包含 `cli_handoff`：

```yaml
cli_handoff:
  executor_skill: .agents/skills/cli/libTV
  cli_version_required: ">=1.0.1"
  auth_check:
    - libtv account info
  project:
    projectUuid: ""
    projectUrl: ""
    commands:
      - libtv project use "<projectUuid>"
  group:
    group_name: ""
    groupNodeKey: ""
    commands:
      - libtv group "<group_name>" -p "<projectUuid>"
  assets:
    upload_commands: []
    existing_node_bindings: []
  video_node:
    node_name: "<分镜组ID>"
    node_type: video
    model: "star-video2"
    planned_left_input_edges:
      - planned_image_index: 1
        stable_subject_id: "<稳定主体ID>"
        node_key: "<主体图node_key>"
        assetId: "<主体图assetId>"
        yaml_name: "<YAML主体名>"
    runtime_image_placeholder_map:
      - image_index: 1
        placeholder: "{{Image 1}}"
        stable_subject_id: "<稳定主体ID>"
        node_key: "<主体图node_key>"
        assetId: "<主体图assetId>"
        yaml_name: "<YAML主体名>"
        verified_by: "queried data.params.imageList"
    queried_runtime_image_map_verified: false
    final_remote_prompt_queried_after_last_prompt_write: false
    remote_prompt_hygiene_verified: false
    commands:
      - libtv node "<分镜组ID>" -p "<projectUuid>" -g "<groupNodeKey>" -t video --left "<主体图node_key_1>" --prompt "<draft prompt>" --set model=star-video2 --set modeType=mixed2video
      - libtv node "<分镜组ID>" -p "<projectUuid>" -g "<groupNodeKey>" --left-add "<主体图node_key_2>"
      - libtv node "<分镜组ID>" -p "<projectUuid>" -g "<groupNodeKey>"
      - libtv node "<分镜组ID>" -p "<projectUuid>" -g "<groupNodeKey>" --prompt "<clean prompt with runtime {{Image N}}>"
      - libtv node "<分镜组ID>" -p "<projectUuid>" -g "<groupNodeKey>"
      - libtv node "<分镜组ID>" -p "<projectUuid>" -g "<groupNodeKey>" --run
  download:
    enabled: false
    command: ""
```

真实字段以 `.agents/skills/cli/libTV` 的 `libtv --help`、`libtv node --help`、`libtv model <modelKey>` 和实际模型 schema 为准；若 schema 与本计划冲突，以 CLI 实际输出为准并回写 submit plan / report。

## Preserved Boundaries

- 本技能只生成计划、绑定、prompt、review 和 handoff，不直接发 HTTP，不维护旧会话。
- 真实执行只通过 `libtv` CLI。
- `projectUuid` 是画布项目主键；能通过 `libtv project use <projectUuid>` 或每条命令 `-p <projectUuid>` 绑定。
- 画布分组使用 `libtv group` 创建、查询和绑定。
- 图片 / 视频 / 音频素材上传使用 `libtv upload`，上传后得到资源节点，而不是旧 OSS URL-only 结果。
- 视频生成节点使用 `libtv node` 创建、更新、左侧连线和 `--run`。
- 主体参照图必须通过 `--left` 或 `--left-add` 连到视频节点左侧；默认按 canonical order 逐张连接，第一张用 `--left`，后续用 `--left-add`。prompt 中用最新版 CLI 支持的 `{{Image 1}}`、`{{Image 2}}` 引用已连线图片。
- `{{Image N}}` 的编号来自新建/更新视频节点后查询到的 runtime `data.params.imageList[]` 或等价左侧输入顺序；执行 `--run` 前必须确认 `runtime_image_placeholder_map[]` 能唯一回指 `stable_subject_id / node_key / assetId/url`。
- 决定性检查点固定在最终节点参数、左侧输入和 `--prompt` 都写完之后、`--run` 之前；只以这一轮查询到的 `data.params.imageList[]` 和 `data.params.prompt` 为放行真源。远端 prompt 中不得出现 `{{Portrait N}}`、绑定表、参考图清单、执行锁、路径或诊断文本；检查不通过时先自动修复可控项，只有不可自动修复时才进入 `needs_rework`，不得继续运行。
- 默认视频模型必须为 `star-video2`（Seedance 2.0 标准模型）；`star-video2-fast` 只允许用户显式要求 fast / 极速 / 草稿预览时使用，并记录覆盖原因。
- 模型字段和 `modeType` 必须通过 `libtv model` 或模型 schema 确认，不得本地臆造。
- 下载必须显式授权后使用 `libtv download`。

## Common Commands

```bash
libtv account info
libtv project list --name "<项目名>"
libtv project use "<projectUuid>"
libtv group "<分镜组视频任务>" -p "<projectUuid>"
libtv upload "<主体名>" -p "<projectUuid>" -g "<分组名或ID>" -f "/path/to/ref.png"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>" -t video --left "<主体图node_key_1>" --prompt "<draft prompt>" --set model=star-video2 --set modeType=mixed2video
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>" --left-add "<主体图node_key_2>"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>" --prompt "<clean prompt with runtime {{Image 1}} {{Image 2}}>"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>" --left-add "<新增主体图node_key>"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>" --prompt "<clean prompt verified against latest imageList>"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>"
libtv node "<分镜组ID>" -p "<projectUuid>" -g "<分组名或ID>" --run
libtv download -p "<projectUuid>" -n "<视频节点名或ID>" --output-dir "<output_dir>"
```

命令示例只表达 handoff 方向；执行前必须读取实际 `--help` 和模型 schema，避免把文档示例当成不可变参数表。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 是否仍引用旧会话脚本、旧 access-key 环境变量或旧会话 ID 作为执行真源？ | `REV-LIBTVCANVAS-07` | `FAIL-OFFICIAL-HANDOFF` | `N5 CLI Handoff` | rg 扫描、submit plan `cli_handoff.executor_skill`、无旧脚本命令 |
| 执行前是否确认新版 CLI 登录与账号状态，而不是读取或输出凭据？ | `REV-LIBTVCANVAS-15` | `FAIL-CLI-AUTH` | `N5 CLI Handoff` | `libtv account info` 成功摘要、无 token 泄漏 |
| project / group / node / upload / download 是否使用 `.agents/skills/cli/libTV` 命令语义？ | `REV-LIBTVCANVAS-07` | `FAIL-OFFICIAL-HANDOFF` | `N5 CLI Handoff` | CLI handoff plan、命令文档引用、执行 stdout/stderr 摘要 |
| 参考图是否通过 `--left/--left-add` 连到视频节点左侧，且 `{{Image N}}` 编号经 runtime `imageList` 查询验证后才运行？ | `REV-LIBTVCANVAS-15` / `REV-LIBTVCANVAS-16` | `FAIL-LEFT-INPUT-ORDER` / `FAIL-RUNTIME-IMAGE-MAP` | `N5 CLI Handoff` | `planned_left_input_edges[]`、`runtime_image_placeholder_map[]`、queried `data.params.imageList[]` |
| 默认交付是否保持画布优先，未获显式下载授权时没有下载本地视频？ | `REV-LIBTVCANVAS-08` | `FAIL-DOWNLOAD-POLICY` | `N7 Explicit Download` | queue record `download=false`、无 `libtv download` 命令或有显式授权 |
| 本技能是否只做计划层，不把 CLI 执行逻辑 fork 成本技能脚本？ | `REV-LIBTVCANVAS-07` | `FAIL-PLAN-EXECUTION-BOUNDARY` | `N5 CLI Handoff` | scripts 目录清单、无 HTTP/provider bridge |
