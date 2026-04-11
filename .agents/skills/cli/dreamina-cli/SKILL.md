---
name: dreamina-cli
description: Use when Codex needs to install Dreamina CLI, complete Dreamina browser/headless/manual-import login, self-check with dreamina user_credit, or submit and follow up Dreamina generation tasks from terminal workflows, especially for text2image, text2video, image2image, image2video, list_task, and query_result.
governance_tier: lite
---

# Dreamina CLI

## Overview

Use Dreamina CLI as the terminal entrypoint for Dreamina login, balance self-check, async task submission, result querying, task review, and queue-ledger maintenance for pending video/image jobs.

Treat this as a reliability-first CLI skill:
- confirm the binary exists
- confirm login works with `dreamina user_credit`
- submit with `--poll` when immediate feedback helps
- fall back to `dreamina query_result --submit_id=...`
- treat pending jobs as a maintained queue, not as terminal scrollback
- inspect local config and credential files only when auth or environment fails

## Governance Tier

- `lite`

## Core Workflow

1. Identify the task type:
   - install or verify CLI
   - login / relogin / logout
   - import login JSON from another machine
   - self-check balance
   - submit generation
   - choose the right generation command: `text2video` / `image2video` / `multimodal2video` / `multiframe2video`
   - query an async result
   - inspect prior tasks
   - create or refresh a manual queue ledger
2. Before any generation command, run `dreamina user_credit`.
3. If the task is async, multi-item, or likely to outlive the current shell session, create or reopen a queue ledger from [templates/task-queue.template.md](./templates/task-queue.template.md).
4. If the command needs local input media, verify the file path exists before submission.
5. Resolve the output root before submission:
   - standalone Dreamina runs default to `output/dreamina/<项目名>/`
   - downloaded media default to `output/dreamina/<项目名>/<模型名称>/`
   - queue ledgers default to `output/dreamina/<项目名>/`
   - when this skill is invoked by `.agents/skills/aigc2026/...`, follow the caller skill's canonical AIGC2026 output contract instead of forcing the standalone Dreamina path
6. Prefer `--poll=<seconds>` on the first submit when the user wants quick feedback.
7. Immediately after submission, write one queue row per submitted asset or job with `submit_id`, task type, prompt summary, current status, and next check action.
8. If polling times out, keep the returned `submit_id`, mark the ledger row as `querying` or `queued`, and switch to `dreamina query_result`.
9. If `query_result --download_dir=...` times out after the remote task is already `success`, treat it as a download-layer failure instead of a generation failure:
   - preserve `submit_id`
   - verify whether a partial local media file was written
   - delete the partial file before retrying the download
   - retry `query_result --download_dir=...`
   - if repeated timeouts persist, capture the `video_url` or `image_url` from `query_result` and finish the download with a direct HTTP client
10. Every later `query_result` or `list_task` check must manually update the queue ledger rather than relying on memory or chat history.
11. If login or permissions fail, inspect the local Dreamina files in the troubleshooting order defined below.

## Command Map

| Scenario | Preferred command | Notes |
| --- | --- | --- |
| Install CLI | `curl -fsSL https://jimeng.jianying.com/cli \| bash` | Installer usually places `dreamina` under `~/.local/bin/` |
| Verify install | `dreamina --help` | Use this before assuming PATH is correct |
| Browser login | `dreamina login` | Default path when the machine can open a browser |
| Headless login | `dreamina login --headless` | Prefer for agent or remote flows; Linux needs `google-chrome` / `google-chrome-stable` |
| Login debug | `dreamina login --debug` | Use when browser callback or login flow gets stuck |
| Re-login | `dreamina relogin` | Clears the old local credential first |
| Manual import login | `dreamina import_login_response --file /path/to/login.json` | Also supports piping JSON through stdin |
| Self-check | `dreamina user_credit` | Must return JSON before generation commands |
| View task list | `dreamina list_task --gen_status=success` | Also supports `--submit_id`, `--limit`, `--offset` |
| Query one task | `dreamina query_result --submit_id=<id>` | Add `--download_dir=...` to download result media |
| Review active queue | `dreamina list_task --limit=20` | Use with the local queue ledger to reconcile pending tasks |
| Refresh one queue row | `dreamina query_result --submit_id=<id>` | Manual update should rewrite `last_checked_at`, `remote_status`, and `next_action` |
| Multimodal video | `dreamina multimodal2video --image <ref1> --image <ref2> ...` | Best fit when the prompt must bind to multiple reference images and `@图N` style mapping |
| Multi-image story video | `dreamina multiframe2video --images a.png,b.png,...` | Best fit for 2-20 ordered keyframes; 3+ images need one `--transition-prompt` per segment |

