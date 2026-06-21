# Context: wjs-publishing-testflight

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2704
current_lines: 60
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-publishing-testflight` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

- `placeholder_or_scheme_drift`
  - 症状：CI 找不到 xcodeproj、scheme、target，或 bundle id 与 provisioning profile 不匹配。
  - 根因层：从参考实现复制时占位符替换不完整。
  - 立即修复：全局核对 `YOUR_BUNDLE_ID`、`YOUR_APP`、`YOUR_SCHEME`、xcodeproj 路径和 target 名称。
  - 系统预防：把替换清单作为项目接入完成门禁。
  - 验证点：PR build 可在无签名模式下编译，`fastlane beta` 能定位同一 scheme 与 bundle id。
- `match_or_secret_shape_failure`
  - 症状：找不到 provisioning profile、ASC 401、match 拉证书失败、tag push 失败。
  - 根因层：证书仓库、GitHub secrets 或 PAT 权限形态错误。
  - 立即修复：本地先跑 `match appstore/development` 建立证书；检查 `MATCH_GIT_BASIC_AUTH`、ASC key content、`FEEDBACK_PAT` scope。
  - 系统预防：只把 secret 名称和格式写入仓库，真实 `.p8` 与密码只进 GitHub Secrets。
  - 验证点：Actions 能完成 match、build、upload，并能推送 `testflight/*` 或 `release/*` tag。
- `release_state_collision`
  - 症状：自动或手动提审在 App Store 版本 `IN_REVIEW` 时失败，或版本号/tag 判断失真。
  - 根因层：App Store 状态与本地版本/tag 真源未对齐。
  - 立即修复：等待审核结束或取消后再 release；确保 checkout 拉完整 history 和 tags。
  - 系统预防：保留 `guard_not_in_review`，并用 `release/*` tag 作为已发布版本真源。
  - 验证点：release lane 只在可编辑版本状态下提交审核，TestFlight lane 正常打 build tag。
- `ci_mutates_main_unexpectedly`
  - 症状：CI 自动改 `MARKETING_VERSION` 或 pbxproj 后尝试提交 main。
  - 根因层：混淆了本地 bump 与 CI 发布职责。
  - 立即修复：CI 可以计算和使用版本，但不得 commit/push main；手动 bump 必须由开发者本地提交。
  - 系统预防：CI 只上传 binary 与 tag，不改写主分支业务文件。
  - 验证点：Actions 结束后 main 无由 CI 产生的 pbxproj commit。

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认任务是为现有 iOS 项目接入 fastlane + GitHub Actions 到 TestFlight。
2. 建立替换清单，先定位 bundle id、repo/app 名、scheme、target、xcodeproj 和 certs repo 名。
3. 生成或修改 `Appfile`、`Matchfile`、`Fastfile`、`Gemfile`、workflow 时，保持 secrets 只以名称引用。
4. 本地先跑 bundle install 与 match 初始化；CI 侧再配置 GitHub Secrets。
5. 用 PR build 验证无签名编译，用空 commit 或 workflow_dispatch 验证 TestFlight 上传。
6. 处理 release 时先检查 `IN_REVIEW`、release tag、pbxproj marketing version，再决定 beta、auto release 或 explicit release。

## Reusable Heuristics

- Cathier 的“每第 10 个 build 自动提审”是参考约定，不是所有新项目的业务必选项。
- `fetch-depth: 0` 与 `fetch-tags: true` 是 release notes 和版本判断的基础，不是性能细节。
- `ASC_API_KEY_CONTENT` 应是 base64 后的 `.p8` 内容；不要把 `.p8` 文件写入仓库或日志。
- `MATCH_GIT_BASIC_AUTH` 需要覆盖 certs repo 访问；tag push 需要单独确认 checkout token 权限。
- TestFlight 成功的用户可见结果是 App Store Connect 出现新 build；本地 `fastlane` 成功日志不等于审核流完成。
- 自动提审前必须尊重 App Store 当前审核状态；遇到 `IN_REVIEW` 应停止而不是覆盖。

## Promotion Backlog

- 抽出项目接入参数模板，减少手工替换 `YOUR_*` 占位符的漏改风险。
- 增加 workflow lint/preflight：检查 Xcode 路径、Ruby、fetch tags、secrets 名称和 placeholder 残留。
- 增加本地 dry-run 文档：验证 scheme、bundle id、match repo、tag 权限和 ASC key 形态。
- 将常见 CI 错误映射成排查表：profile、ASC、tag push、review state、version compare。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
