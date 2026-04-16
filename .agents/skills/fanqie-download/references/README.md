# 番茄小说下载器

一个番茄内容下载工具，支持获取小说目录、批量下载章节内容，以及抓取短篇分享页可见正文。

## 功能特性

- 获取小说完整目录信息
- 按关键词搜索并返回可下载 `book_id`
- 批量下载所有章节内容
- 支持断点续传（自动跳过已下载章节）
- 自动创建目录结构
- 可调节下载速度（请求间隔）
- 搜索/目录/正文接口均支持候选 API 节点自动切换
- 当第三方 API 节点整体失效时，会自动回退到番茄官网搜索接口、官网书页目录解析与官网 `reader` 正文解码
- 当目录来自官网书页回退时，正文仍会先做样章探测；若探测结论是“第三方正文全挂且官网正文被 challenge 拦截”，脚本会在整书开始前直接返回 blocker，而不会继续整书盲打
- 支持 `short-story-share` 链接正文抓取（可见文本）
- 小说下载目录默认按书名命名；旧的 `book_id` 目录会被兼容读取，并在可安全时迁移到书名目录
- 提供 `migrate_legacy_dirs.py`，可批量把历史 `input/番茄小说/<book_id>/` 收敛到 `input/番茄小说/<书名>/`

## 环境要求

- Python 3.10+
- requests 库
- 可用的 Playwright CLI（短篇分享抓取需要）

## 安装依赖

```bash
pip install requests
```

## 项目结构

```
fanqie-download/
├── search.py        # 关键词搜索模块
├── catalog.py       # 目录获取模块
├── download.py      # 章节下载模块
├── short_story.py   # 短篇分享下载模块
├── README.md        # 项目说明
└── input/番茄小说/   # 下载内容存储目录
    └── {书名}/
        ├── metadata.json    # 小说元数据（目录信息）
        └── chapters/        # 章节内容目录
            ├── 第1章 xxx.txt
            ├── 第2章 xxx.txt
            └── ...
```

## 使用方法

### 快速开始

只需要一条命令即可下载整本小说：

```bash
python download.py 7399487167648500798
```

程序会自动：
1. 检查是否已有目录信息，没有则自动获取
2. 下载所有章节，跳过已存在的章节

### 先搜索 book_id（推荐）

```bash
# 文本表格输出
python search.py "太子总让我咒人"

# JSON 输出
python search.py "太子总让我咒人" -j

# 控制显示条数
python search.py "太子总让我咒人" -l 10
```

**输出示例：**

```text
关键词: 太子总让我咒人
命中: 3 条

  1. 太子总让我咒人 | 作者: 青霆 | book_id: 7488719811606757913 | 字数: 0
```

### 获取小说目录

```bash
# 获取目录并保存到本地（默认行为）
python catalog.py 7399487167648500798

# 只显示目录，不保存
python catalog.py 7399487167648500798 -n

# 输出 JSON 格式（解析后的章节列表）
python catalog.py 7399487167648500798 -j

# 输出原始 API 响应
python catalog.py 7399487167648500798 -r
```

**输出示例：**

```
已保存到 input/番茄小说/书名/metadata.json
共 256 章

   1. 第1章 鸡鸭都收
   2. 第2章 男生女相
   3. 第3章 黑道大哥 [付费]
   ...
```

### 下载章节内容

```bash
# 下载所有章节（自动跳过已下载）
python download.py 7399487167648500798

# 自定义请求间隔（默认 0.5 秒）
python download.py 7399487167648500798 -d 1

# 强制重新下载所有章节
python download.py 7399487167648500798 -f

# 并发下载（长篇推荐）
python download.py 7399487167648500798 -d 0 -w 8

# 若正文是“单文件内嵌多章”，额外拆分独立章节文件
python download.py 7399487167648500798 --split-embedded
```

**输出示例：**

```
使用已有目录: input/番茄小说/书名/metadata.json
共 256 章需要下载

[1/256] 下载: 第1章 鸡鸭都收 ... 完成
[2/256] 下载: 第2章 男生女相 ... 完成
[3/256] 跳过: 第3章 黑道大哥
...

下载完成!
```

### 迁移历史 `book_id` 目录

```bash
# 迁移指定旧目录
python migrate_legacy_dirs.py 7399487167648500798

# 扫描并迁移全部数字目录
python migrate_legacy_dirs.py --all

# 先看计划，不落盘
python migrate_legacy_dirs.py --all --dry-run
```

**输出示例：**

```text
7399487167648500798: rename 完成 -> input/番茄小说/书名
```

### 下载短篇分享链接（可见正文）

```bash
python short_story.py "https://changdunovel.com/ug/pages/short-story-share?post_id=..."
```

**输出示例：**

```text
已保存短篇分享: 太子总让我咒人
post_id: 7488719844586738457
正文文件: input/番茄小说/7488719844586738457/短篇分享-7488719844586738457.txt
元数据文件: input/番茄小说/7488719844586738457/share_metadata.json
字符数: 3804
```

## 命令行参数

### catalog.py

| 参数 | 说明 |
|------|------|
| `book_id` | 小说 ID（必填） |
| `-j, --json` | 输出 JSON 格式的章节列表 |
| `-r, --raw` | 输出原始 API 响应 |
| `-n, --no-save` | 不保存到本地文件 |

### download.py

| 参数 | 说明 |
|------|------|
| `book_id` | 小说 ID（必填） |
| `-d, --delay` | 请求间隔秒数（默认 0.5） |
| `-w, --workers` | 并发下载线程数（默认 1；`>1` 时启用并发模式并忽略 `--delay`） |
| `-f, --force` | 强制重新下载已存在的章节 |
| `--split-embedded` | 检测正文中的内嵌章节标题并拆分到 `chapters/_split/` |

