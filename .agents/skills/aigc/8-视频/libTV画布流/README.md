# AIGC 8-视频 / libTV画布流

`libTV画布流` 是 AIGC 视频阶段的 LibTV 计划层技能包。它把 `5-分组` 的组级 prompt、主体参照、时长规格和证据链整理成可执行计划，再把真实执行交给 `.agents/skills/cli/libTV`。

## Directory

```text
libTV画布流/
├── agents/
├── knowledge-base/
├── references/
│   ├── official-libtv-cli-handoff.md
│   ├── canvas-asset-management.md
│   ├── subject-reference-flow.md
│   └── storyboard-reference-flow.md
├── review/
├── scripts/
├── steps/
├── templates/
├── types/
├── CHANGELOG.md
├── CONTEXT.md
├── README.md
└── SKILL.md
```

## Position

- 本技能负责：路线判断、`5-分组` 提取、主体绑定、duration/spec 投影、manifest、submit plan、queue record、CLI handoff plan、review gate。
- `.agents/skills/cli/libTV` 负责：登录、账号、项目、分组、节点、上传、模型 schema、运行、下载。
- 本技能不再维护旧会话接口脚本或本地凭据包装器。

## Default Output

证据工件写入：

```text
projects/aigc/<项目名>/8-视频/libTV画布流/第N集/
```

典型文件：

```text
<分镜组ID>-subject-reference-manifest.json
<分镜组ID>-libtv-submit-plan.json
<分镜组ID>-queue-record.json
<分镜组ID>-cli-handoff-plan.md
<分镜组ID>-执行报告.md
```

显式下载的视频命名为：

```text
<分镜组ID>.mp4
```

## CLI Handoff

执行前读取：

```text
.agents/skills/cli/libTV/SKILL.md
.agents/skills/cli/libTV/commands/*.md
.agents/skills/cli/libTV/node-types/*.md
```

常见执行命令由 CLI skill 裁决：

```bash
libtv account info
libtv project use "<projectUuid>"
libtv group "<group>" -p "<projectUuid>"
libtv upload "<name>" -p "<projectUuid>" -g "<group>" -f "/path/to/ref.png"
libtv node "<group_id>" -p "<projectUuid>" -g "<group>" -t video --prompt "<clean prompt>"
libtv node "<group_id>" -p "<projectUuid>" -g "<group>" --run
```
