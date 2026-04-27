# Context: 漫画生成

本文件沉淀“九刀流 JSON -> `.agents/skills/cli/imagegen` -> 9 张漫画页”的运行经验。当前默认生图工具已调整为仓库内 CLI imagegen，默认模型为 `gpt-image-2`，默认执行方式为 `generate-batch` 中 9 个单页 job。Seedream、Dreamina、AnyFast 与 Codex built-in `image_gen` 只保留为显式 fallback 或 legacy 追溯。

## Context Health

```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-27
```

## Type Map

| type_id | 症状 | 根因层 | 立即修复 | 系统预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-CG-01` | 仍然默认调用 Seedream / Dreamina / built-in `image_gen` | runtime 路由层 | 改走 `.agents/skills/cli/imagegen/scripts/image_gen.py generate-batch` | `SKILL.md` 和 registry 固定 CLI imagegen 为默认路径 | 报告写 `provider=cli-imagegen` |
| `TM-CG-02` | 9 页被合成一张九宫格或 contact sheet | batch 语义层 | 每页一个 JSONL job，`n=1`，输出 `page01..page09` | `references/` 固化单页 job 约束 | `imagegen_jobs.jsonl` 有 9 行 |
| `TM-CG-03` | 输出像同一场景九个变体 | 上游 JSON 层 | 回到 2 号重切 `story_beat_map / pages[]` | 3 号只投影已有剧情，不临场重写 | 9 页 `page_role/action/page_number` 不重复 |
| `TM-CG-04` | CLI 执行因缺少 `OPENAI_API_KEY` 失败 | 环境层 | 保留 dry-run 计划并提示配置 API key | execute gate 先检查环境 | dry-run 不需要 key，execute 报告缺口 |
| `TM-CG-05` | 输出目录漂移到 `output/imagegen/` | 项目持久化层 | 传 `--out-dir` 指向项目 3 号目录 | runner 固定项目根推断和输出目录 | 文件位于项目根下 |
| `TM-CG-06` | 页面比例不稳定 | CLI 参数层 | 使用 `--size 1152x2048` 并在 prompt 内重复 9:16 | Runtime Policy 固定竖版尺寸 | 报告记录 size |
| `TM-CG-07` | 多个 group 连续执行互相覆盖 | group 目标解析层 | 默认每组独立 `imagegen-cli/` 子目录；共享目录时自动加 group 前缀 | N4 gate 检查命名冲突 | report 中 saved_files 不覆盖 |
| `TM-CG-08` | 4 号动画阶段找不到页图 | 跨阶段命名层 | 稳定输出 `page01.png..page09.png` | Output Contract 明确图片命名 | 4 号按页码可定位首帧 |
| `TM-CG-09` | 页码缺失或不是右下角纯数字 | prompt 编译层 | 从 `page_number_overlay` 和页号字段重复写入 prompt | 单页 prompt 后缀固定页码约束 | 每页 prompt 含对应数字页码 |
| `TM-CG-10` | 3 号脚本尝试“优化剧情” | 主创边界层 | 删除脚本中的创作性改写，只保留投影/拼装 | 遵循 LLM-first creative authorship | prompt 保留 `positive_prompt` 原文 |

## Repair Playbook

1. 先看 `comic_generation_report.json` 中的 `provider / model / size / quality / mode / saved_files`。
2. 若 provider 不是 `cli-imagegen`，先修 3 号 runtime 路由和 registry，不继续排查视觉质量。
3. 若 JSON 不合格，不允许绕过 2 号 validator 直接生图。
4. 若缺少 API key，只能停在 dry-run 或提示配置，不静默切换外部 provider。
5. 若输出成九宫格，检查是否误用单 prompt 多图或 `n>1`；正确路径是 9 行 JSONL、每行一页。
6. 若页面语义不对，回到 2 号 JSON 修源；3 号不负责重写剧情。
7. 若输出目录不在项目根，修 `_infer_project_root` 与 `--out-dir`，不要让下游引用 CLI 默认目录。
8. 若形成稳定故障模式，写回本文件；若稳定到必须执行，再晋升到 `SKILL.md` 或对应分区。

## Reusable Heuristics

- 漫画 3 号选择 `.agents/skills/cli/imagegen` 后，最稳的证据形态是 `imagegen_jobs.jsonl + pageXX prompt + comic_generation_report.json`。
- CLI `generate-batch` 可以承载 9 个不同 prompt，但不能把“9 页漫画”误当成一个 prompt 的 `n=9` 变体请求。
- `--no-augment` 对漫画页更稳，因为 2 号 JSON 已经携带完整角色、场景、版式和页码约束；额外自动增强容易稀释连续性。
- 默认 `1152x2048` 比 CLI 的默认横版 2K 更适合 9:16 漫画页；如果用户要更高精度，可显式改 `2160x3840`。
- prompt 编译时应保留 `positive_prompt` 原文，再追加执行后缀和硬约束；不要把上游 prompt 摘要化到丢失角色锁。
- dry-run 不是半成品，它是可审计执行计划；真实执行失败时，dry-run 产物仍可作为排障证据。
