# Type Map

| signal | mode | route |
| --- | --- | --- |
| `4-分组` + `6-图像/A-分镜画面`、四段式 `分镜ID@路径`、分镜画面多图参照 | `frame_reference` | `A-分镜画面参照/SKILL.md` |
| 故事板图、storyboard sheet、`6-图像/B-分镜故事板` | `storyboard_reference` | `B-分镜故事板参照/SKILL.md` |
| 角色、场景、道具主体，组底 YAML，Dreamina 分镜组批量 | `subject_reference` | `C-主体参照/SKILL.md` |
| submit_id、queue ledger、下载 | `query_or_download` | owning child + Dreamina CLI |
| 修复或审查 | `repair / review_only` | owning child or `review/review-contract.md` |
