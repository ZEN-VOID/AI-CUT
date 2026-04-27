# Comic Prompt Heuristics

本文件保存可复用经验和提示词启发式。它按需检索，不替代 `SKILL.md`、`references/`、`steps/` 或 `types/` 的强制合同。

## Prompt Assembly Pattern

页级 `positive_prompt` 推荐骨架：

```text
Vertical 9:16 comic page, [layout_id as natural language], [dominant panel + inset relationship], [reading path], [gutter/SFX/caption placement].
Global style anchor: [rendering medium], [line system], [shadow system], [color policy], [lettering/panel border feeling], [character age ratio], forbidden style shifts.
Character locked across all panels: [main character anchor].
Active recurring characters: [names + distinguishable appearance].
Scene locked across relevant pages: [scene anchor].
Place page number "[N]" in the bottom-right corner, digits only.
Keep character and scene consistency across all pages.
Panel 1: [shot + action + comic technique].
Panel 2: [shot + reaction/transition + comic technique].
Panel 3: [shot + reveal/hook + text slot placement].
Readable Chinese lettering: [speech/caption/SFX rule].
Avoid collage, contact sheet, duplicate composition, nine variations of the same scene.
```

## Style Families

| style_family | 可用提示词 | 最适合页面 | 使用注意 |
| --- | --- | --- | --- |
| 线条压迫 | `heavy black ink linework`, `bold contour lines`, `razor-sharp ink strokes`, `scratchy cross-hatching`, `thick silhouette edges` | 反派压迫、恐怖、命运宣告 | 和 `clean glossy anime` 同时出现会互相抵消 |
| 明暗冲击 | `deep chiaroscuro shadows`, `black gutter suspense`, `hard rim light`, `single bright highlight`, `crushed blacks and stark whites` | 揭示、审讯、绝境、恐怖 | 暗部过多时要指定 readable faces |
| 动作爆发 | `speed lines`, `focus lines`, `impact burst`, `motion trails across panels`, `kinetic diagonal composition`, `foreshortened action pose` | 战斗、坠落、追逐、觉醒 | 每页只让一个动作成为主爆点 |
| 画面变形 | `extreme low-angle perspective`, `wide-angle distortion`, `claustrophobic close-up crop`, `tilted Dutch angle panel`, `overlapping foreground silhouette` | 权力压迫、眩晕、失控 | 变形要服务情绪，不要让识别物漂移 |
| 印刷质感 | `screentone shadows`, `halftone texture`, `printed comic page grain`, `ben-day dot texture`, `rough paper ink texture` | 所有漫画页全局底色 | 作为统一风格锁，别写成单页主戏 |
| 文字冲击 | `oversized hand-lettered SFX`, `SFX breaking the panel border`, `jagged scream balloon`, `rectangular caption anchor`, `caption embedded in black gutter` | 爆炸、尖叫、钩子、旁白页 | SFX 绑定动作源；caption 绑定叙事压缩 |

## Layout Matrix

| layout_id | 页功能 | layout prompt |
| --- | --- | --- |
| `opening-hook-splash` | 第 1 页异常初现 | `vertical 9:16 comic page, one full-bleed opening splash occupying 70% of the page, two small bottom reaction insets, black gutters, final caption in the lower gutter` |
| `threat-low-angle-stack` | 压迫登场 | `three stacked panels: top extreme low-angle villain silhouette, middle narrow terrified eye close-up strip, bottom wide room panel with heavy black gutters` |
| `diagonal-impact-run` | 追逐/攻击 | `four irregular panels cut by one strong diagonal reading path, speed lines crossing gutters, final panel is a foreshortened impact pose with oversized SFX` |
| `splash-with-reaction-insets` | 爆点/觉醒 | `one dominant splash panel with the hero action, 2-3 overlapping reaction insets near the edge, SFX partly breaking the splash border` |
| `silent-beat-triptych` | 情绪停顿 | `three quiet narrow panels with minimal dialogue: hand detail, eye close-up, empty space, one small caption box anchoring the pause` |
| `evidence-ladder` | 推理/线索 | `zigzag evidence ladder: close-up clue panel, witness reaction inset, document strip, final dark room reveal, captions placed in gutters` |
| `vertical-fall-cascade` | 坠落/失控 | `tall vertical cascading panels, body motion trail moving downward through panel borders, narrow black gutters, bottom impact burst` |
| `border-breaking-cliffhanger` | 页末钩子 | `bottom cliffhanger close-up breaks out of the panel border into the black gutter, one short final caption, large negative space above` |

## Anti-Pattern Checklist

- 只写 `cinematic masterpiece`，没有 `panel / gutter / balloon / SFX / screentone`。
- 只写 layout 名称，不写 panel 比例、dominant panel 和阅读路径。
- 9 页都采用同一种上中下条带。
- 高冲击页没有大画面、inset 反应、SFX 或 focus lines。
- 解释页只有人物说话，没有证据 close-up、caption anchor 或静默反应格。
- 气泡远离说话角色；SFX 没有绑定动作源。
- 所有 panel 都塞满效果词，反而没有主次。
