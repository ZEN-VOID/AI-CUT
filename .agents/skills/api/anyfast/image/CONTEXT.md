# Context: anyfast-image-api

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
current_chars: auto
current_lines: auto
status: ok
recommended_action: keep-target-scoped-updates
last_checked_at: 2026-04-21T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `api/anyfast/image` 父级技能的经验层，聚焦 provider 路由、子技能 env 边界、registry 注册与父子合同同步。

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-AFI-ROOT-MISSING` | `api/anyfast/image` 目录只有子技能，没有父级 `SKILL.md + CONTEXT.md` | 技能基线层 | 补齐父级路由合同与经验层 | 把 provider family 的入口、路由与 env 边界固定到父级真源 | 父目录存在 `SKILL.md + CONTEXT.md` 且可直接承接路由问题 |
| `TM-AFI-REGISTRY-DRIFT` | 子技能已被上游引用，但 registry / routes 没有相应条目 | 治理注册层 | 在 `.codex/registry/skills.yaml` 与 `.codex/registry/routes.yaml` 补登记 | 新增 provider family 时同步更新 HARNESS 总览 | registry / routes 中能找到 `api-anyfast-*` 条目 |
| `TM-AFI-ENV-SPLIT` | 把 `seedream` 误当成读取 `ANYFAST_*` 的子接口 | provider 边界层 | 明确 `seedream` 与 `nano-banana` 的认证源彼此独立 | 在父级与子级合同同时声明 env 边界，不再只靠目录名猜 | 调用 `seedream` 时不再读取 `ANYFAST_BASE_URL` 作为认证/端点 |
| `TM-AFI-NANO-ENV-ALIAS` | `nano-banana` 文档、脚本、`.env` 键名不一致 | 环境配置层 | 统一优先读取 `ANYFAST_BASE_URL`，兼容旧键回退 | 让脚本与文档都明确“新键优先、旧键兼容” | 脚本 help、references、SKILL.md 与 `.env` 口径一致 |
| `TM-AFI-SEEDREAM-DRYRUN-AUTH` | 只想校验 payload，却因为没有 `SEEDREAM_API_KEY` 无法 dry-run | 执行入口层 | 允许 `seedream` 在 `--dry-run` 时跳过认证检查 | 固化“真实请求强认证、dry-run 只验结构”的单一合同 | 无 key 时 `seedream --dry-run --print-payload` 可运行 |

## Repair Playbook

1. 先确认父目录是否存在 `SKILL.md + CONTEXT.md`
2. 再区分问题属于：
   - 父级路由缺失
   - `nano-banana` env / 脚本漂移
   - `seedream` 认证或 dry-run 行为漂移
   - registry / routes / HARNESS 未同步
3. 若问题涉及 `.env`：
   - `nano-banana` 看 `ANYFAST_API_KEY / ANYFAST_BASE_URL`
   - `seedream` 看 `SEEDREAM_API_KEY / ARK_API_KEY / VOLCENGINE_ARK_API_KEY`
4. 若问题涉及调用入口：
   - `nano-banana` 优先跑 `--dry-run --print-payload`
   - `seedream` 优先跑 `--dry-run --print-payload`
5. 若问题涉及治理同步：
   - 查 `.codex/registry/skills.yaml`
   - 查 `.codex/registry/routes.yaml`
   - 查根 `HARNESS.md`

## Reusable Heuristics

- “位于同一目录树” 不等于 “共享同一 provider 配置”；真实边界以子技能合同为准。
- 父级路由 skill 的价值不在于多写一层介绍，而在于防止上游把不同 provider 的 env / endpoint / model 混用。
- `nano-banana` 的核心信号是 Gemini 原生 `generateContent + inline_data`。
- `seedream` 的核心信号是 Ark `images/generations + sequential_image_generation + SSE`。
- 如果用户只说 “AnyFast 图像”，默认落到 `nano-banana` 最稳；只有在出现 `seedream` 强信号时再切子技能。
- 只要新增或补录 provider skill，就应该把 registry / routes / HARNESS 视为同一轮任务的必修同步项。
