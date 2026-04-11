# Context: fanqie-download

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 17555
current_lines: 439
current_cases: 12
status: ok
recommended_action: keep-appending
last_checked_at: 2026-03-25T09:30:51Z
```
<!-- CONTEXT_HEALTH_END -->

本文件用于沉淀 `fanqie-download` 的运行经验证据。默认维护知识库核心，Case 仅记录里程碑级事件。

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
6. 将复用价值高的模式写回 `Type Map / Reusable Heuristics`；只有里程碑事件才追加 `Case Log`。

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

### [FQ-20260330-013] 2026-03-30 第三方 API 全挂但番茄官网仍可访问，导致技能链路整体失效

#### symptom
- 用户以“技能路径 + 书名（《欢迎乘坐地狱巴士》）”触发执行。
- `search.py`、`catalog.py` 与 `download.py` 依赖的第三方节点全部失败：
  - `http://47.108.80.161:5005` / `http://101.35.133.34:5000` / `http://103.236.91.147:9999` 返回 `RemoteDisconnected`
  - `https://bk.yydjtc.cn` 返回 `502 Bad Gateway`
- 但番茄官网书页 `https://fanqienovel.com/page/7267831881867988027` 与章节页 `https://fanqienovel.com/reader/7267949118029302796` 仍可访问。

#### root cause
- layered trace:
  - `Symptom/Failure`：技能在搜索、目录、正文三个主链路全部报错，无法继续下载。
  - `Direct Technical Cause`：实现层把第三方 API 节点当成唯一数据源；当这些节点整体失效时，没有官方页面/接口兜底。
  - `规则源`：`scripts/search.py` / `scripts/catalog.py` / `scripts/download.py` 仅实现了第三方节点候选切换，没有实现“官网可访问时的第二通道”。
  - `规则源的规则源`：仓库 `AGENTS.md` 的 Root-Cause First / Learning Loop / Enhancement-complete closure 要求修高杠杆源层并沉淀成可复用预防机制。
  - `Fix Landing Points`：`scripts/search.py`、`scripts/catalog.py`、`scripts/download.py`、`scripts/charset.json`、`SKILL.md`、`CONTEXT.md`。

#### final fix
- immediate fix（当次任务恢复）：
  - 先从番茄官网书页确认目标 `book_id=7267831881867988027`；
  - 验证官网 `reader` 页正文可通过字符表解码为明文。
- systemic prevention fix（源层增强）：
  - `search.py`：第三方搜索节点全部失败时，回退到番茄官网搜索接口。
  - `catalog.py`：第三方目录节点全部失败时，回退到番茄官网书页 HTML 目录解析。
  - `download.py`：第三方正文节点全部失败时，回退到番茄官网 `reader` 页 / 官方 reader 接口，并用 `charset.json` 解码私有区字体正文。
  - 合同同步：`SKILL.md` 写明双通道兜底策略。

#### prevention checklist
- [x] 搜索层不再把第三方 `api/search` 当唯一来源。
- [x] 目录层在官网书页可访问时可直接解析章节列表。
- [x] 正文层在官网 `reader` 页可访问时可自动解码私有区字体正文。
- [x] 文档契约同步标注“第三方 API -> 官网页面/API”双通道兜底。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/search.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/charset.json`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/CONTEXT.md`

#### user feedback/constraint
- 用户输入极简，目标是直接把《欢迎乘坐地狱巴士》落盘，不接受停留在“API 挂了请稍后再试”的建议层。

## Case Log

### [FQ-20260303-012] 2026-03-03 千章长书在高并发下载时出现批量超时失败

#### symptom
- 用户以书名触发整本下载：《大明：夭寿了，我竟成了短命朱标》。
- 目录返回 `1278` 章，单线程耗时过长；并发拉取后主流程完成但出现失败章节（首次并发收敛后剩余 `22` 章失败）。

