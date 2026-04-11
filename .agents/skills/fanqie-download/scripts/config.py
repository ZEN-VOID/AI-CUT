#!/usr/bin/env python3
"""API 配置模块"""

from pathlib import Path
from urllib.parse import quote

# 默认 API 基础地址（格式：protocol://host:port）
DEFAULT_API_BASE = "http://47.108.80.161:5005"
# API 候选节点（用于故障切换）
API_BASE_CANDIDATES = [
    "http://47.108.80.161:5005",
    "http://101.35.133.34:5000",
    "https://bk.yydjtc.cn",
    "http://103.236.91.147:9999",
]
# 默认数据输出根目录
OUTPUT_ROOT = Path("input") / "番茄小说"

# 当前使用的 API 基础地址
_api_base = DEFAULT_API_BASE


def get_api_base() -> str:
    """获取当前 API 基础地址"""
    return _api_base


def get_api_base_candidates() -> list[str]:
    """获取候选 API 节点列表（当前节点优先，自动去重）"""
    bases = [_api_base, *API_BASE_CANDIDATES]
    deduped: list[str] = []
    for base in bases:
        b = str(base).strip().rstrip("/")
        if not b:
            continue
        if b not in deduped:
            deduped.append(b)
    return deduped


def set_api_base(base: str):
    """设置 API 基础地址"""
    global _api_base
    base = base.strip().rstrip("/")
    # 如果没有协议前缀，默认使用 http
    if not base.startswith(("http://", "https://")):
        base = f"http://{base}"
    _api_base = base


def get_book_api_url(book_id: str) -> str:
    """获取书籍目录 API URL"""
    return f"{_api_base}/api/directory?book_id={book_id}"


def get_content_api_url() -> str:
    """获取章节内容 API URL"""
    return f"{_api_base}/api/content"


def get_detail_api_url(book_id: str) -> str:
    """获取书籍详情 API URL"""
    return f"{_api_base}/api/detail?book_id={book_id}"


def get_search_api_url(keyword: str) -> str:
    """获取书籍搜索 API URL（按关键词）"""
    return f"{_api_base}/api/search?key={quote(keyword)}"


def get_referer() -> str:
    """获取 referer"""
    return f"{_api_base}/docs"


def get_output_root() -> Path:
    """获取输出根目录"""
    return OUTPUT_ROOT


def get_book_dir(book_id: str) -> Path:
    """获取单本小说目录"""
    return OUTPUT_ROOT / str(book_id)


def get_metadata_path(book_id: str) -> Path:
    """获取 metadata.json 路径"""
    return get_book_dir(book_id) / "metadata.json"


def get_chapters_dir(book_id: str) -> Path:
    """获取章节目录路径"""
    return get_book_dir(book_id) / "chapters"
