# F1 To F2 Migration Matrix

本 reference 只回答“F1 业务目标如何迁移到 F2/HyperFrames”。它不得把 F1 的 scripts、validators、manifest 或 ffmpeg 实现变成 F2 runtime 依赖；共享 `workflow/_shared/video-to-manifest` 输出只可作为 F2 `asset_evidence.json` 之前的可选素材证据。

## Migration Matrix

| F1 capability / intent | F1 runtime style | F2 HyperFrames-native landing | F2 evidence / gate |
| --- | --- | --- | --- |
| 输入锁定 | result dir、文案、旁白、素材、参考 | `f2_intake.json` + HyperFrames work root | `C1-INPUT-LOCKED` |
| 参考节奏 | reference analysis -> rhythm plan | `reference_rhythm.json`；只提取结构、切点、字幕/叠层风格 | `FAIL-REFERENCE-COPY` gate |
| 视频素材理解 | `视频说明.yaml` / shared video-to-manifest evidence | `asset_evidence.json` from Codex visual understanding, optionally seeded by shared manifest evidence | `C2-EVIDENCE-READY` |
| 旁白主时钟 | ASR/SRT/silence fallback | HyperFrames media transcribe/TTS or supplied transcript + LLM semantic review | `C3-DIALOGUE-CLOCKED` |
| 单行硬字幕 | ASS/SRT + ffmpeg burn-in | HyperFrames captions / DOM text track with fixed CSS style | preview snapshot + caption evidence |
| 画面映射 | EDL / visual alignment plan | `STORYBOARD.md` + `f2_composition_plan.json` + DOM timeline | `C4-PLAN-LOCKED` |
| PiP / 大字报 | ffmpeg overlays or planned visual layers | HyperFrames overlay layers, data timing, animation presets | safe-zone snapshot gate |
| 转场 | ffmpeg transition/filter plan | HyperFrames animation/GSAP/CSS transitions | `hyperframes-animation` gate |
| BGM / SFX | mix plan + ffmpeg audio mix | HyperFrames media/audio tracks, ducking policy, render verification | audio evidence in report |
| Preview validation | mostly post-render checks | HyperFrames lint/validate/inspect/snapshot before render | `C6-PREVIEW-VALIDATED` |
| Final render | ffmpeg final MP4 | `npx hyperframes render` final MP4 | `C7-RENDER-VERIFIED` |
| Execution report | F1 report template | F2 execution report with Reference Execution Matrix and Rule Evidence Map | `C8-FINAL-OUTPUT` |

## Non-Migration Items

- F1 validators are not copied into F2.
- Shared `workflow/_shared/video-to-manifest` is not F2 canonical runtime and does not replace `asset_evidence.json`.
- F1 EDL fields are not the F2 canonical schema.
- F1 hard-subtitle rendering implementation does not control F2 caption implementation.

## Review Gate Mapping

| review_question | review_gate | fail_code | rework_target | report_evidence |
| --- | --- | --- | --- | --- |
| Did this reference introduce any F1 runtime dependency? | Any F1 script/validator/manifest dependency in F2 runtime fails; shared manifest evidence is allowed only as optional input to `asset_evidence.json` | `FAIL-REFERENCE-DRIFT` | `Core Task Contract` | module list and implementation notes |
| Is each migrated target mapped to a HyperFrames artifact? | Missing F2 landing for a claimed F1 capability fails | `FAIL-F2-MIGRATION-GAP` | `N5-STORYBOARD-PLAN` / `N6-HYPERFRAMES-AUTHOR` | migration row and artifact path |
| Are non-migration items respected? | Using reference content, F1 scripts, or F1 manifests as required truth fails | `FAIL-F2-HYPERFRAMES-ONLY` | `N2-HYPERFRAMES-LOAD` | output report |
