# Context: wjs-syncing-multicam

## Context Health
<!-- CONTEXT_HEALTH_START -->
```yaml
monitor_version: 1
soft_limit_chars: 40000
hard_limit_chars: 80000
soft_limit_cases: 80
hard_limit_cases: 140
current_chars: 3091
current_lines: 45
current_cases: 0
status: ok
recommended_action: none
last_checked_at: 2026-06-21T06:49:48Z
```
<!-- CONTEXT_HEALTH_END -->

本文件是 `wjs-syncing-multicam` 技能的经验层知识库，用于沉淀可复用的失败模式、修复策略和运行启发。它不重定义同目录 `SKILL.md` 的入口、路由、输出合同或完成门禁。

## Type Map

| failure_or_outcome_type | root_cause_layer | immediate_fix | systemic_prevention | verification_point |
|---|---|---|---|---|
| 用户期待生成 `*_synced.MOV` 或同步后重编码文件 | 输出合同层 | 说明本技能只产 `.sync.json` sidecar，原始文件不修改、不复制、不重编码 | 下游消费 offset，而不是把 offset 烧进新视频 | 原文件未变，参考与非参考输入旁边有 sidecar |
| 只有单机位素材却要求同步 | 入口路由层 | 报告无可对齐参考；改用切分/剪辑类技能 | 触发前确认 2+ 同一事件录音/视频源 | 输入列表包含 reference 和至少一个 source |
| 用户要自动剪辑、画中画或导出多机位成片 | 下游边界层 | 同步完成后交给 `wjs-editing-multicam` 消费 sidecar | 本技能只做时间线对齐，不承担编辑/render | sidecar 可被下游读取，未生成成片 |
| 低信噪比或不同麦克风导致 raw waveform 相关误判 | 算法层 | 使用 `polysync sync` 的 log-energy envelope 相关，不回退 raw PCM 相关 | 不跳过 envelope；把它视为鲁棒性的核心步骤 | `polysync verify` residual 达标或可解释 |
| 多音轨相机选到静音轨导致同步失败 | 音频流选择层 | 使用 `polysync` loudest audio stream 自动选择 | sync 和 verify 必须使用同一 loudest-stream 逻辑 | 非静音轨被选中，verify 不因轨道不一致发散 |
| partial coverage 片段按全程素材同步失败 | 覆盖窗口层 | 对只覆盖中段的录音/视频使用 `polysync sync REF SRC --partial` | 先判断 source 是否覆盖完整 session；短片段不要求完整 probes | sidecar 记录合理的 `overlap_in_reference` |
| `-itsoffset` 放在 `-i` 后或用于 raw PCM 分析无效 | ffmpeg 消费层 | 消费视频时把 `-itsoffset` 放在对应 `-i` 前；分析 raw PCM 时用 numpy index arithmetic | 文档和下游脚本统一 offset 语义 | 对齐预览中 source 起点符合 `delta_seconds` |
| `median_residual_ms` 很小但 `residual_spread_ms` 偏大 | 验证解释层 | 先判断是否远场/低 SNR outlier；镜头剪辑场景以 median 为主 | 只有长时长 lip-sync 或 spread 超过交付帧级门槛时追 drift | median 几毫秒且视觉/听感对齐，或已启用 drift 修正 |
| 把 `drift_slope` 混入 `delta_seconds` | sidecar schema 层 | 保持 `delta_seconds` 与 `drift_slope` 分离，下游按需 `atempo = 1 + drift_slope` | schema 字段含义不重载；普通剪辑可忽略 drift | sidecar 中 drift 字段独立，delta 表达 midpoint-canonical offset |
| 下游从当前工作目录解析 sidecar 路径 | 路径解析层 | 以 `Path(sidecar).parent` 解析 `source` 与 `reference` | sidecar 内路径相对 sidecar 所在目录，不相对调用进程 cwd | 换 cwd 后下游仍能找到原始素材 |

## Repair Playbook

1. 先读取同目录 `SKILL.md`，确认输入是同一事件的 2+ 录音/视频源，并选定一个 reference。
2. 确认本机可用 `polysync`、`ffmpeg`、`ffprobe`；本技能不再维护本地同步脚本。
3. 对每个非 reference source 独立运行 `polysync sync REF SRC`；同一组素材保持同一个 reference。
4. 若 source 只覆盖 session 中段，改用 `--partial`，不要为了完整覆盖补黑、补静音或重编码。
5. 每个 source 同步后运行 `polysync verify REF SRC SRC.sync.json`，检查 median residual、spread、probe count。
6. 失败时按层排查：输入是否同一事件 -> 音频轨是否有效 -> partial/full 模式是否选错 -> drift 是否需要下游修正 -> sidecar 路径是否正确。
7. 完成后只交付 sidecar 与验证结论；编辑、PiP、成片导出交给下游多机位剪辑技能。

## Reusable Heuristics

- sidecar over re-encode 是本技能的核心取舍：省空间、保质量、可逆、可被不同下游消费。
- reference 也应有 sidecar，哪怕 `delta_seconds: 0`，这样下游可以统一处理所有输入。
- `delta_seconds` 表示 source 的 `t=0` 落在 reference timeline 的位置；正数通常意味着 source 晚于 reference 开始。
- camera-cut editing 通常不需要追很小的 drift；长篇 lip-sync 才需要认真处理 `drift_slope`。
- noisy B-roll 或远场麦克风可能让 spread 偏大，先看 median 和实际听感，不要为少数 outlier 过度修复。
- 消费 sidecar 时，offset 是输入级属性；在 ffmpeg 中必须位于对应 `-i` 前。
- sidecar schema 是下游合同，不要在 JSON 中写注释或临时字段。

## Promotion Backlog

- 可补一个 sidecar schema validator，检查必需字段、相对路径、overlap 区间和 verification 结果。
- 可沉淀同步报告模板，统一列出 reference、source、delta、drift、overlap、median/spread/probe_count。
- 如果 partial coverage 判断反复出错，考虑在运行前增加素材时长/覆盖关系 dry-run 提示。
