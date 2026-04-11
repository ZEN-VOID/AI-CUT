#!/usr/bin/env python3
"""批量下载番茄小说章节内容"""

import argparse
import concurrent.futures
import html
import json
import random
import re
import threading
import time
from pathlib import Path
from urllib.parse import quote

import requests

from config import (
    get_api_base,
    get_api_base_candidates,
    get_chapters_dir,
    get_content_api_url,
    get_metadata_path,
    get_referer,
    set_api_base,
)

_THREAD_LOCAL = threading.local()
CHARSET_PATH = Path(__file__).with_name("charset.json")
OFFICIAL_READER_URL = "https://fanqienovel.com/reader/{item_id}"
OFFICIAL_READER_API_URL = "https://fanqienovel.com/api/reader/full?itemId={item_id}"
CHARSET_CODE_RANGES = ((58344, 58715), (58345, 58716))
_CHARSET_CACHE: list[list[str]] | None = None


def get_http_session() -> requests.Session:
    """
    获取线程内复用 HTTP 会话，减少每章重复 TLS 握手带来的耗时。
    """
    session = getattr(_THREAD_LOCAL, "http_session", None)
    if session is None:
        session = requests.Session()
        session.headers.update({
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
            ),
        })
        _THREAD_LOCAL.http_session = session
    return session


def load_charset() -> list[list[str]]:
    """加载番茄官网私有区字体映射表。"""
    global _CHARSET_CACHE
    if _CHARSET_CACHE is None:
        _CHARSET_CACHE = json.loads(CHARSET_PATH.read_text(encoding="utf-8"))
    return _CHARSET_CACHE


def get_cached_official_cookie() -> str | None:
    """读取线程内缓存的番茄官网 reader cookie。"""
    return getattr(_THREAD_LOCAL, "novel_web_id", None)


def set_cached_official_cookie(cookie: str | None):
    """写入线程内缓存的番茄官网 reader cookie。"""
    _THREAD_LOCAL.novel_web_id = cookie


def normalize_chapter_text(text: str, max_unescape_rounds: int = 3) -> str:
    """
    规范化章节文本，修复常见实体乱码。

    - 多轮 HTML 实体解码：覆盖 `&#39;`、`&#34;` 及双重编码（如 `&amp;#39;`）。
    - 统一不可见空白：将 NBSP 转为普通空格，移除 BOM。
    """
    normalized = text
    for _ in range(max_unescape_rounds):
        decoded = html.unescape(normalized)
        if decoded == normalized:
            break
        normalized = decoded

    normalized = normalized.replace("\u00a0", " ").replace("\ufeff", "")
    return normalized


def decode_charset_text(text: str, mode: int) -> str:
    """按指定字符表模式解码番茄官网私有区字符。"""
    lo, hi = CHARSET_CODE_RANGES[mode]
    charset = load_charset()[mode]
    out: list[str] = []
    for ch in text:
        codepoint = ord(ch)
        if lo <= codepoint <= hi:
            idx = codepoint - lo
            if 0 <= idx < len(charset) and charset[idx] not in {"", "?"}:
                out.append(charset[idx])
            else:
                out.append(ch)
        else:
            out.append(ch)
    return "".join(out)


def score_decoded_text(text: str) -> tuple[int, int, int]:
    """为两套字符表结果打分，优先选择中文更多、私有区更少的结果。"""
    cjk = 0
    private_use = 0
    printable = 0
    for ch in text:
        codepoint = ord(ch)
        if "\u4e00" <= ch <= "\u9fff":
            cjk += 1
        if 0xE000 <= codepoint <= 0xF8FF:
            private_use += 1
        if ch.isprintable():
            printable += 1
    return (cjk, -private_use, printable)


def decode_official_content(text: str) -> str:
    """尝试两套字符表并选择更像正常中文正文的结果。"""
    candidates = [decode_charset_text(text, 0), decode_charset_text(text, 1)]
    best = max(candidates, key=score_decoded_text)
    return normalize_chapter_text(best)


