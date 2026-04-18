# Prompt Assembly Spec

本文件是 `全能参照` 的句式装配真源。

- `SKILL.md` 负责门禁、优先级、验收与返工入口。
- `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md` 负责跨兄弟叶子共享的 `图生视频` 句法总原则。
- 本文件负责组级 specialization：组级桥接句、镜级句式槽、预算压缩落点与可选字段挂句。
- `scripts/generate_episode_packets.py` 必须消费本文件中的 canonical JSON spec，不得再把句法规则散落硬编码在函数体里。

## Scope

- 组级桥接句：
  - `类型元素`
  - `导演意图`
  - `出场角色及穿搭`
- 镜级句式槽：
  - `P1`：镜头起势 + 主体动作与空间关系
  - `P2`：表演、氛围、道具与光感
  - `P3`：构图组织与视觉强化
- 压缩预算：
  - `full`
  - `normal`
  - `tight`
  - `ultra`
- 可选字段挂句：
  - `转场特效`

## Image-to-Video Specialization

- 整体句法更偏 `图生视频` 的“主体锚点 -> 镜头起势 -> 可见动作 -> 环境与光感 -> 视觉组织”顺序。
- 内容来源保持当前设定：只重排和重写句法，不改动字段事实来源。
- 组级任务仍需覆盖整组全部分镜，但表层表达应更像模型指令，而不是字段表复述。

## Compression Contract

- `full`：尽量完整展开 `P1 + P2 + P3`，把主体动作、空间关系、环境与视觉组织都写清。
- `normal`：保留全部 `P1`，适度合并 `P2`，把 `P3` 收束为一条视觉组织句。
- `tight`：仍保留全部 `P1`，优先压缩 `P3`，再收束 `P2`。
- `ultra`：仅在 `tight` 仍超限时启用；允许删除部分 `P2 / P3`，但不得丢失 `P1`。
- `转场特效` 仅在上游非空时挂句；`ultra` 默认省略。

## Canonical JSON Spec

```json
{
  "version": "v2",
  "budgeting": {
    "levels": [
      "full",
      "normal",
      "tight",
      "ultra"
    ],
    "underflow_margin_chars": 260
  },
  "group_bridge": {
    "separator": "，",
    "parts": [
      {
        "field": "类型元素",
        "template": "整体保持{value}",
        "transform": "strip_tail_punct"
      },
      {
        "field": "导演意图",
        "template": "叙事重心落在{value}",
        "transform": "strip_tail_punct"
      },
      {
        "field": "出场角色及穿搭",
        "template": "人物识别与服装锚点保持{value}",
        "transform": "strip_tail_punct"
      }
    ]
  },
  "shot": {
    "opening_template": "分镜{分镜ID} {time_range}",
    "camera_sentence": {
      "separator": "，",
      "clauses": [
        {
          "field": "镜头类型兼容",
          "template": "{value}",
          "transform": "strip_tail_punct"
        },
        {
          "field": "景别",
          "templates": {
            "full": "画面从{value}起势",
            "normal": "画面从{value}起势",
            "tight": "{value}",
            "ultra": "{value}"
          },
          "transform": "strip_tail_punct"
        },
        {
          "field": "镜头视角",
          "templates": {
            "full": "以{value}观察",
            "normal": "以{value}观察",
            "tight": "{value}",
            "ultra": "{value}"
          },
          "transform": "strip_tail_punct"
        },
        {
          "field": "运镜手法",
          "templates": {
            "full": "镜头{value}",
            "normal": "镜头{value}",
            "tight": "{value}",
            "ultra": "{value}"
          },
          "transforms": {
            "full": "strip_tail_punct",
            "normal": "strip_tail_punct",
            "tight": "compact_clause",
            "ultra": "compact_clause"
          }
        },
        {
          "field": "镜头速度",
          "templates": {
            "full": "运动速度{value}",
            "normal": "运动速度{value}",
            "tight": "{value}",
            "ultra": "{value}"
          },
          "transforms": {
            "full": "strip_tail_punct",
            "normal": "strip_tail_punct",
            "tight": "compact_clause",
            "ultra": "compact_clause"
          }
        }
      ]
    },
    "detail_sentences": {
      "full": [
        {
          "bucket": "P1",
          "parts": [
            {
              "field": "运动表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
            {
              "field": "角色表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "道具及状态",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
            {
              "field": "摄影美学",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P3",
          "parts": [
            {
              "field": "分镜构图",
              "template": "画面组织为{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "视觉强化",
              "template": "视觉重心落在{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "镜头类型",
              "template": "整体按{value}推进",
              "transform": "strip_tail_punct"
            }
          ]
        }
      ],
      "normal": [
        {
          "bucket": "P1",
          "parts": [
            {
              "field": "运动表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
            {
              "field": "角色表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "道具及状态",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P2_P3",
          "parts": [
            {
              "field": "摄影美学",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "分镜构图",
              "template": "画面组织为{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "视觉强化",
              "template": "视觉重心落在{value}",
              "transform": "strip_tail_punct"
            }
          ],
          "fallback_parts": [
            {
              "field": "镜头类型",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        }
      ],
      "tight": [
        {
          "bucket": "P1",
          "parts": [
            {
              "field": "运动表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
            {
              "field": "角色表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "道具及状态",
              "template": "{value}",
              "transform": "strip_tail_punct"
            },
            {
              "field": "摄影美学",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        },
        {
          "bucket": "P3",
          "parts": [
            {
              "field": "视觉强化",
              "template": "{value}",
              "transform": "compact_clause"
            }
          ],
          "fallback_parts": [
            {
              "field": "镜头框架",
              "template": "{value}",
              "transform": "compact_clause"
            }
          ]
        }
      ],
      "ultra": [
        {
          "bucket": "P1",
          "parts": [
            {
              "field": "运动表现",
              "template": "{value}",
              "transform": "compact_clause"
            },
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "compact_clause"
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
            {
              "field": "角色表现",
              "template": "{value}",
              "transform": "compact_clause"
            }
          ],
          "fallback_parts": [
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "compact_clause"
            }
          ]
        }
      ]
    },
    "optional_hooks": [
      {
        "field": "转场特效",
        "levels": {
          "full": {
            "template": "镜间连续可按{value}处理",
            "transform": "strip_tail_punct"
          },
          "normal": {
            "template": "镜间连续可按{value}处理",
            "transform": "strip_tail_punct"
          },
          "tight": {
            "template": "衔接按{value}",
            "transform": "compact_clause"
          },
          "ultra": {
            "template": ""
          }
        }
      }
    ]
  }
}
```
