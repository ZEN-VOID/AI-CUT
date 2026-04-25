# Storyboard Sheet Workflow

## Node Network

| node_id | objective | inputs | actions | evidence | route_out | gate |
| --- | --- | --- | --- | --- | --- | --- |
| `S0-intake-lock` | 锁定本轮入口和模式 | 用户请求、source request、项目根 | 判定 `storyboard_full / distill_only / bind_only / handoff_only / repair` | `mode_decision` | `S1 / S5 / S7 / review` | 未锁 mode 不得继续 |
| `S1-group-lock` | 唯一锁定分镜组 | `3-Detail/第N集.json`、`分镜组ID` | 定位 canonical group，收集有序 `source_shot_ids` | `group_lock_note` | `S2` 或阻断 | 组不唯一不得蒸馏 |
| `S2-storyboard-distill` | LLM 生成组级 storyboard prompt | canonical group、共享模板、`references/request-distillation.md` | 消化旧叶子 `N3-N4`：生成固定前缀、组级设计块、多镜融写列，并执行字段覆盖检查 | `prompt_gate` | `S3` | prompt 不得脚本主创、摘要化或缺镜头 |
| `S3-template-map` | 映射 image request 模板 | prompt、group metadata、shared template | 填充 `meta / prompt_style / model / prompt_char_count` | `request_json` | `S4` | 模板骨架完整 |
| `S4-request-land` | 落组级 request JSON | request object、output mode | 写 `5-Image/分镜故事板/第N集/第N集.json`，按需写 manifest | `request_path` | `S5 / S7 / done` | 输出路径正确 |
| `S5-reference-bind` | 保守绑定本地引用 | request JSON、Assets、4-Design | 推导候选、绑定强证据图片、写 provider-neutral 引用 | `binding_candidates` | `S6` | 歧义不得直接绑定 |
| `S6-binding-audit` | 审计参照绑定三件套 | bound JSON、manifest、match-report | 检查真实路径、候选解释、next_entry | `binding_audit` | `S7 / rework` | 未通过不得 handoff |
| `S7-provider-route` | 锁定唯一 provider | request 或 bound request、用户 provider 要求 | 选择 `builtin_image_gen / jimeng_cli / nano_banana` 或输出推荐缺口 | `provider_decision` | `S8` 或 hold | provider 不唯一不得落最终计划 |
| `S8-submit-pack` | 生成 handoff 包 | provider decision、source request | 写 `submit-plan.json + submit-brief.md` | `submit_pack` | `S9` | output_dir 与 submit 包同目录 |
| `S9-converge` | 汇流结案 | 执行证据、跳过链、review verdict | 输出闭环说明和返工入口 | `closure_note` | done | 只有本节点可宣告完成 |

## Branch Rules

- `distill_only`: `S0 -> S1 -> S2 -> S3 -> S4 -> S9`
- `bind_only`: `S0 -> S5 -> S6 -> S9`
- `handoff_only`: `S0 -> S7 -> S8 -> S9`
- `storyboard_full`: `S0 -> S1 -> S2 -> S3 -> S4 -> S5 -> S6 -> S7 -> S8 -> S9`
- `storyboard_full + prompt_only/no_reference`: `S0 -> S1 -> S2 -> S3 -> S4 -> S7 -> S8 -> S9`
- `repair`: `S0 -> review -> failed node`

## Evidence Gate

每个节点都必须留下可复核证据。若仅在回复中说明但无路径、字段或 verdict，不能视为通过。

## Request Distillation Playbook

本节是原 `1-提示词蒸馏/分镜故事板` 完整蒸馏方法在融合包中的执行落位。详细字段与 prompt 句法以 `references/request-distillation.md` 为准；本文件负责把方法固定到 `S0-S4` 的动作、证据、路由和 gate。

### S0 `intake-lock`

#### 着手面

- 当前对象是不是组级 storyboard，而非单帧或漫画页。
- 本轮输出是不是 request JSON / handoff 包，而非真实图片。
- `json_only / full_trace / handoff_pack` 是否已有明确指令。
- `3-Detail/第N集.json` 是否存在，且 adapter readiness 可达 `detail_in_progress | ready`。

#### 动作

1. 锁定 `mode`：`distill_only / storyboard_full / bind_only / handoff_only / repair`。
2. 若从 `3-Detail` 进入，读取 canonical detail root，并检查 `meta + groups[]` 是否成立。
3. 固定非目标：不改写上游镜头事实，不直接出图，不处理漫画页，不把 provider 参数写进 prompt。
4. 将全局缺口与局部缺口分开：全局缺口阻断；局部缺口只允许保守留空或补读 sidecar。

#### Gate

- 未锁定对象范围不得进入 `S1`。
- `groups[]` 缺失、schema 壳破坏或 readiness 不成立时阻断。

