# AIGC Project Runtime Layout

本文件是 `aigc/query` 内置的项目运行时布局参考，用于替代当前新 `aigc` 树尚未提供的根 `_shared/project-runtime-layout.md`。

## Canonical Runtime Root

```text
projects/aigc/<项目名>/
├── MEMORY.md
├── CONTEXT/
├── STATE.json
├── governance-state.yaml
├── 0-初始化/
├── 1-分集/
├── 2-编导/
├── 3-摄影/
├── 4-分组/
├── 5-设计/
│   ├── 场景/
│   ├── 角色/
│   └── 道具/
├── 6-图像/
│   ├── A-分镜画面/
│   └── B-分镜故事板/
├── 7-视频/
│   ├── A-分镜画面参照/
│   ├── B-分镜故事板参照/
│   └── C-主体参照/
└── reports/
```

## Stage Mapping

| current stage | project carrier | legacy carrier | query note |
| --- | --- | --- | --- |
| `0-初始化` | `0-初始化/` | `0-Init/` | 新项目默认中文目录 |
| `1-分集` | `1-分集/第N集.md` | `1-Planning/` | 旧 `1-Planning` 不再是新链路默认分集目录 |
| `2-编导` | `2-编导/第N集.md` | `3-Detail/第N集.json` | 查询旧 JSON 时必须标注 legacy |
| `3-摄影` | `3-摄影/第N集.md` | none | 当前新链路新增的摄影主阶段 |
| `4-分组` | `4-分组/第N集.md` | none | 当前新链路分镜组主阶段 |
| `5-设计` | `5-设计/{场景,角色,道具}/` | `4-Design/` | 旧设计路径只作兼容 |
| `6-图像` | `6-图像/` | `5-Image/` | 旧图像路径只作兼容 |
| `7-视频` | `7-视频/` | `6-Video/`、`7-Cut/` | `7-Cut` 当前不作为默认可执行阶段 |

## Evidence Priority

1. 用户显式提供的项目路径。
2. 当前工作目录最近的 `projects/aigc/<项目名>/` 祖先。
3. `projects/aigc/<项目名>/STATE.json`、`MEMORY.md`、`0-初始化/` 共同指向的项目。
4. 只有一个候选项目时可谨慎推断。
5. 多候选或证据冲突时必须追问项目名。
