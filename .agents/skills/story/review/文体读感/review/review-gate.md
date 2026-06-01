# Review Gate

## Gate Mapping

| Review Question | Review Gate | Fail Code | Rework Target | Report Evidence |
| --- | --- | --- | --- | --- |
| 正文是否有能推动人物反应、信息揭示或关系压力的现场发现？ | scene texture gate | `FAIL-PS-02` | `3-场景和氛围渲染` | `scene_density_gaps`、缺失段落定位 |
| 句群是否过分平均、顺滑到像说明文？ | rhythm gate | `FAIL-PS-03` | `8-润色` | `sentence_rhythm_flattening` |
| 对白和心理是否仍是角色在现场说话/反应？ | voice and psychology gate | `FAIL-PS-03` | `5-对白优化` / `6-心理活动描写` | `emotion_telling_hits`、解释对白样本 |
| 是否存在 AI 腔、meta 腔、分镜腔或模板脸色反应？ | artifact gate | `FAIL-PS-04` | `8-润色` | `ai_formula_hits`、`meta_residue_hits` |

本维度不得直接改写正文，只输出 packet、问题证据和返工入口。
