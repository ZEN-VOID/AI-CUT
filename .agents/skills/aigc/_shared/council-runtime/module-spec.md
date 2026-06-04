# AIGC Council Runtime Module Spec

## Purpose

This module documents the current AIGC stage review handoff surface for audit scripts and governance backfill. It is a runtime support spec, not a second skill route source.

## Current Stage Review Handoffs

| stage | review checkpoint | pass target |
| --- | --- | --- |
| `1-分集` | `episode-split-ready` | `2-编剧` |
| `2-编剧` | `screenwriting-ready` | `3-美学` |
| `3-美学` | `aesthetic-ready` | `4-导演` |
| `4-导演` | `director-ready` | `5-表演` |
| `5-表演` | `performance-ready` | `6-氛围` |
| `6-氛围` | `atmosphere-ready` | `7-分镜` |
| `7-分镜` | `storyboard-ready` | `8-摄影` |
| `8-摄影` | `cinematography-ready` | `9-光影` |
| `9-光影` | `lighting-ready` | `10-分组` |
| `10-分组` | `grouping-ready` | `11-主体` |
| `11-主体` | `subject-assets-ready` | `12-图像` |
| `12-图像` | `image-assets-ready` | `13-画布` |
| `13-画布` | `canvas-video-ready` | `14-审片` |
| `14-审片` | `video-review-ready` | `release` |

## Legacy Readback

`2-编导`、`3-运动`、旧 `4-摄影`、`5-Image`、`6-Video` 和 `7-Cut` are legacy/readback-only project paths. They must not be registered as active stage owners. Migration tools may read them to recover evidence, then map output to the current stage chain above.
