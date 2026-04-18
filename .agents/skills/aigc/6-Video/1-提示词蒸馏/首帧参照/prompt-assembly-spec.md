# Prompt Assembly Spec

本文件是 `首帧参照` 的句法装配真源。

- `SKILL.md` 负责门禁、桥段提取原则、节点网、验收与返工入口。
- `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md` 负责跨兄弟叶子共享的 `图生视频` 句法总原则。
- 本文件负责单镜 specialization：组级桥接句、镜级 `P1/P2/P3` 句式槽、`tight/ultra` 压缩落点与可选字段挂句。
- `scripts/generate_episode_packets.py` 必须消费本文件中的 canonical JSON spec，不得再把句法字符串散落硬编码在函数体里。

## Scope

- 组级桥接句：
  - `类型元素`
  - `导演意图`
  - `出场角色及穿搭`
- 镜级句式槽：
  - `P1`：镜头起势 + 当前画面的动作与空间关系
  - `P2`：人物状态、环境、道具与光感
  - `P3`：构图组织与视觉强化
- 压缩预算：
  - `full`
  - `normal`
  - `tight`
  - `ultra`
- 可选字段挂句：
  - `转场特效`

## Image-to-Video Specialization

- 单镜模式优先把富余字数转成“当前首帧可见内容”的密度，而不是扩写抽象修辞。
- 句法顺序更偏 `图生视频`：先锁定人物识别与镜头起势，再写当前动作与空间，再落环境、光感与视觉强化。
- 内容来源保持当前设定：只重排和重写句法，不改变桥段来源与上游字段口径。

## Compression Contract

- `full`：默认 richest 档。在单镜任务里优先把富余字数转成镜头细节密度，尽量展开 `P1 + P2 + P3`。
- `normal`：保留全部 `P1`，适度合并 `P2`，把 `P3` 收束到一条句子。
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
    ]
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
        "template": "人物识别与服装锚点锁定{value}",
        "transform": "strip_tail_punct"
      }
    ]
  },
  "shot": {
    "opening_template": "分镜 {分镜ID} {time_range}",
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
            }
          ]
        },
        {
          "bucket": "P1",
          "parts": [
            {
              "field": "分镜构图",
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
            }
          ]
        },
        {
          "bucket": "P3",
          "parts": [
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
              "field": "分镜构图",
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
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
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
              "field": "分镜构图",
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
            },
            {
              "field": "镜头类型",
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
              "field": "分镜构图",
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
