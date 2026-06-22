# `libtv project` — 画布条目（CLI legacy project）

`libtv project` 是 CLI 1.0.1 沿用的 legacy 命令名。新版产品语义里，“项目”更接近 `projectSpaceId` / `folderId` 所代表的上层项目空间 / 文件夹，一个项目空间下可以拥有多个画布；而本命令的 `uuid` / `projectUuid` 指向的是**具体画布 UUID**。节点、上传、分组等命令里的 `-p` / `--project` 也必须传具体画布 UUID，不能传 `projectSpaceId` / `folderId`。

创建、查询、更新、删除远程画布，以及**把当前工作目录绑定到某个具体画布**（写入 `.libtv/project.json`）。多数子命令（[`libtv node`](./node.md)、[`libtv upload`](./upload.md)、[`libtv group`](./group.md)）在未传 `-p/--project` 时会读取该文件里的 **`projectUuid`**；未绑定且未传 `-p` 时会报错并提示执行 `libtv project use`。

`.libtv/project.json` 写在当前工作目录；stdout/stderr 与管道嵌套 case 见 [../examples/pipes/README.md](../examples/pipes/README.md)。

## 子命令

| 子命令                                    | 作用                                                                 |
| ----------------------------------------- | -------------------------------------------------------------------- |
| **`libtv project create <canvas>`**       | 新建空白画布；可用 `--folder-id` 放入指定项目空间 / 文件夹           |
| **`libtv project list`**（别名 **`ls`**） | 分页列出当前账号作用域下的画布条目，输出可能含 `folderId/projectSpaceId` |
| **`libtv project update <projectUuid>`**  | 更新具体画布的名称、简介、封面或所属文件夹                           |
| **`libtv project delete <projectUuid>`**  | 删除具体画布                                                         |
| **`libtv project use <projectUuid>`**     | 把当前目录绑定到指定画布                                             |
| **`libtv project unuse`**                 | 解除当前目录与画布的绑定                                             |
| **（默认）`libtv project [projectUuid]`** | 拉取画布详情并输出**精简 JSON**（节点、边、id、展示名、位置）        |

## 新版项目空间字段

| 字段 | 语义 | 可用于 |
| --- | --- | --- |
| `projectUuid` / `uuid` | 具体画布 UUID；CLI 的 `-p/--project`、`.libtv/project.json.projectUuid` 和 `libtv project use` 都使用它 | node / upload / group / image / script / project query |
| `folderId` | 画布所属文件夹或项目空间 ID；当前账号列表中常与 `projectSpaceId` 相同 | `libtv project create --folder-id` / `libtv project update --folder-id` |
| `projectSpaceId` | 新版上层项目空间 ID，可包含多个画布 | 识别归属；不能直接传给 `-p/--project` |

## `libtv project create <canvas>`

用法骨架：`libtv project create <canvas> [flags]`

**位置参数**

- **`<canvas>`**（必填）：新建画布名称（展示用）；含空格时用引号。CLI help 仍称 `<project>`，但运行语义是创建具体画布。

**选项**

| 选项                       | 必填 | 说明 |
| -------------------------- | ---- | ---- |
| `-d, --description <text>` | 否   | 画布简介。 |
| `--cover-url <url>`        | 否   | 封面图 URL。 |
| `-t, --team-id <n>`        | 否   | 所属团队 ID；缺省跟随当前活跃账户作用域，`0` 强制个人空间。 |
| `--folder-id <n>`          | 否   | 父文件夹 / 项目空间 ID；用于把新画布创建到指定 projectSpace。`0` 或不传时使用根目录 / 服务端默认落点。 |
| `--help`                   | 否   | 打印该子命令帮助。 |

**输出**：stdout 为 JSON，含新画布信息。常见结构为 `{ "projectMeta": { "uuid": "...", "name": "...", "folderId": 60925, "projectSpaceId": 60925 } }`；从 `uuid` 取具体画布 UUID，供后续 `libtv project use` 或其它子命令的 `-p` 使用。

## `libtv project list`（别名 `ls`）

用法骨架：`libtv project list [flags]`

**位置参数**：无。

**选项**

| 选项                     | 默认              | 说明 |
| ------------------------ | ----------------- | ---- |
| `-p, --page <n>`         | `1`               | **页码**（从 1 起）。不是画布 UUID，也不是项目空间 ID；勿与 [`libtv node -p`](./node.md) 混淆。 |
| `-s, --page-size <n>`    | `20`              | 每页条数。 |
| `-o, --order-by <field>` | `updated_at_desc` | 排序，须为接口约定值之一：`updated_at_desc` / `edit_time_desc` / `edit_time_asc`。 |
| `--name <text>`          | —                 | 仅保留名称**包含**该关键字的画布条目（子串匹配）。 |
| `-t, --team-id <n>`      | —                 | 团队空间过滤；缺省跟随当前活跃账户作用域，`0` 强制个人空间。 |
| `--help`                 | —                 | 打印帮助。 |

