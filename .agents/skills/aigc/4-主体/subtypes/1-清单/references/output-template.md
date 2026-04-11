# 1-清单输出契约

## 固定交付件

每轮 `1-清单` 至少应稳定交付：

1. 角色清单 JSON 与 `role_design_bridge.json`
2. 场景清单 JSON 与 `scene_design_bridge.json`
3. 道具清单 JSON 与 `prop_design_bridge.json`
4. `validation-report.md`
5. 指向 `2-设计` 的唯一下一入口

## 硬规则

1. 三类主体必须分域落盘，不得混成一份万能总表。
2. 每个域都必须有 bridge sidecar，不得只交名字列表。
3. 同名主体若承担不同功能，必须显式写变体或状态说明。
4. 证据不足时允许标记待补，不得臆造属性补齐。
