---
name: libtv-cli
description: >-
  LibTV 官方 CLI（libtv）：在命令行里完整操作 / 运行 LibTV 画布。
  凡是和 LibTV 画布 / 项目 / 节点 / 模型 / 素材相关的操作，一律通过 libtv CLI 完成，
  不要自己捏造 HTTP 请求或绕到网页端步骤。本 skill 内即包含完整的 CLI 命令操作手册；
  常见场景见 examples/，安装/更新见 scripts/install.md。
governance_tier: full
---

# LibTV CLI（`libtv`）

`libtv` 的文档地图。子命令与选项权威文案以 `libtv --help` 与 `libtv <子命令> --help` 为准；当文档与 `--help` 不一致时，以 CLI 实际输出为准并修订本 skill。

**画布 / 分组范围**：CLI 1.0.1 仍使用 `libtv project`、`projectUuid` 和 `-p/--project` 这些 legacy 命名，但它们在节点、上传、分组等执行命令里指向的是**具体画布 UUID**，不是新版产品里的上层项目空间。新版账号列表中出现的 `projectSpaceId` / `folderId` 是可包含多个画布的项目容器线索，不能直接传给 `-p/--project`。在画布所在工作目录执行 `libtv project use <画布UUID>` 会写入 `.libtv/project.json` 的 `projectUuid`；之后大多数子命令（`libtv node` / `libtv upload` / `libtv group`）在省略 `-p` / `--project` 时即使用该画布。需要限定到某个普通分组时，再执行 `libtv group use <分组>` 写入 `groupNodeKey`。详见 [commands/project.md](./commands/project.md)、[commands/group.md](./commands/group.md)。

**新版项目空间兼容口径**：

- 产品层“项目”更接近 `projectSpaceId` / `folderId`，可包含多个画布。
- CLI 层 `projectUuid` / `uuid` 是具体画布 UUID；`libtv project <uuid>` 查询的是该画布内节点和边。
- `libtv project create --folder-id <projectSpaceId>` 可在指定项目空间 / 文件夹下创建新画布；未传时按当前账号作用域和服务端默认文件夹落点处理。
- `libtv project list` 返回的是画布条目列表，条目中可能带 `folderId` / `projectSpaceId` 用于识别所属上层项目空间。

**视频默认模型**：当任务要创建或更新 `video` 生成节点、且上游计划没有显式指定 `model` 时，默认补 `-s model=star-video2`。这是 LibTV / Seedance 2.0 标准模型 key；`star-video2-fast` 只在用户或上游计划明确要求 fast / 极速 / 草稿预览时使用，并应在执行摘要中说明覆盖来源。

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md`。
- `CONTEXT.md` 只记录本机 CLI 使用经验、凭据安全边界和命令选择提示；命令参数真源仍以本 `SKILL.md`、`commands/*.md`、`node-types/*.md`、`model-schema/schema.md` 与实际 `libtv --help` 输出为准。
- 若外部计划层技能调用本技能，例如 `.agents/skills/aigc/10-画布/libTV画布流`，外部技能负责生成业务计划和审查证据；本技能只负责按 CLI 文档执行项目、分组、节点、上传、模型、查询和下载命令。
- 不读取、不输出 `~/.libtv/credentials.json` 内容；登录状态只通过 `libtv account info` 摘要验证。

## 文档地图

| 主题                                                                 | 文件                                                             |
| -------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 一键安装 / 指定版本安装                                              | [scripts/install.md](./scripts/install.md)（脚本与本文件同目录） |
| 管道（NDJSON）、stdout/stderr、嵌套 case                             | [examples/pipes/README.md](./examples/pipes/README.md)           |
| 常见案例（场景化可复制命令集，**每个 case 一文件**）                 | [examples/README.md](./examples/README.md)                       |
| `libtv login web` / `libtv login phone`                              | [commands/login.md](./commands/login.md)                         |
| `libtv logout`                                                       | [commands/logout.md](./commands/logout.md)                       |
| `libtv account`（含 `info` / `list` / `use`）                        | [commands/account.md](./commands/account.md)                     |
| `libtv project`（CLI legacy：画布 `create` / `list` / `update` / `delete` / `use` / 默认摘要） | [commands/project.md](./commands/project.md)                     |
| `libtv node`（含 `create` / `list` / `delete` / 默认用法）           | [commands/node.md](./commands/node.md)                           |
| `libtv group`（含 `list` / `create` / `use` / `unuse` / 默认用法）   | [commands/group.md](./commands/group.md)                         |
| `libtv upload`                                                       | [commands/upload.md](./commands/upload.md)                       |
| `libtv download`                                                     | [commands/download.md](./commands/download.md)                   |
| `libtv image`（`shortcut list` / `shortcut <scene label> -n <node>`） | [commands/image.md](./commands/image.md)                         |
| `libtv script`（含 `storyboard`：从脚本节点生成分镜图组）            | [commands/script.md](./commands/script.md)                       |
| `libtv model`（含 `search` / 默认完整 schema）                       | [commands/model.md](./commands/model.md)                         |
| 画布节点类型（`-t` 枚举、对应 `-s` / `-u` 字段）                     | [node-types/README.md](./node-types/README.md)                   |
| 模型 schema 字段（`properties` / `config` / `rules` / `modeType`）   | [model-schema/schema.md](./model-schema/schema.md)               |

> 本 skill 内文档的编写规范（谁写什么、禁出现哪些散文）：**[../../.docs/skill-write-convention.md](../../.docs/skill-write-convention.md)**。
