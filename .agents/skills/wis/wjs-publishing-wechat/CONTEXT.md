# Context: wjs-publishing-wechat

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 1687
current_lines: 42
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-publishing-wechat` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

- 风格真源漂移：在 `SKILL.md`、草稿或经验层里临时改风格，会绕开 `STYLE.md`。修复时写作/润色前读取 `STYLE.md`，风格冲突以 `STYLE.md` 为准，机制问题才回到本技能。
- 轻润色变重写：把用户开头、结尾和语气整体改掉，违背“轻润色，不重写”。修复时只改错字、重复、分段和明显拗口处，拿不准宁可保留。
- 隐私扫描遗漏：定稿前没有逐句检查人名、场所、精确地点、联系方式等。修复时在 Step 1.5 泛化或删除，并在交付改动清单里标注“隐私”；无命中也明确写“隐私扫描：无”。
- 发布前跳过标题选择：文件包就绪后直接上传，会越过硬关卡。修复时给 A 原标题 + B/C/D 三个更有冲击力候选，等待用户选择后再上传。
- 配图进入不了草稿：`illustration.png` 没被 `article.md` 引用，或用户本地截图未上传 CDN。修复时确保解释图有 `![](./illustration.png)`，本地正文图片先 `md2wechat upload_image` 并替换 URL。
- 微信草稿 errcode：`40164` 多为 IP 白名单，`45004` 多为摘要为空/太短，`40007` 多为旧 `draft_media_id` 失效。修复时按错误归因处理，不盲目重跑。

## Repair Playbook

1. 先读取同目录 `SKILL.md`；涉及写作或润色时再读取 `STYLE.md`，把风格判断交给风格真源。
2. 输入太散时只问一次“想写一篇文章，还是几个独立想法？”；能判断时直接进入轻润色。
3. 润色后、定稿前执行隐私扫描；命中则泛化/删除并记录，不确定项问用户确认。
4. 生成 3 个标题候选和 50-80 字摘要，摘要只制造真实好奇缺口，不复写第一段。
5. 建立文章文件包，生成 `cover.png` 与 `illustration.png`；确认解释图在正文中被引用，额外本地图片已换成微信 CDN。
6. 上传前必须停在 Step 5.5，让用户从 A/B/C/D 或自拟标题中选择；更新 `meta.json` 后再执行发布脚本。
7. 发布后检查草稿可见、最近文章注入是否按本地账本生效，并按 errcode 定向处理失败。

## Reusable Heuristics

- `SKILL.md` 管机制，`STYLE.md` 管语气；不要把风格红线重复散落到经验层。
- 解释图自己说话，不给“如图所示”之类引导语；默认放在正文最后落点之后、后注或安装方法之前。
- 介绍具体 skill 的文章，末尾安装方法不是正文预算的一部分，但必须先确认 skill 已公开发布。
- 文末“最近文章”是本地账本的离线渲染；账本为空不阻断发布，permalink 回填失败也应降级处理。
- Raw HTML 块内部不能有空行；段内多行的 `<br>` 分行边界必须落在句末标点后。

## Promotion Backlog

- 增加发布前 validator：检查 `meta.json` 字段、摘要长度、隐私扫描标记、标题选择状态、解释图引用和本地图片残留。
- 把常见微信 errcode 整理为脚本输出中的人类可读诊断，减少重复查错。
- 增加“介绍 skill 的文章”检查：公开 URL 是否可访问、安装方法段是否存在、触发语是否填写。
- 为 `content.html` 增加图片一致性检查：`mmbiz` 数量等于正文图片数，本地 `img-` 路径为 0。

## Case Log

暂无案例。后续只追加可复用、可验证、可晋升的案例。
