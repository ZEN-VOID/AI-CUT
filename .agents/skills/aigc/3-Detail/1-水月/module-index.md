# 模块总索引

## 作用

本文件是 `水月` 内部四条编号主链与叶子模块的总索引。

它回答三个问题：

1. 四条主链各自负责什么
2. 12 个叶子子模块各自补什么，不该补什么
3. 四条主链如何汇流成 `角色表现 / 运动表现 / 氛围表现 / 视觉强化`

## 四条主链

| 主链 | 叶子子模块 | 主职责 | 禁止越权 |
| --- | --- | --- | --- |
| `角色表现` | `内心戏 / 动作戏 / 对话戏` | 让人物可感、可演、可互动 | 不直接决定空间方位和镜头调度 |
| `运动表现` | `一致性 / 位置和方向 / 逻辑性` | 让动作路径、站位、因果和朝向成立 | 不替代角色内在动机 |
| `氛围表现` | `层次 / 意境 / 空间诗学` | 让场感、空气、景别层次和抒情密度成立 | 不悬空抒情，不脱离场景承载 |
| `视觉强化` | `冲击力 / 品味 / 观赏性` | 让画面有抓力、完成度和观看收益 | 不靠夸张辞藻制造假高级感 |

## 汇流顺序

1. 先锁组锚点。
2. 四条主链按当前序号串行生成本链 patch；后一条主链必须回读当前已部分写好的 root 与上一步 patch。
3. 先合成 `角色 + 运动`，确保人物与行动成立。
4. 再合成 `氛围 + 视觉`，确保场感和观看收益成立。
5. 最后先写：
   - `分镜明细[].角色表现`
   - `分镜明细[].运动表现`
   - `分镜明细[].氛围表现`
   - `分镜明细[].视觉强化`
6. 若旧下游仍需读取，再保守派生：
   - `group_design_patch.出场角色及穿搭`
   - `compatibility_projection.角色背景面`
   - `compatibility_projection.角色站位走位`
   - `compatibility_projection.道具及状态`
   - `compatibility_projection.分镜表现`

## 使用规则

- 每个叶子模块都只产出局部 patch、提醒或裁决，不产出主稿。
- 若两个模块都想写同一类信息，优先级固定为：
  - 人物行为归 `角色表现`
  - 方位与动作连续归 `运动表现`
  - 场域空气和景观层次归 `氛围表现`
  - 观看抓力和审美收束归 `视觉强化`
- `剧本正文` 是 inherited truth，不得在 `水月` 内重写。
- `水月` 只围绕固定 `剧本正文` 的组内窗口拆事实，不得写第二份 prose。
- `beat_id` 由父层统一规则约束：`<group_id>-bNN`。

## 配置真源规则

- `3-Detail` 共享节点包真源为：`.agents/skills/aigc/3-Detail/_shared/node-pack-contract.md`。
- `3-Detail` 共享创作引导真源为：`.agents/skills/aigc/3-Detail/_shared/creative-guidance-contract.md`。
- 当前技能包内的分类模块与叶子模块统一使用 package-local `module-spec.yaml` 作为执行配置真源。
- `module-guide.md` 是节点解释层，负责说明 why / anti-pattern / 审美尺度；不得改写 `module-spec.yaml` 的 schema。
- `module-spec.yaml` 至少要声明：`module_id / module_level / purpose / triggers / must_answer / patch_contract / merge_policy / quality_gates`。
- 每个 branch / leaf 目录都必须与 `module-spec.yaml` 配对一个 `module-guide.md`。
- 统一结构校验入口：`.agents/skills/aigc/3-Detail/scripts/validate_node_packs.py`
- `route-profile.yaml` 负责“哪类组重打哪条链”，`examples.md` 负责正反例，`creative-review-rubric.md` 负责创作验收。
- 创作引导校验入口：`.agents/skills/aigc/3-Detail/scripts/validate_creative_guidance.py`
- 允许 `module-index.md` 作为总索引存在，但不允许分类目录只靠 `README.md` 承载规范。

## Sidecar 汇流原则

- `水月` 的标准输出不是 prose，而是四个 branch-owned canonical 字段。
- 四条主链都必须服务同一件事：让父层能稳定写回 `角色表现 / 运动表现 / 氛围表现 / 视觉强化`。
- 旧字段只允许作为 compatibility projection 存在，不再反向定义 `水月` 真相。
- 未命中的字段不得补空洞默认值。
- 任何叶子若开始生成 `分镜ID / 时间段 / 景别 / 运镜手法 / 摄影美学`，视为越权。

## 叶子模块回链

- `1-角色表现/module-spec.yaml`
- `1-角色表现/内心戏/module-spec.yaml`
- `1-角色表现/动作戏/module-spec.yaml`
- `1-角色表现/对话戏/module-spec.yaml`
- `2-运动表现/module-spec.yaml`
- `2-运动表现/一致性/module-spec.yaml`
- `2-运动表现/位置和方向/module-spec.yaml`
- `2-运动表现/逻辑性/module-spec.yaml`
- `3-氛围表现/module-spec.yaml`
- `3-氛围表现/层次/module-spec.yaml`
- `3-氛围表现/意境/module-spec.yaml`
- `3-氛围表现/空间诗学/module-spec.yaml`
- `4-视觉强化/module-spec.yaml`
- `4-视觉强化/冲击力/module-spec.yaml`
- `4-视觉强化/品味/module-spec.yaml`
- `4-视觉强化/观赏性/module-spec.yaml`
