# AI-CUT 版本记录

当前版本：`V1.0.4`
版本状态：期初基线后的连续小更新
初始化日期：2026-07-02
最后更新：2026-07-03 05:34 UTC

## 当前版本摘要

`V1.0.3` 将版本维护从零散 hook 逻辑迁移为独立的 `version-sync` 技能包，让 `VERSION.md` 专注展示当前版本内容和每次更新细节。

本版关注三件事：

- 新增 `.agents/skills/version-sync/`，集中维护版本递增、更新时间刷新、变更范围识别和更新明细写入。
- 将 github-push 版本钩子改成薄入口，只转交给 `version-sync` 脚本执行。
- 补充测试覆盖，防止后续自动记录退回单行规则式日志。

## 更新明细

<!-- version-hook:history:start -->
### V1.0.4 - 2026-07-03 05:34 UTC

- 版本变化：`V1.0.3` -> `V1.0.4`
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

### V1.0.3 - 2026-07-03 05:27 UTC

- 版本变化：`V1.0.2` -> `V1.0.3`
- 更新级别：小更新
- 更新范围：version-sync skill update / codex hook update / docs update
- 更新方式：version-sync 自动同步
- 更新内容：
  - 新增 version-sync 技能包，集中维护 VERSION.md 的版本递增、更新时间和更新明细写入。
  - 将 github-push 版本钩子改为薄入口，不再直接改写 VERSION.md，而是转交给 version-sync 脚本。
  - 补充测试覆盖详细更新块和变更范围分类，避免后续记录退回单行规则式日志。
  - 刷新顶部当前版本和最后更新时间，方便直接查看最新状态。

### V1.0.2 - 2026-07-03 03:51 UTC

- 版本变化：`V1.0.1` -> `V1.0.2`
- 更新级别：小更新
- 更新范围：workflow skill update
- 更新方式：github-push 自动更新
- 更新内容：
  - 扩展 `validate_visual_contract.py`，加强开头素材、私域引流素材、社交广告 PiP、网格展示和可读尺寸等检查。
  - 新增 `visual-contract-social-pass` 通过样例，用于覆盖社交广告视觉合同的回归场景。
  - 同步 workflow 的 `SKILL.md`、README、审查合同、执行报告模板、输出模板、测试提示和经验文件。

### V1.0.1 - 2026-07-02 03:38 UTC

- 版本变化：`V1.0` -> `V1.0.1`
- 更新级别：小更新
- 更新范围：workflow skill update / codex hook update
- 更新方式：github-push 自动更新
- 更新内容：
  - 建立 `VERSION.md` 和 github-push 自动版本更新钩子。
  - 增加 `.codex/hooks/update_version_for_github_push.py`、钩子配置、示例输入和说明文档。
  - 同步 workflow 说明、技能合同、视觉合同校验器和执行报告模板，减少内部流程标签泄漏到面向观众的画面中。

### V1.0 - 2026-07-02 03:30 UTC

- 版本变化：初始化为 `V1.0`
- 更新级别：期初基线
- 更新范围：repository version baseline
- 更新方式：手动建立
- 更新内容：
  - 建立仓库级版本基线。
  - 记录后续小更新、中更新和大更新的递增口径。
  - 为 github-push 自动更新历史记录预留可维护区域。
<!-- version-hook:history:end -->

## 维护说明

`VERSION.md` 的主用途是展示当前版本内容和每次更新细节。`version-sync` 脚本负责维护顶部的 `当前版本`、`最后更新`，并在上方历史区域追加新的更新条目。

版本递增口径保留为：小更新用于文档、提示词、校验器和兼容性修复；中更新用于工作流能力或输出合同升级；大更新用于架构、默认行为或跨代合同变化。
