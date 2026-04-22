#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
story 统一入口（内部模块仍保留 `webnovel` 文件名以兼容旧导入）

设计目标：
- 只有一个入口命令，避免到处拼 `python -m data_modules.xxx ...` 导致参数位置/引号/路径炸裂。
- 自动解析正确的 book project_root（包含 `STATE.json` 的目录）。
- 所有写入类命令在解析到 project_root 后，统一前置 `--project-root` 传给具体模块。

典型用法（推荐，不依赖 PYTHONPATH / 不要求 cd）：
  python "<SCRIPTS_DIR>/story.py" preflight
  python "<SCRIPTS_DIR>/story.py" where
  python "<SCRIPTS_DIR>/story.py" use D:\\wk\\xiaoshuo\\凡人资本论
  python "<SCRIPTS_DIR>/story.py" --project-root D:\\wk\\xiaoshuo cards-write --data @cards_payload.json --run-gate --format json
  python "<SCRIPTS_DIR>/story.py" --project-root D:\\wk\\xiaoshuo index stats
  python "<SCRIPTS_DIR>/story.py" --project-root D:\\wk\\xiaoshuo state process-chapter --chapter 100 --data @payload.json
  python "<SCRIPTS_DIR>/story.py" --project-root D:\\wk\\xiaoshuo extract-context --chapter 100 --format json

也支持（不推荐，容易踩 PYTHONPATH/cd/参数顺序坑）：
  python -m data_modules.webnovel where
