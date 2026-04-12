# Type Strategies

## Design Subject Strategy

| 输入状态 | 默认策略 | 说明 |
| --- | --- | --- |
| Markdown 存在且含 `prompt整合` | 直接抽取 | 首选，最贴近下游消费段 |
| Markdown 存在但无 `prompt整合` | JSON synthesis fallback | 保守回退，并记录来源 |
| Markdown 缺失 | JSON synthesis fallback | 不阻断，但 packet 必须显式标记 fallback |

## Role Tier Strategy

| role_tier | 面板策略 | 说明 |
| --- | --- | --- |
| `lead` | 单角色 dossier | 完整展示角色主体、服装与表情/动作 |
| `support` | 单角色 dossier | 可略缩减叙事气压，但 layout 完整 |
| `featured-crowd` | 单角色 dossier + crowd note | 保留辨识度，但不自动切群像 |
| `crowd` | `group_portrait=true` | 视为同阶层群像设计板，不做单人 turnaround |

## Reference Image Strategy

| 条件 | 动作 |
| --- | --- |
| 角色 Markdown 同目录存在图片 | 写入 `reference_images[]` |
| 只有显式 `--reference` | 按 CLI 顺序写入 `explicit_references[]` |
| 两者都没有 | 继续执行，但 `reference_images[]` 为空 |

## Conflict Tie-Break

1. `character_design.json` 的 canonical identity 优先。
2. 逐角色 Markdown 的 `prompt整合` 高于同文件其他段落。
3. 模板 layout 与 critical requirements 高于单次自由发挥。
4. 若 `prompt整合` 与 `character_design.json` 冲突，优先保守采信 JSON identity，同时保留 Markdown 作为主体文案。
