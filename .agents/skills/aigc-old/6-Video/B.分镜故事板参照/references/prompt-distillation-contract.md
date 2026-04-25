# Prompt Distillation Contract

本文件承接旧 `全能参照` 的核心语义，负责 `distill/` 段的创作与落盘约束。

## Scope

- 输入是 `projects/aigc/<项目名>/3-Detail/<episode_id>.json` 中稳定的分镜组。
- 输出是一组组级视频请求对象，每个 `分镜组ID` 对应一条 request packet。
- `第N集.txt` 是人工审阅主稿；`第N集.json` 是 completeness carrier；`_manifest.json` 是追溯台账。

## Authorship Gate

- 组级视频 prompt 正文、TXT 主稿和压缩判断必须由 LLM 主创。
- 脚本只可做读取、投影、校验、统计、manifest 回写，不得直接生成 canonical creative truth。
- 若本轮只是兼容迁移已有人工确认的旧产物，必须在 manifest 标注 `source=legacy_compat_projection`。

## Omni Config Profile Gate

进入 `distill/` 段前，`N1-INTAKE` 必须把旧 `全能参照` 的配置真源消化成 `omni_config_profile`，再交给 N2 执行。该 profile 至少覆盖：

- `全能参照/SKILL.md` 的输入完整性门、BC 输出骨架、压缩优先级、TXT 主稿合同、引用字段骨架和脚本边界。
- `全能参照/CONTEXT.md` 的已知失败模式：漏镜、字段标题泄露、过早短语化、时间锚点漂移、branch-owned 字段被 legacy 反客为主、脚本主创回流。
- `prompt-assembly-spec.md` 的组级设计块、固定音频约束、`xx秒-xx秒｜分镜<组内序号>：` 开头、对白句槽、`full/normal/tight/ultra` 预算层级与 canonical JSON spec。
- `6-Video/_shared/image-to-video-prompt-principles.md` 的图生视频共享语义顺序、branch-owned first、legacy fallback、压缩优先级与转场特效使用原则。

若 `omni_config_profile` 缺失或只停留在路径清单，`N2` 必须视为 `FAIL-SBREF-ROOT-01` 的前置失败，而不是继续生成 prompt。

## Group Prompt Contract

- 最终 prompt 采用 `BC` 结构：一段组级设计块，加逐镜融写行。
- 组级设计块至少吸收 `全局风格 / 类型元素 / 导演意图 / 出场角色及穿搭`，并保留固定音频约束：`不生成字幕，不生成BGM，要生成物理互动音效与环境音。`
- 每镜融写行以 `xx秒-xx秒｜分镜<组内序号>：` 开头。
- 完整四段式 `分镜ID` 只保留在 `meta.source_shot_ids`、manifest 或回链字段中；prompt 正文只显示组内序号。
- `剧情桥段 -> 对白句（如存在） -> 主体动作与表演 -> 镜头控制 -> 环境与摄影 -> 视觉重心` 是默认语义顺序，不是硬表层模板。

## TXT Distillation Contract

`第N集.txt` 必须按“集 -> 分镜组 -> 分镜”的固定模板组织：

1. `分镜组ID`
2. `全局风格 + 类型元素 + 导演意图`
3. `分镜N，x-y秒`
4. `剧本正文：`
5. `主体锚定：`
6. `分镜明细：`
7. `字数统计：xxx`

硬规则：

- 每个 `分镜组ID` 必须独立成块，不得把多个组揉成一段。
- 每个组内的分镜顺序必须跟随 `detail.分镜列表` 的 canonical 顺序。
- `剧本正文`、`主体锚定.场景`、`主体锚定.角色` 不得压缩、裁断或改写。
- `主体锚定.道具` 可轻量压缩，但不得改变事实。
- `分镜明细` 必须展开到 `分镜构图 / 运镜手法 / 角色表现 / 氛围表现 / 摄影表现 / 转场特效` 的下一层字段，再编排为镜头语言优先的自然 prose。
- 禁止显式或隐性字段串联；即便没有字段标题，只要能轻易拆回字段顺排，也视为失败。
- 每个分镜组 block 末尾必须追加 `字数统计：xxx`，统计行本身不计入。
- 每个组的目标字数窗口为 `1600-1900` 字；超限时优先压缩补充镜头组织项，不牺牲剧情桥段和镜头控制。

## Distill Output

- `distill/<episode_id>.json`
- `distill/<episode_id>.txt`
- `distill/_manifest.json`

每条 request packet 至少包含：

- `meta.group_id`
- `meta.source_shot_ids[]`
- `prompt_style`
- `model.prompt`
- `model.prompt_char_count`
- `model.reference_images`
- `model.image_markers`
