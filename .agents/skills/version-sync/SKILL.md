---
name: version-sync
description: Maintain AI-CUT repository version display and detailed update history. Use when updating VERSION.md, preparing github-push version bumps, changing version hooks, migrating version automation, or recording release/update details for repository, workflow, Codex hook, documentation, project asset, or skill changes.
---

# Version Sync

## Purpose

Keep `VERSION.md` as a content display page, not a rules page. All deterministic version edits should go through `scripts/sync_version.py`.

## Workflow

1. Inspect the current repository changes when the user asks to sync, bump, repair, or review version records.
2. Choose a bump level:
   - `none`: refresh or record without incrementing.
   - `small`: documentation, prompts, validators, hooks, small compatible fixes.
   - `medium`: workflow capability expansion, output contract changes, visible behavior upgrades.
   - `large`: architecture changes, default behavior changes, cross-generation contract changes.
3. Run the script from the repository root:

```bash
python3 .agents/skills/version-sync/scripts/sync_version.py --level small
```

Use `--dry-run` before risky changes, and use repeated `--detail` flags when the automatic path-based summary is not specific enough:

```bash
python3 .agents/skills/version-sync/scripts/sync_version.py --level small --detail "说明本次具体更新内容"
```

Use `--scope` when the working tree contains unrelated user changes that should not be included in the version entry:

```bash
python3 .agents/skills/version-sync/scripts/sync_version.py --level small --scope "version-sync skill update / codex hook update"
```

## Hook Contract

Codex hooks should not write `VERSION.md` directly. Hook entrypoints should forward to `scripts/sync_version.py` and preserve the same arguments and stdin.

The script owns:

- current version detection and bumping;
- `最后更新` refresh;
- update entry insertion between `<!-- version-hook:history:start -->` and `<!-- version-hook:history:end -->`;
- path-based scope classification;
- detailed update bullet generation.

## Output Contract

Each new history entry should remain reader-facing:

- version change;
- update level;
- update scope;
- update method;
- concrete update details.

Do not move version rules back into the top of `VERSION.md`; keep maintenance notes short and below the update history.