def extract_reader_paragraphs(html_text: str) -> str:
    """从官网 reader 页提取正文段落，优先走稳定的 chapterData.content。"""
    start_token = '"content":"'
    end_token = '","uid"'
    anchor_idx = html_text.find("chapterData")
    search_from = anchor_idx if anchor_idx != -1 else 0
    start_idx = html_text.find(start_token, search_from)
    if start_idx != -1:
        start_idx += len(start_token)
        end_idx = html_text.find(end_token, start_idx)
    else:
        end_idx = -1

    if start_idx != -1 and end_idx != -1:
        raw_content = html_text[start_idx:end_idx]
        raw_content = (
            raw_content
            .replace("\\u003Cp\\u003E", "<p>")
            .replace("\\u003C\\u002Fp\\u003E", "</p>")
            .replace("\\u003C", "<")
            .replace("\\u003E", ">")
            .replace("\\u002F", "/")
            .replace("\\n", "\n")
            .replace("\\/", "/")
        )
        paragraphs = re.findall(r"<p>(.*?)</p>", raw_content, re.S)
        if paragraphs:
            return "\n".join(normalize_chapter_text(html.unescape(p)) for p in paragraphs)

    dom_match = re.search(
        r'<div class="muye-reader-content noselect">(?P<body>.*?)</div>',
        html_text,
        re.S,
    )
    if not dom_match:
        return ""

    paragraphs = re.findall(r"<p>(.*?)</p>", dom_match.group("body"), re.S)
    if not paragraphs:
        return ""

    return "\n".join(normalize_chapter_text(html.unescape(p)) for p in paragraphs)


