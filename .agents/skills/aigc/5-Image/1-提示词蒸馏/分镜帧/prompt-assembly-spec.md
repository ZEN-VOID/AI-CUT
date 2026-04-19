# Prompt Assembly Spec

本文件是 `分镜帧` 的句法装配真源。

- `SKILL.md` 负责门禁、对象边界、写回与 handoff。
- `.agents/skills/aigc/5-Image/1-提示词蒸馏/_shared/prompt_bridge_helpers.py` 负责 `正文切分参考[] / 正文回指 / shot normalize` 的共享运行时桥接逻辑。
- 本文件负责单帧 specialization：固定英文前缀、组级设计块、镜级融写行与压缩级别。

## Composition Contract

- 最终 prompt 采用：`固定英文前缀 + 组级设计块 + 单镜融写行`
- 不保留独立 A 段整组 `剧本正文`
- 单镜融写行固定以 `xx秒-xx秒｜分镜<组内序号>：` 开头
- 完整四段式 `分镜ID` 只保留在结构化回链字段中
- 除镜级序号标签外，不暴露字段标题

## Canonical JSON Spec

```json
{
  "version": "v3",
  "char_limit": 2200,
  "prefix_lines": [
    "Create a single cinematic frame based on the following shot breakdown.",
    "Render only the specified shot moment as one full-frame image (no multi-panel layout).",
    "Do not add any text, subtitles, speech bubbles, or graphic overlays.",
    "Preserve the shot's composition, camera angle, subject positions, and atmosphere as the primary visual focus."
  ],
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
          "full": "画面以{value}起势",
          "normal": "画面以{value}起势",
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
      }
    ],
    "detail_sentences": {
      "full": [
        {
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
          "parts": [
            {
              "field": "视觉强化",
              "template": "视觉重心压在{value}",
              "transform": "strip_tail_punct"
            }
          ],
          "fallback_parts": [
            {
              "field": "镜头类型兼容",
              "template": "{value}",
              "transform": "strip_tail_punct"
            }
          ]
        }
      ],
      "normal": [
        {
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
        }
      ],
      "tight": [
        {
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
          "parts": [
            {
              "field": "氛围表现",
              "template": "{value}",
              "transform": "compact_clause"
            }
          ],
          "fallback_parts": [
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
          "parts": [
            {
              "field": "运动表现",
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
            "template": "",
            "transform": "compact_clause"
          }
        }
      }
    ]
  }
}
```
