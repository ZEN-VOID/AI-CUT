# Knowledge Base: 漫画生成 Heuristics

本文件保存可检索的稳定经验。执行时不默认全量加载；只有排障、复盘或相似问题检索时读取。

## CLI Batch Lessons

- `generate-batch` 应用于“多个不同 prompt”，不要用单 prompt + `--n 9` 表示九页漫画。
- 漫画页 prompt 已由 2 号 JSON 提供完整创作真源，CLI 侧建议加 `--no-augment`，避免自动增强改变角色和场景连续性。
- 对竖版漫画页，默认尺寸应显式传 `1152x2048`，避免 CLI 默认 2K 横版。
- Dry-run 计划是最小可审计证据；即使 API 不可用，也应该保留 `imagegen_jobs.jsonl` 和逐页 prompt。

## Handoff Lessons

- `4-剧集海报` 参考 3 号图片时最需要稳定页码命名，而不是 provider-specific 文件名。
- 多个 group 批量执行时，最稳目录是 `3-漫画生成/<group_slug>/imagegen-cli/`。
- 如果用户强行共用输出目录，必须把 group slug 加进文件名前缀。
