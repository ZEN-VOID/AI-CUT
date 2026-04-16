#!/usr/bin/env python3
"""API 配置模块"""

import json
from pathlib import Path
import re
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


def sanitize_path_component(name: str, fallback: str) -> str:
    """清理目录名中的非法字符，并保留可读书名。"""
    cleaned = re.sub(r'[\\/:*?"<>|]+', "_", str(name).strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned or fallback


def extract_book_title(metadata: dict) -> str:
    """从 metadata 中提取书名。"""
    data = metadata.get("data", {}) if isinstance(metadata, dict) else {}
    for key in ("book_name", "book_title", "title", "name"):
        value = str(data.get(key, "")).strip()
        if value:
            return value

    for key in ("book_name", "book_title", "title", "name"):
        value = str(metadata.get(key, "")).strip() if isinstance(metadata, dict) else ""
        if value:
            return value

    return ""


def extract_book_id(metadata: dict) -> str:
    """从 metadata 中提取 book_id。"""
    data = metadata.get("data", {}) if isinstance(metadata, dict) else {}
    for key in ("book_id", "bookId", "id"):
        value = str(data.get(key, "")).strip()
        if value:
            return value

    for key in ("book_id", "bookId", "id"):
        value = str(metadata.get(key, "")).strip() if isinstance(metadata, dict) else ""
        if value:
            return value

    return ""


def _read_metadata(path: Path) -> dict | None:
    """安全读取 metadata.json。"""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def find_existing_book_dir(book_id: str) -> Path | None:
    """按 book_id 查找已存在目录，兼容旧的 book_id 目录与新的书名目录。"""
    output_root = get_output_root()
    if not output_root.exists():
        return None

    legacy_dir = output_root / str(book_id)
    if legacy_dir.exists():
        return legacy_dir

    for candidate in output_root.iterdir():
        if not candidate.is_dir():
            continue
        metadata = _read_metadata(candidate / "metadata.json")
        if not metadata:
            continue
        if extract_book_id(metadata) == str(book_id):
            return candidate

    return None


def get_preferred_book_dir(book_id: str, book_title: str) -> Path:
    """根据书名生成首选目录；若同名目录已被其他 book_id 占用，则追加冲突后缀。"""
    safe_title = sanitize_path_component(book_title, fallback=str(book_id))
    primary_dir = OUTPUT_ROOT / safe_title
    existing_metadata = _read_metadata(primary_dir / "metadata.json")
    if existing_metadata and extract_book_id(existing_metadata) not in {"", str(book_id)}:
        safe_title = sanitize_path_component(f"{book_title}__{book_id}", fallback=str(book_id))
        return OUTPUT_ROOT / safe_title
    return primary_dir


def get_book_dir(
    book_id: str,
    book_title: str | None = None,
    *,
    create: bool = False,
    migrate_legacy: bool = False,
) -> Path:
    """获取单本小说目录，默认优先按书名命名并兼容旧 book_id 目录。"""
    existing_dir = find_existing_book_dir(book_id)

    if book_title:
        preferred_dir = get_preferred_book_dir(book_id, book_title)
        if existing_dir and existing_dir != preferred_dir:
            legacy_dir = OUTPUT_ROOT / str(book_id)
            if (
                migrate_legacy
                and existing_dir == legacy_dir
                and existing_dir.exists()
                and not preferred_dir.exists()
            ):
                existing_dir.rename(preferred_dir)
                return preferred_dir
            return existing_dir

        if preferred_dir.exists() or create:
            return preferred_dir

    if existing_dir:
        return existing_dir

    return OUTPUT_ROOT / str(book_id)


def get_metadata_path(
    book_id: str,
    book_title: str | None = None,
    *,
    create: bool = False,
    migrate_legacy: bool = False,
) -> Path:
    """获取 metadata.json 路径"""
    return get_book_dir(
        book_id,
        book_title=book_title,
        create=create,
        migrate_legacy=migrate_legacy,
    ) / "metadata.json"


def get_chapters_dir(
    book_id: str,
    book_title: str | None = None,
    *,
    create: bool = False,
    migrate_legacy: bool = False,
) -> Path:
    """获取章节目录路径"""
    return get_book_dir(
        book_id,
        book_title=book_title,
        create=create,
        migrate_legacy=migrate_legacy,
    ) / "chapters"
