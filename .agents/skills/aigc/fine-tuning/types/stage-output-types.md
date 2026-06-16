# Stage Output Types

本类型包用于帮助 `$fine-tuning` 建立 `type_profile`。它不拥有调优方案、验收门或输出合同。

## Type Profiles

| type_id | signals | stage_hint | required_fields | route_back |
| --- | --- | --- | --- | --- |
| `aesthetic_protocol` | `类型风格.md`、`画面基调`、`风格协议`、`Global Style Prompt` | `2-美学` | project root or pasted protocol, source story anchors | `N2-SCHEME-MATCH` |
| `subject_asset` | `主体注册表.md`、`subject-registry.yaml`、角色/场景/道具清单、设计、生成请求 | `3-主体` | registry source, domain, subject id/name | `N2-SCHEME-MATCH` |
| `screenplay_text` | `4-编剧/第N集.md`、slugline、声画字段、对白、尾钩 | `4-编剧` | episode id, source prose or script path | `N2-SCHEME-MATCH` |
| `director_annotation` | `5-导演/第N集.md`、导演批注、镜头意图、调度 | `5-导演` | screenplay source and annotation text | `N2-SCHEME-MATCH` |
| `storyboard_split` | `6-分镜/第N集.md`、`分镜N（N-N秒）`、景别、景深、构图 | `6-分镜` | storyboard lines and source director/script | `N2-SCHEME-MATCH` |
| `camera_injection` | `7-摄影/第N集.md`、镜头角度、类型、速度、焦点 | `7-摄影` | storyboard source and camera lines | `N2-SCHEME-MATCH` |
| `grouping_output` | `8-分组/第N集.md`、分镜组、组级风格、YAML 主体统计 | `8-分组` | group ids, source camera text, subject registry | `N2-SCHEME-MATCH` |
| `image_stage_output` | 分镜画面、分镜故事板、平面图、imagegen plan、图像结果 | `9-图像` | route leaf, source group/shot id, image evidence if available | `N2-SCHEME-MATCH` |
| `canvas_stage_output` | LibTV、画布、imageList、video node、run id、final query | `10-画布` | source group id, canvas evidence, node ids | `N2-SCHEME-MATCH` |
| `review_finding` | review finding、审片 finding、验收未通过项 | owning stage from finding | target artifact, finding id, severity | `N2-SCHEME-MATCH` |
| `external_reference` | 网页、论文、作品、provider 文档、用户给的好坏样例 | reference only | source URL/file, relevance, boundary | `N3-SOURCE-REFERENCE-BUILD` |

## Conflict Policy

- 路径优先于自然语言关键词；例如 `projects/aigc/<项目名>/8-分组/` 优先判为 `grouping_output`。
- 叶子技能优先于父阶段；例如 `9-图像/分镜故事板` 不退回泛化 `9-图像`。
- review finding 必须追溯 owning stage，不把 review 本身当作业务 owner。
- external_reference 只作为参考资料类型，不可成为调优对象 owner。
