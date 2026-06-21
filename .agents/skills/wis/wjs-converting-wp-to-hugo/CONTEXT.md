# Context: wjs-converting-wp-to-hugo

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2940
current_lines: 46
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-converting-wp-to-hugo` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 缺少 WXR 或 `uploads/` | 输入合同层 | 暂停迁移，要求用户提供 WordPress 全量导出 XML 和 `wp-content/uploads/` | 把 WXR + uploads 作为唯一输入门槛，不用线上抓站替代默认路径 | 工程根存在 WXR，`uploads/` 年/月目录完整 |
| 用户要求保留评论、会员、搜索等动态能力 | 任务适配层 | 明确静态 Hugo 不适用这些动态功能 | 在路由阶段先判定“去动态化迁移”还是“保留动态站” | 用户确认迁移目标是 Hugo + Markdown + GitHub Pages |
| 密码保护文章被误公开 | 安全 / 发布门禁层 | 用 ElementTree 解析 `<wp:post_password>` 并询问处理方式，默认排除 | 禁止用裸 grep 统计密码文章；发布前必须有用户决策 | 转换报告中密码文章处理方式和计数明确 |
| WordPress 脚手架页混入内容站 | 内容过滤层 | 排除 `sample-page`、登录/注册/找回密码短代码页、空页 | `is_real_page()` 规则保留为空正文、单短代码、默认 slug 黑名单 | 生成的 `content/` 不含脚手架页 |
| 老链接 `/archives/<id>/` 断链 | URL 保真层 | 从 WXR `<link>` 保留文章 URL，构建后跑 `verify_build.py` | URL 保持数字 archive 真源，不用 Hugo 默认 slug 重算 | `verify_build.py` 输出 missing 0 |
| CJK permalink 编码/解码不一致 | URL 规范化层 | 对路径执行 `unquote()`，让 Hugo 建 UTF-8 目录 | permalink 规范化逻辑不得回退为字面 `%xx` 目录 | 编码和解码形式的旧链接都能命中 |
| 图片仍从线上 WordPress 加载 | 资源本地化层 | 拷贝 uploads 到 `static/wp-content/uploads/`，正文改根相对路径 | 自托管 `wp-content` 图片一律本地化，外链图片才保留绝对 URL | 页面图片 URL 指向本地 `/wp-content/uploads/...` |
| `.gitignore` 误忽略静态图片 | 发布配置层 | 使用根锚定 `/uploads/`，不要写裸 `uploads/` | gitignore 必须区分原始输入 uploads 和发布用 static uploads | `static/wp-content/uploads/` 文件会进入提交清单 |
| WXR、数据库 dump 或敏感基础设施信息进入公开仓库 | 安全层 | `git rm --cached` 或重建干净历史后再推送 | 推送前检查 WXR、`.sql`、`wordpress_db` 和敏感设计文档 | `git diff --cached --name-only` 不含敏感输入 |
| GitHub Pages 首次 Action 在 `configure-pages` 处 404 | 部署顺序层 | 先开启 Pages workflow，再重跑 Action | 推送和部署 runbook 明确“先开 Pages，后跑 workflow” | 临时 Pages 地址 home/post/category/feed/image 全部 200 |

## Repair Playbook

1. 先确认输入真源：WXR 是内容唯一真相源，`uploads/` 是静态资源真源；缺任一项不进入全量迁移。
2. 迁移前先问两个必须决策：密码保护文章怎么处理、WordPress 脚手架页是否按默认排除。
3. 转换器改动坚持先测后写；任何 HTML 到 Markdown 规则变化都先补失败样例，再改转换逻辑。
4. 构建后必须用 `verify_build.py` 验证旧 URL，肉眼抽查图片帖、多链接帖和视频/iframe 透传。
5. 推公开仓库前先做敏感文件检查；如果历史已污染，优先重建干净历史，不靠 `.gitignore` 掩盖。
6. 部署先验证 GitHub Pages 临时地址，再切 DNS；WP 保持在线直到静态站稳定数日。
7. 新发现的高频坑先写入本文件；重复出现并有脚本或测试承载点后，再晋升到转换器、测试或 `SKILL.md`。

## Reusable Heuristics

- “不下载、不改名 uploads”是最小风险策略；只做路径本地化，避免迁移时制造第二资源真相。
- URL 保真比美化 slug 更重要；只要老站依赖 `/archives/<id>/`，就不要让 Hugo 默认 permalink 重新解释文章地址。
- 密码文章是发布安全问题，不是格式转换问题；没有用户确认前，默认排除比默认公开更安全。
- CJK URL 的判断要同时考虑静态目录名和浏览器入站解码；只看生成路径会漏掉线上断链风险。
- 公开仓库迁移时，把原始 WXR 和原始 uploads 当作敏感输入；发布产物只应包含 Markdown、主题和静态资源副本。
- Pages 部署问题先查是否已启用 Pages workflow，再查 Hugo 构建本身；`configure-pages` 404 通常是顺序问题。
- 静态站能力边界要早说明：评论、会员、动态搜索不属于本技能产出，不应在迁移中临时补第二套系统。

## Promotion Backlog

- 把密码保护文章 ElementTree 计数做成迁移前报告的固定字段，重复稳定后晋升为转换器门禁。
- 为 `.gitignore` 的 `/uploads/` 根锚定规则补一个发布前检查，防止 `static/wp-content/uploads/` 被误排除。
- 为 CJK permalink、gallery `<ul>`、`<a href>` 保留和 video/iframe 透传保留最小回归样例。
- 将 GitHub Pages “先启用后重跑”做成部署 checklist，避免每次从 Action 404 重新排查。
