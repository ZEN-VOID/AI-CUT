# Context: fanqie-download

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
current_chars: 17555
current_lines: 439
status: ok
recommended_action: keep-appending
last_checked_at: 2026-03-25T09:30:51Z
```
<!-- CONTEXT_HEALTH_END -->

本文件用于沉淀 `fanqie-download` 的运行经验证据。默认维护知识库核心。

## Type Map

| 失败类型 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- |
| FAIL-FQ-ROUTE-01 | 输入语义层 | 先区分 `关键词 / book_id / short-story-share / post_id` 再选入口 | 在 `SKILL.md` 固化路由判定与 ID 语义边界 | 不再出现把 `post_id` 直接喂给 `catalog.py` 的执行路径 |
| FAIL-FQ-STR-01 | 搜索入口层 | 对 `search.py` 执行候选节点回退并输出 API 诊断 | 保持 `search.py` 与 `catalog.py/download.py` 同级容错策略 | 关键词搜索在默认节点不可达时仍能切换节点返回结果 |
| FAIL-FQ-STR-02 | 目录门禁层 | 对 0 章目录强制转失败态，并补跑 detail 诊断 `BOOK_REMOVE` | 在 CLI/UI 两端统一“空目录=失败态”语义 | 空目录时不再出现“成功获取/下载完成”假象 |
| FAIL-FQ-MAT-01 | 正文下载层 | 对失败章节补缺重跑，并执行一致性校验 | 保持章节失败即非零退出码，长篇场景支持并发下载与重试 | 本地章节数、目录数、失败数三者一致 |
| FAIL-FQ-MAT-02 | 可见性层 | 检测“单文件内嵌多章”并按需拆分 `_split` 文件 | 将内嵌章节检测与 `--split-embedded` 写入标准流程 | 用户报“少章”时先核对内嵌章节提示与拆分结果 |
| FAIL-FQ-MAT-03 | 短篇分享抓取层 | 优先要求完整链接；仅给 `post_id` 时尝试复用缓存 `source_url` | 保持分享抓取对 `share_token/report_params` 的完整性校验 | 抓取结果同时生成正文文件与 `share_metadata.json` |
| FAIL-FQ-CTX-01 | 文本清洗与诊断层 | 正文写盘前做多轮 HTML 实体解码，失败时统一收敛为可读报错 | 保持 `download.py` 文本规范化与 CLI/UI 一致的错误语义 | 不再残留大批 `&#34;` / `&#39;`，且失败信息可直接指向下一步排查 |
| FAIL-FQ-STR-03 | 第三方依赖层 | 当自建 `api/search` / `api/directory` / `api/content` 节点整体失效时，回退到番茄官网搜索接口、书页目录解析与 `reader` 正文解码链路 | 在脚本内固化“第三方 API -> 官网 HTML/API”双通道兜底，避免技能因单一来源失效而整体瘫痪 | 在第三方节点全挂时，仍可完成 `book_id` 检索、目录落盘与章节明文下载 |
| FAIL-FQ-MAT-04 | 官网挑战页层 | 当 `reader` 页返回“验证码中间页”或 `middle_page_loading` 时，不要继续按普通正文页解析；优先尝试 `novel_web_id` / 浏览器会话 / 降并发 | 在官网正文兜底链路中增加挑战页识别与专门的 cookie / 浏览器策略，避免把挑战页误判成正文缺失 | 失败信息明确指出“挑战页拦截”，而不是笼统报“未解析到正文段落” |

## Repair Playbook

### 固定排障顺序

1. 先按输入类型路由：书名先搜索，`book_id` 走目录/下载，分享链接走短篇抓取。
2. 沿源层向上追：`SKILL.md` -> `scripts/config.py` -> 具体入口脚本 -> 运行证据。
3. 优先修高杠杆门禁：节点回退、0章失败态、章节失败转非零退出、完整链接检查。
4. 再做当次补救：补缺下载、强制重下、拆分内嵌章节、复用缓存 `source_url`。
5. 修复后必须做针对性回归：
   - 搜索链路：确认能返回可下载 `book_id`
   - 目录链路：确认 `metadata.json` 存在且 0章时有诊断
   - 下载链路：确认章节数与失败数收敛
   - 短篇链路：确认正文与元数据双文件齐备
6. 将复用价值高的模式写回 `Type Map / Reusable Heuristics`；若需保留长过程材料，外置到 `CHANGELOG.md` 或 `reports/`。

### 症状到入口的快速映射

- “书名搜不到 / 一上来就报连接失败”
  - 先查 `search.py` 与候选节点回退。
- “目录是 0 章 / 看起来下载完成但没内容”
  - 先查 `catalog.py` 的空目录门禁与 detail 诊断。
- “总章数不对 / 应该 12 章只看到 10 章”
  - 先查正文是否为单文件内嵌多章，再决定是否 `--split-embedded`。
- “正文里全是 `&#39;` / `&#34;`”
  - 先查 `download.py` 的文本规范化，不先手工改单个文件。
- “长篇下载半路失败”
  - 先启用 `-d 0 -w 8` 并在首轮后执行失败章节补缺收敛。
- “短篇分享抓不到正文”
  - 先确认链接是否带 `share_token`，再查缓存 `source_url` 是否可复用。

## Reusable Heuristics

- 书名驱动的任务默认先走 `search.py`，不要让用户手工猜 `book_id`。
- 当目录返回 0 章时，优先怀疑 `BOOK_REMOVE`、ID 语义错误或节点半可用，而不是先怀疑下载脚本本身。
- 千章级长书不要从单线程硬跑起步，优先 `-d 0 -w 8`，然后做失败章节补缺。
- 用户说“少章”时，先验证是不是“单文件内嵌多章”的可见性问题，再判断接口是否真的漏章。
- 分享抓取优先依赖完整链接；仅给 `post_id` 的场景属于降级路径，只能当缓存回退而不能当主路径。
- 正文异常优先做源层文本规范化与重下，不优先手修产出文件。
- 若第三方节点整体失效，但番茄官网页面可打开，优先切到“官网搜索/官网目录/官网 reader 正文解码”链路，不要把任务卡死在旧 API 上。
- 当官网 `reader` 页返回“验证码中间页”时，说明问题已经上升到浏览器 / cookie 指纹层；这时应暂停盲目并发重试，优先切换 cookie 探测或真实浏览器会话。

## Promotion Backlog

- [ ] 候选规则：为 `app.py` 增加与 CLI 对齐的并发下载入口
  - 证据数：0
  - 晋升目标：`SKILL.md` S7 / `app.py`
  - 状态：collecting
- [ ] 候选规则：将下载后的一致性校验沉淀为脚本级显式摘要输出
  - 证据数：1
  - 晋升目标：`scripts/download.py`
  - 状态：collecting
