# Prompt Assembly Spec

本文件是 `首帧参照` 的句法装配真源。

- `SKILL.md` 负责门禁、桥段提取原则、节点网、验收与返工入口。
- `.agents/skills/aigc/6-Video/_shared/image-to-video-prompt-principles.md` 负责跨兄弟叶子共享的 `图生视频` 句法总原则。
- 本文件负责单镜 specialization：组级设计块、镜级融写句法、`tight/ultra` 压缩与可选挂句。
- `scripts/generate_episode_packets.py` 必须消费本文件中的 canonical JSON spec，不得再把句法字符串散落硬编码在函数体里。

## Scope

- 组级设计块：
  - `全局风格`
  - `类型元素`
  - `导演意图`
  - `出场角色及穿搭`
- 镜级融写行：
  - `正文回指 -> 正文切分参考[]`
  - `P1`：剧情桥段 + 主体动作/表演
  - `P2`：镜头控制
  - `P3`：环境、摄影与视觉重心
- 压缩预算：
  - `full`
  - `normal`
  - `tight`
  - `ultra`
- 可选字段挂句：
  - `转场特效`

## Composition Contract

- 最终 prompt 不再保留独立 A 段整组 `剧本正文`。
- 最终 prompt 固定采用 `BC` 结构：
  1. 组级设计块
  2. 单镜融写行
- 单镜融写行必须先融入 `正文回指` 指向的原剧本片段，再吸收当前镜头的动作、构图、运镜、氛围和摄影信息。
- 单镜融写行固定以 `xx秒-xx秒｜分镜<组内序号>：` 开头；完整四段式 `分镜ID` 只保留在结构化回链字段中。
- 除镜级序号标签外，不得泄露字段标题。

## Canonical JSON Spec

```json
{
  "version": "v3",
  "budgeting": {
    "levels": [
      "full",
      "normal",
      "tight",
      "ultra"
    ]
  },
  "group_design_block": {
    "separator": "；",
    "parts": [
      {
        "field": "全局风格",
        "template": "全局风格统一为{value}",
        "transform": "strip_tail_punct"
      },
      {
        "field": "类型元素",
        "template": "本组类型元素为{value}",
        "transform": "strip_tail_punct"
      },
      {
        "field": "导演意图",
        "template": "本组导演意图聚焦{value}",
        "transform": "strip_tail_punct"
      },
      {
        "field": "出场角色及穿搭",
        "template": "出场角色及穿搭为{value}",
        "transform": "strip_tail_punct"
      }
    ]
  },
  "shot": {
    "opening_template": "{time_range}｜分镜{shot_index}：",
    "script_bridge": {
      "field": "剧情桥段",
      "templates": {
        "full": "{value}",
        "normal": "{value}",
        "tight": "{value}",
        "ultra": "{value}"
      },
      "transforms": {
        "full": "strip_tail_punct",
        "normal": "strip_tail_punct",
        "tight": "strip_tail_punct",
        "ultra": "compact_clause"
      }
    },
    "camera_clauses": [
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
        "field": "分镜构图",
        "templates": {
          "full": "构图落成{value}",
          "normal": "构图落成{value}",
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
          "full": "速度保持{value}",
          "normal": "速度保持{value}",
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
        "field": "镜头类型兼容",
        "templates": {
          "full": "{value}",
          "normal": "{value}",
          "tight": "{value}",
          "ultra": ""
        },
        "transform": "strip_tail_punct"
      }
    ],
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
              "field": "摄影美学",
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
          "bucket": "P3",
          "parts": [
            {
              "field": "视觉强化",
              "template": "视觉重心压在{value}",
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
              "field": "道具及状态",
              "template": "{value}",
              "transform": "compact_clause"
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
              "transform": "compact_clause"
            },
            {
              "field": "角色表现",
              "template": "{value}",
              "transform": "compact_clause"
            }
          ]
        },
        {
          "bucket": "P2",
          "parts": [
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "compact_clause"
            },
            {
              "field": "摄影美学",
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
            "template": "镜间衔接按{value}处理",
            "transform": "strip_tail_punct"
          },
          "normal": {
            "template": "镜间衔接按{value}处理",
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