"""

from __future__ import annotations

import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

from runtime_compat import normalize_windows_path
from project_locator import resolve_project_root, write_current_project_pointer, update_global_registry_current_project

try:
    from planning_paths import (
        canonical_book_plan_path,
        canonical_book_plan_relpath,
        canonical_planning_artifact_relpath,
        legacy_planning_artifact_path,
        legacy_planning_artifact_relpath,
        resolve_planning_artifact_path,
    )
except ImportError:  # pragma: no cover
    from scripts.planning_paths import (
        canonical_book_plan_path,
        canonical_book_plan_relpath,
        canonical_planning_artifact_relpath,
        legacy_planning_artifact_path,
        legacy_planning_artifact_relpath,
        resolve_planning_artifact_path,
    )


def _scripts_dir() -> Path:
    # data_modules/webnovel.py -> data_modules -> scripts
    return Path(__file__).resolve().parent.parent


def _resolve_root(explicit_project_root: Optional[str]) -> Path:
    # 允许显式传入工作区根目录或书项目根目录
    raw = explicit_project_root
    if raw:
        return resolve_project_root(raw)
    return resolve_project_root()


def _strip_project_root_args(argv: list[str]) -> list[str]:
    """
    下游工具统一由本入口注入 `--project-root`，避免重复传参导致 argparse 报错/歧义。
    """
    out: list[str] = []
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok == "--project-root":
            i += 2
            continue
        if tok.startswith("--project-root="):
            i += 1
            continue
        out.append(tok)
        i += 1
    return out


def _run_data_module(module: str, argv: list[str]) -> int:
    """
    Import `data_modules.<module>` and call its main(), while isolating sys.argv.
    """
    mod = importlib.import_module(f"data_modules.{module}")
    main = getattr(mod, "main", None)
    if not callable(main):
        raise RuntimeError(f"data_modules.{module} 缺少可调用的 main()")

    old_argv = sys.argv
    try:
        sys.argv = [f"data_modules.{module}"] + argv
        try:
            main()
            return 0
        except SystemExit as e:
            return int(e.code or 0)
    finally:
        sys.argv = old_argv


def _run_script(script_name: str, argv: list[str]) -> int:
    """
    Run a script under the story2026 `scripts/` directory via a subprocess.

    用途：兼容没有 main() 的脚本（例如 workflow_manager.py）。
    """
    script_path = _scripts_dir() / script_name
    if not script_path.is_file():
        raise FileNotFoundError(f"未找到脚本: {script_path}")
    proc = subprocess.run([sys.executable, str(script_path), *argv])
    return int(proc.returncode or 0)


def cmd_where(args: argparse.Namespace) -> int:
    root = _resolve_root(args.project_root)
    print(str(root))
    return 0


def _detect_planning_source(project_root: Path) -> dict[str, str]:
    book_plan_path = canonical_book_plan_path(project_root)
    holomap_path = resolve_planning_artifact_path(project_root, "holomap")
    legacy_holomap_path = legacy_planning_artifact_path(project_root, "holomap")
    legacy_outline_path = project_root / "2-Planning" / "legacy" / "总纲.md"

    if book_plan_path.is_file():
        return {
            "status": "canonical",
            "label": "OK",
            "path": str(book_plan_path),
            "detail": f"默认规划真源：{canonical_book_plan_relpath()}",
        }
    if holomap_path.is_file():
        detail = f"默认规划真源：{canonical_planning_artifact_relpath('holomap')}"
        if holomap_path == legacy_holomap_path:
            detail += f"（当前命中 legacy fallback：{legacy_planning_artifact_relpath('holomap')}）"
        return {
            "status": "compatibility_fallback",
            "label": "WARN",
            "path": str(holomap_path),
            "detail": f"未检测到 {canonical_book_plan_relpath()}，当前回退到兼容规划真源：{detail}",
        }
    if legacy_outline_path.is_file():
        return {
            "status": "legacy_fallback",
            "label": "WARN",
            "path": str(legacy_outline_path),
            "detail": "仅检测到 2-Planning/legacy/总纲.md，尚未切到新的三层规划真源",
        }
    return {
        "status": "missing",
        "label": "INFO",
        "path": str(book_plan_path),
        "detail": f"尚未生成规划真源；完成 2-Planning 后应落盘 {canonical_book_plan_relpath()}",
    }


def _build_preflight_report(explicit_project_root: Optional[str]) -> dict:
    scripts_dir = _scripts_dir().resolve()
    plugin_root = scripts_dir.parent
    skill_root = plugin_root / "3-Drafting"
    entry_script = scripts_dir / "story.py"
    legacy_entry_script = scripts_dir / "webnovel.py"
    extract_script = scripts_dir / "extract_chapter_context.py"

    checks: list[dict[str, object]] = [
        {"name": "scripts_dir", "ok": scripts_dir.is_dir(), "path": str(scripts_dir)},
        {"name": "entry_script", "ok": entry_script.is_file(), "path": str(entry_script)},
        {"name": "legacy_entry_alias", "ok": legacy_entry_script.is_file(), "path": str(legacy_entry_script)},
        {"name": "extract_context_script", "ok": extract_script.is_file(), "path": str(extract_script)},
        {"name": "skill_root", "ok": skill_root.is_dir(), "path": str(skill_root)},
    ]

    project_root = ""
    project_root_error = ""
    planning_source = {
        "status": "unknown",
        "label": "INFO",
        "path": "",
        "detail": "尚未解析 project_root",
    }
    try:
        resolved_root = _resolve_root(explicit_project_root)
        project_root = str(resolved_root)
        checks.append({"name": "project_root", "ok": True, "path": project_root})
        planning_source = _detect_planning_source(resolved_root)
        planning_ok = planning_source["status"] == "canonical"
        checks.append(
            {
                "name": "planning_source",
                "ok": planning_ok,
                "path": planning_source["path"],
                "status_label": planning_source["label"],
                "detail": planning_source["detail"],
                "planning_status": planning_source["status"],
            }
        )
    except Exception as exc:
        project_root_error = str(exc)
        checks.append({"name": "project_root", "ok": False, "path": explicit_project_root or "", "error": project_root_error})

    return {
        "ok": all(bool(item["ok"]) for item in checks),
        "project_root": project_root,
        "scripts_dir": str(scripts_dir),
        "skill_root": str(skill_root),
        "checks": checks,
        "project_root_error": project_root_error,
        "planning_source": planning_source,
    }


def cmd_preflight(args: argparse.Namespace) -> int:
    report = _build_preflight_report(args.project_root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in report["checks"]:
            status = str(item.get("status_label") or ("OK" if item["ok"] else "ERROR"))
            path = item.get("path") or ""
            print(f"{status} {item['name']}: {path}")
            if item.get("detail"):
                print(f"  detail: {item['detail']}")
            if item.get("error"):
                print(f"  detail: {item['error']}")
    return 0 if report["ok"] else 1


def cmd_use(args: argparse.Namespace) -> int:
    project_root = normalize_windows_path(args.project_root).expanduser()
    try:
        project_root = project_root.resolve()
    except Exception:
        project_root = project_root

    workspace_root: Optional[Path] = None
    if args.workspace_root:
        workspace_root = normalize_windows_path(args.workspace_root).expanduser()
        try:
            workspace_root = workspace_root.resolve()
        except Exception:
            workspace_root = workspace_root

    # 1) 写入工作区指针（若工作区内存在 `.claude/`）
    pointer_file = write_current_project_pointer(project_root, workspace_root=workspace_root)
    if pointer_file is not None:
        print(f"workspace pointer: {pointer_file}")
    else:
        print("workspace pointer: (skipped)")

    # 2) 写入用户级 registry（保证全局安装/空上下文可恢复）
    reg_path = update_global_registry_current_project(workspace_root=workspace_root, project_root=project_root)
    if reg_path is not None:
        print(f"global registry: {reg_path}")
    else:
        print("global registry: (skipped)")

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="story unified CLI")
    parser.add_argument("--project-root", help="书项目根目录或工作区根目录（可选，默认自动检测）")

    sub = parser.add_subparsers(dest="tool", required=True)

    p_where = sub.add_parser("where", help="打印解析出的 project_root")
    p_where.set_defaults(func=cmd_where)

    p_preflight = sub.add_parser("preflight", help="校验统一 CLI 运行环境与 project_root")
    p_preflight.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    p_preflight.set_defaults(func=cmd_preflight)

    p_cards_check = sub.add_parser("cards-check", help="校验 1-Cards 的覆盖率与结构完整性")
    p_cards_check.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    p_cards_write = sub.add_parser("cards-write", help="写入 1-Cards 正式 JSON 产物并补齐 trace 字段")
    p_cards_write.add_argument("--data", required=True, help="cards payload，支持 JSON 字符串或 @payload.json")
    p_cards_write.add_argument("--run-gate", action="store_true", help="写入后立即执行 cards-check 并回填 gate_summary")
    p_cards_write.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")

    p_use = sub.add_parser("use", help="绑定当前工作区使用的书项目（写入指针/registry）")
    p_use.add_argument("project_root", help="书项目根目录（必须包含 STATE.json）")
    p_use.add_argument("--workspace-root", help="工作区根目录（可选；默认由运行环境推断）")
    p_use.set_defaults(func=cmd_use)

    # Pass-through to data modules
    p_index = sub.add_parser("index", help="转发到 index_manager")
    p_index.add_argument("args", nargs=argparse.REMAINDER)

    p_state = sub.add_parser("state", help="转发到 state_manager")
    p_state.add_argument("args", nargs=argparse.REMAINDER)

    p_rag = sub.add_parser("rag", help="转发到 rag_adapter")
    p_rag.add_argument("args", nargs=argparse.REMAINDER)

    p_style = sub.add_parser("style", help="转发到 style_sampler")
    p_style.add_argument("args", nargs=argparse.REMAINDER)

    p_entity = sub.add_parser("entity", help="转发到 entity_linker")
    p_entity.add_argument("args", nargs=argparse.REMAINDER)

    p_context = sub.add_parser("context", help="转发到 context_manager")
    p_context.add_argument("args", nargs=argparse.REMAINDER)

    p_migrate = sub.add_parser("migrate", help="转发到 migrate_state_to_sqlite")
    p_migrate.add_argument("args", nargs=argparse.REMAINDER)

    # Pass-through to scripts
    p_workflow = sub.add_parser("workflow", help="转发到 workflow_manager.py")
    p_workflow.add_argument("args", nargs=argparse.REMAINDER)

    p_status = sub.add_parser("status", help="转发到 status_reporter.py")
    p_status.add_argument("args", nargs=argparse.REMAINDER)

    p_update_state = sub.add_parser("update-state", help="转发到 update_state.py")
    p_update_state.add_argument("args", nargs=argparse.REMAINDER)

    p_loopback = sub.add_parser("loopback", help="转发到 loopback_manager.py")
    p_loopback.add_argument("args", nargs=argparse.REMAINDER)

    p_init = sub.add_parser("init", help="转发到 init_project.py（初始化项目）")
    p_init.add_argument("args", nargs=argparse.REMAINDER)

    p_extract_context = sub.add_parser("extract-context", help="转发到 extract_chapter_context.py")
    p_extract_context.add_argument("--chapter", type=int, required=True, help="目标章节号")
    p_extract_context.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    p_extract_context.add_argument("--step-id", help="当前 drafting step_id，可选")

    p_validate = sub.add_parser("validate", help="转发到 validation_runner.py")
    p_validate.add_argument("args", nargs=argparse.REMAINDER)

    p_drafting_guard = sub.add_parser("drafting-guard", help="转发到 drafting_manuscript_guard.py")
    p_drafting_guard.add_argument("--chapter", type=int, help="目标章节号")
    p_drafting_guard.add_argument("--manuscript", help="显式正文路径")
    p_drafting_guard.add_argument("--planning", help="显式 planning 章路径")
    p_drafting_guard.add_argument("--min-body-chars", type=int, help="最小正文字符数")
    p_drafting_guard.add_argument("--min-paragraphs", type=int, help="最小段落数")

    p_drafting_volume_guard = sub.add_parser("drafting-volume-guard", help="转发到 drafting_volume_quality_guard.py")
    p_drafting_volume_guard.add_argument("--volume", type=int, help="目标卷号")
    p_drafting_volume_guard.add_argument("--write-log", help="显式卷级写作日志路径")

    # 兼容：允许 `--project-root` 出现在任意位置（减少 agents/skills 拼命令的出错率）
    from .cli_args import normalize_global_project_root

    argv = normalize_global_project_root(sys.argv[1:])
    args = parser.parse_args(argv)

    # where/use 直接执行
    if hasattr(args, "func"):
        code = int(args.func(args) or 0)
        raise SystemExit(code)

    tool = args.tool
    rest = list(getattr(args, "args", []) or [])
    # argparse.REMAINDER 可能以 `--` 开头占位，这里去掉
    if rest[:1] == ["--"]:
        rest = rest[1:]
    rest = _strip_project_root_args(rest)

    # init 是创建项目，不应该依赖/注入已存在 project_root
    if tool == "init":
        raise SystemExit(_run_script("init_project.py", rest))

    # 其余工具：统一解析 project_root 后前置给下游
    project_root = _resolve_root(args.project_root)
    forward_args = ["--project-root", str(project_root)]

    if tool == "index":
        raise SystemExit(_run_data_module("index_manager", [*forward_args, *rest]))
    if tool == "state":
        raise SystemExit(_run_data_module("state_manager", [*forward_args, *rest]))
    if tool == "rag":
        raise SystemExit(_run_data_module("rag_adapter", [*forward_args, *rest]))
    if tool == "style":
        raise SystemExit(_run_data_module("style_sampler", [*forward_args, *rest]))
    if tool == "entity":
        raise SystemExit(_run_data_module("entity_linker", [*forward_args, *rest]))
    if tool == "context":
        raise SystemExit(_run_data_module("context_manager", [*forward_args, *rest]))
    if tool == "migrate":
        raise SystemExit(_run_data_module("migrate_state_to_sqlite", [*forward_args, *rest]))

    if tool == "workflow":
        raise SystemExit(_run_script("workflow_manager.py", [*forward_args, *rest]))
    if tool == "status":
        raise SystemExit(_run_script("status_reporter.py", [*forward_args, *rest]))
    if tool == "update-state":
        raise SystemExit(_run_script("update_state.py", [*forward_args, *rest]))
    if tool == "loopback":
        raise SystemExit(_run_script("loopback_manager.py", [*forward_args, *rest]))
    if tool == "cards-check":
        raise SystemExit(_run_script("cards_coverage_validator.py", [*forward_args, "--format", str(args.format)]))
    if tool == "cards-write":
        write_args = [*forward_args, "--data", str(args.data), "--format", str(args.format)]
        if args.run_gate:
            write_args.append("--run-gate")
        raise SystemExit(_run_script("cards_writer.py", write_args))
    if tool == "extract-context":
        return_args = [*forward_args, "--chapter", str(args.chapter), "--format", str(args.format)]
        if getattr(args, "step_id", None):
            return_args.extend(["--step-id", str(args.step_id)])
        raise SystemExit(_run_script("extract_chapter_context.py", return_args))
    if tool == "validate":
        raise SystemExit(_run_script("validation_runner.py", [*forward_args, *rest]))
    if tool == "drafting-guard":
        guard_args = [*forward_args]
        if getattr(args, "chapter", None) is not None:
            guard_args.extend(["--chapter", str(args.chapter)])
        if getattr(args, "manuscript", None):
            guard_args.extend(["--manuscript", str(args.manuscript)])
        if getattr(args, "planning", None):
            guard_args.extend(["--planning", str(args.planning)])
        if getattr(args, "min_body_chars", None) is not None:
            guard_args.extend(["--min-body-chars", str(args.min_body_chars)])
        if getattr(args, "min_paragraphs", None) is not None:
            guard_args.extend(["--min-paragraphs", str(args.min_paragraphs)])
        raise SystemExit(_run_script("drafting_manuscript_guard.py", guard_args))
    if tool == "drafting-volume-guard":
        guard_args = [*forward_args]
        if getattr(args, "volume", None) is not None:
            guard_args.extend(["--volume", str(args.volume)])
        if getattr(args, "write_log", None):
            guard_args.extend(["--write-log", str(args.write_log)])
        raise SystemExit(_run_script("drafting_volume_quality_guard.py", guard_args))

    raise SystemExit(2)


if __name__ == "__main__":
    main()
