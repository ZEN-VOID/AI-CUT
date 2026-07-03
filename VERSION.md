# VERSION

当前版本：`V1.0.2`
版本状态：期初基线
初始化日期：2026-07-02
最后更新：2026-07-03 03:51 UTC

## 版本语义

- `V<大版本>.<中版本>` 表示稳定基线，例如 `V1.0`。
- `V<大版本>.<中版本>.<小版本>` 表示同一中版本下的连续小修，例如 `V1.0.1`。
- 当小版本为 `0` 时，展示为 `V<大版本>.<中版本>`；脚本内部按 `V<大版本>.<中版本>.0` 计算。

## 跨代更新规则

| 等级 | 别名 | 适用范围 | 版本变化 |
|---|---|---|---|
| none | baseline/no-bump/不升级 | 初始化、纯记录、只想刷新版本日志但不跨代 | `V1.0` -> `V1.0` |
| small | patch/小更新 | 文档、提示词、校验器、小范围修复、兼容性增强 | `V1.0` -> `V1.0.1` |
| medium | minor/中更新 | 工作流能力扩展、输出合同变化、可见行为升级 | `V1.0.1` -> `V1.1` |
| large | major/大更新 | 架构重组、默认行为明显改变、跨代合同更新 | `V1.1` -> `V2.0` |

## 自动更新约定

- 执行 `github-push` 前，若仓库存在 `.codex/hooks/update_version_for_github_push.py`，推送流程应先运行该脚本，再暂存和提交。
- 未指定级别时，自动更新默认为 `small`。
- 可用环境变量指定级别：`VERSION_BUMP_LEVEL=none|small|medium|large`。
- 也可在提示中显式写入 `version-bump: small`、`version-bump: medium`、`version-bump: large` 或对应中文级别；`github-push` 流程应把这个级别传给版本脚本。

## 版本记录

<!-- version-hook:history:start -->
- 2026-07-03 03:51 UTC：`V1.0.1` -> `V1.0.2`（小更新；github-push 自动更新；scope: workflow skill update）。
- 2026-07-02 03:38 UTC：`V1.0` -> `V1.0.1`（小更新；github-push 自动更新；scope: workflow skill update）。
- 2026-07-02 03:30 UTC：初始化当前版本为 `V1.0`，建立期初基线和小/中/大跨代规则。
<!-- version-hook:history:end -->
