# 变量登记表

| var_id | 变量层级 | 观测信号 | 状态集合 | 检测方法 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| `V-SCN-DES-CATALOG` | 输入 | scene catalog 是否存在且可回链 | `ready/missing/broken` | 检查 `scenes[] / group_scene_map[]` | P0 |
| `V-SCN-DES-GLOBAL` | 输入 | `2-Global` 文档是否齐全 | `ready/partial/missing` | 检查 3 份上游文档 | P0 |
| `V-SCN-DES-EVIDENCE` | 证据 | 单场景是否需要补看镜头证据 | `enough/need-detail/conflicted` | 对比 scene entry 与 shots | P1 |
| `V-SCN-DES-PATCH` | 收束 | specialist patch 是否可聚合 | `clean/conflict/missing` | 检查字段重叠与空洞 | P0 |
| `V-SCN-DES-AUDIT` | 审计 | review / audit 是否通过 | `pass/rework/block` | 检查 note / report | P0 |

# 情况判定表

| case_id | 触发谓词 | 互斥关系 | 可并发关系 |
| --- | --- | --- | --- |
| `C-SCN-DES-CATALOG-MISS` | `V-SCN-DES-CATALOG in {missing,broken}` | 无 | 无 |
| `C-SCN-DES-GLOBAL-GAP` | `V-SCN-DES-GLOBAL in {partial,missing}` | 无 | 可并发全部 |
| `C-SCN-DES-EVIDENCE-DETAIL` | `V-SCN-DES-EVIDENCE=need-detail` | 无 | 可并发 `C-SCN-DES-GLOBAL-GAP` |
| `C-SCN-DES-PATCH-CONFLICT` | `V-SCN-DES-PATCH=conflict` | 无 | 可并发全部 |
| `C-SCN-DES-AUDIT-BLOCK` | `V-SCN-DES-AUDIT=block` | 无 | 无 |

# 策略映射矩阵

| case_id | strategy_id | 执行动作 | 质量门禁 | fallback |
| --- | --- | --- | --- | --- |
| `C-SCN-DES-CATALOG-MISS` | `S-SCN-DES-BACK-TO-CATALOG` | 停止设计，回到 `1-清单` | scene catalog 恢复 | 无 |
| `C-SCN-DES-GLOBAL-GAP` | `S-SCN-DES-GLOBAL-RELINK` | 先补全 `2-Global` 必需文档 | 3 份全局文档齐全 | 保守标注缺失 |
| `C-SCN-DES-EVIDENCE-DETAIL` | `S-SCN-DES-DETAIL-BACKLOOK` | 只回看命中镜头，不重扫全集 | 目标场景证据充分 | 记录待补证据 |
| `C-SCN-DES-PATCH-CONFLICT` | `S-SCN-DES-RECONCILE` | 由父 skill 按模板字段收束冲突 | 字段唯一归属 | 进入 `审景师` veto |
| `C-SCN-DES-AUDIT-BLOCK` | `S-SCN-DES-STOP-WRITEBACK` | 阻止写回并生成返工说明 | 审计项归零 | 无 |
