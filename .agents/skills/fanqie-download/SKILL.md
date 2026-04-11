---
name: fanqie-download
governance_tier: full
description: "番茄小说下载技能：按关键词检索 book_id、拉取目录与章节正文、抓取 short-story-share 可见文本，并提供 Gradio 界面与源层故障诊断。"
license: Proprietary. Internal use only.
---

# fanqie-download

## 角色与目标

本技能是一个面向番茄内容抓取的确定性工具链。目标不是只“跑通一次”，而是围绕同一套字段化产物稳定完成以下动作：

- 按关键词拿到可下载 `book_id`
- 获取目录并持久化为 `metadata.json`
- 批量下载章节正文并在必要时拆分内嵌章节
- 抓取 `short-story-share` 页面可见正文并保存元数据
- 在 CLI 与 Gradio 两种入口下都给出可读、可诊断、可复跑的状态输出

## 何时触发

- 需要从番茄小说获取目录或章节正文
- 需要批量下载并持久化为本地文本
- 用户提供短篇分享链接（`changdunovel.com/ug/pages/short-story-share`）需要落盘
- 需要可视化界面管理下载与预览

## 资源与入口

- `scripts/catalog.py`：目录获取与解析
- `scripts/search.py`：关键词搜索（返回可下载 `book_id`）
- `scripts/download.py`：章节批量下载
- `scripts/short_story.py`：短篇分享可见正文抓取
- `scripts/app.py`：Gradio 界面
- `scripts/config.py`：API Base 配置
- `scripts/requirements.txt`：运行依赖
- `references/README.md`：详细用法与示例

## 输入与路由

- 输入类型 1：`关键词`
  - 先走 `scripts/search.py`，拿到 `book_id` 后再进入目录/下载链路。
- 输入类型 2：`book_id` 或详情页 URL
  - 直接走 `scripts/catalog.py` 与 `scripts/download.py`。
- 输入类型 3：`short-story-share` 链接
  - 走 `scripts/short_story.py`，必要时复用该 `post_id` 的本地缓存 `source_url`。
- 输入类型 4：需要可视化查看与继续下载
  - 走 `scripts/app.py`。

## 标准流程（Mandatory）

### S1. 输入判定与路径选择

- 识别输入属于 `关键词 / book_id / 详情页 URL / short-story-share 链接 / UI 管理需求` 哪一类。
- 若用户仅给书名或模糊描述，不得直接猜 `book_id`，必须先走搜索。
- 若输入为短篇分享链接，先区分 `post_id` 与用于目录/下载的 `content_id(book_id)`，禁止混用。

### S2. 环境与 API 基线校验

- 安装依赖：

```bash
python3 -m pip install -r .agents/skills/fanqie-download/scripts/requirements.txt
```

- 如需切换 API Base，可编辑 `scripts/config.py`、在脚本内调用 `set_api_base(...)`，或在 Gradio 的“API 设置”中更新。
- 出现请求失败时，优先依赖 `search.py` / `catalog.py` / `download.py` 的候选节点回退，不先做局部文本补丁。

### S3. 搜索 `book_id`（条件步骤）

- 当输入不是明确 `book_id` 时，先执行：

```bash
python3 .agents/skills/fanqie-download/scripts/search.py "<关键词>"
python3 .agents/skills/fanqie-download/scripts/search.py "<关键词>" -j
```

- 输出的 `book_id` 必须可直接喂给 `catalog.py` / `download.py`。
- 若无结果，必须输出 API 诊断信息，而不是静默返回空列表。
- 当第三方 `api/search` 不可用时，必须自动回退到番茄官网搜索接口，而不是要求用户手工改 `book_id`。

### S4. 获取目录并保存 `metadata.json`

- 执行：

```bash
python3 .agents/skills/fanqie-download/scripts/catalog.py <book_id>
python3 .agents/skills/fanqie-download/scripts/catalog.py <book_id> -j
python3 .agents/skills/fanqie-download/scripts/catalog.py <book_id> -r
python3 .agents/skills/fanqie-download/scripts/catalog.py <book_id> -n
```

- 目录为空时必须视为失败态并给出诊断。
- 当目录返回 0 章时，优先调用 `detail` 诊断是否为 `BOOK_REMOVE`。
- 当第三方目录接口不可用但番茄官网书页可访问时，必须自动回退到官网书页解析目录并继续流程。

### S5. 下载章节正文

- 执行：

