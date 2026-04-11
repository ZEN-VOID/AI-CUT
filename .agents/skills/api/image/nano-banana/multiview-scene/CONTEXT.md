---
context_health:
  status: ok
  chars: ~1500
  cases: 0
  soft_limit_chars: 40000
  hard_limit_chars: 80000
  soft_limit_cases: 80
  hard_limit_cases: 140
---

# CONTEXT: nano-banana-multiview-scene

## Type Map

| ID | 症状 | 根因层 | 即时修复 | 验证点 |
|----|------|--------|----------|--------|
| TM-MVS-HUMAN-LEAK | 九宫格中出现人物/人影 | 空镜头护栏约束被忽略 | 强化"不出现任何人物、人形剪影、生物或人影"措辞，必要时在提示词末尾追加负面约束 | 逐面板检查是否存在人形轮廓 |
| TM-MVS-LIGHT-INCONSIST | 不同面板光照方向不一致 | 光照连续性约束不够强 | 强化主光源共享描述，明确光源方位与强度 | 比对 P1 全景与其余面板的光影方向 |
| TM-MVS-LAYOUT-WRONG | 输出不是3x3九宫格 | 布局规格被忽略或模型未遵循 | 强化 SCENE_DESIGN_SHEET 约束，补充"严格9个面板"措辞 | 检查面板数量和布局是否为3行3列 |

## Repair Playbook

场景多视图输出异常时，按以下顺序排查：

1. 检查图片是否正确传入（路径存在、BASE64 编码成功）
2. 检查提示词模板注入是否完整（scene_id / scene_name / desc 三个占位符均已替换）
3. 确认 `--aspect-ratio "16:9"` 已传入
4. 若输出中出现人物，强化空镜头护栏措辞并重新生成
5. 若面板数量不对，检查是否遗漏了布局规格段落

## Reusable Heuristics

- 固定 `--aspect-ratio "16:9"`，九宫格标准画幅不可更改。
- 空镜头护栏是场景多视图的核心约束，区别于角色/道具多视图。
- 九宫格 P1-P9 各有明确拍摄角度要求，不可合并或省略。
- 默认 `--no-report`，仅输出图片。
- 第一张图为主参照图（"图一"），后续图为辅助参照。
- 输出命名递增防覆盖，永不覆盖原始文件。

## Case Log

（暂无案例记录）
