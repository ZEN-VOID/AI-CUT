#!/usr/bin/env python3
"""获取番茄小说目录"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

from config import (
    get_api_base,
    get_api_base_candidates,
    get_book_api_url,
    get_detail_api_url,
    get_metadata_path,
    get_referer,
    set_api_base,
)


OFFICIAL_BOOK_PAGE = "https://fanqienovel.com/page/{book_id}"


def request_json_with_base_fallback(
    url_factory,
    *,
    error_prefix: str,
    max_retries: int = 2,
    retry_delay: float = 0.8,
) -> dict:
    """
    使用候选 API 节点拉取 JSON，单节点失败时自动切换。

    Args:
        url_factory: 基于当前 API base 生成 URL 的回调
        error_prefix: 失败报错前缀
        max_retries: 单节点最大尝试次数
        retry_delay: 重试基准等待（秒）
    """
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "referer": get_referer(),
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }
    original_base = get_api_base()
    base_errors: list[str] = []

    for base in get_api_base_candidates():
        set_api_base(base)
        url = url_factory()
        last_error: Exception | None = None

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, headers=headers, timeout=20)
                response.raise_for_status()
                data = response.json()
                if base != original_base:
                    print(
                        f"提示: 目录接口已切换 API 节点 {original_base} -> {base}",
                        file=sys.stderr,
                    )
                return data
            except (requests.RequestException, json.JSONDecodeError) as e:
                last_error = e
                if attempt < max_retries:
                    time.sleep(retry_delay * attempt)
                    continue
                break

        base_errors.append(f"{base}: {last_error}")

    set_api_base(original_base)
    raise RuntimeError(f"{error_prefix}，候选节点均不可用: {' | '.join(base_errors)}")


def get_book_catalog(book_id: str) -> dict:
    """
    获取小说目录

    Args:
        book_id: 小说ID

    Returns:
        包含章节信息的字典
    """
    try:
        return request_json_with_base_fallback(
            lambda: get_book_api_url(book_id),
            error_prefix=f"目录请求失败(book_id={book_id})",
        )
    except RuntimeError:
        return get_book_catalog_from_official_page(book_id)


def get_book_detail(book_id: str) -> dict:
    """获取书籍详情（用于空目录诊断）"""
    return request_json_with_base_fallback(
        lambda: get_detail_api_url(book_id),
        error_prefix=f"详情请求失败(book_id={book_id})",
    )


def get_book_catalog_from_official_page(book_id: str) -> dict:
    """从番茄官网书籍详情页解析目录，作为第三方 API 失效时的兜底方案。"""
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "referer": "https://fanqienovel.com/",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }
    response = requests.get(
        OFFICIAL_BOOK_PAGE.format(book_id=book_id),
        headers=headers,
        timeout=20,
    )
    response.raise_for_status()
    html = response.text

    title_match = re.search(r"<h1[^>]*>([^<]+)</h1>", html)
    title = title_match.group(1).strip() if title_match else str(book_id)

    chapter_matches = re.findall(r'<a href="/reader/(\d+)"[^>]*>(.*?)</a>', html, re.S)
    parsed_chapters: list[tuple[str, str]] = []
    for item_id, inner_html in chapter_matches:
        chapter_title = re.sub(r"<[^>]+>", "", inner_html).strip()
        if not chapter_title.startswith("第"):
            continue
        parsed_chapters.append((item_id, chapter_title))

    if not parsed_chapters:
        raise RuntimeError(
            f"目录请求失败(book_id={book_id})，第三方 API 不可用且官网页面未解析到目录。"
        )

    lists: list[dict] = []
    for idx, (item_id, chapter_title) in enumerate(parsed_chapters, 1):
        lists.append(
            {
                "item_id": str(item_id),
                "title": chapter_title.strip() or f"第{idx}章",
                "volume_name": "正文卷",
                "need_pay": False,
            }
        )

    print(
        "提示: 第三方目录接口不可用，已回退到番茄官网书页解析目录。",
        file=sys.stderr,
    )
    return {
        "code": 0,
        "message": "success",
        "data": {
            "book_id": str(book_id),
            "book_name": title,
            "lists": lists,
            "source": "official_page_fallback",
        },
    }


def parse_catalog(data: dict) -> list[dict]:
    """
    解析目录数据，返回章节列表

    Args:
        data: API返回的原始数据

    Returns:
        章节列表，每个章节包含 item_id, title 等信息
    """
    chapter_list = data.get("data", {}).get("lists")
    if not isinstance(chapter_list, list):
        return []

    chapters = []
    for i, chapter in enumerate(chapter_list, 1):
        item_id = str(chapter.get("item_id", "")).strip()
        if not item_id:
            continue

        title = str(chapter.get("title", f"第{i}章")).strip() or f"第{i}章"
        need_pay_raw = chapter.get("need_pay", chapter.get("needPay", False))

        chapters.append({
            "item_id": item_id,
            "title": title,
            "order": i,
            "volume": str(chapter.get("volume_name", "")).strip(),
            "need_pay": bool(need_pay_raw),
        })

    return chapters


def get_chapters(book_id: str) -> list[dict]:
    """
    获取小说章节列表（便捷函数）

    Args:
        book_id: 小说ID

    Returns:
        章节列表
    """
    data = get_book_catalog(book_id)
    return parse_catalog(data)


def save_catalog(book_id: str, data: dict) -> Path:
    """
    保存目录数据到本地

    Args:
        book_id: 小说ID
        data: API返回的原始数据

    Returns:
        保存的文件路径
    """
    metadata_path = get_metadata_path(book_id)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    return metadata_path


def main():
    parser = argparse.ArgumentParser(description="获取番茄小说目录")
    parser.add_argument("book_id", help="小说ID")
    parser.add_argument("-j", "--json", action="store_true", help="输出JSON格式")
    parser.add_argument("-r", "--raw", action="store_true", help="输出原始API响应")
    parser.add_argument("-n", "--no-save", action="store_true", help="不保存到本地")

    args = parser.parse_args()

    try:
        data = get_book_catalog(args.book_id)
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        print(
            "排查建议: 1) 稍后重试 2) 检查 API Base 可达性 3) 在 Gradio 的 API 设置中切换地址。",
            file=sys.stderr,
        )
        raise SystemExit(1) from e

    # 默认保存到本地
    if not args.no_save:
        path = save_catalog(args.book_id, data)
        print(f"已保存到 {path}")

    chapters = parse_catalog(data)
    empty_catalog = len(chapters) == 0

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.json:
        print(json.dumps(chapters, ensure_ascii=False, indent=2))
    else:
        print(f"共 {len(chapters)} 章\n")
        for ch in chapters:
            pay_mark = " [付费]" if ch["need_pay"] else ""
            print(f"{ch['order']:>4}. {ch['title']}{pay_mark}")

    if empty_catalog:
        api_code = data.get("code")
        api_message = data.get("message", "")
        print(
            (
                f"警告: book_id={args.book_id} 返回空目录（0章）。"
                f"API 响应: code={api_code}, message={api_message!r}"
            ),
            file=sys.stderr,
        )
        print(
            "排查建议: 1) 核对 book_id 是否可访问 2) 切换可用 API Base 3) 用已知 book_id 做连通性对照。",
            file=sys.stderr,
        )
        try:
            detail = get_book_detail(args.book_id)
            detail_data = detail.get("data", {})
            if isinstance(detail_data, dict):
                detail_msg = detail_data.get("message")
                detail_code = detail_data.get("code")
                if detail_msg == "BOOK_REMOVE" or detail_code == 101109:
                    print(
                        "诊断结论: 该 ID 对应内容状态为 BOOK_REMOVE（疑似已下架/删除）。",
                        file=sys.stderr,
                    )
        except RuntimeError:
            pass
        raise SystemExit(2)


if __name__ == "__main__":
    main()
