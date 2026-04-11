#!/usr/bin/env python3
"""番茄短篇分享页下载器（可见正文抓取）"""

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from config import get_book_dir


PLAYWRIGHT_EVAL_JS = (
    "async () => {"
    "  await new Promise((resolve) => setTimeout(resolve, 2500));"
    "  const titleEl = document.querySelector(\"h1, [class*='title'], .title\");"
    "  const title = (titleEl && titleEl.textContent ? titleEl.textContent : document.title || '').trim();"
    "  const text = (document.body && document.body.innerText ? document.body.innerText : '').trim();"
    "  return { url: location.href, title, text };"
    "}"
)


def sanitize_filename(name: str) -> str:
    """清理文件名中的非法字符"""
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name


def extract_post_id_from_url(url: str) -> str | None:
    """从短篇分享 URL 提取 post_id（或回退 content_id）"""
    parsed = urlparse(url)
    if not parsed.scheme:
        return None

    query = parse_qs(parsed.query)
    post_id = (query.get("post_id") or [None])[0]
    if post_id and post_id.isdigit():
        return post_id

    report_raw = (query.get("report_params") or [None])[0]
    if report_raw:
        try:
            report_data = json.loads(unquote(report_raw))
            content_id = str(report_data.get("content_id", "")).strip()
            if content_id.isdigit():
                return content_id
        except json.JSONDecodeError:
            pass

    return None


def has_complete_share_params(url: str) -> bool:
    """判断分享链接是否包含完整鉴权参数"""
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    return bool((query.get("share_token") or [None])[0] and (query.get("report_params") or [None])[0])


def read_cached_source_url(post_id: str) -> str | None:
    """读取该 post_id 最近成功抓取时保存的 source_url"""
    meta_path = get_book_dir(post_id) / "share_metadata.json"
    if not meta_path.exists():
        return None

    try:
        data = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    source_url = str(data.get("source_url", "")).strip()
    if source_url:
        return source_url
    return None


def _resolve_playwright_cli() -> str:
    """定位 playwright-cli 启动命令"""
    pwcli_env = os.environ.get("PWCLI")
    if pwcli_env and Path(pwcli_env).exists():
        return pwcli_env

    codex_home = os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))
    default_pwcli = Path(codex_home) / "skills" / "playwright" / "scripts" / "playwright_cli.sh"
    if default_pwcli.exists():
        return str(default_pwcli)

    global_cli = shutil.which("playwright-cli")
    if global_cli:
        return global_cli

    raise RuntimeError(
        "未找到 playwright-cli。请先确认已安装 Node.js（含 npx）并可用 `$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh`。"
    )


def _run_cli(cmd: list[str], timeout: int = 120) -> str:
    """执行命令并返回 stdout"""
    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        msg = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"命令执行失败: {' '.join(cmd)}\n{msg}")
    return completed.stdout


def _parse_result_json(cli_output: str) -> dict:
    """从 playwright-cli 输出提取 ### Result JSON"""
    match = re.search(r"### Result\s*\n(.*?)(?:\n### Ran Playwright code|\Z)", cli_output, re.S)
    if not match:
        raise RuntimeError("未能从 playwright-cli 输出中提取结果。")

    payload = match.group(1).strip()
    if not payload:
        raise RuntimeError("playwright-cli 返回结果为空。")

    try:
        return json.loads(payload)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"解析 playwright-cli 结果失败: {e}") from e


def _fetch_visible_text_with_playwright(share_url: str) -> dict:
    """通过真实浏览器渲染抓取可见文本"""
    cli = _resolve_playwright_cli()

    _run_cli([cli, "open", share_url], timeout=120)
    try:
        eval_output = _run_cli([cli, "eval", PLAYWRIGHT_EVAL_JS], timeout=120)
        result = _parse_result_json(eval_output)
    finally:
        subprocess.run([cli, "close"], capture_output=True, text=True, check=False)

    text = str(result.get("text", "")).strip()
    if not text:
        raise RuntimeError("页面正文为空，可能链接已失效或需要 App 侧权限。")

    title = str(result.get("title", "")).strip() or "短篇分享"
    url = str(result.get("url", "")).strip() or share_url
    return {"title": title, "text": text, "url": url}


