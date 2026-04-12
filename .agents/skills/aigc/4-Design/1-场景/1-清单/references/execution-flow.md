# 场景清单执行流程细则

## Canonical Inputs

- `projects/<项目名>/3-Detail/第N集.json`
- `.agents/skills/aigc/_shared/director_episode_output.schema.json`

兼容输入：

- 同 schema 的 `projects/<项目名>/3-Detail/第N集.json`

## Canonical Landing

- 子路径根目录：`projects/<项目名>/4-Design/1-场景/1-清单/`
- 单集目录：`projects/<项目名>/4-Design/1-场景/1-清单/第N集/`
- 汇总 JSON：`projects/<项目名>/4-Design/1-场景/1-清单/第N集/第N集.json`
- 汇总清单：`projects/<项目名>/4-Design/1-场景/1-清单/第N集/_manifest.json`（可选）

## 输入合同

### 必需输入

- 上游 episode 根对象
- `final_output.main_content.分镜组列表[]`
- `分镜组列表[].分镜组ID`
- `分镜组列表[].分镜明细[]`
- `分镜明细[].分镜ID`
- `分镜明细[].场景及方位`

### 推荐输入

- `metadata.episode_id`
- `分镜明细[].时间段`
- `分镜组列表[].剧本正文`

### 输入处理原则

1. 一切场景事实以上游 episode JSON 为准。
2. 只抽取已有 `场景及方位`，不新增研究型字段。
3. `3-Detail` 的 shot 级事实只用于提取与映射，不在本阶段反向改写。

## Mandatory Workflow

1. 读取 `.agents/skills/aigc/SKILL.md + CONTEXT.md` 与本技能 `SKILL.md + CONTEXT.md`。
2. 读取 `projects/<项目名>/3-Detail/第N集.json`，校验最小 shared schema 壳是否成立。
3. 遍历 `final_output.main_content.分镜组列表[]`，按原顺序进入每个 `分镜明细[]`。
4. 读取 `场景及方位` 原文，先做空白和尾部标点清洗。
5. 保守拆分：
   - 优先锁定 `scene_name`
   - 其余部分回收到 `scene_variant`
   - 若无法稳定拆分，则整句保守收为 `scene_name`
   - 若为空，则记为 `unknown`
6. 生成 `group_scene_map[]`，至少回链：
   - `group_id`
   - `shot_id`
   - `scene_raw`
   - `scene_name`
   - `scene_variant`
7. 以 `scene_name` 为主键聚合 `scenes[]`，并整理每个场景的：
   - 首次出现
   - group / shot 覆盖范围
   - 变体列表
8. 写入单集 `第N集.json`；仅在显式要求时附带 `_manifest.json`。

## 场景拆分规则

1. 主场景优先：
   - `长廊西端入口朝东` -> `scene_name=长廊`，`scene_variant=西端入口朝东`
   - `寝室窗边` -> `scene_name=寝室`，`scene_variant=窗边`
2. 早切原则：
   - 在已知方位/门槛/边界词出现的最早位置切分。
3. 保守原则：
   - 若切分后主场景为空，则回退整句作为 `scene_name`。
4. 不越权原则：
   - 不把“看向 / 压迫感 / 冷色”之类氛围词提升为新场景。

## Handoff Rule

- 本子技能的消费单位是“当前集的场景清单”，不是研究稿也不是场景设计稿。
- 默认把产物交给 `4-Design/1-场景/2-设计` 继续消费。
- 本子技能本身不负责材质方案、构图设定或参考图生产。
