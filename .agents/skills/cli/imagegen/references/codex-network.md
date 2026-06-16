# Codex network approvals / sandbox notes

Status: deprecated/external reference. This file is not an execution route for `.agents/skills/cli/imagegen`.

Read it only when auditing legacy material or when a separate, explicitly named non-imagegen workflow asks for `scripts/image_gen.py` / CLI / API / model controls. This guidance is intentionally isolated from `SKILL.md` because it can vary by environment and may become stale.

## Why am I asked to approve image generation calls?
The external CLI uses the OpenAI Image API, so it needs outbound network access. `.agents/skills/cli/imagegen` does not use that path and must not request network/API-key setup as part of its normal execution.

## Important note about approvals vs network
- `--ask-for-approval never` suppresses approval prompts.
- It does **not** by itself enable network access.
- In `workspace-write`, network access still depends on your Codex configuration (for example `[sandbox_workspace_write] network_access = true`).

## How do I reduce repeated approval prompts?
If you trust the repo and want fewer prompts, use a configuration or profile that both:
- enables network for the sandbox mode you plan to use
- sets an approval policy that matches your risk tolerance

Example `~/.codex/config.toml` pattern:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

If you want quieter automation after network is enabled, you can choose a stricter approval policy, but do that intentionally and with care.

## Safety note
Enabling network and reducing approvals lowers friction, but increases risk if you run untrusted code or work in an untrusted repository.

## Review Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| Did network approval guidance remain external to this built-in-only skill? | Asking for sandbox/network/API setup during normal imagegen execution fails | `FAIL-IMG-ROUTE-UNSUPPORTED` | `SKILL.md#runtime-guardrails` / `references/codex-network.md` | final route note shows built-in mode or blocked non-built-in route |
