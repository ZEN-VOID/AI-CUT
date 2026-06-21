# Context: wjs-publishing-appstore

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3486
current_lines: 50
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-publishing-appstore` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
| --- | --- | --- | --- | --- |
| App 尚未成功进过 TestFlight 就尝试上架 | 前置链路层 | 先回到 `wjs-publishing-testflight` 完成 signing、CI、beta lane 和至少一个 TestFlight build | 本技能只处理 listing + release lane，不接管 build/signing 初始化 | ASC 中已有 app record 和可选 build |
| `Could not find app` 或 ASC app record 缺失 | App Store Connect 初始化层 | 用 `fastlane produce` 创建 app record | 第一次上架前把 bundle id、app name、ASC 记录作为 checklist 项 | deliver 能找到目标 app |
| App Store name / metadata 被拒 | 元数据字段合同层 | 修改 display name、keywords、subtitle、description 等文本，满足长度和唯一性 | 写文案前先检查 name 30、subtitle 30、keywords 100、promo 170、description 4000 | `fastlane deliver` preview 无字段错误 |
| 截图缺失、尺寸错误或 CI 上传为空 | 截图资产层 | 重新拍 6.9" PNG，移除 `fastlane/screenshots/` 的忽略规则并提交 | 只在 iPad family 包含 iPad 时增加 13" iPad pass；否则 6.9" 覆盖 iPhone-only | 每个 locale 有命名规范 PNG，CI 能读取 |
| 模拟器截图被权限弹窗或 iOS 26 伪影污染 | 截图环境层 | 手动允许麦克风权限一次；对不可达页面用 env-gated DebugRoot | 不把 macOS synthetic click 当稳定脚本能力；sim-only 伪影先用真机或最小复现确认 | 重新截图无权限弹窗，关键画面干净 |
| release lane 被误当作 push 自动触发 | 发布门禁层 | 保持 `fastlane release` 显式触发，避免 push 自动提交审核 | beta lane 和 release lane 分离；提交审核必须是人为发起 | CI / Fastfile 中无 push-to-review 路径 |
| 首次提交最后一步失败，提示 age rating / pricing / privacy / content rights | ASC 一次性配置层 | 到 ASC web console 补齐年龄分级、定价、内容权利、隐私标签 | 首次 release 前把 console-only 项列入人工门禁，不指望 fastlane 全覆盖 | 重新提交不再出现缺失属性列表 |
| 提交了错误 build 或 build 尚未处理完成 | build 选择层 | 先等 beta lane 上传并处理完成，再 `release skip_build:true` 复用该 build | 两步发布：push main → TestFlight processed → workflow_dispatch appstore | ASC 版本关联的是预期 build |
| 已在审核中还想换 build / 文案 / 截图 | ASC 状态层 | 在 ASC 中 Remove this version from review，再重新 dispatch release | `guard_not_in_review` 阻止重复提交，更新前先退回 editable 状态 | 版本状态回到 Waiting for Review |

## Repair Playbook

1. 先确认 TestFlight 前置完成：match、ASC API、beta lane、至少一个已处理 build 和 ASC app record。
2. 初始化或复用 `fastlane/metadata/{zh-Hans,en-US}`；脚手架不得覆盖已有手写文案。
3. 写文案时逐项检查长度、keywords 无空格、review_information、privacy URL 和 App Store name 唯一性。
4. 截图先按 iPhone 6.9" 做每个 locale；检查目标设备族后再决定是否补 iPad。
5. 在 Fastfile 中加入 release lane 后，先跑 deliver preview，确认 metadata + screenshots 能被本地 fastlane 读取。
6. 首次提交前手动检查 ASC web console：age rating、pricing、content rights、App Privacy、build attachment。
7. 正式提交优先使用两步法：main 触发 beta 并等待处理完成，再显式 `release skip_build:true`。
8. 若版本已在审核中需要修改，先在 ASC 移出审核，再重新提交；不要绕过 `guard_not_in_review`。

## Reusable Heuristics

- App Store 上架不是 TestFlight 发布的延伸自动化；审核提交必须保持显式、可撤回、可预览。
- metadata 和 screenshots 必须提交到 `main` 后再 dispatch CI release，否则 CI 看不到最新 listing 资产。
- `fastlane/screenshots/` 在 TestFlight-only 项目里常被 gitignore；上架链路必须显式解除该忽略。
- 首次提交失败通常发生在最后一步，但前面的 metadata / screenshots 已上传；补 ASC console 后可重新 dispatch。
- screenshot 必须匹配正在提交的 binary；不要用未来版本功能图提前包装当前 build。
- iOS 模拟器权限和 Liquid Glass 伪影要先区分环境问题与应用问题，避免无效改代码。

## Promotion Backlog

- 增加 metadata linter：检查必填文件、占位符、长度限制、keywords 格式、privacy URL 和 review_information。
- 增加 screenshot preflight：校验 locale 目录、PNG 尺寸、命名、数量、设备族和 `.gitignore` 状态。
- 增加 Fastfile audit：确认 release lane 不绑定 push 自动触发，且包含 `guard_not_in_review` 和合规答案。
- 增加 ASC first-submit checklist 模板：age rating、pricing、content rights、App Privacy、build attachment。
- 增加 CI release dry-run 指南：区分 beta、appstore workflow_dispatch、`skip_build:true` 和 processed build 等待状态。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
