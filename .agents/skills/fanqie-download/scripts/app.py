#!/usr/bin/env python3
"""番茄小说下载器 - Gradio 可视化界面"""

import json
import re
import time

import gradio as gr
import pandas as pd

from catalog import get_book_catalog, parse_catalog, save_catalog
from download import get_chapter_content, sanitize_filename
from short_story import download_short_story_from_url
from config import (
    DEFAULT_API_BASE,
    extract_book_title,
    get_api_base,
    get_chapters_dir,
    get_metadata_path,
    get_output_root,
    extract_book_id,
    set_api_base,
)


def parse_book_id(input_str: str) -> str:
    """从输入中提取 book_id，支持纯 ID 或 URL"""
    input_str = input_str.strip()
    # 尝试从 URL 中提取 ID
    match = re.search(r'/page/(\d+)', input_str)
    if match:
        return match.group(1)
    # 如果是纯数字，直接返回
    if input_str.isdigit():
        return input_str
    return input_str


def get_downloaded_books():
    """获取已下载的小说列表"""
    book_dir = get_output_root()
    if not book_dir.exists():
        return []

    books = []
    for d in book_dir.iterdir():
        if d.is_dir():
            metadata_path = d / "metadata.json"
            chapters_dir = d / "chapters"

            if metadata_path.exists():
                try:
                    data = json.loads(metadata_path.read_text(encoding="utf-8"))
                    book_name = extract_book_title(data) or d.name
                    book_id = extract_book_id(data) or d.name
                    total_chapters = len(data.get("data", {}).get("lists", []))
                    downloaded = len(list(chapters_dir.glob("*.txt"))) if chapters_dir.exists() else 0

                    books.append({
                        "book_id": book_id,
                        "name": book_name,
                        "total": total_chapters,
                        "downloaded": downloaded,
                        "status": "已完成" if downloaded >= total_chapters else f"{downloaded}/{total_chapters}"
                    })
                except Exception:
                    pass

    return books


def refresh_book_list():
    """刷新小说列表"""
    books = get_downloaded_books()
    if not books:
        return pd.DataFrame(columns=["书名", "ID", "进度", "状态"])

    df = pd.DataFrame([
        {"书名": b["name"], "ID": b["book_id"], "进度": f"{b['downloaded']}/{b['total']}", "状态": b["status"]}
        for b in books
    ])
    return df


def fetch_catalog(book_input):
    """获取小说目录"""
    if not book_input or not book_input.strip():
        return "请输入小说 ID 或详情地址", pd.DataFrame()

    book_id = parse_book_id(book_input)

    try:
        data = get_book_catalog(book_id)
        save_catalog(book_id, data)
        chapters = parse_catalog(data)
        book_name = extract_book_title(data) or book_id

        if not chapters:
            empty_df = pd.DataFrame(columns=["序号", "章节", "状态", "item_id"])
            info = (
                f"获取成功但目录为空（book_id={book_id}）。"
                "请检查 book_id 是否有效，或在「API 设置」中切换地址后重试。"
            )
            return info, empty_df

        df = build_chapter_dataframe(book_id, chapters)
        info = f"**{book_name}** - 共 {len(chapters)} 章"

        return info, df

    except Exception as e:
        return f"获取失败: {e}", pd.DataFrame()


def build_chapter_dataframe(book_id, chapters):
    """构建章节列表 DataFrame"""
    chapters_dir = get_chapters_dir(book_id)

    rows = []
    for ch in chapters:
        title = sanitize_filename(ch["title"])
        downloaded = (chapters_dir / f"{title}.txt").exists() if chapters_dir.exists() else False
        rows.append({
            "序号": ch["order"],
            "章节": ch["title"],
            "状态": "✓" if downloaded else "",
            "item_id": ch["item_id"]
        })

    return pd.DataFrame(rows)


def load_book_from_table(evt: gr.SelectData, book_table):
    """从表格选择加载书籍"""
    if book_table is None or len(book_table) == 0:
        return "", pd.DataFrame()

    row = evt.index[0]
    book_id = book_table.iloc[row]["ID"]

    metadata_path = get_metadata_path(book_id)
    if not metadata_path.exists():
        return book_id, pd.DataFrame()

    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    chapters = parse_catalog(data)
    df = build_chapter_dataframe(book_id, chapters)

    return book_id, df


def filter_chapters(df, keyword):
    """搜索过滤章节"""
    if df is None or len(df) == 0:
        return df
    if not keyword or not keyword.strip():
        return df
    return df[df["章节"].str.contains(keyword.strip(), case=False, na=False)]


def preview_chapter_from_table(evt: gr.SelectData, chapter_table, book_id):
    """从表格选择预览章节"""
    if chapter_table is None or len(chapter_table) == 0 or not book_id:
        return "请选择章节"

    row = evt.index[0]
    title = chapter_table.iloc[row]["章节"]
    safe_title = sanitize_filename(title)
    chapter_file = get_chapters_dir(book_id) / f"{safe_title}.txt"

    if chapter_file.exists():
        content = chapter_file.read_text(encoding="utf-8")
        preview = content[:5000]
        if len(content) > 5000:
            preview += "\n\n... (内容过长已截断)"
        return f"## {title}\n\n{preview}"
    else:
        return f"**{title}**\n\n此章节尚未下载"


