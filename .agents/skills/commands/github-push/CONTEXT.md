# github-push CONTEXT

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 1433
current_lines: 46
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

## Type Map

- `remote_or_upstream_absent`
  - 症状：`git remote -v` 为空，或当前分支没有上游关系。
  - 根因层：技能边界，不是同步执行问题。
  - 立即修复：停止 `/github-push`，要求用户显式确认建仓、绑仓或设置上游。
  - 系统预防：把远端与上游检查放在提交和推送前，避免在同步流程里猜测 `origin`。
  - 验证点：远端存在、当前分支存在上游，才进入暂存、提交、推送。
- `cleanup_scope_drift`
  - 症状：运行缓存、调试探针、临时夹具混进待提交集合，或未跟踪正式资产被误删。
  - 根因层：清理分类不清，不是 Git 命令本身失败。
  - 立即修复：先跑仓库清理入口；若不存在统一脚本，则逐项说明删除、保留和判断理由。
  - 系统预防：反复出现的缓存噪音应收束到 `.gitignore` 或清理脚本，而不是每次手工清。
  - 验证点：`git status --short` 中只剩本轮正式交付物。
- `post_commit_dirty_tree`
  - 症状：提交成功后工作区仍有挂起改动，直接 push 会漏同步。
  - 根因层：提交后未复查状态。
  - 立即修复：重新检查 `git status -sb`，把同属本轮的正式改动补提；不相关改动保持不动并报告。
  - 系统预防：把提交后状态复查作为 push 前门禁。
  - 验证点：本地分支哈希与 `origin/<branch>` 一致，且无额外挂起改动。

## Repair Playbook

1. 先回读同目录 `SKILL.md`，确认本轮只处理“已有远端上的同步”，不承担建仓、绑仓或恢复远端。
2. 用状态检查建立待处理清单，先区分正式交付物、临时产物、被忽略缓存和用户未完成改动。
3. 优先使用 `scripts/dev_artifact_cleanup.py`；缺失时只做目标化清理，并保留删除与保留理由。
4. 提交后再次检查工作区状态；若仍有本轮正式改动，补提交后再推送。
5. 推送后做本地/远端哈希一致性检查；失败时优先定位上游、权限或远端拒绝原因。

## Reusable Heuristics

- 这个命令的关键价值是“清理后再推”，不是单纯代替 `git push`。
- 若仓库没有统一清理脚本，也要保留“删除了什么、保留了什么、为什么”的显式报告。
- 未跟踪文件不是默认垃圾；只有能证明是临时探针、缓存或一次性夹具时才删除。
- 运行时缓存反复出现时，优先修忽略规则或清理脚本这个规则源。
- 用户没有提供提交信息时可以生成时间戳消息；用户提供时不得改写其核心意图。
- 工作区中存在不相关改动时，只同步本轮负责范围，不为了“干净”而覆盖或回退他人改动。

## Promotion Backlog

- 为 `dev_artifact_cleanup.py` 增加 dry-run 摘要，输出删除候选、保留候选和规则命中原因。
- 增加一个轻量 preflight，统一检查 remote、upstream、dirty tree 与 ignored cache 噪音。
- 将高频缓存噪音晋升到仓库 `.gitignore` 或清理脚本，而不是继续依赖人工识别。