### S1 `group-lock`

#### 着手面

- 目标 `分镜组ID` 是否唯一。
- 组内镜头顺序是否稳定。
- `source_shot_ids` 是否能完整回链。
- legacy helper 是否只是 compat projection，而不是第一真源。

#### 动作

1. 按用户或父级提供的 `分镜组ID` 定位目标组。
2. 从 canonical `detail.分镜列表` 抽取有序 `source_shot_ids`。
3. 检查重复 group、空 shot map、顺序冲突、compat helper 断链。
4. 形成 `group_lock_note`：项目、集号、`group_id`、`source_shot_ids`、局部缺口。

#### Gate

- 组不唯一不得蒸馏。
- 镜头顺序不稳定不得进入 `S2`。
- 本节点只锁组，不生成 prompt；完整蒸馏方法必须从 `S2` 执行。

### S2 `storyboard-distill`

#### 着手面

- 固定英文前缀是否逐字保留。
- 组级设计块是否覆盖 `global.*` 与角色/穿搭连续性。
- 多镜融写列是否按 `source_shot_ids` 覆盖每个镜头。
- prompt 是否仍由 LLM 主创，而不是脚本拼接主创。

#### 动作

1. 先生成 `storyboard_group` 内容块：
   - 组级：`分镜组ID / global.剧本正文 / global.全局风格 / global.类型元素 / global.导演意图 / 出场角色及穿搭`。
   - 镜级：按 `detail.分镜列表` 顺序读取 `剧本正文 / 主体锚定 / 运动表现 / 角色表现 / 氛围表现 / 分镜构图 / 摄影表现或摄影美学 / 运镜手法 / 转场特效`。
   - 可选：消费 `景别 / 镜头视角 / 镜头速度 / 视觉强化`。
   - fallback：只在必要时参考 `角色背景面 / 角色站位走位 / 道具及状态 / 分镜表现 / 正文回指`。
2. 逐字放入固定前缀：

   ```text
   Create a multi-panel storyboard based on the following shot breakdown.
   Add the shot sequence number in the bottom-left corner of each panel (no other text).
   Auto-adapt the panel layout grid based on the total number of shots.
   ```

3. 前缀后直接拼接组级设计块与多镜融写列，不插入解释说明。
4. 每镜以 `{time_range}｜分镜{shot_index}：` 起行；完整四段式 `分镜ID` 只进结构化回链字段。
5. 若 prompt 超长，按 `full -> normal -> tight -> ultra` 压缩子句，不能合并或删除镜头。
6. 统计 `prompt_char_count`，并形成 `prompt_gate`。

#### Gate

- prompt 不得遗漏固定前缀。
- prompt 不得把整组 `global.剧本正文` 单独粘贴成摘要段。
- prompt 不得遗漏、乱序或合并组内镜头。
- prompt 不得包含 provider 参数或图片生成宣告。
- 缺失字段只能保守留空，不得脑补。

### S3 `template-map`

#### 着手面

- `meta` 是否锁定组级来源。
- `prompt_style` 是否服务多格 storyboard。
- `model` 是否保留共享模板骨架。
- 参照槽位是否保留而不伪造。

#### 动作

1. 读取共享 image-generation input template。
2. 填充 `meta.project / meta.episode / meta.group_id / meta.source_tranche / meta.shot_level / meta.source_shot_ids`。
3. 填充 `prompt_style.type / prompt_style.language / prompt_style.char_limit`。
4. 写入 `prompt / prompt_char_count`。
5. 保持 `model.model_version / ratio / image_size / output_format / num_images / reference_images / image_markers` 骨架完整。
6. 有设计资产时只登记候选槽位；真实绑定交给 `S5-S6`。

#### Gate

- 模板字段被删改不得落盘。
- `reference_images / image_markers` 缺图也必须保留空槽位。

### S4 `request-land`

#### 着手面

- `第N集.json` 是否仍是唯一 request 业务真源。
- `full_trace` 是否需要 `_manifest.json`。
- 本轮是否应进入绑定、直接 handoff 或结案。

#### 动作

1. 将 request object 写入 `projects/aigc/<项目名>/5-Image/分镜故事板/第N集/第N集.json`。
2. 若 `full_trace`，额外写 `_manifest.json`，记录 `source_file / group_count / source_shot_ids / prompt_char_count / exception_note`。
3. 审计 prompt gate、模板骨架、路径、输出模式和回链字段。
4. 根据 `reference_state` 和用户覆盖决定进入 `S5` 还是 `S7`。

#### Gate

- `prompt_char_count` 必须与实际 prompt 一致。
- `meta.group_id / source_shot_ids` 必须可回链。
- 只有本节点通过，request 蒸馏才算完成。