def jump_to_chapter(df, chapter_num):
    """跳转到指定章节"""
    if df is None or len(df) == 0:
        return df
    try:
        num = int(chapter_num)
        idx = df[df["序号"].astype(int) == num].index
        if len(idx) > 0:
            # 将目标行移到第一行显示
            target_idx = idx[0]
            return pd.concat([df.iloc[target_idx:], df.iloc[:target_idx]])
    except (ValueError, TypeError):
        pass
    return df


def start_download(book_input, delay, force):
    """开始下载"""
    if not book_input or not book_input.strip():
        yield "请输入小说 ID 或详情地址", pd.DataFrame()
        return

    book_id = parse_book_id(book_input)

    try:
        # 确保有目录
        metadata_path = get_metadata_path(book_id)
        if not metadata_path.exists():
            yield "获取目录中...", pd.DataFrame()
            data = get_book_catalog(book_id)
            metadata_path = save_catalog(book_id, data)
        else:
            data = json.loads(metadata_path.read_text(encoding="utf-8"))

        chapters = parse_catalog(data)
        total = len(chapters)
        if total == 0:
            empty_df = pd.DataFrame(columns=["序号", "章节", "状态", "item_id"])
            yield (
                f"目录为空（book_id={book_id}），已停止下载。请检查 book_id 或 API 设置。",
                empty_df,
            )
            return

        chapters_dir = get_chapters_dir(
            book_id,
            book_title=extract_book_title(data),
            create=True,
            migrate_legacy=True,
        )
        chapters_dir.mkdir(parents=True, exist_ok=True)

        downloaded_count = 0
        skipped_count = 0
        last_df = build_chapter_dataframe(book_id, chapters)

        for i, ch in enumerate(chapters):
            item_id = ch["item_id"]
            title = sanitize_filename(ch["title"])
            chapter_file = chapters_dir / f"{title}.txt"

            if chapter_file.exists() and not force:
                skipped_count += 1
                status = f"[{i+1}/{total}] 跳过: {ch['title']}"
            else:
                try:
                    content = get_chapter_content(item_id)
                    chapter_file.write_text(content, encoding="utf-8")
                    downloaded_count += 1
                    status = f"[{i+1}/{total}] 完成: {ch['title']}"
                except Exception as e:
                    status = f"[{i+1}/{total}] 失败: {ch['title']} - {e}"

                if i < total - 1:
                    time.sleep(delay)

            # 每 20 章更新表格
            if (i + 1) % 20 == 0 or i == total - 1:
                last_df = build_chapter_dataframe(book_id, chapters)

            yield status, last_df

        final_msg = f"下载完成! 新下载 {downloaded_count} 章，跳过 {skipped_count} 章"
        df = build_chapter_dataframe(book_id, chapters)
        yield final_msg, df

    except Exception as e:
        yield f"下载失败: {e}", pd.DataFrame()


def download_short_story(share_input: str):
    """下载短篇分享可见正文"""
    if not share_input or not share_input.strip():
        return "请输入短篇分享链接", "", "等待输入分享链接。"

    try:
        result = download_short_story_from_url(share_input)
        content = result["content"]
        preview = content[:5000]
        if len(content) > 5000:
            preview += "\n\n... (内容过长已截断)"

        status = (
            f"提取成功: post_id={result['post_id']}，"
            f"共 {result['chars']} 字。"
        )
        preview_md = f"## {result['title']}\n\n{preview}"
        return status, result["text_path"], preview_md
    except Exception as e:
        return f"提取失败: {e}", "", "请检查链接有效性，或稍后重试。"