### 官网 challenge 说明

- 若 `catalog.py` 只能通过官网书页回退拿到目录，`download.py` 会先拿 1 个样章探测正文通道，而不是直接整书走官网正文。
- 若第三方正文接口全部失败，同时官网 `reader/full`、`reader` 页、浏览器会话 `fetch /api/reader/full` 仍被 challenge 拦截，脚本会在整书下载前直接报 blocker。
- 若本机已有通过验证的番茄浏览器会话，可通过环境变量注入后重跑：

```bash
export FANQIE_COOKIE_HEADER='novel_web_id=...; ...'
# 或仅轻量注入 novel_web_id
export FANQIE_NOVEL_WEB_ID='...'
python download.py <book_id>
```

### short_story.py

| 参数 | 说明 |
|------|------|
| `share_url` | 短篇分享链接（必填） |

### search.py

| 参数 | 说明 |
|------|------|
| `keyword` | 搜索关键词（必填） |
| `-j, --json` | 输出解析后的 JSON 结果 |
| `-r, --raw` | 输出原始 API 响应 |
| `-l, --limit` | 最多显示条数（默认 20） |

## 作为模块使用

### catalog.py 模块

```python
from catalog import get_book_catalog, parse_catalog, get_chapters, save_catalog

# 获取原始目录数据
data = get_book_catalog("7399487167648500798")

# 解析为章节列表
chapters = parse_catalog(data)
for ch in chapters:
    print(f"{ch['order']}. {ch['title']}")
    # ch['item_id']   - 章节 ID
    # ch['title']     - 章节标题
    # ch['order']     - 章节序号
    # ch['volume']    - 所属卷名
    # ch['need_pay']  - 是否付费

# 便捷函数：一步获取章节列表
chapters = get_chapters("7399487167648500798")

# 保存目录到本地
path = save_catalog("7399487167648500798", data)
print(f"保存到: {path}")  # input/番茄小说/书名/metadata.json
```

### download.py 模块

```python
from download import download_book, get_chapter_content

# 下载整本书
download_book("7399487167648500798")

# 自定义下载参数
download_book("7399487167648500798", delay=1.0, force=True)

# 并发下载
download_book("7399487167648500798", delay=0.0, workers=8)

# 检测并拆分正文内嵌章节
download_book("7399487167648500798", split_embedded=True)

# 获取单个章节内容
content = get_chapter_content("7399494428001321534")
print(content)
```

## API 说明

本工具通过 `scripts/config.py` 的 `DEFAULT_API_BASE` 配置 API Base，
默认使用 `http://47.108.80.161:5005`，可在脚本或 Gradio 中切换。

核心接口：

### 搜索书籍

```
GET {API_BASE}/api/search?key={keyword}
```

### 获取目录

```
GET {API_BASE}/api/directory?book_id={book_id}
```

**响应结构：**

```json
{
  "code": 200,
  "data": {
    "data": {
      "allItemIds": ["7399494428001321534", ...],
      "chapterListWithVolume": [
        [
          {
            "itemId": "7399494428001321534",
            "title": "第1章 鸡鸭都收",
            "realChapterOrder": "1",
            "volume_name": "第一卷：默认",
            "needPay": 0,
            "isChapterLock": false
          },
          ...
        ]
      ],
      "volumeNameList": ["第一卷：默认"]
    }
  }
}
```

### 获取章节内容

```
GET {API_BASE}/api/content?item_id={item_id}
```

**响应结构：**

```json
{
  "code": 200,
  "data": {
    "content": "章节正文内容..."
  }
}
```

## 数据存储格式

### metadata.json

保存完整的 API 响应，包含所有章节的元数据信息。

### 章节文件

- 文件名：`{章节标题}.txt`（如 `第1章 鸡鸭都收.txt`）
- 内容：纯文本章节正文
- 编码：UTF-8

### 短篇分享文件

- 正文文件：`短篇分享-{post_id}.txt`
- 元数据：`share_metadata.json`

## 注意事项

1. **请求频率**：默认每次请求间隔 0.5 秒，请勿设置过小以免对服务器造成压力
2. **付费章节**：部分章节可能需要付费，工具会标记但可能无法获取完整内容
3. **文件名处理**：章节标题中的特殊字符（`/\:*?"<>|`）会被替换为下划线
4. **断点续传**：程序会自动跳过已下载的章节，可放心中断后继续
5. **短篇分享限制**：短篇分享默认抓取页面可见正文，若平台限制可能出现截断
6. **Playwright 依赖**：`short_story.py` 需要可用的 Playwright CLI（建议使用 `$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh`）
7. **链接完整性**：短篇分享优先使用完整链接（含 `share_token`）；若只给 `post_id`，脚本会尝试复用同 `post_id` 的历史缓存 `source_url`
8. **ID 语义**：短篇分享链接中的 `post_id` 通常不是目录下载所需 `book_id`。若链接含 `report_params`，请优先取其中 `content_id` 作为 `book_id`
9. **节点故障切换**：`search.py` / `catalog.py` / `download.py` 均会在当前节点断连时自动尝试候选 API 节点
10. **实体乱码清洗**：`download.py` 落盘前会做多轮 HTML 实体解码（如 `&#34;`、`&#39;`、`&amp;#39;`）
11. **内嵌章节拆分**：若目录仅 1 条但正文里含 `第一章/第二章...`，可用 `--split-embedded` 额外输出独立章节文件到 `chapters/_split/`

## 如何获取 book_id

1. 在番茄小说 App 或网页版找到想下载的小说
2. 查看小说的分享链接或页面 URL
3. URL 中的数字即为 book_id，例如：`https://fanqienovel.com/page/7399487167648500798`

## License

MIT
