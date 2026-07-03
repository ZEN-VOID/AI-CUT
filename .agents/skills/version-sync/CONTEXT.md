# version-sync Context

- `VERSION.md` is a reader-facing version page. It should show current content and update details first.
- `.codex/hooks/update_version_for_github_push.py` is only an entrypoint and must not contain the version mutation logic.
- The canonical implementation is `.agents/skills/version-sync/scripts/sync_version.py`.