**输出**：stdout 为 JSON。`projectMetaList[]` 中每项是具体画布条目；可从 `uuid` 取画布 UUID，从 `folderId` / `projectSpaceId` 识别所属上层项目空间。

## `libtv project update <projectUuid>`

用法骨架：`libtv project update <projectUuid> [flags]`

**位置参数**

- **`<projectUuid>`**（必填）：具体画布 UUID。

**选项**

| 选项 | 必填 | 说明 |
| --- | --- | --- |
| `-n, --name <text>` | 否 | 新画布名称。 |
| `-d, --description <text>` | 否 | 新画布简介。 |
| `--cover-url <url>` | 否 | 新封面图链接；传空字符串可清空。 |
| `--folder-id <n>` | 否 | 父文件夹 / 项目空间 ID；可用于把画布移动到指定 projectSpace。 |
| `--help` | 否 | 打印帮助。 |

**输出**：stdout 为 JSON，通常含 `ok`、`projectUuid`。

## `libtv project delete <projectUuid>` / `rm`

用法骨架：`libtv project delete <projectUuid> [flags]`

**位置参数**

- **`<projectUuid>`**（必填）：具体画布 UUID。

**选项**

| 选项 | 必填 | 说明 |
| --- | --- | --- |
| `-t, --team-id <n>` | 否 | 团队空间 ID；缺省时自动从画布详情读取。 |
| `-y, --yes` | 否 | 跳过二次确认；CLI 默认无交互，此 flag 主要兼容脚本。 |
| `--help` | 否 | 打印帮助。 |

**副作用**：彻底删除指定画布；这不是删除上层项目空间 / 文件夹。

## `libtv project use <projectUuid>`

用法骨架：`libtv project use <projectUuid> [flags]`

**位置参数**

- **`<projectUuid>`**（必填）：**仅支持具体画布 UUID**（不支持按名称模糊匹配，也不接受 `projectSpaceId` / `folderId`）。会先调接口校验可访问，再写入本地 `.libtv/project.json`。

**选项**

- **`--help`** — 打印帮助。

**副作用**：**会清除**该文件中原有的 **`groupNodeKey`**（默认分组绑定）；仍需组内限定请重新执行 [`libtv group use`](./group.md)。

**输出**：stdout 为 JSON，含 `cwd`、`projectUuid`；校验成功时可能含 `name`。

## `libtv project unuse`

用法骨架：`libtv project unuse`

**位置参数**：无。**选项**：仅 `--help`。

**副作用**：**删除** `.libtv/project.json`（含其中的 `groupNodeKey` 一并移除）。

**输出**：stdout 为 JSON，如 `{ "unbound": true }`。

## `libtv project` / `libtv project <projectUuid>`（默认子命令）

用法骨架：`libtv project [projectUuid]`

**位置参数**

- **`[projectUuid]`**（可选）：具体画布 UUID；省略时使用当前目录 `.libtv/project.json` 的 `projectUuid`；未绑定且未传参则报错。

**输出**：stdout 为 JSON——节点 id / 展示名 / 类型 / 位置；边的 id / source / target。便于快速查看画布结构，**不等价**于完整的画布元数据接口，也不返回完整项目空间信息。

## 示例

```bash
# case 1: 在指定项目空间下新建画布，然后立刻绑定到当前目录
NEW=$(libtv project create "第6集" --folder-id 60925 | jq -r '.projectMeta.uuid')
libtv project use "$NEW"

# case 2: 翻页列出我的画布（页码走 -p/--page，不是画布 UUID）
libtv project list -p 1 -s 20

# case 3: 按画布名称子串过滤，并查看所属 projectSpaceId/folderId
libtv project list --name "第6集" | jq '.projectMetaList[] | {name, uuid, folderId, projectSpaceId}'

# case 4: 修改画布名称或移动到另一个项目空间
libtv project update 11111111-2222-3333-4444-555555555555 --name "第6集 V2"
libtv project update 11111111-2222-3333-4444-555555555555 --folder-id 60925

# case 5: 仅需画布结构（节点 + 边）时的快速摘要
libtv project                # 省略 UUID：使用目录绑定的画布
libtv project 11111111-2222-3333-4444-555555555555

# case 6: 解除当前目录的画布绑定（同时清除 groupNodeKey）
libtv project unuse
```