## Current Video Model Matrix

Verified on `2026-04-03` against local official CLI build `4946b9d` (`build_time: 2026-03-31T07:24:44Z`) via `dreamina <subcommand> -h`.

| Subcommand | Current official `model_version` exposure | Notes |
| --- | --- | --- |
| `dreamina text2video` | `seedance2.0`, `seedance2.0fast` | Default is `seedance2.0fast`; `720p`; duration `4-15s` |
| `dreamina multimodal2video` | `seedance2.0`, `seedance2.0fast` | Current CLI only exposes the Seedance 2.0 family here |
| `dreamina image2video` | `3.0`, `3.0fast`, `3.0pro`, `3.0_fast`, `3.0_pro`, `3.5pro`, `3.5_pro`, `seedance2.0`, `seedance2.0fast` | This is the broadest current video-model surface in the CLI |
| `dreamina multiframe2video` | no `--model_version` flag | This command does not expose model switching |

Practical implication:
- Do not assume all video commands share the same model set.
- `seedance1.5pro` is not exposed in the current official CLI help for these video subcommands.
- If the user asks for `3.5pro`, route to `image2video`, not `text2video` or `multimodal2video`.

## Submission Patterns

### Text to image

```bash
dreamina text2image \
  --prompt="一只戴墨镜的橘猫" \
  --ratio=1:1 \
  --resolution_type=2k \
  --poll=30
```

### Text to video

```bash
dreamina text2video \
  --prompt="镜头推进，一只橘猫从沙发上跳下来" \
  --duration=5 \
  --ratio=16:9 \
  --video_resolution=720p \
  --poll=30
```

### Image to image

```bash
dreamina image2image \
  --images ./input.png \
  --prompt="改成水彩风格" \
  --resolution_type=2k \
  --poll=30
```

### Image to video

```bash
dreamina image2video \
  --image ./first_frame.png \
  --prompt="镜头慢慢推近" \
  --duration=5 \
  --poll=30
```

### Multimodal to video

```bash
dreamina multimodal2video \
  --image ./ref-1.png \
  --image ./ref-2.png \
  --prompt="@图1 为角色身份锚点，@图2 为场景锚点；保持两者一致性，镜头缓慢推进" \
  --model_version=seedance2.0 \
  --duration=15 \
  --ratio=16:9 \
  --video_resolution=720p \
  --poll=45
```

### Multi-frame story to video

```bash
dreamina multiframe2video \
  --images ./a.png,./b.png,./c.png \
  --transition-prompt="从A平滑过渡到B" \
  --transition-prompt="从B平滑过渡到C" \
  --transition-duration=3 \
  --transition-duration=3 \
  --poll=45
```

### Async follow-up

```bash
dreamina query_result --submit_id=<your_submit_id>
dreamina query_result --submit_id=<your_submit_id> --download_dir=output/dreamina/<项目名>/<模型名称>/
dreamina list_task --gen_status=success
```

## Queue Management

Pending Dreamina work must be tracked as a queue when any of these are true:
- there are multiple submitted jobs
- a video job is still pending after `--poll`
- the task needs to survive terminal/session interruption
- the user explicitly wants a checklist-style progress board

### Recommended ledger location

Use progressive convergence when choosing the queue file path:
1. Base range:
   - for standalone Dreamina runs, prefer `output/dreamina/<项目名>/`
   - if the task is invoked by `.agents/skills/aigc2026/...`, prefer the caller skill's canonical AIGC2026 output location and do not rewrite it back to `output/dreamina/`
2. Narrowing:
   - if the ledger is episode-scoped, include `第N集`
   - if the ledger is batch-scoped, include the batch topic or date
3. Final selection:
   - choose one concrete markdown file, usually `<YYYYMMDD>-<topic>-dreamina-queue.md`

### Default output paths

- Standalone queue ledger root: `output/dreamina/<项目名>/`
- Standalone queue ledger file: `output/dreamina/<项目名>/<YYYYMMDD>-<topic>-dreamina-queue.md`
- Standalone downloaded assets root: `output/dreamina/<项目名>/<模型名称>/`
- If the caller is an AIGC2026 downstream skill, the queue file and downloaded assets must obey that skill's stage output rule even when Dreamina is the transport layer.

### Minimum queue record

