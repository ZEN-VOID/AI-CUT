#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path


def _ensure_scripts_on_path() -> None:
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))


def test_resolve_project_root_prefers_cwd_project(tmp_path):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root

    project_root = tmp_path / "workspace"
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    (project_root / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    resolved = resolve_project_root(cwd=project_root)
    assert resolved == project_root.resolve()


def test_resolve_project_root_stops_at_git_root(tmp_path):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root

    repo_root = tmp_path / "repo"
    (repo_root / ".git").mkdir(parents=True, exist_ok=True)

    nested = repo_root / "sub" / "dir"
    nested.mkdir(parents=True, exist_ok=True)

    outside_project = tmp_path / "outside_project"
    (outside_project / ".webnovel").mkdir(parents=True, exist_ok=True)
    (outside_project / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    try:
        resolve_project_root(cwd=nested)
        assert False, "Expected FileNotFoundError when only parent outside git root has project"
    except FileNotFoundError:
        pass


def test_resolve_project_root_finds_default_subdir_within_git_root(tmp_path):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root

    repo_root = tmp_path / "repo"
    (repo_root / ".git").mkdir(parents=True, exist_ok=True)

    default_project = repo_root / "webnovel-project"
    (default_project / ".webnovel").mkdir(parents=True, exist_ok=True)
    (default_project / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    nested = repo_root / "sub" / "dir"
    nested.mkdir(parents=True, exist_ok=True)

    resolved = resolve_project_root(cwd=nested)
    assert resolved == default_project.resolve()


def test_resolve_project_root_finds_story_project_subdir_within_git_root(tmp_path):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root

    repo_root = tmp_path / "repo"
    (repo_root / ".git").mkdir(parents=True, exist_ok=True)

    default_project = repo_root / "story-project"
    (default_project / ".webnovel").mkdir(parents=True, exist_ok=True)
    (default_project / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    nested = repo_root / "sub" / "dir"
    nested.mkdir(parents=True, exist_ok=True)

    resolved = resolve_project_root(cwd=nested)
    assert resolved == default_project.resolve()


def test_resolve_project_root_uses_workspace_pointer(tmp_path):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root, write_current_project_pointer

    workspace = tmp_path / "workspace"
    (workspace / ".claude").mkdir(parents=True, exist_ok=True)

    project_root = workspace / "凡人资本论"
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    (project_root / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    pointer_file = write_current_project_pointer(project_root, workspace_root=workspace)
    assert pointer_file is not None
    assert pointer_file.is_file()

    resolved = resolve_project_root(cwd=workspace)
    assert resolved == project_root.resolve()


def test_resolve_project_root_ignores_stale_pointer_and_fallbacks(tmp_path):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root

    workspace = tmp_path / "workspace"
    (workspace / ".claude").mkdir(parents=True, exist_ok=True)
    # stale pointer
    (workspace / ".claude" / ".webnovel-current-project").write_text(
        str(workspace / "missing-project"), encoding="utf-8"
    )

    default_project = workspace / "webnovel-project"
    (default_project / ".webnovel").mkdir(parents=True, exist_ok=True)
    (default_project / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    resolved = resolve_project_root(cwd=workspace)
    assert resolved == default_project.resolve()


def test_resolve_project_root_reads_legacy_registry_and_migrates_to_story2026(tmp_path, monkeypatch):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root

    claude_root = tmp_path / ".claude-home"
    workspace = tmp_path / "workspace"
    project_root = workspace / "项目A"
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    (project_root / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    legacy_registry = claude_root / "webnovel-writer" / "workspaces.json"
    legacy_registry.parent.mkdir(parents=True, exist_ok=True)
    legacy_registry.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "workspaces": {
                    str(workspace.resolve()): {
                        "workspace_root": str(workspace.resolve()),
                        "current_project_root": str(project_root.resolve()),
                        "updated_at": "2026-04-07T00:00:00",
                    }
                },
                "last_used_project_root": str(project_root.resolve()),
                "updated_at": "2026-04-07T00:00:00",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("STORY2026_CLAUDE_HOME", str(claude_root))

    resolved = resolve_project_root(cwd=workspace)
    assert resolved == project_root.resolve()
    assert (claude_root / "story2026" / "workspaces.json").is_file()


def test_resolve_project_root_prefers_story_project_root_env(tmp_path, monkeypatch):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root

    project_root = tmp_path / "story-project"
    (project_root / ".webnovel").mkdir(parents=True, exist_ok=True)
    (project_root / ".webnovel" / "state.json").write_text("{}", encoding="utf-8")

    monkeypatch.setenv("STORY_PROJECT_ROOT", str(project_root))
    monkeypatch.delenv("WEBNOVEL_PROJECT_ROOT", raising=False)

    resolved = resolve_project_root(cwd=tmp_path)
    assert resolved == project_root.resolve()


def test_resolve_state_file_uses_state_manifest_runtime_path(tmp_path):
    _ensure_scripts_on_path()

    from project_locator import resolve_project_root, resolve_state_file

    project_root = tmp_path / "manifest-project"
    runtime_dir = project_root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    runtime_state = runtime_dir / "custom-state.json"
    runtime_state.write_text("{}", encoding="utf-8")
    (project_root / "STATE.json").write_text(
        json.dumps(
            {
                "schema_version": "story2026/project-state-manifest/v1",
                "paths": {"runtime_state": "runtime/custom-state.json"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resolved_root = resolve_project_root(cwd=project_root)
    resolved_state = resolve_state_file(cwd=project_root)

    assert resolved_root == project_root.resolve()
    assert resolved_state == runtime_state.resolve()
