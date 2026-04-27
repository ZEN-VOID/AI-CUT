# Prompt Packet Contract

本文件拥有 planning 固定题包直答、创意缺口路由和下游 unknowns 切分合同。

## Fixed Direct-Answer Packet

`roles.planning.members` 必须围绕固定题包直接给出结构化判断，而不是模拟访谈或重新发起旧式问卷。

题包至少覆盖：

1. 项目名 / 工作名
2. 题材走廊与故事核
3. 读者承诺、平台与受众
4. 角色压力与世界约束
5. 应留给 `1-设定 / 2-卷章规划` 的 unknowns

## Answer Shape

每个 planning 成员输出应能被父流程聚合为 patch：

```yaml
member: ""
source_skill: ""
answers:
  project_contract_patch: {}
  cards_seed_patch: {}
  planning_seed_patch: {}
  unknowns: []
  risk_notes: []
```

## Creative Seed Routing

当固定题包暴露创意缺口时，才进入：

- `references/creative-seed-routing/module-spec.md`

该模块负责按需读取题材、反套路、市场定位、卖点或组合创意资料。父技能不得绕过模块入口直接点名 leaf docs。

## Unknowns Rule

- 当前最阻塞长期合同与阶段 seed 的缺口，可以由 planning 直答或创意 seed 补齐。
- 更适合 `1-设定` 对象建模的问题写入 `cards_seed` 或 `unknowns`。
- 更适合 `2-卷章规划` 卷章结构解决的问题写入 `planning_seed` 或 `unknowns`。
- 不允许为了显得初始化完整而补空字段、造默认剧情或压缩成单主文件。

## Provenance Rule

- 用户明确给出的字段记为 `user_confirmed`。
- 助手推断或 planning 直答补出的字段记为 `assistant_inferred` 或对应 `member_inferred`。
- legacy 工件只可记为 evidence，不可覆盖当前真源。
- `decision_owner=assistant` 时，未显式由用户确认的剩余非空字段不得默认归入 `user_confirmed`。
