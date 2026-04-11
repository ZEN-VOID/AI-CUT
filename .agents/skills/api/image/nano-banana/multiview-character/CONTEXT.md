---
context_health:
  status: ok
  chars: ~2000
  cases: 0
  last_compaction: null
---

## Type Map

| ID | 症状 | 根因 | 修复策略 | 验证点 |
|----|------|------|----------|--------|
| TM-MVC-LAYOUT-DRIFT | 输出不是三栏布局而是九宫格 | 提示词中布局约束被忽略 | 强化"must be CHARACTER_DESIGN_SHEET (3-column layout), not 3x3 nine-grid storyboard"措辞 | 检查输出布局是否为左15%+中50%+右35%三栏 |
| TM-MVC-IDENTITY-DRIFT | 不同视图间角色面部/体态不一致 | 身份锁定约束不够强 | 强化 identity lock 描述，增加"same face, hair, skin tone, body proportion across ALL views" | 比对正面/侧面/背面视图的角色一致性 |
| TM-MVC-STYLE-MIX | 不同模块风格不统一（如2D线稿混写实） | 缺少风格一致性约束 | 强化"one coherent style language across all modules"，明确"Rendering style should be inherited from the reference image" | 检查所有模块风格统一性 |

## Repair Playbook

多视图角色设计页故障排查顺序：

1. 检查图片是否正确传入（路径存在、格式支持）
2. 检查提示词模板注入是否正确（`<character_id>`/`<character_name>`/`<desc>` 均已替换）
3. 检查 `--aspect-ratio` 是否为 `16:9`（非 16:9 会导致布局崩坏）
4. 若布局错误（九宫格而非三栏），强化提示词中的布局约束措辞
5. 若身份漂移，检查参照图质量和 desc 描述精度

## Reusable Heuristics

- 固定 `16:9`，不从原图适配比例——三栏布局依赖横向画幅
- 第一张图为主参照（提示词中的"图一"），后续图为辅助参照
- 默认 `--no-report` 减少冗余产物
- 描述控制在 400 字以内，过长会稀释关键特征导致生成模型注意力分散
- 角色 ID badge 固定左上角，便于批量产物识别

## Case Log

（暂无案例记录）
