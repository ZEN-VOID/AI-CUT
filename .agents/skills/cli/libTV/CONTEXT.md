# LibTV CLI Context

本文件是 `.agents/skills/cli/libTV` 的经验层。它不重定义命令参数；命令真源仍是 `SKILL.md`、`commands/*.md`、`node-types/*.md`、`model-schema/schema.md` 和实际 `libtv --help` 输出。

## Type Map

| situation | signal | handling |
| --- | --- | --- |
| login required | 命令返回未登录或账号为空 | 执行 `libtv login web --open`，再用 `libtv account info` 验证 |
| canvas scoped work | 已知具体画布 UUID | 优先每条命令显式传 `-p <projectUuid>`；需要目录默认时才用 `libtv project use <projectUuid>`；不要把 `projectSpaceId` / `folderId` 传给 `-p` |
| group scoped work | 已知分组名或 groupNodeKey | 用 `libtv group` 查询/创建/绑定；批量节点操作传 `-g` 或使用 `libtv group use` |
| asset upload | 本地图片/视频/音频要进入画布 | 用 `libtv upload`，记录 stdout 的 node key 和资源信息 |
| node execution | 已有节点需要运行 | 用 `libtv node <node> --run`；执行前按 `node.md` 校验是否允许只 run |
| model field uncertainty | 不确定模型字段或 `modeType` | 用 `libtv model` 或 `model-schema/schema.md` 查 schema，不凭经验臆造字段 |
| video default model | 创建/更新 video 节点且计划未指定模型 | 默认写 `-s model=star-video2`；fast 只接受显式覆盖 |

## Repair Playbook

1. 命令参数报错：先跑对应 `libtv <command> --help`，再回看 `commands/<command>.md`。
2. 画布找不到：确认当前账号空间和画布所属 `projectSpaceId` / `folderId`，必要时 `libtv account info`、`libtv account list`、`libtv account use <account>`；节点/上传/分组命令需要的是画布 `projectUuid`，不是上层项目空间 ID。
3. 节点重名：优先使用 node key；需要按名称时限定 `-g <group>` 并确保唯一。
4. 分组绑定混乱：用显式 `-p` / `-g` 命令覆盖目录默认；必要时 `libtv project unuse` 或 `libtv group unuse` 清理本地绑定。
5. 执行层与计划层冲突：以调用方的业务计划为任务意图，以本技能命令文档和 CLI help 为执行参数真源。
6. 视频节点沿用到 `star-video2-fast`：检查是否来自用户显式 fast / 极速 / 草稿要求；没有显式覆盖时改回 `star-video2`。

## Reusable Heuristics

- 账号验证只报告摘要，不输出 token、cookie、access key 或 `credentials.json` 内容。
- 管道输出通常是 JSON/NDJSON；后续命令消费时保留 stdout，不把 stderr 进度日志当作数据。
- `project list -p` 中的 `-p` 是页码；节点/上传/分组命令里的 `-p` 是具体画布 UUID，不能混用。
- 真实执行前先确认 `projectUuid`（画布 UUID）、必要的 `projectSpaceId` / `folderId`、目标 group、目标 node 名称/类型和是否需要 `--run`。
- 外部 AIGC 计划层传来的 prompt、subject binding、manifest、queue record 是业务证据；本技能只负责按 CLI 能力落到 LibTV 画布。
- 对 `video` 节点，`star-video2` 是执行层默认模型；历史任务或示例中出现的其它模型不得被继承为默认值。
