# Context: video-api

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
last_checked_at: 2026-04-17T00:00:00Z
```
<!-- CONTEXT_HEALTH_END -->

本文件作为 `.agents/skills/api/video/` 父技能的经验层，默认以知识库模式维护：优先沉淀跨 provider 路由、`create-only` / `full-loop` 闭环识别、共享术语收束、以及父级真源缺失类问题。Provider 专属经验继续沉到各子技能的 `CONTEXT.md`。

## 子技能索引

| 子技能 | 经验聚焦 |
| --- | --- |
| `grok/CONTEXT.md` | `/v1/video/create` 创建回执、模型可用性 |
| `kling/CONTEXT.md` | 图生视频、状态轮询、资产 URL 下载 |
| `luma/CONTEXT.md` | Luma generation 状态模型、URL 抽取 |
| `minimax/CONTEXT.md` | Hailuo 默认模型与海螺边界 |
| `runway/CONTEXT.md` | image-to-video 代理路径、ratio 漂移 |
| `seedance/CONTEXT.md` | 模式互斥、多模态参考、状态归一 |
| `sora/CONTEXT.md` | `/v1/videos` 三段异步闭环、别名链 |
| `veo/CONTEXT.md` | `/v1/video/create` JSON 契约、模型集合 |
| `vidu/CONTEXT.md` | 创建回执解释、模型边界提示 |

## Type Map

| 类型 | 症状 | 根因层 | 立即修复 | 系统性预防 | 验证点 |
| --- | --- | --- | --- | --- | --- |
| `TM-VIDEO-API-PARENT-EMPTY` | 子技能很多，但父级 `SKILL.md / CONTEXT.md` 为空，导致路由失真或直接失联 | 父级真源层 | 先补父级路由合同与知识库骨架 | 把“子技能索引 + 路由规则 + 闭环分类”固定在父级真源，不再散落在记忆里 | 父级文件能独立解释何时下钻到哪个子技能 |
| `TM-VIDEO-API-ROUTE-BY-PROVIDER` | 用户已明确点名 provider，却被改投到另一个“更优” provider | 路由优先级层 | 显式 provider 始终优先，直接进入对应子技能 | 在父技能里把“显式 provider / endpoint / model family 命中优先”写成刚性规则 | 点名 `Sora / Runway / Veo` 时不再误路由 |
| `TM-VIDEO-API-CREATE-VS-FULL` | 创建回执被误说成已经拿到成片 | 闭环分类层 | 先确认目标子技能是 `create-only` 还是 `full-loop` | 在父技能索引里显式维护闭环状态，不再靠临场猜 | 输出能明确写出是 receipt 还是下载结果 |
| `TM-VIDEO-API-ENDPOINT-COLLISION` | 多个 provider 都用相似端点，如 `/v1/video/create` 或 `/v1/video/generations`，结果混路由 | 端点判别层 | 结合 provider 名、字段形态、模型族一起判断，不只看路径片段 | 父技能维护“端点 + 字段 + provider”联合路由表 | 不再把 `Seedance / Vidu / MiniMax` 混为一类 |
| `TM-VIDEO-API-MIXED-PAYLOAD` | 在同一个请求里混入多个 provider 的字段语义 | 子技能移交层 | 回退到父级重新做单一路由，再按目标子技能重构输入 | 父技能明确禁止“跨 provider 通用 payload”幻觉 | 请求体只保留目标 provider 合法字段 |
| `TM-VIDEO-API-UNSPECIFIED-PROVIDER` | 用户没点名 provider，只说“做个图生视频”，主代理在多个子技能间摇摆 | 默认裁决层 | 先按 `full-loop`、输入媒体拓扑、多模态需求做裁决 | 父技能把未指定 provider 时的默认选择表写死 | 模糊需求下也能稳定下钻 |
| `TM-VIDEO-API-MISSING-CHILD` | 当前目录已有子技能，但父级索引漏掉，例如 `kling/` 变成隐形能力 | 索引维护层 | 先补父级索引，再继续执行下游任务 | 每次子技能新增、删除、迁移时都同步更新父级真源 | 父级索引与目录清单一致 |
| `TM-VIDEO-API-RCA-LANDING` | 问题明明出在父级误路由，却只去改某个子技能文案 | 根因落点层 | 先判断问题属于父级路由还是子技能契约 | 把“路由问题修父级、字段问题修子技能”写入 Repair Playbook | 相同误路由问题不会在兄弟子技能重复修补 |
| `TM-VIDEO-API-GENERIC-HOST-DRIFT` | 子技能直接沿用通用 `ANYFAST_API_BASE_URL`，真实请求却拿到前端 HTML 或无关壳页 | 环境配置层 | 回退到 provider 专用 `*_API_BASE_URL` 或 `FINEAPI_API_BASE_URL` | 当某 provider 的通用 host 未验证时，在对应子技能中禁止把 `ANYFAST_API_BASE_URL` 当真实请求默认回退 | 真实请求不再出现 `200 + HTML` 被误判成成功 |
| `TM-VIDEO-API-PLATFORM-VS-GATEWAY` | 技能文档把平台站点、文档站点和 API 网关混写，导致新环境默认打错域名 | 真源治理层 | 显式拆开 `ANYFAST_PLATFORM_URL / ANYFAST_DOCS_URL / ANYFAST_API_BASE_URL`，并把脚本默认值只留给已验证 API 网关 | 在父技能经验层固定“平台页不等于 API Base URL”的跨 provider 规则，再回落到各子技能合同与脚本 | `rg` 不再把平台域名误命中为默认 API host |

## Repair Playbook

1. 先识别用户是否显式点名 provider、端点、模型族或脚本路径。
2. 若已点名，直接进入对应子技能，不再做替换。
3. 若未点名，先判断任务要的是 `create-only` 还是 `full-loop`。
4. 再根据输入媒体拓扑裁决：
   - 多模态参考优先 `seedance`
   - `Runway` / `Luma` / `Sora` 明确信号则各归各位
   - 只要创建回执的 Veo / Grok / Vidu / Hailuo 任务，不要冒充闭环执行
5. 一旦完成路由，立即切换到目标子技能字段语义，不再保留父级抽象字段。
6. 若问题属于 provider 特有脚本、字段或接口漂移，下钻修子技能。
7. 若问题属于误路由、索引缺失、闭环分类错误或共享术语漂移，先修父级真源。

## Reusable Heuristics

- 视频 API 父技能最容易失效的不是“接口不会调”，而是“会调很多接口却没有单一路由真源”。
- 当多个 provider 共享相似路径名时，单看端点字符串不够；必须把 provider 名、模型族和字段形态一起看。
- `create-only` 与 `full-loop` 是父级必须先裁决的第一类边界；如果这一步不清楚，后面的输出说明几乎必漂。
- 父级技能不应该发明通用视频 payload。它的职责是路由，而不是把兄弟子技能压平成一个假统一接口。
- 当用户未点名 provider 时，默认优先选择当前已有稳定闭环的子技能；只有任务目标本身就是“创建回执”，才进入 `create-only` 子技能。
- 父级索引缺失本身就是源层问题。目录里已经有的子技能，如果没出现在父级真源里，应优先补父技能而不是让主代理靠记忆兜底。
- 同类误路由一旦在两个以上 provider 间重复出现，说明问题不在某个子技能，而在父级路由规则或命名索引。
- 某个 provider 若还没验证通用 `ANYFAST_API_BASE_URL` 的真实路由，就不要把它继承成默认 Base URL；这类“通用 host 返回 HTML 壳页”的问题一旦在多个子技能复现，应视为跨 provider 的环境回退链治理问题。
- 同一家供应商体系下，`ANYFAST_PLATFORM_URL` 只表示前台站点，`ANYFAST_DOCS_URL` 只表示文档站点，`ANYFAST_API_BASE_URL` 才是脚本应真正调用的网关；三者不能再互相冒充默认值。
