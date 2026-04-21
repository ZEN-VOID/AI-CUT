---
name: anyfast-image-api
governance_tier: full
description: |
  repo-local AnyFast 图像 provider 家族入口。负责在 `nano-banana` 与 `seedream` 两个子技能之间做路由裁决，并澄清它们各自独立的认证、端点与默认输出合同。适用于用户只知道“要走 AnyFast 图像能力”，但尚未明确该落到 Gemini 原生图像接口还是 Ark/SEEDREAM 连续生图接口的场景。
tools: [Read, Write, Edit, Bash]
color: yellow
version: "v1.0"
---

# AnyFast 图像 API 技能族

## Context Loading Contract

- 每次调用本技能时，必须同时加载同目录 `CONTEXT.md` 作为预加载上下文。
- 若同目录 `CONTEXT.md` 缺失，应先补齐最小知识库骨架，或向用户明确报告阻塞；不得在未检查该上下文的情况下执行技能。
- 冲突优先级：用户显式请求 > 仓库/全局 `AGENTS.md` > 本 `SKILL.md` > 同目录 `CONTEXT.md`。

## 1. 作用范围

本技能是 `.agents/skills/api/anyfast/image/` 目录的父级路由合同，不直接发起 HTTP 请求。它的职责是：

- 统一承接 “AnyFast 图像能力” 入口请求。
- 在 `nano-banana` 与 `seedream` 之间做 provider 裁决。
- 明确两个子技能的环境变量、端点和输出目录彼此独立，防止沿父目录路径名误判为共享同一套配置。

当前子技能：

| 子技能 | 路径 | 实际 provider | 默认认证/环境变量 | 典型场景 |
| --- | --- | --- | --- | --- |
| `nano-banana` | `nano-banana/` | AnyFast Gemini 原生图像接口 | `.env: ANYFAST_API_KEY / ANYFAST_BASE_URL` | Gemini 文生图、图生图、`general / face-swap / costume-swap / multiview-*` |
| `seedream` | `seedream/` | 火山引擎 Ark `images/generations` | `.env: SEEDREAM_API_KEY / ARK_API_KEY / VOLCENGINE_ARK_API_KEY` | `doubao-seedream-5-0-260128`、连续多图、SSE |

说明：

- `seedream` 当前保留在 `api/anyfast/image/` 目录下，是仓库内的 provider family 归档方式，不代表它与 `nano-banana` 共享底层端点或密钥。
- 若用户已经明确命中某个子技能，应直接进入该子技能，不必停留在父级路由层。

## 2. 路由输入

父级路由最少需要以下判断信息之一：

- 用户明确提到的 provider 名称
- 上游合同里写明的模型 ID
- 上游合同里写明的 API 形态
- 调用方技能显式指定的 provider skill 路径

常见判别信号：

- 命中 `seedream / doubao-seedream / 方舟 / Ark / sequential_image_generation`：优先走 `seedream`
- 命中 `nano-banana / Gemini 图片 / gemini-3.1-flash-image-preview / face-swap / costume-swap / multiview`：优先走 `nano-banana`
- 只说 “AnyFast 图像 / AnyFast 生图” 且无更强信号：默认走 `nano-banana`

## 3. 核心约束（Mandatory）

1. **父级只路由，不替代子技能执行**
   - 本技能不得自建第二套平行脚本入口。
   - 真正的 HTTP 调用、payload 构造、响应解析与落盘，必须继续由被选中的子技能负责。
2. **子技能环境变量不可混用**
   - `nano-banana` 读取 `.env: ANYFAST_API_KEY / ANYFAST_BASE_URL`
   - `seedream` 读取 `.env: SEEDREAM_API_KEY / ARK_API_KEY / VOLCENGINE_ARK_API_KEY`
   - 不得因为它们位于同一父目录，就把 `ANYFAST_*` 变量当作 `seedream` 的认证源。
3. **模型与端点信号优先于目录名联想**
   - 若上游显式给出 `doubao-seedream-5-0-260128` 或 Ark `images/generations`，必须路由到 `seedream`
   - 若上游显式给出 Gemini 原生 `generateContent`、`inline_data` 或 `gemini-3.1-flash-image-preview`，必须路由到 `nano-banana`
4. **未明确 provider 时默认 nano-banana**
   - 父级默认路由必须稳定、可预测；未命中 `seedream` 强信号时，默认进入 `nano-banana`
5. **父级修复必须同步子级真源**
   - 若发现 env 键名、默认模型、references、脚本帮助或 registry 路由漂移，修复不得只停在父级文档；必须同步落到对应子技能、注册表与总览文档

## 4. 固定执行流程（Mandatory）

1. 先识别是否已明确命中 `nano-banana` 或 `seedream`
2. 若未明确命中，再查看模型、API 形态、上游 provider hint
3. 选定子技能后，立即切换到对应子技能的 `SKILL.md + CONTEXT.md`
4. 若涉及注册、路由或治理现状变动，同步更新 `.codex/registry/skills.yaml`、`.codex/registry/routes.yaml` 与根 `HARNESS.md`

## 5. 输出约定

- 父级输出是路由裁决，而不是图片文件本身。
- 默认返回格式应至少说明：
  - 命中的子技能
  - 选择依据
  - 需要的环境变量来源
  - 若存在漂移，修复落点在哪些文件

## 6. Root-Cause 执行契约（Mandatory）

当 `api/anyfast/image` 目录出现入口混乱、环境变量漂移或 provider 误路由时，按以下链路上溯：

`Symptom/Failure`
-> `Direct Cause`：父级缺失路由合同、子技能 env 键名漂移、registry 未注册、routes 未声明或上游错误地把 `seedream` 当作 `ANYFAST_*` 子接口
-> `规则源`：`.agents/skills/api/anyfast/image/SKILL.md`、子技能 `SKILL.md` 与对应脚本
-> `规则源的规则源`：仓库根 `AGENTS.md` 中的技能基线、Root-Cause First、registry / HARNESS 同步规则
-> `Fix Landing Points`：优先修父级路由合同、子技能 env/脚本文档、registry/routes 与 `HARNESS.md`

用户侧关闭语必须至少包含：

- 根因位置
- 立即修复
- 系统性预防修复
