#!/usr/bin/env python3
"""按关键词搜索番茄小说并返回可下载 book_id。"""

import argparse
import json
import sys
import time
from urllib.parse import quote

import requests

from config import (
    get_api_base,
    get_api_base_candidates,
    get_referer,
    get_search_api_url,
    set_api_base,
)


OFFICIAL_SEARCH_URL = "https://api5-normal-lf.fqnovel.com/reading/bookapi/search/page/v/"


def search_books_official(keyword: str) -> dict:
    """使用番茄官方搜索接口兜底。"""
    headers = {
        "accept": "application/json, text/plain, */*",
        "referer": "https://fanqienovel.com/",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        ),
    }
    params = {
        "query": keyword,
        "aid": "1967",
        "channel": "0",
        "os_version": "0",
        "device_type": "0",
        "device_platform": "0",
        "iid": "466614321180296",
        "passback": "{(page-1)*10}",
        "version_code": "999",
    }
    response = requests.get(OFFICIAL_SEARCH_URL, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()


def search_books(keyword: str, max_retries: int = 2, retry_delay: float = 0.8) -> dict:
    """
    调用搜索接口获取原始结果（带候选节点回退）。

    Args:
        keyword: 搜索关键词
        max_retries: 单节点最大尝试次数
        retry_delay: 重试基准等待（秒）

    Returns:
        搜索接口的原始 JSON
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
        url = get_search_api_url(keyword)
        last_error: Exception | None = None

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(url, headers=headers, timeout=20)
                response.raise_for_status()
                data = response.json()
                if base != original_base:
                    print(
                        f"提示: 搜索接口已切换 API 节点 {original_base} -> {base}",
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
    set_api_base(original_base)
    try:
        data = search_books_official(keyword)
        print(
            "提示: 第三方搜索节点不可用，已回退到番茄官网搜索接口。",
            file=sys.stderr,
        )
        return data
    except (requests.RequestException, json.JSONDecodeError) as e:
        raise RuntimeError(
            f"搜索请求失败，候选节点均不可用: {' | '.join(base_errors)} | official_search: {e}"
        ) from e


def parse_search_results(data: dict) -> list[dict]:
    """
    解析搜索结果，输出统一字段。

    Returns:
        列表元素示例：
        {
            "book_id": "1234567890",
            "title": "书名",
            "author": "作者",
            "word_number": 123456,
        }
    """
    results: list[dict] = []
    seen_ids: set[str] = set()

    def _append_items(items: list[dict]):
        for item in items:
            book_data = item.get("book_data", [])
            if not isinstance(book_data, list) or not book_data:
                continue

            book = book_data[0]
            if not isinstance(book, dict):
                continue

            book_id = str(book.get("book_id", "")).strip()
            if not book_id or book_id in seen_ids:
                continue

            seen_ids.add(book_id)
            title = str(book.get("book_name", "")).strip() or "未知书名"
            author = str(book.get("author", "")).strip() or "未知作者"
            word_number = book.get("word_number", 0)

            results.append(
                {
                    "book_id": book_id,
                    "title": title,
                    "author": author,
                    "word_number": int(word_number) if isinstance(word_number, int) else 0,
                }
            )

    data_root = data.get("data")
    if isinstance(data_root, list):
        _append_items(data_root)
        return results

    if not isinstance(data_root, dict):
        return results

    tabs = data_root.get("search_tabs")
    if not isinstance(tabs, list):
        return results

    for tab in tabs:
        tab_data = tab.get("data", [])
        if not isinstance(tab_data, list):
            continue
        _append_items(tab_data)

    return results


def main():
    parser = argparse.ArgumentParser(description="按关键词搜索番茄小说")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("-j", "--json", action="store_true", help="输出 JSON")
    parser.add_argument("-r", "--raw", action="store_true", help="输出原始 API 响应")
    parser.add_argument("-l", "--limit", type=int, default=20, help="最多显示条数（默认 20）")
    args = parser.parse_args()

    keyword = args.keyword.strip()
    if not keyword:
        print("错误: 关键词不能为空", file=sys.stderr)
        raise SystemExit(2)

    try:
        data = search_books(keyword)
    except RuntimeError as e:
        print(f"错误: {e}", file=sys.stderr)
        print(
            "排查建议: 1) 检查 API Base 可达性 2) 更换关键词重试 3) 在 Gradio 的 API 设置中切换地址。",
            file=sys.stderr,
        )
        raise SystemExit(1) from e

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    results = parse_search_results(data)
    if args.limit > 0:
        results = results[: args.limit]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if not results:
        api_code = data.get("code")
        api_message = data.get("message", "")
        nested = data.get("data", {})
        nested_code = nested.get("code") if isinstance(nested, dict) else None
        nested_message = nested.get("message") if isinstance(nested, dict) else None

        print(
            (
                f"未检索到结果（keyword={keyword!r}）。"
                f"API: code={api_code}, message={api_message!r}, "
                f"inner_code={nested_code}, inner_message={nested_message!r}"
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    print(f"关键词: {keyword}")
    print(f"命中: {len(results)} 条\n")
    for idx, item in enumerate(results, 1):
        print(
            f"{idx:>3}. {item['title']} | 作者: {item['author']} | "
            f"book_id: {item['book_id']} | 字数: {item['word_number']}"
        )


if __name__ == "__main__":
    main()