def get_chapter_content_official(item_id: str, session: requests.Session | None = None) -> str:
    """从番茄官网 reader 页/API 兜底获取并解码章节正文。"""
    session = session or get_http_session()
    headers = {
        "referer": "https://fanqienovel.com/",
        "origin": "https://fanqienovel.com",
    }
    errors: list[str] = []

    try:
        response = session.get(
            OFFICIAL_READER_API_URL.format(item_id=quote(str(item_id))),
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        content = data.get("data", {}).get("chapterData", {}).get("content")
        if isinstance(content, str) and content.strip():
            return decode_official_content(html.unescape(re.sub(r"</p>\s*<p>", "\n", re.sub(r"<[^>]+>", "", content))))
        errors.append("official_api: 空正文")
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        errors.append(f"official_api: {e}")

    page_url = OFFICIAL_READER_URL.format(item_id=quote(str(item_id)))
    page_errors: list[str] = []
    for attempt in range(30):
        cookie = get_cached_official_cookie()
        if not cookie or attempt > 0:
            cookie = str(random.randint(6 * 10**18, 9 * 10**18))
            set_cached_official_cookie(cookie)
        try:
            response = session.get(
                page_url,
                headers=headers,
                cookies={"novel_web_id": cookie},
                timeout=20,
            )
            response.raise_for_status()
            html_text = response.text
            if "验证码中间页" in html_text or "middle_page_loading" in html_text:
                page_errors.append(f"cookie={cookie}: captcha")
                set_cached_official_cookie(None)
                continue

            extracted = extract_reader_paragraphs(html_text)
            if extracted.strip():
                return decode_official_content(extracted)

            page_errors.append(f"cookie={cookie}: 未解析到正文段落")
            set_cached_official_cookie(None)
        except requests.RequestException as e:
            page_errors.append(f"cookie={cookie}: {e}")
            set_cached_official_cookie(None)

    if page_errors:
        errors.append("official_page: " + " | ".join(page_errors))

    raise RuntimeError(
        f"官网正文兜底失败(item_id={item_id})，" + " | ".join(errors)
    )


def split_embedded_chapters(text: str) -> list[dict]:
    """
    从单文件正文中识别并拆分内嵌章节。

    返回:
        [
          {"title": "第一章", "content": "第一章..."},
          ...
        ]
    """
    pattern = re.compile(r"(?m)^(第[一二三四五六七八九十百千零〇0-9]+章[^\n]*)\s*$")
    matches = list(pattern.finditer(text))
    if len(matches) < 2:
        return []

    sections: list[dict] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        title = match.group(1).strip() or f"第{idx + 1}章"
        content = text[start:end].strip()
        if not content:
            continue
        sections.append({"title": title, "content": f"{content}\n"})

    return sections


def get_chapter_content(item_id: str, max_retries: int = 3, retry_delay: float = 1.0) -> str:
    """
    获取单个章节内容

    Args:
        item_id: 章节ID
        max_retries: 最大重试次数
        retry_delay: 重试基准等待（秒）

    Returns:
        章节正文内容
    """
    params = {"tab": "小说", "item_id": item_id}
    original_base = get_api_base()
    base_errors: list[str] = []
    session = get_http_session()

    for base in get_api_base_candidates():
        set_api_base(base)
        url = get_content_api_url()
        last_error: Exception | None = None

        for attempt in range(1, max_retries + 1):
            try:
                response = session.get(
                    url,
                    params=params,
                    headers={"referer": get_referer()},
                    timeout=20,
                )
                response.raise_for_status()
                data = response.json()

                content = data.get("data", {}).get("content")
                if not isinstance(content, str) or not content.strip():
                    api_code = data.get("code")
                    api_message = data.get("message", "")
                    raise RuntimeError(
                        "章节内容为空或结构异常"
                        f"(item_id={item_id}, code={api_code}, message={api_message!r})"
                    )
                # 番茄接口正文偶发返回 HTML 实体（如 &#34; / &#39;），下载时统一还原。
                content = normalize_chapter_text(content)

                if base != original_base:
                    print(f"切换API成功: {original_base} -> {base}", end=" ... ", flush=True)
                return content
            except (requests.RequestException, json.JSONDecodeError, RuntimeError) as e:
                last_error = e
                if attempt < max_retries:
                    wait_s = retry_delay * attempt
                    print(f"重试({attempt}/{max_retries - 1})", end=f" 等待 {wait_s:.1f}s ... ", flush=True)
                    time.sleep(wait_s)
                    continue
                break

        base_errors.append(f"{base}: {last_error}")

    set_api_base(original_base)
    set_api_base(original_base)
    try:
        content = get_chapter_content_official(item_id, session=session)
        print("提示: 第三方正文接口不可用，已回退到番茄官网 reader 页/接口。", flush=True)
        return content
    except RuntimeError as e:
        raise RuntimeError(
            f"章节请求失败(item_id={item_id})，候选节点均不可用: {' | '.join(base_errors)} | {e}"
        ) from e


def load_metadata(book_id: str) -> dict:
    """从本地加载 metadata.json"""
    metadata_path = get_metadata_path(book_id)
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def ensure_metadata(book_id: str) -> dict:
    """确保 metadata 存在，不存在则自动获取"""
    from catalog import get_book_catalog, save_catalog

    metadata_path = get_metadata_path(book_id)

    if metadata_path.exists():
        print(f"使用已有目录: {metadata_path}")
        return load_metadata(book_id)

    print(f"获取目录中...")
    data = get_book_catalog(book_id)
    save_catalog(book_id, data)
    print(f"目录已保存到: {metadata_path}")
    return data


def get_all_item_ids(metadata: dict) -> list[dict]:
    """
    从 metadata 提取所有章节信息

    Returns:
        章节列表，包含 item_id, title, order
    """
    chapters = []
    chapter_list = metadata.get("data", {}).get("lists")
    if not isinstance(chapter_list, list):
        return chapters

    for i, chapter in enumerate(chapter_list, 1):
        item_id = str(chapter.get("item_id", "")).strip()
        if not item_id:
            continue

        title = str(chapter.get("title", f"第{i}章")).strip() or f"第{i}章"
        chapters.append({
            "item_id": item_id,
            "title": title,
            "order": i,
        })

    return chapters


def sanitize_filename(name: str) -> str:
    """清理文件名中的非法字符"""
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name


def download_single_chapter(
    chapter: dict,
    chapter_file,
    chapters_dir,
    split_embedded: bool,
    prefer_official: bool = False,
) -> dict:
    """
    下载并写入单章，返回下载结果信息。
    """
    item_id = chapter["item_id"]
    if prefer_official:
        content = get_chapter_content_official(item_id)
    else:
        content = get_chapter_content(item_id)
    chapter_file.write_text(content, encoding="utf-8")

    sections = split_embedded_chapters(content)
    if split_embedded and sections:
        split_dir = chapters_dir / "_split"
        split_dir.mkdir(parents=True, exist_ok=True)
        for section in sections:
            split_path = split_dir / f"{sanitize_filename(section['title'])}.txt"
            split_path.write_text(section["content"], encoding="utf-8")

    return {
        "item_id": item_id,
        "title": chapter["title"],
        "embedded_sections": sections,
    }


def download_book(
    book_id: str,
    delay: float = 0.5,
    force: bool = False,
    split_embedded: bool = False,
    workers: int = 1,
):
    """
    下载整本书

    Args:
        book_id: 书籍ID
        delay: 每次请求间隔（秒）
        force: 强制重新下载已存在的章节
    """
    metadata = ensure_metadata(book_id)
    chapters = get_all_item_ids(metadata)
    prefer_official = metadata.get("data", {}).get("source") == "official_page_fallback"
    if not chapters:
        raise ValueError(
            (
                f"book_id={book_id} 目录为空（0章），已停止下载。"
                "请确认 book_id 是否有效，或检查 API Base 是否可用。"
            )
        )

    chapters_dir = get_chapters_dir(book_id)
    chapters_dir.mkdir(parents=True, exist_ok=True)

    print(f"共 {len(chapters)} 章需要下载\n")

    success_count = 0
    skipped_count = 0
    embedded_split_count = 0
    failed: list[dict] = []

    pending: list[tuple[int, dict, object]] = []
    for i, ch in enumerate(chapters, 1):
        title = sanitize_filename(ch["title"])
        chapter_file = chapters_dir / f"{title}.txt"
        if chapter_file.exists() and not force:
            print(f"[{i}/{len(chapters)}] 跳过: {ch['title']}")
            skipped_count += 1
            continue
        pending.append((i, ch, chapter_file))

    if workers <= 1:
        for i, ch, chapter_file in pending:
            print(f"[{i}/{len(chapters)}] 下载: {ch['title']}", end=" ... ", flush=True)
            try:
                result = download_single_chapter(
                    chapter=ch,
                    chapter_file=chapter_file,
                    chapters_dir=chapters_dir,
                    split_embedded=split_embedded,
                    prefer_official=prefer_official,
                )
                sections = result["embedded_sections"]
                if split_embedded and sections:
                    embedded_split_count += len(sections)
                    print(
                        (
                            f"完成（检测到内嵌 {len(sections)} 章，"
                            f"已拆分到 {chapters_dir / '_split'}）"
                        )
                    )
                elif sections:
                    print(
                        (
                            "完成"
                            f"（检测到内嵌 {len(sections)} 章："
                            f"{sections[0]['title']} ~ {sections[-1]['title']}）"
                        )
                    )
                else:
                    print("完成")
                success_count += 1
            except RuntimeError as e:
                print(f"失败: {e}")
                failed.append({"item_id": ch["item_id"], "title": ch["title"], "error": str(e)})

            if delay > 0:
                time.sleep(delay)
    else:
        if delay > 0:
            print("提示: workers>1 时将忽略 --delay 节流参数")
        print(f"并发下载模式: workers={workers}, 待下载 {len(pending)} 章")

        def _task(task: tuple[int, dict, object]) -> dict:
            idx, ch, chapter_file = task
            try:
                result = download_single_chapter(
                    chapter=ch,
                    chapter_file=chapter_file,
                    chapters_dir=chapters_dir,
                    split_embedded=split_embedded,
                    prefer_official=prefer_official,
                )
                return {"ok": True, "idx": idx, "chapter": ch, "result": result}
            except RuntimeError as e:
                return {"ok": False, "idx": idx, "chapter": ch, "error": str(e)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(_task, task) for task in pending]
            for future in concurrent.futures.as_completed(futures):
                outcome = future.result()
                idx = outcome["idx"]
                ch = outcome["chapter"]
                if outcome["ok"]:
                    sections = outcome["result"]["embedded_sections"]
                    if split_embedded and sections:
                        embedded_split_count += len(sections)
                        msg = (
                            f"完成（检测到内嵌 {len(sections)} 章，"
                            f"已拆分到 {chapters_dir / '_split'}）"
                        )
                    elif sections:
                        msg = (
                            "完成"
                            f"（检测到内嵌 {len(sections)} 章："
                            f"{sections[0]['title']} ~ {sections[-1]['title']}）"
                        )
                    else:
                        msg = "完成"
                    print(f"[{idx}/{len(chapters)}] 下载: {ch['title']} ... {msg}")
                    success_count += 1
                else:
                    err = outcome["error"]
                    print(f"[{idx}/{len(chapters)}] 下载: {ch['title']} ... 失败: {err}")
                    failed.append({"item_id": ch["item_id"], "title": ch["title"], "error": err})

    print(
        "\n下载结束: "
        f"成功 {success_count} 章, 跳过 {skipped_count} 章, 失败 {len(failed)} 章"
    )
    if split_embedded and embedded_split_count > 0:
        print(f"内嵌章节拆分完成: 共 {embedded_split_count} 个章节文件")
    if failed:
        failed_titles = ", ".join(f"{item['title']}({item['item_id']})" for item in failed[:5])
        if len(failed) > 5:
            failed_titles += f" 等共 {len(failed)} 章"
        raise RuntimeError(f"存在下载失败章节: {failed_titles}")


def main():
    parser = argparse.ArgumentParser(description="批量下载番茄小说章节")
    parser.add_argument("book_id", help="小说ID")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="请求间隔秒数（默认0.5）")
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=1,
        help="并发下载线程数（默认1，>1 时会启用并发模式）",
    )
    parser.add_argument("-f", "--force", action="store_true", help="强制重新下载已存在的章节")
    parser.add_argument(
        "--split-embedded",
        action="store_true",
        help="若正文含内嵌章节（如 第一章/第二章...），额外拆分为独立章节文件",
    )

    args = parser.parse_args()

    try:
        download_book(
            args.book_id,
            delay=args.delay,
            force=args.force,
            split_embedded=args.split_embedded,
            workers=max(1, args.workers),
        )
    except (ValueError, RuntimeError) as e:
        print(f"错误: {e}")
        raise SystemExit(2) from e


if __name__ == "__main__":
    main()
