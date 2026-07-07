# Changelog: workflow

## 2026-07-07

- Changed the default social-ad visual contract: workflow no longer enables 大字报 / `editorial_overlay` or 画中画 / `semantic_pip` by default; those layers are opt-in only when the user explicitly asks for them.
- Updated `validate_visual_contract.py` so `--strict-social-ad` checks core structure, background video, captions, opening material, traffic no-upscale and diversity by default; unrequested PiP/大字报 now fail, while `--require-pip` and `--require-editorial-overlay` enforce the optional layers only on explicit routes.
- Synced `SKILL.md`, README, scripts docs, templates, `CONTEXT/` memories and regression prompts to focus default execution on best video-material matching, caption handling, audio-video sync and necessary transitions.
- Hardened material usage governance: single material paths now have a 20-use global cap, a single final may use a material path only once, and `projects/素材使用监控.csv` updates are normal cumulative adds instead of ordinary rebuild/refresh writes.
- Updated `update_asset_usage_monitor.py` to fail same-final duplicate material paths, cap overflow and unacknowledged `--rebuild`; its normal success report now exposes `mode=cumulative_add`.

## 2026-07-01

- Clarified the workflow entry audience as short-video platform C-end viewers, not internal learning exchange or project review, and hardened editorial overlay rules so title text must summarize matched copy source cue/text/reason instead of exposing workflow/process labels.
- Expanded `validate_visual_contract.py` to reject visible internal process/learning labels and strict social-ad overlays such as 工作流程, 内部学习交流, 项目复盘, pipeline, or workflow, plus a regression prompt for left-corner title leakage.
- Hardened latest visual regression rules: hook openings now require `projects/素材/开头素材/` or `opening_hook` evidence with 5-10s full-frame/no-crop/no-upscale display, traffic CTA material requires no-upscale/native-scale evidence, and strict social-ad PiP requires simultaneous grid groups with readable sizes.
- Expanded `validate_visual_contract.py` with opening-material, traffic no-upscale, PiP simultaneous/grid/size checks, plus a passing social-ad fixture.
- Added the global material usage monitor `projects/素材使用监控.csv` and `scripts/update_asset_usage_monitor.py`; final close now records actual material usage as `素材名,文件路径,使用次数,使用程度`.
- Hardened the latest-run regression gates: current `projects/内容/文案` + `projects/内容/音频` routes now require explicit same-stem source paths, background layers must be no-mask and fully opaque, and browser/page preview no longer counts as final output.
- Added `validate_dialogue_sync.py --require-script-audio-pair` and expanded `validate_visual_contract.py` background checks for opacity/transparency/mask evidence.
- Updated the shared asset taxonomy: `projects/素材/` remains the visual/keyword material pool, while `projects/内容/文案/` and `projects/内容/音频/` are the current batch script and same-stem voiceover pools.
- Added script/audio pairing rules: `文案N.txt` must pair with `文案N.mp3`, while `BGM.*` is treated only as background music, not the narration clock.
- Synced README, context memories, positive/negative examples and regression prompts so batch workflows build `script_audio_pair_map` before dialogue timing.
- Hardened dialogue-caption order gates: strict final sync now requires script-order evidence, per-cue audio-anchor order, HTML `data-cue-id` mapping and monotonic caption timeline checks so shuffled subtitles cannot pass final validation.

## 2026-06-30

- Removed the split F1/F2 workflow package topology and promoted the HyperFrames-native workflow contract to `.agents/skills/workflow/`.
- Renamed active route, templates, prompts, output artifacts and metadata from F2 to workflow; legacy F1/F2 references now exist only as migration background or old-runtime guardrails.
- Moved `video-to-manifest` into `.agents/skills/workflow/video-to-manifest` as a workflow satellite and updated registry/routes to point at the new topology.
- Updated workflow output topology: `projects/素材/` and `projects/示例/` are cumulative shared asset pools, workflow outputs live under the `projects/output/<日期>/` namespace, and batch final videos are collected under `projects/output/<日期>/成片/`.
- Added the process-file boundary: workflow project files, logs, snapshots, validation reports and intermediate artifacts now default to `projects/output/<日期>/过程/`, while final videos stay outside `过程/`.
- Added the shared asset preprocessing taxonomy for `projects/素材/`: material branches for opening, revenue, comic-drama, big text overlays, workflow, traffic, asset images and transitions, plus the mirrored `核心关键词/` branch.
- Upgraded workflow toward Skill 2.0 runtime-spine compliance: added `Directory Structure & Detail Routing Contract`, split the legacy `CONTEXT.md` knowledge base into the five-file `CONTEXT/` structure, removed the legacy single-file context entry, and synchronized module loading, review gates, registry context carriers and README structure.
- Added Layered Rhythm Assembly for video stitching: hook/content/CTA segment roles, continuous no-mask background throughline, semantic PiP, dialogue captions and core-word editorial overlays are now part of `workflow_composition_plan.json` and `validate_visual_contract.py --strict-social-ad`.

## 2026-06-29

- Added `scripts/validate_visual_contract.py` as a mechanical workflow acceptance gate for audience-visible text hygiene, dialogue caption integrity, overlay/caption duplication, semantic PiP cue binding, manifest match strength, and batch ledger/audit consistency.
- Wired `visual_contract_validation.json` into workflow `N7`, `C6`, `C7`, review gates, scripts documentation, context playbook, and test prompts so social-ad/batch visual failures block final close.
- Added platform deduplication controls for batch and semantic-equivalent workflow videos: `asset_usage_ledger.json`, `asset_diversity_audit.json`, reuse penalties, variation axes, and completion/report gates.
- Strengthened `N3-MEDIA-EVIDENCE` and `N5-STORYBOARD-PLAN` so workflow consumes deep manifest tags (`semantic_vector`, `trigger_profile`, `visual_signature`, `variation_profile`, `analysis_slice_id`, `reuse_profile`) instead of relying on coarse `semantic_tags`.
- Updated execution/output report templates, context heuristics, and test prompts for batch asset diversity and same-meaning copy variation.

## 2026-06-25

- Created workflow as a new HyperFrames-native workflow skill.
- Defined workflow as a successor/rebuild of F1 business goals, not an in-place replacement of F1 runtime.
- Added runtime-spine contract, HyperFrames module routing, review gates, output templates, migration matrix and registry-ready metadata.
