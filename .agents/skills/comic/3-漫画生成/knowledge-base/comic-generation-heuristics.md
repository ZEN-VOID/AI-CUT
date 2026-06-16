# Knowledge Base: 漫画生成 Heuristics

本文件保存可检索的稳定经验。执行时不默认全量加载；只有排障、复盘或相似问题检索时读取。

## Built-in Imagegen Lessons

- built-in `image_gen` 批量语义不是一个 prompt 的 `n=9`；九页漫画必须拆成 9 个不同 prompt / asset task。
- 漫画页 prompt 已由 2 号 JSON 提供完整创作真源，3 号只追加单页执行边界、9:16、非拼图、非变体、页码和项目硬约束。
- 对竖版漫画页，默认分辨率只作为 prompt target 表达；不要把 `gpt-image-2`、`1152x2048`、`quality` 写成 built-in 路径的硬参数。
- Plan 是最小可审计证据；即使 built-in 工具暂不可用，也应该保留 `imagegen_handoff_plan.json`、`imagegen_prompt_set.json` 和逐页 prompt。
- Built-in 结果默认可能在 `$CODEX_HOME/generated_images` 或 subagent 路径；项目交付必须复制/移动到 3 号输出目录。

## Handoff Lessons

- `4-剧集海报` 参考 3 号图片时最需要稳定页码命名，而不是 provider-specific 文件名。
- 多个 group 批量执行时，最稳目录是 `3-漫画生成/<group_slug>/built-in-imagegen/`。
- 如果用户强行共用输出目录，必须把 group slug 加进文件名前缀。
- legacy CLI runner 可以保留为外部路径，但不得再出现在 active runtime policy、父级阶段表或 2 号 schema 的默认 provider 中。
