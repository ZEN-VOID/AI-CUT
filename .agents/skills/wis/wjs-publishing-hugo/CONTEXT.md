# Context: wjs-publishing-hugo

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 2805
current_lines: 92
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-publishing-hugo` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

### hugo-root-not-confirmed

- 症状：直接创建或编辑文章，才发现当前目录不是 Hugo 仓库根。
- 根因层：没有执行前置检测：`hugo.toml`/`config.toml` 与 `content/` 未确认。
- 立即修复：先定位正确仓库根；缺路径时让用户给出路径。
- 系统预防：每次开工先确认配置文件、`content/` 和现有帖子结构。
- 验证点：已读到 Hugo 配置和至少一篇现有帖子 front matter。

### front-matter-drift

- 症状：新增帖子的 date、lastmod、categories、tags、url 字段格式与仓库现状不一致。
- 根因层：手写 front matter 或套用默认格式，没有以仓库现有帖子为准。
- 立即修复：用 `scripts/new-post.py` 生成新帖；若仓库格式不同，按现状调整。
- 系统预防：不要手写新帖 front matter；技能文档中的格式只代表 maggiacito 现状。
- 验证点：新文件位于 `content/posts/<slug>.md`，front matter 与仓库样例一致。

### lastmod-not-updated

- 症状：编辑正文后 `lastmod` 仍停留在旧时间。
- 根因层：编辑帖子时只改正文，遗漏修改时间合同。
- 立即修复：更新 `lastmod` 为当前站点时区时间，`date` 保持原值。
- 系统预防：编辑路径中把 `lastmod` 作为固定检查项。
- 验证点：改过内容的帖子 `lastmod` 已变，`date` 未被误改。

### taxonomy-duplication

- 症状：新增了与现有分类近义或重复的 `categories[]`。
- 根因层：管理类目前没有先列出现有类目。
- 立即修复：运行类目列表脚本或扫描现有帖子，让用户从现有类目中选；确需新增再写入。
- 系统预防：类目变更前先查现状，合并/改名时批量替换所有帖子。
- 验证点：没有出现同义重复类目；改名后已提示旧 `/categories/<旧名>/` 链接会失效。

### url-collision-or-drift

- 症状：`url` 与已有帖子重复，或不符合迁移后的 WordPress 风格路径。
- 根因层：没有查重，也没有确认 `/<主类目>/<标题或slug>/` 的显式 URL 约定。
- 立即修复：搜索现有 `url:`；必要时通过脚本参数指定唯一 URL。
- 系统预防：新增帖子时把 URL 查重放在生成或发布前。
- 验证点：新 URL 唯一，且与仓库既有链接风格一致。

### upload-location-drift

- 症状：新图片被放进 `static/wp-content/uploads/` 或其他历史迁移目录。
- 根因层：混淆新上传目录与旧 WordPress 遗留目录。
- 立即修复：新图放 `static/uploads/<年>/`，用图片脚本生成 markdown 链接。
- 系统预防：历史目录只读保留，新上传固定走 `static/uploads/`。
- 验证点：正文引用路径为 `/uploads/...`，不是 `/wp-content/uploads/...`。

### deploy-trigger-confusion

- 症状：以为普通 push 不会触发部署，或误把反馈机器人 `GITHUB_TOKEN` 防递归限制套到本人推送。
- 根因层：发布合同里的部署触发边界没有区分。
- 立即修复：按仓库现有部署流 commit/push；需要时查看 Actions run。
- 系统预防：发布说明中区分“本人 push 会触发 deploy.yml”和“机器人 token 推送受限”。
- 验证点：push 后可看到部署工作流或明确说明未触发原因。

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认入口、路由、输出合同和门禁。
2. 每次开工先做前置检测：确认 Hugo 仓库根、读取配置、查看一篇现有帖子 front matter。
3. 新增帖子优先走 `scripts/new-post.py`；不要手写 front matter，除非仓库现状要求并已核对。
4. 编辑帖子时正文可直接改，但内容变更必须同步 `lastmod`，不改原 `date`。
5. 管理类目前先列出现有类目；改名/合并必须扫描所有 `content/posts/*.md`。
6. 上传图片固定放 `static/uploads/<年>/`，老的 `static/wp-content/uploads/` 只保留历史内容。
7. 发布前检查 URL 唯一性、front matter 格式、类目、图片路径；确认后 commit/push，必要时看部署状态。

## Reusable Heuristics

- 这个技能的角色是“对话式后台”：直接改 Hugo 仓库文件、提交、推送，不引入 CMS 或服务器。
- 仓库现状优先于技能默认格式；maggiacito 的权威格式是参考当前站点，不是所有 Hugo 站的硬规则。
- 新帖 front matter 的漂移成本高，能用脚本就不要手写。
- Hugo taxonomy 会自动生成分类页；新增类目不需要额外配置，但重复类目会长期污染导航。
- 图片路径读者会长期访问，新图目录要干净，迁移目录不要继续扩写。
- 发布问题先区分本地文件生成、git push、GitHub Actions 三层，不要混成一个“没上线”问题。

## Promotion Backlog

- 若 URL 撞车反复出现，考虑把 URL 查重并入 `new-post.py`。
- 若编辑后漏改 `lastmod` 反复出现，考虑增加帖子编辑 helper 或 pre-publish 检查。
- 若分类重复常见，考虑让 `categories.sh` 输出近义/大小写/空白差异提示。
- 若图片路径漂移常见，考虑在 `add-image.py` 增加历史目录拒绝或 warning。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