#### root cause
- layered trace:
  - `Symptom/Failure`：长书下载耗时过长，并发后出现阶段性失败章节。
  - `Direct Technical Cause`：上游 `https://bk.yydjtc.cn` 在高并发下出现间歇性 `ReadTimeout`，导致章节请求失败并被汇总为任务失败。
  - `规则源`：`scripts/download.py` 仅支持串行模式，缺少并发参数与线程内连接复用；长书场景无法在可接受时长内稳定完成。
  - `规则源的规则源`：仓库 `AGENTS.md` 的 Root-Cause First / Learning Loop 要求“先做源层增强，再做本次补救收敛”。
  - `Fix Landing Points`：`scripts/download.py`、`SKILL.md`、`references/README.md`、本 `CONTEXT.md`。

#### final fix
- immediate fix（当次任务恢复）：
  - 先用并发模式完成主下载，再对失败章节执行补缺重跑，最终 `失败=0`。
  - 一致性校验通过：`catalog=1278, missing=0`，本地章节文件数 `1278`。
- systemic prevention fix（源层增强）：
  - `download.py` 增加 `-w/--workers` 并发下载参数（`workers>1` 启用并发模式）。
  - 引入线程内复用 `requests.Session`，降低重复握手开销。
  - 文档同步：`SKILL.md` 与 `references/README.md` 增加并发用法与参数说明，明确 `workers>1` 时忽略 `--delay`。

#### prevention checklist
- [x] 千章级任务默认优先使用并发参数（建议 `-d 0 -w 8` 起步）。
- [x] 首轮并发结束后必须执行“失败章节补缺重跑”收敛。
- [x] 完成后执行一致性校验（目录章节数、缺失数、本地落盘数）。
- [x] 脚本参数与技能文档保持同步，避免执行契约漂移。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7233058634232499257/metadata.json`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7233058634232499257/chapters/`

#### user feedback/constraint
- 用户输入极简（技能路径 + 书名），约束是直接可执行并落盘，不接受停留在建议层面。

### [FQ-20260223-011] 2026-02-23 “应为12章但只看到10章” 的章节可见性误判

