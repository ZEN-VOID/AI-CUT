---
name: video-downloader
description: Downloads videos from YouTube and other platforms for offline viewing, editing, or archival. Handles various formats and quality options.
---

# Video Downloader

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

This skill downloads videos from YouTube and other platforms directly to your computer.

## When to Use This Skill

- Downloading YouTube videos for offline viewing
- Saving educational content for reference
- Archiving important videos
- Getting video files for editing or repurposing
- Downloading your own content from platforms
- Saving conference talks or webinars

## What This Skill Does

1. **Downloads Videos**: Fetches videos from YouTube and other platforms
2. **Quality Selection**: Lets you choose resolution (480p, 720p, 1080p, 4K)
3. **Format Options**: Downloads in various formats (MP4, WebM, audio-only)
4. **Batch Downloads**: Can download multiple videos or playlists
5. **Metadata Preservation**: Saves title, description, and thumbnail

## How to Use

### Basic Download

```
Download this YouTube video: https://youtube.com/watch?v=...
```

```
Download this video in 1080p quality
```

### Audio Only

```
Download the audio from this YouTube video as MP3
```

### Playlist Download

```
Download all videos from this YouTube playlist: [URL]
```

### Batch Download

```
Download these 5 YouTube videos:
1. [URL]
2. [URL]
...
```

## Example

**User**: "Download this YouTube video: https://youtube.com/watch?v=abc123"

**Output**:
```
Downloading from YouTube...

Video: "How to Build Products Users Love"
Channel: Lenny's Podcast
Duration: 45:32
Quality: 1080p

Progress: ████████████████████ 100%

✓ Downloaded: how-to-build-products-users-love.mp4
✓ Saved thumbnail: how-to-build-products-users-love.jpg
✓ Size: 342 MB

Saved to: ~/Downloads/
```

**Inspired by:** Lenny's workflow from his newsletter

## Important Notes

⚠️ **Copyright & Fair Use**
- Only download videos you have permission to download
- Respect copyright laws and platform terms of service
- Use for personal, educational, or fair use purposes
- Don't redistribute copyrighted content

## Tips

- Specify quality if you need lower file size (720p vs 1080p)
- Use audio-only for podcasts or music to save space
- Download to a dedicated folder to stay organized
- Check file size before downloading on slow connections

## Common Use Cases

- **Education**: Save tutorials and courses for offline learning
- **Research**: Archive videos for reference
- **Content Creation**: Download your own content from platforms
- **Backup**: Save important videos before they're removed
- **Offline Viewing**: Watch videos without internet access

## Context Preload (Mandatory)

- 每次调用本技能时，必须自动加载同目录 `CONTEXT.md` 作为预加载上下文。
- 冲突优先级固定为：用户显式请求 > AGENT.md / 元规则 > SKILL.md > CONTEXT.md。
- 失败闭环必须回写 `CONTEXT.md`：记录 `root cause location + immediate fix + systemic prevention fix + layered trace path`。
- 成功闭环必须回写 `CONTEXT.md`：沉淀可复用 heuristic，并标注 promotion scope。
- 禁止将 `CONTEXT.md` 当作过程日志；默认采用知识库模式（Type Map / Repair Playbook / Reusable Heuristics）。