Each queue row should preserve at least:
- `queue_id`: local stable ID for manual tracking
- `asset_kind`: `video`, `image`, or other output kind
- `task_type`: `text2video`, `image2video`, `text2image`, `image2image`, etc.
- `submit_id`: Dreamina async identifier
- `local_status`: local workflow state such as `submitted`, `querying`, `downloaded`, `manual_hold`
- `remote_status`: remote task state from `query_result` / `list_task`, such as `queued`, `running`, `success`, `failed`
- `created_at`
- `last_checked_at`
- `next_action`: what to do next, not just the latest status
- `prompt_summary` and key input path(s)

### Manual dynamic update rules

- Do not silently delete finished or failed rows; move them from active queue to history or mark them closed.
- Every status refresh must update `last_checked_at`.
- If `--poll` timed out and no final result exists, queue status must not be marked complete.
- If `submit_id` is missing, the row is considered non-runnable and must be backfilled before follow-up.
- `dreamina list_task` and `~/.dreamina_cli/tasks.db` are evidence sources, but the markdown queue ledger is the manual operational source of truth for the current batch.
- If multiple outputs are produced from one creative brief, split them into multiple rows unless the user explicitly wants them grouped.
- If no explicit override exists, downloaded assets should land under `output/dreamina/<项目名>/<模型名称>/`, not in ad hoc `./downloads/`.
- If the job is delegated from an `aigc2026` skill, inherit that downstream stage path and record the inherited target path in the queue ledger.
- If `query_result --download_dir=...` leaves a partial file behind after timeout, that partial file is invalid operational state and should be removed before retrying, otherwise later verification may read a truncated asset as if it were complete.

## Non-Obvious Command Constraints

- `dreamina text2image`
  - omit `--model_version` or `--resolution_type` to use model defaults
  - `3.0` / `3.1` support `1k` or `2k`
  - `4.0` / `4.1` / `4.5` / `4.6` / `5.0` / `lab` support `2k` or `4k`
- `dreamina text2video`
  - current official `model_version` values: `seedance2.0`, `seedance2.0fast`
  - default model is `seedance2.0fast`
  - duration range is `4-15` seconds
  - video resolution is currently `720p` only
  - some high-safety models may require web-side compliance confirmation first
- `dreamina image2image`
  - `--images` accepts one or more local file paths
  - `1k` is not supported
- `dreamina image2video`
  - `--image` accepts one local first-frame path
  - current official `model_version` values: `3.0`, `3.0fast`, `3.0pro`, `3.0_fast`, `3.0_pro`, `3.5pro`, `3.5_pro`, `seedance2.0`, `seedance2.0fast`
  - ratio is inferred from the input image instead of being passed as a flag
- `dreamina multimodal2video`
  - best fit when multiple reference images must be uploaded together and the prompt needs to name them as `@图N`
  - at least one `--image` or `--video` is required
  - image input count is limited to `<=9`
  - current official `model_version` values: `seedance2.0`, `seedance2.0fast`
- `dreamina multiframe2video`
  - accepts `2-20` ordered images
  - for exactly 2 images, use shorthand `--prompt` and optional `--duration`
  - for 3+ images, provide one `--transition-prompt` per transition segment
  - this command does not expose `--model_version` or `--video_resolution` overrides
- `dreamina import_login_response`
  - use a local file or stdin pipe for the full JSON body
  - do not rely on long chat pastes because they are easy to truncate
- For the latest flag set, run `dreamina <subcommand> -h` instead of guessing.

## Lite Field Contract

| field_id | 通过标准 | fail_code | rework_entry |
| --- | --- | --- | --- |
| `FIELD-DRM-01` | `dreamina --help` succeeds and the binary is callable from the current shell | `FAIL-DRM-INSTALL` | Re-run install flow, then verify PATH and binary location |
| `FIELD-DRM-02` | `dreamina user_credit` returns valid JSON, or a valid login / relogin / import flow is completed first | `FAIL-DRM-AUTH` | Use login decision path, then inspect `config.toml` and `credential.json` |
| `FIELD-DRM-03` | The chosen generation subcommand matches the task type and required arguments are present | `FAIL-DRM-SUBMIT` | Re-check the command map and subcommand `-h` output |
| `FIELD-DRM-04` | Async tasks use `--poll` appropriately or preserve `submit_id` for `query_result` follow-up | `FAIL-DRM-ASYNC` | Re-run with `--poll` or switch to explicit query flow |
| `FIELD-DRM-05` | Local image paths exist before upload commands run | `FAIL-DRM-INPUT` | Verify file existence and correct local path |
| `FIELD-DRM-06` | When auth or environment breaks, local Dreamina files are inspected in the defined order | `FAIL-DRM-DIAG` | Follow the troubleshooting sequence below |
| `FIELD-DRM-07` | Pending or multi-item tasks are written into a queue ledger with stable `submit_id`, status, and next-action fields | `FAIL-DRM-QUEUE-MISSING` | Create or repair the queue ledger from the template, then backfill rows from CLI evidence |
| `FIELD-DRM-08` | Every later poll/query/list refresh updates the queue ledger manually instead of relying on chat memory | `FAIL-DRM-QUEUE-DRIFT` | Reconcile the ledger against `query_result`, `list_task`, and local logs/tasks.db |
| `FIELD-DRM-09` | Standalone downloads and queue files land under the default Dreamina path, while AIGC2026 downstream calls obey the caller's stage output rule | `FAIL-DRM-OUTPUT-PATH` | Re-resolve path ownership, then move or re-record files under the correct root |
| `FIELD-DRM-10` | A remote-success task that times out during `--download_dir` follow-up is retried as a download failure, with partial files removed before retry or direct-URL fallback | `FAIL-DRM-DOWNLOAD-TIMEOUT` | Remove partial output, retry `query_result --download_dir`, then fall back to direct HTTP download from the returned media URL if needed |