```bash
python3 .agents/skills/fanqie-download/scripts/download.py <book_id>
python3 .agents/skills/fanqie-download/scripts/download.py <book_id> -d 1
python3 .agents/skills/fanqie-download/scripts/download.py <book_id> -f
python3 .agents/skills/fanqie-download/scripts/download.py <book_id> -d 0 -w 8
python3 .agents/skills/fanqie-download/scripts/download.py <book_id> --split-embedded
```

- 默认按目录章节落盘。
- 若正文是“单文件内嵌多章”，可通过 `--split-embedded` 额外生成 `chapters/_split/*.txt`。
- 长篇下载优先采用并发模式；若首轮仍有失败章节，必须执行补缺重跑直至一致性校验通过。
- 当第三方正文接口不可用时，必须自动回退到番茄官网 `reader` 页 / 官方 reader 接口，并对私有区字体正文做字符表解码。

### S6. 抓取短篇分享可见正文

- 执行：

```bash
python3 .agents/skills/fanqie-download/scripts/short_story.py "<short-story-share链接>"
```

- 当前抓取依赖 `playwright-cli`。
- 若链接不完整，优先要求完整链接；仅给 `post_id` 时可尝试复用本地缓存 `source_url`。

### S7. Gradio 可视化入口

- 执行：

```bash
python3 .agents/skills/fanqie-download/scripts/app.py
```

- UI 当前支持：
  - 下载小说：获取目录、下载、章节筛选、预览
  - 短篇分享：提取正文并落盘
  - 已下载小说：刷新列表、继续下载、预览已下载章节
  - API 设置：动态更新 API Base

### S8. 结果校验与闭环

- 目录链路：校验 `metadata.json` 存在且 `data.lists` 为可解析列表。
- 下载链路：校验本地章节数、缺失数、失败章节数；若有失败章节必须转失败态。
- 短篇分享链路：校验 `短篇分享-<post_id>.txt` 与 `share_metadata.json` 同时存在。
- 发生失败、返工、用户纠错后，必须把可复用经验沉淀到同目录 `CONTEXT.md` 的 `Type Map / Repair Playbook / Reusable Heuristics`，里程碑级事件再追加 `Case Log`。

## 输出约定

- 搜索结果：
  - 终端表格或 JSON 列表，至少含 `book_id / title / author / word_number`
- 目录输出：
  - `input/番茄小说/<book_id>/metadata.json`
- 正文章节输出：
  - `input/番茄小说/<book_id>/chapters/*.txt`
- 内嵌章节拆分输出：
  - `input/番茄小说/<book_id>/chapters/_split/*.txt`
- 短篇分享输出：
  - `input/番茄小说/<post_id>/短篇分享-<post_id>.txt`
  - `input/番茄小说/<post_id>/share_metadata.json`
- UI 输出：
  - Gradio 页面中的状态文本、目录表、章节预览与已下载进度

## 统一字段主表（Mandatory）

| field_id | 输出位置/字段 | 内容要求 | 证据来源 | 默认责任Step | 质量维度 | 失败码 |
| --- | --- | --- | --- | --- | --- | --- |
| FIELD-FQ-ROUTE-01 | 路由判定 | 明确当前走 `search/catalog/download/short_story/app` 哪条主路径，并说明为何这样路由 | 用户输入、URL 结构、ID 形态 | S1 | 路由正确性 | FAIL-FQ-ROUTE-01 |
| FIELD-FQ-STR-01 | 搜索结果 | 返回可直接用于下载的 `book_id` 候选，字段至少含 `book_id/title/author/word_number` | `search.py` API 响应 | S3 | 检索可用性 | FAIL-FQ-STR-01 |
| FIELD-FQ-STR-02 | `metadata.json` | 目录 JSON 成功落盘，`data.lists` 可解析为章节列表；0章必须显式诊断 | `catalog.py` 响应与本地文件 | S4 | 目录完整性 | FAIL-FQ-STR-02 |
| FIELD-FQ-MAT-01 | `chapters/*.txt` | 每章成功写盘，正文经过实体解码；有失败章节时必须转失败态 | `download.py` 请求结果与本地章节文件 | S5 | 正文完整性 | FAIL-FQ-MAT-01 |
| FIELD-FQ-MAT-02 | `chapters/_split/*.txt` | 仅在检测到内嵌多章且启用 `--split-embedded` 时生成；数量与识别章节数一致 | `download.py` 内嵌章节检测结果 | S5 | 可见性增强 | FAIL-FQ-MAT-02 |
| FIELD-FQ-MAT-03 | `短篇分享-<post_id>.txt` + `share_metadata.json` | 可见正文与元数据同时落盘，记录 `post_id/title/source_url/chars/extract_method` | `short_story.py` 抓取结果与本地文件 | S6 | 短篇抓取完整性 | FAIL-FQ-MAT-03 |
| FIELD-FQ-DSP-01 | Gradio 界面状态 | UI 中目录、下载状态、章节预览、短篇分享状态与已下载列表可正常展示 | `app.py` 运行状态与页面组件输出 | S7 | 交互可用性 | FAIL-FQ-DSP-01 |
| FIELD-FQ-CTX-01 | 诊断与退出语义 | 网络失败、空目录、ID 混用、分享失效等情况必须给出可读诊断和正确退出码/停止语义 | CLI stderr、异常消息、UI 状态文本 | S4-S8 | 诊断清晰度 | FAIL-FQ-CTX-01 |