def create_ui():
    """创建 Gradio 界面"""
    with gr.Blocks(title="番茄小说下载器", theme=gr.themes.Soft()) as app:
        gr.Markdown("# 番茄小说下载器")

        # API 设置区域
        with gr.Accordion("API 设置", open=False):
            with gr.Row():
                api_base_input = gr.Textbox(
                    label="API 地址",
                    value=DEFAULT_API_BASE,
                    placeholder="例如: fq.shusan.cn",
                    scale=3
                )
                api_save_btn = gr.Button("保存", variant="secondary", scale=1)
            api_status = gr.Markdown(f"当前 API: `{DEFAULT_API_BASE}`")

            def save_api_base(base):
                if not base or not base.strip():
                    return f"❌ API 地址不能为空，当前: `{get_api_base()}`"
                set_api_base(base)
                return f"✓ API 已更新为: `{get_api_base()}`"

            api_save_btn.click(fn=save_api_base, inputs=[api_base_input], outputs=[api_status])

        # 存储当前 book_id
        current_book_id = gr.State("")

        with gr.Tabs():
            # ===== 下载标签页 =====
            with gr.TabItem("下载小说"):
                with gr.Row():
                    book_id_input = gr.Textbox(
                        label="小说 ID 或详情地址",
                        placeholder="输入 ID 如 7399487167648500798 或地址 https://fanqienovel.com/page/xxx",
                        scale=3
                    )
                    fetch_btn = gr.Button("获取目录", variant="secondary", scale=1)
                    download_btn = gr.Button("开始下载", variant="primary", scale=1)

                with gr.Row():
                    delay_input = gr.Slider(
                        minimum=0.1, maximum=5.0, value=0.5, step=0.1,
                        label="请求间隔(秒)", scale=2
                    )
                    force_check = gr.Checkbox(label="强制重新下载", value=False, scale=1)

                book_info = gr.Markdown("输入小说 ID 后点击「获取目录」")
                status_text = gr.Textbox(label="下载状态", lines=1, interactive=False)

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 章节列表")
                        with gr.Row():
                            search_input = gr.Textbox(
                                label="搜索章节",
                                placeholder="输入关键词过滤",
                                scale=2
                            )
                            jump_input = gr.Number(label="跳转到第N章", scale=1)

                        chapter_table = gr.Dataframe(
                            headers=["序号", "章节", "状态"],
                            datatype=["number", "str", "str"],
                            col_count=(3, "fixed"),
                            max_height=400,
                            interactive=False
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### 章节预览")
                        chapter_preview = gr.Markdown(
                            "点击左侧章节查看内容",
                            elem_id="preview-area"
                        )

                # 事件绑定
                fetch_btn.click(
                    fn=fetch_catalog,
                    inputs=[book_id_input],
                    outputs=[book_info, chapter_table]
                )

                download_btn.click(
                    fn=start_download,
                    inputs=[book_id_input, delay_input, force_check],
                    outputs=[status_text, chapter_table]
                )

                search_input.change(
                    fn=filter_chapters,
                    inputs=[chapter_table, search_input],
                    outputs=[chapter_table]
                )

                jump_input.change(
                    fn=jump_to_chapter,
                    inputs=[chapter_table, jump_input],
                    outputs=[chapter_table]
                )

                chapter_table.select(
                    fn=preview_chapter_from_table,
                    inputs=[chapter_table, book_id_input],
                    outputs=[chapter_preview]
                )

            # ===== 短篇分享标签页 =====
            with gr.TabItem("短篇分享"):
                gr.Markdown("输入 `short-story-share` 链接，提取当前页面可见正文并保存到本地。")
                share_input = gr.Textbox(
                    label="短篇分享链接",
                    placeholder="例如: https://changdunovel.com/ug/pages/short-story-share?...",
                )
                share_download_btn = gr.Button("提取并保存", variant="primary")
                share_status = gr.Textbox(label="处理状态", interactive=False)
                share_saved_path = gr.Textbox(label="保存路径", interactive=False)
                share_preview = gr.Markdown("提取完成后将在此预览正文。")

                share_download_btn.click(
                    fn=download_short_story,
                    inputs=[share_input],
                    outputs=[share_status, share_saved_path, share_preview],
                )

            # ===== 已下载小说标签页 =====
            with gr.TabItem("已下载小说"):
                refresh_btn = gr.Button("刷新列表", variant="secondary")

                gr.Markdown("### 小说列表")
                book_table = gr.Dataframe(
                    headers=["书名", "ID", "进度", "状态"],
                    datatype=["str", "str", "str", "str"],
                    col_count=(4, "fixed"),
                    max_height=200,
                    interactive=False,
                    value=refresh_book_list()
                )

                selected_book_id = gr.Textbox(label="当前选中", interactive=False)

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 章节列表")
                        saved_search = gr.Textbox(label="搜索章节", placeholder="输入关键词过滤")
                        saved_chapter_table = gr.Dataframe(
                            headers=["序号", "章节", "状态"],
                            datatype=["number", "str", "str"],
                            col_count=(3, "fixed"),
                            max_height=350,
                            interactive=False
                        )
                        continue_btn = gr.Button("继续下载此书", variant="primary")
                        continue_status = gr.Textbox(label="状态", interactive=False)

                    with gr.Column(scale=1):
                        gr.Markdown("### 章节预览")
                        saved_preview = gr.Markdown("选择章节查看内容")

                # 事件绑定
                refresh_btn.click(
                    fn=refresh_book_list,
                    outputs=[book_table]
                )

                book_table.select(
                    fn=load_book_from_table,
                    inputs=[book_table],
                    outputs=[selected_book_id, saved_chapter_table]
                )

                saved_search.change(
                    fn=filter_chapters,
                    inputs=[saved_chapter_table, saved_search],
                    outputs=[saved_chapter_table]
                )

                saved_chapter_table.select(
                    fn=preview_chapter_from_table,
                    inputs=[saved_chapter_table, selected_book_id],
                    outputs=[saved_preview]
                )

                continue_btn.click(
                    fn=start_download,
                    inputs=[selected_book_id, gr.Number(value=0.5, visible=False), gr.Checkbox(value=False, visible=False)],
                    outputs=[continue_status, saved_chapter_table]
                )

        gr.Markdown("---\n*提示: 在番茄小说 App 或网页版查看小说 URL 获取 book_id*")

    return app


if __name__ == "__main__":
    app = create_ui()
    app.launch(share=False)
