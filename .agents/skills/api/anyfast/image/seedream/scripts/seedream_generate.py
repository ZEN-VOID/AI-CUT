#!/usr/bin/env python3
"""
SEEDREAM 5.0 图像生成 CLI

支持:
- 文本生图 (T2I)
- 参考图生图 (I2I)
- 连续多图生成 (sequential_image_generation)
- 流式返回 (SSE) 与非流式返回
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

try:
    from dotenv import load_dotenv

    try:
        load_dotenv()
    except Exception:
        # 某些 Python 环境中 find_dotenv 可能失败，退化到显式路径
        load_dotenv(dotenv_path=str(Path.cwd() / ".env"))
except ImportError:
    print("❌ 缺少依赖: pip install requests python-dotenv")
    sys.exit(1)


DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DEFAULT_OUTPUT_DIR = Path("output/seedream")


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _safe_name(text: str, max_len: int = 40) -> str:
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"[^0-9A-Za-z_\u4e00-\u9fff-]+", "", text)
    if not text:
        return "seedream"
    return text[:max_len]


def _detect_ext_from_url(url: str) -> str:
    path = url.split("?", 1)[0]
    ext = Path(path).suffix.lower()
    if ext in {".png", ".jpg", ".jpeg", ".webp"}:
        return ext
    return ".png"


def _extract_image_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    top_level_url = payload.get("url")
    top_level_b64 = payload.get("b64_json")
    if top_level_url or top_level_b64:
        items.append(
            {
                "index": payload.get("image_index", 0),
                "url": top_level_url,
                "b64_json": top_level_b64,
                "revised_prompt": payload.get("revised_prompt"),
                "size": payload.get("size"),
                "event_type": payload.get("type"),
            }
        )

    data = payload.get("data")
    if not isinstance(data, list):
        return items

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        b64_json = item.get("b64_json")
        revised_prompt = item.get("revised_prompt")
        if not url and not b64_json:
            continue
        items.append(
            {
                "index": i,
                "url": url,
                "b64_json": b64_json,
                "revised_prompt": revised_prompt,
                "size": item.get("size"),
                "event_type": payload.get("type"),
            }
        )
    return items


def _merge_items(payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: List[Dict[str, Any]] = []
    seen: set = set()

    for payload in payloads:
        for item in _extract_image_items(payload):
            dedup_key = item.get("url") or item.get("b64_json")
            if not dedup_key or dedup_key in seen:
                continue
            seen.add(dedup_key)
            merged.append(item)
    return merged


def _read_sse_payloads(response: requests.Response) -> List[Dict[str, Any]]:
    payloads: List[Dict[str, Any]] = []
    for raw_line in response.iter_lines(decode_unicode=True):
        if not raw_line:
            continue
        line = raw_line.strip()

        # SSE 标准: "data: ..."
        if line.startswith("data:"):
            line = line[5:].strip()
        elif line.startswith("event:"):
            continue

        if line in {"[DONE]", "DONE"}:
            break

        try:
            event_payload = json.loads(line)
        except json.JSONDecodeError:
            # 忽略非 JSON 的心跳/中间行
            continue

        payloads.append(event_payload)
    return payloads


@dataclass
class SeedreamConfig:
    api_key: str
    api_url: str = DEFAULT_API_URL
    model: str = DEFAULT_MODEL
    timeout: int = 180


class SeedreamClient:
    def __init__(self, cfg: SeedreamConfig):
        self.cfg = cfg
        self.headers = {
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        payload: Dict[str, Any],
        use_stream: bool,
    ) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
        if use_stream:
            with requests.post(
                self.cfg.api_url,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=self.cfg.timeout,
            ) as resp:
                try:
                    resp.raise_for_status()
                except requests.HTTPError as exc:
                    body = resp.text
                    raise RuntimeError(f"HTTP {resp.status_code}: {body}") from exc
                payloads = _read_sse_payloads(resp)
                final_payload = payloads[-1] if payloads else None
                return payloads, final_payload

        resp = requests.post(
            self.cfg.api_url,
            headers=self.headers,
            json=payload,
            timeout=self.cfg.timeout,
        )
        try:
            resp.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text}") from exc

        body = resp.json()
        return [body], body


def _save_from_url(url: str, out_path: Path, timeout: int) -> None:
    with requests.get(url, timeout=timeout) as resp:
        resp.raise_for_status()
        out_path.write_bytes(resp.content)


def _save_from_b64(b64_data: str, out_path: Path) -> None:
    out_path.write_bytes(base64.b64decode(b64_data))


def _env_api_key() -> Optional[str]:
    return (
        os.getenv("SEEDREAM_API_KEY")
        or os.getenv("ARK_API_KEY")
        or os.getenv("VOLCENGINE_ARK_API_KEY")
    )


def _diagnostic_hint(exc: Exception, payload: Dict[str, Any], use_stream: bool) -> Optional[str]:
    message = str(exc)
    max_images = (
        payload.get("sequential_image_generation_options", {}).get("max_images")
        if isinstance(payload.get("sequential_image_generation_options"), dict)
        else None
    )
    is_read_timeout = isinstance(exc, requests.exceptions.ReadTimeout) or "Read timed out" in message

    if is_read_timeout and not use_stream and isinstance(max_images, int) and max_images >= 5:
        return (
            "Large sequential image requests can exceed non-streaming read timeouts. "
            "Retry with --stream, increase --timeout, or reduce --max-images."
        )
    if is_read_timeout:
        return "Read timeout. Retry with --stream or increase --timeout."
    return None


def _empty_result_hint(payloads: List[Dict[str, Any]], final_payload: Optional[Dict[str, Any]]) -> str:
    event_types = [str(payload.get("type")) for payload in payloads if payload.get("type")]
    usage = final_payload.get("usage") if isinstance(final_payload, dict) else None
    generated_images = usage.get("generated_images") if isinstance(usage, dict) else None
    if generated_images:
        return (
            "The API reported generated_images but no url/b64_json was extracted. "
            "Check streaming event parsing for partial_succeeded payloads."
        )
    if any(event_type == "image_generation.partial_failed" for event_type in event_types):
        return "The stream contained partial_failed events. Inspect final_payload/error details."
    return "No image url/b64_json was found in the API response."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SEEDREAM 5.0 图像生成 CLI (Ark OpenAI 兼容接口)"
    )
    parser.add_argument("--prompt", required=True, help="提示词")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="API URL")
    parser.add_argument("--api-key", help="API Key（不传则读取 .env）")
    parser.add_argument("--image-url", action="append", default=[], help="参考图 URL（可重复）")

    parser.add_argument(
        "--sequential-image-generation",
        default="auto",
        help="连续图模式，默认 auto",
    )
    parser.add_argument("--max-images", type=int, default=4, help="连续图最大数量")
    parser.add_argument(
        "--response-format",
        choices=["url", "b64_json"],
        default="url",
        help="返回格式",
    )
    parser.add_argument("--size", default="2K", help="输出尺寸，如 2K")
    parser.add_argument("--stream", action="store_true", help="启用流式返回")
    parser.add_argument("--watermark", dest="watermark", action="store_true", default=True)
    parser.add_argument("--no-watermark", dest="watermark", action="store_false")

    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="输出目录")
    parser.add_argument("--filename-prefix", default="seedream", help="输出文件名前缀")
    parser.add_argument("--save-images", dest="save_images", action="store_true", default=True)
    parser.add_argument("--no-save-images", dest="save_images", action="store_false")
    parser.add_argument("--report-json", help="报告 JSON 路径（默认输出目录自动命名）")

    parser.add_argument("--timeout", type=int, default=180, help="HTTP 超时秒数")
    parser.add_argument("--dry-run", action="store_true", help="仅打印 payload，不调用 API")
    parser.add_argument(
        "--print-payload",
        action="store_true",
        help="打印最终请求 payload",
    )
    parser.add_argument(
        "--extra-json",
        help="额外 JSON 字段，合并到请求体（示例: '{\"foo\":\"bar\"}'）",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload: Dict[str, Any] = {
        "model": args.model,
        "prompt": args.prompt,
        "sequential_image_generation": args.sequential_image_generation,
        "sequential_image_generation_options": {
            "max_images": args.max_images,
        },
        "response_format": args.response_format,
        "size": args.size,
        "stream": bool(args.stream),
        "watermark": bool(args.watermark),
    }
    if args.image_url:
        payload["image"] = args.image_url

    if args.extra_json:
        try:
            extra_data = json.loads(args.extra_json)
            if not isinstance(extra_data, dict):
                raise ValueError("extra_json 必须是 JSON 对象")
            payload.update(extra_data)
        except Exception as exc:
            print(f"❌ --extra-json 解析失败: {exc}")
            return 1

    if args.print_payload or args.dry_run:
        print("[PAYLOAD]")
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    if args.dry_run:
        print("✅ dry-run 完成，未发起远端请求。")
        return 0

    api_key = args.api_key or _env_api_key()
    if not api_key:
        print("❌ 缺少 API Key。请设置 SEEDREAM_API_KEY / ARK_API_KEY / VOLCENGINE_ARK_API_KEY，或传 --api-key")
        return 1

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cfg = SeedreamConfig(
        api_key=api_key,
        api_url=args.api_url,
        model=args.model,
        timeout=args.timeout,
    )
    client = SeedreamClient(cfg)

    try:
        payloads, final_payload = client.generate(payload=payload, use_stream=bool(args.stream))
    except Exception as exc:
        diagnostic_hint = _diagnostic_hint(exc, payload, bool(args.stream))
        report_path = Path(args.report_json) if args.report_json else output_dir / f"seedream_report_{_now_stamp()}.json"
        report_path.write_text(
            json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "diagnostic_hint": diagnostic_hint,
                    "request": payload,
                    "stream": bool(args.stream),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"❌ 调用失败: {exc}")
        if diagnostic_hint:
            print(f"💡 诊断提示: {diagnostic_hint}")
        print(f"📝 已写入错误报告: {report_path}")
        return 2

    all_items = _merge_items(payloads)
    saved_files: List[str] = []
    event_types = [str(payload.get("type")) for payload in payloads if payload.get("type")]

    if not all_items:
        report = {
            "ok": False,
            "error": _empty_result_hint(payloads, final_payload),
            "request": payload,
            "result_count": 0,
            "results": [],
            "saved_files": [],
            "final_payload": final_payload,
            "stream_event_count": len(payloads),
            "stream_event_types": event_types,
        }
        report_path = Path(args.report_json) if args.report_json else output_dir / f"seedream_report_{_now_stamp()}.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"❌ 未提取到图片结果: {report['error']}")
        print(f"📝 报告: {report_path}")
        return 3

    if args.save_images:
        for idx, item in enumerate(all_items, start=1):
            prefix = _safe_name(args.filename_prefix)
            if item.get("url"):
                ext = _detect_ext_from_url(item["url"])
                out_path = output_dir / f"{prefix}_{idx:02d}{ext}"
                try:
                    _save_from_url(item["url"], out_path, args.timeout)
                    saved_files.append(str(out_path))
                    print(f"✅ 已保存: {out_path}")
                except Exception as exc:
                    print(f"⚠️ URL 下载失败: {item['url']} ({exc})")
            elif item.get("b64_json"):
                out_path = output_dir / f"{prefix}_{idx:02d}.png"
                try:
                    _save_from_b64(item["b64_json"], out_path)
                    saved_files.append(str(out_path))
                    print(f"✅ 已保存: {out_path}")
                except Exception as exc:
                    print(f"⚠️ Base64 解码失败: index={idx} ({exc})")

    report = {
        "ok": True,
        "request": payload,
        "result_count": len(all_items),
        "results": all_items,
        "saved_files": saved_files,
        "final_payload": final_payload,
        "stream_event_count": len(payloads),
        "stream_event_types": event_types,
    }
    report_path = Path(args.report_json) if args.report_json else output_dir / f"seedream_report_{_now_stamp()}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"🎯 成功: 共提取 {len(all_items)} 张结果")
    for i, item in enumerate(all_items, start=1):
        if item.get("url"):
            print(f"[{i}] {item['url']}")
    print(f"📝 报告: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
