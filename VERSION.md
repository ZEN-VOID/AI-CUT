# AI-VCR 版本记录

当前版本：`V1.0.1`
版本状态：期初基线
初始化日期：2026-07-07
最后更新：2026-07-13 03:47 UTC

## 当前版本摘要

`V1.0` 为 AI-VCR 建立与 AI-CUT 同构的仓库级版本展示和同步机制，让 `VERSION.md` 专注展示当前版本内容和每次更新细节。

本版关注三件事：

- 建立 AI-VCR 的仓库级版本基线，后续小更新、中更新和大更新都从这里递增。
- 接入 `.agents/skills/version-sync/`，集中维护版本递增、更新时间刷新、变更范围识别和更新明细写入。
- 保留 github-push 版本钩子为薄入口，只转交给 `version-sync` 脚本执行。

## 更新明细

<!-- version-hook:history:start -->
### V1.0.1 - 2026-07-13 03:47 UTC

- 版本变化：`V1.0` -> `V1.0.1`
- 更新级别：小更新
- 更新范围：version-sync skill update / workflow skill update / codex hook update / docs update / project asset update / repository config update
- 更新方式：version-sync 自动同步
- 更新内容：
  - 更新版本同步技能包，使版本展示、更新记录和自动化入口由统一脚本维护。
  - 同步 workflow 相关技能、模板、校验器、示例或经验文件变更。
  - 同步 Codex 钩子、自动化脚本或版本维护配置变更。
  - 更新仓库文档或展示页面，改善说明、记录或使用入口。
  - 同步 projects 工作区中的内容、素材、音频或生成产物变更。
  - 同步仓库配置、忽略规则或 Codex 运行约定。
  - 刷新顶部当前版本和最后更新时间，方便直接查看最新状态。

### V1.0 - 2026-07-07 07:58 UTC

- 版本变化：初始化为 `V1.0`
- 更新级别：期初基线
- 更新范围：repository version baseline / version-sync skill update / codex hook update
- 更新方式：参照 AI-CUT 版本机制手动建立
- 更新内容：
  - 建立 AI-VCR 仓库级版本基线。
  - 接入 `version-sync` 技能包作为版本展示、历史记录和自动化同步的单一执行入口。
  - 配置 `.codex/hooks/update_version_for_github_push.py` 作为 github-push 版本更新薄钩子。
  - 为后续自动更新历史记录预留可维护区域。
<!-- version-hook:history:end -->

## 维护说明

`VERSION.md` 的主用途是展示当前版本内容和每次更新细节。`version-sync` 脚本负责维护顶部的 `当前版本`、`最后更新`，并在上方历史区域追加新的更新条目。

版本递增口径保留为：小更新用于文档、提示词、校验器和兼容性修复；中更新用于工作流能力或输出合同升级；大更新用于架构、默认行为或跨代合同变化。
