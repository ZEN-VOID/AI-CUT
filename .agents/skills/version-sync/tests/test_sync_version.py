from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import sync_version  # noqa: E402


def test_update_text_adds_detailed_entry() -> None:
    source = """# AI-VCR 版本记录

当前版本：`V1.0.2`
最后更新：2026-07-03 03:51 UTC

## 更新明细

<!-- version-hook:history:start -->
### V1.0.2 - old
<!-- version-hook:history:end -->
"""
    summary = sync_version.ChangeSummary(
        "version-sync skill update / docs update",
        ["更新版本同步技能包。"],
    )

    updated = sync_version.update_text(
        source,
        "V1.0.2",
        "V1.0.3",
        "small",
        "2026-07-03 06:00 UTC",
        summary,
        [],
    )

    assert "当前版本：`V1.0.3`" in updated
    assert "最后更新：2026-07-03 06:00 UTC" in updated
    assert "### V1.0.3 - 2026-07-03 06:00 UTC" in updated
    assert "- 更新范围：version-sync skill update / docs update" in updated
    assert "- 更新方式：version-sync 自动同步" in updated
    assert "  - 更新版本同步技能包。" in updated


def test_summarize_changes_classifies_paths() -> None:
    summary = sync_version.summarize_changes(
        [
            ".agents/skills/version-sync/SKILL.md",
            ".codex/hooks/update_version_for_github_push.py",
            "VERSION.md",
        ]
    )

    assert summary.scope == "version-sync skill update / codex hook update / docs update / repository config update"
    assert any("版本同步技能包" in detail for detail in summary.details)
    assert any("Codex 钩子" in detail for detail in summary.details)
