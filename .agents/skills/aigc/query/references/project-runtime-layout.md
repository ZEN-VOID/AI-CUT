# AIGC Project Runtime Layout

本文件是 `aigc/query` 的项目运行时布局参考。当前项目事实以 `projects/aigc/<项目名>/` 为唯一 canonical runtime root；legacy 路径只能作为旧项目回读或迁移证据。

## Canonical Runtime Root

```text
projects/aigc/<项目名>/
├── MEMORY.md
├── CONTEXT/
├── STATE.json
├── governance-state.yaml
├── 0-初始化/
├── 1-分集/
├── 4-编剧/
├── 2-美学/
├── 5-导演/
├── 6-分镜/
├── 7-摄影/
├── 8-分组/
├── 3-主体/
│   ├── 场景/
│   ├── 角色/
│   └── 道具/
├── 9-图像/
│   ├── 分镜画面/
│   └── 分镜故事板/
└── 10-画布/
    └── libTV画布流/
```

## Stage Mapping

| current stage | project carrier | legacy carrier | query note |
| --- | --- | --- | --- |
| `0-初始化` | `0-初始化/`、`MEMORY.md`、`CONTEXT/` | `0-Init/`、legacy `north_star/init_handoff/team` | 新项目 scaffold-only；legacy carrier 存在时标注 optional/readback |
| `1-分集` | `1-分集/第N集.md` | `1-Planning/` | 旧 `1-Planning` 不再是新链路默认分集目录 |
| `4-编剧` | `4-编剧/第N集.md` | `2-编导/第N集.md`、`3-Detail/第N集.json` | 旧编导/detail 只在旧项目或用户点名时回读 |
| `2-美学` | `2-美学/**` | none | 美学协议阶段 |
| `5-导演` | `5-导演/第N集.md` | `2-编导/第N集.md` | legacy 编导中的导演判断只作迁移证据 |
| `6-分镜` | `6-分镜/第N集.md` | `3-运动/第N集.md` | legacy 运动强化只作动作连续性回读 |
| `7-摄影` | `7-摄影/第N集.md` | `4-摄影/第N集.md` | 当前摄影阶段为 `7-摄影` |
| `8-分组` | `8-分组/第N集.md` | none | 分镜组主阶段 |
| `3-主体` | `3-主体/{场景,角色,道具}/` | `4-Design/` | 旧设计路径只作兼容 |
| `9-图像` | `9-图像/` | `5-Image/` | 旧图像路径只作兼容 |
| `10-画布` | `10-画布/` | `6-Video/`、`7-Cut/` | `7-Cut` 当前不作为默认可执行阶段 |
| archived stages | 旧 `5-表演/`、`6-氛围/`、`9-光影/` | `backup/5-表演`、`backup/6-氛围`、`backup/9-光影` | 只在用户显式点名、历史回读、迁移对照或恢复计划时读取 |

## Evidence Priority

1. 用户显式提供的项目路径。
2. 当前工作目录最近的 `projects/aigc/<项目名>/` 祖先。
3. `projects/aigc/<项目名>/STATE.json`、`MEMORY.md`、`0-初始化/` 共同指向的项目。
4. 只有一个候选项目时可谨慎推断。
5. 多候选或证据冲突时必须追问项目名。

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 查询是否把 `projects/aigc/<项目名>/` 识别为唯一 canonical runtime root，而不是把仓库根、技能目录或旧英文阶段根当作项目根？ | `GATE-QUERY-02` | `FAIL-QUERY-PROJECT-ROOT` | `N1-project-root` | 报告锁定的项目根路径，以及用于确认的 `STATE.json`、`MEMORY.md`、`0-初始化/` 或阶段目录证据。 |
| 项目根回答是否区分 `MEMORY.md`、`CONTEXT/`、`STATE.json`、`governance-state.yaml` 和阶段目录的不同职责，避免把任一载体说成全量替代品？ | `GATE-QUERY-04` | `FAIL-QUERY-EVIDENCE` | `N3-carrier-read` | 列出实际读取或缺失的 runtime carrier，并说明每个 carrier 能回答的事实范围。 |
| `2-美学` 到 `8-分组` 查询是否默认读取当前中文阶段链，而不是默认回到旧 `2-编导 / 3-运动 / 4-摄影`？ | `GATE-QUERY-07` | `FAIL-QUERY-CARRIER` | `N3-carrier-read` | 报告当前阶段 carrier 路径、legacy fallback 路径和 fallback 原因。 |
| 角色、场景、道具类查询是否默认读取 `3-主体/{场景,角色,道具}/`，旧 `4-Design/` 只作为兼容证据？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前设计子目录证据，并在使用旧 `4-Design` 时显式标注 legacy。 |
| 图像资产查询是否默认读取 `9-图像/分镜画面` 或 `9-图像/分镜故事板`，旧 `5-Image/` 不作为默认答案？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前图像 carrier、旧图像 fallback 与二者命中情况。 |
| 视频资产查询是否默认读取 `10-画布/`，旧 `6-Video/` 与 `7-Cut/` 只作为 legacy fallback，且 `7-Cut` 不被说成默认可执行阶段？ | `GATE-QUERY-06` | `FAIL-QUERY-LEGACY` | `N3-carrier-read` | 报告当前视频 carrier、旧视频/剪辑 fallback、以及回答中的 canonical/legacy 标注。 |
| Evidence Priority 是否先尊重用户显式项目路径，再使用 cwd 祖先和项目核心载体，只有单候选时才谨慎推断？ | `GATE-QUERY-02` | `FAIL-QUERY-PROJECT-ROOT` | `N1-project-root` | 报告项目根推断来源；多候选或冲突时输出 `needs_clarification` 而不是混答。 |
| 当用户问“完成/通过/可交付”时，runtime layout 命中的文件或目录是否只作为产物存在证据，并继续补读执行报告或 validation report？ | `GATE-QUERY-05` | `FAIL-QUERY-VALIDATION` | `N4-validation-crosscheck` | 报告产物路径、执行报告或验收报告路径；缺报告时写明“未见验收证据”。 |
