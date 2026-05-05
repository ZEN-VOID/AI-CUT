# LibTV Skill

Skill 2.0 wrapper for `libtv-labs/libtv-skills`.

## Directory Tree

```text
libTV/
├── references/
├── scripts/
├── templates/
├── review/
├── steps/
├── knowledge-base/
├── types/
│   ├── editing/
│   ├── generation/
│   └── session-ops/
├── agents/
├── CHANGELOG.md
├── CONTEXT.md
├── LICENSE.txt
├── README.md
└── SKILL.md
```

## Quick Entry

Use `$libTV` for LibTV / LibLib.tv image and video generation, editing, passive session query, user-requested result downloading, project canvas notice, and project switching.

Live calls require:

```bash
export LIBTV_ACCESS_KEY="your-access-key"
```

At task start, the default handoff tells 龙虾 `把全部工作流和结果都放在画布上。` so the workflow and results are managed on the project canvas from the beginning.

For reference-image or reference-video tasks, upload every local file first with the active `LIBTV_ACCESS_KEY`; submit only the returned OSS URLs in the prompt, never local filesystem paths.

After session creation, `$libTV` does not automatically poll progress or download media. The LibTV canvas is the default progress/result surface. Keep the intended output directory, including AIGC `videos/` directories, ready for a later user-requested download.

For video tasks, the default submitted spec is sound/audio enabled, 15 seconds, 16:9, and 720P. Put this as the first hard-parameter block before creative text, and explicitly tell the provider to set the canvas/video duration to 15 seconds, not the default 10 seconds.

## Source

The Python scripts and MIT license are imported from `https://github.com/libtv-labs/libtv-skills`.
