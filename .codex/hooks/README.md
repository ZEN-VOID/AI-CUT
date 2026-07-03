# Codex Hooks

本目录保存仓库级 Codex/Claude 事件钩子。

## github-push 版本钩子

- 配置：`.codex/hooks/hooks.json`
- 入口：`.codex/hooks/update_version_for_github_push.py`
- 实现：`.agents/skills/version-sync/scripts/sync_version.py`
- 触发：用户提示直接调用 `github-push` 时运行；`github-push` 技能本身也会在提交前显式调用同一脚本。
- 默认级别：`small`
- 覆盖级别：`VERSION_BUMP_LEVEL=none|small|medium|large`

钩子入口只负责转发参数和标准输入，不直接改写 `VERSION.md`。版本识别、递增、变更范围识别和更新明细写入都由 `version-sync` 技能包维护。

钩子配置在会话启动时加载；新增或修改后，需要重启 Claude/Codex 会话才会成为事件钩子。但 `github-push` 技能的显式脚本步骤不依赖会话重启。