## 思维导引表（Mandatory）

| step_id | 聚焦字段(field_id) | 核心问题 | 生成动作 | 未达标信号 |
| --- | --- | --- | --- | --- |
| S1 | FIELD-FQ-ROUTE-01 | 当前输入究竟是关键词、`book_id`、详情页 URL，还是 `short-story-share` 链接？ | 解析用户输入、URL query、数字 ID 与任务目标，选定单一路由 | 把 `post_id` 当 `book_id`；用户给书名却直接猜 ID |
| S2 | FIELD-FQ-ROUTE-01, FIELD-FQ-CTX-01 | 当前 API Base 与依赖环境是否足以支撑本次执行？ | 安装依赖、确认 `requirements.txt`、必要时切换 API Base | 请求前置条件不满足却直接开跑 |
| S3 | FIELD-FQ-STR-01, FIELD-FQ-CTX-01 | 关键词能否稳定返回可下载 `book_id`？ | 调用 `search.py`，必要时使用 `-j/-r/-l` 与候选节点回退 | 搜索结果为空却无诊断；结果字段缺失 |
| S4 | FIELD-FQ-STR-02, FIELD-FQ-CTX-01 | 目录是否真实可用，还是 0章 / `BOOK_REMOVE` / 节点异常？ | 调用 `catalog.py`，保存 `metadata.json`，空目录时补跑 detail 诊断 | `metadata.json` 不存在；0章仍被视为成功 |
| S5 | FIELD-FQ-MAT-01, FIELD-FQ-MAT-02, FIELD-FQ-CTX-01 | 正文是否全部写盘，是否存在实体乱码、失败章节或内嵌章节误判？ | 调用 `download.py`，必要时并发下载、强制重下、拆分内嵌章节 | 失败章节仍显示成功；文本残留实体；长篇下载无收敛 |
| S6 | FIELD-FQ-MAT-03, FIELD-FQ-CTX-01 | 分享页链接是否完整，正文是否真正可见并已落盘？ | 调用 `short_story.py`，必要时复用缓存 `source_url` | 仅拿到空页面；只保存正文不保存元数据 |
| S7 | FIELD-FQ-DSP-01, FIELD-FQ-CTX-01 | UI 是否覆盖目录、下载、短篇分享和已下载管理这四类状态？ | 启动 `app.py`，验证标签页、状态文本、预览与继续下载 | UI 文案与 CLI 语义不一致；空目录仍允许继续下载 |
| S8 | 全字段 | 本次执行是否达成“可用输出 + 可读诊断 + 可复跑路径”？ | 对照字段表做验收，并将失败/成功模式沉淀到 `CONTEXT.md` | 只修当次输出，不做经验沉淀；字段验收缺失 |

## 通过表（Mandatory）