def clean_story_text(raw_text: str) -> str:
    """清理页面可见文本，裁掉评论/拉起 App 区域"""
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n").strip()

    cut_markers = [
        "去App查看全部内容",
        "去 APP 查看全部内容",
        "去App查看全部评论",
        "去 APP 查看全部评论",
        "全部回复・",
        "全部评论・",
        "打开APP查看更多回复",
        "打开App查看更多回复",
        "打开 APP 查看更多回复",
        "下载番茄小说",
        "打开番茄小说",
    ]

    cut_pos = len(text)
    for marker in cut_markers:
        idx = text.find(marker)
        if idx != -1 and idx > 80 and idx < cut_pos:
            cut_pos = idx
    text = text[:cut_pos].rstrip()

    lines = [line.rstrip() for line in text.split("\n")]
    compact_lines: list[str] = []
    blank_count = 0
    for line in lines:
        if not line.strip():
            blank_count += 1
            if blank_count > 1:
                continue
        else:
            blank_count = 0
        compact_lines.append(line)

    final_text = "\n".join(compact_lines).strip()
    return f"{final_text}\n" if final_text else ""


def download_short_story_from_url(share_url: str) -> dict:
    """下载短篇分享页可见正文并落盘"""
    share_url = share_url.strip()
    if not share_url:
        raise ValueError("分享链接不能为空。")

    post_id = extract_post_id_from_url(share_url)
    if not post_id:
        raise ValueError("无法从链接中提取 post_id，请确认是短篇分享链接。")

    source_candidates = [share_url]
    cached_source_url = read_cached_source_url(post_id)
    if cached_source_url and cached_source_url != share_url:
        source_candidates.append(cached_source_url)

    fetched = None
    last_error: Exception | None = None
    for candidate in source_candidates:
        try:
            fetched = _fetch_visible_text_with_playwright(candidate)
            break
        except RuntimeError as e:
            last_error = e

    if fetched is None:
        if not has_complete_share_params(share_url):
            raise RuntimeError(
                "页面正文为空，且当前链接缺少完整分享参数。请提供完整 short-story-share 链接（含 share_token）。"
            ) from last_error
        if last_error:
            raise last_error
        raise RuntimeError("页面正文为空，可能链接已失效或需要 App 侧权限。")

    cleaned_text = clean_story_text(fetched["text"])
    if not cleaned_text:
        raise RuntimeError("抓取结果为空，无法保存。")

    book_dir = get_book_dir(post_id)
    book_dir.mkdir(parents=True, exist_ok=True)

    text_path = book_dir / f"短篇分享-{post_id}.txt"
    meta_path = book_dir / "share_metadata.json"

    text_path.write_text(cleaned_text, encoding="utf-8")

    metadata = {
        "post_id": post_id,
        "title": fetched["title"],
        "source_url": fetched["url"],
        "chars": len(cleaned_text),
        "extract_method": "playwright_dom_visible_text",
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "post_id": post_id,
        "title": fetched["title"],
        "content": cleaned_text,
        "chars": len(cleaned_text),
        "text_path": str(text_path),
        "meta_path": str(meta_path),
    }


def main():
    parser = argparse.ArgumentParser(description="下载番茄短篇分享页可见正文")
    parser.add_argument("share_url", help="短篇分享链接")
    args = parser.parse_args()

    try:
        result = download_short_story_from_url(args.share_url)
    except (ValueError, RuntimeError) as e:
        print(f"错误: {e}")
        raise SystemExit(2) from e

    safe_title = sanitize_filename(result["title"])[:80]
    print(f"已保存短篇分享: {safe_title}")
    print(f"post_id: {result['post_id']}")
    print(f"正文文件: {result['text_path']}")
    print(f"元数据文件: {result['meta_path']}")
    print(f"字符数: {result['chars']}")


if __name__ == "__main__":
    main()
