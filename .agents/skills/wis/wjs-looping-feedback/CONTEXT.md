# Context: wjs-looping-feedback

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2568
current_lines: 49
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-looping-feedback` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| symptom | root_cause_layer | immediate_fix | systemic_prevention | verification |
| --- | --- | --- | --- | --- |
| 以为需要自建后端或在客户端放密钥 | architecture boundary | 改回“GitHub Issue 预填 + GitHub Actions 执行”的无后端路径 | 安装说明中持续强调无客户端密钥、无额外服务 | 前端只生成 issue 链接，仓库里没有暴露 token |
| 非 allowlist 用户提交建议后也触发自动改站 | security gate | 检查 `FEEDBACK_ALLOWLIST` 与 workflow 的作者校验，未授权即关闭 issue | 把 allowlist 作为安装必填项和验收项 | 未授权 issue 被关闭，Claude Code Action 不运行 |
| GitHub Pages/同仓 Actions 部署没有被反馈提交触发 | deploy trigger | 给部署 workflow 补 `workflow_run` bridge | 安装前先识别部署宿主：外部 push-deploy 还是同仓 Actions | bot commit 到 `main` 后能看到后续部署 run |
| 把本技能当成托管服务，期望匿名提交或多租户计费 | scope mismatch | 说明本技能只在用户自己的 repo 和自己的 auth 下运行 | 安装前确认 submitter 需要 GitHub 账号，owner 提供 Pro/Max OAuth 或 API key | 没有新增外部服务、匿名入口或共享账单依赖 |
| 自动改站后没有 ledger / dashboard 记录 | runtime artifact | 检查 `.feedback/feedback-ledger.json` 和 `/_feedback` 更新步骤 | workflow 的 finalize 阶段必须写账本和 dashboard | issue 评论、commit、dashboard 三处能互相追踪 |
| revert 被当成手工 git revert，绕过反馈闭环 | revert route | 使用 `revert: #N` issue 走同一套 ledger/dashboard 流程 | 把 revert 视为反馈闭环的一等路径 | dashboard 上对应建议显示 revert 状态和提交 |
| 安装时没有识别 Hugo / Next.js / Astro / static 差异 | install routing | 回到 `references/install.md` 的探测与注入步骤 | 安装脚本/说明按站点类型注入 widget 与 dashboard | 目标站点构建通过，浮动按钮和 `/_feedback` 均可访问 |

## Repair Playbook

1. 先确认目标是“给网站仓库安装反馈闭环”，不是搭建托管 SaaS 或开放匿名反馈系统。
2. 安装前识别站点类型和部署路径，尤其区分外部 push-deploy 与同仓 GitHub Actions 部署。
3. 只向用户索取两个必要输入：GitHub allowlist 和执行 auth；不要要求客户端密钥或新后端。
4. 按 `references/install.md` 复制 `.feedback/` 运行时、workflow、widget 和 dashboard。
5. 验证 allowlist gate、issue label、自动 commit、ledger 更新、dashboard 更新和 issue 评论。
6. 若部署由同仓 Actions 负责，必须验证 `workflow_run` bridge；否则自动 commit 可能不会上线。
7. 回滚需求走 `revert: #N` issue，保持 ledger 与 dashboard 的可追踪性。

## Reusable Heuristics

- 这个技能的关键约束是“借用 GitHub 作为队列和执行器”，不是“把网站接入一个新服务”。
- `GITHUB_TOKEN` 推送不能触发同仓另一个 workflow 是最常见部署断点；安装前先问清部署方式能省掉大量误判。
- allowlist 是安全边界，不是体验选项；没有 allowlist 就不应让自动改站链路上线。
- `/_feedback` 是用户可审计界面，`.feedback/feedback-ledger.json` 是运行时账本；两者缺一都会削弱闭环可信度。
- Revert 也要被记录进同一套系统，否则“可一键撤销”会变成口头承诺。

## Promotion Backlog

- [ ] 候选规则: 增加安装前 preflight 清单，固定检查站点类型、部署宿主、allowlist、auth 与 dashboard 路径。
  - 证据计数: 0
  - 目标落点: `references/install.md` 或安装脚本提示
  - 状态: pending
- [ ] 候选规则: 为同仓 Actions 部署生成 `workflow_run` bridge 示例，减少 GitHub recursion prevention 漏配。
  - 证据计数: 0
  - 目标落点: `references/install.md`
  - 状态: pending

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