#### symptom
- 用户反馈：目标内容应为 `12` 章，但当前只看到 `10` 章。
- 本地下载文件为单文件落盘（目录仅 1 条），容易被误判为“章节不全”。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`: 旧逻辑仅按目录条目落盘，不对“单文件正文内嵌多章”做显式识别与提示，也无一键拆分能力。
- 根因判定：不是接口少返回，而是输出形态缺少“内嵌章节可见性”门禁，导致用户对章节完整性产生误判。

#### final fix
- 源层修复：
  - 在 `download.py` 新增 `split_embedded_chapters()`，识别 `第一章/第二章...` 等内嵌章节标题。
  - 默认下载时增加诊断提示：若检测到内嵌章节，输出“检测到内嵌 N 章（首章~末章）”。
  - 新增参数 `--split-embedded`：将内嵌章节拆分到 `chapters/_split/*.txt`。
- 局部落地：
  - 对 `book_id=7534347382301936702` 重新执行 `-f --split-embedded`，实际生成 `12` 个拆分章节文件。
  - 主文件中可定位 `第十一章` / `第十二章`（行号 `378` / `415`）。
- 文档同步：
  - 更新 `SKILL.md` 与 `references/README.md` 的命令示例、参数表与注意事项。

#### prevention checklist
- [x] 单文件正文场景必须给出“内嵌章节检测”提示。
- [x] 提供显式拆分参数，避免把“目录单条”误判为“内容缺章”。
- [x] 文档与脚本参数保持一致，避免执行口径分裂。
- [x] 用户报“章节数量不对”时，先核对正文内嵌章节标记再判定缺失。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7534347382301936702/chapters/重生后，我抢嫁活阎王.txt`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7534347382301936702/chapters/_split/第十一章.txt`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7534347382301936702/chapters/_split/第十二章.txt`

#### user feedback/constraint
- 用户期望直接拿到正确章节数，不接受“看起来像少章”的输出。

### [FQ-20260223-010] 2026-02-23 默认节点不可达导致“书名搜索直接失败”

#### symptom
- 用户以“技能名 + 书名（《后宫皆大佬，就我是咸鱼》）”触发执行时，`search.py -j` 直接报错：
  - `HTTPConnectionPool(host='47.108.80.161', port=5005)... Failed to establish a new connection: [Errno 61] Connection refused`。
- 在该失败态下，标准流程“先搜索 book_id，再目录/下载”无法继续。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/search.py`: 搜索链路仅请求当前默认 API Base，缺少候选节点回退。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`: 目录/详情链路同样仅请求单节点，与 `download.py` 的容错能力不一致。
- 根因判定：入口能力不对称（`download.py` 有节点切换，而 `search.py/catalog.py` 无），导致“可下载能力存在但前置检索/目录被单点故障卡死”。

#### final fix
- 源层修复：
  - 在 `search.py` 增加“节点候选回退 + 单节点重试 + 聚合失败诊断”。
  - 在 `catalog.py` 新增 `request_json_with_base_fallback()`，统一目录/详情请求的节点回退与重试逻辑。
- 源层增强（系统性预防）：
  - 更新 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md` 与 `references/README.md`，将“search/catalog/download 全链路节点切换”写入契约，避免后续执行口径分裂。
- 本次任务结果：
  - 成功检索到目标 `book_id=7589454200036150297`；
  - 成功下载到 `input/番茄小说/7589454200036150297/chapters/后宫皆大佬，就我是咸鱼.txt`。

#### prevention checklist
- [x] 搜索入口必须具备节点回退能力，禁止单节点硬依赖。
- [x] 目录入口必须与下载入口保持同级容错策略（重试 + 切换 + 可读诊断）。
- [x] 文档契约明确标注“全链路节点切换”，防止实现与说明不一致。
- [x] 出现网络类失败时优先做源层修复后再继续当次下载任务。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/search.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7589454200036150297/metadata.json`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7589454200036150297/chapters/后宫皆大佬，就我是咸鱼.txt`
- 运行证据（stderr）：`提示: 搜索接口已切换 API 节点 http://47.108.80.161:5005 -> https://bk.yydjtc.cn`

#### user feedback/constraint
- 用户输入非常精简（仅技能路径 + 书名），约束是直接可执行，不接受停留在排查建议层面。

### [FQ-20260220-009] 2026-02-20 章节仍残留 `&#39;` 与潜在双重实体编码

#### symptom
- 用户在替换 `&#34;` 后，仍发现 `&#39;` 及其他潜在“乱码”风险。
- 目标文件在处理前仍含 `&#39;` 20 处。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`: 原逻辑只做单轮 `html.unescape`，对历史文件无清洗，且对双重实体（如 `&amp;#39;`）鲁棒性不足。
- 根因判定：实体解码策略不完整（单轮）+ 缺少历史文件批量清洗流程。

#### final fix
- 源层修复：
  - 在 `download.py` 新增 `normalize_chapter_text()`，执行多轮实体解码（最多 3 轮）并规范空白字符（NBSP/BOM）。
  - 正文写盘前统一调用该规范化函数。
- 局部修复：
  - 对 `input/番茄小说/7488719811606757913/chapters/*.txt` 批量清洗实体编码；
  - 本次共修改 1 个文件，实体总数 `20 -> 0`。

#### prevention checklist
- [x] 下载链路改为多轮实体解码，覆盖 `&#34;`/`&#39;`/`&amp;#...;`。
- [x] 对已下载历史文本支持批量实体清洗。
- [x] 验收时检查是否残留 `&...;` 实体串。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7488719811606757913/chapters/太子总让我咒人.txt`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/CONTEXT.md`

#### user feedback/constraint
- 用户明确要求处理 `&#39;` 以及其它可能乱码，不接受仅修单一实体。

### [FQ-20260220-008] 2026-02-20 正文章节含 HTML 实体导致引号乱码（&#34;）

#### symptom
- 用户下载章节后发现正文出现 `&#34;`，期望显示为正常英文双引号 `"`。
- 目标文件：`input/番茄小说/7488719811606757913/chapters/太子总让我咒人.txt`。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`: 章节正文落盘前未做 HTML 实体解码。
- 根因判定：上游接口偶发返回实体编码文本，脚本按原样写盘，导致阅读层出现“乱码”。

#### final fix
- 源层修复：
  - 在 `download.py` 中对章节正文统一执行 `html.unescape()`，落盘前还原实体字符。
- 局部修复：
  - 对已下载文件执行定点替换：`&#34; -> "`（共替换 666 处，残留 0 处）。

#### prevention checklist
- [x] 正文落盘前执行 HTML 实体解码。
- [x] 遇到历史文件乱码时先做定点替换，再决定是否强制重下。
- [x] 验收时增加实体残留检查（至少检查 `&#34;`）。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7488719811606757913/chapters/太子总让我咒人.txt`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/CONTEXT.md`

#### user feedback/constraint
- 用户明确要求将 `&#34;` 还原为正常英文双引号，并验证结果。

### [FQ-20260220-007] 2026-02-20 默认节点目录可用但正文断连导致“可查不可下”

#### symptom
- 《太子总让我咒人》（`book_id=7488719811606757913`）目录可获取，但正文下载连续失败：
  - `RemoteDisconnected('Remote end closed connection without response')`。
- 原脚本在章节失败后仍输出“下载完成”并返回 0，造成成功假象。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/config.py`: 默认节点 `http://47.108.80.161:5005` 在当前时段出现“目录接口可用、正文接口断连”的半可用状态。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`: 无节点故障切换能力；章节级失败统计未强制转失败态。
- 根因判定：单节点依赖 + 缺少自动切换，导致“可查不可下”；同时入口成功语义门禁不足。

#### final fix
- 在 `config.py` 新增候选节点池与 `get_api_base_candidates()`。
- 在 `download.py` 增加章节请求容错链路：
  - 节点内重试（指数等待）；
  - 节点间自动切换（当前节点失败后尝试候选节点）；
  - 若存在失败章节，强制抛错并返回非零退出码，不再输出假成功。
- 回归结果：同书下载成功，自动切换到 `http://101.35.133.34:5000` 后完成正文写盘。

#### prevention checklist
- [x] 下载链路必须具备“节点内重试 + 节点间切换”双层容错。
- [x] 任意章节失败必须转为任务失败态（非零退出码）。
- [x] 文档中明确“自动节点切换”行为，减少手工排障成本。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/config.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7488719811606757913/chapters/太子总让我咒人.txt`

#### user feedback/constraint
- 用户要求先验证“当前技能包能否直接下载”，可行则继续沿用，不可行再换方案。

### [FQ-20260220-006] 2026-02-20 APP-only 选书场景缺少搜索入口且易混淆 post_id/book_id

#### symptom
- 用户目标是“下载仅 APP 可搜索到的番茄内容”，但当前技能主路径只能输入 `book_id`。
- 在短篇分享场景，用户常把 `post_id` 当成 `book_id` 传给 `catalog.py`，出现“0 章 / BOOK_REMOVE”或误判不可下载。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`: 缺少“先搜索拿 `book_id`”的标准入口。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/`: 无关键词搜索脚本，导致用户只能手动找 ID。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`: 未明确 `post_id != book_id(content_id)`。
- 根因判定：输入契约设计不完整（只有目录下载路径，没有检索路径），放大了 ID 语义误用。

#### final fix
- 新增 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/search.py`：
  - 调用 `/api/search?key=` 获取候选书目；
  - 输出 `book_id/书名/作者/字数`，支持 `-j/-r/-l`。
- 扩展 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/config.py`：
  - 新增 `get_search_api_url()`。
- 更新 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md` 与 `references/README.md`：
  - 把“先搜索再下载”纳入标准流程；
  - 明确短篇分享 `post_id` 与目录下载 `book_id(content_id)` 的区别。

#### prevention checklist
- [x] 对“未知 book_id”的场景，先走关键词搜索再下载。
- [x] 在技能文档中固定标注 `post_id` 与 `book_id` 的语义边界。
- [x] 搜索脚本统一返回可直接喂给 `catalog.py/download.py` 的 `book_id`。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/search.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/config.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7488719844586738457/share_metadata.json`

#### user feedback/constraint
- 用户希望先找“更直接方案”，重点是覆盖 APP-only 可见内容，不想被 `book_id` 手工定位卡住。

### [FQ-20260220-005] 2026-02-20 仅 post_id 的短篇链接可通过缓存回退恢复

#### symptom
- 用户只提供 `post_id=7488719844586738457` 时，简化 `short-story-share` 链接首次抓取返回“页面正文为空”。
- 使用同一 `post_id` 的完整分享链接（含 `share_token`）可成功抓取。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/short_story.py`: 抓取逻辑只尝试当前输入链接，未利用历史成功记录。
- 根因判定：短篇分享页通常依赖完整分享参数；仅 `post_id` 链接不稳定，导致正文渲染失败。

#### final fix
- 在 `short_story.py` 增加“源链接候选回退”：
  - 若当前链接失败，自动尝试 `input/番茄小说/<post_id>/share_metadata.json` 中的历史 `source_url`。
  - 当输入链接缺少 `share_token/report_params` 且抓取失败时，输出明确提示“需完整分享链接”。
- 验证结果：同 `post_id` 的简化链接在存在历史缓存时可恢复抓取成功。

#### prevention checklist
- [x] 为短篇抓取建立“输入链接 → 缓存链接”回退链。
- [x] 对“参数不完整”场景提供明确报错文案。
- [x] 文档注明完整链接优先策略与缓存回退机制。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/short_story.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7488719844586738457/share_metadata.json`

#### user feedback/constraint
- 用户仅给出 ID，希望直接可执行，不希望额外来回补参数。

### [FQ-20260220-004] 2026-02-20 仅给 ID 时命中 BOOK_REMOVE 且短篇回退抛 traceback

#### symptom
- 用户输入 `1852462278844425` 后，目录接口返回 0 章，无法下载。
- 尝试短篇回退链接 `short-story-share?post_id=1852462278844425` 时，`short_story.py` 直接抛 traceback。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`: 空目录场景仅提示 0 章，缺少 `BOOK_REMOVE` 结论输出。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/short_story.py`: CLI 入口未捕获运行时异常，导致 traceback 直接暴露。
- 根因判定：
  - 上游内容状态为 `BOOK_REMOVE`（`/api/detail` 返回 `code=101109`），属于内容侧不可用；
  - 脚本侧还存在异常收敛不足，放大了失败噪声。

#### final fix
- `short_story.py`：在 `main()` 统一捕获 `ValueError/RuntimeError`，输出可读错误并以非零退出码结束。
- `config.py` + `catalog.py`：
  - 增加 `get_detail_api_url()`；
  - 在空目录门禁中尝试 detail 诊断，并在命中 `BOOK_REMOVE` 时输出明确结论。

#### prevention checklist
- [x] 对短篇抓取失败统一返回可读错误，禁止默认 traceback。
- [x] 对 0 章目录增加 detail 侧状态识别（`BOOK_REMOVE`）。
- [x] 用户仅提供 ID 时，先做“可用性诊断”再进入下载步骤。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/short_story.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/config.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/CONTEXT.md`

#### user feedback/constraint
- 用户以“技能名 + 单个 ID”触发执行，期望直接下载；若失败，需要明确可操作的失败原因。

### [FQ-20260220-003] 2026-02-20 短篇分享链接无法被目录接口消费

#### symptom
- 用户提供 `short-story-share` 链接后，`catalog.py` / `download.py` 的 `book_id` 路径无法下载。
- `post_id=7488719844586738457` 在目录接口返回 0 章，分享页却可见正文。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`: 仅支持目录型 `book_id`，不支持 `short-story-share`。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`: 依赖目录 metadata，无法处理短篇分享页面。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/app.py`: UI 缺少短篇分享入口。
- 根因判定：数据模型不匹配。短篇分享是 H5 内容页，不是可枚举章节目录。

#### final fix
- 新增 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/short_story.py`：
  - 解析分享链接 `post_id`；
  - 调用 Playwright CLI 渲染页面并提取可见正文；
  - 自动裁切评论/拉起 App 区域并落盘。
- 扩展 `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/app.py`：
  - 新增“短篇分享”标签页，支持一键提取与预览。
- 更新 `SKILL.md` 与 `references/README.md`，补齐短篇分享流程、输出协议与依赖说明。

#### prevention checklist
- [x] 当输入为 `short-story-share` 链接时，避免走目录接口路径。
- [x] 通过独立脚本隔离“目录小说”和“短篇分享”两套输入契约。
- [x] 在 UI 层提供显式入口，避免用户误用 `book_id` 下载流程。
- [x] 把该模式差异沉淀进 CONTEXT，作为后续诊断先验。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/short_story.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/app.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/references/README.md`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7488719844586738457/短篇分享-7488719844586738457.txt`
- `/Volumes/AIGC/AIGC-ZEN-VOID/input/番茄小说/7488719844586738457/share_metadata.json`

#### user feedback/constraint
- 用户明确要求“可以加入拓展”，目标是把短篇分享链接纳入技能可执行范围并直接落盘。

### [FQ-20260220-002] 2026-02-20 接口断连导致 traceback 可读性差

#### symptom
- 回归验证时 API 出现短时断连（`RemoteDisconnected`），CLI 直接打印长 traceback，不利于用户快速定位问题。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`: `requests.get` 异常未收敛到可读错误。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`: 章节请求异常缺少统一错误包装。
- 根因判定：网络异常处理缺少“入口级错误收敛”，导致失败信息噪声过大。

#### final fix
- `catalog.py`：
  - 在目录请求增加 `timeout=20`。
  - 将 `requests.RequestException` 统一包装为 `RuntimeError`。
  - 在 CLI `main()` 输出简洁错误与排查建议，返回非零退出码。
- `download.py`：
  - 在章节请求增加 `timeout=20`。
  - 将请求异常包装为 `RuntimeError`，CLI 入口统一错误收敛并退出。

#### prevention checklist
- [x] 网络请求必须设置超时，避免无限阻塞。
- [x] CLI 入口统一收敛异常文案，禁止把完整 traceback 当作默认用户输出。
- [x] 将短时网络问题纳入 CONTEXT 经验，提示“先重试再定位配置”。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/CONTEXT.md`

#### user feedback/constraint
- 用户场景为“给定 `book_id` 直接执行”，要求快速得到可执行结果或清晰失败原因。

### [FQ-20260220-001] 2026-02-20 目录为空被误判为“下载完成”

#### symptom
- 用户提供 `book_id=7488719844586738457` 后，`catalog.py` 返回 `共 0 章`，`download.py` 继续输出“下载完成!”。
- 该行为会把“接口返回空目录”误导为“任务执行成功”。

#### root cause
- root cause location:
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`: `main()` 未对 `chapters == []` 建立失败门禁。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`: `download_book()` 在空目录场景仍走完成路径。
  - `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/app.py`: UI 对空目录仅展示空表，无显式停止下载提示。
- 根因判定：脚本入口缺少“空目录=异常态”约束，导致错误语义（success-like 输出 + 0 退出码）。

#### final fix
- 在 `catalog.py` 增加空目录门禁：输出 API 诊断信息到 stderr，并 `SystemExit(2)`。
- 在 `download.py` 增加空目录硬失败：抛出 `ValueError` 并在 CLI 入口转为退出码 `2`。
- 在 `app.py` 增加空目录提示与下载中止：明确提示“目录为空，已停止下载”。
- 同步在 `SKILL.md` 增补 Root-Cause 执行契约，固定后续修复顺序与闭环输出格式。

#### prevention checklist
- [x] CLI 入口对“0章”统一设为失败态（非零退出码）。
- [x] UI 层对“0章”给出显式诊断文案，不再显示成功语义。
- [x] 将本次案例落盘到 `CONTEXT.md`，确保后续复盘可检索。
- [x] 在 `SKILL.md` 写入 Root-Cause 契约，要求先修脚本门禁再修局部任务。

#### evidence paths
- `/Volumes/AIGC/AIGC-ZEN-VOID/book/7488719844586738457/metadata.json`（`data.lists` 为空）。
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/catalog.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/download.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/scripts/app.py`
- `/Volumes/AIGC/AIGC-ZEN-VOID/.agents/skills/fanqie-download/SKILL.md`

#### user feedback/constraint
- 用户输入仅为 `book_id`，约束是“直接跑一遍”，期望得到可执行结果或明确失败原因，不接受模糊成功提示。