## Login Decision Path

1. If the current machine can open a browser, run `dreamina login`.
2. If the agent is operating remotely or without an interactive browser, prefer `dreamina login --headless`.
3. If the login page or callback appears stuck, retry with `dreamina login --debug`.
4. If login must happen on another machine, complete the browser flow there and import the full JSON with:
   - `dreamina import_login_response --file /path/to/dreamina-login.json`
   - or `cat /path/to/dreamina-login.json | dreamina import_login_response`
5. After any login path, run `dreamina user_credit` as the required self-check.

## Troubleshooting Order

1. Check `dreamina --help` to confirm the binary is callable.
2. Run `dreamina user_credit`.
3. If `user_credit` fails, inspect:
   - `~/.dreamina_cli/config.toml`
   - `~/.dreamina_cli/credential.json`
   - `~/.dreamina_cli/tasks.db`
   - `~/.dreamina_cli/logs/`
4. If login looked successful but generation still fails, do not trust the session until `dreamina user_credit` returns JSON.
5. If an async task does not finish within the polling window, capture `submit_id` and switch to `dreamina query_result`.
6. If more than one async task remains pending, open or create the queue ledger and reconcile it against `list_task`, `query_result`, and `tasks.db`.
7. If `query_result --download_dir=...` times out after the task is already `success`, inspect the target directory for a partial file, delete the partial file, retry the download, and if necessary switch to direct URL download using the returned media URL.
8. If outputs landed in the wrong directory, first decide whether this was a standalone Dreamina run or an AIGC2026 downstream invocation, then relocate or rewrite the ledger path accordingly.

## Common Mistakes

- Jumping straight to generation without running `dreamina user_credit`
- Forgetting to keep the `submit_id` when polling times out
- Letting pending tasks live only in terminal scrollback instead of a queue ledger
- Updating `query_result` in the terminal but forgetting to sync `last_checked_at` and `next_action`
- Downloading media into temporary `./downloads/` paths when the batch already has a project/model destination
- Treating a `--download_dir` timeout as if the generation itself failed, or keeping a truncated partial MP4/PNG in place and mistaking it for a valid output
- Using standalone `output/dreamina/...` paths inside an AIGC2026 downstream call that already has its own stage output contract
- Passing a non-existent local image path to `image2image` or `image2video`
- Using `image2video` when the task actually needs multiple reference images bound together; prefer `multimodal2video` for `@图N`-style all-around references
- Using `multiframe2video` for a multi-reference editing job that really needs Seedance 2.0 multimodal control; prefer `multiframe2video` for ordered story frames, not general reference binding
- Using `--headless` without the required Chrome dependency in remote environments
- Pasting a long manual-import login JSON through chat instead of a local file or stdin pipe

## Root-Cause Contract

When Dreamina CLI fails, trace upward in this order:

`Symptom/Failure`
-> `Direct Cause`: binary missing, PATH not updated, login callback stuck, credential invalid, local input path missing, async task still pending
-> `规则源`: this `SKILL.md`, `references/official-doc.md`, and the current `dreamina <subcommand> -h` output
-> `规则源的规则源`: repository `AGENTS.md` root-cause, field-centric, and context-deposition rules
-> `Fix Landing Points`: installation path, login flow selection, self-check sequencing, async follow-up sequencing, troubleshooting order

User-facing closure should include:
- root cause location
- immediate fix
- systemic prevention fix

## Resources

- Read [official-doc.md](./references/official-doc.md) for the condensed official guidance, FAQ, and local file semantics.
- Use [task-queue.template.md](./templates/task-queue.template.md) when a pending-job ledger is needed.