| field_id | 质量维度 | 通过标准 | 失败码 | 返工入口 |
| --- | --- | --- | --- | --- |
| FIELD-FQ-ROUTE-01 | 路由正确性 | 输入类型与执行入口一一对应，且不混淆 `post_id/book_id` | FAIL-FQ-ROUTE-01 | 回到 S1 重做输入分类 |
| FIELD-FQ-STR-01 | 检索可用性 | 至少返回 1 个可用候选，或在无结果时输出 API 级诊断 | FAIL-FQ-STR-01 | 回到 S3 重试搜索与节点切换 |
| FIELD-FQ-STR-02 | 目录完整性 | `metadata.json` 成功落盘，章节列表可解析；0章时明确失败并诊断 | FAIL-FQ-STR-02 | 回到 S4 重查目录与 detail |
| FIELD-FQ-MAT-01 | 正文完整性 | 本地章节文件数与成功下载数一致，失败章节数为 0，正文无显著实体残留 | FAIL-FQ-MAT-01 | 回到 S5 重跑下载/补缺 |
| FIELD-FQ-MAT-02 | 可见性增强 | 启用 `--split-embedded` 时，`_split` 文件数与识别到的内嵌章节数一致 | FAIL-FQ-MAT-02 | 回到 S5 重做内嵌章节拆分 |
| FIELD-FQ-MAT-03 | 短篇抓取完整性 | `正文文本 + share_metadata` 同时存在，且 `chars > 0` | FAIL-FQ-MAT-03 | 回到 S6 重跑分享抓取 |
| FIELD-FQ-DSP-01 | 交互可用性 | UI 各标签页可用，目录/下载/预览/短篇分享状态文本与实际行为一致 | FAIL-FQ-DSP-01 | 回到 S7 修正 UI 状态语义 |
| FIELD-FQ-CTX-01 | 诊断清晰度 | 失败态具备可读报错、退出码或停止语义，且能指向下一步排查动作 | FAIL-FQ-CTX-01 | 回到 S2/S4/S5/S6/S7 修正诊断链路 |

## 注意事项

- 确认已获得内容下载与使用授权，避免侵权或超限请求
- API 结构变更时，优先检查 `references/README.md` 与 `scripts/config.py`
- 请求失败或返回空内容时，先校验 API Base 是否可用
- `search.py` / `catalog.py` / `download.py` 均内置候选 API 节点自动切换：当前节点不可用时会自动尝试备用节点
- 当候选 API 节点全部失效时，`search.py` 会回退到番茄官网搜索接口，`catalog.py` 会回退到番茄官网书页目录解析，`download.py` 会回退到番茄官网 `reader` 页 / 官方 reader 接口并进行正文解码
- `download.py` 会在写盘前执行多轮 HTML 实体解码（如 `&#34;`、`&#39;`、`&amp;#39;`），减少“乱码”残留
- `download.py` 默认按目录章节落盘；若正文是“单文件内嵌多章”，可启用 `--split-embedded` 在 `chapters/_split/` 产出独立章节文件
- `download.py` 支持 `-w/--workers` 并发下载（`workers>1` 时会忽略 `--delay` 节流参数）
- 短篇分享抓取依赖 `playwright-cli`（通过 `$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh` 或全局 `playwright-cli`）。
- 当目录返回 0 章时，优先通过 `detail` 诊断是否为 `BOOK_REMOVE`（内容已下架/删除）。
- 短篇分享建议使用完整链接（含 `share_token`）；若仅提供 `post_id`，脚本会尝试复用该 `post_id` 的本地缓存 `source_url`。
- `short-story-share` 的 `post_id` 不等于目录下载所需 `book_id`。当分享链接含 `report_params` 时，应取其中 `content_id` 作为 `book_id`（可用 `search.py` 复核）。

## CONTEXT 预加载契约

- 执行本技能前，必须读取同目录 `CONTEXT.md`。
- `CONTEXT.md` 只承载经验层：
  - `Type Map`：失败类型到修复策略的稳定映射
  - `Repair Playbook`：固定排障顺序
  - `Reusable Heuristics`：已验证的高价值执行经验
  - `Case Log`：里程碑级证据
- 冲突优先级：用户明确要求 > 本 `SKILL.md` > `CONTEXT.md`

## Root-Cause 执行契约（必执行）

- 当出现下载失败、目录为空（0章）、输出异常或用户纠错时，必须先做源层诊断，再做局部补丁。
- 源层诊断顺序固定为：`SKILL.md` → `scripts/config.py` → `scripts/catalog.py` / `scripts/download.py` / `scripts/short_story.py` / `scripts/app.py` → 运行输出证据。
- 立即修复优先级：
  1. 修复脚本/入口门禁（例如空目录显式报错、非零退出码、可读诊断）。
  2. 若仍需补救，再处理本次任务的局部内容。
- 必须将案例沉淀到同目录 `CONTEXT.md`：
  - 普通迭代优先更新 `Type Map / Repair Playbook / Reusable Heuristics`
  - 里程碑事件再追加 `Case Log`
  - 最少字段仍需包含：`symptom`、`root cause`、`final fix`、`prevention checklist`、`evidence paths`、`user feedback/constraint`
- 用户闭环汇报必须给出三项：`root cause location` + `immediate fix` + `systemic prevention fix`。
