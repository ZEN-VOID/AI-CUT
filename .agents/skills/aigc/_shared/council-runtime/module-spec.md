# AIGC Council Runtime Module Spec

## Purpose

This module documents the current AIGC stage review handoff surface for audit scripts and governance backfill. It is a runtime support spec, not a second skill route source.

## Current Stage Review Handoffs

| stage | review checkpoint | pass target |
| --- | --- | --- |
| `1-分集` | `episode-split-ready` | `2-美学` |
| `2-美学` | `aesthetic-ready` | `3-主体` |
| `3-主体` | `subject-assets-ready` | `4-编剧` |
| `4-编剧` | `screenwriting-ready` | `5-导演` |
| `5-导演` | `director-ready` | `6-分镜` |
| `6-分镜` | `storyboard-ready` | `7-摄影` |
| `7-摄影` | `cinematography-ready` | `8-分组` |
| `8-分组` | `grouping-ready` | `9-图像` |
| `9-图像` | `image-assets-ready` | `10-画布` |
| `10-画布` | `canvas-video-ready` | `release` |

## Legacy Readback

`2-编导`、`3-运动`、旧 `4-摄影`、`5-Image`、`6-Video` 和 `7-Cut` are legacy/readback-only project paths. They must not be registered as active stage owners. Migration tools may read them to recover evidence, then map output to the current stage chain above.
