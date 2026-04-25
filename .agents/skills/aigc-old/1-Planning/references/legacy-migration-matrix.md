# Legacy Migration Matrix

本文件记录 2026-04-24 将原 `1-分集 / 2-格式 / 3-分组` 三个 Skill 包融合为 `.agents/skills/aigc/1-规划` 单一 Skill 2.0 包的迁移矩阵。

## Migration Matrix

| source_path | content_class | target_path | operation | semantic_risk | reference_updates | validation_gate |
| --- | --- | --- | --- | --- | --- | --- |
| `1-分集/SKILL.md` | 分集完整细则 | `references/episode-splitter-contract.md` | move + enhance | medium | 更新父 `SKILL.md` mode router | semantic check + `rg` |
| `1-分集/CONTEXT.md` | 分集经验层 | `knowledge-base/episode-splitter-heuristics.md` | move | low | 父 `CONTEXT.md` 回指 | context audit |
| `1-分集/templates/episode-split-plan.template.json` | 分集模板 | `templates/episode-split-plan.template.json` | move | low | 细则路径更新 | Skill 2.0 validator |
| `1-分集/agents/openai.yaml` | 旧入口元数据 | `references/legacy-episode-splitter-openai.yaml` | archive | low | 产品入口改为父 `agents/openai.yaml` | default prompt 检查 |
| `2-格式/SKILL.md` | 格式完整细则 | `references/script-format-contract.md` | move + enhance | medium | comic 参照链接改到 reference | semantic check + `rg` |
| `2-格式/CONTEXT.md` | 格式经验层 | `knowledge-base/script-format-heuristics.md` | move | low | 父 `CONTEXT.md` 回指 | context audit |
| `2-格式/scripts/validate_script_output.py` | 格式 validator | `scripts/validate_script_output.py` | move | low | 路径与审计脚本更新 | `python3 -m py_compile` |
| `2-格式/agents/openai.yaml` | 旧入口元数据 | `references/legacy-script-format-openai.yaml` | archive | low | 产品入口改为父 `agents/openai.yaml` | default prompt 检查 |
| `3-分组/SKILL.md` | 分组完整细则 | `references/grouping-contract.md` | move + enhance | medium | 父 `SKILL.md` mode router 更新 | semantic check + `rg` |
| `3-分组/CONTEXT.md` | 分组经验层 | `knowledge-base/grouping-heuristics.md` | move | low | 父 `CONTEXT.md` 回指 | context audit |
| `3-分组/references/scene-order-duration-strategy.md` | 分组专项方法论 | `references/scene-order-duration-strategy.md` | move | low | 内部路径更新 | reference check |
| `3-分组/scripts/grouping_quantizer.py` | 分组量化脚本 | `scripts/grouping_quantizer.py` | move | medium | postprocess/render/validator imports 保持同目录 | `python3 -m py_compile` |
| `3-分组/scripts/postprocess_grouping_output.py` | 分组 postprocess | `scripts/postprocess_grouping_output.py` | move | medium | `SCRIPT_DIR.parent` 继续指向父包根 | `python3 -m py_compile` |
| `3-分组/scripts/render_grouping_report.py` | 报告 renderer | `scripts/render_grouping_report.py` | move | medium | 模板路径随父包根解析 | `python3 -m py_compile` |
| `3-分组/scripts/validate_grouping_output.py` | 分组 validator | `scripts/validate_grouping_output.py` | move | medium | imports 保持同目录 | `python3 -m py_compile` |
| `3-分组/templates/grouping-output.template.md` | 分组输出模板 | `templates/grouping-output.template.md` | move | low | 细则路径更新 | Skill 2.0 validator |
| `3-分组/templates/grouping-report.template.md` | 分组报告模板 | `templates/grouping-report.template.md` | move | low | renderer 路径验证 | Skill 2.0 validator |
| `3-分组/skill_manifest.json` | 分组 manifest | `skill_manifest.json` | move + rewrite | medium | `skill_path` 与 script path 指向父包 | JSON parse + `rg` |
| `3-分组/agents/openai.yaml` | 旧入口元数据 | `references/legacy-grouping-openai.yaml` | archive | low | 产品入口改为父 `agents/openai.yaml` | default prompt 检查 |
| `_shared/IO_CONTRACT.md` | 规划共享 I/O | `references/planning-io-contract.md` | move + promote | medium | 父 `SKILL.md` 与三份 reference 改链 | semantic check + `rg` |

## Non-Loss Notes

- 旧三份 `SKILL.md` 的长细则没有删减，均以 reference 形式保留。
- 旧三份 `CONTEXT.md` 不再作为运行时 sibling context，但完整迁入 `knowledge-base/`，由父 `CONTEXT.md` 回指。
- 项目 runtime 子目录继续存在；本矩阵只迁移技能包入口与技能包内部资源。

## Remaining Watch Points

- 历史 `CHANGELOG.md` 与历史报告中可能保留旧路径作为证据路径；这些不是当前运行入口。
- 若未来审计需要完全消除历史文本中的旧路径，应先区分“历史证据”与“当前真源”。
