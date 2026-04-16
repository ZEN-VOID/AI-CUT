#!/usr/bin/env python3
"""将历史的 <book_id> 目录迁移到按书名命名的目录。"""

import argparse
import json
import shutil
import sys
from pathlib import Path

from config import extract_book_id, extract_book_title, get_output_root, get_preferred_book_dir


def load_metadata(path: Path) -> dict | None:
    """读取 metadata.json，失败时返回 None。"""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def collect_legacy_book_ids(include_all: bool, book_ids: list[str]) -> list[str]:
    """收集需要迁移的 book_id 列表。"""
    ids: list[str] = []

    if include_all:
        output_root = get_output_root()
        if output_root.exists():
            for candidate in sorted(output_root.iterdir(), key=lambda item: item.name):
                if candidate.is_dir() and candidate.name.isdigit():
                    ids.append(candidate.name)

    ids.extend(book_ids)

    deduped: list[str] = []
    for book_id in ids:
        normalized = str(book_id).strip()
        if normalized and normalized not in deduped:
            deduped.append(normalized)
    return deduped


def ensure_same_book(target_dir: Path, book_id: str) -> None:
    """校验目标目录若已存在，其 metadata 必须属于同一本书。"""
    metadata = load_metadata(target_dir / "metadata.json")
    if not metadata:
        return

    target_book_id = extract_book_id(metadata)
    if target_book_id and target_book_id != book_id:
        raise RuntimeError(
            f"目标目录 {target_dir} 已存在且属于其他 book_id={target_book_id}，已停止迁移。"
        )


def merge_tree(source_dir: Path, target_dir: Path) -> None:
    """将 source_dir 内容安全合并到 target_dir。"""
    target_dir.mkdir(parents=True, exist_ok=True)

    for child in sorted(source_dir.iterdir(), key=lambda item: item.name):
        target_child = target_dir / child.name

        if child.is_dir():
            if target_child.exists() and not target_child.is_dir():
                raise RuntimeError(f"目标路径已存在同名文件，无法合并目录: {target_child}")
            if target_child.exists():
                merge_tree(child, target_child)
                child.rmdir()
            else:
                shutil.move(str(child), str(target_child))
            continue

        if not target_child.exists():
            shutil.move(str(child), str(target_child))
            continue

        if child.read_bytes() == target_child.read_bytes():
            child.unlink()
            continue

        raise RuntimeError(f"目标文件已存在且内容不同，无法安全覆盖: {target_child}")

    source_dir.rmdir()


def migrate_legacy_dir(book_id: str, dry_run: bool = False) -> tuple[str, str]:
    """迁移单个旧目录。"""
    output_root = get_output_root()
    legacy_dir = output_root / book_id

    if not legacy_dir.exists():
        return "skip", f"{book_id}: 未找到旧目录"
    if not legacy_dir.is_dir():
        return "skip", f"{book_id}: 旧路径不是目录"

    metadata = load_metadata(legacy_dir / "metadata.json")
    if not metadata:
        return "skip", f"{book_id}: 缺少或无法解析 metadata.json"

    title = extract_book_title(metadata)
    if not title:
        return "skip", f"{book_id}: metadata.json 中缺少书名，无法迁移"

    target_dir = get_preferred_book_dir(book_id, title)
    ensure_same_book(target_dir, book_id)

    if legacy_dir == target_dir:
        return "ok", f"{book_id}: 已是书名目录 -> {target_dir}"

    action = "rename" if not target_dir.exists() else "merge"
    if dry_run:
        return "plan", f"{book_id}: {action} -> {target_dir}"

    if not target_dir.exists():
        legacy_dir.rename(target_dir)
    else:
        merge_tree(legacy_dir, target_dir)

    return "ok", f"{book_id}: {action} 完成 -> {target_dir}"


def main() -> int:
    parser = argparse.ArgumentParser(description="将旧的 <book_id> 小说目录迁移为书名目录")
    parser.add_argument("book_ids", nargs="*", help="要迁移的 book_id，可传多个")
    parser.add_argument("--all", action="store_true", help="扫描 output_root 下所有数字目录并迁移")
    parser.add_argument("--dry-run", action="store_true", help="仅输出迁移计划，不真正改动")
    args = parser.parse_args()

    book_ids = collect_legacy_book_ids(args.all, args.book_ids)
    if not book_ids:
        parser.error("请传入至少一个 book_id，或使用 --all")

    has_error = False
    for book_id in book_ids:
        try:
            _, message = migrate_legacy_dir(book_id, dry_run=args.dry_run)
            print(message)
        except Exception as exc:  # noqa: BLE001
            has_error = True
            print(f"{book_id}: 迁移失败: {exc}", file=sys.stderr)

    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
